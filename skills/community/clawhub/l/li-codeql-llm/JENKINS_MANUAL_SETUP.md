# Jenkins Pipeline 手动配置指南
# Jenkins Pipeline Manual Configuration Guide

## ⚠️ 为什么需要手动配置？

由于 Jenkins CSRF 保护，自动创建任务需要正确的 crumb。如果自动创建失败，请按以下步骤手动配置。

---

## 📋 方法 1: 使用 Jenkins Web 界面（推荐）

### 步骤 1: 创建新任务

1. **访问 Jenkins**
   ```
   http://localhost:8080
   用户名：devops
   密码：devsecops
   ```

2. **点击 "新建任务" (New Item)**

3. **输入任务名称**
   ```
   名称：codeql-security-scan
   类型：Pipeline
   ```

4. **点击 "确定" (OK)**

### 步骤 2: 配置 Pipeline

1. **滚动到 "Pipeline" 部分**

2. **选择 "Pipeline script"**

3. **复制以下内容到脚本框**:

```groovy
pipeline {
    agent any
    
    parameters {
        string(name: 'SCAN_TARGET', defaultValue: '/root/devsecops-python-web', description: '要扫描的项目目录')
        string(name: 'CODEQL_LANGUAGE', defaultValue: 'python', description: '编程语言')
        string(name: 'CODEQL_SUITE', defaultValue: 'python-security-extended.qls', description: '查询套件')
        string(name: 'OUTPUT_DIR', defaultValue: './codeql-scan-output', description: '输出目录')
        booleanParam(name: 'SECURITY_CHECK', defaultValue: true, description: '扫描前安全检查')
    }
    
    environment {
        CODEQL_PATH = '/opt/codeql/codeql'
        SCANNER_DIR = "${env.HOME}/.openclaw/workspace/skills/codeql-llm-scanner"
    }
    
    stages {
        stage('准备环境') {
            steps {
                script {
                    echo "🔧 准备扫描环境..."
                    echo "📂 扫描目标：${params.SCAN_TARGET}"
                    env.PATH = "${CODEQL_PATH}:${env.PATH}"
                    sh 'codeql --version'
                }
            }
        }
        
        stage('安全检查') {
            when { expression { return params.SECURITY_CHECK } }
            steps {
                script {
                    echo "🔍 运行安全检查..."
                    sh "cd ${SCANNER_DIR} && python3 security_check.py ${params.SCAN_TARGET} || true"
                }
            }
        }
        
        stage('CodeQL 扫描') {
            steps {
                script {
                    echo "🔍 运行 CodeQL 扫描..."
                    sh """
                        cd ${SCANNER_DIR}
                        export PATH=${CODEQL_PATH}:\$PATH
                        python3 scanner.py \\
                            ${params.SCAN_TARGET} \\
                            --output ${params.OUTPUT_DIR} \\
                            --language ${params.CODEQL_LANGUAGE} \\
                            --suite ${params.CODEQL_SUITE}
                    """
                }
            }
        }
        
        stage('生成报告') {
            steps {
                script {
                    archiveArtifacts artifacts: "${params.OUTPUT_DIR}/*.md,${params.OUTPUT_DIR}/*.sarif", 
                                     fingerprint: true, allowEmptyArchive: true
                }
            }
        }
        
        stage('发布报告') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: params.OUTPUT_DIR,
                    reportFiles: 'CODEQL_SECURITY_REPORT.md',
                    reportName: 'CodeQL Security Report'
                ])
            }
        }
    }
    
    post {
        success {
            echo "✅ 扫描成功完成！"
        }
        failure {
            echo "❌ 扫描失败"
        }
    }
}
```

4. **点击 "保存" (Save)**

### 步骤 3: 运行 Pipeline

1. **点击 "立即构建" (Build Now)**

2. **输入参数**:
   - `SCAN_TARGET`: 要扫描的目录（如：`/root/devsecops-python-web`）
   - `CODEQL_LANGUAGE`: 编程语言（如：`python`）
   - `CODEQL_SUITE`: 查询套件

3. **点击 "构建" (Build)**

---

## 📋 方法 2: 使用 Jenkinsfile

