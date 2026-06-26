# ClawHub 上传指南

## 前置要求

- Node.js v22.12+
- npm 或 yarn
- clawhub CLI 已安装

## 安装 clawhub CLI

```bash
npm install -g clawhub
```

## 登录 ClawHub

```bash
clawhub login
```

## 上传 Skill

```bash
# 进入 skill 目录
cd C:\Users\Administrator\.openclaw\workspace\obsidian-master-skill

# 发布到 ClawHub
clawhub publish

# 或指定版本
clawhub publish --version 1.0.0
```

## 验证上传

访问 ClawHub 网站查看已发布的 Skill：
https://clawhub.com/skills/obsidian-master

## 更新 Skill

```bash
# 修改版本号（package.json）
# 然后重新发布
clawhub publish
```

## 本地测试

```bash
# 本地安装 skill
clawhub install ./obsidian-master-skill

# 测试 skill
openclaw ask "obsidian setup"
```

## 文件结构检查清单

确保以下文件存在：

- [x] SKILL.md - Skill 配置文件
- [x] README.md - 使用说明
- [x] package.json - Node.js 配置
- [x] LICENSE - 许可证
- [x] src/index.js - 主入口文件
- [x] references/templates/ - 模板文件
- [x] assets/logo.svg - Skill 图标
- [x] .gitignore - Git 忽略文件

## 常见问题

### Q: 上传失败怎么办？
A: 检查网络连接，确认 clawhub CLI 已登录

### Q: 如何查看上传日志？
A: 使用 `clawhub publish --verbose` 查看详细日志

### Q: 如何删除已发布的 Skill？
A: 使用 `clawhub unpublish obsidian-master`

## 联系支持

如有问题，请访问：
- ClawHub 文档：https://clawhub.com/docs
- 社区论坛：https://discord.gg/clawd

---

**最后更新：** 2026-03-05
