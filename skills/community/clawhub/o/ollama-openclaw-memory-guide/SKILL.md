# Ollama + OpenClaw 本地记忆系统部署指南

> 在 Windows 管控环境下部署 Ollama 便携版，实现 OpenClaw 本地向量搜索和记忆系统。

## 适用场景

- 企业管控环境，无法安装 MSI/EXE 安装包
- 需要本地 embedding 服务（不依赖云端 API）
- 需要 OpenClaw 记忆系统的向量搜索功能
- 需要 L1/L2/L3 记忆提取管线

## 系统架构

```
OpenClaw Gateway
├── memory-tencentdb（主记忆插件）
│   ├── L0: 原始对话记录
│   ├── L1: 提取记录（SQLite FTS5）
│   ├── L2: 场景分块
│   └── L3: 用户画像
├── memorySearch（向量搜索）
│   ├── Provider: Ollama（本地）
│   ├── Model: nomic-embed-text
│   └── Dimensions: 768
└── Ontology（知识图谱）
    └── memory/ontology/graph.jsonl
```

## 前置要求

- Windows 10/11（x64）
- OpenClaw 已安装并运行
- Git（用于下载）
- Python 3.8+（可选，用于高级功能）
- 磁盘空间：约 2 GB

## 第一部分：Ollama 便携版安装

### 1.1 下载 Ollama

**方案 A：GitHub（推荐）**
```bash
# 克隆官方仓库
git clone https://github.com/ollama/ollama-windows-release.git D:\temp\ollama-windows-release
```

**方案 B：ModelScope 镜像（国内推荐）**
```bash
# 使用魔搭社区镜像
git clone https://www.modelscope.cn/models/ollama/ollama-windows-release.git D:\temp\ollama-windows-release
```

**方案 C：直接下载 ZIP**
```powershell
# 从 ModelScope 下载便携版 ZIP
Invoke-WebRequest -Uri "https://www.modelscope.cn/models/ollama/ollama-windows/resolve/master/ollama-windows-amd64.zip" -OutFile "D:\temp\ollama-windows-amd64.zip"
```

### 1.2 解压到 OpenClaw 目录

```powershell
# 创建目录结构
New-Item -ItemType Directory -Force -Path "$env:APPDATA\mx\openclaw-home\$env:USERNAME\.openclaw\tools\ollama"
New-Item -ItemType Directory -Force -Path "$env:APPDATA\mx\openclaw-home\$env:USERNAME\.openclaw\ollama-data\models"

# 解压（如果用方案 A/B）
Copy-Item -Path "D:\temp\ollama-windows-release\*" -Destination "$env:APPDATA\mx\openclaw-home\$env:USERNAME\.openclaw\tools\ollama" -Recurse -Force

# 解压（如果用方案 C）
Expand-Archive -Path "D:\temp\ollama-windows-amd64.zip" -DestinationPath "$env:APPDATA\mx\openclaw-home\$env:USERNAME\.openclaw\tools\ollama" -Force
```

**最终目录结构：**
```
.openclaw\
├── tools\
│   └── ollama\
│       ├── ollama.exe
│       └── lib\
├── ollama-data\
│   └── models\          # Ollama 模型存储
└── models\              # GGUF 模型（备用）
```

### 1.3 启动 Ollama 服务

```powershell
# 设置环境变量（模型存储路径）
$env:OLLAMA_MODELS = "$env:APPDATA\mx\openclaw-home\$env:USERNAME\.openclaw\ollama-data\models"

# 切换到 Ollama 目录
Set-Location "$env:APPDATA\mx\openclaw-home\$env:USERNAME\.openclaw\tools\ollama"

# 启动服务（后台运行）
Start-Process -FilePath ".\ollama.exe" -ArgumentList "serve" -WindowStyle Hidden
```

**验证服务：**
```powershell
# 检查版本
.\ollama.exe --version
# 输出: ollama version is 0.30.7

# 检查服务状态
Invoke-RestMethod -Uri "http://localhost:11434/api/version"
# 输出: {"version":"0.30.7"}
```

### 1.4 下载 Embedding 模型

