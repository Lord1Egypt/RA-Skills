# PPT to Video (Keynote) v2.0 详细设计方案

> **核心原则**: LLM 做认知决策，脚本做技术合成
> **版本**: v2.0  
> **日期**: 2026-05-09  
> **状态**: 开发完成，待测试

---

## 一、架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    PPT to Video (Keynote) v2.0                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Phase 0  │───▶│ Phase 1  │───▶│ Phase 2  │              │
│  │ 输入评估  │    │ 内容理解  │    │ 方案确认  │              │
│  │ LLM驱动  │    │ LLM驱动  │    │ ⛔BLOCKING│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │                                  │                  │
│       ▼                                  ▼                  │
│  ┌──────────────────────────────────────────────┐           │
│  │               Phase 3                        │           │
│  │          技术合成（脚本自动化）                │           │
│  │    PPT截图 → TTS → 视频拼接 → 质量验证         │           │
│  └──────────────────────────────────────────────┘           │
│                           │                                  │
│                           ▼                                  │
│                  ┌────────────────┐                          │
│                  │   Phase 4      │                          │
│                  │  质量验证&输出  │                          │
│                  └────────────────┘                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 职责边界

| 层级 | 负责方 | 职责 |
|------|--------|------|
| **认知层** (Phase 0-2) | LLM（Agent） | 内容理解、讲稿生成、风格判断、方案设计、用户交互 |
| **技术层** (Phase 3-4) | 脚本（Node.js） | PPT截图、TTS合成、视频拼接、格式验证 |

**铁律**: 脚本不做内容决策，LLM 不做技术合成。

---

## 二、文件结构

```
keynote-video/
├── SKILL.md                          # 技能规范（LLM 执行指南）
├── DESIGN.md                         # 本设计文档
├── README.md                         # 用户说明
├── package.json                      # 依赖配置
├── LICENSE
├── .clawhub/
│   └── _meta.json                    # ClawHub 元数据
├── templates/
│   ├── video_design_spec.md          # 方案确认模板
│   └── script_page_template.md       # 单页讲稿模板
├── scripts/
│   ├── generate.js                   # 纯技术合成脚本（v2.0 重写）
│   ├── extract_ppt_text.py           # PPTX 文本提取
│   ├── screenshot_ppt.sh             # PPT 截图封装脚本
│   └── verify_video.sh               # 视频质量验证脚本
└── examples/
    └── video_design_spec_sample.md   # 方案确认示例
```

---

## 三、Phase 详细设计

### Phase 0: 输入评估

**执行方**: LLM（Agent）  
**阻塞条件**: 当输入不足时 ⛔ 需要用户提供

#### 0.1 输入扫描

LLM 执行以下命令扫描输入目录：

```bash
# 扫描所有相关文件
find <input_dir> -type f \( -name "*.pptx" -o -name "*.ppt" -o -name "*.pdf" -o -name "*.md" -o -name "*.txt" -o -name "*.docx" \) | sort

# 统计
ls -la <input_dir>
```

#### 0.2 完整性评分

