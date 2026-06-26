---
name: project-analyzer-generate-doc
description: Java Maven multi-module project documentation generator. Supports MyBatis SQL mapping, Maven dependency analysis, generates L3(file-level) to L2(module-level) to L1(project-level) hierarchical docs. Features task monitoring, auto-retry, checkpoint resume, and health checks.
---

# Project Analyzer Generate Doc - Java 工程智能文档生成器

> 深度支持 Java/Maven/MyBatis 工程的分层文档生成器 - 让 AI 全面理解你的工程架构

## 核心特性

**深度 Java 技术栈支持**: 
- MyBatis Mapper 与 XML 映射分析
- Maven 依赖关系解析
- Spring Boot 配置解析
- 复杂业务逻辑自然语言描述

**智能任务管理**:
- ✅ 任务状态实时跟踪
- ✅ 自动重试机制（最多 3 次）
- ✅ 断点续传支持
- ✅ 子代理健康检查
- ✅ 进度百分比报告

**智能文档管理**:
- 已有文档智能迁移与合并
- 按源码路径结构同步 MD 文档位置
- 重复文档内容去重与整合

**细粒度分析能力**:
- 方法级别业务逻辑分解
- 超大文件智能切分分析
- 完整的 Java 源码解析

## 核心原则

**严格自底向上流程**: `L3 (所有文件) → L2 (所有模块) → L1 (项目全局)`

**绝不跳过任何步骤**: 必须等所有 L3 完成 → 才能生成 L2 → 必须等所有 L2 完成 → 才能生成 L1

**上下文压缩**: 每处理 2-3 个文件自动压缩已处理内容，只保留路径 +1 行摘要

**子代理分片**: 大模块拆分为多个子代理并行处理，每片 8-12 个文件

---

## 激活条件

当用户提到以下关键词时激活：
- "生成项目文档"
- "分析工程架构"
- "创建代码索引"
- "理解这个工程"
- "为 AI 分析准备文档"
- "Java 工程文档"
- "Maven 项目分析"
- "MyBatis SQL 分析"
- "业务逻辑文档"
- "三层级文档"
- "L1/L2/L3 文档"

---

## 文档层级结构

```
项目根目录/
├── .ai-doc/                          # 📁 默认输出目录
│   ├── .generate-state.json          # 📊 任务状态文件（断点续传）
│   ├── .task-log.md                  # 📝 执行日志
│   ├── project.md                    # L1: 项目级架构索引 (~10KB)
│   ├── module-a.md                   # L2: 模块级索引 (~5-15KB)
│   ├── module-b.md
│   └── <模块名>/                     # L3: 文件级文档
│       ├── src/main/java/com/company/ModuleClass.java.md
│       ├── src/main/resources/mapper/ModuleMapper.xml.md
│       └── ...
├── src/
│   └── ...                           # 源代码
└── pom.xml                           # 项目配置
```

**默认输出路径**: `<项目根目录>/.ai-doc/`

**可选自定义**: 通过 `-OutputPath` 参数指定其他位置

---

## 完整工作流程

### 📋 Step 0: 项目扫描与规划

```powershell
# 1. 扫描所有模块 (排除 target, .git, build 等临时目录)
Get-ChildItem <项目路径> -Directory | Where-Object { $_.Name -notmatch 'target|\.git|build|dist|node_modules' }

# 2. 统计每个模块的关键文件数
$javaFiles = Get-ChildItem "$module" -Include *.java -Recurse | Measure-Object
$xmlFiles = Get-ChildItem "$module" -Include *.xml -Recurse | Where-Object { $_.Name -match 'mapper|Mapper' } | Measure-Object
$propertiesFiles = Get-ChildItem "$module" -Include *.properties,*.yml,*.yaml -Recurse | Measure-Object

# 3. 解析 Maven 依赖 (读取 pom.xml)
$dependencyTree = @()
foreach ($pom in Get-ChildItem "$module" -Include pom.xml -Recurse) {
    [xml]$pomXml = Get-Content $pom.FullName
    $dependencyTree += $pomXml.project.dependencies.dependency
}

# 4. 制定分片策略
# - <15 文件：单子代理
# - 15-40 文件：2-3 个子代理分片
# - >40 文件：按目录拆分为多个子代理
```

**输出**: 模块列表 + 文件数统计 + 分片计划 + 依赖关系图

---

### 📁 Step 0.5: 文档迁移与合并（如果.ai-doc 已存在，需用户确认）

