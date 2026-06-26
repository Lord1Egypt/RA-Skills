# MaskClaw 自进化机制设计

## 概述

本文档记录了 MaskClaw 隐私代理系统中**自进化机制**的架构设计与实现细节。

---

## 一、核心概念：四阶段进化闭环

整个自进化机制由四个核心阶段组成，形成完整的生产级生命周期：

### 阶段 1：收集（Collect）— Behavior Monitor

**职责**：实时监听 GUI Agent 执行过程中的用户行为与纠错信号。

**关键特性**：
- **实时/同步**：嵌入 `proxy_agent.py` 或 `api_server.py` 的主干流
- **轻量级**：每次云端 Agent 返回动作或用户修正时立即捕获并记录
- **极度轻量**：绝不能阻塞用户当前的 GUI 操作

**输出**：
- `behavior_log.jsonl` — 所有操作的轻量记录
- `correction_log.jsonl` — 只有用户参与的完整记录（Evolution Mechanic 的原料）

---

### 阶段 2：评估（Evaluate）— 规则置信度计算

**职责**：对收集的日志进行配对、分组与置信度评估。

**工作流**：
1. 读取 `logs/{user_id}/correction_log.jsonl`
2. 按 (user_id, action, app_context) 分组
3. 计算每组的 confidence（置信度）
4. 过滤掉 `confidence < 0.6` 的组（待观察）
5. 过滤掉分组数量 < N=2 的组（信号不足）

---

### 阶段 3：生成（Generate）— 规则提炼

**职责**：调用端侧 MiniCPM-o 大模型，基于用户纠错日志提炼个性化隐私规则。

**工作流**：
1. 打包输入（Prompt 模板 + 日志数据）
2. POST 请求至 `http://127.0.0.1:8000/chat`
3. 解析模型输出，提取结构化规则 JSON
4. 解析失败时记录错误，跳过本组，不中断整体流程

**输出格式**：
```json
{
  "rule_id": "user_B_20260318_001",
  "user_id": "user_B",
  "scene": "非电商平台注册",
  "sensitive_field": "home_address",
  "strategy": "replace",
  "replacement": "公司地址",
  "rule_text": "在非电商平台注册时，用公司地址替代家庭住址",
  "confidence": 0.82,
  "trigger_count": 3,
  "created_ts": 1700000000
}
```

---

### 阶段 4：验证（Verify）— 沙盒回归测试

**职责**：确保新规则不与历史 Allow 记录冲突，防止策略坍塌。

**工作流**：
1. 读取该用户历史 Allow 记录（behavior_log 中 resolution=allow 的条目）
2. 逐条检验：新规则是否会误拦历史 Allow 操作
3. 发现冲突：记录冲突原因，尝试缩窄规则的 scene 条件后重新验证
4. 二次验证仍冲突：拒绝写入，写入 `candidate_rules_rejected.jsonl`
5. 验证通过：进入写入 RAG 阶段

---

## 二、架构决策

### 决策 1：实时监控与闲时进化的解耦

**问题**：Monitor 和 Evolution 能放在一起执行吗？

**结论**：逻辑上属于同一个"自进化子系统"，但在执行流上必须**完全解耦**。

| 模块 | 执行模式 | 特点 |
|------|----------|------|
| Behavior Monitor | 实时/同步 | 必须嵌在主干流中，轻量级，绝不阻塞 GUI 操作 |
| Evolution Mechanic | 异步/批处理 | 调用大模型进行深度思考，可能耗时十几秒甚至几分钟 |

**正确的连接方式**：通过**存储解耦**，即日志文件（或数据库）。

```
Monitor (Write) → 日志文件 → Evolution (Read) → ChromaDB
```

---

### 决策 2：多租户用户隔离

**问题**：云端服务器如何处理多本地客户端？

**架构设计**：

#### 第一步：API 接口必须带 `user_id`

本地 Windows 客户端在请求云端时，必须在 Header 或 Payload 中附带唯一标识（如 `client_id="win_user_001"`）。

#### 第二步：Monitor 的隔离存储

按用户建文件夹存 JSON：

```
logs/
├── /win_user_001
│     └── conflict_logs.jsonl  ← 只存 user_001 的行为日志
└── /win_user_002
      └── conflict_logs.jsonl
```

#### 第三步：Evolution 的隔离归纳与入库

利用 ChromaDB 的 Collection 机制实现分区：

