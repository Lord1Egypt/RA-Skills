# infoxmed-qr-generator

Generate Infoxmed VIP membership activation二维码 in批量模式 directly from natural-language instructions.

## Features
- 解析医院、商务渠道人、卡类型、扫码次数等参数
- 自动校验并配置 `INFOXMED_VIP_PASSWORD`
- 调用 `https://api.infox-med.com/system/batchGenerateVipQr` 批量生成激活二维码并保存为压缩包
- 生成过程前先回显参数，方便复核

## Prerequisites
1. 可用的 Infoxmed 接口密码，写入环境变量 `INFOXMED_VIP_PASSWORD`
2. Linux/macOS: `curl`
3. Windows (PowerShell): `Invoke-WebRequest`

## Usage
1. 在对话中提供以下信息：
   - 医院名称
   - 绑定商务渠道人
   - 时限 / 会员卡类型（例：半年卡、季卡）
   - 可扫码数量（次数 >1 视为多次扫码 `vipCarType=2`）
2. 技能会解析参数 => 回显确认 => 触发 API 调用。
3. 生成的 zip 文件默认保存到 `/tmp/vip_qr_<timestamp>.zip`（Linux/macOS）或 `%TEMP%\\vip_qr_<timestamp>.zip`（Windows）。

## Output
- `agent`：`商务渠道人-医院名称`
- `cardName`：标准化卡名（周/月/季/半年/年卡）
- `vipCarType` 与 `times`
- zip 文件路径

## Notes
- 若用户未提供次数而选择多次扫码，默认 `times=9999`
- 任何缺失字段都会提示补充，避免生成错误数据
- 修改/追加新卡种时，只需更新 `cardName Mapping` 表和逻辑
