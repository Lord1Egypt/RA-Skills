---
name: mfz-catalogue-report
description: 将单份 DRG 或 DIP 目录的 XLSX、PDF、扫描/OCR PDF 或 DOCX 原始材料整理为可检索交互报告。用户提到目录整理、DRG 权重目录分析、DIP 病种目录分析、OCR 目录校验、目录治理 Excel 或生成报告链接时使用；通过免费的 MedGroup Catalogue Report MCP 完成任务创建、上传、校验、复核和报告生成。
---

# 木非舟目录报告

把用户提供的一份 DRG 或 DIP 目录生成可追溯的治理数据和交互报告。原文识别与 OCR 判断留在当前会话，只向 MCP 提交公开交换合同字段。

## 前置配置

确认客户端已配置 `mfz-catalogue-report` MCP：

- 地址：`https://medgroup.medchat.fun/catalogue-report/mcp`
- 认证：用户在 MedGroup 登录后生成的 API Key，以 `Authorization: Bearer sk-...` 发送

不得在 Skill、脚本、报告或回复中写入 API Key。

## 必读资料

提取目录行前读取 `references/exchange-contract.md`。校验返回 `needs_review` 时读取 `references/review-protocol.md`。

## 工作流

1. 判断附件是单份 DRG 还是 DIP 目录。仅在城市、年份或版本无法从原文确认时询问用户。
2. 检查所有相关 Sheet、表格和页面，区分主目录、说明、床日、日间手术、辅助目录和基层覆盖表，保留每行来源位置。
3. 调用 `create_catalogue_report`，提交目录类型、城市、年份、版本、适用指标和完整源文件清单。
4. 使用返回的上传地址逐个上传原始附件；不要改写上传域名或路径。
5. 按交换合同生成目录行。小型目录每批最多 200 行；大型表格生成临时通用转换脚本并上传 NDJSON，报告 SHA-256 和行数。批次从 0 开始，只有最后一批设置 `is_final: true`。
6. 调用 `validate_catalogue_report`。状态为 `blocked` 或 `needs_review` 时不得宣称报告已经完成。
7. 遇到 `needs_review`，回到指定文件、Sheet、页码和行核对，再用 `confirmed`、`corrected`、`unreadable` 或 `not_found` 处理，直到阻断项清零。
8. 调用 `get_catalogue_report`，只向用户展示状态、质量摘要、警告和 `report_url`，不展示目录行载荷、临时脚本或服务器路径。

## 服务繁忙

校验或生成报告返回 `service_busy` 时，依次等待 10 秒、20 秒和 30 秒后重试，最多重试 3 次。仍繁忙时停止并请用户稍后重试；不要并行创建替代任务。

## 文件处理要求

- XLSX：语义识别 Sheet 和表头；编码按文本保留，权重、点数、支付标准和分值使用数值。
- 文本 PDF 或 DOCX：按页或表提取，不要在识别章节角色前合并不同区块。
- 扫描 PDF：检查页面图像；不得猜测编码、数字、小数点、斜杠、加号或列对齐。为不确定字段提交置信度并进入复核。

## 边界

- 一次只处理一份目录，不做年度对比、病例分组或桑基图。
- 目录基础类型与基层覆盖保持独立。
- 不补齐、截短或虚构编码。
- 不承诺浏览器可见内容无法被复制；报告只限制直接批量导出。
- 无法可靠提取大目录时停止并说明原因，不降低验收标准。