**目的**: 整理已存在的文档，使其与源码路径结构匹配

**⚠️ 安全约束**: 执行任何移动/合并/删除操作前，必须**明确询问用户并获得确认**

```powershell
# 1. 扫描.ai-doc 目录下的所有.md 文件
$existingDocs = Get-ChildItem <项目路径>/.ai-doc -Include *.md -Recurse

# 2. 根据文档路径推断对应的源码路径
$migrationPlan = @()
foreach ($doc in $existingDocs) {
    $relativePath = $doc.FullName.Replace("<项目路径>/.ai-doc\", "")
    $expectedSourcePath = $relativePath.Replace(".md", "")
    
    # 3. 查找实际源码路径是否存在
    $actualSourcePath = $null
    foreach ($extension in @(".java", ".xml", ".kt", ".scala")) {
        $potentialPath = "<项目路径>\$expectedSourcePath$extension"
        if (Test-Path $potentialPath) {
            $actualSourcePath = $potentialPath
            break
        }
    }
    
    # 4. 如果源码路径不存在，尝试模糊匹配
    if (!$actualSourcePath) {
        # 在整个项目中查找同名文件
        $matches = Get-ChildItem "<项目路径>" -Include "*$expectedSourcePath*" -Recurse
        if ($matches.Count -eq 1) {
            $actualSourcePath = $matches[0].FullName
        }
    }
    
    # 5. 如果找到对应的源码路径，验证路径是否正确
    if ($actualSourcePath) {
        $correctDocPath = $actualSourcePath.Replace("<项目路径>\", "<项目路径>/.ai-doc\") + ".md"
        
        if ($doc.FullName -ne $correctDocPath) {
            $migrationPlan += @{
                Source = $doc.FullName
                Destination = $correctDocPath
                Action = if (Test-Path $correctDocPath) { "merge" } else { "move" }
            }
        }
    }
}

# 6. 向用户展示迁移计划，请求确认
if ($migrationPlan.Count -gt 0) {
    Write-Host "发现 $($migrationPlan.Count) 个文档需要迁移/合并:"
    foreach ($plan in $migrationPlan) {
        Write-Host "  $($plan.Action): $($plan.Source) → $($plan.Destination)"
    }
    
    # ⚠️ 必须获得用户明确确认
    $confirm = Read-Host "是否执行迁移计划？(y/n)"
    if ($confirm -eq "y") {
        foreach ($plan in $migrationPlan) {
            $targetDir = Split-Path $plan.Destination -Parent
            if (!(Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force
            }
            
            if ($plan.Action -eq "merge") {
                $existingContent = Get-Content $plan.Destination -Raw
                $newContent = Get-Content $plan.Source -Raw
                $mergedContent = Merge-Documents $existingContent $newContent
                Set-Content -Path $plan.Destination -Value $mergedContent
                Remove-Item $plan.Source
            } else {
                Move-Item -Path $plan.Source -Destination $plan.Destination
            }
        }
    } else {
        Write-Host "用户取消迁移，保持文档原位置"
    }
}
```

---

### 📋 Step 0.6: 识别低质量文档和空文件夹（仅报告，需用户确认）

**目的**: 识别不符合要求的文档和空文件夹，**仅生成报告，不自动删除**

```powershell
# 1. 识别低质量文档（只有模板框架，无实际业务内容）
$lowQualityDocs = Get-ChildItem "<项目根目录>/.ai-doc" -Include *.md -Recurse | Where-Object {
    $content = Get-Content $_.FullName -Raw
    $lineCount = (Get-Content $_.FullName).Count
    # 行数少于 20 行
    $lineCount -lt 20 -or
    # 只包含模板框架文字
    $content -match 'Business component - participates in system business processing' -or
    $content -match 'Executes business logic based on specific scenario' -or
    $content -match 'Simple data object' -or
    $content -match 'Interface definition - declares contract specification'
}
# 输出报告，供用户决定是否处理
foreach ($doc in $lowQualityDocs) {
    Write-Host "低质量文档：$($doc.FullName)"
}
Write-Host "共识别 $($lowQualityDocs.Count) 个低质量文档"

# 2. 识别空文件夹（供用户参考）
Get-ChildItem "<项目根目录>/.ai-doc" -Directory -Recurse | ForEach-Object {
    if ((Get-ChildItem $_.FullName -Force).Count -eq 0) {
        Write-Host "空目录：$($_.FullName)"
    }
}
```

