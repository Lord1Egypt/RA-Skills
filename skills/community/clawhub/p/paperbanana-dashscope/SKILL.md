---
name: paperbanana-dashscope
description: Generate academic figures and scientific diagrams from paper text using a multi-agent pipeline powered by Alibaba Cloud DashScope (Qwen-VL + Wanxiang/Qwen-Image). Use when the user wants to create figures for research papers, visualize methods sections, generate architecture diagrams, or produce illustrations for academic content. Supports diagram and plot tasks with multi-round critic refinement.
---

# paperbanana-dashscope

Native TypeScript CLI for generating academic figures from paper text. Zero Python dependencies. Powered by Alibaba Cloud DashScope.

## Install & Update
```bash
npm install -g paperbanana-dashscope
paperbanana-dashscope --version
```

## Prerequisites

User must configure a DashScope API key. Check current status:
```bash
paperbanana-dashscope info
```

If no API key is configured, set one of:
```bash
# Option 1: Environment variable (simplest)
export OPENAI_API_KEY="sk-xxx"

# Option 2: Global config file
mkdir -p ~/.paperbanana-dashscope
cat > ~/.paperbanana-dashscope/config.yaml << 'YAML'
defaults:
  main_model_name: "qwen-vl-max"
  image_gen_model_name: "wanx2.1-t2i-turbo"
api_keys:
  openai_api_key: "sk-xxx"
YAML
```

## Basic Usage

Generate a single figure from text:
```bash
paperbanana-dashscope generate \
  --content "Method section text describing the architecture..." \
  --caption "Figure 1: System overview" \
  --output ~/Downloads/figure.png \
  --num-candidates 1
```

## Key Options

| Option | Description | Default |
|---|---|---|
| `--content <text>` | Paper text describing the method | required |
| `--caption <text>` | Figure caption | required |
| `--output <path>` | Output PNG file path | required |
| `--task <type>` | `diagram` or `plot` | `diagram` |
| `--num-candidates <n>` | Number of candidates to generate | `1` |
| `--max-critic-rounds <n>` | Critic refinement iterations | `3` |
| `--aspect-ratio <ratio>` | `1:1`, `16:9`, `4:3`, `21:9`, etc | `21:9` |
| `--main-model-name <id>` | VLM for planning/critic | `qwen-vl-max` |
| `--image-gen-model-name <id>` | Image generation model | `wanx2.1-t2i-turbo` |

## Available Image Models

DashScope supports three families of text-to-image models:

**Wanxiang legacy (fast, cheap):**
- `wanx2.1-t2i-turbo` (default, fastest)
- `wanx2.1-t2i-plus` (better quality)

**Wanxiang 2.7 (latest, highest quality):**
- `wan2.7-image-pro` (professional, supports 4K output in text-to-image)
- `wan2.7-image` (standard, supports up to 2K, same pricing as wan2.6)

**Wanxiang 2.x (previous generation):**
- `wan2.6-t2i` (flagship of 2.6 series)
- `wan2.5-t2i-preview`
- `wan2.2-t2i-flash` / `wan2.2-t2i-plus`

**Qwen-Image (best for figures with text labels):**
- `qwen-image-plus` (recommended for diagrams with English/Chinese labels)
- `qwen-image-max` (top-tier text rendering)

Switch models inline:
```bash
paperbanana-dashscope generate \
  --content "..." \
  --caption "..." \
  --image-gen-model-name wan2.6-t2i \
  --output figure.png
```

## Pipeline Modes

Use `--exp-mode` to control which agents run:

| Mode | Agents | Use case |
|---|---|---|
| `vanilla` | Vanilla only | Fastest, no refinement |
| `dev_planner` | Planner only | Just generate description |
| `dev_planner_critic` | Planner + Critic | With refinement loop |
| `dev_full` | Planner + Stylist + Visualizer + Critic | Full pipeline |
| `demo_full` | Same as dev_full + retriever | Default, best quality |

## Common Workflows

**Quick draft (fast, low cost):**
```bash
paperbanana-dashscope generate \
  --content "..." \
  --caption "..." \
  --output draft.png \
  --exp-mode vanilla \
  --image-gen-model-name wanx2.1-t2i-turbo
```

**High-quality figure for paper submission:**
```bash
paperbanana-dashscope generate \
  --content "..." \
  --caption "..." \
  --output paper_fig.png \
  --image-gen-model-name wan2.6-t2i \
  --num-candidates 3 \
  --max-critic-rounds 5
```

**Figure with English/Chinese text labels:**
```bash
paperbanana-dashscope generate \
  --content "..." \
  --caption "..." \
  --output labeled.png \
  --image-gen-model-name qwen-image-plus
```

## Troubleshooting

- **"未检测到任何 API Key"**: Run `paperbanana-dashscope info` and follow the configuration guide.
- **"size is not in the correct format"**: This is fixed in v1.0.2+. Run `npm update -g paperbanana-dashscope`.
- **"url error"**: Old version. Upgrade to v1.0.2+ for support of new wan2.6 / qwen-image models.

## Resources

- npm: https://www.npmjs.com/package/paperbanana-dashscope
- GitHub: https://github.com/TashanGKD/PaperBanana-DashScope
