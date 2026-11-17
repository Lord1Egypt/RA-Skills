---
name: mijia-fan
description: Xiaomi 米家风扇控制 Skill。支持开/关/调速/摆风，兼容所有 AI 工具调用。触发词：风扇、开风扇、关风扇、风扇开关。
version: 1.0.0
author: Bob
license: MIT
invocable: true

metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - MIJIA_FAN_DID
    optional:
      env:
        - MIJIA_FAN_SIID
        - MIJIA_FAN_POWER_PIID
        - MIJIA_FAN_SPEED_PIID
        - MIJIA_FAN_SWING_PIID
    install:
      - id: python3
        kind: system
        formula: python3
      - id: mijiaAPI
        kind: pip
        formula: mijiaAPI
---

# mijia-fan — Xiaomi 米家风扇控制 Skill

通用风扇控制接口，支持开/关/调速/摆风，可被任何 AI 工具通过标准化方式调用。

## 安装

```bash
# 方式 A：本地 zip 安装（推荐）
unzip mijia-fan.zip -d ~/.qclaw/skills/
cd ~/.qclaw/skills/mijia-fan
bash install.sh                    # 自动创建虚拟环境并安装依赖

# 方式 B：手动安装
cd ~/.qclaw/skills/mijia-fan
python3 -m venv .venv
source .venv/bin/activate
pip install mijiaAPI
```

## 快速开始

```bash
cd ~/.qclaw/skills/mijia-fan
source .venv/bin/activate
export MIJIA_FAN_DID="812221072"  # 你的风扇 DID

python scripts/fan_cli.py on       # 开
python scripts/fan_cli.py off      # 关
python scripts/fan_cli.py toggle   # 切换
python scripts/fan_cli.py status  # 状态
python scripts/fan_cli.py speed 50  # 风速 50
python scripts/fan_cli.py swing on  # 摆风开
python scripts/fan_cli.py list     # 列出所有设备
```

## 命令速查

| 命令 | 说明 |
|------|------|
| `fan_cli.py on` | 开风扇 |
| `fan_cli.py off` | 关风扇 |
| `fan_cli.py toggle` | 切换开关 |
| `fan_cli.py status` | 查看当前状态 |
| `fan_cli.py speed 1-100` | 设置风速（0=关） |
| `fan_cli.py swing on/off` | 摆风开关 |
| `fan_cli.py list` | 列出所有米家设备 |

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MIJIA_FAN_DID` | **必填** | 风扇设备 DID（运行 `list` 查看） |
| `MIJIA_FAN_SIID` | `2` | 属性服务 ID，一般不需改 |
| `MIJIA_FAN_POWER_PIID` | `1` | 电源属性 ID |
| `MIJIA_FAN_SPEED_PIID` | `2` | 风速属性 ID |
| `MIJIA_FAN_SWING_PIID` | `5` | 摆风属性 ID |

## 自然语言 → 命令映射

当用户说以下内容时，执行对应命令：

| 用户说法 | 执行命令 |
|----------|----------|
| 打开风扇/开风扇 | `fan_cli.py on` |
| 关闭风扇/关风扇 | `fan_cli.py off` |
| 风扇开关/切换风扇 | `fan_cli.py toggle` |
| 风扇状态/风扇开着吗 | `fan_cli.py status` |
| 风扇调速/风速设为XX | `fan_cli.py speed XX` |
| 打开摆风/关闭摆风 | `fan_cli.py swing on/off` |
| 列出风扇/查看风扇设备 | `fan_cli.py list` |

## 执行流程（AI 工具通用）

1. 切换目录：`cd ~/.qclaw/skills/mijia-fan`
2. 激活虚拟环境：`source .venv/bin/activate`
3. 执行命令：`python scripts/fan_cli.py <command>`
4. 检查返回码，报告结果

## 常见问题

**Q: 怎么找风扇的 DID？**
```bash
python scripts/fan_cli.py list
```
在输出中找到风扇设备，复制其 DID 设置到环境变量。

**Q: 权限/登录过期？**
米家 API 通过小米账号授权，首次运行会弹出二维码扫码登录。Token 有效期约 30 天，过期后重新扫码即可。

**Q: 命令无输出或报 code != 0？**
检查设备 ID 是否正确，设备是否在线，或重试登录授权。
