#!/usr/bin/env python3
import os
import subprocess
import re
import sys
from urllib.parse import urlparse

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

def list_joplin_files():
    check_config()
    password = get_joplin_password()
    
    url = JOPLIN_WEBDAV_URL
    if not url.endswith("/"):
        url += "/"

    command = [
        "curl", "-s", "-u", f"{JOPLIN_USERNAME}:{password}",
        "-X", "PROPFIND", "--header", "Depth: infinity", url
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    # Extract path part of the URL for the regex
    url_path = urlparse(url).path
    if not url_path.endswith("/"):
        url_path += "/"
    
    escaped_path = re.escape(url_path)
    return re.findall(rf'<d:href>{escaped_path}([^/]+\.md)</d:href>', result.stdout)

def read_joplin_note_content(filename):
    check_config()
    password = get_joplin_password()
    url = JOPLIN_WEBDAV_URL
    if not url.endswith("/"):
        url += "/"
        
    command = ["curl", "-s", "-u", f"{JOPLIN_USERNAME}:{password}", f"{url}{filename}"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout

def parse_note_data(content):
    lines = content.splitlines()
    title = lines[0].strip() if lines else "Untitled Note"
    
    metadata = {
        "title": title,
        "id": None,
        "parent_id": None,
        "type_": "1"
    }

    metadata_section = False
    for line in lines:
        if line.strip() == "":
            metadata_section = True
            continue
        if metadata_section:
            if line.startswith("id:"):
                metadata["id"] = line.split("id:", 1)[1].strip()
            elif line.startswith("parent_id:"):
                metadata["parent_id"] = line.split("parent_id:", 1)[1].strip()
            elif line.startswith("type_:"):
                metadata["type_"] = line.split("type_:", 1)[1].strip()
            elif line.startswith("type\_:"):
                metadata["type_"] = line.split("type\_:", 1)[1].strip()
    return metadata

def get_structure():
    files = list_joplin_files()
    notes_data = {}
    for filename in files:
        if filename.startswith(('.lock', '.resource', '.sync', 'temp')):
            continue
        content = read_joplin_note_content(filename)
        data = parse_note_data(content)
        if data["id"]:
            notes_data[data["id"]] = data

    notebooks = {
        nid: {"title": n["title"], "notes": []}
        for nid, n in notes_data.items() if n["type_"] == "2"
    }

    # Handle cases where a notebook is referenced as parent but not marked as type 2
    for n in notes_data.values():
        pid = n["parent_id"]
        if pid and pid not in notebooks and pid in notes_data:
             notebooks[pid] = {"title": notes_data[pid]["title"], "notes": []}

    # Assign notes to notebooks
    for n in notes_data.values():
        if n["type_"] == "1" and n["parent_id"] in notebooks:
            notebooks[n["parent_id"]]["notes"].append(n)
        elif n["type_"] == "1" and not n["parent_id"]:
            if "root" not in notebooks:
                notebooks["root"] = {"title": "Root / Unassigned", "notes": []}
            notebooks["root"]["notes"].append(n)

    return notebooks

if __name__ == "__main__":
    try:
        structure = get_structure()
        for nid, nb in structure.items():
            print(f"**Notebook: {nb['title']}** (ID: {nid})")
            for note in sorted(nb["notes"], key=lambda x: x["title"].lower()):
                print(f"  * {note['title']} (ID: {note['id']})")
            print()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
