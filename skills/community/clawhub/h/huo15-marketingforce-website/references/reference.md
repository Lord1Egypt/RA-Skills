# MarketingForce T云 API Reference - Complete

## Authentication

### Login Flow (RSA + SMS)

1. **Get RSA public key**: `GET https://api.71360.com/api/app/tcloud-sso/account/getPublicKey`
2. **Encrypt password**: RSA PKCS1 encrypt, then base64 encode
3. **Login**: `POST /tcloud-sso/account/loginCheckRsa` → returns code 206 if SMS needed
4. **Send SMS**: `GET /tcloud-sso/account/sendSecondValidPhoneSecode?loginName=&password=`
5. **Verify SMS**: `GET /tcloud-sso/account/checkSecondValidPhoneSecode?loginName=&password=&phoneSecode=`

### Token Usage

| Header | Description |
|--------|-------------|
| `X-Token` | Console session token (cookie: `.71360.com` → `X-Token`) |
| `admin-token` | Site admin token (cookie: `.marketingforce.com` → `admin_token`, format: `token_<hex>`) |

## API Base URLs

| Service | Base URL |
|---------|----------|
| SSO/Auth | `https://api.71360.com/api/app` |
| CMS | `https://api.71360.com/api/app/site-admin-api/admin_cms` |
| Site Admin | `https://api.71360.com/api/app/site-admin-api/admin` |
| Plugins | `https://api.71360.com/api/app/site-admin-api/plugin` |
| AI | `https://api.71360.com/api/app/site-admin-api/admin_ai` |
| Site/BPF | `https://api.71360.com/api/app/obor-nginx-php/tweb` |
| Console | `https://api.71360.com/api/app/aggregateservice-web/api` |
| File Upload | `https://fileupload.71360.com` |

## Complete API Endpoint List (354 endpoints)

### 1. Article Management (admin_cms/article)

| Method | Path | Description | Status |
|--------|------|-------------|--------|
| GET | `/article/getlist?type=1&rows=10&page=1&disabled=false` | List articles | ✅ |
| GET | `/article/edit?id=<id>` | Get article detail (data.info) | ✅ |
| POST | `/article/save` | Create/update article | ✅ |
| POST | `/article/remove` | Delete article | ✅ |
| POST | `/article/reduction` | Restore deleted | ✅ |
| POST | `/article/upDownBatch` | Batch publish/unpublish | ✅ |
| POST | `/article/setNodownload` | Set no-download | ✅ |
| GET | `/article/getLastAuthor` | Get last author | ✅ |
| POST | `/article/importFromGoods` | Import from product | ✅ |

Article fields: `id`, `category_id`, `title`, `summary`, `content`(HTML), `img`, `author`, `type`(1), `sort`, `disabled`, `status`(1=published,0=draft), `seo_title`, `seo_keywords`, `seo_description`, `tag_ids`

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
| GET | `/Tag/tagView` | Tag view |
| POST | `/Tag/save` | Save tag |
| POST | `/Tag/remove` | Delete |
| POST | `/Tag/saveTagInfo` | Save tag info |
| POST | `/Tag/saveTagShow` | Toggle show |
| POST | `/Tag/tagInfoDel` | Delete tag info |
| POST | `/Tag/tagSort` | Sort tags |

### 4. Product Management (admin_cms/goods)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/goods/getlist?type=2&rows=10&page=1&disabled=false` | List products |
| GET | `/goods/edit?id=<id>` | Product detail (data.info) |
| POST | `/goods/save` | Create/update |
| POST | `/goods/remove` | Delete |
| POST | `/goods/reduction` | Restore |
| POST | `/goods/upDownBatch` | Batch publish |
| POST | `/goods/uploadPackage` | Bulk import |
| POST | `/goods/importPackageGoods` | Import package |
| GET | `/goods/checkName` | Check name |

Product fields: `id`, `type_id`, `name`, `summary`, `content`(HTML), `img`, `price_sell`, `brand`, `origin`, `unit`, `pack`, `minimum`, `sort`, `disabled`, `tag_ids`, `p_5`~`p_40`(custom fields), `seo_title`, `seo_keywords`, `seo_description`

### 5. Product Categories (admin_cms/goodsType)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/goodsType/getlist?type=2` | List categories |
| GET | `/goodsType/edit?id=<id>` | Category detail |
| POST | `/goodsType/save` | Create/update |
| POST | `/goodsType/saveAll` | Batch save |
| POST | `/goodsType/remove` | Delete |

