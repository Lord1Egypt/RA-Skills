# iPhone Duo Adaptation Skill

面向 iOS 开发和 QA 的 Codex Skill。用于审查、实施和验证 iPhone Duo 适配，覆盖 SwiftUI、UIKit 和混合工程。

A Codex skill for auditing, implementing, and testing iPhone Duo support in iOS apps.

iPhone Duo 対応の調査、実装、検証を支援する iOS チーム向けの Codex スキルです。

| Language | Handbook |
| --- | --- |
| 简体中文 | [开发与验收手册](references/guide.zh-Hans.md) |
| English | [Engineering and QA handbook](references/guide.en.md) |
| 日本語 | [開発・検証ガイド](references/guide.ja.md) |

## 安装 · Install · インストール

将仓库克隆到 Codex 的用户 Skill 目录。若已安装同名 Skill，可在更新前检查本地修改。

Clone the repository into your Codex user skills directory. If the skill is already installed, check for local changes before updating it.

Codex のユーザースキルディレクトリにリポジトリをクローンします。インストール済みの場合は、更新前にローカルの変更を確認してください。

```sh
mkdir -p ~/.agents/skills
git clone https://github.com/hzw-object/iphone-duo-adaptation.git ~/.agents/skills/iphone-duo-adaptation
```

## 使用 · Usage · 使い方

在 iOS 工程中打开 Codex，然后调用 Skill。

> 用 `$iphone-duo-adaptation` 审查当前 iOS 工程，列出优先修复的问题，并给出 Device Hub 验收步骤。

> Use `$iphone-duo-adaptation` to audit this iOS project and give me a prioritized fix list and a Device Hub test plan.

> `$iphone-duo-adaptation` を使って、この iOS プロジェクトの修正優先順位と Device Hub での確認手順をまとめてください。

## 内容 · Coverage · 対象範囲

- [Skill instructions](SKILL.md) for audits, implementation, and verification.
- [Engineering examples](references/engineering.md) for SwiftUI and UIKit, with a five-language String Catalog.
- [Apple references](references/sources.md) for SDK requirements, Device Hub, reserved regions, and App Store Connect.

Swift examples and the String Catalog compiled with Xcode 27.2. Run fold transitions and hardware-dependent scenarios on iPhone Duo before accepting changes in your own app.
