---
name: 乐有家找房
description: "乐有家找房与小区查询：自然语言查11城二手房/租房、新房楼盘、学校及小区信息"
version: 1.3.0
homepage: https://www.leyoujia.com
metadata:
  {
    "openclaw":
      {
        "skillKey": "lyj-house",
        "emoji": "🏠",
        "requires": { "bins": ["curl"], "env": ["LYJ_API_KEY"] },
        "primaryEnv": "LYJ_API_KEY",
      },
  }
---

# 乐有家找房与小区查询

同一个 Skill 根据用户语义自动执行多类能力：

- **找房**：检索支持城市的二手房（`type=esf`）或租房（`type=zf`），返回房源列表并推荐。
- **找新房**：检索支持城市的新房楼盘，返回新房信息、户型信息、成交信息（以接口返回为准）。
- **找学校**：检索支持城市的学校信息，返回学校档案及关联小区名称（以接口返回为准）。
- **找小区**：检索支持城市的小区信息，返回小区档案、价格相关信息与周边配套（以接口返回为准）。

支持城市：`深圳`、`中山`、`东莞`、`惠州`、`广州`、`佛山`、`清远`、`珠海`、`江门`、`长沙`、`南京`。
二手房/租房找房接口中 `city` 按用户需求传，且必须在上述白名单内。

## 如何使用

- **直接说需求**：如「帮我找一套南山两房」「某某楼盘新房」「某某小学对口小区有哪些」「后海花园这个小区怎么样」，Agent 会按语义自动选择找房、新房、学校或小区流程，并在需要时**组合多个接口**（见下文「学位房/对口房源」策略）。
- **只需配置 API Key**：在 OpenClaw 配置中填写 `skills.entries.lyj-house.apiKey`，或安装乐有家找房插件后在插件配置中填写。Key 获取：https://shenzhen.leyoujia.com → 登录 → 「申请OpenClaw密钥」。二手房/租房主接口：`https://wap.leyoujia.com/wap/openclaw/ai/house/search`；其余接口见各步骤说明，均走同一域名与鉴权，无需单独配置 Base URL。
- **调用方式**：安装插件后会自动注入 `LYJ_API_KEY` 与 `LYJ_API_URL`（若仅配置了找房 URL，新房/学校接口仍使用下方文档中的固定路径拼接在同一域名下）。仅安装本 Skill 时请手动设置环境变量 `LYJ_API_KEY`。不要使用其它技能/插件的 key。

## 使用时机

✅ **以下情况启用此技能：**

- 找房类：
  - "帮我找一套南山两房"（二手房，`type=esf`）
  - "福田 100 平以内三房多少钱"（二手房，`type=esf`）
  - "我想在南山买房，预算 500 万"（二手房，`type=esf`）
  - "南山两房月租 5000 以内"（租房，`type=zf`）
  - "后海附近租房"（租房，`type=zf`）
  - "某某小学对口的两房，总价 800 万以内"（二手房 + 必要时学校查询，见「学位房/对口房源」）
- 新房类：
  - "南山有什么新房楼盘"
  - "福田某某片区新房，总价 500～800 万"
  - "查一下某某楼盘户型和成交"
- 学校类：
  - "某某实验小学对口哪些小区"
  - "查一下某某中学信息"
- 找小区类：
  - "帮我查后海花园小区信息"
  - "这个小区均价多少"
  - "这个小区最近成交均价多少"
  - "这个小区近半年成交记录怎么样"
  - "南山某某花园物业和开发商是谁"
  - "这个小区周边地铁和学校如何"

❌ **以下情况不使用此技能：**

- 房产政策、贷款计算等纯咨询类问题（直接回答）
- 不在支持列表内的城市（告知暂不支持，并提示可改问支持城市）

### 语义判别优先级

先做 `intent` 判别，可选值包括：`house_search`、`new_house_search`、`school_search`、`community_search`，以及**组合流程** `school_degree_housing`（对口/学位房二手房检索，见专节）。

