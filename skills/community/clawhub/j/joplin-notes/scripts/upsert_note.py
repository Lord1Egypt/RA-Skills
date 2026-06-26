#!/usr/bin/env python3
import os
import subprocess
import sys
import uuid
import datetime

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

def generate_joplin_id():
    return uuid.uuid4().hex

def format_joplin_metadata(title, note_id, parent_id, type_="1"):
    # Timestamp exactly in Joplin format (UTC)
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    
    # Metadata block (Repeating the title is mandatory for discovery)
    metadata = (
        f"\n\n{title}\n\n"
        f"id: {note_id}\n"
        f"parent_id: {parent_id}\n"
        f"created_time: {now_iso}\n"
        f"updated_time: {now_iso}\n"
        f"is_conflict: 0\n"
        f"latitude: 49.31727650\n"
        f"longitude: 8.44121720\n"
        f"altitude: 0.0000\n"
        f"author:\n"
        f"source_url:\n"
        f"is_todo: 0\n"
        f"todo_due: 0\n"
        f"todo_completed: 0\n"
        f"source: joplin-desktop\n"
        f"source_application: net.cozic.joplin-desktop\n"
        f"application_data:\n"
        f"order: 0\n"
        f"user_created_time: {now_iso}\n"
        f"user_updated_time: {now_iso}\n"
        f"encryption_cipher_text:\n"
        f"encryption_applied: 0\n"
        f"markup_language: 1\n"
        f"is_shared: 0\n"
        f"share_id:\n"
        f"type_: {type_}"
    )
    return metadata

def strip_metadata(content):
    lines = content.splitlines()
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("id: "):
            start_of_block = i
            if start_of_block > 0 and lines[start_of_block-1].strip() == "":
                start_of_block -= 1
                if start_of_block > 0:
                    start_of_block -= 1
                    if start_of_block > 0 and lines[start_of_block-1].strip() == "":
                        start_of_block -= 1
            return "\n".join(lines[:start_of_block]).strip()
    return content.strip()

def upload_note(filename, content):
    check_config()
    password = get_joplin_password()
    
    url = JOPLIN_WEBDAV_URL
    if not url.endswith("/"):
        url += "/"

    command = [
        "curl", "-s", "-u", f"{JOPLIN_USERNAME}:{password}",
        "-X", "PUT", "-T", "-", f"{url}{filename}"
    ]
    result = subprocess.run(command, input=content.encode('utf-8'), capture_output=True)
    if result.returncode != 0:
        print(f"Error during upload: {result.stderr.decode()}", file=sys.stderr)
        sys.exit(1)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 upsert_note.py <note_id|new> <parent_id> <content_file> [type (1=note, 2=notebook)]")
        sys.exit(1)

    note_id = sys.argv[1]
    parent_id = sys.argv[2]
    content_file = sys.argv[3]
    item_type = sys.argv[4] if len(sys.argv) > 4 else "1"

    if not os.path.exists(content_file):
        print(f"Error: File {content_file} not found.", file=sys.stderr)
        sys.exit(1)

    with open(content_file, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    lines = raw_content.splitlines()
    title = lines[0].strip() if lines else "Untitled Note"

    if note_id == "new":
        note_id = generate_joplin_id()
    
    clean_content = strip_metadata(raw_content)
    full_content = clean_content + format_joplin_metadata(title, note_id, parent_id, item_type)

    filename = f"{note_id}.md"
    if upload_note(filename, full_content):
        type_str = "Notebook" if item_type == "2" else "Note"
        print(f"Success: {type_str} {note_id} has been updated.")
        print(f"NOTE_ID={note_id}")
