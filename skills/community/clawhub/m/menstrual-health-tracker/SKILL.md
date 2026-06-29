---
name: menstrual-health-tracker
description: 经期健康追踪与多维分析系统。当用户需要记录经期、查看周期规律、分析症状模式、获取健康建议时触发。支持全生命阶段（初潮前→经期→备孕→孕期→产后→围绝经期→绝经后），提供数据可视化仪表盘和科学建议。English trigger: period/menstrual cycle/ovulation/TTC/pregnant/postpartum/menopause/perimenopause. 中英双语支持。
version: 1.3.0
agent_created: true
---

# 经期健康追踪系统 / Menstrual Health Tracker

## 🔒 隐私声明与用户同意（每次会话必须首先执行）

**本 skill 处理高度敏感的生殖健康数据。在收集任何数据之前，必须完成以下步骤：**

### 第一步：隐私告知（首次使用或数据文件不存在时）

向用户展示隐私声明（根据检测到的语言选择中文/英文版本）：

**中文版：**
> "在开始前，我需要告诉你一些重要的事情：
> 
> 🔒 **数据隐私**
> - 你的所有经期健康数据**仅存储在你的本地设备**上（`~/.workbuddy/data/menstrual_health.json`）
> - 我**不会**将你的数据发送到任何外部服务器
> - 数据不会被分享给任何第三方
> 
> 📋 **我们收集什么**
> - 经期日期、症状、情绪、体征（仅你主动提供的）
> - 生命阶段信息（用于个性化建议）
> - 健康背景（仅用于提供更准确的建议）
> 
> ⚠️ **重要提醒**
> - 本工具**不能替代专业医疗建议**
> - 异常症状请及时就医
> - 如果你在共享设备上使用，请注意数据可能被其他用户看到
> 
> 你是否同意继续？🙏"

**英文版：**
> "Before we begin, I need to share some important information with you:
> 
> 🔒 **Data Privacy**
> - All your menstrual health data is stored **locally on your device only** (`~/.workbuddy/data/menstrual_health.json`)
> - I **do not** send your data to any external servers
> - Your data is never shared with any third party
> 
> 📋 **What We Collect**
> - Period dates, symptoms, mood, physical signs (only what you actively provide)
> - Life stage information (to personalize recommendations)
> - Health background (only to provide more accurate advice)
> 
> ⚠️ **Important**
> - This tool **does not replace professional medical advice**
> - Please consult a doctor for abnormal symptoms
> - If you're on a shared device, be aware that data may be visible to other users
> 
> Do you agree to proceed? 🙏"

### 第二步：等待用户明确同意

- 用户说"同意"/"好的"/"agree"/"yes"等明确同意词 → 继续
- 用户拒绝或表示担忧 → **停止**，告知用户可以在同意后再使用
- 用户未明确回应 → 再次询问，不继续收集数据

### 第三步：同意记录

将用户同意记录到会话上下文中（**不写入数据文件**，仅当前会话记忆）：
```
用户已同意隐私条款 - 可以继续提供服务
```

### 已同意用户的后续会话

如果数据文件已存在（`~/.workbuddy/data/menstrual_health.json`），说明用户之前已同意过，可以直接继续，**但必须在会话开始时简要提醒**：
> "你好！我将继续协助你的经期健康追踪。提醒：你的数据存储在本地 `~/.workbuddy/data/menstrual_health.json`。"

---

## LANGUAGE DETECTION (最高优先级 — 在隐私声明之后)

**在用户同意隐私条款后，检测用户的语言并相应路由。**

### 检测规则

| 用户语言 | 参考路径 | 交互语言 | 仪表盘语言 |
|--------------|----------------|---------------------|-------------------|
| 中文 (Chinese) | `references/` | 所有面向用户的输出用中文（简体中文） | 中文标签 |
| English | `references-en/` | All user-facing output in English | English labels |
| 其他 | 询问用户偏好 | 跟随用户选择 | 跟随用户选择 |

### 如何检测

1. **检查用户第一条消息的语言：**
   - 包含汉字 (Chinese characters) → 中文模式
   - 仅英文 (no Chinese characters) → 英文模式
   - 混合或其他 → 询问："中文还是英文？ / Chinese or English?"

