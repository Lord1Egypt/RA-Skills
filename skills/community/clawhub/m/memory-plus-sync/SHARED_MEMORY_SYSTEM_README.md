# 共享文件夹记忆同步系统

基于共享文件夹的 Hermes ↔ OpenClaw 双向记忆同步系统，避免记忆混乱，保持系统纯净。

## 🎯 设计原则

1. **不交叉存储** - Hermes 记忆存 Hermes 数据库，OpenClaw 记忆存 OpenClaw 数据库
2. **共享文件夹中转** - 使用 `~/.shared-memory/` 作为安全中转站
3. **避免记忆混乱** - 各自维护数据完整性，故障隔离
4. **全自动运行** - 支持定时任务和手动触发

## 🏗️ 系统架构

```
~/.shared-memory/
├── hermes/
│   ├── to_openclaw/      # Hermes → OpenClaw 导出
│   ├── from_openclaw/    # OpenClaw → Hermes 导入  
│   ├── processed/        # 已处理文件
│   └── logs/             # Hermes 同步日志
├── openclaw/
│   ├── to_hermes/        # OpenClaw → Hermes 导出
│   ├── from_hermes/      # Hermes → OpenClaw 导入
│   ├── processed/        # 已处理文件
│   └── logs/             # OpenClaw 同步日志
└── backups/              # 系统备份
```

## 📋 功能特性

### ✅ 双向同步
- **Hermes → OpenClaw**: 导出重要用户偏好、项目配置、关键决策
- **OpenClaw → Hermes**: 导入重要发现、研究洞察、系统告警

### ✅ 记忆清理
- **Hermes 记忆清理**: 自动备份、清理过期记忆、优化 memory.md
- **OpenClaw 数据库优化**: VACUUM 压缩、删除过期记录、重建索引

### ✅ 智能过滤
- **重要性评分**: 自动评估记忆重要性 (1-10)
- **去重检测**: 基于内容哈希和语义相似度
- **时间过滤**: 保留最近重要记忆，自动归档旧记忆

### ✅ 监控日志
- **详细日志**: JSONL 格式日志，便于分析
- **同步报告**: 每次同步生成详细报告
- **健康检查**: 系统状态监控和告警

## 🚀 快速开始

### 1. 安装系统
```bash
cd ~/.hermes/skills/openclaw-imports/memory-plus-sync
chmod +x install.sh
./install.sh
```

### 2. 手动测试
```bash
# 查看系统状态
shared-memory-sync status

# 运行双向同步
shared-memory-sync sync-bidirectional

# 清理记忆文件
shared-memory-sync cleanup

# 运行完整工作流（清理 + 同步）
shared-memory-sync full-workflow
```

### 3. 配置定时任务
```bash
# 查看生成的定时任务配置
cat ~/.shared-memory/cron_config.txt

# 添加到 crontab
crontab -e
# 添加以下内容：
# 每小时同步一次
0 * * * * cd ~/.hermes/skills/openclaw-imports/memory-plus-sync && python3 shared_memory_cli.py sync-bidirectional
# 每天凌晨2点清理记忆
0 2 * * * cd ~/.hermes/skills/openclaw-imports/memory-plus-sync && python3 shared_memory_cli.py cleanup
# 每周日凌晨3点完整工作流
0 3 * * 0 cd ~/.hermes/skills/openclaw-imports/memory-plus-sync && python3 shared_memory_cli.py full-workflow
```

## 📖 详细使用

### 命令行选项
```bash
# Hermes → OpenClaw 单向同步
shared-memory-sync sync-hermes-to-openclaw --min-importance 7

# OpenClaw → Hermes 单向同步  
shared-memory-sync sync-openclaw-to-hermes --limit 15

# 双向同步
shared-memory-sync sync-bidirectional

# 清理记忆（可指定清理目标）
shared-memory-sync cleanup --clean-hermes --clean-openclaw

# 完整工作流（清理 + 双向同步）
shared-memory-sync full-workflow

# 系统状态
shared-memory-sync status
```

### 参数说明
- `--min-importance N`: 最小重要性阈值 (1-10，默认: 7)
- `--limit N`: 导出记忆数量限制 (默认: 20)
- `--clean-hermes`: 清理 Hermes 记忆文件
- `--clean-openclaw`: 清理 OpenClaw 数据库

## 🔧 技术实现

