---
name: manga-animation
description: >
  完整的漫剧（动画漫画）生成工作流 skill。当用户想要：创作漫画剧集、生成动画短片、制作分镜脚本、设计原创角色、生成动漫风格视频片段、将故事想法转化为可视化内容，或任何涉及"漫剧""动漫创作""分镜""人设""画风设定""AI生成动画""参考图生成"的请求时，必须使用此 skill。
  流程覆盖：剧本创作 → 分镜设计 → 人设+画风设定 → 分镜图生成（方舟图像）→ 视频生成（方舟图生视频）。每个阶段结束后必须等待用户确认再继续。即使用户只说"给我做个漫画动画"也应立即触发本 skill。
compatibility: "需要 bash_tool、create_file。Python 依赖：pip install 'volcengine-python-sdk[ark]' requests"
---

# 漫剧生成 Skill

## 核心原则

**每个阶段完成后必须暂停，展示产物，等用户确认或修改后再进入下一阶段。**
禁止一口气跑完所有阶段——用户需要在每个关卡看到结果并决定是否调整。

```
[阶段1] 剧本 ──→ ⏸ 用户确认
   ↓
[阶段2] 分镜表 ──→ ⏸ 用户确认
   ↓
[阶段3] 人设 + 画风 ──→ ⏸ 用户确认
   ↓
[阶段4] 分镜图生成（call_image_api.py）──→ ⏸ 用户确认图像质量
   ↓
[阶段5] 视频生成（call_video_api.py）
```

---

## 技术栈

| 用途 | 模型 | SDK 调用方式 |
|------|------|------------|
| 图像（人设图 + 分镜图） | `doubao-seedream-5-0-260128` | `client.images.generate` |
| 视频（图生视频） | `doubao-seedance-1-0-lite-i2v-250428`（调试）<br>`doubao-seedance-1-0-pro-250528`（正式） | `client.content_generation.tasks.create` |

**只需一个 Key**：`ARK_API_KEY`（方舟平台统一鉴权）

```bash
export ARK_API_KEY="your_key_here"
# 或在脚本顶部直接填写 ARK_API_KEY = "..."
```

---

## 阶段1：剧本创作

**参考：** `references/script-template.md`

- 若用户提供**完整剧本** → 跳过，直接进阶段2
- 若用户提供**创意/想法** → 输出：世界观、角色清单、三幕大纲、分场景剧本（含台词/动作/情绪）

保存：`output/[剧名]/script.md`

**⏸ 检查点**：展示剧本，询问是否调整，确认后进阶段2。

---

## 阶段2：分镜设计

**参考：** `references/storyboard-guide.md`

同时输出两个文件：

### storyboard.md（供人阅读）
完整分镜表格，见 storyboard-guide.md

### storyboard.json（供脚本调用）

```json
{
  "title": "剧名",
  "art_style_prefix": "",
  "shots": [
    {
      "shot_id": "S01_01",
      "duration": 4,
      "description_cn": "中文画面说明",
      "image_prompt": "静态画面的英文描述，不含运动",
      "video_prompt": "运动方式描述，如 character walking slowly forward",
      "characters": ["CHAR_001"],
      "dialogue": "台词/音效",
      "reference_image": null
    }
  ]
}
```

**image_prompt vs video_prompt 分工：**
- `image_prompt`：描述画面构成（景别、角色、场景、光线），用于生成静态分镜图
- `video_prompt`：只描述运动（镜头运动 + 角色动作），图生视频时用

**⏸ 检查点**：展示分镜表，提示用户此处调整最省钱，确认后进阶段3。

---

## 阶段3：人设 + 画风设定

**参考：** `references/character-guide.md`

### 3A. 输出角色人设卡：`characters/CHAR_001.md`

人设卡必须包含可直接用于 Prompt 的精确外貌描述，以及完整的图像生成 Prompt。示例结构：

```markdown
## CHAR_001 — [角色名]
年龄/性别/身份/性格关键词

### 外貌
发型发色 / 眼睛 / 体型 / 标志性特征（疤痕/纹路/配件）

### 服装（日常 / 战斗）

### 图像生成 Prompt（英文，完整可直接使用）
17-year-old teenage boy, [detailed appearance], [clothing],
full body front view, white background,
anime style, cel shading, shonen manga, high quality, masterpiece, sharp focus

ref_image_path:
```

