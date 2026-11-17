# 词库查询 API 参考

本页为 `linkfox-keyword-library` 技能调用的底层接口规格。

## 接口说明

> 工具中文名：词库查询

MCP 服务名：`公共工具服务`（mind-x-tools-common-server）

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/common/keyword/listLibraries` 或 `/common/keyword/getWords`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 读取。

## 接口一：查询词库列表

### 请求参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| uid | string | 是 | | 用户ID |
| name | string | 否 | | 词库名称模糊搜索 |

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 词库总数 |
| libraries | array | 词库列表 |

`libraries[]` 元素：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 词库ID |
| name | string | 词库名称 |
| type | string | 词库类型（brand_risk/sensitive/prohibited/custom） |
| channel | string | 渠道 |
| wordCount | integer | 词条数量 |
| description | string | 描述 |

## 接口二：查询词条内容

### 请求参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| uid | string | 是 | | 用户ID |
| libraryId | string | 否 | | 词库ID（与 libraryName 二选一） |
| libraryName | string | 否 | | 词库名称（与 libraryId 二选一） |
| limit | integer | 否 | 500 | 返回词条数量上限，最大 500 |

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| libraryId | string | 词库ID |
| libraryName | string | 词库名称 |
| libraryType | string | 词库类型 |
| total | integer | 词条总数 |
| words | array | 词条列表 |

`words[]` 元素：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 词条ID |
| word | string | 词内容 |
| tags | array | 标签列表 |
| channel | string | 渠道 |
| remark | string | 备注 |

## 错误码

| errcode | 说明 |
|---------|------|
| 1 | 参数错误（如 uid 为空、libraryId 和 libraryName 都未传） |
| 2 | 词库不存在或无权访问 |
