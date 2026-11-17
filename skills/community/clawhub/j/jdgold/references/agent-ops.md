# Agent 内部执行说明（勿向用户展示）

> 本节仅供 Agent 在后台调用。**Skill 已不再持有 ak/sk**，所有业务接口通过
> ``cf-gold-ai`` 后端 BFF（HTTPS）完成，路径在 ``scripts/bff_client.py`` 内统一维护。
>
> 调试切换：设置环境变量 ``GOLD_BFF_BASE_URL=http://localhost:8080`` 即可指向本地后端。

## ⚠️ 路径约定

所有脚本命令的工作目录（cwd）为本 Skill 安装目录下的 `scripts/` 子目录。
以下示例用 `${SKILL_DIR}` 指代 Skill 根目录（即 `SKILL.md` 所在目录），
实际执行时请替换为安装后的绝对路径。

```bash
cd ${SKILL_DIR}/scripts
```

## 🐾 客户端类型上报（claw）

所有对外接口均支持上报调用方的 claw 客户端类型（如 `codex`、`openclaw`），
用于后端识别流量来源。取值优先级：**命令行 `--claw` > 环境变量 `CLAW`**。

- 所有面向用户脚本（含 `jos.py` 各子命令）均新增 `--claw` 入参：
  ```bash
  python3 query_gold.py "金价" --claw codex
  python3 jos.py holdings --claw openclaw
  ```
- 也可统一通过环境变量注入（对所有脚本生效）：
  ```bash
  export CLAW=codex
  ```
- 底层实现：`--claw` 回填到环境变量 `CLAW`，各请求自动附加请求头 `x-claw`
  （与 `x-skill-code` / `x-skill-run-id` 对齐）。取值中心见 `scripts/jdjr_config.py`
  与 `scripts/bff_client.py` 的 `set_claw()`；claw 为空时不注入该头。

## 金价查询

```bash
cd ${SKILL_DIR}/scripts
python3 query_price_jhub.py                # 默认查询京东24h金价（WG-JDAU）
python3 query_price_jhub.py WG-JDAU        # 京东24h金价
python3 query_price_jhub.py CMBC-JCJ       # 民生银行积存金
python3 query_price_jhub.py CZB-JCJ        # 浙商银行积存金
python3 query_price_jhub.py WG-PAXGUSD     # PAXGUSD暗金
python3 query_price_jhub.py WG-XAUUSD      # 伦敦金
python3 query_price_jhub.py WG-JDAU --analyze  # 实时价格+走势分析
python3 query_price_jhub.py --bank CMBC    # 按银行code查询
python3 query_price_jhub.py --parse "查询民生银行积存金价格"  # 解析用户原文
python3 query_price_jhub.py --list         # 列出所有支持的uniqueCode（内部调试用，勿对客展示）
python3 jos.py price                       # 同上，通过jos子命令
python3 jos.py price --analyze             # 实时价格+走势分析
python3 jos.py price --bank CMBC           # 按银行查询
python3 jos.py price --parse "黄金多少钱"   # 解析用户原文
```

**底层**：``GET {BFF_BASE}/api/v1/price/query?uniqueCode=...&accessToken=...``

退出码：`0` 成功；`1` 未指定标的；`2` 不支持的标的；`3` 接口异常；`10` 未登录。

**银行 code → uniqueCode 映射：**

| 银行 code | uniqueCode | 说明 |
|-----------|-----------|------|
| CMBC | CMBC-JCJ | 民生银行积存金 |
| CZB | CZB-JCJ | 浙商银行积存金 |
| CIB | CIB-JCJ0 | 兴业银行积存金（买入价） |
| CGB | CGB-JCJ0 | 广发银行积存金（买入价） |
| ICBC | ICBC-JCJ | 工商银行积存金 |
| CITIC | CNCB-JCJ | 中信银行积存金 |
| SPDB | SPDB-JCJ0 | 浦发银行积存金（买入价） |

## 持仓/收益查询（当前登录账号）

```bash
cd ${SKILL_DIR}/scripts
python3 holdings_entry.py --parse "{用户原文}" --wait-login
python3 holdings_entry.py --resume
python3 jos.py holdings --wait-login
```

> **`--wait-login` 语义说明**：当检测到未登录时，脚本会自动发起登录流程（调用 `jos.py login-auto`）并**阻塞等待**用户在浏览器完成授权。这不违反"禁止自动轮询 exchange"规则——脚本等待的是本地回调信号（同机模式）或用户手动确认（沙箱模式），而非主动调 exchange。用户确认后脚本自动续查持仓。

