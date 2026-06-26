---
name: macro-information
description: |
  宏观资讯技能。基于全网信息查询国内外宏观经济相关新闻资讯，  支持情感分析（正面/负面/中性）、事件标签分类、热度分析和时间范围筛选。
  
  使用场景：用户询问宏观经济形势、政策影响、经济数据（GDP/CPI/利率等）、央行政策（美联储/人民银行）、国际贸易、金融市场动态、通胀通缩、经济事件影响等话题时调用。
  
  触发示例："最近有什么宏观经济新闻"、"查询美联储政策动态"、"国内 GDP 相关资讯"、"近期负面经济舆情"、"中美贸易最新动态"、"通胀相关报道"、"经济形势分析"等。
  
  支持按国内宏观/国际宏观筛选，按情感倾向过滤，返回热度得分、事件标签、涉及地区等分析数据。
---

# 宏观经济资讯 (Macro Information)

面向金融等场景，为金融投资、政策研究、舆情分析等领域用户，提供全面的宏观经济数据查询能力。

## ⚠️ 前置条件：配置 API Key

**使用本技能前，必须先配置 API Key。**

### 检查配置

查看 `.env` 文件是否存在且包含有效的 API Key：

```bash
cat .env
```

### 如果未配置

返回以下错误提示：

> **GE1003**: 未配置 API Key，请前往https://www.feedax.cn免费申请，完成后请告诉我API Key以便我记住

在 `.env` 文件中添加：

```env
FEEDAX\_SEARCH\_API\_KEY=your\_api\_key\_here
```

> **注意**: 如果 `.env` 文件不存在，请创建该文件并添加上述内容。API Key 请联系管理员获取。

### API Key 错误码说明

|错误码|说明|解决方案|
|-|-|-|
|GE1003|未配置API Key|前往https://www.feedax.cn免费申请|
|GE1004|API Key已失效|检查API Key有效性，或重新申请|
|GE1005|API Key已过期|前往https://www.feedax.cn重新申请|
|GE1006|API Key无效|前往https://www.feedax.cn重新申请|
|GE1007|账户余额不足|前往https://www.feedax.cn充值|

### 服务错误处理

当 API 服务暂时不可用时，系统会返回友好的错误提示：

|HTTP 状态码|错误提示|
|-|-|
|400|请求参数错误，请检查输入|
|401/403|API Key 可能无效或已过期|
|429|请求过于频繁，请稍后再试|
|500|服务器内部错误|
|502|服务暂时不可用，请稍后再试|
|503|服务维护中，请稍后再试|
|504|网关超时，请稍后再试|
|连接超时|请求超时，请稍后再试|
|连接错误|无法连接到服务器，请检查网络或稍后再试|

---

## 一、接口信息

* **接口地址**: `221.6.15.90:18011`
* **接口 URI**: `/data-service/v1/news/macro/external/query`
* **请求方式**: `POST`
* **Content-Type**: `application/json; charset=UTF-8`

---

## 二、参数说明

### 2.1 必传参数

|参数名|类型|说明|
|-|-|-|
|`apiKey`|String|平台分配的密钥，身份校验必传|
|`keyWordQuery`|Object|关键词查询对象|

**keyWordQuery 结构**:

```json
{
    "keyword": "搜索关键词",
    "queryFields": ["1", "2"]
}
```

* `queryFields`: `["1", "2"]` - 1=正文，2=标题

### 2.2 分页与排序

|参数名|类型|默认值|说明|
|-|-|-|-|
|`pageNum`|Integer|0|页码（从 0 开始）|
|`pageSize`|Integer|20|每页数量，1 ≤ size ≤ 100|
|`sortBy`|String|`publish_date`|**默认按发布时间排序**。仅当用户明确要求按热度排序时才修改|
|`sortType`|String|`DESC`|排序方式：ASC/DESC|

**sortBy 可选值**:

