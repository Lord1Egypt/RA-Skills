# Personal Knowledge Base / Obsidian-Friendly Vault

## Principle

The vault is Markdown-first. Obsidian is optional.

- Without Obsidian: OpenClaw can still read/write Markdown.
- With Obsidian: user can visualize graph, backlinks, tags, and relationships.

## Recommended vault

```text
memory/wiki/
├── 00 Inbox/
├── 01 Projects/
├── 02 Areas/
├── 03 Resources/
├── 04 Concepts/
├── 05 People/
├── 06 Decisions/
├── 07 Workflows/
├── 08 Skills/
├── 09 Reviews/
└── 99 Archive/
```

## Karpathy-style three-layer knowledge flow

```text
Raw Capture → Distilled Knowledge → Actionable Workflow
```

Operational flow:

```text
Capture → Distill → Link → Operationalize → Archive
```

Mapping:

```text
00 Inbox       raw capture
04 Concepts    atomic knowledge cards
01 Projects    project context
07 Workflows   SOP / process / templates
08 Skills      skill drafts and skill design
99 Archive     stale/old material
```

## Obsidian instructions

Tell user:

```text
1. Install Obsidian: https://obsidian.md
2. Open Obsidian.
3. Choose “Open folder as vault”.
4. Select memory/wiki/.
5. Use Graph View to see knowledge graph.
```

Do not write `.obsidian/` by default. Only create optional Obsidian config if user explicitly chooses `--with-obsidian`.

## Knowledge-base health checks

Check:

```text
Inbox pile-up, empty notes, orphan notes, broken links, duplicate topics,
stale files, unlinked resources, high-frequency tasks not converted to SOP,
old SkillDrafts, unprocessed ContextCaptures.
```
