---
name: product-pose-prompt-generator
description: Generate English image prompts for front-view product-holding character images based on user-provided text descriptions and image assets. 
---

# Product Pose Prompt Generator

Generate high-quality English image prompts for creating front-view images of characters holding products.

## Use Cases

Use when users need to "generate product character image prompts", "front-view product-holding prompt", or "product display image prompt".

## Workflow

### 1. Understand User Requirements

Carefully analyze user-provided text descriptions and image assets:
- Identify key elements: product appearance, character features (face, clothing, pose), background environment
- If reference images are provided, use the `image` tool to analyze and extract key visual information
- Confirm any special preferences (e.g., style, color tone, atmosphere)

### 2. Generate Prompt

Generate detailed English image generation prompts covering:
- **Character Description**: Facial features, hairstyle, clothing style, pose (specific way of holding the product)
- **Product Description**: Product appearance, color, material, brand features
- **Background Environment**: Indoor/outdoor, specific scene, lighting, atmosphere
- **Reference Elements**: If reference images were provided, indicate which elements to retain or draw from

### 3. Optimize Prompt

Refine the prompt:
- Use concise and clear English, avoiding ambiguity
- Ensure all key points mentioned by the user are covered
- Add appropriate style keywords to enhance expressiveness (e.g., lighting, composition, photography style)

## Output Format

Output only the English prompt, nothing else:

```
[English prompt]
```

## Constraints

- Prompts must be entirely based on user-provided content; do not add unapproved elements
- Prompts must be in English
- Prompt length must not exceed 300 words
- Output only the prompt itself, no explanations or notes
- Do not generate content involving illegal, pornographic, or violent material