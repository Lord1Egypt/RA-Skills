---
name: "github-operations"
description: "提供GitHub操作的完整解决方案，包括仓库管理、分支管理、PR和Issue管理、安全最佳实践、开源项目规范和IM通道集成。当用户需要操作GitHub仓库、创建开源项目或集成IM通道时调用。"
---

# GitHub 操作技能

本技能提供GitHub操作的完整解决方案，包括仓库管理、分支管理、PR和Issue管理、安全最佳实践、开源项目规范和IM通道集成。

## 核心功能

### 1. 仓库管理

- **创建仓库**：支持设置仓库名称、描述和隐私设置
- **列出仓库**：获取用户所有仓库列表
- **查看仓库详情**：获取仓库的详细信息
- **删除仓库**：安全删除指定仓库

### 2. 分支管理

- **创建分支**：从默认分支创建新分支
- **列出分支**：获取仓库的所有分支

### 3. PR管理

- **创建PR**：支持设置标题、内容、源分支和目标分支
- **列出PR**：获取仓库的所有PR

### 4. Issue管理

- **创建Issue**：支持设置标题和内容
- **列出Issue**：获取仓库的开放Issue

### 5. 安全最佳实践

- **Token管理**：使用环境变量存储GitHub token
- **.gitignore配置**：确保敏感文件不被提交
- **Git历史清理**：移除已提交的敏感信息
- **最小权限原则**：使用最小权限的token

### 6. 开源项目规范

- **README.md**：项目说明、安装指南、使用方法
- **LICENSE**：开源许可证文件
- **CONTRIBUTING.md**：贡献指南
- **标准目录结构**：组织代码和文档

### 7. IM通道集成

- **飞书**：通过Webhook发送消息
- **企业微信**：通过企业微信应用发送消息
- **微信个人号**：通过iLink Bot发送消息
- **Slack**：通过Slack API发送消息

## 环境配置

### 1. 安装依赖

```bash
pip install PyGithub python-dotenv requests
```

### 2. 配置环境变量

创建`.env`文件：

```
# GitHub API Token
GITHUB_TOKEN=你的GitHub令牌

# 飞书配置
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-id

# 企业微信配置
WECOM_CORP_ID=你的企业ID
WECOM_APP_SECRET=你的应用密钥
WECOM_AGENT_ID=你的应用ID

# 微信个人号配置
WEIXIN_BOT_TOKEN=你的iLink Bot Token
WEIXIN_API_URL=https://api.ilink.qq.com

# Slack配置
SLACK_API_TOKEN=你的Slack API Token
```

## 使用示例

### 仓库管理

```bash
# 列出所有仓库
python main.py repo list

# 创建新仓库
python main.py repo create --name my-repo --description "我的新仓库"

# 获取仓库详情
python main.py repo get --name my-repo

# 删除仓库
python main.py repo delete --name my-repo
```

### 分支管理

```bash
# 创建新分支
python main.py branch create --repo my-repo --name feature-branch

# 列出分支
python main.py branch list --repo my-repo
```

### PR管理

```bash
# 创建PR
python main.py pr create --repo my-repo --title "添加新功能" --body "这是一个新功能" --head feature-branch --base main

# 列出PR
python main.py pr list --repo my-repo
```

### Issue管理

```bash
# 创建Issue
python main.py issue create --repo my-repo --title "Bug报告" --body "有东西坏了"

# 列出Issue
python main.py issue list --repo my-repo
```

## 安全措施

1. **Token安全**：GitHub token存储在环境变量中，不硬编码在代码中
2. **权限控制**：使用最小权限的token
3. **操作验证**：重要操作需要用户确认
4. **日志记录**：记录所有操作，便于审计
5. **错误处理**：处理异常情况，避免信息泄露

## IM通道集成示例

### 飞书集成

```python
class FeishuIntegration:
    def __init__(self):
        self.feishu_webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
    
    def send_message(self, message):
        if self.feishu_webhook_url:
            payload = {
                "msg_type": "text",
                "content": {
                    "text": message
                }
            }
            response = requests.post(self.feishu_webhook_url, json=payload)
            return response.json()
        return {"error": "FEISHU_WEBHOOK_URL not set"}
```

### 微信集成

```python
class WeChatIntegration:
    def __init__(self):
        # 企业微信配置
        self.wecom_corp_id = os.getenv('WECOM_CORP_ID')
        self.wecom_app_secret = os.getenv('WECOM_APP_SECRET')
        self.wecom_agent_id = os.getenv('WECOM_AGENT_ID')
        
        # 微信个人号配置（使用iLink Bot）
        self.weixin_bot_token = os.getenv('WEIXIN_BOT_TOKEN')
        self.weixin_api_url = os.getenv('WEIXIN_API_URL', 'https://api.ilink.qq.com')
```

## 开源项目规范

### README.md 模板

```markdown
# 项目名称

项目描述

## 功能特性

- 功能1
- 功能2
- 功能3

## 安装说明

1. 克隆仓库
2. 安装依赖
3. 配置环境变量

## 使用方法

### 命令示例

```bash
# 命令1
# 命令2
# 命令3
```

## 贡献指南

详见[CONTRIBUTING.md](CONTRIBUTING.md)文件。

## 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。
```

### .gitignore 模板

```
# 环境变量文件
.env

# 依赖目录
__pycache__/
*.py[cod]

# 编辑器文件
.vscode/
.idea/
*.swp
*.swo
*~

# 系统文件
.DS_Store
Thumbs.db
```

## 最佳实践

1. **代码组织**：使用模块化设计，分离核心逻辑和命令行接口
2. **错误处理**：使用try-except捕获异常，提供友好的错误信息
3. **文档编写**：使用中文编写清晰的文档，便于国内开发者理解
4. **安全意识**：时刻注意保护敏感信息，避免硬编码
5. **版本控制**：使用Git进行版本控制，提交有意义的commit信息

## 常见问题

### 1. GitHub token权限不足

**解决方案**：在GitHub个人访问令牌设置中，确保选择了适当的权限范围，如`repo`权限。

### 2. 网络连接问题

**解决方案**：检查网络连接，确保能访问GitHub API。

### 3. 敏感信息泄露

**解决方案**：使用`.gitignore`文件排除敏感文件，使用环境变量存储敏感信息。

### 4. 命令执行错误

**解决方案**：检查命令参数是否正确，确保仓库名称存在，分支名称有效。

## 总结

本技能提供了GitHub操作的完整解决方案，涵盖了仓库管理、分支管理、PR和Issue管理、安全最佳实践、开源项目规范和IM通道集成。通过使用本技能，用户可以安全、高效地管理GitHub仓库，创建标准化的开源项目，并通过各种IM通道进行控制。
