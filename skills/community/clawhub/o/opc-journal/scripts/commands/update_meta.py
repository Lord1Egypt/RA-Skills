"""Journal command: update metadata with optional retroactive template translation."""
import glob
import os
import re
from pathlib import Path

from utils.storage import build_customer_dir
from scripts.commands._meta import get_language, read_meta, write_meta


# Translation rules are intentionally minimal: the skill now generates English-only templates.
_ZH_TO_EN_REGEX = []
_EN_TO_ZH_REGEX = []


def _translate_file(path: str, old_lang: str, new_lang: str) -> bool:
    if old_lang == new_lang:
        return False
    try:
        text = Path(path).read_text(encoding="utf-8")
    except Exception:
        return False

    if old_lang == "zh" and new_lang == "en":
        regex_pairs = _ZH_TO_EN_REGEX
    elif old_lang == "en" and new_lang == "zh":
        regex_pairs = _EN_TO_ZH_REGEX
    else:
        return False

    lines = text.splitlines()
    new_lines = []
    changed = False
    for line in lines:
        new_line = line
        for pat, repl in regex_pairs:
            new_line, count = re.subn(pat, repl, new_line, count=1)
            if count:
                changed = True
                break
        new_lines.append(new_line)

    if not changed:
        return False

    try:
        Path(path).write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
        return True
    except Exception:
        return False


def run(customer_id: str, args: dict) -> dict:
    """Update journal metadata and retroactively translate document templates if language changes."""
    meta = read_meta(customer_id)
    if not meta:
        return {
            "status": "error",
            "result": None,
            "message": "Journal not initialized. Run `/opc-journal init` first.",
        }

    old_lang = get_language(customer_id)
    new_lang = args.get("language") or old_lang
    goals = args.get("goals")
    preferences = args.get("preferences")

    updated = False
    if new_lang and new_lang != old_lang:
        meta["language"] = new_lang
        updated = True

    if goals is not None:
        meta["goals"] = goals if isinstance(goals, list) else [goals]
        updated = True

    if preferences is not None:
        meta["preferences"] = preferences if isinstance(preferences, dict) else {}
        updated = True

    if not updated:
        return {"status": "success", "result": {"changed": False}, "message": "Nothing to update."}

    write_meta(customer_id, meta)

    translated_count = 0
    if new_lang != old_lang:
        memory_dir = os.path.expanduser(os.path.join(build_customer_dir(customer_id), "memory"))
        if os.path.exists(memory_dir):
            for f in sorted(glob.glob(os.path.join(memory_dir, "*.md"))):
                if _translate_file(f, old_lang, new_lang):
                    translated_count += 1

    msg = f"Meta updated for {customer_id}. Language: {new_lang}."
    if translated_count:
        msg += f" Retroactively translated {translated_count} document(s)."

    return {
        "status": "success",
        "result": {
            "customer_id": customer_id,
            "language": new_lang,
            "changed": True,
            "translated_documents": translated_count,
        },
        "message": msg,
    }
