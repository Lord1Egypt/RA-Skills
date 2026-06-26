# n8n 写入 Windows 桌面文件

> 2026-04-21 实测配置，解决 n8n v2.x 沙箱限制下的文件写入问题

## 核心结论

n8n v2.x Code 节点的 `fs` 模块被屏蔽，使用 **ReadWriteFile 节点** 是唯一官方支持的文件操作方式。

---

## docker-compose 必需配置

```yaml
services:
  n8n:
    image: n8nio/n8n:2.14.0
    container_name: n8n-new
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
      - C:/Users/lujun/Desktop:/home/node/desktop   # 关键：桌面映射
    user: "0:0"    # 关键：解决权限冲突
    environment:
      - N8N_RESTRICT_FILE_ACCESS_TO=/tmp;/home/node/desktop
      - N8N_STORAGE_PATH=/home/node/.n8n
      - N8N_BINARY_DATA_STORAGE_PATH=/home/node/.n8n
```

| 配置 | 值 | 说明 |
|------|-----|------|
| `user` | `"0:0"` | 以 root 运行，解决 Windows/WSL 权限冲突 |
| `N8N_RESTRICT_FILE_ACCESS_TO` | `/tmp;/home/node/desktop` | 分号 `;` 分隔多个路径 |
| 桌面映射 | `C:/Users/lujun/Desktop:/home/node/desktop` | 容器内访问桌面 |

---

## 成功的工作流模板

### 节点结构
```
Webhook → Create Binary (Code) → Write File (ReadWriteFile)
```

### Create Binary 节点（Code v2）
```javascript
const content = '要写入的内容';
const buffer = Buffer.from(content, 'utf8');
return [{
  json: { fileName: 'output.txt' },
  binary: {
    data: {
      mimeType: 'text/plain',
      fileName: 'output.txt',
      data: buffer.toString('base64')
    }
  }
}];
```

### Write File 节点（ReadWriteFile v1.1）
| 参数 | 值 |
|------|-----|
| Operation | `write` |
| File Name | `/home/node/desktop/文件名.txt` |
| Input Binary Field | `data` |

---

## 路径映射

| 容器内路径 | Windows 实际路径 |
|-----------|---------------|
| `/home/node/desktop/` | `C:\Users\lujun\Desktop\` |
| `/home/node/data/` | 需额外配置卷挂载 |

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `Module 'fs' is disallowed` | Code 节点禁用 fs | 用 ReadWriteFile 节点 |
| `is not writable` | 路径无权限 | 确认 N8N_RESTRICT_FILE_ACCESS_TO 配置 |
| `needs binary 'data'` | Binary Field 名不匹配 | Input Binary Field = `data` |

---

## 并发冲突处理

多个进程同时写同一文件会报 `Permission Denied`。

**解决方案：文件名加时间戳**
```
/home/node/desktop/公众号_{{ $now.toFormat('yyyyMMdd_HHmmss_SSS') }}.md
```

---

## Windows 路径注意

- ✅ 使用下划线 `_` 替代空格
- ✅ 分号 `;` 分隔多路径
- ❌ 不要用冒号 `:`
