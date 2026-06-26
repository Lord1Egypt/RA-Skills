---
name: visual-creative
description: 视觉创意生图提示词生成skill。当用户需要为任何视觉物料生成AI生图提示词时使用，包括海报、banner、产品图、社交媒体配图、概念艺术、品牌物料等所有视觉场景。无论用户的需求是模糊的（"帮我做张海报"）、半清晰的（"科技风新品发布海报"）还是已有方向的，都应触发此skill。当用户提到生图、出图、画图、提示词、创意设计、视觉方案等关键词时必须使用此skill。
---

# 视觉创意生图 Skill 主文件

## 概述

本skill帮助AI将用户的视觉需求转化为富有创意的AI生图提示词。核心目标是突破平庸，解决三个常见问题：
1. **创意局限**：避免走最安全、最常见的视觉解法
2. **构图死板**：避免均匀分布和居中对称的惰性构图
3. **画面空洞**：主动填充丰富的视觉细节和层次

处理流程：分析需求 → 识别场景 → 调取创意方法 → 生成设计思路（用户可见）→ 输出提示词（传递下游）

如当前需求属于特定场景，请同时读取对应的场景子文件以获取场景专属方法：
- 场景子文件位于 `scenes/` 目录下
- 见本文件末尾的场景索引

---

## 八、场景子文件索引

识别用户需求后，读取对应场景子文件获取场景专属创意方向：

| 场景 | 子文件路径 |
|-----|----------|
| 电商主图与详情页 | scenes/ecommerce.md |
| 促销海报与活动banner | scenes/promotion.md |
| 户外广告OOH | scenes/ooh.md |
| 产品概念图与产品海报 | scenes/product.md |
| 品牌视觉与品牌故事图 | scenes/brand.md |
| 包装设计概念 | scenes/packaging.md |
| 通用海报设计 | scenes/general-poster.md |
| 小红书视觉（种草/生活/教程/探店） | scenes/xiaohongshu.md |
| 抖音视觉（封面/直播间/主页） | scenes/douyin.md |
| 微信公众号视觉（封面/配图/海报） | scenes/wechat-oa.md |
| 微博视觉（营销/热点/长图/九宫格） | scenes/weibo.md |
| 短视频封面与缩略图 | scenes/video-cover.md |
| 信息图与数据可视化 | scenes/infographic.md |
| 电影与剧集海报 | scenes/film-poster.md |
| 游戏视觉与游戏海报 | scenes/game.md |
| 音乐封面与艺人宣传图 | scenes/music.md |
| 概念艺术与插画 | scenes/concept-art.md |
| 摄影风格图 | scenes/photography.md |
| 抽象艺术与实验性视觉 | scenes/abstract.md |
| 活动现场视觉与展览 | scenes/event.md |
| 室内空间概念图 | scenes/interior.md |
