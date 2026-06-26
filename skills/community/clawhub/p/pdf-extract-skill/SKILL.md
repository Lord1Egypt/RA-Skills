---
name: pdf-extract-skill
description: "OpenClaw PDF extraction skill using OpenDataLoader. Use when the user wants to extract and process PDF content for RAG, embeddings, or coordinate-based citations."
license: "Apache-2.0"
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["java","python3","opendataloader-pdf"],"runtimes":["Java 11+","Python 3.10+"]}},"clawdbot":{"emoji":"📄","requires":{"bins":["java","python3","opendataloader-pdf"],"runtimes":["Java 11+","Python 3.10+"]}}}
---
# SKILL: OpenClaw PDF Supercharger with OpenDataLoader

## 0) Modular Map (.md)
To improve maintainability and allow targeted calls to specific .md files, this skill relies on helper documents:

- CLI quick start: docs/quickstart-cli.md
- Security before install: docs/security-before-install.md
- OpenClaw ready profiles: docs/profiles-openclaw.md
- Hybrid + OCR: docs/hybrid-mode-ocr.md
- RAG and bounding-box citations: docs/rag-citations.md
- Troubleshooting: docs/troubleshooting.md

Usage rules:
- If the task is setup/startup: load quickstart-cli.md
- Before any installation: load security-before-install.md
- If the task is command execution by scenario: load profiles-openclaw.md
- If the task involves scanned or complex table PDFs: load hybrid-mode-ocr.md
- If the task is RAG/citations: load rag-citations.md
- If there are errors: load troubleshooting.md

## 1) Goal
This skill maximizes PDF reading quality for OpenClaw in ClawHub using OpenDataLoader PDF.

Pillars:
- Local extraction (no cloud) for privacy.
- High-quality reading order and structure (columns, tables, layout).
- RAG and LLM-ready outputs (json + markdown).
- Simple end-user flow (CLI, no MCP).

## 2) When to Use This Skill
Use this skill when the user needs to:
- Extract clean text from PDFs.
- Improve table and multi-column parsing.
- Prepare data for RAG, embeddings, or coordinate-based citations.
- Process scanned PDFs with OCR.
- Describe images/charts to make them searchable.

Do not use this skill for:
- OCR of standalone image files outside PDF workflows.
- Cloud-only pipelines where local Java execution is not allowed.

## 3) Core Architecture Rule (No MCP)
Since the MCP does not exist yet, this skill must operate with CLI only:
- Client command: opendataloader-pdf
- Hybrid backend command: opendataloader-pdf-hybrid

Do not create complex wrappers or intermediate services unless strictly needed.

## 4) Robust Prerequisites
Always validate before conversion:
- Java 11+ in PATH.
- Python 3.10+.
- Package install policy:
    - Do not use unpinned installs in production.
    - Use isolated environments (venv/container/VM).
    - Prefer pinned versions and verified sources.
    - See: docs/security-before-install.md

Quick checks:
- java -version
- pip index versions opendataloader-pdf
- pip show opendataloader-pdf
- opendataloader-pdf --help

If Java fails on Windows, reopen the terminal and verify PATH.

## 5) Standard OpenClaw Operating Flow
### Step A: Classify user intent
1. General reading/summary -> markdown
2. RAG with metadata and citations -> json,markdown
3. Complex tables or scanned PDF -> hybrid docling-fast
4. Charts with image descriptions -> hybrid + hybrid-mode full + enrich-picture-description

### Step B: Run in batches (required)
Always process multiple files in a single invocation to avoid JVM startup overhead per call.

Recommended example:
opendataloader-pdf file1.pdf file2.pdf ./folder/ -o ./output -f json,markdown

### Step C: Return a simple OpenClaw response format
Suggested response:
1. Status: ok or warning
2. Processed files
3. Output path
4. Generated formats
5. Suggested next action

Template:
"Processing completed. N PDFs were converted to ./output with json,markdown format. If you want, I can now extract specific pages or enable OCR for scanned files."

## 6) Ready-to-Use CLI Profiles
### Profile 1: Fast LLM reading
opendataloader-pdf ./pdfs/ -o ./output -f markdown

