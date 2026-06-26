# AI行业早报 Skill

定时获取AI行业最新资讯，整理成每日早报发送给用户。

## 文件说明

```
ai-daily-news/
├── skill.yaml       # Skill 元数据配置
├── prompt.md        # 早报生成提示词
└── README.md        # 使用说明
```

## 使用方式

1. **安装 Skill**：将本文件夹复制到 `~/.openclaw/workspace/skills/` 目录

2. **配置定时任务**：
   ```json
   {
     "name": "AI行业早报",
     "schedule": {
       "kind": "cron",
       "expr": "30 8 * * *",
       "tz": "Asia/Shanghai"
     },
     "payload": {
       "message": "请执行AI行业早报任务"
     }
   }
   ```

3. **手动触发**：直接调用此 Skill 即可生成当日早报

## 功能特点

- 搜索过去24小时AI行业重大新闻
- 整理为核心新闻、重要进展、趋势分析
- 包含当日黄历（宜忌）
- 从毛选中选择经典语录结合推荐
- 定时自动发送（每天早上8:30）

## 依赖

- 搜索工具（用于获取AI行业新闻）
- 日历查询工具（获取黄历）
- 消息发送渠道（企业微信/QQ等）