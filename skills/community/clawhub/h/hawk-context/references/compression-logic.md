# 压缩算法详解 · Compression Logic

---

## 压缩流程

```
1. 解析对话历史
       ↓
2. 分离系统提示（永久保留）
       ↓
3. 分类消息（按重要度）
       ↓
4. 应用压缩策略
       ↓
5. 重组上下文
       ↓
6. 输出结构化JSON
```

---

## 第一步：解析对话历史

从当前上下文提取所有消息：

```python
def parse_history(messages):
    system_prompt = None
    dialog = []
    
    for msg in messages:
        if msg['role'] == 'system':
            system_prompt = msg['content']
        elif msg['role'] in ('user', 'assistant'):
            dialog.append({
                'role': msg['role'],
                'content': msg['content'],
                'tokens': estimate_tokens(msg['content'])
            })
    
    return system_prompt, dialog
```

---

## 第二步：重要度评分

```python
def score_importance(msg):
    content = msg['content'].lower()
    
    # 🔴 极高 — 保留原文
    if any(k in content for k in [
        '决定:', '规则:', '架构:', '任务:',
        '规范:', '禁止:', '必须:', '重要:'
    ]):
        return 1.0
    
    # 🟡 高 — 保留摘要
    if any(k in content for k in [
        '代码:', '方案:', '设计:', '实现:',
        '修改:', '新增:', '完成:'
    ]):
        return 0.7
    
    # 🟢 中 — 摘要或合并
    if any(k in content for k in [
        '讨论:', '对话:', '说了', '觉得'
    ]):
        return 0.4
    
    # ⚪ 低 — 直接丢弃
    if any(k in content for k in [
        '好的', '收到', 'ok', '嗯', '好',
        '请问', '谢谢', '抱歉', '对不起'
    ]):
        return 0.1
    
    return 0.5  # 默认中
```

---

## 第三步：应用压缩策略

### Light（轻度）

```python
def compress_light(dialog, keep_recent=10):
    # 保留最近10轮完整
    recent = dialog[-keep_recent:]
    # 其余全部摘要
    summarized = [summarize(msg) for msg in dialog[:-keep_recent]]
    return recent + summarized
```

### Normal（标准，默认）

```python
def compress_normal(dialog, keep_recent=10):
    recent = dialog[-keep_recent:]
    older = dialog[:-keep_recent]
    
    # 分组：按时间段/主题聚合
    groups = group_by_topic(older)
    
    summarized = []
    for group in groups:
        if len(group) > 3:
            summarized.append(summarize_group(group))
        else:
            summarized.extend([summarize(m) for m in group])
    
    return recent + summarized
```

### Heavy（重度）

```python
def compress_heavy(dialog, keep_recent=5):
    recent = dialog[-keep_recent:]
    older = summarize_all(dialog[:-keep_recent])
    return recent + [older]
```

### Emergency（紧急）

```python
def compress_emergency(dialog, keep_recent=3):
    return dialog[-keep_recent:]
```

---

## 第四步：摘要生成

```python
def summarize(msg):
    content = msg['content']
    tokens = msg['tokens']
    
    # 原文 < 200 tokens → 直接保留
    if tokens < 200:
        return msg
    
    # 代码片段 → 折叠
    if '```' in content:
        return {
            'role': msg['role'],
            'content': f"[代码折叠: {count_lines(content)}行]",
            'tokens': 15
        }
    
    # 长文本 → 提取核心句子
    sentences = content.split('。')
    core = sentences[:2] if len(sentences) > 2 else sentences
    
    return {
        'role': msg['role'],
        'content': '。'.join(core) + '。',
        'tokens': estimate_tokens('。'.join(core))
    }
```

---

## 第五步：输出结构化 JSON

```json
{
  "compressed_prompt": "...",
  "original_tokens": 180000,
  "compressed_tokens": 32000,
  "ratio": "5.6x",
  "kept_messages": 5,
  "summarized_count": 87,
  "dropped_count": 12,
  "compression_level": "normal",
  "system_prompt_preserved": true,
  "timestamp": "2026-03-29T00:39:00+08:00",
  "messages": [
    {"role": "system", "content": "...", "tokens": 500},
    {"role": "user", "content": "最新问题...", "tokens": 80},
    {"role": "assistant", "content": "最新回答...", "tokens": 200}
  ]
}
```

---

## Token 估算

```python
def estimate_tokens(text):
    # 粗略估算：中文 ~1.5字/token，英文 ~4字/token
    chinese = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
    english = len([c for c in text if c.isascii()])
    return int(chinese / 1.5 + english / 4)
```

---

## 合并重复消息

```python
def merge_duplicates(dialog):
    merged = []
    for msg in dialog:
        if merged and msg['role'] == merged[-1]['role']:
            # 连续同角色消息
            if is_confirmation(msg['content']):
                continue  # 跳过确认
            if similarity(msg['content'], merged[-1]['content']) > 0.8:
                # 高度相似 → 合并
                merged[-1]['content'] += f"\n[另]: {msg['content']}"
                continue
        merged.append(msg)
    return merged
```