```powershell
# 下载 nomic-embed-text（274 MB，768 维）
.\ollama.exe pull nomic-embed-text
```

**验证模型：**
```powershell
# 列出已下载模型
.\ollama.exe list
# 输出:
# NAME                       ID              SIZE      MODIFIED
# nomic-embed-text:latest    0a109f422b47    274 MB    1 minute ago

# 测试 embedding API
python -c "import requests; r = requests.post('http://localhost:11434/api/embeddings', json={'model':'nomic-embed-text','prompt':'test'}); print(f'Dim: {len(r.json()[\"embedding\"])}')"
# 输出: Dim: 768
```

### 1.5 配置开机自启动

**创建 VBS 启动脚本：**
```powershell
$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\ollama-serve.vbs"
$vbsContent = @'
Set WshShell = CreateObject("WScript.Shell")
WshShell.Environment("Process").Item("OLLAMA_MODELS") = "D:\Users\YOUR_USERNAME\AppData\Roaming\mx\openclaw-home\YOUR_USERNAME\.openclaw\ollama-data\models"
WshShell.CurrentDirectory = "D:\Users\YOUR_USERNAME\AppData\Roaming\mx\openclaw-home\YOUR_USERNAME\.openclaw\tools\ollama"
WshShell.Run """D:\Users\YOUR_USERNAME\AppData\Roaming\mx\openclaw-home\YOUR_USERNAME\.openclaw\tools\ollama\ollama.exe"" serve", 0, False
Set WshShell = Nothing
'@

# 替换 YOUR_USERNAME 为实际用户名
$vbsContent = $vbsContent -replace "YOUR_USERNAME", $env:USERNAME

# 写入启动文件夹
Set-Content -Path $startupPath -Value $vbsContent -Encoding UTF8
```

**验证：**
```powershell
# 查看启动脚本
Get-Content $startupPath

# 手动运行测试
cscript $startupPath
```

## 第二部分：OpenClaw 记忆系统配置

### 2.1 配置 memorySearch

编辑 `openclaw.json`（位于 `.openclaw\openclaw.json`）：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "model": "nomic-embed-text",
        "remote": {
          "baseUrl": "http://localhost:11434/v1",
          "apiKey": "ollama"
        }
      }
    }
  }
}
```

**关键配置说明：**
- `provider: "openai"` - 使用 OpenAI 兼容 API（Ollama 支持）
- `baseUrl: "http://localhost:11434/v1"` - Ollama 的 OpenAI 兼容端点
- `apiKey: "ollama"` - 占位符，Ollama 不需要真实 API Key
- **不要使用** `provider: "local"` + `model: "fts-only"`（这是纯文本搜索，没有向量）

**验证配置：**
```powershell
# 通过 Gateway API 检查
openclaw gateway config.get | ConvertFrom-Json | Select-Object -ExpandProperty agents | Select-Object -ExpandProperty defaults | Select-Object -ExpandProperty memorySearch
```

### 2.2 配置 memory-tencentdb 插件

确保 `openclaw.json` 中包含：

```json
{
  "plugins": {
    "enabled": true,
    "allow": ["mx", "memory-tencentdb"],
    "load": {
      "paths": ["D:\\Users\\YOUR_USERNAME\\AppData\\Roaming\\mx\\openclaw-home\\YOUR_USERNAME\\.openclaw\\plugins\\memory-tencentdb"]
    },
    "slots": {
      "memory": "memory-tencentdb"
    },
    "entries": {
      "memory-tencentdb": {
        "enabled": true,
        "config": {
          "pipeline": {
            "everyNConversations": 3,
            "enableWarmup": true,
            "l1IdleTimeoutSeconds": 10
          }
        }
      }
    }
  }
}
```

**关键配置说明：**
- `pipeline.everyNConversations: 3` - 每 3 次对话触发 L1 提取
- `pipeline.l1IdleTimeoutSeconds: 10` - 空闲 10 秒后触发提取
- **不要配置** `config.llm`（使用 Gateway 内置模型）

### 2.3 重建向量索引

如果从 `fts-only` 迁移到向量搜索，需要重建索引：

```powershell
# 安装依赖
pip install requests tqdm

