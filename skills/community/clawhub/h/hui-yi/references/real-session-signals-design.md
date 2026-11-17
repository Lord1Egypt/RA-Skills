# Real Session Signals Integration Design

这份设计稿定义 Hui-Yi 如何从 **真实会话** 自动累积 `session_signals`，让 repetition-first 不只是静态字段，而是有稳定的数据来源。

原生自动识别与回答前召回参见 [native-memory.md](native-memory.md)。下文描述保留的可选旧 hook 协议，不是当前原生自动采集入口。

## 1.2.13 实现约束与阅读方式

本文保留早期方案的取舍记录；下文“建议 / Phase / 推荐下一步”不表示尚需自动执行的工作，也不是当前 CLI 合约。当前实现以 `SKILL.md`、`README.md` 和源码为准：

- 仅在当前对话、近期/系统记忆及相关工具记录不足、明确需要低频归档知识时选择 Hui-Yi；泛泛的“之前 / 你记得吗”不自动选择 skill。
- 可选 TS hook 必须已由用户安装/启用，并收到可信宿主 Hui-Yi selection，或映射后的 `context.body` 开头的严格 `/hui-yi <查询>` / `/hui_yi <查询>` 文本命令。命令不区分大小写，ASCII 空格/tab 后查询不能为空；前导空白、引用/嵌入/其他前缀、空命令及 `bodyForAgent` 独有命令不触发。没有普通正文 heuristic fallback；批量扫描 transcript 未实现，也未被此设计授权。
- OpenClaw 2026.9.5 原生 mapper 不发 selection metadata；显式命令仅在未包装的映射正文到达 hook 时适用。正文被渠道包装或命令被原生快速路径提前消费时用 CLI/adapter；隔离 mapper 事件验证不等于真实渠道端到端验证。
- TS handler 独立 inline 执行；Python `core/signal_detect.py`、`core/signal_apply.py`、`core/signal_pipeline.py` 组成显式 CLI 管线。runtime probe 在进程内调用 Python adapter，`--stdin` 可承载输入正文。
- 自动 hook 仅写 weak activation；强信号来自明确反馈/调用，不因“回忆”措辞自动变 strong。日内按 session 指纹、note、日期和 source 去重；history 每 note 至多 20 项。连续会话窗口目前为 14 天，不保证扫描过所有会话。
- metadata 只保存 session 指纹；普通/debug hook 日志都不保留正文、原始身份/metadata、note 标题/路径或匹配词。Python detector/pipeline 默认也省略 query/context 与匹配词；显式 `--include-sensitive` 才输出这些敏感诊断字段，仍不输出 raw session key。adapter/probe 没有敏感输出开关。
- archive 是 workspace 共享的；session 指纹不构成授权。文件辅助函数拒绝链接、junction/reparse point、硬链接、特殊文件并复查身份。Python 暂存写入时先复制现有 Windows DACL、再写数据及原子替换；TS 的 POSIX/Windows 新文件使用暂存原子替换，Windows 已有文件通过核验描述符原位写入以保留 DACL，失败时尽力回滚但不保证崩溃原子性。工作区必须由可信 OS 用户控制，这不是对抗同账户并发目录置换的内核沙箱。
- loading skill 不授权 cooling 或后台采集；selector 不注册任务/发送消息；保留 repetition-first 与 Ebbinghaus pacing。

---

## 1. 目标

当前 Hui-Yi 已经具备：
- `Session signals` 字段可存储
- `repetition_signal()` 可计算
- `review.py` / `scheduler.py` 已能消费 repetition 信号

早期设计要补齐的一层（现已有显式 CLI 和 opt-in hook 实现）：

> **如何把真实对话中的重复出现，自动写进 cold memory note 的 session_signals。**

这层接通后，Hui-Yi 才真正从“支持 repetition”升级为“由 repetition 驱动”。

---

## 2. 设计原则

### 2.1 主原则
- 真实会话中的反复提及，才是强化主信号
- 时间只负责 pacing，不负责独立定义“该不该复习”

### 2.2 边界原则
- 不直接替代 OpenClaw 当前会话记忆
- 不扫描所有历史文本做重型索引
- 不把每次命中都当成一次高质量强化
- 不因为单次关键词碰撞就写高 repetition

### 2.3 工程原则
- 第一版尽量薄，不做复杂 NLP 管线
- 优先使用 note 已有 metadata：title / tags / triggers / semantic context
- 将“候选命中”和“确认强化”分层处理
- 允许 false negative，多于 false positive

### 2.4 隐私原则（notice / minimization / retention）

- **告知（notice）**：session_signals 的采集是显式 opt-in 的——hook 必须由用户运行
  `install_hook.py` 安装，并用 `--enable` 启用（启用前打印披露）。`SKILL.md`、
  `manifest.yaml`、`HOOK.md` 都声明了采集内容。
