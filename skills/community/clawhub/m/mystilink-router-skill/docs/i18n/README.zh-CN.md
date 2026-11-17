# Mystilink 路由 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

Agent Skill：在用户未指定体系、询问该用哪种方法、或一次请求混用多种传统时，选择一个 Mystilink 命理/占卜 skill（八字、紫微、塔罗、六爻或西洋占星）。本 skill 不负责排盘或抽牌计算。

## 交付类型

本仓库为 **Agent Skill** 包（`SKILL.md` + references + examples）。**不适用**计算器库所要求的 C / C++ / C# / Java / JavaScript / Python 语言矩阵。

## 环境要求

- 兼容 Agent Skills 规范的宿主（Cursor、Claude Code、OpenClaw、Hermes 等）
- 路由完成后若要继续执行，需已安装对应体系的 skill

## 安装

将本仓库克隆或复制到宿主 skills 目录，目录名使用 `mystilink-router`（须与 `SKILL.md` 中的 `name` 一致）：

| 宿主 | 路径 |
|------|------|
| Cursor | `.cursor/skills/mystilink-router/` 或 `~/.cursor/skills/mystilink-router/` |
| Claude Code | `.claude/skills/mystilink-router/` 或 `~/.claude/skills/mystilink-router/` |

```bash
cp -R mystilink-router-skill /path/to/.cursor/skills/mystilink-router
```

## 用法

按 `SKILL.md` 执行。路由启发式：

| 需求 | Skill |
|------|--------|
| 生辰 → 长期结构、十神 | `mystilink-bazi` |
| 生辰 → 十二宫 / 紫微星曜 | `mystilink-ziwei` |
| 生辰地点 + 时间 → 行星/宫位/相位 | `mystilink-horoscope` |
| 一事一问、牌象 | `mystilink-tarot` |
| 一事一问、卦爻 | `mystilink-liuyao` |

可选 Wiki（需网络）：

```text
GET https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en
```

选定后加载目标 skill 的 `SKILL.md` 并继续。优先每次请求只选一个主体系。

## 示例

见 `examples/routing-cases.md`（示例意图与期望目标）。

## 限制

- 本 skill 不含计算脚本
- 不「五个体系一起跑」
- Wiki 调用可选；省略 `locale`/`lang` → `en`；缺译可能回落 `zh-Hans`

## 许可

MIT。见 [LICENSE](../../LICENSE)。

## 问题反馈

反馈时请附带用户意图原文（仅用虚构内容）以及选中或漏选的 skill 名称。