**⚠️ 重要安全约束**:
- 此步骤**仅生成报告**，绝不自动删除任何文件
- 如需处理低质量文档，必须**明确询问用户并获得确认**
- 删除操作示例（仅当用户明确同意时执行）:
  ```powershell
  # 询问用户确认
  $confirm = Read-Host "是否删除 $($lowQualityDocs.Count) 个低质量文档？(y/n)"
  if ($confirm -eq "y") {
      # 移动到回收站而非直接删除（如果可能）
      foreach ($doc in $lowQualityDocs) {
          Write-Host "将移动到回收站：$($doc.FullName)"
          # 使用安全删除方式
      }
  }
  ```

---

### 📄 Step 1: 生成所有 L3 文件级文档

**核心策略**:
- 每片 8-12 个文件，spawn 多个子代理并行（减少单个代理负担）
- 每处理 2-3 个文件 → 压缩上下文（只保留路径 +1 行摘要）
- 简单文件 (<50 行纯定义/枚举/接口) → 跳过或简化文档
- 复杂文件 → 完整 L3 文档（包含业务逻辑自然语言描述）

**⚠️ 路径规则（重要！）**：
- 输出路径必须是：`<项目根目录>/.ai-doc/<模块名>/src/main/java/包路径/类名.java.md`
- **❌ 错误示例**：`.ai-doc/module/com/company/Class.java.md`（缺少 src/main/java）
- **✅ 正确示例**：`.ai-doc/module/src/main/java/com/company/Class.java.md`

**子代理任务模板**:

```markdown
# 任务：为 <模块名> 模块生成 L3 文档（分片 X/Y）

## 源码路径
<绝对路径>

## 输出路径
<项目根目录>/.ai-doc/<模块名>/src/main/java/

## 本分片文件
<文件列表，8-12 个>

## 要求
1. 为每个文件生成 L3 文档 (*.java.md 或 *.xml.md)
2. **重点分析业务逻辑**，将代码逻辑转换为自然语言描述
3. 对于 MyBatis XML 文件，分析 SQL 与 Java 方法的映射关系
4. 对于复杂 Java 类，按方法分解业务逻辑
5. 简单文件 (<50 行纯定义) → 跳过或极简文档
6. **严格上下文压缩**：每处理完 2-3 个文件，压缩已处理内容的完整描述，只保留路径 +1 行摘要
7. 如文件读取失败，记录该文件并在最终报告中标注
8. 超时前尽可能完成更多文件
9. 完成后返回 JSON 摘要

## L3 文档模板
参考 [references/l3-template.md](references/l3-template.md)

## 跳过规则（⚠️ 严格执行！）

**必须跳过的文件类型**：
| 类型 | 判断标准 | 示例 |
|------|----------|------|
| DTO/VO/Param | 类名以 DTO/VO/Param 结尾，且行数<50，无业务方法 | UserDTO.java |
| 枚举 | 包含 `enum`，且无复杂方法 | PaymentStatus.java |
| 常量类 | 类名含 Constant，只有 `public static final` | AppConstant.java |
| 接口 | `public interface`，无方法实现 | UserService.java |
| MapStruct Converter | `@Mapper` 注解或接口名含 Converter | UserConverter.java |

**代码特征检查**（满足任一即跳过）：
1. 文件行数 < 30 行
2. 不包含 if/for/while/switch/try/catch（getter/setter 除外）
3. 只包含字段定义和 @ 注解

## 文档质量自检（⚠️ 生成后必须检查！）

**✅ 合格文档检查清单**：
- [ ] 文档行数 > 30 行
- [ ] 包含"触发条件"或"处理流程"描述
- [ ] 包含"业务规则"或"判断逻辑"描述
- [ ] 不包含原代码片段（`public class`, `if ()` 等）

**❌ 低质量文档特征**（出现任一需重新生成）：
- [ ] 文档行数 < 20 行
- [ ] 只包含"Business component", "Interface definition"等模板文字
- [ ] 只重复类名和包名，无实际业务解释

## 特殊处理规则
- MyBatis XML 文件：分析 SQL 语句的业务含义，与对应 Mapper 方法的关系
- Service 类：分析业务流程，各方法间的调用关系
- Controller 类：分析 API 接口的业务功能
- Entity/DTO 类：如果是纯数据类，**必须跳过**

## 返回格式
```json
{
  "module": "<模块名>",
  "chunk": "X/Y",
  "status": "completed|partial",
  "processed": ["File1.java", "File2.java"],
  "skipped": ["SimpleClass.java", "EntityClass.java"],
  "failed": ["ProtectedFile.java"],
  "summaries": [
    {"file": "File1.java", "lines": 150, "type": "complex", "summary": "一句话摘要"},
    {"file": "Mapper.xml", "lines": 80, "type": "mybatis", "summary": "SQL 映射文件，包含订单相关查询"}
  ]
}
```
```

