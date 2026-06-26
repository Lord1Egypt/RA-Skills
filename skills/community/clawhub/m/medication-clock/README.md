# 优甲乐服药提醒与记录 Skill

一个用于管理优甲乐（甲状腺素）服药的智能提醒和记录系统，集成到 OpenClaw AI 助手。

## 🎯 功能特点

### 📅 智能提醒系统
- **每日6:30首次提醒**服用优甲乐
- **每15分钟重复提醒**，直到确认服药
- **灵活的时间设置**，可根据需求调整

### 📊 完整记录功能
- **自动记录服药时间**和状态
- **按时/延迟标记**，帮助建立规律
- **连续服药天数统计**
- **服药依从性分析**

### 📈 报表与查询
- **每日状态查询**，了解当日服药情况
- **服药统计报告**，支持自定义时间范围
- **历史记录浏览**，查看所有服药记录
- **数据导出功能**，支持 CSV 格式导出

### 🔒 安全与隐私
- **本地数据存储**，不涉及云端传输
- **用户完全控制**数据访问权限
- **数据备份功能**，防止意外丢失

## 🚀 快速开始

### 1. 安装依赖
确保已安装 Python 3.8+ 和 OpenClaw。

### 2. 运行安装脚本
```bash
cd /Users/robbin/.openclaw/workspace/skills/medication-reminder
python3 setup.py
```

### 3. 测试系统功能
```bash
python3 test_system.py
```

### 4. 配置 OpenClaw cron 任务
按照安装脚本输出的说明配置每日提醒任务。

## 📖 使用指南

### 基本命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/medication-clock start` | 启动每日提醒 | `/medication-clock start` |
| `/medication-clock stop` | 停止每日提醒 | `/medication-clock stop` |
| `/medication-clock taken` | 记录服药 | `/medication-clock taken` |
| `/medication-clock taken 07:15` | 记录特定时间服药 | `/medication-clock taken 07:15` |
| `/medication-clock status` | 查看今日状态 | `/medication-clock status` |
| `/medication-clock report` | 生成7天报告 | `/medication-clock report` |
| `/medication-clock report 30` | 生成30天报告 | `/medication-clock report 30` |
| `/medication-clock records` | 查看最近记录 | `/medication-clock records` |
| `/medication-clock export` | 导出数据为CSV | `/medication-clock export` |
| `/medication-clock settings` | 查看当前设置 | `/medication-clock settings` |
| `/medication-clock help` | 显示帮助信息 | `/medication-clock help` |

### 使用流程示例

#### 日常使用
1. **早上6:30**：系统自动发送首次提醒
2. **每15分钟**：重复提醒，直到确认
3. **服药后**：回复 `/medication-clock taken`
4. **随时查看**：使用 `/medication-clock status` 查看状态

#### 查看统计
```bash
# 查看今日状态
/medication-clock status

# 生成30天报告
/medication-clock report 30

# 查看最近14天记录
/medication-clock records 14
```

## 🛠️ 技术架构

### 文件结构
```
medication-reminder/
├── SKILL.md                    # Skill 说明文档
├── medication_reminder.py      # 核心功能实现
├── openclaw_integration.py     # OpenClaw 集成
├── setup.py                    # 安装配置脚本
├── test_system.py              # 测试脚本
├── README.md                   # 本文件
└── openclaw-skill-config.json  # OpenClaw 配置
```

### 数据存储
```
~/.openclaw/medication_data/
├── medication-records.json     # 服药记录
├── stats.json                  # 统计数据
└── settings.json              # 系统设置
```

### 配置项说明
- `first_reminder_time`: 首次提醒时间（默认: 06:30）
- `reminder_interval`: 重复提醒间隔（默认: 15分钟）
- `on_time_window`: 按时服药时间窗口（默认: 30分钟）
- `reminder_enabled`: 提醒功能开关

## 🔧 自定义配置

### 修改提醒时间
编辑 `~/.openclaw/medication_data/settings.json`：
```json
{
  "first_reminder_time": "07:00",
  "reminder_interval": 20,
  "on_time_window": 45
}
```

### 调整提醒频率
可通过修改 `reminder_interval` 调整重复提醒频率。

### 设置按时窗口
`on_time_window` 控制从首次提醒后多少分钟内服药算作按时。

## 📊 数据导出

### CSV 格式导出
```bash
/medication-clock export
```
导出的 CSV 文件包含以下列：
- 日期（YYYY-MM-DD）
- 时间（HH:MM）
- 是否按时（是/否）
- 记录方式（自动/手动）
- 记录时间戳

### 数据备份
所有数据文件位于 `~/.openclaw/medication_data/` 目录，可手动备份。

## 🔍 故障排除

### 常见问题

#### 1. 提醒未发送
- 检查 OpenClaw cron 任务是否已配置
- 确认 OpenClaw 服务正在运行
- 检查设置中的 `reminder_enabled` 是否为 true

#### 2. 记录不保存
- 检查数据目录权限
- 确保有足够的磁盘空间
- 查看是否有其他进程正在使用数据文件

#### 3. 命令不响应
- 确认已正确安装 Skill
- 检查 OpenClaw 集成配置
- 查看错误日志

### 日志查看
```bash
# 查看 OpenClaw 日志
tail -f /tmp/openclaw/openclaw-*.log

# 查看数据目录
ls -la ~/.openclaw/medication_data/
```

## 📈 统计指标说明

### 服药依从率
```
依从率 = (服药天数 / 总天数) × 100%
```

### 按时服药率
```
按时率 = (按时服药天数 / 服药天数) × 100%
```

### 连续服药天数
从当前日期开始向前连续有服药记录的天数。

### 最佳连续服药
历史最高的连续服药天数记录。

## 🤝 贡献与反馈

### 报告问题
如发现 bug 或有功能建议，请提交 issue。

### 功能建议
欢迎提出改进建议，包括：
- 新的提醒方式
- 更多的统计指标
- 更好的用户界面
- 与其他系统的集成

### 开发贡献
1. Fork 项目
2. 创建功能分支
3. 提交代码更改
4. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

感谢 OpenClaw 项目提供的强大 AI 助手平台。

---

**💊 健康第一，规律服药！**