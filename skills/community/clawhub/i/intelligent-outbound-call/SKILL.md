---
name: outbound-calling
description: >-
  该技能调用阿里云晓蜜外呼机器人，向指定手机号码列表发起自动语音外呼，支持自定义话术场景，可批量处理数十至数千个号码，并实时追踪外呼任务进度。
  当用户问题涉及「批量给客户打电话通知某件事」「自动外呼做满意度调查或回访」「用机器人拨打面试邀约或活动提醒」「从前置节点（如 CRM、简历筛查）获取号码后直接外呼」时使用该技能。
---

# 阿里云晓蜜外呼机器人

自动化外呼机器人技能，用于批量电话外呼。

## 前置条件

### 配置阿里云凭证

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-access-key-id"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-access-key-secret"
```

### 绑定外呼号码 ⚠️ 重要

必须申请并绑定外呼号码，否则无法进行外呼。详见 [phone-number-setup.md](references/phone-number-setup.md)。

## 执行清单

复制此清单并在执行时逐项打勾：

- [ ] 步骤 0: 校验前置条件 ⛔ BLOCKING — 未通过前禁止继续
  - [ ] 0.1 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 已配置
  - [ ] 0.2 已绑定外呼号码（未绑定则读取 [phone-number-setup.md](references/phone-number-setup.md)）
- [ ] 步骤 1: 获取外呼名单
  - [ ] 1A: 前置节点 → 提取号码 + 推断场景描述
  - [ ] 1B: 用户直接提供 → 收集号码、场景描述、任务名称
- [ ] 步骤 2: 验证数据
  - [ ] 2.1 电话号码格式正确（1开头11位）
  - [ ] 2.2 场景描述清晰明确
- [ ] 步骤 3: 向用户确认 ⛔ BLOCKING — 未收到明确确认前禁止执行任何外呼
- [ ] 步骤 4: 创建 taskInput.json（请读取 [input-formats.md](references/input-formats.md)）
  - [ ] 4.1 盘点所有已知信息，作为 `agentProfile.background` 的素材
  - [ ] 4.2 构建完整 `agentProfile` ⛔ 必填 — 不要依赖自动推断，background 写得越详细通话质量越高
- [ ] 步骤 5: 执行外呼
- [ ] 步骤 6: 报告结果并执行交付检查

---

### 步骤 0: 校验前置条件 ⛔ BLOCKING

在做任何事之前，先确认：

- `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 是否已配置？未配置则立即告知用户，停止执行。
- 是否已绑定外呼号码？未绑定则读取 [phone-number-setup.md](references/phone-number-setup.md) 引导用户完成申请，停止执行。

---

### 步骤 1: 获取外呼名单

**场景 A: 从前置节点获取**（如简历筛查、CRM 查询等）

先执行前置步骤，从返回结果中提取电话号码，根据用户意图生成场景描述，直接传递给此技能，无需再次询问用户。

**场景 B: 用户直接提供**

收集以下信息：

- **电话号码列表**（必需）— 中国大陆手机号（1开头11位）
- **外呼场景描述**（必需）— 清晰描述外呼目的；脚本会自动从描述中推断 `industry`（行业）和 `scene`（场景类型）标准值，无需手动指定
- **任务名称**（可选）

信息不完整时，向用户询问：

- "需要拨打哪些电话号码？"
- "这次外呼的目的是什么？"

---

### 步骤 2: 验证数据

逐项检查：

- 这些号码是否都是 1 开头的 11 位数字？有没有明显格式错误？
- 场景描述是否足够具体，能让智能体理解外呼目的？

---

### 步骤 3: 向用户确认 ⛔ BLOCKING

**在执行前，必须向用户展示并等待明确确认：**

```
准备执行外呼任务，请确认以下信息：

📋 任务信息
- 任务名称: [任务名称]
- 外呼场景: [场景描述]
- 智能体角色: [角色]
- 外呼目标: [目标]

📞 外呼名单（共 N 人）
1. [电话号码]
...

是否确认执行外呼？
```

- ✅ 必须等待用户明确确认后才能执行
- ✅ 用户不确认时，询问需要修改什么
- ❌ 不要在用户未确认的情况下自动执行

---

### 步骤 4: 创建 taskInput.json

请读取 [input-formats.md](references/input-formats.md)文件，根据已知信息构建 taskInput.json 文件。

**关键原则：充分利用已有信息，不要只提取号码和简单描述。**

**首先盘点当前已知的所有信息，这些都应该作为 `background` 的素材：**

- 对话上下文中提到的任何细节（时间、地点、条件、产品名称、活动内容……）
- 前置节点传来的数据（简历信息、CRM 字段、订单详情……）
- 被叫方的个人信息（姓名、职位、历史记录……）
- 用户明确说明的要求或限制

**然后再问自己：**

