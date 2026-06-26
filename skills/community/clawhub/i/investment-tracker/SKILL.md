---
name: investment-tracker
description: 投资组合管理助手。可查询/更新持仓、现金、日记、权益曲线，以及通过截图导入持仓。
user-invocable: true
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["curl"]}, "primaryEnv": "DASHSCOPE_API_KEY"}}
---

# Investment Tracker 操作手册

本文档供 AI 代理使用。基础 URL：`http://localhost:8000`。
接口详情见 `references/api-docs.md`。

---

## 全局规则

### 操作分级

| 类型 | 接口 | 执行前是否需要用户确认 |
|------|------|----------------------|
| **只读** | GET /api/holdings、GET /api/cash、GET /api/diary、GET /api/curve、GET /api/imports、GET /api/hs300 | **否**，直接执行并展示结果 |
| **写操作** | POST /api/holdings/bulk、POST /api/cash、POST /api/diary、POST /api/curve/point、POST /api/imports/rollback/{id}、DELETE /api/imports/{id} | **是**，必须先展示预览，等用户回复"确认"后再执行 |
| **分析+写** | POST /api/external/upload → POST /api/holdings/bulk | 分析步骤自动执行；写入步骤需用户确认 |

### 通用错误处理

| curl 错误 / HTTP 状态码 | AI 应对策略 |
|------------------------|------------|
| `curl: (7) Connection refused` | 提示用户："本地服务未启动，请在 backend 目录运行 `uvicorn main:app --reload --port 8000`" |
| `503` | 提示用户："DASHSCOPE_API_KEY 未配置或无效，请检查 backend/.env 文件" |
| `502` | 提示用户："AI 接口调用失败，请稍后重试" |
| `404` | 提示用户："未找到指定记录，请确认 ID 是否正确" |
| `400` | 将响应体中的 `detail` 字段内容告知用户 |

---

## 工作流 A：截图导入持仓

**触发词**：上传截图、导入持仓、更新持仓、今天持仓、截图持仓

### Step 1：上传截图，获取分析结果

```bash
curl -sS -X POST http://localhost:8000/api/external/upload \
  -F "images=@<图片绝对路径>" \
  -F "notes=<用户补充说明，无则省略>" \
  -F "portfolio_date=<YYYY-MM-DD，无则省略>"
```

多张截图时重复 `-F "images=@<路径>"` 参数。

**解析返回结果，向用户展示：**
- `summary`：AI 点评
- `diff.added`：新增持仓（代码、名称、股数）
- `diff.removed`：移除持仓（代码、名称）
- `diff.modified`：变动持仓（代码、名称、before/after 对比）
- `diff.unchanged_count`：未变动数量
- `total_assets` / `total_pnl`（若不为 null）

**必须暂停**，向用户提问：
> "分析完成，是否确认将以上变动更新至持仓系统？"

### Step 2：用户确认后，提交持仓更新

将 Step 1 返回的 `analyzed_holdings` 数组写入临时文件，然后提交：

```bash
# 将 analyzed_holdings 写入临时文件（在当前工作目录）
echo '<analyzed_holdings 的 JSON 数组>' > /tmp/holdings_update.json

curl -sS -X POST http://localhost:8000/api/holdings/bulk \
  -H "Content-Type: application/json" \
  -d "{\"holdings\": $(cat /tmp/holdings_update.json), \"label\": \"<YYYY-MM-DD> 截图导入\"}"

rm /tmp/holdings_update.json
```

成功后告知用户持仓已更新。

### Step 3（可选）：更新权益曲线

若 Step 1 返回的 `total_assets` 不为 null，询问用户：
> "本次截图识别到总资产 ¥<total_assets>，是否同时记录到权益曲线？"

用户确认后执行（日期取 Step 1 返回的 `date`）：

```bash
curl -sS -X POST http://localhost:8000/api/curve/point \
  -H "Content-Type: application/json" \
  -d "{\"date\": \"<date>\", \"value\": <total_assets>}"
```

---

## 工作流 B：查询当前持仓

**触发词**：查看持仓、我的持仓、现在持仓、持仓情况、持仓列表

**直接执行（无需确认）：**

```bash
curl -sS http://localhost:8000/api/holdings
```

**展示格式建议**（表格形式）：

| 代码 | 名称 | 股数 | 成本价 | 现价 | 行业 | 备注 |
|------|------|------|--------|------|------|------|
| ... | ... | ... | ... | ... | ... | ... |

若返回空数组，告知用户："当前持仓为空。"

---

## 工作流 C：现金管理

**触发词**：
- 查询：现金余额、账户现金、剩余资金
- 更新：更新现金、修改现金、现金改成、现金设为

### 查询现金（只读，直接执行）

```bash
curl -sS http://localhost:8000/api/cash
```

