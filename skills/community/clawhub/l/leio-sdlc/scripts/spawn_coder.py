import re
#!/usr/bin/env python3
import argparse
import tempfile
import os
import sys
from agent_driver import build_prompt
import subprocess
import time
from pathlib import Path
def extract_pr_id(pr_file_path):
    basename = os.path.basename(pr_file_path)
    # Match PR prefix followed by digits and underscores (e.g. PR_003_1)
    match = re.search(r'^(PR_[\d_]+)', basename, re.IGNORECASE)
    if match:
        return match.group(1).rstrip('_')
    return basename.split(".")[0]
def openclaw_agent_call(session_key, message, workdir='.'):
    cmd = [
        "openclaw",
        "agent",
        "--local",
        "--session-id",
        session_key,
        "--message",
        message
    ]
    try:
        subprocess.run(cmd, cwd=workdir, check=True)
        return session_key
    except subprocess.CalledProcessError as e:
        print(f"Error calling openclaw agent: {e}")
        sys.exit(1)

def send_feedback(session_key, message, workdir='.'):
    """Function to append reviewer feedback to the existing session."""
    openclaw_agent_call(session_key, message, workdir=workdir)
    print(f"Sent feedback to session {session_key}")
def handle_feedback_routing(workdir, feedback_file, task_string, pr_id, run_dir="."):
    session_file = os.path.join(run_dir, ".coder_session")
    try:
        import json
        with open(feedback_file, "r") as f:
            feedback_content = f.read()
            
        try:
            # Try to extract pure JSON from the file, as it might be wrapped in markdown
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', feedback_content, re.DOTALL)
            if json_match:
                feedback_content = json_match.group(1).strip()
            else:
                json_match = re.search(r'(\{.*?\})', feedback_content, re.DOTALL)
                if json_match:
                    feedback_content = json_match.group(1).strip()
                    
            # Ensure it's valid JSON, then dump it raw
            json_obj = json.loads(feedback_content)
            feedback_content = json.dumps(json_obj, indent=2)
        except Exception:
            pass # Fall back to raw string if parsing fails
            
        msg = build_prompt("coder_revision", feedback_content=feedback_content)
        
        if os.path.exists(session_file):
            with open(session_file, "r") as sf:
                session_key = sf.read().strip()
            send_feedback(session_key, msg, workdir=workdir)
            return True, session_key
        else:
            import uuid
            session_key = f"sdlc_coder_{pr_id}_{uuid.uuid4().hex[:8]}"
            task_string += msg
            openclaw_agent_call(session_key, task_string, workdir=workdir)
            with open(session_file, "w") as f:
                f.write(session_key)
            print(f"Spawned new session {session_key} with feedback")
            return False, session_key
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
def main():
    parser = argparse.ArgumentParser(description="Spawn a coder subagent")
    parser.add_argument("--pr-file", required=True, help="Path to the PR Contract file")
    parser.add_argument("--prd-file", required=True, help="Path to the PRD file")
    parser.add_argument("--feedback-file", required=False, help="Path to the Review Report / Feedback file")
    parser.add_argument("--system-alert", required=False, help="System alert string (e.g. git status)")
    parser.add_argument("--workdir", required=True, help="Working directory lock")
    parser.add_argument("--global-dir", required=False, help="Global directory for playbooks")
    parser.add_argument("--run-dir", default=".", help="Run directory for artifacts")
    RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
    args = parser.parse_args()
    workdir = os.path.abspath(args.workdir)
    os.chdir(workdir)
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL, text=True).strip()
        if branch in ["master", "main"]:
            print("[FATAL] Branch Isolation Guardrail: Coder agent cannot be spawned on the 'master' or 'main' branch.", file=sys.stderr)
            print("[ACTION REQUIRED]: You must create and checkout a new feature branch before assigning work to the Coder.", file=sys.stderr)
            print("Fix this by executing: git checkout -b feature/<pr_name>", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError:
        pass
    if not os.path.exists(args.pr_file):
        print(f"[Pre-flight Failed] Coder cannot start. PR Contract not found at '{args.pr_file}'. You must run spawn_planner.py first.")
        sys.exit(1)
    pr_id = extract_pr_id(args.pr_file)
    test_mode = os.environ.get("SDLC_TEST_MODE") == "true"
    if test_mode:
        log_entry = str({'tool': 'spawn_coder', 'args': {'pr_file': args.pr_file, 'prd_file': args.prd_file, 'feedback_file': args.feedback_file, 'workdir': workdir}})
        
        # Ensure tests dir exists
        Path("tests").mkdir(exist_ok=True)
        
        with open("tests/tool_calls.log", "a") as f:
            f.write(log_entry + "\n")
        
        print('{"status": "mock_success", "role": "coder", "sessionKey": "mock-session-key"}')
        sys.exit(0)
    else:
        try:
            with open(args.pr_file, "r") as f:
                pr_content = f.read()
            with open(args.prd_file, "r") as f:
                prd_content = f.read()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)
            
        # Inject Coder Playbook (PRD_1005)
        RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
        SDLC_ROOT = os.path.dirname(RUNTIME_DIR)
        playbook_path = os.path.join(SDLC_ROOT, "playbooks", "coder_playbook.md")
        playbook_content = ""
        if os.path.exists(playbook_path):
            with open(playbook_path, "r") as f:
                playbook_content = f.read()
        
        task_string = build_prompt("coder", 
            workdir=workdir, 
            playbook_content=playbook_content, 
            pr_file=args.pr_file, 
            pr_content=pr_content, 
            prd_file=args.prd_file, 
            prd_content=prd_content
        )
        
        session_file = os.path.join(args.run_dir, ".coder_session")
        
        if os.path.exists(session_file):
            with open(session_file, "r") as sf:
                session_key = sf.read().strip()
        else:
            import uuid
            session_key = f"sdlc_coder_{pr_id}_{uuid.uuid4().hex[:8]}"
        
        if args.system_alert:
            msg = build_prompt("coder_system_alert", system_alert=args.system_alert)
            if os.path.exists(session_file):
                send_feedback(session_key, msg, workdir=workdir)
            else:
                task_string += msg
                openclaw_agent_call(session_key, task_string, workdir=workdir)
                with open(session_file, "w") as f:
                    f.write(session_key)
                print(f"Spawned new session {session_key} with system alert")
        elif args.feedback_file:
            handle_feedback_routing(workdir, args.feedback_file, task_string, pr_id, args.run_dir)
        else:
            if not os.path.exists(session_file):
                openclaw_agent_call(session_key, task_string, workdir=workdir)
                with open(session_file, "w") as f:
                    f.write(session_key)
                print(f"Spawned new session {session_key}")
            else:
                openclaw_agent_call(session_key, task_string, workdir=workdir)
if __name__ == "__main__":
    main()
