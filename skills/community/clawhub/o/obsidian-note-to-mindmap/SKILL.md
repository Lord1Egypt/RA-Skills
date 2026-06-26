---
name: obsidian-note-to-mindmap
description: Turn a user-provided Obsidian note or Markdown outline into a KMind mind map PNG by default, and an editable KMind map on request. If the audited KMind core skill is missing, ask before installing it from ClawHub.
version: 0.1.0
user-invocable: true
metadata: {"openclaw":{"skillKey":"obsidian-note-to-mindmap","emoji":"🧠","requires":{"bins":["clawhub"]}}}
---

This skill is a thin Obsidian-to-KMind workflow wrapper.

Use it when the user wants to turn:

- a pasted Obsidian note
- a pasted Markdown outline
- a user-specified single note path

into a KMind mind map result, defaulting to `PNG`.

This wrapper does not bundle a renderer. It delegates the actual conversion to the audited core skill `suka233/kmind-markdown-to-mindmap`.

Required audited core skill:

- ClawHub slug: `suka233/kmind-markdown-to-mindmap`
- URL: `https://clawhub.ai/suka233/kmind-markdown-to-mindmap`

Safety and scope:

- Only operate on user-provided content or an explicitly provided single note path.
- Do not scan the vault.
- Do not read Obsidian global configuration files.
- Do not install plugins, packages, binaries, or other skills beyond the exact core skill named above.
- If the core skill is missing, ask for explicit confirmation before installing it.
- If the user declines, stop and provide the exact ClawHub URL instead of improvising another path.
- If the standard ClawHub installation flow is unavailable in the current runtime, stop and explain that limitation. Do not invent alternate installers.

Installation rule:

- Only after explicit user approval, install the exact audited core skill with the runtime's standard ClawHub install flow:
  `clawhub install suka233/kmind-markdown-to-mindmap --workdir ./`
- Never substitute another slug, including localized variants.

Confirmation message:

`This workflow uses the audited core skill suka233/kmind-markdown-to-mindmap to render the final KMind mind map. It is not installed yet. If you want, I can install that exact skill from ClawHub and then continue. I will not install anything else. Proceed?`

Workflow:

1. Confirm the input is pasted Markdown/text or a user-provided single note path.
2. If the input is a file path, read only that exact file.
3. Check whether the audited core skill is available.
4. If missing, ask for explicit confirmation before running the exact install command above.
5. After installation, hand off the content to `suka233/kmind-markdown-to-mindmap`.
6. Default to `PNG` when the user does not specify an output format.
7. Use `.kmindz.svg` only when the user explicitly asks for an editable KMind map.
8. Use `SVG` only when the user explicitly asks for `SVG`.
9. If the installed core skill reports missing Node.js or browser requirements, surface that result clearly instead of bypassing it.

Do not:

- scan the whole vault
- auto-discover notes
- read `~/Library/Application Support/obsidian/obsidian.json` or similar host config files
- rename, move, delete, or rewrite notes
- suggest force-installing any suspicious package or skill
- hide the installation step
