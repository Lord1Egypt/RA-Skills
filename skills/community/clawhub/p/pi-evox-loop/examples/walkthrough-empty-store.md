# 失败类型走查：空库/参数写错时如何用 info 自检

> **EN**: Failure-mode walkthrough — diagnose an empty store or a wrong parameter with `info` (zero-dependency light backend, no model required).

> 本样例补 docQuality 扣分点「样例偏理想化、失败类型覆盖不足」。
> 只用零依赖 light 后端（`node code/light-cli.mjs`），**不需要模型端点**，预期输出为 0.44 实跑所得（隔离库）。

---

## 场景 1：召回没生效，怀疑「沉淀了但没用上」

先跑信息面板，确认库状态和闭环健康度：

```bash
EVO_STORE_DIR=./.evox-demo-store node code/light-cli.mjs info
```

预期输出（0.44 实测，空库形态）：

```
库路径      : <你的 EVO_STORE_DIR>
基因总数    : 0
台账记录    : 0
已审核(可注入): 0

── 闭环健康度 ──
  召回次数    : 0  ← 从未召回，经验不会生效
  ...
  状态        : 未闭合（按下面做一步即可）
```

**判读**：`基因总数=0` 说明还没沉淀；`召回次数=0` 说明即便有基因也不会注入。经验库的价值取决于**召回是否发生**——沉淀不等于生效。下一步按面板提示跑一次 `recall --query`。

## 场景 2：参数写错（常见失败组合）

| 错误写法 | 症状 | 自检/修正 |
|---|---|---|
| `draft` 时 strategy 留占位符 `<在此填写…>` | 拒绝落库 | 补全 `FIX:` 具体参数后重试（策略占位符守卫） |
| 用 `--register-hit 3` 位置参数 | 并发下命中错记 | 改用 `--gene <id>`（位置参数仅兼容保留、不可靠） |
| 审核状态写 `approved` 之外的旧值 | 不注入 | 状态精确 `=== 'approved'`，未知/畸形 fail-closed |
| 未设 `EVO_STORE_DIR` 就跑 | 写入默认用户目录 | 显式设隔离目录，避免污染真实库 |

**关键点**：以上失败类型均可用 `info` + 退出码自检定位，不需要模型端点；复杂参数组合的预期行为见 `docs/common-mistakes.md`（14 条反模式）。
