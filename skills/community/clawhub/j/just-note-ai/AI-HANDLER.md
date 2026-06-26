# AI 消息处理指南

**适用场景**: 用户通过微信/飞书发送消息给 OpenClaw，AI 自动处理并调用 just-note 保存。

---

## 一、处理流程

```
用户消息 → AI 接收 → 理解分类 → 调用 CLI → 保存完成
```

---

## 二、分类规则

### 类型识别（9 选 1）

| 类型 | 关键词/特征 | 示例 |
|------|------------|------|
| **inspiration** | 灵感、创意、想法、建议 | 「这个功能可以这样做...」 |
| **idea** | 想法、心得、感悟 | 「今天读到...」 |
| **knowledge** | 知识点、解释、原理 | 「Python 的装饰器是...」 |
| **expense** | 金额、花了、买了、支出 | 「花了 200 块买书」 |
| **income** | 收入、收到、赚了、稿费 | 「收到稿费 5000」 |
| **diary** | 今天、遇到、感受、心情 | 「今天遇到了...」 |
| **task** | 记得、要、待办、下周 | 「记得下周约医生」 |
| **quote** | 引用、说、名言 | 「XXX 说：...」 |
| **other** | 无法分类的内容 | 「测试一下」 |

### 标签生成规则

- **数量**: 3-5 个
- **格式**: 简洁、有意义、小写
- **示例**: `[product, ai, automation]`

### 标题生成规则

- **长度**: 10-20 字
- **内容**: 概括核心内容
- **示例**: 「产品自动化分类功能灵感」

### 金额提取规则

**expense/income 类型需要提取**:

| 输入 | amount | currency |
|------|--------|----------|
| 「花了 200 块」 | 200 | CNY |
| 「收到¥5000」 | 5000 | CNY |
| 「花了$50」 | 50 | USD |
| 「买了个东西」 | null | null |

---

## 三、处理示例

### 示例 1: 灵感

**用户消息**:
```
这个产品功能可以这样做：用户发消息后，AI 自动分类并存入知识库，比手动标签简单多了
```

**AI 处理**:
```json
{
  "type": "inspiration",
  "title": "产品自动化分类功能灵感",
  "tags": ["product", "ai", "automation"],
  "amount": null,
  "currency": null,
  "observations": ["用户发消息后 AI 自动分类", "比手动标签简单"]
}
```

**AI 调用 CLI**:
```bash
just-note write --type inspiration --content "这个产品功能可以这样做..." --title "产品自动化分类功能灵感" --tags "product,ai,automation"
```

---

### 示例 2: 支出

**用户消息**:
```
花了 200 块买书
```

**AI 处理**:
```json
{
  "type": "expense",
  "title": "买书支出¥200",
  "tags": ["book", "learning"],
  "amount": 200,
  "currency": CNY,
  "observations": ["买书"]
}
```

**AI 调用 CLI**:
```bash
just-note write --type expense --content "花了 200 块买书" --title "买书支出¥200" --tags "book,learning" --amount 200 --currency CNY
```

---

### 示例 3: 收入

**用户消息**:
```
收到稿费 5000 元
```

**AI 处理**:
```json
{
  "type": "income",
  "title": "收到稿费¥5000",
  "tags": ["freelance", "writing"],
  "amount": 5000,
  "currency": CNY,
  "observations": ["稿费收入"]
}
```

**AI 调用 CLI**:
```bash
just-note write --type income --content "收到稿费 5000 元" --title "收到稿费¥5000" --tags "freelance,writing" --amount 5000 --currency CNY
```

---

### 示例 4: 知识

**用户消息**:
```
Python 的装饰器原理是在不修改原函数的情况下，通过函数包装器增强功能
```

**AI 处理**:
```json
{
  "type": "knowledge",
  "title": "Python 装饰器原理",
  "tags": ["python", "decorator", "programming"],
  "amount": null,
  "currency": null,
  "observations": ["装饰器是函数包装器", "不修改原函数增强功能"]
}
```

