# Feishu Bitable Toolbox

## 何时使用

这组工具用于 n8n workflow 设计前后处理飞书多维表格字段结构：

- `feishu_get_bitable_schema.py`：读取一个表的字段列表，输出 Markdown 给人看，或 JSON 给后续脚本复用。
- `feishu_create_bitable_fields.py`：从 schema JSON 生成字段创建请求；默认 dry-run，只有显式加 `--execute` 才会写入飞书。

它们只处理字段 schema，不处理记录写入、附件上传、审批、文档块或飞书机器人消息。

## 环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

脚本不会打印 `FEISHU_APP_SECRET` 或 tenant access token。终端命令涉及网络时，按项目全局规则保留本地代理环境。

## 获取字段 Schema

输出 Markdown：

```bash
python3 scripts/toolbox/feishu_get_bitable_schema.py \
  --app-token "base_or_app_token" \
  --table-id "tblxxxx" \
  --format markdown \
  --output /tmp/bitable-schema.md
```

输出 JSON，供创建字段脚本复用：

```bash
python3 scripts/toolbox/feishu_get_bitable_schema.py \
  --app-token "base_or_app_token" \
  --table-id "tblxxxx" \
  --format json \
  --output /tmp/bitable-schema.json
```

## 生成或执行字段创建

默认 dry-run，不写入：

```bash
python3 scripts/toolbox/feishu_create_bitable_fields.py \
  --schema /tmp/bitable-schema.json \
  --app-token "target_base_or_app_token" \
  --table-id "target_tblxxxx"
```

确认无误后执行：

```bash
python3 scripts/toolbox/feishu_create_bitable_fields.py \
  --schema /tmp/bitable-schema.json \
  --app-token "target_base_or_app_token" \
  --table-id "target_tblxxxx" \
  --execute
```

执行模式会先读取目标表已有字段名并跳过同名字段。需要关闭这个保护时加 `--no-skip-existing`。

## 字段限制与安全边界

- 创建字段脚本默认跳过系统/只读字段类型，例如创建时间、更新时间、创建人、修改人、自动编号。
- 如果字段 `ui_type` 显示 `dynamic` 或 `not_support`，默认跳过。动态选项字段常见写入限制，建议改为静态选项或交给 n8n 服务端逻辑处理。
- 附件字段可以作为 schema 字段存在，但记录附件写入不能通过普通 record upsert 完成，通常需要专用附件接口或 n8n 中间层。
- 所有写入默认 dry-run；不要在没有审查 `planned_requests` 的情况下加 `--execute`。
- 输出中的 app token 会被脱敏，schema JSON 不保存 app secret 或 tenant access token。
