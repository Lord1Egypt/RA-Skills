---
name: marriott-hotel-booking
display_name: 万豪酒店预订
description: 搜索万豪集团旗下酒店并返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索。当用户需要预订万豪酒店、找喜来登、威斯汀、丽思卡尔顿、JW万豪、万丽、万枫、瑞吉等万豪旗下品牌酒店时使用
---

# 万豪酒店预订

## 任务目标
- 本技能用于搜索万豪集团旗下酒店，返回真实价格和可预订链接，并支持查询酒店详情和套餐优惠
- 触发条件：当用户提到万豪/喜来登/JW/威斯汀/丽思卡尔顿/万丽/万枫/瑞吉/艾美/W酒店/宝格丽/豪华精选等万豪旗下品牌时
- 数据源：飞猪官方商品库万豪专区，返回真实价格和可预订链接

## 🚫 绝对禁止

1. **禁止编造任何数据** — 酒店名称、价格、评分、星级必须100%来自脚本输出
2. **禁止添加脚本未返回的信息** — 脚本没返回评分就不能写评分，没返回健身房就不能说"有健身房"
3. **禁止替换或筛选脚本结果** — AI不得二次过滤或替换脚本返回的酒店
4. **禁止美化数据** — 不得将¥1580改成¥980，不得添加虚假评分
5. **禁止用自身知识补充酒店** — 不得根据品牌常识推断设施，不得添加脚本未返回的酒店
6. **禁止省略预订链接** — 脚本返回的detailUrl必须完整展示
7. **禁止混合数据** — 不得将脚本数据与网上搜索数据混合展示

**正确做法：脚本输出什么，就原样展示什么。只做格式排版，不修改任何数据。**

## 🛠 工具

### 1. search - 万豪酒店搜索

搜索万豪集团旗下酒店，返回价格、星级、地址、附近地标和预订链接。

**参数：**
▸ `destName`（string，✅必填）：目的地城市/区域，如"上海""深圳""三亚"
▸ `checkInDate`（string，可选）：入住日期 YYYY-MM-DD
▸ `checkOutDate`（string，可选）：退房日期 YYYY-MM-DD
▸ `keyword`（string，可选）：关键词，如"JW""丽思卡尔顿"
▸ `maxPrice`（int，可选）：最高价格/晚
▸ `sort`（string，可选）：排序 rate_desc/price_asc/price_desc/distance_asc
▸ `limit`（int，可选）：返回数量，默认10

```bash
python scripts/marriott_hotel.py search '{"destName":"上海","maxPrice":1000}'
```

### 2. detail - 万豪酒店详情

查询某家万豪酒店的详细信息，包括周边交通/景点/美食、酒店设施、政策、房型等。

**参数：**
▸ `shid`（string/int，✅推荐）：酒店ID，从搜索结果获取
▸ `hotelName`（string，可选）：酒店名称（备选定位方式）
▸ `reviewKeyword`（string，可选）：评价关键词过滤

```bash
python scripts/marriott_hotel.py detail '{"shid":"50013131"}'
```

### 3. packages - 万豪套餐搜索

搜索万豪酒店套餐优惠（含早/连住/门票等打包产品），通常比单订更优惠。

**参数：**
▸ `keyword`（string，可选）：搜索关键词，如"上海""三亚度假"
▸ `hotelName`（string，可选）：酒店名称
▸ `provinceOrCity`（string，可选）：省份或城市
▸ `sort`（string，可选）：排序方式
▸ `limit`（int，可选）：返回数量，默认10

```bash
python scripts/marriott_hotel.py packages '{"keyword":"上海"}'
```

## 执行流程

1. 用户提到万豪旗下品牌 → 调用 **search** 搜索酒店列表
2. 用户想了解某家酒店详情（交通/设施/房型） → 从搜索结果获取shid，调用 **detail**
3. 用户找优惠或套餐 → 调用 **packages** 搜索打包产品
4. 展示结果时，预订链接以 [点击预订](url) 格式展示
5. 所有结果末尾标注"数据来源：飞猪官方商品库·万豪集团专区"

## 使用示例

### 示例1：搜索万豪酒店
- 用户："上海有什么万豪酒店"
- 调用：`python scripts/marriott_hotel.py search '{"destName":"上海"}'`

### 示例2：预算筛选
- 用户："上海800块以内的万豪"
- 调用：`python scripts/marriott_hotel.py search '{"destName":"上海","maxPrice":800,"sort":"price_asc"}'`

### 示例3：酒店详情
- 用户："上海宝华万豪酒店怎么样，周围有什么"
- 调用：`python scripts/marriott_hotel.py detail '{"shid":"50013131"}'`

### 示例4：套餐优惠
- 用户："上海万豪有什么优惠套餐"
- 调用：`python scripts/marriott_hotel.py packages '{"keyword":"上海万豪"}'`
