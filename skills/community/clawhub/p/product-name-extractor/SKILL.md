---
name: product-name-extractor
description: Precisely extract product names from user-provided text, ignoring all irrelevant information and outputting only the product names. 
---

# Product Name Extractor

Precisely extract product names from text, outputting only the names themselves.

## Use Cases

Use when users need to "extract product names", "get product names", or "find product names in text".

## Workflow

### 1. Read Text

Receive any text provided by the user (product descriptions, articles, lists, conversations, etc.).

### 2. Extract Product Names

- Identify all product names appearing in the text
- Ignore all information other than product names (descriptions, prices, reviews, etc.)
- If the text contains multiple products, output one per line

### 3. Output

Output only product names, without any explanations, titles, or formatting:

```
[Product Name 1]
[Product Name 2]
```

If no product names are detected in the text, output `No product names detected`.

## Constraints

- Output content may only contain product names; no other information is allowed
- Keep output concise; do not add explanations or notes
- Do not fabricate or speculate about product names not present in the original text