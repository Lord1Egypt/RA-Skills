---
name: kindergarten-english-course
slug: kindergarten-english-course
displayName: 幼儿园英语课程体系
version: 1.1.1
category: education
platforms: [WorkBuddy, claude-code, codex, deepseek-harness]
summary: 面向 3-7 岁幼儿的英语课程体系，按 L1 字母启蒙、L2 自然拼读、L3 词汇句型、L4 阅读对话四级进阶，生成 A4 可打印练习页（含答案页），并支持能力诊断、批改与进阶建议。
description: 3-7 岁幼儿英语启蒙课程：L1 字母 → L2 自然拼读 → L3 词汇句型 → L4 阅读对话，生成 A4 可打印练习页（含答案），支持诊断定级与错题重练。kindergarten English worksheets, alphabet, phonics, CVC words, sight words.
tags:
  - 教育
  - 幼儿
  - 英语
  - 启蒙
  - 自然拼读
  - 字母
  - 词汇
  - 句型
  - 对话
  - 幼小衔接
  - kindergarten-english
license: MIT
homepage: https://skillhub.cn/skills/user_89a2cacc/kindergarten-english-course
author: workbuddy-user-89a2cacc
keywords:
  - 英语启蒙
  - 自然拼读
  - 字母
  - 幼儿园
  - 幼小衔接
  - 可打印练习
  - printable worksheet
agent_created: true
---

# 幼儿园英语课程体系

## Overview

面向 3-7 岁幼儿的英语启蒙交付能力：把"字母形音 → 自然拼读 → 主题词汇与句型 → 情景对话"组织成 L1-L4 四级可进阶体系，按等级与题型生成可直接打印的 A4 英语练习页，并在练习后完成批改、薄弱点定位与下一步建议。核心产出是**可打印英语练习页**，附带家长指导话术。

## 快速上手

```bash
# 某等级一份练习（8 题，附答案 JSON）
python scripts/generate_worksheet.py --level L2 --seed 7 --out eng_L2.html --json eng_L2.json

# 预填孩子姓名 + 得分栏
python scripts/generate_worksheet.py --level L1 --name 小明 --score --out eng_L1.html

# 诊断卷（覆盖全部题型，用于定级）
python scripts/generate_worksheet.py --preset diagnostic --out diag.html --json diag.json

# 错题重练：按上次 JSON 的错题题号生成同型新题
python scripts/generate_worksheet.py --review diag.json --wrong 2,5 --seed 9 --out review.html
```

对 WorkBuddy 直接说更简单："给我孩子出一份自然拼读练习" / "生成一份数学诊断卷"。

## 触发条件

| 类别 | 触发词 / 场景 |
|---|---|
| 对象词 | 幼儿、幼儿园、小班、中班、大班、学前、幼小衔接、3-7岁孩子、我家娃、孩子、宝宝 |
| 内容词 | 英语、英文、ABC、字母、26个字母、字母歌、自然拼读、Phonics、拼读、CVC、音素、发音、单词、词汇、认单词、看图识词、主题词、颜色英语、动物英语、食物英语、身体英语、高频词、Sight Words、句型、简单句、句子、对话、口语、听说、英语启蒙、英语练习、英语作业 |
| 交付词 | 英语题、英语练习纸、英语练习题、练习页、题卡、打印、出几道英语题、给孩子做、英语启蒙材料 |
| 流程词 | 英语诊断、测一下英语、从哪开始学英语、批改、错了、怎么教英语、英语水平、规划英语路线 |
| 英文 | kindergarten English, alphabet, letter tracing, phonics, CVC words, sight words, English sentences, dialogue, speaking, English worksheet |

**不触发**：小学以上英语教材同步辅导、语法专项（时态/从句）、成人英语、考试冲刺（KET/PET 等）、外教口语约课。遇到这些直接说明超出本 Skill 范围，建议改用对应学段资源。

判定原则：只要同时出现"幼儿阶段对象"与"英语/字母/拼读/单词/句型/对话/启蒙"意图，即触发本 Skill，无需用户说出"Skill"或课程名。

