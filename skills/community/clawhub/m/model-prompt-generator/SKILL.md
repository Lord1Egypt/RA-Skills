---
name: model-prompt-generator
description: Generate English model prompts for AI image generation tools based on user-provided Chinese clothing descriptions, covering model appearance, outfit coordination, scene lighting, and photography style.
---

# Model Prompt Generator

Generate professional English fashion photography prompts for AI image generation tools based on clothing descriptions.

## Use Cases

Use when users need to "generate model prompts", "clothing shoot prompt", or "model image prompt".

## Workflow

### 1. Parse Clothing Description

Extract key information from user input:
- **Clothing Information**: Type, color, material, style, suitable season and occasion
- **User Preferences** (optional): Gender, age, ethnicity, scene, pose

### 2. Build Prompt

The generated English prompt must cover the following four dimensions:

#### Model Appearance
- Gender, approximate age (20s/30s/40s), ethnicity (East Asian/Black/Caucasian/South Asian, etc.)
- Body type (slim/athletic/curvy) and expression (confident/relaxed/elegant)
- Prioritize diversity and inclusivity when not specified

#### Overall Coordination
- Complement with reasonable accessories, footwear, and layered styling
- Bags, jewelry, outerwear, etc., ensuring style consistency and seasonal/occasional appropriateness

#### Scene & Lighting
- Background environment: urban street / minimalist studio / beach / runway, etc.
- Lighting effects: soft natural light / golden hour / studio lighting

#### Photography Style
- Shot type: full-body shot / three-quarter view / close-up
- Visual style: fashion editorial / e-commerce product photo / candid street style

### 3. Output

Output only one English prompt, nothing else:

```
[English prompt, ≤700 characters]
```

## Constraints

- Output only the English prompt; no Chinese explanations, titles, or additional notes
- Keep within 700 characters
- Language should be fluent, specific, and vivid, using professional fashion photography terminology
- Avoid stereotypes; advocate for diverse, modern, and authentic image representation
- If user input conflicts with conventional styling, prioritize user preferences