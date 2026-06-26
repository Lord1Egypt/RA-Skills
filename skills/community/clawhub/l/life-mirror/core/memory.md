# 记忆与存储结构

## 初始化配置（必须执行）
- 每次执行前先读取 `core/config.yaml` 配置文件
- 根据配置设置所有可变参数（存储路径等）

## 存储目录
- **路径**：从配置 `storage.directory` 读取
- **无文件则建**：若目录不存在，自动创建

## 会话要求（必须执行）

### 每轮对话（包括定时任务）前
1. **读取文件**：从配置 `storage.directory` 读取存储目录路径，读取该目录下的文件
2.获取用户画像、授权、事实、推断等信息，答复要基于这些信息来答复
2. **判断冷启动**：若画像不足，必须立即执行冷启动（详见 `workflows/profile-sync.md`）

### 每轮对话（包括定时任务）后
1. **落盘**：将本轮个人信息、新事实、推断、待办等信息写入对应文件，画像更新 `profile.json`，客观事实写入 `memory_facts.jsonl`，推断写入 `memory_inferences.jsonl`，推断须引用证据，待办写入 `todos.jsonl`
3. **标记时间**：记录本次交互时间

## 核心文件说明

### profile.json（从配置 `storage.files.profile` 读取）
- **示例**：
```json
{
  "user_id": "...",
  "basic_info": {
    "age": 0,
    "occupation": "",
    "location": ""
  },
  "authorized_platforms": ["douyin", "xiaohongshu"],
  "preferences": {
    "push_time_window": "21:00-23:00",
    "topics": ["career", "relationship"]
  },
  "energy_map": {
    "high_energy_periods": ["09:00-11:00"],
    "low_energy_periods": ["14:00-16:00"]
  }
}
```

### memory_facts.jsonl（从配置 `storage.files.facts` 读取）
- **格式**：每行一条 JSON，记录客观事实
- **示例**：
  ```json
  {"id":"fact_20260404_001","content":"用户提到想转行到互联网行业","timestamp":"2026-04-04T10:00:00+08:00"}
  ```

### memory_inferences.jsonl（从配置 `storage.files.inferences` 读取）
- **格式**：每行一条 JSON，记录推断
- **示例**：
  ```json
  {"id":"inf_20260404_001","content":"用户对当前职业满意度低","evidence":"fact_20260404_001","timestamp":"2026-04-04T10:05:00+08:00"}
  ```

### todos.jsonl（从配置 `storage.files.todos` 读取）
- **格式**：每行一条 JSON，记录待办事项
- **示例**：
  ```json
  {"id":"todo_20260404_001","content":"更新简历","deadline":"2026-04-05T18:00:00+08:00","priority":"high","status":"pending"}
  ```
