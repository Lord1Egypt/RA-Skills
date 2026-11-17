# 知识产权 / 合规检测 skills

**21 个 skill**，睿观 6（外观专利 / 实用新型 / 文字商标 / 图形商标 / 版权 / 枪支合规）+ 智慧芽 15（专利书目 / 权利要求 / 说明书 / PDF / 图像搜索 / 法律状态 / 引用/被引用 / 同族 / 摘要 / 翻译）。

**归属 agent**：全部挂载在 `default`。`linkfox-market-analysis-agent` / `linkfox-product-selection-agent` 也继承。

**不确定用哪个 agent？** → 用 `default`。default 覆盖本桶所有 21 个 skill。

## Skills

| skill | 数据源 | 检测/查询类型 | 入参（关键字段） | 返回摘要 |
|---|---|---|---|---|
| `linkfox-ruiguan-copyright-detection` | 睿观 | 图片版权检测 | `imageUrl`, `topNumber`, `enableRadar` | 版权侵权列表：`similarity`·`copyrightCode`·`rightsOwner`·`troCase`·`subRadarResult`·`pathThumb` |
| `linkfox-ruiguan-detection-patent-design` | 睿观 | 外观专利检测 | `imageUrl`, `queryMode`, `regions`, `topLoc` | 外观专利列表：`similarity`·`applicationNumber`·`patentImageUrl`·`radarResult{same,exp}`·`troCase`·LOC |
| `linkfox-ruiguan-gun-parts-search` | 睿观 | 产品图片违规品合规筛查 | `imageUrl` | 违规品匹配：`cosine`·`pdImgOssUrl`·`pdTitle`·`pdTitleCHNCensored`·`detectId` |
| `linkfox-ruiguan-text-trademark-detection` | 睿观 | 文字商标检测 | `productTitle`, `regions`, `limit`, `productText` | 商标风险：`textTrademarkRadar`(0/1/2)·`highestModeScore`·`blacklistTrademarks`·`whitelistTrademarks`·匹配商标详情 |
| `linkfox-ruiguan-trademark-graphic-detection` | 睿观 | 图形商标检测 | `imageUrl`, `topNumber`, `regions`, `trademarkName` | 图形商标匹配：`similarity`·`trademarkName`·`status`·`applicant`·`niceClass`·`radarResult`·`subRadarResult` |
| `linkfox-ruiguan-utility-patent-detection` | 睿观 | 实用新型/发明专利检测 | `productTitle`, `productDescription`, `region`, `topNumber` | 实用专利风险：`similarity`·`title/titleCn`·`applicationNumber`·`patentValidity`·`troCase`·`troHolder`·`exdt` |
| `linkfox-zhihuiya-abstract-data-translated` | 智慧芽 | 专利摘要（翻译） | `patentId`/`patentNumber`, `lang`, `replaceByRelated` | 翻译摘要：`data[].pn`·`title`·`abstractText`·`pnRelated` |
| `linkfox-zhihuiya-abstract-image` | 智慧芽 | 专利摘要附图 | `patentId`/`patentNumber` | 摘要附图：`data[].pn`·`abstractDrawingPath` |
| `linkfox-zhihuiya-bibliography` | 智慧芽 | 专利完整书目 | `patentId`/`patentNumber` | 完整著录：`inventionTitle`·`applicants`·`assignees`·`inventors`·IPC/CPC/LOC·`priorityClaims`·`referenceCitedPatents`·`exdt` |
| `linkfox-zhihuiya-claim-data` | 智慧芽 | 专利权利要求原文 | `patentId`/`patentNumber`, `replaceByRelated` | 权利要求原文：`data[].claims[]`·`claimCount`·`pnRelated` |
| `linkfox-zhihuiya-claim-data-translated` | 智慧芽 | 专利权利要求（翻译） | `patentId`/`patentNumber`, `lang`, `replaceByRelated` | 翻译权利要求：`data[].pn`·`claims`·`pnRelated` |
| `linkfox-zhihuiya-description-data` | 智慧芽 | 专利说明书原文 | `patentId`/`patentNumber`, `replaceByRelated` | 说明书原文：`data[].pn`·`description[]`·`pnRelated` |
| `linkfox-zhihuiya-description-data-translated` | 智慧芽 | 专利说明书（翻译） | `patentId`/`patentNumber`, `lang`, `replaceByRelated` | 翻译说明书：`data[].pn`·`description`·`pnRelated` |
| `linkfox-zhihuiya-fulltext-image` | 智慧芽 | 专利全文附图 | `patentId`/`patentNumber`, `limit`, `offset` | 全文图纸：`data[].pn`·`fulltextImagePath`·`imageType`·`total` |
| `linkfox-zhihuiya-legal-status` | 智慧芽 | 专利法律状态 | `patentId`/`patentNumber` | 法律状态：`simpleLegalStatus`·`legalStatus`·`eventStatus`·`legalDate` |
| `linkfox-zhihuiya-patent-cited` | 智慧芽 | 专利被引用（前向被引） | `patentId`/`patentNumber` | 被引统计：`citedBy3y`·`citedBy5y`·`citedBySimpleFamily`·`citedByInpadocFamily`·`citedByPatsnapFamily`·`citedByPatents[]` |
| `linkfox-zhihuiya-patent-family` | 智慧芽 | 专利同族 | `patentId`/`patentNumber` | 同族成员：`simpleFamily[]`·`inpadocFamily[]`·`patsnapFamily[]` 及对应 `familyId` |
| `linkfox-zhihuiya-patent-forward-citation` | 智慧芽 | 专利引用（本专利引证） | `patentId`/`patentNumber` | 引证参考：`citedPatents[]`·`citedOthers[]` |
| `linkfox-zhihuiya-patent-image-search` | 智慧芽 | 外观专利以图搜专利 | `url`, `patentType=D`, `model`, `country`, `loc` | 外观专利列表：`score`·`apno`·`title`·`inventor`·`loc`·图片 URL·`radarResult` |
| `linkfox-zhihuiya-pdf-data` | 智慧芽 | 专利 PDF 下载 | `patentId`/`patentNumber`, `replaceByRelated` | PDF 链接：`data[].pn`·`pdfPath`·`pnRelated` |
| `linkfox-zhihuiya-simple-bibliography` | 智慧芽 | 专利简版书目 | `patentId`/`patentNumber` | 简版著录：`title`·`abstractContent`·`applicants`·`inventors`·`assignees`·`applicationDate`·`publicationDate`·IPC/CPC/LOC·`citedPatents` |
