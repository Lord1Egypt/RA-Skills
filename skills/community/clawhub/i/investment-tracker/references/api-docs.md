# Investment Tracker API 速查手册（AI 代理版）

基础 URL：`http://localhost:8000`  
完整文档：见项目根目录 `API.md`

---

## 接口速查索引

| 方法 | 路径 | 作用 | 需要用户确认 |
|------|------|------|:----------:|
| POST | /api/external/upload | 上传截图，获取 AI 分析与持仓变动差异 | 否（分析步骤） |
| POST | /api/analyze | 上传 Base64 截图，获取 AI 识图结构化结果 | 否 |
| GET  | /api/holdings | 读取当前全部持仓 | 否 |
| POST | /api/holdings/bulk | 原子替换全部持仓（截图导入确认后） | **是** |
| GET  | /api/imports | 查看导入历史快照列表 | 否 |
| POST | /api/imports/rollback/{id} | 将持仓回滚到指定快照 | **是** |
| DELETE | /api/imports/{id} | 删除一条历史快照记录 | **是** |
| GET  | /api/cash | 查询当前现金余额 | 否 |
| POST | /api/cash | 更新现金余额 | **是** |
| GET  | /api/diary | 查看全部投资日记 | 否 |
| POST | /api/diary | 新增一条投资日记 | **是** |
| GET  | /api/curve | 查看权益曲线数据 | 否 |
| POST | /api/curve/point | 新增或更新权益曲线数据点 | **是** |
| GET  | /api/hs300 | 获取沪深300近N日收盘价 | 否 |

---

## POST /api/external/upload

**用途**：上传持仓截图，AI 自动解析并与当前持仓对比，返回变动差异。这是截图导入流程的第一步，不写数据库。

**即用命令**

```bash
# 单张截图
curl -sS -X POST http://localhost:8000/api/external/upload \
  -F "images=@<图片绝对路径>" \
  -F "notes=<补充说明，可省略>" \
  -F "portfolio_date=<YYYY-MM-DD，可省略>"

# 多张截图（重复 -F images 参数）
curl -sS -X POST http://localhost:8000/api/external/upload \
  -F "images=@<路径1>" \
  -F "images=@<路径2>" \
  -F "notes=<补充说明>"
```

**AI 需要提取的关键响应字段**

| 字段 | 用途 |
|------|------|
| `analyzed_holdings` | 完整持仓数组，用户确认后传给 POST /api/holdings/bulk |
| `summary` | 展示给用户的 AI 点评 |
| `diff.added` | 展示新增持仓明细 |
| `diff.removed` | 展示移除持仓明细 |
| `diff.modified` | 展示变动持仓（含 before/after） |
| `diff.unchanged_count` | 展示未变动数量 |
| `total_assets` | 若不为 null，询问用户是否写入权益曲线 |
| `date` | 持仓日期，用于后续写入权益曲线 |

**错误处理**

| 状态码 | AI 应对 |
|--------|--------|
| `400` | "未检测到上传的图片，请确认文件路径是否正确" |
| `502` | "AI 接口调用失败，请稍后重试" |
| `503` | "DASHSCOPE_API_KEY 未配置，请检查 backend/.env" |

---

## POST /api/analyze

**用途**：将截图的 Base64 编码发送给 AI，返回结构化持仓识别结果。与 /api/external/upload 不同，此接口需要调用方自行提供 current_holdings 上下文，也不计算 diff。

**即用命令**

```bash
# 先将图片转为 Base64
B64=$(base64 -i <图片路径>)

curl -sS -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{
    \"base64_images\": [\"${B64}\"],
    \"media_types\": [\"image/jpeg\"],
    \"description\": \"<补充说明，可省略>\",
    \"portfolio_date\": \"<YYYY-MM-DD，可省略>\"
  }"
```

**AI 需要提取的关键响应字段**

响应结构为 `{"result": "<JSON字符串>"}` ，需要先 JSON.parse result：

| result 中的字段 | 用途 |
|----------------|------|
| `holdings` | 识别到的持仓数组（code / name / shares / cost / price / pnl_pct / sector） |
| `total_assets` | 账户总资产（元），null 表示截图无法识别 |
| `date` | 截图中的日期，null 表示截图无日期 |
| `summary` | AI 点评（≤80字） |

**错误处理**

| 状态码 | AI 应对 |
|--------|--------|
| `400` | "未提供图片" |
| `502` | "AI 接口调用失败，请稍后重试" |
| `503` | "DASHSCOPE_API_KEY 未配置，请检查 backend/.env" |

---

## GET /api/holdings

**用途**：读取数据库中当前全部持仓。只读，直接执行。

**即用命令**

```bash
curl -sS http://localhost:8000/api/holdings
```

**AI 需要提取的关键响应字段**

返回 `Holding[]` 数组，每条记录：

| 字段 | 展示用途 |
|------|---------|
| `code` | 股票代码 |
| `name` | 股票名称 |
| `shares` | 持仓数量 |
| `cost` | 成本价 |
| `price` | 现价 |
| `sector` | 行业 |
| `notes` | 备注 |

空数组时告知用户"当前持仓为空"。

---

## POST /api/holdings/bulk

**用途**：原子替换全部持仓（先清空再整体写入），执行前自动创建快照。**写操作，需用户确认后执行。**

**即用命令**

```bash
curl -sS -X POST http://localhost:8000/api/holdings/bulk \
  -H "Content-Type: application/json" \
  -d "{
    \"label\": \"<YYYY-MM-DD> 截图导入\",
    \"holdings\": <holdings JSON 数组>
  }"
```

`holdings` 数组中每条记录必填字段：`id`、`code`、`name`、`shares`、`cost`、`price`。