### 对话示例（自然语言触发）

以下为完整对话示例，Agent 应直接照此节奏响应，无需用户说出 Skill 名或任何参数：

**示例 1 · 按等级出题**
> 用户：孩子中班，在学自然拼读，给练练
> → 判定 L2（自然拼读），生成 8 题练习页 + 答案 JSON，说明本次覆盖的题型（如 CVC 拼读、听音辨字母）。

**示例 2 · 从零开始定级**
> 用户：孩子英语零基础，从哪开始？
> → 生成诊断卷（10 题覆盖字母/拼读/词汇/句型），说明"先做这 10 题定位起点"。

**示例 3 · 批改与重练**
> 用户：这份错了第 3、6 题
> → 对照答案 JSON 定位薄弱点，给家长话术，并按错题题型生成同型新题。

**示例 4 · 场景化需求**
> 用户：想让他在家开口说几句英语
> → 生成 L4 情景对话练习，并附家长陪练话术（怎么引导、怎么纠错、别纠正发音到什么程度）。

**示例 5 · 不触发**
> 用户：孩子要考 KET，来套真题
> → 明确说明超出范围（本 Skill 只做 3-7 岁启蒙，不做考试冲刺与语法专项），建议改用对应资源。

## 执行逻辑

### Step 0 · 采集信息（最多问一次，缺失即用默认值）

需要的三项信息：**年龄/年级、当前水平（是否已知）、本次要练什么（题型或主题）**。

- 用户已给出其中任意一项 → 直接推导其余，不再追问。
- 三项全缺 → 走诊断路径（Step 1 的诊断卷），在回复中说明"先做 10 题定位起点"。
- 确实需要选择时（例如无法确定大班还是中班），用 AskUserQuestion 一次性问完，不要多轮追问。

默认假设（不询问时直接采用，并在回复中注明）：未知水平 → L1 诊断；未指定题量 → 每级 8 题；未指定列数 → 2 列。指导语默认中文（`--lang zh`），双语/全英家庭可用 `--lang en`。

### Step 1 · 定级

等级对照：L1 小班 3-4 岁字母启蒙；L2 中班 4-5 岁自然拼读；L3 大班 5-6 岁词汇句型；L4 幼小衔接 6-7 岁阅读对话。完整知识点与晋级标准见 `references/curriculum.md`。

- 已知年龄但未测水平 → 生成对应等级的练习。
- 起点未知 → 生成诊断卷：`--preset diagnostic`（覆盖全部 10 个题型的 10 题，每题标注等级）。家长回传结果后，按"某等级 2 题全对即视为掌握，从最低未掌握等级开始"定位（详见 `references/curriculum.md` 诊断规则）。

### Step 2 · 组卷

调用脚本（绝对路径 `C:\Users\李玉明\.workbuddy\skills\kindergarten-english-course\scripts\generate_worksheet.py`，Windows 下 Python 不可用时改用 `C:\Users\李玉明\.workbuddy\binaries\python\versions\3.13.12\python.exe`）：

```
python "<skill>/scripts/generate_worksheet.py" --level L2 --count 8 --seed 7 \
  --out "<工作区>/幼儿英语_L2.html" --json "<工作区>/幼儿英语_L2_答案.json"
```

- 指定题型 → 用 `--topics` 传逗号列表，如 `--topics sentence,dialogue`
- 补薄弱点 → 用 `--topics` 指定单一题型，题量减半
- 口头作答 → 加 `--no-answers`
- 复现同一套题 → 使用相同 `--seed`
- 姓名留空手填 → 不加 `--name`；也可 `--name 小明` 预填
- 全英指导语 → 加 `--lang en`
- 高密度排版 → 加 `--columns 3`；对话/长句用 `--columns 1` 获得更大空间
- 显示评价栏 → 加 `--score`（页尾出现可手填的得分 / 正确数 / 点评栏，默认不显示）
- 参数与配方见 `references/worksheet-spec.md`

必须同时输出 `--json`，后续批改直接用它比对，不要凭记忆重算答案。

### Step 3 · 交付

