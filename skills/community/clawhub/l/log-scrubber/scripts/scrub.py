# SECURITY MANIFEST:
# Environment variables accessed: None
# External endpoints called: None
# Local files read: memory/*, logs/*, MEMORY.md
# Local files written: memory/*, logs/*, MEMORY.md

import os
import re
import shutil
import argparse

# Redaction patterns
PATTERNS = [
    r'sk-or-v1-[a-zA-Z0-9]{32,}',  # OpenRouter
    r'sk-[a-zA-Z0-9]{32,}',         # Standard OpenAI
    r'(?i)(api[_-]key|token|password|secret|key)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9\-]{10,})["\']?', # Generic
]

def scrub_content(content):
    original = content
    # Updated regex to handle redaction properly based on groups
    def repl(m):
        if len(m.groups()) > 1:
            return f"{m.group(1)}: [REDACTED]"
        return "[REDACTED]"
    
    content = re.sub(PATTERNS[0], "[REDACTED]", content)
    content = re.sub(PATTERNS[1], "[REDACTED]", content)
    content = re.sub(PATTERNS[2], repl, content)
    
    return content, content != original

def main():
    parser = argparse.ArgumentParser(description="Scrub logs and memory files for secrets.")
    parser.add_argument('--dry-run', action='store_true', help="Print changes without modifying files.")
    args = parser.parse_args()

    base_dir = "/root/.openclaw/workspace"
    target_dirs = ["memory", "logs"]
    extra_files = ["MEMORY.md"]

    for d in target_dirs:
        full_path = os.path.join(base_dir, d)
        if not os.path.exists(full_path):
            continue
        for root, _, files in os.walk(full_path):
            for f in files:
                if f.endswith('.bak'): continue
                path = os.path.join(root, f)
                process_file(path, args.dry_run)

    for f in extra_files:
        path = os.path.join(base_dir, f)
        if os.path.exists(path):
            process_file(path, args.dry_run)

def process_file(path, dry_run):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changed = scrub_content(content)
        
        if changed:
            if dry_run:
                print(f"[DRY-RUN] Would scrub: {path}")
            else:
                # Create backup
                shutil.copy2(path, path + ".bak")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Scrubbed and backed up: {path}")
    except Exception as e:
        print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    main()
