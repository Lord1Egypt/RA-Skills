# 本 Skill 的定位与零基础说明（与 `SKILL.md` 对应章节全文一致，不得删减）

## 本 Skill 的定位：谁发布、装在哪、数据在哪

- **发布方**：**HiFleet** 将本 Skill 提供给市场；用户在 **Codex、OpenClaw** 等环境中**本地安装**。  
- **路由 A（本人邮箱船货盘）**：用户**本人邮箱**；向量库、本地船货盘库在**本机**；补充信息走 **`CHARTER_ENRICH_API.md`**（须 **`hifleet_api_key`**）。  
- **路由 B（班轮船期）**：HiFleet **`api.hifleet.com`**；**`SCHEDULE_API.md`**。  
- **路由 C（预抵船舶）**：HiFleet 预抵查询；**`DESTINATION_SEARCH_API.md`**。  
- **B/C** 共用 **`hifleet_api_key`**。  
- **首次安装**：**`FIRST_SETUP.md`**。  
- **对用户说话**：**`USER_WORDING.md`**。

---

## 面向用户：零基础友好（必读）

- **不要求用户自己安装 Python**、不要求徒手敲终端。  
- **memory-lancedb-pro**：须用户**同意**后代执行。  
- **本地船货盘库**：单文件 `charter_facts.sqlite3`（见 **`SQLITE_SETUP.md`**）。

**三种能力一句话**：**A=我的邮件**；**B=班轮船期**；**C=预抵船舶**。B/C 要 **API Key**，A 要 **邮箱**。
