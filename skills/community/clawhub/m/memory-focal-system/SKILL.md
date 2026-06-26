---
name: memory-focal-system
slug: memory-focal-system
version: 1.0.0
homepage: https://github.com/openclaw-lark/memory-focal-system
description: 焦距记忆系统 - 智能记忆管理，支持消息分类、按需加载、自动标签、遗忘曲线。Token 优化 40-60%。
changelog: 初始版本 - 完整功能上线
metadata: {"clawdbot":{"emoji":"🧠","os":["linux","darwin","win32"]}}
---

## 🧠 焦距记忆系统 (Memory Focal System)

**让 AI 记住重要的事，忘记不重要的事**

---

## 核心功能

### 1. 🎯 焦距记忆机制
根据消息类型自动调节"记忆焦距"，决定读取多少上下文：

| 焦距模式 | 触发场景 | 加载内容 | Token 节省 |
|----------|----------|----------|-----------|
| **远景 (simple)** | 简单对话 | 无 | 100% |
| **中景 (task)** | 任务执行 | 相关记忆 | 60-75% |
| **近景 (memory)** | 情感/偏好 | 完整记忆 | 正常 |
| **微距 (new_info)** | 新信息 | 完整记忆 + 写入 | 正常 |

### 2. ⚡ 频率触发机制
基于访问频率自动强化重要记忆：
- 高频访问 → 自动提升到热存储
- 低频访问 → 自动降级到冷存储
- 智能计算记忆优先级

### 3. 📊 记忆分层管理
三层存储架构，优化性能：
- **热存储 (active)**：最近 7 天，自动加载
- **温存储 (short_term)**：7-30 天，按需加载
- **冷存储 (long_term)**：30 天+，归档保存

### 4. 🤖 LLM 自动标签
AI 自动生成记忆标签，支持语义检索：
- 调用大模型 API（支持 dashscope、openai 等）
- 基于 MD5 缓存，避免重复调用
- 成本约 ¥0.5-10/月

### 5. 📉 遗忘曲线
艾宾浩斯遗忘曲线算法，智能清理：
- 基于存在天数、访问次数计算记忆强度
- 低强度记忆自动归档
- 超过 365 天可删除

### 6. 🔍 双链索引
标签 - 记忆双向索引，快速检索：
- 标签 → 记忆 ID 列表
- 记忆 ID → 标签列表
- O(1) 时间复杂度查询

### 7. 💾 增量式存储
Append-Only JSONL 格式，保证数据完整性：
- 只追加，不修改
- 避免并发冲突
- 易于备份和恢复

---

## 安装

```bash
# 从 ClawHub 安装
clawhub install memory-focal-system

# 或本地安装（已预装）
cd ~/.openclaw/workspace/skills/memory-focal-system
```

---

## 配置

配置文件：`~/.openclaw/workspace/skills/memory-focal-system/config.json`

```json
{
  "enabled": true,
  "auto_classify": true,
  "auto_write": true,
  "load_user": true,
  "load_memory": true,
  "load_focal_active": true,
  "token_limit": 8000
}
```

### 配置说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | bool | true | 是否启用记忆系统 |
| `auto_classify` | bool | true | 自动分类消息 |
| `auto_write` | bool | true | 自动写入新记忆 |
| `load_user` | bool | true | 加载用户配置文件 |
| `load_memory` | bool | true | 加载长期记忆文件 |
| `load_focal_active` | bool | true | 加载热存储记忆 |
| `token_limit` | int | 8000 | Token 上限 |

---

## 使用方法

### 自动模式（推荐）

安装后自动生效，无需手动调用。

每次对话时：
1. 自动分类消息（4 种焦距模式）
2. 按需加载记忆文件
3. 判断是否需要写入新记忆
4. 自动写入（如需要）

### 手动模式

```python
from memory_manager import MemoryManager

manager = MemoryManager()

# 处理消息
context = manager.process_message("用户偏好早上 8 点起床")
print(context)
# {
#   "category": "memory",
#   "load_user": "...",
#   "load_memory": "...",
#   "load_focal": [...],
#   "should_write": true,
#   "token_count": 907
# }

# 写入记忆
manager.write_memory("用户明天考试", "已记录", "event", ["考试", "日程"])
```

### CLI 命令

```bash
cd ~/.openclaw/workspace/memory-focal

# 初始化
python3 scripts/cli.py init

# 添加记忆
python3 scripts/cli.py add "用户偏好早上 8 点起床" --type preference --tags 作息，偏好

# 搜索记忆
python3 scripts/cli.py search "作息"

# 查看统计
python3 scripts/cli.py stats

# 查看高优先级记忆
python3 scripts/cli.py top 5

# 分类测试
python3 scripts/cli.py classify "在吗"

# 生成标签
python3 scripts/cli.py tag "用户明天考试"

# 预览归档计划
python3 scripts/cli.py cleanup
```

