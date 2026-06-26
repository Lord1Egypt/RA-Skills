### GET /api/douyin/web/get_sec_user_id
**Summary**: 从抖音用户主页链接提取用户sec_user_id

**功能描述**:
该接口用于从抖音用户的个人主页链接中提取用户的sec_user_id，这是后续获取用户信息和作品列表的必要参数。

**API端点**:
`GET {{base_url}}/api/douyin/web/get_sec_user_id`

**请求参数**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | 抖音用户主页完整链接，格式如：https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE |

**参数说明**:
- `url`: 必须是完整的抖音用户主页链接，可以是从抖音APP分享的链接或网页版链接

**请求示例**:
```bash
# 基础请求示例
curl -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/get_sec_user_id?url=https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE" \
  -H "Content-Type: application/json"
```

**快速提取方法**:
如果不想调用API，也可以直接从用户主页链接中提取sec_user_id（使用shell命令）：
```bash
# 直接从URL提取sec_user_id
export USER_URL="https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE"
echo $USER_URL | grep -oP "/user/\K(MS4wLjABAAA[\w-]+)"

# 或使用jq解析
curl -s $USER_URL | grep -oP "secUserId":"\K[^"]+"
```

**快速测试**: 
```bash
# 直接提取并获取用户sec_user_id
curl -s -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/get_sec_user_id?url=https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE" | jq '.sec_user_id, .unique_id'
```

**响应示例**:
```json
{
  "sec_user_id": "MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE",
  "unique_id": "username",
  "nickname": "抖音用户昵称",
  "avatar": "https://example.com/avatar.jpg",
  "status_code": 0,
  "status_msg": "success"
}
```

**注意事项**:
1. 输入的用户主页链接必须是完整的URL，包含https://www.douyin.com/user/前缀
2. 如果链接是短链接（如v.douyin.com），需要先解析为完整链接
3. 该接口返回的sec_user_id是后续所有用户相关API调用的必要参数
4. 部分用户主页可能需要登录才能访问，此时需要提供有效的Cookie或认证令牌