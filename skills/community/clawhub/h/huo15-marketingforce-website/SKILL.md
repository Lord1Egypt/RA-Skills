---
name: huo15-marketingforce-website
displayName: T云建站技能
description: >-
  通过 CMS API 管理和编辑迈富时(T云/MarketingForce)网站内容。全功能覆盖：文章管理、
  产品管理、分类标签、短视频管理、推荐管理、营销互动/询盘、资源库、网站设置、SEO功能、
  蜘蛛分析、导航主题、插件管理、多语言、AI工具、系统管理等 20+ 模块 354 个 API 端点。
  当用户说"编辑官网""发文章""改产品""看询盘""SEO优化""蜘蛛分析""T云建站"
  "siteadmin""uwtsd"等网站管理意图时使用。凭据在 scripts/.env，脚本 scripts/mf_client.py。
---

# T云建站技能 (MarketingForce Website Editor)

全功能管理 MarketingForce T云建站平台网站，通过 CMS API 操作 20+ 模块 354 个端点。

## Authentication

Two tokens required as headers on every request:

| Header | Source |
|--------|--------|
| `X-Token` | Browser DevTools → Cookies → `.71360.com` → `X-Token` |
| `admin-token` | Browser DevTools → Cookies → `.marketingforce.com` → `admin_token` (format: `token_<hex>`) |

Tokens expire. If API returns `401`, ask user to re-login at `https://console.marketingforce.com/login/login`.

## Quick Start

```bash
python3 scripts/mf_client.py test           # Verify tokens
python3 scripts/mf_client.py sites          # List websites
python3 scripts/mf_client.py articles       # List articles
python3 scripts/mf_client.py article 103    # Article detail
python3 scripts/mf_client.py categories     # Article categories
python3 scripts/mf_client.py products       # List products
python3 scripts/mf_client.py product-cats   # Product categories
python3 scripts/mf_client.py videos         # Short videos
python3 scripts/mf_client.py inquiries      # Inquiry messages
python3 scripts/mf_client.py seo-keywords   # SEO keywords
python3 scripts/mf_client.py spider         # Spider analytics
python3 scripts/mf_client.py navigation     # Nav menu
python3 scripts/mf_client.py site-config    # Site config
python3 scripts/mf_client.py dashboard      # Home dashboard
python3 scripts/mf_client.py plugins        # Plugin settings
python3 scripts/mf_client.py templates      # Site templates
python3 scripts/mf_client.py images         # Image library
python3 scripts/mf_client.py anchors        # Anchor points
python3 scripts/mf_client.py system-logs    # System logs
```

## API Base URLs

| Service | Base URL |
|---------|----------|
| CMS | `https://api.71360.com/api/app/site-admin-api/admin_cms` |
| Site Admin | `https://api.71360.com/api/app/site-admin-api/admin` |
| Site/BPF | `https://api.71360.com/api/app/obor-nginx-php/tweb` |
| Console | `https://api.71360.com/api/app/aggregateservice-web/api` |
| Plugins | `https://api.71360.com/api/app/site-admin-api/plugin` |
| AI | `https://api.71360.com/api/app/site-admin-api/admin_ai` |
| File | `https://api.71360.com/api/app/site-admin-api/file` |

## Module Reference

### 1. Article Management (文章管理)
Base: `/admin_cms/article`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/article/getlist?type=1&rows=10&page=1&disabled=false` | List articles |
| GET | `/article/edit?id=<id>` | Get article detail (data.info) |
| POST | `/article/save` | Create/update article |
| POST | `/article/remove` | Delete article |
| POST | `/article/reduction` | Restore deleted |
| POST | `/article/upDownBatch` | Batch publish/unpublish |
| POST | `/article/setNodownload` | Set no-download flag |
| GET | `/article/getLastAuthor` | Get last author |
| POST | `/article/importFromGoods` | Import from product |

Article fields: `id`, `category_id`, `title`, `summary`, `content`(HTML), `img`, `author`, `type`(1=article), `sort`, `disabled`, `status`(1=published,0=draft), `seo_title`, `seo_keywords`, `seo_description`, `tag_ids`

### 2. Article Categories (admin_cms/category)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/category/getlist?type=1` | List categories |
| GET | `/category/edit?id=<id>` | Category detail |
| POST | `/category/save` | Create/update |
| POST | `/category/saveAll` | Batch save |
| POST | `/category/remove` | Delete |

