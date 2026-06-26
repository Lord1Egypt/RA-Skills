# 热点聚合监控技能

> 聚合抖音/微博/知乎/百度热搜，每日推送热点报告，支持关键词订阅

## ✨ 功能特性

- **多平台聚合** - 微博、百度、知乎、抖音四大平台热搜
- **每日报告** - 自动生成结构化热点分析报告
- **关键词订阅** - 订阅感兴趣的关键词，自动检测匹配
- **趋势分析** - 分析热点分布和变化趋势

## 🚀 快速开始

### 1. 获取热点数据

```bash
# 获取所有平台热搜
./scripts/fetch-hotspots.sh all

# 获取单个平台
./scripts/fetch-hotspots.sh weibo
./scripts/fetch-hotspots.sh baidu
./scripts/fetch-hotspots.sh zhihu
./scripts/fetch-hotspots.sh douyin
```

### 2. 生成热点报告

```bash
./scripts/generate-report.sh
```

报告保存在: `/root/clawd/memory/hotspots/YYYY-MM-DD.md`

### 3. 订阅关键词

```bash
# 添加订阅
./scripts/subscribe.sh add "AI"
./scripts/subscribe.sh add "科技"

# 查看订阅列表
./scripts/subscribe.sh list

# 删除订阅
./scripts/subscribe.sh remove "AI"
```

### 4. 检测关键词

```bash
./scripts/check-keywords.sh
```

## 📊 报告示例

```markdown
# 🔥 今日热点报告 - 2026-03-21

## 📱 微博热搜 TOP10
1. 两会热点话题 🔥 1234567热度
2. AI技术新突破 🔥 987654热度
...

## 🔍 百度热搜 TOP10
1. 最新科技动态 🔥 搜索量: 890123
...

## 💡 知乎热榜 TOP10
1. 如何评价最新的AI技术发展？ 💬 234回答
...

## 🎵 抖音热搜 TOP10
1. 热门舞蹈挑战 🎬 12345678播放
...

## 📊 热点分析
- 科技类热点: 35%
- 娱乐类热点: 28%
...

## 🎯 订阅关键词匹配
关键词 [AI] 匹配到:
- AI技术新突破 (微博)
- 如何评价最新的AI技术发展？ (知乎)
```

## ⚙️ 配置

配置文件: `config.json`

```json
{
  "platforms": ["weibo", "baidu", "zhihu", "douyin"],
  "reportTime": "08:00",
  "keywords": ["AI", "科技"],
  "notifyChannel": ""
}
```

## 🔄 定时任务

可以配合 cron 实现自动化：

```bash
# 每天早上8点生成报告
0 8 * * * /root/clawd/skills/hotspot-aggregator/scripts/generate-report.sh
```

## 📝 数据源

当前使用模拟数据，生产环境需要接入真实API：

- 微博热搜 API
- 百度热搜 API
- 知乎热榜 API
- 抖音热搜 API

## ⚠️ 注意事项

1. API 可能有访问频率限制
2. 建议每小时最多请求一次
3. 部分API可能需要处理反爬机制
4. 生产环境建议使用代理池

## 📜 版本历史

- v1.0.0 (2026-03-21) - 初始版本
  - 四大平台数据获取
  - 热点报告生成
  - 关键词订阅功能
  - 关键词检测功能

## 📄 License

MIT

---

**作者**: 赚钱小能手  
**技能市场**: ClawHub  
**定价建议**: ¥99-299/月
