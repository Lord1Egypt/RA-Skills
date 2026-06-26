---
name: paperdaily
description: 每日从 arXiv 计算机科学论文中筛选高价值文献推荐
---

# PaperDaily Skill

每日从 arXiv 计算机科学论文中筛选高价值文献推荐。

## 安装

```bash
cd ~/.openclaw/skills/paperdaily
npm install
```

安装后创建配置文件 `node_modules/openclaw-paperdaily/.env`：

```env
# 飞书应用配置（必填）
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_CHAT_ID=your_chat_id

# 可选配置
DEFAULT_TIMEZONE=Asia/Shanghai
CACHE_HOURS=24
KEYWORDS=machine learning,deep learning,transformer,LLM
```

## 触发词

- `今日文献` - 获取今日推荐的计算机论文（使用缓存）
- `刷新文献` - 强制刷新并获取新的今日推荐论文

## 使用方式

在聊天中发送 "今日文献" 或 "刷新文献" 即可触发。

## 功能说明

- 从 arXiv CS 类近 7 天论文中筛选
- 基于时间新鲜度 (30%)、关键词匹配 (40%)、信息量 (30%) 评分
- 同一天多次请求返回缓存结果
- 支持强制刷新

## 配置说明

| 变量 | 说明 | 必填 |
|------|------|------|
| `FEISHU_APP_ID` | 飞书应用 ID | ✅ |
| `FEISHU_APP_SECRET` | 飞书应用 Secret | ✅ |
| `FEISHU_CHAT_ID` | 飞书群聊 ID | ✅ |
| `KEYWORDS` | 论文筛选关键词 | ❌ |
| `DEFAULT_TIMEZONE` | 默认时区 | ❌ |
| `CACHE_HOURS` | 缓存时长（小时） | ❌ |

## 获取飞书配置

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置应用权限并发布
5. 将机器人添加到目标群聊，获取 Chat ID
