---
name: Li_codeql_LLM
description: "CodeQL 安全扫描与 LLM 智能分析融合工具。自动检测 CodeQL 安装、扫描指定目录、生成漏洞报告、LLM 分析、Jenkins 集成、输出验证 Checklist。"
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["codeql"] },
        "install":
          [
            {
              "id": "codeql",
              "kind": "manual",
              "label": "安装 CodeQL CLI",
              "instructions": "从 https://github.com/github/codeql-cli-binaries 下载或使用系统包管理器安装"
            }
          ],
      }
  }
---

# CodeQL + LLM 融合安全扫描 Skill

## 🎯 核心功能

本 Skill 实现 CodeQL 扫描与 LLM 智能分析的完整自动化流程：

1. **自动检测** - 检查 CodeQL 是否安装及版本
2. **安全扫描** - 扫描指定目录或靶机项目
3. **报告生成** - 生成 SARIF 格式和 Markdown 格式报告
4. **LLM 分析** - 智能分析扫描结果，识别误报，给出优先级
5. **验证清单** - 生成可执行的漏洞验证 Checklist

---

## 📦 前置要求

### 必需
- **CodeQL CLI** (v2.10.0+)
- **Python 3.11+** (用于创建数据库)
- **uv** 或 **pip** (Python 包管理)

### 可选
- **Node.js** (用于某些语言的分析)
- **Java JDK** (用于 Java 项目分析)

---

## 🚀 快速开始

### 1. 检查环境

```bash
# 检查 CodeQL 是否安装
codeql --version

# 如果未安装，下载并解压
wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip
unzip codeql-linux64.zip -d /opt/codeql
ln -s /opt/codeql/codeql/codeql /usr/local/bin/codeql
```

### 2. 使用 Skill

在对话中直接请求：

```
扫描 /path/to/project 的安全漏洞
```

或指定靶机目录：

```
扫描 /root/devsecops-python-web 靶机，生成验证清单
```

---

## 📋 命令参考

### 基础扫描

```bash
# 扫描当前目录
codeql database create codeql-db --language=python --source-root=.
codeql database analyze codeql-db python-security-extended.qls \
  --format=sarif-latest --output=results.sarif
```

### 通过 Skill 调用

在 OpenClaw 会话中：

```
/codeql_scan /path/to/project
```

或直接描述需求：

```
帮我扫描这个项目，用 CodeQL 分析安全问题，然后生成报告
```

---

## 📊 工作流程

### Step 1: 环境检测

```bash
# 检查 CodeQL
which codeql && codeql --version

# 检查支持的語言
codeql resolve languages
```

### Step 2: 创建数据库

```bash
# Python 项目
codeql database create codeql-db \
  --language=python \
  --source-root=/path/to/project \
  --overwrite
```

### Step 3: 运行分析

```bash
# 下载查询包
codeql pack download codeql/python-queries

# 运行分析
codeql database analyze codeql-db \
  /root/.codeql/packages/codeql/python-queries/*/codeql-suites/python-security-extended.qls \
  --format=sarif-latest \
  --output=codeql-results.sarif
```

### Step 4: LLM 分析

将 SARIF 结果发送给 LLM：

```python
import json

with open('codeql-results.sarif') as f:
    data = json.load(f)

# 提取关键信息
results = data['runs'][0]['results']
for r in results:
    print(f"规则：{r['ruleId']}")
    print(f"描述：{r['message']['text']}")
    print(f"位置：{r['locations'][0]['physicalLocation']['artifactLocation']['path']}")
```

LLM 分析内容：
- 漏洞严重程度排序
- 误报识别
- 修复建议
- 利用难度评估

### Step 5: 生成报告

生成以下文件：

1. **CODEQL_SECURITY_REPORT.md** - 完整扫描报告
2. **漏洞验证_Checklist.md** - 可执行的验证清单
3. **codeql-results.sarif** - 原始结果（可上传 GitHub Security）

