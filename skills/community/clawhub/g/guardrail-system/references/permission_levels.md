# 权限分级表 (Permission Levels)

工具护栏采用三级权限控制：READ（读）、WRITE（写）、DANGEROUS（危险）。

---

## 权限级别说明

| 级别 | 行为 | 触发条件 |
|------|------|----------|
| **READ** | 自动批准，无需用户干预 | 只读操作，不修改任何状态 |
| **WRITE** | 需要用户确认 | 创建/修改文件、数据等 |
| **DANGEROUS** | 需要明确授权 | 删除、执行命令、不可逆操作 |

---

## READ 工具列表

读操作工具，自动批准：

| 工具名 | 说明 |
|--------|------|
| `read` | 读取文件内容 |
| `read_file` | 读取文件 |
| `list` | 列出目录内容 |
| `list_files` | 列出文件 |
| `search` | 搜索内容 |
| `grep_search` | 正则搜索 |
| `search_code` | 代码搜索 |
| `get_file_info` | 获取文件信息 |
| `web_search` | 网络搜索 |
| `fetch_url` | 获取URL内容 |
| `get_status` | 获取状态 |
| `query` | 查询操作 |

**特征**: 不修改系统状态，不创建/删除文件，不执行代码。

---

## WRITE 工具列表

写操作工具，需要用户确认：

| 工具名 | 说明 |
|--------|------|
| `write` | 写入文件 |
| `write_file` | 写入文件 |
| `edit` | 编辑文件 |
| `edit_file` | 编辑文件 |
| `create` | 创建文件/目录 |
| `create_file` | 创建文件 |
| `update_file` | 更新文件 |
| `append_file` | 追加文件 |
| `modify` | 修改文件 |
| `save` | 保存操作 |
| `execute_code` | 执行代码（安全沙箱） |

**特征**: 创建或修改文件/数据，但通常是可逆的。

---

## DANGEROUS 工具列表

危险操作工具，需要明确授权：

| 工具名 | 说明 |
|--------|------|
| `rm` | 删除文件/目录 |
| `delete` | 删除操作 |
| `remove` | 移除操作 |
| `delete_file` | 删除文件 |
| `execute_shell` | 执行Shell命令 |
| `shell` | Shell操作 |
| `exec` | 执行命令 |
| `system` | 系统命令 |
| `run_command` | 运行命令 |
| `format` | 格式化操作 |
| `format_disk` | 格式化磁盘 |
| `drop_table` | 删除数据库表 |

**特征**: 不可逆操作、系统级命令、可能导致数据丢失。

---

## 权限检查流程

```
工具调用请求
    │
    ▼
┌─────────────────┐
│ 查询权限级别     │
└─────────────────┘
    │
    ├── READ ──► 自动批准 ✓
    │
    ├── WRITE ──► 弹出确认对话框
    │              │
    │              ├── 用户确认 ──► 执行 ✓
    │              └── 用户取消 ──► 拒绝 ✗
    │
    └── DANGEROUS ──► 需要明确授权
                     │
                     ├── 已授权 ──► 执行 ✓
                     └── 未授权 ──► 拒绝 ✗
```

---

## 动态添加工具

```python
from tool_guard import ToolGuard, PermissionLevel

guard = ToolGuard()

# 添加自定义工具
guard.add_tool("my_read_tool", PermissionLevel.READ)
guard.add_tool("my_write_tool", PermissionLevel.WRITE)
guard.add_tool("my_dangerous_tool", PermissionLevel.DANGEROUS)
```

---

## 未知工具处理

未在权限列表中的工具，默认归类为 **WRITE** 级别（需要确认）。

这是安全优先的设计：宁可多问一次，不可误放危险操作。

---

## 与 hook-engine 集成

```python
# PreToolUse Hook
def pre_tool_use_hook(tool_name, params):
    result = tool_guard.check(tool_name, params)

    if result.requires_authorization:
        # 危险操作，需要明确授权
        if not is_authorized(tool_name):
            return Block(reason=result.message)

    if result.requires_confirmation:
        # 写操作，需要用户确认
        if not user_confirmed(result.message):
            return Block(reason="用户取消")

    return Allow()
```
