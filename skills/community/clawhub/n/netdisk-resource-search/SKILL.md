---
name: netdisk-resource-search
description: 聚合搜索百度网盘/夸克网盘/阿里云盘等网盘分享链接。当用户想按作者名、课程名、剧名、书名、软件名找网盘下载路径，或提到「网盘搜索」「PanSou」「盘搜」「找到下载链接」「夸克/百度/阿里网盘资源」时使用。包含已验证的 PanSou 协议端点、绕过系统代理的必要写法、以及可直接运行的本地 Web 应用 panradar.py。
agent_created: true
slug: netdisk-resource-search
displayName: 网盘资源聚合搜索（百度/夸克/阿里云盘）
version: 1.0.0
category: productivity
visibility: public
license: MIT
---

# 网盘资源搜索

按关键词聚合多个网盘搜索引擎，返回带提取码的分享链接。

> ⚠️ 本文的所有参数都经过实测。**「搜不到」的头号原因从来不是源少，而是两个技术细节：
> `res=merge` 丢结果、以及噪声过滤方法用错。** 换源之前先把这两条对一遍。

## 一、致命细节：绝对不要用 `res=merge`

PanSou 的 `/api/search` 支持 `res=merge|all|results`。**`merge` 会丢掉 97% 的结果**：

| 参数 | 搜「Java高级工程师」 | 搜「风间影月」 |
|---|---|---|
| `res=merge` | 合并出 **2 条** | 0~2 条 |
| `res=all` + 本地过滤 | 原始 **324 条 / 3048 链接** → 保留 47~75 条真命中 | 原始 145~3196 条 → 保留 9~75 条 |

`res=merge` 是服务端把 `results[]` 按 (网盘类型+分享 ID) 去重合并后的结果，去重键过粗，
会把大量不同课程的分享链接合并成一条。**必须取 `res=all`，拿原始 `results[]`，
每条自带 `links[]`，然后在本地按相关度过滤。** 这是本项目最重要的单点结论。

```python
url = base + "?" + urllib.parse.urlencode({"kw": q, "res": "all", "src": "all"})
j = json.loads(op.open(url, timeout=45).read().decode("utf-8", "replace"))
data = j["data"]
for r in data.get("results") or []:        # r: title / content / channel / datetime / images
    for lk in (r.get("links") or []):      # lk: url / password / type
        ...
# 另外 data["merged_by_type"] 是一份上游自己归类去重的高精度小结果集，一并收下
```

## 二、致命细节：噪声过滤必须用「最长公共子串」，不能用「命中词数」

上游是 Telegram 频道聚合，**做的是单字模糊匹配**。搜「风间影月」会返回：
《人间风月录》《兵自风中來》《名侦探柯南》《一饭封神》《超级工程》……

按「命中了几个查询词」判定完全拦不住（一个字就算命中）。正确指标是
**查询词与「title + content」的最长公共子串（连续）占查询词的比例，按词长加权**：

```python
def relevance(item, tokens):
    hay = ((item.get("title") or "") + " " + (item.get("content") or ""))[:600].lower()
    vals, weights = [], []
    for t in tokens:
        tl = t.lower().strip()
        if len(tl) < 2:
            continue
        if tl in hay:
            v = 1.0
        else:
            n = lcs_len(tl, hay)                       # 最长连续公共子串
            need = 2 if len(tl) <= 3 else 3            # 只沾 1~2 个字不算关系
            v = n / len(tl) if n >= need else 0.0
        vals.append(v); weights.append(len(tl))        # 长词信息量大，加权
    if not vals:
        return 1.0
    return sum(v * w for v, w in zip(vals, weights)) / sum(weights)
```

实测判别（阈值 `drop_below = 0.34`）：

| 查询 | 标题 | rel | 判定 |
|---|---|---|---|
| 风间影月 | 慕课网-体系课-Java高级工程师(风间影月) | 1.00 | 保留 |
| 风间影月 | 擦边短剧：人间风月录&浮世繁华 | 0.00 | 丢弃 |
| 一人团队项目开发实战 | mksz989-Vibe Coding 一人团队项目开发实战 | 1.00 | 保留 |
| 一人团队项目开发实战 | 名侦探柯南 剧场版合集 | 0.00 | 丢弃 |

