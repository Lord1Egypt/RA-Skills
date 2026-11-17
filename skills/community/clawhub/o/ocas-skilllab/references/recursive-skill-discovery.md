# Recursive Skill Discovery Pattern

## Problem
Skills may live at any depth under any profile directory:
- `$HERMES_HOME/../indigo/skills/ocas-foo/SKILL.md`
- `$HERMES_HOME/../indigo/skills/infrastructure/util-bar/SKILL.md`
- `$HERMES_HOME/../koda/skills/software-development/ocas-baz/SKILL.md`
- `~/.hermes/skills/util-github/SKILL.md` (default profile)

Hardcoding a single directory (e.g., `~/.hermes/skills/`) misses all skills in the active profile and subdirectories.

## Solution
Always use recursive glob with symlink dedup:

```python
import glob, os

def find_all_skills(search_roots):
    seen = set()
    seen_realpaths = set()
    results = []

    for root in search_roots:
        real_root = os.path.realpath(root)
        if real_root in seen_realpaths:
            continue
        seen_realpaths.add(real_root)

        for path in sorted(glob.glob(f"{root}/**/SKILL.md", recursive=True)):
            real_path = os.path.realpath(path)
            name = os.path.basename(os.path.dirname(real_path))
            if not (name.startswith("ocas-") or name.startswith("util-")):
                continue
            if name in seen:
                continue
            if ".archive" in real_path:
                continue
            seen.add(name)
            results.append((name, real_path))

    return results
```

## Key Points
- **Never use `os.listdir()`** — only finds top-level entries
- **Never use flat glob** — misses subdirectories
- **Always use `os.path.realpath()`** — profiles may have symlinked skill directories
- **Deduplicate by real path** — same skill reachable via symlinks counted once
- **Filter by prefix** — only `ocas-*` and `util-*` are agent-authored skills