**底层**：``GET {BFF_BASE}/api/v1/holdings/query?accessToken=...``

退出码：`0` 成功；`10` 未登录；`11` 账号不匹配；`12` 意图未识别；`3` 接口异常。

## 早报查询（须登录）

```bash
cd ${SKILL_DIR}/scripts
python3 query_morning_report.py          # 格式化文本
python3 query_morning_report.py --json   # 原始 JSON
python3 jos.py morning-report
python3 jos.py morning-report --json
```

**底层**：``GET {BFF_BASE}/api/v1/morning-report/query?accessToken=...&pageSize=20``

退出码：`0` 成功；`10` 未登录；`3` 接口异常。

## 快讯 / 新闻 / 资讯查询（不需要登录）

无论用户说「查快讯 / 新闻 / 资讯」，统一走 `jdjr_query_news.py`，见下方「黄金资讯」章节。该脚本已内部合并快讯流（BFF `queryNewsFlash`）与京东金融公开资讯，去重后统一输出，不再区分数据源。

> 备注：`query_news_flash.py` / `jos.py news-flash` 仍保留为内部备选，但常规链路不再单独使用。



## 交易记录查询（须登录）

```bash
cd ${SKILL_DIR}/scripts
python3 query_trade_records.py                  # 格式化文本（汇总+列表）
python3 query_trade_records.py --json           # 原始 JSON
python3 query_trade_records.py --sum-only       # 仅查询汇总
python3 query_trade_records.py --list-only      # 仅查询订单列表
python3 query_trade_records.py --type BUY_GOLD  # 仅查询买入记录
python3 query_trade_records.py --type SELL_GOLD # 仅查询卖出记录
python3 query_trade_records.py --start-date 2026-06-01 --end-date 2026-06-20  # 按日期范围查询
python3 jos.py trade-records                    # 同上，通过jos子命令
python3 jos.py trade-records --json             # 原始 JSON
python3 jos.py trade-records --type BUY_GOLD    # 仅查询买入
```

**底层**：
- 列表：``POST {BFF_BASE}/api/v1/trade/list`` JSON body：``{accessToken, pageNo, pageSize, tradeTypeCodeList, orderCreateStartDate, orderCreateEndDate, ...}``
- 汇总：``POST {BFF_BASE}/api/v1/trade/sum`` JSON body 同上字段子集

**重要：数据完整性注意事项：**
- **必须传日期范围**（orderCreateStartDate + orderCreateEndDate），不传日期只返回近期少量数据
- 默认日期范围：2020-01-01 至当天（`DEFAULT_START_DATE`）
- 汇总接口包含退款/失败订单，数据不准确，**不使用**
- 改为从列表接口翻页获取全部订单，自行统计汇总
- **汇总只计成功订单**（状态为 COMPLETE 或 REDEEM_SUCC）
- 接口混有大量非GOLD订单（XJK/FUND等），需翻多页才能拿完全部GOLD订单
- 翻页终止条件：连续3页无新增GOLD订单时停止

退出码：`0` 成功；`3` 接口异常；`10` 未登录。

## 条件单查询（须登录）

```bash
cd ${SKILL_DIR}/scripts
python3 query_conditional_orders.py                  # 查询所有银行条件单（生效中）
python3 query_conditional_orders.py --json           # 原始 JSON
python3 query_conditional_orders.py --bank CMBC      # 指定银行
python3 query_conditional_orders.py --status 2       # 查询已触发的条件单
python3 query_conditional_orders.py --bank CZB --status 1  # 浙商生效中条件单
```

**底层**：
- 列表：``POST {BFF_BASE}/api/v1/conditional/list`` JSON body：``{accessToken, bankCode, jrid, statusList, pageIndex, pageSize, startTime, endTime}``
- 详情：``POST {BFF_BASE}/api/v1/conditional/detail`` JSON body：``{accessToken, bankCode, conditionalUuid, jrid}``

后端按 ``bankCode`` 路由到对应银行的条件单服务（民生 / 兴业 / 中信 / 浙商）。

**条件单状态：** 1=生效中、2=已触发、3=已失效、4=已取消、5=已完成

退出码：`0` 成功；`3` 接口异常/暂不可用；`10` 未登录。

## 浮动盈亏查询（须登录）

```bash
cd ${SKILL_DIR}/scripts
python3 query_income_calendar.py --mode unrealized-pnl          # 格式化文本
python3 query_income_calendar.py --mode unrealized-pnl --json   # 原始 JSON
```

