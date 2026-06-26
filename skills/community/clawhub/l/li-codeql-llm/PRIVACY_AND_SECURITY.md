# CodeQL + LLM 融合扫描器 - 隐私与安全声明

# CodeQL + LLM Fusion Scanner - Privacy and Security Statement

---

## 🔒 隐私保护声明 / Privacy Protection Statement

### 中文

**本工具严格保护用户隐私，不会收集、存储或传输任何个人敏感信息。**

#### 数据收集原则

1. **零数据收集** - 本工具不收集任何用户数据
2. **本地处理** - 所有扫描在本地完成，数据不出境
3. **无远程传输** - 扫描结果不会发送到任何远程服务器
4. **用户控制** - 所有输出文件由用户完全控制

#### 扫描数据安全

- ✅ 源代码：仅在本地分析，不上传
- ✅ 扫描结果：存储在用户指定目录
- ✅ 报告文件：生成在本地，不共享
- ✅ LLM 分析：用户可选择是否发送

#### 敏感信息处理

如果扫描发现敏感信息（如密码、密钥等）：

1. **不会自动发送** - 需要用户明确授权
2. **脱敏处理** - 建议用户手动脱敏
3. **本地存储** - 敏感信息保留在本地
4. **用户删除** - 用户可随时删除所有输出

---

### English

**This tool strictly protects user privacy and does not collect, store, or transmit any personal sensitive information.**

#### Data Collection Principles

1. **Zero Data Collection** - This tool does not collect any user data
2. **Local Processing** - All scans are completed locally, data does not leave your environment
3. **No Remote Transmission** - Scan results are not sent to any remote servers
4. **User Control** - All output files are fully controlled by the user

#### Scan Data Security

- ✅ Source code: Only analyzed locally, not uploaded
- ✅ Scan results: Stored in user-specified directory
- ✅ Report files: Generated locally, not shared
- ✅ LLM analysis: User can choose whether to send

#### Sensitive Information Handling

If sensitive information is discovered during scanning (such as passwords, keys, etc.):

1. **No Automatic Sending** - Requires explicit user authorization
2. **Desensitization** - Users are advised to manually desensitize
3. **Local Storage** - Sensitive information remains local
4. **User Deletion** - Users can delete all outputs at any time

---

## 🛡️ 安全检查清单 / Security Checklist

### 中文

#### 使用前检查

- [ ] 确认在安全环境中运行
- [ ] 确认有代码扫描权限
- [ ] 了解输出文件位置
- [ ] 确认不会扫描未授权代码

#### 扫描过程安全

- [ ] 不包含生产环境密钥
- [ ] 不包含真实用户数据
- [ ] 已排除敏感目录（如 `.git/`, `credentials/`）
- [ ] 扫描结果存储在安全位置

#### 输出文件安全

- [ ] 报告文件权限设置为仅用户可读
- [ ] 不将报告上传到公共仓库
- [ ] 定期清理扫描输出
- [ ] 敏感漏洞信息加密存储

---

### English

#### Pre-usage Checks

- [ ] Confirm running in a secure environment
- [ ] Confirm having permission to scan the code
- [ ] Understand output file locations
- [ ] Confirm not scanning unauthorized code

#### Scan Process Security

- [ ] No production environment keys included
- [ ] No real user data included
- [ ] Sensitive directories excluded (e.g., `.git/`, `credentials/`)
- [ ] Scan results stored in secure location

#### Output File Security

- [ ] Report file permissions set to user-read-only
- [ ] Do not upload reports to public repositories
- [ ] Regularly clean up scan outputs
- [ ] Encrypt storage of sensitive vulnerability information

---

## ⚠️ 安全警告 / Security Warnings

### 中文

**警告 1**: 不要在未授权的代码上运行扫描

```bash
# ❌ 错误：扫描他人代码
./run.sh /path/to/someone-else-project

# ✅ 正确：扫描自己的项目
./run.sh /path/to/my-project
```

**警告 2**: 保护扫描结果

```bash
# ❌ 错误：公开扫描结果
git add codeql-results.sarif
git commit -m "Add security scan results"

# ✅ 正确：添加到 .gitignore
echo "codeql-scan-output/" >> .gitignore
```

**警告 3**: 注意敏感信息

扫描可能发现硬编码密码、API 密钥等：

```bash
# 如果发现敏感信息，立即：
# 1. 不要提交到版本控制
# 2. 立即删除或轮换密钥
# 3. 审查代码历史
```

---

### English

**Warning 1**: Do not run scans on unauthorized code

