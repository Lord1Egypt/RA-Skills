# Google Webpage Extraction Module Rules

## 1. Module Scope

Use this module for extracting webpage content from selected URLs.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Webpage extraction

## 2. Webpage extraction

- Documentation: `https://docs.keyapi.ai/en/google/webpage.md`
- Purpose: Extract a webpage from a URL for deeper analysis.

### Best Suited For

- summarizing selected search results
- source verification
- structured page extraction

### Routing Rules

- Use directly when the user provides a URL and wants page content.
- Use after search/vertical results when snippets are insufficient.
- Do not treat search snippets as full source content.

## 3. Common Workflows

- Source analysis: search or user URL -> webpage extraction -> summarize extracted facts.
