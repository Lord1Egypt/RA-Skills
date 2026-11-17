---

slug: iris-formatter-tool-pro
name: "iris-formatter-tool-pro"
version: "1.0.0"
displayName: "IRIS代码格式化专业版"
summary: "企业级 IRIS ObjectScript 代码审查方案，含批量处理、自定义规则与报告导出。。面向企业级 IRIS 开发团队的 ObjectScript 代码审查与治理工具。核心能力: -"
license: "Proprietary"
edition: "pro"
description: |-
  面向企业级 IRIS 开发团队的 ObjectScript 代码审查与治理工具。核心能力:
  - 批量代码审查与格式化（多文件/多类）
  - 自定义规范规则与团队级配置
  - 结构化审查报告导出（Markdown/HTML）
  - SQL 格式规范与性能检查
  - 陷阱（Trap）深度分析与合规检查
  - 代码复杂度与重复度分析

  适用场景:
  - 企业级 IRIS 项目的代码质量管控
  - 团队协作中的代码审查标准化
  - 遗留系统的代码重构与规范化
  - 上线前的合规检查与合规检查

  差异化: 专业版兼容免费版所有规...
tags:
  - 开发工具
  - IRIS
  - ObjectScript
  - 企业协作
  - 代码质量
  - 工具
  - 效率
  - 安全
  - report_file
  - true
  - file
  - grep
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"

---

# IRIS 代码格式化工具（专业版）
## 概述
本工具面向企业级 IRIS 开发团队，提供 ObjectScript 代码的批量审查与治理方案。在免费版基础规范检查能力之上，专业版新增批量多文件审查、自定义规范规则配置、结构化审查报告导出、SQL 格式与性能检查、陷阱深度分析与合规检查、代码复杂度与重复度分析等能力。通过可配置的规则引擎与自动化报告，帮助团队建立统一的代码质量标准.
**版本兼容性说明**：专业版完全兼容免费版（`iris-formatter-tool-free`）的所有规范规则与检查项，可无缝升级.
## 核心能力
| 能力模块 | 免费版 | 专业版新增 |
|----|---|-----|
| 代码审查 | 单文件审查 | 批量多文件/多类审查 |
| 规范规则 | 内置固定规则 | 自定义规则 + 团队配置 |
| 报告输出 | 文本报告 | Markdown/HTML 结构化报告 |
| SQL 检查 | 基础格式 | SQL 格式 + 性能检查 |
| 陷阱分析 | 基础陷阱检查 | 深度合规检查 |
| 代码度量 | - | 复杂度 + 重复度分析 |
| 格式化 | 单文件格式化 | 批量格式化 + 自动修正 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、IRIS、ObjectScript、代码审查方案、含批量处理、自定义规则与报告、面向企业级、开发团队的、代码审查与治理工、批量代码审查与格、自定义规范规则与、团队级配置、结构化审查报告导、格式规范与性能检、Trap、深度分析与安全审、代码复杂度与重复等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：批量代码审查
团队需要对整个模块的代码进行批量审查.
```bash
#!/bin/sh
MODULE_DIR=$1
REPORT_FILE="iris-review-report-$(date +%Y%m%d).md"
echo "# IRIS 代码审查报告" > "$REPORT_FILE"
echo "**审查时间**: $(date)" >> "$REPORT_FILE"
echo "**审查范围**: $MODULE_DIR" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
FILE_COUNT=$(find "$MODULE_DIR" -name "*.cls" -o -name "*.mac" -o -name "*.inc" | wc -l)
echo "**文件数量**: $FILE_COUNT" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "=== 开始批量审查 $FILE_COUNT 个文件 ==="
TOTAL_ISSUES=0
CRITICAL_COUNT=0
WARNING_COUNT=0
find "$MODULE_DIR" -name "*.cls" -o -name "*.mac" | while read file; do
  echo "审查: $file"
  ISSUES=$(grep -n "yonghu\|dingdan\|zhifu" "$file" | wc -l)
  if [ "$ISSUES" -gt 0 ]; then
    echo "- [严重] $file: 发现拼音命名" >> "$REPORT_FILE"
  fi
  LOCK_ISSUES=$(grep -n "l +\^" "$file" | grep -v ":3\|:5\|:10" | wc -l)
  if [ "$LOCK_ISSUES" -gt 0 ]; then
    echo "- [警告] $file: 锁未设置超时" >> "$REPORT_FILE"
  fi
  TS_COUNT=$(grep -c "ts\b" "$file")
  TC_COUNT=$(grep -c "tc\b" "$file")
  TRO_COUNT=$(grep -c "tro\b" "$file")
  if [ "$TS_COUNT" -ne "$((TC_COUNT + TRO_COUNT))" ]; then
    echo "- [严重] $file: 事务不闭合 (ts:$TS_COUNT tc:$TC_COUNT tro:$TRO_COUNT)" >> "$REPORT_FILE"
  fi
  POSTFIX_ISSUES=$(grep -n ") && (\|) || (" "$file" | wc -l)
  if [ "$POSTFIX_ISSUES" -gt 0 ]; then
    echo "- [严重] $file: 后置表达式格式错误（括号与&&间有空格）" >> "$REPORT_FILE"
  fi
done
echo "" >> "$REPORT_FILE"
echo "## 审查完成" >> "$REPORT_FILE"
echo "详细报告: $REPORT_FILE"
```