取响应中的 `amount` 字段，告知用户当前现金余额。

### 更新现金（写操作，需确认）

先告知用户将要执行的操作：
> "将现金余额更新为 ¥<amount>，确认吗？"

用户确认后执行：

```bash
curl -sS -X POST http://localhost:8000/api/cash \
  -H "Content-Type: application/json" \
  -d "{\"amount\": <数值>}"
```

取响应中的 `amount` 字段，告知用户更新后的余额。

---

## 工作流 D：投资日记

**触发词**：
- 查看：查看日记、投资记录、操作记录、历史日记
- 新增：记一条日记、记录操作、今天买了/卖了、写日记

### 查看日记（只读，直接执行）

```bash
curl -sS http://localhost:8000/api/diary
```

按日期倒序展示，包含字段：日期、类型、股票代码、备注、情绪。

若返回空数组，告知用户："暂无日记记录。"

### 新增日记（写操作，需确认）

从用户描述中提取信息，先展示将要记录的内容：
> "将新增以下日记，确认吗？
> 日期：<date> | 类型：<type> | 代码：<code> | 备注：<remark> | 情绪：<mood>"

**`type` 可选值**：买入、卖出、观察、调仓、清仓  
**`mood` 可选值**：理性、审慎、乐观、焦虑（若用户未指定，默认填"理性"）  
**`code`**：若用户未指定具体股票，填 `""`

用户确认后执行：

```bash
curl -sS -X POST http://localhost:8000/api/diary \
  -H "Content-Type: application/json" \
  -d "{\"date\": \"<YYYY-MM-DD>\", \"type\": \"<type>\", \"code\": \"<code>\", \"remark\": \"<remark>\", \"mood\": \"<mood>\"}"
```

取响应中的 `id` 字段，告知用户日记已记录（ID: <id>）。

---

## 工作流 E：权益曲线

**触发词**：
- 查看：权益曲线、资产走势、历史收益、组合表现
- 新增：记录今天资产、更新权益、今天总资产是

### 查看权益曲线（只读，直接执行）

```bash
curl -sS http://localhost:8000/api/curve
```

展示日期与总市值的序列（按日期升序）。若数据点 ≥2，可计算区间涨幅告知用户。

若返回空数组，告知用户："暂无权益曲线数据。"

### 新增/更新数据点（写操作，需确认）

先告知用户将要执行的操作：
> "将记录权益数据点：<date> ¥<value>，若该日期已存在则覆盖，确认吗？"

用户确认后执行：

```bash
curl -sS -X POST http://localhost:8000/api/curve/point \
  -H "Content-Type: application/json" \
  -d "{\"date\": \"<YYYY-MM-DD>\", \"value\": <数值>}"
```

---

## 工作流 F：沪深300基准对比

**触发词**：沪深300、基准对比、跑赢大盘、指数走势、大盘表现

**直接执行（无需确认）：**

```bash
# 默认 180 个交易日
curl -sS "http://localhost:8000/api/hs300"

# 指定天数（7～1000）
curl -sS "http://localhost:8000/api/hs300?days=<N>"
```

返回 `date` / `close` 数组，按日期升序。

**展示建议**：
- 告知最新收盘价和区间起止日期
- 若同时有权益曲线数据，计算同期组合涨幅与 HS300 涨幅进行对比

**错误处理**：
- `502`：告知用户"沪深300数据获取失败，可能是网络问题或 Yahoo Finance 暂时不可用"
- `404`：告知用户"Yahoo Finance 未返回有效数据，请稍后重试"

---

## 工作流 G：导入历史管理

**触发词**：
- 查看：导入历史、历史记录、快照列表
- 回滚：回滚、撤销、恢复到上次、恢复到某次
- 删除：删除历史、清除记录

### 查看导入历史（只读，直接执行）

```bash
curl -sS http://localhost:8000/api/imports
```

展示列表（按时间倒序）：ID、时间、标签、持仓条数。

### 回滚到指定快照（写操作，需二次确认）

1. 先执行查看操作，展示快照列表供用户选择目标 ID
2. 展示目标快照信息，请求确认：
   > "将把持仓回滚到快照 #<id>（<label>，<created_at>，共 <holding_count> 条），回滚前会自动备份当前持仓，确认吗？"
3. 用户确认后执行：

```bash
curl -sS -X POST http://localhost:8000/api/imports/rollback/<id>
```

告知用户回滚成功，并展示回滚后持仓条数。

### 删除历史记录（写操作，需确认）

先展示目标记录信息，请求确认：
> "将删除快照 #<id>（<label>，<created_at>），此操作不影响当前持仓，确认吗？"

用户确认后执行：

```bash
curl -sS -X DELETE http://localhost:8000/api/imports/<id>
```

告知用户删除成功。
