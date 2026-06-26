---
name: "House Price - 房价"
description: 按城市查二手房与新房参考均价、环比同比及近月走势（可生成列表与 SVG 折线图）。当用户说：长沙房价多少？深圳二手房均价走势？给个查房价链接，或类似城市房价问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🏠", "requires": { "bins": ["python3"] } } }
---

# 全国查房价（house-price）

数据来源为 **[查房价](https://fangjia.fang.com/)**（fangjia.fang.com）：各城市 **二手房 / 新房参考均价**、**环比与同比**、走势与排行榜等。数据为平台汇总与挂牌参考，**非房管局等权威发布**。

本技能由**极速数据**提供：[`https://www.jisuapi.com`](https://www.jisuapi.com)  
信息反馈：请发邮件至 `liupandeng@jisuapi.com`

单城市 URL：`https://fangjia.fang.com/{slug}/`（长沙示例：[fangjia.fang.com/cs/](https://fangjia.fang.com/cs/)）

## 何时使用本技能

- 问 **某市房价、二手/新房均价、涨跌、走势**
- 需要 **查房价直达链接** 或 **slug 查询**（全国城市 slug 见同目录 **`city.md`**，与 `SKILL.md` 一层）
- 需在答复中 **统一格式** 展示房价摘要时，使用下文 **固定中文输出模板**
- 需要 **自动拉取** 城市页上的新房/二手房参考均价时，运行 **`get.py`**（见下节）

## 资源路径（与 jisu-wechat-article 同结构）

| 文件 | 说明 |
|------|------|
| `skills/house-price/SKILL.md` | 本技能说明（Agent 主入口） |
| `skills/house-price/city.md` | 城市 slug 速查表 |
| `skills/house-price/get.py` | 命令行抓取并打印 |

## 命令行：get.py 抓取并输出

依赖：

```bash
pip install requests beautifulsoup4
```

```bash
python3 skills/house-price/get.py cs
python3 skills/house-price/get.py bj
python3 skills/house-price/get.py --url https://fangjia.fang.com/nanjing/
# 仅最近 6 个月走势；默认会多请求 2 个走势接口（二手房 + 新房）
python3 skills/house-price/get.py cs --trend-months 6
python3 skills/house-price/get.py cs --no-trend
# 可选：浏览器里看折线图（会写 HTML 文件）
python3 skills/house-price/get.py cs --chart
python3 skills/house-price/get.py cs --chart my_trend.html
# 可选：终端里一条 Unicode 示意（不写文件）
python3 skills/house-price/get.py cs --spark
# 默认会在 stdout 输出两段折线 SVG；不要 SVG 时：
python3 skills/house-price/get.py cs --no-svg-stdout
```

输出含 **当前月均价与环比**（来自城市页 HTML）、**过去多个月的参考均价序列**，以及 **默认附带两段折线 SVG**（与 `--chart` 内同源，打在 stdout，不写文件）。走势接口默认会请求；**`--no-trend`** 时仍会为 SVG **继续请求**走势接口（仅不打印按月文本列表），除非同时 **`--no-svg-stdout`** 才完全不拉走势接口。

**不必生成 HTML。** 只有显式加 **`--chart`** 时才会写出 **`fangjia_{slug}_trend.html`**；路径打在 **stderr**。**`--chart` 不可与 `--no-trend` 同用。**

**`--spark`**（可选）：在走势列表之后，再往 stdout 追加 **Unicode 示意条**；不可与 `--no-trend` 同用。若下游要 **严格按固定字段解析 stdout**，请加 **`--no-svg-stdout`**，且不要加 **`--spark`**。

**`--no-svg-stdout`**：关闭默认的 stdout **SVG** 输出；与 **`--no-trend`** 同用时，不再请求走势接口（仅首页一次）。

`get.py` 默认在按月列表（若有）之后、`极速 API 补充` 之前输出两段 `── SVG：…──` 与 `<svg>…</svg>`。下文「固定中文输出模板」描述的是 **字段语义**；机器按行解析时请使用 **`--no-svg-stdout`**。若首页价格块解析失败，退出码为 `2`。

**注意**：仅作低频、合规使用；勿用于高并发爬取。

## 固定中文输出模板（严格）

向用户展示「某城市房价」摘要时，**必须**按下列字段顺序输出；**无则填 `无`**，勿增删字段名，勿改行首标签。

```text
城市：{城市名}
统计月份或口径：{须写清「哪一年、哪一月」或页面原话；get.py 为「2026年三月」这类合并文案；无则填无}
二手房参考均价：{数值} 元/㎡（无则填无）
二手房环比上月：{【涨】或【跌】或【平】+ 页面原文，如「【跌】比上月下跌0.22%」；无则填无}
二手房同比去年：{同上，仅二手房；无则填无}
新房参考均价：{数值} 元/㎡（无则填无）
新房环比上月：{【涨】【跌】【平】+ 原文；无则填无}
二手房参考均价走势（按月，元/㎡；与站内折线图同源接口）：
  {YYYY-MM：整数元/㎡，每月一行；无数据则该小节仅一行「无」}
新房参考均价走势（按月，元/㎡；与站内折线图同源接口）：
  {同上}
说明：仅供参考，不作购房或投资依据。
```

**规则**

- **月份**：优先从页面均价标题读取（如「三月二手房参考均价」→ 三月），年份可与标题「走势2026」等合并为「2026年三月」；不得凭空编造月份。
- **涨跌**：环比、同比行须在句首用 **【涨】【跌】【平】** 标出方向（依据页面「比上月上涨/下跌」「比去年同期…」等原文判断），再跟原文或摘录，避免只看数字看不出涨跌。
- **月度走势（折线同源）**：与站内折线图一致，接口为 `ajaxtrenddata`（二手房）、`ajaxtrenddatanew`（新房）；按 **YYYY-MM** 每月一行、整数元/㎡；无数据则该小节仅输出一行「无」。不得编造历史月份价格。**`get.py` 默认**在 stdout 输出与 `--chart` 同源的 **两段 SVG**；不要 SVG 时用 **`--no-svg-stdout`**。需要 **浏览器里整页查看** 时用 `get.py --chart`（写 HTML）；**终端扫一眼** 可用 `get.py --spark`。
- 数字、百分比**仅来自用户粘贴的页面内容、get.py 输出或可信引用**，禁止编造。
- 若当前无法访问网页：仍输出 **城市、查房价链接** 与模板 **末行说明**；均价与环比等填 **无**，并提示用户自行打开链接查看。
- 多条城市：重复整块模板，**城市与城市之间空一行**。

## URL 规则（全国）

- 形态：`https://fangjia.fang.com/{slug}/`
- `{slug}` 通常与 `https://{slug}.fang.com/` 主站一致。
- **完整 slug 表**：请读同目录 **`city.md`**。

## 页面上常见信息类型

| 类型 | 说明 |
|------|------|
| 二手房参考均价 | 平台根据挂牌等估算，页内一般有数据说明 |
| 新房参考均价 | 多为市场信息汇总，仅供参考 |
| 环比 / 同比 | 相对上月、去年同期 |
| 走势 / 排行榜 | 曲线、区县榜、小区涨跌榜、热搜小区等 |

## 合规与抓取

- 遵守站点服务声明与 robots；**不提供**高频抓取、绕过风控的做法。
- **优先**用户浏览器打开查房价链接；需要自动化时可使用本技能 **`get.py`**，仍须控制频率。
- 不冒充政府备案价、不伪造成交价。

## 相关链接

- 查房价首页：<https://fangjia.fang.com/>
- 极速数据：<https://www.jisuapi.com/>
