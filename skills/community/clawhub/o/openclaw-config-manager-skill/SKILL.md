# OpenClaw Config Manager Skill

## 概述

OpenClaw配置管理Skill，提供完整的配置备份、恢复、迁移和版本控制功能。

## 功能特性

### 🔄 配置管理
- **智能备份**：自动识别和备份关键配置
- **一键恢复**：从备份快速恢复系统
- **跨环境迁移**：支持不同环境间的配置迁移
- **版本控制**：集成Git进行配置版本管理

### 🔐 安全特性
- **敏感信息脱敏**：自动处理API密钥等敏感信息
- **加密存储**：支持配置文件的加密存储
- **权限控制**：细粒度的访问权限管理

### 🚀 自动化
- **定时备份**：支持定时自动备份
- **变更检测**：自动检测配置变更
- **健康检查**：配置完整性验证

## 安装

### 方式一：从ClawHub安装
```bash
clawhub install openclaw-config-manager
```

### 方式二：手动安装
```bash
# 克隆仓库
git clone https://github.com/wisdom-wozoy/openclaw-config-manager.git

# 安装依赖
cd openclaw-config-manager
npm install

# 注册Skill
openclaw skills register ./openclaw-config-manager
```

## 快速开始

### 1. 初始化配置仓库
```bash
/config git init --url https://github.com/your-username/your-repo
```

### 2. 首次备份
```bash
/config backup --git --message "初始配置备份"
```

### 3. 在新环境恢复
```bash
/config restore --git --url https://github.com/your-username/your-repo
```

## 命令参考

### 备份命令
```bash
# 备份到Git
/config backup --git --message "备份说明"

# 备份到本地文件
/config backup --output ./backup-$(date +%Y%m%d).tar.gz

# 定时备份
/config backup --schedule "0 2 * * *"  # 每天凌晨2点
```

### 恢复命令
```bash
# 从Git恢复
/config restore --git --url https://github.com/username/repo

# 从文件恢复
/config restore --input ./backup.tar.gz

# 恢复特定版本
/config restore --git --commit v1.0.0
```

### 迁移命令
```bash
# 迁移到新服务器
/config migrate --target ssh://user@new-server --env production

# 测试迁移
/config migrate --dry-run --target ssh://user@new-server
```

### Git集成命令
```bash
# 初始化Git仓库
/config git init --url <repository-url>

# 推送更新
/config git push --message "更新说明"

# 拉取更新
/config git pull

# 查看历史
/config git log --oneline

# 创建标签
/config git tag --name v1.0.0 --message "版本1.0.0"
```

### 敏感信息管理
```bash
# 加密敏感信息
/config secrets --encrypt --output ./secrets.enc

# 解密敏感信息
/config secrets --decrypt --input ./secrets.enc

# 轮换密钥
/config secrets --rotate
```

## 配置选项

### Skill配置
在 `openclaw.json` 中添加：
```json
{
  "skills": {
    "openclaw-config-manager": {
      "backup": {
        "schedule": "0 2 * * *",
        "retention": 30,
        "include": ["agents", "workspaces", "config"],
        "exclude": ["logs", "temp", "cache"]
      },
      "git": {
        "repository": "https://github.com/username/repo.git",
        "branch": "main",
        "autoPush": true
      },
      "security": {
        "encryption": "aes-256-gcm",
        "keyRotation": 90
      }
    }
  }
}
```

### 环境变量
```bash
# Git认证
export OPENCLAW_GIT_TOKEN="your-github-token"
export OPENCLAW_GIT_SSH_KEY="~/.ssh/id_ed25519"

# 加密密钥
export OPENCLAW_ENCRYPTION_KEY="your-encryption-key"

# 备份存储
export OPENCLAW_BACKUP_PATH="/backups/openclaw"
```

## 使用场景

### 场景1：日常备份
```bash
# 设置定时备份
/config backup --schedule "0 2 * * *" --git --auto-push

# 手动触发备份
/config backup --now
```

### 场景2：环境迁移
```bash
# 1. 在源环境备份
/config backup --output ./migration.tar.gz

# 2. 传输到目标环境
scp ./migration.tar.gz user@new-server:/tmp/

# 3. 在目标环境恢复
/config restore --input /tmp/migration.tar.gz
```

### 场景3：团队协作
```bash
# 1. 初始化团队仓库
/config git init --url https://github.com/team/openclaw-config

# 2. 添加团队成员
/config git collaborators --add user1@example.com --role admin
/config git collaborators --add user2@example.com --role maintainer

# 3. 设置分支保护
/config git protect --branch main --require-review --require-checks
```

### 场景4：灾难恢复
```bash
# 1. 从最新备份恢复
/config restore --git --latest

# 2. 验证恢复
/config validate --full

# 3. 启动服务
openclaw gateway restart
```

## 高级功能

### 增量备份
```bash
# 启用增量备份
/config backup --incremental --git

# 查看备份差异
/config diff --commit1 HEAD~1 --commit2 HEAD
```

### 配置验证
```bash
# 验证配置完整性
/config validate --full

# 检查配置语法
/config validate --syntax

# 测试配置功能
/config validate --test
```

### 监控和告警
```bash
# 监控配置变更
/config monitor --watch

# 设置变更告警
/config monitor --alert email --recipient admin@example.com
```

## 故障排除

### 常见问题

#### 问题1：Git推送失败
```bash
# 检查Git配置
/config git status

# 重新配置认证
/config git auth --token new-token

# 强制推送
/config git push --force
```

#### 问题2：恢复失败
```bash
# 查看恢复日志
/config restore --log-level debug

# 尝试分步恢复
/config restore --step-by-step

# 使用备份验证
/config backup --verify
```

#### 问题3：权限问题
```bash
# 检查文件权限
/config validate --permissions

# 修复权限
/config fix --permissions

# 以管理员运行
sudo /config restore --input ./backup.tar.gz
```

### 调试模式
```bash
# 启用详细日志
/config backup --verbose --debug

# 查看Skill状态
/config status --detailed
```

## 开发指南

### 项目结构
```
openclaw-config-manager/
├── SKILL.md                    # Skill说明文档
├── package.json               # Skill配置
├── src/
│   ├── commands/              # 命令实现
│   │   ├── backup.js         # 备份命令
│   │   ├── restore.js        # 恢复命令
│   │   ├── migrate.js        # 迁移命令
│   │   └── git.js           # Git集成命令
│   ├── utils/                # 工具函数
│   │   ├── config.js        # 配置处理
│   │   ├── security.js      # 安全处理
│   │   └── validation.js    # 验证工具
│   └── templates/            # 模板文件
│       ├── openclaw.json.template
│       └── secrets.env.template
├── scripts/                  # 辅助脚本
│   ├── deploy.sh
│   ├── restore.sh
│   └── backup.sh
└── docs/                    # 文档
    ├── README.md
    ├── QUICKSTART.md
    └── API.md
```

### 扩展开发
```javascript
// 添加新命令示例
module.exports = {
  name: 'custom-command',
  description: '自定义命令',
  async execute(args, context) {
    // 命令逻辑
  }
};
```

## 许可证

MIT License

## 支持

- 文档：https://github.com/wisdom-wozoy/openclaw-config-manager/docs
- 问题：https://github.com/wisdom-wozoy/openclaw-config-manager/issues
- 讨论：https://github.com/wisdom-wozoy/openclaw-config-manager/discussions

## 版本历史

### v1.0.0 (2026-03-05)
- 初始版本发布
- 基础备份和恢复功能
- Git集成支持
- 敏感信息管理