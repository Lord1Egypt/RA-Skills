# Search Strategies 搜索策略

## 核心原则

1. **双语并行**：同时使用目标地区语言和中文搜索
2. **分层递进**：先官方后民间，由高可信度到低可信度
3. **时效优先**：在搜索词中加入时间限定，按产品类型确定有效期：
   - 数码/科技产品：1 年内 | 家电/消费品：2 年内 | 耐用品/工业品：3 年内 | 默认：2 年
4. **去重择优**：同一信息多个来源时，保留可信度最高的

---

## 搜索词构造公式

### 官方/权威渠道搜索词

```
[产品名/品类] + [地区名] + [官方/Government/Official/Regulatory]
[产品名/品类] + [地区名] + [标准/Standard/认证/Certification]
[产品名/品类] + [地区名] + [行业报告/White Paper/Industry Report]
[产品名/品类] + [地区名] + [价格监管/Price Regulation]
[产品名/品类] + [地区名] + [销量数据/Sales Data/Official Statistics]
```

### 非中文地区搜索词（以英文为例）

```
site:gov [product] [region] price/regulation
site:org [product] [region] market report
[product] [region] official price list
[product] [region] market share statistics
[product] [region] consumer protection
```

### 媒体/行业渠道搜索词

```
[产品名] + [地区] + [测评/评测/Review/Test]
[产品名] + [地区] + [排行榜/Ranking/Top/Best]
[产品名] + [地区] + [市场分析/Market Analysis]
[产品名] + [地区] + [行业媒体/Industry Media]
[产品名] + [品类] + [消费者报告/Consumer Report]
```

### 社区/个人渠道搜索词

```
[产品名] + [使用体验/用户体验/真实评价]
[产品名] + [值得买吗/Worth it/Should I buy]
[产品名] + [Reddit/论坛/贴吧/知乎]
[产品名] + [避坑/踩雷/后悔/差评/Complaints]
[产品名] + [对比] + [竞品名]
```

---

## 地区搜索的常见平台

### 中国大陆
- 官方：政府网站 (gov.cn)、12315、国家标准信息平台
- 电商：京东、天猫、拼多多（价格/销量/评价）
- 媒体：什么值得买、少数派、IT之家、中关村在线
- 社区：知乎、小红书、微博、B 站

### 日本
- 官方：政府機関 (go.jp)、消費者庁、JIS 標準
- 电商：Amazon Japan、楽天市場、ヨドバシ
- 媒体：価格.com、@cosme、家電 Watch
- 社区：知恵袋、Twitter (X)、5ch

### 韩国
- 官方：정부기관 (go.kr)、공정거래위원회
- 电商：Coupang、Naver Shopping、Gmarket
- 媒体：다나와、블로터、IT동아
- 社区：Naver 카페、Clien、뽐뿌

### 美国
- 官方：government sites (.gov)、FTC、CPSC
- 电商：Amazon、Best Buy、Walmart
- 媒体：Wirecutter、Consumer Reports、CNET、The Verge
- 社区：Reddit、YouTube reviews、Trustpilot

### 欧洲
- 官方：EU 官网、各国消费者保护机构
- 电商：Amazon (各国家站点)、MediaMarkt、Fnac
- 媒体：Stiftung Warentest (德国)、Which? (英国)、Que Choisir (法国)
- 社区：Reddit (r/europe)、各国本地论坛

### 东南亚
- 官方：各国政府部门、ASEAN 相关标准
- 电商：Shopee、Lazada、Tokopedia
- 媒体：当地科技/消费类媒体
- 社区：Facebook Groups、本地论坛

### 台湾
- 官方：政府網站 (gov.tw)、消基會、BSMI 標準檢驗
- 电商：PChome、momo 購物網、蝦皮、Yahoo 奇摩購物
- 媒体：Mobile01、比價網 (feebee.com.tw)、電腦王阿達
- 社区：PTT、Dcard、Mobile01 討論區
- 货币：新台币 NT$

### 香港
- 官方：政府網站 (gov.hk)、消費者委員會、香港海關
- 电商：HKTVmall、Price.com.hk、友和 YOHO、Carousell
- 媒体：Price.com.hk 格價、Unwire.hk、ePrice
- 社区：LIHKG 討論區、Baby Kingdom、Uwants
- 货币：港币 HK$

### 澳门
- 官方：政府網站 (gov.mo)、消費者委員會
- 电商：參考香港平台 + 本地小店
- 社区：澳門流動社區、Facebook Groups
- 货币：澳门元 MOP$

---

## 垂直行业平台

不要依赖固定的平台清单——产品千差万别。核心能力是**动态发现**对应品类的垂直平台。

### 平台发现策略

每面对一个新产品品类，执行以下步骤找到最佳数据源：

**1. 电商/交易平台**（获取价格、销量、评价）

搜索词：`[产品名] + 价格/报价/多少钱` + `[地区名]`

根据地区和品类判断优先平台：
- 中国大陆：京东、天猫、淘宝、拼多多（标品）；闲鱼（二手/非标品）
- 日本：Amazon Japan、楽天市場、Yahoo!ショッピング
- 韩国：Coupang、Naver Shopping、Gmarket
- 美国/欧洲：Amazon、eBay、Walmart、Best Buy
- 东南亚：Shopee、Lazada
- 垂直电商：根据品类搜索 `[产品名] + 电商平台` 发现专属平台

