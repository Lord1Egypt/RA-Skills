# 交易请求与批量导入

## 单笔买卖

调用 `request_transaction` 前确认：基金代码、标准名称、买卖方向、金额或份额、日期和分组。卖出必须区分按金额还是按份额。

该工具只创建 App 待确认请求。调用成功后明确说明尚未成交，需要用户在 App 中确认。

## 结构化批量导入

用户已经提供文字、表格或 JSON 时：

1. 整理为结构化 `items`；
2. 已知代码时核对标准基金名；有歧义则轻确认；
3. 直接调用 `request_import_review`；
4. `source_kind` 按实际来源填写 `text`、`table` 或 `json`。

不要调用截图识别工具。`request_import_review` 使用独立结构化接口和 `import:request` scope。

`items` 的字段由 MCP schema 给出，三类最小有效记录为：

- `HOLDINGS`：`code`、`amount`，可选 `name`、`total_return`；`0 < amount <= 100000000`，`total_return < amount` 且绝对值不超过 `100000000`。
- `WATCHLIST`：`code`，可选 `name`。
- `TRANSACTIONS`：`type`、`fund_name`、`matched`、`date`；`matched=true` 时还必须提供 `fund_code` 和 `fund_real_name`。买入 `amount` 必须在 `(0, 100000000]`，卖出 `shares` 必须在 `(0, 1000000000]`，批量卖出不支持按金额。`time_mode` 由 `time` 自动推导，15:00 起为 `POST_MARKET`。

已匹配基金代码必须是非 `000000` 的 6 位代码。确实无法匹配的条目可保留 `code/fund_code="000000"`：持仓/自选同时标记 `match_quality="none"`，交易明确标记 `matched=false`，让用户在 App 确认页修正；不得猜测代码。后端会再次核对基金身份和标准名称。

## 图片导入

本地截图或图片读取 [cli-artifacts.md](cli-artifacts.md)，使用 `huahua import screenshots`。不要生成 Base64。

CLI 识别结果写入带类型标记的文件；只检查未匹配、歧义、缺日期、缺金额/份额的条目。确认后用 `huahua import review` 创建 App 待确认请求，提交类型必须与结果文件一致。

## 幂等与待处理请求

- 同一意图重试复用 `client_request_id`；7 天窗口内不得用同一 ID 提交不同内容。
- `get_agent_requests` 查看最近待处理请求。
- 只有用户明确撤销时才调用 `update_agent_request(..., status="DISMISSED")`。
- 不尝试设置 `PROCESSED`；该状态由 App 成功落账后管理。
