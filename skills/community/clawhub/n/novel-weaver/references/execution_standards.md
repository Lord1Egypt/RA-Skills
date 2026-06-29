# 执行规范

## 字数管理

### 统一标准（三阶段统一）

字数目标在**规划、写作、检查**三个阶段使用同一套标准，不允许 AI 自行配置或偏离。

| 阶段 | 动作 | 字数来源 |
|------|------|---------|
| 规划（plan-chapter） | 注册子结构时按项目篇幅确定字数范围 | `meta.length` → 下文字数表 |
| 写作（context_loader） | 加载上下文时输出字数约束，LLM 按此写作 | 同上 |
| 检查（write-sub） | 写入后校验，与规划/写作使用相同目标 | 同上 |

### 按篇幅字数目标（唯一参照）

| 篇幅 | 每子结构字数 | 校验上浮 |
|------|------------|---------|
| 短篇 | 1,000-1,500 | 上限 +15%（至 1,725） |
| 中篇 | 1,500-2,000 | 上限 +15%（至 2,300） |
| 长篇 | 2,000-4,000 | 上限 +15%（至 4,600） |

### 规则

- **字数目标必须注入 LLM 上下文**：context_loader 在写作前输出字数范围，LLM 据此写作，不得自行配置
- **校验一致**：write-sub 检查时使用相同的字数目标 + 15% 上浮窗口
- 实际字数以叙事单位自然结束为准，不强行撑到目标
- 低于下限打印 `[WARN] 建议补充`；高于上限+15% 打印 `[INFO] 注意控制`；在范围内打印 `[OK]`
- **禁止 AI 自行配置字数目标**：所有字数要求必须从 `meta.length` 读取，不允许基于过往章节实际字数推算

## 文体规范

文体风格由项目 `novel_state.json` 中的 `writing_style` 字段决定（6 字段：叙事视角、时态、句式偏好、词汇、描写深度、自定义规则）。以下规则适用于所有风格：

允许使用的通用修辞工具：
- 代码/协议块
- 系统警告/报告标记（如 `【状态】`、`【诊断】`）
- 可量化体征数据（心率、体温、激素水平）
- 类比与推理论证
- 表格/清单对比

禁止：
- 第三人称叙述插入（除非是人物对白中的转述）
- 纯抒情段落（情绪须通过人物行为或生理反应间接表达）
- 元文本引用（"从第 X 章开始"——读者视角，非叙事者视角）

## 子结构先行规划（v1.2 新增硬约束）

**必须在每个子结构写作前完成，不可跳过。**

### 概述编写规范

概述是整个命题作文体系的核心锚点——它同时服务于因果链验证、context_loader 命题指令、logic_check 内容匹配度检查。概述越精确，LLM 跑偏概率越低。

**概述必须满足以下条件（代码级强制校验，plan-chapter 时执行）：**

| 要求 | 说明 | 校验方式 |
|------|------|---------|
| 最低字数 | ≥12 个有效字符（不计空格/标点） | plan-chapter 强制阻断 |
| 包含动作 | 必须有具体动词或事件描述 | LLM 自觉（不可写纯状态） |
| 包含人物 | 必须涉及至少一个角色 | LLM 自觉 |
| 可验证 | 写完回头看能判断"是否写了这个" | LLM 自觉（logic_check 语义参考） |

**合格示例：**
- ✅ `Atlas 在每日诊断中首次检测到异常神经脉冲，决定不向三浦报告` — 24字符，有动作+人物+事件
- ✅ `三浦发现系统日志有0.3秒间隙，开始暗中调查` — 18字符，因果明确
- ✅ `Atlas 在伪装模式下首次体验人类情感波动，感到困惑` — 21字符，有结果

**不合格示例：**
- ❌ `主角在实验室` — 6字符，无事件无动作
- ❌ `Atlas 做了些事情` — 7字符，无法验证
- ❌ `讨论了一些问题` — 7字符，无具体内容
- ❌ `主角很难过` — 5字符，纯状态无因果

### 规划流程

1. LLM 根据章标题和概述，生成该章全部子结构的规划（S01-S05）
   - 也可先用 `--generate` 获取 JSON 模板：
     ```
     python novel_workflow_engine.py plan-chapter <state_path> <L##> --generate
     ```