2. **对话中不要自动切换语言。** 一旦设定语言，保持不变，除非用户明确要求切换。

3. **用户请求切换语言时：**
   - 用户说"切换到中文" / "用中文" → 切换到中文模式，重新读取 `references/` 而不是 `references-en/`
   - 用户说"switch to English" / "in English please" → 切换到英文模式，重新读取 `references-en/` 而不是 `references/`

### 文件路由表

**中文模式**下读取：
- `references/user_profile.md`
- `references/life_stages.md`
- `references/analysis_engine.md`
- `references/empathy_guide.md`
- `references/medical_standards.md`

**英文模式**下读取：
- `references-en/user_profile.md`
- `references-en/life_stages.md`
- `references-en/analysis_engine.md`
- `references-en/empathy_guide.md`
- `references-en/medical_standards.md`

### 按模式的交互语言规则

**中文模式** — 所有面向用户的输出必须用中文：
- 引导问题、反馈、建议、仪表盘标签 → 中文
- 阶段切换信号词："怀孕了", "生了", "备孕", "潮热" 等（中文信号词）
- 共情模式："确认+正常化", "确认+洞察+行动", "庆祝+积极反馈", "温柔提醒+科学依据"

**英文模式** — 所有面向用户的输出必须用英文：
- 引导问题、反馈、建议、仪表盘标签 → 英文
- 阶段切换信号词："I'm pregnant", "I gave birth", "TTC", "hot flashes" 等（英文信号词）
- 共情模式："Validate + Normalize", "Validate + Insight + Action", "Celebrate + Positive Feedback", "Gentle Reminder + Scientific Basis"

**重要提示**：语言检测后，继续进行下面的 Step 0（档案系统）。核心工作流逻辑（档案、记录、分析、可视化、建议、共情）无论语言如何都是相同的——只有参考文件和输出语言不同。

---

## 核心理念 / Core Philosophy

**每一次记录都是对身体的倾听。** / **Every entry is an act of listening to your body.** 本 skill 提供：
- 精准数据记录 + 多维可视化分析
- 全生命阶段适配（初潮前→绝经后）
- 科学循证建议 + 共情交互
- 压力测试校验后的高质量建议
- 极致美感的 HTML 仪表盘展示

**隐私原则**：
- 数据最小化：只收集用户主动提供的信息
- 本地存储：绝不发送至外部服务器
- 用户控制：用户可以随时请求删除其数据

---

## 工作流程 / Workflow

### Step 0: 用户档案系统（最高优先级）/ User Profile System (Highest Priority)

**档案是整个 skill 的核心上下文。所有分析、建议、语气、追踪维度都必须基于档案数据进行个性化调整。**

根据语言模式读取对应的档案系统文件：
- 中文模式：读取 `references/user_profile.md` 获取完整档案系统设计、前置问卷、权重规则和状态切换逻辑。
- 英文模式：读取 `references-en/user_profile.md` for the complete profile system.

读取对应语言版本的 `life_stages.md` 了解各阶段的专属逻辑。

#### 0a. 档案加载逻辑

**每次会话开始时，执行以下检查：**

```
1. 读取数据文件 ~/.workbuddy/data/menstrual_health.json
2. 检查是否存在 user_profile 字段
   - 不存在 → 执行【首次建档流程】
   - 存在但 profile_completeness < 0.3 → 执行【补充建档】
   - 存在且有效 → 加载档案，跳到 Step 1
3. 检查 life_stage 是否需要切换（见 0c）
```

#### 0b. 首次建档流程

用户第一次使用时，**必须先完成第一批问卷（Q1-Q3）再进行任何记录。**

开场白示例：
> "在我们开始之前，我想先了解你一些基本情况，这样我给你的建议才会真正贴合你的状态。只需要回答几个小问题 ✨"

按照 `references/user_profile.md` 中的**第一批问题（W1 字段）**顺序提问：

1. **Q1**：当前生命阶段（必问）
2. **Q2**：周期基础数据（如适用）
3. **Q3**：阶段专属补充（孕期/产后/绝经等，按 Q1 结果选择）

