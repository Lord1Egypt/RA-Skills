"""
Long-Term Memory Skill — Setup for OpenClaw workspace
"""
import json
import sys
from pathlib import Path


def get_workspace() -> Path:
    for p in [
        Path.home() / ".openclaw" / "workspace",
        Path.home() / ".openclaw" / "workspace-preschool",
        Path.home() / ".openclaw" / "workspace-main",
    ]:
        if p.exists():
            return p
    return Path.cwd()


def print_b(text):
    try:
        import io
        sys.stdout.buffer.write(text.encode('utf-8') + b'\n')
        sys.stdout.buffer.flush()
    except:
        print(text)


def install():
    workspace = get_workspace()
    skill_dir = Path(__file__).resolve().parent.parent

    print_b("=" * 50)
    print_b(" Long-Term Memory — Installer")
    print_b("=" * 50)

    # 1. Create data dir
    data_dir = workspace / "long-term-memory"
    data_dir.mkdir(parents=True, exist_ok=True)
    print_b(f"\n[1/4] Data dir: {data_dir}")

    # 2. Config
    config = {
        "version": "0.2.0",
        "embedding_mode": "simple",
        "max_memories": 5000,
        "auto_capture": True,
        "context_inject": True,
        "context_max_tokens": 2000,
        "session_history_days": 30,
        "installed_at": __import__("time").strftime("%Y-%m-%d %H:%M:%S"),
        "workspace": str(workspace),
    }
    with open(data_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print_b(f"[2/4] Config: {data_dir / 'config.json'}")

    # 3. Init DB
    sys.path.insert(0, str(skill_dir / "scripts"))
    from memory_engine import MemoryStore
    store = MemoryStore(db_path=data_dir / "memory.db")
    print_b(f"[3/4] DB initialized: {store.stats()['total_memories']} existing memories")

    # 4. AGENTS.md integration reminder
    agents_path = workspace / "AGENTS.md"
    print_b(f"[4/4] AGENTS.md: {agents_path}")

    print_b("\n" + "-" * 50)
    print_b(" INSTALLATION COMPLETE")
    print_b("-" * 50)
    print_b(f"\nAdd these lines to your AGENTS.md (in {workspace}):")
    print_b("")
    print_b("## Long-Term Memory")
    print_b("1. On session start: run `python3 scripts/memory_engine.py inject")
    print_b("2. Save key decisions with --importance 8")
    print_b("3. Search memory before answering 'remember' questions")
    print_b("4. On session end: summarize for next session")
    print_b("")
    print_b("Quick test:")
    print_b(f"  cd {skill_dir}")
    print_b(f"  python3 scripts/memory_engine.py demo")
    print_b(f"  python3 scripts/memory_engine.py stats")
    print_b("=" * 50)


if __name__ == "__main__":
    install()
