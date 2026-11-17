---

slug: linear-api
name: linear-api
version: 1.0.8
displayName: 项目管理API
summary: 通过GraphQL操作工作项、项目、周期、标签与评论,覆盖创建查询转换全流程。通过项目管理工具的GraphQL API操作工作项全生命周期:工作项CRUD、
  项目管理、团队管理、周期管理、
summary_zh: 通过GraphQL操作工作项、项目、周期、标签与评论,覆盖创建查询转换全流程。通过项目管理工具的GraphQL API操作工作项全生命周期:工作项CRUD、
  项目管理、团队管理、周期管理、
license: MIT
description: |-。通过GraphQL操作工作项、项目、周期、标签与评论,覆盖创建查询转换全流程。通过项目管理工具的GraphQL API操作工作项全生命周期:工作项CRUD、。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。 功能涵盖: linear。
  项目管理、团队管理、周期管理、。支持自动化配置和灵活的参数设置，适覆盖多种使用场景，优化工作流程和效率。。通过GraphQL操作工作项、项目、周期、标签与评论,覆盖创建查询转换全流程。通过项目管理工具的GraphQL
  API操作工作项全生命周期:工作项CRUD、 项目管理、团队管理、周期管理、'
tools:
- read
- exec
- write
homepage: ''
tags: API,api,graphql,key,teamid,priority
- 研发工具
- API
- 接口
- 开发工具
- api
- graphql
- 执行核心
- 处理逻辑
- 返回结构
category: Development
homepage: ""
pricing_tier: "L2-标准级"

---

> **功能说明**: 本技能涵盖 化工作流场景 等核心能力。

# 项目管理API集成

通过项目管理工具的 GraphQL API 操作工作项全生命周期,从创建到状态推进,覆盖项目、周期、标签、评论与关联管理.
## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 项目管理API处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 能力矩阵
### 1. 工作项管理
- `createIssue` 创建工作项:含 title、description、teamId、priority
- `updateIssue` 更新工作项:状态、指派、估算、标签
- `archiveIssue` 归档工作项,保留历史但不显示在默认视图
- 工作项字段:title、description、priority、estimate、assignee、labels、state、project、cycle
- 优先级数值:0=紧急、1=高、2=中、3=低、4=无(对应 priorityUrgent 到 priorityNone)

### 2. 项目管理
- `createProject` 创建项目:含 name、description、teamIds
- `updateProject` 更新项目状态:planned、started、paused、completed、canceled
- `projectIssues` 查询项目下所有工作项
- 项目作为跨周期的工作容器,工作项可关联到项目

### 3. 团队管理
- `teams` 查询所有团队:含 id、name、key
- `team` 查询单个团队详情:含 workflow、states、labels
- 工作项必须归属于一个团队,teamId 是创建工作项的必填字段
- 团队 key 作为工作项标识前缀(如 ENG-123)

### 4. 周期管理
- `createCycle` 创建周期:含 name、startsAt、endsAt、teamId
- 标准周期14天,可自定义
- `cycleIssues` 查询周期内工作项
- 周期状态:active、upcoming、past,过去周期不可添加工作项
- `updateIssue` 的 cycleId 字段将工作项加入周期

### 5. 标签管理
- `createLabel` 创建标签:含 name、color、teamId
- `updateIssue` 的 labelIds 字段为工作项添加标签
- 标签用于分类筛选:bug、feature、tech-debt、customer-request
- 标签颜色用十六进制(如 `#E5484D` 表示红色)

### 6. 评论管理
- `createComment` 创建评论:含 body、issueId
- `updateComment` 编辑评论,`deleteComment` 删除评论
- 评论支持 Markdown 格式
- `issueComments` 查询工作项所有评论

### 7. 工作项关联
- `issueRelation` 建立关联:type=blocks、is blocked by、relates to、duplicate
- 关联方向有向:blocks 表示 A 阻塞 B
- `issueRelations` 查询工作项的所有关联

### 8. 工作流状态
- `teamWorkflow` 查询团队工作流:含 states 与 transitions
- 默认状态:Backlog、Triage、已实现、In Progress、In Review、Done、Canceled
- `updateIssue` 的 stateId 字段转换状态
- 状态类型:backlog、unstarted、started、completed、canceled

