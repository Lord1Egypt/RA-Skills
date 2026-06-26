# MT5 Trading Assistant Skill - 安装指南

## 技能概述

MT5 Trading Assistant 是一个完整的 MetaTrader 5 自动化交易技能，提供：

- ✅ 账户监控与状态检查
- ✅ 买入/卖出订单执行
- ✅ 持仓管理与平仓操作
- ✅ 实时行情监控
- ✅ K线数据获取
- ✅ 风险管理工具

## 系统要求

### 软件要求
- **Python 3.7+** (推荐 3.10+)
- **MetaTrader 5 桌面客户端** (必须安装并运行)
- **MetaTrader5 Python 包**: `pip install MetaTrader5`
- **OpenClaw** (运行环境)

### 网络要求
- 稳定的互联网连接
- MT5客户端必须连接到交易服务器
- API访问权限（需要开启自动交易）

## 安装步骤

### 步骤 1: 安装 Python 依赖

```bash
# 安装 MetaTrader5 Python 包
pip install MetaTrader5

# 可选：安装数据分析包
pip install pandas numpy
```

### 步骤 2: 配置 MT5 客户端

1. **启动 MT5 桌面客户端**
2. **登录您的交易账户**
3. **启用自动交易功能**:
   - 点击工具栏上的"自动交易"按钮（红绿灯图标 🔴→🟢）
   - 或按 **F7** 快捷键
   - 或通过菜单: 工具 → 选项 → 交易 → 勾选"允许自动交易"

4. **验证连接状态**:
   - 确保客户端显示"已连接"状态
   - 确认品种报价正常更新

### 步骤 3: 安装 OpenClaw 技能

#### 方法 A: 通过 .skill 文件安装 (推荐)

1. **复制技能文件到 OpenClaw 技能目录**:
   ```bash
   # Windows 默认技能目录
   copy mt5-trading-assistant.skill "%USERPROFILE%\.agents\skills\"
   
   # 或 Linux/Mac
   cp mt5-trading-assistant.skill ~/.agents/skills/
   ```

2. **刷新技能列表**:
   ```bash
   openclaw skills refresh
   ```

3. **验证技能安装**:
   ```bash
   openclaw skills list | grep mt5
   ```

#### 方法 B: 通过技能目录安装

1. **复制技能目录**:
   ```bash
   # 复制整个目录到技能文件夹
   xcopy /E mt5-trading-assistant "%USERPROFILE%\.agents\skills\mt5-trading-assistant\"
   ```

2. **重启 OpenClaw**:
   ```bash
   openclaw gateway restart
   ```

### 步骤 4: 配置账户信息

#### 方式 1: 直接修改脚本 (简单)

编辑脚本文件中的配置部分：

```python
# 在 scripts/mt5_buy.py, scripts/mt5_sell.py 等文件中修改
ACCOUNT_CONFIG = {
    "login": YOUR_ACCOUNT_NUMBER,      # 您的MT5账户号码
    "password": "YOUR_PASSWORD",       # 您的MT5账户密码
    "server": "YOUR_SERVER",           # MT5服务器名称
    "symbol": "YOUR_SYMBOL",           # 交易品种
}
```

#### 方式 2: 使用配置文件 (推荐)

1. **创建配置文件**:
   ```bash
   # 从模板创建配置文件
   cp references/config_template.py config.py
   ```

2. **编辑配置文件** (`config.py`):
   ```python
   MT5_CONFIG = {
       "login": 12345678,              # 您的MT5账户号码
       "password": "your_password",    # 您的MT5账户密码
       "server": "YourServer",         # MT5服务器名称
       "symbol": "XAUUSD",             # 交易品种
       "default_volume": 0.01,         # 默认手数
       "default_magic": 100000,        # 默认订单魔法号
   }
   ```

3. **修改脚本以使用配置文件**:
   在每个脚本中添加:
   ```python
   try:
       from config import MT5_CONFIG
       ACCOUNT_CONFIG.update(MT5_CONFIG)
   except ImportError:
       print("NOTE: config.py not found, using default configuration")
   ```

### 步骤 5: 测试安装

运行测试脚本验证安装:

```bash
# 测试MT5连接和K线数据
python scripts/test_mt5_kline.py

# 测试账户状态检查
python scripts/mt5_check.py

# 测试市场快照
python scripts/mt5_snapshot.py
```

## 经纪商特定配置

### Exness (示例)
```python
MT5_CONFIG = {
    "login": 277528870,
    "password": "your_password",
    "server": "Exness-MT5Trial5",      # 模拟账户服务器
    "symbol": "XAUUSDm",               # Exness黄金品种带'm'后缀
}
```

