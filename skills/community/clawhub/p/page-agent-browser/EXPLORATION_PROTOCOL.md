# 自主熟悉（active-safe）

用于**经验未命中**时安全探页：沉淀 `elements` / `exploration-log`，**不**代替高风险业务。**正式任务**（用户已授权，含 `upload`）不受下述禁令约束。

## 目标

识别状态、稳定选择器、可复用非关键入口 → 写入自建 **`platforms/<site>/elements.md`** 与 **`exploration-log.md`**。

## 允许

`state`、滚动、`hover`、展开型只读点击、读文本/role/aria/URL。

## 禁止（仅探索模式）

命中 **`CRITICAL_ACTIONS.md`** 的点击；表单提交；**`input`/`upload`/`select`** 等写数据/传文件；离站白名单导航；删/付/发等账号敏感动作。

| 能力 | 探索 | 正式任务 |
|------|------|----------|
| `upload` | 禁 | 允许（按 `CLI_REFERENCE` 对齐 `[n]`） |
| `input` | 禁 | 允许 |

## 触发

用户要求先熟悉；recipe 缺；回放失败需补单元素。

## 停止探索

需关键操作才能继续；验证码/登录墙；两轮仍找不到入口。

## 效率

结论导向；单页优先 **3–5** 个高价值元素；日志写摘要不写长原文。

## 产出与 recipe 边界

- 探索阶段只沉淀 **`elements.md`** 与 **`exploration-log.md`**（建议写清：触发原因、动作范围、新增/修补条目、仍未覆盖部分）。  
- **不要**在纯探索里写完整业务 **`recipes/*.md`**；完整 recipe 在**真实业务任务跑通后**再写（与 **`ARCHITECTURE.md`** §2 一致）。
