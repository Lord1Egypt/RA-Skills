---
name: li-Record-lecture-video
description: >
  通用录播课学习计划表生成器 v2.0.2。适用于任何培训认证课程（ISO27001/TOGAF/DevOps/ITIL等），
  基于已录视频清单（标题+时长）按天分组生成学习计划Excel。
  支持三种模式：用户上传自定义Excel模板（占位符或自动检测）、内置11列通用默认模板。
  兼容 opencode、hermes、WorkBuddy 等多种智能体。
---

# 通用录播课学习计划生成 Skill (v2.0.2)

## 触发条件

当用户提供**已录好的视频课程清单**（含视频标题和时长），并要求生成按天分组的学习计划Excel时触发。

典型触发词：录播课学习计划、按天安排学习、视频时长分组、生成学习计划表、学习计划Excel、录播课排期

## 核心原则

1. **课程内容是既成事实**：视频标题和时长从源头直接搬运，不可改写
2. **生成的是学习安排**：告诉学员每天学哪几个视频、学到什么程度，不是课程设计
3. **模板可替换**：支持用户提供自定义 Excel 模板（占位符模式或自动检测），也支持内置 11 列默认模板

## 安全约束（必须遵守）

> ⚠️ Agent 在调用本 Skill 时必须执行以下安全检查，不可跳过。

| 约束项 | 规则 |
|--------|------|
| **输入来源** | 仅接受用户明确提供的文件或文字；不主动扫描用户文件系统 |
| **输出路径** | 禁止写入系统目录（/etc, /bin, C:\Windows 等）；禁止路径遍历（../） |
| **参数范围** | daily_hours: 0.25–16h；视频数量: ≤500；标题长度: ≤300字符 |
| **数据脱敏** | 视频标题自动防 Excel 公式注入（= + - @ 前缀转义） |
| **日志安全** | 脚本不输出完整文件路径到 stdout |
| **用途限制** | 仅用于教育培训场景的学习计划生成，不用于其他目的 |
| **用户确认** | 生成前向用户确认课程名称、每日学习上限、输出位置 |

## 输入方式

### 方式A：Excel 文件
用户提供包含「视频标题」和「视频时长」列的 .xlsx 文件。
脚本自动读取并解析时长（支持 `timedelta` 和数值格式）。

### 方式B：直接文字输入
用户通过聊天发送视频清单，格式灵活：
```
课程导入.mp4  16分钟
1.1 信息安全定义.mp4  22分钟
...
```
Agent 需先解析为结构化数据（标题、分钟数），再写入临时 JSON 供脚本读取。

### 方式C：混合输入
用户提供 Excel 视频清单 + 口头补充课程信息（如考试说明）。

## 模板模式（v2.0 新增）

### 用户自定义模板

用户可以提供自己的 Excel 模板，Skill 读取模板后在数据区插入按天分组的视频数据。**模板中的所有样式、配色、列宽、合并规则将被保留**。

#### 方式 A：占位符模式（推荐）

在模板的 Excel 中，在数据区第一行的任意单元格写入 `{{DAILY_DATA}}`。Skill 会自动找到该标记，删除该行，并在该位置插入分组数据。

模板中还可使用以下占位符（可选）：
- `{{COURSE_TITLE}}` — 课程大标题
- `{{REGISTRATION_INFO}}` — 报名阶段文字
- `{{PHASE_TITLE}}` — 精讲阶段标题
- `{{EXAM_INFO}}` — 考试介绍
- `{{EXAM_PHASE}}` — 考试阶段
- `{{SCORE_INFO}}` — 成绩查询

#### 方式 B：自动检测模式

如果模板不含占位符，Skill 会扫描表头行自动匹配列名。支持的列名关键词：

| 字段 | 匹配关键词 |
|------|-----------|
| 时间安排 | 时间安排、日期、天次 |
| 学习时长 | 学习时长、时长、课时 |
| 学习章节 | 学习章节、章节、课程内容 |
| 学习目标 | 学习目标、目标 |
| 目标验证 | 验证方式、目标验证 |
| 学习内容 | 学习内容、知识点 |
| 课后作业 | 课后作业、作业 |
| 学习要求 | 学习要求、学习方法 |
| 学习资料 | 学习资料、资料 |

#### 方式 C：内置默认模板（向后兼容）

不提供模板时，使用内置 11 列通用标准模板（适用于各类培训认证课程场景）。所有现有 v1.x 用法无需改动。

