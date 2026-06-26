# MemDDC

## 技能信息

- **技能名称**: MemDDC
- **版本**: 1.0.2
- **作者**: qihao123
- **描述**: 面向团队协作的项目文档管理与代码迭代智能工具，提供自动文档生成、DDD模型管理、记忆压缩、代码风格统一和智能触发功能
- **触发关键词**: MemDDC, 加载记忆约束修改, 按DDD契约迭代更新, memddc-init, memddc-update, memddc-sync
- **适用场景**: 团队协作开发、复杂架构迭代、遗留系统持续重构、长期多人维护工程AI约束治理

## 快速定位约定

当用户提出涉及具体实体（如 SysDept）或模块（如 system/dept）的修改需求时：

- 第一步：查询 `mem-snapshot.json` 的 `index` 层获取文件路径
- 第二步：读取目标文件
- 禁止在未查索引前进行大规模文件探索

## 实战交互契约

用户说"memddc-sync"或"MemDDC 更新"时：

1. 执行 `git diff --name-only` 获取变更文件列表
2. 将变更文件与 `mem-snapshot.json` 中的模块/实体/API 列表匹配
3. 仅更新受影响的 Markdown 文档段落
4. 更新 snapshot 中标记的字段，其余原样保留

用户提出代码修改需求时：

1. 优先加载 `mem-snapshot.json`
2. 根据 snapshot 中的模块和关键类列表定位相关文件
3. 先输出变更蓝图（影响文件清单），经用户确认后再执行修改

## 记忆快照 (mem-snapshot.json)

采用三级索引结构，便于 AI 快速定位与约束注入：

1. `metadata` — 项目元信息
   - 名称、版本、技术栈、代码规模统计
   - 供 AI 快速识别项目特征

2. `index` — 可查询的文件索引
   - `entities`: 核心实体 → 文件路径、所属模块、对应表名
   - `controllers`: Controller → 文件路径、basePath
   - `services`: ServiceImpl → 文件路径、interface、模块
   - `mappers`: Mapper → java 路径、xml 路径、表名
   - `apis`: 前端 API 封装 → 文件路径
   - `views`: 前端页面 → 文件路径
   - `modules`: 模块职责说明
   - `relations`: 核心实体关联映射（entity→mapper→service→controller→view）
     - 示例：`SysDept` → `{entity, mapper, service, controller, views[]}`
     - AI 修改具体实体时，按 ID 查表定位相关文件，无需探索性读取

3. `context` — 上下文约束
   - `vcsSummary`: 提交规律与近期变更主题
   - `structureAnalysis`: 架构模式与潜在问题
   - `patterns`: 高频设计模式（如 treeBuild、pagination、permission、crudApi）
   - `codeStyle`: 命名规范、返回值类型、注解写法
   - `constraints`: 业务常量映射（状态、类型、数据范围等）

## 团队协作

- **团队共享目录**: `.memddc/`
- **共享配置**: `config.json` 中的 `team.syncBranch`
- **冲突提示**: 当 `mem-snapshot.json` 与 Git 状态不一致时，提示用户先执行 `memddc-sync`

## 目录结构

### v1.0.2 新版目录结构

```
project/
├── .memddc/                          # MemDDC 统一存储目录（团队共享）
│   ├── config.json                   # 团队共享配置
│   ├── mem-snapshot.json             # 全局记忆快照（核心）
│   ├── vcs-log-raw.txt              # 原始VCS日志（最近100条）
│   ├── vcs-log-analysis.md           # AI整理的VCS日志分析
│   ├── file-tree-raw.txt            # 原始文件树
│   ├── file-tree-analysis.md        # AI文件结构分析
│   ├── docs/                        # 项目文档（用户可添加）
│   │   ├── user-docs/              # 用户文档目录（AI会分析其中的业务文档）
│   │   ├── architecture.md          # 架构文档
│   │   ├── business.md             # 业务文档
│   │   ├── api.md                  # API接口文档
│   │   ├── database.md             # 数据库设计文档
│   │   ├── development.md          # 开发指南
│   │   ├── code-style.md           # 代码风格指南
│   │   ├── [language-specific].md # 语言专属文档
│   │   ├── [architecture-specific].md # 架构专属文档
│   │   └── diagrams/               # 图表文档（Mermaid）
│   │       ├── architecture.mmd
│   │       ├── flow.mmd
│   │       ├── sequence.mmd
│   │       └── er.mmd
│   ├── ddd-model.md                 # DDD领域模型
│   ├── snapshots/                   # 历史快照存档
│   │   ├── docs-compressed.zip     # 文档压缩包
│   │   └── mem-YYYYMMDD-HHMMSS.json # 时间戳快照
│   ├── logs/                        # 操作日志
│   │   └── sync-YYYYMMDD.log
│   └── .gitignore                  # 团队共享的git忽略规则
└── [项目源代码目录]
```

