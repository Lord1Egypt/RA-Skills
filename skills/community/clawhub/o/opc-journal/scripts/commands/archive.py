"""Journal command: archive memory files and metadata."""
import glob
import os
import shutil

from utils.storage import build_customer_dir
from utils.timezone import now_tz
from scripts.commands._meta import read_meta, write_meta


def run(customer_id: str, args: dict) -> dict:
    """Archive journal memory files and metadata to a timestamped directory."""
    base = os.path.expanduser(build_customer_dir(customer_id))
    memory_dir = os.path.join(base, "memory")
    meta_path = os.path.join(base, "journal_meta.json")

    if not os.path.exists(memory_dir) or not os.listdir(memory_dir):
        return {"status": "error", "result": None, "message": "No journal data to archive"}

    timestamp = now_tz().strftime("%Y%m%d-%H%M%S")
    archive_dir = os.path.join(base, "archive", timestamp)
    os.makedirs(archive_dir, exist_ok=True)

    archived_files = []
    failed_copies = []

    for f in sorted(glob.glob(os.path.join(memory_dir, "*.md"))):  # Only .md, exclude .bak
        if os.path.isfile(f):
            try:
                shutil.copy2(f, archive_dir)
                archived_files.append(os.path.basename(f))
            except Exception as e:
                failed_copies.append((f, str(e)))

    if os.path.exists(meta_path):
        try:
            shutil.copy2(meta_path, archive_dir)
            archived_files.append("journal_meta.json")
        except Exception as e:
            failed_copies.append((meta_path, str(e)))

    if failed_copies:
        return {
            "status": "error",
            "result": {
                "archive_path": archive_dir,
                "archived_files": archived_files,
                "failed_copies": failed_copies,
            },
            "message": f"Archive incomplete: {len(failed_copies)} file(s) failed to copy",
        }

    clear_after = bool(args.get("clear", False))
    if clear_after and not args.get("force", False):
        return {
            "status": "error",
            "result": None,
            "message": "Clearing files after archive is destructive. Re-run with --force to confirm.",
        }
    if clear_after:
        for f in glob.glob(os.path.join(memory_dir, "*.md")):
            os.remove(f)
        for f in glob.glob(os.path.join(memory_dir, "*.bak")):
            os.remove(f)
        meta = read_meta(customer_id)
        if meta:
            meta["total_entries"] = 0
            write_meta(customer_id, meta)

    return {
        "status": "success",
        "result": {
            "customer_id": customer_id,
            "archive_path": archive_dir,
            "archived_files": archived_files,
            "timestamp": timestamp,
            "cleared": clear_after,
        },
        "message": f"Archived {len(archived_files)} file(s) to {archive_dir}",
    }
