---
name: llms-txt-sniffer
description: Locate and utilize AI-friendly documentation index files (llms.txt, llms-full.txt) or sitemap.xml. Use when encountering documentation URLs (containing /docs/, /api-reference/, /guides/, or platform subdomains) to instantly map sites and reduce token burn.
metadata: {"openclaw": {"requires": {"bins": ["python3", "curl"]}, "version": "1.3.1"}}
argument-hint: [url]
allowed-tools: Bash, Read
---

# llms-txt-sniffer: The Smart Document Radar

This skill streamlines documentation ingestion by locating the most AI-optimized version of a site's content.

## 🧠 Why llms.txt?
It provides a high-density, Markdown-based index designed for LLMs to map entire sites instantly and save tokens.

## 🚀 Discovery Strategy (Two-Stage)

### Stage 1: Quick Jump Probes (Instructional)
1. **URL + /llms.txt**: Probe `{input_url}/llms.txt` using `curl -I`.
2. **Domain Root**: Probe `https://{domain}/llms.txt` using `curl -I`.

### Stage 2: Advanced Sniffing (Tool-based)
If Stage 1 fails, run the companion sniffer script located in this skill's directory:
`python3 sniffer.py $ARGUMENTS`

## 📜 Behavioral Rules
- **User-Initiated Only**: Only invoke this skill when the user explicitly provides a documentation URL. Do not autonomously scan domains.
- **Switch to High-Speed Mode**: Once an index is found, prioritize its links over manual scraping.
- **Index Summary**: Always present a brief structure overview.
- **Fallback**: Use `sitemap.xml` parser results if `llms.txt` is missing.
