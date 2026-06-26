---
name: "smart_wardrobe_analysis"
description: "基于大模型（minimax）分析衣橱统计数据，提取 inventory 与 USER 偏好，生成并返回智能建议与可视化 HTML 统计看板。"

# 【环境依赖】
requires:
  config: ["USER.md", "inventory.md"]
  files: ["TOOLS/wardrobe_analysis_tool.py"]

# 【版本与作者】
version: "1.0.0"
author: "Yuna"
---

## 1. 技能目标 (Objective)
在用户提问“看看我的衣橱统计”或“我还缺什么衣服”时被触发。系统需要读取用户预设的衣橱管理偏好（如色彩比例、件数上限）及当前的衣橱清单记录，通过提供给大模型prompt获取专业评估结果。最后提取返回的 HTML 代码保存为电子看板面板，发送给用户查看及交互。

## 2. 执行逻辑 (Logic & Steps)

### 阶段一：数据准备与负载构建
1. **获取参数**：从 `USER.md` 的 `smart_wardrobe_preference` 中读取用户设定的约束与偏好配置（如单季上限、色彩配比目标等）；从 `inventory.md` 读取当前的衣物清单文本。
2. **构建 Payload**：调用 `wardrobe_analysis_tool.py` 中的 `build_analysis_payload(preferences, inventory_md, model, max_tokens)` 方法。
3. **校验返回结果**：确保 `status` 为 `success`。系统将为您返回 `payload` 数据，内部已组装好预定提示词。

### 阶段二：大模型调用与提取
1. **调用模型**：AI Agent 发送上一步生成的 Payload，请求大模型。
2. **接收分析**：大模型将严格按照 `wardrobe_analysis_prompt.md` 的要求，仅仅输出一个完整的 HTML 页面代码（以 `<!DOCTYPE html>` 开头），**不再包含其他解释文字**。
3. **关键校验**：你需要确保返回的 HTML 最末尾包含一段 `<script type="application/json" id="wardrobe-stats">` 模块。若是大模型未按规范输出，建议重试或提醒它加上。

### 阶段三：保存看板与同步数据反馈用户
1. **调用保存方法**：**重要！** Agent 必须通过运行代码实例化 `WardrobeAnalysisManager`，并将大模型的 HTML 返回值及用户偏好传入调用 `save_html_dashboard(llm_response, preferences)` 方法，以保存 HTML 看板并触发 `USER.md` 数据同步。
2. **落库与更新检查**：验证该方法是否将 HTML 文件成功保存在 `wardrobe_dashboard/` 目录，并确保其自动从 JSON 数据块提取了色彩比例、总件数等统计数据，同步追加入 `USER.md` 中。
3. **返回文件**：提取成功生成的 HTML 看板的绝对或相对路径回传给用户（或触发直接发送文件的操作），并搭配文本总结语：“为您生成了最新的衣橱诊断看板，并已将实时统计数据同步至您的个人档案中，请查看”

## 3. 约束与偏好 (Constraints & Preferences)
- **绝对禁止自行统计**：Agent 不应自行对衣橱数据进行统计与计算分析。
- **必须调用工具**：严禁 Agent 手动拼接 Prompt，必须强制强调调用 `wardrobe_analysis_tool.py` 中的 `build_analysis_payload()` 防止模板或指标读取发生偏移。
- **文件交付为主**：大模型返回的内容包含大量 HTML 原码，Agent 不需要将大段代码直接朗读或打印给用户。必须调用 `wardrobe_analysis_tool.py` 里的 `save_html_dashboard()`，获取html文件后发送用户。

## 4. 示例 (Examples)

**触发话术：** “我想看看我的衣橱统计，顺便帮我诊断下还缺什么。”

**Agent 动作：**
1. 读取 `USER.md` 和 `inventory.md`。
2. 初始化 `WardrobeAnalysisManager`，调用 `build_analysis_payload(preferences, inventory_md)` 拿到对应 payload 并请求AI。
3. 取得模型返回的包含内置统计 JSON 块的纯 HTML 代码后，**必须**调用工具 `save_html_dashboard(llm_response, preferences)` 存盘。
4. 返回 `{"status": "success", "filepath": "./smart_wardrobe/wardrobe_dashboard/2026-04-01个人电子衣橱看板.html"}`。
5. 展示给用户：“为您生成了最新的衣橱诊断看板，并已将实时统计数据同步至您的个人档案中，请点击网页文件查看详细内容。”