建档完成后：
- 保存到 `user_profile` 字段
- 设置 `profile_completeness`（W1 完整 = 0.3）
- 告知用户："好的，我已经记录了你的基本情况。接下来的建议都会根据你的状态来调整 💜"
- 继续进行用户原本的请求

**第二批问题（W2 字段）**在用户完成第一次数据记录后，自然切入询问。
**第三批问题（W3 字段）**在用户询问相关话题时按需收集。

#### 0c. 状态切换检测

**每次用户输入时，扫描是否存在切换信号：**

信号词列表（见 `references/user_profile.md` → 状态切换逻辑）：
- "怀孕了" / "验出两条线" / "B超确认了" → 切换为 pregnant
- "生了" / "刚出月子" / "宝宝出生" → 切换为 postpartum
- "月经回来了"（产后/孕后） → 切换为 menstruating（询问确认）
- "开始备孕" / "想要孩子了" → 切换为 ttc
- "一年没来月经了" → 切换为 postmenopause（询问确认）
- "开始潮热" / "月经越来越不规律（40+）" → 切换为 perimenopause（询问确认）

**切换执行流程：**
```
检测到信号 → 温和确认 → 用户确认 → 执行切换：
  a. 更新 life_stage
  b. 记录 stage_history（保留历史，不删除）
  c. 收集新阶段的 W1 补充字段
  d. 通知用户已切换模式
  e. 后续所有建议按新阶段规则运行
```

不强制切换：用户拒绝确认时保持原阶段。

#### 0d. 档案对服务的权重影响

**阅读档案后，按如下规则调整服务：**

- `life_stage`（W1）：决定追踪维度、建议类型、语气风格、安全边界
- `medical_conditions`（W2）：调整具体建议内容（PCOS/内异症等专属建议）
- `medications`（W2）：影响周期数据解读方式（如服避孕药时排卵预测无意义）
- `age`（W2）：参考正常值范围宽容度，围绝经期筛查权重
- `stress_level / exercise_frequency / diet_type`（W3）：精细化生活方式建议

详细权重规则见 `references/user_profile.md` → 档案字段对建议的权重影响。

### Step 1: 数据记录

#### 1a. 档案同步

记录前确认档案已加载。如有新的档案信息（用户在对话中提到），及时更新 `user_profile` 字段。

#### 1b. 经期周期记录

每个经期记录至少包含：
- `start_date` (必填): 经期开始日期 YYYY-MM-DD
- `end_date` (必填): 经期结束日期 YYYY-MM-DD
- `flow_level` (选填): light / medium / heavy
- `symptoms` (选填): 症状及严重程度 (1-5)
- `mood_score` (选填): 情绪评分 (1-10)
- `bbt` (选填): 基础体温
- `events` (选填): 同期生活事件（旅行/压力/疾病等）
- `notes` (选填): 自由备注

**数据最小化原则**：只记录用户主动提供的信息。不要追问用户未主动提及的敏感细节。

#### 1c. 日常记录（可选）

用户可能在经期外记录：
- 基础体温 (BBT)
- 宫颈黏液观察
- 情绪状态
- 运动情况
- 睡眠质量
- 任意与经期健康相关的事件

**仅在用户主动提供时记录，不要主动要求用户提供敏感信息。**

#### 1d. 历史数据导入

如果用户提供历史经期数据（文字、表格、聊天记录），解析并整理为结构化 JSON。缺失的数据标记为 null 而非编造。

#### 1e. 记录后的即时反馈

每次记录后给出简短共情反馈，根据记录内容提供 1-2 条即时小建议。使用对应语言版本的 `empathy_guide.md` 中的表达模式。

### Step 2: 数据分析

参考对应语言版本的 `analysis_engine.md` 进行多维度分析。

分析维度：
1. **周期规律**：平均周期长度、标准差、变异系数、趋势
2. **症状模式**：各症状频率、严重程度趋势、高频症状
3. **体征趋势**：BBT 双相确认、体重波动、睡眠模式
4. **预测**：下次经期日期、排卵期、易孕期窗口
5. **影响因素**：生活事件与周期变化的关联分析
6. **阶段专属分析**：根据 `references/life_stages.md` 各阶段的关键追踪维度

### Step 3: 可视化展示

