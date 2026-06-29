---
name: image-analyzer-advisor
description: Analyze images and provide detailed visual insights, object detection, composition analysis, and actionable recommendations. Use when the user shares or references an image file or URL and wants detailed analysis, understanding of visual content, or suggestions for improvement. Triggers on requests like: "analyze this image", "what's in this photo", "examine this screenshot", "analyze this chart/graph/diagram", "what does this image show", "look at this image and tell me", or any request to inspect, describe, or get insights from an image. Also use when working with image URLs or file paths that need visual examination.
---

# Image Analyzer Advisor

Analyzes images using the `image` tool and provides structured visual insights + actionable recommendations.

## How It Works

1. **Receive image** — Get image path or URL
2. **Analyze** — Call `image` tool with the image and a detailed analysis prompt
3. **Structure response** — Format findings into: Visual Elements, Composition, Quality, Insights, Recommendations

## Analysis Framework

### Visual Elements
- Primary subjects and objects
- Colors, lighting, mood
- Text or data present (if chart/diagram)
- Notable details or anomalies

### Composition
- Framing and layout
- Balance and focus
- Depth and perspective

### Quality Assessment
- Resolution and clarity
- Exposure and color accuracy
- Noise or artifacts

### Insights & Recommendations
- What the image communicates
- Areas for improvement (if relevant)
- Actionable next steps

## Output Format

```
## 🎨 Image Analysis

### Visual Elements
- ...

### Composition
- ...

### Quality
- ...

### Insights
- ...

### Recommendations
- ...
```

## Tips
- Always include the image path/URL in your response for context
- For screenshots, note any UI elements or text
- For charts, extract key data points and trends
- For photos, focus on subject, lighting, and composition