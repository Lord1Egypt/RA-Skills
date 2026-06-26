---
name: new-stock-analyzer
description: 免费、实时、全面的A股新股分析工具。支持双数据源（东方财富+中财网），提供今日新股查询、基本面分析、风险评估、申购建议，直接在OpenClaw会话中发送通知。
version: 1.0.0
author: 佑安 (Aegis)
contact:
  email: support@openclaw.ai
metadata:
  openclaw:
    requires:
      bins: ["python3", "pip3"]
      packages: ["requests", "pandas", "pyyaml", "python-dotenv", "beautifulsoup4", "lxml"]
    commands:
      - /newstock - 查询今日新股
      - /newstock_weekly - 查询本周新股日历
      - /newstock_test - 测试连接和配置
      - /newstock_setup - 设置定时推送
tags:
  - 股票
  - 新股
  - 投资
  - 分析
  - A股
  - 免费
---

# 新股分析工具 (New Stock Analyzer)

## 🎯 核心功能

### 📊 数据获取
- **双数据源验证**: 东方财富（主）+ 中财网（验证），确保数据准确性
- **实时更新**: 自动获取最新新股申购信息
- **完整信息**: 市场分类、申购日期、发行价格、发行规模、申购上限等

### 🧠 智能分析
- **估值分析**: PE对比分析、价格评估、规模分析
- **风险评估**: 市场风险、价格风险、规模风险评估
- **投资建议**: 综合评分模型、申购建议、仓位管理指导

### 📱 通知推送
- **OpenClaw原生集成**: 直接在OpenClaw会话中发送通知
- **定时任务**: 每日自动分析并推送结果
- **多种分析模式**: 支持每日分析、近期分析、单股深度分析

## 🚀 快速开始

### 安装依赖
```bash
# 进入项目目录
cd new-stock-analyzer

# 安装Python依赖
pip3 install -r requirements.txt
```

### 配置定时任务（无需外部配置）
1. 工具已简化，无需企业微信配置
2. 通知直接在OpenClaw会话中发送
3. 只需设置cron定时任务即可

### 设置定时任务
```bash
# 运行安装脚本
bash scripts/setup_cron.sh

# 或手动设置cron（默认10:00）
crontab -e
# 添加以下行：
0 10 * * * cd /path/to/new-stock-analyzer && bash scripts/openclaw_daily.sh
```

### 手动测试
```bash
# 测试连接
python3 main_fixed.py --test

# 执行每日分析（不发送通知）
python3 main_fixed.py --daily --no-print

# 执行每日分析并发送通知
python3 main_fixed.py --daily

# 执行近期分析（7天内）
python3 main_fixed.py --recent 7
```

## 📁 项目结构

```
new-stock-analyzer/
├── README.md                    # 项目说明
├── SKILL.md                    # 技能说明（本文件）
├── requirements.txt            # Python依赖
├── main_fixed.py              # 修复版主程序（推荐）
├── main_enhanced.py           # 增强版主程序
├── main_simple.py             # 简化版主程序
├── stock_data_enhanced.py     # 增强版数据获取模块
├── stock_analyzer_detailed.py # 详细版分析器
├── stock_analyzer_enhanced.py # 增强版分析器
├── stock_analyzer.py          # 基础分析器
├── stock_data.py              # 基础数据获取模块
├── openclaw_notifier.py       # OpenClaw会话通知模块
├── multi_source_validator.py  # 多数据源验证器
├── ipo_data_validator.py      # IPO数据验证器
├── cfi_data_parser.py         # 中财网数据解析器
├── cfi_simple_parser.py       # 中财网简单解析器
├── scripts/                   # 脚本目录
│   ├── openclaw_daily.sh     # OpenClaw每日推送脚本
│   ├── openclaw_daily_enhanced.sh # 增强版推送脚本
│   └── setup_cron.sh         # 定时任务设置脚本
├── config/                    # 配置目录
│   └── config.example.yaml   # 配置示例
├── data/                      # 数据目录
│   ├── cache/                # 数据缓存
│   └── logs/                 # 运行日志
└── tests/                     # 测试目录
    ├── test_basic.py         # 基础功能测试
    └── test_enhanced.py      # 增强功能测试
```

## 🔧 增强版功能

### 详细版分析器
- **市场分类细化**: 沪市主板、深市主板、创业板、科创板、北交所
- **时间信息完整**: 申购日期、上市日期、中签公布日期
- **价格信息详细**: 发行价格、发行市盈率、行业市盈率、募集资金总额

### 多数据源验证
- **数据可靠性**: 使用中财网交叉验证东方财富数据
- **一致性检查**: 自动检查数据源间的一致性
- **验证标记**: 标记数据的验证状态和可靠性

### 智能分析引擎
- **综合评分模型**: 多维度评分（估值、风险、市场）
- **投资建议**: 申购建议、信心等级、仓位管理
- **风险提示**: 识别风险因素，提供风险等级

## ⚡ 使用示例

### 查询今日新股
```bash
python3 main_fixed.py --daily
```

输出示例：
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

### 查询近期新股
```bash
python3 main_fixed.py --recent 7
```

### 测试数据连接
```bash
python3 main_fixed.py --test
```

## 🔒 安全与隐私

### 数据安全
- 不存储用户敏感信息
- 所有数据均为公开市场数据
- 数据传输使用HTTPS加密

### 隐私保护
- 不收集用户个人信息
- 不记录用户投资行为
- 所有分析在本地完成

## 📈 性能优化

### 缓存机制
- API响应缓存，减少网络请求
- 智能缓存过期，确保数据新鲜度
- 自动清理旧缓存，节省磁盘空间

### 错误处理
- 网络异常自动重试
- API错误友好提示
- 详细日志记录，便于排查问题

### 资源管理
- 内存使用优化，支持长期运行
- 磁盘空间管理，自动清理日志
- CPU使用优化，不影响系统性能

## 🛠️ 开发指南

### 代码结构
- 模块化设计，易于扩展
- 清晰的接口定义
- 完善的错误处理

### 测试覆盖
- 单元测试覆盖核心功能
- 集成测试验证数据流程
- 性能测试确保稳定性

### 代码规范
- PEP 8代码风格
- 类型注解提高可读性
- 文档字符串完善

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License

## 📞 支持与反馈

如有问题或建议，请通过以下方式联系：
- Email: support@openclaw.ai
- GitHub Issues: 提交问题报告

## 🎉 致谢

感谢所有贡献者和用户的支持！

---

**版本**: 1.0.0  
**更新日期**: 2026-03-16  
**作者**: 佑安 (Aegis)  
**签名**: 🛡️ 佑你事业顺利，保你万事平安