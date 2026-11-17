# Threads Search Module Rules

## 1. Module Scope

Use this module for Threads top content and recent content search.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Top and recent content search

## 2. Top and recent content search

- Documentation: `https://docs.keyapi.ai/en/threads/search_top.md`
- Documentation: `https://docs.keyapi.ai/en/threads/search_recent.md`
- Purpose: Search Threads content by keyword using top or recent ordering.

### Best Suited For

- topic discovery
- fresh conversation monitoring
- high-visibility content scan

### Routing Rules

- Use top content when the user wants influential/high-visibility results.
- Use recent content when freshness matters.
- Route selected posts to content rules for detail/comments.

## 3. Common Workflows

- Topic monitor: top or recent search -> selected post detail -> comments if needed.