- **最小化（minimization）**：写回 note / tags.json 的只有激活计数和日期；
  `session_key` 只以截断 sha256 指纹落盘，原始 user/chat/thread 标识和消息正文
  不写入 signal metadata。普通与 `HUI_YI_HOOK_DEBUG=1` 日志均不含正文、原始标识、事件 metadata、note 标题/路径或匹配词；debug 只增加生命周期/计数。
- **留存（retention）**：`signal_history` 每条 note 上限 20 条；hook.log 在 256KB
  自动轮转；用户可随时删除 `hooks/hui-yi-signal-hook/hook.log`，或运行
  `scripts/scrub_metadata.py` 清洗 legacy metadata。

---

## 3. 总体架构

建议拆成两层：

### Layer A. Session Mention Detection
负责：
- 从当前会话片段提取潜在 memory hits
- 判断哪些 cold notes 被再次提及
- 生成一次“激活事件”候选

### Layer B. Signal Aggregation
负责：
- 将激活事件写回对应 note 的 `Session signals`
- 更新 `last_activated`
- 更新跨会话与连续会话计数
- 控制去重、衰减和单会话上限

一句话：

- **Detection 负责发现被提到了什么**
- **Aggregation 负责决定这次提及值不值得算成 repetition**

---

## 4. Signal 模块分工

当前模块位置：

```text
core/
├── signal_detect.py
├── signal_apply.py
└── signal_pipeline.py
```

### 4.1 `signal_detect.py`
输入：
- 当前会话文本 / query / context file / stdin
- `memory/cold/tags.json`

输出：
- 候选 note 列表
- 每个候选的命中原因：
  - title overlap
  - tag overlap
  - trigger overlap
  - semantic context overlap
  - full-text weak match（可选）

建议支持：
- `--query "..."`
- `--context-file file.txt`
- `--stdin`
- `--json`

### 4.2 `signal_apply.py`
输入：
- note path / slug
- activation event
- session id
- event strength

职责：
- 更新 note 中的 `Session signals`
- 控制单会话去重
- 决定是否增加：
  - `current_session_hits`
  - `recent_session_hits`
  - `cross_session_repeat_count`
  - `consecutive_session_count`
- 更新 `last_activated`

### 4.3 `signal_pipeline.py`
输入：
- 当前真实会话上下文
- 当前 session id
- 可选 user turn / full snippet

职责：
1. 调 `signal_detect.py`
2. 做阈值过滤
3. 对高置信候选调用 `signal_apply.py`
4. 输出本轮被强化的 notes

第一版这是最实用的薄接法。

---

## 5. Session ID 模型

要想区分“同一会话重复”和“跨会话重复”，必须引入统一 session 标识。

运行时字段（不原样持久化）：

```text
session_key = <channel>:<scope-type>:<scope-id>:<thread:id-or-main>
```

实际最小可行值：
- direct chat: `feishu:user:ou_xxx:main`
- group thread: `feishu:chat:oc_xxx:thread:omt_xxx`
- normal group stream: `feishu:chat:oc_xxx:main`

如果上层拿不到 thread id，也至少保证：
- chat_id 稳定
- 主会话与线程会话尽量分开

---

## 6. Activation Event 结构

早期概念事件示例，仅用于解释内部输入，不是落盘格式或当前默认输出。例子里的 raw session/query 不得复制到 signal metadata 或 hook.log：

```json
{
  "session_key": "feishu:user:ou_xxx:main",
  "activated_at": "2026-04-12T19:20:00+08:00",
  "query": "hui-yi 的 decay 和 openclaw 记忆边界",
  "matched_note": "memory/cold/hui-yi-memory-boundary.md",
  "match_score": 0.76,
  "match_reasons": ["title", "tags", "semantic_context"],
  "event_strength": "medium",
  "dedup_key": "sha256:example-only|hui-yi-memory-boundary|2026-04-12|signal_pipeline"
}
```

其中：
- `match_score` 用于过滤噪音
- `match_reasons` 用于调试
- `event_strength` 用于区分弱命中/强命中
- `dedup_key` 用于防止同一轮对话疯狂刷计数

---

## 7. `Session signals` 的推荐语义

当前字段建议定义为：

### `current_session_hits`
当前 session 内，本 note 被确认激活的次数。

规则：
- 单 session 内增长
- session 结束后不必永久累加到无限大
- 更适合当作“实时热度”字段

建议：
- rebuild / apply 时保留最近值
- 新 session 首次命中时重置或滚动转存

### `recent_session_hits`
最近若干 session 中，该 note 的累计激活次数。

规则：
- 反映近端重复性
- 可做轻量衰减

### `cross_session_repeat_count`
有多少个不同 session 里，这条 note 被再次激活。

这个字段很关键，因为它比单 session 连续提三次更有价值。

### `consecutive_session_count`
连续多少个 session 都出现过这条 note。

这个字段可用于识别：
- 短期持续关注
- 主题正在回流
- 值得提前强化

### `last_activated`
最近一次真实会话激活时间。

---

## 8. 推荐计数规则

### 8.1 单会话去重
不要把同一轮里连续 5 次提到同一个词，当成 5 次高价值强化。

