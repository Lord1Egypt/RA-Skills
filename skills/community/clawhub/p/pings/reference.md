# 接口文档：获取订阅最新新闻（最小版）

仅保留 skill 调用所需信息，不包含内部实现细节。

## 1. 基本信息

- 方法：`GET`
- URL：`https://wink.run/api/pings/latest`
- 请求体：无（使用 Query 参数）
- 成功响应：`200` + `application/json`

## 2. Query 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `user_id` | string | 否 | - | 用户标识（推荐传用户邮箱） |
| `limit` | integer | 否 | `10` | 返回条数，建议 `1~10` |
| `freshness` | integer | 否 | `12` | 时间窗口（小时） |
| `lang` | string | 否 | `en` | `en` 或 `zh` |

## 3. 响应格式

成功时返回 JSON 数组，每项为新闻对象，常用字段如下：

- `id`
- `title`
- `summary`
- `source`
- `url`
- `date`
- `lang`
- `thumbnail_url`

## 4. 调用示例

```bash
curl "https://wink.run/api/pings/latest?user_id=user@example.com&limit=10&freshness=12&lang=zh"
```
