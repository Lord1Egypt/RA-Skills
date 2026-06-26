# IMA Knowledge AI

[![Version](https://img.shields.io/badge/version-1.0.3-blue.svg)](https://git.joyme.sg/imagent/skills/ima-knowledge-ai)
[![Category](https://img.shields.io/badge/category-productivity-green.svg)](https://clawhub.com)

> **Strategic guidance for IMA Studio multi-media content creation workflows**

## 🎯 What is This?

**ima-knowledge-ai** is a comprehensive knowledge base that helps AI agents make better decisions when creating content with IMA Studio's APIs. It provides strategic guidance on workflow design, model selection, parameter optimization, visual consistency, and production best practices.

**Important**: This skill does NOT make API calls — it provides knowledge to use with `ima-image-ai`, `ima-video-ai`, `ima-voice-ai` more effectively.

---

## 📚 Knowledge Structure

### Core Topics (8 files)

| Topic | File | Size | Use When |
|-------|------|------|----------|
| **Workflow Design** | `workflow-design.md` | 7.2 KB | Planning complex multi-step tasks |
| **Model Selection** | `model-selection.md` | 9.7 KB | Choosing between multiple models |
| **Parameter Guide** | `parameter-guide.md` | 12 KB | Optimizing generation parameters |
| **Visual Consistency** | `visual-consistency.md` | 12 KB | Creating series or character designs |
| **Video Modes** | `video-modes.md` | 31 KB | Understanding video generation modes |
| **Long Video Production** | `long-video-production.md` | 34 KB | Making 30s-3min videos |
| **Character Design** | `character-design.md` | 22 KB | Game/animation character assets & IP |
| **VI Design** | `vi-design.md` | 31 KB | Brand identity systems & applications |

### Specialized Directories (4 collections)

| Directory | Contents | Use When |
|-----------|----------|----------|
| **best-practices/** | 珠宝、护肤、香水、影视艺术案例 (4 guides) | Industry-specific workflows |
| **color-theory/** | 色彩心理、搭配、文化差异 (8 guides) | Color selection and psychology |
| **color-trends-2026/** | 2026 流行色、季节趋势 (5 guides) | Following current color trends |
| **design-pitfalls/** | Logo、海报、产品、Web 常见错误 (4 guides) | Avoiding common design mistakes |

**Total**: 8 core files + 21 specialized guides = **29 documents, ~220 KB**

---

## 🚀 Quick Start

### 1. Install the Skill

```bash
clawhub install ima-knowledge-ai
```

### 2. Read Before Acting

```
User Request → Query ima-knowledge-ai → Make Informed Decision → Call ima-*-ai
```

### 3. Example Usage

**Scenario**: User wants a 16:9 product poster with high quality

```markdown
Step 1: Read ima-knowledge-ai → parameter-guide.md
        Learn: SeeDream 4.5 supports 16:9, Nano Banana Pro for 4K

Step 2: Read ima-knowledge-ai → model-selection.md
        Choose: Nano Banana Pro 4K (best quality, 18pts)

Step 3: Call ima-image-ai with optimized parameters
        Success! 🎉
```

---

## 🔗 Related Skills

- **[ima-image-ai](https://git.joyme.sg/imagent/skills/ima-image-ai)** — Image generation
- **[ima-video-ai](https://git.joyme.sg/imagent/skills/ima-video-ai)** — Video generation
- **[ima-voice-ai](https://git.joyme.sg/imagent/skills/ima-voice-ai)** — Music generation
- **[ima-all-ai](https://git.joyme.sg/imagent/skills/ima-all-ai)** — Unified multi-media generation

---

## 📖 Quick Reference

### Core Knowledge

| Need | Read This |
|------|-----------|
| How to break down complex tasks? | `workflow-design.md` |
| Which model should I use? | `model-selection.md` |
| How to set resolution/aspect ratio? | `parameter-guide.md` |
| Keep visual consistency? ⭐ | `visual-consistency.md` |
| Understand video modes? | `video-modes.md` |
| Make 30s+ videos? | `long-video-production.md` |
| Character/IP design? | `character-design.md` |
| VI/brand identity? | `vi-design.md` |

### Specialized Knowledge

| Need | Explore This |
|------|--------------|
| Industry-specific workflows | `best-practices/` (jewelry, skincare, perfume, cinematic) |
| Color psychology & selection | `color-theory/` (psychology, combinations, cultural) |
| 2026 trending colors | `color-trends-2026/` (annual, seasonal, regional) |
| Common design mistakes | `design-pitfalls/` (logo, poster, product, web) |

---

## 📞 Support

- **GitLab Issues**: [ima-knowledge-ai/-/issues](https://git.joyme.sg/imagent/skills/ima-knowledge-ai/-/issues)
- **IMA Studio**: [imastudio.com](https://imastudio.com)

---

## 📜 License

MIT License — See LICENSE file for details.

---

**Version**: 1.0.3 (2026-03-05)  
**API**: IMA Studio Production (2026-02-27)

**Remember**: Knowledge is power when applied! 🍵
