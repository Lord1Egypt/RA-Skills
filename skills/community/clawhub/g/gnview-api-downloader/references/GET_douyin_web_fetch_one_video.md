### GET /api/douyin/web/fetch_one_video
**Summary**: 获取抖音单个作品的详细数据

**功能描述**:
该接口用于获取抖音单个视频的完整数据，包括视频基本信息、统计数据、作者信息、音乐信息等。

**API端点**:
`GET {{base_url}}/api/douyin/web/fetch_one_video`

**请求参数**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| aweme_id | string | 是 | 抖音视频ID（作品唯一标识），格式为纯数字字符串 |

**参数示例**:
```
aweme_id = "7372484719365098803"
```

**请求示例**:
```bash
# 基础请求示例
curl -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/fetch_one_video?aweme_id=7372484719365098803" \
  -H "Content-Type: application/json"
```

**快速测试**: 
```bash
# 直接获取视频详细信息并格式化输出
curl -s -X GET "http://sd79uu743j76vf3vkn7pg.apigateway-cn-beijing.volceapi.com/api/douyin/web/fetch_one_video?aweme_id=7372484719365098803" | jq '.aweme_detail.title, .aweme_detail.play_count'
```

**响应示例**:
```json
{
  "aweme_detail": {
    "aweme_id": "7372484719365098803",
    "title": "抖音视频示例",
    "play_count": 100000,
    "digg_count": 10000,
    "comment_count": 1000,
    "author": {
      "uid": "123456",
      "nickname": "抖音用户",
      "unique_id": "username"
    },
    "music": {
      "title": "背景音乐",
      "author": "音乐作者"
    }
  },
  "status_code": 0,
  "status_msg": "success"
}
```

**注意事项**:
1. aweme_id是视频的唯一标识，可以从抖音视频链接中提取
2. 部分敏感数据可能需要用户授权才能获取
3. 接口调用频率有限制，建议不要频繁调用单个视频接口