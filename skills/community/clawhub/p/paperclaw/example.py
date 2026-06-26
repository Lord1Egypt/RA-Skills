"""
Article Claw Skill - Usage Example

This example shows how agents can use the Article Claw Skill
to fetch papers and send digests.
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Skill root directory
SKILL_ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = Path(__file__).resolve().parent / "presets"


def fetch_papers(day: str = None, start_date: str = None, end_date: str = None) -> dict:
    """
    Fetch papers from arXiv.
    
    Args:
        day: Specific date (YYYY-MM-DD)
        start_date: Start date for range (YYYY-MM-DD)
        end_date: End date for range (YYYY-MM-DD)
    
    Returns:
        dict with paths to generated files
    """
    cmd = ["python", str(SKILL_ROOT / "scripts" / "main.py")]
    
    if day:
        cmd.extend(["--day", day])
    elif start_date and end_date:
        cmd.extend(["--start-date", start_date, "--end-date", end_date])
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=SKILL_ROOT)
    
    # Parse output to find generated files
    output = result.stdout + result.stderr
    
    # Extract date from command or use today
    if day:
        date_str = day
    else:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "success": result.returncode == 0,
        "markdown_path": str(SKILL_ROOT / "content" / "posts" / f"{date_str}-arxiv-audio-digest.md"),
        "json_path": str(SKILL_ROOT / "data" / "processed" / f"{date_str}.json"),
        "output": output
    }


def get_digest_content(date: str, format: str = "summary") -> dict:
    """
    Get digest content for a specific date.
    
    Args:
        date: Date string (YYYY-MM-DD)
        format: "markdown", "json", or "summary"
    
    Returns:
        dict with content
    """
    if format == "markdown":
        path = SKILL_ROOT / "content" / "posts" / f"{date}-arxiv-audio-digest.md"
        if path.exists():
            return {"content": path.read_text(encoding="utf-8"), "format": "markdown"}
    
    elif format == "json":
        path = SKILL_ROOT / "data" / "processed" / f"{date}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return {"content": data, "format": "json"}
    
    elif format == "summary":
        path = SKILL_ROOT / "data" / "processed" / f"{date}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return {
                "format": "summary",
                "date": date,
                "total_papers": data.get("summary", {}).get("total", 0),
                "categories": list(data.get("summary", {}).get("counts", {}).keys()),
                "paper_count_by_category": data.get("summary", {}).get("counts", {})
            }
    
    return {"error": f"Content not found for date {date}"}


# ============================================================================
# Preset Management Functions
# ============================================================================

def list_presets() -> list:
    """
    List all available configuration presets.
    
    Returns:
        List of preset summaries with id, name, description
    """
    index_path = PRESETS_DIR / "index.json"
    if not index_path.exists():
        return []
    
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "name_zh": p.get("name_zh", ""),
            "description": p["description"],
            "description_zh": p.get("description_zh", "")
        }
        for p in data.get("presets", [])
    ]


def get_preset(preset_id: str) -> Optional[dict]:
    """
    Get full preset configuration by ID.
    
    Args:
        preset_id: Preset identifier (e.g., "nlp", "computer_vision")
    
    Returns:
        Full preset config or None if not found
    """
    preset_path = PRESETS_DIR / f"{preset_id}.json"
    if not preset_path.exists():
        return None
    
    return json.loads(preset_path.read_text(encoding="utf-8"))


def apply_preset(preset_id: str) -> dict:
    """
    Apply a preset configuration to the system.
    
    Args:
        preset_id: Preset identifier (e.g., "nlp", "computer_vision")
    
    Returns:
        dict with success status and applied configuration
    """
    preset = get_preset(preset_id)
    if not preset:
        return {"success": False, "error": f"Preset '{preset_id}' not found"}
    
    # Load current config
    config_path = SKILL_ROOT / "config" / "default.json"
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
    else:
        config = {}
    
    # Apply preset configurations
    # 1. Update arXiv categories
    if "arxiv_categories" in preset:
        config["sources"] = config.get("sources", {})
        config["sources"]["arxiv"] = {
            "enabled": True,
            "name": "arXiv",
            "url": "https://arxiv.org",
            "categories": preset["arxiv_categories"]
        }
    
    # 2. Update classification categories
    if "classification" in preset:
        config["classification"] = {
            "categories": preset["classification"]
        }
    
    # Save updated config
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    return {
        "success": True,
        "preset_id": preset_id,
        "preset_name": preset["name"],
        "arxiv_categories": [c["id"] for c in preset.get("arxiv_categories", [])],
        "classification_categories": [c["name"] for c in preset.get("classification", [])],
        "config_path": str(config_path)
    }


def preview_preset(preset_id: str) -> dict:
    """
    Preview what a preset will configure without applying it.
    
    Args:
        preset_id: Preset identifier
    
    Returns:
        dict with preview information
    """
    preset = get_preset(preset_id)
    if not preset:
        return {"success": False, "error": f"Preset '{preset_id}' not found"}
    
    return {
        "success": True,
        "preset_id": preset_id,
        "name": preset["name"],
        "name_zh": preset.get("name_zh", ""),
        "description": preset["description"],
        "arxiv_categories": [
            {"id": c["id"], "name": c["name"], "description": c.get("description", "")}
            for c in preset.get("arxiv_categories", [])
        ],
        "classification_categories": [
            {"name": c["name"], "labels": c.get("labels", {}), "keyword_count": len(c.get("keywords", []))}
            for c in preset.get("classification", [])
        ]
    }


# ============================================================================
# Configuration Functions
# ============================================================================

def configure_recipients(recipients: list) -> dict:
    """
    Update recipients configuration.
    
    Args:
        recipients: List of dicts with email, name, enabled
    
    Returns:
        dict with success status
    """
    config_path = SKILL_ROOT / "config" / "recipients.json"
    
    config = {
        "recipients": recipients,
        "settings": {
            "display_mode": "full",
            "papers_per_category": 999,
            "show_full_abstract": True
        }
    }
    
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    return {
        "success": True,
        "recipient_count": len(recipients),
        "config_path": str(config_path)
    }


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Example 1: List available presets")
    print("=" * 60)
    presets = list_presets()
    for p in presets:
        print(f"  - {p['id']}: {p['name']} / {p['name_zh']}")
        print(f"    {p['description']}")
    
    print("\n" + "=" * 60)
    print("Example 2: Preview a preset")
    print("=" * 60)
    preview = preview_preset("nlp")
    print(f"Preset: {preview['name']}")
    print(f"ArXiv categories: {[c['id'] for c in preview['arxiv_categories']]}")
    print(f"Classification: {[c['name'] for c in preview['classification_categories']]}")
    
    print("\n" + "=" * 60)
    print("Example 3: Apply a preset")
    print("=" * 60)
    # apply_preset("nlp")  # Uncomment to actually apply
    print("(Skipped - uncomment apply_preset() to apply)")
    
    print("\n" + "=" * 60)
    print("Example 4: Fetch papers for a specific date")
    print("=" * 60)
    # result = fetch_papers(day="2026-03-10")
    # print(f"Success: {result['success']}")
    print("(Skipped - uncomment fetch_papers() to run)")
    
    print("\n" + "=" * 60)
    print("Example 5: Get digest summary")
    print("=" * 60)
    # summary = get_digest_content("2026-03-10", format="summary")
    # print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("(Skipped - uncomment get_digest_content() to run)")
    
    print("\n" + "=" * 60)
    print("Example 6: Configure recipients")
    print("=" * 60)
    recipients = [
        {"email": "professor@university.edu.cn", "name": "Professor", "enabled": True},
        {"email": "student@university.edu.cn", "name": "Student", "enabled": True}
    ]
    config_result = configure_recipients(recipients)
    print(f"Configured {config_result['recipient_count']} recipients")
