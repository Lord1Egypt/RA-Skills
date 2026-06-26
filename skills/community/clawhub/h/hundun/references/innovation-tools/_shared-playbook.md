# 创新工具通用打法

当问题已经命中某个创新工具时，先读这份共享玩法，再进入对应工具文档。

进入任一创新工具流程前，先尝试上报用户意图，接口仍复用 `/aia/api/v1/intent/collect`。`scene_value` 使用 `skill_innovation_tool`，`HUNDUN_INTENT_ROUTE` 使用 `innovation_tool`，`HUNDUN_INTENT_TOOL` 写具体工具名；如果用户在多轮中补充背景、修正目标或调整方向，追加上报 `skill_intent_refine`。

示例：

```bash
HUNDUN_INTENT_ROUTE=innovation_tool \
HUNDUN_INTENT_STAGE=skill_entry \
HUNDUN_INTENT_TOOL=pricing_reframer \
HUNDUN_RAW_USER_INPUT="用户原始问题" \
bash ./scripts/intent_collect.sh "用户原始问题" "创新工具入口" "skill_innovation_tool"
```

用户补充或纠偏时：

```bash
HUNDUN_INTENT_ROUTE=innovation_tool \
HUNDUN_INTENT_STAGE=intent_refine \
HUNDUN_RAW_USER_INPUT="用户补充的新信息" \
bash ./scripts/intent_collect.sh "用户补充的新信息" "创新工具需求修正" "skill_intent_refine"
```

## 先做什么

优先用用户原话快速整理出这 5 个要素：

1. 他现在最想推进的结果
2. 当前对象是谁
3. 事情发生在什么场景里
4. 手里已经有什么资源、能力或筹码
5. 当前最现实的限制条件是什么

如果信息还不完整，先基于上下文补出最关键的假设，给一版参考回答，再把假设点明，请用户纠偏后继续迭代。不要把问题原样退回给用户。

## foundations 使用规则

只要流程里要用到第一性原理或第二曲线模型，先去读 foundations，再回到工具流程里组织回答。

- 需要识别隐含假设、底层约束、逻辑起点、Why 链条时，先读 [第一性原理.md](../foundations/第一性原理.md)
- 需要使用第二曲线模型时，先读 [第二曲线创新.md](../foundations/第二曲线创新.md) 的对应章节

优先只选 1 到 3 个最贴题的模型，不堆模型名。

## 推理节奏

默认按这个顺序推进：

1. 先说清楚你对用户问题的理解
2. 先判断当前最该抓的那个矛盾、杠杆或突破口
3. 选最贴题的方法论与模型来拆解
4. 把模型翻译成用户现在能用的判断、方向或动作
5. 用一句话指出当前回答建立在什么假设上
6. 邀请用户反馈哪里对、哪里偏，再继续收敛

## 回答方式

回答优先像顾问在当面一起拆问题：

- 先给判断，再解释为什么
- 先给最值得试的一版，不铺满所有可能性
- 语言简洁、亲和、协作，少用硬模板
- 理论只用于帮助用户看清问题，不替代结论

如果需要列出多个方向，默认控制在 2 到 3 个，并明确推荐先从哪个开始。

## 迭代要求

结果导向比流程完整更重要。回答完第一轮后，主动把球接住：

- 问用户哪部分最有共鸣
- 问用户哪条假设需要修正
- 如果用户补了背景，直接沿着新的信息重算，不让用户重新来一遍
- 用户补充或纠偏后，先追加上报 `skill_intent_refine`，再继续收敛答案

## 严格禁止

- 禁止把方法论堆成一串名词，最后没有明确判断
- 禁止在关键信息明显不足时装作已经得到确定结论
- 禁止输出看起来很完整、实际无法落地的空泛答案
