# Memory Orchestrator

一个为 OpenClaw 设计的**白盒记忆系统原型**。

## 先看这个：怎么触发记忆

为了控制 token 成本，这套系统默认不靠大规模正则猜测，而是优先使用**显式触发词**和 **`/` 命令**。

### 写入记忆触发词
- 记住
- 以后
- 默认
- 不要
- 改成
- 更新记忆
- 写进记忆
- 记一下

### 召回记忆触发词
- 上次
- 之前
- 还记得
- 继续
- 回到
- 沿用
- 翻一下记忆
- 查一下记忆

### 整理记忆触发词
- 整理记忆
- 反思记忆
- 压缩记忆
- 更新主题卡
- 重整记忆

### `/` 命令
- `/remember`：强制写记忆
- `/recall`：强制召回记忆
- `/reflect`：强制整理记忆
- `/memory`：查看记忆相关信息
- `/topic`：新建或更新主题卡
- `/object`：新建或更新对象卡

## 设计目标

它的目标不是把一堆聊天记录偷偷塞进黑盒，而是让你和代理都能清楚看到：

- 记忆存在哪里
- 为什么某条信息会被记住
- 当前系统正在关注哪些主题
- 代理是通过什么线索召回过往内容的

## 面向后续开发

如果你是未来继续迭代这个 skill 的人，建议按这个顺序看：

1. `README.md` —— 怎么用
2. `ARCHITECTURE.md` —— 为什么这么设计
3. `ROADMAP.md` —— 当前阶段与后续边界
4. `references/object-models.md` —— 数据结构
5. `EXAMPLES.md` —— 输入输出示例
6. `scripts/` —— 具体执行逻辑

## 你可以直接看的目录

默认记忆根目录：`memory/`

重点看这些：

- `memory/session-state.yaml`  
  当前会话正在激活的主题、对象、约束

- `memory/daily/YYYY-MM-DD.md`  
  每天记录的重要交互、偏好更新、决策和纠正

- `memory/topics/*.yaml`  
  主题索引卡，比如技术、科研、职业、投资、meta

- `memory/objects/`  
  长期知识对象，如论文、框架、偏好、决策、开放问题

- `memory/reflections/YYYY-MM-DD.md`  
  反思整理结果：哪些记忆被提升、合并、降权

- `memory/indexes/README.md` / `memory/indexes/manifest.json`  
  人类可读索引与机器可读清单

## 设计原则

1. **summary-first**  
   先看主题摘要和对象摘要，再决定要不要深入。

2. **分层记忆**  
   会话态、日记账、主题卡、对象卡、反思层分开。

3. **白盒可检查**  
   尽量使用 Markdown / YAML / JSON，不引入黑盒数据库。

4. **可整理**  
   记忆不是只追加；允许反思、合并、重命名、降权。

5. **默认有结构，但不把主题写死**  
   `technology / career / investing / research / life / meta` 只是初始种子，不是封闭本体。后续可以继续加主题，也可以扩对象类型。

## 常用脚本

### 1. 输入分类

```bash
python3 skills/memory-orchestrator/scripts/classify_memory_input.py <<'EOF'
我想继续上次关于论文方法比较的话题
EOF
```

### 2. 提取记忆事件

```bash
python3 skills/memory-orchestrator/scripts/extract_memory_events.py <<'EOF'
以后长文用飞书文档，日报没内容就不要硬写。
EOF
```

### 3. 应用事件到记忆

```bash
python3 skills/memory-orchestrator/scripts/extract_memory_events.py <<'EOF' > /tmp/events.json
以后长文用飞书文档，日报没内容就不要硬写。
EOF
python3 skills/memory-orchestrator/scripts/apply_memory_events.py < /tmp/events.json
```

### 4. 召回相关记忆

```bash
python3 skills/memory-orchestrator/scripts/recall_memory.py <<'EOF'
记忆系统 技术方案 openclaw
EOF
```

### 5. 生成反思

```bash
python3 skills/memory-orchestrator/scripts/reflect_memory.py
```

### 6. 生成人类可读索引

```bash
python3 skills/memory-orchestrator/scripts/generate_memory_index.py
```

### 7. 创建新对象

```bash
python3 skills/memory-orchestrator/scripts/new_memory_object.py \
  --type paper \
  --domain research \
  --slug constitutional-ai \
  --title "Constitutional AI"
```

### 8. 创建新主题

```bash
python3 skills/memory-orchestrator/scripts/new_topic_card.py \
  --slug entrepreneurship \
  --title "创业 / 商业模式" \
  --summary "当用户开始反复讨论创业、商业模式、产品验证时，用这个主题做路由。"
```

### 9. 用统一 CLI 管理

```bash
python3 skills/memory-orchestrator/scripts/memory_cli.py bootstrap
python3 skills/memory-orchestrator/scripts/memory_cli.py capture "以后关于记忆系统实现细节，优先给我白盒方案"
python3 skills/memory-orchestrator/scripts/memory_cli.py recall "论文 方法 对比"
python3 skills/memory-orchestrator/scripts/memory_cli.py reflect
```

### 10. 低成本 gate / turn 模式

这是更推荐的运行方式，用来控制 token 成本。

先做 gate 判断：

```bash
python3 skills/memory-orchestrator/scripts/memory_cli.py gate "ok"
python3 skills/memory-orchestrator/scripts/memory_cli.py gate "你还记得我上次说的日报要求吗"
```

再用 `turn` 执行条件触发：

```bash
python3 skills/memory-orchestrator/scripts/memory_cli.py turn "你还记得我上次说的日报要求吗"
```

`turn` 的逻辑是：
- 先用 gate 判断这条消息值不值得处理
- 只在命中时才 recall / write
- 普通轻消息直接跳过

## 对用户最重要的一点

如果你怀疑“它到底记住了什么”，不要猜，直接看：

- `memory/topics/`
- `memory/objects/`
- `memory/daily/`
- `memory/indexes/README.md`

这套系统就是故意做成能被你检查、质疑、修改的。

## 当前状态

这是一个**可用原型**，已经能：

- 写入会话态和日记账
- 按主题/对象做 summary-first 召回
- 生成反思文件
- 生成可读索引
- 用模板新增对象

还没做的更高级功能：

- 更强的语义召回
- 自动关系推断增强
- 更细粒度的对象更新合并策略
- 真正无缝接入每轮会话自动触发