**上下文压缩策略**:
```
每处理 2-3 个文件后：
- 保留：文件路径列表 + 1 行摘要/文件
- 丢弃：已生成文档的完整内容、中间思考过程、详细示例
- 目的：为后续文件腾出上下文空间
```

**文件读取失败处理**:
```
如果文件读取失败（权限限制或其他原因）：
1. 记录失败文件到日志
2. 在最终报告中标注该文件
3. 请求用户确认文件访问权限
4. ⚠️ 禁止尝试提权或使用替代读取工具
5. 继续处理其他文件
```

**大文件处理策略**:
```
对于超过 1000 行的超大文件：
1. 按类/方法进行切分
2. 生成多个子文档（MethodA.md, MethodB.md 等）
3. 最终合并为一个完整的文件文档
```

---

### 📁 Step 2: 生成所有 L2 模块级文档

**触发条件**: 所有 L3 文档生成完成

**核心策略**:
- 每个模块 spawn 一个子代理
- 读取该模块所有 L3 文档的**摘要**（而非完整内容）
- 汇总生成 module.md
- 包含模块内 MyBatis 映射关系、Maven 依赖、Spring 配置

**子代理任务模板**:

```markdown
# 任务：为 <模块名> 模块生成 L2 文档

## 输入
读取 <项目根目录>/.ai-doc/<模块名>/ 目录下所有 L3 文档

## 输出
<项目根目录>/.ai-doc/<模块名>.md

## 要求
1. 读取所有 L3 文档的摘要信息（文件名、行数、类型、职责）
2. 生成 L2 模块级文档，包含：
   - 模块职责概述（200 字）
   - 文件索引表（文件路径 | 职责简述 | 复杂度 | 行数）
   - 公共 API（核心类、核心方法）
   - MyBatis 映射关系图（SQL 与 Java 方法映射）
   - 依赖关系图（模块间依赖、Maven 依赖）
   - 核心业务流程（1-3 个关键业务流程）
   - 配置项（application.properties/yml 内容摘要）
3. **上下文压缩**：读取 L3 时只提取关键信息，不保留完整文档内容
4. 文档大小控制在 5-15KB

## L2 文档模板
参考 [references/l2-template.md](references/l2-template.md)
```

**摘要提取规则**:
```
从每个 L3 文档提取：
- 文件路径
- 行数
- 文件类型（Service/Controller/Entity/Mapper/XML）
- 1 行职责描述
- 核心函数签名（仅复杂文件）
- 业务逻辑摘要

不提取：
- 完整方法实现
- 详细调用关系图
- 变更历史
```

---

### 🏗️ Step 3: 生成 L1 项目级文档

**触发条件**: 所有 L2 文档生成完成

**核心策略**:
- spawn 一个子代理
- 读取所有 L2 文档的**核心摘要**（每模块 500 字）
- 汇总生成 project.md
- 包含项目整体架构、模块依赖、技术栈、部署架构

**子代理任务模板**:

```markdown
# 任务：生成 <项目名> 的 L1 项目级文档

## 输入
读取以下 L2 模块级文档：
<列出所有 module.md 路径>

## 输出
<项目根目录>/.ai-doc/project.md

## 要求
生成 L1 项目级文档，包含：
1. **项目基本信息** - 名称、技术栈、架构模式、数据库、中间件
2. **核心模块索引表** - 模块名 | 职责 | 文档路径 | 文件数 | 关键词
3. **系统架构图** - 模块间依赖关系（ASCII 或 Mermaid）
4. **Maven 依赖关系图** - 项目间依赖、外部依赖
5. **MyBatis 映射概览** - 各模块 SQL 映射情况
6. **目录结构** - 完整的工程目录树
7. **核心业务流程** - 跨模块的核心业务流程（2-4 个）
8. **技术栈汇总** - 框架、中间件、数据库
9. **配置项汇总** - 全局配置
10. **文档覆盖状态** - L3 文档统计
11. **部署架构** - 服务部署关系

## L1 文档模板
参考 [references/l1-template.md](references/l1-template.md)
```

