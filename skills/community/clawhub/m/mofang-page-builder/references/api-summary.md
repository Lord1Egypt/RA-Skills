# 魔方网表记录 API 摘要

供 Trae Skill 生成页面时参考。本文件覆盖生成页面、解析空间/表单、调试代理和发布所需的常用接口。

## 1. 同域部署说明

页面部署到魔方网表同域时，**无需 Token**。浏览器自动携带 Cookie，使用**相对路径**即可：

- 示例：`/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry`
- 不要设置 `Authorization` 头

脚本、proxy 或非同域调试访问真实环境时，需要先登录：

| 能力 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取 JWT/Cookie | POST | `/magicflu/jwt` | `application/x-www-form-urlencoded`，body 为 `j_username=...&j_password=...` |

登录成功响应包含 `token`，后续服务端脚本请求可带 `Authorization: Bearer {token}`，并合并响应里的 `Set-Cookie`。

## 2. 核心接口路径

| 能力 | 方法 | 路径 |
|------|------|------|
| 全量列出空间 | GET | `/magicflu/service/json/spaces/feed?start=0&limit=-1&bq=(created,orderby,desc)` |
| 按名称查询空间 | GET | `/magicflu/service/json/spaces/feed?start=0&limit=10&bq=(label,eq,{spaceLabel})` |
| 查询空间下表单列表 | GET | `/magicflu/service/s/json/{spaceId}/forms/feed?start=0&limit=-1` |
| 按表单名称查询 | GET | `/magicflu/service/s/json/{spaceId}/forms/feed?start=0&limit=10&bq=(label,eq,{formLabel})` |
| 字段定义 | GET | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}?selector=fielddef&lng=en` |
| 查询记录 | GET | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry` |
| 创建记录 | POST | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records` |
| 修改记录 | PUT | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry/{recordId}` |
| 删除记录 | DELETE | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry/{recordId}` |

### 2.1 空间查询响应

查询空间使用顶层 `service/json` 路径：

```text
/magicflu/service/json/spaces/feed?start=0&limit=10&bq=(label,eq,{spaceLabel})
```

常用字段：

| 字段 | 说明 |
|------|------|
| `items[].id` | 空间 ID，也就是后续 `spaceId` |
| `items[].label` | 空间显示名称 |
| `totalCount` | 匹配空间总数 |

如果需要遍历所有空间，使用 `start=0&limit=-1&bq=(created,orderby,desc)`。如果精确匹配没有结果，再尝试模糊匹配：`bq=(label,like_and,{spaceLabel})`。

### 2.2 表单列表响应

查询表单列表使用 `json` 路径，不是 `jsonv2`：

```text
/magicflu/service/s/json/{spaceId}/forms/feed?start=0&limit=-1
```

常用字段：

| 字段 | 说明 |
|------|------|
| `feed.entry[].id` | 表单 ID，也就是后续 `formId` |
| `feed.entry[].content.form.label` | 表单显示名称 |
| `feed.entry[].content.form.name` | 表单英文标识 |
| `feed.totalCount` | 表单总数 |

如果只知道表单名称，先用精确匹配：`bq=(label,eq,{formLabel})`；没有结果再尝试模糊匹配：`bq=(label,like_and,{formLabel})`。

## 3. 查询记录参数

| 参数 | 说明 |
|------|------|
| start | 分页起始（从 0 开始） |
| limit | 每页数量，-1 表示全部 |
| bq | 查询条件，需 encodeURIComponent 编码 |

## 4. 字段规则（必须遵守）

### 4.1 name vs label

- **API 传值**（data 的 key、filters 的 fieldName）：必须用 `name`（英文标识）
- **展示**：用 `label`（中文名称）
- 错误示例：`{"客户名称": "北京公司"}` → 字段会为空
- 正确示例：`{"kehumingcheng": "北京公司"}`

### 4.2 可编辑字段类型

| 类型 | 值格式 |
|------|--------|
| text / multiline_text / url | 字符串 |
| number | 数字，不能提交空字符串 |
| date | `YYYY-MM-DD` |
| datetime | `YYYY-MM-DD HH:mm:ss` |
| dropdown_list | 选项 ID，如 `"1"` |
| checkbox | 选项 ID 逗号分隔，如 `"1,2"` |
| reference（主引用） | `{"id":"记录序号"}` |

### 4.3 不可提交字段

system、serial、辅引用、图片、附件、定位、网页、注释、外部字段组

## 5. bq 查询语法要点

- 格式：`fieldName(operator):value`，多个用 `&&` 或 `||` 连接
- 文本类（string）：`like_and`、`eq` 等，**值需 Base64 编码**
- 数字/日期类（region）：`eq`、`lt`、`gt`、`between` 等，值不编码
- 示例：`mingcheng(like_and):_5YyX5Lqs`（客户名称模糊匹配「北京」）

## 6. 响应结构

### 查询记录

```json
{
  "entry": [{ "id": "25", "mingcheng": "北京公司", ... }],
  "totalCount": 1
}
```

- `entry[].id`：记录 ID，用于修改/删除
- 字段值以 `name` 为 key

### 字段定义

```json
{
  "fields": [
    { "name": "jine", "label": "金额", "type": "number", ... }
  ]
}
```

- 创建/修改前需先获取字段定义，建立 label→name 映射