```bash
# ❌ Wrong: Scanning someone else's code
./run.sh /path/to/someone-else-project

# ✅ Correct: Scanning your own project
./run.sh /path/to/my-project
```

**Warning 2**: Protect scan results

```bash
# ❌ Wrong: Publishing scan results publicly
git add codeql-results.sarif
git commit -m "Add security scan results"

# ✅ Correct: Add to .gitignore
echo "codeql-scan-output/" >> .gitignore
```

**Warning 3**: Watch for sensitive information

Scans may discover hardcoded passwords, API keys, etc.:

```bash
# If sensitive information is found, immediately:
# 1. Do not commit to version control
# 2. Delete or rotate keys immediately
# 3. Review code history
```

---

## 📋 隐私保护最佳实践 / Privacy Best Practices

### 中文

#### 1. 扫描前

```bash
# 检查将要扫描的内容
ls -la /path/to/project

# 排除敏感目录
./run.sh /path/to/project \
  --exclude .git \
  --exclude credentials \
  --exclude .env
```

#### 2. 扫描中

```bash
# 在隔离环境中运行
docker run --rm -v $(pwd):/workspace codeql-scanner

# 或使用虚拟环境
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. 扫描后

```bash
# 设置文件权限
chmod 600 codeql-results.sarif
chmod 600 CODEQL_SECURITY_REPORT.md

# 定期清理
find ./codeql-scan-output -mtime +30 -delete
```

---

### English

#### 1. Before Scanning

```bash
# Check what will be scanned
ls -la /path/to/project

# Exclude sensitive directories
./run.sh /path/to/project \
  --exclude .git \
  --exclude credentials \
  --exclude .env
```

#### 2. During Scanning

```bash
# Run in isolated environment
docker run --rm -v $(pwd):/workspace codeql-scanner

# Or use virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. After Scanning

```bash
# Set file permissions
chmod 600 codeql-results.sarif
chmod 600 CODEQL_SECURITY_REPORT.md

# Regular cleanup
find ./codeql-scan-output -mtime +30 -delete
```

---

## 🔐 数据安全配置 / Data Security Configuration

### config.example.ini (安全配置)

```ini
# 安全配置 / Security Configuration
[security]
# 排除的目录 / Excluded directories
exclude_dirs = .git,credentials,.env,node_modules

# 文件权限 / File permissions
file_permissions = 600

# 自动清理天数 / Auto cleanup days
auto_cleanup_days = 30

# LLM 分析前脱敏 / Desensitize before LLM analysis
llm_desensitize = true

# 本地存储 / Local storage only
local_only = true
```

---

## 🚨 应急响应 / Emergency Response

### 中文

**如果发现敏感信息泄露：**

1. **立即停止** - 停止所有扫描和传输
2. **删除文件** - 删除所有包含敏感信息的输出
3. **轮换密钥** - 立即更换所有泄露的密钥
4. **审查日志** - 检查是否有未授权访问
5. **报告事件** - 向相关人员报告

---

### English

**If sensitive information leakage is discovered:**

1. **Stop Immediately** - Halt all scanning and transmission
2. **Delete Files** - Remove all outputs containing sensitive information
3. **Rotate Keys** - Immediately change all leaked keys
4. **Review Logs** - Check for unauthorized access
5. **Report Incident** - Report to relevant personnel

---

## 📞 联系方式 / Contact

### 中文

**隐私和安全问题请联系：**

- 项目管理员
- 安全团队
- 通过官方渠道报告

---

### English

**For privacy and security concerns, contact:**

- Project Administrator
- Security Team
- Report through official channels

---

**版本 / Version**: 1.0.0  
**更新日期 / Last Updated**: 2026-03-19  
**生效日期 / Effective Date**: 立即生效 / Effective Immediately

---

## ✅ 隐私合规检查表 / Privacy Compliance Checklist

### 中文

- [x] 明确数据收集政策
- [x] 说明数据处理方式
- [x] 提供用户控制选项
- [x] 包含安全警告
- [x] 提供应急响应流程
- [x] 多语言支持（中英文）
- [ ] 第三方审计（可选）
- [ ] 法律审查（可选）

---

### English

- [x] Clear data collection policy
- [x] Explain data handling methods
- [x] Provide user control options
- [x] Include security warnings
- [x] Provide emergency response procedures
- [x] Multi-language support (Chinese/English)
- [ ] Third-party audit (optional)
- [ ] Legal review (optional)

---

**本声明定期审查和更新 / This statement is regularly reviewed and updated**
