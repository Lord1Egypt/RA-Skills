# 外部平台发布技术方案设计 Reference (External Publishing Design Reference)

## 0. 文档说明与适用场景
- **核心目的**：规范所有涉及“跨平台/外部系统内容发布”的技术方案设计，确保发布链路稳定、状态一致，并规避反自动化检测。
- **适用场景**：自动化发帖、机器人回复、基于无头浏览器（Puppeteer/Playwright）的内容同步等。

## 1. 前置状态与环境准备 (Preconditions)
外部发布第一原则：**顺应目标平台的环境，而非粗暴重置**。
- **页面复用原则**：必须基于已打开、具有合法 Session 的目标页面操作。
- **标准规范**：确保已在目标问题页/发布页（如 https://www.zhihu.com/question/{qid}）的 Tab 下。
- **红线警告**：🚫 严禁在流程中使用 `page.goto()` 或 `browser.navigate()` 重新加载页面，极易断连/丢状态/触发风控。

## 2. 标准发布工作流 (The Publishing Workflow)
设计代码逻辑必须遵循“混合驱动”步骤（API 写入 + DOM 激活 + UI 交互）：

### Step 1: 服务端草稿预写 (API 驱动)
- **动作**：调用内部 API 静默写入核心内容。
- **示例**：`PUT /api/v4/questions/{qid}/draft` 注入 HTML 内容（稳定、快速、可保留复杂排版）。

### Step 2: 编辑器状态激活 (DOM 驱动 - 关键节点)
- **痛点**：Draft.js/Quill 等富文本编辑器 State 与 DOM 分离，API 写入无法触发 onChange。
- **动作**：通过底层命令注入少量触发字符，强行唤醒内部状态。
- **示例**：`execCommand('insertText')` 注入空格/无关字符，点亮发布按钮。

### Step 3: 物理动作模拟 (UI 驱动)
- **动作**：定位真实“发布回答”按钮，执行点击提交。

### Step 4: 结果强校验 (Verification)
- **动作**：不依赖 Toast；必须监听 URL 或 DOM 关键元素变化。
- **示例**：轮询直到 URL 含 `/answer/{id}`。

### Step 5: 最终格式清洗 (API 驱动 - 可选但推荐)
- **动作**：发布成功后，用原生 API 覆盖一次 HTML，避免格式丢失。
- **示例**：`PUT /api/v4/answers/{answer_id}` 覆盖纯净 HTML。

## 3. 避坑指南与黄金法则 (TL;DR)
✅ 成功公式：
**API 写草稿 (PUT draft) → execCommand 激活 EditorState → 点击发布 → 强校验 URL**

否则极易卡在“写了 draft 但没发布成功”。

## 4. 异常回滚与重试策略 (Error Handling)
方案中必须回答：
1. **Step 2 激活失败**（找不到编辑器选区）→ 先点击编辑器区域获取 Focus，再尝试注入。
2. **超时未检测到 URL 跳转**→ 记录现场、刷新状态（避免 navigate），必要时告警。
3. **重试上限**→ 明确最大次数与超限告警机制。
