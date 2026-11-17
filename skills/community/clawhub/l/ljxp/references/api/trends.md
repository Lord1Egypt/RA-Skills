# 行业趋势接口

用于类目机会、价格带、销量历史、新品机会、仓储结构、竞争店铺/商品/品牌分析。

## 对应脚本

- `scripts/trends.py --type <type_name>`（9 个子接口，`--type` 切换）

## 接口选择规则（⚠️ 默认不要 9 个全查）

9 个接口每次都是 **2 积分**。**绝大多数场景先查「核心三件套」就够了**。

### 核心三件套（类目机会判断默认只查这 3 个）

| --type 值 | 接口 | 何时调用 |
|---|---|---|
| `statistical` | `/trends/statistical` | 类目大盘数据、市场容量、月/日环比（这个类目怎么样？） |
| `sold_his` | `/trends/sold/his` | 每日销量/销售额/单价趋势、季节性判断（最近走势？） |
| `top_sellers` | `/trends/brand/top/sellers` | 竞争店铺排行、本土/跨境格局、头部店铺集中度（哪些头部店？） |

### 按需补充 6 个（不要默认全查）

| --type 值 | 接口 | 何时调用 | 备注 |
|---|---|---|---|
| `price_list` | `/trends/price/list` | 价格分布、定价建议、哪个价格段竞争少（什么价格好卖？） | |
| `top_brands` | `/trends/brand/top/brands` | 品牌集中度、白牌机会、品牌垄断判断（品牌壁垒高吗？） | |
| `top_items` | `/trends/brand/top/items` | 爆款/代表商品长什么样（类目爆款有哪些？） | 可用 `/items/search` 按类目+销量替代 |
| `sale_list` | `/trends/sale/list` | 子类目销量排行、一级类目下哪个子类好卖 | 需 `--month YYYYMM` |
| `inventory_type` | `/trends/store/inventoryType` | FBM/FULL/CBT/本土仓占比、本土跨境格局（自发货or海外仓？） | 需 `--month YYYYMM` |
| `new_items` | `/trends/new/items` | 新品销量占比、每日/每周/每月上架趋势（新品好做吗？） | |

### 组合建议

- **完整类目调研**（用户明确说"全维度分析"）：9 个全跑（18 积分）
- **价格带专项**：statistical + price_list + （必要时）`/items/search` 验证商品形态
- **品牌格局专项**：statistical + top_brands + （必要时）top_sellers
- **新品机会专项**：statistical + new_items + （必要时）price_list
- **避免重复**：本土/跨境格局用 `inventory_type` 或 `top_sellers` 二选一，不再第三次用 `/seller/search`

---

## 通用请求参数 + CLI

| 必填 | 参数 | 说明 |
|:-:|---|---|
| ✅ | siteId | `MLM`/`MLB`/`MLC`/`MLA`/`MCO` |
| ✅ | categoryId | 类目 ID（如 `MLM458037`） |
| ✅\* | month | 仅 `sale_list` 和 `inventory_type` 必填，格式 `YYYYMM` |

CLI 映射：`siteId→--site`，`categoryId→--category-id`，`month→--month`

```bash
# 核心三件套（先跑这 3 个）
python scripts/trends.py --token <TKN> --site MLM --category-id MLM458037 --type statistical
python scripts/trends.py --token <TKN> --site MLM --category-id MLM458037 --type sold_his
python scripts/trends.py --token <TKN> --site MLM --category-id MLM458037 --type top_sellers

# 需 month 的两个
python scripts/trends.py --token <TKN> --site MLM --category-id MLM458037 --type sale_list --month 202603
python scripts/trends.py --token <TKN> --site MLM --category-id MLM458037 --type inventory_type --month 202603
```

---

## 各接口关键字段

### statistical 统计概览
`total（总商品数）` / `hbTotal（月环比）` / `rhbTotal（日环比）` / `itemCount（30天活跃）` / `soldTotal` / `amountTotal` / `avgSold` / `avgAmount` / `monthGrowth`

### sold_his 销量历史
`dataList[]: date / sold / amount / price` + `currencyId`

### sale_list 销量分布（子类）
`soldTotal` / `categoryId` / `name` / `nameZn`

### price_list 价格分布
`key（价格区间）` / `count（商品数）` / `value（30天销量）` / `price（均价）`

### inventory_type 仓储分布
`fbm / all（含 amount/sale30/avgPrice/totalItems）` / `full / cbt` / `localFull / cbtFull / cbtNotFull / localNotFull` / `usa*（美国仓统计）`

### new_items 新品机会
`sale*/newSale*/newRate*`（30/60/90/180） + `dailySaleList/weeklySaleList/monthlySaleList`（上架趋势）

### top_sellers 竞争店铺
`categoryName/Cn` / `allCount/brandCount/sellerCount/count（活跃店铺）` / `sale30/sumSale30（Top10 30天销量）` / `topList[]: id/key/ count/price/volume/url/sellerType`

### top_items 竞争商品
`topList[]: id/key/price/volume/sale30/url/title`

### top_brands 竞争品牌
`topList[]: key（品牌名）/count/price/volume/url/value（30天销量）`

---

## 本模块积分明细表

| 接口 | 功能 | 积分 |
|---|---|---:|
| 9 个子接口（statistical/sold_his/sale_list/price_list/inventory_type/new_items/top_sellers/top_items/top_brands） | 各接口单次调用 | **2** |
