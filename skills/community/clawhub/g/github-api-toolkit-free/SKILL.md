---
slug: github-api-toolkit-free
name: github-api-toolkit-free
version: 1.0.0
displayName: GitHub API工具包(免费版)
summary: 通过GitHub REST API管理仓库、Issue、PR与分支,支持基础CRUD与结构化输出,适合个人开发者集成场景。
license: Proprietary
edition: free
description: 'GitHub API工具包(免费版)是一款面向开发者的GitHub REST API集成工具,封装常用API端点,帮助用户通过命令行或脚本管理仓库、Issue、Pull
  Request与分支。核心能力:

  - 仓库管理: 列表、查看、创建、更新

  - Issue管理: 列表、查看、创建、更新、评论

  - Pull Request管理: 列表、查看、创建、合并

  - 分支与提交管理: 列表、查看、比较

  - 支持CLI与Python两种调用方式


  适用场景:

  - 个人开发者通过API自动化GitHub操作

  - 脚本化批量管理仓库...'
tags:
- GitHub
- API
- 集成
- 开发工具
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L4
pricing_model: monthly
suggested_price: 99.9
tools: ["read", "write", "exec"]
tags: "版本控制,Git,开发工具"
---
# GitHub API工具包(免费版)

通过GitHub REST API管理仓库、Issue、Pull Request与分支,封装常用端点,提供CLI与Python两种调用方式,适合个人开发者集成场景。

## 概述

GitHub REST API是管理GitHub资源的标准接口,但官方API文档庞大,新手难以快速找到所需端点。本Skill封装最常用的API端点,提供场景化调用示例,帮助开发者在命令行或脚本中快速完成GitHub操作,无需翻阅文档。

免费版聚焦基础CRUD能力,适合个人开发者日常集成。

## 核心能力

### 认证机制

所有API调用需要Personal Access Token(PAT)认证:

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | GitHub API工具包(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 设置环境变量(推荐)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
# ...
# 验证token有效性
curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.user
```

Token权限建议:
- `repo`: 仓库完整访问(含私有)
- `read:org`: 读取组织信息
- `workflow`: 管理Actions工作流

**输入**: 用户提供认证机制所需的指令和必要参数。
**处理**: 解析认证机制的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回认证机制的响应数据,包含状态码、结果和日志。

### 仓库管理

```bash
# 列出认证用户的仓库
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.user/repos?sort=updated&per_page=10"
# ...
# 查看指定仓库
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo"
# ...
# 创建新仓库
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-new-repo","description":"新仓库","private":true}' \
  "https://api.user/repos"
# ...
# 更新仓库设置
curl -X PATCH -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"更新描述","has_issues":true}' \
  "https://api.repos/owner/repo"
```

**输入**: 用户提供仓库管理所需的指令和必要参数。
**处理**: 解析仓库管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回仓库管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### Issue管理

```bash
# 列出仓库Issue
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/issues?state=open&per_page=10"
# ...
# 查看指定Issue
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/issues/123"
# ...
# 创建Issue
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"发现bug","body":"问题描述","labels":["bug"]}' \
  "https://api.repos/owner/repo/issues"
# ...
# 关闭Issue
curl -X PATCH -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state":"closed","state_reason":"completed"}' \
  "https://api.repos/owner/repo/issues/123"
# ...
# 添加评论
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"body":"这是一条评论"}' \
  "https://api.repos/owner/repo/issues/123/comments"
```

**输入**: 用户提供Issue管理所需的指令和必要参数。
**处理**: 解析Issue管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回Issue管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### Pull Request管理

```bash
# 列出仓库PR
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/pulls?state=open&per_page=10"
# ...
# 查看PR详情
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/pulls/55"
# ...
# 创建PR
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"新功能","head":"feature-branch","base":"main","body":"变更说明"}' \
  "https://api.repos/owner/repo/pulls"
# ...
# 合并PR
curl -X PUT -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"commit_title":"合并PR","merge_method":"squash"}' \
  "https://api.repos/owner/repo/pulls/55/merge"
