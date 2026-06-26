# GitHub Issue Auto Triage Skill

🤖 自动分类 GitHub Issue，AI 智能打标签、分配负责人、检测重复、回复 FAQ

## ✨ 功能特性

- 🏷️ **AI 智能分类** - 自动识别 bug/enhancement/question/documentation
- 👤 **自动分配** - 根据 Issue 类型分配给合适的负责人
- 🔍 **重复检测** - 语义相似度分析，发现重复 Issue
- 💬 **FAQ 自动回复** - 识别常见问题并自动回复
- 📊 **处理报告** - 详细的处理日志和统计
- 🔒 **安全模式** - 支持 dry-run 预览操作

## 🚀 快速开始

### 1. 安装

```bash
cd /home/admin/.openclaw/workspace/skills/github-issue-auto-triage
```

### 2. 配置环境变量

```bash
# GitHub 配置
export GITHUB_TOKEN="your_github_token"
export GITHUB_OWNER="your-org"
export GITHUB_REPO="your-repo"

# AI 配置（可选，用于更准确的分类）
export DASHSCOPE_API_KEY="sk-xxx"
```

### 3. 运行

```bash
# Dry run 模式（预览）
python3 scripts/triage.py --dry-run

# 正式运行
python3 scripts/triage.py

# 处理特定 Issue
python3 scripts/triage.py --issue 123
```

## 📋 配置说明

### 默认配置

配置文件：`config.json`（可选）

```json
{
  "triage": {
    "enabled": true,
    "interval_minutes": 30,
    "auto_label": true,
    "auto_assign": true,
    "detect_duplicates": true,
    "auto_reply_faq": true
  },
  "labels": {
    "bug": {
      "keywords": ["bug", "error", "crash", "fail"],
      "priority": "high"
    },
    "enhancement": {
      "keywords": ["feature", "enhancement", "improve"],
      "priority": "medium"
    },
    "question": {
      "keywords": ["question", "help", "how to"],
      "priority": "low"
    }
  },
  "faq": [
    {
      "keywords": ["install", "installation"],
      "answer": "See installation guide: https://docs.example.com/install"
    }
  ]
}
```

### 自定义配置

```bash
# 使用自定义配置运行
python3 scripts/triage.py --config my-config.json
```

## 📖 使用示例

### 示例 1: 处理所有未分类 Issue

```bash
python3 scripts/triage.py
```

输出：
```
🚀 开始 GitHub Issue 自动分类
📅 时间：2026-03-16 15:45:00
📂 仓库：openclaw/openclaw
🔧 模式：正式运行

📊 发现 5 个未分类 Issue

============================================================
📋 处理 Issue #123: App crashes on startup
============================================================

🔍 正在分类...
✅ 分类结果：bug (优先级：high)

🔍 检测重复 Issue...
✅ 未发现重复 Issue

🔍 检查 FAQ...

🏷️  添加标签：bug
✅ 标签添加成功

✅ Issue #123 处理完成

...

============================================================
📊 处理总结
============================================================
处理 Issue 数：5
成功：5
失败：0

💾 结果已保存到：triage_results_20260316_154500.json
```

### 示例 2: Dry Run 模式

```bash
python3 scripts/triage.py --dry-run
```

预览将要执行的操作，不实际修改 Issue。

### 示例 3: 处理特定 Issue

```bash
python3 scripts/triage.py --issue 123
```

## 🔧 GitHub Token 获取

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择权限：
   - ✅ `repo` (完整仓库权限)
   - ✅ `read:user` (读取用户信息)
4. 生成并复制 Token
5. 设置环境变量：`export GITHUB_TOKEN="your_token"`

## 📊 输出文件

运行后生成 JSON 报告：

```json
{
  "timestamp": "2026-03-16T15:45:00",
  "repository": "openclaw/openclaw",
  "dry_run": false,
  "issues_processed": 5,
  "results": [
    {
      "issue_number": 123,
      "classification": {
        "suggested_label": "bug",
        "priority": "high"
      },
      "actions": ["Added label: bug"],
      "success": true
    }
  ]
}
```

## 🤖 定时任务

### Cron 配置

```bash
# 每 30 分钟运行一次
*/30 * * * * cd /path/to/skill && python3 scripts/triage.py >> logs/triage.log 2>&1
```

### Systemd 配置

```ini
[Unit]
Description=GitHub Issue Triage
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/scripts/triage.py
Environment=GITHUB_TOKEN=your_token
Environment=GITHUB_OWNER=your-org
Environment=GITHUB_REPO=your-repo
```

## 🔒 安全说明

- ✅ Token 通过环境变量管理，不写入代码
- ✅ 支持 dry-run 模式预览操作
- ✅ 所有操作记录日志
- ✅ 最小权限原则
- ⚠️ 不要将 Token 提交到 Git

## 🛠️ 故障排查

### 问题 1: 认证失败

```
❌ 错误：401 Unauthorized
```

**解决**: 检查 GITHUB_TOKEN 是否正确设置

```bash
echo $GITHUB_TOKEN  # 应该显示你的 Token
```

### 问题 2: 权限不足

```
❌ 错误：403 Forbidden
```

**解决**: 确保 Token 有 `repo` 权限

### 问题 3: 找不到 Issue

```
❌ 错误：404 Not Found
```

**解决**: 检查 GITHUB_OWNER 和 GITHUB_REPO 是否正确

## 📝 开发计划

- [ ] 支持 GitLab
- [ ] 支持 Jira
- [ ] Slack/Discord 通知集成
- [ ] 更智能的重复检测（使用 Embedding）
- [ ] 自动关闭重复 Issue
- [ ] 多仓库管理
- [ ] Web UI 管理界面

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 支持

遇到问题？请提交 Issue 或联系作者。

---

**版本**: 1.0.0  
**作者**: 于金泽  
**创建时间**: 2026-03-16