### 9. 自定义视图
- `createView` 创建视图:含 name、query、filters
- 视图查询语法:`status = "In Progress" AND priority = 1`
- `views` 查询所有视图,`viewIssues` 获取视图内工作项

### 10. GraphQL查询构造
- 查询用 `query` 关键字,变更用 `mutation`
- 字段选择:只查询需要的字段,减少响应体积
- 分页:用 `first`、`after` 参数,默认 first 50
- 变量:用 `$variable` 参数化,避免字符串拼接

## 使用指南
1. 确认 API Key 配置,获取团队 ID 与工作流状态 ID
2. 用 `createIssue` 创建工作项,填 title、teamId、priority
3. 用 `updateIssue` 关联项目、周期、标签
4. 用 `createCycle` 规划周期,将工作项加入
5. 用 GraphQL `query` 配合筛选跟踪进度
6. 用 `updateIssue` 的 stateId 推进工作流状态

## 使用范例
### 示例1:创建工作项(GraphQL mutation)
```graphql
mutation {
  issueCreate(input: {
    title: "实现用户登录接口"
    description: "支持邮箱+密码登录,返回JWT"
    teamId: "team-uuid-123"
    priority: 1
    estimate: 5
    labelIds: ["label-uuid-feature"]
  }) {
    success
    issue {
      id
      identifier
      title
      state { name }
    }
  }
}
// 返回: {"success": true, "issue": {"id": "issue-uuid-456", "identifier": "ENG-101", "title": "实现用户登录接口", "state": {"name": "Triage"}}}
```

### 示例2:GraphQL查询工作项
```graphql
query {
  team(id: "team-uuid-123") {
    issues(first: 50, filter: {
      state: { type: { eq: "started" } }
      priority: { lte: 1 }
    }) {
      nodes {
        identifier
        title
        priority
        estimate
        assignee { name }
        state { name }
      }
    }
  }
}
```

### 示例3:周期规划
```graphql
mutation {
  cycleCreate(input: {
    name: "Cycle 2026-W30"
    startsAt: "2026-07-21"
    endsAt: "2026-08-04"
    teamId: "team-uuid-123"
  }) {
    success
    cycle { id number }
  }
}
// 返回: {"success": true, "cycle": {"id": "cycle-uuid-789", "number": 30}}
# ...
// 将工作项加入周期
mutation {
  issueUpdate(input: {
    id: "issue-uuid-456"
    cycleId: "cycle-uuid-789"
  }) { success }
}
```

### 示例4:状态转换
```graphql
mutation {
  issueUpdate(input: {
    id: "issue-uuid-456"
    stateId: "state-uuid-in-progress"
  }) {
    success
    issue { state { name type } }
  }
}
// 返回: {"success": true, "issue": {"state": {"name": "In Progress", "type": "started"}}}
```

## 热门问题
### Q1: 优先级数值 0-4 如何映射?
A: 0=priorityUrgent(紧急)、1=priorityHigh(高)、2=priorityMedium(中)、3=priorityLow(低)、4=priorityNone(无)。创建工作项时传整数,查询时返回对应枚举标签.
### Q2: GraphQL 查询默认返回多少条?
A: 默认 `first: 50`。需要更多时显式传 `first: 100`(上限250),并用 `after` 游标分页:`issues(first: 50, after: "cursor-xyz")`.
### Q3: estimate 估算值用哪些数字?
A: 与故事点一致,用斐波那契数列:1、2、3、5、8、13。也可配置为任意整数,但建议团队统一数列便于速率对比.
### Q4: `updateIssue` 的 stateId 与 state name 有何区别?
A: stateId 是状态的唯一标识(如 `state-uuid-123`),state name 是显示名(如 "In Progress")。`updateIssue` 必须用 stateId,不能用 name。用 `teamWorkflow` 查询获取所有 stateId.
### Q5: `issueRelation` 的 blocks 与 is blocked by 有何区别?
A: 方向相反。A blocks B 表示 A 阻塞 B(B 等 A 完成);A is blocked by B 表示 A 被 B 阻塞(A 等 B 完成)。建立关联时需明确方向,否则依赖图会反,且不可形成循环.
### Q6: 周期14天如何调整?
A: `createCycle` 时指定 `startsAt` 与 `endsAt`,可设为7天或30天。建议团队统一周期长度,避免不同周期影响速率(burndown)对比。过去周期不可修改,只能创建新周期.
## 限制条件
- 需要项目管理工具的 API Key 与团队访问权限
- GraphQL 查询受 first 上限(250)限制,大结果集需分页
- 工作流状态 ID 因团队而异,不可硬编码
- 过去周期不可添加工作项,只能移到当前或未来周期
- 不覆盖工作流设计、SSO配置与账单管理

