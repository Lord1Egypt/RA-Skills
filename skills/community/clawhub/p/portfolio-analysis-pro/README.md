# 持仓看盘系统 - 统一网页版

一个功能完整、易于使用的股票投资管理工具，提供网页界面，支持持仓管理、实时价格更新、盈亏分析和报告生成。

## 功能特性

- 📊 **持仓管理** - 增删改查持仓记录
- 🔄 **实时价格** - 自动更新股票价格（支持多个数据源）
- 📈 **数据分析** - 详细的盈亏统计和仓位分析
- 📋 **操作记录** - 完整的操作历史追溯
- 📄 **报告导出** - 生成Markdown格式的持仓报告
- 🌐 **局域网访问** - 支持多设备同时访问
- 📱 **响应式设计** - 适配PC、平板和手机

## 系统架构

```
portfolio-analysis/
├── portfolio_system.py      # 统一主程序
├── templates/
│   └── index.html          # 网页界面
├── portfolio.db            # SQLite数据库（自动创建）
├── reports/               # 报告输出目录（自动创建）
└── static/                # 静态资源目录（自动创建）
```

## 快速开始

### 1. 安装依赖

```bash
pip install flask requests flask-cors
```

### 2. 启动系统

```bash
python portfolio_system.py
```

### 3. 访问系统

启动后会显示访问地址：
- 本地访问：http://localhost:5000
- 局域网访问：http://<你的IP地址>:5000

## 使用说明

### 添加持仓

1. 点击右上角的"➕"按钮
2. 输入股票代码（如：600519）
3. 输入股票名称（可选，不填则自动获取）
4. 输入持仓数量和成本价
5. 点击"确认添加"

### 更新价格

- **手动更新**：点击左侧"更新价格"按钮
- **自动更新**：系统每5分钟自动更新一次

### 编辑持仓

1. 在持仓列表中点击"编辑"按钮
2. 选择要修改的字段（数量或成本价）
3. 输入新值
4. 点击"确认修改"

### 删除持仓

1. 在持仓列表中点击"删除"按钮
2. 确认删除操作

### 搜索持仓

在搜索框中输入股票名称或代码，实时过滤持仓列表。

## API接口

### 获取持仓数据
```
GET /api/portfolio
```

### 更新价格
```
POST /api/portfolio/update
```

### 新增持仓
```
POST /api/portfolio/add
Content-Type: application/json

{
  "symbol": "600519",
  "name": "贵州茅台",
  "quantity": 100,
  "cost_price": 1400.00
}
```

### 编辑持仓
```
PUT /api/portfolio/edit/<symbol>
Content-Type: application/json

{
  "field": "quantity",
  "value": 200
}
```

### 删除持仓
```
DELETE /api/portfolio/delete/<symbol>
```

### 获取操作记录
```
GET /api/portfolio/logs
```

### 生成报告
```
GET /api/portfolio/report
```

### 导出报告
```
GET /api/portfolio/export
```

## 数据库结构

### holdings 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| symbol | TEXT | 股票代码（唯一） |
| name | TEXT | 股票名称 |
| quantity | INTEGER | 持仓数量 |
| cost_price | REAL | 成本价 |
| current_price | REAL | 当前价格 |
| last_updated | TIMESTAMP | 最后更新时间 |
| created_at | TIMESTAMP | 创建时间 |

### operation_log 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| operation_type | TEXT | 操作类型 |
| symbol | TEXT | 股票代码 |
| details | TEXT | 操作详情 |
| created_at | TIMESTAMP | 创建时间 |

## 价格数据源

系统支持多个数据源，自动切换：
1. 新浪财经（优先）
2. 腾讯财经（备用）

## 配置选项

### 修改端口
在 `portfolio_system.py` 最后修改：
```python
start_server(host='0.0.0.0', port=5000, debug=False, auto_update=True)
```

### 修改自动更新间隔
在 `start_server` 函数中修改：
```python
manager.start_auto_update(interval_seconds=300)  # 300秒 = 5分钟
```

### 修改数据库路径
在 `PortfolioManager` 初始化时修改：
```python
manager = PortfolioManager('portfolio.db')  # 修改为你想要的路径
```

## 注意事项

1. **网络要求**：需要网络连接才能获取实时股票价格
2. **数据备份**：定期备份 `portfolio.db` 文件
3. **访问限制**：默认允许局域网访问，如需限制请修改 `host` 参数
4. **数据源限制**：部分股票可能无法获取实时价格

## 故障排除

### 无法获取股票价格
- 检查网络连接
- 确认股票代码格式正确
- 尝试手动更新

### 数据库错误
- 删除 `portfolio.db` 文件，重新启动系统
- 检查文件权限

### 端口被占用
- 修改启动端口
- 关闭占用5000端口的其他程序

## 技术栈

- **后端**：Python 3.6+
- **Web框架**：Flask
- **数据库**：SQLite
- **前端**：HTML5, CSS3, JavaScript
- **UI框架**：Bootstrap 5
- **图标**：Bootstrap Icons

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！

## 更新日志

### v1.0.0 (2026-03-25)
- 整合多个版本，创建统一系统
- 优化界面设计
- 支持多数据源价格获取
- 添加自动更新功能
- 完善操作记录
- 支持报告导出