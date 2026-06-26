---
name: llm-wikimind-mcp
version: 1.0.0
description: "Install and configure the LLM-WikiMind MCP server — a local knowledge base built on Karpathy's LLM Wiki pattern. Triggers: install wikimind, setup knowledge base MCP, configure wiki-kb, llm-wikimind setup, 安装知识库 MCP, 配置 wiki-kb, 搭建个人知识库."
author: HAL-9909
homepage: https://github.com/HAL-9909/llm-wikimind
license: MIT
tags: ["knowledge-base", "MCP", "wiki", "second-brain", "local-first", "llm-wiki", "karpathy", "BM25", "setup"]
requires:
  bins: ["python3", "git"]
  env: []
  os: ["darwin", "linux"]
---

# LLM-WikiMind MCP Setup Skill

Set up the [LLM-WikiMind](https://github.com/HAL-9909/llm-wikimind) MCP server — a local knowledge base built on [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

**What you get:** 5 MCP tools (`wiki_search`, `wiki_get`, `wiki_list`, `wiki_ingest_note`, `wiki_domains`) backed by BM25 full-text search over your local Markdown files. No embeddings, no vector DB, no cloud.

## Trigger phrases

- "Install WikiMind" / "Set up my knowledge base MCP"
- "Configure wiki-kb" / "llm-wikimind setup"
- "安装知识库 MCP" / "配置 wiki-kb" / "搭建个人知识库"

---

## Installation Workflow

### Step 1: Install the only dependency

```bash
pip3 install qmd
```

### Step 2: Clone the repo

```bash
git clone https://github.com/HAL-9909/llm-wikimind
cd llm-wikimind
```

### Step 3: Initialize the wiki

Run the interactive setup — it will ask where to store the knowledge base and handle everything else:

```bash
./wikimind init
```

**Options:**

| Command | When to use |
|---------|-------------|
| `./wikimind init` | Create a fresh wiki (interactive, asks for path) |
| `./wikimind init ~/my-notes --adopt` | Adopt an existing Markdown directory |

`init` automatically:
- Creates the standard wiki directory structure
- Copies the MCP server and watcher into the wiki
- Builds the initial BM25 search index
- Prints the exact config snippet to paste into the AI client

### Step 4: Register the MCP server

The `init` command prints the exact snippet. For reference:

**CatDesk / OpenClaw:**

```bash
catdesk mcp add --name wiki-kb --json '{
  "command": "python3",
  "args": ["<WIKIMIND_ROOT>/.wiki-mcp/server.py"],
  "env": {"WIKIMIND_ROOT": "<WIKIMIND_ROOT>"}
}'
```

Replace `<WIKIMIND_ROOT>` with the path chosen in Step 3 (e.g. `~/Documents/wiki`).

**Claude Desktop** — add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "wiki-kb": {
      "command": "python3",
      "args": ["<WIKIMIND_ROOT>/.wiki-mcp/server.py"],
      "env": { "WIKIMIND_ROOT": "<WIKIMIND_ROOT>" }
    }
  }
}
```

### Step 5: Start the auto-sync watcher

```bash
./wikimind start
```

Auto-start on login:

```bash
echo '/path/to/llm-wikimind/wikimind start > /dev/null 2>&1' >> ~/.zshrc
```

### Step 6: Verify

```bash
./wikimind status
```

Expected output:
```
→ Wiki root:  ~/Documents/wiki
✓ Wiki exists — 1 domain(s), 3 pages
✓ Watcher running (pid 12345)
✓ qmd installed
```

---

## MCP Tools Reference

Once registered, these 5 tools are available to any MCP-compatible AI client:

| Tool | Description |
|------|-------------|
| `wiki_search` | BM25 full-text search across all domains |
| `wiki_get` | Read a specific page in full |
| `wiki_list` | List pages by domain and/or type |
| `wiki_ingest_note` | Write a new page + rebuild index + sync cache |
| `wiki_domains` | List all registered domains and their trigger keywords |

---

## Auto-update: always in sync

The watcher runs in the background and keeps everything current automatically:

- Add a new domain folder → detected within 10 seconds → MCP tool descriptions updated
- Edit `DOMAIN.md` keywords → AI knows about the change in the next conversation
- AI writes a new page via `wiki_ingest_note` → index rebuilt automatically

No restarts. No manual config changes.

---

## Adding knowledge after setup

Install the companion ingest skill:

```bash
npx clawhub@latest install wikimind-ingest
```

Then just say: **"Add this to my knowledge base: [paste content or URL]"**

---

## Troubleshooting

**`qmd: command not found`** → Run `pip3 install qmd`

**MCP server not responding** → Check `./wikimind status` and ensure `WIKIMIND_ROOT` is set correctly

**Watcher not running** → Run `./wikimind start`; add to `~/.zshrc` for auto-start

**New domain not detected** → Ensure `DOMAIN.md` has a `keywords` frontmatter field; check `./wikimind status`