**2. 垂直信息/评测平台**（获取专业评测、排行榜）

搜索词：`[产品名] + 评测/排行榜/推荐/Review` + `[地区名]`

从搜索结果中识别以下类型的站点：
- 专业评测机构（如 Consumer Reports、Stiftung Warentest、中关村在线）
- 比价网站（如 価格.com、PCPartPicker）
- 行业垂直媒体（搜索 `[品类] + 行业媒体/门户`）
- 分类信息平台（如 58 同城、Craigslist、Gumtree）

**3. 社区/口碑平台**（获取用户真实评价）

搜索词：`[产品名] + 使用体验/值得买/推荐吗/怎么样` + `[地区名]`

- 通用社区：知乎、Reddit、Quora
- 消费社区：什么值得买、小红书、大众点评
- 垂直论坛：搜索 `[品类] + 论坛/社区` 发现品类专属论坛

**4. 官方/监管平台**（获取标准、政策、注册信息）

搜索词：`site:gov.cn [产品名] + 标准/备案/监管` 或 `[产品名] + [地区] + regulator`

- 中国大陆：NMPA（药品）、3C 认证（电子）、市场监管总局
- 美国：FTC、CPSC、FDA
- 欧盟：CE 认证、ECHA

### 实战示例

| 用户查 | 电商 | 评测 | 社区 | 官方 |
|--------|------|------|------|------|
| 二手车 | 瓜子、58、二手车之家 | 汽车之家、懂车帝 | 汽车之家论坛、小红书 | 商务部以旧换新政策 |
| 净水器 | 京东、天猫、Amazon | 什么值得买、価格.com | 知乎、小红书 | 卫生部饮用水标准 |
| 手机 | 京东、天猫、Amazon | ZOL、GSMArena、DXOMARK | 酷安、Reddit r/Android | 3C 认证、工信部入网 |
| 护肤品 | 天猫国际、考拉、Olive Young | 小红书、@cosme、Paula's Choice | 小红书、Reddit r/SkincareAddiction | NMPA 备案 |
| 药品 | 阿里健康、1药网 | 丁香园、用药助手 | 暂无（药品不依赖社区） | NMPA、FDA |

以上为示例，实际搜索时应根据用户具体产品动态选择平台。

---

## 工具降级策略

当 `web_search` 不可用时，按以下优先级降级：

1. **搜狗搜索 via web_fetch**：`https://www.sogou.com/web?query=关键词`（实测可用，能获取摘要但无法穿透跳转链）
2. **Bing via web_fetch**：`https://cn.bing.com/search?q=关键词`（缓存可能不随查询更新）
3. **垂直平台直连**：直接访问行业平台的搜索页或城市分站
4. **明确告知用户**：如以上均不可用，如实告知信息不足，列出用户可自行访问的链接

---

## 用户辅助渠道

当自动化搜索无法获取足够数据时，切换到用户辅助模式，即请求用户手动提供信息：

### 模式 A：用户提供链接

```
自动化搜索受限，请帮我提供以下平台的搜索结果链接，我来提取和分析：
- {平台1}：搜索「{关键词}」的页面链接
- {平台2}：{产品}在{地区}的列表页链接
只需复制浏览器地址栏 URL 给我即可
```

### 模式 B：用户上传/粘贴数据

```
如果方便，你也可以：
- 截图搜索结果页发给我（我可以通过图片识别提取数据）
- 复制粘贴关键信息（价格列表、评测内容等）
- 上传 PDF/Excel 报告文件
```

### 模式 C：分步引导

对于无法自动抓取的平台（如京东、天猫、小红书等 JS 渲染页面），列出具体步骤指导用户自行获取信息：

```
请帮我在以下平台手动查看：
1. 打开 {平台URL}
2. 搜索"{关键词}"
3. 截图前 5 条结果发给我
或告诉我：价格范围、主流品牌、评分等关键数据
```

### 触发条件

- 连续 2 次搜索策略失败（web_search 宕机 + web_fetch 不可用/无结果）
- 用户查询的平台明确属于 JS 重度渲染站点（京东、天猫、小红书、抖音、淘宝等）
- 主动切换到用户辅助模式，避免反复无效抓取

### 时间限定
- `site:xxx.com after:2024-01-01 [关键词]`
- 在通用搜索中附加年份「2024」「2025」或「最新」
- 时效窗口按品类区分：数码/科技 1 年、家电/消费品 2 年、耐用品/工业品 3 年

### 语言适配
- 中文搜索用简体中文关键词
- 非中文地区先用当地语言搜索，再用中文关键词补搜
- 如果当地语言搜索结果丰富，优先采用

### 信息不足时的变通策略
1. 去掉地区限定，先看品类整体情况
2. 扩大地区范围（城市→省份→国家→区域）
3. 放宽产品范围（型号→子品类→大品类）
4. 尝试关联产品词搜索
5. 减少搜索条件，逐步增加

### 多轮搜索优化
- 第一轮搜索后发现新品牌/术语 → 加入第二轮搜索
- 发现专业评测网站 → 直接在该网站内搜索
- 发现行业报告标题 → 用完整标题精确搜索
