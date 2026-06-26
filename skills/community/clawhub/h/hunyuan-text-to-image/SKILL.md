---
name: huny-img
description: 使用腾讯混元生图 3.0（HunyuanImage 3.0）生成图片。当用户需要调用混元/腾讯云生图、hunyuan 生图、huny-img 生图时，使用此 skill。调用 Python 脚本完成文生图（text-to-image）和图生图（image-to-image）任务，接口风格与 wanx-img skill 保持一致。
author: 申导
allowed-tools: Bash
---

## Overview

本 skill 通过调用腾讯云 AI Art API（混元生图 3.0）实现文生图和图生图功能。采用异步任务模式：先提交（SubmitTextToImageJob），再轮询查询（QueryTextToImageJob）直至完成。

## Workflow

1. 判断用户意图：文生图（无参考图）还是图生图（提供参考图 URL）
2. 解析图像分辨率：支持比例字符串或像素字符串，转换见下表
3. 若用户提供了参考图 URL/路径，直接将 URL 传入脚本的 `--images` 参数（无需下载）
4. 运行脚本生成图片（异步轮询，约 30–90 秒）
5. 输出：原始 prompt、扩写后 prompt（若开启改写）、分辨率、JobId、图片完整 URL

> ⚠️ 生成的图片 URL **有效期仅 1 小时**，务必在输出中完整展示，提醒用户及时保存。

---

## 分辨率对照表

文生图默认 `1024:1024`；宽高均需在 [512, 2048] 范围内，乘积 ≤ 1024×1024。

| 比例  | 像素尺寸  |
|-------|-----------|
| 1:1   | 1024:1024 |
| 3:4   | 768:1024  |
| 4:3   | 1024:768  |
| 9:16  | 720:1280  |
| 16:9  | 1280:720  |

图生图时若不传分辨率，模型将从 37 种预设尺寸中自动选择。

---

## Available Scripts

- `hunyuan3-text-to-image.py` — 文生图（支持可选参考图实现图生图），使用混元生图 3.0

---

## Setting Up

首次使用时，进入目录并安装依赖：

```bash
cd ~/.claude/skills/huny-img
python3 -m venv ~/.pyenv/versions/py312-huny-img
source ~/.pyenv/versions/py312-huny-img/bin/activate
pip install python-dotenv
cp .env.example .env
# 编辑 .env，填入 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY
```

后续执行脚本时，优先用：
```bash
~/.pyenv/versions/py312-huny-img/bin/python ./scripts/hunyuan3-text-to-image.py ...
```

若 venv 不存在，可直接用系统 python3（脚本仅依赖标准库 + python-dotenv）：
```bash
pip install python-dotenv --break-system-packages
python3 ./scripts/hunyuan3-text-to-image.py ...
```

---

## Usage Examples

**文生图（默认 1:1）**
```bash
~/.pyenv/versions/py312-huny-img/bin/python "./scripts/hunyuan3-text-to-image.py" \
  -p "雨中竹林小路，水墨风格"
```

**指定比例**
```bash
~/.pyenv/versions/py312-huny-img/bin/python "./scripts/hunyuan3-text-to-image.py" \
  -p "夕阳下的城市天际线，摄影风格" \
  -r 16:9
```

**指定像素尺寸 + 关闭 prompt 改写**
```bash
~/.pyenv/versions/py312-huny-img/bin/python "./scripts/hunyuan3-text-to-image.py" \
  -p "可爱的柴犬在草地上奔跑" \
  -r 768:1024 \
  --no-revise
```

**图生图（提供参考图 URL）**
```bash
~/.pyenv/versions/py312-huny-img/bin/python "./scripts/hunyuan3-text-to-image.py" \
  -p "参考图的风格，生成一幅秋日枫林场景" \
  --images "http://example.com/ref1.jpg" "http://example.com/ref2.jpg"
```

**固定随机种子（复现结果）**
```bash
~/.pyenv/versions/py312-huny-img/bin/python "./scripts/hunyuan3-text-to-image.py" \
  -p "星空下的雪山" \
  --seed 42
```

---

## Script Arguments

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--prompt` | `-p` | 文本描述提示词 | 示例花店 |
| `--resolution` | `-r` | 分辨率（比例或像素，如 `16:9` 或 `1024:768`） | `1024:1024` |
| `--seed` | — | 随机种子（正整数） | 随机 |
| `--logo` | — | 添加水印：0=否，1=是 | `0` |
| `--no-revise` | — | 关闭 prompt 改写（开启改写约增加 20s） | 默认开启 |
| `--images` | — | 参考图 URL 列表（最多 3 张） | 无 |
| `--poll-interval` | — | 轮询间隔秒数 | `5` |
| `--timeout` | — | 最长等待秒数 | `300` |

---

## Requirements

- Python 3.8+
- `python-dotenv`（其余全为标准库，无需安装 tencentcloud SDK）
- 腾讯云账号，已开通「腾讯混元生图」服务
- 在 `.env` 中配置：
  - `TENCENTCLOUD_SECRET_ID`
  - `TENCENTCLOUD_SECRET_KEY`
  - `TENCENTCLOUD_REGION`（可选，默认 `ap-guangzhou`）