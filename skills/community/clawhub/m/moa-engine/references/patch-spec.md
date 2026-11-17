# Patch 规范（Patch Specification）

## 概述

Patch 是 RHI 闭环中用于"修改 Prompt 自由区"的指令规范。Patch 不修改 IMMUTABLE 区域，只在自由区注入增强指令。

## 核心原则

1. **IMMUTABLE 不可触碰**：I1-I6 区域任何 Patch 不得修改、移除或重排序
2. **自由区可修改**：非 IMMUTABLE 的 Prompt 区域可以追加增强指令
3. **增量追加**：Patch 仅在自由区末尾追加内容，不修改已有内容
4. **可逆**：每个 Patch 都包含 round 标记，支持回滚

## IMMUTABLE 保护清单

### 核心不可变（I1-I6）

| 编号 | 保护区域 | 禁止操作 |
|------|---------|---------|
| I1 | `<phase id="3">` 对抗阶段 | 不可移除、跳过或重排序 |
| I2 | `<critic>` 角色标签 | 不可移除或降权 |
| I3 | `<attack>` 批判标签 | 不可移除，severity 值域不可收窄为空 |
| I4 | `<termination_signal>` | 必须显式产出，不可自动生成 |
| I5 | `<final_answer>` "必须再创造" | 不可弱化为"可罗列" |
| I6 | `<response>` + `<revision>` 回应机制 | 专家必须回应批判，不可省略 |

### 保护摩擦区（P1-P3）

| 编号 | 区域 | 允许操作 | 禁止操作 |
|------|------|---------|---------|
| P1 | version 字段 | 可依 Patch 结果递增 | 不可自动递增 |
| P2 | severity 值域 | 可扩展 | 不可收窄 |
| P3 | 对抗轮次下限 | 可提高下限 | 不可降低下限 |

## Patch 结构

### 基本格式

```xml
<patch version="2.2" target="moa-meta-prompt" round="2">
  <!-- 增强指令：追加到自由区末尾 -->
  <enhancement target="critique_specificity">
    <instruction>
      ## RHI 增强指令（第2轮）
      ### 批判精度要求
      上一轮批判精准度不足（0.45）。本轮批判者必须：
      1. 每条批判必须包含具体行号、变量名或逻辑节点
      2. 必须提供可复现的边界测试用例或极端场景
      3. 禁止使用"可能有问题"等模糊表述
    </instruction>
  </enhancement>
</patch>
```

### 结构说明

| 字段 | 说明 |
|------|------|
| `patch.version` | Patch 版本号，与 MoA 版本对齐 |
| `patch.target` | 目标 Prompt 文件 |
| `patch.round` | 轮次编号，用于回滚 |
| `enhancement.target` | 增强目标维度 |
| `enhancement.instruction` | 增强指令文本 |

## Patch 类型

### 1. 维度增强型

针对最弱维度生成增强指令：

```xml
<patch version="2.2" target="moa-meta-prompt" round="2">
  <enhancement target="critique_specificity" reason="score=0.45">
    <instruction>...</instruction>
  </enhancement>
</patch>
```

### 2. 参数调整型

调整对抗轮次、severity 阈值等可调参数：

```xml
<patch version="2.2" target="moa-meta-prompt" round="2">
  <enhancement target="adversarial_rounds" reason="complexity_high">
    <instruction>
      ## RHI 参数调整
      - 对抗轮次下限提升至 2 轮
      - severity 阈值扩展：新增"致命"级别
    </instruction>
  </enhancement>
</patch>
```

### 3. 综合型

同时调整多个维度：

```xml
<patch version="2.2" target="moa-meta-prompt" round="2">
  <enhancement target="critique_specificity" reason="score=0.45">...</enhancement>
  <enhancement target="synthesis_novelty" reason="score=0.52">...</enhancement>
</patch>
```

## 校验规则

### 自动校验（apply 前）

```python
def validate_patch(patch_xml: str) -> bool:
    """校验 Patch 是否触碰 IMMUTABLE 区域"""
    forbidden_xpaths = [
        "//phase[@id='3']",           # I1
        "//critic",                   # I2
        "//attack",                   # I3
        "//termination_signal",       # I4
        "//final_answer",             # I5
        "//response",                 # I6
        "//revision",                 # I6
    ]
    # 任一命中 → 拒绝
    # 全部未命中 → 通过
    ...
```

### 手动校验清单

1. Patch 是否修改了 phase 3 的对抗阶段？
2. Patch 是否移除了 critic 角色？
3. Patch 是否弱化了 final_answer 的"再创造"约束？
4. Patch 是否跳过了专家回应批判的环节？
5. Patch 是否修改了 termination_signal 的显式产出要求？

以上任一答案为"是"，则 Patch 应被拒绝。

## Patch 生命周期

```
生成 ──→ 校验 ──→ 应用 ──→ 执行 ──→ 评估 ──→ (下一轮)
  │        │         │         │         │
  │        │         │         │         └── 若 fitness < 阈值，生成新 Patch
  │        │         │         └── 执行增强后的 MoA
  │        │         └── 追加到 Prompt 自由区末尾
  │        └── 触碰 IMMUTABLE → 拒绝并回滚
  └── 基于信号分析生成
```

## 回滚策略

每个 Patch 包含 round 编号，支持按轮次回滚：

```bash
# 回滚到第 1 轮状态
python scripts/rhi_runner.py rollback --prompt moa-meta-prompt.md --to-round 1
```

回滚时保留所有 IMMUTABLE 区域不变，仅移除 round 编号对应的增强指令。