
---
name: practical-news-monitor
description: 实用新闻监控框架 - 专注于可工作的数据源和易扩展性，支持地缘政治、石油、黄金等关键词监控
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python3","requests"]}}}
---

# 实用新闻监控框架

专注于可工作的数据源和易扩展性，支持地缘政治、石油、黄金等关键词监控。

## 核心特性

- 📡 **多数据源支持**: JSON API 和 HTML 解析两种数据源类型
- 🎯 **关键词监控**: 可自定义监控关键词和分类
- 💾 **数据持久化**: 自动保存监控数据到 JSON 文件
- 📊 **摘要报告**: 自动生成新闻监控摘要报告
- 🔧 **易扩展**: 基类设计，轻松添加新数据源

## 快速开始

### 安装依赖

```bash
pip3 install requests
```

### 运行监控

```bash
cd /path/to/skill
python3 practical_news_monitor.py monitor
```

### 测试数据源

```bash
python3 practical_news_monitor.py test
```

## 配置说明

### 监控关键词

在脚本中编辑 `MONITOR_KEYWORDS` 字典：

```python
MONITOR_KEYWORDS = {
    'geopolitical': ['中东', '伊朗', '以色列', '巴勒斯坦'],
    'oil': ['石油', '原油', '油价', 'OPEC'],
    'gold': ['黄金', '贵金属', '避险', '金价'],
    'sanctions': ['制裁', '禁令', '限制', '封锁'],
    'shipping': ['航运', '海运', '物流', '苏伊士'],
    'conflict': ['冲突', '战争', '打击', '攻击']
}
```

### 添加数据源

在 `_init_sources()` 方法中添加新的数据源配置：

```python
source_configs = [
    {
        'type': 'json_api',
        'name': '我的JSON API',
        'config': {
            'enabled': True,
            'url': 'https://api.example.com/news',
            'data_path': 'data.items',
            'title_field': 'title',
            'url_field': 'link',
            'time_field': 'published_at',
            'timeout': 15,
            'limit': 20
        }
    },
    {
        'type': 'html_parse',
        'name': '我的HTML网站',
        'config': {
            'enabled': True,
            'url': 'https://example.com/news',
            'parse_rules': {
                'container_selector': r'&lt;div class="news-item"&gt;(.*?)&lt;/div&gt;',
                'title_selector': r'&lt;a[^&gt;]*&gt;([^&lt;]+)&lt;/a&gt;',
                'link_selector': r'href="([^"]+)"'
            },
            'timeout': 15,
            'limit': 20
        }
    }
]
```

## 数据目录

默认数据保存位置：

```
/Users/zenozhou/shared_memory/practical_news/
```

可以在脚本中修改 `DATA_DIR` 变量来更改位置。

## 输出示例

监控运行后会生成：

1. **JSON 数据文件**: 包含所有新闻和相关性信息
2. **摘要报告**: Markdown 格式的新闻摘要

```
============================================================
📊 实用新闻监控
============================================================
监控时间: 2026-03-23 08:30:00

📡 正在获取 新浪财经（示例）...
   ✓ 获取到 20 条新闻
📡 正在获取 东方财富（示例）...
   ✓ 获取到 15 条新闻

✅ 共获取 35 条新闻
📈 相关新闻: 8 条

📊 来源统计:
  新浪财经（示例）: 5/20 相关
  东方财富（示例）: 3/15 相关

💾 数据已保存: /Users/zenozhou/shared_memory/practical_news/monitor_2026-03-23_083000.json
```

## 扩展开发

### 创建新数据源类型

继承 `NewsDataSource` 基类并实现 `fetch()` 方法：

```python
class MyCustomSource(NewsDataSource):
    """我的自定义数据源"""

    def fetch(self) -&gt; List[Dict[str, Any]]:
        """获取新闻数据"""
        # 实现你的数据获取逻辑
        pass
```

### 自定义相关性检查

重写 `check_relevance()` 方法：

```python
def check_relevance(self, title: str, keywords: Dict[str, List[str]]) -&gt; Dict[str, Any]:
    """自定义相关性检查逻辑"""
    # 实现你的相关性检查
    pass
```

## 常见问题

### Q: 如何添加新的关键词分类？
A: 在 `MONITOR_KEYWORDS` 字典中添加新的键值对即可。

### Q: 数据源返回 HTTP 错误怎么办？
A: 检查 URL 是否正确，是否需要 headers 或 cookies，尝试在浏览器中访问确认。

### Q: 如何调整监控频率？
A: 使用 cron 或其他调度工具定期运行脚本。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

*由 Zbot 自动生成* 💥
