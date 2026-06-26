---
name: hot-search
description: Hot Search - OpenClaw 稳定搜索技能，专为金融数据和市场行情设计。支持多引擎聚合搜索，无需 API 密钥，免费无限次使用。
---

# Hot Search 搜索技能

_版本：1.0.0 | 作者：糖糖 (Tangtang) | 邮箱：fishsomes@gmail.com_

---

## 🔍 技能概述

Hot Search 是专为 OpenClaw 框架设计的稳定搜索技能，特别优化了金融数据和市场行情的搜索能力。

### 核心优势

- **稳定可靠** - 多引擎备份，单引擎失败不影响全局
- **免费使用** - 无需 API 密钥，无使用次数限制
- **快速响应** - 超时控制，避免长时间阻塞
- **金融优化** - 针对原油、股票等金融数据优化

---

## 📦 安装方法

### 方法 1：从 Clawhub 安装

```bash
openclaw skill install hot-search
```

### 方法 2：从 GitHub 安装

```bash
git clone https://github.com/fishsomes/hot-search.git
cd hot-search
pip3 install -r requirements.txt
```

### 方法 3：手动安装

将技能文件复制到 OpenClaw 技能目录：

```bash
cp -r hot-search ~/.openclaw/workspace/skills/
```

---

## 🚀 使用指南

### 命令行使用

```bash
# 基本搜索
python3 search_skill.py "关键词"

# 指定引擎
python3 search_skill.py "关键词" bing_global

# 多引擎搜索
python3 search_skill.py "关键词" all
```

### Python 调用

```python
from search_skill import SearchEngine

search = SearchEngine()

# 单引擎搜索
results = search.search('原油价格', 'bing_global')

# 多引擎搜索
results = search.search_all('Oman crude oil price')

# 去重结果
unique_results = search.deduplicate(results)
```

### OpenClaw 集成

在 OpenClaw 中直接使用：

```
用 hot-search 搜索【原油价格】
用 hot-search 的必应国际搜索【WTI crude oil】
```

---

## 🔧 高级配置

### 超时设置

```python
search = SearchEngine(timeout=5)  # 5 秒超时
```

### 延迟控制

```python
search = SearchEngine(delay_range=(1.0, 2.0))  # 1-2 秒延迟
```

### 自定义引擎

```python
engines = {
    "custom": {
        "name": "自定义引擎",
        "url": "https://example.com/search",
        "params": {"q": "{keyword}"},
        "selector": ".result"
    }
}
```

---

## 📊 搜索结果格式

```json
{
  "bing_cn": [
    {
      "title": "结果标题",
      "link": "https://...",
      "snippet": "摘要内容"
    }
  ],
  "bing_global": [...],
  "yandex": [...],
  "swisscows": [...]
}
```

---

## 💡 最佳实践

### 金融数据搜索

```bash
# 使用必应国际搜索英文数据
python3 search_skill.py "DME Oman crude oil settlement price" bing_global

# 使用必应国内搜索中文数据
python3 search_skill.py "中国原油进口量 2026" bing_cn
```

### 新闻搜索

```bash
# 搜索最新新闻
python3 search_skill.py "今天最新新闻 热点" bing_cn

# 搜索国际新闻
python3 search_skill.py "world news today breaking" bing_global
```

### 组合使用

```python
# 1. 先搜索关键词
results = search.search_all('原油价格')

# 2. 筛选优质链接
good_links = [r['link'] for r in results['bing_global'][:3]]

# 3. 深度抓取内容
for link in good_links:
    content = web_fetch(url=link)
    print(content)
```

---

## ⚠️ 注意事项

1. **合法合规** - 仅用于合法数据抓取
2. **频率控制** - 避免高频请求被封禁
3. **超时设置** - 建议 2-5 秒超时
4. **错误处理** - 捕获异常，记录失败

---

## 🔗 相关资源

- [OpenClaw 文档](https://docs.openclaw.ai)
- [Clawhub 技能市场](https://clawhub.ai)
- [GitHub 仓库](https://github.com/fishsomes/hot-search)

---

_最后更新：2026-03-28_
_作者：FishSome_
_邮箱：fishsomes@gmail.com_
