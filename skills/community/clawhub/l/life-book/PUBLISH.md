# 生命之书 (Life Book) - 发布指南

## 技能已准备就绪 ✅

技能目录：`~/.openclaw/workspace/skills/life-book/`

包含文件：
- `SKILL.md` - 技能文档（含 YAML frontmatter）
- `life-book.sh` - 主执行脚本

## 发布到 ClawHub

### 1. 登录 ClawHub

```bash
clawhub login
clawhub whoami
```

### 2. 发布技能

```bash
clawhub publish ~/.openclaw/workspace/skills/life-book \
  --slug life-book \
  --name "生命之书 (Life Book)" \
  --version 1.0.0 \
  --changelog "首次发布：交互式生命故事记录工具"
```

### 3. 更新技能（后续版本）

```bash
clawhub publish ~/.openclaw/workspace/skills/life-book \
  --slug life-book \
  --name "生命之书 (Life Book)" \
  --version 1.1.0 \
  --changelog "新增：支持多用户、改进交互体验"
```

## 安装使用

其他用户可以通过以下命令安装：

```bash
clawhub install life-book
```

## 技能特点

- 📖 交互式引导记录生命故事
- 📁 支持本地和网络资料收集
- 📝 自动生成 Markdown 格式传记
- 🔒 完全本地化，保护隐私
- 👥 支持多用户管理

## 使用示例

```bash
# 开始记录
./life-book.sh start

# 添加资料
./life-book.sh import ~/photos

# 生成成书
./life-book.sh generate
```

## 注意事项

1. 发布前确保已登录 ClawHub
2. slug 必须唯一（建议使用 `your-username-life-book`）
3. 版本号遵循语义化版本规范（major.minor.patch）
4. changelog 简要说明本次更新内容

## 版本规划

- v1.0.0 - 基础功能（当前）
- v1.1.0 - 添加 AI 辅助内容扩展
- v1.2.0 - 支持导出 PDF/EPUB
- v2.0.0 - 时间线可视化和家族树功能