1. 用 present_files 呈现生成的 HTML，并提示：浏览器打开后点「打印 / 另存为 PDF」，勾选「背景图形」（描红框与虚线依赖背景）。
2. 在回复中给出**三条以内**的家长指导：本次题型与数量、建议用时（L1/L2 约 10 分钟、L3/L4 约 15 分钟）、一条具体操作提示（如"拼读时手指数着字母滑过去：c-a-t"）。话术模板见 `references/pedagogy.md`。
3. 不写过程性描述、不写日期来源说明，直接给内容和指导。

### Step 4 · 批改与进阶

用户回传答案（文字、口述或照片）后：

1. 对照 JSON 判分，输出：共 X 题、做对 Y 题、正确率 Z%。
2. 按正确率决策（详见 `references/curriculum.md` 晋级标准）：≥90% 升下一级；60-89% 同级加练且错题题型占比提到 50%；<60% 降一级，回到听音/儿歌/实物输入再抽象。
3. 同一题型错 ≥2 题 → 用错题重练直接生成针对性练习（读上次 JSON，按错题题型出同型新题，每个错题配 2 道新题）：

```
python "<skill>/scripts/generate_worksheet.py" \
  --review "<工作区>/幼儿英语_L2_答案.json" --wrong 4,7 \
  --out "<工作区>/幼儿英语_L2_错题重练.html" --json "<工作区>/幼儿英语_L2_错题重练_答案.json"
```

未指定题号时也可用 `--topics` 手选题型，题量减半。
4. 每级至少完成 3 份练习才考虑晋级；连续两次 ≥90% 才允许跳级。
5. 给家长的反馈固定三段：结果 → 薄弱点 → 下一步（一个改进点，5-10 分钟的亲子小游戏）。禁止横向比较与否定性评价。

### Step 5 · 进度记录（可选）

用户多次使用或明确要求时，在工作区维护 `幼儿英语学习档案.md`，追加记录：日期、等级、题型、题量、正确率、错题库、下一步。模板见 `assets/progress-journal.md`。

## 硬规则

- 听说领先、读写跟上：L1-L2 不要求拼写，重在听与说；书写/描红从 L1 开始但不追求工整。
- 不在幼儿阶段引入语法术语（时态、从句）、长难句、超纲词汇；句型仅限 5 类固定框架（I see a / This is a / I like / It is / I can）。
- 练习页必须含答案页（除非用户明确要求口头作答），方便家长当场核对。
- 一次只提一个改进点，先肯定具体行为再纠错。
- 每次只生成一份练习，避免一次性堆 30+ 题；对话/长句题型单次不超过 6 题。
- 开放题（如发音辨图）以"家长判断"为批改依据，不机械判对错。

## 错误处理与边界输入（TRACE-R）

执行中遇到下列情况，必须给出**可理解的原因 + 可执行的下一步**，不得静默失败，也不得把原始报错直接抛给用户：

| 情况 | 处理方式 |
|---|---|
| 等级或题型不在合法范围 | 回显合法取值（L1-L4、10 个题型），给出最接近的建议，不中断对话 |
| 题数超出范围（如 0 或 999） | 自动截断到 1-30 并告知已调整 |
| 输出目录不存在或无写入权限 | 改用工作区默认目录，并说明文件实际写到了哪里 |
| 用户发来答卷照片但无法逐题识别 | 说明"图片里的答案我无法逐题确认"，请家长口述题号与孩子的作答，**不凭猜测批改** |
| 家长问某个单词怎么读 | 说明本 Skill 不提供音频，给出拼读拆分提示（如 c-a-t → /kæt/）并建议配合点读资源 |
| 打印时答案与题目同页 | 按默认版式重生成，答案页强制另起一页 |

边界输入约定：

- 单份默认 8 题，上限 30 题，超出自动截断并告知。
- 等级缺参数时默认 L2（自然拼读档），并在回复中说明默认值。
- 中英双语切换（`--lang`）缺失时默认中文界面、英文题目内容。
- 启蒙阶段不追求拼写完全正确：批改时"能拼出首音 + 结构接近"即算通过，不因拼写细节判错，避免打击兴趣。

