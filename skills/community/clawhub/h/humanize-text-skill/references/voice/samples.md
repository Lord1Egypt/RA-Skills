# Voice samples | 人声样本档案

> 每个 voice 档配一段真实作者样本，供 `voiceMode: 'custom'` 校准和人工参照。
> 样本体现该档的指纹特征：句长均值/CV、连接词偏好、第一人称倾向、标点密度。
> 引擎用 `core/voice.js` 的 `calibrateFromSample()` 从这些文本抽取目标指纹。

样本是**合成参考文本**，体现各档的风格目标，不指向任何真实个人。每个档给
中英各一段，方便双语校准。

---

## `casual` — 随性 / blog, social, community

中文样本：

> 昨晚折腾到两点，终于把那个缓存 bug 揪出来了。其实就是 TTL 设短了，热点 key
> 一过期就集体回源，连接池直接打满。改成 5 分钟就好了。其实早该想到的，但
> 当时盯着别的方向，绕了一大圈。下次先看时间线。

英文样本：

> Rolled back the auth thing last night. Cookie scope was wrong — the path
> param ate the session. Fixed it, shipped it, moving on. Honestly should've
> checked that first but I was chasing the wrong thread for an hour.

**指纹**：短句为主（中文 ~15 字，英文 ~8 词），CV 高（长短交替），口语连接词
（其实/不过/honestly/but），第一人称密，标点少。

---

## `professional` — 专业 / LinkedIn, investor email, sponsor pitch

中文样本：

> 本季度我们完成了支付链路的重构，将交易超时率从 1.9% 降至 0.7%。重构涉及
> 三个微服务的接口对齐，因此排期上预留了两周的灰度窗口。下一步计划把这套
> 重试策略推广到订单服务，预计 Q3 完成。

英文样本：

> This quarter we refactored the payment pipeline, cutting transaction timeout
> rate from 1.9% to 0.7%. The work spanned three microservices and required a
> two-week canary window. Next, we'll extend the retry strategy to the orders
> service, targeting Q3 completion.

**指纹**：中等句长（~25 字 / ~18 词），CV 低（节奏稳定），主动语态，每段一个
具体 claim（数字/时间），连接词正式（因此/同时/therefore/however）。

---

## `technical` — 技术 / docs, technical blog

中文样本：

> `refresh_cache` 接受一个 `key` 参数，先失效本地 LRU 对应条目，再异步从 Redis
> 回源。如果 Redis 不可用，降级到本地缓存并记录一条 warn 日志。TTL 由
> `CACHE_TTL` 环境变量控制，默认 300 秒。注意：并发调用同一 key 会触发重复
> 回源，建议配合单飞模式。

英文样本：

> `refresh_cache` takes a `key`, evicts the local LRU entry, then async-fetches
> from Redis. If Redis is unreachable, it falls back to the local cache and
> logs a warning. TTL is controlled by `CACHE_TTL` (default 300s). Concurrent
> calls on the same key trigger duplicate fetches; pair with single-flight.

**指纹**：句长中等偏长（~28 字 / ~20 词），CV 低，祈使句和命令式，术语密集且
首次出现定义，每句一个 idea，几乎无第一人称。

---

## `warm` — 温暖 / mentorship, onboarding, thank-yous

中文样本：

> 第一次 oncall 紧张很正常，我当年第一次也被 pager 吓到过。你先把 runbook 过
> 一遍，遇到不熟的告警别硬扛，直接拉我进来。你看，大部分告警其实都有现成的
> 处置步骤，跟着走就行。这周我先陪你值一次，你就知道节奏了。

英文样本：

> First oncall is always nerve-wracking — I remember mine. Skim the runbook
> first; if an alert looks unfamiliar, page me instead of wrestling it alone.
> Most alerts have a ready-made playbook, you know? I'll shadow you this week
> so you get the rhythm.

**指纹**：中等句长（~22 字 / ~16 词），CV 中等，直接称呼（你/you），温和连接词
（你看/you know/不过），第一人称拉近距离，承认读者感受。

---

## `blunt` — 直率 / decision memos, thought leadership, hard feedback

中文样本：

> 这个方案不行。延迟没解决，只是换了个地方堆。别再加缓存层了，先回去测索引。
> 索引建对了，p99 自然下来。加层只会让排查更难。下周给我带个对比数据。

英文样本：

> This approach doesn't work. Latency isn't fixed, just relocated. Stop adding
> cache layers — go back and profile the index first. Get the index right and
> p99 drops on its own. More layers just make debugging harder. Bring me
> comparison data next week.

**指纹**：短句（~10 字 / ~7 词），CV 高，结论先行，近零 hedging，命令式，第一
人称存在但克制，连接词少而硬（但/so/just）。

---

## `custom` — 自定义（从作者样本校准）

不预设固定样本。使用方式：把作者本人的几段文本作为 `options.sample` 传入，
引擎会用 `calibrateFromSample()` 抽取该作者的真实指纹（句长分布、连接词集、
缩写率、第一人称倾向），作为拉拢目标。

```js
const authorSample = require('./voice/samples.md作者样本片段'); // 或直接传文本
Huorengan.analyzeText(text, {
  voiceMode: 'custom',
  sample: authorSample
});
```

**注意**：custom 只拟合**可观察的风格维度**（句长、节奏、连接词），不拟合隐私
特征或语义内容。它是「让改写向某个写作习惯靠拢」，不是「模仿某个具体人」。

---

## 校准验证

可以用引擎验证每个样本确实反映其档位：

```bash
node -e "
const H = require('./detector/patterns.js');
// 把上面某档的中文样本作为 custom 样本，校准出的目标应接近该档的 voice.toml 值
const sample = '昨晚折腾到两点...';  // casual 中文样本
const text = '值得注意的是，本次架构决策需要全面重新考量。';
const r = H.analyzeText(text, {voiceMode:'custom', sample});
console.log('drift:', r.voice.drift, '| target sentenceLen:', r.voice.target.sentence_len_target);
"
```

预期：casual 样本校准出的 target.sentence_len_target ≈ 12-18，与 voice.toml
的 casual 档一致。
