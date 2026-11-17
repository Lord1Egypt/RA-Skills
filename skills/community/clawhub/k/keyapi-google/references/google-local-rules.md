# Google Local Module Rules

## 1. Module Scope

Use this module for Google places, maps, and reviews.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Places and maps
3. Reviews

## 2. Places and maps

- Documentation: `https://docs.keyapi.ai/en/google/places.md`
- Documentation: `https://docs.keyapi.ai/en/google/maps.md`
- Purpose: Discover local places or map-surface results.

### Best Suited For

- local business discovery
- place comparison
- map-based research

### Routing Rules

- Use places for local discovery and place-oriented results.
- Use maps when the requested surface is map results.
- State location/language/market assumptions.

## 3. Reviews

- Documentation: `https://docs.keyapi.ai/en/google/reviews.md`
- Purpose: Retrieve review evidence for a selected place/business.

### Best Suited For

- reputation analysis
- review sampling
- local competitor comparison

### Routing Rules

- Use reviews only after the relevant place/review input is known.
- Keep review evidence separate from place discovery facts.

## 4. Common Workflows

- Local workflow: places/maps -> selected place -> reviews.
