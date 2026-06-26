# Sif数据分析工具

共 4 个工具。使用 `@工具中文名` 语法在任务提示词中调用。

### @SIF-ASIN的关键词

反查词库、流量入口

工具中文名：SIF-ASIN的关键词
功能说明：根据亚马逊站点 和 asin 查询 这个 商品的 流量关键词

**Prompt 模板：**

> 在亚马逊{{美国站}}查询 ASIN 为{{B089M9KVFS}}的商品关键词数据

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **国家站点**: `US`=亚马逊-美国站, `UK`=亚马逊-英国站, `DE`=亚马逊-德国站, `CA`=亚马逊-加拿大站, `JP`=亚马逊-日本站, `FR`=亚马逊-法国站, `ES`=亚马逊-西班牙站, `IT`=亚马逊-意大利站, `MX`=亚马逊-墨西哥站, `AU`=亚马逊-澳大利亚站, `AE`=亚马逊-阿联酋站, `BR`=亚马逊-巴西站, `SA`=亚马逊-沙特阿拉伯站
- **ASIN码**: 必填
- **关键词，尽量翻译成对应国家站点的语言**
- **时间片段类型，默认 `latelyDay`**: `latelyDay`=最近N天, `month`=某月, `week`=某周
- **时间片段值，默认 `7`**: `latelyDay` 时仅支持 `7` 或 `30`；`month` 时为 `YYYY-MM`（如 `2026-04`）；`week` 时为周开始日期 `YYYY-MM-DD`（如 `2026-04-13`）
- **条件筛选,多个条件以英文逗号隔开**:
  - 标志类：`nfPosition`=自然流量词, `isSpAd`=sp广告词, `isBrandAd`=品牌广告词, `isVedioAd`=视频广告词, `isAC`=ac推荐词, `isAccurateKw`=精准流量词, `isAccurateTailKw`=精准长尾词, `isPurchaseKw`=出单词, `isQualityKw`=转化优质词, `isStableKw`=转化平稳词, `isLossKw`=转化流失词, `isInvalidKw`=无效曝光词, `isMultiVariantKw`=多变体自然位词, `isSearchVolUpKw`=搜索量同比增长词, `isSearchVolDownKw`=搜索量同比下降词
  - 周期计数类：`totalPeriod.in`=新进全部流量词, `nfKeywordCnt.total`=有自然曝光的流量词, `nfKeywordCnt.in`=新进自然流量词, `adKeywordCnt.total`=有广告曝光的流量词, `adKeywordCnt.in`=新进广告流量词, `allSpKeywordCnt.total`=SP广告流量词, `allSpKeywordCnt.in`=新进SP广告流量词, `spKeywordCnt.total`=SP常规流量词, `spKeywordCnt.in`=新进SP常规流量词, `recSpKeywordCnt.total`=SP推荐流量词, `recSpKeywordCnt.in`=新进SP推荐流量词, `allSbKeywordCnt.total`=SB广告流量词, `allSbKeywordCnt.in`=新进SB广告流量词, `sbKeywordCnt.total`=SB常规流量词, `sbKeywordCnt.in`=新进SB常规流量词, `sbvKeywordCnt.total`=SBV流量词, `sbvKeywordCnt.in`=新进SBV流量词
- **排序字段**: ``=默认系统排序, `lastRank`=自然排名, `adLastRank`=广告排名, `updateTime`=关键词抓取时间, `searchesRank`=搜索排名, `estSearchesNum`=月搜索量
- **每页数量,最小10，最大100，默认也是100**: 范围 10~100
- **页码**
- **是否降序，默认传 true **

---

### @SIF-关键词流量来源

曝光分析、竞争卡位

工具中文名：SIF-关键词流量来源
功能说明：支持关键词的流量结构分析，了解该词下自然搜索、SP广告、SB品牌广告、SBV视频广告及 SP 推荐位的竞争格局；支持按 ASIN 过滤、指定日期区间及新进流量词筛选。

**Prompt 模板：**

> 在{{美国站}}查询关键词为{{headphone}}的流量来源

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **国家站点**: `US`=亚马逊-美国站, `UK`=亚马逊-英国站, `DE`=亚马逊-德国站, `CA`=亚马逊-加拿大站, `JP`=亚马逊-日本站, `FR`=亚马逊-法国站, `ES`=亚马逊-西班牙站, `IT`=亚马逊-意大利站, `MX`=亚马逊-墨西哥站, `AU`=亚马逊-澳大利亚站, `AE`=亚马逊-阿联酋站, `BR`=亚马逊-巴西站, `SA`=亚马逊-沙特阿拉伯站
- **搜索关键词，尽量翻译成对应国家站点的语言**: 必填
- **ASIN 过滤列表，多个用英文逗号分隔**: 不传则返回该关键词下所有 ASIN；最大长度 1000 字符
- **条件筛选,每次只能传一个**:
  - 标志类：`nfPosition`=自然流量词, `isSpAd`=sp广告词, `isVedioAd`=视频广告词, `isBrandAd`=品牌广告词, `isPPCAd`=ppc广告词, `isSearchRecommend`=搜索推荐词, `acAd`=SP推荐
  - 周期计数类：`totalPeriod.in`=新进全部流量词, `nfKeywordCnt.total`/`.in`, `adKeywordCnt.total`/`.in`, `allSpKeywordCnt.total`/`.in`, `spKeywordCnt.total`/`.in`, `recSpKeywordCnt.total`/`.in`, `allSbKeywordCnt.total`/`.in`, `sbKeywordCnt.total`/`.in`, `sbvKeywordCnt.total`/`.in`