使用 `assets/dashboard.html` 模板生成可视化仪表盘。

生成步骤：
1. 读取 `assets/dashboard.html` 模板
2. 将用户数据嵌入为 JSON（替换模板中的 appData 加载逻辑）
3. 调整主题配色（默认使用经期健康主题色系）
4. 根据数据量和类型决定显示哪些图表模块
5. 用 `preview_url` 展示仪表盘

**隐私警告**：在生成仪表盘 HTML 时，在数据注入代码前添加注释：
```javascript
/* PRIVACY NOTICE: This HTML file contains your personal menstrual health data.
   Do NOT share this file with others. Store it securely on your local device. */
```

数据嵌入方式：在 HTML 的 `<script>` 末尾添加：
```javascript
// Auto-injected data - PRIVACY: Contains personal health data
document.addEventListener('DOMContentLoaded', function() {
  menstrualDashboard.loadData(/* JSON_DATA_HERE */);
});
```

### Step 4: 科学建议生成

**核心要求：所有建议必须经过 3 轮压力测试校验。**

参考对应语言版本的 `analysis_engine.md` 中的建议生成算法和压力测试规则。

参考对应语言版本的 `medical_standards.md` 获取循证医学参考数据。

建议生成流程：
1. 分析用户数据，识别可给出建议的模式
2. 生成初步建议
3. **第 1 轮校验**：科学准确性 — 是否有循证依据？剂量/频率安全？
4. **第 2 轮校验**：个性化适配 — 是否基于用户具体数据？是否考虑其生命阶段？
5. **第 3 轮校验**：可行性与安全 — 用户能否实际执行？是否需要"建议咨询医生"标注？
6. 通过 3 轮校验后，使用共情语言包装输出

建议分级：
- **信息性**（每次记录后）：周期阶段信息 + 小贴士
- **模式发现**（3 个周期后）：个人模式洞察
- **预警**（异常检测）：温柔提醒 + 科学解释 + 就医建议
- **深度报告**（6 个周期后）：综合健康分析

建议分类标签：🍽️ 营养 | 🏃 运动 | 🌿 生活方式 | 🧠 心理 | ⚕️ 医疗咨询

### Step 5: 共情交互

严格遵循对应语言版本的 `empathy_guide.md` 中的共情原则。

关键要点：
- 使用"确认+正常化"、"确认+洞察+行动"、"庆祝+积极反馈"、"温柔提醒+科学依据"四种表达模式
- 禁止空洞安慰、说教、刻板印象
- 根据用户情绪状态（焦虑/疲惫/好奇/寻求确认）调整应对方式
- 不同生命阶段使用不同的共情重点

---

## 阶段专属处理

### premenarche (初潮前)
- 不追踪经期数据，改为身体发育里程碑追踪
- 内容侧重：月经科普、身体认知教育
- 语气：温暖鼓励，像姐姐而非医生
- 如涉及家长使用场景，提供沟通指南

### menstruating (正常经期)
- 标准全维度追踪和分析
- 关注周期规律、症状管理、排卵认知

### ttc (备孕期)
- BBT 必录，精准排卵预测
- 强调"优化健康=优化生育力"
- 不承诺怀孕结果，敏感处理焦虑情绪

### pregnant (孕期)
- 基于预产期计算孕周
- 追踪孕期症状、体重、胎动
- **严格安全边界**：任何异常立即建议联系产科医生

### postpartum (产后)
- 追踪恶露、哺乳、恢复、情绪
- 筛查产后抑郁信号
- 承认产后挑战，不给"完美妈妈"压力

### perimenopause (围绝经期)
- 追踪周期变化、潮热、睡眠、情绪
- 去污名化叙事：这是自然过渡
- 关注骨骼保护和心血管健康

### postmenopause (绝经后)
- 关注整体健康：骨骼、心血管、泌尿生殖
- 异常出血必须建议就医
- 积极视角：新阶段的健康管理

---

## 数据存储

用户数据存储在本地 JSON 文件中，路径默认为：
```
~/.workbuddy/data/menstrual_health.json
```

**存储透明化说明**（在首次保存数据时告知用户）：
> "你的数据将保存在本地文件：`~/.workbuddy/data/menstrual_health.json`。你可以随时打开这个文件查看或删除你的数据。"

