#!/usr/bin/env python3
import argparse
import os
import sys
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
import agent_driver
from agent_driver import invoke_agent, build_prompt

def main():
    parser = argparse.ArgumentParser(description="Spawn a UAT Verifier agent.")
    parser.add_argument("--prd-files", required=True, help="Comma-separated paths to PRDs")
    parser.add_argument("--workdir", required=True, help="Working directory lock")
    parser.add_argument("--out-file", default="uat_report.json", help="Path to output JSON")
    parser.add_argument("--enable-exec-from-workspace", action="store_true", help="Bypass the workspace path check")
    
    args = parser.parse_args()
    
    if "/root/.openclaw/workspace/projects/" in os.path.abspath(__file__):
        if not args.enable_exec_from_workspace:
            if "--enable-exec-from-workspace" not in sys.argv:
                print("[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nStartup validation failed (likely executing from the wrong directory). You MUST execute the script using its absolute installed path (e.g., `python3 ~/.openclaw/skills/leio-sdlc/scripts/spawn_verifier.py ...`) OR explicitly append the `--enable-exec-from-workspace` flag if testing locally.")
                sys.exit(1)

    workdir = os.path.abspath(args.workdir)
    os.chdir(workdir)

    SDLC_ROOT = os.path.dirname(current_dir)
    playbook_path = os.path.join(SDLC_ROOT, "playbooks", "verifier_playbook.md")

    task_string = build_prompt("verifier",
        workdir=workdir,
        playbook_path=playbook_path,
        prd_files=args.prd_files,
        out_file=os.path.abspath(args.out_file)
    )

    test_mode = os.environ.get("SDLC_TEST_MODE", "").lower() == "true"
    if test_mode:
        import json
        run_dir = os.environ.get("SDLC_RUN_DIR", ".")
        os.makedirs(os.path.join(run_dir, "tests"), exist_ok=True)
        with open(os.path.join(run_dir, "tests", "verifier_task_string.log"), "w") as f:
            f.write(task_string)
            
        mock_result = os.environ.get("MOCK_VERIFIER_RESULT", '{"status": "PASS", "executive_summary": "Mock passed", "verification_details": []}')
        with open(os.path.abspath(args.out_file), "w") as f:
            f.write(mock_result)
        print(f"Mock UAT Verifier completed successfully. Report written to {args.out_file}")
    else:
        print(f"🚀 Launching Agentic UAT Verifier...")
        session_id = f"uat_verifier_{int(time.time())}"
        # The verifier agent is instructed in the prompt to use the 'write' tool to save the JSON directly.
        invoke_agent(task_string, session_key=session_id, role="verifier")
        
        # Verify that the output file was actually created by the agent
        if not os.path.exists(os.path.abspath(args.out_file)):
            print(f"Error: Verifier agent failed to produce {args.out_file}", file=sys.stderr)
            sys.exit(1)

        print(f"UAT Verifier completed successfully. Report written to {args.out_file}")

if __name__ == "__main__":
    main()
