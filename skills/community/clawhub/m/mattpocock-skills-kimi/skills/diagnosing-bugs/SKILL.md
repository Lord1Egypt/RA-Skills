---
name: diagnosing-bugs
description: >
  Disciplined diagnosis loop for hard bugs and performance regressions:
  reproduce → minimise → hypothesise → instrument → fix → regression-test.
  当用户说"修 Bug"、"跑不通"、"报错"、"抛异常"、"性能慢"、"卡顿"、"慢查询"、
  "debug"、"diagnose"、"排查"、"定位问题"、"故障"、"崩溃"、"fail"、"broken"、
  "throwing"时触发。强制六阶段：先建反馈循环，再假设，绝不跳过 Phase 1。
---

# Diagnosing Bugs — Bug 诊断六阶段

> 原始理念来自 Matt Pocock。在 Kimi 生态中，此 skill 为 model-invoked，
> 在 Bug 相关场景自动触发。

## 核心原则

**Phase 1 就是这个 skill。** 没有 tight feedback loop（紧反馈循环），再多的 staring at code 也救不了你。

## 六阶段

### Phase 1 — Build a feedback loop（建立反馈循环）

**这是最重要的阶段。** 投入不成比例的努力在这里。

目标：一个 **tight** pass/fail 信号——一个命令，运行后能告诉你"这个 bug 还在"（red）或"已经修复"（green）。

尝试顺序（从易到难）：

1. **Failing test** — 在能触及 bug 的 seam 上写测试
2. **Curl / HTTP script** — 对运行中的 dev server 发请求
3. **CLI invocation** — 用 fixture 输入，对比 stdout 与已知好快照
4. **Headless browser** — Playwright/Puppeteer 驱动 UI，断言 DOM/console/network
5. **Replay captured trace** — 保存真实网络请求/负载/事件日志，在隔离环境重放
6. **Throwaway harness** — 启动最小系统子集（一个服务 + mock 依赖），单函数调用触达 bug
7. **Property / fuzz loop** — 随机输入，找失败模式
8. **Bisection harness** — 自动化"在状态 X 启动，检查，重复"，配 `git bisect run`
9. **Differential loop** — 同输入跑旧版 vs 新版，对比输出
10. **HITL bash script** — 最后手段。如果需要人类点击，用脚本驱动人类循环

#### 收紧循环

一旦有了 loop，**tighten** 它：
- 能更快吗？（跳过无关初始化，缩小测试范围）
- 信号能更尖锐吗？（断言具体症状，不是"没崩溃"）
- 能更确定吗？（固定时间、固定种子、隔离文件系统、冻结网络）

#### 非确定性 Bug

目标不是 clean repro，而是**提高复现率**。循环触发 100 次，并行化，加 stress，缩小时间窗口，注入 sleep。50% 的 flaky bug 是可调试的；1% 不是。

#### 实在建不出循环时

**停下来明确说。** 列出你尝试了什么。向用户要：
- (a) 能复现的环境访问
- (b) 捕获的 artifacts（HAR 文件、日志 dump、core dump、带时间戳的录屏）
- (c) 添加临时生产监控的权限

**没有 tight loop，不要进入 Phase 2。**

### Phase 2 — Reproduce + minimise（复现 + 最小化）

- [ ] Loop 跑 red，确认失败模式是用户描述的（不是附近的另一个失败）
- [ ] 失败可复现（对非确定性 bug：高复现率）
- [ ] 捕获精确症状（错误消息、错误输出、慢的时间）

然后 **minimise**：逐个砍掉输入、调用者、配置、数据、步骤，每次砍后重跑 loop——只保留对失败 load-bearing 的元素。

完成标准：**每个剩余元素都是 load-bearing**——砍掉任何一个都会变绿。

### Phase 3 — Hypothesise（假设）

在测试任何假设之前，生成 **3-5 个 ranked hypotheses**。单一假设会锚定第一个看似合理的想法。

每个假设必须是**可证伪**的：

> 格式："如果 <X> 是原因，那么 <改变 Y> 会让 bug 消失 / <改变 Z> 会让 bug 更糟"

如果说不出来预测，这个假设是 vibe——丢弃或锐化。

**给用户看 ranked list 再测试。** 他们经常有能瞬间重排的知识（"我们刚部署了 #3 的改动"）。

### Phase 4 — Instrument（探测）

每个 probe 必须映射到 Phase 3 的某个预测。**一次只改变一个变量。**

工具优先级：
1. **Debugger / REPL** — 一个 breakpoint 胜过十个 log
2. **Targeted logs** — 在区分假设的边界处加 log
3. **绝不 "log everything and grep"**

**调试日志加唯一前缀**，如 `[DEBUG-a4f2]`，清理时 `grep` 一次性删除。

**性能分支**：性能回归时，log 通常是错的。先建立 baseline 测量，再 bisect。先测量，再修复。

### Phase 5 — Fix + regression test（修复 + 回归测试）

在修复**之前**写回归测试——但**只有**在存在 **correct seam** 时。

Correct seam = 测试在真实调用点 exercising 真实 bug 模式。如果唯一可用 seam 太浅（单调用者测试覆盖不了多调用者触发的 bug），那回归测试在那里的假阳性会给人虚假信心。

**如果没有 correct seam，这本身就是发现。** 标记：架构阻止了 bug 被锁定。flag 给下一个 phase。

如果有 correct seam：
1. 最小复现 → 该 seam 的 failing test
2. 看它失败
3. 应用修复
4. 看它通过
5. 重跑 Phase 1 的原始 loop（未最小化的场景）

### Phase 6 — Cleanup + post-mortem（清理 + 复盘）

完成前必须：
- [ ] 原始复现不再复现（重跑 Phase 1 loop）
- [ ] 回归测试通过（或缺少 seam 已记录）
- [ ] 所有 `[DEBUG-...]` 已移除（`grep` 前缀）
- [ ] 临时原型已删除（或移到清晰标记的 debug 位置）
- [ ] 正确的假设写在 commit / PR message 中——给下一个 debugger 学习

然后问：**什么能阻止这个 bug？** 如果答案涉及架构变更（没有好测试 seam、调用者纠缠、隐藏耦合），hand off 给 `improve-codebase-architecture`。

**修复后再提建议，不是之前。** 你现在比之前知道得多。

## 触发场景（中文关键词）

- "修 Bug"
- "跑不通"
- "报错"
- "抛异常"
- "性能慢"
- "卡顿"
- "慢查询"
- "debug"
- "diagnose"
- "排查"
- "定位问题"
- "故障"
- "崩溃"
- "fail"
- "broken"
- "throwing"
- "slow"
- "性能回归"
- "内存泄漏"
- "race condition"

## 关联技能

- 被 `tdd` 调用（修 Bug 时按 TDD 流程）
- 后置：`improve-codebase-architecture`（如果架构是 root cause）
- 前置：`grilling`（如果 bug 的 repro 步骤不清晰，先对齐）
