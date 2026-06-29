---
name: hot-analyzer
description: 抓取多平台热榜，分析舆情对利率债/信用债、申万行业、直接关联标的、期货品种的利好利空影响
agent_created: true
---

# 热点舆情金融市场分析

## 触发条件

用户提到"热点分析""热榜分析""今天热点""舆情分析""热搜对市场影响""hot-analyzer"等时自动激活。

## 数据源

调用以下5个API获取全量热榜数据，每个API独立请求，并行抓取。

```yaml
apis:
  头条:
    url: https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc
    ref: https://www.toutiao.com/
    title_key: Title
    hot_key: HotValue
    data_path: [data]
    total: 50
    weight: 1.0

  百度:
    url: https://top.baidu.com/api/board?tab=realtime
    ref: https://top.baidu.com/
    title_key: query
    hot_key: hotScore
    data_path: [data, cards, 0, content]
    total: 50
    weight: 0.9

  微博:
    url: https://weibo.com/ajax/side/hotSearch
    ref: https://weibo.com/
    title_key: word
    hot_key: num
    data_path: [data, realtime]
    total: 51
    weight: 0.8

  抖音:
    url: https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/
    ref: https://www.douyin.com/
    title_key: word
    hot_key: hot_value
    data_path: [word_list]
    total: 20
    weight: 0.7

  知乎:
    url: https://www.zhihu.com/api/v4/search/preset_words
    ref: https://www.zhihu.com/hot
    title_key: query
    hot_key: weight
    data_path: [preset_words, words]
    total: 30
    weight: 0.6
```

## 综合评分公式

### 基础单项得分

每条条目同时记录排名和热度原始值，混合计算：

```
排名因子   = 1 - 排名/总数
热度因子   = heat / max_heat                    # 用 max 归一化
单项得分   = [0.6 × 排名因子 + 0.4 × 热度因子] × 平台权重
```

- 排名从0开始（API返回的自然序）
- **热度归一化**：`heat / max_heat`（相对于平台榜首热度的比例）。不用 `(heat-min)/(max-min)`——实测发现热榜热度值"高地板"（末位仍有榜首的40%~62%），用min减法会把底部推回0
- α=0.6（排名权重60%、热度权重40%）——保留排名主导地位，同时让热度绝对值放大排名尾部的高热度条目
- 特殊处理：知乎的 `weight` 字段固定为1无区分度 → α=1.0（纯排名），不引入热度因子

### 跨平台合并 + 边际递减

同一事件跨多平台出现时不是简单叠加（实测发现5平台全在的娱乐事件会因平台数过多而线性膨胀到6+分），而是按贡献递减：

```
步骤1：将同组内各平台单项得分从高到低排序
步骤2：综合分 = S₁ + 0.8×S₂ + 0.6×S₃ + 0.3×S₄ + 0.3×S₅
```

- 第1个平台贡献全额，之后每个平台的增量信息递减
- 原理：第1个平台已确认事件热度，第2-3个平台主要验证，第4+平台信息增量接近饱和
- 效果：NBA总决赛5平台→6.64→约4.8（不再过度膨胀）；3平台事件和5平台事件的差距缩小到合理范围

### 财经偏好系数

娱乐内容天然热度高（NBA/世界杯/明星八卦），财经信号容易被淹没。对涉及经济/金融/政策/市场的热点给予适度加权：

```
最终得分 = 综合分 × 财经系数
```

系数由LLM判断，取值：

| 系数 | 适用条件 | 示例 |
|:---:|----------|------|
| **1.3** | 直接影响上市公司/期货/货币政策的事件 | 金价大跌、电商被约谈、《新闻联播》A股数据、韩国紧急会议 |
| **1.2** | 经济角度可解读的地缘/产业事件 | 伊朗封锁海峡（石油供应链）、电动车新国标、芯片制裁 |
| **1.1** | 间接经济影响 | 小麦丰收（农产品价格）、高考结束（消费预期） |
| **1.0** | 纯娱乐/体育/社会/泛事件 | NBA、世界杯、明星八卦 |

