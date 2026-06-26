# Pengbo Space API Reference (Skill Mapping)

Base URL (default): `https://pengbo.space/api/v1`  
Method: `POST`  
Content-Type: `application/x-www-form-urlencoded`

## 统一输出格式

成功：
```json
{
  "ok": true,
  "action": "services",
  "data": {},
  "display": {},
  "lang": "zh"
}
```

失败：
```json
{
  "ok": false,
  "action": "services",
  "error": "The selected key is invalid."
}
```

---

## 全局参数
- `--key`：API Key（或环境变量 `PENGBO_API_KEY`）
- `--base-url`：API 地址（默认 `https://pengbo.space/api/v1`）
- `--timeout`：请求超时（默认 20s）
- `--retries`：重试次数（默认 2）
- `--retry-delay`：重试间隔秒（默认 1.5）
- `--lang`：输出语言（`auto|zh|en|es|mixed`，默认 `auto`）
- `--input-text`：语言识别提示文本（可选，推荐传用户原话）

---

## Action Matrix

## 0) setup
- **用途**：首次一键引导（检查 key、执行 health、给出下一步命令）
- **必填参数**：无
- **可选参数**：`--key --base-url --timeout --retries --retry-delay`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py setup
```
- **失败（缺 key）示例**：
```json
{
  "ok": false,
  "action": "setup",
  "error": "missing_api_key",
  "next_steps": [
    "登录 https://pengbo.space",
    "到 https://pengbo.space/user/api/docs 获取 key",
    "export PENGBO_API_KEY=\"<your_api_key>\""
  ]
}
```

## 1) health
- **用途**：预检 key / API / 账号可用性
- **必填参数**：无
- **可选参数**：`--key --base-url --timeout --retries --retry-delay`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py health
```
- **示例返回**：
```json
{
  "ok": true,
  "action": "health",
  "data": {
    "base_url": "https://pengbo.space/api/v1",
    "key_loaded": true,
    "api_reachable": true,
    "account_usable": true
  }
}
```
- **缺 key 返回**：`error=missing_api_key` + `next_steps`（可直接执行）
- **风险提示**：无写操作风险
- **状态展示**：`display.订单状态` 已映射本地化文案（如 `COMPLETED -> 已完成`）

## 2) services
- **用途**：查询服务（支持缓存+本地筛选）
- **必填参数**：无（但 live/auto 需要可用 key）
- **可选参数**：
  - `--source auto|live|cache`（默认 auto）
  - `--cache-path <path>`
  - `--cache-max-age-days <int>`（默认 8）
  - `--jitter <seconds>`（默认 0）
  - `--fields service,name,category,rate,min,max`
  - `--query "twitter followers"`
  - `--limit 20`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py services --query "twitter" --fields service,name,rate,min,max --limit 20
```
- **缓存命名规则（默认）**：
  - `data/services-cache_<host>_<keyhash>.json`
- **风险提示**：无写操作风险

## 3) refresh-cache
- **用途**：强制刷新服务缓存
- **必填参数**：无
- **可选参数**：`--cache-path --jitter`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py refresh-cache --jitter 1.5
```
- **风险提示**：无写操作风险

## 4) add
- **用途**：新建订单
- **必填参数**：`--service --link --quantity --confirm`
- **可选参数**：`--runs --interval --comments`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py add --service 1 --link "https://..." --quantity 1000 --confirm
```
- **示例返回**：上游返回包裹在 `ok/action/data`
- **兼容别名**：`create-order`
- **风险提示**：真实扣费；含 30 秒重复下单幂等保护

## 5) create-order
- **用途**：`add` 的命令别名
- **内部实现**：统一归一化为 `action=add`

## 6) status
- **用途**：单订单状态
- **必填参数**：`--order`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py status --order 12345
```

## 7) orders
- **用途**：多订单状态
- **必填参数**：`--orders`（逗号分隔）
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py orders --orders 1,2,3
```

## 8) list-orders
- **用途**：历史订单列表（`action=list_orders`）
- **必填参数**：无
- **可选参数**：`--limit --offset --status-filter --search`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py list-orders --limit 20
```

## 9) refill
- **用途**：发起补单
- **必填参数**：`--order --confirm`
- **示例命令**：
```bash
python3 skills/pengbo-space/scripts/pengbo_smm.py refill --order 12345 --confirm
```
- **风险提示**：写操作

## 10) refill-status
- **用途**：查询补单状态
- **必填参数**：`--refill`

## 11) balance
- **用途**：账户余额
- **必填参数**：无

---

## 上游不支持 + 替代方案
- `cancel`：返回 `unsupported_by_upstream`
- `bulk refill create`：循环调用 `refill`
- `bulk refill status`：循环调用单个 `refill-status`

---

## 审计与数据文件
- 服务缓存：`data/services-cache_<host>_<keyhash>.json`
- 写操作日志：`data/orders-log.jsonl`
- 首次欢迎标记：`data/onboarding-state.json`（只推送一次欢迎信息）
