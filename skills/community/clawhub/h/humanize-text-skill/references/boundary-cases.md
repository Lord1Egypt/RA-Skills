<!--
  Migrated from shuorenhua/references/boundary-cases.md (MIT, MrGeDiao).
  humanize-text-skill absorbs shuorenhua's Chinese completeness verbatim;
  cross-references updated to humanize-text-skill paths where needed.
-->

# Boundary Cases

These examples are not here to show how aggressively to rewrite. They are here to show when to make a light edit and when to avoid a false positive.

## 1. Technical status update

### Original

这次排查基本把范围收窄到缓存层了。昨天已经把主链路日志补齐，今天会继续把两个异常分支对上，看看是不是同一类失效路径。如果这个判断成立，修复应该能比较快落下去。

### Recommended rewrite

这次排查基本已经定位到缓存层。昨天补齐了主链路日志，今天会继续核对两个异常分支，确认是不是同一类失效路径。如果判断成立，修复会比较快。

### Why this change

- It removes performative engineer-slang such as `收窄`, `对上`, and `落下去`.
- It keeps the three things that matter most in a status update: current judgment, action already taken, and next step.

### What not to break

- Do not delete technical details such as `缓存层`, `异常分支`, and `失效路径`.
- Do not flatten it into a vague line like "the issue is mostly understood now."

## 2. Official announcement tone

### Original

为保障系统稳定性，我们将于今晚 23:00-23:30 对支付服务进行例行维护。维护期间，部分用户可能出现短时下单失败的情况。维护完成后将自动恢复，不需要额外操作。

### Recommended rewrite

为保障系统稳定性，我们将于今晚 23:00-23:30 对支付服务进行例行维护。维护期间，部分用户可能出现短时下单失败。维护完成后会自动恢复，无需额外操作。

### Why this change

- This is only a light cleanup that trims template phrasing.
- Formal announcement tone is already the correct register here and should not be forced into casual speech.

### What not to break

- Do not mechanically delete `为保障系统稳定性`.
- Do not rewrite it into a chat-style reminder or influencer voice.

## 3. Normal PRD language

### Original

当用户首次进入工作台且没有历史项目时，页面展示空状态卡片，引导其创建第一个项目。该卡片在用户创建成功后立即消失，后续不再展示。

### Recommended rewrite

当用户首次进入工作台且没有历史项目时，页面展示空状态卡片，引导其创建第一个项目。用户创建成功后，卡片立即消失，后续不再展示。

### Why this change

- The original is already normal product-writing language and does not need major surgery.
- The only edit is to make the second sentence more direct.

### What not to break

- Do not break the conditional structure just to make it sound "more human."
- Do not replace product terms like `空状态卡片` with casual wording.

## 4. Text that is already fairly natural

### Original

这版我先不继续抠细节了，核心问题其实已经看出来了。后面先把流程走通，再看哪里真的影响体验。

### Recommended rewrite

这版我先不继续抠细节了，核心问题已经比较清楚。后面先把流程走通，再看哪些地方真的影响体验。

### Why this change

- The edit only smooths a few edges without erasing the conversational feel.
- The original already sounds natural; over-correcting it would make it feel less human.

### What not to break

- Do not force it into status-report language.
- Do not add summary-closing phrases like `本质上` or `归根到底`.

## 5. System subjects in documentation

### Original

系统在检测到配置变更后会重新加载规则；如果新规则校验失败，则继续使用上一版配置，并在日志中记录错误原因。

### Recommended rewrite

系统在检测到配置变更后会重新加载规则；如果新规则校验失败，则继续使用上一版配置，并在日志中记录错误原因。

### Why this change

- No change. The system subject, conditional logic, and logging note are all appropriate.
- Removing AI tone is not a campaign against abstract subjects, and it is not a reason to loosen technical documentation.

### What not to break

- Do not force `系统` into a human actor.
- Do not turn technical conditionals into chatty explanation.

## 6. Literal verbs in algorithm descriptions

### Original

The system navigates the network topology using Dijkstra's algorithm, traversing each node to find the shortest path.

### Recommended rewrite

The system navigates the network topology using Dijkstra's algorithm, traversing each node to find the shortest path.

### Why this change

- No change. `navigates` and `traversing` are literal technical actions here, not business-speak.
- AI-tone cleanup should not make algorithm descriptions less precise.

### What not to break

- Do not mechanically replace `navigates` with `handles`.
- Do not blur the path-search behavior of the algorithm.

## 7. Normal passive voice in academic writing

### Original

The experiment was conducted by researchers at MIT. Results were published in Nature in 2024.

