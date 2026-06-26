# Obsidian Note To Mind Map CN

[中文说明](./README_zh_CN.md)

Chinese-localized wrapper variant of the Obsidian note-to-mindmap workflow, defaulting to `PNG` output.

This bundle does not ship a renderer. It asks for explicit approval before installing the audited core skill `suka233/kmind-markdown-to-mindmap` from ClawHub, then delegates the actual conversion to that skill.

## What This Repo Contains

- `SKILL.md`: localized wrapper instructions and safety rules
- `agents/openai.yaml`: localized agent metadata
- `package.json`: version source for this publishable bundle

## Runtime Requirements

- A runtime that supports the `clawhub` CLI
- Network access only for the first-time audited core-skill installation
- After the core skill is installed, conversion follows the core skill's own runtime requirements

## Installation Behavior

If the audited core skill is missing, this wrapper should ask first and only then run:

```bash
clawhub install suka233/kmind-markdown-to-mindmap --workdir ./
```

It must not install any other skill.

## Safety Boundaries

- Only use pasted content or a user-provided single note path
- Do not scan the whole vault
- Do not read Obsidian global config files
- Do not rewrite, move, rename, or delete notes
- Do not suggest force-installing suspicious packages or skills

## Preferred Output

- Default output: `PNG`
- Use `.kmindz.svg` only when the user explicitly asks for an editable KMind map
- Use `SVG` only when the user explicitly asks for `SVG`

## Related

- Audited core skill: `https://clawhub.ai/suka233/kmind-markdown-to-mindmap`
- KMind Zen: `https://kmind.app`
- Skill id: `obsidian-note-to-mindmap-cn`