### 配置文件 (config.json)

```json
{
  "version": "1.0.2",
  "project": {
    "name": "项目名称",
    "type": "backend|frontend|mobile|microservice",
    "language": "java|python|go|javascript|typescript|rust",
    "framework": "spring|django|gin|react|vue|flask",
    "architecture": "mvc|mvvm|ddd|microservice|serverless|monolithic"
  },
  "team": {
    "shared": true,
    "members": ["member1@example.com", "member2@example.com"],
    "syncBranch": "main"
  },
  "triggers": {
    "codeChange": true,
    "structureChange": true,
    "configChange": true,
    "manual": true,
    "scheduled": false,
    "scheduleCron": "0 2 * * *"
  },
  "document": {
    "types": ["architecture", "business", "api", "database"],
    "includeDiagrams": true,
    "autoUpdate": true,
    "analyzeUserDocs": true
  },
  "vcs": {
    "enabled": true,
    "logLimit": 100,
    "types": ["git", "svn"]
  },
  "fileAnalysis": {
    "enabled": true,
    "includeIdeIndexes": true
  },
  "compression": {
    "level": 7,
    "excludePatterns": ["*.log", "*.tmp", "node_modules/**"],
    "contextLimit": 128000,
    "autoCompressThreshold": 0.8
  }
}
```

## 工作流程

### v1.0.2 初始化阶段（核心升级）

1. **VCS日志拉取**
   - 检测版本控制系统类型（Git/SVN）
   - 执行 `git log --pretty=format:"%h %s %b" -n 100` 或 `svn log --limit 100`
   - 保存原始日志到 `.memddc/vcs-log-raw.txt`

2. **AI日志分析**
   - 将原始日志发送给AI分析
   - AI提取：提交规律、关键版本、团队协作模式、业务变更周期
   - 保存分析结果到 `.memddc/vcs-log-analysis.md`

3. **文件树扫描**
   - 递归扫描项目目录结构
   - 收集IDE索引文件（如存在）
   - 保存到 `.memddc/file-tree-raw.txt`

4. **AI结构分析**
   - 将文件结构发送给AI分析
   - AI评估：模块划分、依赖关系、潜在问题
   - 保存分析结果到 `.memddc/file-tree-analysis.md`

5. **用户文档分析**
   - 扫描 `.memddc/docs/user-docs/` 目录
   - 将用户文档发送给AI提取业务上下文
   - 提取：业务流程、业务术语、需求规则

6. **代码扫描与文档生成**
   - 全量代码AST扫描
   - 生成适配项目的结构化文档
   - 构建DDD领域模型

7. **关联映射构建**
   - 扫描核心实体（Controller/Service/Mapper/Entity）
   - 自动构建 entity→mapper→service→controller→view 的关联映射
   - 写入 `mem-snapshot.json` 的 `relations` 字段

8. **整合写入快照**
   - 将VCS分析、文件结构分析、业务上下文整合
   - 生成包含全部上下文信息的 `mem-snapshot.json`

### memddc-sync 增量流程

1. 执行 `git diff --name-only` 获取变更文件
2. 分类：代码文件→更新文档 / 用户文档→更新业务上下文 / 配置文件→更新技术栈说明
3. AI 输出影响面判断：`{"affectedDocs": [...], "snapshotFields": [...]}`
4. 精准读取并更新受影响内容
5. 写入新 snapshot，保留未变更字段

### 迭代修改阶段

