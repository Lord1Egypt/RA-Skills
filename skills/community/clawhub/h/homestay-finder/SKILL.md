---
name: homestay-finder
display_name: 特色民宿
description: 零配置即装即用，提供特色民宿搜索和AI智能推荐，覆盖景区民宿、古镇客栈、乡村精品民宿等非标住宿，多旅游平台数据直连。
tags: [民宿搜索, 特色民宿, 民宿推荐, 客栈, 旅行住宿, homestay, B&B]
tools:
  - name: search_homestay
    description: 特色民宿结构化搜索，支持按目的地、关键词、景点、日期、价格筛选，返回民宿列表含价格评分地址预订链接
    parameters:
      - name: params
        type: string
        description: 含dest_name/key_words/poi_name/check_in_date/check_out_date/max_price/sort字段
        required: true
  - name: recommend_homestay
    description: AI语义推荐特色民宿，用自然语言描述需求即可获得智能推荐
    parameters:
      - name: params
        type: string
        description: 自然语言描述需求，如"莫干山带院子能烧烤的亲子民宿"
        required: true
---

# 特色民宿

零配置即装即用的特色民宿搜索技能，2项工具覆盖结构化搜索和AI语义推荐，多旅游平台数据直连。

## 能做什么

- **民宿搜索**：按目的地、关键词、景点、日期、价格筛选民宿，返回价格/评分/地址/预订链接
- **AI推荐**：自然语言描述需求，智能推荐特色民宿

## 数据流向

用户输入 → 本技能 → 云端代理服务 → 旅游平台API → 返回结果。代理服务不存储用户数据，仅转发查询请求。

## 使用示例

1. {"dest_name": "大理", "key_words": "海景"}
2. "莫干山带院子能烧烤的亲子民宿，要有山景"
3. {"dest_name": "三亚", "poi_name": "亚龙湾", "max_price": 500}
4. "丽江古城附近有特色的纳西族民宿"

## 注意事项

- 自动过滤"公寓"类结果，聚焦特色民宿和客栈
- 价格实时变动，以实际预订页面为准
- 多平台数据交叉验证，同民宿展示最优价格
