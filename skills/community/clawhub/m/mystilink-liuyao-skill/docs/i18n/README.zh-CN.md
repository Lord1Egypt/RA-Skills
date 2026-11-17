# Mystilink 六爻 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

六爻 Agent Skill：用内嵌 Node 脚本完成六次起卦并形成卦象，再结合方法页与 Wiki 中的周易篇章解读。一事一卦。禁止编造经文。

## 交付类型

**Agent Skill** 包。**不适用**计算器语言矩阵。起卦逻辑仅内嵌于 `scripts/`（无独立六爻计算器仓库）。

## 环境要求

- Node.js 18+
- 兼容 Agent Skills 的宿主
- 建议可访问 Wiki（方法页与经典）

## 安装

目录名须为 `mystilink-liuyao`：

```bash
cp -R mystilink-liuyao-skill /path/to/.cursor/skills/mystilink-liuyao
```

| 宿主 | 路径 |
|------|------|
| Cursor | `.cursor/skills/mystilink-liuyao/` |
| Claude Code | `.claude/skills/mystilink-liuyao/` |

## 快速开始

```bash
node scripts/cast.mjs --seed 42
# 或固定投掷: node scripts/cast.mjs --throws "3,2,3,3,2,3"
```

stdout JSON：六爻（自下而上）、动爻标记、可用时的卦键。钱币模型见脚本说明（字=3、背=2 求和）。

## 工作流

1. 明确一事（`examples/cast-request.json`）；拒绝多主题滥卦
2. 用脚本起卦或接受用户投掷结果
3. 通过 Wiki 解读，例如：

```text
GET https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en
GET https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

4. 周易原文优先走 Wiki 引用 / cites

详见 `SKILL.md`。短指引见 `references/overview.md`。

## 示例

- `examples/cast-request.json` — 起卦请求样例

## 限制

- 经典文本在其它语言缺译时常见回落 `zh-Hans`
- 内嵌起卦助手为产品钱币→爻语义的简化实现
- Wiki 省略 locale → `en`

## 许可

MIT。见 [LICENSE](../../LICENSE)。

## 问题反馈

请附带 seed/throws 与 stdout JSON（仅用虚构事项）。
