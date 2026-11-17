# PlantUML 图表类型速查

| 图表类型 | 关键字/标记 | 用途 |
|---------|-----------|------|
| 时序图 | @startuml + participant | 对象间消息交互 |
| 类图 | @startuml + class | 类结构与关系 |
| 活动图 | @startuml + start/stop | 工作流与流程 |
| 用例图 | @startuml + actor/usecase | 系统功能与角色 |
| 状态图 | @startuml + [*] | 对象状态转换 |
| 组件图 | @startuml + component | 组件组织与依赖 |
| 部署图 | @startuml + node | 硬件部署架构 |
| 定时图 | @startuml + clock/binary | 时间约束与信号 |
| 思维导图 | @startmindmap | 思维发散与组织 |
| 甘特图 | @startgantt | 项目进度规划 |
| ER 图 | @startuml + entity + \|\|--o{ | 数据库设计（Crow's Foot）|
| C4 架构图 | !include <C4/C4_Context\|Container\|Component> + Person/System/Container | 系统架构分层描述 |
| 网络图 | nwdiag { network ... } | 网络拓扑/网段划分 |
| WBS | @startwbs + * 层级 | 工作分解结构 |
| Salt 界面原型 | @startsalt + { [控件] } | UI 线框图 |
| JSON 可视化 | @startjson | JSON 数据结构 |
| YAML 可视化 | @startyaml | YAML 数据结构 |

## 主题速查（!theme）

```plantuml
@startuml
' 放到 @startuml 之后、图内容之前
!theme cyborg
class Example
@enduml
```

> `!theme` 等 `!` 预处理指令**不支持行尾注释**——`!theme cyborg ' 注释` 会把整行当成主题名而报错，注释要单独写一行。

| 主题 | 风格 |
|------|------|
| `plain` | 默认/对照 |
| `blueprint` | 蓝图（白底蓝线） |
| `amiga` | 白字蓝底 |
| `cyborg`/`superhero`/`united` | Bootswatch 暗色系列 |
| `hacker` | 终端感 |
| `crt-amber` | CRT 琥珀单色 |
| `reddress-darkblue`/`reddress-lightblue` | 红裙深/浅蓝 |
| `aws-orange` | AWS 配色 |
| `Sunlust` | Solarized |
| `mono` | 单色等宽 |

画廊与预览：<https://the-lum.github.io/puml-themes-gallery/themes/>

## 非 UML 图表速查

| 类型 | 关键字 | 用途 |
|------|--------|------|
| JSON | `@startjson` | 数据结构 |
| YAML | `@startyaml` | 数据结构 |
| WBS | `@startwbs` | 工作分解结构 |
| Salt | `@startsalt` | UI 线框原型 |
| ER | `@startuml` + entity | 实体关系图 |
| 网络图 | `@startuml` + nwdiag | 网络拓扑 |
| 正则 | `@startregex` | 正则可视化 |
| EBNF | `@startebnf` | 语法图 |
| Archimate | `@startuml` + Archimate_* | 企业架构 |

## 箭头速查

### 时序图

- `->` 实线箭头
- `-->` 虚线箭头
- `->>` 实线开放箭头
- `x>` 末端X

### 类图关系

- `--|>` 继承
- `..|>` 实现
- `-->` 关联
- `--*` 组合
- `o--` 聚合
- `..>` 依赖

### 通用连接

- `--` 实线
- `..` 虚线
- `-->` 箭头
- `-[hidden]->` 隐藏箭头
