# 优甲乐服药提醒系统 - 用户指南

## 🎯 系统概述

这是一个专门为管理优甲乐（甲状腺素）服药而设计的智能提醒和记录系统。系统集成了 OpenClaw AI 助手，提供自动化提醒、服药记录、统计报表等功能。

## 📋 已实现功能

### ✅ 核心功能已完成
1. **服药记录系统** - 自动记录服药时间和状态
2. **状态查询功能** - 实时查看今日服药状态
3. **统计报表系统** - 生成服药依从性报告
4. **数据导出功能** - 支持 CSV 格式导出
5. **本地数据存储** - 所有数据安全存储在本地

### 🔧 待配置功能
1. **自动化提醒系统** - 需要配置 OpenClaw cron 任务
2. **定时提醒执行** - 需要设置系统定时任务

## 🚀 快速开始

### 1. 基本命令使用

#### 记录服药
```bash
# 记录当前时间服药
python3 openclaw_integration.py taken

# 记录特定时间服药（如 07:15）
python3 openclaw_integration.py taken 07:15
```

#### 查看状态
```bash
# 查看今日服药状态
python3 openclaw_integration.py status

# 生成7天报告
python3 openclaw_integration.py report

# 生成30天报告
python3 openclaw_integration.py report 30

# 查看最近记录
python3 openclaw_integration.py records
```

#### 数据管理
```bash
# 导出数据为CSV
python3 openclaw_integration.py export

# 查看系统设置
python3 openclaw_integration.py settings

# 获取帮助
python3 openclaw_integration.py help
```

### 2. 通过包装脚本使用
```bash
# 使用包装脚本（更简单）
./medication_wrapper.sh status
./medication_wrapper.sh taken
./medication_wrapper.sh report 30
```

## ⏰ 提醒系统配置

### 方案一：手动提醒（当前推荐）
由于 OpenClaw cron 任务需要特定的渠道配置，建议使用以下手动提醒方案：

1. **设置手机闹钟**：每天 6:30
2. **服药后手动记录**：使用命令记录
3. **定期查看统计**：检查服药依从性

### 方案二：OpenClaw 自动化提醒（需要额外配置）
如果需要完全自动化提醒，需要：

1. 配置 OpenClaw 的 Feishu 或 WebChat 渠道
2. 设置 cron 任务指向特定聊天
3. 测试提醒消息的接收

### 方案三：系统 cron + Python 脚本
可以创建系统级的 cron 任务来运行 Python 脚本发送提醒。

## 📊 数据与统计

### 数据存储位置
```
~/.openclaw/medication_data/
├── medication-records.json     # 服药记录
├── stats.json                  # 统计信息
└── settings.json              # 系统设置
```

### 关键统计指标
- **总服药天数**：有服药记录的总天数
- **按时服药天数**：在6:30-7:00之间服药的天数
- **服药依从率**：(服药天数 / 总天数) × 100%
- **连续服药天数**：当前连续服药的天数
- **最佳连续记录**：历史最高连续服药天数

## 🔍 使用场景示例

### 日常使用流程
```
早上 6:30：手机闹钟响起
早上 7:15：服用优甲乐
服药后：运行 python3 openclaw_integration.py taken 07:15
随时查看：运行 python3 openclaw_integration.py status
每周查看：运行 python3 openclaw_integration.py report 7
```

### 月度健康检查
```bash
# 生成月度报告
python3 openclaw_integration.py report 30

# 导出数据给医生
python3 openclaw_integration.py export
```

## 🛠️ 自定义配置

### 修改提醒时间
编辑 `~/.openclaw/medication_data/settings.json`：
```json
{
  "first_reminder_time": "07:00",
  "reminder_interval": 20,
  "on_time_window": 45,
  "reminder_enabled": true
}
```

### 调整按时窗口
`on_time_window` 控制从首次提醒后多少分钟内服药算作按时（默认30分钟）。

## 🔧 故障排除

### 常见问题

#### 1. 命令不工作
```bash
# 检查脚本权限
chmod +x medication_wrapper.sh

# 检查 Python 环境
python3 --version

# 检查依赖
pip3 install -r requirements.txt  # 如果有的话
```

#### 2. 数据不保存
- 检查数据目录权限
- 确保有足够的磁盘空间
- 检查 JSON 文件格式

#### 3. 统计不准确
- 确认系统时间正确
- 检查记录文件内容
- 重新计算统计

### 日志查看
```bash
# 查看脚本输出
python3 openclaw_integration.py status 2>&1

# 检查数据文件
cat ~/.openclaw/medication_data/medication-records.json | jq .
```

## 📈 健康管理建议

### 优甲乐服药最佳实践
1. **固定时间服药**：尽量每天同一时间服用
2. **空腹服用**：建议早上空腹服用，效果最佳
3. **避免干扰**：服药后至少30分钟再进食
4. **定期检查**：按医生建议定期检查甲状腺功能
5. **记录副作用**：如有不适及时记录并咨询医生

### 系统使用建议
1. **每日记录**：养成服药后立即记录的习惯
2. **每周回顾**：每周查看服药统计，调整习惯
3. **月度总结**：每月生成报告，评估依从性
4. **医生咨询**：定期向医生展示服药记录

## 🔄 系统维护

### 数据备份
```bash
# 手动备份数据
cp -r ~/.openclaw/medication_data ~/medication_data_backup

# 恢复数据
cp -r ~/medication_data_backup ~/.openclaw/medication_data
```

### 系统更新
```bash
# 更新脚本
cd /Users/robbin/.openclaw/workspace/skills/medication-reminder
git pull  # 如果使用 git

# 重新运行安装脚本
python3 setup.py
```

## 📞 支持与反馈

### 获取帮助
```bash
python3 openclaw_integration.py help
```

### 报告问题
如遇到问题，请提供：
1. 错误信息
2. 操作步骤
3. 系统环境信息

### 功能建议
欢迎提出改进建议，包括：
- 新的提醒方式
- 更多的统计指标
- 更好的用户界面

## 🎉 开始使用

现在你已经准备好了！建议：

1. **立即测试**：运行几个基本命令熟悉系统
2. **设置提醒**：配置手机闹钟作为初步提醒
3. **养成习惯**：每天服药后立即记录
4. **定期回顾**：每周查看统计，持续改进

**💊 健康第一，规律服药，坚持记录！**

---

*系统版本：1.0.0 | 最后更新：2026-04-28 | 作者：阿波罗*