"""
Garden Init — Bootstrap a new MindGardener workspace.

Creates the directory structure, config file, and a sample daily log
so new users can run `garden extract` immediately.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path


DEFAULT_CONFIG = """# MindGardener Configuration
# See: https://github.com/maweding/mindgardener

# Workspace root (where memory/ lives)
workspace: .

# LLM Provider: gemini | openai | anthropic | ollama | compatible
provider: gemini

# Model to use for extraction
# gemini: gemini-2.0-flash (default, cheapest)
# openai: gpt-4o-mini
# anthropic: claude-sonnet-4-20250514
# ollama: llama3.2 (local, free)
model: gemini-2.0-flash

# Extraction settings
extraction:
  max_chunk_size: 4000    # Split large files at this size
  pre_filter: true        # Strip noise (heartbeats, code blocks)

# Decay settings
decay:
  archive_after_days: 30  # Archive entities not referenced in N days
  stale_warning_days: 14  # Warn about entities going stale
  protected_types:        # Entity types that never decay
    - project
    - tool

# Surprise scoring
surprise:
  consolidation_threshold: 0.5  # Minimum PE score to promote to MEMORY.md

# Entity aliases (for deduplication)
# aliases:
#   "Peter Steinberger": ["steipete", "@steipete"]
"""

SAMPLE_DAILY = """# {date} Daily Notes

## What happened today
- Started using MindGardener for agent memory
- Set up workspace with `garden init`

## Notes
- Add your daily observations, events, and interactions here
- MindGardener will extract entities, relationships, and events automatically
- Run `garden extract` to process this file
"""

SAMPLE_MEMORY = """# Long-term Memory

This file is your agent's world model. MindGardener's consolidation engine
will automatically append high-surprise events here during the "sleep cycle."

You can also edit this file manually to add permanent knowledge.
"""


def init_workspace(path: Path | None = None, provider: str = "gemini",
                   force: bool = False) -> list[str]:
    """
    Initialize a MindGardener workspace.
    
    Creates:
    - garden.yaml (config)
    - memory/ (daily logs directory)
    - memory/entities/ (wiki pages)
    - memory/<today>.md (sample daily log)
    - MEMORY.md (long-term memory)
    
    Returns list of actions taken.
    """
    if path is None:
        path = Path.cwd()
    else:
        path = Path(path)
    
    actions = []
    
    # Config file
    config_path = path / "garden.yaml"
    if config_path.exists() and not force:
        actions.append(f"⏭️  garden.yaml already exists (use --force to overwrite)")
    else:
        config = DEFAULT_CONFIG.replace("provider: gemini", f"provider: {provider}")
        config_path.write_text(config)
        actions.append(f"✅ Created garden.yaml (provider: {provider})")
    
    # Memory directory
    memory_dir = path / "memory"
    memory_dir.mkdir(exist_ok=True)
    actions.append(f"✅ Created memory/")
    
    # Entities directory
    entities_dir = memory_dir / "entities"
    entities_dir.mkdir(exist_ok=True)
    actions.append(f"✅ Created memory/entities/")
    
    # Sample daily log
    today = date.today().isoformat()
    daily_path = memory_dir / f"{today}.md"
    if not daily_path.exists():
        daily_path.write_text(SAMPLE_DAILY.replace("{date}", today))
        actions.append(f"✅ Created memory/{today}.md (sample daily log)")
    else:
        actions.append(f"⏭️  memory/{today}.md already exists")
    
    # MEMORY.md
    memory_file = path / "MEMORY.md"
    if not memory_file.exists():
        memory_file.write_text(SAMPLE_MEMORY)
        actions.append(f"✅ Created MEMORY.md (long-term memory)")
    else:
        actions.append(f"⏭️  MEMORY.md already exists")
    
    # .gitignore for lock files
    gitignore = path / ".gitignore"
    ignore_entries = ["*.lock", "*.tmp", "__pycache__/"]
    if gitignore.exists():
        existing = gitignore.read_text()
        new_entries = [e for e in ignore_entries if e not in existing]
        if new_entries:
            with open(gitignore, "a") as f:
                f.write("\n# MindGardener\n")
                for e in new_entries:
                    f.write(f"{e}\n")
            actions.append(f"✅ Updated .gitignore")
    else:
        gitignore.write_text("# MindGardener\n" + "\n".join(ignore_entries) + "\n")
        actions.append(f"✅ Created .gitignore")
    
    # Next steps
    actions.append("")
    actions.append("🌱 Workspace ready! Next steps:")
    
    # Check for API key
    provider_keys = {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    key_name = provider_keys.get(provider)
    if key_name and not os.environ.get(key_name):
        actions.append(f"   1. Set your API key: export {key_name}=...")
        actions.append(f"   2. Edit memory/{today}.md with today's events")
        actions.append(f"   3. Run: garden extract")
    else:
        actions.append(f"   1. Edit memory/{today}.md with today's events")
        actions.append(f"   2. Run: garden extract")
    
    actions.append(f"   Then: garden recall <entity>")
    
    return actions
