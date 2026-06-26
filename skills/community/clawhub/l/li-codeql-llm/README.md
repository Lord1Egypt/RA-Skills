# CodeQL + LLM 融合扫描器 - 使用指南

## 🎯 Skill 功能

本 Skill 实现完整的 CodeQL 扫描 + LLM 智能分析流程：

```
用户请求 → 检查 CodeQL → 创建数据库 → 运行扫描 → 生成报告 → LLM 分析 → 输出清单
```

---

## 📦 安装

### 1. 安装 Skill

Skill 已位于：`~/.openclaw/workspace/skills/codeql-llm-scanner/`

### 2. 安装 CodeQL

```bash
# 下载
wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip

# 解压
unzip codeql-linux64.zip -d /opt/codeql

# 添加到 PATH
echo 'export PATH=/opt/codeql/codeql:$PATH' >> ~/.bashrc
source ~/.bashrc

# 验证
codeql --version
```

---

## 🚀 使用方法

### 方法 1: 在对话中直接使用（推荐）

在 OpenClaw 对话中直接说：

```
扫描 /root/devsecops-python-web 的安全漏洞
```

或

```
用 CodeQL 分析这个项目的安全问题，生成验证清单
```

### 方法 2: 使用命令行脚本

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner

# 扫描当前目录
./run.sh /path/to/project

# 扫描靶机
./run.sh /root/devsecops-python-web ./scan-output
```

### 方法 3: 使用 Python 扫描器

```bash
python3 scanner.py /path/to/project \
  --output ./output \
  --language python \
  --suite python-security-extended.qls
```

---

## 📋 完整工作流程

### Step 1: 环境检测

自动检查：
- ✅ CodeQL 是否安装
- ✅ 版本是否兼容
- ✅ 支持的語言

### Step 2: 创建数据库

```bash
codeql database create codeql-db \
  --language=python \
  --source-root=/path/to/project \
  --overwrite
```

### Step 3: 下载查询包

```bash
codeql pack download codeql/python-queries
```

### Step 4: 运行分析

```bash
codeql database analyze codeql-db \
  python-security-extended.qls \
  --format=sarif-latest \
  --output=codeql-results.sarif
```

### Step 5: 生成报告

自动生成 3 个文件：

1. **codeql-results.sarif** - 原始结果
2. **CODEQL_SECURITY_REPORT.md** - 详细报告
3. **漏洞验证_Checklist.md** - 验证清单

### Step 6: LLM 分析

将结果发送到对话中，让 LLM：
- 按严重程度排序
- 识别误报
- 给出修复建议
- 提供利用 payload（靶机场景）

---

## 📊 输出示例

### 1. 安全报告 (CODEQL_SECURITY_REPORT.md)

```markdown
# CodeQL 安全扫描报告

**扫描时间**: 2026-03-19 06:53
**总漏洞数**: 30

## 📊 漏洞统计

| 漏洞类型 | 数量 | 严重程度 |
|----------|------|----------|
| py/sql-injection | 1 | 🔴 严重 |
| py/code-injection | 3 | 🔴 严重 |
| py/weak-sensitive-data-hashing | 4 | 🟠 高危 |

## 🔍 详细发现

### 🔴 严重 py/sql-injection

**位置**: `vulnerable_apps/a03_injection/vulnerable_app.py:44`
**描述**: SQL 查询依赖于用户提供的值
**修复**: 使用参数化查询
```

### 2. 验证清单 (漏洞验证_Checklist.md)

```markdown
# 🔍 漏洞验证 Checklist

## 🔴 py/sql-injection (1 处)

### 🔴 py/sql-injection - #1

**位置**: `vulnerable_apps/a03_injection/vulnerable_app.py:44`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl "http://localhost:5003/search_user?username=' OR '1'='1"
```

**预期结果**: _______________
**实际结果**: _______________
```

---

## 🎯 使用场景

### 场景 1: 靶机漏洞分析

```bash
# 扫描靶机
./run.sh /root/devsecops-python-web ./target-scan

# 在对话中分析
"分析扫描结果，给出 Top 5 可利用漏洞"
```

### 场景 2: 项目安全审计

```bash
# 扫描项目
./run.sh /path/to/my-project ./audit-scan

# 生成审计报告
"根据扫描结果生成安全审计报告"
```

### 场景 3: CI/CD 集成

```yaml
# .github/workflows/security.yml
- name: CodeQL Scan
  run: |
    ./run.sh . ./scan-output

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: ./scan-output/codeql-results.sarif
```

---

## 🔧 配置选项

### 查询套件

| 套件 | 用途 | 推荐 |
|------|------|------|
| `python-security-extended.qls` | 安全扩展 | ✅ 推荐 |
| `python-code-scanning.qls` | 默认扫描 | ⭐ 一般 |
| `python-security-and-quality.qls` | 安全 + 质量 | ⭐ 一般 |
| `python-code-quality.qls` | 代码质量 | ❌ 不推荐 |

### 输出格式

| 格式 | 参数 | 用途 |
|------|------|------|
| SARIF | `--format=sarif-latest` | GitHub Security |
| Markdown | 自动生成 | 人类阅读 |
| CSV | `--format=csv` | 数据处理 |

---

## 🐛 故障排查

### 问题 1: CodeQL 未找到

```bash
# 检查 PATH
echo $PATH

# 临时添加
export PATH=/opt/codeql/codeql:$PATH

# 永久添加
echo 'export PATH=/opt/codeql/codeql:$PATH' >> ~/.bashrc
```

### 问题 2: 数据库创建失败

```bash
# 确保项目可以构建
cd /path/to/project
pip install -r requirements.txt

# 重试
codeql database create db --language=python
```

### 问题 3: 扫描结果为空

```bash
# 检查查询套件
codeql resolve queries --search-path=$(codeql pack download codeql/python-queries)

# 使用完整路径
codeql database analyze db /root/.codeql/packages/.../python-security-extended.qls
```

---

## 📚 相关资源

- [CodeQL 文档](https://codeql.github.com/docs/)
- [查询参考](https://codeql.github.com/codeql-query-help/)
- [SARIF 规范](https://sarifweb.azurewebsites.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## 🎓 示例会话

### 完整对话示例

**用户**: 扫描 /root/devsecops-python-web

**助手**: 
```
✅ 检测 CodeQL 已安装 (v2.22.1)
📦 创建 Python 数据库...
📥 下载查询包...
🔍 运行 52 条安全查询...
📊 发现 30 个安全问题
📝 生成报告...

生成的文件:
  1. codeql-results.sarif
  2. CODEQL_SECURITY_REPORT.md
  3. 漏洞验证_Checklist.md
```

**用户**: 分析最严重的漏洞

**助手**: 
```
🔴 严重漏洞 (6 个):

1. SQL 注入 - vulnerable_app.py:44
   利用：' OR '1'='1
   
2. 代码注入 - vulnerable_app.py:138
   利用：__import__('os').system('id')
   
3. 命令注入 - vulnerable_app.py:88
   利用：; cat /etc/passwd
```

---

**版本**: 1.0.0  
**最后更新**: 2026-03-19
