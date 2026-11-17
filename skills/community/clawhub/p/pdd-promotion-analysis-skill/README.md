# 商品推广数据分析 Skill

## 安装

将此文件夹放入 Trae 的 Skill 目录：
- macOS/Linux: `~/.trae/skills/pdd-promotion-analysis/`
- Windows: `%USERPROFILE%\.trae\skills\pdd-promotion-analysis\`

## 使用

在 agent 对话中使用以下指令：
- "帮我分析这个数据" → 上传分天数据表（.xls/.xlsx/.csv）
- "分析下这个商品" → 上传推广数据（建议同时上传操作记录）
- "这个商品该不该调价" → 自动完成诊断与建议

首次使用会自动申请调用凭据（保存在本地 `~/.pdd_skill/config.json`，无感知），无需手动配置。

## 命令行示例

```bash
# 推荐：命名参数 + 操作日志
python pdd_analyzer.py analyze data.xls \
  --ops-file ops.xls --roi-baseline 3.0 --bid-mode net_target_roi --bid-target 4.0

# analyze 输出 402 时，按其 stdout 提示执行 alipay-bot 402-buyer-pay 付款；
# 支付工具会自动携带支付凭证用同一请求体重放，返回的“资源响应体”即报告 JSON，保存后渲染：
python pdd_analyzer.py render report.json --format html
python pdd_analyzer.py render report.json --format markdown
python pdd_analyzer.py render report.json --format json
```

## 付费说明（Pay Skill · A2M 402 协议）

- 本 Skill 为付费 Skill：数据分析接口（`/api/analyze`）为按次付费（支付宝 AI 按量付费 / A402 402 协议：Payment-Needed 账单 → 付款 → 支付工具携带 Payment-Proof 同体重放），未完成支付无法获得分析结果
- 文件先经免费端点 `/api/stage` 暂存，再用内联 JSON `{"staging_id": ...}` 触发付费分析（支付工具无法重放 multipart）
- **前置依赖**：使用方需安装支付宝官方支付技能 `alipay-payment-skill` 完成付款；未安装时本技能终止分析并提示安装
- 知识库原文查询接口（`/api/query`、`/api/topics`）已下线（410），方法论仅随付费诊断报告输出，无免费套取入口
- 服务端在返回资源后向支付宝异步发送履约确认（fulfillment.confirm）
- 本 Skill 不实现任何支付逻辑，也不包含诊断分析逻辑

## 安全说明

- Skill 壳不包含任何核心分析逻辑，仅负责文件解析、商品 ID 识别、请求调用与报告渲染
- 诊断规则、病症判定、建议映射等核心能力全部保留在付费 API 服务端
- 调用凭据仅保存在本地 `~/.pdd_skill/config.json`，用于识别调用者，不含个人身份信息
- 报告输出目录: `~/.pdd_skill/report_YYYYMMDD_HHMMSS.{html|md|json}`

## 技术细节

- 支持文件: .xls, .xlsx, .csv
- 依赖：Python 3.8+，pandas / xlrd / openpyxl / requests
