---
name: ollama-migrator
description: Ollama 模型迁移技能。用于将 Ollama 模型从 C 盘迁移到其他磁盘，释放 C 盘空间。使用场景：(1) C 盘空间不足需要迁移模型，(2) 更换模型存储位置，(3) 检查 Ollama 模型占用空间，(4) 验证迁移后模型可用性
---

# Ollama 模型迁移助手

本技能帮助将 Ollama 模型安全迁移到其他磁盘，释放 C 盘空间。

## 核心能力

### 1. 空间分析
- 检查当前模型存储位置
- 计算模型总占用空间
- 检查目标磁盘可用空间

### 2. 安全迁移
- 停止 Ollama 服务
- 复制模型文件（保留完整性）
- 设置环境变量
- 验证迁移结果

### 3. 回滚支持
- 保留源文件直到验证完成
- 支持手动回滚
- 迁移日志记录

## 工作流程

### 步骤 1: 检查状态
```powershell
# 检查当前模型位置和大小
python scripts/check_ollama_status.py
```

### 步骤 2: 执行迁移
```powershell
# 迁移到 D 盘（默认）
python scripts/migrate_ollama.py --target D:\Ollama\models

# 迁移到其他位置
python scripts/migrate_ollama.py --target E:\AI\models
```

### 步骤 3: 验证
```powershell
# 验证模型列表
ollama list

# 测试运行模型
ollama run qwen3.5:9b
```

### 步骤 4: 清理（可选）
确认迁移成功后，删除旧文件：
```powershell
python scripts/migrate_ollama.py --cleanup
```

## 环境变量

迁移后设置的环境变量：
- **用户级**: `OLLAMA_MODELS = <目标路径>`
- **系统级**: 需要管理员权限（可选）

## 脚本工具

- `scripts/check_ollama_status.py` - 检查 Ollama 状态和模型占用
- `scripts/migrate_ollama.py` - 执行迁移操作
- `scripts/verify_ollama.py` - 验证迁移结果

## 触发条件

当用户提到：
- "Ollama 迁移"
- "Ollama 模型移动到其他盘"
- "C 盘 Ollama 占用太大"
- "Ollama 模型位置"
- "迁移 Ollama 到 D 盘"

## 安全机制

### 必须遵守的规则

1. **迁移前检查**：
   - 确认 Ollama 服务已停止
   - 检查目标磁盘空间充足
   - 记录当前模型列表

2. **数据完整性**：
   - 使用可靠复制（验证大小）
   - 保留源文件直到验证完成
   - 迁移日志记录

3. **用户确认**：
   - 显示迁移计划
   - 用户明确确认后才执行
   - 支持预览模式

4. **验证机制**：
   - 迁移后自动验证模型列表
   - 测试运行一个模型
   - 确认无误后才建议清理

## 注意事项

1. **新终端窗口**：环境变量在新打开的终端中生效
2. **运行中的服务**：需要重启 Ollama 服务
3. **权限问题**：系统级环境变量需要管理员权限
4. **备份建议**：重要模型建议先备份
