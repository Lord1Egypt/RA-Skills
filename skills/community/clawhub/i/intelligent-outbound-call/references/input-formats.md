# 输入格式参考

## taskInput.json 推荐格式（含被叫方姓名）

**有联系人姓名时，用 `contacts` 作为主字段**，机器人通话中会正确称呼对方：

```json
{
  "contacts": [
    { "phoneNumber": "13800138000", "name": "张三" },
    { "phoneNumber": "13900139000", "name": "李四" }
  ],
  "scenarioDescription": "春季新品推广",
  "taskName": "春季促销活动",
  "agentProfile": {
    "name": "小美",
    "gender": "女",
    "age": 25,
    "role": "销售顾问",
    "communicationStyle": ["热情", "专业", "亲切"],
    "background": "春季新品推广活动",
    "goals": "了解客户购买意向，促成交易",
    "skills": "产品介绍、需求挖掘、促成交易",
    "workflow": "问候 -> 了解需求 -> 介绍产品 -> 处理异议 -> 促成合作",
    "constraint": "保持礼貌、尊重对方意愿、不强制推销",
    "openingPrompt": "您好，我是小美，春季新品推广活动的销售顾问"
  },
  "metadata": {
    "source": "manual",
    "campaign": "spring-2024"
  }
}
```

**无姓名时，用 `phoneNumbers` 简化格式**：

```json
{
  "phoneNumbers": ["13800138000", "13900139000"],
  "scenarioDescription": "春季新品推广",
  "taskName": "春季促销活动"
}
```

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `contacts` | object[] | ✅（推荐） | 结构化联系人列表，**含 `name` 时机器人通话中会正确称呼对方** |
| `phoneNumbers` | string[] | 兼容 | 纯号码列表，无姓名时使用；`contacts` 存在时忽略此字段 |
| `scenarioDescription` | string | ✅ | 外呼场景描述，用于生成话术 |
| `taskName` | string | 否 | 任务名称，便于识别 |
| `agentProfile` | object | ⛔ 必填 | 智能体配置，决定机器人身份和通话行为，不可省略 |
| `metadata` | object | 否 | 额外元数据 |

### contacts 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `phoneNumber` | string | 手机号（必填） |
| `name` | string | **被叫方姓名**，通话中机器人会用此称呼对方，同时注入话术背景 |
| `referenceId` | string | 外部系统 ID，便于结果回查 |

> **重要**：不传 `name` 时，机器人无法知道对方叫什么，通话中只能用通用称呼（如"您好"）。有联系人姓名时务必通过 `contacts` 传入。

## agentProfile 字段说明

> ⛔ **`agentProfile` 必填，不可省略。**
>
> `agentProfile` 决定了机器人在通话中的身份、背景知识和行为方式。**`background` 尤其关键**——它是机器人在通话中唯一能参考的业务信息来源，所有已知的上下文（被叫方信息、活动详情、时间地点、特殊要求等）都应该写入这里。信息越完整，通话质量越高。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `name` | string | 智能体名称 | "小美" |
| `gender` | string | 性别 | "男"、"女" |
| `age` | number | 年龄 | 25 |
| `role` | string | 身份角色 | "销售顾问"、"招聘专员" |
| `communicationStyle` | string[] | 沟通风格 | ["热情", "专业"] |
| `background` | string | **业务背景（最重要）**：把所有已知信息都写进来——被叫方姓名/职位、活动内容、时间地点、前置节点数据等 | "春季新品推广活动，客户张三，VIP 会员" |
| `goals` | string | 业务目标 | "了解客户购买意向" |
| `skills` | string | 业务技能 | "产品介绍、需求挖掘" |
| `workflow` | string | 对话流程 | "问候 -> 介绍 -> 促成" |
| `constraint` | string | 约束条件 | "保持礼貌、不强制推销" |
| `openingPrompt` | string | 开场白 | "您好，我是小美" |

## 智能推断规则（紧急兜底，不推荐）

仅在极端情况下无法提供 `agentProfile` 时，系统才根据 `scenarioDescription` 自动推断基础角色——**推断结果缺少具体业务背景，通话效果极差，请务必手动配置**：

| 场景关键词 | 推断角色 | 推断风格 |
|-----------|---------|---------|
| 面试、招聘 | 招聘专员 | 专业友好 |
| 保险、理财 | 保险顾问 | 专业耐心 |
| 游戏、推广 | 推广专员 | 热情活泼 |
| 审计、调查 | 审计专员 | 专业严谨 |
| 客服、回访 | 客服专员 | 亲切耐心 |
| 销售、产品 | 销售顾问 | 热情专业 |

## 其他支持的输入格式

**格式 2: 简化格式**

```json
{
  "phones": "13800138000,13900139000",
  "scenario": "产品推广",
  "name": "春季促销"
}
```

**格式 3: 候选人/简历筛查格式**（`name` 字段会自动提取，机器人通话中会称呼对方姓名）

```json
{
  "candidates": [
    { "name": "张三", "phone": "13800138000", "score": 85 },
    { "name": "李四", "phone": "13900139000", "score": 90 }
  ],
  "scenarioDescription": "面试邀约 - 蓝领岗位简历筛查通过",
  "taskName": "蓝领简历筛查后约面试",
  "previousStep": "简历筛查"
}
```

**格式 4: CRM/外部工具格式**

```json
{
  "data": {
    "contacts": [
      { "phone": "13800138000", "name": "张三" }
    ],
    "purpose": "客户回访",
    "campaignName": "满意度调查"
  },
  "toolName": "CRM-System"
}
```

**格式 5: 通用列表格式**

```json
[
  { "phone": "13800138000", "name": "张三" },
  { "phone": "13900139000", "name": "李四" }
]
```

注意：使用此格式时，`scenarioDescription` 默认为"批量外呼"。

## 输入优先级

1. 命令行参数（JSON 文件路径）— 最高优先级
2. `$ARGUMENTS` 环境变量 — 次优先级
3. 交互式输入 — 兜底方案
