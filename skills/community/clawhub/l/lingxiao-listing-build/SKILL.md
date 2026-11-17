---
name: lingxiao-listing-build
description: 上架链接自动生成：把一份商品资料拼成 TikTok Shop 或 Etsy 可直接导入的草稿字段，并按平台硬限制出校验报告；Etsy Listing 可逐条体检标题、13 Tags、详情与图位。接领霄官网 MCP，草稿组装与校验免费。当用户要上架商品、批量生成链接、做 Listing、检查标题标签是否超限、把商品资料导入平台、优化 Etsy Listing 时使用。
---

# 上架链接生成

上架失败最常见的原因不是文案不好，是**字段拼错了**：类目 id 缺失、图片用了本地路径、
tag 数量不对。这些平台会拒，但报错信息通常看不懂。先在本地把形状校验过再送过去。

## 接官网 MCP（不用注册）

把这段粘进 MCP 客户端（WorkBuddy、Cursor、Claude Code 写法都一样）：

```json
{ "mcpServers": { "lingxiao": { "url": "https://www.lingxiaochuhai.com/mcp" } } }
```

不填 key 就是匿名试用：每个 IP 每天 20 次工具调用。
`listing_draft_build` 与 `etsy_listing_check` 在免费的 `public` 档，纯计算不花钱。

下面的文案生成会调模型、按人扣配额，那个必须有账号：
<https://www.lingxiaochuhai.com/app/membership?from=mcp-trial>

## 三个工具的分工

搞混这三个会绕远路：

| 工具 | 做什么 | 输入是谁的 | 花钱 |
|---|---|---|---|
| `listing_draft_build` | 组装成平台形状 + 校验 | 你自己的商品资料 | 否 |
| `listing_copy_generate` | 出三档标题、详情正文、tags | 你的关键词与卖点 | 是，约 ¥0.3/次 |
| `listing_packs` | 取研究仓出的成品详情包 | 我们的资产 | 订阅内 |

典型顺序：先用 `listing_copy_generate` 出文案，再喂给 `listing_draft_build` 拼成草稿。

## 组装草稿

```
listing_draft_build({
  platform: "tiktok",
  title: "...", description: "...",
  sku: "BAG-001", price: 29.9, quantity: 50,
  categoryId: "601234",
  images: ["https://cdn.example.com/1.jpg"]
})
```

返回 `draft`（可直接导入的字段）和一份校验报告：
**fail = 平台会拒或字段拼不出来，warn = 能导入但掉转化。先清 fail 再看 warn，别混着改。**

三件事要先知道：

- **这个工具不代你提交。** 它不连你的店、不读库存订单、不碰任何店铺授权，
  只把资料拼成目标平台的形状交回给你，导入由你自己做。
- **图片必须是公网可访问的 http(s) 绝对地址。** 本地路径和内网地址会被丢弃并在校验里点名。
- **`readyToImport` 为 false 时别硬送。** 平台那边的报错比这里的难懂得多。
- 校验过了**不代表能过审**。类目必填属性、资质证书、图片像素要到平台后台才验得了。

TikTok 的 `categoryId` 是必填的，缺了建不了品；不给 `quantity` 时按测款默认 5。

## Etsy Listing 体检

```
etsy_listing_check({
  title: "...", tags: [...13 个...], description: "...",
  primaryKeyword: "linen apron", imageCount: 7,
  hasSceneImage: true, hasSizeReference: true, isPersonalized: false
})
```

硬限制判 fail：标题 140 字符、**正好 13 个 tag**、每个 tag 20 字符以内。
掉转化但不违规的判 warn，比如主词没进标题前 40 字符、标题拿店名开头、缺尺寸对比图。

它只看你给的文本，**不连店铺**，所以判不了类目、属性、变体、运费模板，
也判不了"这个主词值不值得做"——那要看 Etsy 搜索下拉和自家 Shop Stats。
全过不等于会出单，排序还看点击、成交与店铺健康度。

## 标题的排序逻辑

平台搜索读的是标题前段，人读的是第一眼。两者要在同一个位置满足：

```
主关键词（前 40 字符内） + 核心差异点 + 使用场景 + 规格
```

不要用店名开头，不要堆同义词。同一个意思换三种说法占不到三份权重，
只会把真正有区分度的词挤出可见区。

## 到这一步要上官网

**要文案** — `listing_copy_generate` 出三档标题、详情正文与 tags，
按目标市场语种生成。会真调模型，约 ¥0.3 一次，必须带 `confirm: true` 才执行，
不带 confirm 只返回报价。生成记录落在你名下，可在官网"生成记录"里找回，不用重跑。

**要图** — MCP 这条只出文字。主图详情图走网页版链接生成器：
<https://www.lingxiaochuhai.com/tools/link-builder>

**要整套** — 从选品直接出详情包（文案 + 主图详情图 + 图位提示词），不用自己拼字段：
<https://www.lingxiaochuhai.com/tools/auto-listing>

## 边界

- 文案生成扣的是你账号的配额，免费档配额为 0 会直接返回 403。那是套餐问题，重试没有意义。
- 平台字段规则会变。校验规则跟的是当期已知限制，被拒时以平台后台报错为准。
- 批量上架前先跑通一条。第一条的 fail 通常是整批共有的。
