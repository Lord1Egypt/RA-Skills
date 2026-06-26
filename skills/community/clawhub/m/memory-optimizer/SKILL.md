# Memory Optimizer

为 OpenClaw Agent 提供高效的记忆管理系统 — SHA-256 去重、实时监听、季度归档

## 用途

当需要优化 OpenClaw 记忆系统性能时使用：
- 长周期运行（数周/数月），记忆文件累积
- 高频对话，每天产生大量记忆内容
- 需要跨会话记忆检索
- 希望减少索引时间和存储空间

## 安装

```bash
npx skills add sirius/memory-optimizer@1.0.0
```

或手动安装：
```bash
# 1. 复制脚本到工作区
cp scripts/*.py ~/.openclaw/workspace/scripts/
cp scripts/*.sh ~/.openclaw/workspace/scripts/

# 2. 安装依赖
pip3 install watchdog

# 3. 设置权限
chmod +x ~/.openclaw/workspace/scripts/memory-*.py
```

## 使用

### 快速开始

**启动实时监听（推荐）：**
```bash
python3 scripts/memory-watcher.py ./memory/ &
```

**手动索引：**
```bash
python3 scripts/memory-dedup.py ./memory/
```

### 命令说明

| 工具 | 命令 | 用途 |
|------|------|------|
| **memory-dedup** | `python3 scripts/memory-dedup.py ./memory/` | 手动去重索引 |
| **memory-watcher** | `python3 scripts/memory-watcher.py ./memory/ &` | 后台实时监听 |
| **memory-archive** | `bash scripts/memory-archive.sh` | 季度归档 |

### 高级用法

```bash
# 显示索引统计
python3 scripts/memory-dedup.py ./memory/ --stats

# 搜索关键词
python3 scripts/memory-dedup.py ./memory/ --search "关键词"

# 清理过期 chunk
python3 scripts/memory-dedup.py ./memory/ --clean
```

## 核心特性

### 1. SHA-256 去重索引
- 基于内容哈希自动识别重复记忆
- 只索引新增/修改的文件
- 自动清理已删除文件的索引
- 索引速度提升 90%+

### 2. 实时文件监听
- 基于 watchdog 的后台监听
- 文件修改后 1.5 秒自动索引
- 文件删除后自动清理 chunk
- 防抖处理，避免频繁写入

### 3. 季度归档机制
- 自动归档 90 天前的记忆文件
- 压缩存储，节省空间
- 保留完整历史记录
- 可随时回溯恢复

## 配置

编辑脚本修改默认参数：

```python
# memory-dedup.py
max_chunk_size = 500  # 分块大小（字符）

# memory-watcher.py
DEBOUNCE_SECONDS = 1.5  # 防抖时间（秒）

# memory-archive.sh
ARCHIVE_AGE_DAYS = 90  # 归档阈值（天）
```

## 依赖

- Python 3.7+
- watchdog (pip3 install watchdog)

## 性能对比

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 索引时间 | 5-10 秒 | 0.5-1 秒 | 90% ↓ |
| 索引 chunk 数 | 500+ | 200 | 60% ↓ |
| 存储空间 | 10MB+ | 4MB | 60% ↓ |
| 检索速度 | 2-3 秒 | 0.5 秒 | 85% ↓ |

*测试环境：Mac mini M2, 100 个记忆文件，30 天数据*

## 故障排查

**监听器无法启动：**
```bash
pip3 list | grep watchdog
# 如果没有，安装：
pip3 install watchdog
```

**索引文件损坏：**
```bash
rm ~/.openclaw/workspace/memory/.index.json
python3 scripts/memory-dedup.py ./memory/
```

**归档后检索不到旧文件：**
- 解压归档文件到临时目录
- 手动运行索引

## 作者

Sirius (小虾米)

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-03-19)
- ✨ 初始版本发布
- ✅ SHA-256 去重索引
- ✅ 实时文件监听
- ✅ 季度归档机制
