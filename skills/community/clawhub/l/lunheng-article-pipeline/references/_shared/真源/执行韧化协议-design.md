> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# 执行韧化协议（设计者文档）

> **读法**：本文件是主流程读的**协议全文**；7 张角色卡顶部只保留精简索引。协议演进只需改本文件一处，不在各角色卡内联副本。

## 协议三大铁律（每个角色 prompt 头部必读）

### 1. 心跳信号（必须执行）
- **启动 30 秒内**：写自己的心跳文件 `run/<项目>/.tmp/<两位角色号>-<角色名>-heartbeat.md`（状态=🔄 In Progress + 启动时间 + 当前模型）；status.md 由主控独占更新
- **每 5 分钟一次**：在**自己的心跳文件** `run/<项目>/.tmp/<两位角色号>-<角色名>-heartbeat.md` 追加心跳时间戳（格式：`[心跳 HH:MM] model=<model-id>`）；`status.md` 由主控独占写（主控读心跳后转写）
- **超时硬卡（分角色分级）**：
  - **T1-T3 检索员**：10 分钟（中文检索单次 7s+）
  - **T6 批判 / T7 审计**：15 / 12 分钟（批判+修订任务需更长）
  - **T4 分析 / T5 写手**：12 / 15 分钟（旧「8 分钟保持」已废）
  - 各角色硬卡时间点：提前 2 分钟写 `[警告] 已耗时 X 分钟`；提前 1 分钟必须产出 partial output；到点主控 kill + 标记 Failed
  - **读文件 vs 写文件区分**：写文件（落盘）比读文件耗时更长，硬卡判断时对「写文件任务」放宽 2 分钟

### 2. 分阶段 ack（按任务时长分级）

| 任务预估时长 | ack 节点 |
|------------|----------|
| < 2 分钟 | 启动 ack 即可，无需中间 ack |
| 2-5 分钟 | 启动 + 完成二段 ack |
| 5-15 分钟（写手/审计） | 启动 + 25% + 50% + 75% + 完成 五段 ack |
| > 15 分钟 | **禁止**——必须拆任务 |

每段 ack 在自己的心跳文件 `run/<项目>/.tmp/<两位角色号>-<角色名>-heartbeat.md` 追加： `[ack N% HH:MM] <一句话说进度>`；`status.md` 由主控独占写（主控读心跳后转写）。

**完成 ack 的 token 消耗由主控记录（精确机制）**：
角色完成 ack **不**回传自己的 token（子代理拿不到：spawn 返回值无 stats 字段）。token 由**主控**在 `sessions_yield` 收到 completion event 时从事件末尾 Stats line 提取 `Token usage` 记入 status.md 4.7 表：
- **输入**：`Token usage` 的 input（精确值，来自 completion 末尾 Stats line）
- **输出**：`Token usage` 的 output（精确值，来自 completion 末尾 Stats line）
- **总计**：`Token usage` 的 total（input + output）
- 拿不到精确值 = 平台异常（completion event 缺 Stats line），不填「未配置」/「N/A」。

**示例（写手 4758 字）：**
```
[ack 0% 17:35] 已读简报+大纲+10文献+17数据+3案例
[ack 25% 17:38] 完成开篇+第1节（549字）
[ack 50% 17:42] 完成第2-3节（788+592=1380字）
[ack 75% 17:46] 完成第4-5节（599+594=1193字）
[ack 100% 17:52] 完成第6-7节+参考文献（489+432+清单）
```

### 3. LLM 可用性初判（被动观察）

**不做**任何主动探测性请求（不发送探测 ping、不预检模型）；LLM 可用性只在**首次实际调用**时通过响应时间与首 token 延迟观察判定。

- **被动观察**：子代理观察**首次实际 LLM 调用**的响应时间与首 token 延迟；**30 秒内无首字节** → 走降级 fallback（与 dispatch-header ④ 同口径）
- **失败即信号**：401/403/429/配额 → `degraded` 自报 → 候选池下一档（零产物决策树约束）；配额耗尽类 → 暂停等主人

### 3.5 配额耗尽识别 + 授权兜底
> **背景**：SVG→PNG 子代理派发时曾出现 `billing error`。当时主控曾以 exec 亲完成（主人现场知情的一次性授权；该工具现属硬禁用面，此为例外史实、不得据此复用）。现固化为 **Phase 0 显式 opt-in 项**，默认关闭。
> **边界原则**：本技能文档中任何让宿主 agent 调用工具的指令都算技能自身能力，受 `metadata.tools` 声明约束。技能文本**不包含**任何「主控例外」豁免——永久拒绝（exec/process 等）对主控、子代理、fallback 路径、错误恢复流程一律生效。子代理卡死时主控的合法兜底只有：暂停询问主人 / 换 provider 重试 / 用白名单工具接力。