- 判断依据：事件是否可影响上市公司股价/期货价格/货币政策预期/产业政策
- 纯LLM推理，不写死规则——像"日本军国主义"这种涉地缘+军事但经济传导路径长的事件，系数1.1而非1.3
- 乘在边际递减后的综合分上（不是单项得分），确保财经加权只影响最终排名

### 独家信号加分

知乎经常出现其他平台完全没有的财经信号（《新闻联播》A股数据、韩国交易所紧急会议、上海副市长被查等），这些信号的独特价值被平台权重0.5结构性惩罚。对出现在≤2个平台的财经热点额外奖励：

```
最终得分 = 综合分 × 财经系数 × 独家系数
```

| 独家系数 | 条件 |
|:------:|------|
| **1.5** | 仅1个平台出现 + 财经系数≥1.2 |
| **1.3** | 仅2个平台出现 + 财经系数≥1.2 |
| **1.0** | 3+平台 或 财经系数<1.2 |

- 生效前提：财经系数≥1.2（确保财经偏好判断已在先），纯娱乐/体育不享受独家加分
- 效果：《新闻联播》A股数据（知乎独占） 0.33×1.3×1.5=0.65，从~30名外跃入~TOP15
- 韩国交易所紧急会议 0.08×1.3×1.5=0.16，仅小幅提升（排名太靠后）
- 跨3平台的钉钉换帅不受影响（3平台=1.0），其突破主要靠财经系数1.3

## 去重合并规则

1. **精确匹配**（Python脚本）：标题字符串完全相同 → 直接合并
2. **包含匹配**（Python脚本）：一个标题包含另一个 → 直接合并取最长
3. **LLM语义合并**（关键步骤）：
   - 将精确匹配后剩余的标题列表传给大模型
   - 按「核心事件相同」分组（同主体+同动作+同时间窗口）
   - 每组选信息量最大的标题为代表
   - **禁止用纯字符串相似度算法（SequenceMatcher等）替代LLM**
   - 实际测试发现：字符串算法导致伊朗8条热点分散、黄金3条未合并，严重影响排序
4. 合并后综合分为各平台得分之和
5. 记录出现平台数、各平台原始排名、合并成员数

## 申万一级行业（31个）

以下行业分类写死用于分析。每轮分析时，将合并后的热榜词条逐条对照各行业的keywords进行匹配，输出受影响的行业及方向。

