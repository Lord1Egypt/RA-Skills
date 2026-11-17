# gold-silver-daily-report

> **黄金白银行情日报 Skill for WorkBuddy / OpenClaw / CodeBuddy**
> 一键生成结构化的「黄金 + 白银每日行情日报」交互式 HTML 研报，固定十节增强模板：**结论前置 + 三图仪表盘 + 多空矛盾 + 机构目标价 + 风险提醒**。方法论来自两周真实迭代验证。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-blue)](https://github.com/tusu168/gold-silver-daily-report)

---

## 📸 示例截图

下图由本 Skill 于 **2026-07-22** 生成：顶部为简明结论与 5 条固定风险提示（金边高亮），紧随其后的是「核心图表仪表盘」—— 黄金人民币单价 / 黄金美元单价 / 金银比近半年走势，三张 ECharts 折线图一次看清。

![黄金白银行情日报示例](./assets/preview.png)

> 想看交互效果？将生成的 HTML 用浏览器打开即可缩放、悬停查看数据点。

---

## 📋 目录

- [它能做什么](#-它能做什么)
- [核心特性](#-核心特性)
- [报告结构](#-报告结构)
- [快速开始](#-快速开始)
- [安装](#-安装)
- [数据铁律](#-数据铁律)
- [数据源](#-数据源)
- [目录结构](#-目录结构)
- [自定义与二次开发](#-自定义与二次开发)
- [上架到 WorkBuddy 推荐市场](#-上架到-workbuddy-推荐市场)
- [常见问题](#-常见问题)
- [许可证](#-许可证)

---

## ✅ 它能做什么

- **联网检索当日真实行情**：国际现货黄金/白银、国内 Au T+D / Ag T+D / 沪金沪银主力、宏观指标（DXY / 10Y 美债 / 10Y TIPS / USD/CNY / WTI / Brent / CME FedWatch）、央行购金、机构目标价、金银比。
- **按固定模板渲染 HTML**：统一一份、无"原日报/模板新增/增强版"等来源标注，专业可直接阅读或二次分发。
- **三图仪表盘**：近 90 交易日黄金人民币单价（沪金主力连续）+ 近 90 交易日黄金美元单价（COMEX）+ 近半年金银比，均带 dataZoom 缩放与最高/最低标记。
- **本地化生成**：默认写出 `黄金白银日报-YYYY-MM-DD.html`，不依赖任何云盘/飞书账号。

> **设计取舍**：本 Skill **不含飞书/云盘上传步骤**。研报生成后，分发由你自己的工具链处理，保持 Skill 最小可用、可移植。

---

## 🚀 核心特性

| 特性 | 说明 |
|------|------|
| **结论前置** | 报告开头即给结论、5 条风险提示与免责声明，适合快速决策。 |
| **三图仪表盘** | 沪金人民币单价、COMEX 美元单价、金银比半年走势，核心走势一张屏内看完。 |
| **真实金银比半年序列** | 不是只有当日/近几日点，而是重建近半年（约 1/21–当日）序列，含均值线与当前线。 |
| **机构目标价标注下调** | 六家主要投行目标价表，明确标注"是否已下调"及幅度。 |
| **反向传导链解释** | 优先用「地缘 → 油价 → 通胀 → 加息 → 实际利率↑ → 金银跌」解释地缘冲突下的反直觉下跌。 |
| **光伏去银化工业逻辑** | 白银分析必讲银包铜/电镀铜对单瓦耗银 −30%~50% 的影响。 |
| **涨红跌绿** | 遵循中国习惯配色。 |

---

## 📑 报告结构

1. 标题 + 日期 + 数据截止时间
2. **简明结论与风险提示（速览）** — 金边高亮；结论段 + 固定 5 条风险 + 免责声明
3. **核心图表仪表盘** — ① 黄金人民币单价 ② 黄金美元单价 ③ 金银比近半年
4. 一、核心数据一览（国际现货）
5. 二、国内 T+D 与期货价格
6. 三、关键比率与宏观指标
7. 四、金银比（大数字 + 半年最低/均值/最高；图表已在仪表盘）
8. 五、黄金走势关键驱动因素（TIPS / 美元 / 央行购金 / 地缘反向链）
9. 六、白银走势特征（金银比视角 / 光伏去银化 / 结论）
10. 七、近期核心矛盾（利多 vs 利空）
11. 八、主流机构最新目标价
12. 九、后续关键指标与价位（事件日历 + 支撑阻力）

---

## ⚡ 快速开始

### 方式 A：在 WorkBuddy 对话中直接使用

安装 Skill 后，重启会话，直接说：

```text
生成今天的黄金白银行情日报
来一份贵金属每日速览
做一份黄金白银 HTML 研报
```

WorkBuddy 会自动加载本 Skill，联网检索当日数据并生成 HTML。

### 方式 B：用脚本本地渲染（可复现、可集成）

1. 联网检索当日数据，整理成 JSON（字段格式参考 `example_data.json`）。
2. 生成金银比近半年序列片段：

   ```bash
   python3 scripts/build_gsr_series.py --current 69.6 --end-date 7/22
   # 或提供真实检索序列：--json gsr_input.json
   ```

   把输出填入数据 JSON 的 `gsr_script` 字段。

3. 渲染最终 HTML：

   ```bash
   python3 scripts/generate_report.py \
     --data your_data.json \
     --template assets/report_template.html \
     --out 黄金白银日报-2026-07-22.html
   ```

详细字段说明见 `references/template_spec.md`，数据源说明见 `references/data_sources.md`。

---

## 📦 安装

WorkBuddy 在以下路径自动识别 Skill：

| 范围 | 路径 |
|------|------|
| 用户级（跨你所有项目） | `~/.workbuddy/skills/gold-silver-daily-report/` |
| 项目级（仓库协作者共享） | `<项目>/.workbuddy/skills/gold-silver-daily-report/` |

### 从 GitHub 克隆

```bash
# 用户级
 git clone https://github.com/tusu168/gold-silver-daily-report.git ~/.workbuddy/skills/gold-silver-daily-report

# 项目级（随仓库提交，团队共享）
git clone https://github.com/tusu168/gold-silver-daily-report.git .workbuddy/skills/gold-silver-daily-report
```

克隆后重启 WorkBuddy 会话即可生效。

---

## 🛡️ 数据铁律

- 必须联网检索当日真实行情，不得捏造；注明盘面（亚盘盘中 / COMEX 收盘）。
- 人民币折算价 ≠ 国内 T+D，两者并列：

  ```
  元/克 = 美元/盎司 × USD/CNY 汇率 ÷ 31.1035
  ```

- **10Y TIPS 实际收益率**是金价「核心压制变量」，必查必列。
- 优先用「地缘 → 油价 → 通胀 → 加息 → 实际利率↑ → 金银跌」反向传导链解释行情。
- 机构目标价必标注是否已下调及幅度。
- 白银分析必讲「光伏去银化」工业逻辑（单瓦耗银 −30%~50%，2026 光伏用银 −10%~19%）。
- 风险提示固定 5 条：政策超预期 / 地缘反复 / 白银高波动 / 国内流动性 / 数据噪声。
- 涨红跌绿（中国习惯）；金 `#e8c547` / 深蓝 `#1a1a2e`。

---

## 🌐 数据源

| 维度 | 推荐来源 |
|------|----------|
| 国际现货黄金/白银 | 金投网、金十数据、财联社、同花顺、tradingeconomics |
| 国内 T+D / 期货 | 上海黄金交易所、金投网、Wind |
| 沪金主力连续（人民币/克） | 新浪财经期货历史接口 `InnerFuturesNewService.getDailyKLine?symbol=AU0` |
| COMEX 黄金（美元/盎司） | westock `data_kline` code=`fuGC` |
| 宏观（DXY / 美债 / TIPS / 原油 / FedWatch） | 金投外汇、同花顺、华尔街见闻、CME FedWatch、FRED |
| 央行购金 | 中国人民银行月度储备、WGC 央行调研 |
| 金银比半年序列 | T-GolDream / IndexMundi 真实月度/日度值 + 关键极值周度重建，详见 `references/data_sources.md` |

> ⚠️ 避坑：stooq / Yahoo Finance / macrotrends 等对外站普遍有 JS 反爬 / 限流，curl 直连拿不到干净数据，请勿依赖。

---

## 🗂️ 目录结构

```
gold-silver-daily-report/
├── SKILL.md                    # 触发条件 + 完整生成流程 + 数据铁律
├── README.md                   # 本文件
├── LICENSE                     # MIT 许可证
├── example_data.json           # 当日数据 JSON 格式范例
├── assets/
│   ├── preview.png             # 示例截图（README 展示用）
│   └── report_template.html    # HTML 骨架（CSS + 三图仪表盘 + 十节占位符）
├── scripts/
│   ├── build_gsr_series.py     # 生成金银比近半年序列 <script> 片段
│   └── generate_report.py      # 用当日数据 JSON 渲染最终 HTML
└── references/
    ├── template_spec.md        # 十节模板逐节要素与措辞规范
    └── data_sources.md         # 各维度数据源与口径（含 GSR 半年重建法）
```

---

## 🔧 自定义与二次开发

- **改模板**：编辑 `assets/report_template.html`，调整 CSS 配色或增减占位符。
- **改数据字段**：更新 `example_data.json` 与 `scripts/generate_report.py` 的占位替换逻辑（当前为大小写不敏感的 `{{KEY}}`）。
- **改金银比重建逻辑**：编辑 `scripts/build_gsr_series.py` 与 `references/data_sources.md`。
- **接入自己的分发**：在 `scripts/generate_report.py` 渲染后增加上传/推送步骤（本仓库默认不写死任何云盘）。

---

## 🛒 上架到 WorkBuddy 推荐市场

本 Skill 已上架/准备上架至 **ClawHub**（WorkBuddy 推荐市场）：

1. 打开 [clawhub.ai](https://clawhub.ai/)。
2. 使用 GitHub 账号登录。
3. 点击「发布技能」。
4. 输入本仓库地址：

   ```
   https://github.com/tusu168/gold-silver-daily-report
   ```

   或上传打包好的 ZIP（见 [Releases](https://github.com/tusu168/gold-silver-daily-report/releases)）。
5. 填写名称、描述、标签，并上传 `assets/preview.png` 作为封面/截图。
6. 提交审核，通常 1–3 个工作日通过。

上架后，其他 WorkBuddy / OpenClaw / CodeBuddy 用户即可在推荐市场搜索「黄金白银日报」一键安装。

---

## ❓ 常见问题

**Q：生成的报告为什么是一张 HTML？**  
A：自包含 HTML 便于本地查看、邮件发送、飞书/钉钉上传或嵌入任何页面，不依赖外部服务器。

**Q：ECharts 图表能离线使用吗？**  
A：当前模板通过 CDN 加载 ECharts，联网时渲染效果最佳。若需纯离线，可下载 `echarts.min.js` 放到 `assets/` 并修改模板引用。

**Q：可以把报告自动发到飞书吗？**  
A：本 Skill 刻意不做上传，以保持最小依赖。你可以在 `generate_report.py` 渲染后追加自己的上传逻辑，或在 WorkBuddy 对话里再说"把这份 HTML 上传到飞书"。

**Q：和 `precious-metal-trend-analysis` 有什么区别？**  
A：`precious-metal-trend-analysis` 是早期 7 节趋势分析版本；`gold-silver-daily-report` 是**当前维护版本**，采用固定十节日报模板 + 结论前置 + 三图仪表盘。

---

## 📄 许可证

[MIT](./LICENSE) — 自由使用、修改、分发。
