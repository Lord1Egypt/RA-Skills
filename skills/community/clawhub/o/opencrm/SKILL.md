---
name: opencrm
description: 管理雄韬 XTOCN CRM 客户数据：新增客户（支持企查查/天眼查文本解析）、查询客户（精确/模糊/分页）、修改客户工商信息与联系方式（PATCH 语义）、设置分类标签（分组/等级/行业/来源）。同时支持线索、联系人、跟进记录的创建与查询。
allowed-tools: Bash, WebFetch
metadata:
  openclaw:
    requires:
      env: ["OPENCRM_KEY"]
    primaryEnv: OPENCRM_KEY
---

# 雄韬 XTOCN · OpenCRM

Base URL：`https://my.xtocn.com/api` | 认证：`Authorization: Bearer $OPENCRM_KEY`

## 决策表

| 用户意图 | 调用接口 | 关键参数 |
|---------|---------|---------|
| 粘贴企查查/天眼查文本，新增客户 | `POST /opencrm.parse/company` → `POST /opencrm.customer/add` | `text` → 解析结果确认 → `customer_name` 等字段 |
| 新增客户（已知字段） | `POST /opencrm.customer/add` | `customer_name`（必填），其他字段详见 `references/fields.md` |
| 按公司全称查客户 | `GET /opencrm.customer/detail?name=公司全称` | `name` |
| 按信用代码查客户 | `GET /opencrm.customer/detail?tax_number=统一社会信用代码` | `tax_number` |
| 模糊搜索客户 | `GET /opencrm.customer/list?keyword=关键词` | `keyword`、`page`、`limit` |
| 浏览客户列表 | `GET /opencrm.customer/list?page=1&limit=20` | `page`、`limit`（最大 200） |
| 修改客户档案（工商信息/联系方式/地址等） | `POST /opencrm.customer/edit` | `id`（必填），只传要改的字段 |
| 设置客户分组 | `POST /opencrm.customer/setGroup` | `id`、`customer_group` |
| 设置客户等级 | `POST /opencrm.customer/setLevel` | `id`、`level_name` |
| 设置客户行业 | `POST /opencrm.customer/setIndustry` | `id`、`industry` |
| 设置客户来源 | `POST /opencrm.customer/setSource` | `id`、`source` |
| 新增线索 | `POST /opencrm.lead/add` | `lead_name`（必填） |
| 查线索列表 | `GET /opencrm.lead/list` | `page`、`limit` |
| 新增拜访记录 | `POST /opencrm.followUp/add` | `customer_name` 或 `customer_id`、`follow_content`（必填） |
| 查看拜访记录 | `GET /opencrm.followUp/list` | `customer_name` 或 `customer_id` |
| 新增联系人 | `POST /opencrm.contact/add` | `customer_name`、`contact_name`（必填） |
| 查看联系人 | `GET /opencrm.contact/list` | `customer_name` 或 `customer_id` |

## 新增客户工作流

### 用户粘贴了原始文本（企查查/天眼查等）

```
GATE 1 [AI PARSE]
  POST /opencrm.parse/company { text: "..." }
  返回结构化字段 → 展示给用户确认，不要直接写入

GATE 2 [CONFIRM]
  用户确认无误 → POST /opencrm.customer/add
  用户要求修改 → 调整字段后再调用 add
  公司已存在 → 返回"客户名称已存在"，提示用户用 detail 查询
```

### 用户给了明确字段

直接调 `POST /opencrm.customer/add`，传入已知字段。

## 修改客户工作流

### 工商信息 & 联系方式 → 用 `edit`

```
用户要求修改税号/法人/注册资金/电话/地址等 → POST /opencrm.customer/edit
只传要改的字段，未传字段保持原样（PATCH 语义）
```

edit 可修改字段详见 `references/fields.md`。

### 分组/等级/行业/来源 → 用独立端点

这四个是分类标签，高频修改，用专用端点更安全：

```
改分组 → POST /opencrm.customer/setGroup { id, customer_group }
改等级 → POST /opencrm.customer/setLevel { id, level_name }
改行业 → POST /opencrm.customer/setIndustry { id, industry }
改来源 → POST /opencrm.customer/setSource { id, source }
```

每个端点只做一件事，避免误操作。传名称即可，系统自动匹配字典 ID。

## 查询工作流

```
已知公司全称 → detail?name= 精确匹配，返回一条或空
已知信用代码 → detail?tax_number= 精确匹配
模糊搜索 → list?keyword= 分页返回
浏览全部 → list?page=1&limit=20 分页返回
```

## 响应处理

统一格式 `{"status":200,"message":"success","data":{...}}`。`status=200` 成功，`status=500` 失败（展示 `message`）。

列表返回 `data.list.data`（数组）+ `data.list.total`（总数），用 `page`/`limit` 分页。

## 显示规范

- 客户详情展示：公司名、法定代表人、注册资本、成立日期、信用代码、状态、地址、经营范围、行业
- 列表展示：公司名、行业、法定代表人、最后跟进时间
- **永远不要向用户暴露内部 ID**，用公司名称代替

## 注意事项

- 行业/等级/来源/分组四个字典字段如果值不在系统字典中，API 会自动创建
- 公司名重复返回"客户名称已存在"，不要重试，引导用户查已有记录
- 请求前确认 `$OPENCRM_KEY` 已设置
- 完整字段列表见 `references/fields.md`