1. 快速记忆加载：读取 mem-snapshot.json
2. 变更感知：了解本次需要修改的范围和内容
3. 文件定位：根据需求关键词查询 `index` 层（entities / services / mappers / views 等），精准定位相关文件路径
4. DDD约束：确保修改符合领域模型和业务契约
5. 模式约束：参考 `context.patterns` 和 `context.codeStyle`，保持与项目现有约定一致
6. 一致性保证：修改完成后自动同步更新相关文档

### 同步闭环阶段

1. 比对代码变更
2. 更新相关文档
3. 同步DDD模型
4. 重新分析VCS日志和文件结构（如有变化）
5. 更新记忆快照
6. 验证多者一致
7. 按三级索引结构写入 `mem-snapshot.json`
8. **容量检查**：快照大小超过上下文限制80%时触发压缩
   - Level 1：精简描述
   - Level 2：只保留关键字段
   - 最小保证：模块列表、关键API、约束规则

## 技术实现

### 核心模块

1. **项目扫描器**
   - 深度目录结构分析
   - 多语言源码解析
   - 依赖关系分析
   - API接口分析
   - 数据库逻辑分析
   - 配置文件分析
   - 变更检测器

2. **策略选择器**
   - 项目类型识别
   - 编程语言识别
   - 框架识别
   - 架构模式识别
   - 最优策略匹配

3. **文档生成器**
   - 架构文档生成
   - 业务文档生成
   - API文档生成
   - 数据库文档生成
   - 语言专属文档生成
   - 架构专属文档生成
   - Mermaid图表生成

4. **DDD模型构建器**
   - 限界上下文识别
   - 聚合根分析
   - 实体边界定义
   - 值对象设计
   - 领域服务提取
   - 领域事件识别

5. **记忆管理系统**
   - 智能文档压缩
   - 记忆快照生成
   - 历史决策记录
   - 上下文注入
   - 增量更新
   - 冲突检测
   - **容量检查**: 快照大小超过上下文限制80%时自动压缩

6. **变更追踪器**
   - 代码变更检测
   - 文档同步更新
   - 模型一致性验证
   - 影响分析

7. **团队协作器**
   - 配置同步
   - 冲突检测
   - 权限管理
   - 版本控制集成

## 技术栈支持

| 技术栈 | 文档生成 | DDD建模 | 记忆压缩 |
|--------|---------|---------|---------|
| Java/Spring Boot | ✅ | ✅ | ✅ |
| Python/Django/Flask | ✅ | ✅ | ✅ |
| Node.js/Express/Nest | ✅ | ✅ | ✅ |
| Go/Gin | ✅ | ✅ | ✅ |
| 前端框架 | ✅ | ⚠️ | ✅ |
| 微服务 | ✅ | ✅ | ✅ |

## 注意事项

1. **首次使用**: 确保项目目录存在且包含源码文件
2. **权限要求**: 需要对项目目录和 `.memddc` 目录有读写权限
3. **版本控制**: 建议将 `.memddc` 目录纳入版本控制
4. **文档维护**: 代码变更后及时运行更新命令

## 故障排除

### 初始化失败

- 检查项目目录权限
- 确保项目中包含足够的源码文件
- 查看 `.memddc/logs/` 下的日志文件

### 文档未同步

- 运行 `MemDDC 更新` 手动同步
- 检查 `config.json` 中的 `autoUpdate` 配置

### Token消耗未降低

- 确认 `.memddc/mem-snapshot.json` 存在
- 尝试开启新对话再触发技能
- 检查文档是否过大（可考虑精简）

## 版本历史

- **v1.0.2** - 当前稳定版 (推荐)
  - VCS日志分析：Git/SVN日志AI整理写入快照
  - 文件结构分析：IDE索引和目录树AI分析
  - 用户文档纳入：docs目录文档自动业务分析
  - 三级索引结构：metadata/index/context
  - 关联映射：entity→mapper→service→controller→view
  - 实测降低 Token 消耗：项目说明 36%，业务修改 53%

- **v1.0.1** - 历史版本
  - 完整的文档生成和DDD建模
  - 智能记忆压缩
  - 团队协作支持

- **v1.0.0** - 初始版本
  - 基础文档生成
  - 简单DDD模型

## 许可协议

MIT License

## 联系方式

- 项目主页: <https://github.com/qihao123/memddc-ai-skill>
- 作者: qihao123
- 邮件: <qihoo2017@gmail.com>