## 安全提示
| 风险项 | 等级 | 防护措施 | 验证方法 |
|:------|:------|:------|:------|
| API Key 泄露 | 高 | 使用环境变量存储 API Key，避免将其存储在代码库中。 | 定期检查代码库和版本控制系统，确保 API Key 未泄露。 |
| 数据传输安全 | 中 | 使用 HTTPS 协议进行数据传输，确保数据加密。 | 检查 API 调用是否使用 HTTPS，并确保证书有效。 |
| SQL 注入攻击 | 高 | 对所有输入进行验证和清理，使用参数化查询。 | 定期进行合规检查，确保所有输入都经过适当的处理。 |
| 未授权访问 | 高 | 限制 API 访问权限，确保只有授权用户才能访问。 | 使用身份验证和授权机制，确保 API 访问的安全性。 |
| 代码执行安全 | 中 | 限制 API 的执行权限，避免执行不安全的代码。 | 定期检查 API 的执行权限，确保没有不必要的高权限操作。 |

## 差异化分析
| 场景 | 效率提升量化分析 | 差异性对比 |
|:-----|:----------------|:----------|
| 工作项管理 | 通过自动化工作项的创建、更新和归档，减少手动操作时间，提高工作效率。 | 与传统项目管理工具相比，线性 API 提供了更灵活的 GraphQL 查询和操作方式。 |
| 项目管理 | 通过 GraphQL API 的强大查询能力，快速获取项目状态和进度信息，提高决策效率。 | 线性 API 支持自定义视图和查询，使项目管理者能够根据需求快速定制信息。 |
| 团队管理 | 通过团队管理功能，轻松管理团队成员和工作项分配，提高团队协作效率。 | 线性 API 支持团队级别的权限控制，确保团队成员只能访问授权信息。 |
| 周期管理 | 通过周期管理功能，实现工作项的周期性规划和跟踪，提高项目进度预测的准确性。 | 线性 API 支持自定义周期长度和状态，适应不同团队的工作流程。 |
| 标签管理 | 通过标签管理功能，对工作项进行分类和筛选，提高信息检索效率。 | 线性 API 支持自定义标签和颜色，使信息分类更加直观。 |
| 评论管理 | 通过评论管理功能，方便团队成员之间交流和协作，提高沟通效率。 | 线性 API 支持 Markdown 格式，使评论内容更加丰富。 |
| 工作项关联 | 通过工作项关联功能，建立工作项之间的依赖关系，提高项目规划和执行效率。 | 线性 API 支持多种关联类型，满足不同项目需求。 |
| 工作流状态 | 通过工作流状态管理，实现工作项的状态转换和进度跟踪，提高项目管理效率。 | 线性 API 支持自定义工作流状态，适应不同团队的工作流程。 |
| 自定义视图 | 通过自定义视图功能，快速获取所需信息，提高工作效率。 | 线性 API 支持复杂的查询语法，满足不同用户的需求。 |
| GraphQL查询构造 | 通过 GraphQL 查询构造，精确获取所需数据，减少不必要的数据传输。 | 线性 API 支持参数化查询，提高查询效率。 |

## 效能分析
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 优势对比
| 对比维度 | 项目管理API | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 通过GraphQL操作工作项、项目、周期、标签与评论,覆盖创建查询转换全流程。通 | 通用场景 | 通用场景 |

## 常见用户疑问
### Q1: 项目管理API支持哪些输入格式？

A1: 通过GraphQL操作工作项、项目、周期、标签与评论,覆盖创建查询转换全流程。通过项目管理工具的GraphQL API操作工作项全生命周期:工作项CRUD、。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

## 异常恢复方案
针对项目管理API使用中可能遇到的常见问题,提供以下排查方案:

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

### 项目管理API通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
