# Longbridge API 配置

## 配置文件位置

配置文件会按以下优先级查找：

1. **环境变量**（最高优先级 - 最灵活）
   ```bash
   export LONGBRIDGE_CONFIG=/path/to/your/.longbridge_config
   ```

2. **相对路径**（从 skill 目录查找）
   - `<skill-dir>/.longbridge_config`（与 SKILL.md 同目录）
   - `<skill-dir>../../../.longbridge_config`（workspace 根目录）
   - `<skill-dir>../../../config/secrets/.longbridge_config`（如果使用 workspace 结构）
   - `<skill-dir>../../../scripts/.longbridge_config`（备用）

3. **用户主目录**（通用惯例）
   - `~/.longbridge_config`
   - `~/.config/longbridge/.longbridge_config`

**推荐位置:** `<skill-dir>/.longbridge_config` 或 `~/.longbridge_config`

## 必需字段

```bash
LONGPORT_APP_KEY=<你的App Key>
LONGPORT_APP_SECRET=<你的App Secret>
LONGPORT_ACCESS_TOKEN=<你的Access Token>
LONGPORT_REGION=cn           # cn = 中国大陆, hk = 香港, us = 美国
LONGPORT_HTTP_URL=https://openapi.longportapp.cn
LONGPORT_QUOTE_WS_URL=wss://openapi-quote.longportapp.cn
LONGPORT_TRADE_WS_URL=wss://openapi-trade.longportapp.cn
```

## 获取凭证

1. 访问 [长桥开放平台](https://open.longport.com/)
2. 创建应用，获取 App Key 和 App Secret
3. 获取 Access Token（用于交易和高级功能）

## 区域配置

根据你的地区选择接入点：

| 区域 | LONGPORT_REGION | HTTP URL |
|------|-----------------|----------|
| 中国大陆 | cn | https://openapi.longportapp.cn |
| 香港 | hk | https://openapi.longport.com.hk |
| 美国 | us | https://openapi.longport.com |

## 订阅权限

使用前请确认你的订阅权限：

- **美股**: Nasdaq Basic (免费) 或 LV1 实时行情 (付费)
- **港股**: LV1 实时行情
- **A股**: 需要单独订阅
- **期权**: 需要在 Quotes Store 购买

查看权限方法：
```bash
python3 -c "
from longport.openapi import Config, QuoteContext
from longport.openapi import QuotePermission, Market

config = Config(app_key='...', app_secret='...', access_token='...')
ctx = QuoteContext(config)
ctx.quote_permissions([Market.US, Market.HK, Market.CN])
"
```

## 依赖安装

```bash
pip3 install longport
```