### IC Markets
```python
MT5_CONFIG = {
    "login": 12345678,
    "password": "your_password",
    "server": "ICMarkets-MT5",
    "symbol": "XAUUSD",                # 标准符号
}
```

### Pepperstone
```python
MT5_CONFIG = {
    "login": 12345678,
    "password": "your_password",
    "server": "Pepperstone-MT5",
    "symbol": "XAUUSD",
}
```

## 使用技能

### 在 OpenClaw 中使用

技能会自动触发以下关键词:
- **MT5**, **MetaTrader 5**
- **trading automation**, **forex trading**
- **gold trading**, **XAUUSD**
- **automated trading**, **trading bot**
- **execute trade**, **buy/sell orders**
- **close positions**, **stop loss/take profit**
- **account monitoring**, **real-time quotes**

### 直接运行脚本

```bash
# 查看账户状态
python scripts/mt5_check.py

# 获取市场快照
python scripts/mt5_snapshot.py

# 买入0.01手
python scripts/mt5_buy.py 0.01

# 卖出0.02手
python scripts/mt5_sell.py 0.02

# 平仓所有脚本订单
python scripts/mt5_close_all.py

# 测试K线数据
python scripts/test_mt5_kline.py
```

## 常见问题解决

### 错误: "AutoTrading disabled by client"
**问题**: MT5自动交易功能未启用
**解决方案**:
1. 在MT5客户端启用自动交易 (F7或工具栏按钮)
2. 确保EA交易权限已开启
3. 重启MT5客户端后重试

### 错误: "Initialize failed"
**问题**: MT5客户端未运行或版本不兼容
**解决方案**:
1. 确保MT5桌面客户端正在运行
2. 确认已登录交易账户
3. 检查MT5版本（需要Build 2500+）

### 错误: "Invalid symbol"
**问题**: 品种名称不正确
**解决方案**:
1. 检查品种名称是否存在于MT5客户端
2. 注意经纪商特定后缀（如Exness的`XAUUSDm`）
3. 在MT5客户端中右键品种 → "交易"启用

### 错误: "Login failed"
**问题**: 账户信息错误
**解决方案**:
1. 确认账户号码、密码、服务器名称正确
2. 检查账户是否被锁定
3. 验证服务器连接状态

## 安全最佳实践

### 密码安全
1. **不要硬编码密码** - 使用配置文件或环境变量
2. **使用强密码** - 包含大小写字母、数字、特殊字符
3. **定期更换密码** - 每30-90天更换一次

### 文件安全
1. **保护配置文件** - 设置适当的文件权限
2. **避免提交敏感信息** - 将`config.py`添加到`.gitignore`
3. **使用环境变量** (推荐):
   ```python
   import os
   MT5_CONFIG = {
       "login": os.getenv("MT5_LOGIN"),
       "password": os.getenv("MT5_PASSWORD"),
       "server": os.getenv("MT5_SERVER"),
   }
   ```

### 交易安全
1. **先模拟后实盘** - 在模拟账户充分测试
2. **设置止损** - 每笔交易都要设置止损
3. **风险管理** - 单笔风险不超过账户的2%

## 技能文件结构

```
mt5-trading-assistant/
├── SKILL.md                    # 技能主文档
├── scripts/                    # 可执行脚本
│   ├── mt5_buy.py             # 买入订单脚本
│   ├── mt5_sell.py            # 卖出订单脚本
│   ├── mt5_close_all.py       # 平仓管理脚本
│   ├── mt5_check.py           # 账户检查脚本
│   ├── mt5_snapshot.py        # 市场快照脚本
│   └── test_mt5_kline.py      # K线测试脚本
├── references/                 # 参考文档
│   ├── config_template.py     # 配置文件模板
│   └── setup_guide.md         # 详细设置指南
└── assets/                    # 资源文件 (可选)
```

## 更新与维护

### 更新技能
```bash
# 1. 下载新版本技能文件
# 2. 备份原有配置
# 3. 替换技能文件
# 4. 刷新技能列表
openclaw skills refresh
```

### 备份配置
```bash
# 备份配置文件
cp config.py config.py.backup

# 备份交易记录 (如果适用)
```

## 技术支持

如有问题，请:
1. 查看 `references/setup_guide.md` 中的详细说明
2. 检查MT5客户端连接状态
3. 验证账户配置信息
4. 查看技能文档中的常见问题部分

## 许可证

本技能遵循 MIT 许可证。详见 LICENSE 文件。

## 免责声明

本技能仅供学习和研究使用。交易有风险，使用前请充分了解相关风险。开发者不对任何交易损失负责。