### 6. Product Tags/Tabs (admin_cms/goodsTab)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/goodsTab/getlist?type=2` | List tabs |
| GET | `/goodsTab/getAttrList` | Get attributes |
| POST | `/goodsTab/save` | Save |
| POST | `/goodsTab/remove` | Delete |
| POST | `/goodsTab/sortAll` | Sort all |

### 7. Short Video Management (admin_cms/DyVideo, admin_cms/dyVideo)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/DyVideo/sVideoList?rows=10&page=1` | List videos |
| POST | `/DyVideo/saveSvideo` | Save video |
| POST | `/DyVideo/removeVideo` | Delete video |
| GET | `/DyVideo/getMbSaveSvideoQrCode` | Get QR code |
| GET | `/dyVideo/svideoStatus` | Video status |
| GET | `/dyVideo/adminWebVideoInfo` | Web video info |
| GET | `/dyVideo/adminWebVideoEditInfo` | Edit info |
| GET | `/dyVideo/getQvideoStatus` | Q video status |

### 8. Douyin User Management (admin/DyVideoUser)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/DyVideoUser/getUserList` | List users |
| GET | `/DyVideoUser/getFansList` | Fans list |
| GET | `/DyVideoUser/getFollowList` | Follow list |
| POST | `/DyVideoUser/removeUser` | Remove user |

### 9. Recommendation - Keywords (admin/keyword)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/keyword/list?rows=10&page=1` | List keywords |
| GET | `/keyword/contentList` | Content list |
| GET | `/keyword/relationList` | Relations |
| GET | `/keyword/selTag` | Select tags |
| POST | `/keyword/save` | Save |
| POST | `/keyword/remove` | Delete |
| POST | `/keyword/sort` | Sort |
| POST | `/keyword/relationContent` | Relate content |
| POST | `/keyword/relationRemove` | Remove relation |
| POST | `/keyword/relationSort` | Sort relations |

### 10. Recommendation - Anchor Points (admin_cms/AnchorPoint)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/AnchorPoint/anchorList?rows=10&page=1` | List anchors |
| POST | `/AnchorPoint/addAnchor` | Add anchor |
| POST | `/AnchorPoint/editAnchor` | Edit |
| POST | `/AnchorPoint/delAnchor` | Delete |
| POST | `/AnchorPoint/useAnchor` | Toggle |
| POST | `/AnchorPoint/handAddPoint` | Manual add |
| POST | `/AnchorPoint/addAnchorToWord` | Add to word |

### 11. Forms/Inquiries (admin/form)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/form/getlist?rows=10&page=1` | List forms |
| GET | `/form/getRow?id=<id>` | Form detail |
| POST | `/form/save` | Save form |
| POST | `/form/setField` | Set fields |
| POST | `/form/removeForm` | Delete form |
| GET | `/form/msglist?rows=10&page=1` | Messages |
| GET | `/form/msglist2?rows=10&page=1` | Messages (alt) |
| GET | `/form/msgCount` | Stats (total, thisMonth, preMonth) |
| POST | `/form/readMsg` | Mark read |
| POST | `/form/removeMsg` | Delete message |
| GET | `/form/msgExport` | Export |
| GET | `/form/exportFile2` | Export all |
| GET | `/form/xyslist?rows=10&page=1` | XYS forms |
| GET | `/form/xysMsglist?rows=10&page=1` | XYS messages |
| GET | `/form/xysMsgInfo` | XYS detail |
| POST | `/form/xysSave` | Save XYS |
| GET | `/form/xysExportFile` | Export XYS |

### 12. Resource Library - Images (admin/image)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/image?rows=10&page=1` | List images |
| GET | `/image/dirTree` | Directory tree |
| POST | `/image/mkdir` | Create folder |
| POST | `/image/imageUpload` | Upload image |
| POST | `/image/move` | Move image |
| POST | `/image/rename` | Rename |
| POST | `/image/remove` | Delete |

### 13. Albums (admin_cms/album)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/album/getlist?rows=10&page=1` | List albums |
| GET | `/album/getRow?id=<id>` | Album detail |
| POST | `/album/save` | Save |
| POST | `/album/remove` | Delete |
| POST | `/album/reduction` | Restore |

### 14. File Upload (file)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/file/cos/auth` | Get COS auth |
| GET | `/file/cos/finish` | Confirm upload |
| POST | `/file/upload` | Upload file |
| GET | `/file/Template` | Template file |
| GET | `/file/filesearchmodel` | Search model |
| GET | `/file/judgeProduct` | Judge product |