---

## 文档模板规范

### L3 文件级文档模板

详见 [references/l3-template.md](references/l3-template.md)

**核心字段**:
```markdown
# {文件名} - 业务逻辑详解

## 基本信息
- **文件路径**: `{relativePath}`
- **行数**: {lines}
- **文件类型**: {Service/Controller/Entity/Mapper/XML/Configuration}
- **关联文件**: {MyBatis 映射的 XML/Java 文件}

## 业务职责
{用自然语言描述这个文件的业务职责，非技术人员也能理解}

## 核心业务逻辑
{详细描述主要方法的业务逻辑，用自然语言表达，不包含具体代码或方法名}

## 业务流程
{描述方法间的调用关系和业务流转过程}

## 数据交互
{描述与数据库、外部服务的交互方式}

## 依赖关系
{该文件依赖的其他组件和服务}
```

### L2 模块级文档模板

详见 [references/l2-template.md](references/l2-template.md)

**核心章节**:
```markdown
# {模块名} - 模块详解

## 模块职责
{200 字概述模块的业务职责}

## 文件索引表
| 文件路径 | 职责简述 | 类型 | 行数 |
|----------|----------|------|------|

## MyBatis 映射关系
{SQL 与 Java 方法的映射关系图}

## 公共 API
{核心业务类和方法的自然语言描述}

## 模块依赖
{该模块依赖的其他模块和外部服务}

## 核心业务流程
{1-3 个关键业务流程的自然语言描述}

## 配置项
{application 配置文件的主要设置}
```

### L1 项目级文档模板

详见 [references/l1-template.md](references/l1-template.md)

**核心章节**:
```markdown
# {项目名} - 系统架构

## 项目基本信息
{技术栈、架构模式、数据库、中间件}

## 核心模块索引表
| 模块名 | 职责 | 文档路径 | 文件数 | 关键词 |
|--------|------|----------|--------|--------|

## 系统架构图
{模块依赖关系，可用 Mermaid 格式}

## Maven 依赖关系
{项目间依赖、外部依赖关系图}

## MyBatis 映射概览
{各模块 SQL 映射情况汇总}

## 核心业务流程
{跨模块的核心业务流程，自然语言描述}

## 技术栈汇总
{框架、中间件、数据库}

## 部署架构
{服务部署关系，容器化情况等}

## 文档覆盖状态
{L3 文档生成统计，覆盖率}
```

---

## 子代理分片策略

### 上下文监控阈值

| 阈值 | 动作 |
|------|------|
| 30% | 正常处理 |
| 40% | 预警，准备压缩 |
| 50% | **强制压缩**：丢弃已处理文件的完整内容，只保留路径 +1 行摘要 |
| 60% | 停止当前任务，报告进度 |

### 分片规则

```yaml
# 默认配置
chunk_strategy:
  files_per_subagent: 10        # 每个子代理处理文件数（调整为更小分片）
  max_parallel_subagents: 8     # 最大并行子代理数（增加并行度）
  context_threshold: 0.40       # 40% 预警阈值
  compress_threshold: 0.50      # 50% 强制压缩阈值
  compression_interval: 2       # 每处理 2 个文件压缩一次（更频繁压缩）
  
# 文件复杂度估算
file_complexity:
  simple: "< 50 行，纯定义/枚举/接口/Entity/DTO"  # 跳过生成文档
  normal: "50-200 行"                              # 标准 L3 文档
  complex: "> 200 行"                              # 详细 L3 文档
  huge: "> 1000 行"                                # 超大文件，需特殊处理
```

### 上下文压缩操作

```javascript
// 伪代码：上下文压缩策略
function compressContext(processedFiles) {
  if (contextUsage < 0.50) return;
  
  // 保留关键信息
  keep([
    'processed_file_paths',      // 文件路径列表
    'one_line_summaries',        // 每文件 1 行摘要
    'current_task',              // 当前任务描述
    'output_path',               // 输出路径
    'progress_stats'             // 进度统计
  ]);
  
  // 丢弃占用上下文的内容
  discard([
    'full_generated_doc_content', // 已生成文档的完整内容
    'intermediate_thoughts',      // 中间思考过程
    'detailed_examples',          // 详细示例
    'complete_function_bodies'    // 完整函数体
  ]);
}
```

---

## 任务监控与重试机制

### 任务状态跟踪

