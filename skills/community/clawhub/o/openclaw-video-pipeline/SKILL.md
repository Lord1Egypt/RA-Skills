---
name: openclaw-video-pipeline
description: >-
  OpenClaw two-step pipeline: (1) expand a user brief into a three-shot storyboard
  and save it to storyboard/storyboard.json at project root, (2) run python3
  scripts/video-generate.py (defaults to that file) to call Zhipu CogVideoX-3 three
  times (10s each). Use when the user mentions OpenClaw, 分镜头, 30 秒短片,
  three-segment video, or storyboard-to-CogVideoX.
---

# OpenClaw：分镜头 → CogVideoX-3 视频（30s / 三次生成）

## 总览

目标：**总时长 30 秒**，拆成 **3 个分镜头**，每个镜头调用一次 **CogVideoX-3**（每次 **`duration: 10`** 秒），共 **3 次**异步生成。

| 步骤 | 执行方 | 产出 |
|------|--------|------|
| 1 | Agent（本 Skill） | 分镜头脚本写入 **`storyboard/storyboard.json`**（项目根目录下） |
| 2 | `python3 scripts/video-generate.py` | **默认读取**上述文件；三次 API 调用，得到 3 个视频 URL（可选落盘） |

**约定路径（项目根目录 = 与 `SKILL.md` 同级）**

- 第一步：若不存在则创建目录 **`storyboard/`**，将完整 JSON 写入 **`storyboard/storyboard.json`**。
- 第二步：在仓库根目录执行脚本；**不传 `--input` 时默认使用 `storyboard/storyboard.json`**。

```bash
export ZHIPUAI_API_KEY="你的密钥"
python3 scripts/video-generate.py --output-dir ./output_videos
# 显式指定输入（可选）：
# python3 scripts/video-generate.py -i storyboard/storyboard.json -o ./output_videos
```

## 第一步：生成分镜头脚本（提示词）

根据用户**原始创意/一句话需求**，生成符合下述 Schema 的 JSON，并**写入项目根下的 `storyboard/storyboard.json`**（先确保存在 `storyboard/` 目录）。除调试外不要使用其它默认路径。

### 约束

- **`segments` 必须恰好 3 条**，对应 3 次生成；每条对应 **10 秒** 画面。
- 每条 **`prompt`** 为可直接喂给 CogVideoX-3 的英文或中文描述，**单条 ≤ 512 字符**（API 限制）。
- 三条之间 **视觉与叙事连贯**：在每条中简要标注与前后段的衔接（主体、场景、光线、风格保持一致）。
- 可选 **`global_style`**：统一画风、画幅、时代感，三条 `prompt` 都应体现或引用该风格。
- 可选 **`user_brief`**：保留用户原始需求，便于追溯。

### JSON Schema（实例）

```json
{
  "user_brief": "用户原始描述",
  "global_style": "如：电影感、暖色、16:9 横屏、写实",
  "segments": [
    {
      "index": 1,
      "title": "镜头一（0–10s）",
      "prompt": "≤512 字，含景别、主体动作、环境、光线、风格，标明全片第 1/3 段"
    },
    {
      "index": 2,
      "title": "镜头二（10–20s）",
      "prompt": "承接镜头一结尾状态，第 2/3 段，≤512 字"
    },
    {
      "index": 3,
      "title": "镜头三（20–30s）",
      "prompt": "承接镜头二，收束或高潮，第 3/3 段，≤512 字"
    }
  ]
}
```

也支持简化形式（仅字符串数组，脚本会按顺序映射为三段）：

```json
{
  "prompts": ["第一段提示词", "第二段提示词", "第三段提示词"]
}
```

第一步完成后：**文件必须已保存为 `storyboard/storyboard.json`**，再进入第二步。

## 第二步：调用 `scripts/video-generate.py`

- **解释器**：`python3`
- **依赖**：标准库即可发起请求；若本机 Python 报 **SSL 证书验证失败**，请 `pip install certifi`（脚本会自动用其 CA 包）。通过 **HTTPS REST** 调用智谱开放平台（与 [视频生成异步接口](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E5%BC%82%E6%AD%A5) 一致）。
- **环境变量**：`ZHIPUAI_API_KEY`（必填）；可选 `BIGMODEL_API_BASE`（默认 `https://open.bigmodel.cn/api`）。

### 常用参数

| 参数 | 说明 |
|------|------|
| `--input` / `-i` | 分镜 JSON 路径；**默认 `storyboard/storyboard.json`**（相对当前工作目录） |
| `--output-dir` | 若指定，将每个片段视频下载为 `segment_01.mp4` … |
| `--quality` | `quality` 或 `speed`，默认 `quality` |
| `--size` | 如 `1920x1080`，默认 `1920x1080` |
| `--fps` | `30` 或 `60`，默认 `30` |
| `--with-audio` / `--no-audio` | 是否生成 AI 音效，默认开启 |
| `--poll-interval` | 轮询秒数，默认 `3` |
| `--timeout` | 单段任务最长等待秒数，默认 `600` |

脚本行为：对 **每一段** 依次 `POST /paas/v4/videos/generations`（`model=cogvideox-3`，`duration=10`），再用返回的 `id` 轮询 `GET /paas/v4/async-result/{id}` 直至 `SUCCESS` 或 `FAIL`； stdout 打印每段视频 URL，结束时打印一行 JSON 汇总。

## Agent 检查清单

- [ ] 第一步 JSON 中 **恰好 3** 条分镜，每条 **≤512** 字。
- [ ] 已提醒用户配置 **`ZHIPUAI_API_KEY`**，密钥不入库。
- [ ] 第一步已写入 **`storyboard/storyboard.json`**。
- [ ] 第二步在 **项目根目录** 执行，保证 `scripts/video-generate.py` 路径正确（默认会读 `storyboard/storyboard.json`）。
- [ ] 说明 **成片需后期拼接**：API 返回 3 个独立 10s 文件，需用剪辑软件或 `ffmpeg` 串成 30s（本 Skill 不要求脚本自动 concat，避免额外依赖）。

## 相关文档

- CogVideoX-3 能力与示例：[模型指南](https://docs.bigmodel.cn/cn/guide/models/video-generation/cogvideox-3)
- 异步接口与查询结果：[视频生成](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E5%BC%82%E6%AD%A5)、[查询异步结果](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%9F%A5%E8%AF%A2%E5%BC%82%E6%AD%A5%E7%BB%93%E6%9E%9C)