---

## Token 优化效果

| 场景 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 简单对话 | 8000 tokens | 0 tokens | **100%** |
| 任务执行 | 8000 tokens | 2000-3000 tokens | **60-75%** |
| 情感/偏好 | 8000 tokens | 8000 tokens | 0% |
| 新信息 | 8000 tokens | 8000 tokens | 0% |

**综合节省：40-60%**（取决于对话类型分布）

---

## 文件结构

```
memory-focal-system/
├── SKILL.md                  # 技能说明
├── README.md                 # 使用文档
├── _meta.json                # 元数据
├── config.json               # 配置文件
├── memory_manager.py         # 核心管理模块
└── classifier.py             # 消息分类器

memory-focal/                 # 记忆数据存储（独立目录）
├── config/config.json
├── data/raw/buffer.jsonl
├── data/index/
│   ├── tag_index.json
│   └── memory_index.json
├── storage/
│   ├── active/
│   ├── short_term/
│   ├── long_term/
│   └── archive/
└── scripts/
    ├── cli.py
    ├── classifier.py
    ├── frequency_trigger.py
    ├── storage_manager.py
    ├── auto_tag.py
    └── forget_curve.py
```

---

## 记忆数据格式

### 单条记忆（buffer.jsonl）

```json
{
  "id": "mem_0001",
  "text": "用户偏好早上 8 点起床",
  "type": "preference",
  "tags": ["作息", "偏好"],
  "timestamp": "2026-03-29T08:00:00+08:00",
  "created_at": "2026-03-29T08:00:00+08:00",
  "access_count": 0,
  "last_accessed": null,
  "importance": 1.0,
  "layer": "active",
  "priority": 0.0
}
```

### 标签索引（tag_index.json）

```json
{
  "version": "1.0.0",
  "tags": {
    "作息": ["mem_0001", "mem_0002"],
    "偏好": ["mem_0001"]
  }
}
```

---

## 高级功能

### LLM 自动标签

需要配置 dashscope API key：

```bash
python3 scripts/cli.py tag "用户明天考试" --api-key <your-api-key>
```

缓存机制：
- 基于 MD5 哈希缓存
- 相同文本不重复调用
- 查看缓存：`python3 scripts/cli.py tag-stats`
- 清空缓存：`python3 scripts/cli.py tag-clear`

### 频率触发

基于访问次数、最后访问时间、重要性计算优先级：

```python
from frequency_trigger import FrequencyTrigger

trigger = FrequencyTrigger()
priority = trigger.calculate_priority(memory)
```

### 遗忘曲线

艾宾浩斯遗忘曲线算法：

```python
from forget_curve import ForgetCurve

curve = ForgetCurve()
strength = curve.calculate_strength(memory)
schedule = curve.get_archive_schedule(memories)
```

---

## 注意事项

1. **首次使用需要初始化**
   ```bash
   python3 scripts/cli.py init
   ```

2. **LLM 自动标签需要 API key**
   - 成本约 ¥0.5-10/月
   - 可手动关闭：`config.json` 中设置 `"auto_tag": false`

3. **Python 版本要求**
   - 核心功能：Python 3.6+
   - LLM 标签：Python 3.7+（需要 f-string 增强）

4. **备份建议**
   - 定期备份 `data/raw/buffer.jsonl`

---

## 故障排除

### 问题 1：分类不准确

**解决：** 编辑 `classifier.py`，调整关键词列表

```python
# 添加新的关键词
self.simple_keywords.append("新关键词")
```

### 问题 2：记忆写入失败

**解决：** 检查 CLI 路径和权限

```bash
ls -la ~/.openclaw/workspace/memory-focal/scripts/cli.py
chmod +x ~/.openclaw/workspace/memory-focal/scripts/cli.py
```

### 问题 3：Token 超限

**解决：** 降低 `token_limit` 或减少加载的记忆文件

```json
{
  "token_limit": 4000,
  "load_focal_active": false
}
```

---

## 更新日志

### v1.0.0 (2026-03-29)
- ✅ 焦距记忆机制（4 种模式）
- ✅ 频率触发机制
- ✅ 记忆分层管理
- ✅ LLM 自动标签
- ✅ 遗忘曲线
- ✅ 双链索引
- ✅ 增量式存储
- ✅ CLI 工具（add/search/list/stats/top/tag/cleanup/classify）

---

## 反馈

- 问题反馈：GitHub Issues
- 技能更新：`clawhub sync memory-focal-system`
- 技能评分：`clawhub star memory-focal-system`

---

_焦距记忆系统 - 让 AI 记住重要的事，忘记不重要的事_
