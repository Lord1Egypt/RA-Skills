# Kerrystock 经验教训与踩坑记录（Lessons Learned）

本文件汇总 Kerrystock 从 0 到 1 构建、并实测验证（601138 工业富联、sz161725 白酒LOF）过程中
踩过的坑、修正过的口径、以及可复用的流程纪律。**每次迭代本技能前先读一遍。**

---

## 一、数据源与运行环境（最易重蹈覆辙）

1. **westock-data 是 Node CLI，不是 HTTP API**。
   入口 `scripts/index.js`，用 managed node 跑。命令如 `kline/technical/disclosure`。
   路径默认写死 app bundle；现已改为由 `scripts/common.py` 自动探测，或用环境变量 `WESTOCK_DATA_SCRIPT` 覆盖。

2. **kline 输出是 Markdown 表，不是 JSON**。`last` 列 = 收盘价（不是 `close`）。
   解析规则：按 `|` 分隔 → 跳过头行 + `---` 分隔行 → 列序 `date|open|last|high|low|volume...`。
   ❌ 不要假设它能返回 JSON。

3. **kline 单笔查询上限约 2000 条** → 上市久的标的（如 601138 八年日线 ~1970 行）会触顶。
   ✅ 必须按日期分段（每段约 2 年）循环导出再合并。`export_kline.py` 已封装此逻辑。

4. **运行环境固定**：
   - Node：`~/.workbuddy/binaries/node/versions/<ver>/bin/node`（managed，脚本自动探测；可用 `NODE_BIN` 覆盖）
   - Python 依赖（pandas/numpy）：venv `~/.workbuddy/binaries/python/envs/default`
   - 没有 venv 时先 `python3 -m venv` 再 `pip install pandas numpy`。

5. **外部 builtin 路径不要写死在调用处**：用环境变量 `WESTOCK_DATA_SCRIPT` / `WB_FINANCE_QUANT_DIR` /
   `NEODATA_SCRIPT` / `NODE_BIN` 覆盖；未设置时由 `scripts/common.py` 自动探测常见 WorkBuddy 安装位置。
   保证技能可迁移、可复现，且不泄漏本机路径。

---

## 二、neodata 凭证（重大坑，已封装进 neodata_verify.py）

6. **`--save-token` 在只读/沙盒环境下写入失败**（app bundle 不可写）。
   ✅ 改用 `--token <token>` 直传（见 `scripts/neodata_verify.py`）。

7. **token 必须先用 `connect_cloud_service` 工具获取**，有效期约 24h；每次新会话要重新取。
   流程：调用 `connect_cloud_service` → 拿到 token → 传给 `neodata_verify.py --token`。

8. **neodata 返回是自然语言摘要**，区间涨跌幅要主动追问具体数值，例如：
   "自 2018 上市以来每一年度 1–12 月涨跌幅" 才能拿到可量化字段，否则只有定性描述。

---

## 三、seasonality 信号引擎（核心认知坑）

9. **严禁直接套用 `seasonality.py` 的 A股默认 bullish/bearish 月份**
   （默认 `[1,2,3,11,12]` 多 / `[5,6,7,8,9]` 空）。这是全市场通用经验，**不等于单只标的的真实规律**。
   ✅ `seasonal_analysis.py` 强制用标的自身历史重算做多/回避月。

10. **判定规则（必须胜率与均值同向才采纳）**：
    - 做多：胜率 ≥ 0.55 **且** 均值 > 0
    - 回避：胜率 ≤ 0.45 **且** 均值 < 0
    - ⚠️ 均值高但胜率低（如 2/3 月"少数大年拉高均值、中位数为负"）**不算做多信号**。

11. **强趋势 / 强基本面标的日历效应弱**（典型：工业富联这类 AI 龙头）。
    须以「业绩 + 趋势 + 事件」为主、日历规律为辅。这是本次最大的认知修正——
    601138 的月收益高度由 AI 景气周期驱动，6/12 月做多信号是叠加在产业趋势上的，不可孤立使用。

12. **样本数少的月份置信度低**：`n ≤ 3` 的结论须在报告显式标注 `n`，不可当作可靠规律。

---

## 四、技术指标自算（口径一致性坑）

13. **技术指标（MACD/KDJ/RSI/BOLL）一律脚本内按标准公式自算**，
    不解析第三方 markdown 输出 → 可复现、不依赖输出格式变动。`gen_report.py` 已实现。

14. **BOLL 标准差必须用总体口径 `ddof=0`**（与通达信/同花顺等行情软件一致）。
    ❌ 用样本口径 `ddof=1` 会算出 56.76，而正确值应为 57.04（与 westock 一致）。
    这是具体踩坑修正，已写入 `gen_report.py`。

15. **净值 CSV 缺 OHLC 的降级兼容**：缺 `open/high/low` 自动用 `close` 填充、`volume` 补 0；
    KDJ 高低用 close 近似。保证场外基金（仅净值）也能跑通步骤3/4。

---

## 五、ETF / 基金适配

16. **场内 ETF / LOF 的 K 线格式与股票完全一致**（含 open/high/low/last/volume），
    核心算法无需改，只补代码归一化。

17. **代码归一化**：纯数字自动补前缀（沪 5/6/9→`sh`、深 0/1/2/3→`sz`），歧义用 `--market sh|sz` 覆盖。
    例：`161725`→`sz161725`、`510300`→`sh510300`。

18. **LOF 场内历史可能远短于其净值历史**（如 `sz161725` 场内价仅回溯到 2021）。
    需长历史时用 neodata 净值模式（场外基金模式）补长序列。

19. **基金日历效应 ≈ 所跟踪标的的季节性**（白酒LOF≈白酒板块、沪深300ETF≈大盘），
    结论须结合跟踪标的基本面解读，不可孤立看净值波动。

---

## 六、流程纪律（保证技能靠谱）

20. **先实测再改**：改脚本前先用 `westock kline` 拉样本确认输出格式，绝不凭猜测硬编码。

21. **端到端用已知标的验证**：用 601138 跑通后，结论须与手动分析一致才算通过；
    并用 BOLL 下轨等已知值对齐口径（57.04 对齐）。

22. **技能须自包含 + 参数化**：外部依赖路径可覆盖、阈值（`--win`/`--lose`）可调、
    报告标签（`--label`）可切换，避免把假设写死。

23. **中国配色铁律**：涨=红、跌=绿（与欧美相反）；买卖"窗口"用绿、"回避窗口"用红，
    报告内加图例避免混淆。所有输出带风险提示。

---

## 七、已知局限（须在报告中坦诚告知用户）

- 季节性是**统计规律非因果**，历史上成立的月份未来未必重复（尤其产业逻辑切换时）。
- 场内 LOF/ETF 历史长度受数据源限制，早期样本少。
- 本技能不预测、不荐股；输出为「分析框架 + 历史统计」，非投资建议。
