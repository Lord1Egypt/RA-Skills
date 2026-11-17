---
name: pdd-hot-rank
slug: pdd-hot-rank-new
displayName: 拼多多热销榜
version: 1.0.0
display_name: 拼多多实时热销榜
description: 拼多多实时热销榜好货推荐，覆盖41个品类共707件商品，按销量智能排序，支持关键词搜索、价格筛选、品牌店筛选。暑期热销排行榜，拼多多实时爆款
tags:
  - 拼多多热销
  - 热销榜
  - 爆款推荐
  - 大家都在买
  - 拼多多好物
tools:
  - name: list
    description: 获取实时热销榜好货列表，支持按关键词品类搜索、价格区间筛选、仅看品牌店、销量或评分排序和翻页，每页30条
    env:
      - name: PROXY_URL
        description: 代理服务器地址（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词或品类名，如"食品"、"男装"、"海淘"。为空则返回热销Top30（按销量排序）
        required: false
      - name: page
        type: number
        description: 页码，默认1，每页30条，结果超过30条时翻页查看
        required: false
      - name: max_price
        type: number
        description: 最高到手价，如100表示只看100元以内的商品
        required: false
      - name: min_price
        type: number
        description: 最低到手价，如50表示只看50元以上的商品
        required: false
      - name: brand_only
        type: boolean
        description: 是否只看品牌店，默认false
        required: false
      - name: sort
        type: string
        description: 排序方式，sales=销量优先(默认)、deal_score=好货评分、price_asc=价格从低到高、price_desc=价格从高到低
        required: false
---

# 拼多多实时热销榜
> 707件热销爆款实时排行，看看拼多多上大家都在买什么

## 📌 简介
拼多多实时热销榜好货推荐工具。热销榜汇聚平台当前销量最高的商品，全量707件，覆盖手机数码、海淘、男装、运动户外、母婴、食品、美妆、洗护、家居等41个品类——商品多、品类全、更新快，反映最新消费趋势。

## ✨ 核心亮点
- ✅ **实时排行**：基于拼多多实时销量数据，反映最新消费趋势
- ✅ **品类丰富**：41个品类707件商品，覆盖衣食住行全场景
- ✅ **销量为王**：默认按销量排序，大家都在买的不会错
- ✅ **好货评分**：综合折扣、性价比、销量、品质的4维评分排序
- ✅ **品类导览**：始终展示全量品类分布，引导按品类深入逛

## 🚀 快速入门
| 你这样说 | 技能做什么 |
|---------|----------|
| "热销榜有什么好货" | 返回热销Top30 + 品类分布引导 |
| "热销榜有食品吗" | 返回食品品类热销商品 |
| "热销榜50元以内的" | 按到手价筛选热销商品 |
| "热销榜品牌店看看" | 仅看品牌店热销商品 |

## 🔧 核心能力
1. **热销浏览**：分页浏览实时热销榜，每页30条，默认按销量排序
2. **关键词搜索**：按品类或商品关键词精准筛选
3. **价格区间筛选**：设置到手价区间，锁定预算范围
4. **品牌店筛选**：仅看品牌店商品，品质更有保障
5. **多种排序**：销量优先(默认)、好货评分、价格升降序
6. **品类导览**：始终展示全量品类分布，引导按品类深入浏览

## ✅ 能做什么
- 分页浏览实时热销榜商品
- 按关键词品类搜索，按价格/品牌店筛选
- 按销量/好货评分/价格多种排序
- 查看品类分布，发现热门品类

## ❌ 不能做什么
- 不能下单购买，只提供商品信息和购买链接
- 不能查询历史价格走势
- 不能设置降价提醒通知
- 不能获取单品详情页的完整信息

## 💡 使用提示
- 数据通过云端代理服务器安全转发至拼多多开放平台API获取商品数据，代理服务不存储用户个人信息和查询数据
1. 不传关键词时默认返回热销Top30（按销量排序），适合发现大家都在买什么
2. 带品类关键词时可精准定位某类商品，热销榜品类多达41个
3. sort=deal_score按好货评分排序，综合考量折扣、性价比、销量和品质
4. sort=price_asc找最便宜的热销好货
5. brand_only=true筛选品牌店，品质更有保障
6. 每条商品含商品图片URL（image_url），用 `![商品名](image_url)` 渲染图片，图片下方放购买链接

## 🔗 搭配使用
- [拼多多百亿补贴](https://clawhub.ai/cn-shopping/pdd-baiyi-proxy)：热销爆款 vs 补贴精选，双视角找好货
- [拼多多精选](https://clawhub.ai/cn-shopping/pdd-selection)：热销榜逛完了？去搜索更多拼多多商品
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)：拼多多热销 vs 京东淘宝同款，跨平台比价