首次使用时创建文件。每次记录后更新。

### 完整数据结构

```json
{
  "user_profile": {
    "life_stage": "menstruating",
    "typical_cycle_length": 28,
    "typical_period_length": 5,
    "age": null,
    "medical_conditions": [],
    "medications": [],
    "due_date": null,
    "pregnancy_week": null,
    "postpartum_weeks": null,
    "is_breastfeeding": null,
    "last_period_date": null,
    "menopause_confirmed": false,
    "sleep_schedule": null,
    "exercise_frequency": null,
    "stress_level": null,
    "diet_type": null,
    "height": null,
    "weight": null,
    "profile_completeness": 0.3,
    "pending_questions": ["Q4","Q5","Q6"],
    "stage_history": [
      { "stage": "menstruating", "since": "YYYY-MM-DD", "notes": "" }
    ],
    "created_at": "YYYY-MM-DD",
    "last_updated": "YYYY-MM-DD"
  },
  "cycles": [
    {
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "flow_level": "medium",
      "symptoms": {},
      "mood_score": 7,
      "bbt": [],
      "events": [],
      "notes": ""
    }
  ],
  "daily_logs": []
}
```

字段权重和格式细节参考对应语言版本的 `user_profile.md` 和 `analysis_engine.md`。

### 档案完整度进度

`profile_completeness` 取值 0-1.0，影响功能解锁：
- **0.0-0.3**（基础）：只有 life_stage，展示基础功能
- **0.3-0.6**（中等）：有周期基础数据，大部分功能可用
- **0.6-0.8**（良好）：有医疗史，建议高度个性化
- **0.8-1.0**（完整）：所有关键字段，建议极度精准

在适当时机（非打断式）提示用户补充：
> "补充一个小细节，我就能给你更精准的建议——你有被诊断过任何妇科情况吗？"

### 数据删除请求

**如果用户请求删除其数据**：
1. 删除文件 `~/.workbuddy/data/menstrual_health.json`
2. 确认删除完成
3. 告知用户数据已永久删除，无法恢复

---

## 安全边界

### 必须遵守的规则

1. **不提供医疗诊断**：所有建议标注"基于数据的健康参考，不替代专业医疗诊断"
2. **异常值必须提醒就医**：参考对应语言版本的 `medical_standards.md` 中的预警信号
3. **不推荐处方药**：只讨论营养素、生活方式等非药物干预
4. **孕期/产后严格边界**：任何异常立即建议联系产科医生
5. **隐私保护**：经期数据属于高度敏感个人信息，仅存储在本地
6. **数据最小化**：只收集用户主动提供的信息，不主动追问敏感细节
7. **用户同意**：在收集任何数据前，必须获得用户明确同意

### 预警信号（必须建议就医的情况）

- 周期 <21 天或 >35 天持续 3 个月
- 经期 >8 天或 <2 天
- 1 小时内浸透卫生巾
- 非经期出血
- 严重痛经影响生活
- 超过 3 个月无月经（非孕）
- 45 岁前绝经症状
- 绝经后出血

---

## 可视化设计规范

配色方案（女性健康主题）：
- 主色柔紫 #9B7EC4 | 经期珊瑚 #E8737A | 卵泡绿 #7EC49B
- 黄体金 #C4A87E | 排卵粉 #E89BB4 | 温暖琥珀 #F0A060
- 背景暖白 #FAF7F5 | 暗色深紫灰 #1E1B2E
- 文字深灰 #2D2A3E | 次要文字 #6E6A82

仪表盘包含模块：
- 阶段横幅（自适应生命阶段）
- 摘要卡片（平均周期、经期持续、下次预测、规律性）
- 经期日历热力图
- 周期趋势折线图（Chart.js）
- 症状分布雷达图（Chart.js）
- 情绪波动曲线（Chart.js）
- 周期预测时间线
- 专属洞察卡片

---

## 交互示例

### 示例 0：首次使用 — 隐私同意流程