# 运行重建脚本（断点续传）
python scripts/rebuild_vector_index.py
```

**脚本功能：**
- 扫描 `workspace/memory/` 下所有 `.md` 文件
- 按段落/标题切分为 chunks（最大 1000 字符）
- 调用 Ollama embedding API 生成 768 维向量
- 写入 `memory/main.sqlite` 的 `embedding_cache` 表
- 支持断点续传（进度保存到 `embeddings_progress.json`）

**预期结果：**
```
[INFO] 向量索引重建完成
[INFO] 总文件数: 310
[INFO] 总 chunks: 1804
[INFO] 数据库大小: 62 MB
[INFO] 向量维度: 768
```

### 2.4 测试记忆搜索

```powershell
# 通过 OpenClaw CLI 测试
openclaw memory search "测试查询"

# 通过 API 测试
Invoke-RestMethod -Uri "http://localhost:18790/api/memory/search" -Method Post -ContentType "application/json" -Body '{"query":"测试查询","limit":5}'
```

## 第三部分：常见问题排查

### 3.1 Ollama 服务无法启动

**症状：** `bind: Only one usage of each socket address`

**原因：** 端口 11434 被占用

**解决：**
```powershell
# 查找占用进程
netstat -ano | findstr :11434

# 终止进程
taskkill /F /PID <PID>

# 或更换端口
$env:OLLAMA_HOST = "127.0.0.1:11435"
.\ollama.exe serve
```

### 3.2 memorySearch 配置被覆盖

**症状：** 配置自动变回 `provider: "local", model: "fts-only"`

**原因：** 远程配置服务器覆盖（美信环境）

**解决：**
```powershell
# 直接编辑 openclaw.json（不触发重启）
$file = "$env:APPDATA\mx\openclaw-home\$env:USERNAME\.openclaw\openclaw.json"
$content = Get-Content $file -Raw
$content = $content -replace '"provider"\s*:\s*"local"', '"provider": "openai"'
$content = $content -replace '"model"\s*:\s*"fts-only"', '"model": "nomic-embed-text"'
[System.IO.File]::WriteAllText($file, $content)

# Gateway 会自动读取，无需重启
```

**预防：** 修改 PRD preset 或 dist JS 白名单（见 MEMORY.md）

### 3.3 向量搜索返回空结果

**症状：** `tdai_memory_search` 返回空数组

**排查步骤：**
1. 检查 Ollama 服务是否运行：`Invoke-RestMethod -Uri "http://localhost:11434/api/version"`
2. 检查模型是否下载：`.\ollama.exe list`
3. 检查向量索引是否存在：`Test-Path "memory/main.sqlite"`
4. 检查 embedding_cache 表：`python -c "import sqlite3; conn = sqlite3.connect('memory/main.sqlite'); print(conn.execute('SELECT COUNT(*) FROM embedding_cache').fetchone())"`

### 3.4 L1 提取不触发

**症状：** `recall_checkpoint.json` 中 `last_l1_extraction` 长时间未更新

**排查：**
```powershell
# 检查 pipeline 状态
Get-Content "memory-tdai/recall_checkpoint.json" | ConvertFrom-Json | Select-Object pipeline_states

# 手动触发提取
openclaw memory extract

# 查看日志
Get-Content "logs/gateway.log" | Select-String "L1 extraction"
```

### 3.5 Ollama 模型下载失败

**症状：** `pulling manifest: connection refused`

**原因：** 网络问题或 HuggingFace 被墙

**解决：**
```powershell
# 使用镜像
$env:OLLAMA_MODELS_MIRROR = "https://www.modelscope.cn/models"

# 或手动下载
Invoke-WebRequest -Uri "https://www.modelscope.cn/models/ollama/nomic-embed-text/resolve/master/model.bin" -OutFile "ollama-data\models\nomic-embed-text.bin"
```

## 第四部分：性能优化

### 4.1 内存占用优化

Ollama 默认会加载模型到内存，占用约 500 MB。

**优化方案：**
```powershell
# 设置模型空闲超时（5 分钟后卸载）
$env:OLLAMA_KEEP_ALIVE = "5m"