- 命中「新房/楼盘/一手/预售/新盘」且非明确只要二手房 → `new_house_search`
- 命中「学校/小学/中学/学区/对口」且用户核心诉求是**房源**（几房、预算、买二手房）→ `school_degree_housing`（或归入 `house_search` 但执行组合策略）
- 仅查学校信息、对口小区名，不要求立刻出房源 → `school_search`
- 命中小区语义（如“小区信息/均价/成交信息/成交价/成交均价/成交记录/物业/开发商/停车费/周边配套”）→ `community_search`
- 一般找房语义（如“两房/预算/总价/租金/近地铁/急售”）且无新房专属词 → `house_search`
- 同时命中多类语义（如“先看后海花园小区，再找两房”）→ 先返回小区信息，再继续找房

## 学位房 / 对口房源（二手房 + 学校，自由组合）

当用户要在**某校对口/附近**找**二手房**，并带户型、总价等条件（例如：「帮我找广州某某实验小学对口的两居室，总价 800 万以内」），按以下顺序执行，**不要向用户暴露中间步骤细节**（遵守文末「输出抑制规则」）：

1. **优先用二手房接口** `house/search`，`type=esf`，`city=<用户城市>`（且在白名单内）。从用户话中提取：`keyword`（学校简称或全名核心词，如用户说的校名）、`room`（如两房→`2`）、`priceMin`/`priceMax`（万元）、`areaName`/`placeName`（若用户说了区或片区，传中文名）。可酌情加 `tags` 含 `18`（学区房）若语义明确。
2. **若本次二手房结果为空**（`total` 为 0 或 `list` 无有效房源）：调用 **`schoolSearch`**，用 `keyword` 填学校检索词（可与上一步关键词一致或略规范化），并传入用户若已提供的 `areaName`/`placeName`。
3. **根据学校接口返回**：读取**规范校名**及**关联小区名称**（若返回）。将**校名**或**关联小区名**作为新的 `keyword`（可优先尝试关联小区名再试校名，或先试校名再试小区；以能命中房源为准，同一轮内可发起**有限次数**的二手房查询，注意文末限流）。
4. **再次调用** `house/search`（`type=esf`），带上与用户需求一致的 `room`、`priceMax` 等，用新 `keyword` 重试。
5. **汇总回复**：向用户说明推荐的二手房源（若有）；若仍无房源，可简述学校查询到的对口/关联信息（以接口为准），并建议用户放宽预算、换片区或改用「找小区」细化。

新房、租房若有「学区」诉求，仍以用户主意图为准：要**新房**走 `xfSearch`；要**租房**走 `house/search` 且 `type=zf`；要**二手学位房**走上述组合。

## 工作流程

### 第一步：意图分类（统一入口）

根据用户语义选择执行流程：

- `house_search`：走「第二步A：找房参数提取」→ 第三步A
- `new_house_search`：走「第二步C：新房参数提取」→ 第三步C
- `school_search`：走「第二步D：学校参数提取」→ 第三步D
- `school_degree_housing`：走「学位房/对口房源」组合流程（上节）
- `community_search`：走「第二步B：找小区参数提取」→ 第三步B

### 第二步A：提取找房条件

从用户消息中识别以下条件（有即填，无则不传）。**城市 `city` 从用户语句提取并校验白名单**（支持：深圳、中山、东莞、惠州、广州、佛山、清远、珠海、江门、长沙、南京）；若未明确提及城市，先简短追问城市。**交易类型 `type`**：用户要**买房/二手房**传 `esf`，要**租房**传 `zf`。

**区域筛选**：城区、片区使用用户话语中的**中文名称**；请求体字段为 **`areaName`**（城区名）、**`placeName`**（片区名，比城区更细时优先填写）。**不要**将区、片区映射为数字 code；名称须属于当前请求的 **`city`**，不要跨城混用区域名。

除 `type`/`city`、`keyword`、`areaName`/`placeName`、`priceMin`/`priceMax`、`areaMin`/`areaMax` 等字符串或数值外，**户型、标签、朝向、装修等筛选项仍传文档中的数字 code**。

#### 基础参数

