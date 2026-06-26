# 配置说明 / Configuration Guide

## 📖 快速配置 / Quick Configuration

### 1. 复制配置模板 / Copy Configuration Template

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
cp .env.example .env
```

### 2. 编辑配置文件 / Edit Configuration File

```bash
vim .env
# 或
nano .env
```

### 3. 必须配置项 / Required Configuration

```ini
# CodeQL 路径（如果不在系统 PATH 中）
CODEQL_PATH=/opt/codeql/codeql

# Jenkins 配置（如果启用 Jenkins 集成）
JENKINS_URL=http://your-jenkins-server:8080
JENKINS_USER=your-username
JENKINS_TOKEN=your-api-token
JENKINS_JOB_NAME=codeql-security-scan
```

---

## 🔧 配置项详解 / Configuration Details

### CodeQL 配置

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `CODEQL_PATH` | CodeQL 安装路径 | `/opt/codeql/codeql` | 否 |
| `CODEQL_LANGUAGE` | 编程语言 | `python` | 否 |
| `CODEQL_SUITE` | 查询套件 | `python-security-extended.qls` | 否 |
| `CODEQL_DB_NAME` | 数据库名称 | `codeql-db` | 否 |

**查询套件选项 / Query Suite Options:**
- `python-security-extended.qls` - 安全扩展（推荐）
- `python-code-scanning.qls` - 默认扫描
- `python-security-and-quality.qls` - 安全 + 质量

---

### 输出配置

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `OUTPUT_DIR` | 输出目录 | `./codeql-scan-output` | 否 |
| `GENERATE_SARIF` | 生成 SARIF | `true` | 否 |
| `GENERATE_MARKDOWN` | 生成 Markdown | `true` | 否 |
| `GENERATE_CHECKLIST` | 生成 Checklist | `true` | 否 |
| `FILE_PERMISSIONS` | 文件权限 | `600` | 否 |

---

### LLM 配置

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `LLM_AUTO_ANALYZE` | 自动分析 | `false` | 否 |
| `LLM_ANALYSIS_MODE` | 分析模式 | `detailed` | 否 |
| `LLM_GENERATE_EXPLOIT` | 生成 payload | `false` | 否 |

**分析模式 / Analysis Modes:**
- `summary` - 摘要
- `detailed` - 详细
- `exploit` - 包含利用方法

---

### Jenkins 配置

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `JENKINS_URL` | Jenkins 服务器 URL | `http://localhost:8080` | 是* |
| `JENKINS_USER` | Jenkins 用户名 | `devops` | 是* |
| `JENKINS_TOKEN` | API Token | - | 是* |
| `JENKINS_JOB_NAME` | 任务名称 | `codeql-security-scan` | 否 |
| `JENKINS_UPLOAD_SARIF` | 上传 SARIF | `true` | 否 |

*如果启用 `JENKINS_UPLOAD_SARIF=true`，则必须配置

#### 获取 Jenkins Token

1. 登录 Jenkins
2. 点击用户名 → 配置 (Configure)
3. 找到 "API Token" 部分
4. 点击 "添加新 Token"
5. 输入名称（如：CodeQL Scanner）
6. 复制生成的 Token
7. 粘贴到 `.env` 文件的 `JENKINS_TOKEN` 配置项

---

### 安全配置

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `EXCLUDE_DIRS` | 排除目录 | `.git,credentials,.env` | 否 |
| `SECURITY_CHECK_BEFORE_SCAN` | 扫描前检查 | `true` | 否 |
| `CONTINUE_ON_SENSITIVE_INFO` | 发现敏感信息继续 | `false` | 否 |
| `AUTO_CLEANUP_DAYS` | 自动清理天数 | `30` | 否 |

---

### 通知配置

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `EMAIL_NOTIFY` | 邮件通知 | `false` | 否 |
| `EMAIL_RECIPIENT` | 邮件接收者 | - | 否* |
| `DINGTALK_WEBHOOK` | 钉钉 Webhook | - | 否 |
| `FEISHU_WEBHOOK` | 飞书 Webhook | - | 否 |

*如果启用 `EMAIL_NOTIFY=true`，则必须配置

---