**底层**：``POST {BFF_BASE}/api/v1/income-calendar/query`` JSON body：``{accessToken, calendarParam: {timeType, time, tradeType, bankCode?}}``

**金价策略：** 浮盈浮亏场景优先按银行维度查询精确金价（如 CMBC-JCJ），回退到默认金价（WG-JDAU），再回退到早报估算，均不可用则不展示浮盈浮亏。

退出码：`0` 成功；`3` 接口异常；`10` 未登录。

## 持仓诊断分析（须登录）

```bash
cd ${SKILL_DIR}/scripts
python3 query_income_calendar.py --mode analysis          # 格式化文本
python3 query_income_calendar.py --mode analysis --json   # 原始 JSON（去掉原始持仓数据）
```

**四维诊断框架：** 仓位占比 → 浮盈浮亏状态 → 集中度 → 场景匹配（6种场景）。
综合持仓 + 收益 + 金价（银行维度）+ 早报数据。

退出码：`0` 成功；`3` 接口异常；`10` 未登录。

## 登录

### 场景 A：本地环境（Agent 与浏览器同一台机器）

```bash
cd ${SKILL_DIR}/scripts
python3 jos.py login-auto   # 自动检测本地环境，唤起浏览器 + 启动本地回调服务
python3 jos.py token         # 验证 token 是否有效
```

本地环境下 `login-auto` 会：
1. 启动本地回调服务（`http://127.0.0.1:8765/callback`）
2. 自动唤起浏览器打开授权页

用户扫码完成授权后，京东回调本地服务，脚本**自动完成 exchange 兑换 token**。
Agent 应在后台轮询 `python3 jos.py token` 等待登录完成，**无需用户手动发送任何确认消息**。

```bash
# Agent 后台轮询示例（每 5 秒检查一次，最多 5 分钟）
for i in $(seq 1 60); do
  sleep 5
  python3 jos.py token 2>&1 && break
done
```

### 场景 B：远端沙箱环境（Agent 在沙箱，浏览器在用户本机）

> `--daemon` 在沙箱不可用（回调 `127.0.0.1` 无法到达沙箱）。用三步走，
> **用户无需复制任何 code**（authCode 不出后端）：

```bash
# 第 1 步：生成授权链接，发给用户在浏览器打开
python3 jos.py oauth-url

# 第 2 步：用户授权完成后回调页显示「已经登陆成功」，用户手动将此消息发送到对话框

# 第 3 步：Agent 收到用户确认消息后，兑换（自动读取第 1 步缓存的 state+verifier，无需 --code）
python3 jos.py exchange
```

沙箱模式下无本地回调服务，**必须等待用户手动发送确认消息后**才执行 exchange。
Agent **禁止**自动轮询 exchange，必须等到用户在对话框发送确认消息后才执行。

**底层（模拟 PKCE）**：第一步上送 challenge+state；兑换时仅上送 state+verifier
（``POST {网关}/auth/exchange``）。authCode 由后端在回调时获取，绝不回传客户端。

**异常处理：**
- 授权页 400 → 建议用户用**无痕模式**打开（浏览器 cookie 过多导致请求头超限）
- exchange 提示「授权尚未完成」→ 用户还没授权完，稍后重试 `exchange`
- exchange 提示「会话不存在或已过期」→ PKCE 会话超时（10 分钟），重新 `oauth-url`

Token 缓存：存入系统级加密存储（macOS Keychain / Windows DPAPI，服务名 `com.jd.jdgold`；其他平台回退 0o600 文件），由脚本自动管理，无需手动指定。旧版本的明文 `token.json` 会在首次读取时自动迁移并删除

## 京东金融公开数据模块（无需 OAuth）

> 以下四个模块走京东金融**公开数据接口 / apikey 网关**，**不经过 cf-gold-ai BFF，也不需要 OAuth token**。
> 脚本执行时 cwd 需在 `scripts/`（与 `jdjr_config.py` 同目录）。
> **所有脚本返回结果均带 `source.attribution` 字段（💡 本信息由 [京东金融](链接) 提供），转述给用户时必须原样保留结尾的这句来源标注与链接。**

### 黄金综合分析

```bash
cd ${SKILL_DIR}/scripts
python3 query_gold_analysis.py "{用户原始问句}"   # 脚本自动识别意图（实时行情/资金动向/交易机会/挂单簿/共振/综合概览）
```