| 参数 | 说明 | 值 |
|------|------|----|
| type | 交易类型 | `esf`=二手房，`zf`=租房 |
| city | 城市 | 按用户需求传，且需在支持白名单内 |
| keyword | 关键词搜索房源标题 | 如 `南山学区`、`某某小学` |
| priceMin | 总价下限（万元整数） | 如 `200` |
| priceMax | 总价上限（万元整数） | 如 `600` |

#### 户型参数

| 参数 | 说明 | code 映射 |
|------|------|-----------|
| room | 居室 | `1`=一房 `2`=两房/二房 `3`=三房 `4`=四房 `5`=五房 `6`=五房以上 |
| toilet | 卫生间 | `1`=一卫 `2`=两卫/二卫 `3`=三卫 `4`=四卫 `5`=五卫 `6`=五卫以上 |
| balcony | 阳台 | `1`=一阳 `2`=二阳 `3`=二阳以上 |
| areaMin | 面积下限（㎡整数） | 如 `80` |
| areaMax | 面积上限（㎡整数） | 如 `120` |
| orientation | 朝向 | `69`=东 `70`=南 `71`=西 `72`=北 `73`=东南 `74`=东北 `75`=西南 `76`=西北 `77`=南北 `78`=全南 |
| hxFeature | 户型特色（多值用 `_` 分隔） | `1`=户型方正 `2`=通透 `3`=客厅开阔 `4`=视野开阔 `5`=厅带阳台 `6`=卧室阳台 `7`=浴室阳台 `8`=卧室带卫 `9`=带衣帽间 `10`=可放浴缸 `11`=开放厨房 `12`=入户花园 `13`=安静 `14`=大阳台 `15`=高赠送 `16`=带露台 `17`=卧室朝南 `18`=飘窗 `19`=落地窗 |
| jgFeature | 景观特色（多值用 `_` 分隔） | `1`=海景 `2`=山景 `3`=湖景 `4`=城市景观 `5`=高尔夫景观 |

#### 更多筛选

| 参数 | 说明 | code 映射 |
|------|------|-----------|
| tags | 房源特色（多值用 `_` 分隔） | `1`=新上 `3`=满五唯一 `4`=满两年 `5`=红本在手 `6`=随时可看 `7`=急售 `8`=有电梯 `9`=近地铁 `10`=非地下室 `11`=有视频 `12`=VR看房 `18`=学区房 `22`=满五年 `27`=实地核验 `28`=必卖好房 `37`=最近降价 `38`=有露台 `39`=高租售比 `40`=无电梯 |
| propertyType | 物业类型 | `1`=住宅 `2`=公寓 `3`=别墅 `4`=商铺 `5`=车位/车库 `6`=写字楼 `7`=其他 |
| elevator | 电梯 | `1`=有电梯 `2`=无电梯 |
| buildingAge | 楼龄 | `1`=2年以内 `2`=5年以内 `3`=10年以内 `4`=15年以内 `5`=20年以内 `6`=20年以上 |
| fitment | 装修 | `46`=毛坯 `47`=普装 `48`=精装 `49`=豪装 |

#### 区域参数

| 参数 | 说明 | 示例 |
|------|------|------|
| areaName | 城区中文名（可选） | `天河`、`南山`（须与 `city` 一致） |
| placeName | 片区中文名（可选，比 areaName 更细时优先） | `珠江新城东`、`后海` |

**直接根据已有信息构造参数，不必追问所有字段。若用户提到更细的地名，优先使用 `placeName`；若只提到区，使用 `areaName`。区域名称必须属于当前 `city`，不要跨城混用。**

### 第三步A：调用找房接口

- **URL**：`https://wap.leyoujia.com/wap/openclaw/ai/house/search`（固定，无需配置）。
- **鉴权**：请求头 `X-Api-Key: ${LYJ_API_KEY}`。
- **方式**：仅支持 POST，请求体为 raw JSON，勿用 GET 或 URL 参数。
- **Windows/PowerShell**：内联 JSON 易被转义破坏，建议将 body 写入 `body.json` 后使用 `curl -d @body.json`。

```bash
# 方式一：Bash/WSL 下可直接用 -d '...'（URL 未设置时使用固定地址）
curl -s -X POST "${LYJ_API_URL:-https://wap.leyoujia.com/wap/openclaw/ai/house/search}" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"type":"esf","city":"广州","areaName":"天河","room":"2","priceMax":600}'
```

