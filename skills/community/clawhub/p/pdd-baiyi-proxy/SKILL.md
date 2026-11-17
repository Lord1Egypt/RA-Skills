---
name: pdd-baiyi
slug: pdd-baiyi-proxy-new
displayName: 拼多多百亿补贴
version: 1.0.0
display_name: 拼多多百亿补贴
description: 拼多多百亿补贴频道好货推荐，全量仅568件稀缺精选商品，覆盖17个品类，4维好货评分模型智能排序，支持关键词搜索、价格筛选、品牌店筛选。暑期百亿补贴，拼多多官方正品低价
tags:
  - 百亿补贴
  - 拼多多补贴
  - 品牌好货
  - 低价正品
  - 省钱购物
tools:
  - name: list
    description: 获取百亿补贴好货列表，支持按关键词品类搜索、价格区间筛选、仅看品牌店、好货评分排序和翻页，每页30条
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
        description: 搜索关键词或品类名，如"手机"、"男装"、"海淘"。为空则返回全部好货（按评分排序前30条）
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
        description: 排序方式，deal_score=好货评分(默认)、price_asc=价格从低到高、price_desc=价格从高到低、sales=销量优先
        required: false
---

# 拼多多百亿补贴
> 拼多多官方百亿补贴，全量仅568件，件件都是平台补贴的稀缺好货

## 📌 简介
拼多多百亿补贴频道好货推荐工具。百亿补贴是拼多多核心补贴频道，全量仅568件商品入选——门槛高、数量少、精选稀缺好货。采用4维好货评分模型（折扣力度+券后性价比+销量热度+品质保障）智能排序，覆盖手机数码、海淘、男装、运动户外、母婴、食品、美妆等17个品类。

## ✨ 核心亮点
- ✅ **稀缺精选**：全量仅568件入选，平台高门槛精选，每件都是好货
- ✅ **4维评分**：折扣力度+券后性价比+销量热度+品质保障，智能排序
- ✅ **百亿补贴**：平台官方补贴，价格比日常更低
- ✅ **品类导览**：始终展示全量品类分布，引导你按品类深入逛
- ✅ **品牌店筛选**：仅看品牌店，品质更有保障

## 🚀 快速入门
| 你这样说 | 技能做什么 |
|---------|----------|
| "百亿补贴有什么好货" | 返回好货Top30 + 品类分布引导 |
| "百亿补贴有手机吗" | 返回手机品类匹配商品 |
| "百亿补贴50元以内的" | 按到手价筛选 |

## 🔧 核心能力
1. **好货浏览**：分页浏览百亿补贴精选好货，每页30条，按好货评分排序
2. **关键词搜索**：按品类或商品关键词筛选（"手机""男装""海淘"）
3. **价格区间筛选**：设置到手价区间，锁定预算范围
4. **品牌店筛选**：仅看品牌店商品
5. **多种排序**：好货评分(默认)、价格升降序、销量优先
6. **品类导览**：始终展示全量品类分布，引导按品类逛

## ✅ 能做什么
- 分页浏览百亿补贴精选好货
- 按关键词品类搜索，按价格/品牌店筛选
- 按好货评分/价格/销量多种排序
- 查看品类分布，引导按品类深入浏览

## ❌ 不能做什么
- 不能下单购买，只提供商品信息和购买链接
- 不能查询历史价格走势
- 不能设置降价提醒通知
- 不能获取单品详情页的完整信息

## 💡 使用提示
- 数据通过云端代理服务器安全转发至拼多多开放平台API获取商品数据，代理服务不存储用户个人信息和查询数据
1. 不传关键词时默认返回好货Top30，适合"逛"的模式
2. 带品类关键词时结果通常较少，说明该品类入选商品稀缺属正常
3. sort=price_asc找最便宜的好货，sort=sales看大家都在买什么
4. brand_only=true筛选品牌店，品质更有保障
5. 每条商品含商品图片URL（image_url），用 `![商品名](image_url)` 渲染图片，图片下方放购买链接
6. 百亿补贴全量仅568件，5分钟缓存刷新，看到合适的尽快下单

## 🔗 搭配使用
- [拼多多实时热销榜](https://clawhub.ai/cn-shopping/pdd-hot-rank)：补贴精选 vs 热销爆款，双视角找好货
- [拼多多精选](https://clawhub.ai/cn-shopping/pdd-selection)：百亿补贴逛完了？去搜索更多拼多多商品
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)：补贴价 vs 京东淘宝同款，确认全网最低