```yaml
申万行业:
  大消费:
    农林牧渔:
      code: "801010"
      keywords: [粮食安全, 猪肉, 猪周期, 种业, 转基因, 水产, 养殖, 渔业, 农产品涨价, 饲料, 糖, 棉花进口]
    食品饮料:
      code: "801120"
      keywords: [白酒, 茅台, 预制菜, 消费复苏, 餐饮, 乳业, 调味品, 零食, 饮料, 啤酒, 食品安全, 涨价]
    家用电器:
      code: "801110"
      keywords: [家电补贴, 以旧换新, 出口关税, 空调, 冰箱, 洗衣机, 扫地机, 智能家居]
    纺织服饰:
      code: "801130"
      keywords: [服装出口, 新疆棉, 运动品牌, 羽绒服, 纺织, 关税, 汇率]
    轻工制造:
      code: "801140"
      keywords: [造纸, 包装, 出口, 家具, 文具, 跨境电商, 汇率]
    医药生物:
      code: "801150"
      keywords: [集采, 创新药, 疫苗, 疫情, 医保, 医疗器械, CXO, 中药, 减肥药, 流感, 药监局]
    商贸零售:
      code: "801200"
      keywords: [电商, 免税, 消费券, 直播带货, 百货, 超市, 双11, 618]
    社会服务:
      code: "801210"
      keywords: [旅游, 酒店, 景区, 教育, 教培, 出境游, 免税, 演唱会, 节假日]
    美容护理:
      code: "801880"
      keywords: [医美, 化妆品, 护肤品, 监管, 双11, 618]

  大科技:
    电子:
      code: "801080"
      keywords: [芯片, 半导体, 光刻机, 消费电子, 手机, 华为, 苹果, 面板, 存储, AI芯片, 先进封装, 台积电, 美国制裁]
    计算机:
      code: "801750"
      keywords: [AI, 人工智能, 信创, 数据要素, 大模型, ChatGPT, 软件, 云计算, 网络安全, 数字政府, 国产替代]
    传媒:
      code: "801760"
      keywords: [游戏版号, 短剧, 电影, 票房, 直播, 短视频, 互联网平台, 反垄断, 广告]
    通信:
      code: "801770"
      keywords: [5G, 6G, 光模块, 卫星互联网, 光纤, 运营商, 数据センター, 通信设备]

  大金融:
    银行:
      code: "801780"
      keywords: [降息, 降准, 房贷利率, LPR, 存款利率, 银行利润, 不良贷款, 城投, 地方债]
    非银金融:
      code: "801790"
      keywords: [券商合并, 保险, 资本市场, 印花税, IPO, 再融资, 减持, 证监会, 牛市, 成交量]

  大周期:
    煤炭:
      code: "801020"
      keywords: [煤价, 限产, 能源安全, 煤矿事故, 冬季供暖, 发电, 进口煤]
    石油石化:
      code: "801030"
      keywords: [油价, 中东, 伊朗, 沙特, OPEC, 俄罗斯, 炼化, 成品油, 加油站, 地缘冲突, 霍尔木兹海峡]
    基础化工:
      code: "801040"
      keywords: [化工涨价, 新材料, 化肥, 农药, 染料, 钛白粉, 氟化工, 磷化工]
    钢铁:
      code: "801050"
      keywords: [粗钢, 限产, 基建, 房地产, 螺纹钢, 铁矿石, 钢厂, 产能过剩]
    有色金属:
      code: "801060"
      keywords: [铜, 铝, 稀土, 锂, 钴, 镍, 黄金, 白银, 矿产, 资源税, 新能源金属, 碳酸锂]
    建筑材料:
      code: "801710"
      keywords: [水泥, 玻璃, 防水, 涂料, 地产链, 基建, 保障房, 城中村改造]
    建筑装饰:
      code: "801720"
      keywords: [基建, 一带一路, 城中村改造, 专项债, 工程, 铁公基, 水利, 城市更新]
    电力设备:
      code: "801730"
      keywords: [光伏, 风电, 储能, 特高压, 电网, 新能源, 电力改革, 硅料, 逆变器, 充电桩]
    机械设备:
      code: "801890"
      keywords: [机器人, 人形机器人, 工业母机, 工程机械, 挖掘机, 自动化, 减速器, 伺服电机]
    国防军工:
      code: "801740"
      keywords: [地缘冲突, 军演, 导弹, 航母, 战斗机, 军工, 南海, 台海, 武器出口, 冲突升级, 国防预算]
    汽车:
      code: "801880"
      keywords: [新能源车, 出口, 关税, 自动驾驶, 比亚迪, 特斯拉, 充电桩, 补贴, 车展]
    公用事业:
      code: "801160"
      keywords: [电价, 水务, 天然气, 供暖, 环保税, 碳排放]
    交通运输:
      code: "801170"
      keywords: [集运, 运费, 物流, 快递, 港口, 铁路, 航空, 红海, 苏伊士, 海运]
    环保:
      code: "801250"
      keywords: [碳交易, 碳中和, 环保政策, 污染, 固废, 污水, 生态修复]
    房地产:
      code: "801180"
      keywords: [限购, 放松, 房贷, 保交楼, 白名单, 开发商, 救市, 房价, 土地出让, 取消限购]
    综合:
      code: "801230"
      keywords: []
```

## 期货品种映射表

