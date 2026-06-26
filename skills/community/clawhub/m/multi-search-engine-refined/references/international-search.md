# 搜索引擎深度指南（Google / DuckDuckGo / Brave / WolframAlpha）

本文档仅使用以下域名的可抓取搜索 URL：

- `https://www.google.com/...`
- `https://duckduckgo.com/...`
- `https://search.brave.com/...`
- `https://www.wolframalpha.com/...`

---

## Google 深度搜索

### 基础高级操作符

| 操作符 | 功能 | 示例 | URL |
|--------|------|------|-----|
| `""` | 精确匹配 | `"machine learning"` | `https://www.google.com/search?q=%22machine+learning%22` |
| `-` | 排除关键词 | `python -snake` | `https://www.google.com/search?q=python+-snake` |
| `OR` | 或运算 | `machine learning OR deep learning` | `https://www.google.com/search?q=machine+learning+OR+deep+learning` |
| `*` | 通配符 | `machine * algorithms` | `https://www.google.com/search?q=machine+*+algorithms` |
| `()` | 分组 | `(apple OR microsoft) phones` | `https://www.google.com/search?q=(apple+OR+microsoft)+phones` |
| `..` | 数字范围 | `laptop $500..$1000` | `https://www.google.com/search?q=laptop+%24500..%241000` |

### 站点与文件

| 操作符 | 功能 | 示例 |
|--------|------|------|
| `site:` | 站内搜索 | `site:github.com python projects` |
| `filetype:` | 文件类型 | `filetype:pdf annual report` |
| `inurl:` | URL 包含 | `inurl:login admin` |
| `intitle:` | 标题包含 | `intitle:"index of" mp3` |
| `intext:` | 正文包含 | `intext:password filetype:txt` |
| `related:` | 相关网站 | `related:example.com` |
| `info:` | 网站信息 | `info:example.com` |

### 时间筛选

| 参数 | 含义 | URL 示例 |
|------|------|----------|
| `tbs=qdr:h` | 过去 1 小时 | `https://www.google.com/search?q=news&tbs=qdr:h` |
| `tbs=qdr:d` | 过去 24 小时 | `https://www.google.com/search?q=news&tbs=qdr:d` |
| `tbs=qdr:w` | 过去 1 周 | `https://www.google.com/search?q=news&tbs=qdr:w` |
| `tbs=qdr:m` | 过去 1 月 | `https://www.google.com/search?q=news&tbs=qdr:m` |
| `tbs=qdr:y` | 过去 1 年 | `https://www.google.com/search?q=news&tbs=qdr:y` |

### 语言与地区

| 参数 | 功能 | 示例 |
|------|------|------|
| `hl=en` | 界面语言 | `https://www.google.com/search?q=test&hl=en` |
| `lr=lang_zh-CN` | 结果语言 | `https://www.google.com/search?q=test&lr=lang_zh-CN` |
| `cr=countryCN` | 国家/地区 | `https://www.google.com/search?q=test&cr=countryCN` |
| `gl=us` | 地理位置 | `https://www.google.com/search?q=test&gl=us` |

### 特殊类型（`tbm`）

| 类型 | URL |
|------|-----|
| 图片 | `https://www.google.com/search?q={keyword}&tbm=isch` |
| 新闻 | `https://www.google.com/search?q={keyword}&tbm=nws` |
| 视频 | `https://www.google.com/search?q={keyword}&tbm=vid` |
| 地图 | `https://www.google.com/search?q={keyword}&tbm=map` |
| 购物 | `https://www.google.com/search?q={keyword}&tbm=shop` |
| 图书 | `https://www.google.com/search?q={keyword}&tbm=bks` |

### Google 示例

```javascript
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python+machine+learning"})

web_fetch({"url": "https://www.google.com/search?q=machine+learning+tutorial+filetype:pdf&tbs=cdr:1,cd_min:1/1/2024"})

web_fetch({"url": "https://www.google.com/search?q=intitle:tutorial+python"})

web_fetch({"url": "https://www.google.com/search?q=AI+breakthrough&tbs=qdr:w&tbm=nws"})

web_fetch({"url": "https://www.google.com/search?q=人工智能&lr=lang_zh-CN&hl=en"})

web_fetch({"url": "https://www.google.com/search?q=laptop+%241000..%242000+best+rating"})

web_fetch({"url": "https://www.google.com/search?q=python+programming+-wikipedia"})
```

---

## DuckDuckGo

### 内置工具类查询（`duckduckgo.com`）

| 功能 | 说明 | URL 示例 |
|------|------|----------|
| 密码生成 | `password` + 长度 | `https://duckduckgo.com/?q=password+20` |
| 颜色 | `#` + 色值 | `https://duckduckgo.com/?q=+%23FF5733` |
| 短链接关键词 | `shorten` | `https://duckduckgo.com/?q=shorten+example.com` |
| 二维码 | `qr` + 文本 | `https://duckduckgo.com/?q=qr+hello+world` |
| UUID | `uuid` | `https://duckduckgo.com/?q=uuid` |
| Base64 | `base64` + 文本 | `https://duckduckgo.com/?q=base64+hello` |

### 与本技能对齐的 Bangs

在 `https://duckduckgo.com/html/?q=...` 或 `https://duckduckgo.com/?q=...` 中使用：

| Bang | 说明 |
|------|------|
| `!g` | 使用 Google 执行同一查询（浏览器中会跳转 Google；`web_fetch` 仅请求 DuckDuckGo URL） |
| `!brave` | 使用 Brave Search 执行同一查询 |

其他 Bang 由 DuckDuckGo 维护，完整列表见站内 Bang 目录（仅 `duckduckgo.com` 域名）。

### HTML 参数