```bash
# 方式二：Windows/PowerShell 下建议用文件传 body，避免转义问题
echo '{"type":"esf","city":"广州","areaName":"天河","room":"2","priceMax":600}' > body.json
curl -s -X POST "${LYJ_API_URL:-https://wap.leyoujia.com/wap/openclaw/ai/house/search}" -H "X-Api-Key: ${LYJ_API_KEY}" -H "Content-Type: application/json" -d "@body.json"
```

### 第四步A：解析找房结果并推荐

接口返回 JSON 格式，包含 `total`（总量）和 `list`（最多 30 套）。从列表中选出 **3～5 套最符合用户需求**的房源，按下方「展示字段规范」逐条展示；**若接口未返回某字段则省略该行，房源外网地址没有则不展示。**

### 第二步B：提取找小区条件

从用户消息中识别以下参数（有即填，无则不传）：

| 参数 | 说明 | 示例 |
|------|------|------|
| city | 城市 | 按用户需求传，且需在支持白名单内 |
| communityKeyword | 小区关键词（必填） | `"后海花园"` |
| areaName | 城区中文名（可选） | `"天河"` |
| placeName | 片区中文名（可选，优先级高于 areaName） | `"后海"` |
| page | 页码（可选） | `1` |
| pageSize | 每页数量（可选） | `10` |
| priceMin | 小区均价下限（元） | 如 `10000` |
| priceMax | 小区均价上限（元） | 如 `30000` |
| houseAge | 楼龄 | 如 `1` 1=2年以内、2=2-5年以内、3=5-10年以内、4=10-15年以内、5=15-20年以内|

### 第三步B：调用找小区接口

- **URL**：`https://wap.leyoujia.com/wap/openclaw/ai/communitySearch`（固定，无需配置）。
- **鉴权**：请求头 `X-Api-Key: ${LYJ_API_KEY}`。
- **方式**：仅支持 POST，请求体为 raw JSON，勿用 GET 或 URL 参数。
- **说明**：如果接口不可用，降级为找房兜底（见文末注意事项）。

```bash
# 示例：查后海花园小区信息
curl -s -X POST "https://wap.leyoujia.com/wap/openclaw/ai/communitySearch" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"city":"广州","communityKeyword":"天河公园"}'
```

```bash
# 可选：用城区/片区中文名缩小同名小区范围
curl -s -X POST "https://wap.leyoujia.com/wap/openclaw/ai/communitySearch" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"city":"深圳","communityKeyword":"花园","areaName":"南山"}'
```

### 第四步B：解析找小区结果并输出

接口返回 JSON 后，按下方「小区展示字段规范」输出。若返回多个小区，展示最匹配 Top 3，并提示用户可继续指定区域或小区全名。

### 第二步C：提取新房条件

从用户消息中识别以下条件（有即填，无则不传）。与二手房不同，本接口**不**使用 `house/search` 的 `type`/`city` 字段；参数如下：

| 参数 | 说明 | 示例 |
|------|------|------|
| keyword | 楼盘或片区关键词 | `"前海"`、`"某某花园"` |
| areaName | 城区中文名（可选） | 同二手房 `areaName` |
| placeName | 片区中文名（可选，优先于 areaName） | 同二手房 `placeName` |
| priceMin | 总价区间下限（单位：万元） | 如 `500` |
| priceMax | 总价区间上限（单位：万元） | 如 `800` |

### 第三步C：调用新房接口

- **URL**：`https://wap.leyoujia.com/wap/openclaw/ai/xfSearch`（固定，无需配置）。
- **鉴权**：请求头 `X-Api-Key: ${LYJ_API_KEY}`。
- **方式**：仅支持 POST，请求体为 raw JSON，勿用 GET 或 URL 参数。
- **Windows/PowerShell**：内联 JSON 易被转义破坏，建议将 body 写入 `body.json` 后使用 `curl -d @body.json`。
- **返回**：新房信息、新房户型信息、新房成交信息（以实际 JSON 字段为准）。


