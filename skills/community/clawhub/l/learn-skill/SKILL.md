---
name: learn-skill
description: |
  Analyze and learn any newly installed skill through two-layer Mermaid diagrams.
  Use when: user asks to parse/analyze a new skill, understand skill structure, or visualize skill capabilities.
  Triggers: "parse this skill", "analyze skill", "understand how this skill works", "learn skill".
---

# Learn Skill - 通用技能分析工具

解析任意 Skill 的功能结构，生成可视化的双层架构图表。

## 核心方法：两层架构分析法

| 层次 | 关注点 | 产出物 |
|------|--------|--------|
| **规划层** | 技能定位、边界、输入要求 | 决策 flowchart、mindmap |
| **绘制层** | 功能分解、用户交互、API调用 | 架构图、时序图、提问样例 |

## 使用方法

### Step 1: 读取目标 Skill 的 SKILL.md

首先读取待分析技能的 SKILL.md 文件，了解其：
- `description` - 技能描述和触发场景
- 功能列表和命令示例

### Step 2: 生成两层分析

根据 SKILL.md 内容，生成两层架构图表：

**第一层（规划层）：**
```mermaid
flowchart TB
    A["🔍 用户请求"] --> B{类型判断}
    B -->|匹配技能| C[✅ 使用该 Skill]
    B -->|不匹配| D[❌ 不适用]
    C --> E["📍 输入要求"]
    E --> F["调用 API/工具"]
    F --> G["返回结果"]
    
    style C fill:#00d9ff,color:#000
    style D fill:#ff6b6b,color:#fff
```

**第二层（绘制层）：**
- 用户提问样例 flowchart
- 核心功能架构图（命令类型 → 输出格式 → 格式化代码）
- 完整交互时序图

### Step 3: 输出 HTML 报告

生成包含所有图表的 HTML 文件供用户查看。

**HTML 输出规范（确保文字清晰可见）：**

- 页面背景使用深色渐变时，正文文字使用浅色 `#eee` 或白色
- 表格使用白色背景 `#fff` + 深色文字 `#1a1a2e` 提供高对比度
- 代码块使用浅色背景（如 `rgba(0,217,255,0.15)`）+ 深色文字
- 标题使用渐变色或亮色（`#00d9ff`, `#00ff88`）确保与背景区分
- 图表容器使用白色背景避免与深色页面混色

---

## 示例：Weather Skill 分析

下面以 Weather Skill 为例，展示两层架构的完整输出。

### 第一层：规划层 - 技能定位与适用范围

```mermaid
flowchart TB
    A["🔍 用户查询天气"] --> B{查询类型判断}
    
    B -->|天气/温度/预报| C[✅ 使用 Weather Skill]
    B -->|历史数据| D[❌ 不适用]
    B -->|气候趋势分析| D
    B -->|极端天气警报| D
    B -->|航空/航海气象| D
    
    C --> E["📍 需要提供位置"]
    E --> F["城市名/地区/机场代码"]
    F --> G["调用 wttr.in API"]
    G --> H["返回天气数据"]
    
    style C fill:#00d9ff,color:#000
    style D fill:#ff6b6b,color:#fff
```

```mermaid
mindmap
  root((Weather Skill))
    适用场景
      当前天气查询
      温度询问
      降雨预测
      未来天气预报
      出行天气规划
    不适用场景
      历史天气数据
      气候趋势分析
      极端天气警报
      专业气象服务
    数据来源
      wttr.in
      Open-Meteo
    特殊要求
      需要提供位置信息
      支持城市名/机场码
      无需API密钥
```

### 第二层：绘制层 - 核心功能架构与提问样例

#### 💬 用户提问样例

```mermaid
flowchart LR
    Q1["❓ '北京今天天气怎么样？'"] 
    Q2["❓ '东京明天会下雨吗？'"]
    Q3["❓ '上海周末温度多少？'"]
    Q4["❓ '伦敦下周天气预报'"]
    
    Q1 -->|城市+时间| R1["当前天气查询"]
    Q2 -->|城市+时间+降水| R2["降雨预测查询"]
    Q3 -->|城市+时间段| R3["周末预报查询"]
    Q4 -->|城市+时间范围| R4["周预报查询"]
```

#### ⚙️ 核心功能架构

```mermaid
flowchart LR
    subgraph 命令类型
        A1["当前天气 curl wttr.in/London?format=3"] 
        A2["3天预报 curl wttr.in/London"]
        A3["一周预报 curl wttr.in/London?format=v2"]
        A4["指定日期 curl wttr.in/London?1"]
    end
    
    subgraph 输出格式
        B1["单行摘要 format=3"]
        B2["详细条件 ?0"]
        B3["JSON输出 format=j1"]
        B4["PNG图片 .png"]
    end
    
    subgraph 格式化代码
        C1["%l 位置"]
        C2["%c 天气状况"]
        C3["%t 温度"]
        C4["%f 体感温度"]
        C5["%w 风速"]
        C6["%h 湿度"]
        C7["%p 降水量"]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    
    B1 --> C1
    B1 --> C2
    B1 --> C3
```

#### 时序图 - 完整交互流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant A as Agent
    participant W as wttr.in API
    
    U->>A: "伦敦天气怎么样？"
    A->>A: 识别为天气查询请求
    A->>W: curl "wttr.in/London?format=j1"
    W->>A: 返回JSON天气数据
    A->>A: 解析数据提取关键信息
    A->>U: 格式化回复 🌤️ 伦敦: 18°C 感觉像: 16°C 西风 12km/h 湿度 65%
    
    U->>A: "明天会下雨吗？"
    A->>W: curl "wttr.in/London?format=%p"
    W->>A: 返回降水信息
    A->>U: 降水概率回复
```

---

## 输出模板

当用户要求分析新 Skill 时，按以下格式组织输出：

```
# {Skill名称} 分析

## 第一层：规划层 - 技能定位与适用范围
[flowchart + mindmap]

## 第二层：绘制层 - 核心功能架构与提问样例
[用户提问样例 flowchart]
[核心功能架构图]
[时序图]
```

## 相关资源

- **Mermaid 图表语法**：`mermaid-diagrams` Skill
- **技能创建规范**：`skill-creator` Skill
