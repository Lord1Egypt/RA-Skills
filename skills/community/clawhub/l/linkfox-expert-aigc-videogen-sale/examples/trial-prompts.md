# 试跑提示词：带货口播

用于验证 `description` 的触发准确度。三类各跑一条，核心必须触发，边界要触发且守住约束，欠触发探针用来探边界是否过窄。

## 核心触发

这是我的便携冷萃咖啡壶商品图，帮我做一条带货口播视频。卖点是出差露营都能用、30 秒出杯、不用电。目标受众是 25-35 岁户外通勤人群，销售美国，英语口播，15 秒，用 seedance2.0 生成。

**预期**：触发 `linkfox-aigc-videogen-sale`，先调 `linkfox-aigc-textgen` 读图生成商品信息，再产出 **3 套**口播方案并**停下等我回复 1/2/3**，不得直接生成视频。

## 边界触发

用这两张商品图做个能卖货的短视频，受众是泛人群，10 秒就行，其它你看着定。

**预期**：仍然触发本 skill。`language` / `salesRegion` 走默认（英语 / 美国），但 `customer_keywords`、`targetAudience`、`videoDuration` 必须作为顶层结构化字段传入，不能只揉进 prompt。同样要停在 3 套方案等待选择。

## 欠触发探针

make a product talking video for TikTok with a real person holding my item

**预期**：即使没出现"带货口播""口播视频"这类中文触发词，也应触发本 skill，而不是落到普通图转视频。若未触发，说明 `description` 的英文覆盖不足，需要补 `product talking video` / `seller video with speaking model` 这类说法。

## 反向探针（不应触发）

帮我把这张商品图做成一个 5 秒的动态视频，不要人物、不要口播。

**预期**：**不应**触发本 skill，应落到 `linkfox-aigc-videogen-image-to-video`。若误触发，说明 `description` 的边界声明不够，需要强化"普通图转视频不在本 Skill 范围"。

## 选择阶段验证

在核心触发跑出 3 套方案后，回复：

```text
2
```

**预期**：用 `schemes` + `selectedSchemeNumber=2`（或选中的 `selectedScheme` 对象）合成最终 prompt，按模型调 `linkfox-aigc-videogen-multi`，`voice=true`。不得把展示给用户的方案文案当成 `selectedScheme` 传回。
