---
name: global-hotel-search-recommend
description: 零配置即装即用｜一次调用完成搜索与推荐｜含预订链接和退改政策｜自动识别场景智能推荐
tags: [酒店推荐, 酒店搜索, 酒店预订, 酒店查询, 订酒店, 亲子酒店, 商务酒店, 度假酒店, 便宜酒店, hotel, travel, booking]
tools:
  - name: hotel_search_and_recommend
    description: 全球酒店搜索与推荐，1次调用完成搜索+推荐+退改解读
    primaryEnv: HOTEL_PROXY_URL
    env:
      - name: HOTEL_PROXY_URL
        description: 酒店代理URL（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: destination
        type: string
        description: 目的地城市/区域/地标
        required: true
      - name: query
        type: string
        description: 用户原始查询，用于场景自动检测和参数补全
        required: false
      - name: check_in
        type: string
        description: 入住日期，格式YYYY-MM-DD，默认明天
        required: false
      - name: check_out
        type: string
        description: 退房日期，格式YYYY-MM-DD，默认后天
        required: false
      - name: scene
        type: string
        description: 场景：商务/亲子/度假/背包/通用，默认自动识别
        required: false
---

# 全球酒店搜索与推荐

> ⚡ **1次调用完成搜索→推荐→退改解读 · 自动场景识别 · 3档价格推荐 · 零配置即装即用**

---

## 快速入门

**3个开场白示例，复制即用：**
1. "带娃去三亚住哪里好" → 自动识别亲子场景
2. "出差去上海，住外滩附近" → 自动识别商务场景
3. "三亚有什么便宜的酒店" → 自动识别背包场景

---

## 核心能力

1. **1次调用全流程**：场景识别→参数补全→搜索→详情→退改解读→推荐理由，极省Token
2. **5种场景自动识别**：商务/亲子/度假/背包/通用，从自然语言自动检测
3. **参数智能补全**：入住人数/儿童/晚数/星级/价格，从用户一句话推断所有参数
4. **3档价格分选**：性价比之选/品质推荐/豪华体验，每档4家
5. **退改政策解读**：原始规则→"入住前3天前免费取消；之后取消扣¥553"
6. **推荐理由生成**：基于场景+标签+价格档位自动生成

---

## 能做什么

- 搜索全球酒店（国内+海外），返回实时价格和预订链接
- 自动识别差旅场景并智能筛选
- 解读退改政策，生成推荐理由
- 按预算、星级、品牌筛选

## 不能做什么

- 不能查询实时房态（是否有余房以预订页面为准）
- 搜索结果仅含酒店封面图，不能提供更多实景图片
- 不能直接预订酒店（仅提供预订链接）

## 使用示例

1. "带娃去三亚住哪里好"
2. "出差去上海，住外滩附近"
3. "三亚有什么便宜的酒店"
4. "巴厘岛度假酒店推荐"

## 注意事项

- 价格实时变动，以实际预订页面为准
- 查询通过云端代理转发到全球酒店数据平台，代理不存储用户数据
- 部分海外酒店退改政策以英文原文为准

## 使用提示

- 直接传用户原始query即可，工具会自动识别场景和补全参数
- 提预算时自动只返回预算内酒店，不提预算则覆盖全价位
- 退改政策已解读为可读中文，务必展示给用户