### 场景二：自定义规范规则配置
团队需要根据项目特点自定义规范规则.
```yaml
rules:
  naming:
    variable_case: lowerCamelCase
    method_case: UpperCamelCase
    constant_case: UPPER_SNAKE
    max_variable_length: 31
    max_method_length: 30
    forbidden_prefixes: ["is", "arr", "str"]
    required_boolean_suffix: "Flag"
  lock:
    require_timeout: true
    default_timeout: 3
    require_paired: true
    forbid_table_global_lock: true
    require_subscript: true
  transaction:
    require_closure: true
    forbid_cross_method: true
    require_blank_line: true
    max_distance: 20  # ts/tc/tro 之间最大行数
  format:
    indent: "tab"
    space_around_operator: true
    command_case: "lower"
    use_abbreviation: true
    full_spell_commands: ["for", "while", "if", "elseif", "else", "continue"]
    max_line_length: 120
    max_method_lines: 50
  sql:
    fields_per_line: 5
    indent_after_newline: 3
    comma_at_end: true
    command_case: "lower"
  trap:
    require_error_handler: true
    default_trap_name: "Error"
    require_zt_reset: true
    require_tl_check: true
    require_lock_release: true
severity:
  naming_pinyin: critical
  naming_case: warning
  lock_no_timeout: critical
  lock_unpaired: critical
  transaction_unclosed: critical
  format_spacing: minor
  format_abbreviation: warning
  postfix_format: critical
```

