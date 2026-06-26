# 环境变量参考

所有 PinchTab 配置环境变量。

## 网络

| 变量 | 默认 | 描述 |
|---|---|---|
| `BRIDGE_BIND` | `127.0.0.1` | 绑定地址 |
| `BRIDGE_PORT` | `9867` | 监听端口 |
| `BRIDGE_TOKEN` | 无 | API 认证令牌 |

## 浏览器

| 变量 | 默认 | 描述 |
|---|---|---|
| `BRIDGE_HEADLESS` | `true` | 无头模式 |
| `BRIDGE_PROFILE` | 默认配置文件 | 配置文件路径 |
| `BRIDGE_CHROME_PATH` | 自动检测 | Chrome 可执行文件路径 |
| `BRIDGE_BLOCK_IMAGES` | `false` | 阻止图片加载 |

## 会话

| 变量 | 默认 | 描述 |
|---|---|---|
| `BRIDGE_NO_RESTORE` | `false` | 禁用会话恢复 |
| `BRIDGE_NO_SANDBOX` | `false` | 禁用 Chrome 沙箱 |

## 日志

| 变量 | 默认 | 描述 |
|---|---|---|
| `BRIDGE_LOG_LEVEL` | `info` | 日志级别 (debug, info, warn, error) |
| `BRIDGE_LOG_FILE` | 无 | 日志文件路径 |

## 示例

```bash
# 完整配置
BRIDGE_BIND=127.0.0.1 \
BRIDGE_PORT=9867 \
BRIDGE_TOKEN="my-secret" \
BRIDGE_HEADLESS=true \
BRIDGE_PROFILE=~/.pinchtab/auto \
BRIDGE_BLOCK_IMAGES=true \
BRIDGE_LOG_LEVEL=debug \
pinchtab &
```
