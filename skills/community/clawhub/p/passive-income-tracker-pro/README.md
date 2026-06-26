# Passive-Income-Tracker 📊

> 一站式被动收入管理仪表板，让你的每一分钱都清晰可见

## ✨ 特性

- 🔗 **多平台整合**: 自动同步 15+ 收入平台数据
- 📈 **实时追踪**: 收入数据自动更新，随时掌握财务状况
- 🎯 **智能分类**: AI 自动 categorize 收入来源
- 🔮 **财务预测**: 基于历史数据的智能预测
- 📑 **税务报告**: 一键生成税务所需报告
- 🏆 **目标管理**: 设定和追踪财务自由目标
- 🔒 **安全加密**: 银行级数据加密保护

## 🚀 快速开始

### 安装

```bash
clawhub install passive-income-tracker
```

### 基础使用

```bash
# 查看本月收入概览
clawhub run passive-income-tracker overview

# 同步所有平台数据
clawhub run passive-income-tracker sync

# 查看收入趋势
clawhub run passive-income-tracker trends --period year

# 生成月度报告
clawhub run passive-income-tracker report --period month
```

### 高级功能

```bash
# 财务预测
clawhub run passive-income-tracker forecast --months 12

# 税务报告
clawhub run passive-income-tracker tax-report --year 2026

# 导出 CSV
clawhub run passive-income-tracker export --format csv

# 设定目标
clawhub run passive-income-tracker goal --monthly 5000
```

## 📋 支持的平台

| 平台 | 自动同步 | 数据延迟 |
|------|---------|---------|
| Gumroad | ✅ | 实时 |
| Patreon | ✅ | 1 小时 |
| YouTube AdSense | ✅ | 24 小时 |
| Amazon Associates | ✅ | 24 小时 |
| Teachable | ✅ | 1 小时 |
| Udemy | ✅ | 24 小时 |
| Stripe | ✅ | 实时 |
| PayPal | ✅ | 实时 |
| Ko-fi | ✅ | 1 小时 |
| Buy Me a Coffee | ✅ | 1 小时 |
| Substack | ✅ | 24 小时 |
| 博客广告 | ✅ | 24 小时 |
| 联盟营销 | ✅ | 24 小时 |
| 数字产品 | ✅ | 实时 |
| 手动导入 | ✅ | - |

## 🎨 仪表板视图

### 概览视图
- 本月总收入
- 月度增长百分比
- 最佳收入来源
- 距离目标进度

### 趋势视图
- 收入增长曲线
- 平台贡献对比
- 季节性分析
- 同比/环比数据

### 预测视图
- 下月收入预测
- 年度收入预测
- 达成目标时间
- 增长建议

### 税务视图
- 应税收入汇总
- 分类支出追踪
- 预估税额
- 税务报告导出

## 💡 使用技巧

1. **定期同步**: 设置每日自动同步，保持数据最新
2. **分类检查**: 定期检查 AI 分类准确性
3. **目标设定**: 设定实际可达的阶段性目标
4. **报告备份**: 每月导出报告作为备份
5. **税务规划**: 季度生成税务报告，避免年底手忙脚乱

## 📊 分析功能

### 收入分析
- 按平台分解
- 按产品类型分解
- 按时间趋势分析
- 异常检测

### 增长分析
- 增长率计算
- 增长驱动因素
- 瓶颈识别
- 优化建议

### 预测模型
- 基于历史趋势
- 考虑季节性因素
- 纳入市场变量
- 置信区间显示

## 🔐 安全与隐私

- **本地加密**: 所有数据 AES-256 加密存储
- **API 安全**: 使用只读 API 密钥
- **无云同步**: 数据仅存储本地
- **定期备份**: 支持自动备份到指定位置
- **隐私优先**: 不上传任何财务数据

## 📱 通知提醒

可配置的提醒功能：
- 新收入到账通知
- 目标达成提醒
- 异常波动警报
- 税务截止日期提醒
- 定期报告生成提醒

## 📝 更新日志

### v1.0.0
- 首次发布
- 15+ 平台支持
- 基础分析功能
- 财务预测
- 税务报告

## 🤝 贡献

欢迎提交新功能建议和平台集成请求！

## 📄 许可证

MIT License

---

**掌控你的被动收入，迈向财务自由！** 💰