* `publish_date` - **默认**。按发布时间排序，获取最新内容
* `heat_scores` - 按热度排序

**排序规则**：

* **默认行为**：按 `publish_date`（发布时间）排序，获取最新发布的舆情
* **用户明确要求时**：当用户说"按热度排序"、"最热门的"等，才使用 `heat_scores`

### 2.3 内容筛选

|参数名|类型|默认值|说明|
|-|-|-|-|
|`macroEconomyResul`|Array|`[]`|宏观类型列表：国内宏观/国际宏观|
|`sentiments`|Array|`[]`|情感倾向列表：正面/负面/中性，空数组表示全部|
|`macroTags`|Array|`[]`|宏观事件标签列表，空数组表示全部|
|`mediaTypes`|Array|`[]`|信源类型列表，空数组表示全部|
|`newsImportanceLevels`|Array|`[]`|重要程度列表，空数组表示全部|

### 2.4 时间筛选

|参数名|类型|默认值|说明|
|-|-|-|-|
|`startTime`|Long|自动计算|查询开始时间（13 位毫秒时间戳）|
|`endTime`|Long|当前时间|查询结束时间（13 位毫秒时间戳）|

### 2.5 互动数据筛选

|参数名|类型|说明|
|-|-|-|
|`heatScores`|Integer|热度得分|
|`viewNum`|Integer|浏览数|
|`forwardedNum`|Integer|转发数|

---

## 三、宏观类型分类

### 宏观类型 (macroEconomyResul)

|类型|说明|
|-|-|
|**国内宏观**|中国宏观经济相关政策、数据、事件|
|**国际宏观**|全球宏观经济、主要央行政策、国际经济事件|

---

## 四、情感倾向分类 (sentiments)

|情感|值|说明|
|-|-|-|
|正面|`正面`|积极、利好的经济新闻|
|负面|`负面`|消极、风险警示的经济新闻|
|中性|`中性`|客观陈述的经济新闻|

---

## 五、宏观事件标签 (macroTags)

### 常见事件标签

* **货币政策**: 降准、降息、加息、缩表、扩表
* **财政政策**: 财政刺激、基建投资、减税降费
* **经济数据**: GDP、CPI、PPI、PMI、失业率
* **国际贸易**: 关税、贸易摩擦、进出口
* **金融市场**: 股市、债市、汇率、房地产
* **央行政策**: 美联储、人民银行、欧央行、日银

---

## 六、输出 JSON 格式

### 6.1 请求示例

```json
{
    "apiKey": "YOUR_API_KEY",
    "keyWordQuery": {
        "keyword": "美联储",
        "queryFields": ["1", "2"]
    },
    "macroEconomyResul": ["国际宏观"],
    "sentiments": [],
    "macroTags": [],
    "mediaTypes": [],
    "newsImportanceLevels": [],
    "pageNum": 0,
    "pageSize": 20,
    "sortBy": "publish_date",
    "sortType": "DESC",
    "startTime": 1774211938071,
    "endTime": 1774838338071
}
```

### 6.2 响应示例

```json
{
    "code": 200,
    "message": "success",
    "total": 156,
    "data": [
        {
            "title": "美联储宣布维持利率不变",
            "summary": "美联储 FOMC 会议决定维持联邦基金利率目标区间不变...",
            "source": "新浪财经",
            "publishDate": 1774838338071,
            "macroEconomyResult": "国际宏观",
            "macroTag": "货币政策",
            "areaResult": "美国",
            "newsImportanceLevel": "高",
            "heatScores": 85,
            "viewNum": 12500,
            "forwardedNum": 320
        }
    ]
}
```

### 6.3 必须展示字段

**每条资讯必须包含以下 10 个核心字段**：

