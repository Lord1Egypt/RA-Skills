# 新股分析工具 (New Stock Analyzer)

## 🎯 核心功能

### 📊 数据获取
- **双数据源**: 东方财富（主）+ 中财网（验证）
- **实时更新**: 自动获取最新新股数据
- **完整信息**: 市场分类、申购日期、价格、规模等

### 🧠 智能分析
- **估值分析**: PE对比、价格评估、规模分析
- **风险评估**: 市场风险、价格风险、规模风险
- **投资建议**: 综合评分、申购建议、仓位管理

### 📱 通知推送
- **OpenClaw集成**: 直接在会话中发送通知
- **定时任务**: 每日自动分析推送
- **多种模式**: 每日分析、近期分析、单股分析

## 🚀 快速开始

### 安装依赖
```bash
pip3 install -r requirements.txt
```

### 测试连接
```bash
python3 main_fixed.py --test
```

### 执行每日分析
```bash
python3 main_fixed.py --daily
```

### 查看近期新股
```bash
python3 main_fixed.py --recent 7
```

## 📁 项目结构

```
new-stock-analyzer/
├── README.md                    # 项目说明
├── SKILL.md                    # 技能说明
├── requirements.txt            # Python依赖
├── main_fixed.py              # 修复版主程序（推荐）
├── main_enhanced.py           # 增强版主程序
├── main_simple.py             # 简化版主程序
├── stock_data_enhanced.py     # 增强版数据获取
├── stock_analyzer_detailed.py # 详细版分析器
├── stock_analyzer_enhanced.py # 增强版分析器
├── stock_analyzer.py          # 基础分析器
├── stock_data.py              # 基础数据获取
├── openclaw_notifier.py       # OpenClaw通知模块
├── multi_source_validator.py  # 多数据源验证器
├── ipo_data_validator.py      # IPO数据验证器
├── cfi_data_parser.py         # 中财网数据解析器
├── cfi_simple_parser.py       # 中财网简单解析器
├── scripts/                   # 脚本目录
│   ├── openclaw_daily.sh     # 每日推送脚本
│   ├── openclaw_daily_enhanced.sh # 增强版推送脚本
│   └── setup_cron.sh         # 定时任务设置脚本
├── config/                    # 配置目录
│   └── config.example.yaml   # 配置示例
├── data/                      # 数据目录
│   ├── cache/                # 数据缓存
│   └── logs/                 # 运行日志
└── tests/                     # 测试目录
    ├── test_basic.py         # 基础测试
    └── test_enhanced.py      # 增强测试
```

## 🔧 配置说明

### 无需外部配置
工具已简化，无需企业微信配置，通知直接在OpenClaw会话中发送。

### 定时任务配置
```bash
# 运行安装脚本
bash scripts/setup_cron.sh

# 或手动设置cron（默认10:00）
crontab -e
# 添加以下行：
0 10 * * * cd /path/to/new-stock-analyzer && bash scripts/openclaw_daily.sh
```

## 📊 输出示例

### 每日分析输出
```
📊 新股详细分析报告
时间: 2026-03-16 19:58:31
数量: 3只新股

📈 汇总统计
- 新股总数: 3只
- 建议申购: 2只
- 平均评分: 58.7/100

📋 详细分析
1. 悦龙科技(920188)
   市场: 北交所 | 申购: 2026-03-16
   价格: 14.04元 | 规模: 2199万股
   建议: 建议申购 (66.0/100)
```

## 🔒 数据可靠性

### 多数据源验证
- **东方财富**: 主数据源，实时更新
- **中财网**: 验证数据源，交叉验证
- **一致性**: 数据高度一致，可靠性高

### 数据验证标记
- ✅ 已验证（多数据源一致）
- ⚠️ 部分验证（单一数据源）
- ❌ 未验证（数据冲突）

## ⚡ 性能特点

### 快速响应
- 数据缓存机制，减少API调用
- 异步处理，提高响应速度
- 智能重试，网络异常自动恢复

### 稳定可靠
- 异常处理完善
- 日志记录详细
- 自动清理缓存

## 📈 更新日志

### v1.0.0 (2026-03-16)
- ✅ 基础功能开发完成
- ✅ 多数据源验证框架
- ✅ OpenClaw集成
- ✅ 定时任务支持
- ✅ 详细分析报告

## 🛡️ 风险提示

1. **投资有风险**，申购需谨慎
2. 工具分析仅供参考，不构成投资建议
3. 请结合自身风险承受能力做出决策
4. 定期更新工具以获取最新功能

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License