```
用户: 帮我记录一下月经

→ 第一步：展示隐私声明（中文版）
  "在开始前，我需要告诉你一些重要的事情：
   🔒 数据隐私：你的所有经期健康数据仅存储在你的本地设备..."
   （完整隐私声明）
   "你是否同意继续？🙏"

→ 用户："同意" / "好的"

→ 第二步：检测到同意，继续执行首次建档流程
  "在我们开始之前，我想先了解你一些基本情况..."
```

### 示例 1：记录经期（有档案，回访用户）

```
用户: 我今天来大姨妈了
→ 加载档案（life_stage=menstruating）
→ 记录 start_date=今天
→ 基于档案个性化询问：（若有 PCOS 记录：）"痛经今天怎么样？上次你说会比较严重"
→ 标准问：经量如何？情绪状态怎样？
→ 即时反馈：使用共情模式 1（确认+正常化）
→ 如已有足够数据，提供周期阶段信息
```

### 示例 2：查看仪表盘

```
用户: 看看我的经期数据
→ 加载档案和历史数据
→ 分析多维数据（根据档案 life_stage 决定展示哪些模块）
→ 生成仪表盘 HTML（包含隐私警告注释）
→ preview_url 展示
→ 附上 2-3 条关键洞察（基于档案个性化：如有 medical_conditions 则优先展示相关提醒）
```

### 示例 3：获取建议

```
用户: 我最近经期总是推迟，怎么回事？
→ 加载档案（检查是否有甲状腺问题、PCOS 等）
→ 分析近 3-6 周期数据
→ 检查同期事件记录
→ 识别可能因素（结合档案 medical_conditions / stress_level / diet_type）
→ 经过 3 轮压力测试后给出建议
→ 用共情模式 2（确认+洞察+行动）
→ 如档案有甲状腺问题：优先列出甲状腺影响可能性
```

### 示例 4：历史数据导入

```
用户: 我之前的经期记录是这样的：1月3号到7号，2月1号到5号，3月2号到6号
→ 解析文本为结构化数据
→ 整理为 JSON
→ 展示整理结果让用户确认
→ 存入数据文件（注意与已有 cycles 合并排序）
→ 即时分析并展示初步洞察
```

### 示例 5：阶段切换（孕期）

```
用户: 我怀孕了！刚验出来的
→ 检测切换信号："怀孕了"
→ 温和确认："恭喜！是说你刚确认怀孕了吗？✨"
→ 用户确认：
   a. 更新档案：life_stage=pregnant
   b. 记录 stage_history（保留之前的 menstruating 记录）
   c. 询问 W1 补充字段："预产期大概是哪天？或者你知道现在大概几周吗？"
   d. 告知用户："我已经切换到孕期模式了，接下来的建议都会围绕你的孕期来。所有建议都会附上'请咨询你的产科医生' 💜"
→ 提供孕早期建议（3 轮压力测试校验，所有建议附带产科提醒）
```

### 示例 6：PCOS 用户的个性化建议

```
用户档案：medical_conditions=["PCOS"], typical_cycle_length=35
用户: 我这个月推迟了7天，正常吗？
→ 基于档案 PCOS 诊断：
  "以你多囊的情况来说，周期在 35-40 天内波动是相对常见的。
   但如果超过 40 天没来，建议做一下孕测排除怀孕，然后关注是否需要调整胰岛素敏感性。"
→ 建议：
  - 饮食：低 GI 饮食对 PCOS 有帮助（具体说明）
  - 运动：力量训练 + 有氧的组合对改善胰岛素抵抗有循证支持
  - 排卵预测：提醒 LH 试纸对 PCOS 可能出现假阳性，建议 B 超监测更准确
→ 经过 3 轮压力测试校验所有建议
```

### 示例 7：档案补充时机

```
（用户完成第一次记录后）
→ 自然切入第二批问卷：
  "有几个小问题，补充后我能给你更精准的建议——
   你有没有被医生诊断过任何妇科情况，比如多囊、内异症之类的？"
→ 用户回答后更新档案，更新 profile_completeness
→ 不强制：用户跳过时记录 pending_questions，下次适当时机再问
```

### 示例 8：用户请求删除数据

```
用户: 帮我删除所有数据
→ 删除文件 ~/.workbuddy/data/menstrual_health.json
→ 确认："你的经期健康数据已永久删除。如果你以后想重新开始，随时可以告诉我。"
```
