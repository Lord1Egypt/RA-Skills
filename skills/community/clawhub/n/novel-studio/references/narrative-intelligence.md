# Narrative Intelligence Layer

## 1. Goal

把 DOME / SCORE / 统一真相源 / 分类引导提取 / 矛盾配对 / 证据链 / ConStory-Checker / CoKe / ToM / CFPG / SWAG / BVSR 这类研究思路，收敛为一套适配 `novel-studio` 的增量式“叙事智能层”。

目标不是新起一套平行工作流，而是在现有：
- `.novel-state.json`
- 正式项目文件
- 四类长篇账本
- 父 agent 审批门
- subagent 执行协议

之上补一层更稳定的提取、追踪、校验、修订建议能力。

---

## 2. 设计结论

推荐采用 **“统一真相源 + 动态状态追踪 + reviewer 检查层 + staging 创意层”** 的四层架构。

不推荐：
- 把这些研究思路做成一个独立“超级引擎”，脱离当前 `workflow/state/ledger/review` 主链运行
- 让主 agent 或 subagent 直接把“推断结果”当成事实落盘
- 把 BVSR 式发散直接混入正式生产流程

推荐原因：
- 现有 `novel-studio` 已经有状态文件、账本、审批门、subagent 协议，具备承接条件
- 这批方法最有价值的部分不是“生成正文”，而是“减少长篇漂移、显式记录因果、提高审校命中率”
- 增量挂载复杂度明显低于重做 workflow，也更符合当前父 agent 只负责主控、subagent 负责写审校的职责划分

---

## 3. 三种落地方向

### 方案 A：外挂式研究引擎

做一个独立模块，统一做抽取、评分、矛盾检测、修订建议，再把结果回写给当前 workflow。

优点：
- 结构上最“完整”
- 方便后续继续接更多研究方法

缺点：
- 容易和现有 `.novel-state.json`、账本、review gate 重复建模
- 新旧真相源并存，容易冲突
- 实现复杂度最高

结论：**不推荐作为第一步。**

### 方案 B：在现有真相源上增量挂一层叙事智能

保留当前 workflow 不动，把研究能力分别挂到 `state / ledger / review / revision` 上。

优点：
- 改动边界清晰
- 不破坏当前主控 + 子代理流程
- 可以分阶段上线

缺点：
- 设计上没有方案 A “整齐”
- 早期会出现部分能力强、部分能力弱的阶段性不对称

结论：**推荐。**

### 方案 C：先做 reviewer / scorer，不做真相建模

先只做矛盾检查、证据链、套话检测、角色认知检查，不扩状态与账本。

优点：
- 启动最快
- 能较快改善 proofreading / final-review

缺点：
- 只能发现问题，不能稳定追溯问题来源
- 长篇运行一久还是会回到“靠聊天记忆补上下文”

结论：**适合作为极简版，但不是理想主方案。**

---

## 4. 推荐架构

### 4.1 统一真相源层

把“事实”严格限制在可持久化、可追溯、可审核的载体里。

正式真相源包括：
- `.novel-state.json`
- `01B_总主线与卷级推进.md`
- `05B_世界规则账本.md`
- `05C_伏笔回收台账.md`
- `05D_关系状态表.md`
- `05E_能力与资源变化表.md`
- `05A_本轮校对报告.md`
- `07_终审报告.md`

建议新增的正式智能账本：
- `05F_时间与事件图谱.md`
- `05G_伏笔三元组账本.md`
- `05H_角色认知与误判表.md`
- `05I_证据链与矛盾对照表.md`

约束：
- 文本原文仍然是最高优先级事实来源
- 提取结果只是“结构化索引”，不是比原文更高一级的真相
- 任何推断型结果都必须带来源章节 / 来源文件 / 证据片段摘要

### 4.2 动态状态追踪层

这一层对应 SCORE 的价值：不是只记录“现在在哪个 stage”，而是持续追踪叙事对象的动态状态。

建议在 `.novel-state.json` 下新增：

```json
{
  "narrativeIntelligence": {
    "timeline": {
      "enabled": true,
      "lastUpdatedBatch": "第7章-第9章",
      "openTemporalRisks": []
    },
    "cfpg": {
      "foreshadowTriples": [],
      "tripleCounts": {
        "total": 0,
        "pending": 0,
        "fulfilled": 0,
        "broken": 0,
        "expired": 0
      }
    },
    "theoryOfMind": {
      "characterBeliefs": [],
      "beliefConflicts": []
    },
    "consistency": {
      "contradictionCandidates": [],
      "evidenceChains": [],
      "lastCheckStage": null,
      "openCriticalIssues": []
    },
    "styleRisk": {
      "clichePatterns": [],
      "lastCokeScore": null
    }
  }
}
```