```yaml
期货品种:
  上海期货交易所_SHFE:
    黄金_AU:
      category: 贵金属
      keywords: [地缘冲突, 战争, 伊朗, 中东, 避险, 美联储, 降息, 通胀, 美元, 央行购金, 金价, 危机]
      direction: 利好
    白银_AG:
      category: 贵金属
      keywords: [避险, 工业需求, 光伏用银, 通胀, 美元]
      direction: 利好
    铜_CU:
      category: 有色金属
      keywords: [铜价, 基建, 电网投资, 新能源, 供应中断, 铜矿罢工, 经济复苏]
      direction: 利好
    铝_AL:
      category: 有色金属
      keywords: [铝价, 限产, 电解铝, 房地产, 汽车, 云南限电, 出口]
      direction: 利好
    锌_ZN:
      category: 有色金属
      keywords: [锌价, 基建, 镀锌, 汽车, 供应]
      direction: 利好
    铅_PB:
      category: 有色金属
      keywords: [铅价, 蓄电池, 环保限产]
      direction: 中性
    镍_NI:
      category: 有色金属
      keywords: [镍价, 新能源电池, 不锈钢, 印尼出口禁令]
      direction: 利好
    锡_SN:
      category: 有色金属
      keywords: [锡价, 半导体, 焊料, 供应]
      direction: 利好
    螺纹钢_RB:
      category: 黑色金属
      keywords: [基建, 房地产, 稳增长, 城中村改造, 专项债, 钢材, 地产政策]
      direction: 利好
    热轧卷板_HC:
      category: 黑色金属
      keywords: [汽车, 家电, 制造业, 出口, 钢材]
      direction: 利好
    不锈钢_SS:
      category: 黑色金属
      keywords: [镍价, 家电, 建筑, 出口]
      direction: 中性
    天然橡胶_RU:
      category: 能源化工
      keywords: [橡胶, 轮胎, 汽车, 东南亚天气, 合成胶]
      direction: 利好
    合成橡胶_BR:
      category: 能源化工
      keywords: [丁二烯, 轮胎, 汽车, 原油]
      direction: 中性
    燃料油_FU:
      category: 能源化工
      keywords: [原油, 航运, 中东, 炼厂]
      direction: 跟随原油
    石油沥青_BU:
      category: 能源化工
      keywords: [基建, 公路, 原油, 专项债]
      direction: 利好
    纸浆_SP:
      category: 能源化工
      keywords: [纸浆, 造纸, 进口, 汇率, 环保]
      direction: 中性
    氧化铝_AO:
      category: 有色金属
      keywords: [铝土矿, 几内亚, 铝, 限产]
      direction: 利好

  上海国际能源交易中心_INE:
    原油_SC:
      category: 能源
      keywords: [中东, 伊朗, 霍尔木兹海峡, OPEC, 减产, 地缘, 供应中断, 红海, 石油, 沙特, 俄罗斯, 油价]
      direction: 利好
    低硫燃料油_LU:
      category: 能源
      keywords: [航运, 限硫令, 船用油, 原油]
      direction: 跟随原油
    20号胶_NR:
      category: 能源化工
      keywords: [轮胎, 汽车, 东南亚, 橡胶]
      direction: 中性
    国际铜_BC:
      category: 有色金属
      keywords: [铜价, 全球经济, 美元, LME]
      direction: 利好
    集运指数_EC:
      category: 航运
      keywords: [红海, 苏伊士, 运费, 集装箱, 航运, 供应链, 绕航, 中东]
      direction: 利好

  大连商品交易所_DCE:
    黄大豆1号_A:
      category: 农产品
      keywords: [大豆, 中美, 关税, 种植面积, 天气, 巴西, 阿根廷, USDA]
      direction: 利好
    豆粕_M:
      category: 农产品
      keywords: [大豆, 关税, 饲料, 养殖, 生猪, 中美贸易, 巴西]
      direction: 利好
    豆油_Y:
      category: 农产品
      keywords: [食用油, 生物柴油, 大豆, 棕榈油]
      direction: 利好
    棕榈油_P:
      category: 农产品
      keywords: [食用油, 印尼, 马来西亚, 生物柴油, 出口禁令]
      direction: 利好
    玉米_C:
      category: 农产品
      keywords: [玉米, 饲料, 深加工, 进口, 关税, 天气, 种植面积]
      direction: 中性
    玉米淀粉_CS:
      category: 农产品
      keywords: [玉米, 淀粉, 深加工]
      direction: 中性
    鸡蛋_JD:
      category: 农产品
      keywords: [鸡蛋, 禽流感, 饲料成本, 节假日]
      direction: 中性
    生猪_LH:
      category: 农产品
      keywords: [猪肉, 猪周期, 猪价, 存栏, 养殖, 猪瘟]
      direction: 中性
    粳米_RR:
      category: 农产品
      keywords: [稻米, 粮食安全, 储备]
      direction: 中性
    铁矿石_I:
      category: 黑色金属
      keywords: [钢厂, 限产, 粗钢, 房地产, 基建, 澳洲, 巴西, 供应]
      direction: 利空
    焦炭_J:
      category: 黑色金属
      keywords: [钢厂, 限产, 煤炭, 环保, 焦化]
      direction: 利空
    焦煤_JM:
      category: 黑色金属
      keywords: [煤炭, 煤矿, 安全, 进口, 蒙古, 澳洲煤]
      direction: 利好
    聚乙烯_L:
      category: 能源化工
      keywords: [塑料, 原油, 包装, 农业膜]
      direction: 跟随原油
    聚氯乙烯_V:
      category: 能源化工
      keywords: [PVC, 房地产, 管材, 基建]
      direction: 利好
    聚丙烯_PP:
      category: 能源化工
      keywords: [塑料, 原油, 汽车, 家电, 口罩]
      direction: 跟随原油
    苯乙烯_EB:
      category: 能源化工
      keywords: [苯, 原油, 家电, 汽车, EPS]
      direction: 跟随原油
    乙二醇_EG:
      category: 能源化工
      keywords: [聚酯, 纺织, 原油, 煤化工]
      direction: 跟随原油
    液化石油气_PG:
      category: 能源化工
      keywords: [LPG, 原油, 取暖, 化工]
      direction: 跟随原油
    纤维板_FB:
      category: 建材
      keywords: [木材, 家具, 房地产]
      direction: 中性

  郑州商品交易所_ZCE:
    白糖_SR:
      category: 农产品
      keywords: [白糖, 甘蔗, 印度, 巴西, 乙醇, 天气, 糖价]
      direction: 利好
    棉花_CF:
      category: 农产品
      keywords: [棉花, 新疆, 纺织, 出口, 关税, 种植面积, 天气]
      direction: 利好
    棉纱_CY:
      category: 农产品
      keywords: [纺织, 出口, 棉花, 关税]
      direction: 中性
    苹果_AP:
      category: 农产品
      keywords: [苹果, 天气, 产区, 水果]
      direction: 中性
    红枣_CJ:
      category: 农产品
      keywords: [红枣, 新疆, 天气]
      direction: 中性
    花生_PK:
      category: 农产品
      keywords: [花生, 食用油, 种植面积]
      direction: 中性
    菜油_OI:
      category: 农产品
      keywords: [菜籽, 食用油, 加拿大, 进口, 关税]
      direction: 利好
    菜粕_RM:
      category: 农产品
      keywords: [菜籽, 饲料, 水产, 加拿大, 关税]
      direction: 利好
    PTA_TA:
      category: 能源化工
      keywords: [聚酯, 纺织, 原油, PX, 出口]
      direction: 跟随原油
    甲醇_MA:
      category: 能源化工
      keywords: [甲醇, 煤化工, 原油, MTO, 进口]
      direction: 跟随原油
    纯碱_SA:
      category: 能源化工
      keywords: [纯碱, 玻璃, 光伏玻璃, 房地产, 限产]
      direction: 利好
    玻璃_FG:
      category: 建材
      keywords: [玻璃, 房地产, 光伏, 竣工, 保交楼, 城中村改造]
      direction: 利好
    尿素_UR:
      category: 能源化工
      keywords: [化肥, 农业, 出口, 煤炭, 印度招标]
      direction: 中性
    烧碱_SH:
      category: 能源化工
      keywords: [烧碱, 氧化铝, 化工, 出口]
      direction: 中性
    硅铁_SF:
      category: 黑色金属
      keywords: [硅铁, 钢厂, 限产, 电力]
      direction: 中性
    锰硅_SM:
      category: 黑色金属
      keywords: [锰硅, 钢厂, 限产, 锰矿]
      direction: 中性
    动力煤_ZC:
      category: 能源
      keywords: [煤炭, 发电, 限价, 能源安全, 冬季供暖]
      direction: 利好
    短纤_PF:
      category: 能源化工
      keywords: [涤纶, 纺织, 原油, 出口]
      direction: 跟随原油
    原木_LG:
      category: 建材
      keywords: [木材, 进口, 房地产, 建筑]
      direction: 中性

  中国金融期货交易所_CFFEX:
    沪深300_IF:
      category: 股指
      keywords: [A股, 牛市, 降息, 降准, 经济复苏, 外资流入, 政策利好, 证监会]
      direction: 利好
    上证50_IH:
      category: 股指
      keywords: [大盘, 蓝筹, 降息, 银行, 保险, 茅台]
      direction: 利好
    中证500_IC:
      category: 股指
      keywords: [中小盘, 题材, 量化, 成长]
      direction: 利好
    中证1000_IM:
      category: 股指
      keywords: [小盘, 题材, 微盘, 量化]
      direction: 中性
    2年期国债_TS:
      category: 利率
      keywords: [降息, 降准, 流动性, 货币政策, 央行, MLF, LPR]
      direction: 利好
    5年期国债_TF:
      category: 利率
      keywords: [降息, 降准, 经济数据, 通胀, PMI, GDP]
      direction: 利好
    10年期国债_T:
      category: 利率
      keywords: [降息, 降准, 财政刺激, 加息, 通胀, 美联储, 国债收益率]
      direction: 利好

  广州期货交易所_GFEX:
    工业硅_SI:
      category: 新能源
      keywords: [光伏, 多晶硅, 有机硅, 限电, 云南, 四川, 出口]
      direction: 利好
    碳酸锂_LC:
      category: 新能源
      keywords: [锂电池, 新能源车, 宁德时代, 比亚迪, 盐湖, 锂矿, 澳大利亚, 智利]
      direction: 利好
    多晶硅:
      category: 新能源
      keywords: [光伏, 硅料, 硅片, 产能过剩]
      direction: 中性
```

