#!/usr/bin/env python3
import argparse
import os
import sys
from agent_driver import invoke_agent, build_prompt
import subprocess
import uuid

def main():
    parser = argparse.ArgumentParser(description="Spawn an arbitrator agent.")
    parser.add_argument("--pr-file", required=True, help="Path to the PR Contract file")
    parser.add_argument("--diff-target", required=True, help="Git diff target range (e.g., origin/master..HEAD)")
    parser.add_argument("--workdir", required=True, help="Working directory lock")
    parser.add_argument("--run-dir", default=".", help="Run directory for artifacts")
    
    args = parser.parse_args()
    workdir = os.path.abspath(args.workdir)
    os.chdir(workdir)

    # Check test mode
    if os.environ.get("SDLC_TEST_MODE") == "true":
        print("[CONFIRM_REJECT]")
        sys.exit(0)

    if not os.path.exists(args.pr_file):
        print(f"Error: PR file not found: {args.pr_file}")
        sys.exit(1)
        
    with open(args.pr_file, "r") as f:
        pr_content = f.read()
        
    diff_file = os.path.join(args.run_dir, "current_arbitration.diff")
    diff_cmd = f"git diff {args.diff_target} --no-color > {diff_file}"
    subprocess.run(diff_cmd, shell=True)

    task_string = build_prompt("arbitrator",
        workdir=workdir,
        pr_content=pr_content,
        diff_file=diff_file,
        review_report_path=os.path.join(args.run_dir, "review_report.json"), run_dir=args.run_dir
    )
    
    session_id = f"subtask-{uuid.uuid4().hex[:8]}"
    invoke_agent(task_string, session_key=session_id, role='arbitrator')

    report_path = os.path.join(args.run_dir, "arbitration_report.txt")
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            content = f.read()
        if "[OVERRIDE_LGTM]" in content:
            print("[OVERRIDE_LGTM]")
        elif "[CONFIRM_REJECT]" in content:
            print("[CONFIRM_REJECT]")
        else:
            print("[CONFIRM_REJECT]")
    else:
        print("[CONFIRM_REJECT]")

if __name__ == "__main__":
    main()