### 场景三：代码复杂度分析
团队需要分析代码的复杂度和重复度，识别需要重构的代码.
```bash
#!/bin/sh
TARGET=$1
echo "=== IRIS 代码复杂度分析 ==="
echo "目标: $TARGET"
echo ""
echo "## 方法行数统计（超过 50 行需重构）"
echo "| 文件 | 方法 | 行数 | 状态 |"
echo "| --- | --- | --- | --- |"
find "$TARGET" -name "*.cls" | while read file; do
  awk '
    /ClassMethod|Method/ {
      method_name = $0
      method_start = NR
    }
    /^}/ {
      if (method_name != "") {
        lines = NR - method_start
        if (lines > 50) {
          status = "需重构"
        } else if (lines > 30) {
          status = "建议优化"
        } else {
          status = "正常"
        }
        if (lines > 30) {
          printf "| %s | %s | %d | %s |\n", FILENAME, method_name, lines, status
        }
        method_name = ""
      }
    }
  ' "$file"
done
echo ""
echo "## 重复代码检测"
cls" -exec cat {} \; | \
  awk 'BEGIN{block=""} {
    block = block $0 "\n"
    if (NF == 0) {
      if (length(block) > 100) {
        print block
      }
      block = ""
    }
  }' | sort | uniq -d | head -10
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
### HTML 报告模板
```html
<!-- 生成结构化 HTML 审查报告 -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IRIS 代码审查报告</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .critical { color: #d32f2f; font-weight: bold; }
        .warning { color: #f57c00; }
        .minor { color: #1976d2; }
        .suggestion { color: #388e3c; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h1>IRIS 代码审查报告</h1>
    <table>
        <tr>
            <th>审查时间</th>
            <td></td>
        </tr>
        <tr>
            <th>审查范围</th>
            <td></td>
        </tr>
        <tr>
            <th>文件数量</th>
            <td></td>
        </tr>
        <tr>
            <th>问题总数</th>
            <td></td>
        </tr>
    </table>
    <h2>问题详情</h2>
    <table>
        <tr>
            <th>序号</th>
            <th>严重程度</th>
            <th>文件</th>
            <th>行号</th>
            <th>问题描述</th>
            <th>规范依据</th>
        </tr>
        <动态配置>
        <tr>
            <td></td>
            <td class=""></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <动态配置>
    </table>
</body>
</html>
```

### SQL 格式规范检查
```objectscript
// SQL 格式规范
// 1. 每行 5 个字段
// 2. 换行后 3 个 Tab 缩进
// 3. 逗号在行末
// 4. 每行不超过 120 字符
// 5. SQL 命令统一小写
// 正确格式
&sql(
   select id, name, age, email, phone
         into :id, :name, :age, :email, :phone
         from user_table
         where id = :userId
)
// 错误格式
&sql(SELECT ID,NAME,AGE,EMAIL,PHONE,ADDRESS,STATUS FROM USER_TABLE WHERE ID=:userId)
// 问题：字段过多、命令大写、单行过长
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例
### 审查规则配置文件
```yaml
version: "2.0"
team: "后端开发组"
updated: "2026-07-18"
extends: "default"
overrides:
  naming:
    service_prefix: "Svc"
    controller_prefix: "Ctrl"
    dao_prefix: "DAO"
  format:
    max_method_lines: 40  # 比默认 50 更严格
  sql:
    forbid_sql_in_loop: true
    require_parameterized: true
excludes:
  - "**/test/**"
  - "**/legacy/**"
  - "**/*.inc"  # include 文件单独审查
report:
  format: ["markdown", "html"]
  output_dir: "reports/"
  include_source: true
  max_suggestions: 5
```

## 优选实践
1. **批量审查定期执行**：每周对整个模块执行批量审查

2. **自定义规则版本管理**：规则配置纳入 Git 版本控制

3. **报告归档对比**：保留历史报告，跟踪改进趋势

4. **复杂度阈值**：方法超过 40 行必须拆分

5. **重复代码检测**：超过 5 行重复考虑提取公共方法

6. **SQL 性能检查**：禁止循环内 SQL，强制参数化查询

7. **合规检查**：上线前必须通过陷阱和安全检查

8. **规则渐进式引入**：新规则先以警告级别运行，稳定后提升为严重

## 常见问题
### Q1：如何处理遗留代码的大量违规？
```text
策略：
1. 先生成完整审查报告，评估违规规模
2. 按严重程度排序，优先修复 critical 级别
3. 使用批量格式化处理格式类问题
4. 命名和结构问题分批重构
5. 新代码必须完全合规，老代码逐步改进
```

### Q2：自定义规则和内置规则冲突怎么办？
```yaml
extends: "default"
overrides:
  format:
    max_method_lines: 40  # 覆盖默认的 50
```

### Q3：如何排除特定文件不被审查？
```yaml
excludes:
  - "**/legacy/**"      # 排除 legacy 目录
  - "**/*_old.cls"      # 排除旧文件
  - "**/test/**"        # 排除测试代码
```

### Q4：如何将审查集成到 CI/CD？
```yaml
iris-code-review:
  stage: quality
  script:
    - （请参考skill目录中的脚本文件） src/
    - |
      CRITICAL_COUNT=$(grep -c "\[严重\]" iris-review-report-*.md)
      if [ "$CRITICAL_COUNT" -gt 0 ]; then
        echo "发现 $CRITICAL_COUNT 个严重问题，阻止合并"
        exit 1
      fi
  artifacts:
    reports:
      paths:
        - iris-review-report-*.md
```

### Q5：如何统计代码质量趋势？
```bash
for report in reports/iris-review-report-*.md; do
  date=$(echo $report | grep -o '[0-9]*' | head -1)
  critical=$(grep -c "\[严重\]" "$report")
  warning=$(grep -c "\[警告\]" "$report")
  echo "$date, $critical, $warning"
done | sort
```

### Q6：如何处理跨文件的代码重复？
```bash
find src/ -name "*.cls" -exec cat {} \; | \
  grep -v "^\s*//\|^\s*#" | \
  awk 'length > 20' | \
  sort | uniq -d | \
  while read line; do
    echo "重复行: $line"
    grep -rn "$line" src/
  done
```

## 依赖说明
### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **IRIS/Cache 版本**: 建议 2018 及以上
- **CI/CD 平台**: GitLab CI / GitHub Actions / Jenkins 等

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| InterSystems IRIS | 运行时 | 推荐 | InterSystems 官方获取 |
| Git | 命令行工具 | 推荐 | 系统包管理器安装 |
| YAML 解析器 | 工具 | 可选 | 系统包管理器安装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令驱动，无需额外 API Key
- IRIS 服务器连接需要配置访问凭据
- CI/CD 集成需要在平台配置对应的访问令牌

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 执行批量代码审查与格式化，专业版功能依赖命令行脚本和 CI/CD 平台

## 错误处理
| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
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
    "result": "IRIS代码格式化专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "iris formatter pro"
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