2. 每个子结构规划包含以下字段：
   - `s_key`: 如 `S01`
   - `title`: 子结构标题（如"实验室初试"）
   - `summary`: 模糊概述（20-40字，描述该段核心内容）
   - `tone`: **情绪提示**（如"紧张"、"宁静"、"悬疑"、"温馨"等）— 保证跨子结构情绪连贯性
   - `emotions`: **可选** 混合情绪数组 — 每项 `{"type":"愤怒","intensity":0.8}`，强度 0.0-1.0，多维度表达复杂情绪
   - `writing_prompt`: **必填** 预编写作命题（≥50字符）— 规划阶段必须为该子结构编写详细剧情指令。包含场景建立、核心事件、情绪弧等完整 beat。context_loader 将其作为 `[硬性] 写作命题框` 输出，是 LLM 写作的核心依据。缺失则 plan-chapter HOOK-BLOCK 拒绝注册。存量旧子结构无此字段时，context_loader 自动从 summary+tone+emotions 合成 fallback 命题。
3. 用 workflow_engine.py 批量注册：
   ```
   python novel_workflow_engine.py plan-chapter <state_path> <L##> '<json_array>'
   ```
   JSON 示例（必填 writing_prompt + 可选 emotions）：
   ```json
   [
     {"s_key":"S01","title":"实验室初试","summary":"主角第一次接触实验设备，紧张","tone":"紧张",
      "emotions":[{"type":"紧张","intensity":0.7},{"type":"好奇","intensity":0.5}],
      "writing_prompt":"实验室的灯光惨白。主角第一次站在操作台前，手指悬在控制面板上方微微发抖。面前的义肢测试臂正在做循环动作，液压泵的嗡鸣声在安静的空间里格外刺耳。导师站在三米外，不时瞥一眼显示屏。\n\n主角深吸一口气按下启动键——测试臂突然加速，远超预设参数。警报声炸响，液压管压力表指针猛地甩到红色区域。导师冲过来拍下急停键，但主角注意到他在查看日志时眼神闪过一丝异样。"},
     {"s_key":"S02","title":"意外发现","summary":"主角意外发现异常数据，紧张又好奇","tone":"兴奋",
      "emotions":[{"type":"兴奋","intensity":0.8},{"type":"不安","intensity":0.3}],
      "writing_prompt":"显示器上的数据曲线突然偏离了基线。主角反复重启三次测试，每次都出现同样的异常脉冲。他调出日志比对，发现这个脉冲模式在历史记录中从未出现过。这不是设备故障——是某种未知信号的干扰。他犹豫是否要报告给导师。"},
     {"s_key":"S03","title":"导师的警告","summary":"导师对发现表示严重怀疑，要求主角停止调查","tone":"压抑",
      "emotions":[{"type":"压抑","intensity":0.7},{"type":"愤怒","intensity":0.4}],
      "writing_prompt":"导师把主角叫到办公室，语气严肃地警告他不要多管闲事。那个信号可能是系统误差，不需要深究。但主角注意到导师的眼神在回避，手指在桌面上轻轻敲击——那是紧张的表现。他决定暗中调查。"}
   ]
   ```
4. 验证：
   ```
   python novel_workflow_engine.py verify-chapter <state_path> <L##>
   ```
   全部注册后需手动推进 phase：

5. 预览：
   ```
   python novel_workflow_engine.py preview <state_path> <L##>
   ```

### 阻断规则

- **context_loader.py** 在子结构未注册时报错退出，不会降级输出"未知"
- **context_loader.py 串行阻断**：加载子结构时检测上一子结构 state 是否为 completed。若为 pending 则 HOOK-BLOCK 并输出 write-sub 修复命令，强制走管道完成标记后才能继续
- **必须先 plan-chapter，再开始写作**
- **write-sub 字数校验**：写入后对比字数是否达到篇幅目标。低于下限 WARN、超上限+15% INFO、范围内 OK

### write-sub（v2 — 系统组装模式）

v1.33.0 重构：LLM 只输出纯正文，系统自动组装全部元数据。

