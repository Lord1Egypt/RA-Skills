# AI 分析层 Schema（wm_analysis.json）

> 本文件是 skill 分析层的**唯一契约**。assistant 在阶段2 依据 `wm_video_raw.json`
> 的真实数据产出分析，写入 `wm_analysis.json`，再由脚本 `--render` 渲染进
> Markdown / Excel / HTML 三种报告。分析必须**逐条锚定 raw 数据**
> （时间点引用 ≤ 视频实际时长、互动数字及语义引用 `wm_interaction_facts.json`），
> 不臆造 raw 里没有的字段和数字。

> **强制校验**：`--render --analysis` 与 `--check-analysis` 会按本契约对分析文件
> 做 schema 强校验（必填字段、类型、固定六维顺序、分数区间、贡献度合计等）。
> 不合契约直接退出码 8 拒绝渲染并给出逐条错误清单。这是报告结构稳定的
> 前提：**任何通过校验的分析文件，渲染出的报告结构完全一致**
> （相同板块顺序、相同表格列、固定评分维度）。校验只约束**结构**，
> 不约束分析内容本身的质量。

## 产出要求

分析层的核心价值不是复述数据，而是回答三个问题：

1. **哪些做法值得参考**——哪个片段/手法值得优先分析、有什么证据；不能凭单条视频推断实际传播因果贡献
2. **为什么这样判断**（评分理由）——每个分数都要有时间点级别的证据
3. **怎么借鉴**（可复刻策略/运营建议）——落到可执行动作

写之前先通读 `wm_interaction_facts.json` 和 `wm_video_raw.json` 的：
- `wm_interaction_facts.json`：规范化互动事实；`metrics.likeCount`=点赞，`metrics.recommendCount`=推荐，`shareCount`=转发，`commentCount`=评论。**原始 `info.data.metrics.favoriteCount` 是旧命名的点赞，原始 `likeCount` 是推荐，不能按英文字面解释。**
- `info.data.title / description`（文案）、`info.data.accountName`、`info.data.publishedAt`
- `analysis.data.observation.summary / segments[]`（时间线：起止秒、画面、屏幕文字、语音、景别、运镜、情绪线索、叙事作用）
- `analysis.data.observation.visualFacts[]`（可核验画面事实）、`uncertainties[]`（不可确认项——分析中不得与它们矛盾）

## JSON 结构

下例仅演示结构和合成数值；实际 `interactionBasis` 必须整体复制本次 `wm_interaction_facts.json`，其余结论须用本次数据重新生成。旧报告先不带 `--analysis` 执行一次 `--render`，即可生成此文件，无需重新采集。

```json
{
  "schemaVersion": "1.0",
  "interactionBasis": {
    "semanticsVersion": "wechat-channels-interactions-v2",
    "isLocal": false,
    "metrics": {"likeCount": 18000, "shareCount": 1069, "commentCount": 67, "recommendCount": 2969},
    "metricDetails": {
      "likeCount": {"value": 18000, "exact": true, "display": "18000", "relation": "exact"},
      "shareCount": {"value": 1069, "exact": true, "display": "1069", "relation": "exact"},
      "commentCount": {"value": 67, "exact": true, "display": "67", "relation": "exact"},
      "recommendCount": {"value": 2969, "exact": true, "display": "2969", "relation": "exact"}
    }
  },
  "audience": {
    "ageRange": "未获取实际年龄分布，可讨论话题与目标人群的关联",
    "gender": "未获取实际性别分布",
    "interests": ["社会热点", "消费维权"],
    "consumption": "中等，关注日常消费权益……"
  },
  "structure": {
    "scriptType": "个人经历讲述型",
    "rationale": "判断依据：0-2s 新闻字幕叠加事件核心……（引用片段时间点）",
    "summary": "冲突开场→证据展示→留白收尾",
    "segmentNotes": {
      "1": "为什么有效：开篇直接呈现……触发愤怒/好奇心理",
      "2": "为什么有效：……"
    }
  },
  "viralAttribution": [
    {
      "rank": 1,
      "layer": "内容因素",
      "factor": "荒谬冲突与情绪代入",
      "detail": "0-2s 开篇……（时间点+画面证据）",
      "contribution": 45,
      "evidence": "引用本次真实时间点或互动事实；示例数据为点赞18000、推荐2969、评论67……"
    }
  ],
  "viralFormula": "荒诞冲突选题+证据链闭环叙事+情绪共振驱动转发",
  "replicability": {
    "score": 4,
    "note": "结构易复制，但依赖真实争议事件素材，获取有偶然性",
    "replicableStrategy": "证据链展示法——实物特写+手机截图交叉印证",
    "notApplicableScenarios": "品牌商业带货、正向情绪引导场景"
  },
  "sixDimScores": [
    {
      "dimension": "Hook强度",
      "score": 9,
      "evidence": "0-2s 画面叠加红色新闻字幕……",
      "reason": "开篇呈现冲突，但没有留存数据，无法判断真实留存效果",
      "suggestion": "可增加更醒目的花字强化冲突感"
    }
  ],
  "operations": ["建议1（可执行动作）", "建议2"],
  "overall": {
    "totalScore": 76,
    "replicabilityStars": 4,
    "highlights": [
      {"type": "亮点", "text": "……"},
      {"type": "问题", "text": "……"}
    ],
    "primaryImprovement": "一条最优先的改进动作"
  },
  "tags": ["社会热点", "证据展示"]
}
```

## 字段规则