当前实现按 `session 指纹 | note | 日期 | source` 去重；15 分钟滑动窗口未实现。history 保留最近 20 项，不是无限期历史集合。

### 8.2 跨会话更值钱
建议权重：
- 同一 session 重复提及：低到中权重
- 不同 session 再次出现：高权重
- 连续多个 session 都出现：更高权重

### 8.3 强度应来自实际结果
历史措辞不自动授权激活，也不自动提升强度。可信宿主 selection 或严格显式文本命令后的 hook 命中只写 `weak`；成功 recall 后真实 `feedback useful=yes` 可以写强激活。显式 CLI 的强度参数由调用者在授权任务中选择，不根据一句“你记得吗”推断成功强化。

### 8.4 助手主动 resurfacing 不自动算成功强化
如果是系统自己把 note 捞出来，不应直接加很强 repetition。
只有当：
- 用户继续围绕它追问
- 或 feedback 标记 useful

才应提升更强的 session signal。

---

## 9. 接入点建议

### 方案 A. 在 `review.py resurface` 之后接入
适合第一版。

流程：
1. 用户当前 query 进入 `review.py resurface`
2. 命中的 note 先作为候选
3. 对高置信候选写一次 activation event
4. 当用户继续追问或 `feedback useful=yes` 时，再追加强化

优点：
- 最小改动
- 复用现有 ranking
- 不需要另起复杂管线

缺点：
- 只有走 Hui-Yi recall 流程时才积累信号
- 不能覆盖所有真实会话

### 方案 B. 在上层 agent 语义命中 Hui-Yi 时接入
流程：
1. agent 判断当前请求命中 Hui-Yi
2. 把当前 query / snippet 传给 `signal_pipeline.py`
3. 自动累计候选 note 的 activation event

优点：
- 更接近真实会话
- 不必等用户显式运行 review 命令

缺点：
- 需要上层 skill 框架配合

### 方案 C. Heartbeat / transcript 批处理（未实现的历史提案）
流程：
1. 定期扫描最近对话摘要或 session transcript
2. 对命中的 note 批量累计 signals

优点：
- 覆盖更广

缺点：
- 容易重、容易脏、容易误记
- 我不建议作为第一版主路线

### 原始推荐顺序（历史记录）
1. 先做 A
2. 再做 B
3. 最后再考虑 C

---

## 10. 对现有脚本的最小修改建议

### `review.py`
增加：
- `--write-signals`
- 在 `resurface` / `feedback` 成功路径里触发 activation writeback

### `scheduler.py`
保持只读，不建议直接写 signals。
它是 selector，不该偷偷改 note。

### `rebuild.py`
保持可重建 `Session signals` 元数据索引，但不负责从原始会话里“推断新信号”。

### `decay.py`
不要主导 `session_signals` 的衰减，只能做轻量维护或 flag。

---

## 11. 推荐最小实现路线

### Phase 1. 可落地 MVP
- 新增 `signal_detect.py`
- 新增 `signal_apply.py`
- 在 `review.py feedback` 成功路径里调用 `signal_apply`
- 支持 `session_key`
- 支持单 session 去重

这一步就已经能把“用户再次提起并确认有用”积累成真正 repetition。

### Phase 2. 扩展到 `resurface`
- `review.py resurface --write-signals`
- 对高置信候选记一次弱激活
- useful feedback 再升级为中/强激活

### Phase 3. 上层集成
- agent 命中 Hui-Yi skill 时自动传入当前 query
- 统一从真实聊天入口累计 activation event

### Phase 4. Scheduler / Runtime 联动
- 外部调度层或上层 runtime 可以消费 activation density
- 但调度链路仍不直接写回 signals，除非有明确回执机制

---

## 12. 需要避免的坑

### 坑 1. 关键词一碰就算 repetition
这会把噪音记忆刷爆。

### 坑 2. 同一会话无限累加
这会让长对话天然碾压跨会话重复。

### 坑 3. 系统自己提起也算高强激活
这会形成自嗨闭环。

### 坑 4. 没有 session id
没有 session 维度，就无法区分“同一轮重复”与“跨会话复现”。

### 坑 5. 让 scheduler / decay 偷偷写 signals
职责会变脏。

---

## 13. 最终建议

最合理的定义是：

> **session_signals 不是关键词计数器，而是“真实会话里，这条记忆被再次激活并被确认有价值”的轻量强化轨迹。**

所以它的最佳来源不是：
- 全量历史暴力扫描
- 时间驱动脚本乱改

而是：
- 当前真实 query 的高置信命中
- 用户明确回忆/追问
- recall 后的 useful feedback
- 跨 session 的再次出现

---

## 14. 原始实施步骤（历史记录，已由现有模块覆盖）

早期列出的实施顺序是：

1. 给 `review.py` 增加 `session_key` 输入
2. 新增 `signal_apply.py`
3. 先把 `feedback useful=yes` 路径接成真实强化入口
4. 再给 `resurface` 增加可选的弱激活写回

这是最稳的切入点，不花里胡哨，但真能把血接上。