设计原则：
- `workflow.*` 继续回答“流程走到哪了”
- `batch.*` 继续回答“本轮章节执行到了哪”
- `narrativeIntelligence.*` 回答“故事内部状态是否还自洽”

### 4.3 分类引导提取层

这一层负责把正文和规划文件里的信息抽出来，但不直接改正文。

建议固定成四类提取器：
- **事实提取**：事件、时间、地点、人物关系、资源变化、规则触发
- **承诺提取**：伏笔 Promise、角色目标、未兑现压力、读者预期
- **认知提取**：角色知道什么、误判什么、隐瞒什么
- **风格风险提取**：模板化表达、口吻漂移、重复比喻、空转抒情

提取触发点：
- `02_大纲.md` 批准后：初始化时间图谱、CFPG、角色认知基线
- drafting 结果 accepted 后：提取新增事件、关系变化、资源变化、伏笔状态变化
- polishing 结果 accepted 后：重算风格风险与重复表达
- proofreading 结果 accepted 后：生成矛盾配对和证据链摘要
- final-review 前：做全局汇总

约束：
- 只有父 agent 可以把提取结果写入正式账本或 state
- subagent 只能在结果里“建议更新”，不能直接改这些账本

### 4.4 Reviewer / Checker 层

这一层是 ConStory-Checker、矛盾配对、证据链最适合进入的位置。

职责：
- 从统一真相源读取结构化事实
- 对正文、账本、状态做交叉比对
- 输出“哪一对信息互相冲突”
- 输出“为什么判断冲突，证据链是什么”
- 给 revision 提供修复优先级

建议分成四类检查：
- **时间一致性**：先后顺序、持续时长、回忆/现实切换、同一事件多版本
- **人物一致性**：OOC、已知信息越界、动机跳变、关系状态突变
- **规则一致性**：能力限制失效、代价缺失、设定穿模
- **承诺一致性**：伏笔 Promise 无支撑、Payoff 弱于 Promise、悬念失收

输出要求：
- 每条问题必须有 `severity`
- 每条问题必须给 `evidenceChain`
- 每条问题必须落到具体文件 / 章节
- 没有证据链的问题不能直接升级为 blocker

### 4.5 修订建议层

SWAG 适合放在这里，但只作为“动作引导”，不直接自动改正文。

建议产出格式：
- 问题是什么
- 问题属于哪一类
- 最小修复动作是什么
- 优先修哪一个文件
- 会不会影响后续账本 / 大纲 / 开篇门

例子：
- `人物认知越界 -> 先修第8章内心戏，再回填 05H 角色认知表`
- `伏笔 Promise 失支撑 -> 先改第6章埋因，再保留第12章 payoff`
- `世界规则代价缺失 -> 先补 05B 规则账本，再决定是否回改正文`

### 4.6 创意探索层

BVSR 只适合放在 `staging/` 的显式脑暴模式里。

可用场景：
- 开篇方案分叉
- 角色设定分叉
- 卷级冲突设计分叉
- payoff 方案比稿

禁止：
- 在正式 workflow 里静默使用 BVSR 产物覆盖 canonical files
- 脑暴结束后保留过期分叉污染项目目录

规则：
- 用户明确进入脑暴模式才允许写 `staging/`
- 一旦选中分叉，父 agent 必须回填正式文件并清理废弃分支

---

## 5. 概念到 Novel Studio 的映射

| 概念 | 在 `novel-studio` 的建议位置 | 主要价值 |
|------|-----------------------------|----------|
| 统一真相源 | `state + 正式账本 + review artifact` | 防止多份事实并存 |
| SCORE 动态状态追踪 | `narrativeIntelligence.*` | 持续追踪故事内部变化 |
| DOME 时间知识图谱 | `05F_时间与事件图谱.md` | 处理事件先后、时间跨度、因果链 |
| 分类引导提取 | accepted result 后的 parent-side extractor | 降低提取噪声 |
| 矛盾配对 | proofreading / final-review checker | 提高问题命中率 |
| 证据链 | review/revision 输出格式 | 让修订可解释 |
| ConStory-Checker | checker 框架参考 | 形成“检测而非拍脑袋”能力 |
| CoKe | polishing/proofreading 的风格评分器 | 降低套话、空话、AI 腔 |
| ToM | `05H_角色认知与误判表.md` | 减少信息越界和角色行为失真 |
| CFPG | `05G_伏笔三元组账本.md` | 追踪埋约收 |
| SWAG | revision action planner | 生成最小修复动作 |
| BVSR | `staging/` 脑暴层 | 用于分叉探索，不进正式主线 |