**状态文件**: `.ai-doc/.generate-state.json`

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
      "failedFiles": 3,
      "chunks": {
        "total": 28,
        "completed": 12,
        "inProgress": 4,
        "pending": 12,
        "failed": 0
      }
    },
    "L2": {
      "status": "pending",
      "totalModules": 7,
      "completedModules": 0
    },
    "L1": {
      "status": "pending",
      "completed": false
    }
  },
  "subagents": [
    {
      "label": "L3-ces-domain-chunk1",
      "status": "completed",
      "startTime": "2026-03-05T15:32:00+08:00",
      "endTime": "2026-03-05T15:38:00+08:00",
      "processedFiles": 12,
      "retries": 0
    },
    {
      "label": "L3-admin-api-chunk2",
      "status": "running",
      "startTime": "2026-03-05T15:35:00+08:00",
      "processedFiles": 7,
      "retries": 1
    }
  ],
  "lastCheckpoint": "2026-03-05T15:40:00+08:00",
  "canResume": true
}
```

### 自动重试机制

**重试策略**:
```yaml
retry_policy:
  max_retries: 3                    # 最大重试次数
  initial_delay: 30                 # 初始延迟（秒）
  backoff_multiplier: 2             # 延迟倍增因子
  max_delay: 300                    # 最大延迟（秒）
  retryable_errors:                 # 可重试的错误类型
    - "timeout"
    - "context_overflow"
    - "file_access_error"
    - "subagent_crash"
  non_retryable_errors:             # 不可重试的错误类型
    - "invalid_project_path"
    - "permission_denied"
    - "disk_full"
```

**重试流程**:
```
1. 检测子代理失败
2. 判断错误类型是否可重试
3. 如果可重试：
   a. 等待延迟时间（指数退避）
   b. 重新 spawn 子代理
   c. 传递已完成的进度
   d. 继续处理剩余文件
4. 如果达到最大重试次数：
   a. 记录失败文件
   b. 继续处理其他分片
   c. 最后统一处理失败文件
```

### 子代理健康检查

**检查频率**: 每 60 秒

**检查项目**:
```yaml
health_checks:
  - name: "is_alive"
    description: "子代理是否仍在运行"
    action: "sessions_list 检查会话状态"
    
  - name: "progress_making"
    description: "子代理是否有进度更新"
    action: "检查.last_update 时间戳（超过 5 分钟无更新则警告）"
    
  - name: "context_usage"
    description: "上下文使用率是否正常"
    action: "检查上下文使用率（超过 60% 则警告）"
    
  - name: "memory_usage"
    description: "内存使用是否正常"
    action: "检查内存使用（如果框架支持）"
```

**健康状态**:
```
✅ healthy - 正常运行中
⚠️ warning - 有警告但继续运行
❌ unhealthy - 需要干预或重启
```

### 进度报告机制

**报告频率**: 每 5 分钟或每完成 10% 进度

**报告内容**:
```markdown
## 📊 文档生成进度报告

**项目**: mgmt-api-cp
**开始时间**: 2026-03-05 15:30:00
**当前时间**: 2026-03-05 15:45:00
**已用时间**: 15 分钟

### 总体进度：45.5%

```
[████████████░░░░░░░░░░░] 45.5%
```

### 当前阶段：L3 文件级文档生成

| 模块 | 文件数 | 已完成 | 进度 |
|------|--------|--------|------|
| ces-domain | 109 | 65 | 59.6% |
| admin-api | 53 | 28 | 52.8% |
| business-api | 82 | 35 | 42.7% |
| ... | ... | ... | ... |

### 子代理状态

| 子代理 | 状态 | 文件数 | 重试 |
|--------|------|--------|------|
| L3-ces-domain-chunk1 | ✅ 完成 | 12 | 0 |
| L3-ces-domain-chunk2 | ✅ 完成 | 12 | 0 |
| L3-admin-api-chunk1 | 🔄 运行中 | 7/12 | 1 |
| L3-business-api-chunk1 | 🔄 运行中 | 5/10 | 0 |
| ... | ... | ... | ... |

### 统计

- 已处理文件：142
- 已跳过文件：65（纯定义类）
- 失败文件：3（将在最后重试）
- 活跃子代理：5/8

### 预计完成时间

- L3 阶段：约 25 分钟（剩余 60%）
- L2 阶段：约 10 分钟
- L1 阶段：约 3 分钟
- **总计**: 约 38 分钟
```

### 断点续传机制

**状态保存点**:
- 每完成一个分片保存一次
- 每 5 分钟自动保存一次
- 子代理启动/结束时保存

**恢复流程**:
```
1. 检测状态文件是否存在
2. 解析状态文件，获取已完成进度
3. 询问用户是否恢复进度
4. 如果确认恢复：
   a. 跳过已完成的分片
   b. 重新启动失败的子代理
   c. 继续处理剩余文件
