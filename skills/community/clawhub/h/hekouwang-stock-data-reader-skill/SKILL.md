---
name: hekouwang-stock-data-reader-skill
slug: hekouwang-stock-data-reader-skill
displayName: 个股公开数据速读（A股 · akshare）
summary: A-share stock data reader / akshare pipeline — fund flow, LHB seats, financials to compliance-safe recap charts. Not investment advice.
license: MIT-0
homepage: https://github.com/huiyonghkw/hekouwang-stock-data-reader-skill
version: 1.2.7
description: "A 股个股公开数据速读：akshare 拉资金流/估值/财务并出中立复盘图文，守不荐股合规护栏；贴图仅用本地字体与系统字体"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
metadata:
  openclaw:
    homepage: https://github.com/huiyonghkw/hekouwang-stock-data-reader-skill
    requires:
      bins:
        - python3
        - node
    envVars:
      - name: STOCK_REPORT_BRAND
        required: false
        description: 贴图页脚署名；留空则不渲染品牌行
      - name: STOCK_REPORT_HANDLE
        required: false
        description: 贴图页脚账号；留空则不渲染账号行
      - name: CHROME_PATH
        required: false
        description: 覆盖默认 Chrome/Chromium 可执行文件路径
      - name: STOCK_REPORT_THEME
        required: false
        description: 贴图主题 v2 或 v3
---

# 个股公开数据速读 · Skill

把一个股票代码，变成一份「机构观感、但合规中立」的公开数据复盘。是工厂 B 财经栏目「3 天一只」的发动机，也是可对外售卖的工具。

**核心价值（差异化）**：借鉴 `daily_stock_analysis` 的多源数据层思路，但走第三条路——① 挖**资金博弈内核**（主力拉高出货 / 龙虎榜席位 / 北向 / 分部毛利），不是新闻级价格+财报摘要；② **合规护栏内置**（不荐股/不预测/风险条），是唯一能「公开发布且不踩金融红线」的个股分析产出器；③ **数据→可发布图文一条龙**（出版级贴图/长文/头条），不是丢一堆 JSON。详见 README「核心价值」。

## 0. 合规第一（必先读 `references/compliance.md`）
- **不荐股、不预测、不给买卖点**；每份报告文末固定风险提示条。
- 个股内容主走**公众号/头条**；**小红书可发"中立复盘/算账/名词科普"形态**（守合规护栏、零站外导流、别用资金流/席位当钩子），详见 `references/compliance.md`。
- 命中红线（买入/卖出/目标价/翻倍/上车…）→ 停下改写。

## 1. 三步工作流

**先确认再跑**：取数会联网访问第三方行情源（akshare → 东方财富 / 新浪 / 乐咕），并在输出目录写 CSV/JSON/HTML/PNG。开跑前向用户确认「股票代码 + 输出目录」，输出目录只用本 skill 的 `out/` 或用户指定的专用目录。

首次或换机：`bash scripts/bootstrap.sh` → `python3 scripts/fetch.py --probe` 确认 akshare 可连。

```
python3 scripts/fetch.py <代码> [out目录]     # 取数 → out/<代码>/*.csv + _report.json
python3 scripts/analyze.py out/<代码>          # 算指标 → out/<代码>/analysis.json（含龙虎榜买卖对称度）
python3 scripts/build_report.py out/<代码> [--brand 署名 --handle @账号]   # 出贴图初稿（数字已对）
node templates/screenshot.js <贴图目录> [--clean]   # 截图到 output/；默认保留 HTML，--clean 才删
```
- 页脚署名默认关闭；用 `--brand/--handle` 或 `STOCK_REPORT_BRAND/STOCK_REPORT_HANDLE` 才渲染。
- 截图器用参数数组调 Chrome（不拼 shell），不关沙箱；Chrome 路径可用 `CHROME_PATH` 覆盖。
`build_report.py` 出的是**数字正确的初稿**；中立复盘文案由人/LLM 按 `references/report-structure.md` 润色后再截图交付。

## 2. 指标体系（栏目固定，见 report-structure.md）
价格/市值/估值轨迹 · 主力资金进出（含"涨着出货"类反差日）· 龙虎榜席位结构（通道盘 vs 机构长线）· 利润质量（净利 vs 经营现金流）· 利润结构（分部收入 vs 毛利占比）· 资产负债 · 风险线索。

## 3. 数据源与踩坑
- akshare（乐咕估值 / 东方财富资金流·龙虎榜 / sina 财报·日K）。免费、无需 key。
- 日K走 sina 源（`stock_zh_a_daily`）避开 eastmoney `push2his`（受限网络常被挡）。
- `fetch.py` 已清代理环境变量兜底；筹码 `stock_cyq_em` 在受限网络可能拿不到（非核心）。
- 营销号数字常错，一律以 akshare 财报/乐咕口径为准。

## 4. 视觉与产出
- 默认 **V2 米白**（黏土主色），财经可选 V3 Google 财经风。字体统一黑体。
- 贴图复用「会勇禾口王内容工厂」流水线（`_build.py` + `screenshot.js`）。
- 字体优先用本机 `hekouwang-content-factory/assets/fonts/`（Anthropic Sans/Mono + 思源黑体）；截图 HTML 只走本地 `@font-face` / 系统字体，不拉第三方字体资源。

## 5. 加一只新股（3 天一期）
1. `python3 scripts/fetch.py <新代码>`
2. `python3 scripts/analyze.py out/<新代码>`
3. 复制 scripts/build_report.py 到选题目录，按 analysis.json 出初稿 → 润色 → 截图。
4. 套合规框架，发公众号 + 头条；建 `发布记录.md` 回填数据。

## 6. 文件
- `scripts/bootstrap.sh` — 一键 venv + 装依赖
- `scripts/fetch.py` — 取数引擎（`--probe` 探针）
- `scripts/analyze.py` — 指标计算 → analysis.json（含龙虎榜对称度）
- `scripts/build_report.py` — 据指标出 8 贴图初稿（V2 米白）
- `templates/screenshot.js` — 1080×1350 @2x 截图（`--clean` 才删 HTML）
- `references/compliance.md` — 金融合规护栏（先读）
- `references/lhb-symmetry.md` — 龙虎榜买卖对称度解读护栏
- `references/title-checklist.md` — 标题/封面合规自检
- `references/report-structure.md` — 栏目固定报告结构
- `requirements.txt` — akshare + pandas（精确版本 pin）

## 7. 案例
首版样例：利通电子 603629（`Pi.dev/利通电子/litong-0619/`，公众号长文+8贴图、头条三件套）。