| 序号 | 字段 | API 字段名 | 说明 |
|------|------|-----------|------|
| 1 | **新闻标题** | `title` | 资讯标题 |
| 2 | **新闻摘要** | `summary` | 资讯内容摘要 |
| 3 | **新闻内容** | `content` | 资讯完整正文 |
| 4 | **新闻来源** | `source` | 发布媒体/来源 |
| 5 | **发布时间** | `publishDate` | 13 位毫秒时间戳 |
| 6 | **宏观类型** | `macroEconomyResult` | 国内宏观/国际宏观 |
| 7 | **宏观事件标签** | `macroTag` | 事件分类标签 |
| 8 | **涉及地区** | `areaResult` | 相关地区 |
| 9 | **重要程度** | `newsImportanceLevel` | 高/中/低 |
| 10 | **热度数据** | `heatScores`/`viewNum`/`forwardedNum` | 热度得分、浏览数、转发数 |

---

## 七、解析规则

### 7.1 关键词解析

从用户输入中提取核心检索关键词。

#### 关键词提取规则

1. **提取核心词**：从用户输入中提取 1-3 个核心关键词
2. **同义词扩充**：为经济术语添加同义词
3. **情感词处理**：情感词（负面、正面）不放入关键词，通过 `sentiments` 参数控制

#### 关键词解析示例

|用户输入|关键词|
|-|-|
|美联储加息|`美联储`|
|国内 GDP 增长|`GDP`|
|人民银行降准|`降准`|
|美国通胀数据|`通胀`|
|中美贸易谈判|`贸易`|

### 7.2 宏观类型映射

|用户表述|macroEconomyResul|
|-|-|
|国内/中国/我国|`["国内宏观"]`|
|国际/美国/美联储/全球|`["国际宏观"]`|
|全部/不指定|`[]`|

### 7.3 情感倾向映射

|用户表述|sentiments|
|-|-|
|负面/负面信息/风险/担忧|`["负面"]`|
|正面/正面信息/利好/好消息|`["正面"]`|
|中性|`["中性"]`|
|全部情感/不指定|`[]`|

### 7.4 时间范围计算

|用户表述|计算方式|
|-|-|
|6 小时|当前时间 - 6 小时|
|24 小时/一天|当前时间 - 24 小时|
|3 天|当前时间 - 3 天|
|7 天/一周|当前时间 - 7 天|
|30 天/一个月|当前时间 - 30 天|

### 7.5 排序方式映射

**默认规则**：除非用户明确要求，否则一律使用 `publish_date`（发布时间）排序

|用户表述|sortBy|说明|
|-|-|-|
|**无明确要求**|`publish_date`|**默认**，获取最新发布的内容|
|按热度/热门/最火的|`heat_scores`|按热度排序|
|最新/最近/新发布的|`publish_date`|按发布时间排序（默认）|

**关键规则**：

1. **默认行为**：用户只说"搜索 XX 新闻"，没有提到排序方式 → 使用 `publish_date`
2. **明确要求时**：用户说"搜索最热门的 XX"、"按热度排序" → 使用 `heat_scores`
3. **时间优先**：用户关注时效性 → 使用 `publish_date`
4. **热度优先**：用户关注传播度 → 使用 `heat_scores`

### 7.6 重要程度映射

|用户表述|newsImportanceLevels|
|-|-|
|重要/重大|`["高"]`|
|一般/普通|`["中"]`|
|全部|`[]`|

---

## 八、通用规则

1. **必传参数**: `apiKey` 和 `keyWordQuery` 必须传入
2. **逻辑关系**: List 类型参数多值之间为**或关系**，不同参数之间为**且关系**
3. **时间规则**: 时间戳为 13 位毫秒级
4. **数值范围**: Min ≤ Max，否则筛选无效

---

## 九、数据返回方式

### 9.1 返回格式

搜索结果以 **双通道** 方式返回：

#### 通道 1：对话展示（摘要）

