# 漫剧生成 Skill

从一句创意到动画片段的完整流水线，**每个阶段都有检查点，可以看到当前结果并调整**。

---

## 快速上手

### 1. 安装依赖（只需一次）

```bash
pip install 'volcengine-python-sdk[ark]' requests
```

### 2. 配置 API Key

```bash
# 方式一：环境变量（推荐）
export ARK_API_KEY="your_key_here"

# 方式二：直接在脚本顶部修改
ARK_API_KEY = "your_key_here"
```

方舟平台获取 Key：https://console.volcengine.com/ark

### 3. 告诉 Claude 你的想法

安装 skill 后，直接说：
- "帮我做一个赛博朋克少年追查阴谋的漫剧"
- "我有这个剧本，帮我出分镜然后做成动画"

Claude 会引导你走完每个阶段，**每步都会暂停让你确认**再继续。

---

## 完整流程

```
阶段1  剧本      → 由 Claude 生成，用户确认
  ↓
阶段2  分镜表    → Claude 输出 storyboard.md + storyboard.json，用户确认
  ↓
阶段3  人设+画风 → Claude 输出人设卡 + 将 Prompt 填入脚本，用户确认
  ↓
阶段4  分镜图    → python call_image_api.py，用户查看图像质量
  ↓
阶段5  视频      → python call_video_api.py，输出 .mp4
```

---

## 脚本命令速查

### 阶段4：图像生成

```bash
# 生成角色人设参考图
python call_image_api.py characters \
    --output output/my_story/characters/images/

# 生成所有分镜图
python call_image_api.py storyboard \
    --input  output/my_story/storyboard.json \
    --output output/my_story/storyboard/frames/

# 检查点后，重新生成某一帧（调整 Prompt 后用）
python call_image_api.py single \
    --shot-id S01_03 \
    --input  output/my_story/storyboard.json \
    --output output/my_story/storyboard/frames/
```

### 阶段5：视频生成

```bash
# 批量生成所有镜头
python call_video_api.py batch \
    --input  output/my_story/storyboard.json \
    --output output/my_story/videos/

# 如图片目录非默认，手动指定
python call_video_api.py batch \
    --input  output/my_story/storyboard.json \
    --output output/my_story/videos/ \
    --frames-dir output/my_story/storyboard/frames/

# 重新生成某一帧视频（调整 video_prompt 后用）
python call_video_api.py single \
    --shot-id S01_03 \
    --input  output/my_story/storyboard.json \
    --output output/my_story/videos/
```

---

## 模型说明

| 用途 | 模型 | 说明 |
|------|------|------|
| 图像 | `doubao-seedream-5-0-260128` | 统一使用，size=2K |
| 视频（调试） | `doubao-seedance-1-0-lite-i2v-250428` | 速度快，适合调试 |
| 视频（正式） | `doubao-seedance-1-0-pro-250528` | 质量更高，出正式片用 |

切换视频模型：修改 `call_video_api.py` 顶部的 `ARK_VIDEO_MODEL`。

---

## 常见问题

**Q: 分镜图生成后视频里角色长相变了？**  
A: `video_prompt` 只写运动描述（如 `character walking slowly`），不要重复角色外貌。视频模型以图生视频，外貌由首帧图决定。

**Q: 某帧图像或视频质量不满意？**  
A: 用 `single --shot-id` 命令单独重新生成那一帧，不需要全部重跑。

**Q: 找不到参考图？**  
A: 脚本会自动在 `storyboard/frames/`、`frames/` 等目录下查找，也可以用 `--frames-dir` 手动指定。
