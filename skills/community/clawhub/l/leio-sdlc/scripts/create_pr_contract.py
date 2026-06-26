#!/usr/bin/env python3
import argparse
import os
import re
import sys

class SecurityError(Exception):
    pass

def calculate_index(job_dir, insert_after):
    base_pattern = re.compile(r"^PR_(\d+)_.*\.md$")
    if not insert_after:
        max_base = 0
        for f in os.listdir(job_dir):
            match = base_pattern.match(f)
            if match:
                max_base = max(max_base, int(match.group(1)))
        return f"{max_base + 1:03d}"
    else:
        sub_pattern = re.compile(rf"^PR_{insert_after}_(\d+)_.*\.md$")
        max_sub = 0
        for f in os.listdir(job_dir):
            match = sub_pattern.match(f)
            if match:
                max_sub = max(max_sub, int(match.group(1)))
        return f"{insert_after}_{max_sub + 1}"

def main():
    parser = argparse.ArgumentParser(description="Create a PR contract file.")
    parser.add_argument("--workdir", required=True, help="Working directory lock")
    parser.add_argument("--job-dir", required=True, help="Path to job queue directory")
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument("--content-file", required=False, help="Path to file with PR content")
    parser.add_argument("--project", help="Project name (deprecated/ignored)")
    parser.add_argument("--insert-after", help="Prefix of the PR to insert after (e.g., 003)")
    parser.add_argument("--only-scaffold", action="store_true", help="Only scaffold PR contract from template")
    args = parser.parse_args()

    if not args.only_scaffold and not args.content_file:
        parser.error("--content-file is required unless --only-scaffold is provided")

    # Resolve all paths BEFORE changing directory
    workdir = os.path.abspath(args.workdir)
    job_dir_path = os.path.abspath(args.job_dir)
    
    if args.content_file:
        content_file_path = os.path.abspath(args.content_file)

    # OS Lock
    os.chdir(workdir)

    # Validate content file with Path Traversal Defense
    if args.content_file:
        # Allow if it's in workdir OR job_dir
        try:
            common_work = os.path.commonpath([workdir, content_file_path]) == workdir
        except ValueError:
            common_work = False
            
        try:
            common_job = os.path.commonpath([job_dir_path, content_file_path]) == job_dir_path
        except ValueError:
            common_job = False

        if not (common_work or common_job):
            raise SecurityError(f"Path traversal detected: {content_file_path} is outside {workdir} and {job_dir_path}")

        if not os.path.exists(content_file_path):
            print(f"Error: Content file '{content_file_path}' not found.")
            sys.exit(1)

    # Validate/Create job dir
    os.makedirs(job_dir_path, exist_ok=True)

    # Calculate new index
    index = calculate_index(job_dir_path, args.insert_after)

    # Format title
    safe_title = args.title.replace(" ", "_")
    filename = f"PR_{index}_{safe_title}.md"
    file_path = os.path.join(job_dir_path, filename)
    
    # Final output path must be within job_dir_path
    if os.path.commonpath([job_dir_path, file_path]) != job_dir_path:
        raise SecurityError(f"Path traversal detected: {file_path} is outside {job_dir_path}")

    # Read content
    if args.only_scaffold:
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TEMPLATES", "PR_Contract.md.template")
        with open(template_path, "r") as f:
            content = f.read()
        content = content.replace("[ID]", index).replace("[Title]", args.title)
    else:
        with open(content_file_path, "r") as f:
            content = f.read()

    # Write new file
    with open(file_path, "w") as f:
        f.write(content)

    print(f"[PR_CREATED] {file_path}")

if __name__ == "__main__":
    main()
