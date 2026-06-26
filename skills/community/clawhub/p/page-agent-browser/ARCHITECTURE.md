# page-agent-browser 架构

## 1. 文档分层

| 层级 | 文件 | 职责 |
|------|------|------|
| 根 | `SKILL.md` | 最短路径：CDP、Tab、原语入口 |
| CLI | `CLI_REFERENCE.md` | 与 `page-agent --help` 一致 |
| 规范 | `EXPERIENCE_SCHEMA.md`、`CRITICAL_ACTIONS.md`、`EXPLORATION_PROTOCOL.md` | 经验格式、critical、探索边界 |
| 本地 | `platforms/<site>/` | **自建**站点包与经验；仓库内 `platforms/` 仅占位 |

有 `platforms/<site>/` 时阅读顺序：`SKILL.md` → 该站 `SKILL.md` → `recipes`/`elements`；命令细节始终 **`CLI_REFERENCE.md`**。

## 2. 复用

1. **recipe 命中**：按步骤语义执行，`state` 把元素键解析为索引（可按经验省略 `state`，错位即补）。  
2. **仅 elements**：拼步骤，跑通后补 `recipe`。  
3. **未命中**：`EXPLORATION_PROTOCOL.md` 探索 → 写 `elements` → 任务成功后再写 `recipe`。  
经验载体是 **Markdown**，不是隐藏库。

## 3. 自愈与复盘（本地文件）

失败重发现 → 更新 `elements.md` 选择器链；修补记入 **`health.md`**；探索过程记入 **`exploration-log.md`**。用户要复盘时读 `health` + 失败记录。

## 4. 探索（active-safe）

触发与禁止动作见 **`EXPLORATION_PROTOCOL.md`**。产出写入自建 **`platforms/<site>/elements.md`** 与 **`exploration-log.md`**。用户已授权的正式任务（含 `upload`）**不受**探索禁令约束。

## 5. 「权限」

1. **allowed-tools**：宿主决定能否跑 `page-agent`。  
2. **critical**：`CRITICAL_ACTIONS.md` + 本地 `critical.md` + recipe 里 `confirmHuman` → **`AskQuestion` 或文字确认** 后再点。  
3. **探索 vs 正式**：探索禁写站数据、`upload` 等；正式任务在用户授权下可用。  

CDP 控的是**用户本机浏览器**；最终风险由用户是否开调试、是否把敏感操作交给 Agent 决定。
