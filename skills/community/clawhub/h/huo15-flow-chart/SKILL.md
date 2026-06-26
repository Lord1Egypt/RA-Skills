---
name: huo15-flow-chart
displayName: 火一五流程图技能
description: 2026 现代美学的流程图、泳道图、系统架构图、C4 架构图、时序图、状态图、ER 图、甘特图生成。Linear/Vercel/Radix 配色 + 软阴影 + 圆角 + 判断色强调 + 容器分层。输入 YAML/JSON 规格或 Mermaid/PlantUML/DOT 源码，输出 SVG/PNG/PDF/draw.io；PDF 默认单页自适应画布不分页；内置 17 种风格（含 v1.4 新增 editorial NYT 杂志 / bauhaus 红黄蓝几何 / swiss 国际主义 Helvetica 网格 三个有性格风格）；支持 draw.io 源文件 + C4-PlantUML + 架构 Tier 分层。触发词：流程图、泳道图、时序图、状态图、ER 图、系统架构图、C4 图、画流程图、生成流程图、编辑杂志风、纽约客、NYT、Monocle、包豪斯、三原色、瑞士国际主义、Helvetica 网格、Müller-Brockmann。
version: 1.4.0
aliases:
  - 火一五流程图
  - 火一五流程图技能
  - 流程图
  - 流程图生成
  - 画流程图
  - 泳道图
  - 时序图
  - 状态图
  - 甘特图
  - ER图
  - 架构图
  - 系统架构图
  - C4 架构图
  - flowchart
  - flow-chart
  - diagram
  - mermaid
  - draw.io
dependencies:
  python-packages:
    - pyyaml
  external:
    - name: "@mermaid-js/mermaid-cli"
      install: "npm i -g @mermaid-js/mermaid-cli"
      notes: "渲染 Mermaid 时用（mmdc 命令）"
    - name: plantuml
      install: "brew install plantuml"
      notes: "PlantUML / C4-PlantUML 渲染（泳道图和 C4 图必须）"
    - name: graphviz
      install: "brew install graphviz"
      notes: "Graphviz DOT 渲染（可选）"
---

# 火一五流程图技能 v1.3.3

> 2026 现代美学的流程图 / 架构图 / 泳道图 / C4 架构图 / 时序图生成器 — 青岛火一五信息科技有限公司
>
> 设计取向：Linear / Vercel / Radix / Stripe 软色系 + 双层柔和阴影 + 圆角节点 + 判断菱形 accent 强调色 + PDF 单页自适应。

---

## 一、核心能力

### 1.1 支持的图表类型

| type                 | 用途                    | 渲染引擎          | draw.io |
|---------------------|-----------------------|-----------------|---------|
| `flowchart`          | 普通流程图                | Mermaid         | ✅       |
| `architecture`        | 系统架构图（支持 Tier 分层）  | Mermaid         | ✅       |
| `swimlane`           | 真·泳道图（PlantUML）     | PlantUML        | ❌       |
| `swimlane_mermaid`   | 泳道风格（Mermaid，不需要 Java）| Mermaid | ✅ |
| `sequence`           | 时序图                  | Mermaid/PlantUML | ✅       |
| `state`              | 状态图                  | Mermaid         | ✅       |
| `gantt`              | 甘特图                  | Mermaid         | ✅       |
| `er`                 | ER 图                  | Mermaid         | ✅       |
| `class`              | UML 类图                | Mermaid         | ✅       |
| `journey`            | 用户旅程                 | Mermaid         | ✅       |
| `pie`                | 饼图                   | Mermaid         | ✅       |
| `c4_context`          | C4 上下文图（L1）          | Mermaid / **PlantUML** | ✅ |
| `c4_container`        | C4 容器图（L2）            | Mermaid / **PlantUML** | ✅ |
| `mindmap`            | 简单思维导图               | Mermaid         | ✅       |

### 1.2 输出格式