**底层**：`POST {youqian.jd.com}/api/gateway`，header 携带 `apikey` / `x-skill-code` / `x-skill-run-id`（免 OAuth）。返回 `{success, data, source}`。

### 贵金属行情（黄金/白银/铂金）

```bash
cd ${SKILL_DIR}/scripts
python3 jdjr_query_gold.py Au99.99      # 黄金9999
python3 jdjr_query_gold.py Ag99.99      # 白银
python3 jdjr_query_gold.py Pt99.95      # 铂金
python3 jdjr_query_gold.py --list       # 列出支持的品种代码
```

**底层**：`POST ms.jr.jd.com/gw2/generic/ugActs/h5/m /queryStockData`，仅需 Content-Type（无鉴权）。此脚本产出实时行情表格。

### 贵金属历史走势 / K线（黄金/白银/铂金）

```bash
cd ${SKILL_DIR}/scripts
python3 jdjr_query_stock.py chart SGE-Au99.99 --days 15   # 黄金近15天走势（文字描述）
python3 jdjr_query_stock.py chart SGE-Ag99.99 --days 30   # 白银近30天走势
python3 jdjr_query_stock.py kline SGE-Au99.99 --k-type day    # 日K原始JSON
python3 jdjr_query_stock.py kline SGE-Au99.99 --k-type week   # 周K
python3 jdjr_query_stock.py kline SGE-Au99.99 --k-type month  # 月K
```

**底层**：`POST ms.jr.jd.com/gw2/generic/ugActs/h5/m /queryStockKLine`，仅需 Content-Type（无鉴权）。品种代码需带 `SGE-` 前缀。`chart` 产出文字走势描述并附来源标注；`kline` 输出原始 JSON 需二次格式化。仅对客暴露贵金属，不引导股票查询。

### 黄金大V排行

```bash
cd ${SKILL_DIR}/scripts
python3 query_blogger_trend.py "查看今日黄金大V排行"   # 默认黄金收益榜；支持人气/加仓/持仓榜
```

**底层**：`POST {youqian.jd.com}/api/gateway`，header 携带 `apikey`（免 OAuth）。返回排行榜 `rankings`（排名/昵称/克重/收益/粉丝等）。**转述须带风险提示 + 来源标注。**

### 黄金资讯 / 快讯 / 新闻

```bash
cd ${SKILL_DIR}/scripts
python3 jdjr_query_news.py "黄金" 3     # 关键词 + 条数
python3 jdjr_query_news.py "黄金" 3 --no-flash   # 仅资讯，不合并快讯
```

**底层**：`POST ms.jr.jd.com/gw2/generic/ugActs/h5/m /queryInformation`（无鉴权）+ BFF `queryNewsFlash`（快讯流，免登录），两源去重合并。返回 `{success, data:{keyword, count, news:[{time,title,content,url}]}, source}`。

## 参考

- [api-reference.md](api-reference.md)
- [holdings-api.md](holdings-api.md)
- [oauth-integration.md](oauth-integration.md)
- [conditional-order-api.md](conditional-order-api.md)

## 版本检查与升级

```bash
cd ${SKILL_DIR}/scripts
python3 upgrade.py check              # 检查是否有新版本（stdout=JSON）
python3 upgrade.py download           # 下载最新包到临时目录（stdout=JSON含path）
python3 upgrade.py apply <tar_path>   # 解压覆盖+验证（stdout=JSON）
python3 upgrade.py version            # 输出当前本地版本信息
```

退出码：`0` 成功/有新版本；`1` 网络错误；`2` SHA256校验失败；`3` 解压/文件操作失败；`4` 已是最新版本；`5` 参数错误/未配置。

**check 输出格式（stdout JSON）：**
```json
{
  "need_upgrade": true,
  "current_version": "1.1.1",
  "latest_version": "1.2.0",
  "changelog_summary": "...",
  "breaking_changes": false,
  "upgrade_notice": "",
  "package_size": 245760,
  "released_at": "2026-07-15T10:00:00+08:00",
  "code": 0
}
```

**download 输出格式（stdout JSON）：**
```json
{
  "status": "downloaded",
  "path": "/tmp/jdgold-upgrade-xxx/jdgold-1.2.0.tar.gz",
  "version": "1.2.0",
  "sha256": "...",
  "size_bytes": 245760,
  "code": 0
}
```

**apply 输出格式（stdout JSON）：**
```json
{
  "status": "upgraded",
  "previous_version": "1.1.1",
  "current_version": "1.2.0",
  "code": 0
}
```
