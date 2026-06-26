#!/usr/bin/env python3
import argparse
import os
import sys

def main():
    if "/root/.openclaw/workspace/projects/" in os.path.abspath(__file__):
        if "--enable-exec-from-workspace" not in sys.argv:
            print("[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nStartup validation failed (likely executing from the wrong directory). You MUST execute the script using its absolute installed path (e.g., `python3 ~/.openclaw/skills/pm-skill/scripts/init_prd.py ...`) OR explicitly append the `--enable-exec-from-workspace` flag if testing locally.")
            sys.exit(1)

    parser = argparse.ArgumentParser(description="Initialize a new PRD based on the template.")
    parser.add_argument("--project", required=True, help="Target project name (e.g., leio-sdlc, AMS)")
    parser.add_argument("--title", required=True, help="Short title for the PRD (used in filename)")
    parser.add_argument("--enable-exec-from-workspace", action="store_true", help="Bypass the workspace path check")
    args = parser.parse_args()

    workspace_root = "/root/.openclaw/workspace"
    project_dir = os.path.join(workspace_root, "projects", args.project)
    
    if not os.path.exists(project_dir):
        print(f"Error: Target project directory does not exist: {project_dir}", file=sys.stderr)
        sys.exit(1)

    prds_dir = os.path.join(project_dir, "docs", "PRDs")
    os.makedirs(prds_dir, exist_ok=True)
    
    safe_title = args.title.replace(" ", "_").replace("/", "_")
    target_prd_path = os.path.join(prds_dir, f"PRD_{safe_title}.md")

    if os.path.exists(target_prd_path):
        print(f"[SUCCESS] Target PRD already exists at: {target_prd_path}")
        print("Please use the 'edit' or 'write' tool to update this file directly.")
        sys.exit(0)

    # Resolve Template
    template_path = os.path.join(workspace_root, "projects", "docs", "TEMPLATES", "PRD.md.template")
    fallback_template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TEMPLATES", "PRD.md.template")
    
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            template_content = f.read()
    elif os.path.exists(fallback_template_path):
        with open(fallback_template_path, "r") as f:
            template_content = f.read()
    else:
        print(f"Error: Could not find PRD template at {template_path} or {fallback_template_path}", file=sys.stderr)
        sys.exit(1)

    # Inject project name
    template_content = template_content.replace("[Project Name]", args.title)
    
    # Save new PRD
    with open(target_prd_path, "w") as f:
        f.write(template_content)

    print(f"[SUCCESS] Blank PRD scaffold created at: {target_prd_path}")
    print("Please use the 'edit' or 'write' tool to fill in the contents based on your discussion.")

if __name__ == "__main__":
    main()