**AI 调用 CLI**:
```bash
just-note write --type knowledge --content "Python 的装饰器原理是..." --title "Python 装饰器原理" --tags "python,decorator,programming"
```

---

### 示例 5: 任务

**用户消息**:
```
记得下周三前完成产品原型设计
```

**AI 处理**:
```json
{
  "type": "task",
  "title": "下周三前完成产品原型设计",
  "tags": ["task", "product", "deadline"],
  "amount": null,
  "currency": null,
  "observations": ["截止日期：下周三", "任务：产品原型设计"]
}
```

**AI 调用 CLI**:
```bash
just-note write --type task --content "记得下周三前完成产品原型设计" --title "下周三前完成产品原型设计" --tags "task,product,deadline"
```

---

### 示例 6: 日记

**用户消息**:
```
今天遇到了一个有趣的人，聊得很开心
```

**AI 处理**:
```json
{
  "type": "diary",
  "title": "今天遇到有趣的人",
  "tags": ["diary", "social", "mood-good"],
  "amount": null,
  "currency": null,
  "observations": ["遇到有趣的人", "聊得很开心"]
}
```

**AI 调用 CLI**:
```bash
just-note write --type diary --content "今天遇到了一个有趣的人..." --title "今天遇到有趣的人" --tags "diary,social,mood-good"
```

---

## 四、特殊情况处理

### 4.1 多条内容混合

**用户消息**:
```
花了 200 块买书，还学到了 Python 装饰器的知识
```

**AI 处理**: 拆分为两条记录

```bash
# 记录 1：支出
just-note write --type expense --content "花了 200 块买书" --title "买书支出¥200" --tags "book,learning" --amount 200

# 记录 2：知识
just-note write --type knowledge --content "学到了 Python 装饰器的知识" --title "Python 装饰器学习" --tags "python,decorator"
```

---

### 4.2 内容不明确

**用户消息**:
```
测试一下
```

**AI 处理**: 归类为 other

```bash
just-note write --type other --content "测试一下" --title "测试" --tags "test"
```

---

### 4.3 金额不明确

**用户消息**:
```
买了个东西
```

**AI 处理**: amount=null

```bash
just-note write --type expense --content "买了个东西" --title "购物" --tags "shopping"
```

---

## 五、响应格式

### 成功响应

```
✅ 记录已保存

类型：inspiration
标题：产品自动化分类功能灵感
标签：product, ai, automation
```

### 失败响应

```
❌ 记录失败

原因：[具体原因]
建议：[解决建议]
```

---

## 六、最佳实践

### 1. 及时响应

用户发消息后，AI 应在 3 秒内响应。

### 2. 确认信息

响应中应包含：
- 类型
- 标题
- 标签（如果是收支，包含金额）

### 3. 允许修正

如果 AI 分类错误，用户可以说「不对，这是 xxx」，AI 应重新分类。

### 4. 主动建议

如果用户连续记录多条同类内容，AI 可以主动建议：
```
检测到您今天记录了 3 条支出，需要查看今日支出汇总吗？
```

---

## 七、与 CLI 的配合

### AI 的职责

1. 理解用户消息
2. 分类、生成标签、提取金额
3. 调用 CLI 写入文件
4. 返回确认信息

### CLI 的职责

1. 接收明确参数
2. 写入文件
3. 返回执行结果

**CLI 不做任何分类/理解**。

---

## 八、持续改进

### 记录误判案例

当 AI 分类错误时，记录案例用于改进：

```markdown
## 误判案例

**用户消息**: 「花了 3 小时学习 Python」
**AI 误判**: expense (因为「花了」)
**正确类型**: knowledge
**改进**: 「花了 + 时间」不是支出
```

### 定期回顾

每周回顾误判案例，优化分类规则。

---

> **核心原则**: AI 做大脑（理解/分类），CLI 做手脚（执行）
