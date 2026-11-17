# 品牌风格蒸馏(brand-styles)

> 把 awesome-design-md 的 58 个品牌 DESIGN.md 蒸馏为技能可用的色板预设(`assets/presets/brand-*.css`)。
> **保真承诺是"风味级":色板+气质+字距层级,不是像素级复刻**——阴影/字重非标值/OpenType 特性按护栏规则取舍。
> 配套:访谈 Q6 品牌推断规则见 `interview-guide.md`;通用预设见 `theme-presets.md`。

## 一、来源与许可

- 源库:`/Users/martin/dev/html2pptx/awesome-design-md/`(若缺失:`git clone https://github.com/VoltAgent/awesome-design-md`)
- 许可:**MIT © VoltAgent 2026**。每个 `brand-*.css` 文件头必须保留"色值来源:VoltAgent/awesome-design-md, MIT"
- 免责:品牌名仅用于描述视觉风格灵感,与品牌方无任何关联/授权关系
- **内置 11 个品牌预设不依赖源库**;按需蒸馏(第六节)才需要源库在场

## 二、映射总表(DESIGN.md 9 节 → 技能目标)

| DESIGN.md 节 | 映射去向 | 处理方式 |
|---|---|---|
| ①视觉主题与氛围 | 品牌档案"风格关键词/适用场景/装饰建议" | 文字吸收,驱动访谈推荐 |
| ②色板与角色 | theme.css 26 变量值 | **核心映射**:品牌主色→`--brand-primary` 组;品牌深色面→`--brand-dark` 组;文字色阶→`--text-*`(rgba 先混合);承载→`--off-white/--card-bg`;边框→`--border-*`;强调→`--accent-orange`;深底文字→`--on-navy-*`(与品牌深底混合);`--signal-*` 默认保留跨预设一致(仅 figma 类多彩品牌允许替换,且须人工审对比度);`--code-*` 全品牌一致。<br>**2026-08-06 P6**:语义名 `--brand-primary`/`--brand-dark` 是正规名;`--lenovo-red`/`--deep-navy` 已降级为别名(向后兼容历史引用)。写新页面用语义名 —— 否则会出现 `--lenovo-red: #0071E3 /* Apple Blue */` 这种名实不符 |
| ③字体规则 | 字体组变量**不动**;层级关系写入档案 | 只吸收:封面负字距值、标题/正文字号比(对照 density-tiers 档,不照搬网页 px)、字重对比策略 |
| ④组件样式 | 片段选用建议 | 丢弃 hover/focus/active 态;提取静态特征(如胶囊徽章→badge-center 片段) |
| ⑤布局原则 | 配方/密度档推荐语 | 如 Apple 大留白→建议演讲档 |
| ⑥深度与阴影 | 按护栏 3 三档策略 | 默认丢弃或近似 |
| ⑦Do's & Don'ts | 档案"风格红线" | 如 Ferrari 禁堆砌、Linear 禁多彩 |
| ⑧响应式 | 全部丢弃 | — |
| ⑨Agent 提示指南 | 参考素材 | 不直接映射,供交叉验证色值 |

## 三、六条护栏(蒸馏时必须逐条执行并在档案留痕)

### 护栏 1 · rgba → 预算混合色
逐通道 `round(前景×α + 底色×(1-α))`;底色取页面实际承载色(浅页 `--off-white`、深页 `--deep-navy`)。
例:Notion `rgba(0,0,0,0.95)` on `#FFFFFF` → `#0D0D0D`;Linear 边框 `rgba(255,255,255,0.05)` on `#08090a` → `#141518`。
⚠️ validate 不查 rgba 文字——此护栏纯靠蒸馏纪律+档案留痕。

### 护栏 2 · 字重吸附
`<450`→400;`450-549` 按角色(强调位→600,正文位→400);`550-649`→600;`≥650` 就近 700/800/900。
吸附损失的层次用**负字距+字号差**补偿(letter-spacing 转换器无损支持),档案注明补偿策略。

