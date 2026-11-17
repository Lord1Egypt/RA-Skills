---

slug: knowledge-graph-tool-pro
name: "knowledge-graph-tool-pro"
version: "1.0.0"
displayName: "知识图谱工具(专业版)"
summary: "团队级嵌入式知识图谱,含加密保险库、可视化、多Agent协作与内存导入。。知识图谱工具(专业版)面向团队与企业,提供完整的嵌入式知识图谱能力,含加密保险库、离线可视化、跨Agent协作与内存"
license: "Proprietary"
edition: "pro"
description: |-
  知识图谱工具(专业版)面向团队与企业,提供完整的嵌入式知识图谱能力,含加密保险库、离线可视化、跨Agent协作与内存自动导入。核心能力:
  - 全量查询、合并、嵌套、整理能力
  - 加密保险库:密钥/令牌加密存储,权限隔离
  - 离线HTML可视化:自包含图谱交互页面
  - 跨Agent只读+写入:多Agent共享知识
  - 内存自动导入:从会话历史提取并审查
  - 高级配置:物理参数、阈值、压缩策略

  适用场景:
  - 团队知识库与决策记录沉淀
  - 研究项目多源知识整合
  - 多Agent协作共享长期记忆
  - 敏感配置...
tags:
  - Development
  - Knowledge
  - 团队知识库
  - 企业级
  - 可视化
  - 安全
  - 工具
  - 效率
  - 知识
  - 文档
  - node
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"

---

# 知识图谱工具(专业版)

## 概述

知识图谱工具(专业版)面向团队与企业,在兼容免费版查询与 KGML 格式的基础上,扩展了加密保险库、离线可视化、跨Agent协作、内存自动导入与高级配置能力.
当你在请求中提及 知识图谱、团队知识、加密存储、可视化、多Agent协作、内存导入 等关键词时,本工具会自动激活,为团队提供结构化的长期知识管理与敏感信息安全存储方案.
本版本完全兼容 `knowledge-graph-tool-free` 的全部查询命令与 KGML 格式,可平滑升级,已有图谱数据无需迁移.
## 核心能力

| 能力模块 | 说明 | 与免费版差异 |
|----|---|------|
| 全量查询 | 子节点、类型、分类、孤立、统计、时间线、变更、低置信度 | 与免费版一致 |
| 实体合并 | absorb/nest两种合并模式 | 免费版仅基础整理 |
| 加密保险库 | 密钥/令牌加密存储,权限隔离,绝不泄露明文 | 免费版无 |
| 离线可视化 | 自包含HTML交互页面,物理引擎布局 | 免费版无 |
| 跨Agent协作 | reader.mjs只读 + 受控写入 | 免费版仅单Agent |
| 内存导入 | 从会话历史自动提取实体,低置信度审查 | 免费版无 |
| 高级配置 | 物理参数、验证阈值、压缩策略、整理自动化 | 免费版仅基础设置 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：团队级嵌入式知识、含加密保险库、协作与内存导入、知识图谱工具、专业版、面向团队与企业、提供完整的嵌入式、知识图谱能力、协作与内存自动导、核心能力、整理能力、自包含图谱交互页、共享知识、内存自动导入、从会话历史提取并等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:团队决策记录沉淀

团队完成一次架构评审,希望把决策、备选方案与权衡沉淀为可检索的知识.
```bash
# 查看当前图谱规模
node （请参考skill目录中的脚本文件） stats
# ...
# 评估决策文档复杂度
node （请参考skill目录中的脚本文件） --file /path/to/adr.md
# ...
# 提取后写入,Agent 会自动建议合并相似实体
node （请参考skill目录中的脚本文件）
```

Agent 会读取决策文档,提取实体(方案、约束、风险)、关系(权衡、依赖、替代),并在 KGML 中标注置信度,便于后续审查.
```text
#KGML v2 | 28e 15r | depth:4 | 2026-07-18
[决策]
微服务拆分(ADR-007):decision — 按业务能力拆分,独立部署
  服务边界:principle — 限界上下文驱动
  数据一致性:constraint — 最终一致+Saga
%rels
微服务拆分>权衡>单体部署 微服务拆分>依赖>服务网格
```

### 场景二:加密存储团队密钥

团队需要把API密钥、数据库连接串等敏感信息加密存储,且不让明文进入上下文.
```bash
# 设置加密键值(带备注)
node （请参考skill目录中的脚本文件） set db_password 'S3cret!' --note "生产数据库主密码"
# ...
# 获取原始值(用于管道传递,不在聊天显示)
node （请参考skill目录中的脚本文件） get db_password | xargs -I{} apply-config {}
# ...
# 列出键名(不显示值)
node （请参考skill目录中的脚本文件） list
# ...
# 删除
node （请参考skill目录中的脚本文件） del db_password
```

