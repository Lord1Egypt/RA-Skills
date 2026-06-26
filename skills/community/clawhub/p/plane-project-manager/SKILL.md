# Plane 项目管理技能

通过 Plane API 管理项目、任务、文档。

## 凭证设置

创建 `~/.config/plane/credentials.json`：

```json
{
  "PLANE_URL": "http://localhost:8888",
  "PLANE_EMAIL": "你的 Plane 邮箱",
  "PLANE_PASSWORD": "你的密码",
  "PLANE_API_TOKEN": "plane_api_你的实际APIKey"
}
```

> ⚠️ **API Token 是敏感信息**，不要明文写在代码或文档里。

## 快速开始

### 1. 获取 API Token

登录 Plane 后访问：
```
http://localhost:8888/api/v1/users/me/api-tokens/
```

### 2. 测试连接

```bash
curl -s "http://localhost:8888/api/v1/workspaces/" \
  -H "X-API-Key: plane_api_你的实际APIKey"
```

### 3. 常用操作

详见 `references/api-examples.md`

## 注意事项

- 所有 API 请求必须在 `X-API-Key` header 中包含有效的 API Token
- 使用前请将代码和文档中的示例 key 替换为实际值
- 项目权限不足时，联系 Workspace Admin 在 Plane UI 中添加你为成员
