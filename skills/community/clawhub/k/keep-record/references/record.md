# 健康记录

## 工具：`record_tool`

统一的健康记录入口。用户的任何饮食 / 运动 / 体重 / 围度 / 睡眠 / 生理期记录都调这一个工具，具体记录类型由服务端根据 `text`（以及可选图片）自动识别与路由，Agent **不需要**预先分类。

## 使用场景

- 用户想"记录一下"健康相关信息
- 用户描述了饮食 / 运动 / 体重 / 围度 / 睡眠 / 生理期等数据
- 用户提供图片，希望作为记录的辅助信息（食物照片、体重秤读数等）

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 是 | 用户的原始描述。保留自然语言与关键信息：数量、单位、时间（如"午餐 12:30 吃了 200g 鸡胸肉和糙米饭"） |
| `image_url` | string | 否 | 图片 CDN URL，通过 `get_upload_url` 上传后获得 |

### `text` 组织建议

Agent 不做分类，但应**保留原始信息的完整度**，让服务端能正确路由：

- 数量 + 单位：`65kg` / `76cm` / `5km` / `30 分钟`
- 时间信息（如果用户提到）：`昨晚 10 点`、`今天早晨`
- 食物、动作、部位等明确实体：`鸡胸肉沙拉`、`腰围`、`瑜伽`

不要主动追问用户补齐字段——如果缺失（例如只说了"来姨妈了"），直接按原话传给 `record_tool`，由服务端决定是否需要更多信息。

## 图片上传（可选）

如果用户提供了图片：

1. 调用 `get_upload_url` 获取上传凭证
2. 使用返回的 `upload_url` 进行 HTTP PUT 上传
3. 将返回的 `cdn_url` 作为 `image_url` 传给 `record_tool`

详见 [图片上传](get-upload-url.md)。

## 调用示例

exec 方式（OpenClaw / Hermes）：

```bash
node {baseDir}/scripts/mcp-call.js record_tool '{"text":"午餐吃了鸡胸肉沙拉和一碗糙米饭","image_url":"https://cdn.keep.com/media/uid/2026-04-16/abc.jpg"}'
```

原生 MCP 方式：

```json
{
  "method": "tools/call",
  "params": {
    "name": "record_tool",
    "arguments": {
      "text": "午餐吃了鸡胸肉沙拉和一碗糙米饭",
      "image_url": "https://cdn.keep.com/media/uid/2026-04-16/abc.jpg"
    }
  }
}
```

## 返回与异常

成功：`{ ok: true, data: { ... 记录详情 ... } }`。Agent 按 [SKILL.md 的「结果呈现」](../SKILL.md#结果呈现) 格式化给用户。

常见错误码：`AUTH_REQUIRED` / `TOKEN_EXPIRED`（回 [鉴权流程](auth.md)）、`MEDIA_TOO_LARGE`、`MEDIA_TYPE_NOT_ALLOWED`、`RATE_LIMITED`、`UPSTREAM_ERROR`。完整表见 [SKILL.md 通用错误码](../SKILL.md#通用错误码)。
