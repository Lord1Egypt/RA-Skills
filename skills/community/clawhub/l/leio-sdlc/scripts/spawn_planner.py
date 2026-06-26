import argparse
import tempfile
import os
import json
import sys
from agent_driver import invoke_agent, build_prompt
import subprocess
import uuid
import re

def main():
    parser = argparse.ArgumentParser(description="Spawn Planner Agent")
    parser.add_argument("--prd-file", required=True, help="Path to the PRD file")
    parser.add_argument("--run-dir", required=False, default=None, help="Absolute path to the isolated execution directory")
    parser.add_argument("--out-dir", required=False, default=None, help="Output directory for PRs")
    parser.add_argument("--workdir", required=True, help="Working directory lock")
    parser.add_argument("--slice-failed-pr", required=False, default=None, help="Path to a failed PR file to slice")
    parser.add_argument("--global-dir", required=False, help="Global directory for templates")
    RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
    args = parser.parse_args()

    workdir = os.path.abspath(args.workdir)
    os.chdir(workdir)

    if args.run_dir is not None:
        args.out_dir = args.run_dir
    elif args.out_dir is None:
        # Dynamically compute job directory from PRD filename
        prd_filename = os.path.basename(args.prd_file)
        base_name, _ = os.path.splitext(prd_filename)
        target_project_name = os.path.basename(os.path.abspath(args.workdir))
        global_dir = os.path.abspath(args.global_dir) if args.global_dir else os.path.abspath(args.workdir)
        args.out_dir = os.path.join(global_dir, ".sdlc_runs", target_project_name, base_name)

    os.makedirs(args.out_dir, exist_ok=True)

    if not (os.path.isfile(args.prd_file) and os.path.getsize(args.prd_file) > 0):
        print(f"[Pre-flight Failed] Planner cannot start. PRD file not found at '{args.prd_file}'. You must read or create the PRD first.")
        sys.exit(1)

    failed_pr_content = None
    failed_pr_id = None
    if args.slice_failed_pr is not None:
        if not (os.path.isfile(args.slice_failed_pr) and os.path.getsize(args.slice_failed_pr) > 0):
            print(f"[Pre-flight Failed] Planner cannot start. Failed PR file not found or empty at '{args.slice_failed_pr}'.")
            sys.exit(1)
        with open(args.slice_failed_pr, "r") as f:
            failed_pr_content = f.read()
            
        failed_pr_filename = os.path.basename(args.slice_failed_pr)
        match = re.match(r"^PR_(\d+(?:_\d+)*)_", failed_pr_filename)
        if match:
            failed_pr_id = match.group(1)
        else:
            print(f"[Warning] Could not extract failed PR ID from filename '{failed_pr_filename}'. Falling back to default append mode.")

    # Dynamic Toolchain Addressing
    SDLC_DIR = os.path.dirname(os.path.abspath(__file__))
    global_dir = os.path.abspath(args.global_dir) if args.global_dir else os.path.abspath(args.workdir)

    # Scaffolding: Ensure new project has standard guardrail and ignore files
    scaffold_files = {
        ".gitignore": ".gitignore",
        ".sdlc_guardrail": ".sdlc_guardrail",
        ".release_ignore": ".release_ignore"
    }
    for filename, source in scaffold_files.items():
        target_path = os.path.join(workdir, filename)
        if not os.path.exists(target_path):
            source_path = os.path.join(os.path.dirname(SDLC_DIR), source)
            if os.path.exists(source_path):
                import shutil
                shutil.copy(source_path, target_path)
                print(f"[Scaffold] Inherited {filename} from framework.")
            else:
                # Fallback if source is missing in framework root
                pass
    
    contract_script = os.path.join(SDLC_DIR, "create_pr_contract.py")

    try:
        with open(args.prd_file, "r") as f:
            prd_content = f.read()
    except FileNotFoundError:
        print(f"Error: PRD file not found: {args.prd_file}")
        sys.exit(1)
        
    try:
        SDLC_ROOT = os.path.dirname(RUNTIME_DIR)
        with open(os.path.join(SDLC_ROOT, "TEMPLATES", "PR_Contract.md.template"), "r") as tf:
            template_content = tf.read()
    except FileNotFoundError:
        template_content = "status: open\n\n# PR-[ID]: [Title]\n\n## 1. Objective\n\n## 2. Target Working Set & File Placement\n\n## 3. Implementation Scope\n\n## 4. TDD Blueprint & Acceptance Criteria\n"

    SDLC_ROOT = os.path.dirname(RUNTIME_DIR)
    playbook_path = os.path.join(SDLC_ROOT, "playbooks", "planner_playbook.md")
    playbook_content = ""
    if os.path.exists(playbook_path):
        with open(playbook_path, "r") as f:
            playbook_content = f.read()

    if args.slice_failed_pr is not None:
        insert_after_flag = f" --insert-after {failed_pr_id}" if failed_pr_id else ""
        task_string = build_prompt("planner_slice",
            workdir=workdir,
            playbook_content=playbook_content,
            failed_pr_content=failed_pr_content,
            prd_content=prd_content,
            contract_script=contract_script,
            out_dir=args.out_dir,
            insert_after_flag=insert_after_flag,
            template_content=template_content
        )
    else:
        task_string = build_prompt("planner",
            workdir=workdir,
            playbook_content=playbook_content,
            prd_content=prd_content,
            contract_script=contract_script,
            out_dir=args.out_dir,
            template_content=template_content
        )

    test_mode = os.environ.get("SDLC_TEST_MODE", "").lower() == "true"

    if test_mode:
        os.makedirs(os.path.join(args.run_dir or ".", "tests"), exist_ok=True)
        log_entry = str({'tool': 'spawn_planner', 'args': {'prd_file': args.prd_file, 'workdir': workdir, 'contract_script': contract_script, 'slice_failed_pr': args.slice_failed_pr}})
        with open(os.path.join(args.run_dir or ".", "tests", "tool_calls.log"), "a") as f:
            f.write(log_entry + "\\n")
        
        with open(os.path.join(args.run_dir or ".", "tests", "task_string.log"), "a") as f:
            f.write(task_string + "\\n")

        if args.slice_failed_pr is not None:
            with open(os.path.join(args.out_dir, "PR_Slice_1.md"), "w") as f:
                f.write("status: open\n\n# PR-001: Slice 1\n\n## 1. Objective\nMock Obj\n\n## 2. Target Working Set & File Placement\nMock Set\n\n## 3. Implementation Scope\nMock Scope\n\n## 4. TDD Blueprint & Acceptance Criteria\nMock TDD\n")
            with open(os.path.join(args.out_dir, "PR_Slice_2.md"), "w") as f:
                f.write("status: open\n\n# PR-002: Slice 2\n\n## 1. Objective\nMock Obj\n\n## 2. Target Working Set & File Placement\nMock Set\n\n## 3. Implementation Scope\nMock Scope\n\n## 4. TDD Blueprint & Acceptance Criteria\nMock TDD\n")
            print('{"status": "mock_success", "role": "planner", "action": "sliced"}')
        else:
            with open(os.path.join(args.out_dir, "PR_A.md"), "w") as f:
                f.write("status: open\n\n# PR-001: Feature A\n\n## 1. Objective\nMock Obj\n\n## 2. Target Working Set & File Placement\nMock Set\n\n## 3. Implementation Scope\nMock Scope\n\n## 4. TDD Blueprint & Acceptance Criteria\nMock TDD\n")
            with open(os.path.join(args.out_dir, "PR_B.md"), "w") as f:
                f.write("status: open\n\n# PR-002: Feature B\n\n## 1. Objective\nMock Obj\n\n## 2. Target Working Set & File Placement\nMock Set\n\n## 3. Implementation Scope\nMock Scope\n\n## 4. TDD Blueprint & Acceptance Criteria\nMock TDD\n")
            print('{"status": "mock_success", "role": "planner"}')
            
        sys.exit(0)
    else:
        import time
        print("Calling OpenClaw real API...")
        session_id = f"subtask-{uuid.uuid4().hex[:8]}"
        invoke_agent(task_string, session_key=session_id, role="planner")

if __name__ == "__main__":
    main()