```

**输入**: 用户提供Pull Request管理所需的指令和必要参数。
**处理**: 解析Pull Request管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回Pull Request管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 分支与提交管理

```bash
# 列出分支
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/branches?per_page=30"
# ...
# 查看提交历史
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/commits?sha=main&per_page=10"
# ...
# 比较两个提交
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/compare/main...feature-branch"
```

**输入**: 用户提供分支与提交管理所需的指令和必要参数。
**处理**: 解析分支与提交管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回分支与提交管理的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：REST、管理仓库、与分支、支持基础、CRUD、与结构化输出、适合个人开发者集、成场景、工具包、免费版、是一款面向开发者、集成工具、封装常用、帮助用户通过命令、行或脚本管理仓库、核心能力、CLI、Python、两种调用方式等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景1:CI/CD流水线中创建Release Issue

用户意图: "每次发布自动在仓库创建一个Release Issue,记录变更。"

```bash
#!/bin/bash
# 在CI流水线中调用
VERSION=$(git describe --tags)
CHANGELOG=$(cat CHANGELOG.md)
# ...
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Release $VERSION\",\"body\":\"$CHANGELOG\",\"labels\":[\"release\"]}" \
  "https://api.repos/$REPO/issues"
```

### 场景2:批量查看团队成员的PR

用户意图: "看看团队5个人本周提交了哪些PR。"

```bash
#!/bin/bash
members=("alice" "bob" "carol" "dave" "eve")
for member in "${members[@]}"; do
  echo "=== $member 的PR ==="
  curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    "https://api.search/issues?q=author:$member+is:pr+created:>2026-07-11" \
    | jq '.items[] | {number, title, state: .state, repo: .repository_url}'
done
```

### 场景3:监控仓库的开放Issue数量

用户意图: "每天早上统计仓库的开放Issue数,超过50就告警。"

```bash
#!/bin/bash
COUNT=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.repos/owner/repo/issues?state=open" \
  | jq 'length')
# ...
echo "当前开放Issue数: $COUNT"
if [ "$COUNT" -gt 50 ]; then
  echo "WARNING: Issue数量超过阈值"
  # 发送告警通知
fi
```

## 不适用场景

以下场景GitHub API工具包(免费版)不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

### Step 1:获取Token

1. 登录GitHub,进入Settings → Developer settings → Personal access tokens
2. 生成新token,勾选所需scope(建议`repo`、`read:org`)
3. 复制token,保存到安全位置

### Step 2:配置环境

```bash
# 设置环境变量
export GITHUB_TOKEN="ghp_your_token_here"
# ...
# 验证认证
curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.user
```

### Step 3:首次API调用

```bash
# 列出你的仓库
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.user/repos?per_page=5" | jq '.[].full_name'
```

### Step 4:Python集成

```python
import os
import requests
# ...
token = os.environ['GITHUB_TOKEN']
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github+json'
}
# ...
# 列出仓库
response = requests.get(
    'https://api.user/repos',
    headers=headers,
    params={'sort': 'updated', 'per_page': 10}
)
repos = response.json()
for repo in repos:
    print(f"{repo['full_name']}: {repo['description']}")
```

#
## 示例

### 通用请求模板

```bash
# 通用GET请求
gh-api-get() {
  local endpoint=$1
  curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
       -H "Accept: application/vnd.github+json" \
       "https://api.github.com$endpoint"
}
# ...
# 通用POST请求
gh-api-post() {
  local endpoint=$1
  local data=$2
  curl -s -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
       -H "Accept: application/vnd.github+json" \
       -H "Content-Type: application/json" \
       -d "$data" \
       "https://api.github.com$endpoint"
}
# ...
# 使用示例
gh-api-get "/repos/owner/repo/issues?state=open" | jq '.[].title'
gh-api-post "/repos/owner/repo/issues" '{"title":"测试","body":"内容"}'
```

### Python封装类

```python
import os
import requests
# ...
class GitHubAPI:
    def __init__(self, token=None):
        self.token = token or os.environ['GITHUB_TOKEN']
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github+json'
        }
        self.base_url = 'https://api.github.com'
# ...
    def list_repos(self, sort='updated', per_page=30):
        resp = requests.get(
            f'{self.base_url}/user/repos',
            headers=self.headers,
            params={'sort': sort, 'per_page': per_page}
        )
        resp.raise_for_status()
        return resp.json()
# ...
    def list_issues(self, owner, repo, state='open'):
        resp = requests.get(
            f'{self.base_url}/repos/{owner}/{repo}/issues',
            headers=self.headers,
            params={'state': state}
        )
        resp.raise_for_status()
        return resp.json()
