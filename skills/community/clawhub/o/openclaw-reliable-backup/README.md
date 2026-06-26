# OpenClaw 高可靠备份与安全管理技能

## 概述
本技能为 OpenClaw 提供企业级的自动化备份与恢复解决方案，确保您的 AI 助手状态在任何情况下都可安全恢复。

## 核心特性
- 🔄 **自动每日备份**：每天上午 8:00 自动执行完整备份
- ⚡ **变更触发保护**：修改核心文件前自动创建快照
- 📧 **邮件通知**：备份完成后自动发送邮件通知
- 🧹 **智能清理**：自动管理本地和邮箱中的过期备份
- 🔍 **完整可追溯**：详细日志记录所有操作
- 🛡️ **多重安全**：文件校验、操作确认、双重保护机制

## 安装与配置

### 1. 安装技能
bash
从 ClawHub 安装

clawhub install openclaw-reliable-backup

或手动安装

git clone https://github.com/yourusername/openclaw-reliable-backup.git
cp -r openclaw-reliable-backup ~/.openclaw/skills/


### 2. 首次使用配置
首次使用时，技能会引导您完成配置：

1. **设置备份目录**：
   
   技能：请设置备份文件的存储根目录（例如：~/openclaw_backups）：
   用户：/path/to/your/backup


2. **配置邮件通知**（可选但推荐）：
   - 技能会检查您是否已安装邮件管理技能
   - 如未安装，会引导您安装并配置
   - 配置后，所有备份将自动发送到您的邮箱

### 3. 邮箱技能配置
如需邮件通知功能，请确保已安装并配置邮件技能：

bash
安装邮件技能

clawhub install imap-smtp-email

配置邮箱

openclaw skill config imap-smtp-email
然后按提示输入 SMTP 服务器信息



## 使用方法

### 手动触发备份

用户：执行每日备份
或
用户：创建完整快照


### 修改文件前的自动保护
当您说要修改 OpenClaw 的核心文件时，技能会自动触发保护：

用户：我想修改 openclaw.json 的配置
技能：检测到您要修改核心文件，将在执行前自动创建备份。确认继续吗？
用户：确认
技能：✅ 已创建变更前备份，请继续修改...


### 查看备份状态

用户：备份状态
或
用户：最近有备份吗
或
用户：查看备份日志


### 清理旧备份

用户：清理本地备份
或
用户：清理邮箱备份


## 备份文件结构

备份根目录/
├── openclaw_full_backup_YYYYMMDD_HHMMSS.zip    # 备份压缩包
├── openclaw_full_backup_YYYYMMDD_HHMMSS.zip.sha256  # 校验文件
├── logs/
│   └── backup.log                              # 操作日志
├── snapshots/
│   └── [文件名]_before_change.bak             # 变更前快照
└── tmp/                                        # 临时目录


## 恢复指南

### 从备份恢复 OpenClaw
如果 OpenClaw 完全无法启动：

1. **查看日志确认备份**：
   bash
   cat /path/to/backup/logs/backup.log | tail -5


2. **下载备份文件**：
   - 从最新备份邮件中下载 ZIP 文件和 `.sha256` 文件
   - 或从本地备份目录获取

3. **验证文件完整性**：
   bash
   sha256sum -c openclaw_full_backup_YYYYMMDD_HHMMSS.zip.sha256


4. **停止 OpenClaw**：
   bash
   openclaw gateway stop


5. **恢复备份**：
   bash
   # 备份当前配置（可选但推荐）
   mv ~/.openclaw ~/.openclaw-old-$(date +%Y%m%d_%H%M%S)
   
   # 解压备份
   unzip openclaw_full_backup_YYYYMMDD_HHMMSS.zip -d ~


6. **重启 OpenClaw**：
   bash
   openclaw gateway start


### 恢复单个文件
如果只需恢复特定文件：

bash
从变更前快照恢复

cp /path/to/backup/snapshots/[文件名]_before_change.bak ~/.openclaw/[原文件路径]

从完整备份中提取单个文件

unzip -j openclaw_full_backup_YYYYMMDD_HHMMSS.zip ".openclaw/[文件路径]" -d ~


## 配置参数说明

### 环境变量
- `BACKUP_ROOT`：备份文件存储根目录
- `BACKUP_RETENTION_DAYS`：本地备份保留天数（默认：3）
- `EMAIL_RETENTION_DAYS`：邮箱备份保留天数（默认：7）

### 定时备份配置
每日备份默认在上午 8:00 执行。如需修改时间，可通过 OpenClaw 的定时任务功能配置。

## 故障排除

### 常见问题
1. **备份失败：权限不足**
   bash
   sudo chown -R USER:USER /path/to/backup


2. **邮件发送失败**
   - 检查邮件技能配置：`openclaw skill config imap-smtp-email`
   - 测试邮件发送：`openclaw email test`

3. **磁盘空间不足**
   - 清理旧备份：`用户：清理本地备份`
   - 增加备份目录空间

4. **恢复后配置丢失**
   - 检查是否覆盖了正确的目录
   - 验证备份文件的完整性
   - 从变更前快照恢复：`snapshots/` 目录

### 日志查看
bash
查看完整日志

cat /path/to/backup/logs/backup.log

查看最近操作

tail -f /path/to/backup/logs/backup.log

搜索特定操作

grep "SUCCESS" /path/to/backup/logs/backup.log
grep "FAILED" /path/to/backup/logs/backup.log


## 安全建议
1. **敏感信息保护**：
   - `credentials/` 目录包含 API 密钥，请确保备份文件的安全存储
   - 建议对备份文件进行加密存储

2. **访问控制**：
   bash
   # 设置备份目录权限
   chmod 700 /path/to/backup


3. **多地备份**：
   - 本地备份 + 邮件备份 + 云存储（建议）
   - 定期测试恢复流程

## 更新日志
- **v1.0.0**（初始版本）：基础备份、恢复、生命周期管理功能
- **v1.1.0**：增加变更触发保护、专项备份功能
- **v1.2.0**：优化日志系统、增加完整性校验

## 技术支持
如遇问题，请：
1. 查看 `backup.log` 获取详细错误信息
2. 检查磁盘空间和权限
3. 确认邮件技能配置正确
4. 在项目 Issues 中提交问题

---

**提示**：首次使用后，建议手动执行一次完整备份，并测试恢复流程，确保备份系统正常工作。


文件结构说明


openclaw-reliable-backup/
├── SKILL.md      # 主技能文件（AI 执行的指令集）
└── README.md     # 使用说明文档（用户参考手册）