```
输入（stdin）: 纯正文叙事内容
  [可选尾部] 【别名】原名 = 别名

内部流程:
  1. 读取 stdin → body
  2. 从 state 读取 sub_structures[].title
  3. 调用 atomic_writer.v4.validate_and_write_body():
     a. 检测 body 末尾 【别名】行 → 剥离 + 注册（register-alias）
     b. body 无别名行 → 系统自动补 【别名】无（不再 HOOK-BLOCK）
     c. 正文非空检验
     d. 正文禁止 L#S# 校验
     e. 正文禁止署名/代名校验
     f. 系统组装：title_line + body + alias_line
     g. 原子写入 + fsync
     h. 追加标记行 L##S## + fsync
  4. state_manager update-sub → word_count + status
  5. entity_extractor 非阻断提取
  6. 字数校验（与规划阶段同源）

输出文件：
  L## · S##《title》              ← 系统生成
  （正文）                         ← LLM 写的
  【别名】无                      ← LLM 或系统补
  L##S##                          ← 系统追加
```

### context_loader 输出优先级

v1.33.0 重构：按注意力优先级排列输出块：

```
区块A（黄金位 — LLM 最先看到）：
  [上下文] L##S## | 章标题 · 子结构标题 | 概述摘要
  [情绪基调] 格式化 emotions[] 或 tone
  [硬性] 字数约束     ← 埋在中段 → 移至头部
  [硬性] 文风约束     ← 同上
  [硬性] 署名约束     ← 同上
  [硬性] 写作命题框  ← 有预编则输出，无则自动合成 fallback
  [参考] 叙事节奏参考

区块B（参考数据）：
  [上一子结构末3行]
  [硬性] 已出场关键人物 + 人格约束
  [硬性] 实体关系网
  [硬性] 上一章行为轨迹

区块C（尾部条件）：
  [硬性] 收尾约束（仅 is_ending）
  [参考] 钩子位建议（仅 is_hook_possible）

区块D（尾部固定）：
  [硬性] 输出模板（填空框 + 校验规则）
  [下一步] 管道命令

已删除：情绪写作参考词块（低价值，情绪信息已在标识行和命题框中）
```

## 统一项目状态文件

所有元数据写入一个文件 `novel_state.json`。

### 模型存储

BERT 语义检查和 DeepSeek-R1-Distill-Qwen-1.5B 推理审核的模型文件集中存储在 `_path_utils.py` 的 `MODELS_DIR` 管理的目录下：
```
~/.workbuddy/skills/.standardization/novel-weaver/models/
├── bge-small-zh/             ← BERT 33MB（sentence-transformers 缓存）
└── ds-r1-distill-qwen-1.5b/            ← DeepSeek-R1-Distill-Qwen-1.5B（transformers 缓存）
```
首次下载模型时自动存入对应子目录。如有镜像需求配置 `HF_ENDPOINT` 环境变量。

### 编号规则
- 章节编号：`L01`、`L02` … `L15`
- 子结构编号：`S01`、`S02` …
- 完整引用：`L10S04` = 第 10 章第 4 个子结构

novel_state.json 包含字段：project, meta.current_phase, meta.length, writing_style, signature, characters（含 aliases 别名数组）, timeline, chapters（含章摘要、子结构标题/概述/情绪提示/字数和状态、章节衔接/校验备注），以及运行时字段：entity_tracker（实体关系网，含 entities+relations）、behavior_summary（行为轨迹摘要）、cross_chapter_check（跨章承诺链记录）、continuity_notes（连通性记录）。

更新时机：
1. 项目初始化 → 填充 writing_style / chapters / characters
2. 子结构先行规划 → plan-chapter 批量注册 title/summary/tone
3. 子结构写入完成 → 更新 word_count + status
4. 角色更新 → 更新 characters（含 aliases）
5. 角色别名注册 → atomic_writer 写入时拦截【别名】行，自动调用 register-alias
6. 时间推进 → 更新 timeline
7. 连通性补充后 → 更新 continuity_notes
8. 风格校验后 → 更新 style_check_notes
9. 实体关系提取 → write-sub 后 entity_extractor 自动提取 entity_tracker.entities + entity_tracker.relations
10. 行为摘要提取 → finalize-chapter 通过后自动提取 behavior_summary
11. 语义检查 → finalize-chapter 中 BERT 检测 overview-vs-content 对齐和子结构间语义跳跃（有模型时）
12. 推理审核 → finalize-chapter 中 DeepSeek-R1-Distill-Qwen-1.5B 检测因果/人格/情绪/对话/论证一致性（有模型时）