**AI 需要提取的关键响应字段**

返回写入后的 `Holding[]` 数组，告知用户持仓已更新，共 N 条记录。

---

## GET /api/imports

**用途**：查看全部导入历史快照列表（最新在前）。只读，直接执行。

**即用命令**

```bash
curl -sS http://localhost:8000/api/imports
```

**AI 需要提取的关键响应字段**

| 字段 | 展示用途 |
|------|---------|
| `id` | 快照 ID，用于回滚/删除操作 |
| `created_at` | 快照时间 |
| `label` | 导入标签 |
| `holding_count` | 快照包含的持仓条数 |

空数组时告知用户"暂无导入历史"。

---

## POST /api/imports/rollback/{id}

**用途**：将持仓回滚到指定快照。执行前自动备份当前持仓。**写操作，需用户二次确认。**

**操作前置步骤**：先调用 GET /api/imports 获取列表，展示目标快照信息后再确认。

**即用命令**

```bash
curl -sS -X POST http://localhost:8000/api/imports/rollback/<id>
```

**AI 需要提取的关键响应字段**

返回回滚后的 `Holding[]` 数组，告知用户回滚成功，共 N 条记录。

**错误处理**

| 状态码 | AI 应对 |
|--------|--------|
| `404` | "未找到 ID 为 <id> 的快照，请确认 ID 是否正确" |

---

## DELETE /api/imports/{id}

**用途**：删除一条历史快照记录，不影响当前持仓。**写操作，需用户确认。**

**即用命令**

```bash
curl -sS -X DELETE http://localhost:8000/api/imports/<id>
```

**AI 需要提取的关键响应字段**

响应为 `{"ok": true}`，告知用户删除成功。

**错误处理**

| 状态码 | AI 应对 |
|--------|--------|
| `404` | "未找到 ID 为 <id> 的快照" |

---

## GET /api/cash

**用途**：查询账户当前现金余额。只读，直接执行。

**即用命令**

```bash
curl -sS http://localhost:8000/api/cash
```

**AI 需要提取的关键响应字段**

响应为 `{"amount": <数值>}`，告知用户当前现金余额。

---

## POST /api/cash

**用途**：覆盖更新现金余额。**写操作，需用户确认。**

**即用命令**

```bash
curl -sS -X POST http://localhost:8000/api/cash \
  -H "Content-Type: application/json" \
  -d "{\"amount\": <数值>}"
```

**AI 需要提取的关键响应字段**

响应为 `{"amount": <数值>}`，告知用户现金已更新为 ¥<amount>。

---

## GET /api/diary

**用途**：查看全部投资日记（按日期倒序）。只读，直接执行。

**即用命令**

```bash
curl -sS http://localhost:8000/api/diary
```

**AI 需要提取的关键响应字段**

| 字段 | 展示用途 |
|------|---------|
| `id` | 日记 ID |
| `date` | 日期 |
| `type` | 操作类型（买入/卖出/观察等） |
| `code` | 关联股票代码 |
| `remark` | 备注内容 |
| `mood` | 操作情绪 |

空数组时告知用户"暂无日记记录"。

---

## POST /api/diary

**用途**：新增一条投资日记。**写操作，需用户确认。**

**即用命令**

```bash
curl -sS -X POST http://localhost:8000/api/diary \
  -H "Content-Type: application/json" \
  -d "{
    \"date\": \"<YYYY-MM-DD>\",
    \"type\": \"<买入|卖出|观察|调仓|清仓>\",
    \"code\": \"<股票代码，无则为空字符串>\",
    \"remark\": \"<备注内容>\",
    \"mood\": \"<理性|审慎|乐观|焦虑，默认理性>\"
  }"
```

**AI 需要提取的关键响应字段**

响应为完整 DiaryEntry 对象，取 `id` 字段，告知用户"日记已记录（ID: <id>）"。

---

## GET /api/curve

**用途**：查看全部权益曲线数据点（按日期升序）。只读，直接执行。

**即用命令**

```bash
curl -sS http://localhost:8000/api/curve
```

**AI 需要提取的关键响应字段**

返回 `{"date": "YYYY-MM-DD", "value": <数值>}[]` 数组。  
若数据点 ≥2，可计算区间涨幅（最新值/最早值 - 1）告知用户。  
空数组时告知用户"暂无权益曲线数据"。

---

## POST /api/curve/point

**用途**：追加或更新某日的权益曲线数据点（同日期覆盖）。**写操作，需用户确认。**

**即用命令**

```bash
curl -sS -X POST http://localhost:8000/api/curve/point \
  -H "Content-Type: application/json" \
  -d "{\"date\": \"<YYYY-MM-DD>\", \"value\": <数值>}"
```

**AI 需要提取的关键响应字段**

响应为写入后的 CurvePoint 对象，告知用户"权益数据点已记录：<date> ¥<value>"。

---

## GET /api/hs300

**用途**：获取沪深300指数（000300.SS）近 N 个交易日的收盘价，用于与持仓收益对比。只读，直接执行。

**即用命令**

```bash
# 默认 180 个交易日
curl -sS "http://localhost:8000/api/hs300"

# 指定交易日数（范围 7～1000）
curl -sS "http://localhost:8000/api/hs300?days=<N>"
```

**AI 需要提取的关键响应字段**

返回 `{"date": "YYYY-MM-DD", "close": <数值>}[]` 数组（升序）。  
展示最新收盘价，并可计算区间涨幅与组合表现对比。

**错误处理**

| 状态码 | AI 应对 |
|--------|--------|
| `502` | "沪深300数据获取失败，可能是网络问题或 Yahoo Finance 暂时不可用，请稍后重试" |
| `404` | "Yahoo Finance 未返回有效数据，请稍后重试" |
