# mijia-fan

Xiaomi 米家风扇控制 Skill，支持开/关/调速/摆风，兼容所有 AI 工具调用。

## 功能

- ✅ 开/关风扇
- ✅ 切换风扇状态
- ✅ 查看风扇状态
- ✅ 调节风速（0-100）
- ✅ 控制摆风
- ✅ 列出所有米家设备

## 安装

```bash
# 通过 ClawHub 安装
clawhub install mijia-fan

# 或本地安装
cd ~/.qclaw/skills/mijia-fan
bash install.sh
```

## 使用方法

```bash
cd ~/.qclaw/skills/mijia-fan
source .venv/bin/activate
export MIJIA_FAN_DID="<你的风扇 DID>"

python scripts/fan_cli.py on       # 开风扇
python scripts/fan_cli.py off      # 关风扇
python scripts/fan_cli.py toggle   # 切换
python scripts/fan_cli.py status   # 查看状态
python scripts/fan_cli.py speed 50 # 风速 50
python scripts/fan_cli.py swing on # 摆风开
python scripts/fan_cli.py list     # 列出设备
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| MIJIA_FAN_DID | 必填 | 风扇设备 DID |
| MIJIA_FAN_SIID | 2 | 属性服务 ID |
| MIJIA_FAN_POWER_PIID | 1 | 电源属性 ID |
| MIJIA_FAN_SPEED_PIID | 2 | 风速属性 ID |
| MIJIA_FAN_SWING_PIID | 5 | 摆风属性 ID |

## 触发词

- "开风扇" → 开启
- "关风扇" → 关闭
- "风扇状态" → 查看状态
- "风速 XX" → 调节风速
- "打开摆风" → 开启摆风

## 依赖

- Python 3.8+
- mijiaAPI

## 作者

Bob
