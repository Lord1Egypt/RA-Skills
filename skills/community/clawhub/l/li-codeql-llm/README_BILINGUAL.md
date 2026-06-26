# CodeQL + LLM 融合扫描器

# CodeQL + LLM Fusion Scanner

> **自动化安全扫描与智能分析工具**  
> **Automated Security Scanning and Intelligent Analysis Tool**

---

## 📖 简介 / Introduction

### 中文

本工具实现 **CodeQL 安全扫描** 与 **LLM 智能分析** 的完整自动化流程。通过一次命令，即可完成从代码扫描到漏洞分析报告的全过程。

**核心功能：**
- ✅ 自动检测 CodeQL 环境
- ✅ 创建代码数据库
- ✅ 运行 52+ 条安全查询
- ✅ 生成 3 种格式报告
- ✅ LLM 智能分析结果
- ✅ 输出可执行验证清单

### English

This tool implements a complete automated workflow for **CodeQL security scanning** and **LLM intelligent analysis**. With a single command, you can complete the entire process from code scanning to vulnerability analysis reports.

**Core Features:**
- ✅ Automatic CodeQL environment detection
- ✅ Create code database
- ✅ Run 52+ security queries
- ✅ Generate 3 report formats
- ✅ LLM intelligent analysis
- ✅ Output executable verification checklist

---

## 🚀 快速开始 / Quick Start

### 中文

#### 1. 安装 CodeQL

```bash
# 下载
wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip

# 解压
unzip codeql-linux64.zip -d /opt/codeql

# 添加到 PATH
export PATH=/opt/codeql/codeql:$PATH

# 验证
codeql --version
```

#### 2. 运行扫描

```bash
# 方式 1: 使用脚本
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
./run.sh /path/to/project

# 方式 2: 在对话中使用
"扫描 /root/devsecops-python-web 的安全漏洞"

# 方式 3: 使用 Python
python3 scanner.py /path/to/project --output ./output
```

#### 3. 查看结果

```bash
# 查看报告
cat ./output/CODEQL_SECURITY_REPORT.md

# 打印验证清单
cat ./output/漏洞验证_Checklist.md
```

### English

#### 1. Install CodeQL

```bash
# Download
wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip

# Extract
unzip codeql-linux64.zip -d /opt/codeql

# Add to PATH
export PATH=/opt/codeql/codeql:$PATH

# Verify
codeql --version
```

#### 2. Run Scan

```bash
# Method 1: Use script
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
./run.sh /path/to/project

# Method 2: Use in conversation
"Scan /root/devsecops-python-web for security vulnerabilities"

# Method 3: Use Python
python3 scanner.py /path/to/project --output ./output
```

#### 3. View Results

```bash
# View report
cat ./output/CODEQL_SECURITY_REPORT.md

# Print checklist
cat ./output/漏洞验证_Checklist.md
```

---

## 📦 文件结构 / File Structure

```
codeql-llm-scanner/
├── SKILL.md              # Skill 定义 / Skill definition
├── README.md             # 本文档 / This document
├── README_ZH.md          # 中文文档 / Chinese document
├── README_EN.md          # English document
├── PRIVACY_AND_SECURITY.md  # 隐私与安全 / Privacy and Security
├── IMPLEMENTATION.md     # 实现说明 / Implementation guide
├── scanner.py            # 核心扫描器 / Core scanner
├── run.sh                # 启动脚本 / Launch script
└── config.example.ini    # 配置示例 / Configuration example
```

---

## 🎯 使用场景 / Use Cases

### 场景 1: 靶机漏洞分析 / Target Machine Analysis

#### 中文

```bash
# 扫描安全靶机
./run.sh /root/devsecops-python-web ./target-scan

# 在对话中分析
"分析扫描结果，给出 Top 5 可利用漏洞"
```

**输出：**
- 漏洞列表（按严重程度排序）
- 利用 payload 示例
- 验证步骤清单

#### English

```bash
# Scan security target machine
./run.sh /root/devsecops-python-web ./target-scan

# Analyze in conversation
"Analyze scan results, give Top 5 exploitable vulnerabilities"
```

**Output:**
- Vulnerability list (sorted by severity)
- Exploit payload examples
- Verification checklist

---

### 场景 2: 项目安全审计 / Project Security Audit

#### 中文

```bash
# 扫描项目
./run.sh /path/to/my-project ./audit-scan

# 生成审计报告
"根据扫描结果生成安全审计报告"
```

**输出：**
- 安全审计报告
- 修复优先级建议
- 合规性检查

#### English

```bash
# Scan project
./run.sh /path/to/my-project ./audit-scan

# Generate audit report
"Generate security audit report based on scan results"
```

**Output:**
- Security audit report
- Remediation priority recommendations
- Compliance checklist

---

### 场景 3: CI/CD 集成 / CI/CD Integration

#### 中文

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  codeql-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Install CodeQL
      run: |
        wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip
        unzip codeql-linux64.zip -d /opt/codeql
    
    - name: Run Scan
      run: |
        export PATH=/opt/codeql/codeql:$PATH
        ./run.sh . ./scan-output
    
    - name: Upload SARIF
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: ./scan-output/codeql-results.sarif
```

#### English

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  codeql-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Install CodeQL
      run: |
        wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip
        unzip codeql-linux64.zip -d /opt/codeql
    
    - name: Run Scan
      run: |
        export PATH=/opt/codeql/codeql:$PATH
        ./run.sh . ./scan-output
    
    - name: Upload SARIF
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: ./scan-output/codeql-results.sarif
```

