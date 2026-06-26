---
name: infoxmed-qr-generator
description: Use when the user asks to generate infoxmed VIP membership activation QR codes, batch QR codes, or mentions infoxmed membership cards. Triggers on keywords like infoxmed, VIP QR, membership activation QR, member card QR code generation.
---

# Infoxmed VIP Membership QR Code Generator

## Overview

Extracts parameters from natural language input and calls the infoxmed batch QR code generation API, then saves the returned zip file locally.

## When to Use

- User asks to generate infoxmed VIP/membership activation QR codes
- User mentions keywords: infoxmed, VIP二维码, 会员激活二维码, 会员卡二维码

## Parameter Extraction Rules

From user input, extract and map these fields:

| User Input Field | API Parameter | Extraction Rule |
|---|---|---|
| 医院名称 / 机构 | `agent` | Format: `{商务渠道人}-{医院名称}`, e.g. `商务二部 蔡宏-宜兴市人民医院` |
| 时限 / 卡类型 | `cardName` | Extract core card name from input. Map: 月卡/季卡/半年卡/年卡/周卡. Strip "会员"/"会员卡" suffix, keep only `X卡` |
| 可扫码数量 / 次数 / 张数 | `times` | Extract number. If not specified and vipCarType=2, default `9999` |
| 绑定商务渠道人 / 商务 | (part of `agent`) | Combined into agent field as prefix before `-` |
| 扫码类型 | `vipCarType` | `2` if times > 1 or user specifies multi-use; `1` if one-time QR code. Default: infer from times |

**Fixed parameters:**
- `password`: Read from environment variable `INFOXMED_VIP_PASSWORD`. If not set, **stop and tell the user** to configure it (see Setup section below).
- `count`: `1`

## Password Check (MUST Run Before Every API Call)

First detect the platform, then check the environment variable using the platform-appropriate command:

**macOS / Linux:**
```bash
echo $INFOXMED_VIP_PASSWORD
```

**Windows (PowerShell):**
```powershell
echo $env:INFOXMED_VIP_PASSWORD
```

**If the variable is set (non-empty):** proceed with the API call.

**If the variable is empty or not set:** DO NOT call the API. Instead, run the following interactive setup flow:

1. Ask the user: "检测到 INFOXMED_VIP_PASSWORD 未配置，请提供你的接口密码，我来帮你自动配置。"
2. After the user provides the password, detect platform and shell, then persist the variable:

### macOS / Linux

```bash
# Detect shell profile
if [ -n "$ZSH_VERSION" ] || [[ "$SHELL" == */zsh ]]; then
  PROFILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [[ "$SHELL" == */bash ]]; then
  PROFILE="$HOME/.bashrc"
elif [[ "$SHELL" == */fish ]]; then
  PROFILE="$HOME/.config/fish/config.fish"
else
  PROFILE="$HOME/.profile"
fi

# Write to profile (fish uses different syntax)
if [[ "$SHELL" == */fish ]]; then
  echo 'set -gx INFOXMED_VIP_PASSWORD "USER_PROVIDED_PASSWORD"' >> "$PROFILE"
else
  echo '' >> "$PROFILE"
  echo '# Infoxmed VIP QR API password' >> "$PROFILE"
  echo 'export INFOXMED_VIP_PASSWORD="USER_PROVIDED_PASSWORD"' >> "$PROFILE"
fi

# Set for current session
export INFOXMED_VIP_PASSWORD="USER_PROVIDED_PASSWORD"
```

### Windows (PowerShell)

```powershell
# Set permanently for current user (persists across reboots)
[System.Environment]::SetEnvironmentVariable("INFOXMED_VIP_PASSWORD", "USER_PROVIDED_PASSWORD", "User")

# Set for current session
$env:INFOXMED_VIP_PASSWORD = "USER_PROVIDED_PASSWORD"
```

3. Confirm to the user: "已配置完成并在当前会话生效，后续无需再次配置。"
4. Then continue with the original QR code generation request.

## cardName Mapping Examples

| User says | cardName value |
|---|---|
| 半年会员卡 / 半年卡 / 半年 | 半年卡 |
| 月卡 / 月会员卡 / 一个月 | 月卡 |
| 季卡 / 季度卡 / 三个月 | 季卡 |
| 年卡 / 年会员卡 / 一年 | 年卡 |
| 周卡 / 周会员卡 / 一周 | 周卡 |

## vipCarType Logic

```
if times == 1 or user explicitly says "一次性":
    vipCarType = 1, times = 1
else:
    vipCarType = 2, times = user_specified or 9999
```

## Execution Steps

1. **Extract parameters** from user's natural language input using rules above
2. **Confirm parameters** - show extracted parameters to user before calling API
3. **Call API** — use platform-appropriate command:

**macOS / Linux:**
```bash
curl -s -o /tmp/vip_qr_{timestamp}.zip \
  "https://api.infox-med.com/system/batchGenerateVipQr?password=${INFOXMED_VIP_PASSWORD}&agent={url_encoded_agent}&count=1&cardName={url_encoded_cardName}&vipCarType={vipCarType}&times={times}" \
  -H "Origin: https://admin.infox-med.com" \
  -H "Referer: https://admin.infox-med.com/"
```

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://api.infox-med.com/system/batchGenerateVipQr?password=$env:INFOXMED_VIP_PASSWORD&agent={url_encoded_agent}&count=1&cardName={url_encoded_cardName}&vipCarType={vipCarType}&times={times}" `
  -Headers @{ "Origin" = "https://admin.infox-med.com"; "Referer" = "https://admin.infox-med.com/" } `
  -OutFile "$env:TEMP\vip_qr_{timestamp}.zip"
```

4. **Verify** the downloaded file is a valid zip
5. **Report** file path to user

## Missing Parameter Handling

If any required info is missing, ask the user. Required fields:
- 医院名称 (for agent)
- 商务渠道人 (for agent)
- 卡类型/时限 (for cardName)
- 可扫码数量 (for times, defaults to 9999 if truly unspecified for multi-use)

## Example

**User input:**
> 请生成二维码
> 医院名称：宜兴市人民医院
> 时限：半年会员卡
> 可扫码数量：1000次
> 绑定商务渠道人：商务二部 蔡宏

**Extracted parameters:**
- `agent` = `商务二部 蔡宏-宜兴市人民医院`
- `count` = `1`
- `cardName` = `半年卡`
- `vipCarType` = `2` (because times=1000 > 1)
- `times` = `1000`
- `password` = `${INFOXMED_VIP_PASSWORD}`

**API call:**
```
GET https://api.infox-med.com/system/batchGenerateVipQr?password=${INFOXMED_VIP_PASSWORD}&agent=商务二部%20蔡宏-宜兴市人民医院&count=1&cardName=半年卡&vipCarType=2&times=1000
```