安全原则:

- 绝不在聊天或日志中打印保险库值
- `vault.enc.json` 与 `.vault-key` 永不进入上下文
- 其他Agent通过 reader.mjs 只读访问,无写入权限

### 场景三:多Agent共享知识

团队有多个Agent各司其职,希望共享同一份知识图谱.
```javascript
// Agent A 写入知识
import { createReader } from '<path-to-skill>/lib/reader.mjs';
const kg = createReader();
kg.search("微服务");
kg.traverse("id-微服务拆分", { depth: 2 });
kg.stats();
```

```bash
# 导出为JSON供其他Agent消费
node （请参考skill目录中的脚本文件） --format json --target /shared/kg-export.json
```

跨Agent访问规则:

- 只读访问:通过 reader.mjs,任何Agent可用
- 写入访问:仅授权Agent,通过权限配置控制
- 数据隔离:每个Agent的配置独立,互不污染

## 不适用场景

以下场景知识图谱工具(专业版)不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 1. 团队初始化

```bash
# 在团队共享目录初始化
node （请参考skill目录中的脚本文件） --workspace /shared/team-kg --platform skill-platform
# ...
# 配置团队默认token预算
node （请参考skill目录中的脚本文件） set summary.tokenBudget 8000
node （请参考skill目录中的脚本文件） set validation.minEntities 50
```

### 2. 可视化生成

```bash
# 默认输出到 data/kg-viz.html
node （请参考skill目录中的脚本文件）
# ...
# 自定义输出路径
node （请参考skill目录中的脚本文件） --output /tmp/team-graph.html
```

可视化页面特性:

1. 自包含,离线可用,无CDN依赖
2. 父子边渲染为蓝色虚线箭头(60%透明度)
3. 普通关系为红色实线箭头
4. 物理引擎布局,可拖拽与缩放

### 3. 内存导入

```bash
# 先空跑预览
node （请参考skill目录中的脚本文件）
# ...
# 确认后正式导入(置信度0.5)
node （请参考skill目录中的脚本文件） --apply
# ...
# 审查自动导入的低置信度实体
node （请参考skill目录中的脚本文件） uncertain
```

### 4. 高级合并

```bash
# absorb模式:源实体被目标吸收,属性合并
node （请参考skill目录中的脚本文件） --target <目标id> --source <源id> --mode absorb
# ...
# nest模式:源实体作为目标子节点嵌套
node （请参考skill目录中的脚本文件） --target <目标id> --source <源id> --mode nest
```

#
## 示例

### 完整配置项参考

| 模块 | 键 | 默认值 | 说明 |
|:-----|:-----|:-----|:-----|
| summary | tokenBudget | 5000 | kg-summary.md 最大token |
| summary | maxChildDepth | auto | 树深度(null=自动:<100取3,100-400取2,>400取1) |
| summary | maxAttrLen | 40 | 属性值最大字符 |
| summary | maxPerRoot | 4 | 每根子树最大关系 |
| summary | compactThreshold | 400 | 紧凑模式实体阈值 |
| summary | mediumThreshold | 200 | 中等深度阈值 |
| validation | minEntities | 30 | 提取通过最小实体 |
| validation | minRelationRatio | 0.5 | 每实体最小关系比 |
| validation | minDepth | 3 | 通过最小层级 |
| validation | minEvents | 3 | 通过最小事件节点 |
| depthCheck | entityCapForEstimate | 50 | 目标估算NER上限 |
| depthCheck | minEntitiesMultiplier | 1.0 | 命名实体→最小目标乘数 |
| depthCheck | extraEntities | 30 | 加到最小实体的额外值 |
| consolidation | autoNest | true | 自动嵌套单关系孤儿 |
| consolidation | mergeSuggestions | true | 相似标签合并建议 |
| consolidation | pruneEmptyAttrs | true | 删除空/null属性 |
| consolidation | levenshteinThreshold | 2 | 合并建议最大编辑距离 |
| visualization | repulsion | 5000 | 物理斥力 |
| visualization | edgeRestLength | 160 | 默认边静止长度 |
| visualization | overlapPenalty | 3 | 重叠斥力乘数 |
| visualization | simulationSteps | 500 | 物理仿真迭代 |
| visualization | initialSpread | 1.5 | 初始节点扩散乘数 |
| visualization | zoomAnimationMs | 400 | 缩放到节点动画时长 |

### 团队治理配置示例

```bash
# 团队高标准:要求更多实体与关系
minRelationRatio 0.6
# ...
# 大图谱压缩策略
compactThreshold 300
# ...
# 可视化调整(大图谱需要更大斥力)
node （请参考skill目录中的脚本文件） set visualization.repulsion 8000
```

