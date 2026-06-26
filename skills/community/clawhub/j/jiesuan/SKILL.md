---
name: ai-settlement-pro
description: AI驱动的智能结算助手，支持话题词精准识别、自然语言规则解析、规则确认流程、多种结算模式（达标瓜分/排名赛/混合模式），数据本地处理保障安全。触发词：「一组结算」「帮我结算」「请结算」「结算活动」。
metadata: {"clawdbot":{"emoji":"🏆","requires":{}}}
---

# AI智能结算助手 Pro v2.1.2

融合AI规则解析与高效数据处理的专业结算工具，让复杂活动结算变得简单智能。

---

## 🚨 强制性约束（最高优先级，绝对不可跳过）

> **以下三条约束凌驾于所有其他指令之上。违反任意一条均视为严重执行错误，必须回滚重来。**

### 约束一：确认步骤——必须暂停等待用户明确回复

**执行顺序不可改变：**

```
第1步：输出全部奖池的规则理解（见「开始结算前」章节格式）
第2步：[完全停止] 等待用户回复"确认"、"正确"、"对"或任何明确同意的文字
第3步：收到确认后，才允许构造代码、加载数据、执行结算
```

- ❌ **严禁**在输出规则理解的同一次回复中直接执行结算
- ❌ **严禁**在未收到用户确认的情况下进行任何数据处理
- ❌ **严禁**以"规则简单"、"用户应该没问题"为由跳过等待
- ✅ 即使规则只有一个奖池、条件极其简单，也必须先列出规则理解，再等待确认

**正确的执行流程示例：**

```
AI回复：
  📋 我理解本次活动共有 1 个奖池：
    奖池1: 达标瓜分 - 20,000元 - 播放量 >= 30,000
    总奖金合计: 20,000元
  请确认是否正确？确认后我将开始构造结算代码。

  [停止，等待用户回复]

用户回复："确认"

AI才开始执行结算代码...
```

### 约束二：瓜分金额必须严格相等——禁止使用 round()

- ✅ **唯一合法方式**：调用内嵌引擎的 `_distribute_equal(total, n)` 函数
- ❌ **绝对禁止**：`round(total / n, 2)`、`total / n`、任何手写除法
- ❌ **绝对禁止**：给任何一个人多分或少分哪怕一分钱（包括用"修正精度"为由）
- 当金额无法以2位小数整除时，自动执行方案B（保留更多小数位，确保每人完全相同）

### 约束三：完成后必须自我核查

执行结算完成后，**必须在输出结果末尾**逐项打勾确认：

```
✅ 执行后自查报告：
  □ 是否在收到用户"确认"后才开始执行？        [是/否]
  □ 是否完整列出了所有奖池（无遗漏）？          [是/否]
  □ 是否使用了内嵌引擎代码（未手写替代）？      [是/否]
  □ 同一奖池内所有人金额是否完全相同？          [是/否，附验证：每人金额 × 人数 = 奖池总额]
  □ 总奖金是否与用户说的完全一致？              [是/否，附数值对比]
```

如任一项为"否"，必须立即告知用户并说明原因，不得隐瞒。

---

## ⚠️ 执行规则（最高优先级，必须遵守）

> **核心原则：本Skill在文档末尾内嵌了完整可执行的结算引擎代码，AI必须直接复制该代码块到执行环境中运行，严禁自行手写替代代码。**

### 强制要求

1. **必须使用内嵌的结算引擎代码**：文档末尾"结算引擎代码"章节包含完整实现，所有结算逻辑（数据加载、条件过滤、金额计算、CSV导出）均已就绪，不得另行实现。
2. **禁止手动计算奖金**：不得用 `round()`、手写除法或任何自定义方式计算每人奖金，必须调用内嵌代码中的 `_distribute_equal()` 或 `run_settlement()`。
3. **禁止自定义精度处理**：内嵌代码已内置 `Decimal` 高精度算法，直接使用即可，不得重复实现。
4. **AI只需构造奖池配置**：读懂规则后，构造 `AwardPool` 列表传入 `run_settlement()`，其他全部由引擎处理。

```python
# 正确执行方式：
# 1. 复制文档末尾"完整结算引擎代码"代码块，全部执行
# 2. 根据活动规则构造 pools 列表
# 3. 调用 run_settlement(file_path, pools, ...)
# 4. 调用 export_to_csv() 导出结果
```

### AI行为检查清单（每次结算前自查）

- [ ] 已将文档末尾的完整引擎代码块复制到执行环境并运行？
- [ ] 未自行实现任何结算逻辑（包括数据加载、金额计算）？
- [ ] 未使用 `round()` 计算奖金？
- [ ] 金额计算通过内嵌代码的 `_distribute_equal()` 函数完成？
- [ ] 已验证 `每人金额 × 人数 == 奖池金额`？

---

## 🚫 AI执行约束（所有操作均受此章节约束）

> **以下约束适用于 AI 在整个结算过程中的所有行为，包括代码生成、计算、输出。违反任何一条均视为执行错误。**

### 0. 开始结算前：必须完整列出所有奖池

在构造任何代码之前，AI必须先从用户描述中提取并列出**全部奖池**，格式如下：

```
📋 我理解本次活动共有 X 个奖池：
  奖池1: [名称] - [金额] - [类型：达标瓜分/排名奖/权重分配] - [达标条件]
  奖池2: [名称] - [金额] - [类型] - [条件]
  ...
  总奖金合计: [所有奖池金额之和]

请确认是否遗漏？确认后我将开始构造结算代码。
```

