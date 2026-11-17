---
name: money-never-sleep
version: 0.6.0
description: |
  MNS (Money Never Sleeps) CLI operations manual for autonomous agents. Tracks an investment
  portfolio in a local ledger, reads market sentiment (CNN Fear & Greed Index), and generates
  target-weight rebalancing suggestions. Use when the user asks to view holdings, record a
  trade they already executed, generate a daily strategy report, inspect or tune strategy
  parameters, or run a backtest.

  CRITICAL: MNS connects to NO broker and executes NO trades. `mns buy` / `mns sell` are
  bookkeeping entries that record trades the human has ALREADY executed elsewhere. Never call
  them to "act on" a suggestion — doing so silently corrupts every downstream number.

  Triggers: "查看持仓", "记录买入", "记录卖出", "生成策略报告", "调仓建议", "再平衡",
  "恐贪指数", "更新价格", "现金余额", "交易历史", "回测策略", "调整策略参数", "MNS"
license: MIT
compatibility: Single static binary (Rust). No runtime dependencies.
metadata:
  {
    "openclaw":
      {
        "source": "https://github.com/sopaco/money-never-sleep",
        "homepage": "https://github.com/sopaco/money-never-sleep",
        "author": "Sopaco",
        "os": ["darwin", "linux", "win32"]
      }
  }
---

# MNS 操作手册（面向 Agent）

## 0. 先读这三条硬约束

**① `mns buy` / `mns sell` 是记账，不是下单。**
MNS 不连接任何券商。这两个命令的唯一用途是把**用户已经在券商完成的**交易登记进本地账本。

- ✅ 用户说"我刚买了 100 份 QQQ，成交价 450" → `mns buy QQQ 100 450`
- ❌ `mns report` 建议买入 ¥2000 → **不要**据此调用 `mns buy`

记入一笔并未真实发生的交易，会同时污染现金余额、成本价、持有天数、收益率和后续所有调仓建议，且没有撤销命令。**不确定用户是否真的成交过，就先问。**

**② 建议不是投资建议。**
`mns report` 的输出是规则引擎的机械计算结果。向用户转述时要说明它来自什么规则，不要包装成推荐意见，也不要替用户做买卖决定。用户自己的判断和持牌顾问才是决策来源。

**③ 数字只能来自命令输出。**
不要凭记忆或推算填写价格、份额、收益率。拿不到数据就说拿不到——不要编。

---

## 1. 安装与可用性检查

**执行任何操作前，先判断 `mns` 是否已安装可用，不要重复安装。**

```bash
mns --version
```

- 输出正常版本号 → 已安装，直接跳到第 2 节使用即可。
- 报 `command not found` / 找不到命令 → 执行下方安装步骤。

**通过 npm 安装**（会按当前系统自动拉取对应平台的预编译二进制，支持 macOS Apple Silicon / Linux x64 / Windows x64）：

```bash
npm install -g @never-sleeps/mns-cli
```

安装完成后重新执行 `mns --version` 复核。若已执行过安装且 `mns --version` 仍失败，说明是 PATH 未生效或当前平台/架构暂无预编译包，直接向用户反馈原因即可，**不要**反复重跑安装命令。

---

## 2. 命令速查（语法已逐条实测）

| 命令 | 作用 | 备注 |
|---|---|---|
| `mns init` | 初始化配置与数据库 | **会清空既有数据**，有确认提示；`--force` 跳过确认 |
| `mns cash` | 查看现金余额 | |
| `mns cash set <金额>` | 设为指定余额 | 覆盖式 |
| `mns cash add <金额>` | 增加现金（注资） | 金额须为正 |
| `mns portfolio` | 持仓概览（份额/成本/现价/市值/收益） | 只读，最常用 |
| `mns add <代码> <名称> <类别>` | 把标的加入持仓池（份额为0） | 类别只能是 `us_stocks` / `cn_stocks` / `counter_cyclical` |
| `mns buy <代码> <份额> <价格>` | **登记**已成交买入 | 现金不足会报错；须先 `add` |
| `mns sell <代码> <份额> <价格>` | **登记**已成交卖出 | 份额超出持有量会报错 |
| `mns price <代码> [价格]` | 省略价格=查看；带价格=手工更新 | |
| `mns update-prices` | 自动抓取全部持仓现价 | 需要网络；单个失败会跳过并继续 |
| `mns remove <代码>` | 从持仓池删除标的 | 不可逆，先与用户确认 |
| `mns sentiment` | 当前恐贪指数 | 需要网络 |
| `mns report` | 生成今日调仓报告并存盘 | 需要网络；同时写入 `reports/YYYY-MM-DD.txt` |
| `mns history [条数]` | 交易历史，默认 20 条 | **位置参数**，不是 `--limit` |
| `mns config` | 打印全部配置 | |
| `mns config <键>` | 读单项 | 必须是完整叶子键 |
| `mns config <键> <值>` | 改单项 | 校验不通过则拒绝写入，原配置不变 |
| `mns backtest` | 四种策略对比回测 | 纯离线，不碰账本 |
| `mns backtest validate` | 样本外验证 + 收益分布 | `--iterations` / `--block` 可调 |
| `mns backtest params` | 列出可调参数及默认值 | 忘记键名时先跑这个 |
| `mns market` / `mns market-indices` / `mns analyze <代码>` | 全球指数 / 个股报价 | 依赖 Yahoo，**部分网络环境不可用**，见 §7 |