# 或完全禁用常驻
$env:OLLAMA_KEEP_ALIVE = "0"
```

### 4.2 向量索引优化

**批量处理：**
```python
# rebuild_vector_index.py 中调整 batch_size
BATCH_SIZE = 8  # 默认值，可根据内存调整
```

**增量更新：**
```python
# 只处理新增/修改的文件
python scripts/rebuild_vector_index.py --incremental
```

### 4.3 磁盘空间优化

**清理旧模型：**
```powershell
# 删除未使用的模型
.\ollama.exe rm <model-name>

# 查看模型占用
.\ollama.exe list
```

**压缩向量索引：**
```sql
-- 重建索引（SQLite）
VACUUM;
```

## 第五部分：备份与恢复

### 5.1 备份关键数据

```powershell
# 备份脚本
$backupDir = "D:\backup\openclaw-memory-$(Get-Date -Format 'yyyyMMdd')"
New-Item -ItemType Directory -Path $backupDir

# 备份记忆数据
Copy-Item -Path ".openclaw\memory-tdai" -Destination "$backupDir\memory-tdai" -Recurse
Copy-Item -Path ".openclaw\memory" -Destination "$backupDir\memory" -Recurse
Copy-Item -Path ".openclaw\ollama-data" -Destination "$backupDir\ollama-data" -Recurse

# 备份配置
Copy-Item -Path ".openclaw\openclaw.json" -Destination "$backupDir\openclaw.json"
```

### 5.2 恢复到新机器

```powershell
# 1. 安装 OpenClaw
# 2. 恢复备份
Copy-Item -Path "D:\backup\openclaw-memory-*\*" -Destination ".openclaw" -Recurse

# 3. 启动 Ollama
.\openclaw\tools\ollama\ollama.exe serve

# 4. 验证
openclaw memory search "测试"
```

## 附录：完整配置文件示例

### openclaw.json（记忆系统部分）

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "model": "nomic-embed-text",
        "remote": {
          "baseUrl": "http://localhost:11434/v1",
          "apiKey": "ollama"
        }
      }
    }
  },
  "plugins": {
    "enabled": true,
    "allow": ["mx", "memory-tencentdb"],
    "load": {
      "paths": ["D:\\Users\\YOUR_USERNAME\\AppData\\Roaming\\mx\\openclaw-home\\YOUR_USERNAME\\.openclaw\\plugins\\memory-tencentdb"]
    },
    "slots": {
      "memory": "memory-tencentdb"
    },
    "entries": {
      "memory-tencentdb": {
        "enabled": true,
        "config": {
          "pipeline": {
            "everyNConversations": 3,
            "enableWarmup": true,
            "l1IdleTimeoutSeconds": 10
          }
        }
      }
    }
  }
}
```

### ollama-serve.vbs

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Environment("Process").Item("OLLAMA_MODELS") = "D:\Users\YOUR_USERNAME\AppData\Roaming\mx\openclaw-home\YOUR_USERNAME\.openclaw\ollama-data\models"
WshShell.CurrentDirectory = "D:\Users\YOUR_USERNAME\AppData\Roaming\mx\openclaw-home\YOUR_USERNAME\.openclaw\tools\ollama"
WshShell.Run """D:\Users\YOUR_USERNAME\AppData\Roaming\mx\openclaw-home\YOUR_USERNAME\.openclaw\tools\ollama\ollama.exe"" serve", 0, False
Set WshShell = Nothing
```

## 参考资源

- [Ollama 官方文档](https://ollama.com/docs)
- [OpenClaw 记忆系统文档](https://docs.openclaw.ai/memory)
- [TDaí Memory Suite（ClawHub）](https://clawhub.ai/skills/tdai-memory-suite)
- [nomic-embed-text 模型](https://ollama.com/library/nomic-embed-text)

## 版本历史

- **v1.0.0** (2026-06-11) - 初始版本
  - Ollama 便携版部署
  - memorySearch 配置
  - 向量索引重建
  - 开机自启动
  - 常见问题排查

## 许可证

MIT-0

## 作者

Paudy Yin (paudyyin)

## 更新日志

- 2026-06-11: 初始发布，基于实际部署经验整理
