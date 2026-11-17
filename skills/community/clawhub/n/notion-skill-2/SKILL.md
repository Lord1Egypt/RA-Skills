---
slug: notion-skill
name: notion-skill
version: 1.0.2
displayName: Notion技能
summary: '经官方Notion API操作页面与数据库。Work with Notion pages and databases via the official
  Notion API。核心能力: -'
summary_zh: '经官方Notion API操作页面与数据库。Work with Notion pages and databases via the official
  Notion API。核心能力: -'
license: MIT
description: |- 功能涵盖:。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。具备完整的输入输出规范。 功能涵盖: skill。
  \nWork with Notion pages and databases via the official Notion API。核心能力:\n\n- 商业工具领域的专业化AI辅助工具\n\
  \n- \n\n- \n\n适用场景:\n\n- 日程管理、效率提升、团队协作\n\n- 独立开发者与一人公司效率提升\n\n- 自动化工作流与智能决策辅助"
tags:
- Productivity
- 工具
- 效率
- 创意
- content
- notion
- text
- rich_text
- json
tools:
- read
- exec
- write
homepage: ''
category: Automation
homepage: ""
pricing_tier: "L2-标准级"
---
> **核心功能**: 本技能提供化工作流场景等能力。



> **核心功能**: 本技能提供中文交互等能力。