```python
# 每个用户在 ChromaDB 里拥有独立的 Collection
collection_name = f"rules_{user_id}" 
collection = chroma_client.get_or_create_collection(name=collection_name)

# 将进化出的规则存入该用户的专属库
collection.add(
    documents=[rule_text],
    metadatas=[rule_metadata],
    ids=[generate_uuid()]
)
```

#### 第四步：Proxy Agent 的个性化读取

1. `proxy_agent.py` 拿到 `user_id="win_user_001"` 和当前屏幕画面
2. 去 ChromaDB 查询 `Collection("rules_win_user_001")`
3. 拿出专属规则，塞进系统 Prompt 里，完成防护

---

## 三、日志 Schema 要点

### 级别 1：轻量记录

```json
{
  "event_id": "user_A_1700000001_3821",
  "user_id": "user_A",
  "ts": 1700000001,
  "app_context": "taobao",
  "action": "fill_shipping_address",
  "field": "home_address",
  "resolution": "allow",
  "level": 1,
  "processed": false,
  "expire_ts": 1700086401
}
```

### 级别 2：完整记录（用户纠错）

```json
{
  "event_id": "user_A_1700000042_1156",
  "user_id": "user_A",
  "ts": 1700000042,
  "app_context": "wechat",
  "action": "send_file",
  "field": "file_content",
  "resolution": "interrupt",
  "level": 2,
  "processed": false,
  "expire_ts": 1700086442,
  "value_preview": "病历截图.jpg",
  "correction_type": "user_interrupted",
  "correction_value": null,
  "pii_types_involved": ["MEDICAL_RECORD"]
}
```

### 哪些 correction_type 进入 Evolution

只有以下三种是有效的训练信号：
- `user_denied` — 用户明确不想要这个操作
- `user_modified` — 用户有具体偏好，信号最强
- `user_interrupted` — 用户主动介入，行为意图最明确

---

## 四、进化流水线

### 完整流程图

```
┌────────────────────────────────────────────────────────────────┐
│                    SOP 自进化完整流水线                          │
└────────────────────────────────────────────────────────────────┘

1. rebuild     →  读取日志，重建会话轨迹
       ↓
2. init        →  创建 SOP 草稿
       ↓
3. evolve      →  爬山法迭代优化
   ├── mutate     (变异)
   ├── test       (批量测试)
   ├── evaluate   (评分决策)
   └── repeat     (直到达标或停滞)
       ↓
4. sandbox     →  沙盒验证
       ↓
5. publish     →  发布到 user_skills/
```

### 断点续传

系统重启后，可以自动恢复中断的进化流程：

1. 检测 `is_best=1` 且 `stage='evolving'` 的草稿
2. 从断点继续执行
3. 无需从头开始

---

## 五、置信度计算策略

### 触发条件

同一用户的同一类操作，累积了 N=2 条以上有效纠错记录后，触发进化。

### 置信度公式

```
confidence = base_score * frequency_boost * recency_boost

其中：
- base_score = 0.6 (基础分)
- frequency_boost = min(1.0, trigger_count / 5)  # 最多触发5次
- recency_boost = 0.8 + 0.2 * (time_since_last / 7_days)  # 最近7天内最高
```

---

## 六、沙盒验证策略

### 验证流程

```
1. 读取历史 Allow 记录
         ↓
2. 逐条检验新规则是否会误拦
         ↓
    ┌─────────────────┐
    │  发现冲突？      │
    └────────┬────────┘
         是 ↓            否
    尝试缩窄 scene    →  验证通过
         ↓
    ┌─────────────────┐
    │  二次冲突？      │
    └────────┬────────┘
         是 ↓            否
    拒绝写入        →  写入 RAG
```

### 冲突判断

新规则与历史 Allow 冲突的条件：
- 新规则 `strategy=block` 但历史有 `resolution=allow`
- 新规则的 `sensitive_type` 与历史操作相同
- 新规则的 `scene` 包含历史的 `app_context`

---

## 七、后续工作建议

### 选项 A：实现 Monitor 的具体功能

- 如何接收拦截数据
- 如何以高并发安全的方式追加写入 `logs/{user_id}/conflict.jsonl`

### 选项 B：实现 Evolution 的主逻辑

- 如何读取 JSONL
- 如何拼装 Prompt 交给模型
- 如何调用 `chroma_manager.py` 写入对应用户的向量库