---

## 📊 输出示例 / Output Examples

### 1. 安全报告 / Security Report

#### 中文

```markdown
# CodeQL 安全扫描报告

**扫描时间**: 2026-03-19 07:00
**总漏洞数**: 38

## 漏洞统计

| 漏洞类型 | 数量 | 严重程度 |
|----------|------|----------|
| SQL 注入 | 1 | 🔴 严重 |
| 代码注入 | 3 | 🔴 严重 |
| 命令注入 | 2 | 🔴 严重 |
| 反序列化 | 3 | 🟠 高危 |
```

#### English

```markdown
# CodeQL Security Scan Report

**Scan Time**: 2026-03-19 07:00
**Total Vulnerabilities**: 38

## Vulnerability Statistics

| Vulnerability Type | Count | Severity |
|-------------------|-------|----------|
| SQL Injection | 1 | 🔴 Critical |
| Code Injection | 3 | 🔴 Critical |
| Command Injection | 2 | 🔴 Critical |
| Deserialization | 3 | 🟠 High |
```

---

### 2. 验证清单 / Verification Checklist

#### 中文

```markdown
# 🔍 漏洞验证 Checklist

## 🔴 SQL 注入 (1 处)

### 验证步骤:
- [ ] 定位代码：`vulnerable_app.py:44`
- [ ] 构造 payload: `' OR '1'='1`
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试命令**:
```bash
curl "http://localhost:5003/search_user?username=' OR '1'='1"
```
```

#### English

```markdown
# 🔍 Vulnerability Verification Checklist

## 🔴 SQL Injection (1 found)

### Verification Steps:
- [ ] Locate code: `vulnerable_app.py:44`
- [ ] Craft payload: `' OR '1'='1`
- [ ] Send request
- [ ] Confirm vulnerability
- [ ] Screenshot record

**Test Command**:
```bash
curl "http://localhost:5003/search_user?username=' OR '1'='1"
```
```

---

## 🔧 配置选项 / Configuration Options

### 中文

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--language` | 编程语言 | `python` |
| `--output` | 输出目录 | `./codeql-scan-output` |
| `--suite` | 查询套件 | `python-security-extended.qls` |
| `--db-name` | 数据库名称 | `codeql-db` |

### English

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--language` | Programming language | `python` |
| `--output` | Output directory | `./codeql-scan-output` |
| `--suite` | Query suite | `python-security-extended.qls` |
| `--db-name` | Database name | `codeql-db` |

---

## 🛡️ 安全与隐私 / Security and Privacy

### 中文

**本工具严格保护用户隐私：**

- ✅ 零数据收集
- ✅ 本地处理，数据不出境
- ✅ 无远程传输
- ✅ 用户完全控制输出

**详细信息请查看：** [隐私与安全声明](PRIVACY_AND_SECURITY.md)

### English

**This tool strictly protects user privacy:**

- ✅ Zero data collection
- ✅ Local processing, data stays on your machine
- ✅ No remote transmission
- ✅ User has full control of outputs

**For details, see:** [Privacy and Security Statement](PRIVACY_AND_SECURITY.md)

---

## 🐛 故障排查 / Troubleshooting

### 中文

#### 问题 1: CodeQL 未找到

```bash
# 检查 PATH
echo $PATH

# 临时添加
export PATH=/opt/codeql/codeql:$PATH

# 永久添加
echo 'export PATH=/opt/codeql/codeql:$PATH' >> ~/.bashrc
```

#### 问题 2: 数据库创建失败

```bash
# 确保项目可以构建
cd /path/to/project
pip install -r requirements.txt

# 重试
codeql database create db --language=python
```

### English

#### Issue 1: CodeQL not found

```bash
# Check PATH
echo $PATH

# Temporarily add
export PATH=/opt/codeql/codeql:$PATH

# Permanently add
echo 'export PATH=/opt/codeql/codeql:$PATH' >> ~/.bashrc
```

#### Issue 2: Database creation failed

```bash
# Ensure project can be built
cd /path/to/project
pip install -r requirements.txt

# Retry
codeql database create db --language=python
```

---

## 📚 相关资源 / Related Resources

### 中文

- [CodeQL 官方文档](https://codeql.github.com/docs/)
- [CodeQL 查询参考](https://codeql.github.com/codeql-query-help/)
- [SARIF 格式规范](https://sarifweb.azurewebsites.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### English

- [CodeQL Official Documentation](https://codeql.github.com/docs/)
- [CodeQL Query Reference](https://codeql.github.com/codeql-query-help/)
- [SARIF Specification](https://sarifweb.azurewebsites.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## 📄 许可证 / License

MIT License

---

**版本 / Version**: 1.0.0  
**创建日期 / Created**: 2026-03-19  
**最后更新 / Last Updated**: 2026-03-19  
**作者 / Author**: OpenClaw Community

---

## 📞 联系方式 / Contact

- **项目主页**: `~/.openclaw/workspace/skills/codeql-llm-scanner/`
- **问题反馈**: 通过 OpenClaw 社区
- **安全报告**: 查看 [PRIVACY_AND_SECURITY.md](PRIVACY_AND_SECURITY.md)
