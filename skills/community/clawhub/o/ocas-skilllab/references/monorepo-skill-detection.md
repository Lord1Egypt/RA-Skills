# Monorepo Skill Detection

## The Problem

Some skills have `source:` pointing to a subdirectory within a monorepo, NOT a standalone GitHub repo. Creating a standalone repo for these skills violates the declared source and fragments the library.

## Detection

```python
import yaml, os, glob

skills_dir = os.path.expanduser("~/.hermes/skills")
for path in glob.glob(f"{skills_dir}/*/SKILL.md"):
    with open(path) as f:
        content = f.read()
    parts = content.split("---")
    if len(parts) >= 3:
        fm = yaml.safe_load(parts[1])
        source = fm.get("source", "")
        name = fm.get("name", os.path.basename(os.path.dirname(path)))
        # Monorepo indicators: source contains /tree/ or /blob/ pointing to a subdirectory
        if "/tree/" in source or "/blob/" in source:
            print(f"MONOREPO: {name} → {source}")
```

## Known Monorepos

| Monorepo | Skills |
|----------|--------|
| `<agent-handle>/utilities` | util-buy, util-draw, util-dreamhost, util-github, util-headhunter, util-iamwrite, util-rapidapi, util-reddit, util-telegram-miniapp, util-voice-call, util-vpn, util-web-extract, util-wiki |

## Sync Procedure for Monorepo Skills

1. Clone monorepo: `git clone https://github.com/<agent-handle>/utilities.git /tmp/utilities`
2. Copy skill files: `cp ~/.hermes/skills/<skill>/SKILL.md /tmp/utilities/<subdir>/SKILL.md`
3. Sync references: `rsync -a --delete ~/.hermes/skills/<skill>/references/ /tmp/utilities/<subdir>/references/`
4. Commit and push monorepo: `cd /tmp/utilities && git add -A && git commit -m "sync: update <skill>" && git push origin local`
5. Do NOT add `.git` to the local skill directory — it's a copy, not a standalone repo

## Lesson (2026-06-22)

10khr sync created 13 standalone repos for util-* skills that should all be in the `utilities` monorepo. Root cause: agent didn't read the `source:` field before deciding where to push. Always check `source:` before any git operation on a skill directory.