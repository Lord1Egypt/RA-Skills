---
name: pixel-asset-pipeline
description: AI pixel art sprite generation + processing pipeline for Godot games. Generate sprite sheets with Seedream, auto-process into Godot-ready assets (hframes, transparent PNG).
metadata:
  {
    "openclaw": {
      "emoji": "🎮",
      "requires": { "bins": ["python"] }
    }
  }
---

# 🎮 Pixel Asset Pipeline

AI 生成像素游戏素材 → 自动处理为 Godot 可用格式。

## Pipeline 概览

```
Prompt → AI生图(Seedream) → 去背景 → 切帧 → NEAREST缩放 → Godot sprite sheet + 单帧PNG
```

## 依赖

- Python 3.8+ with Pillow (`pip install Pillow`)

## Quick Start

```bash
# 1. 处理已有的大图
python scripts/process_sprite_sheet.py raw_sprite.png --output-dir ./out --target-size 48 --cols 4

# 2. 批量生成+处理
python scripts/batch_generate.py references/sample_config.json
```

## 支持的生成后端

| 后端 | 脚本 | 说明 |
|------|------|------|
| **Seedream** (默认) | `lumi-work/脚本/生图/seedream_generate.py` | 2048x2048，效果好 |
| 通义万相 | `lumi-work/脚本/生图/wanx_generate.py` | 备选 |
| Gemini | OpenClaw image_generate | 备选 |

## 输出格式

- `{name}_spritesheet.png` — 横排 sprite sheet，Godot 设置 `hframes=N` 即可
- `frames/{name}_frame_00.png` ~ `_frame_XX.png` — 单帧透明 PNG

## Prompt 技巧

像素风 prompt 模板（英文效果最佳）：

```
16-bit pixel art sprite sheet, [角色/物品描述], top-down RPG, [N] frames, white background, clean outline, no shading
```

示例：
- 角色：`16-bit pixel art sprite sheet, green slime monster, top-down RPG, 4 frames idle animation, white background`
- 物品：`pixel art, silver sword with blue glow, 16x16 icon, white background, game asset`
- 瓦片：`pixel art tileset, grass and dirt path, top-down RPG, seamless tiles, white background`

**关键后缀**：加 `white background` 或 `black background` 确保可去背景。

## 完整使用示例

1. 用 Seedream 生成：
   ```bash
   python lumi-work/脚本/生图/seedream_generate.py "16-bit pixel art sprite sheet, red dragon, 4 frames, white background" dragon_raw.png ""
   ```

2. 处理为 Godot 素材：
   ```bash
   python scripts/process_sprite_sheet.py dragon_raw.png --output-dir ./game_assets/dragon --target-size 64 --cols 4
   ```

3. 在 Godot 中：`Texture2D → Hframes = 4`，搞定。

## scripts/

- `process_sprite_sheet.py` — 单图处理（去背景→切帧→缩放→输出）
- `batch_generate.py` — 批量生成+处理（读JSON配置）
