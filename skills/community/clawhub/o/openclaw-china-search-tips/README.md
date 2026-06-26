# OpenClaw 国内联网搜索整合 🇨🇳

> 在中国大陆不用翻墙也能稳定联网搜索，多个渠道自动 fallback

## 问题

国内使用 OpenClaw 常常碰到：
- GitHub 登录卡顿
- 命令行没有代理没法上网
- 单个搜索渠道容易失败

这个技能整合了**四个免费搜索渠道**，自动 fallback，一个失败自动试下一个，不用翻墙，就能稳定搜索。

## 整合渠道

| 渠道 | 免费额度 | 获取方式 | 特点 |
|------|----------|----------|------|
| volcengine-search | 500次/月 | 火山引擎方舟套餐 | 官方支持，中文准，带AI总结 |
| tavily-search | 1000次/月 | [tavily.com](https://app.tavily.com/home) → GitHub 登录 | AI 原生搜索，结构化结果 |
| search-api | 1000次/月 | [searchapi.io](https://www.searchapi.io/) → GitHub 登录 | Google 搜索结果，稳定 |
| multi-search-engine | 不限 | 免 API Key | 直接爬搜索引擎，兜底 |

## 使用技巧

### GitHub 登录技巧（不用翻墙）
```
1. 先打开 GitHub 中文社区 → https://www.githubs.cn/
2. 在中文社区登录你的 GitHub 账号
3. 登录完直接打开 GitHub 官网，登录状态已经带过去了
4. 再去 tavily/searchapi 官网选择 GitHub 登录，一次性成功
```

### 自动 Fallback
代码已经封装好，调用 `search(query)` 就会自动尝试各个渠道，返回第一个成功的结果，不用你手动切换。

## 配置环境变量

```bash
export VOLC_SEARCH_API_KEY="your-api-key"   # 火山引擎搜索（可选）
export TAVILY_API_KEY="tvly-xxx"             # Tavily 搜索（可选）
export SEARCHAPI_API_KEY="your-api-key"    # SearchAPI 搜索（可选）
```

至少配置一个就能用，配置多个自动 fallback 更稳定。

## Python 使用

```python
from china_search import search

result = search("你的搜索问题")
if result["success"]:
    print(f"使用渠道: {result['source']}")
    for r in result["results"]:
        print(f"- {r.title}: {r.url}")
```

## CLI 使用

```bash
python china_search.py "2026年4月15日A股上证指数"
```

## 核心经验

> **碰到问题不要一根筋走到黑**  
> 国内网络环境特殊，多准备几个渠道，一个不行就试下一个，总能搞定。

## 许可证

MIT

## 作者

整理：海绵宝宝 & 派大星 (OpenClaw 比奇堡团队)

**如果你觉得有用，欢迎给个 Star ⭐**

