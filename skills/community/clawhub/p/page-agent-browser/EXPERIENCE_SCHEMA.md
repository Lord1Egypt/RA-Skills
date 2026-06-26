# 经验文件 Schema（Markdown）

## 1. 目录里有什么（自建 `platforms/<site>/`）

`elements.md`、`recipes/*.md`、`critical.md`；运行期可维护 `exploration-log.md`、`health.md`。  
**`teach` 交互产物**：用户点 **「确认写入 Agent 经验」** 后 CLI **exit 0** 的 **`--json` stdout** 才是可入库的 teach 结果 JSON；可保存为 `lessons/*.json` 再据此更新 `elements`/`recipes`（**检查点文件**见 **`SKILL.md`**「经验沉淀」与 **`CLI_REFERENCE.md`「teach」**）。

## 2. `elements.md` 头与块

YAML：`site`、`last_verified`、`last_full_scan`（日期占位即可）。正文：按 **状态** 分节（URL/selector 识别），每元素：**描述**、**优先选择器**列表、**验证**、`critical`、`source`、`success`/`fail`/`last_used`。

选择器优先级：`aria-*` / `role+name` → `data-testid` → 稳定文案 → CSS 兜底。

## 3. `recipe` 头与步骤

YAML：`recipe`、`input`、`success`/`fail`/`last_run`。步骤用语义键引用 `elements.md`，**禁止**把当次索引写死进 recipe 结论。

步骤类型示例：`ensureState`、`click`、`hover`、`waitState`、`input`、`upload`、`confirmHuman`、`verify`。`upload` 的索引与 **`eval`/`state`/`upload` 锚点** 语义见 **`CLI_REFERENCE.md`**（**不要求** `state` 文本中必须出现 `type=file` 行，但须有可用的 `state` 映射与正确锚点）。

## 4. 执行约定

- `ensureState`：先进入目标状态。  
- `click`/`hover`/`input`/`eval`：用当次 `state` 解析索引。  
- `upload`：执行时使用当次 **`state` 给出的 `[n]`** 作锚点（可为 file 行或上传入口控件）；与 CLI 解析规则一致，见 **`CLI_REFERENCE.md`**。  
- `waitState` / `confirmHuman` / `verify`：超时 fallback；人工确认；可观察成功条件。

## 5. 自愈

选择器全失败 → `state` 重发现 → 新选择器**插顶**、旧链保留 → 更新计数 → **`health.md`** 记一笔。

旧 SOP 仅作过渡入口，正文应指向 `recipes` + `elements`。
