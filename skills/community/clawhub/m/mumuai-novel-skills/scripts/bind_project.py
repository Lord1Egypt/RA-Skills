import json
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
from client import MumuClient
import runtime_state

WIZARD_STAGES = {
    0: "world_building",
    1: "career_system",
    2: "characters",
    3: "outline",
}

LAST_COMPLETED_STAGE = {
    0: None,
    1: "world_building",
    2: "career_system",
    3: "characters",
    4: "outline",
}

WAIT_HINTS = {
    "career_system": (45, 3),
    "characters": (45, 4),
    "outline": (60, 3),
    "character_enrichment": (45, 2),
    "organization_enrichment": (60, 3),
    "external": (60, 3),
    "done": (0, 0),
}

SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
RUNTIME_STALE_SECONDS = int(os.getenv("MUMU_RUNTIME_STALE_SECONDS", "300"))


def build_outline_payload(project):
    payload = {
        "project_id": project["id"],
        "narrative_perspective": project.get("narrative_perspective") or "第三人称",
    }
    return payload


def infer_subphase(step_name, message=None):
    message = message or ""
    if "解析" in message:
        return "parsing"
    if "保存" in message:
        return "saving"
    if "校验角色" in message or "角色信息" in message:
        return "character_enrichment"
    if "校验组织" in message or "自动创建了" in message and "组织" in message:
        return "organization_enrichment"
    if "生成" in message:
        return "generating"
    if step_name:
        return "starting"
    return "pending"


def get_last_completed_stage(project):
    step = int(project.get("wizard_step") or 0)
    return LAST_COMPLETED_STAGE.get(step)


def get_eta_hint(phase, subphase):
    if phase == "completed" or subphase == "done":
        return WAIT_HINTS["done"]
    if subphase in WAIT_HINTS:
        return WAIT_HINTS[subphase]
    return WAIT_HINTS.get(phase, (45, 3))


def progress_message_from_state(progress_state):
    if not progress_state:
        return None
    return progress_state.get("last_message") or progress_state.get("message")


def build_advance_status(project, progress_state=None):
    phase = get_wizard_stage_label(project)
    if phase == "completed":
        subphase = "done"
        message = "Project initialization is complete."
        next_action = "done"
    else:
        subphase = "pending"
        message = f"Next initialization stage: {phase}."
        next_action = "advance"
        if progress_state:
            subphase = progress_state.get("subphase") or subphase
            message = progress_message_from_state(progress_state) or message
            if progress_state.get("status") == "external":
                message = f"Another agent ({progress_state.get('owner_id')}) is already advancing this project."

    recommended_wait_seconds, estimated_remaining_minutes = get_eta_hint(phase, subphase)
    return {
        "project_id": project.get("id"),
        "title": project.get("title"),
        "status": (progress_state or {}).get("status", "completed" if is_project_ready(project) else "running"),
        "ready": is_project_ready(project),
        "wizard_status": project.get("wizard_status"),
        "wizard_step": project.get("wizard_step"),
        "phase": phase,
        "subphase": subphase,
        "message": message,
        "last_completed_stage": get_last_completed_stage(project),
        "next_action": next_action,
        "recommended_wait_seconds": recommended_wait_seconds,
        "estimated_remaining_minutes": estimated_remaining_minutes,
    }


def build_runtime_payload(project, progress_state, status, pid=None, runner_id=None):
    return {
        "project_id": project.get("id"),
        "title": project.get("title"),
        "owner_id": runtime_state.get_owner_id(),
        "runner_id": runner_id or runtime_state.new_runner_id(),
        "status": status,
        "phase": get_wizard_stage_label(project),
        "subphase": (progress_state or {}).get("subphase", "pending"),
        "last_message": progress_message_from_state(progress_state),
        "last_progress": (progress_state or {}).get("progress"),
        "last_completed_stage": get_last_completed_stage(project),
        "next_action": "advance" if not is_project_ready(project) else "done",
        "pid": pid,
        "updated_at": time.time(),
    }


