---
name: medical-training-report
version: "3.0.0"
description: "医疗器械培训活动报告自动撰写技能 v3.0。当用户需要为消化内镜培训课程（如ERCP、EUS-FNA、ESD等技术培训）撰写活动报告时触发。v3.0支持三种会议模式（纯线下offline/线上+线下hybrid/纯线上online），统一模板输出。支持从日程海报、签到表、成绩表、PPT照片、Excel（成绩/QUIZ/反馈）等多种材料中提取信息。触发场景：用户提到活动报告、培训报告或提供了培训会议的相关材料。"
agent_created: true
tags:
  - 医疗
  - 内镜
  - 培训
  - 活动报告
  - ERCP
  - EUS
  - ESD
  - 消化内镜
  - 报告生成
  - medical
  - training
---

# 医疗器械培训活动报告生成 v3.0

## 概述

本技能用于自动生成消化内镜技术培训活动报告。v3.0 核心升级：**三种会议模式公用一个统一模板**。

### 三种会议模式

| 模式 | meeting_mode | 典型场景 | 核心内容 |
|------|-------------|---------|---------|
| 纯线下 | `offline` | 全天线下培训班 | 理论授课+操作+病例讨论+总结 |
| 线上+线下 | `hybrid` | LMS线上+线下实操 | 线上部分(课程+QUIZ)+线下(同offline) |
| 纯线上 | `online` | 在线培训/直播 | 根据会议文字版+日程提炼每个环节3-5句+总结 |

### 报告统一结构

1. **基本信息表** — 8 字段（名称/主办/时间/地点/专家/规模/员工/项目介绍）
2. **一、活动致辞** — 主持人+致辞专家+开场致辞内容
3. **二、活动日程** — 时间|内容|讲者/专家
4. **三、会议详细内容** — 按模式分支
5. **四、总结** — 参会人数+满意度+各环节亮点
6. 落款：[培训部门]

## 触发条件

- 用户提到「写活动报告」「培训报告」「活动报告书」「生成报告」
- 用户发送培训材料：海报/PPT照片/Excel/日程/签到表/成绩表
- 用户说「帮我生成上次培训的报告」

## 首次对话提示

**当技能被触发时，第一步必须先输出以下提示语，引导用户选择会议模式并准备材料：**

---

请根据以下不同的会议形式，给我相对应的会议信息：

### 1. 纯线下培训班 (offline)

适合全天线下实操培训，需要提供：
- 📋 **日程海报** — 用于提取会议基本信息、日程表、专家名单
- 📸 **理论授课PPT照片** — 每个讲座的PPT截图，AI自动总结内容摘要
- 📊 **操作考核成绩表** — Excel或照片，含学员姓名+医院+成绩
- 📋 **病例讨论信息** — 发表人、医院、题目、病例概述
- 📸 **签到表/合影照片** — 可选

### 2. 线上+线下混合培训 (hybrid)

适合LMS线上理论学习+线下实操，需要提供：
- 📋 纯线下培训班所需的全部材料
- 📊 **LMS线上课程明细** — Excel导出表
- 📝 **QUIZ答题情况** — Excel或截图，含学员姓名+得分
- 📋 **学员反馈打分** — Excel或截图（满意度等），可选

### 3. 纯线上培训 (online)

适合在线直播/研讨会，需要提供：
- 📝 **会议文字版转录** — 平台导出的会议记录/文字稿
- 📋 **会议日程** — 时间、环节、讲者
- 📋 **参会人员信息** — 人数、主要专家等

---

> 请告诉我您的会议属于哪一种形式，然后把相应材料发给我，我会自动提取信息并生成报告。

---

### 第一步：识别会议模式

根据用户提供的材料和描述判断模式：

- **纯线下**：只有线下议程、理论授课PPT、操作考核、病例讨论 → `offline`
- **线上+线下**：有LMS/线上课程+QUIZ+线下日程 → `hybrid`
- **纯线上**：有会议文字版转录/会议日程+参会名单 → `online`

> 默认假设为 `hybrid`（最常见）。

### 第二步：提取信息

根据模式从用户材料中提取对应字段：

#### 通用字段（所有模式）

- `basic_info`：会议名称、主办单位、时间、地点、专家（姓名+医院）、规模、参加员工
- `activity_opening`：致辞专家（从海报提取）、主持人（如未提供默认「[培训部门]」）、致辞内容（如未提供生成常规开场致辞）
- `schedule`：日程表。从海报图片提取；如没有则追问日程
- `project_intro`：如未提供，根据课程类型自动生成专业描述

#### offline 特有字段

- `detailed_content.lectures[]`：理论授课（每个讲座：题目、讲者、医院、**内容摘要**）
  - 内容摘要来源：用户提供的PPT照片 → AI 根据PPT内容总结2-3句话
  - 如无PPT则根据题目推断
- `detailed_content.operations[]`：操作环节。每个操作：名称、概况、考核统计、**成绩表**
  - 成绩表优先从 Excel 自动解析
- `detailed_content.case_discussions[]`：病例讨论。每个病例：发表人、医院、题目、病例概述
  - 内容来源：用户提供的病例讨论PPT照片

#### hybrid 特有字段（在 offline 基础上增加）

- `detailed_content.online.lectures[]`：线上理论课程列表（题目+讲者）
- `detailed_content.online.quiz`：QUIZ答题情况（参与人数+平均分+满分）
  - 优先从 Excel 自动解析

#### online 特有字段

- `detailed_content.online_sessions[]`：每个会议环节（标题+讲者+3-5句话总结）
  - 总结来源：用户提供的会议文字版本 → AI 提炼每个环节的核心内容
- `schedule`：如果用户提供了会议日程，同时填入

### 第三步：AI 智能生成

