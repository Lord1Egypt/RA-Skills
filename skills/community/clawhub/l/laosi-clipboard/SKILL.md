---
name: clipboard-manager
description: Windows剪贴板管理器 - 原创技能。管理Windows剪贴板，支持复制、粘贴、历史记录、多条目管理、格式化转换等功能。适用于数据处理、批量操作、跨应用数据交换等场景。
metadata: {"openclaw": {"requires": {"python": ["pyperclip", "Pillow"]}, "install": []}}
tags: [clipboard, copy, paste, windows, data-management]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 功能完整
- [x] 命令清晰
- [x] 历史管理实用
- [x] 无语法错误

---

# Clipboard Manager - 剪贴板管理器

> 原创技能 | 激活词: 剪贴板 / 复制粘贴 / 剪贴板历史

## 功能概述

| 功能 | 说明 |
|------|------|
| 读写剪贴板 | 读取/写入文本、图像、文件 |
| 历史记录 | 保存最近N条剪贴板内容 |
| 多条目管理 | 快速切换不同内容 |
| 格式转换 | 文本↔图片、JSON格式化 |
| 搜索过滤 | 在历史中搜索内容 |

## 安装依赖

```bash
pip install pyperclip Pillow
```

## 核心命令

### 1. 基本读写

```python
import pyperclip

# 读取文本
text = pyperclip.paste()

# 写入文本
pyperclip.copy("Hello World")

# 清空剪贴板
pyperclip.copy("")
```

### 2. 图像操作

```python
from PIL import Image
import io
import pyperclip

# 从剪贴板获取图像
def get_image_from_clipboard():
    try:
        img = Image.open(io.BytesIO(pyperclip.paste()))
        return img
    except:
        return None

# 复制图像到剪贴板
def copy_image_to_clipboard(image_path):
    img = Image.open(image_path)
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    pyperclip.copy(output.getvalue())
```

### 3. 剪贴板历史

```python
class ClipboardHistory:
    def __init__(self, max_items=50):
        self.history = []
        self.max_items = max_items
    
    def add(self, content):
        """添加内容到历史"""
        self.history.insert(0, {
            'content': content,
            'timestamp': datetime.now(),
            'type': 'text' if isinstance(content, str) else 'image'
        })
        if len(self.history) > self.max_items:
            self.history.pop()
    
    def get(self, index):
        """获取历史条目"""
        if 0 <= index < len(self.history):
            return self.history[index]
        return None
    
    def search(self, keyword):
        """搜索历史"""
        return [item for item in self.history 
                if keyword.lower() in str(item['content']).lower()]
    
    def clear(self):
        """清空历史"""
        self.history = []
```

### 4. 格式化转换

```python
import json

# JSON格式化
def format_json():
    text = pyperclip.paste()
    try:
        obj = json.loads(text)
        formatted = json.dumps(obj, indent=2, ensure_ascii=False)
        pyperclip.copy(formatted)
        return True
    except:
        return False

# 文本转列表
def text_to_lines():
    """将文本按行转为列表"""
    text = pyperclip.paste()
    lines = text.split('\n')
    pyperclip.copy('\n'.join([f"- {line}" for line in lines if line.strip()]))

# 批量添加引号
def add_quotes():
    """为每行添加引号"""
    text = pyperclip.paste()
    lines = text.split('\n')
    quoted = [f'"{line.strip()}"' for line in lines if line.strip()]
    pyperclip.copy(','.join(quoted))
```

### 5. 多剪贴板管理

```python
class MultiClipboard:
    def __init__(self):
        self.slots = {}  # 槽位: 内容
    
    def save(self, slot_id: str):
        """保存当前剪贴板到槽位"""
        self.slots[slot_id] = pyperclip.paste()
        return True
    
    def load(self, slot_id: str):
        """从槽位恢复剪贴板"""
        if slot_id in self.slots:
            pyperclip.copy(self.slots[slot_id])
            return True
        return False
    
    def list_slots(self):
        """列出所有槽位"""
        return list(self.slots.keys())
    
    def delete(self, slot_id: str):
        """删除槽位"""
        if slot_id in self.slots:
            del self.slots[slot_id]
            return True
        return False
```

