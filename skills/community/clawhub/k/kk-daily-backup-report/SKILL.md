---
name: kk-daily-backup-report
description: kk每日备份汇报 - 简洁移动端优化的备份状态报告
homepage: https://clawhub.com
metadata: {"kk":{"emoji":"📱","style":"简洁移动端优化"}}
---

# kk-daily-backup-report

kk每日备份汇报技能，提供简洁、移动端优化的备份状态报告。

## 功能特点

### 🎯 核心功能
1. **多目录备份检查** - 自动检查1Panel各备份目录
2. **移动端优化** - 简洁扼要的汇报格式
3. **时间排序** - 按创建时间顺序显示
4. **大小统计** - 显示文件大小和总量
5. **分类清晰** - 按目录分类展示

### 📁 支持目录
- **homeserver** - 家庭服务器备份
- **vps_jp** - 日本VPS备份  
- **xps** - XPS电脑备份
- **YouTube** - 音频视频媒体备份
- **notion** - Obsidian笔记备份

### 📱 汇报格式
简洁移动端优化格式，包含：
- 文件名
- 文件大小
- 创建时间
- 分类统计

## 快速开始

### 安装后使用
```bash
# 技能会自动加载，在OpenClaw会话中直接使用
kk每日备份汇报
```

### 手动运行
```bash
# 运行主脚本（功能完整版）
./kk_daily_backup_report.sh

# 运行极简移动端版（推荐）
./kk_backup_report_simple.sh

# 或使用完整路径
/home/node/.openclaw/workspace/skills/kk-daily-backup-report/kk_backup_report_simple.sh
```

## 配置说明

### 默认目录配置
```bash
# 1Panel备份目录
BACKUP_ROOT="/hellox/openclaw/1panel_backup"

# Obsidian笔记目录  
OBSIDIAN_ROOT="/hellox/openclaw/obsidian"

# 汇报时间范围（今天）
REPORT_DATE=$(date '+%Y-%m-%d')
```

### 自定义配置
创建配置文件：
```bash
cat > ~/.config/kk-backup-report/config.json << EOF
{
  "backup_root": "/your/backup/path",
  "obsidian_root": "/your/obsidian/path",
  "report_style": "mobile",  # mobile | detailed | summary
  "timezone": "Asia/Shanghai"
}
EOF
```

## 使用示例

### 基本使用
```
用户: kk每日备份汇报

助理: 📱 kk每日备份汇报
      [详细汇报内容...]
```

### 输出示例
```
## 📱 kk每日备份汇报

### 1. 🖥️ homeserver今日备份
**04:01** `backup_file.tar.gz` (115MB)

### 2. 🌐 vps_jp今日备份  
**00:58** `config_backup.tar.gz` (221MB)

[更多内容...]

## 📊 今日备份统计
- 总文件: 13个
- 总大小: 约2.5GB+
- 系统状态: ✅ 正常
```

## 高级功能

### 1. 时间范围筛选
```bash
# 查看最近3天备份
./kk_daily_backup_report.sh --days 3

# 查看特定日期
./kk_daily_backup_report.sh --date 2026-02-24
```

### 2. 输出格式选择
```bash
# 移动端简洁格式（默认）
./kk_daily_backup_report.sh --format mobile

# 详细格式
./kk_daily_backup_report.sh --format detailed

# 仅摘要
./kk_daily_backup_report.sh --format summary
```

### 3. 目录筛选
```bash
# 仅检查特定目录
./kk_daily_backup_report.sh --dir homeserver
./kk_daily_backup_report.sh --dir vps_jp,xps
```

## 集成到工作流

### 定时自动汇报
```bash
# 添加到crontab，每天上午9点汇报
0 9 * * * /path/to/kk_daily_backup_report.sh --format mobile
```

### 与其他技能结合
```bash
# 结合健康检查
kk健康检查 && kk每日备份汇报

# 结合系统监控
系统状态检查 && kk每日备份汇报
```

## 故障排除

### 常见问题
1. **目录不存在**
   ```
   错误: 备份目录不存在
   解决: 检查BACKUP_ROOT配置
   ```

2. **权限问题**
   ```
   错误: 无法访问目录
   解决: 检查目录权限，确保可读
   ```

3. **无新增文件**
   ```
   提示: 今日无新增备份
   状态: 正常，可能备份未运行
   ```

### 调试模式
```bash
# 启用详细日志
./kk_daily_backup_report.sh --debug

# 查看配置
./kk_daily_backup_report.sh --config
```

## 更新日志

### v1.0.0 (2026-02-24)
- 初始版本发布
- 支持5个目录备份检查
- 移动端优化汇报格式
- 时间排序和大小统计

## 技术支持

如有问题，联系：
- **助理**: kk (幽默轻松风格)
- **技能名**: kk-daily-backup-report
- **版本**: 1.0.0

---

*让备份汇报变得简单明了！* 📱