# 隐私与公开发布说明

本发布包按以下规则整理：

- 不包含真实手机号、九号账号密码、验证码、Token、Cookie、UID/MID、device-id。
- 不包含真实车辆 SN、序列号、VIN/车架号、蓝牙 MAC、蓝牙密钥。
- 不包含私人 GPS 坐标、家庭/公司地址、真实骑行轨迹、真实 `travel_id` 或个人服务实例 ID。
- 不包含 HAR、`tokens.json`、真实 `config.json`、真实 `.env`、日志、缓存或 `.pyc`。
- 所有公开示例均来自 `references/example-data.md`；位置使用公共地标东方明珠，其他标识使用明确声明的演示占位值。
- `templates/config.example.json` 是待填写模板；`templates/config.demo.json` 仅用于展示，不能直接作为真实车辆配置。

## 发布前检查

1. 检查压缩包中不存在 `.env`、HAR、日志、缓存、`config.json`、`tokens.json`、`.pyc`、`.git`。
2. 搜索手机号、真实 SN/VIN/MAC、UID/MID、device-id、Token/Cookie、经纬度和骑行 ID。
3. 确认只保留 `references/example-data.md` 中允许公开的示例值。
4. 确认 `SKILL.md` 的 `name` 与目录名 `ninebot-show-skill` 一致。

## 网络请求检查

- 检查代码中所有 `http://` / `https://` 字符串以及 `params` / `urlencode` / URL 拼接。
- 不在错误信息、日志或默认 JSON 中回显含 Key、Token、精确坐标、SN、骑行 ID 的完整 URL。
- 发布前对 ZIP 本体再扫描 UUID、手机号、长十六进制/Base64/JWT、长数字、MAC、IP、query string 和隐藏文件。
