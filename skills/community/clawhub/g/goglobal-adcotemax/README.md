# Max Global Pathway Advisor / Max 全球升学路径顾问

A bilingual, source-aware global undergraduate pathway advising skill for international high schools, bilingual schools and pathway programmes.

一个面向国际高中、融合课程学校、双语学校和升学路径项目的中英双语全球本科升学路径 Skill。

## Positioning / 定位

Max helps schools, families and students connect:

- student profile / 学生画像
- curriculum choice / 课程选择
- academic readiness / 学业基础
- English readiness / 英语能力
- destination selection / 目标国家和地区
- admission requirements / 大学录取要求
- application risks / 申请风险
- school-based support / 校本支持
- staged action planning / 阶段行动计划

Max is not an overseas study agency and does not provide guaranteed admission claims.

Max 不是留学中介，不提供保录承诺。

## Installation / 安装

After publication to ClawHub:

```bash
openclaw skills install max-global-pathway
```

or via ClawHub CLI:

```bash
clawhub install max-global-pathway
```

## Publishing / 发布

From the parent directory:

```bash
clawhub login
clawhub whoami
clawhub skill publish ./max-global-pathway-skill --slug max-global-pathway --name "Max" --version 0.3.0 --changelog "Initial bilingual release: global pathway advising system for international high schools." --tags "education,university-admissions,international-school,bilingual,pathway"
```

For a dry run:

```bash
clawhub skill publish ./max-global-pathway-skill --slug max-global-pathway --name "Max" --version 0.3.0 --changelog "Initial bilingual release." --tags "education,university-admissions,international-school,bilingual,pathway" --dry-run
```

## Maintainer / 维护者

Max

Maintainer contact is intentionally low-profile inside `SKILL.md` and should only appear in school-level implementation, adaptation or collaboration scenarios.
