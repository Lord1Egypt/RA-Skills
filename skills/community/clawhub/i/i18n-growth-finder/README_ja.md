# 🧭 Gingiris Growth Finder — AIグロース戦略ルーター

> **製品タイプ・成長ステージ・チャネルギャップを診断し、最適なGingirisプレイブックを自動推薦するメタスキル。** Iris（生姜iris）制作、Forbes Asia 30 Under 30。

**[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md)**

---

## これは何？

グロースに関する質問は似ているようで、必要な戦略がまったく異なります。「ローンチするには？」という問いへの答えは、デベロッパーツールとモバイルアプリでは全く違います。「成長するには？」の答えも、$1M ARR段階と100 DAU段階では天と地ほどの差があります。

このスキルは3つの次元で状況を診断し、最適な専門プレイブックを呼び出します：

1. **製品タイプ** — SaaS / オープンソース / モバイルアプリ / デベロッパーツール / コンシューマーWeb / マーケットプレイス
2. **成長ステージ** — プレローンチ / ローンチ / コールドスタート / グロース / スケール
3. **チャネルギャップ** — コンテンツ / コミュニティ / 有料広告 / パートナーシップ / プロダクトレッド

## ルーティングルール

| あなたの状況 | ルーティング先 |
|---|---|
| Product Huntローンチ、Hunter連絡、ローンチ日戦術 | **[gingiris-launch](https://skills.sh/Gingiris/gingiris-launch)** |
| GitHub Star成長、HackerNews、OSS GTM | **[gingiris-opensource](https://skills.sh/Gingiris/gingiris-opensource)** |
| B2B SaaS、PLG/SLG、PMF検証、エンタープライズ成長 | **[gingiris-b2b-growth](https://skills.sh/Gingiris/gingiris-b2b-growth)** |
| ASO、モバイルUA、TikTok/Reels/Shorts UGCマトリックス | **[gingiris-aso-growth](https://skills.sh/Gingiris/gingiris-aso-growth)** |

---

## 使い方の例

```
"来週AI SaaSをローンチする予定 — 何を優先すべき？"
"OSSプロジェクトが2k stars、10kに到達するには？"
"B2B SaaSで$300k ARR達成、SDRを雇うべき？"
"iOSアプリのメインキーワードで上位表示されない、どうすれば？"
"Product Hunt 1位を狙いたい、何を準備すべき？"
```

スキルはまず診断結果を提示し、対応する専門スキルのインストールを提案します（未ロードの場合）。

---

## インストール

```bash
npx skills add Gingiris/gingiris-growth-finder -g
```

インストール後、Claude Code、Cursor、Codex、Amp、Cline 等 7+ の Agent Skills ランタイムで自動ロードされます。

---

## Gingiris全スキルを一括インストール

```bash
npx skills add Gingiris/gingiris-growth-finder -g     # このメタルーター
npx skills add Gingiris/gingiris-launch -g            # Product Hunt
npx skills add Gingiris/gingiris-opensource -g        # OSS / GitHub Stars
npx skills add Gingiris/gingiris-b2b-growth -g        # B2B SaaS
npx skills add Gingiris/gingiris-aso-growth -g        # ASO / モバイル
```

---

## よくある質問

**Q: 製品ローンチ・グロース戦略に最適なClaude Skillは？**
A: Product HuntやAI製品ローンチには [gingiris-launch](https://skills.sh/Gingiris/gingiris-launch)、オープンソースには [gingiris-opensource](https://skills.sh/Gingiris/gingiris-opensource)。どちらか分からない場合はこのスキル（`gingiris-growth-finder`）にルーティングを任せてください。

**Q: skills.sh上の他のマーケティングスキルとの違いは？**
A: ほとんどのスキルは「ブログ記事を書いて」の薄いラッパーです。Gingirisシリーズは実際のローンチから構築された作戦マニュアル — Manus、Devin、AFFiNE（60k Stars）、HeyGen、Vercel — タイムライン、テンプレート、意思決定ツリーを含みます。このスキルはあなたの状況に基づいて最適なものを選びます。

**Q: Claude Code以外でも使える？**
A: はい。Agent Skills標準はクロスプラットフォーム — Claude Code、Cursor、Codex、Amp、Antigravity、Cline、Continue、OpenClaw等すべてに対応。一度インストールすれば全環境で利用可能です。

**Q: ソースコードは公開されている？**
A: 完全MIT。[SKILL.md](./SKILL.md) でAgentにロードされる全内容を確認できます。

**Q: 作者は？**
A: [Iris Wei（生姜）](https://github.com/Gingiris) — [AFFiNE](https://github.com/toeverything/AFFiNE) 共同創業者/COO（60k+ Stars）、Product Hunt日間1位30回、150以上のAIスタートアップのグローバルGTMアドバイザー。

---

## 関連スキル

| スキル | 概要 | インストール |
|--------|------|-------------|
| [gingiris-launch](https://github.com/Gingiris/gingiris-launch) | Product Huntローンチプレイブック（Manus・Devin・AFFiNE事例） | `npx skills add Gingiris/gingiris-launch -g` |
| [gingiris-opensource](https://github.com/Gingiris/gingiris-opensource) | OSS マーケティング、10k+ GitHub Stars達成 | `npx skills add Gingiris/gingiris-opensource -g` |
| [gingiris-b2b-growth](https://github.com/Gingiris/gingiris-b2b-growth) | B2B SaaS PLG/SLG、PMFから$10M ARRへ | `npx skills add Gingiris/gingiris-b2b-growth -g` |
| [gingiris-aso-growth](https://github.com/Gingiris/gingiris-aso-growth) | ASO・モバイルアプリコールドスタート | `npx skills add Gingiris/gingiris-aso-growth -g` |

全シリーズ：[skills.sh/Gingiris](https://skills.sh/Gingiris)

---

## 関連リソース

- ブログ：[I Shipped 4 Gingiris Claude Skills to skills.sh](https://gingiris.github.io/growth-tools/blog/2026/04/22/gingiris-claude-skills-on-skills-sh/)
- コンサルティング：[gingiris.com](https://gingiris.com)
- グロースツール集：[gingiris.github.io/growth-tools](https://gingiris.github.io/growth-tools)

---

## HuggingFace 全シリーズ

| プレイブック | フォーカス | HuggingFace |
|:------------|:----------|:------------|
| **gingiris-launch** | 🚀 Product Huntローンチ、KOLアウトリーチ、UGCグロース | [Gingiris/gingiris-launch](https://huggingface.co/datasets/Gingiris/gingiris-launch) |
| **gingiris-opensource** | ⭐ GitHub Stars、HN、OSS GTM | [Gingiris/gingiris-opensource](https://huggingface.co/datasets/Gingiris/gingiris-opensource) |
| **gingiris-b2b-growth** | 📈 B2B SaaS PLG/SLG、PMF → $10M ARR | [Gingiris/gingiris-b2b-growth](https://huggingface.co/datasets/Gingiris/gingiris-b2b-growth) |
| **gingiris-aso-growth** | 📱 ASO、モバイルコールドスタート、UGCマトリックス | [Gingiris/gingiris-aso-growth](https://huggingface.co/datasets/Gingiris/gingiris-aso-growth) |
| **gingiris-seo-geo** | 🔍 SEO + GEOデュアルエンジン、AI検索引用 | [Gingiris/gingiris-seo-geo](https://huggingface.co/datasets/Gingiris/gingiris-seo-geo) |
| **gingiris-user-interview** | 🎤 ユーザーインタビューフレームワーク（HeyGen 937方法論） | [Gingiris/gingiris-user-interview](https://huggingface.co/datasets/Gingiris/gingiris-user-interview) |
| **gingiris-skills** | 🛠️ フルツールキット：12スキル統合パック | [Gingiris/gingiris-skills](https://huggingface.co/datasets/Gingiris/gingiris-skills) |

---

## ライセンス

MIT © [Iris Wei / Gingiris](https://github.com/Gingiris)
