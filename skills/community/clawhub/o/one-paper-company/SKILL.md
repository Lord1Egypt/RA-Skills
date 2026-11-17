---
name: "one-paper-company"
slug: "one-paper-company"
displayName: "One Paper Company 一个公司一张纸"
description: "把任意公司做成一张可分享、可离线、可打印的深度研究 HTML 单页。10 步滚动联动 + 15 类数据可视化 + ECharts 内联 + 像素风品牌动画。可选能力：抓取公司行情/财务数据（用户触发时）、写入本地 HTML 产物（用户指定路径）。"
version: "2.0.0"
license: "MIT"
summary: "单公司深度研究 → 自包含 HTML 产物（周期复盘 scrollytelling + 15 类图表）"
allowed-tools: "Read, Write, Edit, Glob, Grep, LS, RunCommand, WebSearch, WebFetch, AskUserQuestion"
metadata:
  openclaw:
    skillKey: "one-paper-company"
    emoji: "📄"
    homepage: "https://github.com/EdwardWason/one-paper-company"
    os: ["windows", "macos", "linux"]
    requires:
      bins: ["python"]
      env: []
    primaryEnv: ""
    envVars: []
    always: false
---

# 一个公司一张纸

> **当前状态（v2.0.0）**：仅周期复盘形态可用 ✅；速览卡/估值地图/竞争格局为路线图 🔲

把任意公司做成一张可分享、可离线、可打印的深度研究 HTML 单页。基于英伟达 2026Q3 scrollytelling 复盘页 1:1 逆向抽离。

---

## 权限声明

**本技能的行为范围（用户须知）**：

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ✅ | WebSearch 抓取公司行情/财务/事件数据；WebFetch 抓取公司 IR 页面；可通过"不触发 Phase A 数据抓取"关闭 |
| 文件读写 | ✅ | 读 data.json + 模板；写入用户指定 output.html 路径；默认输出到桌面，可通过 `--output` 指定；不读取用户 memory/profile |
| 环境变量 | ❌ | 不读取任何凭证环境变量 |
| subprocess | ✅ | 调用 `python scripts/build_html.py` 和 `python scripts/validate.py` |
| 外部 API | ❌ | 不调用任何外部 API（行情数据通过 mx-xuangu / mx-zixuan skill 间接获取） |

