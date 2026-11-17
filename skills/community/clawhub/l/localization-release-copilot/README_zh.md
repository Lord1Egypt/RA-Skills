# 本地化发布运营影子助手（Localization Release Copilot）

> 本地化 / 翻译发布运营的影子审阅助手。

[![ClawHub](https://img.shields.io/badge/ClawHub-localization--release--copilot-blue)](https://clawhub.com)
[![GitHub](https://img.shields.io/badge/GitHub-haiyangchenbj%2Flocalization--release--copilot-lightgrey)](https://github.com/haiyangchenbj/localization-release-copilot)

## 它做什么

给定一份**源稿**和其一/多个**目标语言版本**，它在发布前充当影子审阅者，抓出会破坏发布的漂移：

- **术语锁定** — 强制术语表里的强制词每次发布都遵守。
- **数字完整性** — locale-aware：`8.3亿`≈`830M`、`117亿`≈`€11.7B` 算匹配，不算错误。
- **专有名词检查** — 产品名、机构、人名、框架名必须 survive 翻译。
- **来源标注保留** — 源稿里的 `(机构, 年份)` 引用必须留在目标稿。
- **结构损失标记** — 只标记"主张级"掉落，不标记合理的压缩。
- **可审阅预览** — PR 式差异，人一次就能批完。

它**绝不重写**译文。设计上只审阅。

## 何时用

- 你有成型的源稿（中文文章 / 论文 / 文档 / 发版说明）和另一语言的译文，想做发布前一致性检查。
- 你同一内容多语言发布（微信中文 → LinkedIn/Substack 英文；文档中文 → 英文），想确认目标稿没悄悄丢掉数字、专有名词或来源引用。
- 你维护术语表，需要每次发布都遵守锁定词。
- 你想要一个可一键审阅的"源稿→目标稿"差异预览。
- 你怀疑"英文读着通顺但数据丢了"——本 Skill 专门抓这类。

## 何时不用

- 单语润色 → `claim-to-source-auditor`（或本地已安装的专门合规审查 Skill）。
- 同一主题多份材料间的一致性 → `cross-material-consistency-auditor`。
- 选题评估 → `editorial-topic-portfolio`。
- 机器翻译生成（本 Skill 只审，不译）。

## 快速开始

```bash
python scripts/locale_aware_diff.py \
  --source path/to/source.zh.md \
  --targets path/to/target.en.md \
  --labels LinkedIn \
  --output 01-extracted-claims.json
```

然后按 `SKILL.md` 跑 LLM 差异矩阵 + 预览步骤。

## 范围

| 已支持（v1.0.0） | 待补（需真实样本） |
|---|---|
| 长文 editorial ZH↔EN 本地化 | SaaS `.po` / i18n locale 文件 diff |
| 术语表合规审阅 | 占位符 / 复数检查 |
| 多目标（LinkedIn / Substack / 文档） | 翻译记忆集成 |

## 许可

内部使用。公开发布前移除个人语境。