| 材料类型 | 必需 | 权重 | 评分规则 |
|----------|------|------|----------|
| PPT 文件 (.pptx/.ppt/.pdf) | ✅ 必需 | - | 无则直接报错 |
| 讲稿文件 (notes/*.md) | ❌ 可选 | 40% | 按 PPT 页数比例计算 |
| 背景材料 (任意 .md/.txt) | ❌ 可选 | 30% | 存在即满分 |
| 方案说明 (README.md) | ❌ 可选 | 30% | 存在即满分 |

**总分 = 讲稿覆盖分 + 背景材料分 + 方案说明分**

#### 0.3 交互策略

```
完整 (≥80分):
  → 自动进入 Phase 1

可用 (50-79分):
  → 提示用户：
    "当前输入评分 {score}/100，讲稿覆盖 {n}/{total} 页。
     建议补充以下内容以获得更好的效果：
     - {缺少项1}
     - {缺少项2}
     
     请选择：
     [1] 直接继续（LLM 将基于现有材料生成讲稿）
     [2] 我稍后补充，先继续"
  → 用户确认后进入 Phase 1

不足 (<50分):
  → 阻塞，展示补充清单 ⛔ BLOCKING
  → 等待用户提供材料或确认继续
```

#### 0.4 输出

在 `project/` 目录下创建独立项目文件夹，将用户输入文件拷贝到项目目录中：
```
project/<project_name>/
├── input/                  # 用户输入文件副本
│   ├── presentation.pptx   # PPT 文件副本
│   ├── notes/              # 讲稿副本（如果有）
│   └── background.md       # 背景材料副本（如果有）
├── scripts_rewritten/      # LLM 生成的讲稿
│   ├── 01_xxx.txt
│   ├── ...
│   └── 19_xxx.txt
├── ppt_text.md             # PPT 提取的文字
├── video_design_spec.md    # 方案确认文档
├── video_design_spec.json  # 脚本配置 JSON
└── .temp/                  # 临时文件
    ├── screenshots/        # PPT 截图
    ├── audio/              # TTS 音频
    └── clips/              # 视频片段
```

**规则**：
- 所有操作在项目目录内进行，不影响原始文件
- 用户输入文件拷贝到 `input/` 目录
- 临时文件放在 `.temp/` 子目录
- 项目完成后，用户可选择保留或删除项目目录

---

### Phase 1: 内容理解 & 讲稿生成

**执行方**: LLM（Agent）

#### 1.1 PPT 内容提取

```bash
python3 scripts/extract_ppt_text.py <pptx_path> > <PROJECT_DIR>/ppt_text.md
```

`extract_ppt_text.py` 输出格式：
```markdown
## Slide 1
[标题]: AI Agent：从科幻到现实的智能革命
[正文]: ...

## Slide 2
[标题]: 开场
[正文]: ...
```

#### 1.2 风格确定（Phase 1 第一步）

LLM 根据 PPT 内容和用户意图，确定 **全局演讲风格**。这是讲稿生成的前提，必须在写讲稿前确定。

**6 种预定义风格**：

| 风格 ID | 风格名 | 适用场景 | 主音色 | 语速 |
|---------|--------|----------|--------|------|
| `news` | 新闻播报 | 每日情报、资讯简报、行业动态 | zh-CN-XiaoxiaoNeural | +30% |
| `news_brief` | 资讯快报 | B站AI资讯视频、科技情报播报、每日动态 | zh-CN-XiaoxiaoNeural | +15% |
| `tech_report` | 技术汇报 | 技术方案汇报、架构讲解、性能对比 | zh-CN-YunxiNeural | +20% |
| `tech_training` | 技术培训 | 教程、入门指南、概念讲解 | zh-CN-YunxiNeural | +15% |
| `story` | 故事讲述 | 案例分享、场景代入、产品故事 | zh-CN-YunxiNeural | +10% |
| `business` | 商业演讲 | 商业计划书、市场分析、投资路演 | zh-CN-YunjianNeural | +25% |
| `casual` | 轻松闲聊 | 团队分享、非正式讲解 | zh-CN-XiaoyiNeural | +20% |

**确定流程**：
1. LLM 分析 PPT 内容 → 自动推荐 1-2 个风格
2. 向用户展示推荐及理由 ⛔ BLOCKING
3. 用户确认或自选
4. 风格确定，进入讲稿生成

#### 1.3 讲稿生成（LLM 核心工作）

LLM 读取以下材料：
1. `ppt_text.md`（PPT 文字内容）
2. 已有的 notes/*.md（如果存在）
3. 背景材料（如果存在）
4. **已确定的全局风格**

然后为每页生成口语化演讲稿，遵循 **通用规则 + 风格特定规则**：

**通用规则（所有风格必须遵守）**：
```
1. 纯文本输出
   - 最终讲稿文件为纯文本 .txt
   - 不含任何 markdown/HTML/特殊标记（**、#、|、` 等）
   - 不使用特殊 TTS 标记（<break>、<prosody> 等）
   - 直接喂给 edge-tts，无需二次清洗

2. 节奏控制
   - 用标点符号控制停顿（逗号=短停，句号=正常停，破折号=强调）
   - 避免连续 3 个以上逗号无句号
   - 每 3-5 句换一个句号，给听众喘息时间

3. 先重点后事实
   - 每页开头用一句话概括核心信息
   - 先说结论/观点，再给数据/事实

4. 时长标注
   - 每页讲稿末尾标注预计朗读时长（秒）
   - 目标：每页 10-30 秒

5. 特殊字符处理
   - 数字："2026年"→"二零二六年"，"46.3%"→"百分之四十六点三"
   - 英文缩写："AI"→"A I"（字母分开读），"API"→"A P I"
   - 货币："$526亿"→"五百二十六亿美元"
   - 表格：转为叙述句式，不用行列罗列
```

**风格特定规则**：


##### 📰 资讯快报 (news_brief)
```
适用场景：B站 AI 资讯视频、科技情报播报、每日动态
主音色：zh-CN-XiaoxiaoNeural（女声，亲切有活力）
语速：+15%

句式：15-25字/句，节奏明快但不急促
结构：钩子 → 核心动态（3-5条） → 趋势洞察 → 互动引导

开场："今天 AI 圈发生了一件大事..." 或 "你可能没想到..."
      （口语化，有情绪，能留住观众）

内容组织：
  - 每条动态：一句话标题 + 核心事实 + 影响分析
  - 先结论后事实，每条不超过 50 字
  - 有观点、有判断，不做流水账

过渡："再看第二条..."、"第三条更重磅..."、"你以为这就完了？"
      （口语化，带动作感）

结尾："你觉得谁能赢？" 或 "你最期待哪个？在评论区告诉我"
      （必须抛问题引导评论）

语气：亲切、有活力、像朋友在分享情报
特色：有观点输出，不纯客观播报；用情绪词增加感染力
数字处理：保留关键数据，快速报出但不展开

禁忌：
  - 不要用"让我们想象一下"等故事化表达
  - 不要过于学术化或使用专业术语
  - 不要做成流水账式的信息罗列
```

##### 📰 新闻播报 (news)
```
句式：15-20字/句，简短有力
开场："各位好，今天是X月X日，一起来看今天的情报..."
结构：先结论（一句话概括），再补充事实和数据
过渡："接下来看..."、"再看..."、"另外..."
结尾："以上就是今天的全部内容..."
语气：客观、简洁、不拖泥带水
禁忌：不用"让我们想象一下"等故事化表达
数字处理：快速报数，不展开解释
```

##### 📊 技术汇报 (tech_report)
```
句式：20-30字/句，保持专业术语
开场："本次汇报的主题是X，主要包括三个方面..."
结构：背景→方案→数据→结论，逻辑清晰
过渡："从数据上看..."、"进一步分析..."、"对比可以发现..."
结尾："综上所述..."、"建议下一步..."
语气：严谨、专业、有数据支撑
特色：保留关键技术术语，不强行简化
数据呈现：先说数据结论，再给具体数字
```

##### 🎓 技术培训 (tech_training)
```
句式：15-25字/句，多用短句
开场："大家好，今天我们来学习一下X..." 或 "不知道大家有没有遇到过这种情况..."
结构：概念解释→生活类比→技术细节→实操例子
过渡："打个比方..."、"你可以这样理解..."、"我们来看一个例子..."
结尾："总结一下今天的要点..."、"回去可以试试..."
语气：亲切、耐心、像老师在讲课
特色：大量使用类比和日常例子，降低理解门槛
新概念：每引入一个概念，必须配一个类比或例子
```

##### 🎬 故事讲述 (story)
```
句式：长短结合，有节奏感
开场："让我给你讲一个故事..." 或 "想象一下这个场景..."
结构：场景铺垫→冲突/问题→转折→解决→启示
过渡："就在这时..."、"结果呢..."、"你猜怎么着..."
结尾："这个故事告诉我们..." 或 "所以我想说的是..."
语气：有感染力、像朋友在分享经历
特色：大量使用画面感描写、对话感、情绪词
节奏：关键情节处放慢语速（短句+句号），推动处加快（逗号串联）
```

##### 💼 商业演讲 (business)
```
句式：20-30字/句，有力量感
开场："今天我要和大家分享一个重要的机会..."
结构：痛点→方案→市场→收益→行动号召
过渡："这意味着..."、"数据告诉我们..."、"想象一下这个规模..."
结尾："现在是最好的时机..."、"加入我们..."
语气：自信、有力、有感染力
特色：强调价值、机遇、紧迫感
数据呈现：突出增长数字和市场空间
```

##### ☕ 轻松闲聊 (casual)
```
句式：15-25字/句，口语化
开场："嘿，今天来聊聊X这个话题..."
结构：自由展开，像聊天一样
过渡："对了..."、"还有个有意思的事..."、"你们觉得呢..."
结尾："好了今天就聊到这里..." 或 "大家有什么想法可以聊聊..."
语气：轻松、随意、像朋友聊天
特色：可以用反问句、感叹词、偶尔调侃
禁忌：不要太正式或学术化
```

#### 1.4 单页讲稿模板

`templates/script_page_template.md`：
```markdown
# 第 {n} 页 - 演讲稿

## 页面信息
- PPT标题: {slide_title}
- 内容类型: {content_type}  // 概念讲解 / 案例故事 / 数据展示 / 技术对比 / 总结号召 / 封面 / 过渡页
- 全局风格: {global_style}  // news / tech_report / tech_training / story / business / casual
- 页面风格: {page_style}     // 通常同全局，个别页面可微调
- 预计时长: {duration}s
- 推荐音色: {voice}

## 演讲稿（纯文本，直接用于 TTS）
{script_text}
```

#### 1.5 输出目录

```
<PROJECT_DIR>/
├── input/                  # 用户输入文件副本
├── scripts_rewritten/      # LLM 生成的讲稿
│   ├── 01_xxx.txt
│   ├── ...
│   └── 19_xxx.txt
├── ppt_text.md             # PPT 提取的文字
├── video_design_spec.md    # 方案确认文档
├── video_design_spec.json  # 脚本配置 JSON
└── .temp/                  # 临时文件（截图/音频/视频片段）
```

---

### Phase 2: 方案确认

**执行方**: LLM（Agent）  
**阻塞条件**: ⛔ BLOCKING — 必须等待用户确认

#### 2.1 生成 video_design_spec.md

LLM 根据 Phase 1 的产出，生成方案确认文档。

**模板** (`templates/video_design_spec.md`):
```markdown
# 📹 {项目名} - 视频生成方案

## 基础信息
| 项目 | 值 |
|------|-----|
| PPT 总页数 | {total_pages} |
| 讲稿覆盖 | {scripted}/{total_pages} ({coverage}%) |
| 预计总时长 | {total_duration} |
| 分辨率 | 1280×720 (16:9) |
| 输出格式 | MP4 (H.264 + AAC) |

## 全局风格
| 项目 | 值 |
|------|-----|
| 风格 | {main_style} ({style_name}) |
| 主音色 | {main_voice} |
| 语速 | {rate} |
| 风格特征 | {style_description} |

## 逐页预览
| 页码 | PPT标题 | 内容类型 | 页面风格 | 预计时长 | 音色 | 讲稿预览（前25字） |
|------|---------|----------|----------|----------|------|---------------------|
| 1 | {title} | {type} | {style} | {dur}s | {voice} | "{preview}..." |
| 2 | {title} | {type} | {style} | {dur}s | {voice} | "{preview}..." |
| ... | ... | ... | ... | ... | ... | ... |

## 确认事项
请确认以下内容：
- [ ] 全局风格选择合适（{main_style}）
- [ ] 讲稿内容准确，符合该风格的表达规范
- [ ] 音色选择合适
- [ ] 语速合适
- [ ] 预计时长可接受

请输入：
1. **确认生成** — 进入 Phase 3
2. **修改讲稿** — 告诉我要改哪些页
3. **调整设置** — 调整音色/语速等参数
```

#### 2.2 交互处理

```
用户输入 →
  "确认生成" / "1" / "可以" → 进入 Phase 3
  "修改第X页" → LLM 修改对应讲稿 → 重新展示该页 → 再次确认
  "调整音色" → 更新设置 → 重新确认
```

#### 2.3 输出

用户确认后，标记 Phase 2 完成，进入 Phase 3。

---

### Phase 3: 技术合成

**执行方**: 脚本（generate.js v2.0）  
**特点**: 纯自动化，无需用户干预

#### 3.1 脚本输入

```bash
node scripts/generate.js \
  --slides "<PROJECT_DIR>/input/<pptx_file>" \
  --scripts-dir "<PROJECT_DIR>/scripts_rewritten/" \
  --output "<output_dir>" \
  --spec "<PROJECT_DIR>/video_design_spec.json" \
  --project-dir "<PROJECT_DIR>"
```

参数说明：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--slides` | ✅ | PPT/PDF 文件路径（在项目 input/ 目录下） |
| `--scripts-dir` | ✅ | 纯文本讲稿目录 |
| `--output` | ✅ | 输出目录 |
| `--spec` | ❌ | 方案 JSON（包含音色/语速配置） |
| `--project-dir` | ✅ | 项目目录（临时文件放在此目录下） |
| `--keep-temp` | ❌ | 保留临时目录 |
| `--cleanup` | ❌ | 完成后清理临时文件 |

#### 3.2 合成流程

```
步骤 1: PPT 截图
  LibreOffice --headless --convert-to pdf
  pdftoppm -png -r 150
  输出: screenshots/01.png ~ 19.png

步骤 2: TTS 语音合成
  for each script in scripts_rewritten/:
    edge-tts --text "$(cat script.txt)" \
             --voice {voice} \
             --rate {rate} \
             --write-media audio/01.mp3
  输出: audio/01.mp3 ~ 19.mp3

步骤 3: 视频片段合成
  for i in 1..n:
    ffmpeg -loop 1 -i screenshots/{i}.png \
           -i audio/{i}.mp3 \
           -c:v libx264 -tune stillimage \
           -c:a aac -b:a 128k \
           -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
           -shortest clips/clip_{i}.mp4

步骤 4: 片段拼接
  ffmpeg -y -f concat -safe 0 \
         -i clips/files.txt \
         -c copy -movflags +faststart \
         output/final.mp4
```

#### 3.3 错误处理

```
截图失败:
  → 检查 LibreOffice 是否安装
  → 检查 PPTX 文件是否损坏
  → 尝试 pdftoppm 直接处理 PDF

TTS 失败:
  → 检查文本长度（edge-tts 单次有长度限制）
  → 过长文本自动分段合成再拼接
  → 检查网络连接（edge-tts 需要联网）

视频合成失败:
  → 检查截图和音频文件是否存在
  → 检查 ffmpeg 版本
  → 降级到逐页重新编码模式
```

---

### Phase 4: 质量验证 & 输出

**执行方**: 脚本（自动生成） + LLM（生成报告）

#### 4.1 自动检查项

```bash
bash scripts/verify_video.sh <output_video>
```

检查清单：

| 检查项 | 规则 | 失败处理 |
|--------|------|----------|
| 文件存在 | 输出文件存在且 > 1MB | 报错 |
| 编码格式 | H.264 video + AAC audio | 警告 |
| 分辨率 | 1280×720 | 警告 |
| 页数匹配 | clip 数 == PPT 页数 | 警告 |
| 音频时长 | 每段音频 > 3 秒 | 警告 |
| 音画同步 | 音频时长 ≤ 截图显示时长 | 提示 |
| 可播放 | ffprobe 能解析 | 报错 |

#### 4.2 输出目录

```
<output_dir>/
├── video_YYYY-MM-DD.mp4        # 最终视频
├── VIDEO_COMPLETE.md           # 完成报告
├── screenshots/                # PPT 截图（可选保留）
├── audio/                      # TTS 音频（可选保留）
└── clips/                      # 视频片段（可选保留）
```

#### 4.3 VIDEO_COMPLETE.md

```markdown
# 📹 视频生成完成报告

## 基本信息
- 文件名: video_YYYY-MM-DD.mp4
- 大小: {size} MB
- 时长: {duration} 秒
- 分辨率: 1280×720
- 编码: H.264 + AAC

## 质量检查结果
- ✅ 文件完整
- ✅ 编码格式正确
- ✅ 页数匹配 (19/19)
- ✅ 所有音频 > 3 秒
- ⚠️ 第 5 页音频较长，截图自动延长时间

## 逐页时长
| 页码 | PPT标题 | 音频时长 | 状态 |
|------|---------|----------|------|
| 1 | 封面 | 15.2s | ✅ |
| 2 | 开场 | 22.1s | ✅ |
| ... | ... | ... | ... |
```

---

## 四、generate.js v2.0 脚本规范

### 4.1 设计变更

```
v3.2 (旧版)                    v2.0 (新版)
─────────────────────────      ─────────────────────────
✅ 扫描输入目录                 ✅ 接收明确的 --slides 和 --scripts-dir
✅ 自动检测风格                 ✅ 从 --spec 读取预设风格
✅ 讲稿不足时提示               ✅ 讲稿不存在时报错
✅ 正则清洗 markdown            ✅ 直接读取纯文本（无需清洗）
✅ 单一脚本完成所有工作          ✅ 只负责技术合成
```

### 4.2 核心代码结构

```javascript
// generate.js v2.0 伪代码

// ========== 参数解析 ==========
const config = {
  slides: null,        // PPT/PDF 路径（必需）
  scriptsDir: null,    // 讲稿目录（必需）
  outputDir: null,     // 输出目录（必需）
  spec: null,          // 方案JSON（可选）
  keepTemp: false,     // 保留临时文件
  cleanup: false       // 完成后清理
};

// 默认配置
const DEFAULT_VOICE = 'zh-CN-YunxiNeural';
const DEFAULT_RATE = '+25%';

// ========== 阶段 1: PPT 截图 ==========
async function screenshotSlides(pptPath, outputDir) {
  // 1. LibreOffice 转 PDF
  // 2. pdftoppm 导出 PNG
  // 3. 重命名为 01.png, 02.png, ...
  // 返回: [png路径数组]
}

// ========== 阶段 2: TTS 合成 ==========
async function synthesizeTTS(scriptsDir, spec, audioDir) {
  // 1. 读取 scriptsDir 下所有 .txt 文件
  // 2. 按文件名排序
  // 3. 逐页调用 edge-tts
  //    - 文本超长（>3000字）时自动分段
  //    - 从 spec 读取每页的 voice/rate 配置
  // 返回: [mp3路径数组]
}

// ========== 阶段 3: 视频合成 ==========
async function synthesizeVideo(screenshots, audioFiles, clipsDir, finalVideo) {
  // 1. 逐页合成：ffmpeg -loop 1 -i image -i audio → clip
  // 2. 生成 files.txt
  // 3. ffmpeg concat 拼接
}

// ========== 阶段 4: 质量验证 ==========
async function verifyVideo(videoPath, expectedPages) {
  // 1. ffprobe 检查编码/分辨率/时长
  // 2. 生成 VIDEO_COMPLETE.md
}

// ========== 主函数 ==========
async function main() {
  // 1. 参数验证（缺少必需参数 → 报错）
  // 2. 创建临时目录
  // 3. Phase 1-4 顺序执行
  // 4. 清理/保留临时文件
  // 5. 输出完成信息
}
```

### 4.3 关键变更点

**输入验证更严格**：
```javascript
if (!config.slides || !config.scriptsDir || !config.outputDir) {
  console.error('❌ 必需参数: --slides, --scripts-dir, --output');
  process.exit(1);
}
if (!fs.existsSync(config.scriptsDir)) {
  console.error('❌ 讲稿目录不存在: ' + config.scriptsDir);
  process.exit(1);
}
```

**纯文本读取，无需清洗**：
```javascript
// v3.2 (旧): 需要复杂的正则清洗
const cleanText = script.replace(/#{1,6}\s+/g, '').replace(/\*\*/g, '')...