**入库前先做一次宽松过滤**（`relevance(i, [query]) >= 0.25`），否则上游一次返回 3000+ 条
模糊匹配会把缓存撑爆、拖慢后续所有合并。

## 三、致命细节：上游 `title` 字段被字节截断，全名在 `content` 的「名称：」里

这是「明明搜到了课程，界面却显示成『马老师的』」的根因。上游同一条结果：

```
title   : '马老师的'                            ← 被按字节硬截断
title   : '慕课网-体系课-Java高级工程师('          ← 截断后还挂着半个括号
content : '名称：马老师的Java高级工程师 就业班 描述：本课程由资深Java专家马老师授课…'
```

规则：**把 `content` 里「名称：xxx」抠出来；若 title 归一化（去空格/括号/标点）后是它的前缀，
且只少 ≤25 个字 —— 那必然是截断，用完整名替换。** 多出几十个字的不算（那是标题里塞了整段
描述，例如「IT培训教程合集【网易云课堂…23.8G】…」，用了反而更糟）。

同时要裁掉截断留下的悬空括号：只在左括号出现在结尾 12 字内**且不配对**时才裁，
否则会误伤「超级工程 (2012) 1080P」「马老师的Java就业班（完结）」。

### 顺着作者名挖到课程名 —— 用户只给作者名时的关键一步

**资源是按课程名索引的，不是按作者名。** 所以搜作者名常常只出几条，用户会认为「搜不到」。
但上面从 `content` 补全出来的那个完整标题，正好就是课程名。把它抠出来再搜一次即可：

```
搜「风间影月」 -> 2 条（只有 pansou.app 收录）
  从标题「慕课网-体系课-Java高级工程师(风间影月)」剥掉查询词 -> 得到「Java高级工程师」
再搜「Java高级工程师」 -> 42 条（同一门课在 TG 频道里被分享了几十次）
```

实现要点（`derive_topics()`）：只从高相关（rel ≥ 0.6）的标题里挖；抠掉查询词时用**分隔符
顶替而不是空格**（否则「马老师的Java高级工程师就业班」去掉中段会粘成无意义的「马老师的就业班」）；
词组归一化后要 ≥5 字（拦住「就业班」「合集」这类泛词）；剥掉「095.」这类序号前缀；
按出现频次排、再按长度排；互相包含的只留更具体的那个。结果以可点击的按钮放在状态栏下方。

## 四、已实测的可用源

| 源 | 类型 | 端点 | 状态 |
|---|---|---|---|
| so.252035.xyz | pansou | `https://so.252035.xyz/api/search` | ✅ 主力，单次可返 3000+ 原始条目 |
| pansou.app | pansou | `https://pansou.app/api/search` | ✅ 量小但精度高 |
| Misoso | disksearch | `https://www.misoso.cc/v1/search/disk` | ✅ 夸克为主 |
| 混合盘 | disksearch_slim | `https://hunhepan.com/open/search/disk` | ⚠️ 容易 429，需分级冷却 |

已失效 / 别浪费时间的：`pansou.252035.xyz`（DNS 失败）、`pansou.us`（空）、
`qkpanso.com` / `kuake8.com`（签名校验，414/400）、`jikepan.xyz`（DNS 失败）、
`www.pansearch.me`（连接重置）、`pan666.net`（520）、`panta.me` / `qupansou.com`（404）。

搜索引擎兜底（Bing / 360 / 搜狗 site:pan.quark.cn）**实测几乎拿不到网盘链接**，不要指望。
微信/知乎/贴吧/掘金等平台页需要 JS 渲染，抓不到。

## 五、第四类细节：hunhepan 系的 `disksearch_slim` 只吃三个字段

hunhepan 与 misoso 虽同属 disksearch 协议，但**参数体完全不同**：

