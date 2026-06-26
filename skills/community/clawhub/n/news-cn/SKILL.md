---
name: "News Brief - 新闻简报"
description: 中文新闻门户列表抓取，可输出 Markdown 简报或 JSON/RSS，无需新闻类 API Key。当用户说：给我一份今日要闻链接简报、抓一下门户新闻标题，或类似中文新闻聚合时，使用本技能。
metadata: { "openclaw": { "emoji": "📰", "requires": { "bins": ["python3"] } } }
---

## 中文新闻网页聚合（news-cn）

以 **网站列表页 URL** 为主，用本地脚本下载 HTML，通过 **BeautifulSoup** 抽取站内文章链接与标题（**网易 `*.163.com`、新浪 `*.sina.com.cn` 等同系子域**已做宽松匹配），合并为简报；可选 `mode=rss`（Solidot、BBC 等 feed）。**网易与新浪请走网页模式**。

本技能由**极速数据**整理维护：[`https://www.jisuapi.com`](https://www.jisuapi.com)  
信息反馈：`liupandeng@jisuapi.com`

### 与工作流

1. **脚本 `fetch.py`**：`list` 查看预设键名；`fetch` 拉取条目；**`digest` 一条命令输出按来源分组的 Markdown 简报**（仅标题+链接，本地完成）。
2. **Agent**：对强 JS 站点可配合 **web_fetch**；若需要叙事型「成稿」，由 Agent 在拿到 `digest`/`fetch` 输出后再加工即可。

### 依赖

```bash
pip install beautifulsoup4
```

- **Python 3** 必选；**网页模式必须**安装 `beautifulsoup4`。
- 可选 **`NEWS_CN_UA`**：自定义 `User-Agent`（部分站反爬较严）。
- 可选 **`NEWS_CN_ALLOW_HOSTS`**：域名白名单（逗号分隔），如 `36kr.com,ithome.com,.sina.com.cn`。
- 可选 **`NEWS_CN_BLOCK_PRIVATE`**：是否拦截本机/私网/链路本地地址，默认开启（`1`）。

```powershell
$env:NEWS_CN_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
$env:NEWS_CN_ALLOW_HOSTS="36kr.com,ithome.com,.163.com,.sina.com.cn"
# 默认就是 1；设为 0 可关闭私网拦截（不建议）
$env:NEWS_CN_BLOCK_PRIVATE="1"
```

### 脚本路径

- `skills/news-cn/fetch.py`（仓库内一般为 `skill/news-cn/fetch.py`）

### 列出预设「列表页」与备用 RSS

```bash
python3 skills/news-cn/fetch.py list
```

返回 `pages`（主用）与 `feeds_rss`（可选）。`list-feeds` / `list-pages` 同样指向该命令。

### 网页模式：抓取并输出 JSON（默认）

```bash
python3 skills/news-cn/fetch.py fetch '{
  "pages": ["36kr", "ithome", "jiqizhixin"],
  "per_page": 12,
  "dedupe": true,
  "max_total": 40
}'
```

省略 `pages` 时默认：`["netease_news","sina_news","36kr","ithome"]`（网易新闻首页、新浪新闻首页、**36氪快讯**、IT之家）。另有预设键：`netease_tech`、`sina_tech` 等，见 `list` 输出。

| 字段 | 类型 | 说明 |
|------|------|------|
| pages | array | 预设 **键名**，或 **完整列表页 `https://...` URL**，或对象 `{"url":"...","key":"标签","selector":"main"}`（可选 CSS 缩小解析范围） |
| mode | string | `pages`（默认）、`rss`，或 `auto`（有 `feeds` 且无 `pages` 则走 RSS） |
| per_page | int | 每个列表页最多条数，默认 12，最大 40 |
| max_html_bytes | int | 单页下载上限，默认 3500000 |
| timeout | number | 请求超时秒数，默认 30 |
| dedupe | bool | 按标题去重，默认 true |
| max_total | int | 合并后总条数上限 |
| format | string | `json` 或 `markdown` |
| md_title | string | Markdown 标题 |

**PowerShell** 建议：`python skills\news-cn\fetch.py fetch @out\news_req.json`

### 输出 Markdown

```bash
python3 skills/news-cn/fetch.py fetch '{
  "pages": ["36kr", "qbitai"],
  "per_page": 8,
  "format": "markdown",
  "md_title": "科技快讯（网页抓取）"
}'
```

### 可选：RSS 模式（备用）

BBC 简体中文 feed 在不少网络下无法访问；预设里 `bbc_zh` 为**繁体主 feed**（`…/trad/rss.xml`）。简体 XML 可用 **`bbc_zh_simp`**。大陆若无法访问 `bbci.co.uk`，请优先 **`solidot_rss`** 或 **网页模式**。

```bash
python3 skills/news-cn/fetch.py fetch '{"mode":"rss","feeds":["solidot_rss","bbc_zh"],"per_feed":10}'
```

（网易 / 新浪 **无稳定 RSS**，请用网页模式的 `netease_news`、`sina_news` 等。）

### 一键每日简报（digest）

**一条命令**：按与 `fetch` 相同规则拉取条目，输出 **按来源分组** 的 **Markdown**（`# 标题` + 各源 `## 来源名` + 链接列表）到 stdout，**不调用任何外部 LLM**。

```bash
python3 skills/news-cn/fetch.py digest '{}'

python3 skills/news-cn/fetch.py digest '{"pages":["netease_news","sina_news","36kr"],"max_total":35}'
```

| JSON 字段 | 说明 |
|-----------|------|
| `digest_title` | 简报主标题，默认「今日新闻简报」 |
| `date` | 日期文案，默认当天（ISO 日期） |
| `stderr_meta` | `1` 时将抓取告警输出到 stderr |
| 其余 | 与 `fetch` 相同：`pages`、`per_page`、`max_total`、`dedupe`、`mode` 等 |

### 行为与限制

- 仅抓取 **http(s)**；从列表页挑出同站、**看起来像正文链接** 的 `<a>`（启发式规则；链接过少时可传 **`selector`** 或换 **频道子 URL**）。
- **SPA / 强 JS** 页面可能几乎无有效链接——请换 **文章列表直连** 或交给 Agent **web_fetch**。
- 条目版权与真实性以**源站**为准；付费墙可能导致点入后无全文。

### 安全说明

- 禁止 `file://`；仅请求 `http(s)` URL。
- 默认拦截 `localhost`、私网/链路本地/保留地址（可用 `NEWS_CN_BLOCK_PRIVATE=0` 关闭，不建议）。
- 如需更严格控制，设置 `NEWS_CN_ALLOW_HOSTS` 仅允许指定域名或其子域。
- 请遵守目标站 **robots** 与使用条款，控制抓取频率。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

