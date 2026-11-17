# Live-Proof 案例库

> 本文件记录真实 PR 中通过 ClawSweeper 评审、获得 `status: 👀 ready for maintainer look` 的 live-proof 实践。
> 开发 PR 时参考本案例库，确保提供的 proof 足够充分。

## 目录

- [ClawSweeper 评级体系](#clawsweeper-评级体系)
- [什么是 live-proof](#什么是-live-proof)
- [案例一：配置验证类修复（#110051）](#案例一配置验证类修复110051)
- [案例二：竞品对比学习（#109875）](#案例二竞品对比学习109875)
- [失败案例：修改了不可达路径（#109885）](#失败案例修改了不可达路径109885)
- [通用 Proof 模板](#通用-proof-模板)
- [检查清单](#检查清单)

---

## ClawSweeper 评级体系

ClawSweeper（OpenClaw 的自动评审机器人）对 PR 给出三个维度的甲壳类评级：

| 评级 | 含义 | 可合并性 |
|------|------|----------|
| 🦀 challenger crab | 罕见，卓越的就绪状态 | 极高 |
| 🦞 diamond lobster | 很强，仅需少量 maintainer 审查 | 高 |
| 🐚 platinum hermit | 良好的普通 PR，普通审查即可 | 中高 |
| 🦐 gold shrimp | 有用信号，但 proof/confidence 仍有限 | 中 |
| 🦪 silver shellfish | 信号薄弱，proof/validation/实现需改进 | 低 |
| 🧂 unranked krab | 不可合并（proof 缺失或有严重问题） | 不可合并 |
| 🌊 off-meta tidepool | 评级不适用 | N/A |

### 三个评分维度

| 维度 | 说明 |
|------|------|
| **Overall** | 综合 = proof 和 patch quality 中较弱者（短板效应） |
| **Proof** | 真实行为证明的充分性 |
| **Patch quality** | 代码实现质量 |

> ⚠️ **关键规则**：`Overall follows the weaker of proof and patch quality, so missing proof can cap an otherwise strong patch.`
> 即使 patch 质量是 🐚 platinum hermit，如果 proof 只有 🦪 silver shellfish，整体仍是 🦪。

### 状态标签

| 标签 | 含义 |
|------|------|
| `status: 📣 needs proof` | 需要补充真实行为证明才能合并 |
| `status: 👀 ready for maintainer look` | ClawSweeper 无 contributor 阻塞项，等待 maintainer 审查 |
| `proof: sufficient` | Contributor 真实行为证明充分 |

**目标**：获得 `status: 👀 ready for maintainer look` + `proof: sufficient`。

---

## 什么是 live-proof

Live-proof（真实行为证明）是 ClawSweeper 要求的、证明修复**实际生效**的证据。

### ❌ 不是 live-proof 的东西

- 只有单元测试通过（"X tests passed"）
- 纯代码阅读得出的结论（"代码逻辑应该正确"）
- 声称修复有效但没有运行验证

### ✅ 是 live-proof 的东西

被合并的 PR 全部使用**终端命令输出**作为 proof，不用截图/视频：

| Proof 类型 | 命令模式 | 适用场景 |
|-----------|---------|---------|
| 直接验证 | `node --import tsx -e "..."` | 配置验证、纯函数行为 |
| 聚焦测试 | `node scripts/run-vitest.mjs <path>` | 运行时修复、回归测试 |
| 完整 gate | `node scripts/check-changed.mjs -- <files>` | 多文件变更 |
| 格式检查 | `git diff --check` / `oxfmt --check` | 代码格式 |
| Autoreview | `autoreview --mode uncommitted` | 代码审查 |

### 关键：BEFORE vs AFTER 对比

最有效的 proof 是展示**修复前**和**修复后**的对比：

```
BEFORE (current main) - gateway.port: 65536 passed validation with ok: true
AFTER - gateway.port: 65536 is rejected with clear error message
```

---

## 案例一：配置验证类修复（#110051）

**Issue**: #109293 - `gateway.port` 接受超出 TCP 端口范围的值
**PR**: https://github.com/openclaw/openclaw/pull/110051
**修复类型**: 配置 schema 收紧 + Doctor 迁移

### 问题描述

`gateway.port` 的 Zod schema 只有 `.positive()` 没有 `.max(65535)`，导致 `65536` 等无效端口通过验证。

### 关键教训：收紧 config 验证 = 破坏性变更

**这是最重要的教训。** 收紧 config schema 会让之前合法的配置变非法，必须配 Doctor 迁移！

> CLAUDE.md 明确规定："If a config change invalidates existing files, add a matching `openclaw doctor --fix` migration."

只加 schema 约束而不加 Doctor 迁移的后果：
- 已有 `gateway.port: 65536` 的用户升级后直接报错，无升级路径
- ClawSweeper 标记 `merge-risk: 🚨 compatibility`
- 无法获得 `status: 👀 ready for maintainer look`

### Doctor 迁移设计决策

迁移应**替换为默认值**而非删除键：

| 策略 | #109875（竞品） | #110051（我们的） |
|------|-----------------|------------------|
| 做法 | `delete gateway.port` | `gateway.port = DEFAULT_GATEWAY_PORT` |
| 迁移后配置 | 无 port 键 | `port: 18789` |
| 用户体验 | 困惑：配置里没 port，网关用什么端口？ | 明确：绑定到默认 18789 |

### 提供的 Proof 内容

**1. Schema validation - BEFORE vs AFTER**

```sh
# BEFORE (current main) - passes validation
{"ok": true, "config": {"gateway": {"port": 65536}}}

# AFTER - rejected
$ node --import tsx -e "
import { validateConfigObjectRaw } from './src/config/validation.ts';
console.log(JSON.stringify(validateConfigObjectRaw({gateway:{port:65536}}), null, 2));"
{
  "ok": false,
  "issues": [{
    "path": "gateway.port",
    "message": "Too big: expected number to be <=65535 (maximum: 65535)"
  }]
}
```

**2. Doctor migration - 升级路径证明**

```sh
$ node --import tsx -e "
import { applyLegacyDoctorMigrations } from './src/commands/doctor/shared/legacy-config-compat.js';
const raw = {gateway:{port:65536}};
const { next, changes } = applyLegacyDoctorMigrations(raw);
console.log('changes:', JSON.stringify(changes));
console.log('next:', JSON.stringify(next));"
changes: ["Replaced out-of-range gateway.port (65536) with default 18789..."]
next: {"gateway":{"port":18789}}
```

覆盖场景：
- port 65536（超上限）→ 替换为默认
- port 0（低于下限）→ 替换为默认
- port 65535（有效）→ 无迁移
- port 65536 + bind:loopback → port 替换，bind 保留
- 幂等性：第二次迁移无变化

**3. 测试结果**

```
- node scripts/run-vitest.mjs src/config/zod-schema.gateway.test.ts - 7 tests
- node scripts/run-vitest.mjs src/config/validation.policy.test.ts - 8 tests
- node scripts/run-vitest.mjs src/commands/doctor/shared/legacy-config-migrate.test.ts - 158 tests
- git diff --check - passed
```

### 评级结果

| 维度 | 评级 |
|------|------|
| Patch quality | 🐚 platinum hermit |
| Proof | 🦞 diamond lobster（加入 Doctor proof 后） |
| Overall | 🦞 diamond lobster |

---

## 案例二：竞品对比学习（#109875）

**Issue**: 同 #109293
**PR**: https://github.com/openclaw/openclaw/pull/109875
**结果**: 获得 `status: 👀 ready for maintainer look` + `proof: sufficient`

### 它做对了什么

1. **Doctor 迁移配对**：schema 收紧 + `openclaw doctor --fix` 迁移
2. **BEFORE vs AFTER 对比**：明确展示修复前后验证输出
3. **Doctor 迁移的完整场景证明**：6 个场景，每个都有终端输出
4. **测试分散在正确的位置**：验证策略测试 + 迁移测试

### ClawSweeper 的关键评语

> `status: 👀 ready for maintainer look`: ClawSweeper has no concrete contributor-facing blocker left for this PR.
> `proof: sufficient`: The PR body includes after-fix terminal output for raw validation and Doctor migration behavior, including invalid, valid-boundary, idempotence, and sibling-key cases.

### 它的不足（我们改进的点）

1. Doctor 迁移用 `delete` 而非 `replace`，用户体验较差
2. `legacyRules` 的 `match` 没有覆盖非数字/非整数类型
3. 迁移测试没覆盖负数端口

---

## 失败案例：修改了不可达路径（#109885）

**Issue**: #109673 - `browser.headless` 配置被忽略
**PR**: https://github.com/openclaw/openclaw/pull/109885（已关闭）
**结果**: 🧂 unranked krab → 关闭

### 失败原因

**修改了一个正常代码路径不会走到的 fallback。**

```typescript
// resolveManagedBrowserHeadlessMode 的 fallback (line 730)
return { headless: resolved.headless, source: "default" };  // 我改成了 resolved.headlessSource
```

ClawSweeper 的批评：
> The changed final fallback is bypassed by the normal resolved profile according to the PR's own tests, so the patch does not yet identify or repair the boundary producing the reported behavior.

### 教训

1. **修改前先证明 bug 在该路径**：写一个测试，在修复前应该失败。如果修复前测试就通过，说明 bug 不在这。
2. **不要修改"看起来不对"但实际不影响行为的代码**：要验证改动是否真正改变运行时行为。
3. **ClawSweeper 会读你的测试**：如果测试本身说明"正常 profile 走早期分支"，它就知道你的 fallback 修改无效。
4. **找不到根因时不要硬提交**：诚实说明，关闭 PR，评论 issue 说明调查结果。

### 正确的流程

```
1. 写测试复现 bug（修复前应失败）
   ↓ 失败 = 找到了根因
2. 修复代码
   ↓ 测试通过
3. 验证修复改变了运行时行为（live-proof）
   ↓
4. 提交 PR
```

---

## 通用 Proof 模板

### 配置验证类修复

```markdown
## Evidence

### 1. Schema validation - BEFORE vs AFTER

**BEFORE** (current main) - `<invalid input>` passed validation with `ok: true`

**AFTER** - `<invalid input>` is rejected:

\`\`\`sh
$ node --import tsx -e "
import { validateConfigObjectRaw } from './src/config/validation.ts';
console.log(JSON.stringify(validateConfigObjectRaw({<path>:<value>}), null, 2));"
<actual output showing ok:false + error message>
\`\`\`

### 2. Doctor migration - upgrade path proof

\`\`\`sh
$ node --import tsx -e "
import { applyLegacyDoctorMigrations } from './src/commands/doctor/shared/legacy-config-compat.js';
const raw = {<path>:<invalid_value>};
const { next, changes } = applyLegacyDoctorMigrations(raw);
console.log('changes:', JSON.stringify(changes));
console.log('next:', JSON.stringify(next));"
<output showing repair>
\`\`\`

覆盖场景：
- 无效值 → 修复
- 有效边界值 → 不变
- 幂等性
- sibling key 保留

### 3. Test results
- `node scripts/run-vitest.mjs <test-path>` - N tests passed
- `git diff --check` - passed
```

### 运行时逻辑修复

```markdown
## Evidence

- Focused proof: `node scripts/run-vitest.mjs <test-path>` - N tests passed.
- BEFORE: <描述修复前的错误行为，最好有测试断言证明>
- AFTER: <描述修复后的正确行为>
- `git diff --check` - passed.
```

### Bug 复现型修复

```markdown
## Evidence

### Regression test (fails before fix, passes after)
\`\`\`
node scripts/run-vitest.mjs <test-path>
# Before fix: FAIL - <error>
# After fix: PASS
\`\`\`

### Live behavior proof
<运行实际命令展示修复前后行为变化>
```

---

## 检查清单

### 提交 PR 前的 proof 检查

- [ ] 提供了 BEFORE vs AFTER 对比（不只是 AFTER）
- [ ] Proof 是终端命令输出，不是只有"测试通过"
- [ ] 覆盖了边界值（最小、最大、无效）
- [ ] 覆盖了幂等性（如涉及迁移）
- [ ] 覆盖了 sibling key 保留（如涉及删除/修改配置项）
- [ ] 如果收紧了 config 验证，配了 Doctor 迁移
- [ ] 修复前能复现 bug（测试在修复前会失败）

### 自问：修改是否真正改变运行时行为？

- [ ] 我写的测试在**修复前**会失败吗？
- [ ] 我修改的代码路径在**正常情况下**会被走到吗？
- [ ] ClawSweeper 读完我的测试后，会认为我的修复有效吗？

如果任何一项为"否"，**不要提交**，继续调查根因。

### 达标目标

提交 PR 后，目标评级：
- ✅ `status: 👀 ready for maintainer look`
- ✅ `proof: sufficient`
- ✅ Overall ≥ 🐚 platinum hermit

---

## 经验总结

### 1. 收紧配置验证必须配 Doctor 迁移

这是 OpenClaw 的硬规则。任何让之前合法配置变非法的变更，都要提供 `openclaw doctor --fix` 升级路径。

### 2. Proof 要展示真实运行时行为

ClawSweeper 明确说："Only unit-test claims are provided" 是不够的。要运行实际命令展示修复效果。

### 3. BEFORE vs AFTER 对比最有效

明确展示"修复前是坏的，修复后是好的"比单纯展示"修复后是好的"更有说服力。

### 4. 修改前先证明 bug 在该路径

写一个在修复前会失败的测试。如果修复前测试就通过，说明 bug 不在你修改的地方。

### 5. Doctor 迁移用替换而非删除

替换为默认值比删除键更安全：用户看到的配置文件行为明确，不依赖隐式默认。

### 6. 诚实面对找不到根因的情况

如果代码逻辑看起来正确但 bug 仍存在，可能 bug 在运行时其他地方或已被间接修复。诚实说明，关闭 PR，评论 issue，比硬提交一个无效修复好。
