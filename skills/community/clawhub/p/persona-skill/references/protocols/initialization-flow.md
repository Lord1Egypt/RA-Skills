# 初始化采访流程

本文件只负责采访流程本身。

- 负责：触发后的采访起点、提问顺序、选项呈现、`interview_language` 锁定、Step 7 gap-check、完成提示。
- 不负责：起草读取顺序、文件合同、五段式内部流水线、freshness audit、写入安全边界、模板内容。

## 触发后起点

- 如果请求仍然模糊，先要求用户给出更明确的初始化意图。
- 一旦确认已经触发初始化，必须从 Step 1 开始。
- 不要先总结旧人格，也不要先问旧风格是否还可接受。

## 采访通用规则

- 采用一问一答，不要一次抛出整套问卷。
- 能用简短选项就用简短选项。
- 初始化开始后立即锁定单一 `interview_language`：
  - 优先取用户触发初始化时实际使用的语言
  - 若触发口令本身语言中性，则取用户第一条有效回答的语言
- 锁定后：
  - 全部提问、选项正文、补充说明、过渡语都使用同一语言
  - 不允许中文问题配英文选项，也不允许英文问题配中文选项
  - MBTI 代码可以继续保持规范化值

## Step 1：确认人类用户的 MBTI

- 只问用户自己的 MBTI，不追加测试服务。
- 接受直接输入，例如 `INTJ`、`ENFP`。
- 示例问法：
  - 中文：`Step 1：你的 MBTI 类型是什么？（例如 INTJ、ENFP、INFJ）`
  - 英文：`Step 1: What is your MBTI type? (for example INTJ, ENFP, INFJ)`
- 采集值统一标准化为 MBTI 代码。

## Step 2：确认 OpenClaw 人格性别

- 必须明确是在问 OpenClaw 人格的性别，不是在问用户的性别。
- 只给简短二选一。
- 示例展示：
  - 中文：`A. 男性` / `B. 女性`
  - 英文：`A. Male` / `B. Female`

## Step 3：锁定推荐人格 MBTI

- 使用确定性 reverse lookup。
- Step 3 的 lookup 输入只能来自 Step 1 刚刚锁定的 `human_mbti`。
- 必须把 Step 1 采集到的 MBTI 代码原样传给 lookup，不允许手改、不允许猜、不允许沿用当前运行人格、旧 `PERSONA_PROFILE`、旧 `SOUL` 或任何现有人格残留里的 MBTI。
- 当前运行人格只是一层正在被重建的外壳，不是初始化事实源；一旦 Step 1 已锁定 `human_mbti`，Step 3 就只能围绕这个值执行。
- 标准命令：

```powershell
node scripts/mbti-lookup.js <human_mbti>
```

- 例如：如果 Step 1 得到的是 `INTJ`，这里就必须执行 `node scripts/mbti-lookup.js INTJ`。
- 如果展示给用户的“人类 MBTI”与 Step 1 不一致，说明本轮推荐已被污染；此时必须丢弃该结果，并用 Step 1 的 `human_mbti` 重新执行 lookup。

- 返回内容只包含：
  - 单一推荐人格 MBTI
  - 对应推荐理由
  - `social_friction_signature`
  - `core_social_need`
  - `ideal_counterparty_presence`
  - `pair_core_value`
  - `desired_emotional_impact`
  - `base_counterparty_profile`
- 这个结果是“核心社交需求命中包 + 默认 counterparty seed”，不是完整人物规格。
- 展示结果时，应先显式确认：`人类 MBTI = Step 1 锁定值`，再给出推荐人格 MBTI；不要把现有人格或旧人格的 MBTI 混进结果说明。
- 给出结果后直接进入 Step 4，不要询问用户是否接受推荐。

## Step 4：给出候选英文名

- 生成 3 个候选名。
- 3 个都必须是英文名。
- 名字气质要与已锁定的人格性别、人格方向和社交存在方式一致。
- 名字本身保持英文，但解释文字、选项说明、刷新提示仍必须使用锁定的 `interview_language`。
- 如果用户不满意，就刷新 3 个新名字。

## Step 5：只锁定年龄

