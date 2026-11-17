# 常见错误用法完整清单（Common Mistakes）

> 每条附「**为什么会错**」——讲机制而非现象；全部条目来自本项目实测踩坑（[A] 实证）。SKILL.md 反模式速查表是子集，本文件是完整版。
>
> **状态图例 / Status legend**：🔧 **现行**——机制层无法完全防止，用户仍可能犯（改写/加固注意力）；✅ **已修复**——机制层已封堵该路径（命令/守卫/脚本强制），条目仅作历史回溯，不代表当前缺陷。

## 沉淀侧（T4）

### 1. 注入「成功总结」型 strategy　`🔧 现行`

> 机制说明：叙事守卫过滤（REPAIR_SIGNAL_RE），写前自检。
- **EN**: A 'conclusion' in a soft prompt is zero information for an agent - only executable actions change the next turn. Write executable fixes (params/commands/encodings).
- **现象**：写成 "脚本运行正确，结果如下…"。
- **机制**：软提示里「结论」对智能体是零信息；只有**可执行动作**能改变下一轮行为。
- **后果**：守卫过滤 / 等效噪声，比不注入更差（实测 +36pp）。
- **正确**：写成可执行修法（含参数/命令/编码："用 `encoding='gbk' 打开`"）。

### 2. FIX 留占位符就 --commit　`🔧 现行`

> 机制说明：depositionGate 拒绝并给出修正指引。
- **EN**: depositionGate (0.17.0 fail-closed) rejects placeholders - by design, not a bug. Fill in the real fix in draft first.
- **现象**：草稿里 FIX 还是 `<在此填写可执行修法>` 就落库。
- **机制**：depositionGate（0.17.0 fail-closed）会拒绝——这是设计而非故障。
- **后果**：入库失败，回显给出修正指引。
- **正确**：补上真实修法再提交。

### 3. 用 distill 多 signals 碰运气　`🔧 现行`

> 机制说明：门控机制不改，靠写前判断。
- **EN**: Targeting scores on the INTERSECTION with query tokens - piling on unrelated words dilutes rather than helps. Write signals that will truly intersect the query.
- **现象**：`--signals a,b,c,d,e` 堆一串词希望多召回。
- **机制**：对靶打分按与查询词的**交集**——堆无关词不提升命中，反而稀释。
- **后果**：召回率不升，误判"库没用"。
- **正确**：signals 写**与查询词会真实交集**的信号词（报错类型/工具名/场景词）。

### 4. 该用 draft 时手写 distill，该用 distill 时硬套 draft　`🔧 现行`

> 机制说明：两入口并存，需按场景选。
- **EN**: `draft` = single-pit guided (auto signals + AVOID prefill + anti_patterns); `distill` = manual with explicit signals. Use draft for pasted errors, distill for structured multi-pit batches.
- **机制**：`draft` = 单坑引导式（自动抽 signals + 预填 AVOID + anti_patterns）；`distill` = 手写式（已明确 signals/批量）。
- **正确**：贴报错场景用 draft；已结构化多坑用 distill。

## 召回侧（T1/T3/T5）

### 5. 用位置编号回填（register-hit <N>）　`✅ 已修复 · 0.18`

> 机制说明：按 gene_id 寻址（位置写法仍兼容但并发下会漂移）。
- **EN**: Positional back-fill drifts under concurrency (shared selection snapshot). Use `--register-hit --gene <asset_id|gene_id>` since 0.18.
- **现象**：多会话并行时按 `#N` 回填。
- **机制**：选择快照是共享单文件，会被其他会话的 recall 覆盖 → 编号漂移（实测 63→65 错记）。
- **正确**：`--register-hit --gene <asset_id|gene_id>`（0.18 起）。

### 6. 任务结束不回填　`🔧 现行`

> 机制说明：回填无强制，靠纪律；--negate 补分母。
- **EN**: No back-fill = no inject-to-effective conversion rate, dead fixes go undetected. Use `--negate` too - it feeds the denominator.
- **现象**：召回了、采用了，但没 register-hit。
- **机制**：不回填 → 「注入→有效」转化率算不出，失效修法发现不了。
- **正确**：T5 收尾时一行命令回填；没效果用 `--negate` 同样有价值（进分母）。

