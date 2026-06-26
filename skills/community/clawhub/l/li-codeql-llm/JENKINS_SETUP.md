# Jenkins 配置说明 / Jenkins Configuration Guide

## 📖 当前配置 / Current Configuration

根据您的需求，已配置以下信息：

```ini
# Jenkins 配置
JENKINS_URL=http://localhost:8080
JENKINS_USER=devops
JENKINS_TOKEN=devsecops
JENKINS_JOB_NAME=codeql-security-scan
JENKINS_UPLOAD_SARIF=true

# Gitea 配置
GITEA_URL=http://localhost:3000
GITEA_USER=devops
GITEA_TOKEN=devsecops
GITEA_REPO_OWNER=devops
GITEA_REPO_NAME=devsecops-python-web
```

---

## ⚠️ 重要提示 / Important Notice

### Jenkins API Token 配置

**当前使用的 `JENKINS_TOKEN=devsecops` 是密码，不是 API Token。**

为了安全起见，建议使用 Jenkins API Token 而不是密码。

### 获取 Jenkins API Token

1. **登录 Jenkins**
   ```
   访问：http://localhost:8080
   用户名：devops
   密码：devsecops
   ```

2. **进入用户配置**
   ```
   点击右上角用户名 (devops) → 配置 (Configure)
   ```

3. **生成 API Token**
   ```
   找到 "API Token" 部分
   点击 "添加新 Token" (Add new Token)
   输入名称：CodeQL Scanner
   点击 "生成" (Generate)
   ```

4. **复制 Token**
   ```
   复制生成的 Token（类似：1185ff36f5e1c67a5b7c7d20731c95937a）
   ⚠️ Token 只显示一次，请妥善保存！
   ```

5. **更新 .env 文件**
   ```bash
   vim .env
   # 修改这一行：
   JENKINS_TOKEN=your-new-token-here
   ```

6. **验证配置**
   ```bash
   python3 jenkins_integration.py
   ```

---

## 🔍 测试 Jenkins 连接

### 方法 1: 使用测试脚本

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
python3 jenkins_integration.py
```

### 方法 2: 使用 curl

```bash
# 测试连接（使用密码）
curl -u devops:devsecops http://localhost:8080/api/json

# 测试连接（使用 Token）
curl -u devops:YOUR_TOKEN http://localhost:8080/api/json
```

### 方法 3: 在 Pipeline 中使用

```groovy
pipeline {
    agent any
    environment {
        JENKINS_CREDENTIALS = credentials('your-credentials-id')
    }
    stages {
        stage('Test') {
            steps {
                sh 'echo "Jenkins is running"'
            }
        }
    }
}
```

---

## 🏢 Gitea 配置说明

### 获取 Gitea Access Token

1. **登录 Gitea**
   ```
   访问：http://localhost:3000
   用户名：devops
   密码：devsecops
   ```

2. **进入设置**
   ```
   点击右上角头像 → 设置 (Settings)
   ```

3. **生成 Access Token**
   ```
   点击 "应用" (Applications)
   在 "管理访问令牌" 下点击 "生成新令牌"
   输入令牌名称：CodeQL Scanner
   选择权限：至少需要 "仓库" 权限
   点击 "生成令牌"
   ```

4. **复制 Token**
   ```
   复制生成的 Token
   ⚠️ Token 只显示一次！
   ```

5. **更新 .env 文件**
   ```bash
   vim .env
   # 修改：
   GITEA_TOKEN=your-gitea-token-here
   ```

---

## 📋 当前服务状态

### 检查服务状态

```bash
# 检查 Jenkins
curl -s http://localhost:8080/login | head -1

# 检查 Gitea
curl -s http://localhost:3000/explore/repos | head -1

# 检查端口
netstat -tlnp | grep -E '8080|3000'
```

### 启动服务（如果未运行）

```bash
# Jenkins (根据安装方式选择)
sudo systemctl start jenkins
# 或
sudo service jenkins start
# 或
java -jar jenkins.war

# Gitea
sudo systemctl start gitea
# 或
sudo service gitea start
```

---

## 🧪 测试配置

### 1. 测试配置加载

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
python3 config_loader.py
```

### 2. 测试 Jenkins 连接

```bash
python3 jenkins_integration.py
```

### 3. 运行完整扫描

```bash
./run.sh /root/devsecops-python-web ./test-output
```

---

## 📝 配置验证清单

- [ ] Jenkins 服务运行中
- [ ] Jenkins API Token 已生成并配置
- [ ] Gitea 服务运行中
- [ ] Gitea Access Token 已生成并配置
- [ ] .env 文件权限正确（600）
- [ ] 配置验证通过

---

## 🔒 安全建议

1. **不要使用密码作为 Token**
   - 使用专门的 API Token
   - Token 可以随时撤销和重新生成

2. **保护 .env 文件**
   ```bash
   chmod 600 .env
   ```

3. **不要提交 .env 到版本控制**
   ```bash
   echo ".env" >> .gitignore
   ```

4. **定期轮换 Token**
   - 每 3-6 个月更换一次
   - 离职员工立即撤销访问

---

## 📞 故障排查

### 问题 1: Jenkins 无法访问

```bash
# 检查服务状态
sudo systemctl status jenkins

# 检查端口
sudo netstat -tlnp | grep 8080

# 查看日志
sudo tail -f /var/log/jenkins/jenkins.log
```

### 问题 2: Token 无效

**症状**: `401 Unauthorized`

**解决**:
1. 重新生成 Token
2. 确认用户名正确
3. 检查 Jenkins 安全配置

### 问题 3: 权限不足

**症状**: `403 Forbidden`

**解决**:
1. 检查用户权限
2. 确认 Token 有足够权限
3. 联系管理员

---

**更新时间**: 2026-03-19  
**版本**: 1.0.0
