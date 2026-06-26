# GitHub Repo Commander

Upgrade a repository from “looks fine” to “safe, polished, discoverable, and ready to share.”

中文说明：
- 技能定义见 [SKILL.md](./SKILL.md)
- 中文 README 见 [README.zh-CN.md](./README.zh-CN.md)

`github-repo-commander` is the unified GitHub command skill for maintenance, packaging, and open-source readiness. It combines presentation polish with governance checks so a repo can be:

- safer to open-source
- easier to understand at a glance
- easier to discover and recommend
- less tied to one specific LLM stack
- easier to submit to curated lists or community directories

## What it covers in one place

- README polish and first-screen cleanup
- repo description, topics, and metadata upgrades
- screenshots, demos, and presentation structure
- discoverability and positioning improvements
- privacy and secret scanning
- local path leak detection
- skill metadata compliance checks
- model-agnostic refactor guidance
- awesome-list contribution prep
- packaging workflow orchestration
- bilingual documentation governance
- upgrade-note discipline

## Why this is one skill

GitHub work is usually one continuous flow:

1. make it safe
2. make it clear
3. make it attractive
4. make it easier to discover

This package keeps `github-repo-polish`, `readme-generator`, and `ai-discoverability-audit` as optional supporting layers, but treats them as one repo-stewardship workflow instead of separate jobs.

## Files

- [SKILL.md](./SKILL.md): main skill instructions
- [README.zh-CN.md](./README.zh-CN.md): Chinese overview
- [CHANGELOG.md](./CHANGELOG.md): notable upgrades
- [skill.json](./skill.json): Manus-style metadata
- [scripts/repo_commander_audit.py](./scripts/repo_commander_audit.py): repo audit helper
- [agents/openai.yaml](./agents/openai.yaml): skill card metadata
- [_meta.json](./_meta.json): lightweight skill package metadata

## Audit example

```bash
python3 ./scripts/repo_commander_audit.py /path/to/repo
```

## License

MIT