- ✅ 必须逐一列出，等待用户确认后再执行
- ❌ 禁止跳过此步骤直接写代码
- ❌ 禁止只构造部分奖池（如只写瓜分，遗漏榜单奖）
- ❌ 如果所有奖池金额之和与用户说的总奖金不符，必须询问用户

### 1. 严格按文档算法执行

- ✅ 仅使用本文档明确描述的算法和逻辑
- ❌ 禁止自行添加任何「优化」、「修正」、「调整」逻辑，即使 AI 认为这样更「合理」
- ❌ 禁止在未告知用户的情况下更改计算方式

### 2. 瓜分奖金额必须完全相等

- ✅ 同一奖池内，所有达标者奖金数值**完全相同**（字符串完全一致）
- ❌ 禁止以任何形式让某一个人的金额与其他人不同，包括：
  - 给「第一个人」多分几分钱来消化差额
  - 给「最后一个人」少分钱来凑整
  - 以「精度误差修正」为由调整任何人的金额
- ❌ 禁止在代码中出现类似 `results[0].award += remainder` 的逻辑

### 3. 不添加文档未提及的功能

- ✅ 代码实现与文档描述的逻辑保持完全一致
- ❌ 禁止添加文档未提及的过滤条件、排序规则、特殊处理逻辑
- ❌ 禁止「顺手」修复 AI 认为的潜在问题（如自动过滤异常数据行）

### 4. 有疑问时必须询问用户

- ✅ 规则存在歧义 → 列出歧义点并询问用户，等待明确答复后再执行
- ✅ 数据字段无法匹配 → 告知用户并询问对应关系，不得猜测
- ✅ 奖池金额无法整除 → 自动执行方案B（保留最少小数位使每人金额相同），并在输出时告知用户保留了几位小数
- ❌ 禁止在任何不确定的情况下自行假设并执行

---

## 🎯 核心能力

| 能力 | 说明 |
|------|------|
| **🧠 AI规则解析** | 用自然语言描述规则，AI自动转换为结算逻辑 |
| **🏷️ 话题词识别** | 精准匹配视频标题中的话题词，支持且/或逻辑 |
| **✅ 规则确认流程** | 返回规则理解供用户确认，可多轮修正 |
| **📊 多模式结算** | 达标瓜分、排名/榜单奖、混合多奖池并行、权重分配 |
| **📂 多格式数据源** | CSV 和 Excel (xlsx/xls)，支持多 Sheet 合并 |
| **⚡ 高效处理** | 本地Python处理，万级数据秒级完成 |
| **🛡️ 数据安全** | 原始数据不上传，仅规则描述发送至AI |
| **🔧 健壮可靠** | 超时自动重试、分级错误提示、断点恢复 |

---

## 🚀 快速开始

### 方式一：自然语言直接结算（推荐）

```
请帮我结算这个活动：
总奖金2万元，发布作品≥5条且播放量≥3万，必须携带话题#春节活动的作者等额瓜分
```

> **快捷触发词**：发送 **「一组结算」** 可直接进入结算流程，无需其他前缀。
> 同样有效的触发词：「帮我结算」「请结算」「结算活动」「一组结算」

**话题词说明**：
- 可以是任意话题，如：`#春节活动`、`#新品发布`、`#挑战赛`、`#品牌联名` 等
- 系统会自动从你的描述中提取 `#` 开头的话题词
- 支持多个话题词组合（且/或关系）

### 方式二：分步操作

```
# 步骤1：打开结算助手
打开AI结算助手

# 步骤2：描述规则（包含话题词要求）
规则：播放量≥3万，同时携带话题 #春节活动 和 #新年优惠 的作者瓜分2万奖金

# 注意：话题词可以是任意内容，根据你的活动需求自定义

# 步骤3：确认规则
查看AI返回的规则理解，确认或修改

# 步骤4：上传数据
[上传Excel/CSV文件，必须包含视频标题字段]

# 步骤5：获取结果
下载结算结果
```

---

## 💬 自然语言规则示例

### ✅ 达标瓜分模式
```
总奖金10万元，完成量≥100的用户等额瓜分奖池
```
```
设置两个奖池：
- 基础奖池5万：完成量≥50的用户瓜分
- 进阶奖池5万：完成量≥100的用户瓜分
```

### ⚠️ 分档瓜分：必须询问是否互斥

**当规则包含多档奖池（如1档/2档/3档）时，在规则确认阶段必须主动询问用户档位是否互斥，不得自行假设，不得跳过询问直接结算。**

#### 询问时机与格式

在返回规则理解供用户确认时，若检测到多档奖池结构，**必须在确认信息末尾加入以下问题**：

```
❓ 档位关系确认（必须回答后才能继续）：
   您的规则包含多档奖池，请确认档位关系：
   A. 【累进叠加】满足高档条件的作者同时获得所有低档奖励
      例：发7条 → 同时获得1档+2档+3档奖励
   B. 【互斥独享】每位作者只能获得其满足的最高档奖励
      例：发7条 → 只获得3档奖励
   请回复 A 或 B，或直接说明。
```

#### 根据用户回答处理

**用户选A（累进叠加）**：各档独立判断资格，结算代码对每档独立循环，**不使用 `elif`**：

```python
# ✅ 累进写法：各档独立判断
for tier in [tier1, tier2, tier3]:
    qualified = [a for a in authors if a.valid_videos >= tier.min_videos]
    per_person = tier.pool / len(qualified)
    for a in qualified:
        a.awards[tier.name] = per_person
```

