# Mystilink 占星 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

西洋本命盘 Agent Skill：用内嵌脚本根据出生时间与地点计算行星、宫位与相位，再结合理论词条解读。

## 交付类型

**Agent Skill** 包。**不适用**计算器语言矩阵。可选同系列：`mystilink-horoscope-calculator`。

## 环境要求

- Python 3.9+
- `pip install pyswisseph`
- 兼容 Agent Skills 的宿主
- Wiki API 可选（需网络）

## 安装

目录名须为 `mystilink-horoscope`：

```bash
cp -R mystilink-horoscope-skill /path/to/.cursor/skills/mystilink-horoscope
```

| 宿主 | 路径 |
|------|------|
| Cursor | `.cursor/skills/mystilink-horoscope/` |
| Claude Code | `.claude/skills/mystilink-horoscope/` |

## 快速开始

```bash
python3 scripts/astro_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --lat 31.23 --lon 121.47 \
  --output json

python3 scripts/astro_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

可选：`--zodiac tropical|sidereal`、`--true-solar-time`。

成功：stdout JSON。失败：非零退出 + JSON error。

## 工作流

1. 采集出生资料——`examples/profile.v0.json`（BirthProfile）或旧版 `examples/profile.json`
2. 运行本命盘脚本
3. 可选 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en
GET https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en
```

4. 区分盘面数据与解释

详见 `SKILL.md`。短指引见 `references/overview.md`。

## 示例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`，虚构）
- `examples/profile.json` — 旧版虚构本命输入

## 限制

- 依赖 `pyswisseph`（Swiss Ephemeris）
- 内嵌脚本供 skill 独立使用，非多语言 SDK
- Wiki 省略 locale → `en`；缺译可能回落 `zh-Hans`

## 许可

MIT。见 [LICENSE](../../LICENSE)。

## 问题反馈

请附带完整命令（虚构坐标/时间）与 JSON 输出或错误。