## 工作流（Python + LLM 二段式）

**核心原则**：所有确定性公式（解析、去重、计分、排序、HTML生成）由 `compute.py` 处理，LLM 只做三件事——**语义分组、系数判断、市场推理**。

配套脚本：`compute.py`（与本 SKILL.md 同目录）

> **⚠️ 运行前必须先将 compute.py 复制到工作目录**：
> ```bash
> cp <skill_dir>/compute.py {cwd}/compute.py   # Windows: copy <skill_dir>\compute.py {cwd}\compute.py
> ```
> `<skill_dir>` 是本 SKILL.md 所在目录。各平台安装路径不同：WorkBuddy 上为 `~/.workbuddy/skills/hot-analyzer/`，其他平台按实际安装路径替换。以下所有命令均从 `{cwd}` 执行 compute.py。

---

### 第一步：并行抓取数据（全 Python urllib）

> **⚠️ 全部 5 个平台都用 Python `urllib` 抓取，不用 WebFetch。**
> WebFetch 处理纯 JSON API 返回不稳定（百度/抖音/知乎均失败过），Python urllib 一次成功。

```python
import urllib.request, json, os

os.chdir("{cwd}")  # 切换到工作目录，各平台自动替换
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'

# 1. 头条
req = urllib.request.Request('https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc',
    headers={'User-Agent': UA, 'Referer': 'https://www.toutiao.com/'})
with urllib.request.urlopen(req, timeout=15) as r:
    with open('raw_toutiao.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(r.read()), f, ensure_ascii=False)

# 2. 百度
req = urllib.request.Request('https://top.baidu.com/api/board?tab=realtime',
    headers={'User-Agent': UA, 'Referer': 'https://top.baidu.com/'})
with urllib.request.urlopen(req, timeout=15) as r:
    with open('raw_baidu.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(r.read()), f, ensure_ascii=False)

# 3. 微博
req = urllib.request.Request('https://weibo.com/ajax/side/hotSearch',
    headers={'User-Agent': UA, 'Referer': 'https://weibo.com/'})
with urllib.request.urlopen(req, timeout=15) as r:
    with open('raw_weibo.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(r.read()), f, ensure_ascii=False)

# 4. 抖音
req = urllib.request.Request('https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/',
    headers={'User-Agent': UA, 'Referer': 'https://www.douyin.com/'})
with urllib.request.urlopen(req, timeout=15) as r:
    with open('raw_douyin.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(r.read()), f, ensure_ascii=False)

# 5. 知乎
req = urllib.request.Request('https://www.zhihu.com/api/v4/search/preset_words',
    headers={'User-Agent': UA, 'Referer': 'https://www.zhihu.com/hot'})
with urllib.request.urlopen(req, timeout=15) as r:
    with open('raw_zhihu.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(r.read()), f, ensure_ascii=False)

print("5个平台数据全部保存完成")
```