#### 模板模式 config 示例

```json
{
  "course_name": "课程名称",
  "daily_hours": 2,
  "template": "path/to/user_template.xlsx",
  "videos": [["视频.mp4", 30.0]],
  "guide": {"视频.mp4": ["目标", "验证", "内容"]},
  "registration_info": "...",
  "exam_info": "...",
  "output": "output/学习计划.xlsx"
}
```

## 必需参数（缺失时主动询问）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 课程名称 | 大标题（如 "APMG ISO/IEC 27001 Foundation"） | **必须提供** |
| 每日学习上限 | 小时数（0.25–16） | 2 |
| 视频清单 | 标题+时长 | **必须提供** |
| 精讲阶段日期 | "X月XX日-X月XX日" | X月XX日-X月XX日 |
| 学习指引 | 每视频的（目标/验证/重点）映射 | 可选，无则留空 |
| 考试信息 | 考试介绍/阶段/成绩查询 | 可选，使用默认模板 |
| 注册说明 | 报名阶段文字 | 可选，使用默认模板 |
| 课后作业 | 统一文字 | "完成本章节课后练习题" |

## 工作流

1. **确认输入**：读取 Excel 或解析文字，确认视频数量和总时长
2. **收集缺失参数**：按上表问用户（一次性问完，不要逐个问）
3. **确认模板**（v2.0）：检查用户是否提供了自定义模板 Excel；如有则使用模板模式，否则使用内置默认模板
4. **构建 config.json**：根据场景选路径（见下方）
5. **自动生成学习指引**（可选但推荐）：对无 guide 的视频自动匹配学习目标/验证/内容（见下方）；也可使用 `scripts/auto_guide.py` 提供的 `build_guide_map()` 函数
6. **安全校验**：检查输出路径不在系统目录、参数在合法范围
7. **调用脚本**：`python scripts/generate_study_plan.py --config <config.json> [--template <模板路径>]`
8. **日期校验**：脚本自动检查实际分组天数与用户指定日期范围是否匹配，不匹配时输出 WARNING
9. **展示结果**：用 `present_files` 展示生成的 .xlsx

### config.json 构建指南

**场景 A — 简单模式（无学习指引）**：视频清单来自 Excel，不需要填写学习目标/验证/内容。

直接用 `input_excel` 字段，脚本自动读取视频：

```json
{
  "course_name": "课程名称",
  "daily_hours": 2,
  "phase_name": "精讲阶段",
  "phase_dates": "X月XX日-X月XX日",
  "input_excel": {
    "path": "用户提供的Excel路径",
    "title_col": 1,
    "dur_col": 2,
    "header_row": 1
  },
  "output": "output/学习计划.xlsx"
}
```

**场景 B — 完整模式（含学习指引）**：需要填写每视频的学习目标/验证/内容。

先用 Python 读取 Excel 提取视频标题和时长，构造 `videos` 数组，再用关键词匹配自动生成 `guide` 映射（见下一节），最终构建完整 config：

```json
{
  "course_name": "...",
  "daily_hours": 2,
  "phase_name": "...",
  "phase_dates": "...",
  "videos": [["标题.mp4", 16.5], ["另一个.mp4", 22.0]],
  "guide": {
    "标题.mp4": ["学习目标", "验证方式", "学习内容"],
    "另一个.mp4": ["目标", "验证", "内容"]
  },
  "exam_info": "考试信息...",
  "score_info": "成绩查询...",
  "output": "output/学习计划.xlsx"
}
```

**场景 C — 模板模式（v2.0 新增）**：用户提供了自定义 Excel 模板。

```json
{
  "course_name": "课程名称",
  "daily_hours": 2,
  "template": "path/to/user_template.xlsx",
  "phase_name": "精讲阶段",
  "phase_dates": "X月XX日-X月XX日",
  "videos": [["标题.mp4", 16.5]],
  "guide": {"标题.mp4": ["目标", "验证", "内容"]},
  "registration_info": "注册说明...",
  "exam_info": "考试信息...",
  "exam_phase": "考试阶段...",
  "score_info": "成绩查询...",
  "output": "output/学习计划.xlsx"
}
```

先用 Python 读取 Excel 提取视频标题和时长，构造 `videos` 数组，再用关键词匹配自动生成 `guide` 映射（见下一节），最终构建完整 config：