### 护栏 3 · 阴影三档策略
①**放弃**(品牌本就"边框优于阴影"时,如 Linear/Notion:用 `--border-light` 细边框表达层次);
②**转换器固定近似**(默认,不干预);
③**两层错位形状模拟**(仅当阴影是品牌风格核心,如 Ferrari/Apple 产品卡:档案给出错位参数)。

### 护栏 4 · 字体替代
字体组三变量(`--font-cn/--font-en/--font-mono`)全品牌统一(Noto Sans SC/Inter/JetBrains Mono;转换映射雅黑/Arial)。
品牌字体名只写入档案"原设计字体"栏作溯源;负字距值吸收进档案与片段示例。

### 护栏 5 · 深色原生品牌双态
每个品牌预设天然双态(浅承载组+深底组同存):品牌有官方 light mode → 浅态用之;
无 → 浅态用中性 `#f7f8f8` 系+品牌文字色阶。档案注明"明暗倾向"(深态原生/浅态原生),供访谈 Q7 联动。

### 护栏 6 · 丢弃清单
响应式断点、交互态、动效、OpenType 特性(cv01/ss03/lnum)、组件 DOM 结构——档案固定一栏"已舍弃",禁止搬运。

## 四、品牌速查表

| 预设(文件) | 风格关键词 | 适用场景 | 明暗倾向 | 一句话取舍 |
|---|---|---|---|---|
| `brand-linear.css` | 深色精密、工程感 | 技术发布/开发者向 | 深态原生 | 510→600,边框替阴影 |
| `brand-apple.css` | 浅色素净、大留白 | 产品发布/高管汇报 | 浅态原生 | 300→400,负字距补偿 |
| `brand-notion.css` | 暖白极简、人文 | 文档型汇报/教育 | 浅态原生 | rgba 混合最多,蓝为唯一强调 |
| `brand-vercel.css` | 纯黑白几何、零装饰 | 极简技术/双态皆宜 | 双态 | 与石墨黑白分工:无金纯对比 |
| `brand-stripe.css` | 企业紫蓝、渐变 | 金融/基础设施 | 浅态原生 | 渐变条走截图,可无损 |
| `brand-figma.css` | 明快多彩、创作 | 设计/创意/教育 | 浅态原生 | 唯一覆盖 signal 组 |
| `brand-airbnb.css` | 珊瑚暖、亲和 | 消费/社区/文旅 | 浅态原生 | 珊瑚≠橙,与暖橙预设错位 |
| `brand-spotify.css` | 深灰鲜绿、律动 | 娱乐/活动/年轻受众 | 深态原生 | 绿只作强调不大面积铺 |
| `brand-ferrari.css` | 黑红编辑、海报感 | 奢侈品/keynote | 深态原生 | 大字+红黑+极简,阴影错位模拟 |
| `brand-claude.css` | 暖米陶土、编辑感 | AI/思想领导力 | 浅态原生 | 陶土 #D97757 系,米白承载 |
| `brand-nvidia.css` | 绿黑能量、硬核 | 硬件/游戏/AI 基建 | 深态原生 | 与 spotify 绿错位:更荧光 |

## 五、品牌蒸馏档案

> 每品牌一页:来源文件、26 变量映射明细、rgba 混合计算、字重吸附记录、层级吸收建议、
> 片段与配方推荐、风格红线、已舍弃项、demo 保真结论。
> (随蒸馏进度逐节补全——见下方各品牌小节。)

<!-- BRANCH-ARCHIVE-START -->

### 档案 · Linear(`brand-linear.css`)

