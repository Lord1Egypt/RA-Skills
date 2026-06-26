#!/usr/bin/env python3
import os
import subprocess
import sys

# Configuration via environment variables
JOPLIN_WEBDAV_URL = os.getenv("JOPLIN_WEBDAV_PATH")
JOPLIN_USERNAME = os.getenv("JOPLIN_ACCOUNT")

def check_config():
    if not JOPLIN_WEBDAV_URL or not JOPLIN_USERNAME:
        print("Error: JOPLIN_WEBDAV_PATH or JOPLIN_ACCOUNT environment variable not set.", file=sys.stderr)
        sys.exit(1)

def get_joplin_password():
    password = os.getenv("JOPLIN_PASSWORD")
    if not password:
        print("Error: JOPLIN_PASSWORD environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return password

def read_joplin_note_content(note_id):
    check_config()
    password = get_joplin_password()
    
    url = JOPLIN_WEBDAV_URL
    if not url.endswith("/"):
        url += "/"
        
    filename = f"{note_id}.md"
    command = [
        "curl", "-s", "-u", f"{JOPLIN_USERNAME}:{password}",
        f"{url}{filename}"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0 or "404" in result.stdout:
        print(f"Error: Note with ID {note_id} not found.", file=sys.stderr)
        sys.exit(1)
    return result.stdout

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 get_note.py <note_id>")
        sys.exit(1)
    
    note_id = sys.argv[1].replace(".md", "")
    try:
        content = read_joplin_note_content(note_id)
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