5. 如果选择重新开始：
   a. 备份旧状态文件
   b. 从头开始执行
```

### 日志记录

**日志文件**: `.ai-doc/.task-log.md`

**日志格式**:
```markdown
# 任务执行日志

## 任务信息
- **项目路径**: E:\projects\mgmt-api-cp
- **开始时间**: 2026-03-05 15:30:00
- **模式**: 完整生成 (L3→L2→L1)

## 执行记录

### [15:30:00] 任务启动
- 扫描项目结构...
- 发现 7 个模块，共 312 个关键文件

### [15:31:00] 分片计划完成
- 制定 28 个分片计划
- 最大并行子代理数：8

### [15:32:00] L3 阶段开始
- Spawn 子代理：L3-ces-domain-chunk1
- Spawn 子代理：L3-ces-domain-chunk2
- ...

### [15:38:00] 子代理完成
- ✅ L3-ces-domain-chunk1 完成（12 文件）
- ✅ L3-ces-domain-chunk2 完成（12 文件）

### [15:40:00] 子代理重试
- ⚠️ L3-admin-api-chunk2 超时，准备重试（1/3）
- 等待 30 秒后重试...

### [15:41:00] 子代理重试成功
- ✅ L3-admin-api-chunk2 重试成功（12 文件）

### [15:45:00] 进度报告
- 总体进度：45.5%
- 已完成：142 文件
- 活跃子代理：5/8

...
```

---

## 错误处理

### 子代理超时

```
问题：子代理处理大模块时超时（5 分钟限制）

解决：
1. 检查已生成的文件
2. 将剩余文件拆分为更小的分片（每片 5-7 个文件）
3. 缩短超时时间到 3 分钟，快速失败快速重试
4. 记录已完成进度，避免重复劳动
5. 为超时子代理设置更长的超时时间（如 10 分钟用于超大文件）
6. 如果重试 3 次仍失败，标记为"需要手动干预"
```

### 上下文爆炸

```
问题：子代理上下文使用率超过 60%

解决：
1. 立即触发强制压缩
2. 如果仍超过 60%，停止当前子代理
3. 将剩余文件拆分为更小的分片
4. 为新分片 spawn 新的子代理
5. 增加压缩频率（每 1 个文件就压缩）
6. 记录错误到日志，用于后续优化分片策略
```

### 文件访问权限问题

```
问题：文件因权限限制无法读取

解决：
1. 记录无法访问的文件到日志
2. 在最终报告中标注无法访问的文件
3. 请求用户确认文件访问权限
4. ⚠️ 禁止尝试提权、bash 工具或其他替代读取方式
5. 继续处理其他文件
6. 如关键文件无法访问，暂停任务等待用户解决
```

### 模块扫描失败

```
问题：无法找到模块目录或源码文件

解决：
1. 确认项目路径正确
2. 检查是否有权限访问
3. 尝试使用绝对路径
4. 如果项目不在本地，请求用户提供源码位置
5. 验证路径中的特殊字符或长度限制
6. 如果是网络路径，检查网络连接
```

### 子代理崩溃

```
问题：子代理意外退出或崩溃

解决：
1. 检查子代理日志，确定崩溃原因
2. 如果是因为上下文溢出，减小分片大小
3. 如果是因为超时，增加超时时间
4. 重新 spawn 子代理，传递已完成进度
5. 如果连续崩溃 3 次，暂停任务并请求用户干预
```

---

## 配置项

在 `TOOLS.md` 中添加：

```markdown
### Project Analyzer - Java 工程智能文档生成器

- 默认分片大小：10 文件/子代理
- 上下文阈值：40% 预警，50% 强制压缩
- 最大并行：8 子代理
- 简单文件阈值：50 行
- 超时时间：300 秒（基础），1000 秒（大文件）
- 文件读取失败处理：记录并报告
- 文档迁移：自动合并已存在文档
- 重试策略：最多 3 次，指数退避
- 健康检查：每 60 秒
- 进度报告：每 5 分钟或 10% 进度
- 断点续传：自动保存状态
```

---

## 使用示例

### 基础用法

```
用户：为 E:\projects\mgmt-api-cp 生成业务逻辑文档

