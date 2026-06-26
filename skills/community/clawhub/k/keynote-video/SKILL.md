---
name: keynote-video
description: >-
  PPT/演示文稿 → 播报视频。交互式内容评估 + LLM讲稿生成 + 风格化口语重写 +
  方案确认后自动合成。v2.0 架构：LLM管内容，脚本管技术。
  支持7种风格：新闻播报/资讯快报/技术汇报/技术培训/故事讲述/商业演讲/轻松闲聊。

read_when:
  - 用户说"生成视频"、"做视频"、"PPT转视频"、"把PPT做成视频"
  - 用户提供PPT文件要求生成播报视频
  - 用户提到"keynote-video"、"视频生成"

metadata:
  openclaw:
    emoji: 🎬
    priority: high
    category: video-generation
    tags:
      - ppt
      - video
      - tts
      - presentation
    conflicts_with:
      - keynote-video (v3.2 旧版)
---

# PPT to Video (Keynote) v2.0

> 将演示文稿 + 背景材料 → 风格化播报视频

**核心流程**:
```
输入评估 → 内容理解 → 风格确定 → 讲稿生成 → 方案确认 → 技术合成 → 质量验证
  (LLM)      (LLM)      (LLM)       (LLM)      (LLM)      (脚本)      (脚本)
 Phase 0    Phase 1    Phase 1     Phase 1     Phase 2    Phase 3    Phase 4
```

---

## 🚨 执行纪律（最高优先级）

1. **PHASE 分隔** — Phase 0-2 由 LLM 驱动（认知决策），Phase 3-4 由脚本驱动（技术合成）
2. **BLOCKING 步骤** — Phase 0（输入不足时）和 Phase 2（方案确认）⛔ 必须等待用户响应
3. **禁止跳过确认** — 未经 Phase 2 用户确认，不得调用 generate.js
4. **脚本做技术，LLM 做内容** — 脚本不判断风格、不改写讲稿、不做内容决策
5. **串行执行** — Phase 必须按顺序执行，不得跳跃
6. **讲稿必须是纯文本** — 不含 markdown 标记，直接喂给 edge-tts

---

## Phase 0: 输入评估

🚧 **GATE**: 用户提供了输入目录或文件

### 0.1 扫描输入

```bash
# 扫描所有相关文件
find <input_dir> -type f \( -name "*.pptx" -o -name "*.ppt" -o -name "*.pdf" -o -name "*.md" -o -name "*.txt" -o -name "*.docx" \) 2>/dev/null | sort

# 统计
ls -la <input_dir>
```

### 0.2 完整性评分