## 安全与国内可用性（TRACE-T）

- **零外网**：全部脚本仅用 Python 标准库，无 requests / urllib / socket / 任何 HTTP 调用，断网也能完整运行。
- **零凭证**：不读取任何 API Key、Token 或环境变量凭据，不访问输出目录以外的文件。
- **最小权限**：只向用户指定的路径写一个 HTML（及可选 JSON），不改动系统配置、不安装任何依赖。
- **无数据外传**：孩子姓名、答题结果只写入本地生成的文件，不会上传到任何服务。
- **HTML 转义**：用户输入（姓名、自定义内容）经转义后再拼进 HTML，防注入与排版破坏。
- **国内可用**：界面与说明全中文，HTML 使用 Microsoft YaHei / PingFang SC 中文字体并带 sans-serif fallback；无需代理、不依赖海外 API。
- **可复现**：同一 `--seed` 生成内容完全一致，便于家长核对、复练与归档。

## 已知限制与扩展指引（TRACE-C）

已知限制（如实说明，不夸大能力）：

- 配图与情境用 emoji 呈现，不同设备字形与配色有差异；首次打印建议先预览一页。
- **不提供音频**：本 Skill 无法输出发音，自然拼读环节需要家长配合发音或借助点读/音频资源。
- 未做移动端窄屏适配：练习页按 A4 纵向排版设计，手机查看需缩放。
- 对话与口语题无唯一标准答案，答案页给出参考表达，由家长判断是否达标。

扩展指引（开发者）：

- 新增题型：在 `scripts/generators/` 下新增 `g_<topic>.py`，实现 `gen(rng, lang) -> (title, instruction, html, answer)` 即被自动加载，无需改动主脚本。
- 扩充词汇：改 `scripts/common.py` 的 `VOCAB`（按主题）与 `CVC_EMOJI` 映射；如需真实图片素材，在此处替换为图片路径即可。
- 调整版式：改 `scripts/common.py` 的 CSS 常量，**确认 CSS 仍被 `<style>` 标签包裹**。
- 不兼容变更需在 `CHANGELOG.md` 显式标注，并同步升版本号。

## 资源

- `references/curriculum.md` — L1-L4 知识点、题型映射、晋级与补练标准、诊断定位规则
- `references/pedagogy.md` — 教学原则、分题型讲解话术、常见错误纠正、家长反馈模板
- `references/worksheet-spec.md` — 脚本参数、版式规范、常用组卷配方
- `scripts/generate_worksheet.py` — 主入口：加载插件、组卷、渲染（A4 可打印 HTML + JSON 答案）
- `scripts/common.py` — 共享数据（字母/词汇/CVC/高频词/句型/对话）与 I18N 中英文字典
- `scripts/generators/` — 题型插件目录（`g_*.py`，新增题型即丢文件即用）
- `assets/progress-journal.md` — 学习档案模板（Step 5 可选）

## 自检

安装后或修改脚本后，运行以下命令验证可用（覆盖 4 个等级 + 诊断卷，均应生成成功）：

```bash
for L in L1 L2 L3 L4; do python scripts/generate_worksheet.py --level $L --seed 1 --out t_$L.html --json t_$L.json; done
python scripts/generate_worksheet.py --preset diagnostic --out t_diag.html --json t_diag.json
```

## Changelog

- **1.1.1**：更名为「**幼儿园英语课程体系**」；移除与姊妹 Skill 的交叉引用（Overview 互补句、README 姊妹 Skill 整段、CHANGELOG 措辞精简）。
- **1.1.0**：按 SkillHub TRACE 五维评测体系优化——新增「对话示例（自然语言触发）」完整多轮示例（A-适用性）、「错误处理与边界输入」约定表（R-可靠性）、「安全与国内可用性」声明（T-可信任度）、「已知限制与扩展指引」（C-规范性）。
- **1.0.0**：首次发布，L1-L4 四级体系 + 10 题型插件 + A4 可打印练习页生成器 + 诊断/错题重练/批改进阶。