### 15. Site Settings - Base Config (admin/SysConfig)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/SysConfig/siteConfig` | Site config (title, ico, keywords, verify, no_copy) |
| GET | `/SysConfig/getBaseConfig` | Base config |
| POST | `/SysConfig/setBaseConfig` | Update config |
| GET | `/SysConfig/seoParams` | SEO params (10 items) |
| GET | `/SysConfig/seoTkd` | TKD settings |
| GET | `/SysConfig/mailConfig` | Mail config |
| GET | `/SysConfig/mailTemplateList` | Mail templates |
| POST | `/SysConfig/mailTemplate` | Save template |
| POST | `/SysConfig/mailTest` | Test mail |
| GET | `/SysConfig/pushSwitchGet` | Push settings |
| POST | `/SysConfig/pushSwitchSet` | Update push |
| POST | `/SysConfig/editForm` | Edit form |
| POST | `/SysConfig/goodsBackgroundConfig` | Goods background |

### 16. Site Settings - Customer Service (admin/Sysconfig)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/Sysconfig/getCustomerService` | CS config (position, style, WeChat, QQ, etc.) |
| POST | `/Sysconfig/setCustomerService` | Update CS |
| POST | `/Sysconfig/sortCustomerService` | Sort CS |
| GET | `/Sysconfig/botConfig` | Bot config |
| GET | `/Sysconfig/anchorConfig` | Anchor config |
| POST | `/Sysconfig/setStyle` | Set style |
| GET | `/Sysconfig/isShow` | Show status |
| GET | `/Sysconfig/talkIsShow` | Talk show |
| GET | `/Sysconfig/ztbIsShow` | ZTB show |
| GET | `/Sysconfig/qrCodeConfig` | QR config |

### 17. Navigation (admin/navigation)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/navigation` | List nav (14 items) |
| POST | `/navigation/create` | Create item |
| POST | `/navigation/update` | Update |
| POST | `/navigation/remove` | Delete |
| POST | `/navigation/saveNav` | Save all |
| GET | `/navigation/detail` | Detail |
| POST | `/navigation/copyNavigation` | Copy |
| POST | `/navigation/quickSwitch` | Quick switch |
| POST | `/navigation/setLevel` | Set level |

### 18. Theme (admin/theme)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/theme` | Current theme |
| GET | `/theme/mbList` | Mobile themes |
| GET | `/theme/PhoneThemeList` | Phone themes |
| POST | `/theme/chooseTheme` | Switch theme |
| POST | `/theme/edit` | Edit theme |
| POST | `/theme/mbChoose` | Choose mobile |
| POST | `/theme/mbEdit` | Edit mobile |
| POST | `/theme/delMbTemplet` | Delete mobile |
| POST | `/theme/delXysTemplet` | Delete XYS |
| POST | `/theme/addXysTp` | Add XYS |
| GET | `/theme/isChangeTheme` | Check change |

### 19. Page & Menu (admin/page, admin/menu)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/page` | Page settings |
| GET | `/menu/getlist` | Menu list (15 items) |

### 20. SEO - Keywords (admin/Words)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/Words/keyWords` | All keywords (120) |
| GET | `/Words/wordsList?rows=10&page=1` | Paginated |
| GET | `/Words/wordsNum` | Stats (now_num, words_num, words_add) |
| GET | `/Words/forbiddenWords` | Forbidden words |
| POST | `/Words/saveWords` | Save keyword |
| POST | `/Words/removeWords` | Delete |
| POST | `/Words/intoWords` | Import |
| POST | `/Words/submitDetection` | Detect |
| GET | `/Words/getInfoByUrl` | URL info |
| POST | `/Words/createTable` | Create table |

### 21. SEO - Extract (admin/seoExtract)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/seoExtract/title` | Extract title |
| GET | `/seoExtract/keywords` | Extract keywords |
| GET | `/seoExtract/description` | Extract description |

### 22. SEO - Site Score (admin/SiteScore)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/SiteScore/status` | Score status |
| GET | `/SiteScore/evaluate` | Evaluation |
| POST | `/SiteScore/close` | Close |

### 23. Spider Analytics (admin/Spider)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/Spider/hotTop` | Hot pages (top 10: spider_cnt_sum, title, url, included) |
| GET | `/Spider/trendData` | Trend (list, lastList) |
| GET | `/Spider/trendDataAverage` | Average (yesterday, thirty: num, average) |
| GET | `/spider/getTop` | Top pages |

