---
name: jusou-search
slug: jusou-search
displayName: 聚搜GO 联网搜索
version: 1.0.3
summary: One API key for 8 search engines — web search, latest info and fact-checking for AI agents. 一个 Key 调 8 个搜索引擎，给 Agent 联网搜索、查最新信息与核实事实。
license: MIT
description: 用聚搜GO（Jusou）给 Agent 联网搜索：一个 Key 调 8 个搜索引擎（Exa / Tavily / Serper / SerpApi / Brave / 博查 / 百度 / AnySearch），按积分计费、失败不扣分。用户要求联网搜索、查最新信息、找资料、核实事实、多引擎对比，或提到 Tavily/Exa/Serper 替代、聚合搜索时使用。Web search for AI agents: search the web, latest information, fact-checking, multi-engine search with one API key — a Tavily / Exa / Serper alternative and a unified search API for AI agents. New users get 100 free points on sign-up (valid 7 days). 新用户注册赠送 100 积分（7 天有效）。
---

# Jusou Search — Web Search for AI Agents

## When to use

- You need real-time / latest information (news, prices, versions, schedules, policies) or facts beyond training data
- Finding sources, similar pages, documentation and official sites
- Comparing results across multiple search engines (global + China coverage complement each other)

## Setup

Set the environment variable `JUSOU_API_KEY` to the user's key from the console at https://jusouai.cn (keys look like `jsk_...`).
**New users get 100 free points on sign-up (valid 7 days)** — enough to try every engine. If there is no key, ask the user to sign up or redeem a card at jusouai.cn and put the key in the environment variable. Never ask the user to paste the key into the chat.

## How to search

Prefer the bundled script (zero-dependency Python 3). It lives in `scripts/` next to this SKILL.md; `$SKILL_DIR` below means the directory containing this file — locate it first, then build the path:

```bash
python3 "$SKILL_DIR/scripts/jusou_search.py" "Hangzhou weather"
python3 "$SKILL_DIR/scripts/jusou_search.py" "GPT-5 review" --engine exa --num 5
python3 "$SKILL_DIR/scripts/jusou_search.py" "新能源汽车销量" --engines baidu,bocha,exa --merge
python3 "$SKILL_DIR/scripts/jusou_search.py" "earnings report" --engine tavily --depth advanced
```

You can also call the unified API directly: `POST https://jusouai.cn/v1/search` (Bearer auth), with the same parameters as the script.

## Examples
```text
# User: "What's the weather in Hangzhou today?"
$ python3 "$SKILL_DIR/scripts/jusou_search.py" "杭州天气" --engine bocha --num 3
1. 2026年11月19日杭州天气预报
   https://bocha.cn/share/7c867faf-48ae-49a6-9243-9cee3166cc61
   2026年11月19日杭州天气预报: 11/19 (周四): 天气:晴,温度:14/6°C,风向风力:西南风<3级 …
-- 本次：博查 -1 积分，剩余 129        (charged 1 point, balance 129 — printed on stderr)
# User: "Verify the latest official height of Mount Everest for me."
$ python3 "$SKILL_DIR/scripts/jusou_search.py" "珠穆朗玛峰最新高程" --engines exa,bocha --merge --num 3
1. 习近平同尼泊尔总统班达里互致信函 共同宣布珠穆朗玛峰高程_中国政府网 (gov.cn)
3. 8848.86米！珠穆朗玛峰最新高程公布_央视网
   https://news.cctv.com/2020/12/09/ARTIf96rCeRLlKsVWjJ9i9G1201209.shtml
   …中尼两国8日联合对外宣布，珠穆朗玛峰的最新高程为8848.86米…
-- 本次：Exa -1 积分、博查 -1 积分，共 -2 积分，剩余 127        (charged 2 points, balance 127)
```

## Choosing an engine

| Scenario | Engine |
|---|---|
| English / semantic research, finding similar pages | `exa` |
| Structured results to feed a model | `tavily` |
| Google web / news / scholar / shopping | `serper` |
| Google results in the official SerpApi shape | `serpapi` |
| Independent index | `brave` |
| Chinese web pages (China-site coverage) | `bocha`, `baidu` (advanced depth = Baidu AI Search, generates an answer directly) |
| "Find me a WeChat Official Account article about X" | `bocha`, `baidu` — append `site:mp.weixin.qq.com` to the query |
| "See what Zhihu says about X" | `bocha`, `baidu` — append `site:zhihu.com` to the query |
| "How do I fix this error?" (Stack Overflow) | `serper`, `exa` — append `site:stackoverflow.com` to the query |
| "Check the official docs for X" | `exa`, `serper` — append `site:` + the official domain to the query |
| Default engine, multi-source aggregation fallback | `anysearch` |

Omit `engine` to use the default engine (anysearch). To compare, pass `--engines a,b,c` (each engine is charged separately). **Fact-checking:** for a claim that matters, don't trust a single source — run 2–3 engines at once (`--engines exa,bocha,serper --merge`) and compare: if independent sources agree, it's likely solid; if they conflict, dig deeper before answering. This is just the server-side multi-engine search used deliberately, not extra logic in this skill.

## Pricing (keep it in mind, don't burn points)

- Most engines cost 1 point per basic search (serpapi 4, brave 2). Higher tiers: exa advanced 2 / deep 4, tavily advanced 2, baidu advanced (AI Search) 3. serper, serpapi, anysearch and bocha only have a basic tier — passing a higher tier returns 400.
- Failed calls are never charged. Every response reports the points charged and the remaining balance; when the balance is insufficient the API says so explicitly — stop and tell the user to top up instead of retrying.
- Exa can return up to 100 results; beyond 10 results, each additional block of 10 costs extra points. Test with a small sample before large crawls.

