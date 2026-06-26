---
name: mem0-memory
version: 2.1.0
description: "mem0 本地记忆层完整实现（增强版）。语义记忆存储/检索/管理，WAL 协议，SESSION-STATE，多级记忆（User/Session/Agent）。参考 ZejunCao/bilibili_code Mem0框架解读优化。"
---

# mem0 Memory 🧠 — 完整实现（增强版）

## 组件

| 组件 | 技术 | 作用 |
|------|------|------|
| LLM | MiniMax-M2.7 | 记忆生成与提取 |
| Embedder | Ollama `nomic-embed-text` | 本地语义向量化（完全离线） |
| 向量库 | Chroma | 本地向量存储 |
| Ollama | 开机自启 | 向量服务 |

文件路径：`D:\autoclaw\结果\mem0\`

## 增强功能（参考 bilibili_code 课件）

### chat_with_memories 对话模式
`mem0_wrapper.py chat` 命令实现了完整的记忆增强对话流程：
```
1. search 检索相关记忆
2. 将记忆注入 system prompt
3. 调用 MiniMax LLM 生成回复
```

### 中文记忆提取
内置 FACT_RETRIEVAL_PROMPT，自动将用户对话提取为中文记忆条目。

### 多级记忆支持
`--run` 参数支持 Session 级别记忆，`--agent` 支持 Agent 级别记忆。

## 完整 API（10 个命令）

```bash
# 增删改查
python D:\autoclaw\结果\mem0\mem0_wrapper.py add <user_id> "<内容>"              # 添加记忆（自动提取）
python D:\autoclaw\结果\mem0\mem0_wrapper.py search <user_id> "<query>"          # 语义搜索
python D:\autoclaw\结果\mem0\mem0_wrapper.py get_all <user_id>                 # 全部记忆
python D:\autoclaw\结果\mem0\mem0_wrapper.py get <memory_id>                    # 单条记忆
python D:\autoclaw\结果\mem0\mem0_wrapper.py update <memory_id> "<新内容>"     # 更新记忆
python D:\autoclaw\结果\mem0\mem0_wrapper.py delete <memory_id>                # 删除记忆
python D:\autoclaw\结果\mem0\mem0_wrapper.py history <memory_id>               # 修改历史

# 记忆增强对话（新增）
python D:\autoclaw\结果\mem0\mem0_wrapper.py chat <user_id> "<问题>"            # 检索+注入+LLM回答

# 重置
python D:\autoclaw\结果\mem0\mem0_wrapper.py delete_all <user_id>               # 清空用户记忆
python D:\autoclaw\结果\mem0\mem0_wrapper.py reset                              # 清空全部记忆（慎用）

# 可选参数
--limit N    # 限制返回数量（search/chat 默认5）
--run <id>  # 指定会话ID（session级别记忆）
--agent <id> # 指定智能体ID（agent级别记忆）
```

## 多级记忆架构

```
mem0 存储层
├── User Memory（user_id=main_user）  ← 跨会话长期记忆
├── Session Memory（run_id）           ← 单会话临时记忆
└── Agent Memory（agent_id）           ← 多智能体共享记忆
```

当前实现：User Memory（`main_user`），SESSION-STATE.md 作为 Session 层补充。

## WAL 触发扫描（每消息必做）

| 触发类型 | 示例 | 存储 |
|---------|------|------|
| 偏好 | "我喜欢..." / "不要..." | mem0 add |
| 经历 | "我去了..." / "我做过..." | mem0 add |
| 重要事实 | "我有..." / "我是..." | mem0 add |
| 纠正 | "不是Y，是X" / "其实..." | SESSION-STATE |
| 决定 | "就用X" / "去..." | SESSION-STATE + mem0 |
| 数字/日期 | 具体数字+单位、日期 | SESSION-STATE |
| URL/路径 | 链接、文件路径 | SESSION-STATE |
| 专有名词 | 名字、地点、公司、产品 | 判断后存储 |

**优先级**：SESSION-STATE > mem0

## 完整工作流

### 收到消息时
```
扫描类型
  ├─ [偏好/经历/事实] → mem0 add
  ├─ [纠正/决定/数字/URL] → SESSION-STATE.md
  └─ [闲聊/无价值] → 不存
回复用户
```

### 回复后
```
上下文使用率 > 60%？
  └─ 是 → WORKING-BUFFER.md 激活
```

### 截断恢复（下次会话）
```
1. mem0 get_all → 恢复长期语义记忆
2. mem0 chat → 主动询问是否继续上次任务
3. SESSION-STATE.md → 恢复当前任务状态
4. WORKING-BUFFER.md → 恢复危险区对话
```

## 参考资料

- **ZejunCao/bilibili_code**（Mem0框架解读）：https://github.com/ZejunCao/bilibili_code
  - `mcp_server.py` — FastMCP + mem0 REST 服务架构参考
  - `prompts_zh.py` — 中文提示词模板（USER_MEMORY_EXTRACTION_PROMPT 等）
  - `demo.ipynb` — chat_with_memories 完整流程
  - `踩坑记录.md` — OpenMemory 调试踩坑

## 注意事项

- Ollama 必须后台运行（已设开机自启）
- 添加需要 LLM（慢），搜索只需 embedder（快）
- SESSION-STATE 优先于 mem0
- 危险操作（reset/delete_all）需要二次确认
- memory_id 是记忆的唯一标识，用于 update/delete/history
