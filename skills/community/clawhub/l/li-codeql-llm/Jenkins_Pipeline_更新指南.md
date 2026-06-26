# 🔄 Jenkins Pipeline 更新指南

## ❌ 问题原因

Jenkins Pipeline 使用的是**旧版本**脚本，缺少 `mkdir -p` 命令来创建输出目录。

**错误信息**:
```
A fatal error occurred: Cannot create database at 
/root/.openclaw/workspace/skills/codeql-llm-scanner/codeql-scan-output/codeql-db 
because /root/.openclaw/workspace/skills/codeql-llm-scanner/codeql-scan-output does not exist.
```

---

## ✅ 解决方案

### 方法 1: Jenkins 界面更新（推荐，2 分钟）

#### 步骤 1: 访问配置页面

打开浏览器访问：
```
http://192.168.4.53:8080/job/codeql-security-scan/configure
```

#### 步骤 2: 找到 Pipeline 部分

向下滚动到 **"Pipeline"** 部分

#### 步骤 3: 更新脚本

找到 **"CodeQL 数据库创建 / Create Database"** 阶段，修改为：

```groovy
stage('CodeQL 数据库创建 / Create Database') {
    steps {
        script {
            echo "📦 创建 CodeQL 数据库..."
            
            // ✅ 添加这一行：确保输出目录存在
            sh """
                mkdir -p ${params.OUTPUT_DIR}
            """
            
            sh """
                cd ${SCANNER_DIR}
                export PATH=${CODEQL_PATH}:\$PATH
                codeql database create ${params.OUTPUT_DIR}/codeql-db \
                    --language=${params.CODEQL_LANGUAGE} \
                    --source-root=${params.SCAN_TARGET} \
                    --overwrite
            """
        }
    }
}
```

**关键**: 添加 `mkdir -p ${params.OUTPUT_DIR}` 这一行

#### 步骤 4: 保存

点击页面底部的 **"保存"** 按钮

#### 步骤 5: 重新构建

1. 访问：`http://192.168.4.53:8080/job/codeql-security-scan/`
2. 点击 **"立即构建"**
3. 使用默认参数
4. 点击 **"构建"**

---

### 方法 2: 使用 Groovy 脚本更新（高级）

#### 步骤 1: 访问脚本命令行

访问：
```
http://192.168.4.53:8080/script
```

#### 步骤 2: 执行更新脚本

```groovy
import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.*

def jobName = "codeql-security-scan"
def job = Jenkins.instance.getItemByFullName(jobName, WorkflowJob.class)

if (job) {
    println "✅ 找到任务：${jobName}"
    
    // 读取新的 Jenkinsfile
    def jenkinsfile = new File('/root/.openclaw/workspace/skills/codeql-llm-scanner/Jenkinsfile').text
    
    // 更新 Pipeline 定义
    def definition = new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(jenkinsfile, true)
    job.definition = definition
    job.save()
    
    println "✅ Pipeline 已更新"
} else {
    println "❌ 任务不存在：${jobName}"
}
```

#### 步骤 3: 运行

点击 **"运行"** 按钮

#### 步骤 4: 验证

访问 Pipeline 配置页面，确认脚本已更新

---

### 方法 3: 完全重新创建（如果以上都失败）

#### 步骤 1: 删除旧任务

访问：
```
http://192.168.4.53:8080/job/codeql-security-scan/doDelete
```

确认删除

#### 步骤 2: 重新创建

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner
python3 create_jenkins_pipeline.py
```

---

## 📋 验证更新

### 检查点 1: 脚本中包含 mkdir

在 Pipeline 配置页面，搜索 `mkdir -p`，应该能找到

### 检查点 2: 运行测试构建

```
1. 点击 "立即构建"
2. 使用默认参数
3. 观察控制台输出
```

### 预期输出

```
✅ 准备环境
✅ 安全检查
✅ 创建 CodeQL 数据库  ← 这步应该成功
📦 创建 CodeQL 数据库...
+ mkdir -p ./codeql-scan-output
+ codeql database create ./codeql-scan-output/codeql-db ...
✅ 数据库创建成功
✅ 运行安全扫描
✅ 生成报告
✅ 发布报告
✅ 扫描成功完成
```

---

## 🐛 常见问题

### Q1: 找不到 "CodeQL 数据库创建" 阶段

**A**: 滚动查找 `stage('CodeQL` 关键字

### Q2: 保存后不生效

**A**: 
1. 清除浏览器缓存
2. 重新加载配置页面
3. 确认脚本已更新

### Q3: 构建仍然失败

**A**: 检查控制台输出，确认是否有 `mkdir -p` 命令执行

---

## 📊 对比

### ❌ 旧版本（会失败）

```groovy
stage('CodeQL 数据库创建') {
    steps {
        script {
            sh """
                codeql database create ./codeql-scan-output/codeql-db ...
            """
        }
    }
}
```

**问题**: 没有创建目录

---

### ✅ 新版本（成功）

```groovy
stage('CodeQL 数据库创建') {
    steps {
        script {
            // ✅ 先创建目录
            sh """
                mkdir -p ./codeql-scan-output
            """
            
            // ✅ 再创建数据库
            sh """
                codeql database create ./codeql-scan-output/codeql-db ...
            """
        }
    }
}
```

**解决**: 先创建目录，再创建数据库

---

## ✅ 验收清单

更新后检查：

- [ ] Pipeline 配置已保存
- [ ] 脚本包含 `mkdir -p`
- [ ] 重新构建成功
- [ ] 所有阶段都是绿色✅
- [ ] 报告生成成功
- [ ] Jenkins 可以看到报告

---

## 🎯 快速验证命令

```bash
# 1. 检查 Jenkinsfile 是否已更新
grep "mkdir -p" ~/codeql-llm-scanner/Jenkinsfile

# 2. 触发构建
curl -u devops:110ffb6071ded434a52bd153217f3fc873 \
  -X POST "http://192.168.4.53:8080/job/codeql-security-scan/build" \
  --data-urlencode "json={'parameter': [{'name':'SCAN_TARGET','value':'/root/devsecops-python-web'}]}"

# 3. 查看构建状态
curl -u devops:110ffb6071ded434a52bd153217f3fc873 \
  "http://192.168.4.53:8080/job/codeql-security-scan/lastBuild/api/json" | python3 -m json.tool
```

---

**更新时间**: 2026-03-19  
**预计时间**: 2-5 分钟  
**难度**: 简单
