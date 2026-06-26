#!/usr/bin/env python3
import argparse
import os
import glob
import sys
import re

class SecurityError(Exception):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True, help="Working directory lock")
    parser.add_argument("--job-dir", required=True)
    args = parser.parse_args()

    workdir = os.path.abspath(args.workdir)
    job_dir = os.path.abspath(args.job_dir)
    os.chdir(workdir)

    # Job dir can now be in global workspace, removed strict workdir containment check

    if not os.path.exists(job_dir):
        print(f"[Pre-flight Failed] Job directory '{job_dir}' does not exist.")
        sys.exit(1)

    pattern = os.path.join(job_dir, "*.md")
    md_files = glob.glob(pattern)
    md_files.sort()

    for md_file in md_files:
        pass # path traversal logic relaxed for global dir
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(r'^status:\s*open\b', content, re.MULTILINE):
                    print(md_file)
                    sys.exit(0)
        except Exception:
            pass
    
    print(f"[QUEUE_EMPTY] All PRs in {job_dir} are closed or blocked.")
    sys.exit(0)

if __name__ == "__main__":
    main()
