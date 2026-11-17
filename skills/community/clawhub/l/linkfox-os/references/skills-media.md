# 图片/视频/文本生成 skills

**10 个 skill**，覆盖 AIGC 底层（imagegen / textgen / videogen）+ 编排型套图（product / cloth / bestseller-replicate / mannequin-to-model / fission）+ 品牌基因 + 批量视频。

**归属 agent**：
- 底层（`linkfox-aigc-imagegen` / `-textgen` / `-videogen` / `-videogen-multi` / `-imagegen-brand-gene-extract` / `-imagegen-product` / `-imagegen-cloth`）都在 `default`
- 3 个 image-agent 独占：`bestseller-replicate` / `image-fission` / `mannequin-to-model`

**用什么 agent**：
- 底层生图/生视频、商品/服饰套图 → `default` 就行
- 爆款复刻 / 图片裂变 / 人台换模特 → **必须** `--model linkfox-image-agent`
- 用视频专业 agent（`linkfox-video-agent`）也 OK，但它只挂了单/多视频两个 skill

## Skills

| skill | 类型 | 用途 | 入参（关键字段） | 返回摘要 | 归属 agent |
|---|---|---|---|---|---|
| `linkfox-aigc-imagegen` | 原子生图 | Tier1 文/图生图，多 provider 多比例底层能力 | `imageUrls`, `prompt`, `provider`(BANANA_PRO/GPT_2_IMAGE/AIDRAW_EDIT/WAN2_7/SEEDREAM5), `outputNum`, `resolution`, `aspectRatio` | stdout `Saved full response: [本地路径数组]`，失败为单个 json 路径 | default / image / listing / market |
| `linkfox-aigc-imagegen-bestseller-replicate` | 爆款复刻 | 亚马逊 listing 或参考图的排版套到用户商品原图 | `product_image`, `amazon_input` 或 `reference_images`, `provider`, `aspectRatio` | 每张参考图 1:1 出复刻图本地路径列表（图二↔复刻结果对照表） | image |
| `linkfox-aigc-imagegen-brand-gene-extract` | 品牌基因 | 从商品图+品牌参数提取统一 Brand DNA | `images`, `brandKey`(brandColor/fontStyle/brandName/language/platform/salesRegion) | 落盘 `brandGeneJson`（长度 1 的 JSON 列表）绝对路径，供套图 S3 复用 | default / image / listing |
| `linkfox-aigc-imagegen-cloth` | 服饰套图 | 服饰白底/模特/种草/卖点/A+/尺码统一编排调度 | `imageUrls`, `type`(WHITE_BG/MODEL_IMAGE/SCENE/SELLING_POINT/*_APLUS/SIZE), `provider`, `ratio`, `resolution` | 单张:imagegen 路径；套图:三阶段 pipeline，summary 输出内联 `![]()` 明细 + manifest | default / image / listing |
| `linkfox-aigc-imagegen-image-fission` | 图片裂变 | 商品不变、视觉差异化裂变，铺货防关联 | `images`, `model`(BANANA_PRO/GPT_2_IMAGE), `quality`, `similarity_threshold`, `fission_count`, `image_advice_list` | 原图↔裂变图本地绝对路径对照表（每原图 × fission_count 张） | image |
| `linkfox-aigc-imagegen-mannequin-to-model` | 人台换模特 | 人台图转真人模特上身电商展示图 | `imageUrls`(人台/模特参考/背景参考), `customerKeywords`, `provider`, `ratio`, `resolution` | 单次 `run_mannequin.py` 出图，stdout `Saved full response: [本地路径]` | image |
| `linkfox-aigc-imagegen-product` | 商品套图 | 非服饰白底/场景/特写/卖点/A+ 统一编排调度 | `imageUrls`, `type`(WHITE_BG/SCENE/CLOSE_UP/SELLING_POINT/*_APLUS), `provider`, `ratio`, `resolution` | 单张:imagegen 路径；套图:三阶段 pipeline，summary 输出 `![]()` 明细 + asset manifest | default / image / listing |
| `linkfox-aigc-textgen` | 文本生成 | Tier1 文本/图文/视频理解，被套图链式调用或独立生文 | `prompt`, `imageUrls`(图/视频), `model`(GEM_3_FLASH/GEM_3_1_PRO), `thinkingLevel` | stdout JSON 含 `content`（换行压平为 `⏎`），或 `--content-only` 单行文本 | default / image / listing / market / selection / video |
| `linkfox-aigc-videogen` | 单视频 | 首尾帧/单图生视频 | `imageUrl`, `videoType`(KLING/WAN/SEED/SEED_FAST/HAILUO), `videoTime`, `lastFrameImageUrl`, `prompt` | stdout `Saved full response: [本地视频路径]`，task 记录落盘 data/ | default / video |
| `linkfox-aigc-videogen-multi` | 多图视频 | 多参考图生成 1 条视频 | `imageList`, `videoType`(KLING/SEED/SEED_FAST/HAPPY_HORSE), `videoTime`, `aspectRatio`, `resolution`, `prompt` | stdout `Saved full response: [本地视频路径]`，task 记录落盘 data/ | default / video |
