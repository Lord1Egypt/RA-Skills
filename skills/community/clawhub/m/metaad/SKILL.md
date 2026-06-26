---
name: meta-ads-creator
description: This skill automates the creation of Meta (Facebook/Instagram) ads using the Marketing API. It handles campaign setup, audience targeting, media upload, and ad creation in a streamlined workflow. Use this skill when users want to create Meta ads programmatically, manage ad campaigns via API, or automate their advertising workflow.
---

# Meta Ads Creator

自动化创建 Meta (Facebook/Instagram) 广告的 Skill，通过 Marketing API 实现从素材上传到广告发布的完整流程。

## 适用场景

当用户需要以下功能时触发此 Skill：
- 通过 API 自动创建 Meta 广告
- 批量创建广告系列、广告组、广告
- 程序化管理广告投放
- 自动化广告素材上传

## 前置要求

### 1. Meta 开发者账号
- 访问 https://developers.facebook.com 注册开发者账号
- 创建应用并添加 Marketing API 产品
- 生成 User Access Token

### 2. 配置信息
运行配置脚本获取所需信息：
```bash
cd .workbuddy/skills/meta-ads-creator/scripts
python config_manager.py
```

需要的信息：
- **Access Token**: Meta API 访问令牌
- **Ad Account ID**: 广告账户 ID (格式: act_123456789)
- **App ID** (可选): 应用 ID
- **App Secret** (可选): 应用密钥

### 3. 主页权限
创建广告需要 Facebook 主页 ID，确保你的账号有该主页的管理员权限。

## 使用方法

### 方式一：一键创建完整广告

使用 `create_full_ad.py` 脚本，通过 JSON 配置文件创建完整的广告结构：

```bash
python scripts/create_full_ad.py ad_config.json
```

配置文件示例 (`ad_config.json`):
```json
{
  "product_name": "夏季连衣裙",
  "daily_budget": 50,
  "campaign_name": "夏季促销2024",
  "objective": "conversions",
  "status": "PAUSED",
  "targeting": {
    "countries": ["US"],
    "age_min": 25,
    "age_max": 45,
    "genders": [2]
  },
  "ad": {
    "page_id": "YOUR_PAGE_ID",
    "message": "限时优惠！夏季新款连衣裙5折起，快来选购！",
    "headline": "夏季大促",
    "images": ["image1.jpg", "image2.jpg"],
    "link_url": "https://yourstore.com/summer-sale",
    "call_to_action": "SHOP_NOW"
  }
}
```

生成示例配置文件：
```bash
python scripts/create_full_ad.py --example
```

### 方式二：分步创建

如需更精细控制，可分步创建：

#### 1. 上传素材
```bash
python scripts/upload_media.py image1.jpg image2.jpg
```

#### 2. 创建广告系列
```bash
python scripts/create_campaign.py "广告系列名称" conversions PAUSED
```

#### 3. 创建广告组
```bash
python scripts/create_adset.py <campaign_id> "广告组名称" 5000 '{"countries":["US"],"age_min":25,"age_max":45,"genders":[2]}'
```

#### 4. 创建广告
```bash
python scripts/create_ad.py <adset_id> "广告名称" '<creative_json>'
```

### 方式三：在代码中使用

```python
from scripts.create_full_ad import create_full_ad

result = create_full_ad(
    product_name="产品名称",
    daily_budget=50,
    targeting_config={
        "countries": ["US"],
        "age_min": 25,
        "age_max": 45,
        "genders": [2]
    },
    ad_config={
        "page_id": "YOUR_PAGE_ID",
        "message": "广告文案",
        "images": ["image1.jpg"],
        "link_url": "https://example.com",
        "call_to_action": "SHOP_NOW"
    }
)
```

## 配置参数说明

### 广告目标 (Objective)
- `conversions` - 转化量 (默认)
- `traffic` - 流量
- `awareness` - 品牌知名度
- `engagement` - 互动率
- `app_installs` - 应用安装
- `lead_generation` - 潜在客户开发

### 受众定位 (Targeting)

| 参数 | 类型 | 说明 |
|------|------|------|
| `countries` | array | 国家代码，如 `["US", "CA"]` |
| `age_min` | int | 最小年龄 |
| `age_max` | int | 最大年龄 |
| `genders` | array | `[1]`=男, `[2]`=女, `[1,2]`=全部 |
| `interests` | array | 兴趣标签 ID 列表 |

### CTA 按钮
- `SHOP_NOW` - 立即购买
- `LEARN_MORE` - 了解更多
- `SIGN_UP` - 注册
- `DOWNLOAD` - 下载
- `GET_OFFER` - 获取优惠

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `config_manager.py` | 管理 API 配置 (Token、账户ID) |
| `meta_api.py` | API 基础模块，包含通用请求方法 |
| `upload_media.py` | 上传图片/视频素材 |
| `create_campaign.py` | 创建广告系列 |
| `create_adset.py` | 创建广告组 (受众、预算) |
| `create_ad.py` | 创建广告 (文案、素材) |
| `create_full_ad.py` | 一键创建完整广告 |

## 测试 API 连接

配置完成后，测试 API 连接：
```bash
python scripts/meta_api.py
```

成功后会显示：
- Token 有效性
- 广告账户信息
- 现有广告系列列表

## 注意事项

1. **默认暂停**: 所有创建的广告默认状态为 `PAUSED`，请在 Meta 广告管理器中审核后手动启用
2. **预算单位**: API 中预算以"分"为单位，如 $50 需传入 `5000`
3. **素材复用**: 相同图片上传后会获得相同 hash，避免重复上传
4. **错误处理**: 脚本会输出详细的错误信息，请根据提示检查配置

## 参考文档

- [Meta Marketing API 文档](https://developers.facebook.com/docs/marketing-api/)
- [API 限制和配额](https://developers.facebook.com/docs/marketing-api/overview/limits)
- [受众定位文档](https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting)

查看本 Skill 的 `references/meta_api.md` 获取更详细的 API 参考。