- **来源**:`design-md/linear.app/DESIGN.md`;原设计字体 Inter Variable(Berkeley Mono)
- **明暗倾向**:深态原生(#08090A 画布);浅态用官方 light mode #F7F8F8(护栏 5)
- **关键映射**:主色 Brand Indigo #5E6AD2;深底 Marketing Black;深底文字直接用官方三级文字(#F7F8F8/#D0D6E0/#8A8F98);强调用更亮的 Accent Violet #7170FF(深底上更出彩)
- **rgba 混合**:边框 `rgba(255,255,255,0.05)` on `#08090A` → `#141518`(用于档案,预设中浅态边框走官方 #E6E6E6/#D0D6E0)
- **字重吸附**:招牌 510→600(强调位),590→600,400 保留;略重的层次用**负字距**补偿:封面标题 `letter-spacing:-1.5px`、页标题 `-1.0px`(官方 72px/-1.584px、48px/-1.056px)
- **阴影策略**:①放弃——Linear 本就"边框优于阴影",深底卡用 `--deep-navy-light` 面 + 细边框表达层次
- **片段建议**:gradient-bar(主色→主色深渐变)、badge-center(紫底白字);装饰强度"简洁-适中"
- **风格红线**:禁多彩(强调紫是唯一彩色)、禁大圆角(≤10px)、禁厚边框
- **已舍弃**:cv01/ss03 OpenType、Radix 组件态、510/590 非标字重、rgba 边框原值

### 档案 · Apple(`brand-apple.css`)

- **来源**:`design-md/apple/DESIGN.md`;原设计字体 SF Pro Display/Text
- **明暗倾向**:浅态原生(#F5F5F7 招牌承载);深色段(#000000)仅用于封面/结尾 hero
- **关键映射**:主色 Apple Blue #0071E3(界面唯一彩色);强调 Bright Blue #2997FF(深底专用亮蓝)
- **rgba 混合**:`rgba(0,0,0,0.8)` on `#FFF` → `#333333`(次级文字);`rgba(0,0,0,0.48)` on `#F5F5F7` → `#7F7F80`(三级文字)
- **字重吸附**:300→400(Button Large/Sub-nav);轻盈感损失用**大留白+负字距**补偿:正文 `letter-spacing:-0.37px`、hero 标题 `-0.28px`(官方 17px/-0.374px)
- **阴影策略**:产品卡是 Apple 阴影核心场景时用 ③两层错位(底层卡 `#E5E5EA` 向右下偏移 6px,面层白卡);其余 ①放弃
- **片段建议**:card-accent-top 去顶条(Apple 无强调条习惯);badge-center(蓝底胶囊,radius=半高)
- **风格红线**:禁多彩(蓝是唯一彩色)、禁粗边框、大留白优先于信息密度(建议演讲档)
- **已舍弃**:SF Pro 字族、300 字重、媒体 overlay scrim、动效

### 档案 · Notion(`brand-notion.css`)

- **来源**:`design-md/notion/DESIGN.md`;原设计字体 NotionInter(lnum/locl)
- **明暗倾向**:浅态原生(#F6F5F4 招牌暖白);深色段用官方 Deep Navy #213183
- **关键映射**:主色 Notion Blue #0075DE + 官方按下态 #005BAB 作主色深;强调用官方装饰色 Pink #FF64C8(深底/点缀均出彩)
- **rgba 混合**:`rgba(0,0,0,0.95)` on `#FFF` → `#0D0D0D`(正文);`rgba(0,0,0,0.1)` on `#F6F5F4` → `#DDDCDC`(whisper 边框)
- **字重吸附**:Body Medium 500→400(正文位)/600(导航强调位);标题 700 保留;hero 负字距 `letter-spacing:-2px`(官方 64px/-2.125px,全名单最激进)
- **阴影策略**:①放弃——Notion 层次靠 whisper 边框,不需要阴影
- **片段建议**:badge-center 改胶囊(Notion 徽章全是胶囊);卡片圆角 ≤8px
- **风格红线**:蓝是唯一彩色(Pink 仅限小面积装饰);暖灰文字阶不可换成冷灰
- **已舍弃**:lnum/locl OpenType、500 字重、多层卡片阴影原值、组件态

### 档案 · Vercel(`brand-vercel.css`)

- **来源**:`design-md/vercel/DESIGN.md`;原设计字体 Geist Sans/Mono
- **明暗倾向**:双态皆宜(黑白皆可作主舞台);深态即主色黑 #171717
- **关键映射**:主色 Vercel Black(微暖黑防生硬);强调 Develop Blue #0A72EF(工作流蓝,唯一彩色)
- **字重吸附**:常规;几何感靠**字号差+留白**而非字重
- **阴影策略**:①放弃——零装饰,层次靠 Gray 100 细边框
- **片段建议**:badge-center(黑底白字或蓝底);装饰强度"简洁"
- **风格红线**:禁金/禁多彩(蓝是唯一彩色)、与石墨黑白分工:纯对比无香槟金
- **已舍弃**:Geist 字族、Ship Red/Preview Pink 工作流色(幻灯片场景过于具体)、hsla focus 环

### 档案 · Stripe(`brand-stripe.css`)

- **来源**:`design-md/stripe/DESIGN.md`;原设计字体 sohne(Söhne)
- **明暗倾向**:浅态原生;深色段用官方 Brand Dark #1C1E54
- **关键映射**:主色 Stripe Purple #533AFD + 官方 hover #4434D4 作主色深;强调 Magenta #F96BEE(渐变中段)
- **渐变专长**:`linear-gradient(90deg, #533AFD, #F96BEE)` 紫→品红渐变条走截图还原,可无损——品牌签名视觉
- **字重吸附**:常规;heading 用深蓝黑 #061B31 而非纯黑(官方"不是黑不是灰,是有温度的深蓝")
- **阴影策略**:①放弃——层次靠 #E5EDF5 细边框
- **风格红线**:紫蓝为主,品红仅限渐变/小面积点缀;标题禁纯黑
- **已舍弃**:sohne 字族、多层渐变网格、组件态

### 档案 · Figma(`brand-figma.css`)

- **来源**:`design-md/figma/DESIGN.md`;原设计字体 Manrope
- **明暗倾向**:浅态原生(官方背景即纯白);深色段用纯黑
- **关键映射**:界面严格 #000+#FFF 二元;文字灰阶为推导值(官方未列)
- **signal 组覆盖(唯一例外)**:换成 Figma 官方产品五色 #14AE5C/#FFCD29/#00B3FF/#FF7237/#9747FF(gray 位借给品牌紫)——依据:官方设计系统公开色;DESIGN.md 仅描述"electric greens, bright yellows, deep purples, hot pinks"未给 hex
- **风格红线**:界面黑白 + 彩色**只出现在内容区**(统计带/图示),卡片chrome保持黑白——"白墙画廊挂彩画"
- **阴影策略**:①放弃
- **已舍弃**:Manrope 字族、Glass 玻璃拟态、hero 多彩渐变网格(可用 gradient-bar 多色渐变局部表达)

### 档案 · Airbnb(`brand-airbnb.css`)

- **来源**:`design-md/airbnb/DESIGN.md`;原设计字体 Cereal
- **明暗倾向**:浅态原生;深色段用暖近黑 #222222
- **关键映射**:主色 Rausch #FF385C + 官方按下态 Deep Rausch #E00B41;强调 Legal Blue #428BFF(珊瑚的冷对比)
- **rgba 混合**:无主要混合(官方色多为实色);Border Gray #C1C1C1 直接用
- **字重吸附**:常规;Cereal 圆润感用大圆角(卡片 12-16px、徽章胶囊)补偿
- **阴影策略**:②转换器固定近似(Airbnb 卡片是"阴影+细边"组合,近似可接受)
- **风格红线**:珊瑚≠橙(与暖橙预设错位);圆角要"胖";禁冷硬几何
- **已舍弃**:Cereal 字族、Luxe/Plus 分层色、hover 阴影态

### 档案 · Spotify(`brand-spotify.css`)

- **来源**:`design-md/spotify/DESIGN.md`;原设计字体 Circular Sp
- **明暗倾向**:深态原生(#121212);浅态无官方 light mode → 中性 #F7F8F8 系(护栏 5)
- **关键映射**:主色 Spotify Green #1ED760 + 官方变体 #1DB954 作主色深;深底文字直接用官方色阶(#FFF/#B3B3B3/#7C7C7C)
- **字重吸附**:常规;律动靠**大小数字+色块对比**表达
- **阴影策略**:①放弃(深底层次靠 #121212/#181818/#252525 三层面)
- **风格红线**:绿只作强调,**不大面积铺**;深灰为底、鲜绿点睛
- **已舍弃**:Circular Sp 字族、播放态组件、inset border-shadow 组合

### 档案 · Ferrari(`brand-ferrari.css`)

- **来源**:`design-md/ferrari/DESIGN.md`;原设计字体 Fregat/Italiana
- **明暗倾向**:深态原生(Absolute Black);浅态为纯白编辑面板
- **关键映射**:主色 Rosso Corsa #DA291C + 官方 Dark Red #B01E0A;强调 Modena Yellow #F6E500(**仅限赛车/heritage 语境**,日常用红)
- **字重吸附**:常规;海报感靠**超大字+负字距+红黑对比**:封面标题 100px+、`letter-spacing:-1px`
- **阴影策略**:③hero 产品卡用两层错位(底层 #303030 偏移 8px)营造画框感;其余 ①
- **风格红线**:大字+红黑+极简,禁堆砌装饰;黄色禁滥用
- **已舍弃**:Fregat/Italiana 字族、赛车渐变带、overlay scrim

### 档案 · Claude(`brand-claude.css`)

- **来源**:`design-md/claude/DESIGN.md`;原设计字体 Styrene/Copernicus
- **明暗倾向**:浅态原生(#F5F4ED 招牌羊皮纸);深色段用暖黑 #141413
- **关键映射**:主色 Terracotta #C96442 + 推导深色;强调 Coral #D97757(官方亮变体);深底文字用官方 Warm Silver #B0AEA5
- **字重吸附**:常规;编辑感靠**暖色文字阶+宽松行距**(正文 line-height 1.6-1.7)
- **阴影策略**:①放弃——Border Cream 细边足以分层
- **风格红线**:全暖色系,禁冷色(Focus Blue #3898ec 仅限无障碍场景);陶土不大面积铺,以羊皮纸为底
- **已舍弃**:Styrene/Copernicus 字族、Error Crimson 语义变体、组件态

### 档案 · NVIDIA(`brand-nvidia.css`)

- **来源**:`design-md/nvidia/DESIGN.md`;原设计字体 NVIDIA Sans
- **明暗倾向**:深态原生(True Black);浅态白底
- **关键映射**:主色 NVIDIA Green #76B900 + 推导深色;强调 Green Light #BFF230(荧光青柠,深底上能量感强)
- **官方禁令映射**:绿**不作大面积填充**——用于边框/下划线/CTA 轮廓/强调字;预设中主色只用于 kicker、细条、文字强调
- **字重吸附**:常规;硬核感靠字号对比
- **阴影策略**:①放弃
- **风格红线**:绿不大铺(与 Spotify 绿错位:更荧光、更克制);黑底白字为主
- **已舍弃**:NVIDIA Sans 字族、Purple/Fuchsia 促销色、组件态

<!-- BRANCH-ARCHIVE-END -->

## 六、全量索引与按需蒸馏 SOP

### 58 品牌索引(按源库目录)

- **科技/开发者**:linear.app、vercel、cursor、warp、raycast、supabase、mongodb、hashicorp、clickhouse、sentry、posthog、resend、replicate、together.ai、voltagent、opencode.ai、minimax、clay、composio
- **AI**:claude、cohere、mistral.ai、ollama、x.ai、openai(无)、nvidia
- **设计/创意**:figma、framer、webflow、lovable、runwayml、pinterest、sanity、mintlify
- **消费/生活**:airbnb、spotify、uber、pinterest、cal、superhuman
- **金融/企业**:stripe、coinbase、kraken、revolut、wise、ibm、airtable、intercom、zapier、notion、miro、expo
- **汽车/奢侈**:ferrari、lamborghini、bmw、tesla、renault
- **其他**:apple、spacex、elevenlabs

### 按需蒸馏五步(用户点名任意品牌时)

1. 读源库 `design-md/<品牌>/DESIGN.md`(缺失先 clone;文件缺"色板与角色"节 → 拒绝蒸馏,建议换品牌或自定义 hex)
2. 按第二/三节规则填"品牌蒸馏档案"(第六节模板同第五节)
3. 生成 `brand-<slug>.css` 复制进**项目** `assets/theme.css`(覆盖)
4. `validate` 零 ERROR → `convert` smoke 一页
5. **治理:产物只落项目目录,不回灌技能 presets/**;用户显式要求"加入精选"时才走完整档案+parity+回灌流程
