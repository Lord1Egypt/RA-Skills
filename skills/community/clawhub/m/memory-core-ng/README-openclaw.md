# Memory Core - OpenClaw Skill 集成指南

## 🎯 项目改造完成

已按照 OpenClaw skill 格式重构项目结构，现在可以发布到 ClawHub。

## 📁 新的项目结构
```
memory-core/
├── SKILL.md              # ClawHub 必需 - 技能文档
├── package.json          # 简化版配置
├── index.js              # 主入口（代理到 src/index.js）
├── entry.js              # OpenClaw skill 入口文件 ✅
├── README.md             # 项目文档
├── README-openclaw.md    # 本文件
├── .gitignore
├── config/
│   ├── template.json     # 原有配置
│   └── openclaw.json     # OpenClaw 配置模板 ✅
├── src/
│   ├── index.js          # 整合的核心模块 ✅
│   ├── adapters/
│   ├── managers/
│   ├── providers/
│   ├── services/
│   └── utils/
├── examples/
│   └── quick-start.js
├── tests/
│   └── integration.test.js
└── test-real/
    └── real-api-test.js
```

## ✅ 已完成的关键改造

### 1. **添加 OpenClaw skill 必需文件**
- `SKILL.md` - ClawHub 必需文档
- `entry.js` - OpenClaw skill 入口类
- `config/openclaw.json` - OpenClaw 配置模板

### 2. **简化 package.json**
- 移除 `@openclaw/` scope → `memory-core`
- 移除 `devDependencies`
- 添加 `files` 字段
- 添加 `openclaw` 配置段

### 3. **优化项目结构**
- 创建 `src/index.js` 整合模块
- 保持原有功能，简化调用接口
- 确保向后兼容性

### 4. **分支结构**
- 已从 `master` 重命名为 `main`
- 等待 SSH 问题解决后推送

## 🚀 发布到 ClawHub

### 先决条件
1. 解决 SSH 连接问题
2. 确保 GitHub 仓库权限

### 发布步骤
```bash
# 1. 登录 ClawHub
clawhub login

# 2. 发布到 ClawHub
clawhub publish . --version 1.0.0

# 或使用 sync 命令
clawhub sync --dir .
```

### 备用方案（如果重名）
如果 `memory-core` 名称已被占用，可以：
```bash
# 修改 package.json 中的名称
"name": "memory-core-jazzqi"

# 然后重新发布
clawhub publish . --version 1.0.0
```

## 📋 验证发布
1. 访问 https://clawhub.ai
2. 搜索 "memory-core"
3. 查看技能页面是否正确显示

## 🔧 集成到 OpenClaw
用户安装后，在 `~/.openclaw/openclaw.json` 中添加：
```json
"skills": {
  "memory-core": {
    "enabled": true,
    "config": {
      "apiKey": "sk-your-edgefn-api-key"
    }
  }
}
```

## 📞 支持
- 问题反馈: GitHub Issues
- 社区支持: OpenClaw Discord