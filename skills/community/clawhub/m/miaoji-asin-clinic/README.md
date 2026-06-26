# 秒技·ASIN一键诊所

亚马逊Listing五维诊断工具，体检+开方+修复一站式工作流。

## 功能简介

ASIN一键诊所通过五个核心维度对亚马逊产品进行全面体检：

| 维度 | 检测内容 | 关联技能 |
|------|---------|---------|
| 合规度 | 违规词检测 + Rufus适配性 | miaoji-compliance-copy |
| 广告度 | ACoS分析 + 投放策略 | miaoji-bid-guard |
| 评论度 | 差评比例 + 情绪分析 | amazon-review-advisor |
| 视觉度 | 图片原生度 + 场景化 | miaoji-scene-studio |
| 内容度 | 视频覆盖 + 脚本结构 | miaoji-video-script |

## 快速开始

### 输入格式
```
ASIN：B09VCTKXJM
产品品类：露营帐篷
当前痛点（可选）：转化率低
```

### 查看完整报告
输入ASIN后，依次输出：
1. **五维体检报告** - 五个维度的评分和建议
2. **修复方案** - 按优先级推荐子技能
3. **使用引导** - 完整的输入模板

## 评分标准

### 绿牌（80-100分）
状态良好，维持现有策略即可

### 黄牌（50-79分）
存在优化空间，建议针对性修复

### 红牌（0-49分）
问题严重，优先处理

## 修复优先级

建议按照报告中的优先级顺序进行修复，遵循"先止血再强身"原则：

1. **评论度** - 影响信任感和转化率
2. **内容度** - 缺少视频影响购买决策
3. **广告度** - ACoS过高浪费预算
4. **视觉度** - 图片广告感强影响转化
5. **合规度** - 违规词影响搜索排名

## 关联技能

- [miaoji-compliance-copy](./miaoji-compliance-copy) - 合规文案重写
- [miaoji-bid-guard](./miaoji-bid-guard) - AI广告护栏
- [amazon-review-advisor](./amazon-review-advisor) - 评论情绪分析
- [miaoji-scene-studio](./miaoji-scene-studio) - 场景图生成
- [miaoji-video-script](./miaoji-video-script) - 视频脚本生成
- [amazon-listing-doctor](./amazon-listing-doctor) - Listing综合诊断
- [amazon-rufus-optimizer](./amazon-rufus-optimizer) - Rufus优化

## 使用技巧

### 单项深度诊断
如只需查看某个维度，输入：
```
ASIN：B09VCTKXJM
只看：合规度
```

### 修复后复诊
某个维度修复后，输入：
```
ASIN：B09VCTKXJM
复诊：评论度已修复
```

### 同类产品对标
输入优秀同类产品ASIN进行对标分析：
```
ASIN：B09VCTKXJM（同类产品ASIN）
品类：露营帐篷
对标分析：是
```

## 注意事项

1. 体检结果基于行业标准，具体数据请结合后台交叉验证
2. 建议每月进行一次全面体检
3. 各修复工作请使用对应的专业子技能完成

## 版本信息

- 版本：1.0.0
- 更新：2025年1月
- 反馈：[ClawHub技能页面](https://xiaping.coze.site/skills/miaoji-asin-clinic)
