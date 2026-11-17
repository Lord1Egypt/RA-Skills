# Google Vertical Module Rules

## 1. Module Scope

Use this module for Google news, shopping, scholar, and patents.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. News and shopping
3. Scholar and patents

## 2. News and shopping

- Documentation: `https://docs.keyapi.ai/en/google/news.md`
- Documentation: `https://docs.keyapi.ai/en/google/shopping.md`
- Purpose: Retrieve current news or shopping/product search results.

### Best Suited For

- news monitoring
- commerce result comparison
- market scan

### Routing Rules

- Use news for current events/media coverage.
- Use shopping for commerce/product result surfaces.
- Use webpage extraction for selected result pages when needed.

## 3. Scholar and patents

- Documentation: `https://docs.keyapi.ai/en/google/scholar.md`
- Documentation: `https://docs.keyapi.ai/en/google/patents.md`
- Purpose: Retrieve academic literature or patent results.

### Best Suited For

- academic research
- patent landscape research
- technology/company research

### Routing Rules

- Use scholar for literature and patents for IP records.
- State the selected vertical in the final answer.

## 4. Common Workflows

- Vertical research: choose news/shopping/scholar/patents -> selected webpage extraction if needed.
