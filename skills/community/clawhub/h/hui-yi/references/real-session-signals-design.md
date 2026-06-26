# Real Session Signals Integration Design

这份设计稿定义 Hui-Yi 如何从 **真实会话** 自动累积 `session_signals`，让 repetition-first 不只是静态字段，而是有稳定的数据来源。

---

## 1. 目标

当前 Hui-Yi 已经具备：
- `Session signals` 字段可存储
- `repetition_signal()` 可计算
- `review.py` / `scheduler.py` 已能消费 repetition 信号

但还缺一层：

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
  一律不持久化。默认 hook 日志同样不含正文预览和原始标识，详细诊断需要
  `HUI_YI_HOOK_DEBUG=1` 显式开启。
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

## 4. 建议新增脚本

建议增加：

```text
scripts/
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

建议字段：

```text
session_key = <channel>:<chat_id>:<thread_id-or-main>:<date-bucket?>
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

建议统一事件结构：

```json
{
  "session_key": "feishu:user:ou_xxx:main",
  "activated_at": "2026-04-12T19:20:00+08:00",
  "query": "hui-yi 的 decay 和 openclaw 记忆边界",
  "matched_note": "memory/cold/hui-yi-memory-boundary.md",
  "match_score": 0.76,
  "match_reasons": ["title", "tags", "semantic_context"],
  "event_strength": "medium",
  "dedup_key": "feishu:user:ou_xxx:main|hui-yi-memory-boundary|2026-04-12"
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

建议：
- 每个 note 在同一 session 中，按事件窗口去重
- 比如 15 分钟窗口内最多 +1 次强激活，或 +2 次弱激活

### 8.2 跨会话更值钱
建议权重：
- 同一 session 重复提及：低到中权重
- 不同 session 再次出现：高权重
- 连续多个 session 都出现：更高权重

### 8.3 用户显式回忆请求更值钱
如果用户说：
- “之前怎么处理来着”
- “你记得吗”
- “上次我们说过那个”

这种 activation event 应该比普通关键词碰撞更强。

建议 event_strength：
- `weak`: 只有 tags/title 弱命中
- `medium`: 多字段命中或明确相关 query
- `strong`: 用户显式追问历史 / 复盘 / 延续旧决策

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

### 方案 C. Heartbeat / transcript 批处理
流程：
1. 定期扫描最近对话摘要或 session transcript
2. 对命中的 note 批量累计 signals

优点：
- 覆盖更广

缺点：
- 容易重、容易脏、容易误记
- 我不建议作为第一版主路线

### 推荐顺序
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

## 14. 推荐下一步

如果继续落代码，最值得先做的是：

1. 给 `review.py` 增加 `session_key` 输入
2. 新增 `signal_apply.py`
3. 先把 `feedback useful=yes` 路径接成真实强化入口
4. 再给 `resurface` 增加可选的弱激活写回

这是最稳的切入点，不花里胡哨，但真能把血接上。