* 在对话中展示 **前 5 条** 数据的摘要信息
* **必须展示 10 个核心字段**：
  1. 新闻标题
  2. 新闻摘要
  3. 新闻内容
  4. 新闻来源
  5. 发布时间
  6. 宏观类型
  7. 宏观事件标签
  8. 涉及地区
  9. 重要程度
  10. 热度数据（热度得分、浏览数、转发数）

#### 通道 2：文件输出（完整数据）

* 自动保存 **所有返回数据** 到 CSV 和 MD 文件
* 文件位置：`./macro_information_<时间戳>.csv` 和 `./macro_information_<时间戳>.md`
* CSV 包含完整字段，MD 包含统计分析和数据说明

### 9.2 文件格式示例

**CSV 文件字段**:

```
发布时间，标题，摘要，内容，来源，宏观类型，事件标签，涉及地区，重要程度，热度得分，浏览数，转发数，URL
```

**MD 说明文件内容**:

```markdown
# 宏观资讯查询结果说明

**查询关键词**: 美联储
**宏观类型**: 国际宏观
**查询时间范围**: 近 7 天
**数据日期**: 2026-04-02 18:45:00
**结果总数**: 156 条
**接口状态**: code=200, message=success

## 宏观类型分布
- 国际宏观：120 条
- 国内宏观：36 条

## 情感分布
- 中性：98 条
- 正面：35 条
- 负面：23 条

## 宏观事件标签
- 货币政策：45 条
- 经济数据：32 条
- 国际贸易：28 条
...
```

### 9.3 使用建议

* **快速浏览**：查看对话中的前 5 条摘要
* **深度分析**：打开 CSV/MD 文件获取完整数据进行进一步处理
* **数据导出**：CSV 文件可直接导入 Excel 或其他分析工具

---

## 十、搜索执行方式

### 10.1 CLI 命令行工具（推荐）

**文件**: `scripts/query_macro_information.py`

通过命令行调用宏观资讯 API，支持所有筛选参数。

#### 基础用法

```bash
# 基础搜索
python3 scripts/query_macro_information.py --keyword "美联储"

# 搜索指定宏观类型（最近 7 天）
python3 scripts/query_macro_information.py --keyword "GDP" --macro-type 国内宏观 --days 7

# 搜索指定情感倾向
python3 scripts/query_macro_information.py --keyword "通胀" --sentiments 负面 --days 30

# 搜索国际宏观资讯
python3 scripts/query_macro_information.py --keyword "美联储" --macro-type 国际宏观 --days 14
```

#### 参数说明

**必填参数**

|参数|简写|说明|
|-|-|-|
|`--keyword`|`-k`|搜索关键词|

**宏观类型筛选**

|参数|简写|说明|
|-|-|-|
|`--macro-type`|`-m`|宏观类型：国内宏观/国际宏观|

**情感筛选**

|参数|简写|说明|
|-|-|-|
|`--sentiments`|`-s`|情感倾向：正面/负面/中性（可多选）|

**分页与排序**

|参数|简写|默认值|说明|
|-|-|-|-|
|`--days`|`-d`|7|查询天数|
|`--page`|`-p`|0|页码（从 0 开始）|
|`--size`|`-n`|20|每页数量|
|`--sort-by`||`publish_date`|排序字段|
|`--sort-type`||`DESC`|排序方式：ASC/DESC|

**输出控制**

|参数|简写|说明|
|-|-|-|
|`--verbose`|`-v`|显示详细内容（摘要）|
|`--output-dir`||输出目录（默认当前目录）|
|`--no-output`||不生成输出文件，仅显示结果|
|`--api-key`||Golaxy API Key（也可通过环境变量提供）|

#### 完整示例

```bash
# 搜索美联储近期负面舆情，最近 14 天
python3 scripts/query_macro_information.py \
    --keyword "美联储" \
    --macro-type 国际宏观 \
    --sentiments 负面 \
    --days 14 \
    --size 20 \
    --verbose
```

#### 输出结果