### Recommended rewrite

The experiment was conducted by researchers at MIT. Results were published in Nature in 2024.

### Why this change

- No change. This is standard academic register, and the passive voice is not hiding information.
- Removing AI tone does not mean converting every English sentence to active voice.

### What not to break

- Do not rewrite an academic abstract into casual prose.
- Do not remove the publication source in the name of directness.

## 8. Real debug talk with concrete evidence

### Original

刚查了下，root cause 是连接池打满了，max_connections 才 20，高峰期不够用。我把它调到 100，观察了半小时，没再报错。

### Recommended rewrite

刚查了下，root cause 是连接池打满了，max_connections 才 20，高峰期不够用。我把它调到 100，观察了半小时，没再报错。

### Why this change

- No change. The line contains concrete parameters, actions, and outcomes, so it is normal engineering communication rather than performative debug-speak.
- The key in this kind of exchange is information density, not stripping out every spoken technical term.

### What not to break

- Do not mechanically replace `root cause` with a more formal or more casual synonym.
- Do not delete key evidence like `20 -> 100` and `观察了半小时`.

## 9. Mixed scene: technical blog with embedded incident review

### Original

> 上个月我们把网关从 Nginx 换到了 Envoy。这篇文章聊聊为什么换、踩了什么坑。
>
> 值得注意的是，在当今云原生快速发展的时代，选择一个真正赋能团队的网关方案已经成为不容忽视的关键议题。
>
> 切换当天出了一次事故。事故复盘如下：
>
> 根因：Envoy 默认连接超时 15 秒，我们的长连接服务需要 300 秒。流量切过去后，长连接全断了，触发上游大面积重连。修复动作：`idle_timeout` 从 15s 改到 300s，灰度验证 2 小时后全量。错误率从 12% 降到 0.1%。
>
> 综上所述，这次迁移充分体现了团队在技术创新领域的持续探索与不懈追求。未来可期！

### Scene judgment

1. **Pick the primary scene**: the piece is a public technical blog, so the main scene is `public-writing` with the default `standard` tier.
2. **Detect the nested sub-scene**: the middle section is an incident review, so that local span belongs to `docs`.
3. **Let the main-scene guardrails set the ceiling**: `public-writing` should not be turned into slogan copy or hype.

### Recommended rewrite

> 上个月我们把网关从 Nginx 换到了 Envoy。这篇文章聊聊为什么换、踩了什么坑。
>
> 切换当天出了一次事故。事故复盘如下：
>
> 根因：Envoy 默认连接超时 15 秒，我们的长连接服务需要 300 秒。流量切过去后，长连接全断了，触发上游大面积重连。修复动作：`idle_timeout` 从 15s 改到 300s，灰度验证 2 小时后全量。错误率从 12% 降到 0.1%。

### Why this change

- **Delete the entire second paragraph**: it hits formulaic opener language (`值得注意的是`), business jargon (`赋能`), and empty importance inflation (`关键议题`), all of which fall inside `standard` rewrite territory for `public-writing`.
- **Keep the incident-review paragraph as is**: although `根因` is a Tier 1 term, it is standard incident-review terminology here, backed by concrete parameters and metrics, so it is protected by the nested `docs` scene.
- **Delete the final paragraph entirely**: it is a summary closer plus motivational closer (`综上所述`, `充分体现`, `持续探索`, `不懈追求`, `未来可期`) with no payload.

### What not to break

- Do not replace `根因` with a more casual synonym in the review section; this is technical postmortem language, not everyday chat.
- Do not break the concise `root cause -> fix -> outcome` structure; it is correct for the `docs` register.
- Do not force the blog introduction to sound like a postmortem just for consistency.

## 10. "Catch" language in a technical context

### Original

网关在压测里接住了峰值 2.4 万 QPS，请求超时率稳定在 0.3% 以下；超过阈值的流量会自动走降级，不再继续打满下游连接池。

### Recommended rewrite

网关在压测里接住了峰值 2.4 万 QPS，请求超时率稳定在 0.3% 以下；超过阈值的流量会自动走降级，不再继续打满下游连接池。

### Why this change

- No change. Here `接住` describes technical handling capacity; the object is `峰值 2.4 万 QPS`, and the sentence includes concrete metrics, system behavior, and degradation bounds.
- This is not the same as emotional reassurance such as "稳稳地接住你 / 所有人", and it should not be removed just because the wording overlaps.

### What not to break

- Do not flatten `接住了峰值 2.4 万 QPS` into a vague line like "performance is good."
- Do not delete technical evidence such as `0.3%`, `降级`, and `下游连接池`.