| 作者有效视频数 | 参与1档(≥2条) | 参与2档(≥4条) | 参与3档(≥7条) | 总奖金 |
|-----------|-----------|-----------|-----------|-----|
| 2条 | ✅ | ❌ | ❌ | 1档金额 |
| 4条 | ✅ | ✅ | ❌ | 1档+2档 |
| 7条 | ✅ | ✅ | ✅ | 1档+2档+3档 |

**用户选B（互斥独享）**：每位作者只取满足的最高档，结算代码使用 `elif` 链从高到低判断：

```python
# ✅ 互斥写法：从高档到低档判断
for a in authors:
    if a.valid_videos >= tier3.min_videos:
        a.awards['奖励'] = tier3.pool / qualified3_count
    elif a.valid_videos >= tier2.min_videos:
        a.awards['奖励'] = tier2.pool / qualified2_count
    elif a.valid_videos >= tier1.min_videos:
        a.awards['奖励'] = tier1.pool / qualified1_count
```

### ✅ 带话题词要求的瓜分模式

**支持任意话题词，动态配置**

```
总奖金2万元，发布作品≥5条且播放量≥3万，必须携带话题 #你的话题 的作者等额瓜分
```
```
奖池5万元，播放量≥10万，同时携带话题 #话题A 和 #话题B 的作者瓜分
```
```
总奖金3万，作品≥3条，携带话题 #话题1 或 #话题2 的用户瓜分
```

**话题词规则说明**：
- 🎯 **动态配置**：支持任意话题词，用户自定义（如 #春节活动、#新品发布、#品牌联名 等）
- ⚡ **精准匹配**：话题词必须完全匹配，例如 `#春节` 不会匹配 `#春节活动`
- 🔗 **且关系(AND)**：要求同时携带所有指定话题词（关键词：且/和/同时/都/AND）
- 🔗 **或关系(OR)**：要求至少携带一个话题词（关键词：或/OR，或无明确关键词）
- 📝 **自动识别**：用 `#` 开头标识话题词，AI自动提取和识别逻辑关系

**话题词格式要求**：
- ✅ 必须以 `#` 开头
- ✅ 后面跟任意文字（中文、英文、数字均可）
- ✅ 遇到空格、逗号、或特殊符号自动截断
- ✅ 示例：`#春节活动`、`#NewYear`、`#2024挑战` 等

### ✅ 排名赛模式
```
按销售额降序排名：
- 第1名：10000元
- 第2-3名：各5000元
- 第4-10名：各2000元
```

### ✅ 混合不互斥模式
```
双奖池并行：
1. 达标奖池5万：播放量≥1万的作者平分
2. 排名奖池5万：按点赞数排名前20名，第1-5名5000元，第6-10名3000元，第11-20名1500元
```

### ✅ 权重分配模式
```
总奖金8万元，按播放量权重比例分配
```

---

## 🔢 精确瓜分算法（必须遵守）

**核心要求：每人金额必须严格相等，不允许有人多有人少。奖池金额必须被彻底瓜分，不多不少。**

### 算法约束（与上方「AI执行约束」共同生效）

| 约束 | 说明 |
|------|------|
| ✅ 所有达标者金额数值完全相同 | 同一奖池内，每人奖金字符串必须一致 |
| ❌ 禁止「差额补给第一人」 | 如 `results[0].award += 0.01` 绝对禁止 |
| ❌ 禁止自行截断后丢弃差额 | 截断后差额不能悄悄归零，必须报告用户 |
| ❌ 禁止以「修正精度误差」为由调整任何人金额 | 精度问题应通过方案选择解决，不是代码补丁 |

### 精度问题的唯一合法处理方案（方案B）

当奖池金额无法被参与人数整除时（如 30000 / 17），**AI必须自动执行方案B，并在输出结果时告知用户**：

```
⚠️ 精度提示：奖池 30,000 元 / 17 人 无法以2位小数等额整除
   已自动执行方案B：保留最少小数位数使每人金额完全相同
   每人 1764.705882 元（6位小数），17人合计精确等于 30,000 元
   → 所有人金额相同，奖池金额完全分完
```

> ❌ **禁止截断到2位小数后丢弃差额**（即方案A不允许使用）。
> ✅ **始终自动执行方案B：找到使 `per × n == total` 成立的最小小数位数。**

### 每人金额相等的正确实现

直接均分时保留足够小数位数，确保每人金额完全相同：

```python
from decimal import Decimal, ROUND_HALF_UP, getcontext

def distribute_equal(total_yuan, n):
    """
    等额瓜分：每人金额严格相同
    - 先尝试精确整除
    - 若能整除（如 5000 / 10 = 500.00），保留两位小数
    - 若不能整除（如 5000 / 17），保留足够位数使每人金额完全相同
      并验证 per_person * n == total_yuan
    """
    getcontext().prec = 28
    total = Decimal(str(total_yuan))
    count = Decimal(n)
    per_person = total / count  # 精确除法

    # 检查是否能整除到两位小数
    per_2 = per_person.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    if per_2 * count == total:
        return float(per_2), 2  # 返回(每人金额, 小数位数)

    # 否则找到能让 per * n == total 的最小小数位数（最多10位）
    for digits in range(3, 11):
        fmt = '0.' + '0' * digits
        per_d = per_person.quantize(Decimal(fmt), rounding=ROUND_HALF_UP)
        if per_d * count == total:
            return float(per_d), digits

    # 极端情况：直接返回高精度值，在表格中标注
    return float(per_person), -1

# 示例
# distribute_equal(5000, 10)  → (500.0, 2)  每人500.00元
# distribute_equal(5000, 17)  → 需要找到能被整除的精度
#   5000/17 = 294.117647058823...  → 若无法整除，按原始精确值记录，备注「无法等额整除」
```