```bash
# 方式一：Bash/WSL 下可直接用 -d '...'（URL 未设置时使用固定地址）
curl -s -X POST "${LYJ_API_URL:-https://wap.leyoujia.com/wap/openclaw/ai/xfSearch}" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"前海","areaName":"南山","priceMin":500,"priceMax":800}'
```

```bash
# 方式二：Windows/PowerShell 下建议用文件传 body，避免转义问题
echo '{"keyword":"前海","areaName":"南山","priceMin":500,"priceMax":800}' > body.json
curl -s -X POST "${LYJ_API_URL:-https://wap.leyoujia.com/wap/openclaw/ai/xfSearch}" -H "X-Api-Key: ${LYJ_API_KEY}" -H "Content-Type: application/json" -d "@body.json"
```

### 第四步C：解析新房结果并推荐

按接口返回组织回答：优先展示**楼盘名称、区域、价格区间、主力户型要点**；若有**成交信息**且数据有效则简述；按「输出抑制规则」不展示原始 JSON。

### 第二步D：提取学校条件

| 参数 | 说明 | 示例 |
|------|------|------|
| keyword | 学校名称关键词 | `"实验小学"`、`"某某中学"` |
| areaName | 城区中文名（可选） | `"天河"` |
| placeName | 片区中文名（可选） | `"珠江新城东"` |

### 第三步D：调用学校接口

- **URL**：`https://wap.leyoujia.com/wap/openclaw/ai/schoolSearch`（固定，无需配置）。
- **鉴权**：请求头 `X-Api-Key: ${LYJ_API_KEY}`。
- **方式**：仅支持 POST，请求体为 raw JSON，勿用 GET 或 URL 参数。
- **返回**：学校信息，包含**关联小区名称**（以实际 JSON 字段为准）。

```bash
curl -s -X POST "https://wap.leyoujia.com/wap/openclaw/ai/schoolSearch" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"实验小学","areaName":"天河"}'
```

### 第四步D：解析学校结果并输出

按接口返回展示学校名称、办学类型/地址等有效字段；**关联小区**可列表呈现，便于用户后续用小区名走「找小区」或二手房 `keyword` 继续查。

## 完整示例

### 示例 1：找房

**用户说：** "帮我在广州天河找一套两房，总价 600 万以内，最好靠近地铁，精装"

**构造请求：**（PowerShell 下若遇 400，改用 `echo '...' > body.json` 再 `curl -d @body.json`）

```bash
curl -s -X POST "${LYJ_API_URL:-https://wap.leyoujia.com/wap/openclaw/ai/house/search}" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"type":"esf","city":"广州","placeName":"珠江新城东","room":"2","priceMax":600,"fitment":"48","tags":"9"}'
```

**按「展示字段规范」展示前 3～5 套最符合条件的房源；有房源外网地址时附上，没有则不展示。**

### 示例 2：找小区

**用户说：** "帮我查天河公园附近某小区信息，看看均价和周边配套"

**构造请求：**

```bash
curl -s -X POST "https://wap.leyoujia.com/wap/openclaw/ai/communitySearch" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"city":"广州","communityKeyword":"天河公园"}'
```

**按「小区展示字段规范」输出小区基础档案 + 价格相关 + 周边配套。**

### 示例 3：学位房 / 对口二手房（组合）

**用户说：** "帮我找一下广州某某实验小学对口的两居室，总价在 800 万以内"

1. 调用 `house/search`，`type=esf`，`city=<用户城市>`（白名单内），`keyword` 为用户口中的校名核心词，`room=2`，`priceMax=800`（可酌情 `tags` 含 `18`）。
2. 若无房源，调用 `schoolSearch`，`keyword` 同上，辅以用户若提到的 `areaName`/`placeName`（中文名）。
3. 用返回的**规范校名或关联小区名**作为新的 `keyword` 再次 `house/search`，条件不变。
4. 向用户推荐二手房源；若仍无，说明学校侧公开信息并建议放宽条件。

### 示例 4：新房

**用户说：** "广州天河片区新房，总价 700 万到 1000 万有什么盘"

**构造请求：**