---

## 6. 与现有主控 / 子代理模型的边界

这个叙事智能层必须服从你当前已经确定的职责边界。

父 agent：
- 读取 state / 账本 / checker 结果
- 组织 dispatch
- 验收 child 结果
- 更新正式账本
- 解释 stop reason / blocker / revision gate

subagent：
- 负责 drafting / polishing / proofreading 的具体执行
- 可以返回“建议的结构化发现”
- 不能越权修改 `.novel-state.json`
- 不能直接修改 `05F` 到 `05I` 这类父级真相账本

自动推进模式下也不变：
- autopilot 只能推动安全 gate
- 不能把 checker、提取器、账本维护偷换成“父 agent 顺手自己写正文”
- 一旦 checker 发现 critical contradiction，必须明确停下并报原因

---

## 7. 推荐的实现顺序

### P0：先把真相源补齐

先做：
- `05F_时间与事件图谱.md`
- `05G_伏笔三元组账本.md`
- `05H_角色认知与误判表.md`
- `.novel-state.json` 的 `narrativeIntelligence.*`

原因：
- 没有结构化真相源，后续 checker 只能做浅层扫描

### P1：接入 accepted-result 后提取

在父 agent 接受 drafting / polishing / proofreading 结果后：
- 调 extractor
- 生成结构化增量
- 回填到账本与 state

原因：
- 这是最符合当前 parent-orchestrated runtime 的接入点

### P2：做 proofreader / final-review checker

先做：
- 时间矛盾配对
- 角色认知越界检查
- 伏笔 Promise / Payoff 健康度检查
- 规则代价缺失检查

原因：
- 这些问题最常见，也最影响长篇稳定性

### P3：做 SWAG 式修订动作规划

把 checker 输出转成：
- 最小修复动作
- 修订顺序
- 是否影响上游文件

### P4：做 CoKe / 风格风险评分

作为 polishing / proofreading 的辅助评分器，而不是单独审批门。

### P5：最后再考虑 DOME 深化和 BVSR 工具化

原因：
- DOME 的完整时间图谱实现成本较高
- BVSR 更适合脑暴模式，不是正式主链的首要痛点

---

## 8. 复杂度评估

如果按上面的顺序做，复杂度大致是：

- **低到中**：统一真相源、CFPG、基础 ToM 表、proofreading 矛盾配对
- **中**：accepted-result 提取器、证据链生成、revision action planner
- **中到高**：DOME 风格时间图谱、复杂多角色认知跟踪、CoKe 风格评分器
- **高**：把所有能力做成强耦合、实时联动的“单体智能内核”

对 `novel-studio` 最有价值的，不是最高复杂度那部分，而是前两层：
- 统一真相源
- 动态状态追踪
- proofreader / final-review checker
- 角色认知与伏笔追踪

---

## 9. 明确不该做的事

- 不要让“推断出的结构化信息”覆盖原文事实
- 不要让 subagent 直接写真相账本
- 不要在没有显式脑暴授权时使用 BVSR 分叉
- 不要让 checker 只有结论、没有证据链
- 不要把 CoKe 之类风格分数当成唯一审批依据
- 不要因为加了叙事智能层，就模糊现有审批门和 stop reason 纪律

---

## 10. 最小可落地版本

如果只做一个最小但有价值的版本，建议是：

1. 扩 `.novel-state.json` 的 `narrativeIntelligence` 字段
2. 新增 `05F/05G/05H/05I` 四个智能账本
3. 在 accepted drafting / polishing / proofreading 结果后做 parent-side 提取
4. 在 proofreading / final-review 增加矛盾配对 + 证据链输出
5. revision 阶段改为优先消费这些 checker 结果

这样做的结果是：
- 不改现有主控/子代理大框架
- 能显著降低长篇漂移
- 能让“为什么停下、为什么要改、先改哪里”更明确