在构建 JSON 之前，AI 需要对原始材料进行智能处理：

#### 3.1 活动致辞生成

如果用户未提供致辞内容，自动生成 2-3 句常规开场致辞：

```
致辞专家对各位学员的到来表示热烈欢迎，指出消化内镜技术的规范化培训
对于提高基层医疗机构的诊疗水平具有重要意义，希望学员们珍惜学习机会，
通过理论学习和实践操作，切实提升自身技术水平，更好地服务于临床患者。
```

#### 3.2 PPT 照片内容总结

用户发送的理论授课 PPT 照片 → AI 逐页浏览 → 总结2-3句主要内容：
- 讲座题目和讲者（从PPT标题页提取）
- 核心知识点（2-3个关键要点）
- 不要逐字翻译PPT，而是概括

#### 3.3 线上会议文字版处理

纯线上模式：用户提供会议平台导出的文字记录 → AI 按日程环节分段 → 每段提炼3-5句话：
- 讲了什么主题
- 核心观点/知识点
- 互动情况（如有）

#### 3.4 总结生成规则

总结必须包含：
- 参会人数（从材料中提取或用户提供）
- 满意度评价人数和平均分（如有反馈表则自动解析）
- 各环节亮点：授课亮点、操作亮点、病例讨论亮点（如有）
  - 如用户未明确提供亮点描述，AI 根据各环节内容摘要生成

### 第四步：生成报告

将 AI 处理后的数据构建为 JSON，执行脚本：

```bash
C:/Users/om002228/.workbuddy/binaries/python/envs/default/Scripts/python.exe scripts/generate_report.py input.json output.docx
```

脚本自动：
1. 解析 Excel（成绩/QUIZ/反馈）
2. 成绩按降序排列并重新编号
3. 自动计算平均分
4. 按 meeting_mode 生成对应的详细内容结构

### 第五步：输出与确认

用 present_files 呈现 docx，告知用户：
1. 报告文件路径
2. 会议模式
3. AI 自动生成的内容（致辞、PPT总结、亮点等）提醒审阅
4. 成绩统计摘要

## v3.0 JSON 数据结构

```json
{
  "meeting_mode": "hybrid",
  "basic_info": {
    "meeting_name": "会议全称",
    "organizer": "主办单位",
    "meeting_time": "日期/时间",
    "meeting_location": "地点",
    "experts": "专家名+医院",
    "scale": "参训人数",
    "staff": "参加员工",
    "project_intro": "项目介绍"
  },
  "activity_opening": {
    "expert": "致辞专家名",
    "host": "主持人",
    "speech": "致辞内容（可选，AI自动生成）"
  },
  "schedule": [
    {"time": "08:00-08:30", "content": "签到", "speaker": "/"}
  ],
  "detailed_content": {
    // hybrid 模式：线上部分
    "online": {
      "lectures": [{"title": "课程名", "speaker": "讲者"}],
      "quiz": {
        "excel_path": "C:/data/quiz.xlsx",  // 可选，自动解析
        "participants": "16",
        "avg_score": "3.8",
        "full_score": "5"
      }
    },
    // 理论授课（offline/hybrid）
    "lectures": [
      {
        "title": "讲座题目",
        "speaker": "讲课人",
        "hospital": "讲课人医院",
        "content_summary": "根据PPT照片总结的内容"
      }
    ],
    // 操作环节（offline/hybrid）
    "operations": [
      {
        "name": "ERCP模型操作与考核",
        "course_name": "ERCP",
        "summary": "操作概况描述",
        "excel_path": "C:/data/scores.xlsx",
        "assessment": {"participants": "12", "avg_score": "69.2", "full_score": "100"},
        "scores": [{"name": "...", "province": "...", "hospital": "...", "score": 75}]
      }
    ],
    // 病例讨论（offline/hybrid）
    "case_discussions": [
      {
        "presenter": "发表人",
        "hospital": "医院",
        "topic": "题目",
        "summary": "病例概述"
      }
    ],
    // 纯线上会议环节
    "online_sessions": [
      {
        "title": "环节名称",
        "speaker": "讲者",
        "summary": "3-5句话总结"
      }
    ]
  },
  "summary": {
    "total_participants": "12",
    "feedback_respondents": "12",
    "feedback_avg_score": "4.8分",
    "highlights": {
      "lecture": "授课亮点",
      "operation": "操作亮点",
      "case_discussion": "病例讨论亮点"
    },
    "improvements": "改进建议"
  },
  "group_photo_path": "C:/photos/",
  "signature": "[培训部门]"
}
```

## 资源文件说明

| 文件 | 用途 |
|------|------|
| `scripts/generate_report.py` | 报告生成脚本 v3.0，支持三种会议模式 |
| `references/info_collection_template.md` | 信息收集模板 |
| `references/template_structure.md` | 文档模板结构说明 |
| `references/course_intro_templates.md` | 课程介绍模板库 |
| `assets/template.docx` | 原始模板文档 |

## Excel 自动解析

脚本支持三种 Excel 独立导入（v2.2 功能，v3.0 保留）：

| Excel 类型 | JSON 路径 | 说明 |
|-----------|----------|------|
| 操作考核成绩 | `detailed_content.operations[].excel_path` | 自动解析、排序、算平均分 |
| QUIZ 答题 | `detailed_content.online.quiz.excel_path` | 明细/汇总两种格式自动识别 |
| 学员反馈 | feedback Excel 待扩展 | 手动填入 summary |

## 注意事项

1. **字体**：正文宋体，标题微软雅黑
2. **落款**：默认「[培训部门]」
3. **PPT 总结**：提醒用户审阅 AI 根据 PPT 生成的内容
4. **Excel 路径**：使用绝对路径，脚本自动容错
5. **meeting_mode**：必填字段，不填默认 hybrid
