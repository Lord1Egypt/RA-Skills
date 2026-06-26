# 🦅 新闻斥候 (News Scout)

自动化收集、筛选并分析全球/国内的 AI 新闻和美股市场趋势。

## 📖 功能特点

- ✅ **双领域覆盖**：AI 科技 + 投资市场
- ✅ **全球视野**：区分全球 AI 前沿和中国国内动态
- ✅ **智能去重**：自动识别并合并同一事件的多方报道
- ✅ **热度评分**：1-5 星评估新闻重要性
- ✅ **影响分析**：每条新闻附带专业影响分析
- ✅ **定时更新**：支持定时任务自动获取

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install feedparser duckduckgo-search requests
```

### 2. 运行脚本

```bash
# 获取全部新闻（AI + 投资）
python3 scripts/scout.py --category ai,investing

# 仅获取 AI 新闻
python3 scripts/scout.py --category ai

# 仅获取投资新闻
python3 scripts/scout.py --category investing

# 调试模式（输出详细信息）
python3 scripts/scout.py --category ai,investing --debug
```

### 3. 查看输出

脚本输出 JSON 格式的新闻列表，示例：

```json
{
  "ai": [
    {
      "title": "Anthropic 发布 Claude 新功能",
      "url": "https://...",
      "source": "Anthropic News",
      "priority": "P0",
      "snippet": "...",
      "date": "2026-03-12T10:00:00+00:00",
      "category": "ai"
    }
  ],
  "investing": [...]
}
```

## 📋 配置说明

### 新闻源配置

编辑 `resources/news_sources.json` 自定义新闻源：

```json
{
  "rss_feeds": {
    "ai": [
      {
        "name": "媒体名称",
        "url": "https://.../rss.xml",
        "priority": "P0",
        "region": "global",
        "language": "en"
      }
    ]
  },
  "search_queries": {
    "ai": ["搜索关键词 1", "搜索关键词 2"]
  }
}
```

### 优先级说明

| 优先级 | 说明 | 示例 |
|--------|------|------|
| P0 | 最高 | 官方博客、权威媒体 |
| P1 | 高 | 主流科技媒体 |
| P2 | 中 | 其他来源 |

## 🔧 故障排查

### 问题：缺少依赖库

```
错误：缺少必要的依赖库。请运行：pip install feedparser duckduckgo-search
```

**解决方案：**
```bash
pip3 install feedparser duckduckgo-search requests
```

### 问题：配置文件不存在

```
错误：配置文件不存在：.../news_sources.json
```

**解决方案：**
- 确保 `news_sources.json` 位于 `resources/` 目录下
- 检查文件路径是否正确

### 问题：RSS 源无法访问

**可能原因：**
- 网络连接问题
- RSS 源已失效
- 需要科学上网

**解决方案：**
- 检查网络连接
- 在配置文件中替换为可用的 RSS 源
- 使用搜索模式作为备用

### 问题：搜索结果为空

**可能原因：**
- DuckDuckGo 触发反爬限制
- 搜索词过于冷门

**解决方案：**
- 减少搜索词数量
- 优化搜索词（更具体、更热门）
- 增加 RSS 源数量

## 📊 输出格式

脚本输出的 JSON 数据结构：

```typescript
{
  "ai": Array<{
    title: string;       // 新闻标题
    url: string;         // 原文链接
    source: string;      // 来源媒体
    priority: "P0"|"P1"|"P2";  // 优先级
    snippet: string;     // 摘要
    date: string;        // 发布日期
    category: string;    // 分类
    multi_source?: boolean;  // 是否多家媒体报道
    other_sources?: string[]; // 其他来源列表
  }>,
  "investing": Array<...>
}
```

## 🔄 集成到 OpenClaw

在 OpenClaw 中使用此技能：

1. 确保技能位于 `~/.openclaw/workspace/skills/news-scout/`
2. 用户发送"新闻简报"、"今日新闻"等触发词
3. 技能自动执行并格式化输出

### 备用方案

如果脚本无法运行，OpenClaw 会使用以下工具替代：
- `web_search` - 搜索最新新闻
- `web_fetch` - 抓取新闻网站内容

## 📝 更新日志

### v2.0 (2026-03-12)
- ✨ 新增中文注释和文档
- ✨ 增加去重功能
- ✨ 优化错误处理
- ✨ 扩展新闻源（20+ AI 源，20+ 投资源）
- ✨ 增加调试模式
- ✨ 添加超时控制
- ✨ 优化并发性能

### v1.0 (初始版本)
- 基础 RSS 抓取功能
- DuckDuckGo 搜索集成
- JSON 输出格式

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 添加新闻源

1. Fork 仓库
2. 编辑 `resources/news_sources.json`
3. 测试新源是否正常工作
4. 提交 PR

### 优化搜索词

- 分析哪些搜索词产生高质量结果
- 更新过时的搜索词
- 增加新的热点关键词

## 📄 许可证

MIT License

---

**维护者**: OpenClaw Community  
**最后更新**: 2026-03-12
