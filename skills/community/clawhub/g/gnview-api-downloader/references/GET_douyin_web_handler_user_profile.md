### GET /api/douyin/web/handler_user_profile
**Summary**: 获取抖音指定用户的详细信息

**功能描述**:
该接口用于通过用户sec_user_id获取抖音用户的完整个人信息，包括用户基本资料、统计数据、认证信息等。

**API端点**:
`GET {{base_url}}/api/douyin/web/handler_user_profile`

**请求参数**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| sec_user_id | string | 是 | 用户sec_user_id（用户唯一标识） |

**参数说明**:
- `sec_user_id`: 可以通过`GET_douyin_web_get_sec_user_id.md`接口获取，格式如：MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y

**前置依赖**:
必须先通过`GET_douyin_web_get_sec_user_id.md`接口获取目标用户的sec_user_id

**请求示例**:
```bash
# 基础请求示例
curl -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/handler_user_profile?sec_user_id=MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y" \
  -H "Content-Type: application/json"
```

**快速测试**: 
```bash
# 直接获取用户详细信息并格式化输出
curl -s -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/handler_user_profile?sec_user_id=MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y" | jq '.nickname, .unique_id, .follower_count'
```

**响应示例**:
```json
{
  "sec_user_id": "MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y",
  "unique_id": "example_user",
  "nickname": "示例用户",
  "avatar": "https://p1.douyincdn.com/aweme/1000x1000/xxx.jpeg",
  "signature": "这个用户很懒，什么都没留下",
  "follower_count": 10000,
  "following_count": 500,
  "aweme_count": 200,
  "total_favorited": 500000,
  "verify_info": "抖音认证用户",
  "gender": 1,
  "birthday": "2000-01-01",
  "location": "北京市",
  "status_code": 0,
  "status_msg": "success"
}
```

**常用字段说明**:
| 字段名 | 类型 | 说明 |
|--------|------|------|
| unique_id | string | 用户抖音号（唯一标识） |
| nickname | string | 用户昵称 |
| follower_count | integer | 粉丝数量 |
| following_count | integer | 关注数量 |
| aweme_count | integer | 发布作品数量 |
| total_favorited | integer | 总获赞数量 |
| verify_info | string | 用户认证信息 |

**完整工作流程**:
1. 获取用户主页链接：`https://www.douyin.com/user/xxx`
2. 调用`GET_douyin_web_get_sec_user_id.md`接口提取sec_user_id
3. 调用当前接口获取用户详细信息

**注意事项**:
1. 该接口返回的信息非常全面，包含用户隐私相关数据
2. 部分敏感信息可能需要用户授权才能获取
3. 频繁调用可能触发抖音API限流，建议添加适当延迟
4. 不同用户的信息字段可能存在差异，注意处理缺失字段的情况