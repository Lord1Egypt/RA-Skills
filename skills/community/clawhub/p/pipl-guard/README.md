# 🛡️ pipl-guard — PIPL 运行时护栏

在 AI 应用的输入/输出链路中**实时**检测个人信息，按风险分级脱敏或阻断，
供 Agent 主动调用。区别于事后审计，这是**事中防护**。

纯本地运行，零网络请求，零动态执行。

## 安装

```bash
openclaw skill install pipl-guard
```

## 用法

```bash
# 检测并脱敏（默认）
python3 scripts/guard.py --text "我的身份证是110101199003074477"

# 管道 / Agent 调用
echo "手机号13800138000" | python3 scripts/guard.py --stdin --format json

# 高危阻断
python3 scripts/guard.py --text "身份证110101199003074477" --action block

# 列出规则包
python3 scripts/guard.py --list-profiles
```

## 动作

| 动作 | 行为 |
|------|------|
| `detect` | 仅检测并报告，不改动文本 |
| `mask` | 脱敏后放行（默认） |
| `block` | 命中达阈值则阻断，否则脱敏 |

默认脱敏放行、仅 `high` 级阻断，阈值由 `--block-on` 调整。

## 检测范围（common v1.0.0）

身份证、护照、港澳通行证、统一社会信用代码、手机号、固话、邮箱、
银行卡（Luhn）、IPv4、MAC、车牌；生物识别 / 医疗健康 / 行踪轨迹 /
未成年人等关键词线索。

## 架构

```
scripts/
  guard.py          检测内核（动作、校验、脱敏、分级）
  rules/
    common.py       通用规则包
```

内核与规则分离：行业版只需新增规则包并在 `PROFILES` 登记，内核复用。

## 系列规划

- `pipl-guard`（通用版）— 本项目
- `pipl-guard-finance`（金融版）— 在通用规则上叠加金融专属规则，规划中

## 许可证与声明

MIT 许可证。本工具仅为运行时防护的辅助手段，不构成法律建议或合规证明，
检测不保证 100% 完整。详见 [SKILL.md](SKILL.md) 法律声明。