### 7. 用字符串计数统计错误（"提到 error"≠报错）　`🔧 现行`

> 机制说明：只信权威标志的规则需人执行。
- **EN**: Text mention != real error (9 false positives historically). Only trust authoritative flags: isError=true / non-zero exit_code.
- **现象**：grep 日志里的 "error" 字样计错误数。
- **机制**：正文提及 ≠ 真错误（曾把成功命令里带 error 字样的输出误判，9 例）。
- **正确**：只信权威标志 `isError=true` / 非零 `exit_code`。

## 共享池侧

### 8. 以为 submit 会把待审基因推出去　`🔧 现行`

> 机制说明：池语义（shareable AND approved）需理解。
- **EN**: Pool semantics (0.18.1) = only shareable AND approved genes are exported; pending ones stay local. Approve first, next submit picks them up automatically.
- **机制**：池语义（0.18.1）= **只导出 shareable 且已审核通过**的基因；待审留在本地。
- **正确**：先 `approve`，下次 submit 自动带上；submit 会报告"待审未推池 N 条"。

### 9. 把项目专属基因标 shareable　`🔧 现行`

> 机制说明：靠分享者自律判断。
- **EN**: The pool is cross-machine shared - general lessons only. Project-specific genes are noise for others and may carry private details.
- **机制**：池是跨机器共享——只放**通用**教训；项目专属（某私有工程的实现细节）进池对别人是噪声，还可能带私有信息。
- **正确**：仅通用教训标 `--shareable`；项目专属留本地库。

### 10. 用 community 池不设审　`✅ 已修复 · 0.18.1`

> 机制说明：import 默认 community→隔离，审门不可绕过。
- **EN**: `gene import` defaults to community -> quarantined (review gate never bypassed). Community-pool genes must be approved before injection.
- **机制**：`gene import` 默认 community → **待审**（审核门控不被绕过）。
- **正确**：社区池基因 import 后必须 approve 才注入。

## 验证侧（元教训，本项目作者亲测）

### 11. 写操作后只看退出码　`✅ 已修复（approve 假阳性已修）· 纪律仍现行`

> 机制说明：approve 幂等写入已修；"换路径读回"仍是纪律。
- **EN**: Never trust exit codes alone - proven: approve false-positive (idempotency skipped the write, ledger unchanged). Read back via a DIFFERENT code path after every write.
- **现象**：命令 exit 0 就当成功。
- **机制**：实测 approve 假 ✓（幂等逻辑跳过写入，台账根本没变）。
- **正确**：写后**换一条代码路径回读**验证（approve 后直接读台账文件）。

### 12. 验证新版本时跑错副本　`🔧 现行`

> 机制说明：多副本并存，靠绝对路径+版本核验纪律。
- **EN**: Same machine, multiple versions coexist (release stage / local skill / backups). Always use absolute paths to the target build dir; verify version before running.
- **现象**：cd+相对路径或默认技能目录，跑到旧版报「未知命令」。
- **机制**：同机器多版本并存（发布 stage / 本地技能 / 备份目录）。
- **正确**：绝对路径指向目标构建目录；跑前核对 version。

### 13. 复合命令测失败语义　`🔧 现行`

> 机制说明：shell 语义，需构造时注意。
- **EN**: A failing segment followed by a success tail exits 0 overall - the failure is masked. The failing segment must be the LAST statement of the whole tool call.
- **现象**：`失败段; echo ok` 整体 exit 0，失败被掩盖，误判"捕获失败"。
- **正确**：失败段必须是**整条工具调用的最后一句**。

### 14. 发版基座用旧快照　`✅ 机制已防`

> 机制说明：build_stages/verify_stages 脚本化门禁（0.25）。
- **EN**: Building a stage from a stale snapshot loses local hot-fixes (twice: local, then the release artifact). `diff -r` local vs base before building; after release the diff should be empty.
- **现象**：stage 从旧 publish_clean 复制，本地热补丁丢失（先丢本地、再丢发布物）。
- **正确**：构建前 `diff -r 本地技能目录 基座目录` 逐条裁决；发布后 diff 应为空。