### 步骤 1: 创建任务

1. **访问 Jenkins**
   ```
   http://localhost:8080
   用户名：devops
   密码：devsecops
   ```

2. **新建任务**
   ```
   名称：codeql-security-scan
   类型：Pipeline
   ```

### 步骤 2: 配置 Pipeline script from SCM

1. **在 Pipeline 部分，选择 "Pipeline script from SCM"**

2. **SCM 选择 "Git"**

3. **配置 Git 仓库**（如果有）
   ```
   Repository URL: http://localhost:3000/devops/devsecops-python-web.git
   Credentials: devops/devsecops
   ```

4. **脚本路径**: `Jenkinsfile`

5. **保存**

---

## 📋 方法 3: 使用命令行（需要禁用 CSRF）

### 临时禁用 CSRF（仅测试环境）

```bash
# 1. 访问 Jenkins 脚本命令行
# http://localhost:8080/script

# 2. 执行以下 Groovy 脚本
Jenkins.instance.getDescriptor("hudson.security.csrf.DefaultCrumbIssuer").setUseStandardCrumb(false)
```

### 然后运行创建脚本

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
python3 create_jenkins_job.py
```

---

## 🔧 配置说明

### .env 中的 Jenkins 配置

```ini
# Jenkins 配置
JENKINS_URL=http://localhost:8080
JENKINS_USER=devops
JENKINS_TOKEN=devsecops
JENKINS_JOB_NAME=codeql-security-scan
JENKINS_UPLOAD_SARIF=true

# 默认扫描目录（可以在 Jenkins 中覆盖）
JENKINS_SCAN_TARGET=/root/devsecops-python-web

# 是否自动创建 Jenkins Pipeline
JENKINS_AUTO_CREATE_PIPELINE=true
```

### Pipeline 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `SCAN_TARGET` | 要扫描的目录 | `/root/devsecops-python-web` |
| `CODEQL_LANGUAGE` | 编程语言 | `python` |
| `CODEQL_SUITE` | 查询套件 | `python-security-extended.qls` |
| `OUTPUT_DIR` | 输出目录 | `./codeql-scan-output` |
| `SECURITY_CHECK` | 安全检查 | `true` |

---

## ✅ 验证配置

### 1. 检查任务是否创建

```bash
curl -u devops:devsecops http://localhost:8080/job/codeql-security-scan/api/json
```

### 2. 触发构建

```bash
curl -u devops:devsecops \
  -X POST http://localhost:8080/job/codeql-security-scan/build \
  --data-urlencode json='{"parameter": [{"name":"SCAN_TARGET","value":"/root/devsecops-python-web"}]}'
```

### 3. 查看构建状态

```bash
curl -u devops:devsecops \
  http://localhost:8080/job/codeql-security-scan/lastBuild/api/json
```

---

## 🐛 故障排查

### 问题 1: 403 Forbidden

**原因**: CSRF crumb 问题

**解决**:
1. 使用方法 1（Web 界面）手动创建
2. 或临时禁用 CSRF（测试环境）

### 问题 2: 找不到任务

**解决**:
```bash
# 列出所有任务
curl -u devops:devsecops http://localhost:8080/api/json | python3 -m json.tool
```

### 问题 3: Pipeline 执行失败

**检查**:
1. CodeQL 是否安装
2. 扫描目录是否存在
3. 权限是否正确

---

## 📝 使用示例

### 扫描默认目录

1. 访问：`http://localhost:8080/job/codeql-security-scan`
2. 点击 "立即构建"
3. 使用默认参数
4. 点击 "构建"

### 扫描指定目录

1. 访问：`http://localhost:8080/job/codeql-security-scan`
2. 点击 "立即构建"
3. 修改 `SCAN_TARGET` 参数（如：`/path/to/your/project`）
4. 点击 "构建"

### 扫描其他语言

1. 修改 `CODEQL_LANGUAGE` 参数
   - `python`
   - `javascript`
   - `java`
   - `go`
   - 等
2. 修改 `CODEQL_SUITE` 参数
3. 点击 "构建"

---

**更新时间**: 2026-03-19  
**版本**: 1.0.0