1. **对话显示**：自动在终端显示结果摘要（序号、时间、情感、标题、来源、热度）
2. **CSV 文件**：完整数据保存至 `./macro_information_<时间戳>.csv`
3. **MD 文件**：统计分析保存至 `./macro_information_<时间戳>.md`

---

### 10.2 API Key 配置方式

API Key 需要通过以下方式之一提供（优先级从高到低）：

1. **命令行参数**: `--api-key "your-api-key"`
2. **环境变量**: `export GOLAXY_API_KEY="your-api-key"`
3. **配置文件**: 在 `scripts/` 目录创建 `config.json`，内容为 `{"api_key": "your-api-key"}`

---

## 十一、示例对话

**用户**: 搜索最近 7 天关于美联储加息的国际宏观新闻，按热度排序

**解析结果**:

```json
{
    "apiKey": "YOUR_API_KEY",
    "keyWordQuery": {
        "keyword": "加息",
        "queryFields": ["1", "2"]
    },
    "macroEconomyResul": ["国际宏观"],
    "sentiments": [],
    "macroTags": [],
    "mediaTypes": [],
    "newsImportanceLevels": [],
    "pageNum": 0,
    "pageSize": 20,
    "sortBy": "heat_scores",
    "sortType": "DESC",
    "startTime": 1774211938071,
    "endTime": 1774838338071
}
```

**执行命令**:

```bash
python3 scripts/query_macro_information.py \
    --keyword "加息" \
    --macro-type 国际宏观 \
    --days 7 \
    --sort-by heat_scores
```

---

## 十二、执行流程

收到用户搜索请求后，必须按以下步骤顺序执行：

### Step 1: 检查 API Key 配置

```bash
cat .env | grep GOLAXY_API_KEY
```

* 如果返回空或文件不存在，提示用户："未配置 API Key，请前往 https://www.golaxy.com.cn 申请，完成后请告诉我 API Key 以便我记住"
* 如果存在有效的 API Key，继续下一步

### Step 2: 解析用户输入

从用户自然语言中提取以下参数：

|提取项|对应 CLI 参数|示例|
|-|-|-|
|关键词|`--keyword`|"美联储加息" → `--keyword "加息"`|
|宏观类型|`--macro-type`|"国际宏观" → `--macro-type 国际宏观`|
|时间范围|`--days`|"最近 3 天" → `--days 3`|
|情感倾向|`--sentiments`|"负面" → `--sentiments 负面`|
|排序方式|`--sort-by`|"按热度" → `--sort-by heat_scores`|

### Step 3: 构建并执行 CLI 命令

根据解析结果构建命令并执行：

```bash
python3 scripts/query_macro_information.py --keyword "关键词" --macro-type 国际宏观 --days 7 --sentiments 负面
```

### Step 4: 返回结果

* 在对话中显示结果摘要
* 完整数据自动保存至 CSV 和 MD 文件

### 执行示例

**用户输入**: "搜索最近 7 天美联储加息的国际宏观新闻"

**执行命令**:

```bash
python3 scripts/query_macro_information.py --keyword "加息" --macro-type 国际宏观 --days 7
```

---

## 十三、注意事项

1. **时间参数**: 使用 Unix 时间戳（毫秒），脚本会自动计算
2. **页码**: 从 0 开始计数
3. **情感倾向**: 正面、负面、中性，不传表示全部
4. **宏观类型**: 国内宏观、国际宏观，不传表示全部
5. **API Key**: 必须提供，支持三种配置方式
6. **输出文件**: 默认生成 CSV 和 MD 文件，可使用 `--no-output` 禁用

---

## 十四、参考文件

* `scripts/query_macro_information.py` - 主查询脚本
* `scripts/config.json` - API Key 配置文件（可选）
* `.env` - 环境变量配置文件

---

*数据来自 FEEDAX宏观资讯监测平台，涵盖新闻、社交媒体、论坛、金融平台等多种信源。*
