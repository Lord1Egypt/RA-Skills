# 配置说明

默认配置文件：`~/.config/ninebot-show-skill/config.json`。

## 字段

- `ninebot.sn`：必填。来自 `ninecli vehicles --json` 的 `wnumber`。
- `ninebot.full_range`：满电理论续航，单位 km，仅用于电量折算展示。
- `ninebot.vehicle_name`：报告中的车辆显示名。
- `ninebot.vehicle_model`：可选，用户自行填写的车型标签。
- `location`：天气城市，例如 `上海`。
- `timezone`：IANA 时区，例如 `Asia/Shanghai`。
- `privacy_mode`：`off` / `district` / `exact` / `coordinates`。
- `weather_enabled`：是否查询天气。

## 位置隐私模式

- `off`：不展示位置，不做逆地理编码。
- `district`：默认，只展示省/市/区县。
- `exact`：展示完整格式化地址。
- `coordinates`：只展示坐标，不调用逆地理编码。

## 凭据

九号账号密码不写入本 Skill。用户只在本机执行 `ninecli login`，由 `ninecli` 管理自己的登录令牌。

高德 Web 服务 Key 支持：

- `AMAP_WEBSERVICE_KEY`
- `AMAP_WEB_KEY`

优先从进程环境变量读取。也可以放到本机 `~/.config/ninebot-show-skill/.env`，或者通过 `NINEBOT_ENV_FILE` 指向单独的环境文件。真实 `.env` 不应进入公开 Skill 包。

其他可选环境变量：

- `NINEBOT_SHOW_CONFIG`：覆盖 Skill 配置文件路径。
- `NINEBOT_REPORT_CONFIG`：旧变量名，继续兼容。
- `NINEBOT_CONFIG_DIR`：覆盖 ninecli 配置目录。
- `NINECLI_BIN`：覆盖 ninecli 可执行文件路径；覆盖值必须解析为真实、可执行的普通文件。Skill 包装层仅允许只读子命令。
- `NINEBOT_OUTPUT_DIR`：图片输出目录；默认使用 `~/.local/share/ninebot-show-skill/`。
- `NINEBOT_MAP_PROXY`：OSM 瓦片可选代理，例如 `http://127.0.0.1:7890`；不设置则直连。

## Agent 识别目录

同一个 Skill 目录可直接放到不同 Agent 的标准位置：

- Claude Code：`~/.claude/skills/ninebot-show-skill/`
- Hermes：`~/.hermes/skills/ninebot-show-skill/`
- OpenClaw：`<workspace>/skills/ninebot-show-skill/`
- 通用 Agent Skills：`~/.agents/skills/ninebot-show-skill/`

`SKILL.md` 的 `name` 必须保持为 `ninebot-show-skill`，并与目录名一致。

## 公开包规则

不要把实际 `config.json`、`tokens.json`、HAR、`.env`、日志、缓存、真实骑行 ID 或 `.pyc` 打进压缩包。
