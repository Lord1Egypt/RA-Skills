# 孤舟小说工作室 - 文件格式规范

> **版本**：v1.0  
> **更新日期**：2026-04-29

---

## 目录

1. [目录结构规范](#1-目录结构规范)
2. [文件命名规范](#2-文件命名规范)
3. [JSON格式规范](#3-json格式规范)
4. [Markdown格式规范](#4-markdown格式规范)
5. [模板文件](#5-模板文件)

---

## 1. 目录结构规范

### 1.1 整体目录结构

```
novel-workspace/
├── projects/                              # 所有小说项目
│   └── {project-name}/                    # 单个项目目录
│       │
│       ├── project.json                   # 项目基础配置
│       │
│       ├── outline/                       # 大纲目录
│       │   ├── outline.json              # 大纲JSON
│       │   ├── outline.md                # 大纲Markdown
│       │   ├── chapters.md               # 章节规划
│       │   └── foreshadowing.md          # 伏笔规划
│       │
│       ├── characters/                    # 人物档案
│       │   ├── protagonist.json          # 主角档案
│       │   ├── supporting/               # 配角目录
│       │   │   ├── character-a.json
│       │   │   └── character-b.json
│       │   └── relationships.json        # 人物关系图
│       │
│       ├── world/                         # 世界观目录
│       │   ├── setting.json              # 基础设定
│       │   ├── locations.json            # 地点设定
│       │   └── timeline.json             # 时间线
│       │
│       ├── chapters/                      # 章节目录
│       │   ├── chapter-01.md             # 第1章
│       │   ├── chapter-02.md
│       │   └── ...
│       │
│       ├── memory/                        # 记忆系统
│       │   ├── style-dna.json           # 风格DNA
│       │   ├── memory.json              # 主记忆文件
│       │   ├── active/                   # 活跃记忆
│       │   │   ├── current-plot.json
│       │   │   ├── active-characters.json
│       │   │   └── unresolved-foreshadowing.json
│       │   └── archive/                 # 归档记忆
│       │       └── chapter-01-summary.json
│       │
│       ├── qa-reports/                    # 质检报告
│       │   ├── qa-chapter-01.md
│       │   └── qa-chapter-02.md
│       │
│       └── assets/                        # 辅助资源
│           └── illustrations/             # 插画配图
│
├── research/                              # 调研报告库
│   └── {project-name}/                    # 按项目组织
│       └── research-report.json
│
├── style-library/                         # 风格库
│   ├── extracted/                         # 用户提取的风格
│   │   └── {style-id}.json
│   └── presets/                           # 预设风格
│       ├── shuoshurenv.json
│       ├── maoni.json
│       └── ...
│
└── templates/                             # 模板库
    ├── character-template.json
    ├── chapter-template.md
    └── outline-template.json
```

### 1.2 项目目录创建规则

```bash
# 项目名称规范
- 仅使用中文、英文、数字、下划线、短横线
- 禁止使用空格和特殊字符
- 长度限制：2-30个字符

# 示例
星际迷途/         ✓ 正确
my-novel/        ✓ 正确
project_001/     ✓ 正确
我的小说/         ✗ 错误（中文在某些系统可能有问题）
```

---

## 2. 文件命名规范

### 2.1 命名规则表

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| 项目配置 | `project.json` | `星际迷途/project.json` |
| 大纲JSON | `outline.json` | `星际迷途/outline/outline.json` |
| 大纲Markdown | `outline.md` | `星际迷途/outline/outline.md` |
| 章节规划 | `chapters.md` | `星际迷途/outline/chapters.md` |
| 伏笔规划 | `foreshadowing.md` | `星际迷途/outline/foreshadowing.md` |
| 章节文件 | `chapter-{序号}.md` | `星际迷途/chapters/chapter-01.md` |
| 人物档案 | `{角色名}.json` | `星际迷途/characters/李明.json` |
| 关系图谱 | `relationships.json` | `星际迷途/characters/relationships.json` |
| 记忆文件 | `memory.json` | `星际迷途/memory/memory.json` |
| 风格DNA | `style-dna.json` | `星际迷途/memory/style-dna.json` |
| 质检报告 | `qa-chapter-{序号}.md` | `星际迷途/qa-reports/qa-chapter-01.md` |
| 调研报告 | `research-report.json` | `research/星际迷途/research-report.json` |

### 2.2 章节序号规范

```markdown
# 序号格式
chapter-01.md    ✓ 正确（两位数补零）
chapter-1.md     ✗ 不推荐
chapter_01.md    ✗ 错误（使用下划线）

# 批量处理时使用
chapter-{01..50}.md  # Bash展开
```

---

## 3. JSON格式规范

### 3.1 编码与格式

```json
{
  "编码": "UTF-8",
  "缩进": "2空格",
  "无尾部逗号": true,
  "键名双引号": true
}
```

### 3.2 project.json 模板

```json
{
  "project_id": "uuid-string",
  "project_name": "项目名称",
  "genre": "题材类型",
  "target_platform": "目标平台",
  "target_length": "预计总字数",
  "current_chapter": 1,
  "total_chapters_planned": 50,
  "created_at": "2026-04-29",
  "last_updated": "2026-04-29",
  "status": "writing|paused|completed",
  "style_dna_id": "关联的风格DNA ID",
  "outline_id": "关联的大纲ID"
}
```

### 3.3 人物档案模板

```json
{
  "character_id": "uuid-string",
  "name": "角色姓名",
  "role": "protagonist|supporting|antagonist|minor",
  "basic_info": {
    "age": 28,
    "gender": "male|female|other",
    "occupation": "职业"
  },
  "personality": {
    "core_traits": ["特质1", "特质2"],
    "flaws": ["缺点1"],
    "speech_pattern": "说话风格描述"
  },
  "goals": {
    "surface_goal": "表面目标",
    "deep_goal": "深层目标"
  },
  "backstory": "背景故事摘要",
  "current_state": {
    "location": "当前位置",
    "emotional_state": "当前情绪",
    "physical_condition": "身体状况"
  },
  "relationships": [
    {
      "target_id": "关联角色ID",
      "relationship_type": "friend|enemy|family|romantic",
      "description": "关系描述"
    }
  ],
  "dialogue_samples": [
    "「对话示例1」",
    "「对话示例2」"
  ]
}
```

### 3.4 Style-DNA 模板

```json
{
  "style_id": "uuid-string",
  "style_name": "风格名称",
  "created_at": "2026-04-29",
  "source_texts": ["文本片段1", "文本片段2"],
  
  "linguistic_features": {
    "sentence_length": "short|medium|long|mixed",
    "paragraph_length": "short|medium|long|mixed",
    "vocabulary_level": "simple|moderate|advanced|mixed",
    "formality_level": "casual|neutral|formal"
  },
  
  "narrative_voice": {
    "perspective": "first|second|third",
    "tone": "serious|humorous|ironic|lyrical",
    "distance": "intimate|neutral|detached"
  },
  
  "dialogue_style": {
    "quotation_marks": "「」|「」|\"\"'",
    "dialogue_tags": "minimal|moderate|heavy",
    "speech_patterns": ["特点1", "特点2"]
  },
  
  "pacing_features": {
    "rhythm": "fast|moderate|slow|varied",
    "scene_transitions": "abrupt|gradual|mixed"
  },
  
  "genre_markers": ["标记1", "标记2"],
  "memorable_phrases": ["经典句式1", "经典句式2"]
}
```

### 3.5 调研报告模板

```json
{
  "project_name": "项目名称",
  "created_at": "2026-04-29",
  "genre_analysis": {
    "current_trends": ["趋势1", "趋势2"],
    "platform_preference": "平台建议"
  },
  "competitor_analysis": [
    {
      "title": "竞品标题",
      "strengths": ["优势1", "优势2"],
      "differentiation_angles": ["角度1"]
    }
  ],
  "target_audience": {
    "age_range": "18-35",
    "preferences": ["偏好1", "偏好2"]
  },
  "writing_recommendations": ["建议1", "建议2"],
  "creative_directions": ["方向1", "方向2"]
}
```

### 3.6 章节摘要模板

```json
{
  "chapter_id": 1,
  "title": "第一章 标题",
  "summary": "本章摘要（100-200字）",
  "key_events": [
    {
      "event": "事件描述",
      "significance": "重要性",
      "characters_involved": ["角色名"]
    }
  ],
  "character_states": [
    {
      "name": "角色名",
      "state_before": "章前状态",
      "state_after": "章后状态",
      "change_description": "变化说明"
    }
  ],
  "foreshadowing": {
    "planted": ["埋设的伏笔"],
    "resolved": ["回收的伏笔"]
  },
  "word_count": 3500,
  "created_at": "2026-04-29"
}
```

---

## 4. Markdown格式规范

### 4.1 章节文件格式

```markdown
# 第一章 章节标题

正文内容...

---

[章节元信息]
- 字数：3500+
- 伏笔：本章埋设的伏笔列表
- 人物状态：本章结束时的人物状态
- 下一章预告：（可选）
```

### 4.2 质检报告格式

```markdown
# 质检报告：第X章

## 检查结果汇总
- ✅ 通过项：N项
- ⚠️ 警告项：M项
- ❌ 问题项：K项

## 问题详情

### ❌ 问题1：人物OOC [严重]
**位置**：第3段
**问题描述**：人物A的性格与设定不符
**当前内容**：「......」
**人物设定**：A是冷静理性的性格
**建议修改**：「......」

### ⚠️ 警告1：伏笔未埋设 [中等]
**位置**：第5段
**问题描述**：大纲要求埋设伏笔X，但未体现
**建议**：在适当位置添加...

## 优先修复清单
1. [🔴 高] 人物OOC问题
2. [🔴 高] 逻辑漏洞
3. [🟡 中] 伏笔遗漏
```

### 4.3 大纲Markdown格式

```markdown
# 《项目名称》大纲

## 基础信息
- 题材：
- 类型：
- 预计字数：

## 核心设定
### 世界观
...

### 主要人物
1. 主角1
2. 主角2

## 故事主线
### 第一幕（1-10章）
...

### 第二幕（11-30章）
...

### 第三幕（31-50章）
...

## 章节规划
详见 `chapters.md`

## 伏笔设计
详见 `foreshadowing.md`
```

---

## 5. 模板文件

### 5.1 人物模板 (templates/character-template.json)

```json
{
  "character_id": "",
  "name": "",
  "role": "",
  "basic_info": {
    "age": null,
    "gender": "",
    "occupation": ""
  },
  "personality": {
    "core_traits": [],
    "flaws": [],
    "speech_pattern": ""
  },
  "goals": {
    "surface_goal": "",
    "deep_goal": ""
  },
  "backstory": "",
  "current_state": {
    "location": "",
    "emotional_state": "",
    "physical_condition": ""
  },
  "relationships": [],
  "dialogue_samples": []
}
```

### 5.2 章节模板 (templates/chapter-template.md)

```markdown
# 第X章 章节标题

正文内容...

---

[章节元信息]
- 字数：
- 伏笔：
- 人物状态：
```

### 5.3 项目模板 (templates/project-template/)

已创建完整项目目录模板，参考 `templates/project-template/` 目录。

---

## 附录：编码规范

| 项目 | 规范 |
|------|------|
| 字符编码 | UTF-8 |
| 换行符 | LF（Unix风格） |
| 缩进 | 2空格（JSON）/ 正常缩进（Markdown） |
| 行尾空格 | 删除 |
| 文件末尾 | 保留一个换行符 |

---

*规范版本：v1.0 | 最后更新：2026-04-29*
