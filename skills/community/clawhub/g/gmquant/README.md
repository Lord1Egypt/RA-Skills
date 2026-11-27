# 掘金量化 Skill — 自然语言策略引擎

> **用中文说话就能跑量化策略。** 告诉我你的交易想法，我帮你生成代码、执行回测、查看结果。

## 快速开始（3 步）

### 1️⃣ 准备环境

确保你的电脑已安装：

- [**掘金终端**](https://www.myquant.cn) — 打开并登录
- **Python 3.8+** — 安装 `gm` SDK 包：
  ```bash
  pip install gm
  ```

### 2️⃣ 设置 Token

获取方式：掘金终端 → 系统设置 → 密钥管理 → 复制 Token

然后告诉我："我的 token 是 `xxxxx`"，我会自动保存。

### 3️⃣ 用自然语言描述策略 + 提供 Strategy ID

直接说你想做什么，**同时告诉我你的策略 ID**：

> "帮我写个双均线策略：茅台和平安银行，5 日均线上穿 20 日均线买入，下穿卖出，回测最近一年。**策略 ID 叫 `ma_cross_v1`**"

> "写个动量策略：沪深 300 里选过去 20 天涨幅最大的 10 只等权买入，每月初调仓。**strategy_id 用 `momentum_top10`**"

> "查一下贵州茅台最近半年的日线收盘价"（纯查询不需要 strategy_id）

我会自动生成完整的可运行策略文件并帮你跑起来。

---

## 支持的策略类型

| 类型 | 示例描述 | 关键字 |
|------|---------|--------|
| **趋势跟踪** | "双均线金叉死叉" / "布林带突破" / "MACD 策略" | 均线、MA、MACD、布林带 |
| **动量/因子** | "选涨幅最大的 N 只" / "RSI 超卖买入" / "量价配合" | 动量、RSI、成交量、排名 |
| **均值回归** | "偏离均值太多就反向操作" / "网格交易" | 均值回归、网格、偏离 |
| **多因子选股** | "按 PE+ROE 选股" / "小市值+高成长" | 因子、筛选、排序 |
| **事件驱动** | "财报后买入" / "涨停板打板" | 财报、涨停、事件 |
| **纯数据查询** | "查行情" / "拉数据" / "看 K 线" | 查询、历史、行情 |

---

## 运行模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **回测 (Backtest)** | 用历史数据模拟交易 | 验证策略效果（默认） |
| **实盘/仿真 (Live)** | 连接实时行情和模拟账户 | 策略验证后上线运行 |

---

## 典型对话示例

### 示例 1：从零开始写策略

```
你: 写个双均线交叉策略，标的用贵州茅台，5日和20日均线。策略ID用 ma_cross_kweichow
我: [生成 strategy_ma.py，strategy_id='ma_cross_kweichow']
    策略已生成！参数如下：
    - 策略ID: ma_cross_kweichow ← 终端可查看绩效
    - 标的: SHSE.600519（贵州茅台）
    - 周期: 日线 1d
    - 信号: MA5上穿MA20买入 / 下穿卖出
    - 回测: 2024-01 ~ 2025-12, 初始资金100万

    要跑回测吗？
你: 跑吧
我: [自动调用 run_strategy.py --strategy-id ma_cross_kweichow 执行]
    回测完成！结果摘要：
    - 总收益: +23.5%
    - 年化收益: 18.2%
    - 最大回撤: -12.3%
    - 夏普比率: 1.45
    
    ✅ 已保存到掘金终端 → 打开 https://www.myquant.cn 查看完整绩效图表
```

### 示例 2：只查询数据

```
你: 查一下中芯国际最近30天的收盘价
我: [直接调用 API 返回 DataFrame]
    SZSE.002371 中芯国际 最近30日收盘价：
    日期          | 收盘价   | 涨跌幅
    2026-03-10    | 52.30    | +2.1%
    2026-03-11    | 51.80    | -0.96%
    ...
```

---

## 🆕 新增能力（v2.2）

### 持久化数据（gm ≥ 3.0.191）

策略状态不再"重启即失忆"。用 `persist_*` 系列把股票池、动态参数、持仓记录**落盘保存**，跨 bar、跨进程重启都能恢复。

```python
def init(context):
    persist_init('my_state', is_async=False)   # 回测/查询模式用 False

    # 首次运行创建，之后复用
    if persist_get('stock_pool') is None:
        persist_set('stock_pool', 'SHSE.600519,SZSE.000001')

    # 恢复上次运行留下的计数
    cnt = persist_get('bar_count')
    context.bar_count = int(cnt) if cnt else 0

def on_bar(context, bars):
    context.bar_count += 1
    persist_set('bar_count', str(context.bar_count))
```

| 函数 | 用途 |
|------|------|
| `persist_init(bucket, is_async)` | 初始化并绑定 bucket（一个运行周期只能绑 1 个） |
| `persist_set` / `persist_get` | 字符串读写 |
| `persist_set_obj` / `persist_get_obj` | dict / list 等 JSON 对象读写 |
| `persist_delete` / `persist_clear` | 删单个 key / 清空 bucket |
| `persist_delete_bucket` / `persist_get_all_buckets` / `persist_get_all_keys` | bucket 与 key 盘点 |

详见 `references/19-persist-data.md`。

### 基础指标新增自由流通股本

`stk_get_daily_basic` / `stk_get_daily_basic_pt` 新增两个字段：

| 字段 | 含义 | 量纲 |
|------|------|------|
| `free_shr` | 自由流通股本（剔除限售股和持股 5% 以上大股东） | 股 |
| `free_turnrate` | 自由流通换手率 = 成交量 ÷ 自由流通股本 × 100% | % |

**算自由流通市值要用 `free_shr × 上一交易日收盘价`：**

```python
d = stk_get_daily_basic(symbol='SHSE.600519', fields='tclose,free_shr',
                        start_date='2026-11-18', end_date='2026-11-26', df=True)
d = d.sort_values('trade_date').reset_index(drop=True)
d['free_mv'] = d['free_shr'] * d['tclose'].shift(1)   # shift(1) 避免未来函数
```

> ⚠️ `free_shr` 和 `ttl_shr_unl` 不是一回事。茅台实测：`ttl_shr_unl` 12.5 亿股，`free_shr` 6.25 亿股，差一倍。用错会显著高估市值。

---

## 文件结构

```
~/.workbuddy/skills/gm-quant/
├── SKILL.md                  # 技能主文件（AI 读取此文件理解如何工作）
├── README.md                 # 本文件 — 用户引导
├── TEST_REPORT.md            # API 测试报告
├── references/               # API 详细参考文档
│   ├── 01-quick-start.md
│   ├── 04-market-data.md
│   ├── 17-financial-data-fields.md
│   ├── 19-persist-data.md    # 🆕 持久化数据 API 全集
│   └── ...
└── scripts/
    ├── run_strategy.py            # ⭐ 策略一键运行器
    ├── test_all_apis.py           # API 全量测试脚本
    ├── test_account_apis.py       # 账户 API 策略环境测试
    ├── test_persist_apis.py       # 🆕 持久化 API 测试
    ├── test_daily_basic_free.py   # 🆕 自由流通股本字段测试
    ├── strategy_persist_demo.py   # 🆕 持久化策略示例
    └── check_import.py            # 导入检测
```

> 所有脚本从环境变量 `GM_TOKEN` 读取 token，不再硬编码。用法：`GM_TOKEN=xxx python scripts/test_persist_apis.py`

---

## ⭐ Strategy ID — 在掘金终端查看绩效分析

> **这是使用回测功能前必须填写的一步。**

### 什么是 Strategy ID？

`strategy_id` 是你的策略在**掘金终端**中的唯一标识名。每次运行策略时传入它，回测结果会**持久化保存**到终端后台。

### 填写后你能看到什么？

登录 [掘金量化终端](https://www.myquant.cn) → **策略列表** → 找到你的策略 → 点击查看：

| 绩效分析内容 | 说明 |
|-------------|------|
| 📈 **收益曲线** | 策略净值 vs 基准对比 |
| 📉 **回撤分析** | 最大回撤、回撤持续时间 |
| 📊 **风险指标** | 夏普比率、年化收益、波动率 |
| 💰 **交易明细** | 每笔买入/卖出记录 |
| 🎯 **持仓快照** | 每日持仓变化 |

### 如何提供？

在描述策略时顺便告诉我，例如：

```
你: 写个双均线策略，标的茅台。策略ID用 ma_cross_kweichow
我: [生成代码，自动填入 strategy_id='ma_cross_kweichow']
    回测完成！打开掘金终端 → 策略列表 → ma_cross_kweichow → 查看绩效图表
```

如果你没提供，**我会主动问你**，不会偷偷跳过。

---

## 注意事项

- **掘金终端必须保持打开** — 所有 API 调用都通过终端通信
- **Token 不要泄露给他人** — 相当于你的账号密码
- **回测不等于实盘** — 回测结果仅供参考，实盘需考虑滑点、流动性等因素
- **A 股 T+1** — 当天买入的股票当天不能卖出
