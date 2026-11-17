# Google Search Module Rules

## 1. Module Scope

Use this module for Google web search and autocomplete query expansion.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Web search
3. Autocomplete

## 2. Web search

- Documentation: `https://docs.keyapi.ai/en/google/search.md`
- Purpose: Retrieve Google web search results for a query.

### Best Suited For

- source discovery
- SERP research
- general web research

### Routing Rules

- Use for general web search when no more specific vertical is requested.
- Use webpage extraction for selected results when snippets are insufficient.
- Keep search-result facts separate from extracted-page facts.

## 3. Autocomplete

- Documentation: `https://docs.keyapi.ai/en/google/autocomplete.md`
- Purpose: Generate search suggestions from a seed query.

### Best Suited For

- keyword expansion
- search intent exploration
- query refinement

### Routing Rules

- Use before search when the user asks for ideas or query expansion.
- Do not present autocomplete suggestions as ranking evidence.

## 4. Common Workflows

- Research: autocomplete when useful -> web search -> selected webpage extraction.