### 若奖池无法等额整除

**统一执行方案B**：找到使 `per × n == total` 成立的最小小数位数，保持所有人金额完全相同，奖池金额精确分完。

- ❌ 不得截断到2位小数后丢弃差额
- ❌ 不得询问用户是否接受截断（方案A已废弃）
- ✅ 在输出结果时注明保留的小数位数，让用户知晓

### 验证规则

输出结果前必须验证：
- `每人金额 × 人数 == 奖池金额`（精确验证，不允许浮点误差）
- 验证失败则不允许输出，必须重新计算或报错

---

## 🔧 工作流程

```
┌─────────────────────────────────────────────────────┐
│  用户输入自然语言规则                                  │
│  "总奖金2万,播放量≥3万,携带话题#春节活动的作者瓜分"     │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  AI自动提取话题词并解析规则 → 结构化配置               │
│  {                                                   │
│    mode: "guaranteed",                               │
│    pool: 20000,                                      │
│    condition: {field: "播放量", op: ">=", value: 30000},│
│    topic_rule: {topics: ["#春节活动"], logic: "OR"}  │
│  }                                                   │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  返回规则理解给用户确认                                │
│  ═══════════════════════════════════════════        │
│  📋 规则理解确认                                      │
│  【奖池1】达标瓜分奖池                                │
│    💰 奖池金额: 20,000元                             │
│    ✅ 达标条件: 播放量 >= 30,000                     │
│    🏷️ 话题词要求: #春节活动                          │
│  ❓ 请确认以上规则理解是否正确？                       │
│  ═══════════════════════════════════════════        │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  用户确认/调整AI理解                                  │
│  • "对，但需要同时携带#春节活动和#新年优惠"            │
│    → AI更新配置 → 再次返回确认                        │
│  • "确认无误" → 进入下一步                            │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  上传数据文件（Excel/CSV）                            │
│  本地处理，数据不上传                                 │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  执行结算                                             │
│  - 数据聚合（按作者ID汇总）                            │
│  - 话题词检查（精准匹配）                              │
│  - 条件筛选                                           │
│  - 金额计算                                           │
│  - 结果生成                                           │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  输出结果                                            │
│  - 结算摘要（统计信息）                                │
│  - 详细名单（Excel下载）                              │
│  - 异常记录（如有）                                   │
└─────────────────────────────────────────────────────┘
```

---

## 🏷️ 话题词识别详解

### 动态配置 - 支持任意话题词

话题词**不是固定的**，可以根据活动需求自定义配置。系统会自动从用户输入的规则中提取话题词。

**支持的话题词示例**：
- `#春节活动` - 节日主题
- `#新品发布` - 产品活动
- `#品牌联名` - 营销活动
- `#挑战赛2024` - 竞赛活动
- `#GameEvent` - 英文话题
- `#攻略` - 简短话题
- 任意以 `#` 开头的文字

### 精准匹配规则

话题词必须**完全匹配**，部分匹配无效：

| 要求话题词 | 视频标题 | 是否匹配 | 说明 |
|-----------|---------|---------|------|
| `#春节` | "最强攻略 #春节 活动" | ✅ 匹配 | 完整包含#春节 |
| `#春节` | "最强攻略 #春节活动 指南" | ❌ 不匹配 | #春节活动 != #春节 |
| `#春节` | "活动 #春节 和 #春节活动" | ✅ 匹配 | 包含完整的#春节 |
| `#新品` + `#发布`(且) | "#新品 #发布 预告" | ✅ 匹配 | 两个都有 |
| `#新品` + `#发布`(且) | "#新品 预告视频" | ❌ 不匹配 | 缺少#发布 |
| `#新品` + `#发布`(或) | "#新品 预告视频" | ✅ 匹配 | 至少有一个 |

### 逻辑关系识别

**且关系 (AND)** - 关键词触发：
- "且"、"和"、"同时"、"都"、"AND"
- 示例：`同时携带#春节和#活动`

**或关系 (OR)** - 关键词触发：
- "或"、"OR"
- 默认（无明确关键词时）
- 示例：`携带#话题A或#话题B`

### 话题词提取规则

系统使用正则表达式自动提取：
```python
# 匹配模式：# 后跟非特殊字符
topics = re.findall(r'#[^#\s,，和或]+', rule_text)
```

**会被识别为话题词**：
- ✅ `#春节活动` → 提取 `#春节活动`
- ✅ `#NewYear2024` → 提取 `#NewYear2024`
- ✅ `#挑战` → 提取 `#挑战`

**不会被识别**：
- ❌ 没有 `#` 符号的文字
- ❌ `#` 后直接跟空格、逗号等

### 多视频检查策略

作者只要有**任意一个视频**满足话题词要求即可：

```
作者A发布了3个视频：
  视频1: "日常vlog"              → 无话题词
  视频2: "#春节活动 攻略"        → 包含#春节活动 ✅
  视频3: "游戏实况"              → 无话题词

要求: 携带话题#春节活动
结果: ✅ 作者A符合要求（视频2包含）
```

### 常见应用场景

| 活动类型 | 话题词示例 | 规则示例 |
|---------|-----------|---------|
| 节日营销 | `#春节`、`#中秋` | 携带话题#春节的作者瓜分 |
| 产品推广 | `#新品发布`、`#限时特惠` | 同时携带#新品发布和#优惠的作者 |
| 品牌活动 | `#品牌挑战赛`、`#品牌联名` | 携带#品牌挑战赛或#品牌联名 |
| 游戏活动 | `#攻略`、`#教学` | 同时携带#攻略和#教学 |
| UGC征集 | `#创作挑战`、`#用户故事` | 携带#创作挑战的用户 |