**识别（LLM 推理判定，不靠硬阈值）**：
- **关键信号**（任一命中即视为配额类失败）：
  - 子代理回复中包含：`billing error` / `quota exceeded` / `insufficient balance` / `429`（响应头带 `rate limit`）/ `payment required` / `usage limit` / `over quota`
  - **LLM 推理判定**：主控读到这些信号时，**推理为**「这是账号级配额问题，不是网络/超时类临时问题」，与 ping 超时区别开
- **判定时机**：**不限定硬性秒数** —— 主控根据当前任务进展感判断（如果子代理刚启动就连续报错→几乎肯定是配额；跑了 10 分钟才出问题→可能是临时网络）。LLM 推理 vs 硬代码 `if elapsed > 300:`，区别就在这里。

**处理（默认暂停等主人）**：
1. **status.md 状态标注**（建议做法，**不强制**）：写一行记录配额告警
2. **不再自动切 fallback**（**硬建议**）：配额耗尽是账号级问题，切单个 fallback 不解——下一档同样会撞同个账户的余额。**LLM 推理例外**：主控推理判断「切换到不同 provider 可能解」时，仅换 provider 不换同 provider 的档位
3. **暂停流水线，向主人呈报**（fail-closed，**默认必停**）：主控在对话里告知「本轮 LLM 配额可能耗尽」+ 3 选项，**等主人拍板后才继续**：
   - □ 主人切其他 provider（如 OpenAI / Google）重试子代理
   - □ 主控用白名单工具（read/write/edit）接力完成该子代理任务（零 exec 路径，任何宿主环境均合规）
   - □ 等下个计费周期（保留 partial 产物，安全终止）
   - **禁止**：主控自行调用 exec/process/browser 等永久拒绝工具——该约束无例外，Phase 0 一般性同意不覆盖工具/权限变更
   - **无应答兜底**：主人无应答（分钟数真源 = [`phase-order.yaml`](phase-order.yaml) `owner_timeout_policy.no_answer_minutes`，本文件不重列）→ 按 ③「等下个计费周期，保留 partial 安全终止」安全终止并回报
4. **Phase 0 opt-in 预授权（可选，默认关闭）**：若主人在 Phase 0 任务简报「授权记录」段明确勾选「配额耗尽时授权 X（换 provider / 白名单接力）」，配额事件发生时主控按预授权选项直接执行并事后通报，无需再次等待。**未勾选 = 无预授权 = 必须暂停等主人**。
5. **记录与追溯**：配额事件 + 主人选择 + 执行动作写入 status.md「配额事件」段，供 T7 审计追溯

## 改造要点（角色卡层面）

每个角色 prompt 头部新增段落：
```markdown
## 执行韧化协议（30 秒心跳 + 分阶段 ack）

1. 启动 30 秒内写自己的心跳文件（`run/<项目>/.tmp/<两位角色号>-<角色名>-heartbeat.md`，状态=🔄 In Progress + 启动时间 + 当前模型）；status.md 由主控独占更新
2. 按任务时长选择 ack 节奏（<2分钟/2-5分钟/5-15分钟）
3. LLM 可用性初判：子代理观察首次 LLM 调用响应；30 秒无首响应则降级 fallback
4. 超时硬卡（角色分级）：按「`_shared/真源/主动介入机制.md` 硬卡阈值表」执行（T1-T3 10 分钟 / T4 12 / T5 15 / T6 15 / T7 12 / T9 10 / G14 8）；到点主控 kill + 接受 partial
5. **禁止假装在线**：心跳 ack 必须真实反映进度，禁止编造 ack
```

## 改造要点（主控层面）

主控在 spawn 子代理时：
- 每次 spawn 后立即 watch 子代理 status.md 心跳（不再静默等待）
- 30 秒内未心跳 → 主控 console 警告，但**不**自动 kill（给子代理多一次机会）
- 5 分钟无 ack → 主控主动 ping 子代理 session（sessions_history）
- 超角色分级阈值无 ack + 无产出 → 主控 kill + 标记 Failed + 决定是否重试（阈值表见主控扩展职责 §二十二）

### 4. 编排循环防空转
> **背景**：编排循环对「完成事件恰好投递一次」过度依赖，缺三道防御——曾致 T8→T5 交接点的 spawn tool call 丢失而主控误以为已 spawn。