```json
{
  "course_name": "...",
  "daily_hours": 2,
  "phase_name": "...",
  "phase_dates": "...",
  "videos": [["标题.mp4", 16.5], ["另一个.mp4", 22.0]],
  "guide": {
    "标题.mp4": ["学习目标", "验证方式", "学习内容"],
    "另一个.mp4": ["目标", "验证", "内容"]
  },
  "exam_info": "考试信息...",
  "score_info": "成绩查询...",
  "output": "output/学习计划.xlsx"
}
```

## 自动学习指引生成

当用户未提供每视频的学习目标/验证/内容时，Agent 应使用内置 `scripts/auto_guide.py` 模块自动生成 `guide` 映射。

### 推荐用法：调用 auto_guide.py

```python
import sys
sys.path.insert(0, r'<skill_root>/scripts')
import auto_guide

# 从视频标题列表生成 guide 映射
guide = auto_guide.build_guide_map([title for title, _ in videos])

# 验证覆盖率
missing = auto_guide.validate_coverage(guide, [title for title, _ in videos])
auto_guide.print_coverage_report(guide, [title for title, _ in videos])
```

### 高级用法：自定义规则

```python
import auto_guide

# 定义课程专属关键词规则
my_rules = [
    auto_guide.make_simple_rule('DevOps', ['devops', 'dev ops'],
        ('掌握DevOps核心概念', '能说明DevOps定义与价值', 'DevOps原则与实践')),
    auto_guide.make_multi_rule('流水线', ['流水线', 'pipeline', 'CI/CD'],
        ('掌握持续交付流水线', '能设计部署流水线', 'CI/CD流程与工具')),
]

# 用自定义规则构建
guide = auto_guide.build_guide_map(videos, rules=my_rules)
```

### 内置通用规则

`auto_guide.py` 内置了三组通用规则模板（`COMMON_RULES`），Agent 也可以基于视频标题主题自行构建 `auto_guide.build_guide_map(course='iso27001'|'devops'|'general')` 快速生成。

### 注意事项

- 规则按优先级从具体到宽泛排列
- 兜底规则确保每个视频都有指引，不留空
- 匹配规则随课程主题调整（ISO27001 / TOGAF / DevOps 等各有不同关键词）
- 如有教学大纲 PDF 可作为更精确的指引来源（Agent 应基于 PDF 手动构建 guide 映射）

## 脚本调用说明

脚本接受一个 JSON 配置文件，包含所有课程参数和视频数据。

```bash
python scripts/generate_study_plan.py --config /path/to/config.json

# 或使用自定义模板
python scripts/generate_study_plan.py --config config.json --template my_template.xlsx
```

配置文件结构见 `references/template-spec.md`。

### 备用：无配置文件模式

如果只有视频清单和课程名，Agent 可直接构造最小 config：

```json
{
  "course_name": "课程名称",
  "daily_hours": 2,
  "videos": [["视频标题.mp4", 16.5], ["另一个视频.mp4", 22.0]],
  "phase_name": "精讲阶段",
  "phase_dates": "X月XX日-X月XX日",
  "registration_info": "默认注册说明",
  "exam_info": "默认考试信息",
  "exam_phase": "默认考试阶段",
  "score_info": "默认成绩查询",
  "guide": {},
  "output": "output/学习计划.xlsx"
}
```

其中 `videos` 为 `[[标题, 分钟数], ...]`。

## 输出物

- 一个 `.xlsx` 文件，按用户选择的模式输出：
  - **自定义模板模式**：保留用户模板的全部样式和布局，在数据区填入按天分组数据
  - **内置模板模式**：11 列通用学习计划表（含大标题、报名阶段、精讲阶段、按天数据、考试信息、成绩查询）
- 每天自动小计，同天单元格合并，表头冻结

## 兼容性

与智能体无关：脚本是纯 Python + openpyxl，任何能执行 Python 的 agent（opencode、hermes、WorkBuddy 等）均可使用。Agent 的职责只是收集参数、构造 config JSON、调用脚本、展示结果。

---

## 使用说明 / Usage Instructions / Mode d'emploi

### 中文

**功能简介**：通用录播课学习计划生成工具。适用于任何培训认证课程（ISO27001、TOGAF、DevOps、ITIL 等），将已录好的视频课程清单（标题+时长）自动生成按天分组的学习计划 Excel 表格。