def load_runtime_snapshot(project_id):
    state = runtime_state.load_state(project_id)
    if not state:
        return None
    if state.get("owner_id") and state.get("owner_id") != runtime_state.get_owner_id():
        state["status"] = "external"
        return state
    if state.get("status") == "running" and runtime_state.is_stale(state, stale_after_seconds=RUNTIME_STALE_SECONDS):
        state["status"] = "stale"
    return state


def wait_for_runtime_snapshot(project_id, initial_updated_at=None, budget_seconds=0):
    deadline = time.monotonic() + max(0, budget_seconds)
    latest = load_runtime_snapshot(project_id)
    while time.monotonic() < deadline:
        latest = load_runtime_snapshot(project_id)
        if not latest:
            return None
        if latest.get("status") != "running":
            return latest
        if initial_updated_at is None:
            return latest
        if float(latest.get("updated_at") or 0) > float(initial_updated_at):
            return latest
        time.sleep(1)
    return latest


def get_wizard_stage_label(project):
    if is_project_ready(project):
        return "completed"
    step = int(project.get("wizard_step") or 0)
    return WIZARD_STAGES.get(step, "unknown")


def is_project_ready(project):
    status = (project.get("wizard_status") or "").lower()
    step = int(project.get("wizard_step") or 0)
    return status == "completed" and step >= 4


def get_next_wizard_action(project):
    if is_project_ready(project):
        return None

    step = int(project.get("wizard_step") or 0)
    if step <= 1:
        return "career-system"
    if step == 2:
        return "characters"
    if step in (2, 3):
        return "outline"
    return None


def build_status_payload(project, runtime_snapshot=None):
    payload = {
        "project_id": project.get("id"),
        "title": project.get("title"),
        "wizard_status": project.get("wizard_status"),
        "wizard_step": project.get("wizard_step"),
        "stage": get_wizard_stage_label(project),
        "ready": is_project_ready(project),
        "next_action": get_next_wizard_action(project),
        "recommended_command": "done" if is_project_ready(project) else "advance",
    }
    runtime_snapshot = runtime_snapshot or {}
    if runtime_snapshot:
        payload["runtime_status"] = runtime_snapshot.get("status")
        payload["runtime_phase"] = runtime_snapshot.get("phase")
        payload["runtime_subphase"] = runtime_snapshot.get("subphase")
        payload["runtime_message"] = progress_message_from_state(runtime_snapshot)
        payload["runtime_progress"] = runtime_snapshot.get("last_progress") or runtime_snapshot.get("progress")
    return payload


def emit_project_status(project, runtime_snapshot=None, json_mode=False):
    payload = build_status_payload(project, runtime_snapshot=runtime_snapshot)
    if json_mode:
        print(json.dumps(payload, ensure_ascii=False))
        return

    print("=== Project Status ===")
    for key, value in payload.items():
        print(f"{key}: {value}")
    print("======================")


def emit_advance_status(project, progress_state=None, json_mode=False):
    payload = build_advance_status(project, progress_state=progress_state)
    if json_mode:
        print(json.dumps(payload, ensure_ascii=False))
        return

    print("=== Advance Status ===")
    for key, value in payload.items():
        print(f"{key}: {value}")
    print("======================")


def wait_for_sse(resp, step_name, progress_callback=None):
    print(f"--- Running: {step_name} ---")
    final_result = None
    chunk_count = 0
    progress_state = {
        "step_name": step_name,
        "subphase": "starting",
        "message": f"Starting {step_name}...",
        "progress": 0,
    }
    if progress_callback:
        progress_callback(progress_state)
    try:
        for line in resp.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith("data: "):
                    try:
                        payload = json.loads(decoded[6:])
                        ptype = payload.get("type")
                        if ptype == "progress":
                            message = payload.get("message")
                            progress = payload.get("progress")
                            progress_state["message"] = message
                            progress_state["subphase"] = infer_subphase(step_name, message)
                            progress_state["progress"] = progress
                            progress_state["updated_at"] = time.time()
                            if progress_callback:
                                progress_callback(progress_state)
                            if message:
                                print(f"[{progress}%] {message}")
                        elif ptype == "chunk":
                            chunk_count += 1
                            progress_state["subphase"] = "generating"
                            progress_state["message"] = f"{step_name} is generating content."
                            progress_state["updated_at"] = time.time()
                            if progress_callback and chunk_count % 25 == 0:
                                progress_callback(progress_state)
                            if chunk_count % 100 == 0:
                                print(f"[stream] received {chunk_count} content chunks...")
                        elif ptype == "error":
                            print(f"❌ Error during {step_name}: {payload.get('error')}")
                            sys.exit(1)
                        elif ptype == "result":
                            final_result = payload.get("data")
                        elif ptype == "done":
                            progress_state["subphase"] = "done"
                            progress_state["message"] = f"{step_name} completed."
                            progress_state["progress"] = 100
                            progress_state["updated_at"] = time.time()
                            if progress_callback:
                                progress_callback(progress_state)
                            print(f"✅ Finished: {step_name}")
                    except json.JSONDecodeError:
                        pass
    finally:
        resp.close()
    return final_result, progress_state