| 材料 | 必需 | 权重 | 评分规则 |
|------|------|------|----------|
| PPT 文件 | ✅ 必需 | - | 无则直接报错退出 |
| 讲稿 (notes/*.md) | ❌ 可选 | 40% | 按 PPT 页数比例 |
| 背景材料 | ❌ 可选 | 30% | 存在即满分 |
| 方案说明 | ❌ 可选 | 30% | 存在即满分 |

### 0.3 交互策略

```
≥80分 → 自动进入 Phase 1

50-79分 → 提示用户:
  "当前输入评分 {score}/100，讲稿覆盖 {n}/{total} 页。
   建议补充：{缺少项}
   [1] 直接继续（LLM 将基于现有材料生成）
   [2] 我稍后补充"
  → 确认后进入 Phase 1

<50分 → ⛔ BLOCKING，展示补充清单，等待用户
```

### 0.4 创建项目目录

在 `project/` 目录下创建独立项目文件夹，将用户输入文件拷贝到项目目录中，确保在"笼子"里操作：

```bash
# 项目名：日期 + 简短描述
PROJECT_NAME="ppt-$(date +%Y%m%d)-<short-desc>"
PROJECT_DIR="<workspace>/project/${PROJECT_NAME}"
mkdir -p "${PROJECT_DIR}/scripts_rewritten/"
mkdir -p "${PROJECT_DIR}/input/"

# 拷贝用户输入文件到项目目录（保护原始文件）
cp <input_dir>/*.pptx "${PROJECT_DIR}/input/" 2>/dev/null
cp <input_dir>/*.ppt "${PROJECT_DIR}/input/" 2>/dev/null
cp <input_dir>/*.pdf "${PROJECT_DIR}/input/" 2>/dev/null

# 如果有 notes 或背景材料，也拷贝
find <input_dir> -name "*.md" -o -name "*.txt" | while read f; do
  cp "$f" "${PROJECT_DIR}/input/"
done
```

**规则**：
- 所有操作在项目目录内进行
- 原始文件不被修改或删除
- 临时文件（截图、音频、视频片段）也放在项目目录的 `.temp/` 子目录下
- 项目完成后，用户可选择保留或删除项目目录

---

## Phase 1: 内容理解 & 讲稿生成

🚧 **GATE**: 输入评估通过，项目目录已创建

### 1.1 PPT 内容提取

```bash
python3 <SKILL_DIR>/scripts/extract_ppt_text.py "<PROJECT_DIR>/input/<pptx_file>" > "<PROJECT_DIR>/ppt_text.md"
```

### 1.2 风格确定

LLM 分析 PPT 内容后，向用户推荐风格（⛔ BLOCKING）：

```
根据内容分析，推荐以下风格：
[1] 技术培训 (tech_training) — 适合教程/概念讲解
[2] 故事讲述 (story) — 适合案例/场景代入
请确认或自选。
```

**6 种风格速查**：

| ID | 名称 | 适用 | 音色 | 语速 |
|----|------|------|------|------|
| `news` | 新闻播报 | 情报/资讯 | XiaoxiaoNeural | +30% |
| `news_brief` | 资讯快报 | B站情报视频 | XiaoxiaoNeural | +15% |
| `tech_report` | 技术汇报 | 方案/架构 | YunxiNeural | +20% |
| `tech_training` | 技术培训 | 教程/入门 | YunxiNeural | +15% |
| `story` | 故事讲述 | 案例/产品 | YunxiNeural | +10% |
| `business` | 商业演讲 | BP/路演 | YunjianNeural | +25% |
| `casual` | 轻松闲聊 | 团队分享 | XiaoyiNeural | +20% |

### 1.3 讲稿生成

LLM 读取：
1. `ppt_text.md`（PPT 文字）
2. 已有的 notes/*.md（如果有）
3. 背景材料（如果有）

为每页生成演讲稿，遵循 **通用规则 + 风格特定规则**：

**通用规则**（所有风格）：
- 纯文本输出，不含 markdown（**、#、|、` 等）
- 用标点控制节奏：逗号=短停，句号=正常停，破折号=强调
- 每 3-5 句换句号，给听众喘息
- 先重点后事实，每页开头一句话概括核心
- 特殊字符：数字转中文读法，缩写分开读，表格转叙述
- 每页标注预计时长（目标 10-30 秒）

**风格特定规则**（详见 DESIGN.md §1.3）：

每种风格有独立的句式、开场、过渡、结尾、语气规范。生成讲稿时必须严格遵守当前风格的写作规范。

### 1.4 保存讲稿

每页保存为独立纯文本文件：
```
<PROJECT_DIR>/scripts_rewritten/
├── 01_xxx.txt
├── 02_xxx.txt
├── ...
└── 19_xxx.txt
```

文件内容格式：
```
{纯文本讲稿内容，直接可喂 TTS}
```

### 1.5 生成方案总览

生成 `<PROJECT_DIR>/video_design_spec.md`（用于 Phase 2 确认）：

```markdown
# 📹 {项目名} - 视频生成方案

## 基础信息
| 项目 | 值 |
| PPT 总页数 | {n} |
| 讲稿覆盖 | {n}/{n} (100%) |
| 预计总时长 | {t} 秒 |

## 全局风格
| 风格 | {style_name} |
| 主音色 | {voice} |
| 语速 | {rate} |

## 逐页预览
| 页码 | 标题 | 内容类型 | 时长 | 讲稿预览 |
| 1 | ... | ... | ...s | "前25字..." |
...
```

同时生成脚本可读的 JSON：
```bash
# LLM 手动创建或生成 <PROJECT_DIR>/video_design_spec.json
```

JSON 结构：
```json
{
  "global": { "style": "tech_training", "styleName": "技术培训", "defaultVoice": "zh-CN-YunxiNeural", "rate": "+15%" },
  "pages": [
    { "num": 1, "title": "封面", "contentType": "封面", "pageStyle": "story", "voice": "zh-CN-XiaoxiaoNeural", "rate": "+15%", "duration": 15 }
  ]
}
```

---

## Phase 2: 方案确认

🚧 **GATE**: Phase 1 完成，方案总览已生成
⛔ **BLOCKING** — 必须等待用户确认

向用户展示 `video_design_spec.md`，等待响应：

```
请确认：
1. 确认生成 → 进入 Phase 3
2. 修改第X页 → 重新生成该页 → 再次确认
3. 调整风格/音色 → 更新设置 → 重新确认
```

用户确认后，进入 Phase 3。

---

## Phase 3: 技术合成

🚧 **GATE**: Phase 2 用户已确认

调用 generate.js，纯自动化执行：

```bash
node <SKILL_DIR>/scripts/generate.js \
  --slides "<PROJECT_DIR>/input/<pptx_file>" \
  --scripts-dir "<PROJECT_DIR>/scripts_rewritten/" \
  --output "<output_dir>" \
  --spec "<PROJECT_DIR>/video_design_spec.json" \
  --project-dir "<PROJECT_DIR>" \
  --keep-temp
```

脚本职责：
1. PPT 截图（LibreOffice → pdftoppm）
2. TTS 合成（edge-tts，直接读取纯文本）
3. 视频片段合成（ffmpeg）
4. 片段拼接（ffmpeg concat）

脚本不做：内容判断、风格检测、讲稿改写。

---

## Phase 4: 质量验证

🚧 **GATE**: Phase 3 完成

```bash
bash <SKILL_DIR>/scripts/verify_video.sh <output_video> <expected_pages>
```

检查项：
- 文件存在且 > 1MB
- H.264 + AAC 编码
- 1280×720 分辨率
- 页数匹配
- 每段音频 > 3 秒

生成 `VIDEO_COMPLETE.md` 报告，向用户输出结果。

---

## 🛠️ 依赖要求

```bash
# 必需
node --version          # v18+
python3 --version       # 3.8+
ffmpeg -version         # 5.0+
libreoffice --version   # 7.0+
edge-tts --version      # 7.0+

# Python 依赖
pip install python-pptx  # PPTX 文字提取
pip install PyMuPDF      # PDF 文字提取（可选）

# 系统依赖
sudo apt-get install poppler-utils  # pdftoppm
```

---

## ⚠️ 故障排除

| 问题 | 解决 |
|------|------|
| `extract_ppt_text.py` 报错 | `pip install python-pptx` |
| edge-tts 失败 | 检查网络；文本超长时分段合成 |
| 截图失败 | `libreoffice --version` 检查安装 |
| 视频合成失败 | `ffmpeg -version` 检查；检查截图/音频文件存在 |
| TTS 读出 markdown 符号 | 检查讲稿是否为纯文本，无 **/#/| 等标记 |

---

## 🔗 相关技能

- **pptx-master**: 专业 PPT 生成
- **fireworks-tech-graph**: 架构图生成

---

*版本: v2.0 | 架构参考: pptx-master 多阶段串行管道模式*
