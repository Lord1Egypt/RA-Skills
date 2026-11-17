---
name: linkfox-ruiguan-text-trademark-detection
description: 电商产品Listing文字商标检测与侵权风险分析，支持标题、描述等文本的违规品牌筛查。
---

# 睿观-文字商标检测（Ruiguan Text Trademark Detection）

本技能用于对电商产品标题及其他产品文本进行文字商标检测，帮助卖家在发布 Listing 前识别潜在的商标侵权风险。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 对产品文本（标题、描述、五点描述）进行文字商标检测，覆盖 15 个国家/地区的注册商标数据库。
- 返回匹配商标及其风险分数、注册详情、权利人信息，并给出整体产品风险等级。
- 识别黑名单商标（高危，需始终规避）与白名单商标（安全，可忽略），帮助卖家规避知识产权侵权。

### ❌ 边界与限制

- **仅文本检测**：只检测文本中的商标，不分析 Logo、图片或外观设计商标。
- **结果上限**：单次请求最多 500 条结果。
- **字符限制**：`productTitle` 与 `productText` 各限 1000 字符。
- **数据库覆盖**：覆盖 15 个国家/地区，其他司法辖区的注册商标可能无法检测。
- **非法律意见**：结果仅供参考，不构成法律建议；如需确定性的商标清权结论请咨询知识产权律师。
- **不在范围内**：Logo/图片商标分析、专利侵权检测、版权检测、法律意见或诉讼策略、商标注册/申请协助。

## 核心概念

文字商标检测将产品文本（标题、描述、五点描述）与 15 个国家/地区的注册商标数据库进行比对，返回匹配商标及其风险分数、注册详情、权利人信息，帮助卖家规避知识产权侵权。

**风险分数逻辑**：`highestModeScore` 字段取值 0-5，数值越高侵权风险越大。`textTrademarkRadar` 字段将产品整体风险分为三级：0（低风险）、1（待人工核查）、2（高风险）。

**黑名单与白名单**：响应可能包含 `blacklistTrademarks`（已知高危商标，需始终规避）与 `whitelistTrademarks`（安全商标，可忽略）。黑名单匹配需重点提示用户。

## 调用方式

- **API 端点**：`POST /ruiguan/textTrademarkDetection`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/ruiguan_text_trademark_detection.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-ruiguan-text-trademark-detection-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

> 请求构建原则：始终传入完整产品标题（`productTitle`）；按销售市场选择目标地区；有五点描述/描述/后台关键词时填入 `productText` 做更全面扫描；常规检测用默认 `limit: 100`，潜在匹配多时可提高到 500。用户未指定地区时默认 **US**。

**1. 基础美国商标检测（产品标题）**
```
productTitle: "Wireless Bluetooth Headphones Noise Cancelling Over Ear"
regions: "US"
limit: 100
```

**2. 多区域检测（美国 + 欧盟 + 英国）**
```
productTitle: "Portable USB-C Charger Fast Charging Power Bank"
regions: "US,EM,GB"
limit: 100
```

**3. 含附加文本的完整 Listing 扫描**
```
productTitle: "Stainless Steel Vacuum Insulated Water Bottle"
productText: "BPA-free, double-wall insulation, keeps drinks cold 24 hours, fits standard cup holders"
regions: "US,JP"
limit: 200
```

**4. 全球大范围检测**
```
productTitle: "LED Ring Light with Tripod Stand for Streaming"
regions: "US,EM,GB,DE,FR,IT,ES,AU,CA,MX,JP,CN"
limit: 500
```

**5. 中国国内市场检测**
```
productTitle: "智能蓝牙耳机降噪头戴式"
regions: "CN"
limit: 100
```

## 展示规则

1. **风险优先呈现**：始终在结果顶部突出整体风险等级（`textTrademarkRadar`），使用明确表述："低风险"、"待人工核查"、"高风险"。
2. **黑名单突出**：若 `blacklistTrademarks` 非空，优先展示并给出明确警示。
3. **表格格式**：以表格展示商标匹配，列包含：商标名称、地区、风险分数、状态、权利人、申请号、是否著名、是否亚马逊品牌、是否活跃维权人。
4. **分数说明**：提醒用户 `highestModeScore` 取值 0（安全）至 5（最高风险）。
5. **白名单说明**：若 `whitelistTrademarks` 有记录，标注为安全/豁免商标。
6. **错误处理**：请求失败时说明原因，建议用户检查产品标题或调整地区。
7. **非法律建议**：始终提醒结果仅供参考，不构成法律建议；如需确定性商标清权请咨询知识产权律师。