**主控编排循环必须遵守的三防**：适用于 T1→T3 / T3→T4 / T4→T8 / T8→T5 / T5→T4（修订）/ T5→T7 等**所有 T 角色 spawn 交接点**。

#### 4.1 spawn 后验证落地（必做）
每次 `sessions_spawn` 后，**必须**立即调 `subagents(action=list)` 确认 runId 出现在 active runs，再进入 yield。没出现 = spawn 丢失，立即重试（≤2 次）：
```python
# 伪代码（spawn 验证）
run = sessions_spawn(task=...)
if not subagents_has_active(run.runId):
    # spawn 丢失，判定为 duplicate 事件 / 网路问题
 log("[防御] spawn runId={} 未落地，重试".format(run.runId))
    run = sessions_spawn(task=...)  # 重试 1 次
```

#### 4.2 yield watchdog 超时自查（必做）
> ⚠️ **本节的形态是「事件驱动的单次自查」，不是轮询循环。** `sessions_yield` **会结束当前 model turn**——完成事件只能作为**下一条 message** 到达，**不可能在同 turn 内循环等待**。官方明确：不要为等待而循环调用 `subagents list` / `sessions_list` / `sessions_history`，**仅调试时按需查一次**（`docs/tools/subagents.md`）。

**判据**：收到完成事件即推进编排；**若本 turn 未收到预期完成事件**（或收到同一子代理的重复事件），做**一次**自查 `subagents(action=list)`（宿主强制 self-spawn 列表）：
- 预期角色仍在 active runs + 最近有 status.md 心跳 → 子代理真在跑，**结束本 turn 继续等下一事件**（记录已等待 X 分钟）
- 预期角色不在 active runs（已结束但未投递完成事件）或同一子代理完成事件重复 ≥2 次 → **duplicate 事件嫌疑**，补 spawn：
```python
# 伪代码（事件驱动 yield watchdog —— 无 while、无轮询）
# 入口：本 turn 已 sessions_yield，但未收到预期 completion（或收到重复事件）
def on_yield_turn_end(role, runId):
    if expected_completion_seen_this_turn:
        # 幂等检查：status.md 该角色是否已 Done？
        if is_role_done(status_md, role):
 log("[幂等] {} 完成事件已处理过，忽略 duplicate".format(role))
            return  # 不重复推进
        advance_pipeline()  # 推进编排
        return
    # 未收到预期事件 → **单次** on-demand 自查（仅一次，非循环）
    if subagent_alive_in_active_runs(runId):
 log("[防御] {} 仍在 active，结束本 turn 等下一事件".format(role))
        return
 log("[修复] yield 超时 + 子代理不在 active = spawn 丢失，重派")
    respawn()  # 补 spawn
```

#### 4.3 完成事件幂等处理（必做）
收到任何角色完成事件时，**先查 `status.md` 该角色是否已 Done**——已 Done = duplicate 事件，忽略不重复推进：
```python
# 伪代码（完成事件幂等）
def on_completion(role, runId):
    if status_md[role]['state'] == 'Done':
 log("[幂等] {} 已在 Done，忽略 duplicate 完成事件 runId={}".format(role, runId))
        return  # 静默忽略，不推进下一个 T
    # 正常推进
    status_md[role]['state'] = 'Done'
    spawn_next_role()
```

#### 4.4 交接点「三段式 spawn」
关键交接点（T8→T5、T4→T8、T5→T4 修订）**必须**走「spawn → 验证落地 → 确认后 yield」三段，**禁止**「spawn → 直接 yield」：
```
# 错误（之前模式，duplicate 事件可击穿）
sessions_spawn(T5)
sessions_yield()  # ← 被打断则空转

# 正确（修复后）
sessions_spawn(T5)
assert subagents_has_active(runId)  # 验证落地
sessions_yield()  # 确认后才 yield
```

#### 4.5 诊断边界（sessions_history 措辞歧义）

> **一句话**：本协议区分两类诊断能力，边界不可混：
> - 🔒 **仅人类主人诊断**：读 OpenClaw runtime 内部会话轨迹文件 / 执行 shell 命令（exec/process）——**agent 零 exec，永不调用**
> - ✅ **主流程诊断**：用白名单工具（subagents / sessions_history / progress_card）看**论衡自己 spawn 的子代理**——**仅限 self-spawn 的子代理，不跨会话抓取**（其发现职责由宿主强制的 subagents 列表承担，不枚举宿主可见会话）

##### 🔒 仅人类主人诊断（agent 零 exec，主流程永不调用）