---

## 🎯 使用场景

### 场景 1: 靶机漏洞分析

```
扫描 /root/devsecops-python-web 靶机
- 识别所有安全漏洞
- 按 OWASP Top 10 分类
- 生成利用 payload
- 输出验证 Checklist
```

### 场景 2: 项目安全审计

```
扫描 /path/to/my-project
- 检测严重和高危漏洞
- 给出修复优先级
- 生成审计报告
```

### 场景 3: CI/CD 集成

```yaml
# .github/workflows/security.yml
- name: CodeQL Scan
  run: |
    codeql database create db --language=python
    codeql database analyze db python-security-extended.qls \
      --format=sarif-latest --output=results.sarif

- name: LLM Analysis
  run: |
    # 调用 LLM 分析 results.sarif
    # 生成修复建议
```

---

## 📁 输出文件说明

### 1. CODEQL_SECURITY_REPORT.md

包含：
- 执行摘要（漏洞总数、分布）
- 按严重程度分类的详细信息
- 每个漏洞的代码位置、描述、修复建议
- 统计图表

### 2. 漏洞验证_Checklist.md

包含：
- 可打印的检查清单
- 每个漏洞的验证步骤
- 测试 payload 和命令
- 预期结果
- 截图/日志记录项

### 3. codeql-results.sarif

- 标准 SARIF 格式
- 可上传到 GitHub Security
- 可用 VS Code SARIF Viewer 查看

---

## 🔧 配置选项

### 扫描语言

```bash
# Python
--language=python

# JavaScript
--language=javascript

# Java
--language=java

# Go
--language=go

# 多语言
--language=python,javascript
```

### 查询套件

```bash
# 安全扩展（推荐）
python-security-extended.qls

# 代码质量
python-code-quality.qls

# 安全与质量
python-security-and-quality.qls

# 代码扫描（默认）
python-code-scanning.qls
```

### 输出格式

```bash
# SARIF（推荐）
--format=sarif-latest

# CSV
--format=csv

# JSON
--format=json
```

---

## 🐛 常见问题

### Q: CodeQL 数据库创建失败？

**A**: 确保项目可以正常构建：
```bash
# Python 项目
python -m pip install -r requirements.txt

# 然后创建数据库
codeql database create db --language=python
```

### Q: 扫描结果太多？

**A**: 使用过滤：
```bash
# 只看严重和高危
codeql database analyze db python-security-extended.qls \
  --rerun --checkout=latest \
  --sarif-category=severity \
  --output=results.sarif
```

### Q: 如何减少误报？

**A**: 
1. 使用 `python-security-extended.qls` 而非 `python-code-scanning.qls`
2. 让 LLM 分析识别误报
3. 手动验证关键漏洞

---

## 📚 相关资源

- [CodeQL 官方文档](https://codeql.github.com/docs/)
- [CodeQL 查询套件](https://github.com/github/codeql)
- [SARIF 格式规范](https://sarifweb.azurewebsites.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## 🎓 示例会话

### 完整流程示例

**用户**: 扫描 /root/devsecops-python-web 靶机

**助手**: 
1. ✅ 检测 CodeQL 已安装 (v2.22.1)
2. ✅ 创建数据库 (13 个 Python 文件)
3. ✅ 运行 52 条安全查询
4. ✅ 发现 30 个漏洞
5. ✅ 生成报告：
   - CODEQL_SECURITY_REPORT.md
   - 漏洞验证_Checklist.md
   - codeql-results.sarif

**用户**: 分析最严重的 3 个漏洞

**助手**: 
1. SQL 注入 - 行 44 - 利用：`' OR '1'='1`
2. 代码注入 - 行 138 - 利用：`__import__('os').system('id')`
3. 命令注入 - 行 88 - 利用：`; cat /etc/passwd`

详细利用方法见报告...

---

**版本**: 1.0.0  
**作者**: OpenClaw Community  
**许可**: MIT