**注意**：微博API返回中混有广告条目（`is_ad=1`），Py脚本自动过滤。将以上代码写入 `{cwd}/fetch_all.py`，然后用 `python` 执行。

---

### 第二步：Python 精确去重 + 单项计分

运行 `compute.py prepare`：

```bash
python {cwd}/compute.py prepare \
  --state {cwd}/state.json \
  --toutiao {cwd}/raw_toutiao.json \
  --baidu {cwd}/raw_baidu.json \
  --weibo {cwd}/raw_weibo.json \
  --douyin {cwd}/raw_douyin.json \
  --zhihu {cwd}/raw_zhihu.json
```

脚本自动完成：
- 解析5个API的JSON，提取标题/排名/热度
- 精确匹配 + 包含匹配去重（标题完全相同或包含关系）
- 计算每条条目的单项得分：`[0.6×排名因子 + 0.4×热度因子] × 平台权重`（知乎 α=1.0 纯排名）
- 输出「已自动合并的精确匹配组」和「待LLM语义合并列表」
- 状态保存到 `state.json`，待合并列表额外写入 `pending.json`（UTF-8 JSON，**无Windows终端乱码问题**）


**⚠️ 重要 — 读取 prepare 输出的方式**：

终端/控制台输出可能因编码问题导致中文乱码（如 Windows PowerShell 的 GBK 编码）。建议直接读取文件：
1. 读取 `{cwd}/pending.json`
2. 从中获取 `items` 数组（待语义合并条目）和 `multi_member_groups`（已自动合并的组）