def fetch_project(client, project_id):
    return client.get(f"projects/{project_id}")


def run_world_building_stage(client, args):
    data = {
        "title": args.title,
        "description": args.description,
        "theme": args.theme,
        "genre": args.genre,
        "narrative_perspective": "第三人称",
        "target_words": 1000000,
        "chapter_count": 5,
        "character_count": 5,
        "outline_mode": "one-to-many",
    }
    resp = client.post("wizard-stream/world-building", json_data=data, stream=True)
    result, progress_state = wait_for_sse(resp, "World Building")
    new_id = result.get("project_id") if result else None
    if not new_id:
        raise RuntimeError("Failed to get project_id from World Building")
    client.set_project_id(new_id)
    return fetch_project(client, new_id), progress_state


def run_next_stage(client, project, theme=None, genre=None, progress_callback=None):
    project_id = project["id"]
    next_action = get_next_wizard_action(project)
    if not next_action:
        return project, None

    if next_action == "career-system":
        resp = client.post("wizard-stream/career-system", json_data={"project_id": project_id}, stream=True)
        _, progress_state = wait_for_sse(resp, "Career System", progress_callback=progress_callback)
    elif next_action == "characters":
        resp = client.post(
            "wizard-stream/characters",
            json_data={
                "project_id": project_id,
                "count": 5,
                "theme": theme or project.get("theme"),
                "genre": genre or project.get("genre"),
            },
            stream=True,
        )
        _, progress_state = wait_for_sse(resp, "Characters", progress_callback=progress_callback)
    elif next_action == "outline":
        resp = client.post(
            "wizard-stream/outline",
            json_data=build_outline_payload(project),
            stream=True,
        )
        _, progress_state = wait_for_sse(resp, "Outline", progress_callback=progress_callback)
    else:
        raise RuntimeError(f"Unknown wizard action: {next_action}")

    return fetch_project(client, project_id), progress_state


def spawn_stage_runner(project_id, theme=None, genre=None):
    cmd = [
        sys.executable,
        str(SCRIPT_PATH),
        "--action",
        "_run-stage",
        "--project_id",
        project_id,
    ]
    if theme:
        cmd.extend(["--theme", theme])
    if genre:
        cmd.extend(["--genre", genre])
    proc = subprocess.Popen(
        cmd,
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env=os.environ.copy(),
    )
    return proc.pid


def run_stage_background(client, project_id, theme=None, genre=None):
    project = fetch_project(client, project_id)
    runtime = load_runtime_snapshot(project_id)
    if runtime and runtime.get("status") in {"running", "external"}:
        return project, runtime

    runner_id = runtime_state.new_runner_id()
    pid = spawn_stage_runner(project_id, theme=theme, genre=genre)
    runtime = runtime_state.save_state(
        project_id,
        build_runtime_payload(
            project,
            {
                "subphase": "starting",
                "message": f"Starting {get_wizard_stage_label(project)} in the background.",
                "progress": 0,
            },
            status="running",
            pid=pid,
            runner_id=runner_id,
        ),
    )
    return project, runtime


