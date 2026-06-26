# PizzINT Monitor - 披萨指数监测表 v3.0

## 触发词
- 披萨指数
- PizzINT
- 五角大楼披萨
- Pentagon Pizza
- 军事情报
- 地缘紧张

## 功能
实时监测 PizzINT (Pentagon Pizza Index) 指数，生成地缘政治威胁报告。

## ⚠️ 重要限制
**pizzint.watch 是纯前端渲染（JavaScript 加载数据），curl / requests 无法获取实时数据。**

- **获取实时数据**：使用浏览器工具打开 pizzint.watch，截图或抓取 DOM
- **脚本用途**：数据解析 + 逻辑校验（当数据已获取时）
- **定时任务**：依赖浏览器工具在 isolated session 中运行

## 数据来源
- https://pizzint.watch/ - 实时披萨情报（需浏览器）

## 报告内容

### 1. 整体状态
- 系统状态、市场状态（美股开盘/闭盘）、监控店铺数

### 2. Nothing Ever Happens (NEH) 指数
| 指数区间 | 状态 | 说明 |
|----------|------|------|
| 0–30 | 🟢 Nothing Ever Happens | 平静期 |
| 30–65 | 🟡 Something Might Happen | 密切关注 |
| 65–99 | 🟠 Something is Happening | 高风险 |
| 99–100 | 🔴 It Happened | 重大事件 |

### 3. DOUGHCON 等级
| 等级 | 信号 |
|------|------|
| 1 | NORMAL - Baseline Activity |
| 2 | ELEVATED - Increased Orders |
| 3 | HIGH - Multiple Spikes |
| 4 | ⚠️ DOUBLE TAKE - Intelligence Watch |
| 5 | 🚨 CRISIS - Military Operation Imminent |

### 4. 披萨店异常活动
识别 SPIKE / Busier / Quieter 等异常状态

### 5. PolyPulse 双边威胁
- 🔴 CRITICAL: USA / IRAN
- 🟠 HIGH: RUS / UKR, USA / VEN
- 🟡 MODERATE/ELEVATED: USA / RUS, USA / CHN, CHN / TWN

### 6. Polymarket 预测市场（Breaking Ticker）

### 7. OSINT 动态摘要

## ⚠️ 逻辑校验要求
**输出报告前必须执行以下检查：**

1. **NEH 数值 vs 状态描述一致性**
   - NEH < 30 → 状态必须是 "Nothing Ever Happens"
   - 30 ≤ NEH < 65 → "Something Might Happen"
   - 65 ≤ NEH < 99 → "Something is Happening"
   - NEH ≥ 99 → "It Happened"
   - 描述与数值矛盾时，**以数值为准**，并在报告中明确指出矛盾

2. **阈值表述检查**
   - "NEH 超过阈值 X" 仅在 NEH > X 时使用
   - 数值比较必须用正确的符号（> / < / >= / <=）

3. **数据来源矛盾检查**
   - 同一数据源内出现矛盾时，指出并给出正确解读
   - 不要照搬原始报告的错误表述

4. **风险等级 × 描述一致性**
   - PolyPulse 风险等级必须与 GDELT 实际数值区间匹配

## 使用方式

### 浏览器获取（推荐，实时数据）
```bash
# 使用 browser 工具打开
open https://pizzint.watch/
# 然后 snapshot / screenshot 获取完整 DOM
```

### 脚本解析（已有数据时）
```bash
python3 pizzint.py
```

## 输出示例
生成包含以下内容的报告：
- 整体状态（系统/市场/监控店铺）
- NEH 指数 + 状态描述 + ⚠️ 逻辑校验结果
- DOUGHCON 等级
- 披萨店异常（SPIKE 店铺高亮）
- PolyPulse 双边威胁表
- Polymarket 预测市场（实时）
- 最新 OSINT 动态
- 逻辑校验警告（如有）

## 风险提示
⚠️ 披萨指数是 OSINT 开源情报工具，相关性≠因果性，仅供参考。