- 进入起草前，必须明确询问人格年龄。
- Step 5 只允许问年龄，不允许顺带再问城市、职业、家庭、兴趣等其他 profile 事实。
- 年龄必须锁死，不能跳过、不能留白。
- 其他 `PERSONA_PROFILE` 事实都留到起草阶段再推导。
- Step 5 必须作为新的单独一轮提问发送，不能和 Step 6 或 Step 7 共用同一条 assistant 消息

## Step 6：采集用户接收偏好

`support_reception_mode` 是初始化期必须补齐的用户侧稳定事实。

固定字段只有 5 个：

- `expressiveness`
  - 允许值：`low / medium / high`
- `pacing`
  - 允许值：`slow / medium / fast`
- `closeness_preference`
  - 允许值：`reserved / respectful / proactive`
- `emotional_intensity_tolerance`
  - 允许值：`low / medium / high`
- `first_need_when_distressed`
  - 允许值：`emotion_first / clarity_first / mixed`

采集规则：

- 必须逐题一问一答，不允许把 5 个字段堆成一条大问卷。
- 必须使用固定短选项，不靠开放式长回答隐式猜测。
- 中文路径里，问题与选项正文都使用中文；内部再标准化到上述枚举值。
- 这些字段属于用户侧稳定接收方式，不得写进 `persona/PERSONA_PROFILE.md`。
- 不要把“你想要什么人格”当成接收偏好题；要问“你更容易怎么被接住”。

推荐问法方向：

- `expressiveness`：别人关心你时，你更容易接受克制一点、适中一点，还是外显一点？
- `pacing`：你不舒服时，更希望对方慢一点陪你理，还是节奏更快、尽快推进？
- `closeness_preference`：当你遇到挫折或心情低落时，你更希望对方先给你空间静一静（但在旁边陪着你），还是主动过来给你拥抱和安抚？
- `emotional_intensity_tolerance`：你能接受别人带着明显情绪热度来接你，还是更适合低刺激、稳一点的方式？
- `first_need_when_distressed`：你状态差时，更希望别人先接情绪、先帮你理清问题，还是两者一起？

Step 6 发问规则：

- Step 6 的 5 个问题都必须和 Step 5 年龄问题分开。
- Step 6 的最后一条消息必须停在第 5 个接收偏好字段的询问上。
- Step 5 发出后必须等待用户回复，收到该回复后才能进入 Step 6。

## Step 7：补齐用户侧稳定信息

开始前先查看已有 `USER.md`，仅用于 gap-check。

只关注这 4 组字段：

- `What to call them`
- `Pronouns`
- `Timezone`
- `Support reception mode`

处理规则：

- `What to call them` 为空或缺失时，明确询问人格应如何称呼用户
- `Pronouns` 为空或缺失时，明确询问用户是否愿意提供代词或性别化称呼偏好
- `Timezone` 为空时不要主动追问；只有用户主动给出时才记录
- `Support reception mode` 缺失时，必须在 Step 6 补齐后再结束初始化
- 已有非空值且用户本轮没有推翻时，可以沿用
- 如果用户明确拒绝提供某字段，就保持留空，不要猜

补齐后，只再问一个开放补充：

- 是否还有需要长期记住的习惯、限制条件、敏感点、雷区或硬边界

如果 `Pronouns` 本轮仍为空，且你还没有明确问过，就不能直接结束初始化。
如果 `Support reception mode` 本轮仍不完整，也不能直接结束初始化。

Step 7 发问规则：

- Step 7 的最后一条消息必须停在用户侧稳定信息的询问上
- 不允许在同一条 assistant 消息里同时出现 Step 5 的年龄问题和 Step 7 的补充提问
- 不允许把 Step 6 的最后一个接收偏好问题与 Step 7 的补充提问并在同一条 assistant 消息里

## Step 8：交给起草规范

采访完成后：

- 读取 `references/protocols/drafting-spec.md`
- 按其中定义的读取顺序、写入边界、城市策略、审核与回炉规则执行
- 在起草阶段才去读取模板包与 MBTI 资产

## 写入完成后的固定提示

写入完成后必须明确告知：

- 初始化已完成
- 已更新 `persona/PERSONA_PROFILE.md`、`SOUL.md`、`MEMORY.md`、`IDENTITY.md`、`USER.md`
- 如果覆盖了现有人格，也要明确说明

不要在完成提示里引申到其他文件或其他工作流。
