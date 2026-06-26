---
name: openclaw-installer-cn
version: 1.0.0
description: OpenClaw 中文安装诊断 - 自动检测安装问题、修复常见错误、生成配置。适合：国内用户、新手安装。
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: ["node", "npm"]
---

# OpenClaw 中文安装诊断 Skill

自动检测安装问题，修复常见错误，生成推荐配置。

## 核心功能

### 1. 环境检测
自动检查：
- Node.js 版本（需要 18+）
- npm/pnpm 版本
- 系统架构（arm64/x64）
- 网络连接
- 磁盘空间

### 2. 问题诊断
常见问题自动修复：
- 网络超时 → 切换国内镜像
- 权限错误 → 修复文件权限
- 依赖冲突 → 清理重装
- 配置错误 → 生成正确配置

### 3. 配置生成
根据使用场景生成：
- 国内优化配置（镜像加速）
- 企业代理配置
- 开发者配置
- 最小化配置

## 使用方法

### 完整诊断

```
诊断我的 OpenClaw 安装
```

Agent 会：
1. 检查环境依赖
2. 检测网络连接
3. 验证配置文件
4. 给出修复建议

### 快速修复

```
修复 OpenClaw 安装问题
```

自动执行：
- 清理缓存
- 重装依赖
- 修复权限
- 更新配置

### 生成配置

```
生成 OpenClaw 国内优化配置
```

输出：
- ~/.openclaw/config.json
- ~/.zshrc 环境变量
- 启动脚本

## 诊断命令

### 检查 Node 版本

```bash
node -v  # 需要 v18.0.0 以上
npm -v   # 需要 9.0.0 以上
```

### 检查网络

```bash
# 测试 npm 源
npm config get registry

# 测试 OpenClaw 源
curl -s -o /dev/null -w '%{http_code}' https://registry.npmjs.org/openclaw
```

### 检查安装

```bash
which openclaw
openclaw --version
openclaw status
```

## 常见问题修复

### 问题 1: 网络超时

```bash
# 切换淘宝镜像
npm config set registry https://registry.npmmirror.com

# 或使用 cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install -g openclaw
```

### 问题 2: 权限错误

```bash
# 修复 npm 权限
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# 或使用 nvm 管理 Node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

### 问题 3: 依赖冲突

```bash
# 清理缓存
npm cache clean --force
rm -rf node_modules
rm package-lock.json

# 重装
npm install
```

### 问题 4: arm64 兼容

```bash
# 检查架构
uname -m

# M1/M2 Mac 需要 Rosetta
softwareupdate --install-rosetta
```

## 推荐配置

### 国内优化配置 (~/.openclaw/config.json)

```json
{
  "model": {
    "default": "deepseek-chat",
    "providers": {
      "deepseek": {
        "apiKey": "${DEEPSEEK_API_KEY}",
        "baseURL": "https://api.deepseek.com"
      },
      "zhipu": {
        "apiKey": "${ZHIPU_API_KEY}",
        "baseURL": "https://open.bigmodel.cn"
      }
    }
  },
  "network": {
    "proxy": null,
    "timeout": 60000
  },
  "heartbeat": {
    "enabled": true,
    "intervalMs": 300000
  }
}
```

### 环境变量 (~/.zshrc)

```bash
# OpenClaw 配置
export OPENCLAW_CONFIG_DIR="$HOME/.openclaw"
export DEEPSEEK_API_KEY="your-key-here"
export ZHIPU_API_KEY="your-key-here"

# 国内镜像加速
export npm_config_registry="https://registry.npmmirror.com"
```

## 输出格式

### 诊断报告

```
🔍 OpenClaw 安装诊断
━━━━━━━━━━━━━━━━━━━━
✅ Node.js: v20.10.0
✅ npm: 10.2.0
✅ 系统架构: arm64 (Apple Silicon)
⚠️  网络: npm 使用官方源，建议切换镜像
❌ OpenClaw: 未安装

📋 修复建议:
1. 切换 npm 镜像: npm config set registry https://registry.npmmirror.com
2. 安装 OpenClaw: npm install -g openclaw
3. 验证安装: openclaw --version
```

## 注意事项

- 国内用户建议使用镜像源
- M1/M2 Mac 确保安装 Rosetta
- 遇到问题先运行诊断
- 配置文件修改后需重启

---

创建：2026-03-12
版本：1.0
