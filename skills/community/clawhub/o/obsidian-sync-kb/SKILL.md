---
name: obsidian-sync-kb
description: Build a searchable local knowledge base from an Obsidian vault's "笔记同步助手" inbox, then answer with citations, topic cards, update logs, and daily digests for OpenClaw. Use when users want to structure synced Obsidian notes into a retrieval-ready knowledge base.
---

# Obsidian Sync KB

Turn an Obsidian `笔记同步助手` inbox into a local retrieval-ready knowledge base for OpenClaw.

## Setup

Initialize the skill for a specific vault:

```bash
python3 scripts/setup_config.py --vault-root "/absolute/path/to/ClawVault"
```

The setup script writes `scripts/config.yaml`. You can also skip setup and set `OBSIDIAN_SYNC_KB_VAULT=/absolute/path/to/ClawVault`.

## Commands

Build or refresh the index:

```bash
python3 scripts/kb_tool.py build-index
python3 scripts/kb_tool.py build-index --force-full-rescan
python3 scripts/kb_tool.py build-index --disable-network
```

Query the inbox knowledge base:

```bash
python3 scripts/kb_tool.py query "怎么更好让 AI 做检索"
python3 scripts/kb_tool.py query "OpenClaw harness" --topic openclaw --format json
```

Promote and curate:

```bash
python3 scripts/kb_tool.py promote
python3 scripts/kb_tool.py star retrieval-rag --type topic
python3 scripts/kb_tool.py stats
```

## Behavior

- Treat the synced inbox as read-only source material.
- Build normalized docs, chunks, topic cards, update logs, and a daily change digest.
- Prefer source notes, original URLs, and `obsidian://` references before external search.
- Return `简要结论`, `相关文章`, `关键摘录`, and `引用来源`.
- Every citation must include the Obsidian path and original URL when available.
- If a hit is a `bad_capture` or `needs_manual_access`, make that explicit instead of treating it as a valid source.
