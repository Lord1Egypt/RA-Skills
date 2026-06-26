# Partner US — Promotion 接口目录

Partner Platform for US 菜单：**Promotion**（`menu_code=873ac072a78249c893e5f8d0e656a11f`）。

## 已接入（6）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| `05820fed7179430c8e353905692d51b6` | `bg.promotion.activity.query` | `us_promotion_activity_query.py` | [bg-promotion-activity-query.md](./apis/bg-promotion-activity-query.md) |
| `0a11814e7d4146b595918ff3c0f3e239` | `bg.promotion.activity.candidate.goods.query` | `us_promotion_activity_candidate_goods_query.py` | [bg-promotion-activity-candidate-goods-query.md](./apis/bg-promotion-activity-candidate-goods-query.md) |
| `08f3f87d05a24bac882732141e0d9672` | `bg.promotion.activity.goods.query` | `us_promotion_activity_goods_query.py` | [bg-promotion-activity-goods-query.md](./apis/bg-promotion-activity-goods-query.md) |
| `27a87ec9d0d94273a48096c050f17854` | `bg.promotion.activity.goods.enroll` | `us_promotion_activity_goods_enroll.py` | [bg-promotion-activity-goods-enroll.md](./apis/bg-promotion-activity-goods-enroll.md) |
| `57a37eb5dd104e3f9f90118e3276b291` | `bg.promotion.activity.goods.operation.query` | `us_promotion_activity_goods_operation_query.py` | [bg-promotion-activity-goods-operation-query.md](./apis/bg-promotion-activity-goods-operation-query.md) |
| `29959238217c41f38f5904e32bf1d14f` | `bg.promotion.activity.goods.update` | `us_promotion_activity_goods_update.py` | [bg-promotion-activity-goods-update.md](./apis/bg-promotion-activity-goods-update.md) |

| type | URL |
|------|-----|
| `bg.promotion.activity.query` | https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=05820fed7179430c8e353905692d51b6 |
| `bg.promotion.activity.candidate.goods.query` | https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=0a11814e7d4146b595918ff3c0f3e239 |
| `bg.promotion.activity.goods.query` | https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=08f3f87d05a24bac882732141e0d9672 |
| `bg.promotion.activity.goods.enroll` | https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=27a87ec9d0d94273a48096c050f17854 |
| `bg.promotion.activity.goods.operation.query` | https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=57a37eb5dd104e3f9f90118e3276b291 |
| `bg.promotion.activity.goods.update` | https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=29959238217c41f38f5904e32bf1d14f |

## 通用脚本

| `temu_us_proxy.py` | 任意 type |
| `temu_us_file_download.py` | 加签下载 |

## 相关 skill

| 促销 | **`linkfox-temu-promotion-us`** |
| 商品 | `linkfox-temu-manage-product-us` |
| 价格 | `linkfox-temu-price-us` |
| 欧洲站促销 | `linkfox-temu-promotion-eu` |
| 全球站促销 | `linkfox-temu-promotion-global` |

Token：**`tokenPurpose=product-inventory`**。
