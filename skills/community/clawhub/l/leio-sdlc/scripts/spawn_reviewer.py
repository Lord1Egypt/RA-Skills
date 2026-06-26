import argparse
import tempfile
import os
import sys
from agent_driver import invoke_agent, build_prompt
import subprocess
import uuid
import fnmatch

def check_guardrails(workdir, pr_content, diff_files):
    guardrail_path = os.path.join(workdir, ".sdlc_guardrail")
    if not os.path.exists(guardrail_path):
        return None
        
    with open(guardrail_path, "r") as f:
        protected_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
    if not protected_patterns:
        return None
        
    modified_files = set()
    for diff_file in diff_files:
        if os.path.exists(diff_file):
            with open(diff_file, "r") as f:
                for line in f:
                    if line.startswith("+++ b/") and not line.startswith("+++ b/dev/null"):
                        modified_files.add(line[6:].strip())
                    elif line.startswith("--- a/") and not line.startswith("--- a/dev/null"):
                        modified_files.add(line[6:].strip())
                    
    for mod_file in modified_files:
        # Check against patterns
        for pattern in protected_patterns:
            is_protected = False
            if pattern.endswith("/"):
                if mod_file.startswith(pattern):
                    is_protected = True
            else:
                if fnmatch.fnmatch(mod_file, pattern):
                    is_protected = True
                    
            if is_protected:
                # If explicitly authorized in PR content
                if mod_file not in pr_content:
                    return f"[ACTION_REQUIRED]: Guardrail violation detected. Unauthorized modification of protected file: {mod_file}"
                    
    return None

def main():
    parser = argparse.ArgumentParser(description="Spawn a reviewer agent.")
    parser.add_argument("--pr-file", required=True, help="Path to the PR Contract file")
    parser.add_argument("--diff-target", required=True, help="Git diff target range (e.g., base_hash..latest_hash)")
    parser.add_argument("--override-diff-file", help="Override the diff file and skip git diff", default=None)
    parser.add_argument("--job-dir", required=False, default=".", help="Working directory for the Reviewer to generate artifacts")
    parser.add_argument("--workdir", required=True, help="Working directory lock")
    parser.add_argument("--out-file", default="review_report.json", help="Path to write the review report")
    parser.add_argument("--global-dir", required=False, help="Global directory for templates/playbooks")
    parser.add_argument("--run-dir", default=".", help="Run directory for artifacts")
    
    RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
    args = parser.parse_args()

    workdir = os.path.abspath(args.workdir)
    os.chdir(workdir)

    # Production mode
    if not os.path.exists(args.pr_file):
        print(f"Error: PR file not found: {args.pr_file}")
        sys.exit(1)
        
    with open(args.pr_file, "r") as f:
        pr_content = f.read()
        
    import re
    pr_num = 5
    match = re.search(r'PR_0*(\d+)', os.path.basename(args.pr_file))
    if match:
        pr_num = int(match.group(1))

    if args.override_diff_file:
        diff_file = args.override_diff_file
    else:
        diff_file = os.path.join(args.run_dir, "current_review.diff")

    if not args.override_diff_file:
        diff_cmd = f"git diff {args.diff_target} --no-color > {diff_file}"
        subprocess.run(diff_cmd, shell=True)
            
        baseline_file = os.path.join(args.run_dir, "baseline_commit.txt")
        if os.path.exists(baseline_file):
            with open(baseline_file, "r") as f:
                baseline_hash = f.read().strip()
            history_cmd = f"git log -p {baseline_hash}..HEAD > {os.path.join(args.run_dir, 'recent_history.diff')}"
        else:
            history_depth = max(5, pr_num)
            history_cmd = f"git log -n {history_depth} -p {args.diff_target} > {os.path.join(args.run_dir, 'recent_history.diff')}"
        subprocess.run(history_cmd, shell=True)
        
    guardrail_violation = check_guardrails(workdir, pr_content, [os.path.join(workdir, diff_file)])
    if guardrail_violation:
        print(f"[Reviewer Guardrail] Fast-failing PR due to guardrail violation.")
        with open(os.path.join(args.run_dir, args.out_file), "w") as rf:
            rf.write(guardrail_violation)
        if os.environ.get("SDLC_TEST_MODE") == "true":
            print('{"status": "mock_success", "role": "reviewer_guardrail"}')
            sys.exit(0)
        sys.exit(0)

    SDLC_ROOT = os.path.dirname(RUNTIME_DIR)
    template_content = ""

    playbook_path = os.path.join(SDLC_ROOT, "playbooks", "reviewer_playbook.md")
    playbook_content = ""
    if os.path.exists(playbook_path):
        with open(playbook_path, "r") as f:
            playbook_content = f.read()

    task_string = build_prompt("reviewer",
        workdir=workdir,
        playbook_content=playbook_content,
        pr_content=pr_content,
        diff_file=diff_file,
        out_file=args.out_file, run_dir=args.run_dir,
        template_content=template_content
    )
    

    if os.environ.get("SDLC_TEST_MODE") == "true":
        os.makedirs("tests", exist_ok=True)
        with open("tests/tool_calls.log", "w") as tf:
            tf.write(task_string)
        # Mock LLM writing the report
        with open(os.path.join(args.run_dir, args.out_file), "w") as rf:
            rf.write('```json\n{"status": "APPROVED", "comments": "Mock LGTM"}\n```')
        print('{"status": "mock_success", "role": "reviewer"}')
        sys.exit(0)

    import time
    session_id = f"subtask-{uuid.uuid4().hex[:8]}"
    invoke_agent(task_string, session_key=session_id, role="reviewer")

    review_report_path = os.path.join(args.run_dir, args.out_file)
    if not os.path.exists(review_report_path):
        print(f"[FATAL] The Reviewer agent failed to generate the physical '{args.out_file}'. This is a severe process violation.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