## 子结构文件格式（系统组装，LLM 不负责格式）

v1.33.0 变更：LLM 只输出纯正文，系统自动组装标题行+别名行+标记行。

### 写入磁盘的最终文件格式

```
L## · S##《子结构标题》         ← 系统从 state 读取 title 生成
（正文叙事内容）                 ← LLM 输出的纯正文
【别名】无                     ← LLM 输出或系统自动补
L##S##                         ← 系统追加
```

### 规则

- **LLM 写入的内容**：纯正文叙事文本 + 可选尾部 `【别名】` 行
- **标题行**：由 write-sub 自动生成（格式 `L## · S##《title》`），原子性无需 LLM 关心
- **别名行**：LLM 在正文末尾输出 `【别名】原名 = 别名` 或 `【别名】无`。未输出时系统自动补 `【别名】无`
- **末行标记**：由 atomic_writer 在文件写入后自动追加（格式 `L##S##`）
- **正文禁止**：出现 `L##S##` 子结构标记、署名/代名内容、元注释污染
- **验证机制**：atomic_writer.v4 `validate_and_write_body()` 校验正文合法性，不校验标题/标记格式（系统生成，无需校验）

## 章节完成输出

每章完成后输出简表（从 novel_state.json 直接读取），并调用：
```
python novel_workflow_engine.py finalize-chapter <state_path> <chapter>
```

此命令自动执行：章内连通性 → 跨章承诺链 → 风格校验 → 逻辑检查 → 语义检查(BERT，可选) → 推理审核(DeepSeek-R1-Distill-Qwen-1.5B，可选，CPU 可跑) → HARD 阻断决策。存在 HARD 问题时阻断（不标记门禁，不推进 phase），写入 `_{chapter}_fixes.json` 后等待 LLM 修复；全部通过才推进 phase。

## 一键完结篇章（v1.9.0 质量闭环）

代替手动依次调用各检查器的繁琐流程。内部执行 6 步检查 + 1 步阻断决策：

```
章内连通性    → 检查子结构间时间/角色断链         → HARD: 双断裂阻断
跨章承诺链    → 检查上章尾 vs 下章头关键词续接       → SOFT: 仅建议
风格校验      → 检查禁用词/末行编号/行数             → HARD: 发现问题阻断
逻辑检查      → 检查角色+时间线+概述忠实度           → HARD: 关键词命中<30%阻断
语义检查(BERT)→ overview-vs-content 对齐+子结构间跳跃 → HARD: <0.4阻断（有模型时）
推理审核(DeepSeek-R1) → 因果/人格/情绪/对话/论证 5项    → 按结果 HARD/SOFT（有模型时）
    ↓
聚合决策：有 HARD 问题 → 写入 _fixes.json → 阻断
         全部通过      → 标记门禁 → phase → chapter_done
```

输出：
- `data/reports/logic_L##.md` — 逻辑一致性报告
- `data/chapters/L##/_L##_fixes.json` — 修复指引（仅 HARD 阻断时生成）
- phase → chapter_done（仅全部通过时）

## 时间线追踪

每章结束时调用 `novel_timeline.py add <project_dir> <chapter> <days> <summary>`。

## 角色信息表

新出场角色或已有角色属性变化时调用：
`novel_state_manager.py add-char <path> <name> <role> <first_appearance>`

## 角色人格系统（v1.7.0 新增）

每个角色可配置 `mbti`（16 类型）和 `archetype`（荣格 12 原型），驱动角色行为和叙事功能。

### MBTI 16 类型

| 维度 | 取值 | 含义 |
|------|------|------|
| E/I | E / I | 外向 / 内向 |
| S/N | S / N | 实感 / 直觉 |
| T/F | T / F | 思考 / 情感 |
| J/P | J / P | 判断 / 感知 |

完整类型如 `INTJ`、`ENFP`、`ISTP` 等。

### 荣格 12 原型

| 原型 | 叙事功能 |
|------|---------|
| Innocent | 天真者，追寻理想 |
| Sage | 智者，追求真理 |
| Explorer | 探险者，渴望自由 |
| Outlaw | 反叛者，挑战权威 |
| Magician | 魔法师，转化现实 |
| Hero | 英雄，证明价值 |
| Lover | 爱人者，创建连接 |
| Jester | 小丑，享受当下 |
| Everyperson | 普通人，归属群体 |
| Caregiver | 照顾者，保护他人 |
| Ruler | 统治者，掌控秩序 |
| Creator | 创造者，留下遗产 |