### 24. Dashboard/Home (admin/home)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/home/siteSettingState` | Setup completion |
| GET | `/home/statistics` | Content stats (goods, article counts) |
| GET | `/home/statisticalArticles` | Article stats |
| GET | `/home/taskList` | Task overview |
| GET | `/home/siteDiag` | Site diagnostic |
| GET | `/home/guide` | Setup guide |
| GET | `/home/domainRemain` | Domain remaining |
| GET | `/home/getQrcode` | QR code |
| GET | `/home/saasBanner` | SaaS banner |
| POST | `/home/refreshConf` | Refresh cache |
| POST | `/home/allClearCatch` | Clear cache |
| POST | `/home/setLoginTime` | Set login time |
| POST | `/home/updateWordsStatus` | Update words |
| GET | `/home/health` | Health check |

### 25. Plugins (plugin)

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/floatvideo/get\|set` | Floating video |
| GET/POST | `/floatphonebottom/get\|set` | Floating phone menu |
| GET/POST | `/baidushare/get\|set` | Baidu share |
| GET/POST | `/bizqq/get\|setqq` | Business QQ |
| GET/POST | `/location/get\|set` | Location |
| GET/POST | `/xiongzhang/get\|set` | Xiongzhang |
| GET/POST | `/Xysen/floatqq` | XYS float QQ |
| GET/POST | `/Xysen/sharebtn` | XYS share |
| GET/POST | `/ByteDanceVerify/get\|set` | ByteDance verify |

### 26. Multi-Language (admin/language, admin/SyncData, admin/translateZh)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/language/getLangs` | Available languages |
| GET | `/language/list` | Active languages |
| GET | `/SyncData/getLanguages` | Sync languages |
| GET | `/SyncData/list` | Sync list |
| GET | `/SyncData/total` | Sync total |
| POST | `/SyncData/batchTranslate` | Batch translate |
| POST | `/SyncData/openStatus` | Toggle |
| POST | `/SyncData/tagTrans` | Translate tags |
| GET | `/translateZh/toTranslate` | To Chinese |
| GET | `/translateZh/ensiteInfo` | English site |

### 27. User Center (admin/ucenterConfig, admin/ucenterMember)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/ucenterConfig/loginConfig` | Login config |
| GET | `/ucenterConfig/registerConfig` | Registration |
| GET | `/ucenterConfig/privacyConfig` | Privacy |
| GET | `/ucenterConfig/smsConfig` | SMS |
| GET | `/ucenterConfig/smsEquity` | SMS equity |
| GET | `/ucenterMember/list` | Member list |
| GET | `/ucenterMember/rankList` | Ranks |
| POST | `/ucenterMember/add` | Add member |
| POST | `/ucenterMember/remove` | Remove |
| POST | `/ucenterMember/rankEdit` | Edit rank |
| POST | `/ucenterMember/updateUserRank` | Update rank |

### 28. AI Functions (admin_ai, admin_cms/AiExtract, admin_cms/AiArticle)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin_ai/taskList` | AI task list |
| GET | `/admin_ai/taskDetail` | Task detail |
| POST | `/admin_ai/saveTask` | Save task |
| GET | `/admin_cms/AiExtract/index` | Extract list |
| GET | `/admin_cms/AiExtract/getTask` | Get task |
| POST | `/admin_cms/AiExtract/createTask` | Create |
| POST | `/admin_cms/AiExtract/save` | Save |
| GET | `/admin_cms/AiExtract/detail` | Detail |
| POST | `/admin_cms/AiExtract/delete` | Delete |
| GET | `/admin_cms/AiArticle/getDetail` | Article detail |
| GET | `/admin_cms/AiArticle/lastInfo` | Last article |

### 29. System (admin/System)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/System/getLogList?rows=10&page=1` | Operation logs |
| GET | `/System/backupList` | Backups |
| POST | `/System/addBackup` | Create backup |
| POST | `/System/removeBackup` | Remove |
| POST | `/System/restore` | Restore |
| GET | `/System/exportLog` | Export logs |
| GET | `/System/backupLog` | Backup log |
| POST | `/System/backupRemark` | Remark |

### 30. Site/Template Management (tweb)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/site/weblist` | All websites |
| GET | `/site/get` | Current site |
| POST | `/site/set` | Update |
| GET | `/site/themeInfo` | Theme info |
| GET | `/site/siteParams` | Parameters |
| POST | `/site/setSiteParams` | Update params |
| GET | `/site/inline` | Inline status |
| GET | `/site/build` | Build site |
| GET | `/site/active` | Active |
| GET | `/site/getDesktopUrl` | Desktop URL |
| POST | `/site/bindProductID` | Bind product |
| GET | `/pub/tplist?page=1&rows=10` | Templates (968+) |
| GET | `/pub/industryList` | Industries |
| GET | `/pub/colorlist` | Colors |
| GET | `/pub/funcTagList` | Function tags |
| GET | `/pub/getAvailableServices` | Services |
| GET | `/pub/getPlusRole` | Plus role |
| GET | `/pub/mbqrcode` | QR code |