| 格式   | 类型   | 说明 |
|--------|--------|------|
| `.svg` | 矢量图  | 浏览器直接打开，最推荐（任意缩放不糊） |
| `.png` | 位图    | **默认 3× 高清**（≈288 DPI 印刷级），适合 PPT / 文档 |
| `.pdf` | 矢量 PDF | 适合打印；**默认单页自适应不分页** |
| `.mmd` | Mermaid 源码 | 复制到 [mermaid.live](https://mermaid.live) 编辑 |
| `.puml` | PlantUML 源码 | 复制到 PlantUML 编辑器 |
| `.drawio` | **draw.io 源文件** | 用 draw.io 桌面版打开，精美编辑 |
| `.dot` | Graphviz DOT 源码 | 复杂网络拓扑 |

**`--scale N`（v1.3.3）**：高清倍率，作用于 PNG。默认 `3.0`（≈288 DPI 印刷级）。
- `1.0` 普通屏（96 DPI，文件最小）
- `2.0` 视网膜屏（192 DPI）
- `3.0` 印刷级 / 默认
- `4.0` 高印刷（≈384 DPI，文件大约 1.5MB+）

底层映射：mmdc 走 `-s SCALE`，PlantUML 走 `-Sdpi=N`，rsvg-convert 走 `-z N`，Graphviz 走 `-Gdpi=N`。

### 1.3 十七种风格（v1.4 扩充到 17 种）

| key | 名称 | 设计范式 | 适用场景 | 中文别名 |
|------|-----|---------|---------|---------|
| `modern`      | 现代商务     | Radix Indigo/Slate，浅底 + 靛紫描边 + 琥珀判断       | 默认首选，商务/技术文档        | 现代、商务、linear、vercel |
| `classic`     | 经典稳重     | 淡蓝卡 + 深蓝字 + 琥珀强调                           | 咨询报告、正式汇报             | 经典、稳重 |
| `dark`        | 暗色霓虹     | Linear Dark，深底 + 紫霓虹描边 + 青色 accent         | 演示大屏、技术分享             | 暗色、黑色、霓虹、linear-dark |
| `xiaohongshu` | 小红书暖奶油 | 奶油底 + 粉卡节点 + 玫红描边                         | 种草封面、女性向运营           | 小红书、奶油、xhs |
| `ocean`       | 海洋蓝       | 浅天蓝节点 + 深蓝字 + 橙色 accent                    | SaaS 产品、技术架构            | 海洋、蓝、蓝色 |
| `forest`      | 森林绿       | 浅绿卡 + 墨绿字 + 橙色 accent                        | 环保、农业、健康               | 森林、绿、自然 |
| `sunset`      | 夕阳暖橙     | 浅橙卡 + 赭红字 + 青色 accent                        | 运营活动、温暖叙事             | 夕阳、暖橙、橙 |
| `minimal`     | 极简素雅     | Notion 风，近白底 + 深灰字 + 单蓝 accent + 细描边    | 学术论文、出版物、技术书稿     | 极简、素雅、学术、论文、黑白、notion |
| `pastel`      | 马卡龙粉嫩   | 浅紫底 + 深紫字 + 玫粉 accent                        | 儿童教育、女性向               | 马卡龙、粉嫩、粉、儿童 |
| `github`      | 极客 GitHub  | 浅蓝卡 + 品牌蓝 + 绿色 accent                        | 开源 README、技术文档          | 极客、程序员、gh |
| `corporate`   | 企业蓝金     | 深海蓝 + 暖金 accent，小圆角高正式感                 | 金融/政府/年报/提案            | 企业、蓝金、金融、政府 |
| `ink`         | 水墨朱砂     | 米黄宣纸底 + 墨黑节点 + 朱砂 accent                  | 中国风/国学/文化/出版           | 水墨、朱砂、中国风、宣纸 |
| `neubrutalism`| 新粗野主义   | 亮色硬填 + 2.8px 黑描边 + 4px 硬阴影 + 0 圆角         | 潮流独立站、设计作品集         | 粗野、新粗野、brutalism、潮流 |
| `duotone`     | 双色调       | 纯白 + 深海蓝 + 珊瑚粉两色极简（Stripe 风）          | 品牌官网、技术 blog            | 双色、stripe、珊瑚 |
| `editorial` ⭐v1.4 | 编辑杂志 NYT 风  | 米色卡底 + 衬线字 + 报头朱红描边 + 番茄红 accent + 2px 圆角 | NYT/Monocle 杂志风信息图、长篇报道、编辑型品牌、思想类 SaaS  | 编辑、杂志、纽约客、纽约时报、nyt、monocle、editorial |
| `bauhaus` ⭐v1.4   | 包豪斯       | 红 #D32F2F + 黄 #FFD600 + 蓝 #1565C0 三原色硬填 + 1.8pt 黑描边 + 0 圆角 + Futura 风字体 | 文化机构、艺术展、几何品牌、教育、设计运动主题 | 包豪斯、三原色、几何、bauhaus、primary-colors |
| `swiss` ⭐v1.4     | 瑞士国际主义 | 纯白底 + Helvetica + 1px 黑描边 + 报头红 accent + 0 圆角 + 网格化 | 网格化信息图、政府公共项目、博物馆展览图、Müller-Brockmann 风学术 | 瑞士、国际主义、swiss、helvetica、grid、müller、brockmann |

**设计共性（所有风格统一遵循）**：
- 节点：浅色填充 + 彩色描边 + 深色文字，12px 圆角，1.5px 描边
- 阴影：双层 drop-shadow（近 1/2px + 远 4/12px），模拟 Linear/Vercel 的浮起质感
- 判断菱形：统一用 `accent_color` 突出，区别于普通节点
- 数据库圆柱：`secondary_color` 填充，区别于业务节点
- **终端节点**（shape: stadium）：`primary_border_color` 实填 + 白字，像 START 按钮（v1.3.1）
- **分类着色**（`category: 1..5`）：按风格 palette 自动分 5 种色调（v1.3.1）
- 字体：Inter 优先 + PingFang SC/HarmonyOS Sans 回落，节点 `font-weight: 500`，标题 `600`
- 连线：`basis` 曲线（flowchart/C4）/ `linear`（泳道）/ 端点圆角
- 边标签：`border-radius: 999px` 圆角胶囊 + 微阴影（v1.3.1）
- 间距：`nodeSpacing: 60`、`rankSpacing: 80`、`padding: 20`（更透气）

### 1.4 draw.io 精美增强

- 导出 `.drawio` 源文件，用 draw.io 桌面版打开
- draw.io 支持：渐变填充、投影、圆角、图标嵌入
- draw.io 支持 Google Fonts（Mermaid 不支持的中文字体）
- 配合 `--theme` / `--font` / `--shadow` 参数生成精美效果

---

## 二、快速开始

### 2.1 准备渲染器

```bash
# 方案 A：Mermaid（推荐，覆盖 90% 场景）
npm i -g @mermaid-js/mermaid-cli

# 方案 B：PlantUML（C4-PlantUML / 泳道图必须）
brew install plantuml        # macOS
# apt install plantuml       # Ubuntu/Debian

# 方案 C：Graphviz（网络拓扑可选）
brew install graphviz

# Python 依赖
pip install pyyaml
```

### 2.2 最短上手

```bash
# 从 YAML 规格生成 PNG（默认 modern 风格）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.png

# 泳道图（真·PlantUML）
python3 scripts/create-flow-chart.py \
  -i examples/swimlane.yaml \
  -o /tmp/lane.svg

# 导出 draw.io 源文件（精美编辑）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.drawio

# 同时导出多种格式（一键到位）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.png \
  --export-formats svg,pdf,mmd,drawio

# 风格色卡清单（终端 ANSI 预览）
python3 scripts/create-flow-chart.py --list-styles

# 风格画廊：一张图里 14 种风格对比
python3 scripts/create-flow-chart.py \
  -i examples/showcase.yaml --gallery \
  -o /tmp/gallery.png --gallery-cols 5

# 高清 PNG（4K 屏 / 印刷级，v1.3.3）
python3 scripts/create-flow-chart.py \
  -i examples/showcase.yaml \
  -o /tmp/print.png --style modern --scale 4

# 普通屏 PNG（更小文件）
python3 scripts/create-flow-chart.py \
  -i examples/flowchart.yaml \
  -o /tmp/preview.png --scale 1

# draw.io 精美主题（带投影）
python3 scripts/create-flow-chart.py \
  -i examples/architecture.yaml \
  -o /tmp/arch.png \
  --theme modern --font "Microsoft YaHei" --shadow

# C4-PlantUML（专业 C4 图）
python3 scripts/create-flow-chart.py \
  -i examples/c4_context.yaml \
  -o /tmp/c4.puml \
  --engine plantuml
```

---

## 三、YAML 规格速查

### 3.1 流程图 `flowchart`

```yaml
type: flowchart
title: 用户下单流程
direction: TB          # TB | LR | BT | RL

nodes:
  - { id: start, label: 开始, shape: stadium }
  - { id: check, label: 是否有商品?, shape: diamond }
  - { id: pay,   label: 结算付款 }

edges:
  - { from: start, to: check }
  - { from: check, to: pay, label: 是 }
```

**形状**：`rect` / `round` / `stadium` / `diamond`（判断） / `hexagon` / `circle` / `cylinder`（数据库） / `subroutine` / `parallelogram` / `trapezoid`

**边类型**：`solid`（实线）/ `dashed`（虚线）/ `thick`（粗线）/ `dotted`（点线）/ `bidir`（双向）

**语义边（v1.3.2）**：`semantic: success / warning / error / info / neutral` 自动染色。暗色风格下会亮化：
```yaml
edges:
  - { from: check, to: pay,  semantic: success, label: "通过 ✓" }
  - { from: check, to: back, semantic: error,   label: "失败 ✗" }
  - { from: build, to: deploy, semantic: warning, kind: dashed }
  - { from: audit, to: report, semantic: info }
```

**节点 emoji 图标（v1.3.2）**：label 里用 `:name:` 语法自动替换：
```yaml
nodes:
  - { id: login, label: ":key: 登录" }         # 🔑 登录
  - { id: db,    label: ":db: 订单库", shape: cylinder }  # 💾 订单库
  - { id: ship,  label: ":ship: 发货" }        # 🚚 发货
```
已内置图标：user/login/lock/db/cache/cloud/api/mail/cart/pay/order/ship/deploy/rocket/bug/gear/shield/alarm 等 70+ 个，查完整列表见 [flowchart_core.py](scripts/flowchart_core.py) 中的 `_ICON_ALIASES`。

**节点分类（v1.3.1）**：`category: 1..5`（或 `c1..c5`）自动分色，按当前风格的 palette 配色。

### 3.2 系统架构图 `architecture`（支持 Tier 分层）

**方式一：groups 分组**
```yaml
type: architecture
title: 火一五 SaaS 系统架构
groups:
  - { id: frontend, label: 前端层,  children: [web, mobile] }
  - { id: backend,  label: 业务层,  children: [svc_user, svc_order] }
  - { id: data,     label: 数据层,  children: [pg, redis] }
nodes:
  - { id: web, label: Web 门户 }
  - { id: pg,  label: PostgreSQL, shape: cylinder }
edges:
  - [web, svc_user]
  - [svc_user, pg]
```

**方式二：tiers 分层（推荐，层次更清晰）**
```yaml
type: architecture
title: 系统架构（Tier 分层）
tiers:
  - { id: edge, label: 边缘层 }
  - { id: biz,  label: 业务层 }
  - { id: data, label: 数据层 }
nodes:
  - { id: cdn,   label: CDN,       tier: edge }
  - { id: api,   label: API 网关,   tier: biz }
  - { id: pg,    label: PostgreSQL, tier: data, shape: cylinder }
edges:
  - [cdn, api]
  - [api, pg]
```

### 3.3 泳道图 `swimlane`（真·PlantUML）

```yaml
type: swimlane
title: 采购审批流程
lanes:
  - name: 申请人
    steps:
      - { id: A1, label: 填写采购申请 }
      - { id: A2, label: 提交审批 }
  - name: 部门经理
    steps:
      - { id: B1, label: 初审 }
edges:
  - [A1, A2]
  - [A2, B1]
```

### 3.4 时序图 `sequence`

```yaml
type: sequence
title: 用户登录
auto_number: true
nodes:
  - { id: U,  label: 用户,   shape: actor }
  - { id: FE, label: 前端 }
  - { id: BE, label: 后端 }
edges:
  - { from: U,  to: FE, label: 点击登录 }
  - { from: FE, to: BE, label: POST /login }
  - { from: BE, to: FE, label: JWT token, kind: dashed }
notes:
  - { position: over, over: BE, text: "首次登录自动建账" }
```

### 3.5 状态图 `state`

```yaml
type: state
title: 订单状态机
direction: LR
nodes:
  - { id: Pending, label: 待付款 }
  - { id: Paid,    label: 已付款 }
edges:
  - { from: "[*]", to: Pending, label: 下单 }
  - { from: Pending, to: Paid, label: 付款 }
```

### 3.6 甘特图 `gantt`

```yaml
type: gantt
title: Q2 路线图
dateFormat: YYYY-MM-DD
axisFormat: "%m-%d"
sections:
  - name: 基建
    tasks:
      - { name: 服务器扩容, id: i1, status: done,   start: 2026-04-01, duration: 5d }
      - { name: 监控升级,   id: i2, status: active, start: 2026-04-06, duration: 10d }
```

状态值：`done` / `active` / `crit`（关键路径红）/ `milestone`（里程碑）/ 留空即未开始。

### 3.7 C4 架构图 `c4_context` / `c4_container`

**Mermaid 引擎（默认）**
```yaml
type: c4_context
title: 火一五 SaaS 上下文图
nodes:
  - { id: customer, label: 企业客户\n使用 SaaS,  shape: person }
  - { id: huo15,    label: 火一五 SaaS\n企业数字化平台,  shape: system }
  - { id: wecom,    label: 企业微信\nIM,               shape: system_ext }
edges:
  - { from: customer, to: huo15, label: 使用 }
  - { from: huo15,    to: wecom, label: OAuth }
```

**PlantUML 引擎（C4-PlantUML，更专业）**
```bash
python3 scripts/create-flow-chart.py \
  -i examples/c4_context.yaml \
  -o /tmp/c4.puml \
  --engine plantuml
```

C4 shape：`person` / `person_ext` / `system` / `system_ext` / `container` / `container_db` / `component`。

### 3.8 ER 图 / UML 类图 / 用户旅程 / 饼图

- `er` — ER 图，label 用 `\n` 分隔字段
- `class` — UML 类图，edge kind 支持 `extends` / `implements` / `composition` / `aggregation` / `dependency`
- `journey` — 用户旅程，用 `sections[].tasks[]`
- `pie` — 饼图，用 `items` 数组

---

## 四、命令行参数

| 参数 | 说明 |
|------|------|
| `-i, --input` | 输入文件（yaml/json/mmd/puml/dot） |
| `-o, --output` | 输出路径（.svg/.png/.pdf/.mmd/.puml/.dot/.drawio） |
| `--export-formats` | 附加输出格式，逗号分隔。如 `svg,pdf,mmd,drawio` |
| `--export-dir` | 源文件输出目录，默认与主输出同目录 |
| `--style` | 风格：modern / classic / dark / xiaohongshu / ocean / forest / sunset / minimal / pastel / github / corporate / ink / neubrutalism / duotone / editorial / bauhaus / swiss |
| `--theme` | draw.io 主题（与 --style 对应，影响 draw.io 导出效果） |
| `--font` | 字体名称，默认 PingFang SC（Mac）/ Microsoft YaHei（Win） |
| `--shadow` | 为 draw.io 节点添加投影效果 |
| `--engine` | 强制渲染引擎：mermaid / plantuml / dot / drawio / auto |
| `--width, --height` | 输出尺寸（像素） |
| `--background` | 背景色，默认用 style 的 background |
| `--dump-source` | 只打印源码到 stdout，不渲染（仅 draw.io 输出时生效） |
| `--no-pdf-fit` | 取消 PDF 自适应画布（默认自适应，单页输出，不分页）|

---

## 五、Python API

```python
import sys; sys.path.insert(0, 'scripts')

from flowchart_core import parse, to_mermaid, to_plantuml, to_drawio
from flowchart_render import render
from styles import get_style, to_mermaid_init_directive, to_plantuml_skinparam

fc = parse('spec.yaml')
style = get_style('modern')  # 也可传中文别名：'现代' / 'linear' / 'vercel'

# Mermaid（推荐：同时传 style，自动启用 decision / database classDef）
init = to_mermaid_init_directive(style, diagram_type=fc.diagram_type)
code = to_mermaid(fc, init, style=style)
render(code, '/tmp/out.svg', engine='mermaid')

# PDF 单页自适应（默认开启；传 pdf_fit=False 关闭）
render(code, '/tmp/out.pdf', engine='mermaid', pdf_fit=True)

# draw.io（现代风：渐变 + 圆角 + 阴影）
drawio_xml = to_drawio(fc, style=style, theme='modern',
                       font_family='Inter', shadow=True)
render(drawio_xml, '/tmp/out.drawio', engine='mermaid')

# C4-PlantUML
puml = to_plantuml(fc, to_plantuml_skinparam(style))
render(puml, '/tmp/out.puml', engine='plantuml')
```

主要接口：

| 函数 | 说明 |
|------|------|
| `parse(path_or_text, hint='auto')` | YAML/JSON/Mermaid/PlantUML/DOT → FlowChart |
| `to_mermaid(fc, init_directive, style=None)` | → Mermaid 源码；传 style 启用自动 classDef |
| `to_plantuml(fc, skinparam)` | → PlantUML/C4-PlantUML 源码 |
| `to_dot(fc, style)` | → Graphviz DOT |
| `to_drawio(fc, style, theme, font_family, shadow=True)` | → draw.io XML 源码（v1.3 现代风格）|
| `render(source, out, engine, pdf_fit=True)` | 调用 mmdc/plantuml/dot 渲染，PDF 默认单页自适应 |
| `get_style(key)` | 获取 Style 对象（中文别名也能识别）|
| `to_mermaid_init_directive(style, diagram_type='flowchart')` | 返回 `%%{init: ...}%%`；按图类选曲线 |
| `to_plantuml_skinparam(style)` | 返回 PlantUML skinparam 配色指令 |
| `decision_classdef(style)` / `database_classdef(style)` | v1.3 新增：生成 classDef 行 |

---

## 六、与其他技能的边界

| 需求 | 用哪个技能 |
|------|----------|
| 自由层级的思维导图，要导出 XMind | **huo15-mind-map** |
| 流程图 / 架构图 / 泳道图 / 时序图 / C4 图 | **huo15-flow-chart**（本技能）|
| **精美架构图**（渐变/投影/圆角），本地编辑 | **huo15-flow-chart** + draw.io 导出 |
| 工程制图 / 原型图 | 不在范围内，建议 draw.io / Figma |
| 数据仪表盘 | 用图表库（Chart.js / ECharts / matplotlib） |

---

## 七、触发词

- 流程图 / 画流程图 / 生成流程图 / 做一张流程图
- 泳道图 / 跨职能流程图 / swim lane
- 系统架构图 / 架构图 / C4 图 / C4 上下文 / C4 容器
- **draw.io 架构图** / 导出 draw.io / draw.io 源文件
- **C4-PlantUML** / C4 图 PlantUML 格式
- 时序图 / 序列图 / sequence diagram
- 状态图 / 状态机 / state diagram
- ER 图 / 实体关系图
- 甘特图 / gantt
- Mermaid / PlantUML
- **架构分层** / Tier 分层 / 多层架构图

---

## 八、版本历史

- **v1.4.0（当前 · 2026-04-28）** — 三个有性格风格扩展
  - ✅ 新增 `editorial` 编辑杂志风：米色卡底 `#F5EFE0` + 衬线字（Cheltenham/NYT Imperial/Plantin）+ 报头朱红 `#D0021B` 描边 + 番茄红 `#FF6347` accent + 2px 接近直角的圆角（杂志感）— 用于 NYT/Monocle 风信息图、长篇报道、编辑型品牌、思想类 SaaS。中文别名：编辑、杂志、纽约客、纽约时报、nyt、monocle、editorial、report
  - ✅ 新增 `bauhaus` 包豪斯风：红 `#D32F2F` + 黄 `#FFD600` + 蓝 `#1565C0` 三原色硬填 + 1.8pt 黑描边 + 0 圆角 + Futura/Avenir Next 字体栈 + bold 模式 category — 用于文化机构、艺术展、几何品牌、教育、设计运动主题。中文别名：包豪斯、三原色、几何、bauhaus、primary-colors
  - ✅ 新增 `swiss` 瑞士国际主义风：纯白底 + Helvetica/Akzidenz-Grotesk + 1px 黑描边 + 报头红 `#D4181F` accent + 0 圆角 + 极简网格化 — 用于网格化信息图、政府公共项目、博物馆展览图、Müller-Brockmann 风学术。中文别名：瑞士、国际主义、swiss、helvetica、grid、müller、brockmann
  - ✅ 三个新风格**与软色范式 14 风格反差互补**，专攻"有性格 / 设计师作品级"场景；和 design-director v3.0 §二 视觉三元组的 §2.1 #3 Swiss Design / §2.5 #19 Bauhaus / §2.2 #6 NYT 锚点 1:1 对应
  - ✅ 总风格数 14 → 17，`--list-styles` / `--gallery` / 中英文别名 / 多端导出全套支持

- **v1.3.3** — 高清渲染 默认 3× 印刷级
  - ✅ **PNG 默认 3× 高清**（≈288 DPI），告别朴素低分辨率，PPT / 印刷直接可用
  - ✅ **`--scale` 新参数**：1/2/3/4 自由切换，矢量格式（SVG/PDF）不受影响
  - ✅ **三引擎统一**：mmdc `-s`、PlantUML `-Sdpi`、rsvg-convert `-z`、Graphviz `-Gdpi` 同一抽象
  - ✅ **gallery 子图同步升级**为 2.5× 渲染，PIL LANCZOS 缩放后细节锐利
  - ✅ **PDF 矢量字体**通过 rsvg-convert `-z` 进一步细化（PlantUML 路径）
  - ✅ 实测：1500×5400px / 240KB（3×），4K 屏放大无锯齿

- **v1.3.2** — 预设风格 + 语义边 + emoji 图标
  - ✅ **新增 4 种风格**：`corporate` 企业蓝金、`ink` 水墨朱砂、`neubrutalism` 新粗野主义、`duotone` 双色调（共 14 种）
  - ✅ **语义边**：`semantic: success/warning/error/info/neutral` 自动染色（绿/橙/红/蓝/灰）
    - 支持 `kind: success` 简写
    - 走 Mermaid `linkStyle N stroke:...,color:...` 指令
    - 暗色风格下自动切换为亮色系语义色
  - ✅ **节点 emoji 前缀**：label 里写 `:rocket: 部署` / `:db: 数据库` 自动替换为 emoji，覆盖 70+ 流程图常用图标
  - ✅ **category_mode 双模式**：
    - `soft`（默认）→ Linear/Vercel 软色填充
    - `bold` → Neubrutalism 硬色填充
  - ✅ **中文别名大扩展**：企业、金融、水墨、朱砂、中国风、宣纸、粗野、brutalism、双色、stripe 等

- **v1.3.1** — 自我迭代 · 终端/分类/画廊
  - ✅ **终端节点自动高亮**：stadium 形（开始/结束）自动挂 `classDef terminal`，主色实填 + 白字，像 START 按钮
  - ✅ **五色分类支持**：Node 新增 `category: 1..5` 字段，自动生成 `classDef c1..c5`，按风格 palette 配色，一张图里视觉分层更清
  - ✅ **边标签 pill 化**：边上文字用 `border-radius: 999px` 圆角胶囊 + 微阴影，替代朴素背景块
  - ✅ **箭头 / 连线圆润**：`stroke-linecap: round`、`stroke-linejoin: round`，marker overflow 放大
  - ✅ **Subgraph 标题强化**：字重 700、accent 色、字距 .3px，让分组更像 Linear 的卡片
  - ✅ **`--gallery` 模式**：同一张规格一键渲染全部 10 种风格并拼成对比大图（`scripts/gallery.py`）
  - ✅ **`--list-styles` 终端色卡**：Truecolor ANSI 直接在终端显示每套风格的主色 / 描边 / 文字 / palette
  - ✅ **新增 `examples/showcase.yaml`**：电商订单履约全链路样例，演示终端 + 判定 + 数据库 + 分类 + 分组的组合美学
  - ✅ **文档 `--help` 扩充**：新增 `--gallery` / `--gallery-styles` / `--gallery-cols` / `--list-styles` 四个开关

- **v1.3.0** — 2026 现代美学大改造
  - ✅ **十种风格全面重绘**：从"深色填充 + 白字"老旧扁平风，升级为 Linear/Vercel/Radix 范式的"浅色填充 + 彩色描边 + 深色文字"
  - ✅ **双层 drop-shadow**：`drop-shadow(0 1px 2px) drop-shadow(0 4px 12px)`，复刻 Linear/Vercel 的浮起质感
  - ✅ **判断菱形 accent 强调**：自动 `classDef decision`，每套风格独立 accent 色
  - ✅ **数据库圆柱自动识别**：自动 `classDef database`，用次级色区别于业务节点
  - ✅ **Mermaid init 优化**：`nodeSpacing: 60` / `rankSpacing: 80` / `padding: 20`，按图类自动切换曲线（flowchart basis、swimlane linear）
  - ✅ **PDF 自适应画布（默认开启）**：Mermaid 走 `mmdc --pdfFit`，PlantUML 走 `SVG → rsvg-convert → PDF`，单页不分页
  - ✅ **draw.io 生成器重写**：修复 XML 属性重复 bug、edge 源/目标 id 计算错乱；新增渐变、圆角、正交弧线、容器嵌套
  - ✅ **PlantUML skinparam 扩充**：圆角 + 阴影 + 时序参与者 + 分组 + dpi:120
  - ✅ **新 Style 字段**：`accent_text_color`、`accent_border_color`、双层阴影参数、`corner_radius`、`stroke_width`、`node_spacing`、`rank_spacing`、`padding`、`palette`
  - ✅ **别名扩展**：linear / vercel / notion / linear-dark 等

- **v1.2.0** — draw.io 导出 + C4-PlantUML + Tier 分层
  - ✅ 新增 `.drawio` 源文件导出（draw.io 桌面版打开，精美编辑）
  - ✅ 新增 `--theme` / `--font` / `--shadow` 参数（draw.io 精美效果）
  - ✅ 新增 `--export-formats`（一键导出多种格式，兼容旧名 `--also`）
  - ✅ 新增 C4-PlantUML 引擎（`--engine plantuml` 输出专业 C4 图）
  - ✅ 新增 `tiers` 分层字段（architecture 类型专用，层次更清晰）
  - ✅ 新增 `node.tier` 属性（替代 group 归类，tiers 模式下使用）
  - ✅ `to_drawio()` Python API（可直接集成到其他工具）
  - ✅ 修复 `.drawio` 导出时 `return` 缺失 bug

- **v1.1.0** — 扩展 6 种风格
  - 新增：`ocean` / `forest` / `sunset` / `minimal` / `pastel` / `github`

- **v1.0.0** — 首版
  - 支持 13 种图表（flowchart / architecture / swimlane / swimlane_mermaid / sequence / state / gantt / er / class / journey / pie / c4_context / c4_container）
  - 3 种输入（YAML/JSON、Mermaid、PlantUML）、6 种输出（svg/png/pdf/mmd/puml/dot）
  - 4 种风格：modern / classic / dark / xiaohongshu

---

**技术支持：** 青岛火一五信息科技有限公司
