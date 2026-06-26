# 邮件定时解析入库（路由 A · 硬性）

**路由 A** 的邮件 **2.4 解析 → 2.4.1 SQLite → 2.4.2 富化** 由**后台定时任务**完成，**不是**用户每次提问时才解析。

---

## 1. 原则

1. **每 10 分钟**（或宿主环境允许的等价周期）执行一轮：**增量同步邮箱 → 脱敏 → LLM 解析 → `save` 落库 → `enrich` 富化**。  
2. 用户提问时（**Workflow 2.3**）：**只读**已入库的 SQLite + 向量检索；**禁止**因「本轮还没解析」而在回答流程里批量解析历史邮件（除非用户明确要求「立即解析某封」）。  
3. 目标：**每封新邮件最终都会被解析并入库**，不依赖用户是否提问。

---

## 2. 单轮流水线（助手或脚本代执行）

| 步骤 | 说明 |
|------|------|
| ① 增量同步 | 与 **2.2** 相同：IMAP/记忆插件拉取未入库新邮件 |
| ② 待解析队列 | 取尚未写入 `charter_facts.sqlite3` 的 `message_id`（或插件标记为 unparsed） |
| ③ 脱敏 | **2.3.5** 规则 |
| ④ 解析 | **2.4** + **`PARSE_SCHEMA.md`** |
| ⑤ 落库 | `python scripts/charter_facts_tool.py save -f …` |
| ⑥ 富化 | `python scripts/charter_facts_tool.py enrich`（enrich-row **与 portid 解耦**；**每行 portid 必须尝试入库**，见 **`CHARTER_ENRICH_API.md` §2**） |

**一键脚本（推荐）**：`python scripts/mail_parse_loop.py --once`（单轮：IMAP 增量 → 解析/待解析队列 → `save` → `enrich`）；常驻 `python scripts/mail_parse_loop.py --daemon`。  
助手在 OpenClaw 计划任务中可每 **10 分钟**调用 `--once`，**勿**要求用户手写 cron。

- 若本机有 **`charter_ai`**（或设置 `HIFLEET_CHARTER_AI_ROOT`），脚本自动调用大模型完成 **2.4** 解析。  
- 否则将脱敏后的邮件写入 **`mail_pending/`**，由助手读取后解析，并将完整 JSON 放入 **`mail_parsed_inbox/`**（含 `message_id`、`parsed` 等），下一轮 `--once` 自动 `save`。

---

## 3. 定时方式（零基础）

- **OpenClaw / 宿主计划任务**：每 **10 分钟**触发一次上述流水线（由助手配置或用户点确认，**勿**要求用户手写 cron 语法）。  
- **对话内兜底**：用户提问前若距上次解析 **>10 分钟**，助手可先跑**一轮**流水线再检索；**不得**替代常驻定时任务。  
- **失败**：记录错误；下一轮重试；向用户说明「部分新邮件尚未解析完成」。

---

## 4. 与 Workflow 2 的衔接

- **2.2**：保留「提问前增量同步」仅同步**原文到向量库**；解析入库走本节定时任务。  
- **2.3 第 4 步**：删除「向量召回后再 2.4 解析」的默认路径；改为「未入库邮件等待定时任务，或触发一次立即解析」。  
- **2.4.2**：定时任务在每次 **`save` 后必须 `enrich`**。

---

## 5. 配置

`config.json` 可选：

```json
{
  "mail_parse_interval_minutes": 10
}
```

环境变量 **`HIFLEET_MAIL_PARSE_INTERVAL_MINUTES`** 可覆盖。