| 字段 | 必填 | 规则 |
| --- | --- | --- |
| `schemaVersion` | 是 | 固定 `"1.0"` |
| `interactionBasis` | 是 | 整体复制本次 `wm_interaction_facts.json`；校验与原始数据规范化后的结果逐字段一致。缺失或不一致拒绝渲染。旧分析的互动结论、建议和评分须重新审查，不能仅补此字段伪装重算；本地视频也复制此文件，metrics 为空 |
| `audience` | 是 | 对象本身必填；四个子字段可省略。可以提出目标人群假设；未采集真实年龄、性别、购买力分布时不得编造百分比，加“约”也不允许 |
| `structure.scriptType` | 是 | 短视频脚本类型（如 冲突对质型/教程型/剧情反转型） |
| `structure.rationale` | 是 | 必须引用片段序号+时间点作为依据 |
| `structure.summary` | 是 | 一句话结构总结，形如「A→B→C」 |
| `structure.segmentNotes` | 是 | 非空对象；key 是片段序号字符串（"1"、"2"…，不得超出实际片段数），value 为「为什么有效：…」注解 |
| `viralAttribution` | 是 | 2-4 条；`layer` 用 内容因素/传播因素/表现因素/账号因素；保留 `contribution` 字段兼容旧结构，但仅表示人工分析注意力权重，合计≈100（±5），不表示实际因果贡献；`evidence` 引用真实画面或互动，不把推测说成事实 |
| `viralFormula` | 是 | 一句话，形如「A+B+C」结构 |
| `replicability.score` | 是 | 1-5 整数；`note/replicableStrategy/notApplicableScenarios` 若提供须非空 |
| `sixDimScores` | 是 | 恰好 6 项且**顺序固定**：Hook强度、信息密度、节奏控制、产品展示（无商品时按道具处理并说明）、情绪曲线、转化引导；`score` 0-10 数值可带 0.5；每项 `evidence/reason/suggestion` 必填 |
| `operations` | 是 | 3-5 条，每条是可执行动作，不要空话 |
| `overall.totalScore` | 是 | 0-100 整数，与六维均值×10 自洽（偏差 ≤15） |
| `overall.replicabilityStars` | 是 | 1-5 整数 |
| `overall.highlights` | 是 | 2-3 条，`type` 为 `亮点` 或 `问题` |
| `overall.primaryImprovement` | 是 | 一条最优先的改进动作 |
| `tags` | 可选 | 若提供须 4-6 个短标签 |
| `interactionNotes` | 可选 | 2-4 条，对脚本**自动反推的互动结构**做人工补充解读（须锚定真实数字）。不提供则只渲染脚本反推结果 |

## 互动结构反推（脚本自动计算，非 AI 生成）

脚本 `infer_interaction_profile()` 使用规范化后的点赞/转发/评论/推荐四项计数，确定性计算并渲染进三种格式：

- **占比** = 该项 / 四项之和；**比值** = 该项 / 点赞。合计不是去重人数，不是播放量，不能算播放互动率。
- 四项均有精确值且点赞大于 0 时才计算结构；任何缺失/非精确值都不填 0。不把“1.8万”当精确 18000。
- 只描述哪项占比最高和具体比值，不由计数直接认定“工具/存档型”“情绪认同型”或争议原因。
- **独立收藏数没有提供**。不得把点赞或推荐描述成收藏、存档意愿、反复观看意愿；旧版基于收藏比值的推断与建议已移除。
- AI 可结合画面和真实评论证据提出有边界的判断，不编造留存率、受众动机或传播因果。评分以可见内容证据为依据，不因字段更名自动加减分。

## 红线

- **不得引用 raw 中不存在的数据**（尤其是播放量——视频号 API 不返回）。
- 时间点、数字必须与 `segments` / `metrics` 完全一致，不得四舍五入后还写错。
- `uncertainties` 里声明无法确认的内容（人物身份、完整原声等），分析中不得当作事实下结论。
- 本地视频（`isLocal=true`）没有互动数据：`viralAttribution[].evidence` 留空或引用画面证据，`overall` 与六维评分侧重内容维度。

## 写作规范（去 AI 味，保证报告像专业分析而非营销文案）

**必须做到**

- 每条结论挂数字或时间点，例如“推荐 2969、点赞 18000，推荐/点赞约 16.5%”（仅对应上方合成示例）。收藏未提供时不得写收藏表现。
- 区分事实与判断：接口/模型给的写"画面显示…"，自己的推论写"推断…""更接近…"，不要用断定语气包装推断。
- 用平实动词：呈现、说明、指向、构成、降低、提高。避免"引爆""狂欢""飙升""直击痛点""拿捏"。
- 对涉事人员用中性称谓（"当事双方""涉事顾客"），只描述视频呈现的行为，**不作道德定性、不使用贬损性网络用语**。
- 建议要可执行且边界清晰：写清做什么、放在哪个时间点，不写"强化心智""提升调性"这类无法落地的表述。
- 长句拆短，一段一意；每段控制在 2-4 句。

**禁止出现**

- 过度加粗与感叹号；emoji；"**A+B+C = D**"式公式炫技（爆款公式用一句话说清机制即可）。
- 三段式排比堆砌、空泛的"值得关注""显而易见""综上所述"。
- 绝对化表述："必然""一定""完美""史上最"。
- 未标注来源的百分比或行业均值。
- 对未采集维度（完播率、粉丝增量、流量来源）作任何数值推断。
