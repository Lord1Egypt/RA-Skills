# 招标项目分析技能

![Skill Logo](https://img.shields.io/badge/OpenClaw-Skill-blue)
![Version](https://img.shields.io/badge/Version-1.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

一个强大的招标项目分析和管理技能，帮助用户从招标文件中提取信息、管理数据库、并提供智能分析功能。

## ✨ 功能特点

### 📊 数据提取
- 从Excel/PDF招标文件中自动提取关键信息
- 支持多种招标文件格式
- 智能识别项目信息、时间节点、金额等

### 🗄️ 数据库管理
- 自动创建MySQL数据库和表结构
- 支持批量导入招标数据
- 数据验证和清洗功能

### 🔍 智能查询
- 多条件组合查询
- 统计分析功能
- 时间节点提醒
- 地理位置分析

### 📈 报告生成
- 自动生成招标分析报告
- 统计图表可视化
- 导出Excel/PDF报告

## 🚀 快速开始

### 安装要求
```bash
# 系统要求
- OpenClaw 2026.3.0+
- MySQL 8.0+
- Python 3.8+

# Python依赖
pip install pandas mysql-connector-python openpyxl
```

### 安装技能
```bash
# 通过ClawHub安装
clawhub install my-first-skill

# 或手动安装
git clone https://clawhub.com/skills/my-first-skill.git
cd my-first-skill
```

### 配置数据库
```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE bid_analysis_db;"

# 配置连接信息
编辑 config.json 文件：
{
  "mysql": {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "bid_analysis_db"
  }
}
```

## 📖 使用指南

### 基础使用
```bash
# 分析招标文件
openclaw skill my-first-skill analyze --file 招标文件.xlsx

# 导入数据库
openclaw skill my-first-skill import --file 招标文件.xlsx

# 查询项目
openclaw skill my-first-skill query --province 辽宁省
```

### 交互式使用
```
用户: 分析这个招标文件
技能: 正在分析文件...已提取10个关键信息字段

用户: 导入数据库
技能: 正在导入...成功导入1条记录到数据库

用户: 查询待办事项
技能: 找到3个待办事项，最近的是3月30日的获取招标文件截止
```

## 🗂️ 项目结构
```
my-first-skill/
├── SKILL.md                 # 技能主文档
├── README.md                # 项目说明
├── package.json             # 技能配置
├── config.json              # 配置文件
├── references/              # 参考文件
│   ├── excel-template.xlsx  # Excel模板
│   └── sample-data.json     # 示例数据
└── scripts/                 # 执行脚本
    ├── analyze.py           # 分析脚本
    ├── import.py            # 导入脚本
    └── query.py             # 查询脚本
```

## 🔧 配置说明

### 数据库配置
在 `config.json` 中配置MySQL连接：
```json
{
  "database": {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "bid_analysis_db",
    "charset": "utf8mb4"
  }
}
```

### 技能配置
```json
{
  "skill": {
    "name": "my-first-skill",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "招标项目分析技能",
    "triggers": ["招标", "投标", "项目分析", "数据库"],
    "category": "business"
  }
}
```

## 📊 数据模型

### 项目信息表 (project_bid_info)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 项目ID |
| project_name | VARCHAR(500) | 项目名称 |
| publish_date | DATE | 发布日期 |
| bid_unit | VARCHAR(200) | 招标单位 |
| bid_estimate | DECIMAL(15,2) | 招标估价 |
| winning_company | VARCHAR(200) | 中标公司 |
| winning_price | DECIMAL(15,2) | 中标价格 |
| province | VARCHAR(50) | 省 |
| city | VARCHAR(50) | 市 |
| county | VARCHAR(50) | 县 |
| project_level | VARCHAR(50) | 项目级别 |
| project_type | VARCHAR(100) | 项目类型 |
| project_analysis | TEXT | 项目分析 |
| market_suggestion | TEXT | 市场建议 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 时间节点表 (project_timeline)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 节点ID |
| project_id | INT | 项目ID |
| event_name | VARCHAR(100) | 事件名称 |
| event_date | DATETIME | 事件时间 |
| event_location | VARCHAR(200) | 事件地点 |
| remarks | TEXT | 备注 |
| status | VARCHAR(20) | 状态 |
| created_at | TIMESTAMP | 创建时间 |

## 🛠️ 开发指南

### 添加新功能
1. 在 `scripts/` 目录下创建新的Python脚本
2. 在 `SKILL.md` 中更新技能描述
3. 在 `package.json` 中更新版本号
4. 测试功能确保正常工作

### 测试技能
```bash
# 运行测试
python3 scripts/test_skill.py

# 测试数据库连接
python3 scripts/test_database.py

# 测试文件解析
python3 scripts/test_parser.py
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个技能！

### 开发流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 使用Python PEP 8代码风格
- 添加适当的注释
- 编写单元测试
- 更新相关文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与反馈

- 问题反馈: [GitHub Issues](https://github.com/yourusername/my-first-skill/issues)
- 功能建议: 提交Issue或Pull Request
- 文档改进: 欢迎贡献文档

## 🙏 致谢

感谢以下开源项目：
- [OpenClaw](https://openclaw.ai) - 提供技能平台
- [pandas](https://pandas.pydata.org) - 数据处理库
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) - MySQL连接器

---

**最后更新**: 2026年3月24日  
**版本**: 1.0.0  
**状态**: 稳定发布