### 31. Statistics (tweb/statistic, admin/home)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/statistic/getCount` | Visit count |
| GET | `/statistic/getDataByHour` | Hourly |
| GET | `/statistic/getDataBydate` | Daily |
| GET | `/statistic/pagetopn` | Top pages |
| GET | `/admin/home/statistics` | Content stats |

### 32. Recruitment (admin/information, admin/resume, admin/job)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/information/list` | Job list |
| GET | `/information/detail?id=<id>` | Job detail |
| POST | `/information/add` | Add job |
| POST | `/information/edit` | Edit |
| POST | `/information/remove` | Delete |
| GET | `/information/degree` | Degrees |
| POST | `/information/import` | Import |
| GET | `/information/permission` | Permission |
| GET | `/information/recordList` | Records |
| GET | `/resume/list` | Resume list |
| GET | `/resume/detail` | Resume detail |
| POST | `/resume/deal` | Process |
| POST | `/resume/remove` | Delete |
| GET | `/resume/resumeColumn` | Columns |
| GET | `/resume/exportResume` | Export |
| GET | `/job/index` | Job index |
| POST | `/job/create` | Create |
| GET | `/job/detail` | Detail |
| POST | `/job/enable` | Enable |
| POST | `/job/remove` | Remove |

### 33. Other Admin APIs

| Method | Path | Description |
|--------|------|-------------|
| GET | `/admin/SysConfig/goodsBackgroundConfig` | Goods bg |
| GET | `/admin/ReplaceWords/replaceWords` | Replace words |
| GET | `/admin/businessRadar/list` | Business radar |
| GET | `/admin/visual/anchor` | Visual anchor |
| GET | `/admin/platformInfo` | Platform info |
| GET | `/admin/tsite/getlist` | T-site list |
| POST | `/admin/tsite/save` | Save T-site |
| GET | `/admin/ZtbConfig/getDeptList` | ZTB depts |
| GET | `/admin/ZtbConfig/getEmployList` | Employees |

### 34. Mini Program (admin/xcx, admin/Xcx, tweb/xcxManage)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/xcx/index` | XCX index |
| GET | `/xcx/getQrcode` | QR code |
| POST | `/xcx/authorize` | Authorize |
| POST | `/xcx/commit` | Commit |
| POST | `/xcx/release` | Release |
| POST | `/xcx/submitAudit` | Submit audit |
| POST | `/xcx/modify` | Modify |
| GET | `/Xcx/create` | Create |
| GET | `/Xcx/xcxInfo` | Info |
| GET | `/xcxManage/goodsTypelist` | Goods types |
| POST | `/xcxManage/goodsSave` | Save goods |
| GET | `/xcxManage/goodsdetail` | Goods detail |

### 35. English Site (tweb/enSite, tweb/enTheme, tweb/EnTheme)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/enSite/lists` | English sites |
| POST | `/enSite/addLanguage` | Add language |
| POST | `/enSite/bindingPc` | Bind PC |
| GET | `/enTheme/lists` | English themes |
| POST | `/EnTheme/changeTemplate` | Change template |

## Environment Variables (from JS)

| Variable | Value |
|----------|-------|
| VUE_APP_BASE_API | `https://api.71360.com/api/app` |
| VUE_APP_BASE_API_BPF | `https://api.71360.com/api/app/obor-nginx-php/` |
| VUE_APP_BASE_API_PC | `https://tyunclient.71360.com/` |
| VUE_APP_STATION | `https://api.71360.com/api/app/site-admin-api/` |
| VUE_APP_JZ_HOME | `https://siteadmin.marketingforce.com/` |
| VUE_APP_TYUN_DOMAIN | `https://tyun.71360.com/` |
| VUE_APP_DOWNLOADTEMPLATE | `https://siteadminapi.71360.com/` |

## Key URLs

| Purpose | URL |
|---------|-----|
| Console Login | https://console.marketingforce.com/login/login |
| Site Admin | https://siteadmin.marketingforce.com/ |
| T云 Console | https://tyun.marketingforce.com/buildPlatform/index |
| Website | https://www.uwtsd.com |
| Official Site | https://www.marketingforce.com |