## Troubleshooting

- 401: key invalid or not set — ask the user to check the environment variable.
- 402: insufficient points — suggest redeeming a card to top up (the same key accumulates automatically).
- 429: engine busy or rate-limited — retry once with a different engine, or wait and retry.
- 400: bad parameters (e.g. empty query) — fix the parameters; don't retry as-is.

---

# 聚搜GO 联网搜索

## 什么时候用

- 需要实时/最新信息（新闻、价格、版本、赛程、政策）或训练数据之外的事实
- 找资料、找同类网页、查文档与官网
- 想让多家搜索引擎对比着搜（国内外覆盖互补）

## 准备

环境变量 `JUSOU_API_KEY` = 用户在 https://jusouai.cn 控制台的 Key（形如 `jsk_...`）。
**新用户注册赠送 100 积分（7 天有效）**，够把每个引擎都试一遍。没有 Key 时，提示用户去 jusouai.cn 注册/兑换后把 Key 配到环境变量，不要让用户把 Key 贴在聊天里。

## 怎么搜

优先用随附脚本（零依赖 Python 3）。脚本在本 SKILL.md 同目录的 `scripts/` 下，下例 `$SKILL_DIR` 指本文件所在目录，先定位它再拼路径：

```bash
python3 "$SKILL_DIR/scripts/jusou_search.py" "杭州天气"
python3 "$SKILL_DIR/scripts/jusou_search.py" "GPT-5 review" --engine exa --num 5
python3 "$SKILL_DIR/scripts/jusou_search.py" "新能源汽车销量" --engines baidu,bocha,exa --merge
python3 "$SKILL_DIR/scripts/jusou_search.py" "财报" --engine tavily --depth advanced
```

也可以直接调统一接口 `POST https://jusouai.cn/v1/search`（Bearer 鉴权），参数同脚本。

## 示例
```text
# 用户：「杭州今天天气怎么样？」
$ python3 "$SKILL_DIR/scripts/jusou_search.py" "杭州天气" --engine bocha --num 3
1. 2026年11月19日杭州天气预报
   https://bocha.cn/share/7c867faf-48ae-49a6-9243-9cee3166cc61
   2026年11月19日杭州天气预报: 11/19 (周四): 天气:晴,温度:14/6°C,风向风力:西南风<3级 …
-- 本次：博查 -1 积分，剩余 129
# 用户：「珠穆朗玛峰现在到底多高？帮我核实一下。」
$ python3 "$SKILL_DIR/scripts/jusou_search.py" "珠穆朗玛峰最新高程" --engines exa,bocha --merge --num 3
1. 习近平同尼泊尔总统班达里互致信函 共同宣布珠穆朗玛峰高程_中国政府网 (gov.cn)
3. 8848.86米！珠穆朗玛峰最新高程公布_央视网
   https://news.cctv.com/2020/12/09/ARTIf96rCeRLlKsVWjJ9i9G1201209.shtml
   …中尼两国8日联合对外宣布，珠穆朗玛峰的最新高程为8848.86米…
-- 本次：Exa -1 积分、博查 -1 积分，共 -2 积分，剩余 127
```

## 选引擎

| 场景 | 引擎 |
|---|---|
| 英文/语义找资料、找相似网页 | `exa` |
| 给模型喂结构化结果 | `tavily` |
| Google 网页/新闻/学术/购物 | `serper` |
| 与 SerpApi 官方同形的 Google 结果 | `serpapi` |
| 独立索引 | `brave` |
| 中文网页（国内站覆盖） | `bocha`、`baidu`（advanced 深度 = 百度 AI 搜索，直接生成答案） |
| 「找一篇讲 X 的公众号文章」 | `bocha`、`baidu`，查询词后加 `site:mp.weixin.qq.com` |
| 「看看知乎怎么说 X」 | `bocha`、`baidu`，查询词后加 `site:zhihu.com` |
| 「这个报错怎么修」（Stack Overflow） | `serper`、`exa`，查询词后加 `site:stackoverflow.com` |
| 「查一下 X 的官方文档」 | `exa`、`serper`，查询词后加 `site:` + 官网域名 |
| 默认引擎、多源聚合兜底 | `anysearch` |

不指定 engine 用默认引擎 anysearch；要对比就 `--engines a,b,c`（各自扣分）。**事实核查：** 重要的说法别只信一家——用 `--engines exa,bocha,serper --merge` 一次搜 2–3 家对照：独立来源说法一致，可信度就高；互相打架就先深挖再回答。这只是把服务端现成的多引擎搜索用在核查上，Skill 里不另做逻辑。

## 计费（心里有数，别乱烧）

- basic 档多为 1 积分/次（serpapi 4、brave 2）；高级档：exa advanced 2 / deep 4、tavily advanced 2、baidu advanced（AI 搜索）3。serper、serpapi、anysearch、bocha 只有 basic 档，传高级档会报 400。
- 失败不扣分；每次返回都带本次扣分与剩余积分，余额不足会明确报错——这时停下来告诉用户去续费，不要反复重试。
- Exa 最多可返回 100 条结果，超过 10 条后每多 10 条加收积分，大批量抓取前先小样试。

## 出错怎么办

- 401：Key 无效或没配，让用户检查环境变量。
- 402：积分不足，提示兑换卡密续费（同一 Key 自动叠加）。
- 429：引擎繁忙或限流，换一家引擎重试一次，或稍后再试。
- 400：参数问题（如 query 为空），修正参数，不要原样重试。
