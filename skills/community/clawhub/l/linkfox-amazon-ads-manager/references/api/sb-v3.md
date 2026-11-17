# Sponsored Brands V3 Legacy API

V3 仅用于历史 Legacy Campaign。共存与路由规则见 [sb-coexistence.md](./sb-coexistence.md)。

## 脚本

| 脚本 | Amazon 路径 | 方法 | 说明 |
|---|---|---|---|
| `sb/v3/list_campaigns.py` | `sb/campaigns` | GET | offset 分页查询 Legacy 活动 |
| `sb/v3/create_campaigns.py` | `sb/campaigns` | POST | 创建 Legacy 活动；新业务不推荐 |
| `sb/v3/update_campaigns.py` | `sb/campaigns` | PUT | 更新 Legacy 活动 |
| `sb/v3/list_ad_groups.py` | `sb/adGroups` | GET | 查询 Legacy 活动关联的 Ad Group |
| `sb/v3/list_keywords.py` | `sb/keywords` | GET | 查询关键词 |
| `sb/v3/create_keywords.py` | `sb/keywords` | POST | 创建关键词，最多 100 个 |
| `sb/v3/update_keywords.py` | `sb/keywords` | PUT | 更新关键词，最多 100 个 |
| `sb/v3/list_targets.py` | `sb/targets/list` | POST | nextToken 分页查询商品定向 |
| `sb/v3/create_targets.py` | `sb/targets` | POST | 创建商品定向，最多 100 个 |
| `sb/v3/update_targets.py` | `sb/targets` | PUT | 更新商品定向 |

V3 Creative 没有独立 CRUD；品牌名、标题、ASIN、素材等位于 Campaign 的 `creative` 字段中，通过 Campaign create/update 管理。

## Legacy 安全参数

V3 脚本额外接受：

| 参数 | 作用 |
|---|---|
| `campaignStructure` | 传 `MULTI_AD_GROUP` 时拒绝调用 |
| `isMultiAdGroupsEnabled` | 传 `true` 时拒绝调用 |

这些字段只用于本地保护，不会发送给 Amazon。

## GET list 参数

Campaign：

- `campaignIdFilter`
- `stateFilter`
- `nameFilter`
- `portfolioIdFilter`
- `creativeType`

Ad Group：

- `adGroupIdFilter`
- `campaignIdFilter`
- `stateFilter`
- `nameFilter`
- `creativeType`

Keyword：

- `keywordIdFilter`
- `adGroupIdFilter`
- `campaignIdFilter`
- `stateFilter`
- `matchTypeFilter`
- `keywordText`
- `creativeType`
- `locale`

ID、状态、匹配类型可传字符串、数组或 `{"include":[...]}`，脚本转换成 Amazon 所需的逗号分隔 query。分页参数为 `maxResults`、`fetchAll`、`maxPages`。

## Target list 参数

Target list 接受 Amazon 原生 `filters`，也接受顶层 Object/Array 过滤（脚本会映射为 Amazon `filters[]`）：

```json
{
  "profileId": 1234567890,
  "region": "NA",
  "campaignIdFilter": {"include": ["1122334455"]},
  "stateFilter": ["enabled", "paused"],
  "maxResults": 100
}
```

等价原生写法：

```json
{
  "profileId": 1234567890,
  "region": "NA",
  "payload": {
    "maxResults": 100,
    "filters": [
      {"filterType": "CAMPAIGN_ID", "values": ["1122334455"]},
      {"filterType": "TARGETING_STATE", "values": ["enabled", "paused"]}
    ]
  }
}
```

可映射字段：`campaignIdFilter`→`CAMPAIGN_ID`，`adGroupIdFilter`→`AD_GROUP_ID`，`stateFilter`→`TARGETING_STATE`，`targetIdFilter`→`TARGET_ID`，`creativeTypeFilter`→`CREATIVE_TYPE`。

## 示例

```bash
python scripts/sb/v3/list_campaigns.py '{"profileId":1234567890,"region":"NA","stateFilter":["enabled","paused"]}'

python scripts/sb/v3/list_keywords.py '{"profileId":1234567890,"region":"NA","campaignIdFilter":["1122334455"]}'

python scripts/sb/v3/update_keywords.py '{"profileId":1234567890,"region":"NA","campaignStructure":"LEGACY","payload":[{"keywordId":1,"campaignId":2,"adGroupId":3,"bid":1.2}]}'
```

写操作不会自动切换到 V4；非 2xx 原样返回。
