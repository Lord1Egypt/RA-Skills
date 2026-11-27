# 配方卡索引（INDEX）

> 改卡必须同步改本索引。卡名 = 文件名。

| 卡 | 输入 | 一句话适用 | 稳定性 | 代表案例图 |
|---|---|---|---|---|
| brainstorm-12 | 纯文字 | 画面方向不清时先出 12 套创意方案（概念/画面/风格/slogan/渠道），挑 1 套再生成 | 高 | 无（文字方案） |
| surreal-micro-world | 文生图 | 要创意冲击/脑洞：巨型产品×微缩小人，卖点翻译成物理场景 | 高 | assets/surreal-honey-fall.png |
| surreal-frozen-liquid | 文生图（可附参考图） | 要氛围感+设计感：液体反重力定格（时间暂停），液体/膏体/酱体类产品 | 中（流体质感是命门） | assets/surreal-frozen-liquid-ketchup.png |
| hand-drawn-theater | 图生图（**需照片**） | 要可爱互动感：真实主体+米白底+黑色手绘小剧场 | 高（主体识别强） | assets/handdrawn-milkshake.png（对照 milkshake-original.png 原图） |
| retro-print-poem | 图生图（**需照片**） | 要高级复古感：大字衬线+半调网点+英文诗 | **中**（穿字指令 v0.2.0 定稿回灌并实测 1/1 通过；诗句/颜色槽位化防乱码防发黑） | assets/retro-milkshake-joyful.png（对照 milkshake-original.png 原图） |
| product-in-hand | 文生图 | 要时尚大片感：低机位广角仰拍，前景产品锐利+背景人物虚化 | 高（槽位全可换） | assets/product-in-hand-milkshake.png |
| apple-minimal | 文生图 | 要发布会级极简：纯白+超多留白+影棚柔光+手持产品 | **未知**（Day3 新入未实测） | 首测后回补 |
| ecomm-white-bg | 图生图（**需实拍图**） | 电商白底精修：保结构保配色换纯白底+C4D 质感（非海报，电商主图） | **未知**（Day3 新入未实测） | 首测后回补 |
| sticker-collage | 文生图 | 清单式种草：容器+5-7 件贴纸单品+箭头标注（自带官方模板/负面词） | **未知**（Day3 新入未实测） | 首测后回补 |
| retro-collage-holiday | 图生图（照片可选） | 节日礼物指南：酒红+奶白复古拼贴+拍立得+丝带 | **未知**（Day3 新入未实测） | 首测后回补 |
| retro-diner-food | 文生图 | 复古美式快餐：明黄高对比+复古大字排版+潮流回归叙事 | **未知**（Day3 新入未实测，资料包未配图） | 首测后回补 |
| chinese-street-food | 文生图 | 中式市井烟火气：毛笔书法大字+印章+动态细节（官方占位符模板） | **未知**（Day3 新入未实测） | 首测后回补 |
| xhs-home-annotate | 图生图（**需实拍图**） | 小红书家居笔记标注：原片+白色描边+手写批注+箭头（非海报，笔记封面） | **未知**（Day3 新入未实测） | 首测后回补 |
| second-world-split | 图生图（**需照片**） | 创意型格款：上半实拍原貌+下半象牙纸涂鸦第二世界（连贯性纪律最严） | **未知**（Day3 新入未实测） | 首测后回补 |

## 选卡速查

- 有照片？→ hand-drawn-theater（可爱）/ retro-print-poem（复古）/ second-world-split（创意型格）/ xhs-home-annotate（家居笔记）/ ecomm-white-bg（电商白底）/ retro-collage-holiday（节日拼贴）
- 无照片？→ surreal-micro-world（脑洞）/ surreal-frozen-liquid（液体定格）/ product-in-hand（时尚）/ apple-minimal（极简）/ sticker-collage（清单）/ retro-diner-food（美式快餐）/ chinese-street-food（中式美食）
- 没想法？→ 先 brainstorm-12
- 液体/酱体类产品、要「氛围感+设计感」、无人 → 优先 surreal-frozen-liquid（与 surreal-micro-world 的「微缩小人」路线不同）

> 槽位口径：文生图卡（surreal-micro-world）标准四槽「产品名/品类/一句话卖点/主色」；图生图卡的核心输入是「照片 1 张」，无照片时换文生图卡或请用户补拍。
> Day3 新卡（后 8 张）稳定性一律「未知」——prompt 原文照录课程资料包（配官方模板/负面词/占位符的已槽位化），**首测后按实测回写稳定性**。
