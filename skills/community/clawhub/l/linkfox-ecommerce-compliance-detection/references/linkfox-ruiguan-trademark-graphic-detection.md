---
name: linkfox-ruiguan-trademark-graphic-detection
description: 基于睿观的产品图片图形商标与 Logo 侵权检测及相似度比对工具。
---

# 睿观-图形商标检测（Ruiguan Graphic Trademark Detection）

本技能用于对产品图片进行图形商标检测与相似度搜索，帮助电商卖家与品牌方在商品上架前识别潜在的商标侵权风险。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于产品图片检测图形商标，将图片中的图形/Logo 与全球多国已注册商标数据库进行视觉相似度比对。
- 支持按国家/地区筛选检测范围，返回商标图片、相似度、商标名称、状态、受理局、尼斯分类、申请人及关键日期等信息。
- 支持开启切图（局部定位）与雷达监测，提供聚合风险评估。

### ❌ 边界与限制

- **图片必填**：`imageUrl` 为必填，无图片无法检测。
- **结果上限**：`topNumber` 单次最多 100 条，实际返回数量可能少于传参。
- **图片质量**：检测精度依赖图片分辨率与清晰度，图片越清晰结果越准。
- **地区覆盖**：并非所有国家都覆盖，支持 15 个主要商标受理局（US、WO、ES、GB、DE、IT、CA、MX、EM、AU、FR、JP、TR、BX、CN）。
- **本地图片需先上传**：工具要求可公开访问的图片 URL，本地文件需先通过上传脚本获取公网链接。
- **不在范围内**：文字商标检索（无图片）；商标注册/申请；专利或版权检查；商标纠纷法律建议；商品 Listing 优化。

## 核心概念

图形商标检测通过分析产品图片，在全球多国/地区的已注册商标库中查找视觉相似的商标。工具采用基于 YOLO 的目标检测定位图片中的类 Logo 区域，再与全球商标数据库比对。

**相似度评分**：`similarity` 值越高，表示检测到的图形与已注册商标在视觉上越相似；接近 1.0 表示近似一致，侵权风险越高。

**商标状态含义**：

| 状态 | 含义 |
|--------|---------|
| registered | 商标已有效注册 |
| act | 商标处于有效状态 |
| pend | 商标申请待审 |
| filed | 商标申请已提交 |
| ended | 商标已到期 |
| DEL | 商标已注销/删除 |

## 本地图片上传

本工具要求**可公开访问的图片 URL**。若用户提供本地图片文件路径（如 `C:\Users\...\photo.png`、`/home/.../image.jpg`），须先上传以获取公网链接。

运行上传脚本：
```bash
python scripts/upload_image.py /path/to/local/image.png
```

脚本会返回一个公网 URL（有效期 24 小时），用作 `imageUrl` 参数。

## 调用方式

- **API 端点**：`POST /ruiguan/trademarkGraphicDetection`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/ruiguan_trademark_graphic_detection.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-ruiguan-trademark-graphic-detection-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 基础图片商标检测**
对产品图片在所有地区检测商标，最多返回 10 条结果：
```
imageUrl: "https://example.com/product-image.jpg"
topNumber: 10
```

**2. 指定地区检测**
仅对照美国与欧盟商标库检测：
```
imageUrl: "https://example.com/product-image.jpg"
topNumber: 5
regions: "US,EM"
```

**3. 带产品上下文的详细检测**
提供产品标题与疑似 Logo 名称以提升检测精度：
```
imageUrl: "https://example.com/product-image.jpg"
topNumber: 10
productTitle: "Wireless Bluetooth Headphones with Noise Cancellation"
trademarkName: "SonicWave"
regions: "US,GB,DE"
```

**4. 开启切图的完整检测**
开启 `enableLocalizing` 以获取检测到的 Logo 区域切图：
```
imageUrl: "https://example.com/product-image.jpg"
topNumber: 20
enableLocalizing: true
regions: "US"
```

## 展示规则