AI: 收到！开始执行完整流程：

Step 0: 扫描项目结构，分析 Maven 依赖...
Step 0.5: 检查.ai-doc 目录，执行文档迁移合并...
Step 1: 生成所有 L3 文档（312 个关键文件）...
  📊 进度：45.5% (142/312)
  🔄 活跃子代理：5/8
  ⏱️ 预计剩余时间：25 分钟
Step 2: 生成所有 L2 文档（7 个模块）...
Step 3: 生成 L1 项目文档...

✅ 完成！生成 355 个文档文件，包含业务逻辑详解。
```

### 增量更新

```
用户：ces-domain 模块有代码变更，更新文档

AI: 收到！执行增量更新：

1. 检测变更文件（git diff 或 时间戳比较）
2. 只更新变更文件的 L3 文档
3. 重新汇总生成 ces-domain.md (L2)
4. 更新 project.md (L1) 的统计信息
5. 保持 MyBatis 映射关系同步
```

### 断点续传

```
用户：继续之前的文档生成任务

AI: 检测到未完成的生成任务...

## 上次任务状态
- 项目：E:\projects\mgmt-api-cp
- 中断时间：2026-03-05 14:30:00
- 完成进度：L3 阶段 45.5% (142/312 文件)
- 失败分片：2 个（已重试 3 次）

是否从断点继续？(y/n)

用户：y

AI: 恢复任务...
- 跳过已完成的 142 个文件
- 重新处理 2 个失败分片
- 继续生成剩余 170 个文件的 L3 文档
```

### 单模块生成

```
用户：只生成 business-api 模块的文档

AI: 收到！执行单模块流程：

1. 扫描 business-api 模块（82 个文件，含 15 个 XML）
2. 分片生成 L3 文档（7 个子代理）
3. 汇总生成 business-api.md (L2)

注意：不生成 L1 项目文档（需要所有模块完成）
```

---

## 性能参考

### 生成时间估算

| 工程规模 | L3 生成 | L2 生成 | L1 生成 | 总计 |
|----------|---------|---------|---------|------|
| 1 万行 (50 文件) | ~8 分钟 | ~3 分钟 | ~2 分钟 | ~13 分钟 |
| 10 万行 (200 文件) | ~35 分钟 | ~12 分钟 | ~3 分钟 | ~50 分钟 |
| 50 万行 (500 文件) | ~3 小时 | ~45 分钟 | ~8 分钟 | ~4 小时 |

### Token 消耗估算

| 阶段 | 每文件/模块 | 总计 (200 文件) |
|------|-------------|-----------------|
| L3 生成 | 200k tokens/文件 | 40M tokens |
| L2 生成 | 250k tokens/模块 | 1.75M tokens (7 模块) |
| L1 生成 | 600k tokens/项目 | 600k tokens |

---

## 相关文件

- L3 模板：[references/l3-template.md](references/l3-template.md)
- L2 模板：[references/l2-template.md](references/l2-template.md)
- L1 模板：[references/l1-template.md](references/l1-template.md)
- 上下文压缩指南：[references/context-compression.md](references/context-compression.md)
- 断点续传指南：[references/checkpoint-resume.md](references/checkpoint-resume.md)
- 增量更新流程：[references/incremental-update.md](references/incremental-update.md)
- 任务监控指南：[references/task-monitoring.md](references/task-monitoring.md)
- 重试机制指南：[references/retry-mechanism.md](references/retry-mechanism.md)

## 版本

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.4 | 2026-03-10 | **安全修复 (完整)**：移除所有 bash/external tool 引用、移除 elevated 权限引用、修复 task-execution-guide.md 中的不安全指令 |
| 2.1.3 | 2026-03-10 | **安全修复**：移除提权/bash 引用、明确要求用户确认删除/迁移操作 |
| 2.1.2 | 2026-03-09 | 文档描述优化、移除模糊指令 |
| 2.1.1 | 2026-03-08 | SKILL.md 编码修复、文档格式优化 |
| 2.1.0 | 2026-03-05 | 增强任务监控、重试机制、健康检查、断点续传 |
| 2.0.0 | 2026-03-05 | 重大更新，增加 Java 特定支持、MyBatis 分析、文档迁移合并 |
| 1.1.0 | 2026-03-03 | 添加断点续传、增量更新、L1 样例 |
| 1.0.0 | 2026-03-03 | 初始版本，基于 Infypower Energy AI 项目实战经验 |
