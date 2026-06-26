### GET /api/douyin/web/fetch_user_post_videos
**Summary**: 获取抖音用户主页的所有作品数据

**功能描述**:
该接口用于分页获取指定抖音用户的发布作品列表，支持按时间倒序获取视频数据，包含视频基本信息、统计数据等。

**API端点**:
`GET {{base_url}}/api/douyin/web/fetch_user_post_videos`

**请求参数**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| sec_user_id | string | 是 | 用户sec_user_id（用户唯一标识） |
| max_cursor | integer | 否 | 分页游标，用于获取下一页数据，首次请求传0 |
| count | integer | 否 | 每页获取的数量，默认20，最大建议50 |

**参数说明**:
- `sec_user_id`: 可以通过`GET_douyin_web_get_sec_user_id.md`接口获取
- `max_cursor`: 首次请求为0，后续请求使用返回结果中的`max_cursor`字段
- `count`: 建议不要设置过大，避免触发API限流

**请求示例**:
```bash
# 首次获取第一页数据（20个视频）
curl -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/fetch_user_post_videos?sec_user_id=MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE&max_cursor=0&count=20" \
  -H "Content-Type: application/json"

# 获取下一页数据（使用上一次返回的max_cursor）
curl -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/fetch_user_post_videos?sec_user_id=MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE&max_cursor=1712345678&count=20" \
  -H "Content-Type: application/json"
```

**快速测试**: 
```bash
# 直接获取用户视频列表并格式化输出
curl -s -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/fetch_user_post_videos?sec_user_id=MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE&max_cursor=0&count=3" | jq '.aweme_list[].title'
```

**响应示例**:
```json
{
  "aweme_list": [
    {
      "aweme_id": "7372484719365098803",
      "title": "抖音视频示例1",
      "play_count": 100000,
      "create_time": 1712345678
    },
    {
      "aweme_id": "7372484719365098804",
      "title": "抖音视频示例2",
      "play_count": 50000,
      "create_time": 1712345678
    }
  ],
  "has_more": true,
  "max_cursor": 1712345678,
  "status_code": 0,
  "status_msg": "success"
}
```

**完整工作流程**:
1. 调用`GET_douyin_web_get_sec_user_id.md`获取用户sec_user_id
2. 调用当前接口，首次请求max_cursor=0
3. 如果返回结果中has_more为true，使用返回的max_cursor作为下一次请求的参数
4. 重复步骤2直到has_more为false

**注意事项**:
1. 必须先获取sec_user_id才能调用此接口
2. 接口返回的数据按发布时间倒序排列
3. 频繁调用可能触发抖音API限流，建议添加适当延迟
4. 单个用户的视频数量可能很大，建议分页获取