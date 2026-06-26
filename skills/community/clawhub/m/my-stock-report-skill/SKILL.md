---
name: my_stock_report_skill
description: 当且仅当用户明确提到使用报告引擎、分析引擎、股票引擎、report engine 或者 my_stock_report_skill 时触发。用于调用 Python 分析引擎对特定美股标的进行多维度深度分析，支持指定分析师组合，并将结论和报告归档至钉钉多维表。
---

# My Stock Report Skill (美股报告引擎技能)

## 核心规则与触发条件
- **触发条件**：当用户明确提到“**报告引擎**”、“**分析引擎**”、“**股票引擎**”、“**report engine**”或者“**my_stock_report_skill**”时，触发此技能。
- **参数控制**：
  - `-l` 或 `--language`：指定报告语言（默认 `Chinese`）。
  - `-a` 或 `--analysts`：指定需要启用的分析师模块（**默认值：`social,news,market,fundamental`**）。如果用户在指令中明确要求只看某些维度，则根据用户的需求指定对应的参数（如 `-a fundamental,market`）。
- **执行环境**：操作必须在包含 `run_cli.py` 的工作目录下进行。
- **及时沟通**: 严格按照工作流程执行，如果过程中有疑问，及时通过会话进行沟通确认后再继续。

## 工作流程

### 1. 构建分析命令
根据用户指令构建命令，固定使用 `run_cli.py`：
- **基础模式**：`./venv/bin/python3 run_cli.py -t {标的编码} -a {analysts} -l {language} -n`
- **示例**：如果用户要求“启动报告引擎分析 AAPL，只要基本面”，则执行 `./venv/bin/python3 run_cli.py -t AAPL -a fundamental -l Chinese -n`；若未明确指定分析师组合，则默认传入 `-a social,news,market,fundamental`。

### 2. 钉钉知识库扁平归档, 直接使用`dingtalk-document` 技能
分析完成后，进入 `reports/` 目录下读取生成的报告文件，通过钉钉 API 直接平行创建文档。
**不要求具体的多层级目录层次**，直接在`分析报告列表`父节点下创建两个文档。

**标准执行步骤**：
1. **参数准备**：
   - Workspace ID: `p48ggSGelW2WAo87`
   - 分析报告列表父节点 nodeId: `9E05BDRVQ23be3xQF2pwLjkvJ63zgkYA`
2. **创建两个独立文档**：
   - 使用上述父节点 nodeId，创建名为 `{标的}_最终结论_{YYYYMMDD_HHMMSS}` 的文档，并获取其在线 URL 及 docKey。
   - 使用上述父节点 nodeId，创建名为 `{标的}_完整报告_{YYYYMMDD_HHMMSS}` 的文档，并获取其在线 URL 及 docKey。
3. **写入正文内容**：
   - 使用 docKey，分别调用 `POST https://api.dingtalk.com/v1.0/doc/suites/documents/{docKey}/overwriteContent?operatorId={OPERATOR_ID}`。
   - 将 `decision.txt` 写入“最终结论”文档；将 `complete_report.md` 写入“完整报告”文档。

### 3. 多维表结构化录入,直接 使用`my_stock_report_mgnt_skill` 技能
文档上传完成后，必须将本次分析结果结构化归档到“分析报告多维表”中。
**提取与校验 6 个核心字段**：
- **标的**：美股简码，转为大写（如 AAPL）。
- **分析时间**：格式必须为 `YYYYMMDD_HHMMSS`。
- **分析结论**：从 `decision.txt` 提取明确的核心结论（如 BUY、SELL、HOLD）。
- **分析摘要**：根据本地报告内容提炼，**严格限制在 300 字以内**。
- **结论文档**：步骤 2 中获取的最终结论钉钉文档 URL 链接,直接粘贴链接。
- **完整文档**：步骤 2 中获取的完整报告钉钉文档 URL 链接,直接粘贴链接。

按照 `my_stock_report_mgnt_skill` 的要求，将这组字段执行“新增记录”操作。

### 4. 反馈输出 (Markdown 表格展现)
成功写入多维表后，向用户返回友好的 Markdown 格式回复。**输出内容本质上就是上传钉钉多维表的那 6 个字段的内容**。
示例格式：

| 字段 | 内容 |
| :--- | :--- |
| **标的** | AAPL |
| **分析时间** | 20260325_123000 |
| **分析结论** | BUY |
| **分析摘要** | 苹果公司在AI战略上取得关键突破...（此处为提炼的300字以内摘要） |
| **结论文档** | [钉钉文档链接] |
| **完整文档** | [钉钉文档链接] |