### 3. Tags (admin_cms/Tag)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/Tag/getList` | List tags |
| GET | `/Tag/selTag` | Select tags |
| POST | `/Tag/save` | Save tag |
| POST | `/Tag/remove` | Delete |
| POST | `/Tag/saveTagInfo` | Save tag info |
| POST | `/Tag/saveTagShow` | Toggle show |
| POST | `/Tag/tagSort` | Sort tags |

### 4. Product Management (产品管理)
Base: `/admin_cms/goods`, `/admin_cms/goodsType`, `/admin_cms/goodsTab`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/goods/getlist?type=2&rows=10&page=1&disabled=false` | List products |
| GET | `/goods/edit?id=<id>` | Product detail (data.info) |
| POST | `/goods/save` | Create/update |
| POST | `/goods/remove` | Delete |
| POST | `/goods/reduction` | Restore |
| POST | `/goods/upDownBatch` | Batch publish |
| POST | `/goods/uploadPackage` | Bulk import |
| GET | `/goodsType/getlist?type=2` | List product categories |
| GET | `/goodsType/edit?id=<id>` | Category detail |
| POST | `/goodsType/save` | Create/update |
| POST | `/goodsType/remove` | Delete |
| GET | `/goodsTab/getlist?type=2` | List product tags |
| GET | `/goodsTab/getAttrList` | Get attributes |
| POST | `/goodsTab/save` | Save tag |
| POST | `/goodsTab/remove` | Delete |

Product fields: `id`, `type_id`, `name`, `summary`, `content`(HTML), `img`, `price_sell`, `brand`, `origin`, `unit`, `sort`, `disabled`, `tag_ids`, `p_5`~`p_40`(custom fields)

### 5. Short Video Management (短视频管理)
Base: `/admin_cms/DyVideo`, `/admin/DyVideoUser`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/DyVideo/sVideoList?rows=10&page=1` | List short videos |
| POST | `/DyVideo/saveSvideo` | Save video |
| POST | `/DyVideo/removeVideo` | Delete video |
| GET | `/DyVideo/getMbSaveSvideoQrCode` | Get QR code |
| GET | `/dyVideo/svideoStatus` | Video status |
| GET | `/dyVideo/adminWebVideoInfo` | Web video info |
| GET | `/DyVideoUser/getUserList` | List Douyin users |
| GET | `/DyVideoUser/getFansList` | Fans list |
| POST | `/DyVideoUser/removeUser` | Remove user |

### 6. Recommendation Management (推荐管理)
Base: `/admin/keyword`, `/admin_cms/AnchorPoint`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/keyword/list?rows=10&page=1` | List keywords |
| GET | `/keyword/selTag` | Select tags |
| POST | `/keyword/save` | Save keyword |
| POST | `/keyword/remove` | Delete keyword |
| POST | `/keyword/sort` | Sort keywords |
| POST | `/keyword/relationContent` | Relate to content |
| GET | `/AnchorPoint/anchorList?rows=10&page=1` | List anchor points |
| POST | `/AnchorPoint/addAnchor` | Add anchor |
| POST | `/AnchorPoint/editAnchor` | Edit anchor |
| POST | `/AnchorPoint/delAnchor` | Delete anchor |
| POST | `/AnchorPoint/useAnchor` | Enable/disable |

### 7. Marketing/Forms (营销互动/询盘管理)
Base: `/admin/form`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/form/getlist?rows=10&page=1` | List forms |
| GET | `/form/getRow?id=<id>` | Form detail |
| POST | `/form/save` | Save form config |
| POST | `/form/setField` | Set form fields |
| POST | `/form/removeForm` | Delete form |
| GET | `/form/msglist?rows=10&page=1` | List form messages |
| GET | `/form/msglist2?rows=10&page=1` | Messages (alt) |
| GET | `/form/msgCount` | Message statistics |
| POST | `/form/readMsg` | Mark as read |
| POST | `/form/removeMsg` | Delete message |
| GET | `/form/msgExport` | Export messages |
| GET | `/form/xyslist` | XYS form list |
| GET | `/form/xysMsglist` | XYS messages |
| POST | `/form/xysSave` | Save XYS form |

