---
name: mem0-status-check
description: |
  检查 mem0 本地记忆系统的功能完整性和运行状态。每次被问到 mem0 功能、状态、是否完整时触发。
  触发词：mem0状态、mem0功能、检查mem0、mem0正常吗、mem0完整性
---

# mem0 状态检查

## 执行步骤

### 第一步：运行 mem0 search 测试语义搜索
```powershell
& C:\Users\Administrator.DESKTOP-BD1JUD0\anaconda3\python.exe D:\autoclaw\结果\mem0\mem0_wrapper.py search main_user "test" --limit 1
```
预期：有返回结果（memory 字段非空）

### 第二步：运行 get_all 获取全部记忆数量
```powershell
& C:\Users\Administrator.DESKTOP-BD1JUD0\anaconda3\python.exe D:\autoclaw\结果\mem0\mem0_wrapper.py get_all main_user
```
预期：返回记忆列表，计数 > 0

### 第三步：检查 cron 任务状态
```powershell
# 从当前会话的 cron list 获取 mem0 相关任务运行状态
```

### 第四步：检查 Chroma 向量库
```powershell
Get-ChildItem D:\autoclaw\结果\mem0\chroma_db -ErrorAction SilentlyContinue | Measure-Object
```
预期：文件数量 > 0

---

## 检查项目列表（逐项报告）

| # | 功能 | 状态 | 说明 |
|---|------|------|------|
| 1 | add 第一次 LLM 提取 | 待确认 | 使用 USER_MEMORY_EXTRACTION_PROMPT + AGENT_MEMORY_EXTRACTION_PROMPT（含 few-shot examples） |
| 2 | add 第二次 LLM 对比 | 待确认 | 应有 ADD/UPDATE/DELETE 决策逻辑，目前疑似直接调 m.add() |
| 3 | search 语义搜索 | 待确认 |  |
| 4 | get_all 获取全部记忆 | 待确认 |  |
| 5 | update 更新记忆 | 待确认 |  |
| 6 | delete 删除记忆 | 待确认 |  |
| 7 | history 操作历史 | 待确认 |  |
| 8 | delete_all 全量删除 | 待确认 |  |
| 9 | reset 重置 | 待确认 |  |
| 10 | 流程记忆 Procedural | 待确认 | memory_type="procedural_memory" 支持 |
| 11 | 情景记忆 Episodic | 待确认 | cmd_add_episodic() 实现 |
| 12 | MEMORY_ANSWER_PROMPT | 待确认 | cmd_chat() 里使用 |
| 13 | 增强版提示词模板 | 待确认 | prompts_zh.py 中的模板 |
| 14 | MCP Server (stdio) | 待确认 | mem0_mcp_server.py |
| 15 | 定时去重合并 cron | 待确认 | mem0-daily-dedup，每天凌晨3点 |
| 16 | Chroma 向量库存储 | 待确认 | D:\autoclaw\结果\mem0\chroma_db |

---

## 输出格式

```
【mem0 状态报告】

✅ 正常运行：
- search：正常
- get_all：X 条记忆
- 定时 cron：mem0-session-memory / mem0-daily-dedup
- Chroma：X 个文件

⚠️ 缺失功能：
- [具体功能名]：[原因/说明]

🔧 建议补充：
- [具体建议]
```