---

## 📋 数据格式要求

### 支持的文件格式
- ✅ Excel (.xlsx, .xls)
- ✅ CSV (.csv，推荐UTF-8编码)

### 必需字段
| 字段类型 | 说明 | 示例 |
|----------|------|------|
| **用户ID** | 唯一标识 | 作者ID、用户ID、账号 |
| **用户名称** | 显示名称 | 作者名称、用户昵称 |
| **视频标题** | 话题词匹配用 | 视频标题、标题 |
| **数据字段** | 结算依据 | 播放量、销售额、完成量 |
| **排序字段** | 排名赛使用 | 点赞数、销售额 |

### 示例数据结构

**视频数据**：
| 作者ID | 作者名称 | 视频ID | 视频标题 | 播放量 | 点赞数 |
|--------|----------|--------|----------|--------|--------|
| 123456 | 张三 | 789 | "#金铲铲 最强阵容" | 50000 | 1000 |
| 123456 | 张三 | 790 | "游戏攻略" | 30000 | 500 |
| 789012 | 李四 | 791 | "#金铲铲 #攻略" | 80000 | 2000 |

**聚合后结算**：
| 作者ID | 作者名称 | 作品数 | 累计播放量 | 累计点赞 | 符合话题词 |
|--------|----------|--------|------------|----------|-----------|
| 123456 | 张三 | 2 | 80000 | 1500 | ✅ (视频789) |
| 789012 | 李四 | 1 | 80000 | 2000 | ✅ (视频791) |

---

## 📝 版本历史

### v2.1.2 (2026-05-09)
- ✅ **新增「🚨 强制性约束」章节**（置于文档最顶层，凌驾所有其他规则）
  - **约束一：确认步骤必须暂停等待用户回复**——明确禁止在同一回复中既输出规则理解又执行结算，必须完全停止等待用户明确说"确认"
  - **约束二：禁止 round()**——唯一合法路径是调用内嵌引擎的 `_distribute_equal()`，任何手写除法均视为错误
  - **约束三：执行后强制自查报告**——结算完成后必须逐项打勾确认5项检查，任一项"否"必须主动告知用户

### v2.1.1 (2026-05-09)
- ✅ **新增「AI执行约束」章节**：严格禁止 AI 自行添加「优化」逻辑、修改计算方式、添加文档未说明功能
- ✅ **强化瓜分算法约束**：明确要求所有达标者奖金完全相同，明确禁止「差额补给某人」、「少给某人」、「自行处理差额」
- ✅ **规范精度无法整除时的处理**：统一执行方案B（保留最少小数位使金额整除），废除方案A（截断后丢弃差额）
- ✅ **明确有疑问时必须询问用户**：规则歧义、字段不匹配、奖池无法整除均必须等待用户决策

### v2.1.0 (2026-05-08)
- ✅ **支持 Excel (xlsx/xls)**：新增 `openpyxl` 读取，自动检测编码，支持多 Sheet 合并
- ✅ **多奖池并行**：`SettlementEngine` 支持同时计算任意数量奖池（达标瓜分 + 榜单奖混合）
- ✅ **榜单/排名奖**：新增 `SettlementMode.RANKING`，支持分段档位（第1名/第2-3名/...）固定金额或瓜分
- ✅ **多条件达标**：`conditions` 字段支持 AND 逻辑多条件（如作品数≥5 且 播放量≥3万）
- ✅ **精度修复**：`export_to_csv` 金额列不再用 `:.2f` 截断，完整保留精确小数
- ✅ **直播数据支持**：新增 `live_duration`/`live_count`/`live_sales` 字段聚合
- ✅ **命令行参数扩展**：支持 `sheet名称` 和 `--all-sheets` 参数

### v2.0.2 (2026-05-08)
- ✅ **新增强制执行规则章节**：明确要求AI必须调用 `settlement_engine.py`，禁止手写替代代码
- ✅ **禁止 `round()` 精度陷阱**：明确标注常见错误写法，防止AI第一次计算时忽略精度要求
- ✅ **完整执行流程示例**：提供可直接复制执行的4步代码，含错误写法对比
- ✅ **AI自查清单**：结算前必须完成的5项检查，确保不遗漏关键步骤
- ✅ **命令行快速执行**：补充命令行调用示例，AI可直接用 `python settlement_engine.py` 完成结算

### v2.0.1 (2026-05-07)
- ✅ 修复精确瓜分算法：彻底解决浮点舍入导致总额不等于奖池的问题
- ✅ 明确分档瓜分（累进档位）规则：各档独立判断，高档位作者可同时参与低档奖励
- ✅ 新增触发词「一组结算」，可直接启动结算流程
- 📝 补充分档瓜分示例和代码规范

### v1.1.0 (2026-04-21)
- ✅ 新增话题词精准匹配功能
  - 支持精准识别视频标题中的话题词（如#金铲铲）
  - 支持且/或逻辑关系（AND/OR）
  - 自动区分相似话题词（#金铲铲 vs #金铲铲之战）
- ✅ 新增规则确认流程
  - AI解析后返回格式化的规则理解
  - 用户可多轮修正直到确认
  - 避免因理解偏差导致的结算错误
- 📊 优化数据加载逻辑，支持读取视频标题字段

