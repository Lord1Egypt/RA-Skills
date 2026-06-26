# 🚀 CodeQL + LLM 扫描器 - 快速使用指南

## ✅ 当前状态

**项目已 100% 完成并可以使用！**

---

## 📋 配置检查清单

### .env 配置文件

**位置**: `~/.openclaw/workspace/skills/codeql-llm-scanner/.env`

**已配置**:
```ini
✅ CODEQL_PATH=/opt/codeql/codeql
✅ CODEQL_LANGUAGE=python
✅ JENKINS_URL=http://localhost:8080
✅ JENKINS_USER=devops
⚠️ JENKINS_TOKEN=devsecops (建议使用 API Token)
✅ JENKINS_SCAN_TARGET=/root/devsecops-python-web
```

---

## 🎯 三种使用方式

### 方式 1: 一键测试脚本（最简单）✨

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
./test_scan.sh
```

**输出**:
- ✅ 自动检查配置
- ✅ 运行安全检查
- ✅ 执行 CodeQL 扫描
- ✅ 生成 3 个报告文件
- ✅ 显示漏洞统计

---

### 方式 2: 命令行扫描

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner

# 扫描默认目录
./run.sh /root/devsecops-python-web

# 扫描指定目录
./run.sh /path/to/your/project ./output

# 扫描其他语言
CODEQL_LANGUAGE=javascript ./run.sh /path/to/js/project
```

---

### 方式 3: 在对话中使用

```
扫描 /root/devsecops-python-web 的安全漏洞
```

---

## 📁 生成的文件

每次扫描生成 3 个文件：

```
./test-YYYYMMDD-HHMMSS/
├── codeql-results.sarif         # SARIF 格式结果
├── CODEQL_SECURITY_REPORT.md    # 详细安全报告
└── 漏洞验证_Checklist.md        # 验证清单
```

---

## 🏢 Jenkins 集成

### 当前状态

- ✅ Jenkins 服务器：`http://localhost:8080`
- ✅ 用户名：`devops`
- ⚠️ 使用密码而非 API Token（建议更换）
- ✅ SARIF 自动上传成功

### 手动创建 Pipeline（推荐）

由于 CSRF 保护，建议手动创建 Pipeline：

**步骤**:
1. 访问：`http://localhost:8080/newJob`
2. 名称：`codeql-security-scan`
3. 类型：`Pipeline`
4. 复制 `Jenkinsfile` 内容
5. 保存

**详细步骤**: 查看 `JENKINS_MANUAL_SETUP.md`

### 自动生成 API Token

```bash
# 访问 Jenkins 生成 Token
http://localhost:8080/user/devops/security

# 生成后更新 .env
JENKINS_TOKEN=<your-new-token>
```

---

## 🧪 测试结果

### 最新扫描

```
扫描目标：/root/devsecops-python-web
扫描时间：2026-03-19 07:21
发现漏洞：40 个
生成文件：3 个
上传 Jenkins: ✅ 成功
```

### 漏洞统计

```
总发现数：40
⚪ 提示：40
```

---

## 📖 相关文档

| 文档 | 用途 |
|------|------|
| `README_BILINGUAL.md` | 完整使用指南（中英文） |
| `CONFIG_GUIDE.md` | 配置说明 |
| `JENKINS_MANUAL_SETUP.md` | Jenkins 手动配置指南 |
| `JENKINS_SETUP.md` | Jenkins/Gitea设置说明 |
| `TEST_REPORT.md` | 测试报告 |

---

## 🔧 常用命令

### 检查配置

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
cat .env | grep -E "JENKINS|CODEQL"
```

### 测试配置

```bash
python3 config_loader.py
```

### 运行扫描

```bash
./test_scan.sh
```

### 查看报告

```bash
cat ./test-*/CODEQL_SECURITY_REPORT.md
```

### 检查 Jenkins

```bash
curl -u devops:devsecops http://localhost:8080/api/json | python3 -m json.tool
```

---

## ⚠️ 重要提示

### 1. Jenkins API Token

当前使用密码 `devsecops`，建议更换为 API Token：

**原因**:
- 更安全
- 可以单独撤销
- 符合最佳实践

**生成方法**:
1. 访问：`http://localhost:8080/user/devops/security`
2. 点击 "Add new Token"
3. 名称：`CodeQL_Scanner`
4. 生成并复制
5. 更新 `.env` 的 `JENKINS_TOKEN`

### 2. .env 文件权限

```bash
chmod 600 .env
```

### 3. 不要提交到版本控制

```bash
echo ".env" >> .gitignore
```

---

## 🎉 快速验证

运行以下命令验证一切正常：

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner

# 1. 检查配置
python3 config_loader.py

# 2. 运行测试
./test_scan.sh

# 3. 查看结果
ls -lh test-*/
```

---

## 📞 故障排查

### 问题 1: CodeQL 未找到

```bash
# 设置 PATH
export PATH=/opt/codeql/codeql:$PATH

# 或更新 .env
CODEQL_PATH=/opt/codeql/codeql
```

### 问题 2: Jenkins 连接失败

```bash
# 检查 Jenkins 是否运行
curl http://localhost:8080/login

# 检查用户名密码
curl -u devops:devsecops http://localhost:8080/api/json
```

### 问题 3: 扫描失败

```bash
# 查看详细错误
cat ./codeql-scanner.log

# 检查扫描目录
ls -la /root/devsecops-python-web
```

---

## ✅ 验收清单

- [x] .env 配置文件已创建
- [x] CodeQL 已安装并配置
- [x] 可以运行扫描
- [x] 生成 3 个报告文件
- [x] SARIF 上传到 Jenkins
- [x] 文档完整

---

**更新时间**: 2026-03-19  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪
