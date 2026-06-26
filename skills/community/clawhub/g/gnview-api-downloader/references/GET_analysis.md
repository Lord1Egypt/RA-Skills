### GET /api/analysis
**Summary**: 通过大模型，分析抖音视频结构

**Description**:

## 返回:
- 返回分析结果响应。

# [示例/Example]
url: https://www.bilibili.com/video/BV1U5efz2Egn
text：分析视频脚本，提取分镜信息

**Parameters**:
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| url | string | 是 | 视频或图片的URL地址，支持抖音|TikTok|Bilibili的分享链接，例如：https://v.douyin.com/e4J8Q7A/ 或 https://www.bilibili.com/video/BV1xxxxxxxxx |
| text | string | 是 | 大模型分析指令 |