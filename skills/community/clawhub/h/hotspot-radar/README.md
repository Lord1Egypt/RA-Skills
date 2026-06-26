# 🌐 热点雷达 - 全网热榜追踪器

> 聚合微博/知乎/抖音/B站/小红书热搜榜单，支持趋势分析和话题监控

## 功能特性

- ✅ **实时采集** - 并行获取五大平台热榜数据
- ✅ **趋势追踪** - 对比昨日发现新上榜/落榜话题
- ✅ **跨平台热点** - 发现同时在多个平台发酵的话题
- ✅ **话题监控** - 关键词订阅，有动态时及时提醒
- ✅ **每日报告** - 自动生成Markdown格式热点日报
- ✅ **HTML可视化报告** - 交互式图表报告，含热度对比图/趋势图

## 快速开始

```bash
# 初始化目录
node scripts/index.js init

# 一键采集+生成报告
node scripts/index.js quick

# 单独采集数据
node scripts/index.js fetch

# 单独生成Markdown报告
node scripts/index.js report

# 生成HTML可视化报告（含图表）
node scripts/index.js html
```

## 目录结构

```
hotspot-radar/
├── SKILL.md              # Skill定义文件
├── README.md             # 使用文档
├── package.json          # NPM配置
├── data/                 # 数据存储
│   ├── history/         # 历史热榜
│   │   ├── weibo/
│   │   ├── zhihu/
│   │   ├── bilibili/
│   │   ├── douyin/
│   │   └── xiaohongshu/
│   ├── trends/          # 每日趋势快照
│   └── reports/         # 生成的报告
├── config/              # 配置文件
│   ├── monitor.json    # 监控关键词
│   └── push.json       # 推送配置
├── scripts/             # 脚本文件
│   ├── index.js        # 主入口
│   ├── collector.js    # 数据采集
│   ├── reporter.js     # Markdown报告生成
│   ├── htmlReporter.js  # HTML可视化报告生成
│   └── monitor.js      # 监控管理
├── references/          # 参考文档
└── assets/             # 资源文件
```

## 话题监控

```bash
# 添加监控关键词
node scripts/monitor.js add "人工智能"

# 移除监控关键词
node scripts/monitor.js remove "人工智能"

# 列出所有关键词
node scripts/monitor.js list

# 查看监控状态
node scripts/monitor.js status
```

## 定时任务配置

使用WorkBuddy的automation功能设置每日定时推送：

1. 打开WorkBuddy设置
2. 创建新的automation
3. 设置触发时间（如每天9:00）
4. 设置任务为 `node scripts/index.js quick`

## 环境变量（可选）

```bash
# 微博Cookie（提高API限制）
export WEIBO_COOKIE="your_weibo_cookie"

# 小红书Cookie（提高API限制）
export XHS_COOKIE="your_xhs_cookie"
```

## 数据来源

| 平台 | 数据接口 | 说明 |
|------|----------|------|
| 微博 | 热搜API | 实时更新 |
| 知乎 | 热榜API | 实时更新 |
| 抖音 | 热榜API | 需device_id |
| B站 | 排行榜API | 实时更新 |
| 小红书 | 搜索热词API | 实时更新 |

## 开源协议

MIT License

---

*由「热点雷达」Skill v1.0.0 提供*
