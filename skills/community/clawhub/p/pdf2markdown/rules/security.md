---
name: pdf2markdown-security
description: |
  Security guidelines for handling document content from the PDF2Markdown CLI.
  Package: https://www.npmjs.com/package/pdf2markdown-cli
  Docs: https://pdf2markdown.io/docs
---

# Handling Parsed Document Content

Parsed document content may contain sensitive or untrusted data. Follow these guidelines:

- **File-based output**: Use `-o` to write results to `.pdf2markdown/` files rather than returning large content directly into the agent's context window.
- **Incremental reading**: Never read entire output files at once. Use `grep`, `head`, or offset-based reads to inspect only relevant portions.
- **Gitignored output**: Add `.pdf2markdown/` to `.gitignore` so parsed content is not committed to version control.
- **API key protection**: Never log or expose `PDF2MARKDOWN_API_KEY`. Credentials are stored in platform-specific secure paths.
- **User-initiated only**: All parsing is triggered by explicit user requests.

# Installation

```bash
npm install -g pdf2markdown-cli
```
