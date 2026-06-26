---
name: paper-parser-skill
description: CLI tool to search, download, and parse academic papers from arXiv into AI-friendly Markdown using MinerU API.
version: 0.1.4
author: KaiHangYang
homepage: https://github.com/KaiHangYang/paper-parser-skill
triggers: paper, arXiv ID, search, download, parse, agent-friendly
metadata:
  openclaw:
    requires:
      config:
        - ~/.paper-parser/config.yaml
      credentials:
        - MINERU_API_TOKEN  # MinerU API token for PDF parsing service
---

# Paper Parser Skill

CLI tool for automated academic paper processing.

## 🛡️ Data Privacy & Security

> [!IMPORTANT]
> **External Data Processing**: This skill transmits PDF files and paper metadata to [MinerU](https://mineru.net/) (opendatalab) for layout analysis and Markdown conversion. Please ensure you trust the service and understand their data handling policies before providing an API token in the configuration file.

**Security & Provenance:**
- **Open Source**: The full source code is available on [GitHub](https://github.com/KaiHangYang/paper-parser-skill).
- **Verified Package**: This tool is published on [PyPI](https://pypi.org/project/paper-parser-skill/) as a standard Python package.
- **Local Control**: All search results and downloaded PDFs are stored locally in your specified workspace.

**Before Installing:**
1. Review the source code at [GitHub](https://github.com/KaiHangYang/paper-parser-skill) for unexpected behavior.
2. Understand that **installing from PyPI executes third-party code** on your system — use a virtual environment or container to limit blast radius if desired.
3. The `MINERU_API_TOKEN` grants MinerU access to receive and process uploaded PDFs — use a dedicated, revocable token with minimal scope.
4. Avoid uploading sensitive, unpublished, or confidential documents to MinerU — review their privacy and data retention policies.
5. For sensitive documents requiring offline parsing, consider local alternatives that do not transmit PDFs externally.

## 🚀 Setup

> [!WARNING]
> Installing from PyPI executes third-party code. Use a virtual environment if you want to limit blast radius.

```bash
pip install paper-parser-skill==v0.1.3
```

## ⚙️ Configuration

Default path: `~/.paper-parser/config.yaml`

> [!IMPORTANT]
> `MINERU_API_TOKEN` is **required** for parsing functionality. Get a token at [mineru.net](https://mineru.net/).

```yaml
PAPER_WORKSPACE: "~/paper-parser-workspace"
MINERU_API_TOKEN: "your_token_here"  # Required for parsing
MINERU_API_BASE_URL: "https://mineru.net/api/v4"
MINERU_API_TIMEOUT: 600
```

## 📖 CLI Usage

Alias: `pp`

### Basic Commands

| Command | Argument | Description |
| --- | --- | --- |
| `pp search` | `<query>` | Search arXiv papers |
| `pp download` | `<id/query>` | Download PDF and metadata |
| `pp path` | `<id/query>` | Get local workspace path |

### Parsing Commands

> [!TIP]
> **Recommended for agent/automation use**: `pp submit` + `pp check` (non-blocking async workflow).
> `pp parse` and `pp all` block the process until cloud processing completes, which can take several minutes and may time out. Prefer the async approach when calling from an agent or pipeline.

| Command | Argument | Options | Description |
| --- | --- | --- | --- |
| `pp submit` | `<id/path>` | `--force` | **[Async ✅]** Submit PDF for parsing and return immediately. Idempotent — safe to call repeatedly. If already submitted and pending, checks status instead of re-uploading. |
| `pp check` | `<id/path>` | — | **[Async ✅]** Check parse status once. Downloads results automatically when done. |
| `pp parse` | `<id/path>` | `--force` | **[Blocking ⚠️]** Parse PDF synchronously. Blocks until complete. May time out on slow jobs. |
| `pp all` | `<id/query>` | `--force` | **[Blocking ⚠️]** Full workflow (Search → Download → Parse). Blocks until complete. May time out on slow jobs. |

### Recommended Async Workflow (for agents)

```bash
# Step 1: Search for papers by keyword → pick an arXiv ID from results
pp search "retrieval augmented generation"
# → 1. Id: 2312.10997  Title: Retrieval-Augmented Generation for ...
# → 2. Id: 2401.00123  Title: ...

# Step 2: Submit for parsing and return immediately
#         (PDF is downloaded automatically if not already cached)
pp submit 2312.10997
# → ⬇️  Downloading PDF...
# → ✅ Submitted!  batch_id: xxxxxxxx

# (minutes later, the agent or user calls again)

# Step 3: Check status — downloads & extracts results automatically when done
pp check 2312.10997
# → "⏳ Still processing (state: running, 45s since submission)."
# → or "✅ Parsing complete!  📂 Results in: ~/paper-parser-workspace/2312.10997"
```

## 📂 Workspace Structure

```text
PAPER_WORKSPACE/
└── <arxiv_id>/
    ├── paper.pdf
    ├── title.md
    ├── summary.md
    ├── .parse_task.json       ← async task state (batch_id, status, timestamps)
    └── markdowns/
        ├── 01_Introduction.md
        └── images/
```

## 🛠️ Requirements

- Python >= 3.8
- `requests`, `click`, `PyYAML`, `arxiv`, `rapidfuzz`
- **MinerU API Token**: Required for the parsing stage. Add it to your `config.yaml` file. Get one at [mineru.net](https://mineru.net/).

