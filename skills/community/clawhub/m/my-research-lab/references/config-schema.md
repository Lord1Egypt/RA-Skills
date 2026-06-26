# 配置文件 Schema (lab-config.json)

每个研究院实例维护独立的 lab-config.json，存储在记忆系统中。同时在本地存档目录保留一份副本。

## 完整 Schema

```json
{
  "name": "[研究院名称]",
  "domain": "[研究方向]",
  "version": "3.3.0",
  "cronJobs": {
    "dailyDiscovery": { "id": "xxx", "time": "09:00" },
    "thoughtExperiment": { "id": "xxx", "frequency": "weekly", "day": "wed" }
  },
  "keywords": {
    "zh": ["关键词1"],
    "en": ["keyword1"]
  },
  "domains": [
    { "name": "主方向", "weight": 1.0 },
    { "name": "子方向（可选）", "weight": 0.7 }
  ],
  "sourceList": [
    { "name": "信源", "url": "...", "weight": 1.0, "missCount": 0 }
  ],
  "domainSpecificSkills": [
    {
      "skillId": "aihot-skill",
      "displayName": "AI HOT 实时资讯",
      "matchedDomain": "AI/大模型",
      "enabled": true,
      "endpoint": "https://aihot.virxact.com",
      "missCount": 0,
      "hitRate": 0.85
    }
  ],
  "pushChannels": {
    "email": { "enabled": true, "address": "..." },
    "wecom": { "enabled": true, "webhookUrl": "..." },
    "localFile": { "enabled": true }
  },
  "storage": {
    "primary": "wecomDoc|local|wiki",
    "wecomDoc": { "enabled": false, "url": "...", "spaceId": "..." },
    "local": { "enabled": true, "path": "./research-lab-archive/" }
  },
  "boundMasters": [
    { "skillId": "xxx-perspective", "displayName": "大师名", "matchScore": 0.9 }
  ],
  "masterRotation": {
    "enabled": true,
    "currentWeek": ["masterA-perspective", "masterB-perspective"],
    "rotationLog": []
  },
  "activeProjects": [
    {
      "name": "项目名",
      "status": "进行中",
      "startDate": "2026-04-08",
      "tasks": [],
      "fromExperiment": "2026-04-05-xxx"
    }
  ],
  "feedbackRules": [
    { "rule": "不要推送纯广告内容", "source": "user", "date": "2026-04-08" }
  ],
  "preferences": {
    "pushTime": "09:00",
    "language": "zh+en",
    "maxItemsPerDay": 5,
    "masterCommentary": true,
    "autoAction": false,
    "dedupeWindowDays": 30,
    "domainCoverageCheck": true
  }
}
```

## 关键字段说明

| 字段 | 说明 |
|------|------|
| `domains` | 研究子方向，配置多个时启用领域覆盖自检 |
| `domainSpecificSkills` | 领域专属信源 skill 列表（如 AI 领域的 aihot-skill） |
| `boundMasters` | 绑定的大师列表，自动扫描填充 |
| `masterRotation.currentWeek` | 本周轮值大师 |
| `feedbackRules` | 用户反馈生成的过滤规则 |
| `preferences.dedupeWindowDays` | 排重窗口天数（默认 30） |
| `preferences.domainCoverageCheck` | 是否启用多领域覆盖自检 |
| `activeProjects` | 当前在跟的动手实践项目 |

## 多研究院隔离

一个用户可运行多个研究院实例，每个实例必须独立的：
- lab-config.json（独立配置，独立记忆键名）
- 定时任务（独立 cron job，不同时间避免冲突）
- 推送渠道（可共用，但必须各自验证可用性）
- 沉淀空间（必须独立目录/文档，不能混在一起）

院长要管理的：
- 每个研究院的定时任务不要撞车（至少错开30分钟）
- 推送格式里标注是哪个研究院的简报
- 沉淀空间用研究院名称做隔离