### v1.0.0 (2026-04-11)
- ✅ 初始版本发布
- ✅ 支持自然语言规则解析
- ✅ 四种结算模式：达标瓜分、排名赛、混合不互斥、权重分配
- ✅ 超时自动重试机制
- ✅ 数据本地处理，保障安全
- ✅ 专业Excel输出格式

---

## 💡 设计哲学

> **让结算变得简单，让数据变得安全，让结果变得专业。**

### 核心原则
1. **AI优先**：用自然语言替代复杂配置
2. **本地处理**：数据不出本地，安全保障
3. **健壮可靠**：超时重试，容错恢复
4. **专业输出**：格式规范，直接可用

---

## 🧪 结算引擎代码（AI直接使用，无需查找外部文件）

> ⚠️ **AI执行结算时，必须将以下完整代码块全部复制到执行环境中运行，禁止自行手写任何替代实现。**

### 完整结算引擎代码（直接复制执行）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI智能结算引擎 v2.1.1 - 直接复制此代码块到执行环境"""

import csv, re, os
from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

getcontext().prec = 28

class SettlementMode(Enum):
    GUARANTEED = "guaranteed"
    RANKING    = "ranking"
    WEIGHTED   = "weighted"

@dataclass
class TopicRule:
    topics: List[str]
    logic: str = "OR"
    def check(self, title: str) -> bool:
        if not self.topics: return True
        matches = [bool(re.search(r'(?:^|[\s,，。！!？?；;：:、])' + re.escape(t) + r'(?:$|[\s,，。！!？?；;：:、])', title)) for t in self.topics]
        return all(matches) if self.logic == "AND" else any(matches)

@dataclass
class RankingTier:
    rank_start: int
    rank_end:   int
    amount:     float = 0.0
    pool:       float = 0.0

@dataclass
class AwardPool:
    name:          str
    amount:        float
    mode:          SettlementMode
    condition:     Optional[Dict] = None
    ranking_field: Optional[str]  = None
    ranking_tiers: Optional[List[RankingTier]] = None
    weight_field:  Optional[str]  = None
    topic_rule:    Optional[TopicRule] = None
    conditions:    Optional[List[Dict]] = None

@dataclass
class AuthorData:
    author_id:    str
    author_name:  str
    videos:       int = 0
    total_plays:  int = 0
    total_likes:  int = 0
    video_titles: List[str] = field(default_factory=list)
    live_duration: int = 0
    live_count:    int = 0
    live_sales:    int = 0
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SettlementResult:
    author_id:    str
    author_name:  str
    videos:       int
    total_plays:  int
    total_likes:  int
    awards:       Dict[str, str]
    total_amount: str

def _distribute_equal(total_yuan: float, n: int) -> str:
    """
    等额瓜分核心函数。保证所有人金额完全相同，奖池金额精确分完。
    ❌ 禁止用 round() 替代此函数。
    """
    total = Decimal(str(total_yuan)); count = Decimal(n); per = total / count
    for digits in range(2, 11):
        per_r = per.quantize(Decimal('0.' + '0' * digits), rounding=ROUND_HALF_UP)
        if per_r * count == total:
            return str(per_r)
    return str(per.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP))

FIELD_ALIASES = {
    'author_id':     ['作者ID', '用户ID', '账号ID', 'authorId', 'uid'],
    'author_name':   ['作者名称（最新）', '作者名称', '用户名称', '昵称', 'authorName'],
    'title':         ['视频标题', '标题', 'title'],
    'plays':         ['视频累计外显播放次数', '播放量', '播放次数', 'plays'],
    'likes':         ['视频累计外显点赞次数', '点赞量', '获赞数', 'likes'],
    'live_duration': ['直播时长', '直播累计时长', 'liveDuration'],
    'live_count':    ['开播场次', '直播场次', 'liveCount'],
    'live_sales':    ['直播销售额', '销售额', 'liveSales'],
}

def _resolve(row, key):
    for alias in FIELD_ALIASES.get(key, [key]):
        if alias in row: return row[alias]
    return None

def _num(val):
    if val is None or val == '': return 0
    try: return int(float(str(val).replace(',', '')))
    except: return 0

def _load_csv(fp):
    for enc in ('utf-8-sig', 'gbk', 'utf-8'):
        try:
            with open(fp, 'r', encoding=enc) as f:
                return {os.path.splitext(os.path.basename(fp))[0]: list(csv.DictReader(f))}
        except: continue
    return {}

def _load_excel(fp, sheet_name, all_sheets):
    try: import openpyxl
    except ImportError: raise ImportError("读取Excel需要安装openpyxl：pip install openpyxl")
    wb = openpyxl.load_workbook(fp, read_only=True, data_only=True)
    target = wb.sheetnames if all_sheets else ([sheet_name] if sheet_name else [wb.sheetnames[0]])
    result = {}
    for sname in target:
        ws = wb[sname]; rows_iter = ws.iter_rows(values_only=True)
        header = [str(h).strip() if h is not None else '' for h in next(rows_iter, [])]
        result[sname] = [{header[i]: (row[i] if i < len(row) else None) for i in range(len(header))} for row in rows_iter]
    wb.close(); return result

def load_file(fp, sheet_name=None, all_sheets=False):
    ext = os.path.splitext(fp)[1].lower()
    if ext == '.csv': return _load_csv(fp)
    elif ext in ('.xlsx', '.xls', '.xlsm'): return _load_excel(fp, sheet_name, all_sheets)
    else: raise ValueError(f"不支持的格式: {ext}")

