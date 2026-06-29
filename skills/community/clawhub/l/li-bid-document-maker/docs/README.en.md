# li-bid-document-maker Usage Guide

> **Bid Document Expert** — Automatically convert tender documents into score-oriented professional bid response documents

## Installation

```bash
clawhub install li-bid-document-maker
```

## Quick Start

After installation, trigger the skill by saying any of the following to your AI assistant:

- "Create a bid response document"
- "Analyze this tender and generate a bid"
- "Help me prepare a bid submission"
- "Generate a response to this RFP"

The AI will automatically execute a 6-stage workflow: **Parse Tender → Strategy Analysis → Outline Generation → Chapter Writing → Quality Check → PDCA Auto-Improvement**

## Usage

### Method 1: Upload File

Drag and drop the tender document (PDF or Word) into the chat, then say:
> "Use li-bid-document-maker to analyze this document"

### Method 2: Specify File Path

> "Use li-bid-document-maker, tender file at /projects/tender.pdf"

## System Requirements

| Item | Requirement |
|------|-------------|
| OS | Windows 10/11, macOS, Ubuntu 20.04+ |
| AI Platform | Claude, OpenClaw, Hermes, or any LLM Agent with file I/O support |
| File Format | PDF (searchable preferred) or Word (.docx) |
| Dependencies | `python-docx`, `PyPDF2` (for file processing, optional) |

## Output

- Complete bid response document (16-chapter standard structure)
- PDCA quality improvement report
- Scoring criteria mapping with point values

## Workflow

```
Stage 1: Parse Tender        → Extract project info, technical specs, scoring criteria
Stage 2: Strategy Analysis   → Score weight analysis, competitive strategy
Stage 3: Outline Generation  → Score-oriented outline (user confirmation required)
Stage 4: Chapter Writing     → Write content section by section
Stage 5: Quality Check       → 6-dimensional full coverage check
Stage 6: PDCA Improvement    → 3 rounds of auto-improvement, then deliver
```

## License

MIT-0
