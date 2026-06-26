### POST /api/hybrid/update_cookie
**Summary**: 更新指定服务的Cookie值，用于维护会话有效性

**功能描述**:
该接口用于更新指定服务的Cookie值，解决会话过期、访问受限等问题，是维持抖音网页版会话有效性的重要接口。

**API端点**:
`POST {{base_url}}/api/hybrid/update_cookie`

**请求参数**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| service | string | 是 | 服务名称，标识要更新Cookie的服务，如`douyin_web` |
| cookie | string | 是 | 新的Cookie值，完整的Cookie字符串 |

**参数说明**:
- `service`: 目前支持`douyin_web`（抖音网页版），后续可能扩展其他服务
- `cookie`: 从浏览器或其他途径获取的有效抖音Cookie字符串，包含`ttwid`、`odin_tt`等关键字段

**请求示例**:
```bash
# 基础请求示例
curl -X POST "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/hybrid/update_cookie" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "douyin_web",
    "cookie": "ttwid=1%7Cabc123...; odin_tt=def456...; passport_csrf_token=789xyz"
  }'
```

**快速测试**: 
```bash
# 直接更新Cookie并查看结果
curl -s -X POST "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/hybrid/update_cookie" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "douyin_web",
    "cookie": "ttwid=1%7Cabc123...; odin_tt=def456...; passport_csrf_token=789xyz"
  }' | jq '.status_msg'
```

**响应示例**:
```json
{
  "status_code": 0,
  "status_msg": "success",
  "service": "douyin_web",
  "update_time": 1712345678
}
```

**Cookie获取方法**:
1. **浏览器获取**: 打开抖音网页版，登录后在开发者工具→应用程序→Cookie中复制
2. **API获取**: 部分登录API可返回有效Cookie
3. **工具获取**: 使用浏览器自动化工具（如Playwright、Selenium）自动获取

**有效Cookie字段**:
至少需要包含以下字段之一才能维持抖音会话：
- `ttwid`: 抖音会话主令牌
- `odin_tt`: 设备验证令牌
- `passport_csrf_token`: CSRF防护令牌

**完整工作流程**:
1. 访问抖音网页版并登录
2. 复制当前有效的Cookie字符串
3. 调用当前接口更新服务Cookie
4. 后续API请求将使用新的Cookie进行身份验证

**注意事项**:
1. Cookie具有时效性，过期后需要重新获取更新
2. 不同设备的Cookie不能共享，需使用对应设备的Cookie
3. 频繁更新Cookie可能触发安全验证
4. 请妥善保管Cookie，避免泄露导致账号安全问题
5. 部分抖音接口可能需要特定的Cookie字段才能正常访问