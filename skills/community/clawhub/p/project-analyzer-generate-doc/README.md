# project-analyzer-generate-doc Skill

> Java Maven 工程智能文档生成器 - 让 AI 全面理解你的工程架构

---

## 📖 简介

本 Skill 通过**自底向上**的完整流程（L3 → L2 → L1），为 Java/Maven/MyBatis 工程生成三层级文档索引：

- **L3 文件级**: 每个 Java/XML 文件生成详细业务逻辑文档
- **L2 模块级**: 汇总模块内所有文件，生成模块架构文档
- **L1 项目级**: 汇总所有模块，生成系统架构全景文档

**核心优势**:
- ✅ 深度支持 Java 技术栈（MyBatis、Maven、Spring Boot）
- ✅ 任务状态实时跟踪与监控
- ✅ 自动重试机制（最多 3 次）
- ✅ 断点续传支持
- ✅ 子代理健康检查
- ✅ 进度百分比报告
- ✅ 智能文档迁移与合并
- ✅ 使用子代理分片策略，规避上下文限制
- ✅ 严格的上下文压缩，确保任务稳定性

---

## 🚀 快速开始

### 环境要求

| 工具 | 版本 | 用途 |
|------|------|------|
| PowerShell | 5.1+ | 执行脚本 |
| Git | 2.x+ | 增量更新检测 |
| OpenClaw | 最新 | 子代理调度 (sessions_spawn) |
| Java | 17+ | 目标项目语言 (可选) |

### 激活方式

**方式 1: 直接对话激活**
```
用户：为 E:\projects\mgmt-api-cp 生成业务逻辑文档

AI: 收到！开始执行完整流程...
```

**方式 2: 指定输出路径**
```
用户：为 E:\projects\mgmt-api-cp 生成文档，输出到 D:\docs\mgmt-api-cp

AI: 收到！文档将生成到 D:\docs\mgmt-api-cp\.ai-doc\
```

### 完整流程

```
1. 扫描项目结构（统计模块和文件数）
2. 检查.ai-doc 目录，执行文档迁移合并（如果存在）
3. 制定分片计划（大模块拆分为多个子代理）
4. 并行生成 L3 文档（每片 8-12 文件，严格上下文压缩）
5. 汇总生成 L2 文档（所有 L3 完成后）
6. 生成 L1 文档（所有 L2 完成后）
7. Git 提交文档（可选）
```

---

## 📁 文件结构

```
project-analyzer-generate-doc/
├── SKILL.md                          # 主技能文档
├── README.md                         # 使用说明
├── templates/                        # 文档模板
│   ├── l1-template.md
│   ├── l2-template.md
│   ├── l3-template.md
│   └── gitignore-template.txt
├── references/                       # 参考指南
│   ├── context-compression.md
│   ├── checkpoint-resume.md
│   ├── incremental-update.md
│   └── subagent-task-template.md
├── examples/                         # 真实案例样例
│   ├── l1-example.md
│   ├── l2-example.md
│   └── l3-example.md
└── scripts/                          # 执行脚本
    └── generate-l3-doc.ps1

生成的文档结构（目标工程）:
<项目根目录>/.ai-doc/
├── .generate-state.json              # 任务状态文件（断点续传）
├── .task-log.md                      # 执行日志
├── project.md                        # L1 项目级
├── <module1>.md                      # L2 模块级
├── <module2>.md
└── <project-name>/
    ├── <module1>/                    # L3 文件级
    │   ├── src/main/java/.../ClassA.java.md
    │   └── src/main/resources/.../Mapper.xml.md
    └── <module2>/
        └── ...
```

---

## 🎯 使用场景

### 1. 新工程文档化

```
用户：为 E:\projects\mgmt-api-cp 生成完整文档

AI: 执行完整流程 L3→L2→L1，生成 355 个文档
📊 实时进度报告，每 5 分钟更新
✅ 自动重试失败的任务
💾 断点续传支持
```

### 2. 增量更新

```
用户：ces-domain 模块有代码变更，更新文档

AI: 检测变更文件 → 更新对应 L3 → 重新汇总 L2 → 更新 L1 统计
```

### 3. 断点续传

```
用户：继续之前的文档生成任务

AI: 检测到未完成的生成任务...
- 项目：E:\projects\mgmt-api-cp
- 完成进度：L3 阶段 45.5% (142/312 文件)
是否从断点继续？(y/n)
```

### 4. 单模块生成

```
用户：只生成 business-api 模块的文档

AI: 执行单模块流程 L3→L2（不生成 L1）
```

---

## 📊 任务监控

### 进度报告

**报告频率**: 每 5 分钟或每完成 10% 进度