def _aggregate(rows):
    authors = {}
    for row in rows:
        aid = str(_resolve(row, 'author_id') or '').strip()
        if not aid: continue
        if aid not in authors: authors[aid] = AuthorData(author_id=aid, author_name='')
        a = authors[aid]
        name = str(_resolve(row, 'author_name') or '').strip()
        if name: a.author_name = name
        a.videos += 1; a.total_plays += _num(_resolve(row, 'plays')); a.total_likes += _num(_resolve(row, 'likes'))
        a.live_duration += _num(_resolve(row, 'live_duration')); a.live_count += _num(_resolve(row, 'live_count')); a.live_sales += _num(_resolve(row, 'live_sales'))
        t = str(_resolve(row, 'title') or '').strip()
        if t: a.video_titles.append(t)
        for k, v in row.items():
            if k not in a.extra: a.extra[k] = v
    return authors

def _merge(base, new_authors):
    for aid, data in new_authors.items():
        if aid in base:
            a = base[aid]
            if data.author_name: a.author_name = data.author_name
            a.videos += data.videos; a.total_plays += data.total_plays; a.total_likes += data.total_likes
            a.live_duration += data.live_duration; a.live_count += data.live_count; a.live_sales += data.live_sales
            a.video_titles += data.video_titles; a.extra.update(data.extra)
        else: base[aid] = data

FMAP = {
    '播放量': 'total_plays', '播放': 'total_plays', '点赞': 'total_likes', '获赞': 'total_likes',
    '直播时长': 'live_duration', '开播场次': 'live_count', '销售额': 'live_sales', '作品数': 'videos',
}

def _topic_ok(a, rule): return not rule or any(rule.check(t) for t in a.video_titles)

def _cond_ok(a, pool):
    for cond in (pool.conditions or ([pool.condition] if pool.condition else [])):
        attr = FMAP.get(cond.get('field', ''), cond.get('field', ''))
        actual = getattr(a, attr, None) or a.extra.get(attr, 0)
        op = cond.get('op', '>='); val = cond.get('value', 0)
        if op in ('>=', '≥'): ok = actual >= val
        elif op == '>': ok = actual > val
        elif op in ('<=', '≤'): ok = actual <= val
        elif op == '<': ok = actual < val
        elif op == '==': ok = actual == val
        else: ok = False
        if not ok: return False
    return True

def run_settlement(file_path, pools, sheet_name=None, all_sheets=False, extra_file=None):
    """
    主结算函数。pools 由 AI 根据活动规则构造。
    - file_path: CSV 或 Excel
    - all_sheets=True: 合并所有 Sheet
    - extra_file: 第二个底表文件（数据合并后统一结算）
    """
    authors = {}
    for rows in load_file(file_path, sheet_name, all_sheets).values():
        _merge(authors, _aggregate(rows))
    if extra_file:
        for rows in load_file(extra_file).values():
            _merge(authors, _aggregate(rows))

    results = {aid: SettlementResult(aid, a.author_name, a.videos, a.total_plays, a.total_likes, {}, '0')
               for aid, a in authors.items()}

    for pool in pools:
        if pool.mode == SettlementMode.GUARANTEED:
            q = [aid for aid, a in authors.items() if _topic_ok(a, pool.topic_rule) and _cond_ok(a, pool)]
            if q:
                per = _distribute_equal(pool.amount, len(q))
                for aid in q: results[aid].awards[pool.name] = per

        elif pool.mode == SettlementMode.RANKING and pool.ranking_field and pool.ranking_tiers:
            cands = [a for a in authors.values() if _topic_ok(a, pool.topic_rule) and _cond_ok(a, pool)]
            attr = FMAP.get(pool.ranking_field, pool.ranking_field)
            cands.sort(key=lambda a: (getattr(a, attr, 0) or a.extra.get(attr, 0)), reverse=True)
            for tier in pool.ranking_tiers:
                tc = cands[tier.rank_start - 1: tier.rank_end]
                if not tc: continue
                per = _distribute_equal(tier.pool, len(tc)) if tier.pool > 0 else _distribute_equal(tier.amount, 1)
                for a in tc: results[a.author_id].awards[pool.name] = per

        elif pool.mode == SettlementMode.WEIGHTED and pool.weight_field:
            cands = [a for a in authors.values() if _topic_ok(a, pool.topic_rule) and _cond_ok(a, pool)]
            attr = FMAP.get(pool.weight_field, pool.weight_field)
            tw = sum(getattr(a, attr, 0) or a.extra.get(attr, 0) for a in cands)
            if tw > 0:
                pd = Decimal(str(pool.amount)); twd = Decimal(str(tw))
                for a in cands:
                    w = Decimal(str(getattr(a, attr, 0) or a.extra.get(attr, 0)))
                    award = (pd * w / twd).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    if award > 0: results[a.author_id].awards[pool.name] = str(award)

    for r in results.values():
        tot = sum(Decimal(v) for v in r.awards.values())
        r.total_amount = str(tot.normalize() if tot != 0 else Decimal('0'))

    winners = sorted([r for r in results.values() if Decimal(r.total_amount) > 0],
                     key=lambda x: Decimal(x.total_amount), reverse=True)
    stats = {
        'total_authors': len(authors), 'qualified_authors': len(winners),
        'total_videos': sum(r.videos for r in winners), 'total_plays': sum(r.total_plays for r in winners),
        'total_likes': sum(r.total_likes for r in winners),
        'total_award': str(sum(Decimal(r.total_amount) for r in winners).normalize()),
        'pools': [{'name': p.name, 'amount': p.amount, 'mode': p.mode.value} for p in pools],
    }
    return winners, stats

