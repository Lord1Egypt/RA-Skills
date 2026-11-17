# 搜索引擎适配器文档

本文档说明各搜索引擎的实现细节、解析规则与扩展方式，对应 V1.2 架构。

## 引擎列表

引擎清单的唯一来源是 `scripts/engines_registry.py`，运行 `python -m scripts.search --list-engines` 可查看实时属性。

| 引擎名称 | 标识 | 类型 | 区域 | 隐私等级 | strict 可用 | 说明 |
|---------|------|------|------|---------|------------|------|
| 本地 SearXNG | `searxng` | JSON API | 本机 | 高 | ✅ | 元搜索，query 不出本机，支持 bangs |
| Yandex | `yandex` | HTML 解析 | 俄罗斯 | 中 | ✅ | 国内直连速度较好 |
| Startpage | `startpage` | HTML 解析 | 荷兰 | 高 | ✅ | Google 结果代理 |
| Qwant | `qwant` | HTML 解析 | 法国 | 高 | ✅ | 受欧盟隐私法约束 |
| Brave Search | `brave` | HTML 解析 | 美国 | 高 | ✅ | 独立索引 |
| DuckDuckGo | `duckduckgo` | HTML 解析 | 美国 | 高 | ✅ | 国内直连不稳定，作兜底 |
| 百度 | `baidu` | HTML 解析 | 中国 | 低 | ❌ | 反爬较强，返回跳转链接 |
| 必应 | `bing` | HTML 解析 | 中国 | 低 | ❌ | 国内可直接访问 |
| 搜狗 | `sogou` | HTML 解析 | 中国 | 低 | ❌ | 返回跳转链接 |
| 360 搜索 | `360` | HTML 解析 | 中国 | 低 | ❌ | 返回跳转链接 |

## 架构分层

V1.2 将传输与解析彻底分离，适配器不再各自处理 HTTP 细节。

```
CLI / SearchOrchestrator
        │
        ├── engines_registry.py   引擎清单与元数据（单一真相源）
        │
        ├── privacy.py            隐私配置 → RequestContext
        │        │
        ├── http_client.py        统一出口：UA 池 / 隐私头 / 代理 / 重试
        │        │
        ├── EngineAdapter         仅负责 build_url() 与结果映射
        │        │
        ├── engine_selectors.py   多套备选选择器 + 解析诊断
        │
        ├── ranking.py            SimHash 去重 + 多因子加权排序
        │
        ├── cache.py              结果缓存与搜索历史
        │
        └── logging_util.py       运行日志
```

这样设计的原因：V1.1 时九个适配器各自硬编码请求头，导致隐私配置无法统一生效——只有三个适配器偶然带了 `DNT: 1`。收归统一出口后，隐私设置对所有引擎一致有效。

## 请求策略

### 超时与重试
- 超时由 `search.timeout` 控制，默认 15 秒
- 仅对网络类错误重试（连接失败、超时、连接重置），解析失败不重试
- 指数退避 + 随机抖动，避免多引擎同时重试形成请求尖峰
- 重试次数由 `search.retry_max` 控制，默认 2 次

### 频率控制
- 每日上限：单引擎 200 次（`search.daily_request_limit`）
- 请求间隔：1–5 秒随机延迟
- 超限自动跳过该引擎，不影响其他引擎

### 请求头
所有引擎统一经由 `http_client` 出口，不再逐引擎硬编码。

| 模式 | User-Agent | DNT | Cookie | Referer | 代理 |
|------|-----------|-----|--------|---------|------|
| normal | UA 池随机 | 按配置 | 保留 | 保留 | 按配置 |
| strict | UA 池随机 | `1` | 移除 | 移除 + `Referrer-Policy: no-referrer` | 按配置 |

UA 池内置 8 个主流浏览器标识，随机轮换以降低指纹一致性。在 `privacy.strict.user_agent` 填入固定值可覆盖此行为。

## 解析规则

每个引擎配置多套备选选择器（见 `engine_selectors.py`）。首套解析不到结果时自动尝试下一套，用于缓解搜索引擎改版。

### 百度
- 容器：`div.result, div.result-op` → `div[class*='result']` → `div#content_left > div`
- 标题：`h3 a`
- 摘要：`div.c-abstract` 等

### 必应
- 容器：`li.b_algo` → `.b_algo`
- 标题：`h2 a`
- 摘要：`p`

### DuckDuckGo
- 容器：`div.result` → `div.web-result`
- 标题：`a.result__a`
- 摘要：`a.result__snippet`

### SearXNG
- 端点：`GET /search?q=...&format=json`
- 响应：`results[].title / url / content`
- 支持 bangs 语法透传（`!w` `!gh` `!yt` 等）

### 解析诊断

解析为空时不直接判定"无结果"，而是区分四种情况：

| 诊断 | 判定依据 | 含义 |
|------|---------|------|
| `EMPTY_CONFIRMED` | 页面含"没有找到相关结果"等标记 | 确实无匹配 |
| `BLOCKED` | 页面含验证码、安全验证等标记 | 触发风控 |
| `SELECTOR_STALE` | 页面正常但所有选择器均未命中 | 引擎已改版 |
| `UNKNOWN` | 其余情况 | 需人工查看 |

这个区分很重要：把"引擎改版"误报为"无结果"会让用户以为搜索词有问题，而非插件需要更新。

### 跳转链接处理

百度、搜狗、360 返回的是形如 `baidu.com/link?url=...` 的中转地址而非真实 URL。这类链接会导致跨引擎去重失效（同一结果在不同引擎下 URL 不同）且域名质量评分失准，因此排序时统一降权。

## SimHash 去重

V1.2 采用标准 SimHash 实现（V1.1 的 MD5 异或合并并非真正的 SimHash，近似文本无法识别）。

1. 中文用 jieba 分词，缺失时降级为 2-gram 字符切分
2. 统计词频作为特征权重
3. 每个特征取 MD5 哈希，按位加权投票：该位为 1 则加权重，为 0 则减权重
4. 投票结果 > 0 的位置为 1，得到 64 位指纹
5. 汉明距离 ≤ 3 视为重复

## 多因子加权排序

综合得分由五个因子加权求和，权重可在 `config.yaml` 的 `ranking` 段调整：

| 因子 | 默认权重 | 说明 |
|------|---------|------|
| 共识度 | 6.0 | 被越多引擎收录越可信 |
| 位次 | 3.0 | 引擎内原始排名，对数衰减 |
| 相关度 | 4.0 | 查询词在标题摘要中的覆盖率 |
| 权威度 | 2.0 | 引擎自身权威度，取自注册表 |
| 域名质量 | 1.5 | 优质站点加分，低质站点与跳转链接降权 |

## 扩展指南

新增引擎只需三步，无需改动传输层：

1. 在 `engines_registry.py` 的 `ENGINE_REGISTRY` 中登记元数据
2. 在 `engine_selectors.py` 的 `SELECTORS` 中配置选择器
3. 在 `search.py` 中实现适配器，只需覆盖 `build_url()`

```python
class NewEngineAdapter(EngineAdapter):
    """新引擎适配器：仅需构造 URL，解析与传输由框架承担"""

    def __init__(self):
        super().__init__("newengine")

    def build_url(self, query: str, num: int) -> str:
        return f"https://example.com/search?q={quote(query)}&n={num}"
```

若引擎返回 JSON 而非 HTML，参考 `SearXNGAdapter` 覆盖 `search()` 方法。

完成后运行 `python -m scripts.search --selftest` 验证连通性与解析状态。

---

有更好建议：njskills@agent.qq.com
