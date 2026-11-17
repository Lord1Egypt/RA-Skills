# plantuml-skill

[![ClawHub](https://img.shields.io/badge/ClawHub-plantuml--skill--2-blue)](https://clawhub.ai/holdyounger/skills/plantuml-skill-2)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

用 PlantUML 文本语法绘制 UML 图与架构图。面向 OpenClaw / Claude 等 AI Agent 的技能（Skill），也让 Agent 一次说对话，直接产出可渲染的 `.puml`。

**Draw UML and architecture diagrams with PlantUML text syntax — sequence, class, activity, use case, state, component, deployment, timing, ER, C4, network, mindmap, Gantt, WBS, JSON/YAML, Salt wireframes.**

## 预览

全部预览图由官方在线服务实时渲染自 `examples/` 中的源码，所见即所得。

### 新增亮点图类型

| ER 实体关系 | C4 容器图 | 网络图 nwdiag |
|---|---|---|
| <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/er.svg" width="240" alt="ER 实体关系图预览"> | <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/c4-container.svg" width="240" alt="C4 容器图预览"> | <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/network.svg" width="240" alt="网络图（nwdiag）预览"> |

| JSON 可视化 | Salt 界面原型 | 甘特图 |
|---|---|---|
| <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/json.svg" width="240" alt="JSON 数据可视化预览"> | <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/salt.svg" width="240" alt="Salt 界面原型预览"> | <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/gantt.svg" width="240" alt="甘特图预览"> |

### 基础 UML

| 时序图 | 类图 | 活动图 |
|---|---|---|
| <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/sequence.svg" width="240" alt="时序图预览"> | <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/class.svg" width="240" alt="类图预览"> | <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/activity.svg" width="240" alt="活动图预览"> |

| 状态图 | 思维导图 | |
|---|---|---|
| <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/state.svg" width="240" alt="状态图预览"> | <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/mindmap.svg" width="240" alt="思维导图预览"> | |

## 为什么选这个技能

- **覆盖面广**：15+ 图类型，含 ER（Crow's Foot）、C4 架构（官方 C4 标准库）、nwdiag 网络图、JSON/YAML 数据可视化、Salt 界面原型等高频非 UML 图——同类技能大多只覆盖基础 UML
- **可渲染性优先**：所有语法片段按官方文档核对，Agent 生成即可渲染，不用反复试错
- **主题与美化**：内置 25+ 主题速查（`!theme` 一键换肤），附主题画廊链接
- **进阶能力**：预处理（变量/条件/循环/函数）、`<style>` CSS 定制、skinparam 迁移指南

## 支持的图表类型

| 类别 | 图类型 |
|------|--------|
| 结构 UML | 类图、组件图、部署图、对象图、包图 |
| 行为 UML | 时序图、活动图、用例图、状态图、定时图 |
| 架构与数据 | **C4（Context/Container/Component）**、**ER 实体关系**、**网络图 nwdiag**、Archimate |
| 可视化 | **JSON**、**YAML**、正则图、EBNF 语法图、数学公式 |
| 规划 | 甘特图、**WBS 工作分解**、思维导图 |
| 界面 | **Salt UI 线框原型** |

## 安装

### ClawHub（推荐）

```bash
openclaw skills install @holdyounger/plantuml-diagrams
```

或全局安装：

```bash
openclaw skills install @holdyounger/plantuml-diagrams --global
```

### 从源码

```bash
git clone https://github.com/holdyounger/plantuml-skill.git ~/.openclaw/workspace/skills/plantuml-skill
```

## 使用示例

装好后直接对 Agent 说：

- 「画一个用户登录的时序图」
- 「给这个微服务系统画 C4 容器图」
- 「根据这段建表 SQL 画 ER 图」
- 「把这个 JSON 画成结构图」
- 「画一个 App 首页的界面原型」

## 实践指南：如何用得好

只会语法只能保证图「能渲」。要让图「好用」，遵循几条核心原则（完整版见 SKILL.md 末尾「如何用得好」与 `references/best-practices.md`）：

- **一张图只讲一件事**，超过约 20 个节点就拆
- **命名即文档**：用业务名而非 A/B/C
- **分组圈边界** + 类图 / 组件图 / 部署图优先 `left to right direction`（活动图不适用，见下）
- **克制用色**，颜色只区分关注点；统一用 1 个 `!theme`
- **箭头语义统一**，别一张图里 `->` 忽指调用忽指数据

下面这张「分阶段活动图」就是好实践示范——用 `partition` 把流程切成清晰的阶段：

| 好实践示范（活动图：用 partition 分阶段） |
|---|
| <img src="https://raw.githubusercontent.com/holdyounger/plantuml-skill/main/assets/preview/bp-activity-good.svg" width="440" alt="好实践活动图（partition 分阶段）预览"> |

> 更多「好 / 差对照」（活动图 / 类图 / 时序图 + 可复制统一样式片段）见 `references/best-practices.md`。

## 渲染输出

技能生成 `.puml` 源码后，可选任意一种方式出图：

```bash
# 本地（需 Java）
java -jar plantuml.jar -tsvg diagram.puml

# 在线服务器（无需 Java）：把 .puml 源码 URL 编码后拼接
#   PNG: https://www.plantuml.com/plantuml/png/?~<url-encoded-source>
#   SVG: https://www.plantuml.com/plantuml/svg/?~<url-encoded-source>
# VS Code：PlantUML 插件，Alt+D 预览
# 在线手绘：https://www.plantuml.com/plantuml
# Mermaid 互转不适用，PlantUML 语法独立
```

## 文件结构

```text
plantuml-skill/
├── SKILL.md              # 主技能文件（1055 行：语法参考 + 选择指南 + 渲染闭环 + 实践指南，Agent 按需加载）
├── README.md             # 本文件
├── examples/             # 可渲染示例（16 个）
│   ├── sequence.puml / class.puml / activity.puml / state.puml / usecase.puml
│   ├── component.puml / deployment.puml / timing.puml
│   ├── er.puml / c4-container.puml / network.puml
│   ├── json.puml / salt.puml / mindmap.puml / gantt.puml
│   └── bp-activity-good.puml   # 实践指南示范图（partition 分阶段）
├── scripts/
│   └── render_preview.py   # 渲染 + 校验预览图（零依赖，见下）
└── references/
    ├── cheatsheet.md      # 速查表
    └── best-practices.md  # 好图/差图对照 + 统一样式模板
```

### 重渲预览图

改了 `examples/` 里的源码后，用自带脚本一键重渲并校验（Python 3 标准库即可，无需装依赖）：

```bash
python scripts/render_preview.py              # 全部重渲
python scripts/render_preview.py timing class # 只渲指定几个
python scripts/render_preview.py --check      # 只校验已有 svg 是不是真图
```

脚本用的是 PlantUML **自定义 64 字符编码表**（不是标准 base64），并且会在写盘前检查内容里有没有 `Syntax Error` / `bad URL` 等标记——因为服务器报错时返回的也是一张合法 SVG，肉眼很容易误判成渲染成功。

## 与同类技能的对比

| | 本技能 | 基础 PlantUML 技能 |
|---|---|---|
| 基础 UML（9 类）| ✅ | ✅ |
| ER 图（Crow's Foot 完整记号）| ✅ 独立章节 | 多数只有最小示例 |
| C4 架构图 | ✅ 官方 C4 库 | ❌ |
| 网络图 nwdiag | ✅ | ❌ |
| JSON/YAML 可视化 | ✅ | ❌ |
| Salt UI 原型 | ✅ | ❌ |
| 主题速查（25+）| ✅ | 部分 |
| 预处理/style 进阶 | ✅ | ❌ |

## License

MIT