数据位置：配置 `~/.mns/config.toml`，账本 `~/.mns/mns.db`，报告 `./reports/`。

---

## 3. Agent 需要理解的最小策略模型

不需要了解内部实现，只需理解这一句：**策略回答的是"现在应该持有多少"，而不是"现在该花掉多少钱"。**

1. 恐贪指数落入某个情绪区间 → 得出**风险资产目标总权重**（越恐慌越高）
2. 该权重按资产配置比例拆到三条腿（美股/A股/逆周期）
3. 每条腿把**实际权重**与**目标权重**比较
4. 偏离超过**偏离带**（默认 4 个百分点）才建议动作，且只补到目标为止
5. 偏离在带内 → **不动作，这是正常状态**

默认目标权重曲线（`mns config target_weight.*` 可调）：

| 情绪 | 指数范围 | 风险资产目标权重 |
|---|---|---|
| 极度恐慌 | < 30 | 85% |
| 恐慌 | 30–45 | 75% |
| 中性 | 45–55 | 60% |
| 贪婪 | 55–70 | 45% |
| 极度贪婪 | ≥ 70 | 35% |

两条 agent 容易误判的规则：

- **"今日无需调仓"是健康输出，不是故障。** 中长线框架下多数月份都不该有动作。不要因为没有建议就反复重跑，也不要去调窄偏离带来"制造"建议。
- **卖出有最短持有天数限制**（默认 30 天）。报告可能显示"需减仓但持仓未满 N 天"，这是刻意规避国内基金惩罚性赎回费，不是 bug。

---

## 4. 标准工作流

### 4.1 每日/每周例行

```bash
mns update-prices   # 先刷新价格，否则报告基于过期价格
mns report          # 生成调仓报告
```

向用户汇报时应包含：当前恐贪指数与区间、风险资产目标 vs 实际权重、每条腿的建议动作（或不动作的原因）、净操作方向。若某腿建议为"不动作"，把原因一并说明。

### 4.2 用户已成交，登记入账

```bash
# 用户："我在券商买了 300 份 018966，成交价 1.52"
mns buy 018966 300 1.52
mns portfolio            # 复核登记结果
```

登记前确认三件事：标的是否已 `add` 过、份额与价格是否为**实际成交值**（不是建议值）、现金余额是否够（不够会报错）。

### 4.3 新增标的建仓

```bash
mns add 518880 "黄金ETF华安" counter_cyclical   # 先入池
mns buy 518880 1000 8.38                        # 再登记已成交买入
```

### 4.4 参数调整

```bash
mns backtest params                    # 先查键名与默认值
mns config rebalance.band_pp           # 读当前值
mns config rebalance.band_pp 6         # 改（校验不通过会拒绝）
mns backtest                           # 改完跑回测看影响
```

改参数前先告知用户当前值和预期影响；参数变化会直接改变后续所有建议。

### 4.5 首次初始化（危险）

```bash
mns init            # 若已有数据会提示确认
mns cash set 100000
```

`mns init` 会**删除既有数据库**。只在用户明确要求全新开始时调用，且**永远不要**加 `--force`，除非用户明确说了"强制覆盖/不用问我"。

---

## 5. 如何读 `mns report` 的输出

报告固定含以下章节，可按 `【章节名】` 定位：

