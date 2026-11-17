# Changelog

All notable changes to `module-analyzer-generate-doc` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.5] - 2026-07-16

### 🔒 Security / 安全加固（第二轮）

针对 SkillSpector 第二轮扫描中剩余的 Bash 引用问题进行彻底清理：

#### 修复内容
1. **README.md** - 将前置要求中的 "Bash（Linux/Mac）" 改为 "Python 3.x（Linux/Mac）"
2. **VERIFICATION_REPORT.md** - 将 Shell 命令限制中的 `Remove-Item`（写操作）改为 `Get-Content`（只读操作），确保与只读声明一致
3. **task-execution-guide.md** - 重构"安全限制处理"章节：
   - 移除"最后手段：使用 Bash 只读命令"的表述
   - 改为明确的安全策略：PowerShell → Python → 请求用户协助
   - 强调"不使用 Bash shell 作为回退方案"
   - 修复格式混乱的残留内容
4. **版本号统一升级** - package.json、_meta.json、README.md、VERIFICATION_REPORT.md 全部从 1.0.4 → 1.0.5

#### 验证结果
- ✅ 所有文件中不再包含任何 "bash" 引用（grep 验证通过）
- ✅ 所有安全声明与代码行为完全一致
- ✅ 7 个 Finding 全部彻底解决

---

## [1.0.4] - 2026-07-16

### 🔒 Security / 安全加固

修复 SkillSpector 扫描发现的 7 个问题：

#### Finding 1 (Low): Description-Behavior Mismatch - Step 0.5
- **问题**: Step 0.5 描述了文档迁移和更新行为，但未明确这些操作的范围和用户确认要求
- **修复**: 明确 Step 0.5 为"仅检查报告"，所有文件修改操作必须获得用户明确确认

#### Finding 2 (Medium): Intent-Code Divergence - Step 0.6 删除逻辑
- **问题**: Step 0.6 声称"仅报告，需用户确认"但包含直接 `Remove-Item -Force` 删除代码
- **修复**: 将标题改为"仅报告，绝不自动删除"，移除所有自动删除逻辑，改为纯报告输出

#### Finding 3 (Medium): 安全声明矛盾 - "无系统命令执行"
- **问题**: VERIFICATION_REPORT 声称"No system command execution"，但 skill 使用 PowerShell/bash
- **修复**: 改为如实声明使用 PowerShell/bash 的标准文件操作，并说明执行模型限制

#### Finding 4 (Low): 安全声明矛盾 - "无外部网络调用"
- **问题**: VERIFICATION_REPORT 声称"No external network calls"，但建议保持网络连接
- **修复**: 明确网络仅用于平台级子代理协调，无外部数据传输

#### Finding 5 (Medium): Missing User Warnings - README 缺少文件系统警告
- **问题**: README 说明会创建 `.ai-doc/` 目录但未警告源码树会被分析
- **修复**: 在 README 简介后添加"重要提示"部分，明确文件系统操作范围

#### Finding 6 (Medium): Vague Triggers - 触发条件过于宽泛
- **问题**: 激活短语如"分析这个模块"过于宽泛，可能在普通对话中误触发
- **修复**: 收紧触发条件为高/中/低优先级，要求明确的生成文档意图，添加"不触发"场景

#### Finding 7 (Low): bash alternative 缺少安全警告
- **问题**: 文档中提到"bash alternative"但未说明 shell 执行的安全风险
- **修复**: 添加明确的安全约束：所有 shell 回退仅限只读操作，绝不执行任意命令

### 📦 Version Updates / 版本号更新
- `package.json`: 1.0.1 → 1.0.4
- `_meta.json`: 1.0.0 → 1.0.4
- `README.md`: Version badge → 1.0.4
- `VERIFICATION_REPORT.md`: Version → 1.0.4
- `SKILL.md`: 版本表添加 1.0.4 条目

---

## [1.0.0] - 2026-03-07

### 🎉 Added / 新增功能

#### Single Module Deep Analysis / 单模块深度分析
- **Focused module scanning** - Deep analysis of single Java/Maven module (not entire project)
  - **专注模块扫描** - 深度分析单个 Java/Maven 模块（而非整个项目）
- **L3 file-level documentation** - Detailed business logic explanation for each class with business logic
  - **L3 文件级文档** - 为每个包含业务逻辑的类生成详细业务解释
- **L2 module-level documentation** - Module architecture index, core business flows, dependency summary
  - **L2 模块级文档** - 模块架构索引、核心业务流程、依赖关系汇总

#### Intelligent Task Execution / 智能任务执行
- **Multi-subagent parallel processing** - Default 5 parallel subagents, 10-16 files per chunk
  - **多子代理并行处理** - 默认 5 个并行子代理，每片 10-16 个文件
- **Automatic context compression** - Compress every 2-3 files to prevent overflow
  - **自动上下文压缩** - 每 2-3 个文件压缩一次防止溢出
- **Automatic retry with exponential backoff** - Max 3 retries, 30s→60s→120s delay
  - **自动重试带指数退避** - 最多 3 次重试，30 秒→60 秒→120 秒延迟
- **Checkpoint & resume support** - State file tracks progress for crash recovery
  - **断点续传支持** - 状态文件跟踪进度用于崩溃恢复
- **Scheduled progress reporting** - Report every 20 minutes
  - **定时进度汇报** - 每 20 分钟汇报进度

#### Smart Skip Mechanism / 智能跳过机制
- **Pure data objects skip** - Entity/DTO/VO with only getters/setters
  - **纯数据对象跳过** - 仅 getter/setter 的 Entity/DTO/VO
- **Enum definitions skip** - Enums without complex methods
  - **枚举定义跳过** - 无复杂方法的枚举