| 参数 | 功能 | 示例 |
|------|------|------|
| `kp=1` / `kp=-1` | 安全搜索严格 / 关闭 | `https://duckduckgo.com/html/?q=test&kp=1` |
| `kl=cn` / `kl=us-en` | 区域 | `https://duckduckgo.com/html/?q=news&kl=cn` |
| `ia=web` / `images` / `news` / `videos` | 结果类型 | `https://duckduckgo.com/?q=test&ia=news` |

### DuckDuckGo 示例

```javascript
web_fetch({"url": "https://duckduckgo.com/html/?q=!g+machine+learning"})

web_fetch({"url": "https://duckduckgo.com/html/?q=!brave+privacy+tools"})

web_fetch({"url": "https://duckduckgo.com/?q=password+16"})

web_fetch({"url": "https://duckduckgo.com/?q=base64+hello+world"})

web_fetch({"url": "https://duckduckgo.com/?q=%23FF5733"})

web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

web_fetch({"url": "https://duckduckgo.com/html/?q=tech+news&ia=news"})
```

---

## Brave Search

### 参数

| 参数 | 功能 | 示例 |
|------|------|------|
| `tf=pw` / `pm` / `py` | 本周 / 本月 / 本年 | `https://search.brave.com/search?q=news&tf=pw` |
| `safesearch=strict` | 严格安全 | `https://search.brave.com/search?q=test&safesearch=strict` |
| `source=news` / `images` / `videos` | 新闻 / 图片 / 视频 | `https://search.brave.com/search?q=tech&source=news` |

### Goggles（过滤器语法，概念说明）

在 Brave 产品内创建规则时使用，例如提升特定 `site:` 的权重；抓取时仍使用 `search.brave.com` 的查询 URL。

### Brave 示例

```javascript
web_fetch({"url": "https://search.brave.com/search?q=technology&tf=pw&source=news"})

web_fetch({"url": "https://search.brave.com/search?q=artificial+intelligence&tf=pm"})

web_fetch({"url": "https://search.brave.com/search?q=machine+learning&source=images"})

web_fetch({"url": "https://search.brave.com/search?q=python+tutorial&source=videos"})

web_fetch({"url": "https://search.brave.com/search?q=privacy+tools"})
```

---

## WolframAlpha

### 类型与 URL 示例

| 类型 | 查询示例 | URL |
|------|----------|-----|
| 数学 | `integrate x^2 dx` | `https://www.wolframalpha.com/input?i=integrate+x%5E2+dx` |
| 单位 | `100 miles to km` | `https://www.wolframalpha.com/input?i=100+miles+to+km` |
| 货币 | `100 USD to CNY` | `https://www.wolframalpha.com/input?i=100+USD+to+CNY` |
| 股票 | `AAPL stock` | `https://www.wolframalpha.com/input?i=AAPL+stock` |
| 天气 | `weather in Beijing` | `https://www.wolframalpha.com/input?i=weather+in+Beijing` |

### WolframAlpha 示例

```javascript
web_fetch({"url": "https://www.wolframalpha.com/input?i=integrate+sin%28x%29+from+0+to+pi"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=solve+x%5E2-5x%2B6%3D0"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=Apple+stock+price"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=weather+in+Shanghai+tomorrow"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=GDP+of+China+vs+USA"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=molar+mass+of+H2SO4"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=speed+of+light"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=calories+in+banana"})

web_fetch({"url": "https://www.wolframalpha.com/input?i=events+on+July+20+1969"})
```

---

## 综合策略

### 引擎选择

| 目标 | 首选 | 说明 |
|------|------|------|
| 通用网页 | Google | 操作符与 `tbm` 最丰富 |
| 少追踪 | DuckDuckGo / Brave | 隐私向 |
| 独立索引新闻/媒体 | Brave `source=` | 与 `tf` 配合 |
| 公式 / 单位 / 数据 | WolframAlpha | 结构化答案 |

### 多引擎对比（同一关键词）

```javascript
const keyword = "climate change 2024";

const searches = [
  { engine: "Google", url: `https://www.google.com/search?q=${encodeURIComponent(keyword)}&tbs=qdr:m` },
  { engine: "Brave", url: `https://search.brave.com/search?q=${encodeURIComponent(keyword)}&tf=pm` },
  { engine: "DuckDuckGo", url: `https://duckduckgo.com/html/?q=${encodeURIComponent(keyword)}` },
  { engine: "WolframAlpha", url: `https://www.wolframalpha.com/input?i=${encodeURIComponent(keyword)}` }
];
```

### URL 编码

```javascript
function encodeKeyword(keyword) {
  return encodeURIComponent(keyword);
}
```

### 批量模板（仅四引擎）

```javascript
function generateSearchUrls(keyword) {
  const encoded = encodeURIComponent(keyword);
  return {
    google: `https://www.google.com/search?q=${encoded}`,
    duckduckgo: `https://duckduckgo.com/html/?q=${encoded}`,
    brave: `https://search.brave.com/search?q=${encoded}`,
    wolframalpha: `https://www.wolframalpha.com/input?i=${encoded}`
  };
}
```

### Google 时间筛选

```javascript
function googleTimeSearch(keyword, period) {
  const periods = {
    hour: "qdr:h",
    day: "qdr:d",
    week: "qdr:w",
    month: "qdr:m",
    year: "qdr:y"
  };
  return `https://www.google.com/search?q=${encodeURIComponent(keyword)}&tbs=${periods[period]}`;
}
```

---

## 参考资料（允许的域名）

- DuckDuckGo Bang 目录：`https://duckduckgo.com/bang`
- Brave Search 帮助：`https://search.brave.com/help/`
- WolframAlpha 示例：`https://www.wolframalpha.com/examples/`

Google 高级搜索说明请查阅 Google 官方搜索帮助（使用 `google.com` 站内文档）。