### 核心模块
1. **shared_folder_sync.py** - 共享文件夹同步引擎
2. **hermes_exporter.py** - Hermes 记忆导出器
3. **openclaw_importer.py** - OpenClaw 记忆导入器  
4. **openclaw_exporter.py** - OpenClaw 记忆导出器
5. **hermes_importer.py** - Hermes 记忆导入器
6. **memory_cleaner.py** - 记忆清理器
7. **shared_memory_controller.py** - 主控制器
8. **shared_memory_cli.py** - 命令行接口

### 同步流程
```
Hermes 记忆导出 → ~/.shared-memory/hermes/to_openclaw/
OpenClaw 监控导入 → 存储到本地数据库 → 移动文件到 processed/
OpenClaw 记忆导出 → ~/.shared-memory/openclaw/to_hermes/
Hermes 监控导入 → 更新 memory.md → 移动文件到 processed/
```

### 清理策略
- **Hermes memory.md**: 保留30天内的重要记忆，自动备份原文件
- **OpenClaw SQLite**: VACUUM 压缩，删除90天前的记录，备份数据库
- **共享文件夹**: 自动清理30天前的已处理文件

## 📊 监控与调试

### 查看日志
```bash
# Hermes 同步日志
ls -la ~/.shared-memory/hermes/logs/

# OpenClaw 同步日志  
ls -la ~/.shared-memory/openclaw/logs/

# 系统备份
ls -la ~/.shared-memory/backups/
```

### 检查同步状态
```bash
# 查看待处理文件
ls -la ~/.shared-memory/hermes/to_openclaw/
ls -la ~/.shared-memory/openclaw/to_hermes/

# 查看已处理文件
ls -la ~/.shared-memory/hermes/processed/
ls -la ~/.shared-memory/openclaw/processed/
```

### 手动调试
```bash
# 导出 Hermes 记忆（不实际同步）
cd ~/.hermes/skills/openclaw-imports/memory-plus-sync
python3 -c "
from hermes_exporter import HermesMemoryExporter
exporter = HermesMemoryExporter()
memories = exporter.export_important_memories(min_importance=5)
print(f'导出 {len(memories)} 条记忆')
"

# 检查 OpenClaw 数据库
sqlite3 ~/.openclaw/memory/main.sqlite "SELECT COUNT(*) FROM imported_hermes_memories;"
```

## ⚠️ 注意事项

1. **首次同步前备份**
   ```bash
   cp ~/.hermes/memories/MEMORY.md ~/.hermes/memories/MEMORY_backup_$(date +%Y%m%d).md
   cp ~/.openclaw/memory/main.sqlite ~/.openclaw/memory/main_backup_$(date +%Y%m%d).sqlite
   ```

2. **权限要求**
   - 需要读取 `~/.hermes/memories/` 和 `~/.openclaw/memory/`
   - 需要写入 `~/.shared-memory/`

3. **依赖检查**
   - Python 3.8+
   - sqlite3 模块
   - 足够的磁盘空间（建议 > 100MB）

4. **故障处理**
   - 检查日志文件 `~/.shared-memory/*/logs/`
   - 查看同步报告 `~/.shared-memory/sync_report_*.json`
   - 恢复备份文件到原始位置

## 🔄 更新维护

### 更新系统
```bash
cd ~/.hermes/skills/openclaw-imports/memory-plus-sync
git pull origin main  # 如果使用 git
# 或手动更新文件后重新运行安装脚本
./install.sh
```

### 清理旧数据
```bash
# 清理30天前的日志和备份
find ~/.shared-memory -name "*.log" -mtime +30 -delete
find ~/.shared-memory -name "*.json" -mtime +30 -delete
find ~/.shared-memory -name "*.bak" -mtime +30 -delete
find ~/.shared-memory -name "*.md" -mtime +30 -delete
```

## 📞 支持与反馈

### 常见问题
1. **同步失败**: 检查目录权限和磁盘空间
2. **记忆丢失**: 从备份文件恢复 `~/.shared-memory/backups/`
3. **性能问题**: 调整同步频率和记忆数量限制

### 报告问题
1. 收集相关日志文件
2. 描述具体操作步骤
3. 提供错误信息截图

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 👥 贡献者

- **伊娃 (Eva)** - 系统设计与实现
- **主人 (Lewis)** - 需求提出与架构指导

---

**最后更新**: 2026-04-17  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