def execute_stage_runner(client, project_id, theme=None, genre=None):
    project = fetch_project(client, project_id)
    existing = runtime_state.load_state(project_id)
    runner_id = (existing or {}).get("runner_id") or runtime_state.new_runner_id()

    def persist(progress_state):
        runtime_state.save_state(
            project_id,
            build_runtime_payload(project, progress_state, status="running", pid=os.getpid(), runner_id=runner_id),
        )

    runtime_state.save_state(
        project_id,
        build_runtime_payload(
            project,
            {
                "subphase": "starting",
                "message": f"Starting {get_wizard_stage_label(project)}...",
                "progress": 0,
            },
            status="running",
            pid=os.getpid(),
            runner_id=runner_id,
        ),
    )

    try:
        updated_project, progress_state = run_next_stage(
            client,
            project,
            theme=theme,
            genre=genre,
            progress_callback=persist,
        )
        runtime_state.save_state(
            project_id,
            build_runtime_payload(updated_project, progress_state, status="completed", pid=os.getpid(), runner_id=runner_id),
        )
    except Exception as exc:
        runtime_state.save_state(
            project_id,
            build_runtime_payload(
                project,
                {
                    "subphase": "failed",
                    "message": str(exc),
                    "progress": 0,
                },
                status="failed",
                pid=os.getpid(),
                runner_id=runner_id,
            ),
        )
        raise