`pending.json` 格式：
```json
{
  "total": 130,
  "items": [
    {"index": 0, "title": "伊朗关闭霍尔木兹海峡", "platform": "zhihu", "rank": 27, "score": 0.06},
    ...
  ],
  "multi_member_groups": [
    {"representative": "全长标题", "members": ["短标题1","短标题2"], "platforms": ["baidu","toutiao"]},
    ...
  ]
}
```



---

### 第三步：LLM 语义合并 + 系数判断

读取 **`{cwd}/pending.json`**（`compute.py prepare` 生成的UTF-8 JSON文件，**不是控制台输出**），获取 `items`（待语义合并列表）和 `multi_member_groups`（已自动合并的组）。完成两个任务：

**任务A — 语义合并分组：**

按「核心事件相同」分组（同主体 + 同动作 + 同时间窗口）。示例：
- ✅ 「伊朗关闭霍尔木兹海峡」「伊朗宣布封锁海峡」「伊朗局势」→ 合并
- ✅ 「黄金一直跌」「黄金别跌了」「黄金进入熊市」→ 合并
- ✅ 「钉钉换帅」「陈航卸任CEO」「陈宇森接棒」→ 合并
- ❌ 「黄金一直跌」和「金饰克价下跌400元」→ 有重叠但不强制合并，LLM自主判断
- **禁止用 SequenceMatcher/Levenshtein 等纯字符串算法替代LLM**

每组选信息量最大的标题为代表（优先头条/百度来源）。

**任务B — 财经系数 + 独家系数判断：**

对每个分组，判断：

| 系数 | 值 | 适用条件 |
|------|:--:|----------|
| 财经系数 | **1.3** | 直接影响上市公司/期货/货币政策 |
| 财经系数 | **1.2** | 经济角度可解读的地缘/产业事件 |
| 财经系数 | **1.1** | 间接经济影响 |
| 财经系数 | **1.0** | 纯娱乐/体育/社会 |
| 独家系数 | **1.5** | 仅1平台 + 财经系数≥1.2 |
| 独家系数 | **1.3** | 仅2平台 + 财经系数≥1.2 |
| 独家系数 | **1.0** | 3+平台 或 财经系数<1.2 |

**输出格式**（保存为 `{cwd}/groups.json`）：

