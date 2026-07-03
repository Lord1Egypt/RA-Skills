# KingDoc 安全设计

> 本文档定义 KingDoc Skill 的多层安全防御模型。

---

## 1. 安全架构总览

```
┌──────────────────────────────────────────────────┐
│               第 1 层：用户确认层                  │
│  - 删除/覆盖/批量操作必须用户显式确认              │
│  - 可配置安全模式：始终确认 / 仅危险操作确认       │
└──────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────┐
│               第 2 层：权限前置校验层              │
│  - 所有写入操作前自动检查用户权限                  │
│  - 无权限直接拒绝执行                             │
└──────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────┐
│               第 3 层：输入校验层                  │
│  - file_id 格式正则校验                           │
│  - 路径遍历攻击过滤                               │
│  - 可执行文件 MIME 类型拦截                       │
│  - 大小限制（单文件 <500MB）                      │
└──────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────┐
│               第 4 层：操作保护层                  │
│  - 品类隔离（禁止跨品类操作）                     │
│  - 版本冲突检测（写入带 version）                 │
│  - 软删除（回收站 API，不物理删除）               │
│  - 审计日志（所有写操作记录）                     │
└──────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────┐
│               第 5 层：限流/配额层                 │
│  - 单次会话写入配额（防失控循环）                 │
│  - API 级别限流（429 → 指数退避）                 │
│  - 存储配额检查（写入前确认空间）                 │
└──────────────────────────────────────────────────┘
```

---

## 2. 用户确认层（Layer 1）

### 2.1 确认触发条件

以下操作**必须**经过用户显式确认：

| 操作类型 | 确认内容 | 示例 |
|---------|---------|------|
| 删除文件 | 显示文件名 + 大小 | "确认删除《2026年报告.doc》(2.3MB)？" |
| 覆盖文件 | 显示原文件版本 | "确认覆盖当前文档？此操作不可撤销。" |
| 批量操作 | 显示数量 + 文件列表 | "确认批量移动 50 个文件？" |
| 权限变更 | 显示目标用户 + 权限 | "确认授予张三编辑权限？" |
| 回收站清空 | 显示数量 + 影响 | "确认清空回收站？此操作不可恢复。" |

### 2.2 确认模式配置

```json
{
  "safety": {
    "confirm_mode": "dangerous",    // "always" 或 "dangerous"
    "dry_run": false,               // true 时只显示操作但不执行
    "audit_enabled": true
  }
}
```

---

## 3. 权限前置校验层（Layer 2）

### 3.1 校验规则

所有写入操作（create/update/delete/move/copy/permission change）执行**前**必须：

1. 调用 `kdoc.file.permission.check` 检查当前用户权限
2. 无权限直接终止，返回 `KD002` 错误
3. 不发出任何修改请求

### 3.2 权限类型

| 权限 | 说明 | 可执行操作 |
|------|------|-----------|
| `owner` | 文档所有者 | 全部操作（含删除、权限变更） |
| `editor` | 编辑者 | 编辑内容、移动、复制 |
| `viewer` | 查看者 | 查看、下载、创建副本 |
| `none` | 无权限 | 无 |

---

## 4. 输入校验层（Layer 3）

### 4.1 file_id 校验

```python
import re

FILE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{8,64}$')

def validate_file_id(file_id: str):
    if not FILE_ID_PATTERN.match(file_id):
        raise ParamError(f"非法 file_id 格式: {file_id}")
```

### 4.2 文件类型拦截

**禁止上传的文件扩展名**：

```python
BLOCKED_EXTENSIONS = {
    '.exe', '.bat', '.ps1', '.cmd', '.com', '.scr',
    '.vbs', '.js', '.wsf', '.msi', '.msp', '.mst',
    '.cpl', '.ins', '.isp', '.jse', '.lnk', '.pif',
    '.reg', '.sct', '.shb', '.shs', '.vb', '.vbe',
    '.wsc', '.wsf', '.wsh'
}
```

**禁止上传的 MIME 类型**：

```python
BLOCKED_MIME_TYPES = {
    'application/x-msdownload',
    'application/x-executable',
    'application/x-dosexec',
    'application/x-msdos-program',
    'application/x-powershell',
    'text/javascript',
    'application/javascript',
    'application/x-vbs',
    'application/x-bat'
}
```

### 4.3 大小限制

| 文件类型 | 大小限制 |
|---------|---------|
| 文字文档 | 100MB |
| 电子表格 | 100MB |
| 演示文稿 | 100MB |
| 图片 | 20MB |
| 附件 | 500MB |

---

## 5. 操作保护层（Layer 4）

### 5.1 品类隔离

- 通过 `kdoc.file.info` 识别文档品类
- 使用场景路由表选择对应工具集
- 严禁用 A 品类工具操作 B 品类文档

### 5.2 版本冲突检测

```
读取文档 → 获取当前版本号 V1
编辑准备 → 用户修改内容
写入文档 → 携带版本号 V1
如果服务端版本 != V1 → 返回 KD007 版本冲突
提示用户：获取最新版本 → 合并 → 重新写入
```

### 5.3 软删除

- 所有删除操作调用 `kdoc.file.delete`（→ 回收站）
- **绝不调用** `kdoc.file.delete(permanent=true)`（除非用户显式要求）

### 5.4 审计日志

所有写操作记录以下信息：

```json
{
  "timestamp": "2026-07-02T14:00:00+08:00",
  "operation": "file.create",
  "file_id": "file_abc123",
  "user_id": "user_xyz",
  "ip": "192.168.1.1",
  "success": true,
  "details": {"name": "会议纪要", "type": "doc"}
}
```

日志存储：本地文件 `kingdoc.log`

---

## 6. 限流/配额层（Layer 5）

### 6.1 限流策略

**收到 429 时的处理**：

```python
import time
import random

def exponential_backoff(retry_count: int, max_retries: int = 5):
    if retry_count >= max_retries:
        raise RateLimitError("超过最大重试次数")
    
    delay = min(2 ** retry_count + random.uniform(0, 1), 300)
    time.sleep(delay)
    return retry_count + 1
```

### 6.2 单次会话配额

| 限制项 | 阈值 | 说明 |
|--------|------|------|
| 写入次数 | 100 次/会话 | 防止 AI 失控循环 |
| 文件总大小 | 1GB/会话 | 防止批量大文件撑爆配额 |
| API 调用 | 1000 次/会话 | 综合限制 |

### 6.3 存储配额检查

写入前检查用户空间剩余容量：

```python
quota = kdoc.space.quota()
if quota["data"]["remaining"] < file_size:
    raise QuotaError("空间不足，请先清理文件或扩容")
```

---

## 7. Token 安全

| 规则 | 说明 |
|------|------|
| **不落盘** | Token 仅存在于内存中的 `KingDocAuth` 实例 |
| **不输出** | 任何日志、消息中不包含完整 Token |
| **有效期** | 2 小时，提前 5 分钟自动刷新 |
| **范围最小化** | 默认只申请 `user:file:read` + `user:file:write` |

---

## 8. 文件上传安全

### 8.1 上传前检查

1. 文件扩展名是否在黑名单
2. MIME 类型是否在黑名单
3. 文件大小是否超限
4. 目标文件夹是否可写

### 8.2 上传后处理

1. 服务端返回文件 ID
2. 记录上传日志
3. 可选：病毒扫描（如金山提供）

---

*最后更新：2026-07-02*
