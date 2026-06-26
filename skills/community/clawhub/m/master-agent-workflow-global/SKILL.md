# 🏗️ master-agent-workflow-global - 全局可迁移的主控代理工作流技能

## 🎯 技能概述

`master-agent-workflow-global` 是一个完善的主控代理工作流技能，专为需要并行任务调度、代理层级控制和完整错误处理的场景设计。这是原始 `master-agent-workflow` 技能的全局可迁移版本，支持一键安装、配置迁移和跨平台使用。

### ✨ 核心特性

- **✅ 全局可迁移**: 在任何OpenClaw实例中安装即可使用
- **✅ 一键安装**: 通过安装脚本或ClawdHub快速安装
- **✅ 配置迁移**: 支持导出/导入配置和模板
- **✅ 模板系统**: 预定义任务模板，快速启动
- **✅ 跨平台兼容**: Windows/Linux/macOS全支持
- **✅ 版本管理**: 语义化版本，支持升级和回滚

## 🚀 快速开始

### 安装方式

#### 方法1：使用安装脚本（推荐）
```bash
# 下载并安装
cd master-agent-workflow-global
./install.sh
```

#### 方法2：通过ClawdHub
```bash
# 发布后可用
clawdhub install master-agent-workflow-global
```

#### 方法3：手动安装
```bash
# 复制到全局技能目录
cp -r master-agent-workflow-global ~/.openclaw/global-skills/
# 激活技能
~/.openclaw/global-skills/master-agent-workflow/scripts/activator.sh
```

### 基本使用

```bash
# 使用默认配置执行任务
使用 master-agent-workflow-global execute "处理我的任务"

# 快捷命令
maw "处理我的任务"

# 指定并行数和超时
maw "批量处理" --max-workers 10 --timeout 2h
```

## 📋 功能详解

### 1. 代理层级架构
```
主代理 (Main) → 主控代理 (Master) → 工作代理 (Worker) × N
```
- 清晰的权限边界
- 正确的工具使用限制
- 自动清理机制

### 2. 智能调度算法
- 动态任务队列管理
- 并行度控制（可配置）
- 工作代理状态监控
- 自动重试和失败处理

### 3. 安全退出机制
- 超时退出（可配置时间）
- 卡住检测（无进展退出）
- 失败过多退出
- 工作代理超时终止

### 4. 工具安全规范
- 禁止使用系统命令（timeout、ping、sleep等）
- 只使用OpenClaw安全工具
- 正确的消息发送格式
- 完善的错误处理

## ⚙️ 配置管理

### 配置文件位置
```
~/.openclaw/global-skills/master-agent-workflow/config/
├── default.json          # 默认配置
├── production.json       # 生产环境配置
├── development.json      # 开发环境配置
└── custom-config.json    # 自定义配置
```

### 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| max_workers | number | 5 | 最大并行工作代理数 |
| timeout_hours | number | 3 | 主控代理超时时间（小时） |
| worker_timeout_minutes | number | 30 | 工作代理超时时间（分钟） |
| stuck_threshold_minutes | number | 15 | 卡住检测阈值（分钟） |
| fail_threshold | number | 10 | 失败阈值（超过则退出） |
| auto_cleanup | boolean | true | 是否自动清理完成的工作代理 |
| report_channel | string | "feishu" | 进度报告渠道 |

### 配置命令

```bash
# 保存自定义配置
maw configure save high-performance --max-workers 20 --timeout 4h

# 使用特定配置
maw execute "任务" --config high-performance

# 列出所有配置
maw configure list
```

## 🎨 模板系统

### 预定义模板

#### 文件处理模板
```bash
maw execute "处理文件" --template file_processing
```
- 最大并行数: 5
- 工作代理超时: 45分钟
- 适合: 批量文件处理

#### API调用模板
```bash
maw execute "调用API" --template api_calling
```
- 最大并行数: 3
- 工作代理超时: 60分钟
- 失败阈值: 3
- 适合: 批量API调用

#### 数据处理模板
```bash
maw execute "处理数据" --template data_processing
```
- 最大并行数: 10
- 工作代理超时: 30分钟
- 适合: 批量数据处理

### 自定义模板
1. 创建模板文件 `my-template.json`:
```json
{
  "name": "my_template",
  "description": "我的自定义模板",
  "config": {
    "max_workers": 8,
    "timeout_hours": 2
  }
}
```

2. 复制到模板目录:
```bash
cp my-template.json ~/.openclaw/global-skills/master-agent-workflow/templates/
```

3. 使用模板:
```bash
maw execute "任务" --template my_template
```

## 🔄 迁移功能

### 导出配置
```bash
# 导出所有配置和模板
maw migrate export --output maw-backup.json

# 导出包含运行状态
maw migrate export --include-state --output maw-full-backup.tar.gz
```

### 导入配置
```bash
# 导入配置
maw migrate import maw-backup.json

# 从其他系统导入
scp user@remote:~/maw-backup.json .
maw migrate import maw-backup.json
```

### 备份和恢复
```bash
# 创建完整备份
maw migrate backup

# 列出备份
maw migrate list

# 清理旧备份（30天前）
maw migrate clean 30
```

## 🖥️ 跨平台支持

### Windows
```bash
# 安装后会自动创建批处理文件
maw.bat "执行任务"

# 环境变量
set MAW_HOME=%USERPROFILE%\.openclaw\global-skills\master-agent-workflow
```

### Linux/macOS
```bash
# 安装后会自动创建shell脚本
maw "执行任务"

# 环境变量
export MAW_HOME=~/.openclaw/global-skills/master-agent-workflow
```