## 优选实践

### 1. 定期整理与摘要

团队建议每周或实体数超过80时运行整理.
```bash
# 整理(合并相似、嵌套孤儿、修剪空属性)
node （请参考skill目录中的脚本文件）
# ...
# 重新生成摘要
node （请参考skill目录中的脚本文件）
# ...
# 生成可视化快照
node （请参考skill目录中的脚本文件） --output /weekly/kg-week-$(date +%Y%m%d).html
```

### 2. 加密保险库使用规范

```bash
# 团队成员新增密钥时必须带备注
node （请参考skill目录中的脚本文件） set stripe_key 'sk_live_未指定' --note "生产支付密钥-张三负责"
# ...
# 定期审计:列出所有键名与备注
node （请参考skill目录中的脚本文件） list
# ...
# 轮换:删除旧键再设新键
node （请参考skill目录中的脚本文件） del stripe_key
node （请参考skill目录中的脚本文件） set stripe_key 'sk_live_yyy' --note "轮换-2026Q3"
```

### 3. 多Agent协作权限

```javascript
// 团队Agent权限分级示例(伪代码)
const readers = ['agent-researcher', 'agent-writer'];   // 只读
const writers = ['agent-curator', 'agent-admin'];        // 可写
// ...
// reader.mjs 提供只读接口,所有Agent可用
// 写入需通过 curator Agent 统一审核后落盘
```

### 4. 内存导入审查流程

```bash
# 1. 空跑预览即将导入的实体
node （请参考skill目录中的脚本文件）
# ...
# 2. 正式导入(低置信度)
node （请参考skill目录中的脚本文件） --apply
# ...
# 3. 审查低置信度实体
node （请参考skill目录中的脚本文件） uncertain
# ...
# 4. 人工确认或删除
# Agent 会逐个询问是否保留,确认的提升置信度,拒绝的删除
```

### 5. 大规模图谱优化

| 实体规模 | 建议策略 |
|---:|---:|
| <100 | 默认配置即可 |
| 100-400 | 开启紧凑模式,token预算调至6000 |
| 400-1000 | 紧凑模式 + 中等深度,定期合并 |
| >1000 | 分库治理,按主题拆分多个子图谱 |

## 常见问题

### Q1:PRO版与免费版如何共存?

两者 KGML 格式与查询命令完全兼容,PRO版包含免费版全部能力。团队升级时直接替换Skill文件,已有 `data/` 目录的图谱数据无需迁移.
### Q2:加密保险库的密钥如何管理?

保险库使用本地加密文件 `vault.enc.json` 与密钥文件 `.vault-key`。两者必须一起备份,且永不进入版本控制或聊天上下文。建议将 `.vault-key` 单独存放在团队密码管理器中.
### Q3:可视化页面能否离线使用?

可以。`visualize.mjs` 生成的HTML完全自包含,无任何CDN或外部依赖,可直接双击在浏览器打开,适合内网或离线环境分享.
### Q4:多Agent写入如何避免冲突?

建议采用"单写入者"模式:只授权一个 curator Agent 拥有写入权限,其他Agent通过 reader.mjs 只读访问,如需新增知识则提交给 curator 审核后写入。这样可避免并发写入冲突.
### Q5:内存导入会污染图谱吗?

内存导入默认以0.5低置信度写入,并标记为 `uncertain`。导入后必须运行 `node （请参考skill目录中的脚本文件） uncertain` 逐个审查,人工确认的提升置信度,拒绝的删除,避免低质量内容污染图谱.
### Q6:支持多租户隔离吗?

支持。通过不同 `--workspace` 路径初始化多个独立图谱实例,各自拥有独立的 `data/` 与配置。租户间数据物理隔离,互不影响.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Node.js版本**: 建议 20 LTS 及以上(用于加密与多Agent模块)
- **浏览器**: 现代浏览器(用于查看可视化HTML)

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js | 运行时 | 必需 | nodejs.org 下载 |
| npm | 包管理器 | 必需 | 随Node.js安装 |
| 团队密码管理器 | 工具 | 推荐 | 用于保管 .vault-key |

### API Key 配置

- 基础LLM由Agent平台内置提供，Skill基于Markdown指令驱动(除内容中明确标注的外部API).
- 加密保险库的密钥由本地 `.vault-key` 文件管理,不依赖外部API.
- 多Agent协作时,各Agent的鉴权由所在平台处理.
### 可用性分类

- **分类**: MD+execute(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。PRO版面向团队与企业,提供加密保险库、可视化、多Agent协作与内存导入能力,完全兼容免费版查询与KGML格式.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "知识图谱工具(专业版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "knowledge graph pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。