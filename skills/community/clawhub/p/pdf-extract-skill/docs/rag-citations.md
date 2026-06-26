# RAG + Citations

## Recommended format
json,markdown

## Why
- json preserves semantic structure
- json includes bounding boxes per element
- markdown improves chunking and readability

## Minimum metadata per chunk (recommended)
- source
- page
- bounding box
- type

## Quick decision
- If you need text-only context: markdown
- If you need precise citations: json or json,markdown

## Best practices
- Keep safety filters enabled
- Process in batches
- Use hybrid mode for complex tables and OCR