1. **清晰呈现结果**：以结构化表格展示商标图片、相似度、商标名称、状态、受理局、尼斯分类、申请人及关键日期。
2. **高亮高风险匹配**：当相似度高于 0.8 时，明确提醒用户存在高侵权风险。
3. **解释商标状态**：展示结果时说明各商标状态对风险评估的含义。
4. **雷达结果**：响应中存在 `radarResult` 时突出展示，因其包含聚合风险评估。
5. **子雷达结果**：单条结果含 `subRadarResult` 时，将其与对应匹配一并列出。
6. **地区范围**：始终说明本次检索覆盖了哪些地区，便于用户理解检测范围。
7. **错误处理**：检测失败时根据响应说明原因，并建议调整（如使用更清晰的图片、指定地区、调整 `topNumber`）。

## 用户表达与场景速查

**适用** —— 图形商标检测任务：

| 用户说 | 场景 |
|--------|------|
| "这张图片有没有商标问题" | 基础商标检测 |
| "这个 Logo 在哪注册过" | 多地区商标检索 |
| "我的产品图有商标风险吗" | 上架前风险评估 |
| "找和这个图形相似的商标" | 相似度检索 |
| "对照美国商标查这张图" | 指定地区检测 |
| "这个设计会不会侵权" | 侵权风险检查 |
| "扫一下产品图里的 Logo" | 产品图 Logo 检测 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# 睿观-图形商标检测 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/ruiguan/trademarkGraphicDetection`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imageUrl | string | 是 | 产品图片URL或base64编码的图片数据（最大1000字符） |
| topNumber | integer | 是 | 返回YOLO坐标的最大数量，默认 `5`，最大 `100`。实际返回数量可能少于传参数量 |
| productTitle | string | 否 | 产品标题，用于上下文感知检测（最大1000字符） |
| trademarkName | string | 否 | 可能的图形logo名称，用于缩小检索范围（最大1000字符） |
| regions | string | 否 | 需要检测的国家/地区代码，多个时使用逗号隔开，不传默认全部国家。可选值：US（美国）、WO（世界知识产权）、ES（西班牙）、GB（英国）、DE（德国）、IT（意大利）、CA（加拿大）、MX（墨西哥）、EM（欧盟）、AU（澳大利亚）、FR（法国）、JP（日本）、TR（土耳其）、BX（玻利维亚）、CN（中国） |
| enableLocalizing | boolean | 否 | 是否开启切图，默认 `false` |
| enableRadar | boolean | 否 | 是否开启雷达监测，默认 `true` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| boundingBoxCount | integer | 检测结果数量 |
| radarResult | string | 雷达检测结果 |
| total | integer | 记录数 |
| data | array | 检测结果列表（详见下方） |
| detectId | string | 检测ID |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data 数组项字段

`data` 数组中每个对象包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| image | string | 匹配的商标图片地址 |
| boundingBox | string | YOLO坐标（逗号隔开） |
| subRadarResult | string | 子雷达检测结果 |
| applicationNumber | string | 申请号 |
| niceClassName | string | 尼斯分类名称（逗号隔开） |
| applicantName | string | 权利人（逗号隔开） |
| tradeMarkStatus | string | 商标状态，枚举值：`"DEL"`、`"ended"`、`"registered"`、`"act"`、`"pend"`、`"filed"`、`""` |
| niceClass | array | 尼斯分类详情 |
| similarity | number | 相似度（0到1，值越高越相似） |
| registrationNumber | string | 注册号 |
| registrationOfficeCode | string | 商标受理局 |
| registrationDate | string | 注册日期 |
| bid | string | logo标识 |
| trademarkName | string | 图片中的文字商标名称 |
| applicationDate | string | 申请日期 |

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
curl -X POST https://tool-gateway.linkfox.com/ruiguan/trademarkGraphicDetection \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"imageUrl": "https://example.com/product-image.jpg", "topNumber": 5, "productTitle": "无线蓝牙耳机", "regions": "US,EM"}'
```
