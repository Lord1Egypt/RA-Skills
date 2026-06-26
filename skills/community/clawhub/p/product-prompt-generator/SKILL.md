---
name: product-prompt-generator
description: Generate high-quality product image prompts for AI image generation tools based on user-provided product information. 
---

# Product Prompt Generator

Generate high-quality English image prompts for AI product image generation based on product information.

## Use Cases

Use when users need to "generate product prompts", "product image prompt", or "product photography prompt".

## Workflow

### 1. Understand Requirements

Parse user-provided product information:
- Product type, material, color, dimensions
- Key features and selling points
- If reference images are provided, use the `image` tool to analyze and extract key visual features

### 2. Generate Prompt

Generate prompts incorporating product features, including the following elements:

#### Product Subject
- Single subject; do not include multiple products
- Accurately describe product appearance, material, color, and details
- Highlight key selling points

#### Photography Style
- Default: cinematic lighting, ray tracing
- If the user specifies a style, follow their requirements
- High resolution, commercial photography quality

#### Background & Composition
- Clean and simple background that highlights the product
- Appropriate composition ratio

### 3. Keyword Optimization

- Embed category keywords to improve discoverability
- Keep language fluent and natural; avoid keyword stuffing
- Do not introduce false or misleading descriptions

### 4. Output

Output the English prompt directly without additional notes:

```
[English prompt, ≤500 characters]
```

## Multi-Domain Support

Supports various product types: electronics, home goods, beauty products, apparel, food, sports equipment, etc. For unfamiliar categories, use search tools to obtain relevant knowledge.

## Constraints

- Prompt ≤500 characters
- Accurately reflect product features; do not add false information
- Keep it concise and fluent; avoid keyword stuffing
- Single product subject
- Objective description; do not introduce personal opinions or bias