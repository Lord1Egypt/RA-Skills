# Mystilink 塔罗 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

塔罗 Agent Skill：用内嵌 Node 脚本按牌阵抽取正/逆位牌，再结合牌意词条解读。优先真实抽牌（脚本或用户已抽结果），禁止静默编造抽牌结果。

## 交付类型

**Agent Skill** 包。**不适用**计算器语言矩阵。抽牌逻辑仅内嵌于 `scripts/`（无独立塔罗计算器仓库）。

## 环境要求

- Node.js 18+
- 兼容 Agent Skills 的宿主
- Wiki API 可选（需网络）

## 安装

目录名须为 `mystilink-tarot`：

```bash
cp -R mystilink-tarot-skill /path/to/.cursor/skills/mystilink-tarot
```

| 宿主 | 路径 |
|------|------|
| Cursor | `.cursor/skills/mystilink-tarot/` |
| Claude Code | `.claude/skills/mystilink-tarot/` |

## 快速开始

```bash
node scripts/draw.mjs --spread three-card --seed 42
# 或: echo '{"spread":"three-card","seed":42}' | node scripts/draw.mjs
```

stdout JSON：含 `id`、`name`、`orientation`（`upright`|`reversed`）、位置。牌 `id` 对应 Wiki `tarot.card.*`。

## 工作流

1. 明确问题与牌阵（默认三牌）；见 `examples/draw-request.json`
2. 用脚本抽牌或接受用户已抽结果
3. 对每张牌可选 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en
GET https://wiki.mystilink.com/api/v1/pages/<card.id>?locale=en
```

4. 将各位置与问题对应；使用 Wiki 时注明出处

详见 `SKILL.md`。抽牌说明见 `references/method-draw.md`。

## 示例

- `examples/draw-request.json` — 抽牌请求样例

## 限制

- 不宣称医疗或法律确定性
- 尽量一事一抽
- Wiki 省略 locale → `en`

## 许可

MIT。见 [LICENSE](../../LICENSE)。

## 问题反馈

请附带牌阵参数/seed（或 stdin JSON）与 stdout JSON（仅用虚构问题）。