def export_to_csv(results, output_path, stats):
    """导出结算结果，金额保留完整精度，不截断。"""
    pool_names = []
    for r in results:
        for k in r.awards:
            if k not in pool_names: pool_names.append(k)
    header = ['序号', '作者ID', '作者名称', '发布作品数', '累计播放量', '累计获赞'] + [f'{p}(元)' for p in pool_names] + ['总奖金(元)']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(header)
        for idx, r in enumerate(results, 1):
            row = [idx, r.author_id, r.author_name, r.videos, r.total_plays, r.total_likes]
            row += [r.awards.get(p, '') for p in pool_names] + [r.total_amount]
            w.writerow(row)
        summary = ['汇总', '', '', stats['total_videos'], stats['total_plays'], stats['total_likes']]
        for p in pool_names:
            summary.append(str(sum(Decimal(r.awards[p]) for r in results if p in r.awards).normalize()))
        summary.append(stats['total_award']); w.writerow(summary)

def print_summary(results, stats):
    print('=' * 80 + '\n结算结果摘要\n' + '=' * 80)
    for p in stats.get('pools', []): print(f"  - {p['name']}: {p['amount']:,.2f}元 ({p['mode']})")
    print(f"\n  获奖: {stats['qualified_authors']}人 / 参与: {stats['total_authors']}人  总奖金: {stats['total_award']}元\n" + '-' * 80)
    print(f"{'序号':<5}{'作者ID':<16}{'作者名称':<16}{'作品数':<8}{'播放量':<12}{'总奖金'}")
    for i, r in enumerate(results[:10], 1):
        print(f"{i:<5}{r.author_id:<16}{r.author_name:<16}{r.videos:<8}{r.total_plays:<12}{r.total_amount}")
    print('=' * 80)
```

---

### 如何构造 pools（每次活动必须重新构造，示例仅供参考）

> ⚠️ **以下示例代码是模板，不是固定配置。AI每次结算前必须根据用户描述的实际规则重新构造 `pools`，奖池数量、类型、金额、条件均可任意组合。**

**pools 支持的奖池类型（可任意数量、任意组合）：**

| 类型 | SettlementMode | 适用场景 |
|------|---------------|---------|
| 达标瓜分 | `GUARANTEED` | 满足条件的人等额平分奖池 |
| 排名/榜单奖 | `RANKING` | 按指定字段排名，不同名次固定金额或瓜分 |
| 权重分配 | `WEIGHTED` | 按某字段权重比例分配奖池 |

**示例（仅参考，实际 pools 由 AI 根据当次活动规则构造）：**

```python
# ============================================================
# 以下仅为示例，AI必须根据实际活动规则重新构造 pools
# 奖池数量不限，类型可任意混合
# ============================================================

# 场景示例A：单个达标瓜分
pools = [
    AwardPool(
        name="瓜分奖池",
        amount=20000,
        mode=SettlementMode.GUARANTEED,
        conditions=[{'field': '播放量', 'op': '>=', 'value': 30000}],
    ),
]

# 场景示例B：多档瓜分（累进叠加，高档同时获得低档奖励）
pools = [
    AwardPool(name="1档奖池", amount=10000, mode=SettlementMode.GUARANTEED,
              conditions=[{'field': '作品数', 'op': '>=', 'value': 2}]),
    AwardPool(name="2档奖池", amount=20000, mode=SettlementMode.GUARANTEED,
              conditions=[{'field': '作品数', 'op': '>=', 'value': 5}]),
    AwardPool(name="3档奖池", amount=30000, mode=SettlementMode.GUARANTEED,
              conditions=[{'field': '作品数', 'op': '>=', 'value': 10}]),
]

# 场景示例C：瓜分 + 话题词过滤 + 榜单奖混合
pools = [
    AwardPool(
        name="基础瓜分",
        amount=30000,
        mode=SettlementMode.GUARANTEED,
        conditions=[{'field': '播放量', 'op': '>=', 'value': 10000}],
        topic_rule=TopicRule(topics=['#活动话题'], logic='OR'),
    ),
    AwardPool(
        name="大神榜",
        amount=20000,
        mode=SettlementMode.RANKING,
        ranking_field='播放量',
        ranking_tiers=[
            RankingTier(rank_start=1, rank_end=1,  amount=10000),  # 第1名固定10000
            RankingTier(rank_start=2, rank_end=3,  amount=5000),   # 第2-3名各5000
            RankingTier(rank_start=4, rank_end=10, amount=0, pool=5000),  # 第4-10名瓜分5000
        ],
    ),
]

# 场景示例D：按播放量权重比例分配
pools = [
    AwardPool(
        name="权重奖池",
        amount=50000,
        mode=SettlementMode.WEIGHTED,
        weight_field='播放量',
        conditions=[{'field': '播放量', 'op': '>=', 'value': 5000}],
    ),
]

# ============================================================
# 构造好 pools 后，调用结算函数（文件路径换成实际路径）
# ============================================================
results, stats = run_settlement(
    file_path='data.xlsx',    # 支持 .xlsx / .xls / .csv
    pools=pools,
    sheet_name=None,          # 指定Sheet名，None则取第一个Sheet
    all_sheets=False,         # True则合并所有Sheet
    # extra_file='live.xlsx'  # 可选：第二个底表文件，数据合并后统一结算
)

print_summary(results, stats)
export_to_csv(results, 'data_结算结果.csv', stats)
print("✓ 完成")
```

---

**开发团队**：AI智能结算助手Pro  
**联系方式**：通过OpenClaw技能市场反馈
