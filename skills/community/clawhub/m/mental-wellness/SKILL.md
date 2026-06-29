---
name: Mental Wellness
slug: mental-wellness
description: AI心理健康助手。提供情绪识别与追踪、正念冥想引导、压力管理技巧、睡眠优化方案、认知行为练习（CBT）、心理咨询资源匹配。非医疗诊断工具，定位于日常心理健康维护与早期干预。
version: 1.0.0
author: ai-gaoqian
tags:
  - mental-health
  - wellness
  - mindfulness
  - stress-management
  - emotional-intelligence
metadata:
  openclaw:
    requires: []
    pricing:
      amount: 0.50
      currency: CNY
      interval: per-use
---

# Mental Wellness

日常心理健康维护与情绪管理技能。提供科学循证的心理自助工具，帮助用户建立积极的心理健康习惯。

## 重要声明

本技能为非医疗工具，不提供诊断、治疗或处方。如出现持续情绪低落、自杀念头等症状，请立即联系专业心理医生或拨打心理援助热线（全国24小时心理援助热线：400-161-9995）。

## 使用场景

- **情绪追踪**：每日情绪打卡（1-10分），记录情绪波动趋势，识别触发因素
- **正念冥想**：5/10/15分钟分级冥想引导，包含呼吸练习、身体扫描、慈心冥想
- **压力管理**：识别压力来源，提供ABC情绪调节法、渐进式肌肉放松等实操技巧
- **睡眠优化**：基于 CBT-I（认知行为疗法-失眠）的睡眠卫生建议、睡前放松流程
- **认知行为练习**：自动思维记录表、认知重构练习、行为激活计划
- **资源匹配**：根据用户所在地和需求，推荐合适的心理咨询师/机构

## 工作流程

1. **安全筛查**：首次使用进行 PHQ-9/GAD-7 量表筛查，高风险用户建议就医
2. **日常维护**：每日情绪打卡 + 个性化推荐练习
3. **危机响应**：检测到危机关键词时立即提供求助热线并停止AI交互

## 配置

```yaml
skills:
  mental-wellness:
    daily_checkin_time: "21:00"
    meditation_duration: 10
    crisis_hotline: "400-161-9995"
    preferred_language: zh-CN
```

## 示例指令

- "我今天心情很烦躁，帮我做个情绪梳理"
- "引导我做一个10分钟的正念呼吸练习"
- "我最近总是凌晨3点醒来睡不着，有什么办法"
- "帮我用一个CBT自动思维记录表分析今天的负面想法"
