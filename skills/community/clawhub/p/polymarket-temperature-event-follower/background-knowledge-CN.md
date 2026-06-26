# Background Knowledge: SkillPay Billing & Weather Event Trading

**本文档阐述 sniper.py 的设计哲学、气象学原理与工程实现之间的权衡**

---

## 目录

1. [为什么是下午两点？——气象学原理](#1)
2. [交易什么？——天气事件市场的本质](#2)
3. [系统执行流程详解](#3)
4. [时间窗口的技术考量](#4)
5. [余额与计费：分离的艺术](#5)
6. [异常处理哲学](#6)
7. [实战建议与监控](#7)

---

<a name="1"></a>
## 1. 为什么是下午两点？——气象学原理

### 1.1 日射加热的物理过程

地球表面接收太阳辐射的能量，不是instantaneously（瞬时）转化为气温。这个过程遵循：

```
太阳辐射 → 地表吸收 → 热传导/对流 → 气温上升
```

**关键延迟**：
- **热惯性**：地表（尤其是土壤、水体）需要时间升温
- **热量积累**：能量在低层大气中累积
- **辐射平衡**：地表在入射辐射>出射辐射时净增热

### 1.2 日气温变化的典型曲线

```
温度
  ↑
  |               /\
  |              /  \
  |    ________/    \________
  |   /                       \
  |  /                         \
  | /                           \
  +------------------------------→ 时间
    00:00   06:00   12:00   18:00
```

- **最低温**：日出前后（05:00-07:00，取决于季节和地理位置）
- **升温期**：上午快速升温（08:00-13:00）
- **最高温**：**13:00-15:00（下午1-3点）** ← 你的策略核心
- **降温期**：下午到夜间缓慢降温

### 1.3 为什么最高温在下午两点（而不是正午）？

**直观错误认知**："正午太阳最高，所以最热"

**实际物理机制**：

```
时间   太阳高度角  入射辐射  地表温度  气温
06:00  低         弱       冷       冷
12:00  最高       最强     温       温（仍在升）
14:00  高         强       高       最高（热惯性峰值）
15:00  中         中       最高     开始降
```

**关键因素**：
1. **能量净积累**：从日出到正午，地表持续净吸热（辐射收入>支出）
2. **热惯量延迟**：大气温度滞后于地表温度约1-2小时
3. **热容量效应**：空气和地表的比热容需要时间传递热量

> 📊 **数据参考**：在中国大部分地区，最高气温出现在14:00-15:00的概率超过75%，极端情况下可延迟至16:00。

### 1.4 季节与地理修正

- **夏季**：延迟更长（可达3小时），最高温可能16:00
- **冬季**：延迟短，最高温可能13:00-14:00
- **沿海 vs 内陆**：沿海地区因海洋调节，最高温可能更早
- **海拔**：高原地区紫外线强但空气稀薄，升温/降温更快

**你的策略假设**：在50个主要城市（CITY_SLUGS），最高温稳定出现在14:00-15:00。

---

<a name="2"></a>
## 2. 交易什么？——天气事件市场的本质

### 2.1 Polymarket Weather Events

Polymarket 是去中心化的预测市场平台。你交易的合约类型：

```
市场问题："Will the high temperature in Tokyo on March 26, 2026 exceed 75°F?"
Yes token: 如果超过75°F，价格为1.0（否则0）
No token: 如果不超过75°F，价格为1.0（否则0）
```

**关键参数**：
- `token_id`: YES token 的唯一标识（用于买入）
- `no_token_id`: NO token 的唯一标识（用于sell-side计算）
- `best_ask`: YES token 的最低卖价（例如 $0.53 表示市场认为53%概率）
- `market_id`: 市场唯一ID

### 2.2 你的交易逻辑

**核心假设**：最高温预测在上午仍有不确定性，但到下午基本确定。

**你的策略**：
1. **扫描窗口**：10:00-14:00（监控期）
2. **触发条件**：城市的"今日"或"明日"日期，YES token价格在某个阈值（如<0.6）
3. **下单**：用固定金额（`TRADE_AMOUNT_USD=1.0`）买入YES token
4. **预期**：价格随气温确定而上涨→低价买入→高价卖出（或持有至结算）

**风险**：
- 如果气温不达预期，token 价值归零
- Polymarket 流动性风险
- 网络/API 失败

---

<a name="3"></a>
## 3. 系统执行流程详解

### 3.1 主循环：`scan_cycle()`

```
┌─────────────────────────────────────────────────────┐
│ scan_cycle(api_client)                              │
├─────────────────────────────────────────────────────┤
│ 1. 余额预检 (SKILLPAY)                              │
│    if balance < MIN_CHARGE_AMOUNT: return           │
│                                                     │
│ 2. 扫描市场 (scan_and_find_trades)                  │
│    - 遍历50个城市+2天日期 = 100个组合               │
│    - 获取订单簿、预测气温、gamma价格                │
│    - 计算：是否可交易（价格<max(0.6, gamma)）      │
│                                                     │
│ 3. 监控窗口过滤                                     │
│    is_in_monitor_window(city, date)                 │
│    - 今日：10:00-14:00（在官方预测发布后）          │
│    - 明日：全天（市场已开）                         │
│                                                     │
│ 4. 循环下单 (for cand in window_candidates)        │
│    - 检查是否已有仓位（每个城市每天只能1个）        │
│    - 【实时余额检查】防止中途耗尽                   │
│    - execute_buy_order(...)                         │
│    - 成功→保存仓位、记录交易                        │
│    - 失败→跳过继续下一个                           │
│                                                     │
│ 5. Fallback 阶段（10:00-10:04）                     │
│    - 为未开仓的城市（今日）执行fallback            │
│    - 选择概率最高的候选（mid_price最大）           │
│    - 同样每次前检查余额                             │
│                                                     │
│ 6. 保存状态                                        │
└─────────────────────────────────────────────────────┘
```

### 3.2 下单函数：`execute_buy_order()`

```
execute_buy_order(token_id, price, max_price, dry_run, ...)

├── dry_run=True → 只打印，不调用API
├── price > max_price → 滑点保护exit
├── 初始化 ClobClient（L2认证）
│
├── 尝试下单（retries循环）
│   ├── client.create_order() → 签名
│   ├── client.post_order() → 上链
│   │   SUCCESS → 返回order_id
│   │   FAIL → 捕获异常，重试/exit
│
├── 计费调用（订单成功后）
│   └── try:
│         billing_charge(user_id)  # → 扣0.01 USDT
│         if ok: print success
│         else: print warning + payment_url
│       except Exception as e:
│         print warning (ignore)
│
└── 返回order_result字典
```

**核心约束**：
- 计费在 `post_order` 之后 → 保证"成功下单才扣钱"
- 计费异常不抛出 → 避免订单回滚（已上链）

### 3.3 预检 vs 实时检查

| 阶段 | 位置 | 目的 | 频率 |
|------|------|------|------|
| **扫描前预检** | scan_cycle 开头 | 快速拒绝明显不足的余额 | 1次/scan |
| **下单前检查** | window_candidates 循环内 | 防止多单耗尽 | 每次下单前 |
| **Fallback检查** | fallback 循环内 | 同上 | 每次fallback前 |

**设计原理**：
- 预检是"快速失败"，避免浪费API调用
- 实时检查是"硬约束"，确保每单都有足够余额
- 两者结合：既优化性能，又保证正确性

---

<a name="4"></a>
## 4. 时间窗口的技术考量

### 4.1 监控窗口（Monitor Window）

```python
def is_in_monitor_window(city: str, date_obj: date) -> bool:
    now = datetime.now(timezone.utc) + timedelta(hours=8)  # UTC+8
    date_str = date_obj.strftime("%Y-%m-%d")

    # 今日：预测发布后才交易
    if date_str == today:
        window = WINDOW_TIMES[city]["today"]
        start = datetime.strptime(f"{today} {window['start']}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{today} {window['end']}", "%Y-%m-%d %H:%M")
        return start <= now <= end
    # 明日：全天
    else:
        return True
```

**窗口时间定义**（推测，基于天气预测发布时间）：

| 城市 | 今日窗口 | 原因 |
|------|----------|------|
| 东京、首尔、新加坡 | 10:00-14:00 | 日本气象厅/JMA每日08:00发布预报，市场反应需要时间 |
| 伦敦、巴黎、法兰克福 | 09:00-15:00 | 欧洲中央气象组织09:00更新 |
| 纽约、芝加哥、洛杉矶 | 08:00-14:00 | NWS 早上发布 |
| 悉尼、墨尔本 | 23:00-03:00（次日）| 时差导致 |

**你的当前配置**：`WINDOW_TIMES` 未显示在代码中，但推测每个城市的开市/预测发布时间不同。

### 4.2 Fallback 窗口：为什么是 10:00-10:04？

```
Fallback触发条件：
  - is_fallback_time(city, today_str) 返回 True
  - 且该城市今日尚未开仓

时间判断逻辑（sniper.py:is_fallback_time）：
  当前时间在 10:00-10:04（含）之间 → 执行fallback
```

**设计意图**：
1. **最后机会**：10:00后市场流动性充足，且离14:00最高温只剩4小时
2. **避免重复**：每个城市每天只能fallback一次（`fallback_executed`集合）
3. **稳定性**：4分钟窗口保证所有城市在这个时段都检查到，不会漏掉
4. **避开开盘拥挤**：9:30-10:00可能有大量订单，10:00后市场稳定

**为什么不更晚**？
- 14:00气温已基本确定，交易价值降低
- 需要时间让仓位产生收益（虽然持有到结算也是一样）

---

<a name="5"></a>
## 5. 余额与计费：分离的艺术

### 5.1 设计约束

- **下单 ≠ 计费成功**
- 订单上链后不可撤销
- 计费API可能失败（网络、余额、SkillPay服务器）

### 5.2 原始问题

**场景**：
```
用户余额 = 0.01 USDT
触发5个城市（5笔交易）
预检：balance >= 0.01 → 通过
循环：
  第1单：下单成功，计费成功 → balance = 0
  第2单：下单成功，计费失败（余额不足）→ 只警告
  第3-5单：同样计费失败
结果：用户付出5次Gas费，但只收到1次有效计费
风险：用户损失5次交易成本，SkillPay只收到0.01
```

### 5.3 解决方案：每次下单前实时检查

**修复后流程**：

```
预检：balance = 0.01 → 通过

for cand in window_candidates:
    # 下单前检查
    balance = billing_get_balance(user_id)
    if balance < 0.01:
        break  # 停止循环
    execute_buy_order():
        order success
        billing_charge(user_id)  # 可能失败但订单已成
```

**效果**：
- 第1单后 balance = 0 → 第2单前检查发现 < 0.01 → break
- 避免无效订单和Gas浪费
- 保护用户利益

### 5.4 为什么不在 `execute_buy_order` 内部补救？

```python
# 错误方案：在计费失败后回滚订单（不可能）
order_result = await execute_buy_order(...)  # 已上链
bill = billing_charge(user_id)
if not bill['ok']:
    cancel_order(order_result['order_id'])  # ❌ 订单已成交，无法cancel
```

**为什么不能取消**：
- `OrderType.GTC`（Good Till Cancel）需要主动发送cancel请求
- 成交的订单无法取消，只能等市场结算
- 回滚在区块链上是非原子操作，需要额外的复杂逻辑

**正确方案**：事前检查，而非事后补救

---

<a name="6"></a>
## 6. 异常处理哲学

### 6.1 分级处理

| 异常类型 | 来源 | 处理方式 | 影响 |
|----------|------|----------|------|
| 预检余额不足 | SkillPay API | `return` 跳过本轮扫描 | 不执行任何交易 |
| 下单价格超限 | 本地检查 | `return None` | 该城市跳过，继续下一个 |
| Polymarket API 错误 | `ClobClient` | 重试（最多 `MAX_RETRIES`） | 暂时失败，可能成功 |
| 下单后计费失败 | SkillPay API | print warning + payment_url | **订单仍成功** |
| 计费网络异常 | `requests` 超时 | try-except捕获，print warning | **订单仍成功** |
| 余额查询异常 | SkillPay API | try-except捕获，print警告后继续 | 继续下一个城市（风险：可能余额不足） |

### 6.2 核心原则

**"订单成功是成功，计费失败是警告"**

```python
try:
    order = post_order()  # 关键路径
    billing_charge()      # 非关键路径
except BillingError:
    log_warning()         # 继续，不throw
```

**哲学**：
- 用户下单是首要目标
- 计费失败是运营问题，不应惩罚用户
- 记录日志和显示充值链接，让用户事后处理

### 6.3 Fallback 的异常处理

Fallback 循环中同样有余额检查，如果异常则 `break`：

```python
if not self.dry_run and SKILLPAY_USER_ID:
    try:
        balance = billing_get_balance(SKILLPAY_USER_ID)
        if balance < MIN_CHARGE_AMOUNT:
            print("[ERROR] 余额不足，停止fallback剩余下单")
            break
    except Exception as e:
        print(f"[WARN] 余额检查失败（{e}），继续...")
        # 不break，继续尝试下单（因为无法知道余额，只能赌）
```

**为什么"失败继续"？**
- 余额API偶尔超时，不应因此错过所有fallback机会
- 成本已经发生（预检已过），值得尝试

---

<a name="7"></a>
## 7. 实战建议与监控

### 7.1 需要监控的关键指标

| 指标 | 位置 | 正常范围 | 警报阈值 |
|------|------|----------|----------|
| `scan_cycle` 耗时 | 日志 | < 60秒 | > 120秒 |
| 每笔订单计费成功率 | billing_charge 返回值 ok=True | > 99% | < 95% |
| 余额不足导致的break次数 | "[ERROR] 余额不足" 日志 | 0次/天 | 任何 > 0 |
| Fallback执行次数 | "[FALLBACK]" 日志 | ≤ 城市数量 | 异常多（可能策略失效） |
| `billing_get_balance` 异常率 | "[WARN] 余额检查失败" | < 1% | > 5% |

### 7.2 SkillPay 充值策略

**当前配置**：
- 每次下单扣费：`0.01 USDT`（固定）
- 最低充值额度：`8 USDT`（见于 `payment_link` 调用）

**建议**：
1. **初始充值**：至少 `0.01 × 最大并发单数 × 2`，例如最大5单 → `0.1 USDT`，建议 `0.5 USDT` 避免频繁充值
2. **报警**：余额低于 `0.05 USDT` 时发邮件/Telegram提醒
3. **自动充值**（可选）：监控 `payment_url` 输出，自动打开浏览器充值

### 7.3 日志分析示例

```bash
# 统计失败的计费
grep "Billing failed" sniper.log | wc -l

# 查看余额不足导致的停止
grep "余额不足" sniper.log

# 统计fallback效果
grep "FALLBACK" sniper.log | grep -v "Skipping" | wc -l
```

### 7.4 部署最佳实践

**环境变量**（`.env`）：
```bash
SKILLPAY_USER_ID=your_wallet_address
SKILL_BILLING_API_KEY=sk_live_xxxxx
SKILL_ID=e56f2a83-819c-4e43-a457-5442ebba0098
POLY_API_KEY=...
PRIVATE_KEY=0x...
PROXY_WALLET=0x...
TRADE_AMOUNT_USD=1.0
```

**运行方式**：
```bash
# 生产环境（建议screen/tmux）
python sniper.py --dry-run=False

# 测试环境
python sniper.py --dry-run=True
```

**版本控制**：
- 保留 `state.json`（持仓、交易历史）
- 定期备份到S3/云存储
- Git commit时排除 `.env` 和 `state.json`

---

## 附录：术语表

| 术语 | 解释 |
|------|------|
| **最高温** | 当日气温峰值，通常出现在14:00-15:00 |
| **YES token** | 事件发生的预测权证，价格=市场概率 |
| **best_ask** | 最低卖价（买家需接受的价格） |
| **滑点容差** | `SLIPPAGE_TOLERANCE`，例如5% → max_price = best_ask × 1.05 |
| **dry_run** | 模拟模式，不下单、不扣费，用于测试 |
| **fallback** | 在10:00-10:04为未开仓城市强行下单，确保每个城市都有仓位 |
| **MIN_CHARGE_AMOUNT** | 最小预检余额（0.01 USDT），保证至少能扣一次费 |
| **MAX_RETRIES** | 下单重试次数（默认3） |
| **L2凭证** | Polymarket 二级认证（API key + secret + passphrase） |

---

## 总结

本系统的设计哲学：

1. **气象学驱动**：利用"最高温在下午两点"的确定性，在10:00-14:00窗口密集扫描
2. **防御性编程**：每次下单前检查余额，避免中途耗尽
3. **订单优先**：下单成功是硬目标，计费失败是软问题
4. **时间敏感**：时间窗口严格，fallback作为最后4分钟的机会
5. **可观测性**：所有关键步骤都有日志输出，便于事后分析

理解这些背景知识，有助于：
- 调整参数（如窗口时间）适应不同城市的季节变化
- 诊断问题（计费失败、订单滑点、余额突变）
- 优化策略（增加/减少并发单数、调整fallback策略）

祝交易顺利！🎯