```json
[
  {
    "representative": "伊朗全面关闭霍尔木兹海峡",
    "members": ["伊朗关闭霍尔木兹海峡", "伊朗宣布封锁海峡", "伊朗局势"],
    "finance_coeff": 1.2,
    "exclusive_coeff": 1.0
  },
  {
    "representative": "电商平台被约谈",
    "members": ["淘宝京东拼多多抖音小红书被约谈"],
    "finance_coeff": 1.3,
    "exclusive_coeff": 1.5
  }
]
```

> **注意**：`members` 必须是 prepare 输出列表中的**精确标题名**，否则 compute.py 无法匹配。
>
> **⚠️ 文件写入方式**：`groups.json` 内容较大时直接写入文件可能截断。优先用 Python 脚本写入：
> ```bash
> python -c "import json; json.dump(groups, open('groups.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)"
> ```
>
> **⚠️ 去重检查**：写入 `groups.json` 前检查是否有重复 `representative`，LLM 语义合并可能产生同组重复。
>
> **⚠️ Unicode 转义谨防写错**：书名号「《》」的 Unicode 是 `\u300a`（左）和 `\u300b`（右），中文双引号「""」是 `\u201c`（左）和 `\u201d`（右）。写成JSON时推荐直接使用 `"members": ["《新闻联播》披露A股重要数据"]`（UTF-8原文），不要用Unicode转义形式，避免开/闭符号打错。

---

### 第四步：Python 计算最终排名 + 生成 HTML

```bash
# 计算最终排名
python {cwd}/compute.py compute \
  --state {cwd}/state.json \
  --groups {cwd}/groups.json

# 生成 HTML 可视化
python {cwd}/compute.py html \
  --state {cwd}/state.json \
  --output {cwd}/hot_analysis_report.html
```

脚本自动完成：
- 应用LLM分组合并，计算边际递减综合分：`S₁ + 0.8×S₂ + 0.6×S₃ + 0.3×S₄₊`
- 乘以财经系数 + 独家系数 → 最终得分
- 按最终得分排序 → TOP 30
- 生成暗色主题HTML报告（汇总指标卡片 + TOP 30 得分柱状图）

**预览 HTML**：

使用各平台支持的文件预览方式打开 `{cwd}/hot_analysis_report.html`。

---

### 第五步：LLM 市场分析

读取 `compute.py compute` 输出的 TOP 30 结果，逐条分析四个维度：

**① 利率债方向**：判断10Y国债收益率方向 + 2-3句逻辑
**② 信用债方向**：判断信用利差方向 + 2-3句逻辑
**③ 申万行业影响**：扫描TOP 30匹配上方31个行业keywords，输出利好/利空行业表格
**④ 直接关联标的**：精确定位上市公司（A股/港股/美股），不能映射的跳过
**⑤ 期货品种影响**：匹配上方期货映射表 + LLM补充，输出含置信度表格

### 第五步 B：将 LLM 分析注入 HTML

`compute.py html` 生成的 HTML 只有框架（TOP 30 排名表 + 汇总卡片），第二部分显示占位文字「此部分需 LLM 市场分析后补充」。需要将占位块替换为完整的分析内容（利率债/行业/标的/期货/关键信号），填入对应的 HTML 表格和卡片中。

> 占位块匹配字符串：`<p>此部分需 LLM 市场分析后补充</p>`

---

### 第六步：输出 Markdown 报告

```markdown
## 📊 综合热点舆情分析报告
**时间：YYYY-MM-DD HH:MM**

---

### 一、综合热点榜 TOP 30

| 排名 | 热点标题 | 平台数 | 最终得分 | 来源平台 |
|------|---------|:------:|:------:|----------|
| 1 | ... | 4 | 2.48 | 头条#2, 百度#6, 微博#8 |

---

### 二、利率债/信用债方向
（第五步的①②分析结果）

### 三、申万行业影响
（第五步的③分析结果）

### 四、直接关联标的
（第五步的④分析结果）

### 五、期货品种影响
（第五步的⑤分析结果）
```

---

### 输出要求
- 语气客观、简洁，每条逻辑不超过2句话
- 置信度：多平台+多关键词命中=高；单平台=中；间接推断=低
- 不输出"无法判断"条目，不确定的不列
- 债券部分专注方向性判断，不给具体点位
- `compute.py` 已生成 HTML，预览后 Markdown 报告中也提及 HTML 已就绪