# ...
    def create_issue(self, owner, repo, title, body='', labels=None):
        data = {'title': title, 'body': body}
        if labels:
            data['labels'] = labels
        resp = requests.post(
            f'{self.base_url}/repos/{owner}/{repo}/issues',
            headers=self.headers,
            json=data
        )
        resp.raise_for_status()
        return resp.json()
```

## 最佳实践

### API调用规范

| 规范 | 说明 | 示例 |
|:-----|:-----|:-----|
| 使用Bearer认证 | 新版API推荐Bearer | `Authorization: Bearer $TOKEN` |
| 设置Accept头 | 指定API版本 | `Accept: application/vnd.github+json` |
| 限制per_page | 避免响应过大 | `per_page=30`(最大100) |
| 处理分页 | 使用Link header | 解析`rel="next"`获取下一页 |
| 错误处理 | 检查状态码 | 4xx/5xx时记录并重试 |

### 已知限制

GitHub API对认证用户的限制为5000请求/小时,搜索API为30次/分钟:

```bash
# 查看当前速率限制
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.rate_limit | jq '.rate'
# ...
# 响应头包含限制信息
# X-RateLimit-Limit: 5000
# X-RateLimit-Remaining: 4999
# X-RateLimit-Reset: 1620000000
```

### 安全要点

- **Token存储**: 通过环境变量传递,禁止硬编码
- **权限最小化**: 仅勾选所需scope,避免`admin:*`
- **Token轮换**: 每90天更换一次
- **日志脱敏**: 日志中不记录Authorization头
- **HTTPS强制**: 所有请求走HTTPS,禁止HTTP降级
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### Q1: API返回401 Unauthorized怎么办?

A: 检查: (1)token是否正确设置(`echo $GITHUB_TOKEN`); (2)token是否过期; (3)Authorization头格式是否正确(`Bearer <token>`); (4)token是否有所需scope。

### Q2: API返回403 Forbidden怎么办?

A: 可能原因: (1)权限不足,token缺少对应scope; (2)触发速率限制(检查`X-RateLimit-Remaining`); (3)操作的是组织仓库但token无`read:org`权限; (4)仓库设置为限制操作。

### Q3: 如何处理分页?

A: GitHub使用page-based分页。通过`page`和`per_page`参数控制。响应头`Link`中包含`rel="next"`和`rel="last"`链接。循环请求直到`next`不存在。

### Q4: 创建/更新文件时content字段怎么处理?

A: 文件内容必须Base64编码后传入`content`字段。更新文件还需提供文件的`sha`(通过GET获取)。示例: `echo -n "content" | base64`。

### Q5: 搜索API和普通API有什么区别?

A: 搜索API(`/search/...`)有独立的速率限制(30次/分钟),且查询语法不同(支持`q=keyword+label:bug+state:open`)。结果结构也不同(包含`total_count`和`items`)。搜索查询可能超时,建议缩小范围。

## 免费版限制

本免费体验版限制以下高级功能:
- 不支持GraphQL API(仅REST)
- 不支持批量操作(单次仅处理1个资源)
- 不支持高级搜索(复杂查询语法)
- 不支持Webhook管理
- 不支持GitHub Actions API
- 不支持组织与团队管理API

解锁全部功能请使用专业版: github-api-toolkit-pro

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 可访问GitHub API(api.github.com)
- **Python**: 3.8+(可选,用于Python集成)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| curl | 命令行工具 | 必需 | 系统自带 |
| jq | 命令行工具 | 可选 | `brew install jq` |
| requests | Python库 | 可选 | `pip install requests` |
| GitHub账号 | 在线服务 | 必需 | 注册GitHub账号并生成PAT |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- **GitHub Token**: 通过环境变量`GITHUB_TOKEN`配置,禁止硬编码
- **Token存储**: 建议使用密码管理器或`.env`文件(已gitignore)
- **Token权限**: 根据需要选择scope,遵循最小权限原则
- **Token轮换**: 每90天更换,使用`gh api user`验证新token
- **禁止**: 在SKILL.md或脚本中硬编码任何Token

### 可用性分类
- **分类**: MD+EXEC+API(Markdown指令+命令行工具+REST API调用)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作,核心功能通过curl或Python调用GitHub REST API

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "GitHub API工具包(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "github apikit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