## 用户表达与场景速查

**适用** —— 产品文本商标风险分析：

| 用户说 | 场景 |
|--------|------|
| "检查我的标题有没有商标问题" | 基础商标扫描 |
| "这个产品名能用吗" | 侵权风险检查 |
| "扫描我的 Listing 有无品牌违规" | 完整 Listing 扫描 |
| "这个标题有商标风险吗" | 风险评估 |
| "查美国和欧盟的商标" | 多区域检测 |
| "XX 是不是注册商标" | 特定词查询 |
| "我的 Listing 会不会因知识产权被下架" | 合规筛查 |
| "这个关键词会不会侵权某个品牌" | 关键词安全检查 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题
发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# 睿观-文本商标检测 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/ruiguan/textTrademarkDetection`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productTitle | string | 是 | 产品标题，用于商标检测（最大1000字符） |
| regions | string | 否 | 国家/地区代码，多个用逗号分隔。支持值：US、EM、GB、DE、FR、IT、ES、AU、CA、MX、JP、CN、WO、TR、BX |
| limit | integer | 是 | 返回结果数量限制（默认100，最大500） |
| productText | string | 否 | 产品的其他文本信息，如五点描述或产品描述（最大1000字符） |

### 支持的地区代码

| 代码 | 地区 |
|------|------|
| US | 美国 |
| EM | 欧盟 |
| GB | 英国 |
| DE | 德国 |
| FR | 法国 |
| IT | 意大利 |
| ES | 西班牙 |
| AU | 澳大利亚 |
| CA | 加拿大 |
| MX | 墨西哥 |
| JP | 日本 |
| CN | 中国 |
| WO | WIPO（世界知识产权组织） |
| TR | 土耳其 |
| BX | 玻利维亚 |

用户未指定地区时默认 **US**。

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 匹配到的商标记录数 |
| data | array | 商标列表（扁平化），每个元素包含以下字段 |
| detectId | string | 接口调用 ID |
| columns | array | 渲染的列定义 |
| blacklistTrademarks | array | 文本中检测到的黑名单商标 |
| whitelistTrademarks | array | 文本中检测到的白名单（安全）商标 |
| textTrademarkRadar | string | 产品风险等级："0" = 低风险，"1" = 待人工核查，"2" = 高风险 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data[] 元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| trademarkName | string | 商标词 |
| region | string | 国家/地区代码 |
| score | integer | 风险分数 |
| highestModeScore | integer | 最高风险分数（范围0-5） |
| trademarksStatus | string | 最高分商标词状态 |
| regionStatus | string | 商标在匹配地区的状态 |
| holder | string | 权利人 |
| applicationNumber | string | 申请号 |
| registrationNumber | string | 注册号 |
| isFamous | boolean | 是否著名商标 |
| isAmazonBrand | boolean | 是否亚马逊热搜品牌 |
| isActiveHolder | boolean | 是否活跃维权人 |
| isCompatibility | boolean | 是否兼容性 |
| isCommonSense | boolean | 是否常用词 |
| niceClass | array | 尼斯分类 |
| originalTextMatches | array | 触发匹配的原词 |

### blacklistTrademarks[] 和 whitelistTrademarks[] 元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| trademark | string | 商标名称 |
| region | string | 国家/地区代码 |
| note | string | 备注 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分或余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/ruiguan/textTrademarkDetection \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "productTitle": "Wireless Bluetooth Headphones Noise Cancelling Over Ear",
    "regions": "US",
    "limit": 100
  }'
```

### 附带产品文本的示例

```bash
curl -X POST https://tool-gateway.linkfox.com/ruiguan/textTrademarkDetection \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "productTitle": "Portable USB-C Charger Fast Charging Power Bank",
    "productText": "Compatible with iPhone, Samsung Galaxy, supports QC 3.0",
    "regions": "US,EM,GB",
    "limit": 200
  }'
```
