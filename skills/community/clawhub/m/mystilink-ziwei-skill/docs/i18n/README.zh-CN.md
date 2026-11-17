# Mystilink 紫微 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

紫微斗数 Agent Skill：用内嵌 Python 脚本排出十二宫盘（可选四化），再结合理论词条解读。排盘逻辑在 `scripts/`。

## 交付类型

**Agent Skill** 包。**不适用**计算器语言矩阵（C / C++ / C# / Java / JS / Python SDK）。可选同系列：`mystilink-ziwei-calculator`。

## 环境要求

- Python 3.9+
- `pip install zhdate`
- 兼容 Agent Skills 的宿主
- Wiki API 可选（需网络）

## 安装

目录名须为 `mystilink-ziwei`：

```bash
cp -R mystilink-ziwei-skill /path/to/.cursor/skills/mystilink-ziwei
```

| 宿主 | 路径 |
|------|------|
| Cursor | `.cursor/skills/mystilink-ziwei/` |
| Claude Code | `.claude/skills/mystilink-ziwei/` |

## 快速开始

```bash
python3 scripts/ziwei_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender female \
  --output json

python3 scripts/ziwei_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

可选：`--si-hua`、`--year YYYY`、`--longitude E`、`--midnight-zi`。

成功：stdout JSON。失败：非零退出 + JSON error。

## 工作流

1. 采集出生资料——`examples/profile.v0.json`（BirthProfile）或旧版 `examples/profile.json`
2. 运行排盘脚本
3. 可选 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=life+palace&system=ziwei&locale=en
GET https://wiki.mystilink.com/api/v1/pages/ziwei.concept.ming-gong?locale=en
```

4. 区分盘面事实与解释

详见 `SKILL.md`。短指引见 `references/overview.md`。

## 示例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`，虚构）
- `examples/profile.json` — 旧版虚构输入样例

## 限制

- 农历转换依赖 `zhdate`
- 内嵌脚本供 skill 独立使用，非多语言 SDK
- Wiki 省略 locale → `en`；缺译可能回落 `zh-Hans`

## 许可

MIT。见 [LICENSE](../../LICENSE)。

## 问题反馈

请附带完整命令（虚构时间）与 JSON 输出或错误。