| 章节 | 内容 | agent 用法 |
|---|---|---|
| `【市场情绪】` | 恐贪指数 + 前日/周/月/年同比 | 判断情绪所处区间与变化方向 |
| `【账户概览】` | 现金、持仓市值、总资产、持仓明细表 | 核对账本状态 |
| `【调仓计划】` | 目标/当前/偏离 + 每腿建议，含标的级分摊 | **核心结论来源** |
| `【净操作指引】` | 净买入/净卖出/持仓不动 | 一句话总结 |
| `【目标仓位预案】` | 各情绪区间下的目标权重与对应金额 | 回答"如果继续跌该买多少" |
| `【信号口径】` | 当前由哪个信号驱动及其局限 | 转述结论时必须带上的限定 |

报告已同时写入 `reports/YYYY-MM-DD.txt`，需要复述历史结论时读文件，不要重跑（重跑会得到不同时点的指数）。

---

## 6. 转述效果时必须带上的限定

用户问"这个策略行不行"时，不要只报有利数字。仓库内经修正数据（真实全收益、计入交易成本与赎回费）的回测结论是：

- **买入持有在收益上领先**（年化约 14.6% vs 12.8%）。本工具不能宣称提高收益。
- 优势只在**风险调整后**成立：最大回撤约 10.9% vs 14.9%，Calmar 1.17 vs 0.98。
- **恐贪指数的边际贡献接近于零**——加入趋势锚后，带情绪倾斜与不带几乎无差别。
- **2000–2002、2008 等长期熊市未被数据覆盖**，而"熊市回撤保护"正是该策略的主要卖点，该卖点尚未经检验。
- 回测区间是美股强牛市 + 长期低利率，结论不应外推到其他环境。

跑 `mns backtest` / `mns backtest validate` 可复现上述数字。**不要**把回测年化当作对未来收益的预期转述给用户。

---

## 7. 故障模式与处理

| 现象 | 原因 | 处理 |
|---|---|---|
| `mns report` / `sentiment` 失败 | CNN 接口需要网络，且可能反爬返回 418 | 内置重试；仍失败则告知用户拿不到实时情绪，**不要**用旧指数假装是今天的 |
| `mns market` / `analyze` 全部失败，报 HTTP 403 | 部分网络环境完全拦截 Yahoo Finance | 属环境限制，非配置问题。告知用户需代理；`update-prices` 的**国内基金**部分仍可用 |
| `update-prices` 个别标的被跳过 | 该代码在数据源无对应数据（如特殊 QDII） | 用 `mns price <代码> <价格>` 手工补 |
| `Error: 现金余额不足` | 登记买入金额超过账面现金 | 多为漏记注资，先 `mns cash add`，或核对成交金额 |
| `Error: 卖出份额超出持有量` | 份额记错，或漏记了此前买入 | 用 `mns portfolio` / `mns history` 核对 |
| `Error: 未知的配置项: buy_ratio` | 只能读写完整叶子键 | 用 `mns config buy_ratio.extreme_fear`；或 `mns config` 看全量 |
| `Error: 情绪阈值必须满足单调递增` / `target_weight 必须随情绪升高而单调不增` | 参数值违反策略内在约束 | 校验已拒绝写入，原配置完好。按提示改成合法值 |
| 中文输出乱码（Windows） | PowerShell 默认 GBK | 切 UTF-8 终端，或重定向到文件再读 |
| 数据库被锁 | 多进程并发写 SQLite | **串行调用**，不要并发跑多个 mns 命令 |

错误一律以非零退出码 + `Error: <中文原因>` 形式返回，原因可直接转述给用户。

---

## 8. 常见错误用法（明确不要这么做）

| ❌ 错误 | ✅ 正确 |
|---|---|
| `mns history --limit 50` | `mns history 50`（位置参数） |
| `mns config buy_ratio` | `mns config buy_ratio.fear`（叶子键） |
| 看到建议就 `mns buy` 落账 | 只登记用户**实际已成交**的交易 |
| 报告无建议就反复重跑 | "不动作"是正常结论，直接如实汇报 |
| 为了产出建议而调窄 `band_pp` | 参数调整需用户同意，且要说明影响 |
| `mns init --force` 图省事 | 除用户明确授权外不加 `--force` |
| 并发跑多个 mns 命令 | 串行执行 |
| 把回测年化当预期收益转述 | 带上 §6 的全部限定 |

---

## 9. 快速自检

不确定环境是否可用时，按序执行（全部只读，不改数据）：

```bash
mns --version        # 二进制可用
mns config           # 配置可加载（旧配置缺新字段会自动取默认值）
mns portfolio        # 账本可读
mns sentiment        # 网络与 CNN 接口可用
mns backtest params  # 参数键名参考
```