### 注册方式

```bash
python novel_state_manager.py add-char <state_path> <name> <role> <first_appearance> [traits] [mbti] [archetype]
```

### context_loader 输出

涉及角色有人格配置时自动输出：
```
🔴 人格约束（硬性）
  三浦: MBTI=INTJ, 原型=Sage
  提示: 角色言行必须符合其人格配置
```

## 情绪混合系统（v1.7.0 新增）

子结构可配置多维度情绪，每项情绪带强度数值（0.0-1.0）。

### 格式

子结构注册时在 JSON 中加入 `emotions` 数组：

```json
{"s_key":"S01","title":"...","summary":"...","tone":"紧张",
 "emotions":[
   {"type":"愤怒","intensity":0.8},
   {"type":"恐惧","intensity":0.3}
 ]}
```

### 强度分级

| 区间 | 标签 | 描述 |
|------|------|------|
| 0.0-0.2 | 微弱 | 几乎不可察觉的底色 |
| 0.2-0.4 | 轻度 | 偶尔流露 |
| 0.4-0.6 | 中等 | 明显可感知 |
| 0.6-0.8 | 强烈 | 主导当前场景 |
| 0.8-1.0 | 极致 | 情绪爆点/崩溃/狂喜 |

### context_loader 输出

```
[情绪基调] 愤怒 强烈[0.8/1] + 恐惧 轻度[0.3/1]
           → 色厉内荏：愤怒主导，恐惧底色
```

### 向后兼容

仅有 `tone` 无 `emotions` 时，输出同旧版：`[情绪提示] 紧张`。

## 文风系统（v1.7.0 新增）

项目级文风格式，在 `novel_state.json` 顶层配置，全局生效。

### 字段说明

| 字段 | 可选值 | 说明 |
|------|--------|------|
| `narrative_voice` | 第一人称/第三人称有限视角/第三人称全知视角/第二人称 | 叙事视角 |
| `tense` | 过去式/现在式 | 时态 |
| `sentence_preference` | 短句为主/长句为主/长短句交错 | 句式偏好 |
| `vocabulary_register` | 文学化/平实/学术/口语化 | 词汇风格 |
| `description_depth` | 详尽/中等/克制 | 描写密度 |
| `custom_rules` | 自由文本 | 自定义约束 |

### 配置方式

项目初始化时在 `novel_state.json` 顶层添加：

```json
"writing_style": {
  "narrative_voice": "第三人称有限视角",
  "tense": "过去式",
  "sentence_preference": "长短句交错",
  "vocabulary_register": "文学化",
  "description_depth": "中等",
  "custom_rules": "每段不超过3句对话；环境描写不超过2句"
}
```

### context_loader 输出（每个子结构写作前重复输出）

```
🔴 文风约束（硬性）
  叙事视角: 第三人称有限视角（仅从三浦的视角出发）
  句式偏好: 长短句交错
  词汇: 文学化
  描写深度: 中等
  提示: 全文文风一致，不可偏离
```

## 别名系统（v1.13.x 新增）

角色在正文中可能出现多种称呼（老贾→"姓贾的"）。LLM 写作后必须在正文末尾声明 `【别名】` 行。

### 声明格式

```
【别名】老贾 = 贾老头,姓贾的
【别名】无   ← 未引入新别名时
```

### 代码级阻断

`novel_atomic_writer.py` 在写入时扫描最后几行：
- 检测到 `【别名】行` → 剥离后调用 `register-alias` 注册到 characters[].aliases
- 未检测到 → **HOOK-BLOCK 阻断写入**（第一子结构可豁免，尚无角色）
- 非末章末子结构豁免，末子结构强制要求

### context_loader 输出

```
[硬性] 别名声明（必须，缺失则阻断写入）
  若本次写作引入了角色的别名，请在正文末尾单独一行输出：
    【别名】老陈 = 陈叔
  若未引入任何别名，请输出：
    【别名】无
  atomic_writer 将拦截此标记行，不写入正文。
```

### 别名在检查器中的使用

