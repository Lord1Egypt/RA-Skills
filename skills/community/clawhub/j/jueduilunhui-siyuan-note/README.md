# 思源笔记读写技能

这是一个为OpenClaw设计的思源笔记（SiYuan Note）读写技能，允许你轻松地查询和写入思源笔记内容。

## 功能特性

- ✅ **连接测试** - 测试思源笔记API连接
- ✅ **笔记本查询** - 获取所有笔记本列表
- ✅ **文档查询** - 获取笔记本中的文档
- ✅ **内容搜索** - 在思源笔记中搜索内容
- ✅ **对话同步** - 将OpenClaw对话同步到思源笔记
- ✅ **文档创建** - 创建新文档
- ✅ **配置管理** - 管理API连接配置

## 快速开始

### 1. 前置要求

确保满足以下条件：
1. 思源笔记正在运行
2. 思源笔记API已启用
3. 获取了有效的API token
4. Python环境已安装requests库

### 2. 安装依赖

```bash
pip install requests
```

### 3. 配置思源笔记

编辑配置文件 `/home/zero/.openclaw/workspace/siyuan-openchat-sync/config.json`：

```json
{
  "siyuan": {
    "api_url": "http://你的思源笔记地址:端口",
    "token": "你的思源笔记API token"
  },
  "sync": {
    "notebook_name": "其他",
    "document_name": "openchat",
    "auto_sync": true,
    "sync_interval_minutes": 5
  }
}
```

### 4. 在OpenClaw中使用

当你在OpenClaw会话中提到以下关键词时，此技能会自动激活：
- "查询思源笔记"
- "写入思源笔记" 
- "同步到思源笔记"
- "从思源笔记读取"

## 使用方法

### 基本查询

```python
# 在OpenClaw中
from skills.siyuan_note.siyuan_note import SiYuanNote

# 初始化
siyuan = SiYuanNote()

# 测试连接
if siyuan.test_connection():
    print("✅ 已连接到思源笔记")
    
# 获取笔记本
notebooks = siyuan.get_notebooks()
print(f"找到 {len(notebooks)} 个笔记本")

# 搜索内容
results = siyuan.search_content("关键词")
```

### 同步对话

```python
# 同步当前对话到思源笔记
conversation_data = {
    'summary': '对话摘要',
    'messages': [
        {'role': 'user', 'content': '用户消息'},
        {'role': 'assistant', 'content': '助手回复'}
    ],
    'conclusion': '对话总结'
}

success = siyuan.sync_conversation(conversation_data)
if success:
    print("✅ 对话已同步到思源笔记")
```

### 快速同步脚本

使用提供的快速同步脚本：

```bash
# 同步示例对话
python quick_sync.py --test

# 同步自定义内容
python quick_sync.py "这是要同步的内容"

# 从文件同步
python quick_sync.py --file conversation.txt
```

## API参考

### SiYuanNote类

#### 初始化
```python
siyuan = SiYuanNote(
    api_url="http://192.168.1.6:6811",  # 可选
    token="your_token",                 # 可选
    config_path="config.json"           # 可选
)
```

#### 主要方法

**连接相关**
- `test_connection()` - 测试API连接
- `get_notebooks()` - 获取所有笔记本
- `get_notebook_id(notebook_name)` - 获取笔记本ID

**读取操作**
- `get_documents(notebook_id)` - 获取笔记本中的文档
- `get_document_content(document_id)` - 获取文档内容
- `search_content(query, notebook_name=None)` - 搜索内容

**写入操作**
- `create_document(notebook_name, document_name, content)` - 创建新文档
- `append_to_document(document_id, content)` - 向文档追加内容
- `sync_conversation(conversation_data, notebook_name=None, document_name=None)` - 同步对话

**配置管理**
- `load_config()` - 加载配置
- `save_config()` - 保存配置
- `update_config(new_config)` - 更新配置

## 示例

### 示例1：完整查询流程

```python
from skills.siyuan_note.siyuan_note import SiYuanNote

siyuan = SiYuanNote()

# 1. 测试连接
if not siyuan.test_connection():
    print("❌ 连接失败")
    exit(1)

# 2. 获取笔记本
notebooks = siyuan.get_notebooks()
print(f"📚 找到 {len(notebooks)} 个笔记本")

# 3. 获取默认笔记本的文档
notebook_id = siyuan.get_notebook_id("其他")
if notebook_id:
    documents = siyuan.get_documents(notebook_id)
    print(f"📄 找到 {len(documents)} 个文档")

# 4. 搜索内容
results = siyuan.search_content("OpenChat")
if results:
    print(f"🔍 找到 {len(results)} 个相关结果")
```

### 示例2：自动同步对话

```python
import json
from datetime import datetime
from skills.siyuan_note.siyuan_note import SiYuanNote

def auto_sync_conversation(messages, summary=None):
    """自动同步对话到思源笔记"""
    siyuan = SiYuanNote()
    
    conversation_data = {
        'summary': summary or f"对话记录 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        'messages': messages,
        'conclusion': '对话已自动同步',
        'metadata': {
            'auto_sync': True,
            'timestamp': datetime.now().isoformat()
        }
    }
    
    return siyuan.sync_conversation(conversation_data)

# 使用示例
messages = [
    {'role': 'user', 'content': '你好'},
    {'role': 'assistant', 'content': '你好！有什么可以帮助你的？'}
]

success = auto_sync_conversation(messages, "问候对话")
print("同步结果:", "成功" if success else "失败")
```

## 故障排除

### 常见问题

1. **连接失败**
   ```
   ❌ 连接测试失败: Connection refused
   ```
   **解决方案：**
   - 检查思源笔记是否正在运行
   - 确认API地址和端口正确
   - 验证防火墙设置

2. **认证失败**
   ```
   ❌ 连接失败: 无效的token
   ```
   **解决方案：**
   - 检查API token是否正确
   - 在思源笔记中重新生成token
   - 更新配置文件中的token

3. **权限问题**
   ```
   ❌ 未找到笔记本: 其他
   ```
   **解决方案：**
   - 确认笔记本名称正确
   - 检查token是否有访问权限
   - 尝试使用其他笔记本名称

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from skills.siyuan_note.siyuan_note import SiYuanNote
siyuan = SiYuanNote()
siyuan.test_connection()
```

## 文件结构

```
siyuan-note/
├── SKILL.md              # 技能说明文档
├── siyuan_note.py        # 核心Python模块
├── example_usage.py      # 使用示例
├── quick_sync.py         # 快速同步脚本
├── test_skill.py         # 测试脚本
└── README.md            # 本文件
```

## 测试

运行完整测试：

```bash
python test_skill.py
```

运行特定测试：

```bash
# 测试基本功能
python -c "from test_skill import test_basic_functionality; test_basic_functionality()"

# 测试同步功能
python -c "from test_skill import test_sync_functionality; test_sync_functionality()"
```

## 更新日志

### v1.0.0
- 初始版本发布
- 基本读写功能
- 对话同步支持
- 配置管理

## 许可证

MIT License

## 支持

如有问题或建议，请：
1. 检查故障排除部分
2. 运行测试脚本诊断问题
3. 查看示例代码参考用法