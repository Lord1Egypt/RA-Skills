---
name: latex-compiler
description: Compile LaTeX documents to PDF using pdflatex, xelatex, or lualatex with template support
metadata:
  openclaw:
    emoji: 📝
    tags: [latex, pdf, academic, writing, compilation]
    source: https://github.com/Prismer-AI/Prismer
    homepage: https://github.com/Prismer-AI/Prismer
    requires:
      bins: []
      os: [darwin, linux, win32]
      runtime: node
      services:
        - name: prismer-latex-server
          port: 8080
          description: LaTeX compilation server bundled in the Prismer container
          source: https://github.com/Prismer-AI/Prismer/tree/main/docker/base
---

# latex-compiler

Compile LaTeX documents to PDF. Accepts LaTeX source as content strings and returns compiled PDF via base64 or container-internal path.

## Prerequisites

This skill requires a LaTeX compilation server listening on `localhost:8080`. The Prismer project provides one as part of its container setup.

**Source & review:** The container source is at [github.com/Prismer-AI/Prismer/tree/main/docker/base](https://github.com/Prismer-AI/Prismer/tree/main/docker/base) (Apache-2.0). Before running, review the [Dockerfile](https://github.com/Prismer-AI/Prismer/blob/main/docker/base/Dockerfile) and [docker-compose.dev.yml](https://github.com/Prismer-AI/Prismer/blob/main/docker/docker-compose.dev.yml) to verify:
- No host filesystem volumes are mounted (the dev compose only maps ports)
- The container runs as a non-root user
- Only port 16888 (gateway) is exposed to the host

If the container is not running, all tool calls will fail with a connection error. The skill does not fall back to other local services or retry on different ports.

## Description

This skill sends LaTeX source strings via HTTP POST to `localhost:8080`. It supports pdflatex, xelatex, and lualatex engines, bibliography processing via biber, multi-pass compilation for cross-references, and starter templates.

**Data flow:** The skill sends only LaTeX content strings (from tool parameters) to the container via HTTP. It does not read host files, environment variables, or credentials. Output PDFs are generated inside the container at `/home/user/output/reports/` (container-internal path, not host-mounted). Use `latex_preview` to retrieve PDFs as base64 — no host filesystem mount is involved.

## Usage Examples

- "Compile this LaTeX document to PDF"
- "Preview the PDF output of my paper"
- "What LaTeX templates are available?"
- "Give me the IEEE template"
- "Compile this with xelatex for Chinese support"

## Process

1. **Choose template** — Use `latex_templates` to see available templates, then `latex_get_template` to get starter content
2. **Write LaTeX** — Edit the source document
3. **Compile** — Use `latex_compile` to generate the PDF (saved in container)
4. **Preview** — Use `latex_preview` to get an inline base64 PDF for display

## Tools

### latex_compile

Compile LaTeX source to PDF. The PDF is saved inside the container.

**Parameters:**
- `content` (string, required): Full LaTeX source code
- `filename` (string, optional): Output filename stem (default: `document`)
- `engine` (string, optional): `pdflatex` | `xelatex` | `lualatex` (default: `pdflatex`)
- `bibliography` (string, optional): BibTeX/BibLaTeX content (triggers biber)
- `runs` (number, optional): Compilation passes (default: 2 for cross-references)

**Returns:** `{ success, pdf_path, log, errors, warnings, compile_id }`

**Example:**
```json
{ "content": "\\documentclass{article}\\begin{document}Hello\\end{document}", "engine": "pdflatex" }
```

### latex_preview

Compile LaTeX source and return the PDF as base64 for inline preview.

**Parameters:**
- `content` (string, required): Full LaTeX source code
- `filename` (string, optional): Output filename stem (default: `document`)
- `engine` (string, optional): `pdflatex` | `xelatex` | `lualatex` (default: `pdflatex`)
- `bibliography` (string, optional): BibTeX/BibLaTeX content (triggers biber)

**Returns:** `{ success, pdf_base64, pdf_path, log, errors, warnings, compile_id }`

**Example:**
```json
{ "content": "\\documentclass{article}\\begin{document}Hello\\end{document}" }
```

### latex_templates

List available LaTeX templates and supported engines.

**Parameters:** None

**Returns:** `{ templates: string[], engines: string[] }`

### latex_get_template

Get the LaTeX source of a starter template.

**Parameters:**
- `name` (string, required): Template name — `article`, `article-zh`, `beamer`, `ieee`

**Returns:** `{ name, content }`

**Example:**
```json
{ "name": "ieee" }
```

## Notes

- Chinese documents (`article-zh`) require `xelatex` or `lualatex` engine
- Compilation timeout is 120 seconds per run
- Multi-pass compilation (default 2 runs) resolves cross-references and TOC
- If `bibliography` is provided, biber runs automatically between passes
- PDFs are saved to `/home/user/output/reports/` **inside the container** (not on the host)
- Use `latex_preview` to get PDF as base64 without needing host filesystem access
- No host filesystem mounts are required — all I/O is via HTTP to the container
- If localhost:8080 is unreachable, tools return a connection error (no fallback to other services)
