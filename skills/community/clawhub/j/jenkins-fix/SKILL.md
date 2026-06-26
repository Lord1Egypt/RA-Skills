---
name: jenkins
description: |
  Jenkins 构建助手。触发关键词：
  - 构建、build、编译、打包、部署
  - Jenkins、CI/CD、job、项目
  - 分支、branch、tag
  - 构建状态、构建结果、产物下载
  
  使用场景：
  1. 用户要求构建项目："构建 xxx"、"build xxx"、"编译 xxx"
  2. 用户查询项目列表："Jenkins 项目列表"、"列出所有 job"
  3. 用户指定分支："构建 xxx 分支=yyy"
  4. 用户查看构建结果："xxx 构建状态"

# ⚠️ 安全警告

**此技能已修复为使用环境变量存储认证信息，不再硬编码密码。**

请务必配置 `JENKINS_USERNAME` 和 `JENKINS_API_TOKEN` 或 `JENKINS_PASSWORD` 环境变量后再使用。

详见下方的「认证配置」章节。
---

# Jenkins 构建助手

## 快速使用

**查看所有项目：**
```
Jenkins 项目列表
```
或
```
列出所有 Jenkins job
```

**触发构建（默认分支）：**
```
构建 <项目名>
```

**触发构建（指定分支）：**
```
构建 <项目名> <分支名>
```
或
```
构建 <项目名> 分支=<分支名>
```

**查看构建状态：**
```
<项目名> 构建状态
```

## 认证配置（安全）

### 配置方式（二选一）

**方式一：环境变量（推荐，安全）**

在运行脚本前设置以下环境变量：

```bash
# 方式 A: 使用 API Token（推荐）
export JENKINS_URL="http://jks.huimei-inc.com"
export JENKINS_USERNAME="jiaofu"
export JENKINS_API_TOKEN="your_api_token_here"

# 方式 B: 使用用户名密码（API Token 过期时回退）
export JENKINS_URL="http://jks.huimei-inc.com"
export JENKINS_USERNAME="jiaofu"
export JENKINS_PASSWORD="your_password_here"
```

**方式二：Shell 配置文件（永久生效）**

将上述环境变量添加到 `~/.zshrc` 或 `~/.bash_profile`：

```bash
# Jenkins 构建助手认证信息
export JENKINS_URL="http://jks.huimei-inc.com"
export JENKINS_USERNAME="jiaofu"
export JENKINS_API_TOKEN="your_api_token_here"
```

然后执行：
```bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

### 获取 Jenkins API Token

1. 登录 Jenkins: http://jks.huimei-inc.com
2. 点击右上角用户名 → "Configure"（配置）
3. 在 "API Token" 区域点击 "Add new Token"
4. 复制生成的 Token 到环境变量

### 认证优先级

1. **优先使用 API Token**（更安全，可随时撤销）
2. **回退到用户名密码**（仅当 API Token 失效时）

> **⚠️ 安全提示**：切勿将密码、API Token 提交到版本控制系统（如 git）。使用 `.env` 文件或系统环境变量存储敏感信息。

## 核心功能

### 1. 列出所有项目
返回 Jenkins 中所有可用的 job 名称列表。

### 2. 触发构建
用户指定项目名称后自动触发构建，支持：
- 精确项目名匹配
- 模糊匹配（包含关键词的项目）
- **指定构建分支**（支持多种格式）

### 3. 构建结果
构建完成后返回：
- ✅ 成功：程序包下载地址（OSS 链接）
- ❌ 失败：失败原因和异常信息

## 使用示例

```
用户：Jenkins 项目列表
助手：可用项目：
- hospital__go_crf_service
- hospital__java_omc-business
...

用户：构建 hospital__go_crf_service cloud_251230_release
助手：🔄 正在触发 hospital__go_crf_service 构建...
   使用默认参数: ['HM_ENV', 'REMOTE_HOST', 'PROJECT_TYPE', 'PROJECT_NAME', 'GIT_URL', 'BRANCH_TAG', 'IMAGE_NAME']
   🔀 指定分支: cloud_251230_release
   ✅ 构建已触发，等待构建完成...

✅ hospital__go_crf_service 构建成功！
构建号: #71
耗时: 65.3秒

📦 程序包下载地址：
1. http://ovf.oss-cn-hangzhou.aliyuncs.com/package%2Fpython%2Fcrf_service%2F...
```

## 支持的分支指定格式

| 格式 | 示例 |
|------|------|
| 空格分隔 | `构建 hospital__go_crf_service cloud_251230_release` |
| 分支=参数 | `构建 hospital__go_crf_service 分支=cloud_251230_release` |
| branch=参数 | `构建 hospital__go_crf_service branch=cloud_251230_release` |

## 注意事项

- 构建可能需要几分钟时间，请耐心等待
- 如果构建失败，会显示具体的错误日志
- 程序包下载链接通常为 OSS 格式
- 分支名必须是该 job 支持的 git 分支或 tag
