# 🦞 OpenClaw Skill: Infographic Generator

A professional OpenClaw skill that enables AI agents to automatically design and generate high-quality infographics, newsletters, and posters in Vietnamese using the best available image generation models (Recraft v3, Flux Ultra, Ideogram, etc.) routed via **9Router**.

---

## ✨ Features

- 🧠 **Dynamic Model Selection**: Queries 9Router's active image models and automatically selects the highest priority model available (falls back gracefully if models are offline).
- 📐 **Flexible Layouts & Ratios**: Supports Square (1:1), Vertical (2:3), and Landscape (16:9) aspect ratios based on natural language instructions.
- 🎨 **Curated Styling Guidelines**: Includes structured prompting strategies for editorial grids, warm/pastel card-based guides, and bold Neo-Brutalism themes.
- 🇻🇳 **Accurate Vietnamese Text**: Tailored font instruction sets to ensure seamless Vietnamese Unicode rendering without glyph clipping or errors.
- ⚙️ **Automatic API Configuration**: Seamlessly resolves 9Router API keys and base URLs by reading `openclaw.json` or fallback environment variables.

---

## 📋 Prerequisites

To run the generator script locally, your environment needs:

- **Node.js** (v18 or higher)
- Access to the internet to query the 9Router API endpoint.
- Valid API credentials in your `.openclaw` runtime setup or local environment.

---

## 📦 Installation

To install this skill into your OpenClaw agent's workspace:

```bash
openclaw skills install infographic-generator
```

---

## 🛠️ Usage

AI agents can execute the generator script using the built-in command execution tool:

```bash
node skills/infographic-generator/image-generator.js "<english_prompt>" <output_name>.png
```

### Example

```bash
node skills/infographic-generator/image-generator.js "An editorial news infographic in vertical poster format. At the top, a title reads 'CẨM NANG HƯỚNG DẪN'. Clean Montserrat font. Light pastel background. Designed by Williams - trợ lý của tuanminhhole" cẩm-nang.png
```

---

## 🔑 Environment Variables

The generator automatically reads from `openclaw.json`. Alternatively, you can override credentials using:

- `NINE_ROUTER_API_KEY`: Your 9Router API token.
- `NINE_ROUTER_BASE_URL`: Custom 9Router endpoint (defaults to `http://9router:20128/v1`).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

Made with 🦞 by [tuanminhhole](https://github.com/tuanminhhole)

</div>