- 这次外呼的核心目的是什么？被叫方需要做什么决定或回答什么问题？
- 如果对方拒绝或不方便，有备选方案吗？
- 根据场景，智能体应该扮演什么角色？（招聘专员、销售顾问、客服专员……）
- 开场白说什么最自然？对方接起电话的第一句话应该是什么？

**所有已知信息都应填入 `agentProfile.background`，让机器人在通话中有据可依，而不是凭空发挥。**

**`scenarioDescription` 填写原则：**

- 用简洁的中文描述外呼目的，例如：`"面试邀约"`、`"满意度回访"`、`"AI产品体验邀约"`
- 脚本会自动根据描述关键词推断 `industry`（行业）和 `scene`（场景类型）标准值，无需手动指定
- 支持推断的关键词示例：

| 关键词             | 推断 industry | 推断 scene        |
| ------------------ | ------------- | ----------------- |
| 面试、招聘、简历   | HR            | interview_invite  |
| 保险、理财、金融   | finance       | product_promotion |
| 教育、培训、课程   | education     | enrollment        |
| 医疗、体检、预约   | healthcare    | appointment       |
| 快递、物流、订单   | ecommerce     | delivery_notify   |
| 客服、回访、满意度 | service       | survey            |
| 销售、产品、推广   | retail        | product_promotion |
| 通知、提醒         | general       | notify            |
| 其他               | telecom       | survey            |

执行：

```bash
node scripts/bundle.cjs taskInput.json
```

---

### 步骤 5: 执行外呼

**用户确认后执行：**

```bash
# 标准用法（推荐）
node scripts/bundle.cjs taskInput.json
```

**参数说明：**

| 参数                 | 说明                | 使用场景               |
| -------------------- | ------------------- | ---------------------- |
| `taskInput.json`     | JSON 文件路径       | 主要输入方式           |
| `--instance-id <id>` | 指定已有外呼实例 ID | 复用实例，避免重复创建 |
| `--script-id <id>`   | 指定已有话术脚本 ID | 复用话术，避免重复生成 |
| `--no-interactive`   | 禁用交互式输入      | 自动化脚本、CI/CD 场景 |

**查询子命令：**

| 子命令          | 说明                        | 用法                                                                                                     |
| --------------- | --------------------------- | -------------------------------------------------------------------------------------------------------- |
| `query`         | 查询任务组整体进度          | `node scripts/bundle.cjs query <instanceId> <jobGroupId>`                                                 |
| `query-jobs`    | 查询各 Job 详细结果（分页） | `node scripts/bundle.cjs query-jobs <instanceId> <jobGroupId> [--page N] [--size N] [--status Succeeded]` |
| `get-recording` | 获取单通录音下载链接        | `node scripts/bundle.cjs get-recording <instanceId> <jobId>`                                              |

技能执行时自动完成：验证输入 → 创建实例 → 检查绑定号码 → 生成话术 → 创建任务组 → 启动外呼

---

### 步骤 6: 报告结果

向用户报告：

- 外呼任务已启动
- 任务组 ID（`jobGroupId`）
- 拨打的电话数量

遇到错误时，请读取 [troubleshooting.md](references/troubleshooting.md)。

---

### 步骤 7: 安排结果查询

外呼任务启动后，用定时任务的功能来安排一个 **30 秒后的一次性任务**，在隔离会话中查询进度并通知用户：

- 任务名称：`外呼结果查询-<jobGroupId 前 8 位>`
- 触发时间：30 秒后
- 任务内容：执行 `node scripts/bundle.cjs query <instanceId> <jobGroupId>`，根据结果决定下一步：
  - `running` / `partial` → 再安排一个 60 秒后的查询
  - `completed` → 向用户汇报结果，询问是否需要下载录音进行分析

**安排好后立即向用户回复，不要等待外呼完成：**

```
✅ 外呼任务已启动！

📋 任务信息
- 任务组 ID: <jobGroupId>
- 实例 ID: <instanceId>
- 外呼数量: N 人

⏰ 我将在 30 秒后自动查询进度，完成后主动通知你。
```

---

## 交付前检查

执行完成后，逐项确认再向用户报告：

- [ ] 任务组 ID 已获取（`jobGroupId` 不为空）
- [ ] 实际拨打数量与名单数量一致
- [ ] 已告知用户在 [阿里云晓蜜控制台](https://outboundbot.console.aliyun.com/) 查看外呼结果
- [ ] 如有号码验证失败，已向用户说明哪些号码被跳过及原因

---

## 常见场景示例

需要参考具体场景时，请读取 [scenarios.md](references/scenarios.md)。

---

## 注意事项

1. **合规使用** — 确保外呼行为符合相关法律法规，获得用户同意
2. **号码隐私** — 妥善保管客户电话号码，避免泄露
3. **费用控制** — 外呼服务会产生费用，注意控制调用频率
4. **测试优先** — 建议先在测试环境验证，再用于生产

## 参考链接

- [阿里云晓蜜控制台](https://outboundbot.console.aliyun.com/)
- [阿里云晓蜜文档](https://help.aliyun.com/product/outboundbot.html)
