# Product Launch Radar 使用示例

## 示例 1: 日常使用

**用户输入**:
```
今天有什么值得关注的产品发布吗？
```

**Agent 响应**:
```
📊 今日产品发布简报 (2026-03-20)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 高优先级 (3条)

1. [AI] OpenAI 发布 GPT-5 技术预览
   来源: TechCrunch | 评分: 9.2/10
   摘要: 多模态能力提升 3 倍，支持实时视频理解，推理成本降低 40%
   链接: https://techcrunch.com/...

2. [DevOps] Docker 推出 AI 容器优化方案
   来源: Hacker News | 评分: 8.7/10
   摘要: 自动化镜像构建，减少 60% 构建时间，支持自然语言配置
   链接: https://docs.docker.com/...

3. [开源] LangChain 3.0 正式发布
   来源: GitHub Trending | 评分: 8.5/10
   摘要: 新增 Agent 工作流编排器，支持多 Agent 协作，性能提升 50%
   链接: https://github.com/langchain-ai/...

🟡 中优先级 (5条)

4. [工具] Notion AI 写作助手更新
   来源: Product Hunt | 评分: 7.8/10
   
5. [数据库] PlanetScale 推出分支功能
   来源: V2EX | 评分: 7.2/10
   
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 今日共聚合 47 条动态，筛选出 8 条高价值内容
⏰ 下次更新: 明天 09:00
```

---

## 示例 2: 竞品追踪

**用户输入**:
```
帮我追踪 OpenAI 和 Anthropic 这两周的动态
```

**Agent 响应**:
```
🎯 竞品动态追踪报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## OpenAI (过去 14 天)

### 产品发布
- 3/18: GPT-5 技术预览发布
- 3/15: ChatGPT 新增语音对话功能
- 3/12: API 定价调整（降价 20%）

### 技术博客
- 3/17: "Scaling Laws for Neural Language Models" 更新
- 3/10: 安全性研究报告

### 社区动态
- GitHub Stars 增长: +15,000
- Hacker News 热帖: 3 篇

## Anthropic (过去 14 天)

### 产品发布
- 3/19: Claude 3.5 Sonnet 更新
- 3/14: 企业版安全合规认证

### 技术博客
- 3/16: Constitutional AI 2.0 论文发布

### 社区动态
- GitHub Stars 增长: +8,500
- Hacker News 热帖: 2 篇

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 对比分析
- OpenAI 发布频率更高，市场动作更激进
- Anthropic 专注安全合规，企业客户导向明显
- 两者 API 定价趋势均向下
```

---

## 示例 3: 行业定制

**用户输入**:
```
我关注电商和支付领域，帮我配置过滤器
```

**Agent 响应**:
```
✅ 已更新 Product Launch Radar 配置

新增关注关键词:
- 电商、电商系统、商城
- 支付、支付网关、结算
- 供应链、物流、仓储
- 跨境电商、海外仓

已调整信息源:
- 新增: 电商派、支付圈
- GitHub Topics: e-commerce, payment, checkout

是否需要添加特定公司追踪？
例如: Shopify, Stripe, 支付宝, 微信支付
```

---

## 示例 4: 定时推送

**用户输入**:
```
每天早上 9 点推送到飞书产品群
```

**Agent 响应**:
```
✅ 已配置定时任务

执行时间: 每天 09:00 (北京时间)
推送渠道: 飞书
目标群组: 产品团队群

任务 ID: cron-product-radar-001

管理命令:
- 查看状态: /cron status cron-product-radar-001
- 暂停推送: /cron pause cron-product-radar-001
- 恢复推送: /cron resume cron-product-radar-001
- 修改时间: /cron update cron-product-radar-001 --time "08:30"
```

---

## 示例 5: 周报汇总

**用户输入**:
```
生成上周产品发布周报
```

**Agent 响应**:
```
📊 产品发布周报 (2026.03.14 - 2026.03.20)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🏆 本周 Top 10

| 排名 | 产品 | 类别 | 来源 | 评分 |
|-----|------|-----|------|-----|
| 1 | GPT-5 技术预览 | AI | TechCrunch | 9.2 |
| 2 | Docker AI 优化 | DevOps | HN | 8.7 |
| 3 | LangChain 3.0 | 开源 | GitHub | 8.5 |
| 4 | Notion AI 更新 | 工具 | PH | 7.8 |
| 5 | PlanetScale 分支 | 数据库 | V2EX | 7.2 |
| ... | ... | ... | ... | ... |

## 📈 趋势分析

### 热门领域
1. AI/LLM (42% of items)
2. DevOps 工具 (18%)
3. 数据库技术 (12%)
4. 低代码平台 (10%)

### 关键事件
- OpenAI 发布 GPT-5，引发行业热议
- 多家数据库厂商推出 AI 功能
- 低代码平台竞争加剧

## 💡 建议

基于本周动态，建议关注:
1. GPT-5 API 定价策略，可能影响产品成本
2. LangChain 3.0 的 Agent 编排能力
3. 数据库 AI 功能集成趋势

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 完整报告已保存至: reports/weekly-2026-03-20.md
```

---

## 示例 6: API 集成

**请求**:
```bash
curl -X POST https://your-openclaw-instance/api/skills/product-launch-radar/trigger \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["github_trending", "hacker_news"],
    "filter": {
      "keywords": ["AI", "Agent"],
      "min_score": 7.0
    },
    "output": {
      "format": "json",
      "channels": ["feishu"]
    }
  }'
```

**响应**:
```json
{
  "status": "success",
  "job_id": "plr-20260320-001",
  "summary": {
    "total_items": 47,
    "filtered_items": 8,
    "high_priority": 3,
    "medium_priority": 5
  },
  "notification": {
    "sent": true,
    "channels": ["feishu"],
    "timestamp": "2026-03-20T09:05:00Z"
  }
}
```