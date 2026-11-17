# Sponsored Brands（SB）API 索引

本 skill 同时提供 V3 Legacy 兼容入口和 V4 主入口：

- [V3 Legacy 参数与脚本](./sb-v3.md)
- [V4 参数与脚本](./sb-v4.md)
- [V3/V4 共存、路由和禁止自动回落规则](./sb-coexistence.md)

## 能力摘要

| 入口 | Campaign | Ad Group | Ad | Keyword | Target | Creative Version |
|---|---:|---:|---:|---:|---:|---:|
| `scripts/sb/v3/` | ✅ Legacy | 查询 | — | ✅ | ✅ | Campaign payload 内嵌 |
| `scripts/sb/v4/` | ✅ | ✅ | ✅ | ✅（共享路径） | ✅（共享路径） | ✅ |

## 默认选择

1. 新业务、新建 Campaign、多 Ad Group、Ad 和 Creative 使用 V4。
2. Keyword / Target 未指定版本时也使用 V4 入口；底层是 Amazon 共享 targeting 路径。
3. 只有已确认 Campaign 为 Legacy，或用户明确要求 V3 时，才调用 V3。
4. 不执行 V4 → V3 自动回落。
5. V3 不允许管理已知的 Multi-Ad-Group Campaign。

## 兼容路径

原 `scripts/sb/*.py` 保留，仍指向既有 V4 Campaign/AdGroup/Ad/BudgetRule 实现。新调用统一使用带版本的路径，避免后续新增能力时产生歧义。
