# 店铺接口

用于店铺搜索、卖家画像、风控和对标店铺池构建。

## 对应脚本

- 店铺搜索：`scripts/search_sellers.py`（封装 `POST /seller/search`）

## 接口选择规则

- **何时调用**：找本土/跨境对标店铺、找绿级/铂金店铺、某类目店铺画像、风控画像
- **何时不调**：只要商品列表/详情、不涉及店铺维度筛选
- **不要默认全查**：按需选 sellerType/levelId/powerType，先拿 50 个；默认绿级+铂金即可
- **组合**：拿到店铺 `id` 后用 `/items/search? sellerId=` 查商品矩阵，**不要对每个结果店铺都跑**

---

## POST /seller/search 店铺搜索

> ⚡ 每次 **2 积分** ｜ 方法：POST

### 请求参数

| 必填 | 参数 | 枚举/说明 | 脚本已封装 CLI |
|:-:|---|---|:-:|
| ✅ | siteId | `MLM`/`MLB`/`MLC`/`MLA`/`MCO`，默认 MLM | ✅ `--site`（默认 MLM） |
| | pageNo/pageSize | 默认 1/50 | ✅ `--page-no` / `--page-size` |
| | sellerType | `LOCAL`（本土）/ `CBT`（跨境）/ `CBT_OTHER` / `CBT_FBM` | ✅ `--seller-type`（默认 LOCAL） |
| | levelId | 优秀绿级/良好浅绿/一般黄/较差橙/很差红 | ✅ 脚本只开放前 3 档：`5_green` / `4_light_green` / `3_yellow`（默认 `5_green`）；`2_orange` / `1_red` 后端接受但脚本 choices 未封装 |
| | powerType | `platinum`（铂金）/ `gold`（黄金）/ `silver`（白银）/ 空=普通 | ✅ `--power-type`（默认 platinum） |

### CLI 映射

`siteId→--site`，`sellerType→--seller-type`，`levelId→--level-id`，`powerType→--power-type`。
脚本默认值：`--site MLM --seller-type LOCAL --level-id 5_green --power-type platinum`（对标高质量绿级铂金本土店，用户要降档再手动传）。

```bash
# 墨西哥本土铂金绿店（高质量对标）
python scripts/search_sellers.py --token <TKN> --site MLM \
  --seller-type LOCAL --level-id 5_green --power-type platinum
```

### SellerDetail 关键字段

- 基本：`id / name / permalink / site_id / country_id / registration_date / seller_status / power_seller_status / level_id / seller_type`
- 商品销量：`item_total / sale_total / sale_completed / sell_completed / completed60`
- 风控（核心指标）：`sell_canceled / sale_cancel` → `cancel60 / cancel60_rate`；`delayed60 / delayed60_rate`；`claims60 / claims60_rate`
- SA：`sa30 / sa60 / sa90`
- 评价：`SellerRatings.positive / neutral / negative`
- 地址：`SellerAddress.city / state`

---

## 本模块积分明细表

| 接口 | 功能 | 积分 |
|---|---|---:|
| `POST /seller/search` | 店铺分页查询 | 2 |
