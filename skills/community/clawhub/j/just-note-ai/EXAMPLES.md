# just-note 使用示例

## 示例 1: 记录灵感

**输入**:
```bash
just-note record "这个产品功能可以这样做：用户发消息后，AI 自动分类并存入知识库，比手动标签简单多了"
```

**输出**:
```
正在处理...
✓ 记录已保存：/memory/just-note/2026-03/2026-03-26-121556.md
  类型：inspiration
  标题：产品自动化分类功能灵感
  标签：product, ai, automation
```

**生成的文件**:
```markdown
---
title: "产品自动化分类功能灵感"
type: inspiration
created: 2026-03-26T12:15:56+08:00
day-id: 2026-03-26
tags: [product, ai, automation]
source: manual
---

# 产品自动化分类功能灵感

## 原始内容
这个产品功能可以这样做：用户发消息后，AI 自动分类并存入知识库，比手动标签简单多了

## AI 整理
- [insight] 用户发消息后 AI 自动分类
- [insight] 比手动标签简单

## 关联笔记
- relates_to [[待实现]]
```

---

## 示例 2: 记录支出

**输入**:
```bash
just-note record "花了 200 块买书"
```

**输出**:
```
正在处理...
✓ 记录已保存：/memory/just-note/2026-03/2026-03-26-121600.md
  类型：expense
  标题：买书支出¥200
  标签：book, learning
  金额：¥200
```

**生成的文件**:
```markdown
---
title: "买书支出¥200"
type: expense
created: 2026-03-26T12:16:00+08:00
day-id: 2026-03-26
tags: [book, learning]
source: manual
amount: 200
currency: CNY
---

# 买书支出¥200

## 原始内容
花了 200 块买书

## AI 整理
- [meta] 金额：¥200

## 关联笔记
- relates_to [[待实现]]
```

---

## 示例 3: 查看今日记录

**输入**:
```bash
just-note today
```

**输出**:
```
# 2026-03-26 日记

## 今日概览
共 2 条记录

- inspiration: 1 条
- expense: 1 条

## 详细记录

---
title: "产品自动化分类功能灵感"
type: inspiration
...

---

---
title: "买书支出¥200"
type: expense
...

---
```

---

## 示例 4: 搜索历史记录

**输入**:
```bash
just-note search "产品"
```

**输出**:
```
# 搜索结果：产品

- [inspiration] 产品自动化分类功能灵感 (2026-03-26T12:15:56+08:00)
  文件：/memory/just-note/2026-03/2026-03-26-121556.md
```

---

## 示例 5: 按类型筛选

**输入**:
```bash
just-note list --type expense
```

**输出**:
```
# 记录列表

- [expense] 买书支出¥200 (2026-03-26T12:16:00+08:00)
```

---

## 示例 6: 统计信息

**输入**:
```bash
just-note stats
```

**输出**:
```
# 统计信息

总记录数：2

按类型分布:
  inspiration     1 条
  expense         1 条

按月份分布:
  2026-03     2 条
```

---

## 示例 7: 快速记录

**输入**:
```bash
just-note quick "突然想到一个点子"
```

**输出**:
```
✓ 快速记录已保存：/memory/just-note/2026-03/2026-03-26-121700.md
```

**生成的文件**:
```markdown
---
title: "突然想到一个点子"
type: other
created: 2026-03-26T12:17:00+08:00
day-id: 2026-03-26
tags: [quick]
source: quick
---

# 快速记录

突然想到一个点子
```

---

## 真实场景示例

### 场景 1: 会议中快速记录

```bash
# 会议中想到一个点子
just-note quick "可以把 AI 分类做成可配置的，用户自定义规则"

# 听到一个重要数据
just-note record "Q1 营收增长 30%，主要来自新产品线"

# 记住一个待办
just-note record "下周三前完成产品原型设计"
```

### 场景 2: 日常收支记录

```bash
# 早餐
just-note record "早餐 15 元"

# 工资收入
just-note record "收到工资¥15000"

# 购物
just-note record "买了一件衬衫 300 元"
```

### 场景 3: 学习记录

```bash
# 学到新知识
just-note record "Python 装饰器的本质是函数包装器，可以在不修改原函数的情况下增强功能"

# 读书心得
just-note record "《深度工作》里说：专注能力是 21 世纪最稀缺的能力"
```

### 场景 4: 灵感捕捉

```bash
# 产品灵感
just-note record "可以做一个 AI 自动分类的笔记工具，比 flomo 更智能"

# 写作灵感
just-note record "文章开头可以用一个故事引入，增加可读性"
```

---

## 最佳实践

### 1. 及时记录

灵感来了立刻记，不要等：
```bash
just-note quick "突然想到的点子"
```

### 2. 不用整理

AI 会自动分类标签，你只需要记录：
```bash
# 好的：直接记录
just-note record "今天学到了 xxx"

# 不好的：自己加标签
just-note record "今天学到了 xxx #learning #knowledge"
```

### 3. 定期回顾

每天睡前查看今日记录：
```bash
just-note today
```

每周查看周报：
```bash
just-note weekly
```

### 4. 善用搜索

找特定内容用搜索：
```bash
just-note search "产品"
just-note search "#ai"
```

按类型筛选：
```bash
just-note list --type expense
```

---

## 下一步

1. **开始记录** - 试试 `just-note record "你的第一条记录"`
2. **查看帮助** - `just-note help`
3. **阅读文档** - 见 [SKILL.md](SKILL.md)
