#!/usr/bin/env python3
import os
import subprocess
import sys
import uuid

# Paths to the other scripts
SKILL_DIR = "/home/openclaw/.openclaw/workspace/skills/joplin-notes"
UPSERT_SCRIPT = os.path.join(SKILL_DIR, "scripts/upsert_note.py")

def create_notebook(title, parent_notebook_id=""):
    # A notebook only needs a file with the title and metadata (Type 2)
    # A notebook normally doesn't have body content.
    temp_file = "/tmp/new_notebook_init.md"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(title + "\n") # First line is the title
    
    # Call upsert with Type 2 (Notebook)
    cmd = ["python3", UPSERT_SCRIPT, "new", parent_notebook_id, temp_file, "2"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
        
    if result.returncode == 0:
        # Extract the new ID from the output
        for line in result.stdout.splitlines():
            if line.startswith("NOTE_ID="):
                return line.split("=")[1].strip()
    else:
        print(f"Error creating notebook: {result.stderr}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 create_notebook.py <title> [parent_notebook_id]")
        sys.exit(1)
    
    title = sys.argv[1]
    parent_id = sys.argv[2] if len(sys.argv) > 2 else ""
    
    new_id = create_notebook(title, parent_id)
    if new_id:
        print(f"Success: Notebook '{title}' created.")
        print(f"NOTEBOOK_ID={new_id}")