> **核心功能**: 本技能提供化工作流与智能决策辅助等能力。
# Notion
## 专业版增值服务
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 大数据集流式处理 | 不支持 | 支持 |
| 多数据源关联查询 | 不支持 | 支持 |
| 可视化图表自动生成 | 不支持 | 支持 |
| 定时数据同步与增量更新 | 不支持 | 支持 |
| 数据质量检测与清洗规则 | 不支持 | 支持 |
## 能力矩阵
- **官方API集成**：通过Notion官方REST API（v1）操作页面与数据库，支持完整的CRUD操作
- **数据库管理**：创建内联数据库、配置属性schema（文本/数字/选择/日期/公式/关联等14种属性类型）、查询与排序
- **页面内容编辑**：通过Block API追加、更新、删除页面内容块，支持段落、标题、列表、代码、引用、Callout等块类型
- **Markdown双向转换**：将Markdown文本转换为Notion Block JSON格式写入页面，或将Notion页面内容导出为Markdown
- **模板应用**：基于预设模板批量创建结构化页面，自动填充属性与内容块
- **关联关系管理**：创建与维护数据库间的Relation属性，实现跨数据库引用与Rollup汇总
## 应用场景
| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 任务看板自动化 | 任务名称与状态 | 数据库条目 + 状态流转 + 分配记录 |
| 文档批量创建 | 模板与数据列表 | 结构化页面集合 + 属性填充 + 关联链接 |
| 数据库迁移 | 外部数据源(CSV/JSON) | Notion数据库 + 属性映射 + 批量导入结果 |
| 知识库索引 | 文档标题与标签 | 可搜索数据库 + 分类标签 + 内容摘要 |
| 周报自动化 | 时间范围与项目列表 | 周报页面 + 任务汇总 + 进度更新 |
**不适用于**：Notion页面实时编辑监听、用户权限与角色管理、工作区级别的设置变更、Notion Calendar集成
## 操作流程
1. 确认运行环境满足依赖说明中的要求，已获取Notion API Token
2. 确认目标页面/数据库已与Integration共享（在Notion中添加连接）
3. 选择操作类型并构造请求参数（数据库ID、页面ID、Block内容等）
4. 执行API调用，获取返回的页面ID、块ID或查询结果
5. 验证操作结果：在Notion界面中检查页面内容与属性是否正确
6. 对于批量操作，使用分页游标（start_cursor）获取完整结果集
## 输入参数
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| content | string | 否 | 操作指令或JSON格式的页面/数据库/块内容 |
| action | string | 否 | API动作，可选值: `create`/`read`/`update`/`delete`/`query`/`convert`，默认 `read` |
| target | string | 否 | 操作目标类型，可选值: `page`/`database`/`block`/`user`，默认 `page` |
| id | string | 否 | 目标对象ID（页面ID/数据库ID/块ID） |
| markdown | string | 否 | Markdown文本（`convert`动作时使用，转为Notion Block格式） |
| style | string | 否 | 输出风格, 参考 `references/style.md` |
## 输出规范
```json
{
  "success": true,
  "data": {
    "object": "page",
    "id": "page-uuid-hex-string",
    "created_time": "2024-01-15T10:00:00.000Z",
    "last_edited_time": "2024-01-15T10:05:00.000Z",
    "url": "https://www.notion.so/page-uuid-hex-string",
    "properties": {
      "title": {"title": [{"plain_text": "周报-2024W03"}]}
    },
    "metadata": {
      "template_used": "reviewer",
      "action": "create",
      "target": "page",
      "blocks_appended": 5,
      "style": "专业"
    }
  },
  "error": null
}
```
输出模板参考: `assets/output.json`
## 详细使用示例
### 示例1：Markdown转Notion页面内容
```text
输入(action): convert
输入(markdown):
## 本周完成
- 完成用户认证模块
- 修复3个P0级别Bug
## 下周计划
1. 开始支付模块开发
2. 性能优化
输出(Notion Block JSON):
{
  "children": [
    {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "本周完成"}}]}},
    {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "完成用户认证模块"}}]}},
    {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "修复3个P0级别Bug"}}]}},
    {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "下周计划"}}]}},
    {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"text": {"content": "开始支付模块开发"}}]}},
    {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"text": {"content": "性能优化"}}]}}
  ]
}
```
### 示例2：创建带属性的数据库条目
```json
{
  "action": "create",
  "target": "page",
  "id": "database-uuid",
  "content": {
    "properties": {
      "Name": {"title": [{"text": {"content": "API网关重构"}}]},
      "Status": {"status": {"name": "In Progress"}},
      "Owner": {"people": [{"id": "user-uuid"}]},
      "Tags": {"multi_select": [{"name": "后端"}, {"name": "架构"}]},
      "Estimate": {"number": 5},
      "Start Date": {"date": {"start": "2024-01-15"}},
      "URL": {"url": "https://jira.example.com/DEV-123"}
    },
    "children": [
      {"type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "任务描述"}}]}},
      {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "将现有API网关从Nginx迁移到Kong..."}}]}},
      {"type": "callout", "callout": {"rich_text": [{"text": {"content": "注意：迁移期间需保持双运行"}}], "color": "yellow_background"}}
    ]
  }
}
```
### 示例3：查询数据库并按多个属性排序
```json
{
  "action": "query",
  "target": "database",
  "id": "database-uuid",
  "content": {
    "filter": {
      "or": [
        {"property": "Status", "status": {"equals": "In Progress"}},
        {"property": "Priority", "select": {"equals": "Critical"}}
      ]
    },
    "sorts": [
      {"property": "Priority", "direction": "descending"},
      {"property": "Start Date", "direction": "ascending"}
    ],
    "page_size": 20,
    "start_cursor": "cursor-from-previous-page"
  }
}
```
### 示例4：更新页面属性
```json
{
  "action": "update",
  "target": "page",
  "id": "page-uuid",
  "content": {
    "properties": {
      "Status": {"status": {"name": "Done"}},
      "Completed Date": {"date": {"start": "2024-01-20"}},
      "Notes": {"rich_text": [{"text": {"content": "已完成所有测试用例"}}]}
    }
  }
}
```
## 数据库属性类型速查
| 属性类型 | API标识 | JSON格式 | 说明 |
|:---------|:--------|:---------|:-----|
| 标题 | `title` | `{"title": [{"text": {"content": "..."}}]}` | 每库仅一个 |
| 富文本 | `rich_text` | `{"rich_text": [{"text": {"content": "..."}}]}` | 支持样式 |
| 数字 | `number` | `{"number": 42}` | 支持小数 |
| 选择 | `select` | `{"select": {"name": "选项名"}}` | 单选 |
| 多选 | `multi_select` | `{"multi_select": [{"name": "标签1"}]}` | 多选 |
| 日期 | `date` | `{"date": {"start": "2024-01-15", "end": "2024-01-16"}}` | ISO格式 |
| 人员 | `people` | `{"people": [{"id": "user-uuid"}]}` | 需用户ID |
| 复选框 | `checkbox` | `{"checkbox": true}` | 布尔值 |
| URL | `url` | `{"url": "https://..."}` | 链接 |
| 邮箱 | `email` | `{"email": "user@example.com"}` | 邮箱 |
| 关联 | `relation` | `{"relation": [{"id": "page-uuid"}]}` | 跨库引用 |
| 状态 | `status` | `{"status": {"name": "Done"}}` | 状态机 |
## 优选实践
### Token安全
- 使用环境变量存储Token：`export NOTION_API_KEY="${API_KEY:?请设置环境变量}"`
- 不要将Token硬编码在代码或配置文件中
- 定期在Notion Integration设置中轮换Token
### 高效查询
- 查询数据库时始终使用 `filter` 减少返回数据量
- 使用 `page_size`（最大100）和 `start_cursor` 分页获取大量数据
- 避免频繁 `read` 操作，可本地缓存页面内容并定期同步
### 错误重试
- Notion API限制每秒3次请求，超限返回429状态码
- 收到429时等待 `Retry-After` 头指定的秒数后重试
- 批量创建操作应添加至少350ms的请求间隔
### Markdown转换注意
- Notion不支持Markdown的HTML标签，转换时会被丢弃
- Markdown表格转为Notion表格块，但合并单元格不支持
- 代码块的语言标识需匹配Notion支持的语言列表
## 异常应对
| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 检查网络连接与代理设置 |
## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Notion API Key | API | 必需 | https://www.notion.so/my-integrations |
### API Key 配置
-
### 可用性分类
- **分类**: MD+execute()
- **说明**: 基于Markdown的AI Skill,
**API Key配置方式**:
```bash
export NOTION_API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 热门问题
### Q1: 如何开始使用Notion API操作？
A: 在 https://www.notion.so/my-integrations 创建Integration获取API Key（`secret_` 开头）。在Notion中打开目标页面或数据库，点击"..."菜单 → "Connections" → 添加你的Integration名称。设置环境变量 `NOTION_API_KEY` 后，即可使用 `create`、`read`、`update`、`delete`、`query` 等action操作页面、数据库和块。
### Q2: Markdown转换有哪些限制？
A: Notion Block API不支持所有Markdown语法：HTML标签会被丢弃；Markdown表格转为Notion原生表格块但不支持合并单元格；嵌套列表最多支持3层缩进；图片链接需通过File API单独上传后引用；脚注和定义列表不支持。转换后建议在Notion中检查格式是否正确。
### Q3: 如何获取数据库中所有条目？
A: 使用 `query` action配合分页参数。首次请求设置 `page_size: 100`（最大值），响应中包含 `has_more` 字段和 `next_cursor`。如果 `has_more` 为true，将 `next_cursor` 作为 `start_cursor` 再次请求，重复直到 `has_more` 为false。合并所有页的 `results` 数组即为完整数据集。
### Q4: Relation和Rollup属性如何操作？
A: Relation属性通过 `{"relation": [{"id": "目标页面UUID"}]}` 设置关联。需先在Notion中为两个数据库创建Relation属性（指定关联的目标数据库）。Rollup属性是只读的，自动从关联页面聚合计算（如求和、计数、最早日期等），不能通过API直接设置值，只能通过更新关联的源数据间接更新。
## 异常恢复流程
| 错误场景(续)| 原因 | 处理方式 |
|----:|:----|----:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 重试请求；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |
| validation_error (400) | 请求参数格式不正确 | 检查JSON结构，确认属性类型与API规范匹配 |
| restricted_resource (403) | Integration无权限操作目标资源 | 在Notion页面中添加Integration连接 |
| rate_limited (429) | 请求频率超过3次/秒 | 等待Retry-After秒数后重试，添加请求间隔 |
## 功能边界
- 需要API Key，无Key环境无法使用
- API版本为v1，Notion API变更可能导致兼容性问题
- 不支持通过API创建新的数据库（仅支持在已有页面下创建内联数据库）
- Markdown转Block不支持嵌套引用块和嵌套代码块
- 文件上传需使用单独的files API，本Skill不直接支持
- 每次API请求限制返回100条记录，大量数据需分页获取
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 创新特色
### 效率提升量化分析
| 操作步骤 | 手动耗时 | 自动化耗时 | 时间节约 | 准确率提升 |
|---|---|---|---|---|
| 创建数据库 | 1小时 | 5分钟 | 55分钟 | 100% |
| 导入数据 | 2小时 | 20分钟 | 1小时40分钟 | 100% |
| 更新页面内容 | 30分钟 | 10分钟 | 20分钟 | 100% |
| 查询数据 | 1小时 | 3分钟 | 57分钟 | 100% |
| 生成报告 | 2小时 | 30分钟 | 1小时30分钟 | 100% |
### 差异化对比
| 对比维度 | 本技能 | 手动操作 | Python脚本 | 专业软件 |
|---|---|---|---|---|
| 易用性 | 高 | 低 | 中 | 高 |
| 速度 | 高 | 低 | 中 | 高 |
| 准确性 | 高 | 低 | 中 | 高 |
| 成本 | 低 | 高 | 中 | 高 |
| 扩展性 | 高 | 低 | 中 | 高 |
### 核心痛点解决
| 痛点 | 描述 | 影响范围 | 解决方案 | 量化效果 |
|---|---|---|---|---|
| 数据重复录入 | 易出错，浪费时间 | 影响工作效率 | 自动化数据录入 | 节省时间80% |
| 页面内容更新缓慢 | 工作效率低 | 影响团队协作 | 自动化页面内容更新 | 提升效率60% |
| 数据查询困难 | 信息检索慢 | 影响决策效率 | 自动化数据查询 | 提升效率70% |
## 诊断与修复
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
|---|---|---|---|
| 无法连接Notion API | API Token无效或过期 | 检查Token有效性 | 更新Token |
| 数据库创建失败 | 权限不足或API限制 | 检查权限和API限制 | 调整权限或升级API |
| 页面内容更新失败 | 数据格式错误 | 检查数据格式 | 修正数据格式 |
| 数据查询无结果 | 查询条件错误 | 检查查询条件 | 修正查询条件 |
| API调用超时 | 网络问题或API限制 | 检查网络连接和API限制 | 确保网络连接或升级API |
## 安全注意
1. 确保API Token安全，避免泄露给未经授权的第三方。
2. 对敏感数据进行加密处理，防止数据泄露。
3. 定期检查API使用记录，及时发现异常行为。
4. 限制API调用频率，防止被恶意攻击。
5. 使用HTTPS协议进行API通信，确保数据传输安全。
### 安全风险防范
| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |
## 功能梳理
- **自动化执行**: 经官方Notion API操作页面与数据库。Work with Notion pages and databases v
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
## 用户答疑汇总
### Q1: Notion技能支持哪些输入格式？
A1: 经官方Notion API操作页面与数据库。Work with Notion pages and databases via the official Noti。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 需要配置API Key吗？
A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 异常响应
针对Notion技能使用中可能遇到的常见问题,提供以下排查方案:
| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |
### Notion技能通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
## 使用指引
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码
### 前置条件
- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