### 路径处理
技能自动处理不同操作系统的路径差异：
- Windows: 使用 `%USERPROFILE%`
- Linux/macOS: 使用 `~`
- 自动检测和转换路径格式

## 📊 监控和报告

### 进度报告
- 定期发送进度报告（每10分钟）
- 报告渠道可配置（feishu、telegram、console等）
- 包含任务统计和性能指标

### 执行日志
```
~/.openclaw/global-skills/master-agent-workflow/logs/
├── execution-20260327-0930.log
├── error-20260327-0935.log
└── performance-20260327-0940.log
```

### 性能指标
- 任务完成率
- 平均执行时间
- 并行效率
- 资源利用率

## 🔧 高级用法

### 环境变量覆盖
```bash
# 使用环境变量设置配置
export MAW_MAX_WORKERS=20
export MAW_TIMEOUT_HOURS=4
maw "任务"
```

### 脚本集成
```bash
#!/bin/bash
# 自动化脚本示例

# 加载配置
CONFIG="--config production"

# 执行任务
maw "每日备份任务" $CONFIG --max-workers 8 --timeout 2h

# 检查结果
if [ $? -eq 0 ]; then
    echo "✅ 任务成功"
else
    echo "❌ 任务失败"
    exit 1
fi
```

### 与cron集成
```bash
# 每日凌晨2点执行
0 2 * * * /usr/bin/maw "每日任务" --config production
```

## 🐛 故障排除

### 常见问题

#### Q1: 安装失败
**原因**: 权限问题或依赖缺失
**解决**:
```bash
# 检查权限
ls -la ~/.openclaw/

# 重新安装
./install.sh --force
```

#### Q2: 命令未找到
**原因**: 环境变量未生效
**解决**:
```bash
# 重新加载shell配置
source ~/.bashrc  # 或 source ~/.zshrc

# 或直接使用完整路径
~/.openclaw/global-skills/master-agent-workflow/scripts/maw.sh
```

#### Q3: 配置导入失败
**原因**: 版本不兼容或文件损坏
**解决**:
```bash
# 检查文件格式
file backup.json

# 使用兼容模式
maw migrate import backup.json --force
```

### 调试模式
```bash
# 启用详细日志
export MAW_DEBUG=true
maw "任务" --dry-run

# 查看日志
cat ~/.openclaw/global-skills/master-agent-workflow/logs/debug.log
```

## 📈 性能优化

### 并行度优化
- **I/O密集型任务**: 增加并行数（5-10）
- **CPU密集型任务**: 减少并行数（2-3）
- **网络密集型任务**: 中等并行数（3-5）

### 内存优化
- 及时清理完成的工作代理
- 使用流式处理大文件
- 避免在内存中保存大量数据

### 网络优化
- 批量发送进度报告
- 使用压缩传输大数据
- 减少不必要的网络请求

## 🔄 从v1.0.0迁移

### 迁移步骤
1. **备份当前配置**
   ```bash
   cd ~/.openclaw/workspace/skills/master-agent-workflow
   cp -r . ~/maw-v1-backup/
   ```

2. **安装v2.0.0**
   ```bash
   cd master-agent-workflow-global
   ./install.sh
   ```

3. **迁移配置**
   ```bash
   maw migrate import ~/maw-v1-backup/skill.json
   ```

4. **验证迁移**
   ```bash
   maw --version
   maw execute "测试任务" --dry-run
   ```

### 兼容性说明
- **完全兼容**: v2.0.0完全兼容v1.0.0的配置格式
- **新增功能**: 模板系统、迁移工具、全局安装
- **向后兼容**: 所有v1.0.0功能在v2.0.0中可用

## 📚 参考资源

### 文档目录
- `SKILL.md` - 本文件，主技能文档
- `references/examples.md` - 使用示例
- `references/openclaw-integration.md` - OpenClaw集成指南
- `migration-guide.md` - 迁移指南

### 脚本目录
- `scripts/activator.sh` - 激活脚本
- `scripts/migrate.sh` - 迁移工具
- `scripts/maw.sh` - 快捷命令

### 模板目录
- `templates/file_processing.json` - 文件处理模板
- `templates/api_calling.json` - API调用模板
- `templates/data_processing.json` - 数据处理模板

## 🆘 支持与帮助

### 获取帮助
```bash
# 查看帮助
maw help

# 查看版本
maw --version

# 查看技能状态
maw status
```

### 报告问题
```bash
# 生成诊断报告
maw diagnose --output diagnosis.json

# 查看日志
cat ~/.openclaw/global-skills/master-agent-workflow/logs/error.log
```

### 联系支持
- **GitHub**: https://github.com/xiaolong-ai/master-agent-workflow
- **ClawdHub**: https://clawhub.com/skills/master-agent-workflow-global
- **问题反馈**: 通过GitHub Issues或ClawdHub反馈

## 📄 许可证

MIT License - 详见LICENSE文件

---

**技能名称**: master-agent-workflow-global  
**版本**: 2.0.0  
**创建时间**: 2026年3月25日  
**全局版本发布时间**: 2026年3月27日  
**作者**: 小龙  
**状态**: ✅ 生产就绪  
**兼容性**: OpenClaw >= 1.0.0  

**更新日志**:
- v2.0.0 (2026-03-27): 全局可迁移版本，添加模板系统和迁移工具
- v1.0.0 (2026-03-25): 初始版本，基本的主控代理工作流功能