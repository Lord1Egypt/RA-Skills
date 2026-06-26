# Meta Marketing API 参考文档

## API 基础信息

- **Base URL**: `https://graph.facebook.com/{API_VERSION}/`
- **当前版本**: v18.0
- **文档**: https://developers.facebook.com/docs/marketing-api/

## 认证

所有请求需要 Access Token:

```
Authorization: Bearer {ACCESS_TOKEN}
```

或使用 URL 参数:
```
?access_token={ACCESS_TOKEN}
```

## 核心对象层级

```
Ad Account (act_xxx)
  └── Campaign
        └── Ad Set
              └── Ad
                    └── Creative
```

## 常用 API 端点

### 广告账户

| 操作 | 端点 | 方法 |
|------|------|------|
| 获取账户信息 | `/{ad_account_id}` | GET |
| 获取广告系列 | `/{ad_account_id}/campaigns` | GET |
| 创建广告系列 | `/{ad_account_id}/campaigns` | POST |
| 创建广告组 | `/{ad_account_id}/adsets` | POST |
| 创建广告 | `/{ad_account_id}/ads` | POST |
| 上传图片 | `/{ad_account_id}/adimages` | POST |
| 上传视频 | `/{ad_account_id}/advideos` | POST |

### 广告系列 (Campaign)

```json
{
  "name": "Campaign Name",
  "objective": "CONVERSIONS",
  "status": "PAUSED",
  "special_ad_categories": []
}
```

**目标类型 (Objective)**:
- `BRAND_AWARENESS` - 品牌知名度
- `REACH` - 覆盖人数
- `TRAFFIC` - 流量
- `ENGAGEMENT` - 互动率
- `APP_INSTALLS` - 应用安装
- `VIDEO_VIEWS` - 视频观看量
- `LEAD_GENERATION` - 潜在客户开发
- `CONVERSIONS` - 转化量
- `CATALOG_SALES` - 目录促销
- `MESSAGES` - 消息互动

### 广告组 (Ad Set)

```json
{
  "campaign_id": "123456789",
  "name": "Ad Set Name",
  "daily_budget": 5000,
  "targeting": {
    "geo_locations": {
      "countries": ["US"]
    },
    "age_min": 25,
    "age_max": 45,
    "genders": [2]
  },
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "billing_event": "IMPRESSIONS",
  "status": "PAUSED"
}
```

**预算单位**: 分（如 $50 = 5000）

**优化目标 (Optimization Goal)**:
- `IMPRESSIONS` - 展示次数
- `REACH` - 覆盖人数
- `LINK_CLICKS` - 链接点击
- `LANDING_PAGE_VIEWS` - 落地页浏览
- `OFFSITE_CONVERSIONS` - 站外转化
- `VALUE` - 价值优化
- `THRUPLAY` - 完整播放

**计费事件 (Billing Event)**:
- `IMPRESSIONS` - 按展示计费
- `LINK_CLICKS` - 按点击计费
- `THRUPLAY` - 按完整播放计费

### 受众定位 (Targeting)

```json
{
  "geo_locations": {
    "countries": ["US", "CA"],
    "regions": [{"key": "region_key"}],
    "cities": [{"key": "city_key", "radius": 10, "distance_unit": "mile"}]
  },
  "age_min": 18,
  "age_max": 65,
  "genders": [1, 2],
  "interests": [
    {"id": "6003139266461", "name": "Online shopping"}
  ],
  "behaviors": [
    {"id": "6071631541183", "name": "Engaged Shoppers"}
  ],
  "custom_audiences": [{"id": "123456789"}],
  "excluded_custom_audiences": [{"id": "987654321"}]
}
```

**性别**:
- `1` - 男性
- `2` - 女性

### 广告 (Ad)

```json
{
  "adset_id": "123456789",
  "name": "Ad Name",
  "creative": {
    "name": "Creative Name",
    "object_story_spec": {
      "page_id": "YOUR_PAGE_ID",
      "link_data": {
        "message": "广告文案",
        "image_hash": "IMAGE_HASH",
        "link": "https://example.com",
        "name": "标题",
        "description": "描述",
        "call_to_action": {
          "type": "SHOP_NOW"
        }
      }
    }
  },
  "status": "PAUSED"
}
```

**CTA 按钮类型**:
- `SHOP_NOW` - 立即购买
- `LEARN_MORE` - 了解更多
- `SIGN_UP` - 注册
- `DOWNLOAD` - 下载
- `BOOK_TRAVEL` - 预订行程
- `CONTACT_US` - 联系我们
- `GET_OFFER` - 获取优惠
- `GET_QUOTE` - 获取报价
- `SUBSCRIBE` - 订阅
- `WATCH_MORE` - 观看更多
- `SEND_MESSAGE` - 发送消息
- `APPLY_NOW` - 立即申请

### 素材上传

**图片上传**:
```bash
curl -X POST \
  "https://graph.facebook.com/v18.0/{ad_account_id}/adimages" \
  -F "access_token={ACCESS_TOKEN}" \
  -F "file=@image.jpg"
```

返回:
```json
{
  "images": {
    "image_hash": {
      "hash": "image_hash",
      "url": "https://..."
    }
  }
}
```

**视频上传**:
```bash
curl -X POST \
  "https://graph.facebook.com/v18.0/{ad_account_id}/advideos" \
  -F "access_token={ACCESS_TOKEN}" \
  -F "file=@video.mp4" \
  -F "name=Video Name"
```

## 错误处理

常见错误码:

| 错误码 | 说明 |
|--------|------|
| 200 | 权限不足 |
| 80004 | 超出请求限制 |
| 100 | 无效参数 |
| 1487442 | 广告账户未验证 |
| 1885183 | 无效的目标受众 |

## 限制和配额

- **API 调用限制**: 每 3600 秒 200 次调用 / 用户
- **批量请求**: 支持，最多 50 个操作
- **素材限制**:
  - 图片: 最大 8MB
  - 视频: 最大 4GB

## 最佳实践

1. **测试环境**: 使用 `sandbox` 模式测试
2. **错误重试**: 实现指数退避重试机制
3. **日志记录**: 记录所有 API 调用和响应
4. **状态管理**: 广告创建后默认设为 PAUSED，审核后再启用
5. **素材复用**: 相同素材使用相同 hash，避免重复上传