// v2.0 (新): 直接读取纯文本
const scriptText = fs.readFileSync(scriptPath, 'utf-8').trim();
```

**逐页配置支持**：
```json
// video_design_spec.json（脚本可读配置）
{
  "global": {
    "style": "tech_training",
    "styleName": "技术培训",
    "defaultVoice": "zh-CN-YunxiNeural",
    "rate": "+15%"
  },
  "pages": [
    {
      "num": 1,
      "title": "封面",
      "contentType": "封面",
      "pageStyle": "story",
      "voice": "zh-CN-XiaoxiaoNeural",
      "rate": "+15%",
      "duration": 15
    },
    {
      "num": 2,
      "title": "AI Agent 是什么",
      "contentType": "概念讲解",
      "pageStyle": "tech_training",
      "voice": "zh-CN-YunxiNeural",
      "rate": "+15%",
      "duration": 22
    }
  ]
}
```

---

## 五、SKILL.md 执行流程

SKILL.md 是 LLM 的操作手册，定义完整的执行流程：

```markdown
---
name: keynote-video
description: >-
  PPT/演示文稿 → 播报视频。交互式内容评估 + LLM讲稿生成 + 
  方案确认后自动合成。v2.0 架构。
---

# PPT to Video (Keynote) v2.0

## 🚨 执行纪律（最高优先级）

