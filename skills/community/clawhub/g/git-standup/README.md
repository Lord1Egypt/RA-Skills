# Git Standup

分析 Git 提交自动生成工作日报

## 功能特性

- 📅 按日期范围筛选提交
- 👤 支持多作者筛选
- 📁 按仓库/目录分组
- 🏷️ 智能分类（功能/修复/重构/文档）
- 📝 生成 Markdown 格式日报
- 🔗 自动关联 issue/PR 链接

## 安装

作为 OpenClaw Skill 使用:
```bash
clawhub install git-standup
```

或直接使用:
```bash
git clone https://github.com/kimi-claw/skill-git-standup.git
cd skill-git-standup
./bin/daily-standup --help
```

## 使用方法

### 生成今日日报

```bash
/daily-standup
```

### 生成指定日期日报

```bash
/daily-standup --date 2026-03-10
```

### 生成周报

```bash
/daily-standup --since "1 week ago"
```

### 指定作者

```bash
/daily-standup --author "username"
```

### 多仓库汇总

```bash
/daily-standup --repos /path/to/project1,/path/to/project2
```

## 提交信息规范

工具会解析符合以下格式的提交信息：

```
[type] 描述 (#issue)

类型:
- feat: 新功能
- fix: 修复
- refactor: 重构
- docs: 文档
- test: 测试
- chore: 杂项
```

## License

MIT