```python
# hunhepan：多传任何字段都返回「参数错误」。且忽略 size，每页固定 10 条，必须翻页。
POST https://hunhepan.com/open/search/disk
Body: {"q": "关键词", "page": 1, "size": 30}
Headers: Referer / Origin 必须带

# misoso：完整参数体
POST https://www.misoso.cc/v1/search/disk
Body: {"page":1,"q":"关键词","user":"","exact":false,"format":[],"share_time":"",
       "size":30,"type":"","exclude_user":[],
       "adv_params":{"wechat_pwd":"","platform":"pc"}}
```

- `disk_type` 映射：BDY→baidu, ALY→aliyun, QUARK→quark, TIANYI→tianyi, UC→uc,
  CAIYUN→mobile, 115→115, XUNLEI→xunlei, 123PAN→123, PIKPAK→pikpak
- **`code=417` 表示"没有搜索结果"，要按空结果处理，不能当报错**
- 标题里带 `<em>` 高亮标签要剥掉

## 六、必须绕过系统代理

本机代理会让请求报 `Tunnel connection failed: 502 Bad Gateway` 或
`WinError 10054 远程主机强迫关闭了一个连接`。**很多"源挂了"其实是代理问题。**

```python
op = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # 必带
op.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"),
                 ("Accept", "application/json, text/plain, */*"),
                 ("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8")]
```

另外**不要传 `plugins` 参数**（实测传了会 400/403/超时），只传 `kw` / `res` / `src`。

## 七、上游不稳定，要用「缓存并集累积 + 分级冷却」兜住

1. **单源响应随机性极大**：同一关键词实测出现过 145 条和 3196 条两种响应，
   真命中分散在不同批次里。所以缓存**不能覆盖写，要按 url 去重并入**（`merge_cache`），
   让「再挖一次」越挖越全。界面提供「⟳ 再挖一次」按钮，搜同一关键词多按几次结果会累积增长。
2. **失败源要冷却**，否则每次搜索都在等重试。按错误类型分级：
   限流（429/403）冷却 10 分钟，其它错误 2 分钟。
   **限流不要重试** —— 对端已记账，退避再打只会把机器钉得更死（实测 hunhepan 3 次重试白等 9 秒）。
3. 全部源都在冷却时仍放行全部，避免无源可用。

## 八、空结果降级：关键词太长就拆词

长课程名在所有源都可能是 0 条。**拆成独立词（如「一人公司」/「AI产品创造营」）再各搜一遍**，
命中率天差地别。降级触发条件要看**「相关度不为 0 的条数」而不是「总条数」**，
否则模糊匹配源的噪声会挡住降级。

## 九、推荐做法

直接用现成的本地 Web 应用，别重写：

```bash
python pan-radar/panradar.py                     # 打开 http://127.0.0.1:8931
python panradar.py --selftest 关键词              # 命令行验证链路，结果写 data/selftest.txt
```

已内置：双协议 4 源并发、`res=all` 原始结果采集、LCS 相关度过滤、标题补全（含悬空括号裁切）、
顺藤摸瓜（作者名 → 课程名二次搜索）、查询扩展 + 空结果分词降级、去重（网盘类型 + 归一化分享 ID）、
**跨网盘聚合**（bigram Dice 聚类「同一份资源的多个分享」）、**质量标签**（1080P / 完结 / 含源码…）、
相关度打分（匹配度/时效/网盘偏好）、整体超时上限、sqlite 缓存并集累积、失败源分级冷却、
提取码一键复制 / 复制本组全部 / 复制全部结果、Markdown/CSV 导出。

长期最稳：Docker 自建 PanSou 当主源，公共实例做备份。

```bash
docker run -d --name pansou -p 8888:8888 -v pansou-cache:/app/cache ghcr.io/fish2018/pansou:latest
```

## 十、同一份资源跨网盘怎么聚到一起

搜到 42 条 **≠** 有 42 份资源。同一门课常被转存到百度 / 夸克 / 阿里，而搜索结果的去重键是
「网盘类型 + 分享 ID」，所以**这些分享不会被合并**，用户得自己认出「这是同一个东西」。

按标题相似度聚类即可。**用 bigram（字符二元组）Dice 系数，不要用编辑距离**：