### 8. Resource Library (资源库)
Base: `/admin/image`, `/admin_cms/album`, `/file`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/image?rows=10&page=1` | List images |
| GET | `/image/dirTree` | Directory tree |
| POST | `/image/mkdir` | Create folder |
| POST | `/image/imageUpload` | Upload image |
| POST | `/image/move` | Move image |
| POST | `/image/remove` | Delete |
| GET | `/album/getlist?rows=10&page=1` | List albums |
| GET | `/album/getRow?id=<id>` | Album detail |
| POST | `/album/save` | Save album |
| POST | `/album/remove` | Delete album |
| GET | `/file/cos/auth` | Get COS upload auth |
| POST | `/file/upload` | Upload file |

### 9. Site Settings (网站设置)
Base: `/admin/SysConfig`, `/admin/Sysconfig`, `/admin/navigation`, `/admin/theme`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/SysConfig/siteConfig` | Site config (title, ico, keywords, verify) |
| POST | `/SysConfig/setBaseConfig` | Update config |
| GET | `/SysConfig/seoParams` | SEO parameters |
| GET | `/SysConfig/seoTkd` | TKD settings |
| GET | `/SysConfig/mailConfig` | Mail config |
| GET | `/SysConfig/mailTemplateList` | Mail templates |
| GET | `/Sysconfig/getCustomerService` | Customer service config |
| POST | `/Sysconfig/setCustomerService` | Update CS config |
| GET | `/Sysconfig/botConfig` | Bot config |
| GET | `/navigation` | Navigation menu |
| POST | `/navigation/create` | Create nav item |
| POST | `/navigation/update` | Update nav |
| POST | `/navigation/saveNav` | Save full nav |
| GET | `/theme` | Current theme |
| GET | `/theme/mbList` | Mobile themes |
| POST | `/theme/chooseTheme` | Switch theme |
| GET | `/menu/getlist` | Page menu list |

### 10. SEO Functions (SEO功能)
Base: `/admin/Words`, `/admin/seoExtract`, `/admin/SiteScore`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/Words/keyWords` | All keywords |
| GET | `/Words/wordsList?rows=10&page=1` | Paginated keywords |
| GET | `/Words/wordsNum` | Keyword stats |
| GET | `/Words/forbiddenWords` | Forbidden words |
| POST | `/Words/saveWords` | Save keyword |
| POST | `/Words/removeWords` | Delete keyword |
| POST | `/Words/intoWords` | Import keywords |
| GET | `/seoExtract/title` | Extract SEO title |
| GET | `/seoExtract/keywords` | Extract keywords |
| GET | `/seoExtract/description` | Extract description |
| GET | `/SiteScore/status` | Score status |
| GET | `/SiteScore/evaluate` | Site evaluation |

### 11. Spider Analytics (蜘蛛分析)
Base: `/admin/Spider`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/Spider/hotTop` | Hot pages (top 10) |
| GET | `/Spider/trendData` | Trend data |
| GET | `/Spider/trendDataAverage` | Average (yesterday, 30 days) |
| GET | `/spider/getTop` | Top pages |

### 12. Dashboard (首页概况)
Base: `/admin/home`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/home/siteSettingState` | Setup completion |
| GET | `/home/statistics` | Content stats |
| GET | `/home/taskList` | Task overview |
| GET | `/home/siteDiag` | Site diagnostic |
| POST | `/home/refreshConf` | Refresh cache |
| POST | `/home/allClearCatch` | Clear cache |

### 13. Plugins (插件管理)
Base: `/plugin`

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/floatvideo/get\|set` | Floating video |
| GET/POST | `/floatphonebottom/get\|set` | Floating phone menu |
| GET/POST | `/baidushare/get\|set` | Baidu share |
| GET/POST | `/bizqq/get\|setqq` | Business QQ |
| GET/POST | `/location/get\|set` | Location |
| GET/POST | `/xiongzhang/get\|set` | Xiongzhang |
| GET/POST | `/ByteDanceVerify/get\|set` | ByteDance verify |

### 14. Multi-Language, User Center, AI, System
See references/reference.md for complete API list of:
- Multi-language (`/admin/language`, `/admin/SyncData`)
- User center (`/admin/ucenterConfig`, `/admin/ucenterMember`)
- AI functions (`/admin_ai`, `/admin_cms/AiExtract`)
- System (`/admin/System` - logs, backups)
- Templates (`/tweb/pub/tplist` - 968+ templates)
- Statistics (`/tweb/statistic`)

## Token Storage

`scripts/.env` (gitignored, not committed):
```
MF_X_TOKEN=<token>
MF_ADMIN_TOKEN=token_<hex>
```

## Safety Rules

- **Always backup** content before editing
- **Be idempotent**: search before create
- **Preview before publish**: set `status: 0` (draft) first
- Don't delete without confirmation — prefer `disabled: "true"`
- Sanitize user-provided HTML

## Additional Resources

- For complete 354-endpoint API reference, see [references/reference.md](references/reference.md)