- **连通性检查**：关键词匹配使用 `name + aliases`，别名被视为有效关键词
- **实体提取**：`novel_entity_extractor.py` 在扫描正文时自动识别别名及其映射

## 实体关系追踪（v1.13.x 新增）

写作完成后自动提取并追踪五类实体及其关系。

### 触发

write-sub 管道中 `novel_entity_extractor.py` 非阻断执行。

### 五类实体

| 类型 | 说明 | 示例 |
|------|------|------|
| character | 角色 | 林铁生、老贾 |
| object | 物品 | 《实用擒拿格斗术》、义肢 |
| location | 地点 | 下层区、老贾的摊子 |
| organization | 组织 | 恒达机电、归元会 |
| data | 数据/信息 | 索赔链记录、格斗术理论 |

### 存储

存入 novel_state.json 的 `entity_tracker` 字段：
```json
{
  "entities": [
    {"id": "e001", "name": "林铁生", "type": "character",
     "attributes": {"status": "受伤", "location": "下层区"},
     "first_chapter": "L01", "first_sub": "S01"}
  ],
  "relations": [
    {"from_entity": "e001", "predicate": "购买", "to_entity": "e002",
     "chapter": "L01", "sub": "S01"}
  ]
}
```

### context_loader 输出

每个子结构写作前输出全量实体关系网：
```
[硬性] 实体关系网（累计 12 实体, 8 关系）
    角色: 林铁生[status=受伤 | location=下层区] [L01S01]
    物品: 实用擒拿格斗术[owner=林铁生] [L01S01]
  ── 关联关系 ──
    林铁生 → 购买 → 实用擒拿格斗术 [L01S01]
```

## 行为摘要（v1.13.x 新增）

finalize-chapter 通过后自动提取本章各角色的行为轨迹。

### 存储

存入 novel_state.json 章节字段的 `behavior_summary`：
```json
{
  "behavior_summary": {
    "林铁生": ["购买格斗术书籍", "尝试关节锁控原理", "反制混混挑衅"],
    "铁心": ["抱怨哥哥乱花钱", "关心哥哥受伤"]
  }
}
```

### context_loader 输出

下一章写作前输出上一章行为轨迹：
```
[硬性] 上一章行为轨迹（L01）
  林铁生: 购买格斗术书籍 → 尝试关节锁控原理 → 反制混混挑衅
  铁心: 抱怨哥哥乱花钱 → 关心哥哥受伤
  提示: 当前章应自然延续以上轨迹，无重大断裂
```

## 结尾收束规范 v2

### 收尾类型标签

末章最后一个子结构的概述**必须**以 `【收尾类型: xxx】` 结尾，三选一：
- `【收尾类型: 封闭式】` — 核心冲突彻底解决，所有角色弧闭合
- `【收尾类型: 开放式】` — 核心冲突有明确结果，但留有合理延续空间
- `【收尾类型: 悬停式】` — 冲突暂不解决，在节奏最高处戛然而止

### 命题约束

末子结构写作前，`novel_context_loader.py` 检测到 `is_ending: true` 时自动输出收尾类型对应的强制命题框。命题框中每一项均为硬约束，LLM 不可偏离。

### 自动标记

`novel_workflow_engine.py plan-chapter` 在执行时自动检测：
- 如果当前注册的章节是末章（chapters[-1]）
- 且当前注册的子结构是该章的最后一个
- → 自动在 novel_state.json 中标记 `is_ending: true`，并从概述中解析 `ending_type`

### 收尾验证

`finalize-novel` 在 fidelity 检查通过后自动调用 `verify-ending`。验证逻辑在 `novel_fidelity.py verify_ending()` 中，分为三种收尾类型的独立检查项：

| 类型 | 检查项数 | 硬性通过要求 |
|------|---------|-------------|
| 封闭式 | 4 | 全部通过 |
| 开放式 | 4（2硬+2软） | 2硬全过 + 2软至少1过 |
| 悬停式 | 6 | 全部通过 |

不通过则阻断 finalize-novel，不推进 phase → complete。报告写入 `data/reports/ending_report.md`。

### 通用规范

- 完成标记替换为 `---全文 完---`
- 不预告下一章
- 末子结构 ≥200 字（防止一句话结尾）
- 最后一句用动作收束（推门。/关灯。/转身。）