**三种使用方式**：
1. **内置模板（零配置）**：直接提供视频清单 + 课程名，自动生成 11 列通用标准学习计划
2. **自定义模板（占位符）**：上传自己的 Excel 模板，在数据区标记 `{{DAILY_DATA}}`，工具自动填入分组数据，保留模板全部样式
3. **自定义模板（自动检测）**：上传任意 Excel 模板，工具自动扫描表头关键词匹配列

**使用步骤**：
1. 准备视频清单：Excel 文件（含标题列和时长列）或直接在聊天中发送 `视频名 时长` 格式的列表
2. 告诉 Agent 课程名称和每天想学多少小时（默认 2 小时）
3. 可选：提供一个自定义 Excel 模板（支持占位符或自动检测）
4. Agent 自动构造配置，调用生成脚本
5. 完成：获得按天分组的完整学习计划 Excel

**示例**：
> 我有一个 ISO27001 的录播课，视频清单在 videos.xlsx 里，每天学 2 小时，帮我生成学习计划

> 用我这个 Excel 模板生成学习计划，视频数据在 videos.xlsx

**安全提示**：脚本仅读取您指定的文件，输出受限目录外写入，视频标题自动防 Excel 注入。不访问网络，不上传数据。

---

### English

**Overview**: A universal recorded-course study plan generator. Works with any training/certification course (ISO27001, TOGAF, DevOps, ITIL, etc.). Automatically generates a day-by-day study plan Excel from a recorded video list (title + duration).

**Three Modes**:
1. **Built-in Template (zero config)**: Just provide a video list + course name to generate an 11-column universal study plan
2. **Custom Template (placeholders)**: Upload your own Excel template, mark `{{DAILY_DATA}}` in the data area, and the tool fills in grouped daily data — preserving all of your template's styling
3. **Custom Template (auto-detect)**: Upload any Excel template; the tool scans header keywords to auto-map columns

**Steps**:
1. Prepare your video list: either an Excel file (with title and duration columns) or send `video_name duration` pairs directly in chat
2. Tell the Agent the course name and how many hours per day you'd like to study (default: 2h)
3. Optional: provide a custom Excel template (supports placeholders or auto-detection)
4. The Agent builds a config and invokes the generation script
5. Done: receive a complete day-by-day study plan Excel

**Example**:
> I have an ISO27001 recorded course, the video list is in videos.xlsx, 2 hours per day. Generate a study plan.

> Use my Excel template to generate a study plan, with video data from videos.xlsx

**Security**: The script only reads files you explicitly provide. Output is restricted from system directories. Video titles are automatically sanitized against Excel formula injection. No network access, no data upload.

---

### Français

**Aperçu** : Un générateur universel de plans d'étude pour cours enregistrés. Fonctionne avec tout type de formation/certification (ISO27001, TOGAF, DevOps, ITIL, etc.). Génère automatiquement un plan d'étude Excel jour par jour à partir d'une liste de vidéos (titre + durée).

**Trois Modes** :
1. **Modèle intégré (zéro config)** : Fournissez simplement une liste de vidéos + le nom du cours pour générer un plan standard universel à 11 colonnes
2. **Modèle personnalisé (placeholders)** : Téléversez votre propre modèle Excel, marquez `{{DAILY_DATA}}` dans la zone de données, l'outil remplit les données groupées par jour — en conservant tout le style de votre modèle
3. **Modèle personnalisé (auto-détection)** : Téléversez n'importe quel modèle Excel ; l'outil scanne les mots-clés d'en-tête pour mapper automatiquement les colonnes

**Étapes** :
1. Préparez votre liste de vidéos : soit un fichier Excel (avec colonnes titre et durée), soit envoyez des paires `nom_vidéo durée` directement dans le chat
2. Indiquez à l'Agent le nom du cours et le nombre d'heures d'étude par jour souhaité (par défaut : 2h)
3. Optionnel : fournissez un modèle Excel personnalisé (supporte les placeholders ou l'auto-détection)
4. L'Agent construit une configuration et lance le script de génération
5. Terminé : recevez un plan d'étude Excel complet jour par jour

**Exemple** :
> J'ai un cours enregistré ISO27001, la liste des vidéos est dans videos.xlsx, 2 heures par jour. Générez un plan d'étude.

> Utilisez mon modèle Excel pour générer un plan d'étude, avec les données vidéo de videos.xlsx

**Sécurité** : Le script lit uniquement les fichiers que vous fournissez explicitement. La sortie est limitée aux répertoires non-système. Les titres des vidéos sont automatiquement protégés contre l'injection de formules Excel. Pas d'accès réseau, pas de téléchargement de données.