> 读取 OpenClaw runtime 内部会话轨迹文件不在论衡主流程职责范围（属 runtime 内部诊断）。**以下步骤仅供人类主人手动排查论衡编排故障时在 host shell 执行**：
>
> <!-- 人类诊断命令（agent 零 exec，主人手动执行） -->
> - 进入 OpenClaw runtime 内部会话目录
> - 取最近的会话轨迹文件
> - 统计 `sessions_spawn` 调用次数
> - 统计 `sessions_yield` 调用次数
> - 取出现频次前 5 的子代理 session_key

##### ✅ 主流程诊断（白名单工具，仅限 self-spawn 子代理）

**论衡主流程实际能跑的诊断**（用 read 工具推理 / 用 progress_card 打钩，全部是 `metadata.tools` 声明的白名单工具）：
- `subagents(action=list)` —— 看当前 session 有没有真的 spawn 出子代理、runId / sessionKey 在不在 active（宿主强制 self-spawn 列表）
- `sessions_history(sessionKey=...)` —— **仅限查看论衡自己 spawn 的子代理会话产物**（`subagent:xxx` sessionKey，来自 spawn 返回或 subagents 列表），**不跨会话读取、不抓取其他 session 的隐藏状态**
- `progress_card` 打钩「§ 4.1 spawn 验证」「§ 4.2 watchdog 自查」「§ 4.3 幂等检查」

**论衡 agent 不调用的**：exec / process / 读 OpenClaw runtime 内部路径 / sha256 直接计算（这些是**人类主人**的能力，不在 agent 范围内）。

> **边界澄清**：`sessions_history` 是白名单工具，但论衡**只用它读自己 spawn 的子代理**（`subagent:xxx`），用途是编排监控（看子代理有没有产出、有没有死循环），**不是跨会话读取历史或抓取隐藏状态**。上方「🔒 仅人类主人诊断」段的 `session_key` 字样指主人手动排查时在 host shell 查看轨迹文件，与主流程 `sessions_history` 是两回事，勿混。

#### 4.6 spawn 后静默探测（三子代理 401 静默退出主控无感知）

spawn 任何子代理后，主控**不能只等完成事件**。

> **与 §4.2 的关系**：§4.2 禁止的是「**轮询循环**」（连续 tick 盯着看）；本节要求的是「**事件驱动的点状主动探测**」——**两个固定探测点 + 一次产物落盘校验**。二者不矛盾；原措辞未区分，曾致执行时只能二选一（实际退化为「静默等硬卡」）。

**两个强制探测点（不可省）**：
- **探测点①**：spawn 落地验证后立即（§4.1）；
- **探测点②**：首个 ack 缺失时（到硬卡警告点仍无 ack）。
- 判定：status=running 但 tokens=0 且 history 停留在初始 prompt → 判「未启动」，走下方决策树。
- 子代理遇 provider 401 / 配额耗尽：**在 final message 返回 `{"status": "degraded", "reason": "<错误摘要>"}`**，禁止 0 tokens 静默退出（各 dispatch 已注入此条）。

**零产物 / tokens=0 决策树**：

| 步 | 条件 | 动作 |
|---|---|---|
| ① | 子代理声称完成 | **`read` 其产物路径**：不存在 / 字节数 0 → 判**零产物** |
| ② | 判零产物 | 同档重派，**上限 2 次**（每次记独立行入 status.md） |
| ③ | 同档 2 次仍零产物 | **降档重派**（按候选池下一档，记降档事实） |
| ④ | 降档仍失败 | 按 §3.5 三选项**暂停问主人**（不自行硬推） |

> **适用边界**：本树**只用于「未启动 / spawn 丢失」**（tokens=0 ∧ history 停在初始 prompt）。**已启动但硬卡静默**（零产物 ∧ 超 `runTimeoutSeconds` ∧ 心跳未续）**不走本树** —— 按 [`../agents/00-主控-扩展职责.md`](../../agents/00-主控-扩展职责.md)「§不通过处理」状态机：主控亲写兜底 + status 记录 + 告知主人，**不重试**。
>
> 「正常 ack 但零产物文件」是最典型的静默失败；错误信息模板见 `errors.md` E13。

**主控 fallback 顶替时的五条硬要求**：
①status.md「降级运行记录」段写独立行 `⚠️ DEGRADED RUN：<角色> 由主控顶替（<原因>）HH:MM`；②亲出产物头部强制标注 `[主控 fallback 产物 / <实际模型> / <日期>]`；③**亲出前必 `read` 对应角色卡 + dispatch 最新版**，按当前版本格式产出（禁止凭 memory 写旧版格式）；④对话中向主人显式报告降级事实；⑤**【新增】兜底产物必须重跑该角色原本对应的门控**（M 门 + 该角色 G 项），执行记录写入 `final/局限.md` 或 status.md「降级运行记录」段，由 T7 复核 —— 原四条只看「格式合规 + 告知」，等于绕过了该角色的全部验收门。