1. **PHASE 分隔** — Phase 0-2 由 LLM 驱动，Phase 3-4 由脚本驱动
2. **BLOCKING 步骤** — Phase 0（输入不足）和 Phase 2（方案确认）必须等待用户
3. **禁止跳过确认** — 未经 Phase 2 确认，不得进入 Phase 3
4. **脚本做技术，LLM 做内容** — 脚本不判断风格、不改写讲稿

## Phase 0: 输入评估

1. 扫描输入目录，列出所有相关文件
2. 评估输入完整性：
   - PPT 文件存在？→ 必需
   - 讲稿文件存在？→ 计算覆盖率
   - 背景材料存在？→ 加分
3. 评分 ≥ 80 → 进入 Phase 1
4. 评分 50-79 → 提示用户，确认后继续
5. 评分 < 50 → 列出缺失项，等待用户 ⛔ BLOCKING

## Phase 1: 内容理解 & 讲稿生成

1. 提取 PPT 文字：`python3 scripts/extract_ppt_text.py <pptx>`
2. 读取所有可用材料（notes、背景、README）
3. 为每页生成口语化演讲稿：
   - 纯文本输出，无 markdown 标记
   - 15-25字/句，先重点后事实
   - 标注预计时长和推荐音色
4. 保存到 <PROJECT_DIR>/scripts_rewritten/
5. 生成 video_design_spec.md

