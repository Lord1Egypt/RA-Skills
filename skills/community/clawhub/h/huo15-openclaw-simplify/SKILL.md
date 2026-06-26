---
name: huo15-openclaw-simplify
displayName: 火一五代码简化技能
description: 对最近修改的代码做"复用/质量/效率"三维审查，产出可执行的清理清单；然后实际修复命中的问题。用于刚写完功能、PR 提交前、重构前的自检。触发词：简化代码、清理冗余、重构建议、simplify、code cleanup、代码体检、能不能更简洁。
version: 1.0.0
aliases:
  - 火一五代码简化
  - 简化代码
  - 代码清理
  - 重构建议
  - simplify code
  - code cleanup
  - 代码体检
license: MIT
---

# 火一五代码简化技能 v1.0

> 对刚写完的代码做"复用/质量/效率"三维体检 — 青岛火一五信息科技有限公司

---

## 一、触发场景

当用户刚完成一段实现，或准备提 PR，说：

- "简化一下"
- "这段代码能不能更简洁"
- "帮我清理下冗余"
- "重构一下"
- "code review 一下（偏重质量）"

**产出**：三维清单（复用 / 质量 / 效率）+ 每条命中标注严重程度 + 自动修复可安全改的（保守策略）。

---

## 二、三维审查清单

### 维度 A：**复用（Reuse）**

| 项 | 命中信号 | 默认行动 |
|----|---------|---------|
| 与仓库内已有函数重复 | grep 到名称/行为相似的函数 | 标记 → 建议替换，**不自动改**（需用户确认契合） |
| 逻辑可抽函数（重复出现 ≥3 次的片段）| 肉眼识别 + grep 验证 | 抽函数，放到最近的共用模块 |
| 重新发明了标准库 / 已有依赖 | 出现如自写 deep-merge / debounce | 改用依赖；**若依赖未装，不自动 `npm install`**，给命令让用户装 |
| 可下沉到 util | 业务代码里混进了纯函数 | 提取到 `utils/` 或 `lib/` |

### 维度 B：**质量（Quality）**

| 项 | 命中信号 | 默认行动 |
|----|---------|---------|
| 裸 any / 裸 `unknown` 未收窄 | TS 语言明显 | 收窄类型，优先用 TypeBox / Zod 已有 schema |
| 魔法数字 / 魔法字符串 | `42`, `"pending"` 散落 | 提常量，放到 `constants.ts` |
| 嵌套 if-else > 3 层 | 阅读困难 | 提前返回 / early return / 卫语句 |
| console.log 残留 | grep `console\.(log|info|debug)` | 删 / 改 logger；**test 文件放过** |
| 注释是"做了什么"而非"为什么" | 注释重复代码 | 改"为什么"或删 |
| 命名不达意（`data` / `temp` / `obj`） | 一眼看不出含义 | 改成表达意图的名字 |

### 维度 C：**效率（Efficiency）**

| 项 | 命中信号 | 默认行动 |
|----|---------|---------|
| O(n²) 可降 O(n) | 嵌套 for + 查找 | Map / Set 替代 | 
| 同一对象重复 JSON.parse/stringify | 显眼的往返 | 缓存中间结果 |
| 在循环里做 I/O（db 查询 / fetch）| await 在 for 里 | Promise.all 或批量查 |
| 不必要的 re-render / 重新计算 | React useMemo 缺失；大对象每次新建 | 加记忆化 |
| 整包导入（`import *`）| 引起 bundle 膨胀 | 按需导入 |

---

## 三、工作流（严格按序）

1. **定位本次改动**
   - 优先 `git diff HEAD~1` 或 `git diff --staged`
   - 若 git 不干净，问用户"审查当前整个工作区还是只看刚改的？"
2. **只读扫描**
   - 对命中文件做 Read + Grep
   - **不要**扫整个仓库（除非用户指定）
3. **生成清单**
   - 按 A/B/C 三维打表
   - 每条打严重度：🔴 必改 / 🟡 建议改 / 🟢 可选
   - 每条给出 `file:line`
4. **与用户同步**
   - 先出**清单**
   - 问"全改 / 只改🔴 / 只改某几条"
5. **执行修复**
   - 按用户选择执行 Edit
   - 每改一处解释一行"因为 X 改为 Y"
6. **收尾**
   - 列出**没动但建议改**的项
   - 不跑测试不跑 build（除非用户要求）

---

## 四、产出模板

```markdown
## 简化报告 — <commit/path>

### 🔴 必改（3 项）
1. [reuse] `src/a.ts:45` — deep-merge 自写实现，应改用 lodash.merge（已装）
2. [quality] `src/b.ts:12` — 裸 any，应收窄为 `User | null`
3. [quality] `src/c.ts:88` — 3 层嵌套 if，建议 early return

### 🟡 建议（2 项）
4. [efficiency] `src/d.ts:33` — for 循环里 await fetch，改 Promise.all 减 3× 耗时
5. [reuse] `src/e.ts:70` — 与 `utils/slugify.ts` 逻辑重复

### 🟢 可选（1 项）
6. [quality] `src/f.ts:5` — 变量名 `data` 可改为 `userProfiles`

### 未动
- [quality] test 文件中的 console.log（按惯例放过）
```

---

## 五、硬红线（绝不触碰）

1. **不自动重命名跨文件符号** — 除非用户明确说"改所有引用"
2. **不动测试断言** — 可以补测试，不改已有断言
3. **不引入新依赖** — 即使建议了，也只给 `npm install x` 命令，不 exec
4. **不跑格式化器** — 除非用户明确说"顺便跑 prettier"
5. **不碰 generated 代码** — 识别 `@generated` / `// DO NOT EDIT` / `dist/` / `build/`

---

## 六、与相邻技能的边界

| 场景 | 用哪个 |
|------|--------|
| 只看代码质量 | **本技能** |
| 看安全漏洞（密钥 / 注入 / XSS）| `huo15-openclaw-security-review` |
| PR 全流程评审（含安全 + 质量 + 设计）| `huo15-openclaw-code-review` |
| 设计稿 / UI 打分 | `huo15-openclaw-design-critique` |