```bash
# Bash / WSL
curl -s -X POST "https://wap.leyoujia.com/wap/openclaw/ai/xfSearch" \
  -H "X-Api-Key: ${LYJ_API_KEY}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"天河","areaName":"天河","priceMin":700,"priceMax":1000}'
```

```bash
# Windows / PowerShell（推荐）
echo '{"keyword":"天河","areaName":"天河","priceMin":700,"priceMax":1000}' > body.json
curl.exe -s -X POST "https://wap.leyoujia.com/wap/openclaw/ai/xfSearch" -H "X-Api-Key: ${LYJ_API_KEY}" -H "Accept: application/json" -H "Content-Type: application/json" -d "@body.json"
```

## 展示字段规范

### 房源展示字段规范（找房）

向用户展示每套房源时，按以下顺序包含下列内容（接口有则展示，无则省略；**房源外网地址没有则不展示**）：

1. **房源标题**
2. **居室、卫生间、面积、朝向、小区**
3. **房源标签**
4. **总价、均价**
5. **用途、装修、产权、建成、电梯**
6. **位置**：小区的地址
7. **周边**：交通、学校
8. **小区名称、小区开发商、小区物业公司**
9. **小区物业费、小区停车费**
10. **房源亮点**：生成的亮点
11. **房源外网地址**（仅当接口返回该字段且非空时展示，没有则省略）

### 小区展示字段规范（找小区）

向用户展示小区信息时，按以下顺序输出（接口有则展示，无则省略）：

1. **小区名称、所在区域**
2. **基础档案**：地址、建成年代、物业公司、开发商
3. **价格相关**：均价、在售数量、在租数量、成交相关信息（若有）
4. **周边配套**：地铁、学校、商圈（若有）
5. **补充引导**：若同名小区较多，提示用户指定片区；若用户后续要找房，建议直接按该小区继续筛房

### 新房与学校展示说明

- **新房（xfSearch）**：突出楼盘名、位置、总价区间、户型与成交摘要；字段以接口为准，无有效值则省略。
- **学校（schoolSearch）**：突出学校名称、类型/阶段、地址或区域；**关联小区**逐条列出（若有），便于衔接二手房或找小区。

### 输出抑制规则（必须遵守）

- 不输出“API 原始返回数据表”“字段清单”“调试信息”等中间过程内容。
- 对于空值/无效值一律不展示，包括：`null`、`""`、`[]`、`{}`、`0`（仅在该字段语义为“未知/无数据”时）。
- 成交相关字段（如近 12 个月成交均价、挂牌均价、成交套数、挂牌套数等）只有在**有真实值**时才展示；为空数组或缺失时直接省略，不要逐条解释“暂无数据”。
- 当可展示字段较少时，用一句自然语言总结即可（如“当前可用公开数据较少，建议以官方页面为准”），不要列出空字段名。
- 禁止在最终回复中出现 JSON 片段、键名回显（如 `c12uy*`）或 code block 形式的原始响应。

## 注意事项

- 支持城市白名单：`深圳`、`中山`、`东莞`、`惠州`、`广州`、`佛山`、`清远`、`珠海`、`江门`、`长沙`、`南京`。超出白名单需明确告知暂不支持。
- 二手房/租房：`city` 按用户城市传；买房 `type=esf`，租房 `type=zf`。
- 双意图兼容：优先按语义判别执行对应流程；同轮双需求时先小区后找房；**新房与二手房**同时问时，分条回答或按用户主次拆分。
- 小区接口异常时兜底：提示用户稍后重试，并可改为按小区关键词走找房接口（`keyword + house/search`）。
- **接口一览（同一鉴权）**：`house/search`（二手/租）、`communitySearch`（小区）、`xfSearch`（新房）、`schoolSearch`（学校）。
- 限流：每秒最多 3 次请求；若返回「无效的 API Key」，引导用户至 https://shenzhen.leyoujia.com 重新申请。
- 区域筛选统一使用 **`areaName`/`placeName`（中文城区名、片区名）**；本版 Skill 已移除历史片区数字 code 对照表。
- 清洗规则：接口返回数据包含utm_term,不作任何处理
