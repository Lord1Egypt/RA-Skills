# 🚀 kk每日备份汇报 - 快速开始

## 📱 技能简介

**kk每日备份汇报**是一个专门为移动端优化的备份状态报告技能，提供简洁扼要的备份状态信息。

## 🎯 核心功能

### 1. 多目录备份检查
- 🖥️ homeserver (家庭服务器)
- 🌐 vps_jp (日本VPS)  
- 💻 xps (XPS电脑)
- 📺 YouTube (音频视频)
- 📝 notion (Obsidian笔记)

### 2. 移动端优化格式
- 简洁明了，适合手机查看
- 时间排序，一目了然
- 文件大小，心中有数

### 3. 灵活配置
- 支持自定义目录
- 多种输出格式
- 时间范围筛选

## ⚡ 立即使用

### 方式1: 直接运行脚本
```bash
cd /home/node/.openclaw/workspace/skills/kk-daily-backup-report
./kk_daily_backup_report.sh
```

### 方式2: 在OpenClaw会话中使用
安装技能后，直接在会话中说：
```
kk每日备份汇报
```

### 方式3: 定时自动汇报
```bash
# 每天上午9点自动汇报
0 9 * * * /path/to/kk_daily_backup_report.sh
```

## 🎨 输出格式示例

### 移动端格式 (默认)
```
## 📱 kk每日备份汇报

### 1. 🖥️ homeserver今日备份
**04:01** `backup_file.tar.gz` (115MB)

### 2. 🌐 vps_jp今日备份  
**00:58** `config_backup.tar.gz` (221MB)

## 📊 今日备份统计
- 总文件: 13个
- 系统状态: ✅ 正常
```

### 详细格式
```bash
./kk_daily_backup_report.sh --format detailed
```

### 摘要格式  
```bash
./kk_daily_backup_report.sh --format summary
```

## 🔧 常用命令

### 基本检查
```bash
# 今日备份汇报
./kk_daily_backup_report.sh

# 指定日期
./kk_daily_backup_report.sh --date 2026-02-24

# 最近3天
./kk_daily_backup_report.sh --days 3
```

### 目录筛选
```bash
# 仅检查特定目录
./kk_daily_backup_report.sh --dir homeserver
./kk_daily_backup_report.sh --dir vps_jp,xps
```

### 配置管理
```bash
# 显示当前配置
./kk_daily_backup_report.sh --config

# 自定义目录
./kk_daily_backup_report.sh --backup-root /your/backup/path
```

## 📁 目录结构

```
kk-daily-backup-report/
├── SKILL.md              # 技能文档
├── kk_daily_backup_report.sh  # 主脚本
├── test_skill.sh         # 测试脚本
└── QUICK_START.md        # 本指南
```

## ⚙️ 配置说明

### 默认配置
```bash
BACKUP_ROOT="/hellox/openclaw/1panel_backup"
OBSIDIAN_ROOT="/hellox/openclaw/obsidian"
TIMEZONE="Asia/Shanghai"
REPORT_STYLE="mobile"
```

### 自定义配置
1. 修改脚本中的默认值
2. 或通过命令行参数覆盖

## 🐛 故障排除

### 常见问题
1. **目录不存在**
   ```bash
   ./kk_daily_backup_report.sh --backup-root /正确/路径
   ```

2. **无权限访问**
   ```bash
   # 检查目录权限
   ls -la /hellox/openclaw/
   ```

3. **无新增文件**
   - 正常情况，可能今天没有备份
   - 检查备份系统是否正常运行

### 调试模式
```bash
./kk_daily_backup_report.sh --debug
```

## 📈 进阶使用

### 集成到工作流
```bash
# 结合健康检查
系统健康检查 && kk每日备份汇报

# 生成日报
echo "## 系统日报 $(date)" > daily_report.md
./kk_daily_backup_report.sh --format detailed >> daily_report.md
```

### 自动化监控
```bash
# 监控脚本示例
#!/bin/bash
REPORT=$(./kk_daily_backup_report.sh --format summary)
if echo "$REPORT" | grep -q "0个文件"; then
    echo "⚠️ 今日无备份，请检查系统"
else
    echo "✅ 备份正常"
fi
```

## 🎉 技能特点

### 优点
- ✅ **移动端优化** - 简洁适合手机查看
- ✅ **时间排序** - 按创建时间顺序显示
- ✅ **大小统计** - 文件大小一目了然
- ✅ **分类清晰** - 按目录分类展示
- ✅ **配置灵活** - 支持自定义目录和格式

### 适用场景
- 📱 每日手机查看备份状态
- 🖥️ 系统管理员日常检查
- 📊 备份系统健康监控
- 📝 生成备份状态报告

## 🤝 贡献与反馈

技能由 **kk** (幽默轻松助理) 开发，如有建议或问题：
1. 在ClawHub上提交反馈
2. 联系助理kk
3. 提交改进建议

---

**让备份汇报变得简单明了！** 📱

*技能版本: 1.0.0*
*最后更新: 2026-02-24*