# MT5 Trading Assistant 安装与设置指南

## 系统要求

### 软件要求
- **Python 3.7+** (推荐 3.10+)
- **MetaTrader 5 桌面客户端** (必须安装并运行)
- **MetaTrader5 Python 包**

### 网络要求
- 稳定的互联网连接
- MT5客户端必须连接到交易服务器
- API访问权限（需要开启自动交易）

## 安装步骤

### 1. 安装 Python 包

```bash
# 安装 MetaTrader5 Python 包
pip install MetaTrader5

# 可选：安装 pandas 用于数据分析
pip install pandas numpy
```

### 2. 配置 MT5 客户端

1. **启动 MT5 桌面客户端**
2. **登录您的交易账户**
3. **启用自动交易功能**:
   - 点击工具栏上的"自动交易"按钮（红绿灯图标 🔴→🟢）
   - 或按 **F7** 快捷键
   - 或通过菜单: 工具 → 选项 → 交易 → 勾选"允许自动交易"

4. **验证连接状态**:
   - 确保客户端显示"已连接"状态
   - 确认品种报价正常更新

### 3. 配置账户信息

1. **复制配置文件模板**:
   ```bash
   cp references/config_template.py config.py
   ```

2. **编辑配置文件** (`config.py`):
   ```python
   MT5_CONFIG = {
       "login": 12345678,              # 您的MT5账户号码
       "password": "your_password",    # 您的MT5账户密码
       "server": "YourServer",         # MT5服务器名称
       "symbol": "XAUUSD",             # 交易品种
   }
   ```

### 4. 测试安装

运行测试脚本验证安装:

```bash
# 测试MT5连接
python scripts/test_mt5_kline.py

# 测试账户信息
python scripts/mt5_check.py
```

## 常见问题解决

### 错误: "AutoTrading disabled by client"
**问题**: MT5自动交易功能未启用
**解决方案**:
1. 在MT5客户端启用自动交易
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

## 经纪商特定配置

### Exness
```python
MT5_CONFIG = {
    "login": 277528870,
    "password": "your_password",
    "server": "Exness-MT5Trial5",  # 模拟账户服务器
    "symbol": "XAUUSDm",           # Exness黄金品种
}
```

### IC Markets
```python
MT5_CONFIG = {
    "login": 12345678,
    "password": "your_password",
    "server": "ICMarkets-MT5",
    "symbol": "XAUUSD",            # 标准符号
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

## 性能优化

### 连接管理
```python
# 最佳实践：及时关闭连接
import MetaTrader5 as mt5

try:
    mt5.initialize()
    # 执行操作...
finally:
    mt5.shutdown()  # 确保总是关闭连接
```

### 错误处理
```python
import MetaTrader5 as mt5

def safe_execute(func):
    """安全执行MT5操作的装饰器"""
    def wrapper(*args, **kwargs):
        try:
            if not mt5.initialize():
                print("MT5初始化失败")
                return None
            return func(*args, **kwargs)
        except Exception as e:
            print(f"操作失败: {e}")
            return None
        finally:
            mt5.shutdown()
    return wrapper
```

## 故障排除

### 连接测试脚本
创建 `test_connection.py`:

```python
import MetaTrader5 as mt5
from config import MT5_CONFIG

print("测试MT5连接...")
if not mt5.initialize():
    print("❌ MT5初始化失败")
    exit()

print(f"登录账户 {MT5_CONFIG['login']}...")
if mt5.login(MT5_CONFIG['login'], MT5_CONFIG['password'], server=MT5_CONFIG['server']):
    print("✅ 登录成功")
    
    # 测试品种
    if mt5.symbol_select(MT5_CONFIG['symbol'], True):
        tick = mt5.symbol_info_tick(MT5_CONFIG['symbol'])
        if tick:
            print(f"✅ 品种 {MT5_CONFIG['symbol']} 报价正常")
            print(f"   买价: {tick.bid} | 卖价: {tick.ask}")
        else:
            print(f"❌ 无法获取 {MT5_CONFIG['symbol']} 报价")
    else:
        print(f"❌ 无法选择品种 {MT5_CONFIG['symbol']}")
else:
    print("❌ 登录失败")

mt5.shutdown()
print("测试完成")
```

## 下一步

安装完成后，您可以:
1. 运行 `python scripts/mt5_snapshot.py` 查看账户状态
2. 运行 `python scripts/mt5_buy.py 0.01` 测试买入功能
3. 创建自定义交易策略

如需帮助，请参考脚本中的文档注释或创建issue报告问题。