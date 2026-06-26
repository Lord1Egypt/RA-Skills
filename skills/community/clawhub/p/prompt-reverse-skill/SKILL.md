---
name: prompt-reverse-skill
description: Convert image to structured prompts for multiple AI models
version: 1.0.0
tags: ["ai", "multimodal", "prompt", "image"]
---

# Prompt Reverse Skill

## Description

Convert an image into structured prompts using a category-aware prompt generation system.

This skill performs:

- Image understanding (multimodal analysis)
- Structured feature extraction (JSON)
- Visual type classification
- Style-aware prompt generation
- Multi-model prompt adaptation

---

## Visual Category System

This skill uses a **7-category visual classification framework**:

1. Photography  
2. Illustration  
3. 3D Render  
4. Typography / Logo  
5. Landscape  
6. Character Design  
7. General (fallback)

Each category applies **specialized prompt strategies**.

---

## Prompt Strategy by Category

### Photography
- camera lens (50mm, wide angle)
- lighting (cinematic, HDR)
- depth of field
- realism emphasis

### Illustration
- drawing style (anime, digital art)
- line quality
- color palette

### 3D Render
- rendering engine (octane, blender)
- material (PBR)
- lighting & shadows

### Typography / Logo
- layout design
- font style
- vector graphics

### Landscape
- composition (wide angle, perspective)
- atmospheric depth
- natural lighting

### Character Design
- face details
- pose and expression
- stylization

---

## Inputs

### image_path
Path to the input image.

---

## Outputs

### structured_data

```json
{
  "subject": "...",
  "style": "...",
  "lighting": "...",
  "color": "...",
  "composition": "...",
  "details": "..."
}