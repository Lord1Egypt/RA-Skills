# iflow-nb

An [Agent Skills](https://agentskills.io) compatible skill for managing [iflow](https://iflow.cn) knowledge bases through AI agents.

## Features

- **Knowledge Base Management** - Create, list, update, delete, and share notebooks
- **File Import** - Upload local files (PDF, DOCX, TXT, Markdown, images) and import web URLs
- **Content Generation** - Generate reports (PDF/DOCX/Markdown), PPTs, podcasts, mind maps, and videos from your knowledge base
- **Web Search & Import** - Search the web or academic papers (arXiv, etc.), auto-import results, and generate summaries
- **Deep Research** - Multi-round web search with comprehensive research report generation
- **Semantic Search** - Deep content retrieval across your knowledge base
- **File Management** - List, rename, delete, and batch-manage files in notebooks

## Compatibility

This skill follows the open [Agent Skills](https://agentskills.io) standard and works with multiple AI agent platforms:

| Agent | Install Method |
|-------|---------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Copy to `~/.claude/skills/iflow-nb/` or `.claude/skills/iflow-nb/` |
| [OpenClaw](https://github.com/openclaw/openclaw) | `npx clawhub@latest install iflow-nb` |
| [Devin](https://devin.ai) | Commit to `.agents/skills/iflow-nb/` in your repo |
| [Windsurf](https://windsurf.com) | Copy to `.windsurf/skills/iflow-nb/` |
| [CrewAI](https://www.crewai.com) | `skills=["./iflow-nb"]` |

> For any agent that supports the Agent Skills standard, simply place this skill directory under the agent's skill discovery path.

## Setup

### 1. Get an API Key

Visit [platform.iflow.cn](https://platform.iflow.cn/profile?tab=apiKey) to create your API key.

### 2. Configure Credentials

Choose one of the following methods:

```bash
# Option A - Config file (recommended)
mkdir -p ~/.config/iflow-nb && echo "your_api_key" > ~/.config/iflow-nb/api_key

# Option B - Environment variable
export IFLOW_API_KEY="your_api_key"
```

The skill resolves credentials in order: environment variable > config file.

## Project Structure

```
iflow-nb/
├── SKILL.md                  # Main skill definition (entry point)
├── knowledge-base/
│   └── SKILL.md              # Knowledge base & file management APIs
├── reports/
│   └── SKILL.md              # Content generation APIs
├── search/
│   └── SKILL.md              # Web search APIs
├── scripts/
│   ├── iflow_common.py       # Shared utilities (auth, API helpers)
│   ├── pipeline_create_kb_and_generate.py    # Pipeline 1: Create KB + upload + generate
│   ├── pipeline_import_and_generate.py       # Pipeline 3: Import to existing KB + generate
│   ├── pipeline_search_and_generate.py       # Pipeline 2: Search KB + generate
│   ├── pipeline_semantic_search.py           # Pipeline 4: Semantic search + generate/share
│   ├── pipeline_file_management.py           # Pipeline 5: File list/rename/delete
│   └── pipeline_web_search.py                # Pipeline 6: Web search + import + generate
├── examples/                 # Usage examples for common workflows
│   ├── student-literature-review.md
│   ├── add-file-then-generate.md
│   ├── search-then-generate.md
│   ├── semantic-search.md
│   ├── text-import.md
│   ├── ppt-with-preset.md
│   ├── share-knowledge-base.md
│   ├── long-task-async.md
│   ├── web-search-fast.md
│   └── web-search-deep.md
└── references/
    └── api.md                # Full API reference
```

## Quick Examples

### Create a knowledge base, upload files, and generate a report

```
You: Create a KB called "Research Papers", upload these PDFs, and generate a literature review.
```

The agent runs Pipeline 1 behind the scenes:

```bash
python3 scripts/pipeline_create_kb_and_generate.py \
  --name "Research Papers" \
  --files "/path/to/paper1.pdf,/path/to/paper2.pdf" \
  --output-type "PDF" \
  --query "Generate a literature review comparing methodologies"
```

### Search the web for papers and import into your KB

```
You: Search for recent papers on LLM agents and create a summary report.
```

The agent runs Pipeline 6:

```bash
python3 scripts/pipeline_web_search.py \
  --kb "Research Papers" \
  --query "LLM agent latest research" \
  --source SCHOLAR \
  --output-type PDF
```

### Save a quick note

```
You: Record that I spent $50 on lunch today.
```

The agent auto-matches (or creates) the right notebook and imports via Pipeline 3.

### Share a knowledge base

```
You: Share the "Research Papers" notebook with my team.
```

The agent generates a read-only share link.

## Supported Output Types

| Type | Description |
|------|-------------|
| `PDF` | PDF report |
| `DOCX` | Word document |
| `MARKDOWN` | Markdown document |
| `PPT` | PowerPoint presentation (supports style presets) |
| `XMIND` | Mind map |
| `PODCAST` | Audio podcast |
| `VIDEO` | Video content |

## License

[MIT](LICENSE)
