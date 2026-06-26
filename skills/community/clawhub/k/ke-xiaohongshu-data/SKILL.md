---
name: ke-xiaohongshu-data
description: 科特船长 - 小红书数据抓取，笔记数据/博主分析/热搜词监控
version: 1.0.0
metadata: {"openclaw": {"emoji": "📕", "requires": {"env": ["XIAOHONGSHU_COOKIE"]}, "primaryEnv": "XIAOHONGSHU_COOKIE"}}
---

# 小红书数据抓取 - 科特船长版

## ⚠️ 重要说明

**本技能仅抓取小红书公开数据，遵守平台规则：**
- 不抓取用户隐私信息
- 不高频请求（间隔 3-5 秒）
- 仅用于个人学习/研究/商业分析
- 不得用于违法用途

## 功能说明

帮助用户抓取小红书公开数据，包括：
- 笔记数据（点赞、收藏、评论数）
- 博主信息（粉丝数、笔记数）
- 热搜词监控
- 竞品笔记分析

## 使用方法

### 前置准备

1. **获取 Cookie**（可选，用于提高抓取成功率）
   - 打开小红书网页版 (xiaohongshu.com)
   - 登录账号
   - F12 打开开发者工具
   - 复制 Cookie 值

2. **设置环境变量**
```bash
export XIAOHONGSHU_COOKIE="your_cookie_here"
```

### 基础用法

```bash
# 抓取博主笔记数据
clawhub run ke-xiaohongshu-data --action profile --url "https://www.xiaohongshu.com/user/profile/xxx"

# 抓取单篇笔记数据
clawhub run ke-xiaohongshu-data --action note --url "https://www.xiaohongshu.com/explore/xxx"

# 搜索关键词笔记
clawhub run ke-xiaohongshu-data --action search --keyword "护肤" --limit 50

# 监控热搜词
clawhub run ke-xiaohongshu-data --action trending --category "美妆"
```

### 参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `--action` | 是 | 操作类型：profile/note/search/trending | - |
| `--url` | 条件必填 | 博主主页或笔记 URL | - |
| `--keyword` | 条件必填 | 搜索关键词 | - |
| `--limit` | 否 | 抓取数量上限 | 20 |
| `--output` | 否 | 输出文件路径 | ./xiaohongshu-data.xlsx |
| `--cookie` | 否 | Cookie 值（或用环境变量） | - |
| `--delay` | 否 | 请求间隔（秒） | 3 |

## 输出数据格式

### 博主数据 (profile)

| 字段 | 说明 |
|------|------|
| 博主 ID | 小红书用户 ID |
| 昵称 | 博主昵称 |
| 粉丝数 | 粉丝数量 |
| 关注数 | 关注数量 |
| 获赞数 | 总获赞数 |
| 笔记数 | 笔记总数 |
| 简介 | 个人简介 |

### 笔记数据 (note)

| 字段 | 说明 |
|------|------|
| 笔记 ID | 笔记唯一 ID |
| 标题 | 笔记标题 |
| 内容 | 笔记正文 |
| 点赞数 | 点赞数量 |
| 收藏数 | 收藏数量 |
| 评论数 | 评论数量 |
| 发布时间 | 发布时间 |

## 商业化应用

### 品牌方
- 寻找合适的 KOL/KOC 合作
- 监控竞品投放效果
- 分析热门内容趋势

### MCN 机构
- 评估达人价值
- 监控达人数据
- 内容策略分析

### 个人博主
- 学习爆款笔记
- 分析竞品内容
- 优化自身运营

## 定价建议

| 版本 | 功能 | 价格 |
|------|------|------|
| 免费版 | 每日 10 次查询，基础数据 | 免费 |
| 专业版 | 无限查询，导出数据，监控预警 | ¥29.9/月 |
| 企业版 | API 接入，定制报表，多账号 | ¥299/月 |

## 定制服务

需要定制数据抓取服务？
- 电商竞品监控：¥500-2000/项目
- 月度数据报告：¥1000/月
- 私有化部署：¥5000+

联系：私信获取报价

## 注意事项

1. **合法合规**: 仅抓取公开数据，不侵犯隐私
2. **频率控制**: 避免高频请求，防止被封
3. **Cookie 安全**: 不要泄露 Cookie，定期更换
4. **数据使用**: 仅用于分析学习，不得商用转售

## 常见问题

**Q: 抓取失败怎么办？**
A: 检查 Cookie 是否过期，尝试更新 Cookie；或降低抓取频率。

**Q: 会被封号吗？**
A: 正常使用不会，但请遵守平台规则，不要高频抓取。

**Q: 能抓取评论详情吗？**
A: 目前仅抓取评论数量，评论详情需要额外开发。

---

**作者**: 科特船长
**更多技能**: https://clawhub.ai/@xiaoheizp