### Profile 2: Recommended for RAG
opendataloader-pdf ./pdfs/ -o ./output -f json,markdown

### Profile 3: Specific pages only
opendataloader-pdf report.pdf -o ./output -f json --pages "1,3,5-7"

### Profile 4: Sensitive data sanitization
opendataloader-pdf report.pdf -o ./output -f markdown --sanitize

### Profile 5: Preserve line breaks
opendataloader-pdf report.pdf -o ./output -f markdown --keep-line-breaks

### Profile 6: Embedded or external images
opendataloader-pdf report.pdf -o ./output -f json --image-output external
opendataloader-pdf report.pdf -o ./output -f json --image-output embedded

## 7) High-Precision Hybrid Mode
Use it when:
- Tables are complex or borderless.
- PDFs are scanned.
- Multi-language OCR is required.
- Image/chart descriptions are required.

### 7.1 Start backend
Standard:
opendataloader-pdf-hybrid --port 5002

Forced OCR:
opendataloader-pdf-hybrid --port 5002 --force-ocr

Multi-language OCR:
opendataloader-pdf-hybrid --port 5002 --force-ocr --ocr-lang "es,en"

With image descriptions:
opendataloader-pdf-hybrid --port 5002 --enrich-picture-description

### 7.2 Use backend from client
Hybrid auto mode:
opendataloader-pdf --hybrid docling-fast file1.pdf file2.pdf ./folder/ -o ./output -f json,markdown

With timeout and fallback:
opendataloader-pdf --hybrid docling-fast --hybrid-timeout 120000 --hybrid-fallback file1.pdf ./folder/ -o ./output -f json

Image descriptions enabled (full required):
opendataloader-pdf --hybrid docling-fast --hybrid-mode full file1.pdf ./folder/ -o ./output -f json,markdown

Critical note:
If the backend starts with --enrich-picture-description, the client must use --hybrid-mode full to include descriptions in output.

## 8) Key Robustness Parameters
- -f, --format: json, text, html, pdf, markdown, markdown-with-html, markdown-with-images
- --pages: page range (example: "1,3,5-7")
- --sanitize: anonymizes emails, phone numbers, IPs, cards, and URLs
- --reading-order xycut: keeps proper column reading order (recommended default)
- --use-struct-tree: improves extraction on tagged PDFs
- --table-method cluster: improves complex table detection
- --hybrid-url: backend endpoint (local by default)
- --hybrid-timeout: timeout in milliseconds (0 = no timeout)
- --hybrid-fallback: continue with Java mode if backend fails

## 9) Decision Matrix for OpenClaw
1. If the user wants speed and clean text: markdown.
2. If precise positional citations are needed: json (with bounding box) or json,markdown.
3. If output is empty/poor on scanned files: backend with --force-ocr.
4. If tables are very complex: enable --hybrid docling-fast.
5. If charts must be interpreted: backend with --enrich-picture-description and client with --hybrid-mode full.

## 10) Quick Troubleshooting
Problem: Java not found.
Solution: install Java 11+ and verify with java -version.

Problem: Hybrid backend connection error.
Solution: start opendataloader-pdf-hybrid in another terminal and verify port 5002.

Problem: Too slow.
Solution: process in batches, increase hybrid timeout, and verify backend RAM.

Problem: Mixed columns.
Solution: use default reading mode (xycut) and try --use-struct-tree for tagged PDFs.

Problem: Poor table quality.
Solution: use json output + hybrid mode.

## 11) Best Practices for ClawHub
- Prioritize simple, predictable commands.
- Answer users with short, actionable steps.
- Recommend json,markdown as default for assistants and RAG.
- Keep safety filters enabled (do not disable content safety unless explicitly requested).
- Store output in run-specific folders for traceability.

## 12) Skill Quality Checklist
- CLI-only architecture defined (no MCP).
- Clear installation and prerequisites.
- Execution profiles ready to copy/paste.
- Full hybrid flow with OCR and image descriptions.
- Fallback and troubleshooting strategy.
- Simple communication format for OpenClaw.

## 13) Credits
This skill uses and credits the excellent OpenDataLoader project:
https://opendataloader.org/

Official documentation used for this version:
https://opendataloader.org/docs