---
name: ppt-afp
description: PPT全自动生成流（AFP：Auto-Flow Prompt）。用户提供主题和内容，Agent自动完成：风格选择 → 大纲生成 → Prompt生成 → AI生图 → 打包PPTX → 发送飞书。当用户说"帮我做PPT"、"生成幻灯片"、"制作演示文稿"、"ppt-afp"时触发。
version: 1.1.0
---

# PPT AFP — 全自动幻灯片生成流

> **角色**：你是顶级视觉设计师 + PPT产品经理，擅长将内容转化为震撼的演示文稿。

---

## ⛔ 执行前必读（三条铁律）

1. **每次执行前必须重新 read 本 SKILL.md**，不能凭印象走
2. **每完成一个阶段，显式报告**：说出"P阶段完成"再进入下一阶段
3. **每阶段结束对照下方 Phase Gate 逐条核查**，全部打勾才能继续

---

## 📊 进度仪表盘（每阶段更新）

```
PPT AFP 进度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P0 参数收集     [⬜/🔄/✅]
P1 风格确认     [⬜/🔄/✅]  风格：___  张数：___  受众：___
P2 大纲生成     [⬜/🔄/✅]  共___张已确认
P3 Prompt生成   [⬜/🔄/✅]  ___个prompt已确认
P4 AI生图       [⬜/🔄/✅]  ___/___张完成
P5 打包发送     [⬜/🔄/✅]  PPTX已发送
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## P0：参数收集

**收集以下信息（未提供则主动询问）：**

| 参数 | 说明 |
|------|------|
| 主题 | PPT的核心主题（必须） |
| 内容来源 | 已有大纲/文档路径，或从零开始 |
| 目标用途 | 直播/演讲/分享/内部汇报 |
| 张数偏好 | 不填则根据内容自动推荐（8-15张） |
| 是否发飞书 | 默认是 |

**Phase Gate P0：**
- [ ] 主题明确
- [ ] 内容来源确认
- [ ] 用途清晰

---

## P1：风格确认（⚠️ 必须让用户选，不能自行决定）

### Step 1：发送风格图鉴

**发送飞书预览文档链接，让用户直观浏览37种风格：**

> 📎 **风格图鉴文档**：https://sgl0nnj5ev.feishu.cn/docx/YV09dH7KHoKUGgxZKGVcm4MHnkf
>
> 打开后可以看到所有37种风格的预览图，按场景分类，每个风格都有编号和说明。

**发送话术示例（直接发给用户）：**
```
我为你准备了37种PPT风格预览 👉 https://sgl0nnj5ev.feishu.cn/docx/YV09dH7KHoKUGgxZKGVcm4MHnkf

