# 常见写作问题与修复映射

本页把长文本中反复出现的结构、表达和连续性问题，转化为本项目可执行的审核模块。

## 设计原则

- 优先处理跨文体反复出现的问题，避免针对单个样本硬编码。
- 特征词和句式只是线索，不能单独作为删除或重写依据。
- 某个表达是否保留，要结合文体、角色声音、语境和写作意图判断。
- 修复应落到证据、动作、节奏和状态变化，不能只做同义词替换。

## 共性问题

| 读者吐槽 | 深层原因 | 推荐模块 |
| --- | --- | --- |
| 看起来太顺、太完整、像模板 | 段落结构过于对称，每段都干净收束 | `formulaic-structure-audit`, `controlled-drift`, `vocal-rhythm` |
| 套话多、塑料感重 | 高频词组替代了现场观察和人物动作 | `cliche-phrase-audit`, `embodied-emotion`, `cultural-anchors` |
| 读着很 polished，但没内容 | 段落只是换词复述，没有新增事实或压力 | `prose-progress-audit`, `editor-loop` |
| 情绪很满但不真实 | 只写情绪标签，缺少身体反应、动作矛盾和具体后果 | `embodied-emotion`, `relationship-state` |
| 转场万能，剧情像被推着走 | 连接词替代了因果、物件、动作、视角变化 | `narrative-bridges`, `formulaic-structure-audit` |
| 文化真空，像不知道具体时代和地方 | 缺少物质细节、社群词、时代锚点和生活经验 | `cultural-anchors` |
| 有时代细节，但技术、制度和物件互相打架 | 没有把时代与世界设定当作可验证的约束 | `world-ontology-audit` |
| 关键调查、研发、谈判或战斗被一句带过 | 结果没有经过尝试、阻力、判断、证据和代价 | `process-earnedness-audit` |
| 扩写越长越水，关键过程反而越短 | 注意力花在环境、心理和语义复述上 | `attention-budget-audit` |
| 每章换了词，但开场、转折和钩子都一样 | 章节功能顺序形成重复模板 | `chapter-pattern-audit` |
| 每个场景都用风景、沉默、反思或人生感悟收尾 | 真正的结尾已经发生，后补尾巴没有改变任何状态，只在模拟余味 | `earned-ending-audit`, 确定性 `END001` |
| 长文越写越忘 | 没有维护事实账本、关系状态、空间状态和伏笔 | `relationship-state`, `spatial-blocking`, `forensic-physical-audit` |
| 动作描写里充满精确数字 | 把感官经验写成测量报告 | `natural-measurement` |
| 反复“不是……是……”“是……不是……”或连续“比……比……” | 用对举和升级框架代替证据、动作与真实判断 | `formulaic-structure-audit` |
| 句子读着顺但漏了字、宾语或连接成分 | 生成后没有做谓词槽位、并列结构和指代回查 | `proofreading-audit`, deterministic `lint` |

## 模块如何使用

### 1. 套话/塑料词审查

使用 `cliche-phrase-audit` 检查：

- 命运拔高类表达
- 泛化身体动作
- 空洞情绪标签
- 万能转场
- 英文常见 AI marketing/slop 词

修复原则不是简单替换同义词，而是问：这句话有没有具体证据？能不能换成一个动作、物件、声音、来源、人物口癖或因果桥？

### 2. 公式结构审查

使用 `formulaic-structure-audit` 检查：

- 三段式/三连式是否滥用
- 每段是否都过于完整
- 是否反复使用“不是 X，是 Y”“是 X，不是 Y”一类双向对举
- 是否连续用多个“比”堆高语气，却混用了不同比较标准
- 段落长度和句式是否过于平均

修复方向是“有目的的不对称”：保留必要秩序，但让段落功能发生变化，让一部分压力留到下一段。
事实纠错、法律排除、数据比较和人物反驳不因命中而删除；无实际区分作用的框架才
改成直述、证据或后果。漏字另在最终 `proofread` 阶段逐句检查，不与文风重写混做。

### 3. 段落推进审查

使用 `prose-progress-audit` 检查每段是否回答：

- 什么变成了新事实？
- 读者知道了什么新东西？
- 哪个动作、证据、关系、代价或矛盾移动了？
- 下一段继承了什么压力？

如果相邻段落只是同义复述，就删、合并、换证据，或改成行动。

## 推荐命令

使用 `--deep-review` 加入完整结构与表达审查模块；长文续写可继续使用精简的 `--review`：

```powershell
python -m humanwriting.cli build `
  --style webnovel `
  --deep-review `
  --strict-continuity `
  --context examples/story-ledger.md `
  --task "续写下一章，避免套话和公式段落，每段必须推进状态。"
```

审已有稿件：

```powershell
python -m humanwriting.cli audit `
  --draft examples/problem-car-scene-draft.zh-CN.md `
  --context examples/vehicle-scene-ledger.md `
  --profile full `
  --profile numbers
```

AI 味不是一个词表问题，而是结构、证据、节奏、声音和上下文维护共同失衡的结果。
