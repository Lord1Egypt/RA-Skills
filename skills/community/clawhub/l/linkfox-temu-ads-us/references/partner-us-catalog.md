# Partner US — Ads 接口目录

Partner Platform for US 菜单：**Ads**（`menu_code=1e72b5cceef545ec8f9652b9e56dd054`）。

## 已接入（7）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| `dfff26bad8e94ed5abaaf5cdade50c26` | `temu.searchrec.ad.roas.pred` | `us_ads_searchrec_ad_roas_pred.py` | [temu-searchrec-ad-roas-pred.md](./apis/temu-searchrec-ad-roas-pred.md) |
| `595f05856989480aa03abd58da203047` | `temu.searchrec.ad.reports.mall.query` | `us_ads_searchrec_ad_reports_mall_query.py` | [temu-searchrec-ad-reports-mall-query.md](./apis/temu-searchrec-ad-reports-mall-query.md) |
| `7bc9231776304158a895e41a816b7805` | `temu.searchrec.ad.create` | `us_ads_searchrec_ad_create.py` | [temu-searchrec-ad-create.md](./apis/temu-searchrec-ad-create.md) |
| `66db5438c37446f49c122829489ac6d4` | `temu.searchrec.ad.detail.query` | `us_ads_searchrec_ad_detail_query.py` | [temu-searchrec-ad-detail-query.md](./apis/temu-searchrec-ad-detail-query.md) |
| `c2c5eda51c414e788bab914a297d1881` | `temu.searchrec.ad.log.query` | `us_ads_searchrec_ad_log_query.py` | [temu-searchrec-ad-log-query.md](./apis/temu-searchrec-ad-log-query.md) |
| `374d1f7fefdb4232b7b7a0239cb4465d` | `temu.searchrec.ad.goods.create.query` | `us_ads_searchrec_ad_goods_create_query.py` | [temu-searchrec-ad-goods-create-query.md](./apis/temu-searchrec-ad-goods-create-query.md) |
| `0b7140898262428eb8a4b28609112651` | `temu.searchrec.ad.modify` | `us_ads_searchrec_ad_modify.py` | [temu-searchrec-ad-modify.md](./apis/temu-searchrec-ad-modify.md) |

| type | URL |
|------|-----|
| `temu.searchrec.ad.roas.pred` | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=dfff26bad8e94ed5abaaf5cdade50c26 |
| `temu.searchrec.ad.reports.mall.query` | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=595f05856989480aa03abd58da203047 |
| `temu.searchrec.ad.create` | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=7bc9231776304158a895e41a816b7805 |
| `temu.searchrec.ad.detail.query` | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=66db5438c37446f49c122829489ac6d4 |
| `temu.searchrec.ad.log.query` | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=c2c5eda51c414e788bab914a297d1881 |
| `temu.searchrec.ad.goods.create.query` | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=374d1f7fefdb4232b7b7a0239cb4465d |
| `temu.searchrec.ad.modify` | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=0b7140898262428eb8a4b28609112651 |

> **说明**：`Partner Platform-rgq.htm` 未在提供目录中找到；若对应 `temu.searchrec.ad.reports.goods.query` 等接口，请补充 HTML 后接入。

## 相关 skill

| 欧洲站广告 | `linkfox-temu-ads-eu` |
| 全球站广告 | `linkfox-temu-ads-global` |

## 通用脚本

| `temu_us_proxy.py` | 任意 type |
| `temu_us_file_download.py` | 加签下载 |
