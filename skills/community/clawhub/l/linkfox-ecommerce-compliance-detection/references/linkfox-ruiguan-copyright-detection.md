---
name: linkfox-ruiguan-copyright-detection
description: 基于睿观的图片版权侵权检测与风险分析工具，用于排查已登记作品的侵权与 TRO 风险。
---

# 睿观版权检测（Ruiguan Copyright Detection）

本技能用于执行图片版权检测，帮助电商卖家和设计师在使用图片前识别潜在的版权侵权风险。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 对给定的图片 URL 进行版权检测，与已登记版权作品库比对，返回视觉相似的版权作品及风险指标。
- 提供相似度、权利人、版权标识码、TRO 维权史、雷达侵权判定等多维风险信息。
- 支持本地图片上传获取公开 URL 后再检测。

### ❌ 边界与限制

- **图片 URL 必需**：仅接受可公开访问的图片 URL，不直接接收本地上传；本地文件需先用上传脚本转为公开 URL。
- **URL 长度**：图片 URL 不超过 1000 字符。
- **结果上限**：单次查询最多返回 200 条结果。
- **检测范围**：仅限检测服务维护的已登记版权作品库。
- **非法律意见**：仅呈现检测数据，不提供法律结论。
- **不在范围内**：商标或专利检索；文字或音乐版权检测；图片编辑修改；非版权目的的反向图片搜索；法律咨询或诉讼策略。

## 核心概念

版权检测通过将给定图片与已登记版权作品库进行比对来工作。系统返回视觉相似的版权作品及关键风险指标，如相似度、权利人信息、TRO（临时限制令）维权史、雷达侵权判定。

**相似度（similarity）**：字符串小数（如 `"0.85"`），表示输入图片与版权作品的匹配程度，值越高风险越大。

**雷达检测（enableRadar）**：额外的分析层，提供二元侵权判定（`1` = 侵权，`0` = 不侵权）。开启时每条结果包含此二次评估。

**TRO 维权史**：TRO（Temporary Restraining Order，临时限制令）是版权维权中常用的法律手段。结果中标记 TRO 史表示权利人曾发起法律行动，风险较高。

## 调用方式

- **API 端点**：`POST /ruiguan/copyrightDetection`（完整参数/响应/错误码见 [references/api.md](references/api.md)）
- **Python 脚本**：`python scripts/ruiguan_copyright_detection.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-ruiguan-copyright-detection-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 本地图片上传

本工具要求**可公开访问的图片 URL**。若用户提供的是本地图片文件路径（如 `C:\Users\...\photo.png`、`/home/.../image.jpg`），须先上传以获取公开 URL。

运行上传脚本：
```bash
python scripts/upload_image.py /path/to/local/image.png
```

脚本返回一个公开 URL（有效期 24 小时），可作为 imageUrl 参数使用。

## 使用示例

**1. 单张图片基础版权检测**
> "帮我查一下这张图片有没有版权问题：https://example.com/my-image.jpg"
动作：设置 `imageUrl` 为提供的 URL，其余参数用默认值。

**2. 快速扫描少量结果**
> "对这张产品图做个快速版权扫描，只要最匹配的几条：https://example.com/product.png"
动作：设置 `topNumber` 为 10，更快返回。

**3. 最大结果全面审计**
> "我要对这张设计图做一次完整的版权审计：https://example.com/design.jpg"
动作：设置 `topNumber` 为 200，最全面扫描。

**4. 仅相似度检测（关闭雷达）**
> "只查这张图和版权作品的相似度，不需要详细侵权分析：https://example.com/photo.jpg"
动作：设置 `enableRadar` 为 `false`。

**5. 批量检测多张图片**
> "帮我检测这三张图片的版权：url1、url2、url3"
动作：对每个图片 URL 调用一次 API，汇总结果。

## 展示规则

1. **清晰呈现数据**：以结构化表格展示检测结果，关键列包括相似度、权利人、版权标识码、雷达结果、TRO 史、版权来源链接。
2. **高亮高风险**：相似度较高（如 ≥ 0.80）或雷达检测判定侵权（`subRadarResult` = 1）时，明确标注为高风险条目。
3. **TRO 警告**：当 `troCase` 或 `troHolder` 为 `true` 时，醒目提示用户该权利人存在 TRO 维权史。
4. **图片预览**：`path` 或 `pathThumb` 可用时，提示用户可在该 URL 查看版权作品缩略图。
5. **结果数量提示**：告知用户匹配的 `total` 总数；结果较多时优先展示相似度最高的条目。
6. **错误处理**：请求失败时说明原因，建议检查图片 URL 是否可公开访问、格式是否正确。
7. **不做法律建议**：如实呈现检测数据，不提供法律结论；建议用户咨询法律人士获取权威版权评估。

## 用户表达与场景速查

**适用** —— 图片版权风险评估：

| 用户说 | 场景 |
|--------|------|
| "查这张图有没有版权问题" | 基础版权检测 |
| "这张图用着安全吗" | 侵权风险检测 |
| "找相似的版权图片" | 版权相似度搜索 |
| "这张图有 TRO 风险吗" | TRO 维权风险分析 |
| "这张图的版权归谁" | 权利人查询 |
| "产品图版权审计" | 批量版权合规检查 |
| "这设计是原创还是抄袭" | 原创性验证 |

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

# 睿观-版权检测 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/ruiguan/copyrightDetection`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imageUrl | string | 是 | 检测的版权图片URL（最大长度1000字符） |
| topNumber | integer | 是 | 召回数量（默认100，最小10，最大200） |
| enableRadar | boolean | 是 | 是否开启雷达检测（默认 `true`） |

- `imageUrl` 必须为可公开访问的图片URL
- `topNumber` 控制返回匹配版权作品的数量，默认100，范围10-200
- `enableRadar` 开启后将进行额外的侵权雷达判定，建议设为 `true` 以获得更全面的分析

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 检测结果列表（详见下方） |
| detectId | string | 检测id |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### 检测结果对象（`data` 数组中的元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| path | string | 版权画图片路径 |
| pathThumb | string | 版权画缩略图路径 |
| similarity | string | 相似度 |
| subRadarResult | integer | 1-侵权 0-不侵权，null 没有进行雷达检测 |
| copyrightUrl | string | 来源 |
| copyrightCode | string | 版权标识码 |
| rightsOwner | string | 权利人 |
| link | string | 版权官网链接 |
| troCase | boolean | 是否有TRO维权史 |
| troHolder | boolean | 是否是TRO权利人的版权 |

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
curl -X POST https://tool-gateway.linkfox.com/ruiguan/copyrightDetection \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrl": "https://example.com/test-image.jpg",
    "topNumber": 100,
    "enableRadar": true
  }'
```