def main():
    parser = argparse.ArgumentParser(description="Bind or Create a Novel Project")
    parser.add_argument("--action", required=True, choices=["create", "status", "wait", "resume", "advance", "_run-stage", "ready", "list", "bind", "list-styles", "bind-style"], help="Action: manage projects or bind writing styles")
    parser.add_argument("--title", type=str, help="Title of the new novel (for create)")
    parser.add_argument("--description", type=str, help="Description/Synopsis of the novel (for create)")
    parser.add_argument("--theme", type=str, help="Theme of the novel (for create) e.g. 奋斗、复仇")
    parser.add_argument("--genre", type=str, help="Genre of the novel (for create) e.g. 科幻、修仙")
    parser.add_argument("--project_id", type=str, help="The project ID to bind (for bind)")
    parser.add_argument("--style_id", type=str, help="The writing style ID to bind (for bind-style)")
    parser.add_argument("--timeout", type=int, default=300, help="Maximum seconds to wait when using wait")
    parser.add_argument("--interval", type=int, default=5, help="Polling interval in seconds for wait")
    parser.add_argument("--budget-seconds", type=int, default=90, help="Advisory time budget for advance guidance")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON for status-style actions")
    
    args = parser.parse_args()
    client = MumuClient(project_id=getattr(args, 'project_id', None), style_id=getattr(args, 'style_id', None))
    
    if args.action == "create":
        if not args.title or not args.theme or not args.genre or not args.description:
            print("Error: --title, --description, --theme, and --genre are all required for create action.")
            return
        print(f"Creating a new project: {args.title} and starting the first initialization stage...")
        try:
            project, progress_state = run_world_building_stage(client, args)
            print(f"Project created with ID: {project.get('id')}")
            print("World building finished. Use `--action resume --project_id <ID>` to continue the next stage, or `--action status` to inspect progress.")
            if args.json:
                emit_advance_status(project, progress_state=progress_state, json_mode=True)
            else:
                emit_project_status(project, json_mode=False)
        except Exception as e:
            print(f"Failed to create project: {e}")

    elif args.action == "status":
        if not args.project_id:
            print("Error: --project_id is required for status action.")
            return
        try:
            project = fetch_project(client, args.project_id)
            runtime = load_runtime_snapshot(args.project_id)
            emit_project_status(project, runtime_snapshot=runtime, json_mode=args.json)
        except Exception as e:
            print(f"Failed to fetch project status: {e}")

    elif args.action == "wait":
        if not args.project_id:
            print("Error: --project_id is required for wait action.")
            return
        deadline = time.monotonic() + args.timeout
        try:
            while True:
                project = fetch_project(client, args.project_id)
                runtime = load_runtime_snapshot(args.project_id)
                if is_project_ready(project):
                    emit_project_status(project, runtime_snapshot=runtime, json_mode=args.json)
                    return
                if time.monotonic() >= deadline:
                    print(f"Initialization is still in progress after {args.timeout} seconds.")
                    if runtime:
                        emit_advance_status(project, progress_state=runtime, json_mode=args.json)
                    else:
                        emit_project_status(project, runtime_snapshot=runtime, json_mode=args.json)
                    return
                time.sleep(args.interval)
        except Exception as e:
            print(f"Failed while waiting for project readiness: {e}")

    elif args.action == "resume":
        if not args.project_id:
            print("Error: --project_id is required for resume action.")
            return
        try:
            project = fetch_project(client, args.project_id)
            if is_project_ready(project):
                print("Project initialization is already complete.")
                emit_project_status(project, json_mode=args.json)
                return
            print(f"Resuming initialization for project {args.project_id} from stage {get_wizard_stage_label(project)}...")
            project, progress_state = run_next_stage(client, project, theme=args.theme, genre=args.genre)
            if args.json:
                emit_advance_status(project, progress_state=progress_state, json_mode=True)
            else:
                emit_project_status(project, json_mode=False)
        except Exception as e:
            print(f"Failed to resume initialization: {e}")

    elif args.action == "advance":
        if not args.project_id:
            print("Error: --project_id is required for advance action.")
            return
        try:
            project, runtime = run_stage_background(client, args.project_id, theme=args.theme, genre=args.genre)
            if runtime and runtime.get("status") == "external":
                emit_advance_status(project, progress_state=runtime, json_mode=args.json)
                return
            runtime = wait_for_runtime_snapshot(
                args.project_id,
                initial_updated_at=runtime.get("updated_at") if runtime else None,
                budget_seconds=args.budget_seconds,
            ) or runtime
            project = fetch_project(client, args.project_id)
            if is_project_ready(project):
                runtime_state.clear_state(args.project_id)
                emit_advance_status(project, json_mode=args.json)
                return
            print(f"Advancing initialization for project {args.project_id} from stage {get_wizard_stage_label(project)}...")
            emit_advance_status(project, progress_state=runtime, json_mode=args.json)
        except Exception as e:
            print(f"Failed to advance initialization: {e}")

    elif args.action == "_run-stage":
        if not args.project_id:
            print("Error: --project_id is required for _run-stage action.")
            return
        execute_stage_runner(client, args.project_id, theme=args.theme, genre=args.genre)

    elif args.action == "ready":
        if not args.project_id:
            print("Error: --project_id is required for ready action.")
            return
        try:
            project = fetch_project(client, args.project_id)
            if args.json:
                print(json.dumps({"project_id": args.project_id, "ready": is_project_ready(project)}, ensure_ascii=False))
            else:
                print("READY" if is_project_ready(project) else "NOT_READY")
        except Exception as e:
            print(f"Failed to check project readiness: {e}")
            
    elif args.action == "list":
        print("Fetching your existing novel projects...")
        try:
            resp = client.get("projects", params={"limit": 20})
            print("=== Existing Projects ===")
            for item in resp.get("items", []):
                print(f"- ID: {item['id']} | Title: {item['title']} | Words: {item.get('current_words', 0)}")
            print("=========================")
            print("Use `--action bind --project_id <ID>` to pick one.")
        except Exception as e:
            print(f"Failed to list projects: {e}")

    elif args.action == "bind":
        if not args.project_id:
            print("Error: --project_id is required for bind action.")
            return
        client.set_project_id(args.project_id)
        print(f"Successfully bound this Agent to project {args.project_id}.")

    elif args.action == "list-styles":
        print("Fetching all available writing styles...")
        try:
            resp = client.get("writing-styles/presets/list")
            print("=== Available Styles ===")
            for item in resp:
                print(f"- ID: {item.get('id')} | Name: {item.get('name')} | Desc: {item.get('description', '')[:50]}")
            print("========================")
            print("Use `--action bind-style --style_id <ID>` to pick one.")
        except Exception as e:
            print(f"Failed to list styles: {e}")

    elif args.action == "bind-style":
        if not hasattr(args, 'style_id') or not args.style_id:
            print("Error: --style_id is required for bind-style action.")
            return
        client.set_style_id(args.style_id)
        print(f"Successfully bound writing style {args.style_id} to this Agent.")

if __name__ == "__main__":
    main()
