# OpenClaw 智能记账本

一个基于 OpenClaw 框架的个人财务管理技能，支持自然语言输入、自动分类和数据分析。

## 🎯 功能特性

- **自然语言记账** - 支持中文自然语言输入（"今天午饭花了35元"）
- **智能分类** - 自动识别餐饮、交通、购物、娱乐等类别
- **多维度统计** - 日/周/月支出分析和趋势报告
- **数据可视化** - 按类别和时间的支出分布图表
- **本地存储** - 数据安全保存在本地 JSON 文件
- **OpenClaw 集成** - 充分利用 OpenClaw 的消息处理能力

## 📖 使用指南

### 基本记账

```
记账：今天午饭花了35元
记录：打车花了25元
添加：超市购物120元
```

### 查询统计

```
查询：这个月花了多少钱
统计：本月支出
查询：本周消费情况
```

### 查看明细

```
列表：最近记录
明细：查看支出
```

## 🔧 技术实现

### 核心功能

1. **自然语言解析** - 使用正则表达式匹配金额和描述
2. **智能分类算法** - 基于关键词的类别识别
3. **数据统计引擎** - 多时间维度的支出分析
4. **本地数据存储** - JSON 格式的数据持久化

### 数据结构

```json
{
  "id": "timestamp",
  "amount": 35.0,
  "category": "餐饮",
  "description": "午饭",
  "date": "2026-03-08",
  "timestamp": 1772950000000
}
```

## 🚀 部署安装

### 方法一：通过 skillhub 安装

```bash
skillhub install openclaw-expense-tracker
openclaw skill run expense-tracker
```

### 方法二：本地开发

```bash
# 克隆或创建技能目录
mkdir openclaw-expense-tracker && cd openclaw-expense-tracker

# 安装依赖
npm install @openclaw/sdk

# 运行技能
node index.js
```

## 💡 使用场景

- **个人财务管理** - 记录日常开支，控制预算
- **旅行记账** - 跟踪旅行花费，优化行程安排
- **家庭理财** - 家庭成员共同管理家庭支出
- **创业记账** - 小微企业的基础财务记录
- **学习统计** - 分析消费习惯，培养理财意识

## 🛠️ 开发者文档

### API 参考

#### `parseExpense(text)`
解析自然语言文本，提取金额和分类信息

#### `addExpense(expense)`
添加新的记账记录到数据库

#### `getStatistics(period)`
获取指定时间周期的统计信息

### 扩展功能

- [ ] 收入记录支持
- [ ] 预算设置和提醒
- [ ] 数据导入导出
- [ ] 多用户支持
- [ ] 云同步功能

## 📝 更新日志

### v1.0.0 (当前版本)
- 基础记账功能
- 智能分类识别
- 多维度统计分析
- OpenClaw 原生集成

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request