---
name: "Stock Monitor - 股票监控"
description: 对持仓做一次性检查：盈亏、涨跌、缺口、均线与 RSI 等（无常驻进程，可配阈值与状态文件）。当用户说：帮我检查一下持仓要不要告警？我的 ETF 今天触发止损了吗？或类似持仓体检问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🛎️", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY", "JISU_STOCK_MONITOR_STATE"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据持仓监控（jisu-stock-monitor）

基于 [股票查询 API](https://www.jisuapi.com/api/stock/) 与 [股票历史行情 API](https://www.jisuapi.com/api/stockhistory/)，对本地 JSON 配置的持仓列表执行 **`check`**，输出 JSON 结果与触发说明。

**免责声明：仅供技术学习与信息整理，不构成投资建议；行情与指标可能存在延迟或误差，请自行核实。**


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"
# 可选：默认状态文件路径（当请求体未写 state_file 时）
export JISU_STOCK_MONITOR_STATE="/path/to/jisu-stock-monitor.state.json"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
# 可选：默认状态文件（当请求体未写 state_file 时）
$env:JISU_STOCK_MONITOR_STATE="C:\path\to\jisu-stock-monitor.state.json"
```

依赖：`pip install requests`。Windows 下若无 `python3` 命令，可改用 `py -3` 或 `python`。

## 脚本路径

文档与示例统一写作 **`skills/jisu-stock-monitor/monitor.py`**。若你克隆的仓库目录实际是 **`skill/`**，请把命令里的 `skills/` 换成 **`skill/`**。

## 使用方式

### check（持仓检查）

```bash
python3 skills/jisu-stock-monitor/monitor.py check @skills/jisu-stock-monitor/config.example.json
```

也可传入内联 JSON，或从标准输入：

```bash
python3 skills/jisu-stock-monitor/monitor.py check '{"holdings":[{"code":"300917","cost":10,"alerts":{}}]}'
echo '{"holdings":[...]}' | python3 skills/jisu-stock-monitor/monitor.py check -
```

### 请求体字段（根级）

| 字段 | 类型 | 说明 |
|------|------|------|
| holdings | array | **必填**，每项见下表 |
| history_days | int | 可选，拉取历史 K 线的日历跨度（30–365），默认 90 |
| state_file | string / null | 状态文件路径（跨日止盈峰值、告警冷却）。`null`/`false`/空字符串 表示禁用 |
| alert_cooldown_minutes | int | 可选，同一标的同一 `rule` 在多少分钟内只报一次（0 表示关闭）。>0 且未配置 `state_file` 且未设环境变量时，会默认使用当前目录下 `jisu-stock-monitor.state.json` |

单只持仓 `holdings[]`：

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 股票代码，必填 |
| name | string | 可选，缺省用接口返回名称 |
| cost | number | 可选，成本价；用于成本盈亏% 与动态止盈 |
| type | string | 可选，影响**默认**日内涨跌幅阈值：`individual` 个股 ±4%（默认）、`etf` ±2%、`gold` / `au` / `commodity` ±2.5% |
| state_key | string | 可选，状态文件里跟踪峰值/冷却的主键，默认等于 `code`（同一账户多策略时可区分） |
| alerts | object | 可选，规则见下 |

`alerts` 中可选规则（未配置则跳过对应检查；**日内涨跌幅**在未显式关闭时使用上表 `type` 对应默认阈值）：

| 键 | 说明 |
|----|------|
| cost_pct_above / cost_pct_below | 相对成本盈利/亏损达到阈值（%）时告警，如 +15 / -12 |
| change_pct_above / change_pct_below | 日内涨跌幅阈值（%）；若设为 JSON `false` 可关闭该侧默认阈值 |
| ma_monitor | `true` 时根据日线收盘计算 MA5/MA10，检测上一交易日相对再前一日的金叉/死叉 |
| volume_surge | 放量：例如 `2` 表示最后一根日线成交量 ≥ 近 5 日均量 × 2 |
| volume_shrink | 缩量：例如 `0.5` 表示最后一根日线成交量 ≤ 近 5 日均量 × 0.5 |
| gap_monitor | `true` 时用 `stock/detail` 的今开、昨收计算**开盘跳空%** |
| gap_up_pct / gap_down_pct | 可选，向上/向下开盘跳空阈值（%），默认分别为 `1` 与 `-1` |
| gap_true_monitor | `true` 时用日线**昨日高/低**与**当日 detail 高/低**判断**真缺口**（今日低 > 昨日高 / 今日高 < 昨日低） |
| gap_true_min_pct | 可选，缺口体幅度（占昨高或昨低的%）下限，过滤微小缺口；不设则只要满足真缺口形态即告警 |
| dynamic_trailing | 对象，见下表「动态止盈」 |
| rsi_monitor | `true` 时计算简化 RSI(14)，并结合 rsi_overbought / rsi_oversold（默认 70 / 30） |

**动态止盈** `dynamic_trailing`：

| 子字段 | 默认 | 说明 |
|--------|------|------|
| enable | true | 设为 `false` 可关闭 |
| persist | true | 在配置了 `state_file`（或环境变量路径）时，将**跟踪高点**写入状态文件，实现**跨日**峰值；为 `false` 时仅用当前接口一次快照中的价高（跨 run 不记忆） |
| min_peak_profit_pct | 10 | 相对成本，跟踪高点达到的盈利% ≥ 此值才参与回撤判断 |
| drawdown_warn_pct | 5 | 自跟踪高点回撤 ≥ 此% 触发 `dynamic_trailing_warn` |
| drawdown_urgent_pct | 10 | 自跟踪高点回撤 ≥ 此% 触发 `dynamic_trailing_urgent`（与上一档互斥，优先更严） |

**告警冷却**：`alert_cooldown_minutes` > 0 时，每条触发的 `rule` 在冷却期内重复满足条件不会出现在 `triggers` 中，而记入该标的的 `suppressed_by_cooldown`（便于排查「为何没响」）。

需要历史 K 线时才会请求 `stockhistory/query`；**仅成本、日内、开盘跳空、动态止盈（且未开真缺口）**时可能只调 `stock/detail`。

### 成功时 JSON 顶层（便于代理解析）

- **`ok`**：整体是否成功执行脚本逻辑  
- **`checked_at`**：检查日期（ISO 日期字符串）  
- **`summary`**：`holdings`、`trigger_events`、`warning_level_events`、`suppressed_by_cooldown`、`state_file`、`alert_cooldown_minutes` 等汇总  
- **`results`**：数组，每项对应一只标的，含 **`triggers`**、**`suppressed_by_cooldown`**、**`indicators`**、**`ok`** / **`error`**

### 常见错误返回（节选）

| 情况 | 说明 |
|------|------|
| `missing_credential` | 未设置 `JISU_API_KEY` |
| `missing_param` | 未提供非空 `holdings` |
| `state_save_failed` | 状态文件目录不可写等 |
| 单条 `results[].ok: false` | 该代码 `stock/detail` 请求失败，见 `error` 字段 |

非零退出码表示参数错误、凭据缺失或状态写入失败；成功时 stdout 为一整段 JSON。

**提示**：含**成本**的 JSON、**状态文件**路径勿提交公开仓库，建议写入 **`.gitignore`**。

`.gitignore` 示例（按你的实际目录调整）：

```gitignore
# jisu-stock-monitor 本地配置与状态
skill/jisu-stock-monitor/*.state.json
skill/jisu-stock-monitor/config*.local.json
```

## 推荐用法

1. 用户说「跑持仓监控」「有没有触发预警」「检查这几只票」等，且已有或愿意让你维护一份 **JSON 配置**（可参考 `config.example.json`）时。
2. 确认环境已设 **`JISU_API_KEY`**，再执行一次：`python3 skills/jisu-stock-monitor/monitor.py check @<配置文件.json>`（或内联 JSON / 管道 `check -`）；**不要**为本技能启动后台常驻进程。
3. 从打印的 JSON 中取 **`summary`**、每条 **`results[].triggers`**；若有 **`suppressed_by_cooldown`**，说明「规则仍满足，但在冷却期内未重复播报」。
4. 用自然语言归纳触发的标的、**`rule`** 与 **`message`**，并复述本技能**免责声明**；不得把输出杜撰为买卖建议或新闻结论。
5. 仅需现价/列表 → 用 **jisu-stock**；要更长周期 K 线 → **stockhistory**；要新闻/舆情 → **news-cn**（或其它新闻技能），再与本技能的告警结果分开呈现。

### 用户侧提示词模板（可复制）

把下面整段发给代理，按需改掉括号里的内容即可：

```text
帮我用 jisu-stock-monitor 监控这几只股票：（股票名称或代码一）、（股票名称或代码二）……
持仓成本分别为（成本1）、（成本2）……（与上面顺序一一对应；没有成本的标的请说明「只监控不设成本」）。

请根据极速数据可用的 6 位代码生成或更新 JSON 配置（可参考 skills/jisu-stock-monitor/config.example.json），需要的话加上 state_file 与 alert_cooldown_minutes；
然后执行：python3 skills/jisu-stock-monitor/monitor.py check @（配置文件路径）

把输出里的 summary、各标的 triggers 用中文说明清楚；若有 suppressed_by_cooldown 也要解释；最后提醒非投资建议。
```

**示例（填好后的样子）：**

```text
帮我监控一下宁德时代、比亚迪这两个票，持仓成本分别为 402、98。请生成配置并跑一遍 jisu-stock-monitor 的 check，把有没有触发规则用中文告诉我，并带免责声明。
```

## 与单项技能的关系

- 实时行情字段与 **jisu-stock**（`stock/detail`）一致。
- 均线、放量/缩量、RSI、真缺口依赖 **stockhistory** 同源日线数据。

## 相关链接

- ClawHub 本技能：<https://clawhub.ai/jisuapi/jisu-stock-monitor>
- 股票 API：<https://www.jisuapi.com/api/stock/>
- 历史行情 API：<https://www.jisuapi.com/api/stockhistory/>
- 极速数据官网：<https://www.jisuapi.com/>

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

