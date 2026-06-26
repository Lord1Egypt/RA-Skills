---
name: hifleet-mytonnages
version: 1.2.0
description: >
  hifleet-skills 租船模块：A=本人邮箱船货盘；B=班轮船期；C=预抵船舶查询。须 hifleet_api_key（B/C及A补充信息）与邮箱（A）。首次安装见 FIRST_SETUP.md。勿伪造数据。
metadata:
  openclaw:
    homepage: https://mytonnages.hifleet.com
    requires:
      anyBins:
        - python
        - python3
---

## 必读分册（附录正文不得删减）

执行任意查询步骤前：**`read_file` `SKILL_CONTEXT.md`**、**`read_file` `ROUTING_AND_WHEN.md`**（能力路由 A/B/C、When to Run）。

**对用户说话**：**`read_file` `USER_WORDING.md`**（禁止对用户说 workflow、schema 等术语）。

**首次安装 / 配置缺失**：**`read_file` `FIRST_SETUP.md`** 全文，完成 API Key 与邮箱检查，并向用户说明提问方式与路由对应（**§E**）。

**首次启用记忆（memory-lancedb-pro）**：**`MEMORY_LANCEDB.md`**；路由 A 邮件检索前须执行。

**首次写入本地船货盘库**：**`SQLITE_SETUP.md`**（若随包）；路由 A 落库前须执行。

**列表全量（路由 B/C）**：**`FULL_LIST_POLICY.md`**；班轮船期/预抵须分页拉齐 **`total`**，**查到多少展示多少**，禁止只返回前几条。

**邮件定时解析（路由 A）**：**`MAIL_PARSE_SCHEDULE.md`**；每 **10 分钟**解析入库+补充信息，用户提问时只读库。

---

## 查询步骤（助手内部）

### 0. 就绪顺序（每次会话 / 首次安装）

1. **（强制）能力路由**：**`ROUTING_AND_WHEN.md`**。判断 A / B / C 或组合。  
2. **（强制）首次与配置检查**：若 `config.json` 不存在、或用户说「第一次用」「初始化」「怎么配置」、或 B/C 无 **`hifleet_api_key`**、或 A 无邮箱配置 → **`FIRST_SETUP.md`**（**§B～G**）。  
3. **若本次不含路由 A**：跳过下列第 5～7 步中与邮件/本地库相关的部分。  
4. **若本次不含路由 B/C**：跳过 **步骤 3～4**（班轮/预抵）。  
5. **记忆（路由 A）**：未完成 memory-lancedb-pro 知情同意 → **`MEMORY_LANCEDB.md`**。  
6. **邮箱（路由 A）**：`config.json` 不完整 → **邮箱配置**（**`WORKFLOW_1_MAIL.md`**）。  
7. **本地船货盘库（路由 A）**：未确认可写 `charter_facts.sqlite3` → **`SQLITE_SETUP.md` §B**。  
8. 就绪后：路由 A → **邮件查询**；路由 B → **班轮船期**；路由 C → **预抵查询**。同轮多路由**分别**执行。

### 1. 邮箱配置（路由 A）

**`WORKFLOW_1_MAIL.md`** 全文（**1.1～1.4**）。执行前 **`read_file`**。

### 2. 邮件查询（路由 A）

**`WORKFLOW_2_MAIL.md`** 全文；补充船货信息 **`CHARTER_ENRICH_API.md`**；定时解析 **`MAIL_PARSE_SCHEDULE.md`**。  

### 3. 班轮船期（路由 B）

**`SCHEDULE_API.md`** 全文；须 **`hifleet_api_key`**。**列表须全量**：**`FULL_LIST_POLICY.md`**。解锁 `typeCode=product_vessel_liner_charter`。

### 4. 预抵船舶（路由 C）

**`DESTINATION_SEARCH_API.md`** 全文；须 **`hifleet_api_key`**。**列表须全量**：**`FULL_LIST_POLICY.md`**。  
`POST {charter}/destination/search?api_key=…`

## Output 与配置口令

**`WORKFLOW_OUTPUT.md`**、**`USER_WORDING.md`**（**不得删减含义**）。

## Notes

**日期**：邮件仅月日则补当前年 2026；船龄则建造年 = 2026 − 船龄。**命名**：TBN 保留；多港用 `+`。**安全**：密码 base64 等本地存储；对话勿显式密码与完整 `api_key`。

**随包文件索引**

```text
<技能安装目录>/hifleet-skills/hifleet-mytonnages/
├── SKILL.md
├── SKILL_CONTEXT.md
├── USER_WORDING.md          # 对用户说话用词
├── FIRST_SETUP.md
├── ROUTING_AND_WHEN.md      # 能力路由 A/B/C
├── MEMORY_LANCEDB.md
├── SQLITE_SETUP.md
├── WORKFLOW_1_MAIL.md
├── WORKFLOW_2_MAIL.md
├── WORKFLOW_OUTPUT.md
├── SCHEDULE_API.md          # 路由 B
├── DESTINATION_SEARCH_API.md # 路由 C 预抵
├── FULL_LIST_POLICY.md
├── MAIL_PARSE_SCHEDULE.md
├── CHARTER_ENRICH_API.md
├── PARSE_SCHEMA.md          # 邮件解析字段（助手内部）
├── CONFIG.example.md
├── scripts/charter_facts_tool.py
├── scripts/mail_parse_loop.py
└── charter_facts.sqlite3（运行时生成）
```

ClawHub 发布说明见 **`PUBLISH.md`**。