**报告内容**:
```markdown
## 📊 文档生成进度报告

**项目**: mgmt-api-cp
**已用时间**: 15 分钟
**总体进度**: 45.5%

[████████████░░░░░░░░░░░] 45.5%

### 当前阶段：L3 文件级文档生成

| 模块 | 文件数 | 已完成 | 进度 |
|------|--------|--------|------|
| ces-domain | 109 | 65 | 59.6% |
| admin-api | 53 | 28 | 52.8% |
| business-api | 82 | 35 | 42.7% |

### 子代理状态

| 子代理 | 状态 | 文件数 | 重试 |
|--------|------|--------|------|
| L3-ces-domain-chunk1 | ✅ 完成 | 12 | 0 |
| L3-admin-api-chunk1 | 🔄 运行中 | 7/12 | 1 |

### 预计完成时间

- L3 阶段：约 25 分钟（剩余 60%）
- L2 阶段：约 10 分钟
- L1 阶段：约 3 分钟
- **总计**: 约 38 分钟
```

### 任务状态文件

**位置**: `.ai-doc/.generate-state.json`

**内容**:
```json
{
  "version": "2.1.0",
  "projectPath": "E:\\projects\\mgmt-api-cp",
  "startTime": "2026-03-05T15:30:00+08:00",
  "currentPhase": "L3",
  "overallProgress": 45.5,
  "phases": {
    "L3": {
      "status": "in_progress",
      "totalFiles": 312,
      "processedFiles": 142,
      "skippedFiles": 65,
      "failedFiles": 3
    },
    "L2": { "status": "pending" },
    "L1": { "status": "pending" }
  },
  "canResume": true
}
```

---

## 🔄 重试机制

### 重试策略

```yaml
max_retries: 3                    # 最大重试次数
initial_delay: 30                 # 初始延迟（秒）
backoff_multiplier: 2             # 延迟倍增因子
max_delay: 300                    # 最大延迟（秒）
```

### 可重试错误

- ✅ timeout - 子代理超时
- ✅ context_overflow - 上下文溢出
- ✅ file_access_error - 文件访问错误
- ✅ subagent_crash - 子代理崩溃

### 不可重试错误

- ❌ invalid_project_path - 项目路径无效
- ❌ permission_denied - 权限不足
- ❌ disk_full - 磁盘已满

---

## ⚙️ 配置项

在 `TOOLS.md` 中添加：

```markdown
### Project Analyzer - Java 工程智能文档生成器

- 默认分片大小：10 文件/子代理
- 上下文阈值：40% 预警，50% 强制压缩
- 最大并行：8 子代理
- 简单文件阈值：50 行
- 超时时间：300 秒（基础），1000 秒（大文件）
- 重试策略：最多 3 次，指数退避
- 健康检查：每 60 秒
- 进度报告：每 5 分钟或 10% 进度
- 断点续传：自动保存状态
```

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-03-05 | 增强任务监控、重试机制、健康检查、断点续传 |
| 2.0.0 | 2026-03-05 | 重大更新，增加 Java 特定支持、MyBatis 分析、文档迁移合并 |
| 1.1.0 | 2026-03-03 | 添加断点续传、增量更新、L1 样例 |
| 1.0.0 | 2026-03-03 | 初始版本，基于 Infypower Energy AI 项目实战经验 |

---

## 🔧 包装与发布

### 本地测试

```powershell
# 验证 skill 结构
Test-Path D:\ai\workspace\skills\project-analyzer-generate-doc\SKILL.md

# 检查所有必需文件
ls D:\ai\workspace\skills\project-analyzer-generate-doc\
```

### 发布到 ClawHub

```bash
# 使用 clawhub CLI 发布
clawhub publish project-analyzer-generate-doc --version 2.1.0
```

---

## 📊 性能参考

### 生成时间

| 工程规模 | 文件数 | 预计时间 |
|----------|--------|----------|
| 小型 | 50 文件 | ~13 分钟 |
| 中型 | 200 文件 | ~50 分钟 |
| 大型 | 500 文件 | ~4 小时 |

### Token 消耗

| 阶段 | 每文件/模块 | 200 文件总计 |
|------|-------------|--------------|
| L3 生成 | 200k tokens | 40M tokens |
| L2 生成 | 250k tokens | 1.75M tokens |
| L1 生成 | 600k tokens | 600k tokens |

---

## ⚠️ 已知限制

1. **执行逻辑依赖框架**: 当前实现依赖 OpenClaw 的 `sessions_spawn` 能力
2. **上下文压缩依赖自觉**: 压缩策略需要子代理主动执行
3. **增量更新需手动触发**: git diff 检测需要额外配置

---

## 🔮 待改进项

- [ ] 添加自动化压缩钩子（如果框架支持）
- [ ] 完善增量更新流程图和变更传播规则
- [ ] 支持更多语言（Python/TypeScript/Go）
- [ ] 添加文档质量检查（检测过期文档）
- [ ] 支持 MyBatis XML 与 Java 方法的自动关联分析

---

## 🔗 相关资源

- [SKILL.md](SKILL.md) - 完整技能文档
- [templates/](templates/) - 文档模板
- [references/](references/) - 参考指南
- [examples/](examples/) - 真实案例样例
- [ClawHub](https://clawhub.com) - 查找更多 skill

---

## 📄 许可证

MIT License