## Phase 2: 方案确认 ⛔ BLOCKING

1. 向用户展示 video_design_spec.md
2. 等待用户确认：
   - "确认生成" → 进入 Phase 3
   - "修改" → 重新生成对应页面 → 再次展示
3. 用户确认后，生成 video_design_spec.json（脚本可读格式）

## Phase 3: 技术合成

```bash
node scripts/generate.js \
  --slides <pptx> \
  --scripts-dir <PROJECT_DIR>/scripts_rewritten/ \
  --output <output_dir> \
  --spec <PROJECT_DIR>/video_design_spec.json
```

## Phase 4: 质量验证

1. 检查输出视频（ffprobe 验证）
2. 生成 VIDEO_COMPLETE.md
3. 向用户报告结果
```

---

## 六、实施状态

### ✅ 核心文件创建（已完成）

| 任务 | 产出 | 状态 |
|------|------|------|
| SKILL.md | Phase 0-4 完整流程 + 6种风格规范 | ✅ |
| generate.js v2.0 | 纯技术合成脚本（参数验证/截图/TTS/合成/验证） | ✅ |
| extract_ppt_text.py | PPTX/PDF 文字提取 | ✅ |
| verify_video.sh | 视频质量验证 | ✅ |
| 模板文件 | video_design_spec + script_page_template | ✅ |
| README.md + package.json | 文档和元数据 | ✅ |

### 阶段 2: 测试验证（1 小时）

| 任务 | 场景 |
|------|------|
| 完整输入测试 | PPTX + notes + 背景材料 |
| 仅 PPT 测试 | 只有 PPTX，测试交互引导 |
| 讲稿覆盖不足测试 | PPTX + 部分 notes |

### 阶段 3: 实战验证

使用现有项目验证：
- `/home/Vincent/.openclaw/workspace/WORK/TOPIC分析/AI AGENT专题/`

---

## 七、风险与边界

| 风险 | 应对 |
|------|------|
| edge-tts 单次文本长度限制 | 自动分段合成 |
| PPTX 包含特殊字体/动画 | 截图可能略有偏差，不影响核心功能 |
| 用户反复修改讲稿 | Phase 2 支持迭代修改 |
| 网络断开导致 TTS 失败 | 提示用户检查网络，支持重试 |
| 超大 PPT（50+ 页） | 分批处理，避免内存问题 |

---

## 八、与 pptx-master 的架构对照

| 维度 | pptx-master | keynote-video v2.0 |
|------|-------------|----------------|
| **架构模式** | 多步骤串行管道 | 多步骤串行管道 |
| **认知/技术分离** | LLM 做内容，脚本做导出 | LLM 做内容，脚本做合成 |
| **确认机制** | Step 4 八项确认 ⛔ | Phase 2 方案确认 ⛔ |
| **输入评估** | Step 1 内容转换 | Phase 0 完整性评分 |
| **脚本角色** | 纯技术（PDF转换/SVG导出） | 纯技术（截图/TTS/视频） |
| **质量验证** | SVG 质量检查 | 视频编码/音画同步检查 |

keynote-video v2.0 的架构直接参考了 pptx-master 的成功模式：**LLM 管内容，脚本管技术，中间有确认**。

---

*文档版本: v2.0-draft*  
*创建日期: 2026-05-09*  
*下一步: 用户确认后开始实施*