### 3B. 确定画风，填入 storyboard.json

```json
"art_style_prefix": "anime style, shonen manga, cel shading, vibrant colors, high quality, masterpiece"
```

### 3C. ⚡ 关键步骤：更新脚本的 CHARACTER_PROMPTS

将角色 Prompt 填入 `call_image_api.py` 顶部的字典，每次有新角色都要更新：

```python
CHARACTER_PROMPTS = {
    "CHAR_001": "17-year-old teenage boy, black short hair, ..., full body front view, white background, anime style, ...",
    "CHAR_002": "...",
}
```

**⏸ 检查点**：展示所有人设卡 + 画风设定，确认 Prompt 准确描述了目标形象后进阶段4（开始消耗 API 额度）。

---

## 阶段4：分镜图生成

**脚本：** `scripts/call_image_api.py`
**API：** 方舟 `doubao-seedream-5-0-260128`，size=`2K`

### 运行命令

```bash
# Step 1：生成角色人设参考图
python call_image_api.py characters \
    --output output/[剧名]/characters/images/

# Step 2：生成分镜图（读取 storyboard.json 的 art_style_prefix + image_prompt）
python call_image_api.py storyboard \
    --input  output/[剧名]/storyboard.json \
    --output output/[剧名]/storyboard/frames/
```

脚本完成后自动将帧图路径写回 `storyboard.json` 的 `reference_image` 字段。

**⏸ 检查点**：引导用户打开 `storyboard/frames/` 查看图像，重点检查：
1. 角色外貌是否符合人设
2. 场景氛围/构图是否正确
3. 记录需要重生成的 shot_id（可单独重跑）

确认后进阶段5。

---

## 阶段5：视频生成

**脚本：** `scripts/call_video_api.py`
**API：** 方舟 `doubao-seedance-1-0-lite-i2v-250428`（lite，调试）

前置条件：`storyboard.json` 中所有 shot 的 `reference_image` 已填写。

### 运行命令

```bash
python call_video_api.py batch \
    --input  output/[剧名]/storyboard.json \
    --output output/[剧名]/videos/

# 如图片目录非默认，加 --frames-dir
python call_video_api.py batch \
    --input  output/[剧名]/storyboard.json \
    --output output/[剧名]/videos/ \
    --frames-dir output/[剧名]/storyboard/frames/
```

脚本工作流：提交任务 → 每8s轮询 → 成功后下载 .mp4 → 更新 generation_log.json。

### lite vs pro 切换

```python
# call_video_api.py 顶部修改这一行
ARK_VIDEO_MODEL = "doubao-seedance-1-0-lite-i2v-250428"   # 调试
ARK_VIDEO_MODEL = "doubao-seedance-1-0-pro-250528"         # 正式出片
```

---

## 输出文件结构

```
output/[剧名]/
├── script.md
├── storyboard.md
├── storyboard.json              ← 核心，贯穿阶段2-5
├── art_style.md
├── characters/
│   ├── CHAR_001.md
│   └── images/
│       └── CHAR_001_front.png
├── storyboard/
│   └── frames/
│       ├── S01_01.png           ← 阶段4产物 = 阶段5首帧
│       └── ...
├── videos/
│   └── S01_01.mp4
└── generation_log.json
```

---

## 常见问题快查

| 问题 | 解决方式 |
|------|---------|
| `❌ 未配置 ARK_API_KEY` | 脚本顶部填写，或 `export ARK_API_KEY=xxx` |
| `❌ 找不到参考图` | 先完成阶段4生成分镜图；或用 `--frames-dir` 手动指定 |
| 视频人物外貌与分镜图不符 | `video_prompt` 只描述动作，不重复角色外貌 |
| 图像风格不统一 | 检查 `storyboard.json` 的 `art_style_prefix` 是否已填写 |
| `volcengine SDK` 未安装 | `pip install 'volcengine-python-sdk[ark]' requests` |