### 日志配置

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `LOG_LEVEL` | 日志级别 | `INFO` | 否 |
| `LOG_FILE` | 日志文件 | `./codeql-scanner.log` | 否 |
| `LOG_COLOR` | 彩色日志 | `true` | 否 |

**日志级别 / Log Levels:**
- `DEBUG` - 调试
- `INFO` - 信息
- `WARNING` - 警告
- `ERROR` - 错误

---

## 🚀 使用示例 / Usage Examples

### 示例 1: 基础扫描

```bash
# 1. 配置 .env
cat > .env << EOF
CODEQL_PATH=/opt/codeql/codeql
CODEQL_LANGUAGE=python
OUTPUT_DIR=./scan-results
EOF

# 2. 运行扫描
./run.sh /path/to/project
```

### 示例 2: Jenkins 集成

```bash
# 1. 配置 Jenkins
cat > .env << EOF
JENKINS_URL=http://jenkins.example.com:8080
JENKINS_USER=devops
JENKINS_TOKEN=1234567890abcdef
JENKINS_JOB_NAME=security-scan
JENKINS_UPLOAD_SARIF=true
EOF

# 2. 运行扫描并上传
./run.sh /path/to/project ./output
```

### 示例 3: 靶机分析

```bash
# 1. 配置靶机模式
cat > .env << EOF
LLM_AUTO_ANALYZE=true
LLM_ANALYSIS_MODE=exploit
LLM_GENERATE_EXPLOIT=true
SECURITY_CHECK_BEFORE_SCAN=false
EOF

# 2. 扫描靶机
./run.sh /root/devsecops-python-web ./target-scan
```

### 示例 4: 多语言项目

```bash
# 1. 扫描 Python
CODEQL_LANGUAGE=python ./run.sh /path/to/project ./python-output

# 2. 扫描 JavaScript
CODEQL_LANGUAGE=javascript ./run.sh /path/to/project ./js-output
```

---

## 🔍 配置验证 / Configuration Validation

### 检查配置是否生效

```bash
# 运行配置测试
python3 config_loader.py
```

输出示例：
```
✅ 已加载配置 / Configuration loaded: /path/to/.env

============================================================
  配置摘要 / Configuration Summary
============================================================

📦 CodeQL 配置:
   路径 / Path: /opt/codeql/codeql
   语言 / Language: python
   套件 / Suite: python-security-extended.qls

📁 输出配置:
   目录 / Directory: ./codeql-scan-output
   SARIF: True
   Markdown: True
   Checklist: True

✅ 配置验证通过 / Configuration validation passed
```

### 测试 Jenkins 连接

```bash
python3 jenkins_integration.py
```

输出示例：
```
🔍 测试 Jenkins 连接 / Testing Jenkins connection...
✅ Jenkins 连接成功 / Jenkins connection successful

📋 任务信息 / Job Info:
   名称 / Name: codeql-security-scan
   颜色 / Color: blue
   可构建 / Buildable: true
```

---

## 🐛 故障排查 / Troubleshooting

### 问题 1: 配置未加载

**症状**: 提示 `.env file not found`

**解决**:
```bash
# 确认 .env 文件存在
ls -la .env

# 检查文件权限
chmod 600 .env

# 确认在正确的目录
pwd
```

### 问题 2: Jenkins Token 无效

**症状**: `401 Unauthorized`

**解决**:
1. 重新生成 Jenkins Token
2. 确认用户名正确
3. 检查 Jenkins URL 是否正确

### 问题 3: CodeQL 未找到

**症状**: `codeql: command not found`

**解决**:
```bash
# 在 .env 中设置正确的路径
CODEQL_PATH=/opt/codeql/codeql

# 或添加到系统 PATH
export PATH=/opt/codeql/codeql:$PATH
```

---

## 📚 相关文档 / Related Documentation

- [README_BILINGUAL.md](README_BILINGUAL.md) - 使用指南
- [PRIVACY_AND_SECURITY.md](PRIVACY_AND_SECURITY.md) - 隐私与安全
- [Jenkinsfile](Jenkinsfile) - Jenkins Pipeline 模板

---

**版本 / Version**: 1.0.0  
**最后更新 / Last Updated**: 2026-03-19
