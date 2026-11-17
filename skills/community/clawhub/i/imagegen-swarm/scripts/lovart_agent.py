"""Lovart Agent CLI.

HTTP calls live in lovart_client.py. The local project list lives in
lovart_state.py. This file is the command entry: python3 lovart_agent.py.
"""
import json

from lovart_client import AgentSkill, AgentSkillError
from lovart_commands import THREAD_REMOVE
from lovart_state import LocalState

def main():
    import argparse
    import os
    import sys

    # Read from env vars, fall back to CLI args
    env_base_url = os.environ.get("LOVART_BASE_URL", "https://lgw.lovart.ai")
    env_ak = os.environ.get("LOVART_ACCESS_KEY", "")
    env_sk = os.environ.get("LOVART_SECRET_KEY", "")

    parser = argparse.ArgumentParser(description="Lovart Agent OpenAPI Skill")
    parser.add_argument("--base-url", default=env_base_url)
    parser.add_argument("--ak", default=env_ak)
    parser.add_argument("--sk", default=env_sk)
    parser.add_argument("--timeout", type=int, default=180)
    sub = parser.add_subparsers(dest="command")

    # chat
    p = sub.add_parser("chat")
    p.add_argument("--prompt", required=True)
    p.add_argument("--project-id", default=None)
    p.add_argument("--thread-id", default=None, help="Reuse thread for context continuity")
    p.add_argument("--attachments", nargs="*", default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--download", action="store_true", help="Download artifacts to local files")
    p.add_argument("--output-dir", default="/tmp/lovart", help="Download output directory")
    p.add_argument("--prefer-models", default=None,
                   help='JSON: model preferences by category, e.g. \'{"IMAGE":["generate_image_midjourney"]}\'')
    p.add_argument("--include-tools", nargs="*", default=None,
                   help="Tools the Agent is told to prioritize, e.g. upscale_image. "
                        "Strong instruction, not an enforced whitelist.")
    p.add_argument("--exclude-tools", nargs="*", default=None,
                   help="Accepted for forward compatibility; currently has no effect "
                        "on tool selection. Use --include-tools to steer instead.")
    p.add_argument("--subjects", default=None,
                   help='JSON list of already-approved asset-library subjects to use as '
                        'references, e.g. \'[{"url":"LIBRARY_URL","asset_id":"asset_x",'
                        '"display_name":"Hero","channel":"ark_sd2"}]\'')
    p.add_argument("--kits", nargs="*", default=None,
                   help="Brand kit IDs. The project's active kit is attached automatically; "
                        "pass this only to reference a different kit.")
    p.add_argument("--mode", choices=["thinking", "fast"], default=None,
                   help="Reasoning mode: 'thinking' for deep structured reasoning, 'fast' for lightweight single-pass. Locked per thread.")

    # send (non-blocking: just send, return thread_id immediately)
    p = sub.add_parser("send")
    p.add_argument("--prompt", required=True)
    p.add_argument("--project-id", default=None)
    p.add_argument("--thread-id", default=None, help="Reuse thread for context continuity")
    p.add_argument("--attachments", nargs="*", default=None)
    p.add_argument("--mode", choices=["thinking", "fast"], default=None,
                   help="Reasoning mode: 'thinking' or 'fast'. Locked per thread.")

    # watch (stream partial results: send + incremental polling, emits NDJSON per completed artifact)
    p = sub.add_parser("watch", help="Send a prompt (or attach to existing thread) and stream artifacts as they complete")
    p.add_argument("--prompt", default=None, help="Prompt to send. If omitted, must provide --thread-id")
    p.add_argument("--project-id", default=None)
    p.add_argument("--thread-id", default=None, help="Attach to an existing running thread")
    p.add_argument("--attachments", nargs="*", default=None)
    p.add_argument("--output-dir", default="/tmp/lovart")
    p.add_argument("--interval", type=int, default=3, help="Poll interval in seconds")
    p.add_argument("--mode", choices=["thinking", "fast"], default=None,
                   help="Reasoning mode: 'thinking' or 'fast'. Locked per thread.")

    # create-project
    sub.add_parser("create-project")

    # upload-artifact
    p = sub.add_parser("upload-artifact")
    p.add_argument("--project-id", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--type", default="image", choices=["image", "video"])

    # upload (local file → server → OSS → returns CDN URL)
    p = sub.add_parser("upload")
    p.add_argument("--file", required=True, help="Local file path to upload")

    # confirm (confirms, polls until done, returns result)
    p = sub.add_parser("confirm")
    p.add_argument("--thread-id", required=True, help="Thread with pending high-cost operation")
    p.add_argument("--json", action="store_true")
    p.add_argument("--download", action="store_true", help="Download artifacts after completion")
    p.add_argument("--output-dir", default="/tmp/lovart")

    # set-mode
    p = sub.add_parser("set-mode")
    p.add_argument("--unlimited", action="store_true", help="Enable unlimited mode (queue, no credits)")
    p.add_argument("--fast", action="store_true", help="Enable fast mode (costs credits)")

    # query-mode
    sub.add_parser("query-mode")

    # status
    p = sub.add_parser("status")
    p.add_argument("--thread-id", required=True)

    # result
    p = sub.add_parser("result")
    p.add_argument("--thread-id", required=True)
    p.add_argument("--json", action="store_true")
    p.add_argument("--download", action="store_true", help="Download artifacts to local files")
    p.add_argument("--output-dir", default="/tmp/lovart")

    # download (standalone: download from URLs)
    p = sub.add_parser("download")
    p.add_argument("--urls", nargs="+", required=True, help="Artifact URLs to download")
    p.add_argument("--output-dir", default="/tmp/lovart")
    p.add_argument("--prefix", default="lovart")

    # config (local state management)
    p = sub.add_parser("config", help="View or update local state ($HOME/.lovart/state.json)")
    p.add_argument("--json", action="store_true")

    # project management
    p = sub.add_parser("projects", help="List all projects")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("project-add", help="Add and activate a project")
    p.add_argument("--project-id", required=True)
    p.add_argument("--name", default="", help="Friendly name for the project")

    p = sub.add_parser("project-switch", help="Switch active project")
    p.add_argument("--project-id", required=True, help="Full or prefix of project_id")

    p = sub.add_parser("project-rename", help="Rename a project")
    p.add_argument("--project-id", required=True)
    p.add_argument("--name", required=True)

    p = sub.add_parser("project-remove", help="Remove a project and its threads")
    p.add_argument("--project-id", required=True)

    # threads (list saved threads)
    p = sub.add_parser("threads", help="List saved thread history")
    p.add_argument("--project-id", default=None, help="Filter by project")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("thread-remove", help="Remove a thread from local history")
    p.add_argument("--thread-id", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    state = LocalState()

    # config, projects, and project-switch touch only the local state file.
    # project-add and project-rename also rename the remote project when keys are set.
    if args.command == "config":
        data = state.load()
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            active = data.get("active_project", "(not set)")
            projects = data.get("projects", {})
            name = projects.get(active, {}).get("name", "") if active != "(not set)" else ""
            print(f"active project: {active}" + (f" ({name})" if name else ""))
            print(f"projects: {len(projects)}")
            print(f"threads: {len(data.get('threads', []))}")
            print(f"state file: {state.path}")
        sys.exit(0)

    if args.command == "projects":
        projects = state.get_projects()
        active = state.get_project_id()
        if args.json:
            print(json.dumps({"active": active, "projects": projects}, indent=2, ensure_ascii=False))
        else:
            if not projects:
                print("No projects. Use: project-add --project-id PID --name NAME")
            else:
                for pid, info in projects.items():
                    marker = " *" if pid == active else "  "
                    name = info.get("name", "")
                    threads = len(state.get_threads(pid))
                    print(f"{marker} {pid[:12]}... {name:20s} ({threads} threads)")
        sys.exit(0)

    if args.command == "project-add":
        state.add_project(args.project_id, args.name)
        # Sync name to server if AK/SK available and name provided
        if args.name and args.ak and args.sk:
            try:
                s = AgentSkill(base_url=args.base_url, access_key=args.ak, secret_key=args.sk)
                s.rename_project(args.project_id, args.name)
            except Exception:
                pass
        print(f"Added and switched to project: {args.project_id}" + (f" ({args.name})" if args.name else ""))
        sys.exit(0)

    if args.command == "project-switch":
        if state.switch_project(args.project_id):
            full_id = state.get_project_id()
            name = state.get_projects().get(full_id, {}).get("name", "")
            print(f"Switched to: {full_id}" + (f" ({name})" if name else ""))
        else:
            print(f"Error: project '{args.project_id}' not found", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    if args.command == "project-rename":
        state.rename_project(args.project_id, args.name)
        if args.ak and args.sk:
            try:
                s = AgentSkill(base_url=args.base_url, access_key=args.ak, secret_key=args.sk)
                s.rename_project(args.project_id, args.name)
            except Exception:
                pass
        print(f"Renamed: {args.project_id} → {args.name}")
        sys.exit(0)

    if args.command == "project-remove":
        state.remove_project(args.project_id)
        print(f"Removed project: {args.project_id}")
        sys.exit(0)

    if args.command == "threads":
        pid = getattr(args, "project_id", None)
        if getattr(args, "all", False):
            threads = state.get_threads()
        else:
            threads = state.get_threads(pid or state.get_project_id())
        if args.json:
            print(json.dumps(threads, indent=2, ensure_ascii=False))
        else:
            if not threads:
                print("No saved threads.")
            else:
                for i, t in enumerate(threads):
                    pid_short = t.get("project_id", "")[:8]
                    print(f"  {i+1}. [{t['id'][:8]}...] [{pid_short}] {t.get('topic', '(no topic)')}  ({t.get('updated_at', '')})")
        sys.exit(0)

    if args.command == THREAD_REMOVE:
        state.remove_thread(args.thread_id)
        print("Removed thread: " + str(args.thread_id))
        sys.exit(0)

    if not args.ak or not args.sk:
        print("Error: LOVART_ACCESS_KEY and LOVART_SECRET_KEY must be set "
              "(via env vars or --ak/--sk)", file=sys.stderr)
        sys.exit(1)

    skill = AgentSkill(base_url=args.base_url, access_key=args.ak,
                       secret_key=args.sk, timeout=args.timeout)

    try:
        if args.command == "chat":
            # Auto-fill project_id from local state if not provided
            project_id = args.project_id or state.get_project_id()

            prefer_models = json.loads(args.prefer_models) if args.prefer_models else None
            subjects = json.loads(args.subjects) if args.subjects else None
            result = skill.chat(prompt=args.prompt, project_id=project_id,
                                attachments=args.attachments, thread_id=args.thread_id,
                                prefer_models=prefer_models,
                                include_tools=args.include_tools,
                                exclude_tools=args.exclude_tools,
                                mode=args.mode,
                                subjects=subjects, kits=args.kits)

            # Auto-save state
            if result.get("project_id"):
                name = result.get("project_name", args.prompt[:30].strip())
                state.add_project(result["project_id"], name)
            if result.get("thread_id"):
                topic = args.prompt[:50].strip()
                state.upsert_thread(result["thread_id"], topic)
            # Auto-download if requested
            if args.download:
                dl = skill.download_artifacts(result, output_dir=args.output_dir)
                result["downloaded"] = dl

            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Status: {result['final_status']}")
                print(f"Thread: {result['thread_id']}")
                print(f"Project: {result.get('project_id', 'N/A')}")
                for item in result.get("items", []):
                    if item.get("text"):
                        print(f"\n[{item['type']}] {item['text']}")
                    for a in item.get("artifacts", []):
                        print(f"  [{a['type']}] {a['content']}")
                for dl in result.get("downloaded", []):
                    if dl.get("local_path"):
                        print(f"  -> {dl['local_path']}")

        elif args.command == "send":
            project_id = args.project_id or state.get_project_id()
            if not project_id:
                project_id = skill.create_project()
            tid = skill.send(prompt=args.prompt, project_id=project_id,
                             attachments=args.attachments, thread_id=args.thread_id,
                             mode=args.mode)
            state.add_project(project_id, args.prompt[:30].strip())
            state.upsert_thread(tid, args.prompt[:50].strip())
            print(json.dumps({"thread_id": tid, "project_id": project_id}))

        elif args.command == "watch":
            if not args.thread_id and not args.prompt:
                print("Error: watch requires either --thread-id or --prompt", file=sys.stderr)
                sys.exit(1)

            # Either send a new prompt or attach to an existing thread
            if args.thread_id:
                tid = args.thread_id
                project_id = args.project_id or state.get_project_id()
            else:
                project_id = args.project_id or state.get_project_id()
                if not project_id:
                    project_id = skill.create_project()
                tid = skill.send(prompt=args.prompt, project_id=project_id,
                                 attachments=args.attachments, mode=args.mode)
                state.add_project(project_id, args.prompt[:30].strip())
                state.upsert_thread(tid, args.prompt[:50].strip())

            # Emit initial event
            print(json.dumps({"event": "started", "thread_id": tid, "project_id": project_id}, ensure_ascii=False), flush=True)

            # Stream: poll status + result, download new artifacts each round, emit NDJSON
            seen_urls = set()
            deadline = time.time() + skill.timeout
            final_status = "timeout"
            while time.time() < deadline:
                try:
                    status_info = skill.get_status(tid)
                    status = status_info.get("status", "running")
                    result = skill.get_result(tid)
                    dl = skill.download_artifacts(result, output_dir=args.output_dir)
                    for d in dl:
                        if d.get("url") in seen_urls or not d.get("new"):
                            if d.get("url") not in seen_urls and d.get("local_path"):
                                # Already on disk from previous run — still emit once
                                seen_urls.add(d["url"])
                                print(json.dumps({"event": "artifact", "type": d["type"], "url": d["url"], "local_path": d.get("local_path")}, ensure_ascii=False), flush=True)
                            continue
                        seen_urls.add(d["url"])
                        print(json.dumps({"event": "artifact", "type": d["type"], "url": d["url"], "local_path": d.get("local_path")}, ensure_ascii=False), flush=True)
                    pc = result.get("pending_confirmation")
                    if pc:
                        final_status = "pending_confirmation"
                        print(json.dumps({"event": "pending_confirmation", "thread_id": tid, "pending_confirmation": pc}, ensure_ascii=False), flush=True)
                        break
                    if status == "abort":
                        final_status = "abort"
                        break
                    if status == "done":
                        final_status = "done"
                        break
                except AgentSkillError as e:
                    print(json.dumps({"event": "error", "message": e.message}, ensure_ascii=False), flush=True)
                time.sleep(args.interval)

            print(json.dumps({"event": "finished", "thread_id": tid, "final_status": final_status, "artifact_count": len(seen_urls)}, ensure_ascii=False), flush=True)

        elif args.command == "confirm":
            skill.confirm(args.thread_id)
            # Poll until done after confirmation
            status = skill.poll(args.thread_id)
            result = skill.get_result(args.thread_id)
            result["final_status"] = status
            if args.download:
                dl = skill.download_artifacts(result, output_dir=args.output_dir)
                result["downloaded"] = dl
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Status: {status}")
                print(f"Thread: {args.thread_id}")
                for item in result.get("items", []):
                    if item.get("text"):
                        print(f"\n[{item['type']}] {item['text']}")
                    for a in item.get("artifacts", []):
                        print(f"  [{a['type']}] {a['content']}")
                for dl in result.get("downloaded", []):
                    if dl.get("local_path"):
                        print(f"  -> {dl['local_path']}")

        elif args.command == "set-mode":
            if args.fast:
                r = skill.set_mode(unlimited=False)
                print(json.dumps({"mode": "fast", "detail": r}, ensure_ascii=False))
            elif args.unlimited:
                r = skill.set_mode(unlimited=True)
                print(json.dumps({"mode": "unlimited", "detail": r}, ensure_ascii=False))
            else:
                print("Error: specify --fast or --unlimited", file=sys.stderr)
                sys.exit(1)

        elif args.command == "query-mode":
            r = skill.query_mode()
            mode = "unlimited" if r.get("unlimited") else "fast"
            print(json.dumps({"mode": mode, "detail": r}, indent=2, ensure_ascii=False))

        elif args.command == "create-project":
            pid = skill.create_project()
            state.add_project(pid)
            print(json.dumps({"project_id": pid}))

        elif args.command == "upload":
            url = skill.upload_file(args.file)
            print(json.dumps({"url": url}))

        elif args.command == "upload-artifact":
            r = skill.upload_artifact(args.project_id, args.url, args.type)
            print(json.dumps(r, indent=2, ensure_ascii=False))

        elif args.command == "status":
            print(json.dumps(skill.get_status(args.thread_id), indent=2))

        elif args.command == "result":
            r = skill.get_result(args.thread_id)
            if args.download:
                dl = skill.download_artifacts(r, output_dir=args.output_dir)
                r["downloaded"] = dl
            print(json.dumps(r, indent=2, ensure_ascii=False))

        elif args.command == "download":
            # Download from explicit URLs
            fake_result = {"items": [{"artifacts": [{"type": "image", "content": u} for u in args.urls]}]}
            dl = skill.download_artifacts(fake_result, output_dir=args.output_dir, prefix=args.prefix)
            print(json.dumps({"downloaded": dl, "output_dir": args.output_dir}, indent=2, ensure_ascii=False))

    except AgentSkillError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
