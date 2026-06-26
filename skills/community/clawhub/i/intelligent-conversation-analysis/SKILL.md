---
name: ccai-conversation-analysis
description: >-
  该技能调用阿里云晓蜜 CCAI AIO，对客服通话或文字对话进行 AI 智能分析，支持摘要生成、服务质检、情绪检测、满意度评估、关键词提取、字段抽取、QA 生成、用户画像、标签分类等多种分析任务，输入可以是文本对话或语音文件 URL。
  当用户问题涉及「总结/摘要一段对话或通话内容」「对客服录音做质检或合规检查」「分析用户情绪或满意度」「从对话中提取关键词、字段、待办事项」「对通话做 QA 抽取或用户画像」时使用该技能。
---

# 晓蜜 CCAI AIO 对话分析

基于阿里云通义晓蜜 CCAI AIO，对文本对话或语音通话进行智能分析。

## 前置条件

### 配置阿里云凭证

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-access-key-id"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-access-key-secret"
```

### 配置 CCAI 应用信息 ⚠️ 重要

需要在 [百炼控制台](https://bailian.console.aliyun.com/#/app-center) 开通 CCAI AIO 服务并创建应用，获取以下两个 ID：

```bash
export CCAI_APP_ID="your-app-id"           # 必填：应用 ID
export CCAI_WORKSPACE_ID="your-workspace-id"  # 必填：业务空间 ID
```

如何获取 App ID 和 Workspace ID，请读取 [setup.md](references/setup.md)。

## 执行清单

复制此清单并在执行时逐项打勾：

- [ ] 步骤 1: 了解用户需求
  - [ ] 1.1 分析类型是什么？（摘要/质检/情绪/…）
  - [ ] 1.2 输入来源是什么？（文本对话 / 语音文件 URL / 前置节点输出）
- [ ] 步骤 2: 验证前置条件
  - [ ] 2.1 AK/SK 环境变量已配置
  - [ ] 2.2 CCAI_APP_ID 已配置（必填）
  - [ ] 2.3 CCAI_WORKSPACE_ID 已配置（必填）
  - [ ] 2.4 输入内容有效（文本非空 / 语音 URL 可访问）
- [ ] 步骤 3: 生成 task.json ⛔ BLOCKING — 向用户确认后才执行
  - [ ] 3.1 根据意图推断 resultTypes（请读取 [task-types.md](references/task-types.md)）
  - [ ] 3.2 构建 dialogue 或 transcription（请读取 [input-formats.md](references/input-formats.md)）
  - [ ] 3.3 如需质检，补充 serviceInspection 配置
- [ ] 步骤 4: 执行分析
- [ ] 步骤 5: 展示结果并执行交付检查

---

### 步骤 1: 了解用户需求

**分析类型推断**（根据用户描述自动选择 resultTypes）：

- 用户说"摘要、总结、概括" → `["summary", "title"]`
- 用户说"关键词、标签" → `["keywords", "category_tag"]`
- 用户说"质检、合规检查" → `["service_inspection"]`
- 用户说"问题和解决方案、处理结果" → `["question_solution"]`
- 用户说"QA、问答对" → `["questions_and_answer"]`
- 用户说"字段提取、结构化" → `["fields"]`
- 用户说"自定义分析、自定义指令" → `["custom_prompt"]`
- 用户说"全量分析、完整分析" → 全部 9 种类型

**输入来源判断**：

- 用户粘贴了对话文本 → `taskType: "text"`，构建 `dialogue.sentences`
- 用户提供了音频 URL → `taskType: "audio"`，构建 `transcription`
- 来自前置节点（如外呼录音）→ 从上下文提取 URL 或对话内容，无需再次询问

问自己：

- 用户描述的分析目标是什么？对应哪些 resultTypes？
- 对话内容是文本还是语音？每条消息的说话角色是谁（user/agent/system）？
- 如果是质检，质检的场景和维度是什么？

---

### 步骤 2: 验证前置条件

逐项检查：

- 环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 是否已配置？
- `CCAI_APP_ID` 是否已配置？（必填，没有则无法调用）
- 文本输入是否有实际内容？语音 URL 是否是可访问的公网地址？

---

### 步骤 3: 生成 task.json ⛔ BLOCKING

请读取 [input-formats.md](references/input-formats.md)，根据已知信息构建 task.json 文件。

**向用户展示并等待确认：**

```
准备执行对话分析，请确认以下信息：

📋 任务信息
- 输入类型: [文本对话 / 语音文件]
- 分析类型: [resultTypes 列表]
- 对话条数/文件: [N 条 / 文件名]

是否确认执行分析？
```

- ✅ 必须等待用户明确确认后才能执行
- ❌ 不要在用户未确认的情况下自动执行

---

### 步骤 4: 执行分析

**模式 A：直接执行（适合简单场景，等待结果）**

```bash
node scripts/bundle.cjs task.json
```

脚本自动完成：提交任务 → 每 2 秒轮询一次 → 最多等待 120 秒 → 格式化输出结果

**模式 B：非阻塞执行（OpenClaw 环境推荐）**

Step 1 — 提交任务，获取 taskId：

```bash
CCAI_ASYNC=1 node scripts/bundle.cjs task.json
```

脚本提交任务后立即输出 `taskId`，不等待结果。

Step 2 — 用 `cron.add` 安排一个 **15 秒后的一次性任务**，在隔离会话中查询结果并通知用户：

- 任务名称：`CCAI分析结果查询-<taskId 前 8 位>`
- 触发时间：15 秒后
- 任务内容：执行 `node scripts/bundle.cjs query <taskId>`，根据结果决定下一步：
  - `QUEUE` → 再安排一个 15 秒后的查询
  - `FINISH` → 格式化输出结果并通知用户
  - `ERROR` → 告知用户错误信息

**安排好后立即向用户回复，不要等待分析完成：**

```
✅ 分析任务已提交！

📋 任务信息
- 任务 ID: <taskId>
- 分析类型: <resultTypes>

⏰ 我将在 15 秒后自动查询结果，完成后主动通知你。
```

遇到错误时，请读取 [troubleshooting.md](references/troubleshooting.md)。

---

### 步骤 5: 展示结果

## 交付前检查

执行完成后，逐项确认再向用户报告：

- [ ] 所有 resultTypes 均有对应结果输出（无"无结果"项）
- [ ] 已向用户说明每种分析类型的结果含义
- [ ] 如有字段提取或质检，结果是否符合用户预期？是否需要调整配置后重跑？

---

## 常见场景示例

需要参考具体场景时，请读取 [scenarios.md](references/scenarios.md)。

---

## 注意事项

1. **数据合规** — 对话内容可能含有用户隐私，确保符合数据处理规范
2. **字数限制** — 对话内容上限 2 万字，超过部分自动截断
3. **音频格式** — 建议使用 8k 采样率，其他采样率会影响识别效果
4. **任务保留** — 任务数据在服务端保存 90 天
5. **费用控制** — CCAI AIO 按调用量计费，注意控制频率

## 参考链接

- [百炼控制台](https://bailian.console.aliyun.com/#/app-center)
- [CCAI AIO 产品文档](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-overview)