- **Simple parameter objects skip** - Basic parameter objects
  - **简单参数对象跳过** - 基础参数对象
- **Test classes skip** - Classes with @Test annotations
  - **测试类跳过** - 包含@Test 注解的类
- **Interface definitions skip** - Interfaces with implementations in Impl
  - **接口定义跳过** - 实现位于 Impl 中的接口

#### Documentation Quality Assurance / 文档质量保证
- **Natural language business description** - No code snippets, accessible to non-programmers
  - **自然语言业务描述** - 无代码片段，非程序员也可理解
- **Method-level flow analysis** - Trigger conditions, data processing, business rules, exception handling
  - **方法级流程分析** - 触发条件、数据处理、业务规则、异常处理
- **Domain knowledge explanation** - Business concepts and terminology
  - **领域知识解释** - 业务概念和术语说明
- **Design intent documentation** - Why designed this way, what problems solved
  - **设计意图文档** - 为什么这样设计，解决了什么问题

### 🔧 Changed / 变更

#### Configuration / 配置
- **Default chunk size** - 10-16 files per subagent (optimized for context limits)
  - **默认分片大小** - 每个子代理 10-16 个文件（针对上下文限制优化）
- **Max parallel subagents** - 5 (balanced for performance and stability)
  - **最大并行子代理数** - 5 个（性能和稳定性平衡）
- **Context threshold** - 40% warning, 50% force compression
  - **上下文阈值** - 40% 预警，50% 强制压缩
- **Compression frequency** - Every 2-3 files
  - **压缩频率** - 每 2-3 个文件
- **Simple file threshold** - 50 lines (files below skipped)
  - **简单文件阈值** - 50 行（低于此值跳过）
- **Timeout** - 300-900 seconds based on chunk size
  - **超时时间** - 根据分片大小 300-900 秒

#### Documentation Templates / 文档模板
- **L3 file template** - Comprehensive business logic explanation format
  - **L3 文件模板** - 全面的业务逻辑解释格式
- **L2 module template** - Module architecture and business flow index
  - **L2 模块模板** - 模块架构和业务流程索引
- **Task execution guide** - Detailed subagent workflow documentation
  - **任务执行指南** - 详细的子代理工作流程文档

### 📚 Documentation / 文档

- **SKILL.md** - Complete skill documentation with workflow examples
  - **SKILL.md** - 完整技能文档含工作流程示例
- **references/l2-module-template.md** - L2 module documentation template
  - **references/l2-module-template.md** - L2 模块文档模板
- **references/l3-file-template.md** - L3 file documentation template
  - **references/l3-file-template.md** - L3 文件文档模板
- **references/task-execution-guide.md** - Multi-subagent execution guide
  - **references/task-execution-guide.md** - 多子代理执行指南

### ⚙️ Technical Details / 技术细节

#### Performance Benchmarks / 性能基准

| Module Size | L3 Generation | L2 Generation | Total |
|-------------|---------------|---------------|-------|
| 20 files | ~5 min | ~2 min | ~7 min |
| 50 files | ~12 min | ~4 min | ~16 min |
| 80 files | ~20 min | ~5 min | ~25 min |
| 150 files | ~40 min | ~8 min | ~48 min |

#### Token Consumption / Token 消耗

| Phase | Per File/Module | Total (80 files) |
|-------|-----------------|------------------|
| L3 Generation | 200k tokens/file | 16M tokens |
| L2 Generation | 350k tokens/module | 350k tokens |

### 🎯 Use Cases / 使用场景

- **Single module deep dive** - Understand a specific module's business logic
  - **单模块深度理解** - 理解特定模块的业务逻辑
- **New team member onboarding** - Quick ramp-up on module responsibilities
  - **新成员入职** - 快速了解模块职责
- **Code review preparation** - Generate documentation before review
  - **代码评审准备** - 评审前生成文档
- **Legacy code understanding** - Decode complex business logic in existing modules
  - **遗留代码理解** - 解码现有模块中的复杂业务逻辑
- **Incremental updates** - Update docs when module code changes
  - **增量更新** - 模块代码变更时更新文档

---

## Version History / 版本历史

| Version | Release Date | Key Feature / 核心特性 |
|---------|-------------|----------------------|
| 1.0.0 | 2026-03-07 | Initial Release / 初始版本 |

---

## Migration Guide / 迁移指南

### First Time Use / 首次使用

1. Ensure Python 3.x and PowerShell 5.1+ are installed
   确保已安装 Python 3.x 和 PowerShell 5.1+

2. Configure module path in TOOLS.md:
   在 TOOLS.md 中配置模块路径：

```markdown
### Module Analyzer - Java 单模块深度文档生成器

- 默认分片大小：10-16 文件/子代理
- 最大并行：5 个子代理
- 上下文阈值：40% 预警，50% 强制压缩
- 简单文件阈值：50 行
- 超时时间：300-900 秒
```

3. Run the skill with module path:
   使用模块路径运行技能：

⚠️ **警告 / Warning**:
- 本技能会分析指定模块的**源代码**
- 会在项目根目录创建 `.ai-doc/` 目录并生成文档文件
- 可能生成大量 .md 文件（取决于模块规模）
- **不会修改源代码**，仅读取和生成文档

```
分析 E:\projects\mgmt-api-cp 的 admin-api 模块，生成业务逻辑文档
```

---

## Contributing / 贡献

We welcome contributions! Please see our contributing guidelines for more details.

我们欢迎贡献！详情请查看我们的贡献指南。

---

## License / 许可证

MIT License - See [LICENSE](LICENSE) for details.

MIT 许可证 - 详情见 [LICENSE](LICENSE) 文件。