**修订轮作者标记**：
- 修订轮（T5/T7）产物的每一段末尾由**产出者自己**写 `<!-- src:<角色>|<model>|<HH:MM> -->`。
- 主控拼接时**不得删改已有标记**；主控新增/补写的段落必须写 `<!-- src:T0-fallback -->`。
- 审计员（T7）统计「主控占比」：**> 15% 即 P1**。
- 效果：把「代笔」从不可检测变为**可统计**。

#### 4.7 报告长度上限 + 超限分块协议

> **背景**：T6 v1 首跑 16k 字符超外化阈值被截 → 主控被迫分块拼接 → 质量降级。根因 = 报告无长度上限 + fallback 无分级。

**1. 硬上限（单一真源 = phase-order.yaml 各节点 `output_chars_max`）**：

| 产出 | 上限（字符量级，read 估算非 wc） |
|------|------|
| T4 分析大纲 | ≤12000 |
| T6 批判报告 | ≤12000 |
| G14 检测报告 | ≤6000 |
| T7 审计报告 | ≤10000 |
| T9 审稿报告 | ≤15000 |
| T8 终检说明 | ≤10000 |

> 口径：上限是「回传长度」控制，不是「内容深度」限制——超限优先砍展开论述、保结论 + 证据编号；禁止砍维度本身。

**2. 超限分块协议（子代理侧主动，主控侧接收）**：
- 子代理回传前自查：read 估行数/字符量级，超限 → **按报告结构分块回传**（T6 按 C1-C7、T7 按 G 门分组、T9 按 6 维度），每块 ≤ 上限，块间用分隔行 `<!-- chunk N/M -->`
- 单块仍超 → 砍细节保结论（各块结论 + 证据编号必留，展开论述可省）
- 主控侧：逐块接收 → `write` 落盘拼接 → 「读盘确认铁律」核验首尾与块数；块缺失 → 立即要求补块，不静默接受不完整报告
- 禁止「一次性全量发出赌截断」——截断后丢失内容主控无从知晓，是质量黑洞

**3. fallback 质量分级（主控拼接/顶替时的接受标准）**：

| 级 | 定义 | 处置 |
|----|------|------|
| **A 级（可接受）** | 主控仅机械拼接各块（子代理内容完整、仅因分块需拼接），未改实质内容 | 正常继续；产物头部标注 `[多块拼接产物]` 即可 |
| **B 级（警告）** | 主控做了内容补充/裁剪/重组（如砍细节保结论、补缺失块概述） | 产物头部标注 `[主控 fallback 产物]` + **逐段标注哪些段含主控补充**；对话中向主人报告 |
| **C 级（阻断）** | 主控不得不自己写实质段落（子代理核心产出丢失/静默退出） | **触发完整重跑**（同角色同档重 spawn，或降档后重跑）；禁止以主控代写冒充子代理产出 |

> 与既有标记的关系：旧版 `[主控 fallback 产物 / <实际模型> / <日期>]` 对应 B 级；回传截断标记（主控落盘后对照回传原文抽查首尾）是 A/B 级的检测手段，保留。

## 三检索员并行监控补充

> 背景：v2.1.8 主控一次性 spawn T1 + T2 + T3 三个独立 sessions_spawn（同一 function_calls 块内），三方并行。与传统单 spawn 不同，主控需额外监控：

- **三方并行心跳看总和**：T1+T2+T3 三个 sessions 都心跳后才视为「三方并行存活」——任一 30s 未心跳 = 该 T 心跳异常
- **三方独立超时**：硬卡阈值对每个 T **独立生效**——T1 超时 ≠ T2/T3 也超；主控只 kill 超时的那个，其他不受影响
- **runtime vs 墙钟区分**：runtime = 模型推理 + 工具调用纯耗时；墙钟 = runtime + OpenClaw 调度 + 子会话启动 + 文件落盘；硬卡阈值**指的是墙钟**（含调度延迟），runtime 通常 1-3 分钟
- **失败隔离**：T1 失败不影响 T2/T3 继续；T3 失败不影响 T1/T2；主控收到失败 ack 后标 `Failed` + T0 合并层标「案例缺角」/「文献缺角」/「数据缺角」对应降级
- **三方同步 ack 节点**：三方共享同一 Phase 1 阶段行的 status.md（避免三份独立 status 难以合并）