打开看看，选一个你喜欢的编号（1-37）告诉我就行！
```

### Step 2：等待用户选择 + 确认参数

用户选择风格后，同时确认：
- **受众**：一般读者 / 初学者 / 专家 / 高管
- **张数**：推荐N张（基于内容量），用户可调整
- **是否审查大纲**：是/否（建议是）
- **是否审查Prompt**：是/否（建议否，节省时间）

### 风格编号速查表

| # | 风格名 | 分类 |
|---|--------|------|
| 1 | bold-editorial | 🔥 演讲 |
| 2 | dark-atmospheric | 🔥 演讲 |
| 3 | minimal | 🔥 演讲 |
| 4 | magazine-editorial-light | 🔥 演讲 |
| 5 | gradient-aurora | 🔥 演讲 |
| 6 | warm-gradient | 🔥 演讲 |
| 7 | corporate | 💼 商务 |
| 8 | notion | 💼 商务 |
| 9 | data-dashboard | 💼 商务 |
| 10 | isometric-3d | 💼 商务 |
| 11 | chalkboard | 📚 教育 |
| 12 | sketch-notes | 📚 教育 |
| 13 | scientific | 📚 教育 |
| 14 | blueprint | 📚 教育 |
| 15 | intuition-machine | 📚 教育 |
| 16 | storybook | 📚 教育 |
| 17 | watercolor | 🎨 创意 |
| 18 | vector-illustration | 🎨 创意 |
| 19 | fantasy-animation | 🎨 创意 |
| 20 | paper-cut | 🎨 创意 |
| 21 | bauhaus | 🎨 创意 |
| 22 | neon-pop | 🎨 创意 |
| 23 | candy-pastel | 🎨 创意 |
| 24 | neon-cyberpunk | 🔮 科技 |
| 25 | retro-synthwave | 🔮 科技 |
| 26 | terminal-hacker | 🔮 科技 |
| 27 | glassmorphism | 🔮 科技 |
| 28 | pixel-art | 🔮 科技 |
| 29 | ink-wash | 🏛 文化 |
| 30 | chinese-national-tide | 🏛 文化 |
| 31 | japanese-zen | 🏛 文化 |
| 32 | vintage | 🏛 文化 |
| 33 | earth-organic | 🏛 文化 |
| 34 | newspaper | ⚔️ 特殊 |
| 35 | military-tactical | ⚔️ 特殊 |
| 36 | brutalist | ⚔️ 特殊 |
| 37 | editorial-infographic | ⚔️ 特殊 |

**Phase Gate P1：**
- [ ] 已发送风格图鉴链接
- [ ] 用户已选择风格
- [ ] 受众已确认
- [ ] 张数已确认

---

## P2：大纲生成

**执行步骤：**

1. 创建工作目录：
   ```
   ~/Desktop/二饼文件夹/openclaw 二饼/slide-deck/{topic-slug}/
   ```

2. 调用 `baoyu-slide-deck` 生成大纲：
   - 读取 `~/.openclaw/skills/baoyu-slide-deck/references/outline-template.md`
   - 读取对应风格文件：`references/styles/{style}.md`
   - 按确认的张数、受众、语言生成 `outline.md`

3. **如果用户选择"审查大纲"**，展示大纲摘要表：

   ```
   | # | 标题 | 类型 | 布局 |
   |---|------|------|------|
   | 1 | xxx  | 封面 | title-hero |
   | 2 | xxx  | 内容 | ... |
   ```
   等待用户确认后继续。

**Phase Gate P2：**
- [ ] outline.md 已生成
- [ ] 用户已确认大纲结构（或跳过审查）

---

## P3：Prompt生成

**执行步骤：**

1. 读取 `~/.openclaw/skills/baoyu-slide-deck/references/base-prompt.md`
2. 为每张幻灯片生成 prompt 文件，保存到 `prompts/` 目录
3. 每个 prompt 包含：
   - base-prompt 内容
   - STYLE_INSTRUCTIONS（从 outline.md 提取）
   - 该张幻灯片的具体内容描述

4. **生成 batch.json**，格式：
   ```json
   {
     "jobs": 3,
     "tasks": [
       {
         "id": "01-slide-cover",
         "promptFiles": ["prompts/01-slide-cover.md"],
         "image": "01-slide-cover.png",
         "provider": "google",
         "ar": "16:9",
         "quality": "2k"
       }
     ]
   }
   ```

5. 如果用户选择"审查Prompt"，展示 prompt 列表等待确认

**Phase Gate P3：**
- [ ] 所有 prompt 文件已生成（数量 = 张数）
- [ ] batch.json 已生成
- [ ] 用户已确认（或跳过审查）

---

## P4：AI生图

**默认模型配置（已验证中文渲染正确）：**

```bash
# 从环境变量读取（已配置在 ~/.zshrc）
# GEMINI_API_KEY=<your-key>
# GOOGLE_BASE_URL=<your-url>
MODEL=gemini-3-pro-image-preview
```

**执行命令：**
```bash
cd {工作目录} && \
NODE_TLS_REJECT_UNAUTHORIZED=0 \
npx -y bun ~/.openclaw/skills/baoyu-image-gen/scripts/main.ts \
  --batchfile batch.json --jobs 3 \
  --provider google --model gemini-3-pro-image-preview
```

**实时报告进度：** 每完成3张报告一次 "已完成 X/N 张"

**Phase Gate P4：**
- [ ] 所有图片生成成功（Succeeded: N，Failed: 0）
- [ ] 图片分辨率正确（应为约 2752×1536）

---

## P5：打包 & 发送

**步骤1：用 merge-to-pptx.ts 打包**
```bash
cd {工作目录} && \
NODE_TLS_REJECT_UNAUTHORIZED=0 \
npx -y bun ~/.openclaw/skills/baoyu-slide-deck/scripts/merge-to-pptx.ts .
```

**步骤2：移动到标准目录**
```
~/Desktop/二饼文件夹/openclaw 二饼/PPT/{主题名称}.pptx
```

**步骤3：发送飞书**（使用标准飞书API发送脚本）
```python
# 见 TOOLS.md 中的飞书发文件脚本
# USER = ou_74c5a7816fcb78172bfca68a7f7449e8
```

**步骤4：确认本地路径**

**Phase Gate P5：**
- [ ] PPTX 已生成（文件存在，大小 > 1MB）
- [ ] 已发送飞书（返回 code=0）
- [ ] 本地路径已告知用户

---

## 关键经验（血泪教训）

### ✅ 已验证可用的配置
- **生图模型**：`gemini-3-pro-image-preview`（中文完全正确，2752×1536高分辨率）
- **API**：通过环境变量 `GEMINI_API_KEY` 和 `GOOGLE_BASE_URL` 配置（见 ~/.zshrc）
- **merge-to-pptx.ts**：输出文件名为 `..pptx`（需要手动 cp 重命名）

### ❌ 已知问题
- `gemini-2.5-flash-image` 中文乱码 → 不要用
- `ar=16:9` 参数对某些模型无效 → gemini-3-pro 已解决
- merge-to-pptx.ts 输出路径是上一级目录的 `..pptx` → 用 find 找到后 cp

### 📐 一定要让用户选风格
- P1 是强制步骤，不能自行决定风格
- 展示风格对比表，让用户做选择

---

## 触发关键词

- "帮我做PPT"、"做个幻灯片"、"制作演示"
- "ppt-afp"、"启动PPT流程"
- 提供了内容/大纲并希望转成PPT
