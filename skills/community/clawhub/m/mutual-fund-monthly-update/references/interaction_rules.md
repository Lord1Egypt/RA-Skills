# 交互规则

## 问题场景

用户在聊天框中一个一个发送文件，AI如何知道用户是否发完了？

---

## 解决方案

### 方案1：用户明确确认（推荐）

**规则：用户发送完所有文件后，说"好了"或"开始处理"**

```
用户：[发送模板.xlsx]
AI：收到：模板.xlsx（等待更多文件...）

用户：[发送汇丰10月.pdf]
AI：收到：汇丰10月.pdf（等待更多文件...）

用户：[发送汇丰11月.pdf]
AI：收到：汇丰11月.pdf（等待更多文件...）

用户：[发送汇丰12月.pdf]
AI：收到：汇丰12月.pdf（等待更多文件...）

用户：好了
AI：收到4个文件，开始处理...
    [提取数据 → 生成Excel]
```

**触发词：**
- "好了"
- "开始处理"
- "处理"
- "可以开始了"
- "文件发完了"

---

### 方案2：超时自动开始（备选）

**规则：如果用户超过30秒没有发送新文件，自动开始处理**

```
用户：[发送模板.xlsx]
AI：收到：模板.xlsx（等待更多文件...）

用户：[发送汇丰10月.pdf]
AI：收到：汇丰10月.pdf（等待更多文件...）

... 用户超过30秒没有发送新文件 ...

AI：未收到新文件，开始处理...
    [提取数据 → 生成Excel]
```

**超时设置：**
- 默认超时：30秒
- 可配置超时：60秒、90秒

---

### 方案3：AI主动询问（兜底）

**规则：如果AI不确定用户是否发完，主动询问**

```
用户：[发送模板.xlsx]
AI：收到：模板.xlsx

用户：[发送汇丰10月.pdf]
AI：收到：汇丰10月.pdf

... 等待10秒 ...

AI：您还有其他文件要发送吗？如果没有，请说"好了"，我开始处理。
```

---

## AI执行逻辑

### 判断规则

```python
def should_start_processing(user_message, time_since_last_file):
    """判断是否应该开始处理"""
    
    # 规则1：用户明确确认
    if user_message in ["好了", "开始处理", "处理", "可以开始了", "文件发完了"]:
        return True
    
    # 规则2：超时自动开始
    if time_since_last_file > 30:  # 30秒超时
        return True
    
    # 规则3：用户发送了非文件消息（可能是确认）
    if not is_file_message(user_message):
        return True
    
    # 否则，继续等待
    return False


def process_incoming_files(files_received, user_message):
    """处理接收到的文件"""
    
    # 添加文件到列表
    files_received.append(user_message)
    
    # 回复确认
    filename = get_filename(user_message)
    reply(f"收到：{filename}（等待更多文件...）")
    
    # 不立即处理，等待用户确认或超时
    return files_received
```

---

## 实现细节

### 文件接收流程

```
步骤1：用户发送文件
    ↓
步骤2：AI识别文件类型（PDF/Excel）
    ↓
步骤3：AI回复确认收到
    ↓
步骤4：AI等待
    ├─ 用户发送更多文件 → 回到步骤1
    ├─ 用户说"好了" → 开始处理
    ├─ 超过30秒 → 开始处理
    └─ 用户发送其他消息 → 询问确认
```

### 状态管理

```python
# 会话状态
session_state = {
    "files_received": [],  # 已接收的文件列表
    "last_file_time": None,  # 最后一个文件的时间
    "is_waiting": True,  # 是否在等待更多文件
    "user_confirmed": False  # 用户是否确认
}
```

---

## 用户体验优化

### 清晰的提示

**文件接收时：**
```
AI：✅ 收到：汇丰10月.pdf
    📁 已接收：1个文件
    💡 发送更多文件，或说"好了"开始处理
```

**用户确认时：**
```
AI：收到确认！
    📁 总计：4个文件
    🚀 开始处理...
```

**处理完成时：**
```
AI：✅ 处理完成！
    📊 生成Excel：2个文件
    [发送Excel文件]
```

---

## 错误处理

### 情况1：用户忘记确认

```
用户：[发送文件1]
用户：[发送文件2]
... 用户忘记说"好了" ...

AI：您还有其他文件要发送吗？
    如果没有，请说"好了"，我开始处理。
```

### 情况2：用户中途离开

```
用户：[发送文件1]
... 用户离开很长时间 ...

AI：超过30秒未收到新文件，开始处理...
    📁 已接收：1个文件
```

### 情况3：用户误操作

```
用户：[发送文件1]
用户：[发送文件2]
用户：算了，重新发
AI：好的，已清空文件列表。
    请重新发送文件。
```

---

## 推荐流程（最佳实践）

```
用户操作：
1. 发送Excel模板（如果有）
2. 发送PDF文件（一个或多个）
3. 说"好了"或"开始处理"

AI响应：
1. 收到每个文件时，回复"收到：xxx（等待更多文件...）"
2. 收到确认后，回复"收到确认！总计：N个文件，开始处理..."
3. 处理完成后，发送生成的Excel文件
```

---

## 代码示例

```python
class FileProcessor:
    def __init__(self):
        self.files = []
        self.last_file_time = None
        self.timeout = 30  # 秒
    
    def add_file(self, file_path):
        """添加文件"""
        self.files.append(file_path)
        self.last_file_time = time.time()
        return f"✅ 收到：{os.path.basename(file_path)}\n📁 已接收：{len(self.files)}个文件\n💡 发送更多文件，或说"好了"开始处理"
    
    def should_start(self, user_message):
        """判断是否应该开始处理"""
        # 用户确认
        if user_message.strip() in ["好了", "开始处理", "处理"]:
            return True
        
        # 超时
        if self.last_file_time and time.time() - self.last_file_time > self.timeout:
            return True
        
        return False
    
    def process(self):
        """开始处理"""
        result = f"收到确认！\n📁 总计：{len(self.files)}个文件\n🚀 开始处理..."
        
        # 提取数据、生成Excel
        # ...
        
        return result
```

---

## 总结

**推荐方案：用户明确确认 + 超时自动开始**

1. **用户明确确认**：发送完所有文件后，说"好了"或"开始处理"
2. **超时自动开始**：如果用户超过30秒没有发送新文件，自动开始处理
3. **AI主动询问**：如果AI不确定，主动询问用户是否发完了

**避免的问题：**
- ✅ 不会在中途就开始处理
- ✅ 不会遗漏文件
- ✅ 用户体验清晰明确