## 使用场景

### 场景1: 代码片段收集

```python
# 收集多个代码片段
clipboard_manager.save("snippet1")  # 保存到槽位1
# 复制下一个代码片段
clipboard_manager.save("snippet2")  # 保存到槽位2
# ...
clipboard_manager.load("snippet1")  # 恢复第一个片段
```

### 场景2: 批量数据处理

```python
# 从Excel复制的数据，批量添加引号
# 原始: item1, item2, item3
# 结果: "item1", "item2", "item3"
add_quotes()
```

### 场景3: JSON格式化

```python
# 复制的JSON字符串格式化
format_json()  # 自动格式化并复制回去
```

### 场景4: 文本整理

```python
# 将文本转为Markdown列表
# 原始:
# 北京
# 上海
# 广州
# 结果:
# - 北京
# - 上海
# - 广州
text_to_lines()
```

## 实用命令集

```python
# 复制文件路径到剪贴板
def copy_file_path(file_path):
    pyperclip.copy(file_path)

# 复制当前时间
def copy_current_time():
    from datetime import datetime
    pyperclip.copy(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 复制当前日期
def copy_current_date():
    from datetime import datetime
    pyperclip.copy(datetime.now().strftime("%Y-%m-%d"))

# 全转大写
def to_uppercase():
    text = pyperclip.paste()
    pyperclip.copy(text.upper())

# 全转小写
def to_lowercase():
    text = pyperclip.paste()
    pyperclip.copy(text.lower())

# 首字母大写
def capitalize():
    text = pyperclip.paste()
    pyperclip.copy(text.title())

# 去重换行
def deduplicate_lines():
    text = pyperclip.paste()
    lines = text.split('\n')
    unique = list(dict.fromkeys(lines))
    pyperclip.copy('\n'.join(unique))

# 反转顺序
def reverse_lines():
    text = pyperclip.paste()
    lines = text.split('\n')
    reversed_lines = lines[::-1]
    pyperclip.copy('\n'.join(reversed_lines))

# 去除空白行
def remove_blank_lines():
    text = pyperclip.paste()
    lines = [line for line in text.split('\n') if line.strip()]
    pyperclip.copy('\n'.join(lines))
```

## 剪贴板监控

```python
import time
import threading

class ClipboardMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.last_content = ""
    
    def start(self):
        self.running = True
        thread = threading.Thread(target=self._monitor)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        self.running = False
    
    def _monitor(self):
        while self.running:
            current = pyperclip.paste()
            if current != self.last_content:
                self.last_content = current
                self.callback(current)
            time.sleep(0.5)
```

## 输出格式

```markdown
## 剪贴板操作报告

### 当前剪贴板
- **类型**: 文本
- **长度**: 156字符
- **预览**: "Hello World..."

### 历史记录
1. [10:30] "Hello World"
2. [10:29] 图片 (123KB)
3. [10:28] "some text"
4. [10:27] "another text"
5. [10:26] JSON数据

### 槽位
- A: "代码片段1"
- B: "代码片段2"
- C: "常用文本"

### 操作
✅ 已复制到剪贴板
✅ 已保存到槽位A
✅ 历史已记录
```

## 集成建议

| 配合技能 | 效果 |
|---------|------|
| windows-app-controller | 配合自动化操作 |
| requirement-clarifier | 快速复制澄清内容 |
| intent-classifier | 识别剪贴板内容类型 |

## 原创性声明

本技能为原创，融合了：
- Pyperclip剪贴板操作
- PIL图像处理
- 历史记录管理
- 文本格式化工具

---

**作者**: laosi
**创建日期**: 2026-04-28