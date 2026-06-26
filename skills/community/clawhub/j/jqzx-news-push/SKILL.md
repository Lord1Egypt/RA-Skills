---
name: 每日科技新闻推送
description: |
  每日科技新闻自动推送服务。
  
  **当用户想要「每日科技新闻」「自动推送新闻」「设置新闻定时任务」时使用此技能。**
  
  功能：
  - 获取机器之心最新科技热榜
  - 定时发送到飞书
  - 自动保存到 Get笔记
  
  使用此技能前需要配置：
  - 机器之心 MCP Token
  - Get笔记 API Key 和 Client ID
  - 飞书用户ID
---

# 每日科技新闻推送 Skill

## ⚠️ 必读 - 首次使用配置

### 需要配置的环境变量

**先检查环境变量**：
```bash
echo "JI_ZHIXIN_TOKEN: $JI_ZHIXIN_TOKEN"
echo "GETNOTE_API_KEY: $GETNOTE_API_KEY"
echo "GETNOTE_CLIENT_ID: $GETNOTE_CLIENT_ID"
```

**如果环境变量为空**，告诉用户需要配置以下内容：

> 使用此技能需要先配置以下凭证：
>
> ### 1. 机器之心 Token
> - 访问 https://mcp.applications.jiqizhixin.com/ 申请 MCP/RSS 服务
> - 获取 Token（格式：mcp-sk-xxx）
>
> ### 2. Get笔记 凭证（已有可跳过）
> - 访问 https://www.biji.com/openapi 获取
> - API Key（格式：gk_live_xxx）
> - Client ID（格式：cli_xxx）
>
> ### 3. 飞书用户ID
> - 打开飞书 → 点击头像 → 复制用户ID
> - 格式：ou_xxx
>
> **配置命令**（添加到 ~/.bashrc）：
> ```bash
> export JI_ZHIXIN_TOKEN="你的机器之心Token"
> export GETNOTE_API_KEY="你的Get笔记API Key"
> export GETNOTE_CLIENT_ID="你的Get笔记Client ID"
> export FEISHU_TARGET="你的飞书用户ID"
> ```
> 
> 然后运行 `source ~/.bashrc` 使配置生效

---

## 功能说明

### 核心功能

1. **获取科技新闻** - 从机器之心 RSS 获取最新热榜
2. **飞书推送** - 自动发送到指定飞书用户/群
3. **笔记保存** - 自动保存到 Get笔记
4. **定时任务** - 每天自动执行

### 使用方式

| 用户说 | 含义 |
|--------|------|
| "推送今天的新闻" | 立即获取并发送 |
| "设置每日新闻" | 配置定时任务 |
| "取消新闻推送" | 删除定时任务 |
| "查看新闻配置" | 显示当前配置状态 |

### 定时任务设置

**告诉用户**：设置每天早上 8 点自动推送：

1. 创建定时任务：
```bash
crontab -e
```

添加：
```
0 8 * * * /root/.openclaw/workspace/skills/daily-news-push/scripts/push-news.sh >> /tmp/daily-news.log 2>&1
```

2. 或让用户说"设置每日新闻"，我帮他配置

---

## 脚本说明

### push-news.sh

脚本位置：`/root/.openclaw/workspace/skills/daily-news-push/scripts/push-news.sh`

功能：
1. 获取机器之心 RSS 新闻
2. 发送到飞书
3. 保存到 Get笔记
4. 输出日志

### 配置检查脚本

位置：`/root/.openclaw/workspace/skills/daily-news-push/scripts/check-config.sh`

用于检查环境变量是否配置完整。

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 发送失败 | 检查 FEISHU_TARGET 是否正确 |
| 笔记保存失败 | 检查 GETNOTE_API_KEY 和 CLIENT_ID |
| 获取新闻失败 | 检查 JI_ZHIXIN_TOKEN 是否有效 |
| 定时不执行 | 检查 crontab 是否添加成功 |

---

## 安全规则

- 用户凭证仅用于为该用户服务
- 不保存用户 Token 到代码中
- 定时任务日志包含敏感信息，需保护
