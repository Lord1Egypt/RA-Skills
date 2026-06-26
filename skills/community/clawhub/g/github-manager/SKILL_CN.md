# GitHub Manager Skill

一个全面的GitHub仓库管理工具，提供代码审查、自动部署、changelog生成、CI/CD配置、Bug追踪和项目管理自动化功能。

## 功能特性

### 1. 代码审查
- 自动PR审查和建议
- 代码质量检查
- 安全漏洞扫描
- 代码风格一致性检查

### 2. 自动部署
- 自动化部署流水线
- 多环境部署（开发/测试/生产）
- 回滚机制
- 部署状态监控

### 3. Changelog自动生成
- 基于commit消息自动生成changelog
- 版本号管理
- 发布说明生成

### 4. CI/CD配置
- GitHub Actions工作流模板
- 测试自动化
- 构建和发布流程
- 环境变量管理

### 5. Bug追踪与修复
- Issue模板管理
- Bug优先级分类
- 自动分配和跟踪
- 修复验证

### 6. 项目管理自动化
- 项目看板管理
- 里程碑跟踪
- 自动化任务分配
- 进度报告生成

## 配置要求

### 必需配置
1. **GitHub Token**: 具有repo权限的Personal Access Token
2. **GitHub用户名**: 你的GitHub用户名

### 可选配置
1. **默认仓库**: 经常操作的仓库
2. **Webhook URL**: 用于接收GitHub事件通知
3. **部署环境**: 开发/测试/生产环境配置

## 使用方法

### 初始化配置
```bash
# 设置GitHub认证
github config --token YOUR_GITHUB_TOKEN --username YOUR_USERNAME

# 设置默认仓库
github config --default-repo username/repo-name
```

### 常用命令

#### 仓库管理
```bash
# 列出所有仓库
github repos list

# 创建新仓库
github repos create --name my-new-repo --description "New repository"

# 克隆仓库
github repos clone username/repo-name

# 同步仓库
github repos sync username/repo-name
```

#### 代码审查
```bash
# 审查PR
github review pr --number 123

# 自动审查所有打开的PR
github review all

# 设置审查规则
github review rules --set "require-tests=true"
```

#### 部署管理
```bash
# 部署到开发环境
github deploy dev --branch main

# 部署到生产环境
github deploy prod --tag v1.0.0

# 查看部署状态
github deploy status

# 回滚部署
github deploy rollback --to v0.9.0
```

#### Changelog管理
```bash
# 生成changelog
github changelog generate --since v1.0.0

# 发布新版本
github release create --version v1.1.0 --notes "New features added"

# 更新changelog
github changelog update --version v1.1.1 --type "fix"
```

#### CI/CD管理
```bash
# 查看工作流状态
github ci status

# 运行特定工作流
github ci run --workflow test.yml

# 查看构建日志
github ci logs --run-id 123456
```

#### Bug管理
```bash
# 列出所有issue
github issues list

# 创建bug报告
github issues create --title "Bug found" --body "Description" --label bug

# 分配issue
github issues assign --number 45 --assignee username

# 关闭issue
github issues close --number 45 --comment "Fixed in PR #123"
```

#### 项目管理
```bash
# 查看项目看板
github projects list

# 添加任务到看板
github projects add-task --project "Development" --title "Implement feature X"

# 更新任务状态
github projects update --task 123 --status "In Progress"

# 生成进度报告
github projects report --weekly
```

## 自动化工作流

### 每日检查
```bash
# 检查未处理的PR
github daily-check prs

# 检查失败的CI构建
github daily-check ci

# 检查过期的issue
github daily-check issues
```

### 发布流程
```bash
# 完整的发布流程
github release workflow --version v1.2.0
```

## 配置文件

### config.json
```json
{
  "github": {
    "token": "YOUR_GITHUB_TOKEN",
    "username": "YOUR_USERNAME",
    "defaultRepo": "username/repo-name",
    "webhookUrl": "https://your-webhook-url.com",
    "environments": {
      "dev": {
        "branch": "develop",
        "autoDeploy": true
      },
      "prod": {
        "branch": "main",
        "requireReview": true
      }
    }
  }
}
```

## 安全注意事项

1. **Token安全**: 不要将token提交到版本控制
2. **权限最小化**: 只授予必要的权限
3. **定期轮换**: 定期更新访问token
4. **审计日志**: 记录所有操作

## 故障排除

### 常见问题
1. **认证失败**: 检查token是否有效且有足够权限
2. **API限制**: GitHub API有速率限制，使用缓存避免频繁调用
3. **网络问题**: 检查网络连接和代理设置

### 调试模式
```bash
github --debug <command>
```

## 扩展功能

### 自定义脚本
可以在`scripts/`目录下添加自定义脚本扩展功能。

### 插件系统
支持通过插件添加新功能：
```bash
github plugin install <plugin-name>
```

## 更新和维护

定期检查更新：
```bash
github self-update
```

查看版本信息：
```bash
github version
```

---

**注意**: 使用前请确保已正确配置GitHub认证信息。