| 对比 | 编辑距离 | bigram Dice |
|---|---|---|
| 「尚硅谷Redis分布式缓存」vs「尚硅谷MySQL高级」 | 只差 4 字符 → 判成很像 ✗ | 交集仅「尚硅」「硅谷」→ 0.29 ✓ 不聚 |
| 「马老师的Java高级工程师就业班」vs 同名 +「【完整版】」 | 子串 → 同组 | 子串 → 同组 ✓ |

中文没有分词库，编辑距离对短标题过于宽松。判定顺序：

1. 长度差 > 60% → 直接排除（快速剪枝）
2. 归一化后互为连续子串 → 同一份（覆盖「课程名 + 【完结】【1080P】」这类后缀差异）
3. bigram Dice ≥ 0.75 → 同一份（兜住中间插字的情况）

每簇最多记 6 个 key，防止簇变大后两两比较的次数失控。实测搜「Java高级工程师」84 条
聚成 14 组，最大一组含 29 个分享（同一门课在 TG 频道被转存了几十次）。

## 十一、质量标签：把标题里的结构化信息抽出来

`title` + `content` 里本来就藏着大量可用信息，正则抽出来做成徽章即可，零网络请求：

| 类别 | 正则 | 展示 |
|---|---|---|
| 清晰度 | `4K\|2160P\|蓝光` ／ `1080P\|FHD` ／ `720P\|高清` | 绿 / 灰 |
| 状态 | `完结\|完整版\|全集` ／ `更新中\|连载` | 绿 / 橙 |
| 内容 | `源码\|源代码` ／ `课件\|讲义\|PPT` ／ `面试题\|题库\|笔记` ／ `PDF\|电子书` | 绿 / 灰 |
| 规模 | `(\d{2,4})\s*[集讲期]` | 灰 |
| 便利 | `无密\|无秘\|无提取码\|免提取码` | 绿 |

**坑**：裸的「资料」二字太宽松，几乎每条标题都沾，必须收紧成
`附资料|含资料|配套资料|资料包`。同一类别只取第一条命中的规则，否则「1080P 高清 超清」
会刷一排同义标签 —— 但「有没有源码」和「有没有课件」是两件独立的事，要拆成不同类别都保留。

## 十二、前后端两侧的健壮性（不做的话，用户只会看到一句天书）

搜索类应用的等待时间天然很长（多源并发几十秒），失败面也广。这两条是实际踩出来的：

**前端：绝对不要裸用 `(await fetch()).json()`。**
响应体为空时它抛的是 `Failed to execute 'json' on 'Response': Unexpected end of JSON input`，
用户完全无法据此判断发生了什么。统一封一层：`AbortController` 控超时 → 先 `text()`
→ 判空 → 判 `resp.ok/status` → 再 `JSON.parse`，每种情况给一句可操作的中文提示。
瞬时断连（服务重启、上游抖动）**静默重试一次**再报错。错误块里放「重试」按钮。

**后端：任何异常都不能让响应变成空 body。**
`BaseHTTPRequestHandler` 里异常冒泡会直接关连接，前端收到 0 字节 —— 这正是上面那句天书的来源。
必须：① 路由外层包总异常捕获，抛错也回 `{"ok": false, "error": ...}` 的 500 JSON；
② `json.dumps(..., default=str)` 兜底，防止某个字段混进 `set`/`datetime` 把整个响应炸掉。

**日志必须行缓冲。**
`python x.py > log 2>&1` 时 Python 默认块缓冲（8KB），`print(..., flush=True)` 之外的全卡在内存里。
`main()` 开头加 `sys.stdout.reconfigure(line_buffering=True)`，启动时再带 `-u` 双保险。
现象是**日志文件长期 0 字节**，服务端出错完全无从查证 —— 这个坑很容易误判成"服务没输出"。

**测试怎么覆盖这些分支**：给 DOM 桩的 `fetch` 加一个 `FETCH_MODE`（`ok/empty/badjson/http500/throw/abort/failOnce/hang`），
一次跑完全部故障路径。注意桩必须**同时提供 `text()` 和 `json()`**，只给 `json()` 的话新请求层根本跑不起来。

## 权限与合规

只聚合公开索引的分享链接，不托管文件。涉及付费课程 / 付费软件时，
不要代替用户检索并交出侵权资源链接；说明边界后让其自行决定，或改用免费/授权来源。