**第三方库声明**：本技能内联使用 [ECharts 5.5.0](https://echarts.apache.org/) (Apache 2.0) 第三方库（1MB，压缩代码含 `eval(`/`exec(` 字面量，属正常压缩代码特征，非真实危险调用）。

---

## 触发词

### 主入口（3 个变体）

| 触发词 | 行为 |
|---|---|
| **「一个公司一张纸」** | 进入技能，列出 4 种产物形态让用户选 |
| **「一公司一纸」** / **「公司一张纸」** | 同上 |

### 形态直达（4 种产物形态）

| 形态 | 触发词 | 产物 | 状态 |
|---|---|---|---|
| 周期复盘 | 「公司周期复盘」/「scrollytelling 复盘」/「公司周期拆解」 | 10 步滚动 HTML（2-3 MB）| ✅ v1.0 |
| 速览卡 | 「公司速览卡」/「公司一页速览」/「公司速览」 | 单页 KPI HTML（200-500 KB）| 🔲 v2.1 |
| 估值地图 | 「公司估值地图」/「公司估值」/「估值地图」 | 估值历史 + 同业对比 HTML | 🔲 v2.2 |
| 竞争格局 | 「公司竞争格局」/「公司格局」/「竞争格局墙」 | 行业格局墙 HTML | 🔲 v2.3 |

**不触发**：行业全景研究（→ `industry_research_report`）、多公司对比、纯财务报表导出。

**冲突规避**：与 `industry_research_report` 互补——本 skill 聚焦**单公司单页深度研究**。

---

## 用户引导示例

**首次触发或用户表述模糊时，AI 主动展示示例菜单**：

```
你说什么 → 技能做什么
─────────────────────────────────────────────────────────────
"用 AMD 做一个公司一张纸"            → 列出 4 种形态让你选
"用台积电做一个公司周期复盘"          → 直接进 10 步滚动形态
"用特斯拉做一个公司速览卡"            → 直接进单页 KPI 形态
"用英伟达做一个公司估值地图"          → 直接进估值形态
"用比亚迪做一个公司竞争格局"          → 直接进格局墙形态
"用英伟达做一个公司一张纸，2026Q3"   → 完整参数 + 选形态
"一个公司一张纸：茅台 2026Q2"        → 完整参数 + 选形态
"用海康威视做一张公司纸"             → 列出形态
"帮我研究下宁德时代"                → 列出形态（通用研究意图）
"AMD 现在值不值得买"                → 推荐估值地图或周期复盘
```

**推荐策略**：只说"研究下 X" → 列形态；说"周期/历史/复盘" → 周期复盘；说"估值/贵不贵" → 估值地图；说"对手/格局" → 竞争格局；说"速览/快速看下" → 速览卡。

---

## 两段式工作流（周期复盘形态）

```
Phase A: 客观数据草案（自动）
  ├─ 1. 解析公司名 → 股票代码（mx-xuangu / mx-zixuan）
  ├─ 2. 抓行情 K 线（mx-xuangu qfq 前复权）
  ├─ 3. 抓财务/分部/库存（WebSearch 公司 IR / SEC 10-K）
  ├─ 4. 抓高频需求（WebSearch 四大客户 capex / 行业租金报价）
  ├─ 5. 抓事件时间线（WebSearch 公司大事记）
  ├─ 6. 行业格局墙（WebSearch 行业出清史 + 内置行业模板兜底）
  ├─ 7. 填充文案层（hero/10 steps/outro）基于上述数据
  ├─ 8. 识别品牌色（用户指定 > logo 主色 > 默认 #76b900）
  └─ 9. 调 build_html.py → 产出草案 HTML

Phase B: 研究观点增强（半自动，AskUserQuestion 逐项确认）
  ├─ 10. scores（类比打分卡 5 项）— 让用户确认/修改
  ├─ 11. excluded（被排除的诱人类比 3 项）— 让用户确认/修改
  ├─ 12. radar（雷达 5 维 now/cisco/mine 对比）— 让用户确认
  ├─ 13. clock（4 子板块时钟位置）— 让用户确认
  └─ 14. signals（8 信号现值/阈值/时滞/证伪）— 让用户确认
  → 确认后重生成最终 HTML
```

**关键**：Phase A 产出的草案 HTML 即可交付（结构完整、数据齐全、图表可交互）。Phase B 是增强，不阻塞交付。

**4 种产物形态详细说明**：见 [`references/product-forms.md`](references/product-forms.md)

---

## 模板层文件

```
one-paper-company/
├── SKILL.md                       # 本文件（技能身份 + 流程编排）
├── README.md                      # 产品说明
├── README.en.md                   # 英文说明
├── CHANGELOG.md                   # 变更日志
├── LICENSE                        # MIT
├── plugin.json                    # Claude 插件元数据
├── .gitignore                     # 排除大文件
├── template/
│   ├── template.html              # 周期复盘形态模板（38KB，__PLACEHOLDER__ 槽位）
│   ├── echarts.5.5.0.min.js       # ECharts 5.5.0 UMD（1MB，内联用）
│   └── pixel-font.js              # A-Z + 0-9 + 标点 像素字字母表（2KB）
├── scripts/
│   ├── build_html.py              # data.json + template → HTML（核心引擎）
│   └── validate.py                # 产物校验（8 项）
├── references/
│   ├── nvidia_data.json           # 英伟达原页数据（回归基准）
│   ├── amd_data.json              # AMD 实战数据（端到端验证）
│   ├── product-forms.md           # 4 种产物形态详细说明
│   ├── data-contract.md           # data.json schema + 数据获取链路
│   ├── responsive-spec.md         # 响应式断点 + 滚动跟随 + 配色铁律
│   └── exception-handling.md      # 异常处理 + 验收清单 + 已知限制
└── .github/
    └── ISSUE_TEMPLATE/            # 社区模板
```

---

## build_html.py 用法

```bash
python scripts/build_html.py <data.json> <output.html>
# 可选参数：
#   --template <path>     默认 template/template.html
#   --pixel-font <path>   默认 template/pixel-font.js
#   --echarts <path>      默认 template/echarts.5.5.0.min.js
```

**输出**：自包含 HTML，内联 ECharts + 像素字 + base64 图片 + 所有数据。
**退出码**：0=成功；非 0=失败（检查 data.json schema）。

## validate.py 用法

```bash
python scripts/validate.py <output.html> [--data data.json]
```

检查 8 项：结构完整性、10 步联动、数据注入、配色铁律、占位符、资产内联、体积、信源三层。

---

## 核心规范（铁律）

| 规范 | 文档 |
|---|---|
| 数据契约 schema + 数据获取链路 | [`references/data-contract.md`](references/data-contract.md) |
| 响应式断点 + 滚动跟随 + 配色铁律 + K 线算法 | [`references/responsive-spec.md`](references/responsive-spec.md) |
| 异常处理 + 验收清单 + 已知限制 | [`references/exception-handling.md`](references/exception-handling.md) |
| 4 种产物形态详细说明 | [`references/product-forms.md`](references/product-forms.md) |

**关键铁律**：
- IntersectionObserver `rootMargin: -38% 0px -52% 0px`（与原始素材 1:1 对齐，不可调整）
- `.steps::after` 60vh tail spacer（确保 s9/s10 激活）
- 配色仅替换 `--green`/`--green-d`，中性色跨公司通用
- 模板占位符不得被注释包裹（`/*__X__*/` 会导致脚本不执行）
- JS 上下文字符串占位符必须用 `js_val()` 包裹（避免语法错误）