- **是否取最近 7 天数据，默认 `true`**: 传 `false` 时使用 `startDate`/`endDate` 区间
- **开始日期 `yyyy-MM-dd`**: `last7d=false` 时生效；不填取系统最新整周
- **结束日期 `yyyy-MM-dd`**: 与 `startDate` 配套
- **排序字段**: `totalKeywordNum`=全部流量词, `naturalKeywordNum`=自然流量词, `brandKeywordNum`=品牌广告词, `vedioKeywordNum`=视频广告词, `acKeywordNum`=ac推荐词, `erKeywordNum`=er推荐词, `trKeywordNum`=tr推荐词, `sumScore`=所有关键词下曝光总得分, `totalNfScore`=所有自然排名曝光总得分, `totalSpSocre`=所有sp广告曝光总得分（注意拼写）, `totalBrandScore`=所有品牌广告曝光总得分, `totalVedioScore`=所有视频广告曝光总得分, `totalAcScore`=所有ac推荐曝光总得分, `totalTrScore`=所有tr推荐曝光总得分, `totalErScore`=所有er推荐曝光总得分
- **每页数量，最小10，最大100，默认也是100**: 范围 10~100
- **页码**
- **是否降序，默认传 true **

---

### @SIF-ASIN流量来源

流量结构、渠道占比、周期对比

工具中文名：SIF-ASIN流量来源
功能说明：支持竞品流量来源拆解，分析其自然搜索、广告投放及推荐流量的占比结构；额外提供"本期/上期/新进/退出"等周期对比字段，便于跨周对比。

**Prompt 模板：**

> 在{{美国站}}查询 ASIN 为 {{B0C3LRC59F}} 的流量来源

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **国家站点**: `US`=亚马逊-美国站, `UK`=亚马逊-英国站, `DE`=亚马逊-德国站, `CA`=亚马逊-加拿大站, `JP`=亚马逊-日本站, `FR`=亚马逊-法国站, `ES`=亚马逊-西班牙站, `IT`=亚马逊-意大利站, `MX`=亚马逊-墨西哥站, `AU`=亚马逊-澳大利亚站, `AE`=亚马逊-阿联酋站, `BR`=亚马逊-巴西站, `SA`=亚马逊-沙特阿拉伯站
- **搜索值，ASIN码，多个用逗号分隔，最多10个ASIN**: 必填
- **是否取最近 7 天数据，默认 `true`**: 传 `false` 时使用 `startDate`/`endDate` 区间
- **开始日期 `yyyy-MM-dd`**: `last7d=false` 时生效；不填取系统最新周
- **结束日期 `yyyy-MM-dd`**: 与 `startDate` 配套
- **条件筛选,多个条件以英文逗号隔开**: `nf`=自然流量, `sp`=SP广告, `sb`=SB常规, `sbv`=视频广告, `ad`=广告流量, `acAd`=SP推荐, `totalPeriod.in`=新进全部流量词
- **排序字段**: `totalKeywordNum`, `naturalKeywordNum`, `brandKeywordNum`, `vedioKeywordNum`, `acKeywordNum`, `erKeywordNum`, `trKeywordNum`, `sumScore`, `totalNfScore`, `totalSpSocre`（注意拼写）, `totalBrandScore`, `totalVedioScore`, `totalAcScore`, `totalTrScore`, `totalErScore`
- **每页数量，最小10，最大 10000，默认 10000**: 范围 10~10000
- **页码**
- **是否降序，默认传 true **

---

### @SIF-关键词竞品数量

竞争激烈度、市场机会

工具中文名：SIF-关键词竞品数量
功能说明：支持关键词的市场竞争度评估，通过统计竞品数量计算供需比；额外返回推荐位广告/非广告商品数拆分以及 SIF 跟踪的有曝光 ASIN 去重数。

**Prompt 模板：**

> 以关键词"{{yoga mat}}"分析竞争情况和竞品数量

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **国家站点**: `US`=亚马逊-美国站, `UK`=亚马逊-英国站, `DE`=亚马逊-德国站, `CA`=亚马逊-加拿大站, `JP`=亚马逊-日本站, `FR`=亚马逊-法国站, `ES`=亚马逊-西班牙站, `IT`=亚马逊-意大利站, `MX`=亚马逊-墨西哥站, `AU`=亚马逊-澳大利亚站, `AE`=亚马逊-阿联酋站, `BR`=亚马逊-巴西站, `SA`=亚马逊-沙特阿拉伯站
- **关键词，尽量翻译成对应国家站点的语言**: 必填
- **是否取最近 7 天数据，默认 `true`**: 传 `false` 时使用 `startDate`/`endDate` 区间
- **开始日期 `yyyy-MM-dd`**: `last7d=false` 时生效
- **结束日期 `yyyy-MM-dd`**: 与 `startDate` 配套

---
