# Mystilink 八字 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

八字 Agent Skill：通过内嵌脚本根据出生资料计算四柱、大运、流年，再结合理论词条（日主、十神等）进行解读。排盘算法位于 `scripts/`。

## 交付类型

本仓库为 **Agent Skill** 包（`SKILL.md` + `scripts/` + `references/` + `examples/`）。**不适用**计算器库的 C / C++ / C# / Java / JavaScript / Python 语言矩阵。多语言 SDK/CLI 见同系列 `mystilink-bazi-calculator`（可选，运行本 skill 非必需）。

## 环境要求

- Python 3.9+（`zoneinfo`）
- 兼容 Agent Skills 的宿主
- 解读时可选访问 Mystilink Wiki API（需网络）

## 安装

安装目录名须为 `mystilink-bazi`（与 `SKILL.md` 的 `name` 一致）：

| 宿主 | 路径 |
|------|------|
| Cursor | `.cursor/skills/mystilink-bazi/` |
| Claude Code | `.claude/skills/mystilink-bazi/` |

```bash
cp -R mystilink-bazi-skill /path/to/.cursor/skills/mystilink-bazi
```

## 快速开始（脚本）

在 skill 目录下：

```bash
python3 scripts/bazi_calculate.py --date 1990-05-15 --hour 12
python3 scripts/bazi_calculate.py --birth-json examples/profile.v0.json
python3 scripts/bazi_calculate.py --profile-json examples/profile.json
python3 scripts/bazi_dayun_calculate.py --date 1990-05-15 --gender female --count 8
python3 scripts/bazi_liunian_calculate.py --year 2026 --day-stem 甲
```

成功：stdout 输出 JSON。失败：非零退出码，并输出 `{"error":…}`。

柱对象含 `stem_index`、`branch_index`、`text`，并保留旧字段 `ganzhi`（与 `text` 相同）。

## 工作流

1. 采集出生资料——任选其一：
   - `examples/profile.v0.json`（`mystilink.birth/0.1` BirthProfile），或
   - `examples/profile.json`（旧版 skill 字段）
2. 按需运行排盘脚本（`--birth-json` / `--profile-json` 两种形状均可）
3. 可选 Wiki 解读：

```text
GET https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en
GET https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en
```

4. 区分 **盘面事实** 与 **解释**；使用 Wiki 时注明出处

完整说明见 `SKILL.md`。常用页面 id 见 `references/wiki-ids.md`。

## 示例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`，虚构）
- `examples/profile.json` — 旧版出生资料（虚构）；脚本仍接受

## 限制

- 脚本为独立安装用的内嵌副本，不是多语言 SDK
- 大运节气日为公历近似
- 真太阳时需同时提供时区与经度
- Wiki：省略 locale → `en`；缺译可能回落 `zh-Hans`

## 许可

MIT。见 [LICENSE](../../LICENSE)。

## 问题反馈

请附带完整脚本命令（仅用虚构日期）及 stdout/stderr JSON。
