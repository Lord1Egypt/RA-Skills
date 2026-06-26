# 内科学 Internal-Medicine-PMPH-10edition
<div align="center">

> *「21世紀 医学生ガイド」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 人民衛生出版社『内科学』第10版に基づく臨床スキルハンドブック — 内科領域423の核心的臨床スキル
<br>
<br>
<img src="assets/Internal-Medicine.jpg" width="260px">
<br>

教科書を丸ごと読む必要はありません。<br>
質問を入力するだけで、教科書から即座に解決策を得られます。

<br>

**他の言語 / Other Languages:**

[English](README_EN.md) · [简体中文](README.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## プロジェクト概要

本プロジェクトは、内科領域の核心的知識を体系的に統合し、**15 大分類** — 心血管疾患、呼吸器疾患、消化器疾患、内分泌・代謝疾患、腎疾患、血液疾患、リウマチ・免疫疾患、感染症・結核、中毒・物理化学的損傷、腫瘍・総合、慢性疾患管理・地域連携診療、臨床スキル・手技、薬物治療・安全性、検査・画像診断、教育リソース・品質管理 — を網羅し、全 **423 項目の主要臨床スキル** を収録しています。

**対象読者**: 内科医、総合診療医、救急医、医学生、初期臨床研修医

**参考教科書**: 人民衛生出版社『内科学』第10版

**⚠️ リスク ⚠️**: 高リスクの臨床治療、手順、投薬量の指示は、一般的なインストール環境や無監督での使用には適さない場合があります。

**対策**: 資格のある臨床医による使用、指導下での医学教育環境に限定し、出力を取り扱う前に臨床医による確認を必須とします。

**⚠️ リスク ⚠️**: 本ガイダンスが現在の地域ガイドライン、施設プロトコル、または患者固有の禁忌と矛盾する可能性があります。

**対策**: 使用前に、計画、手順、基準値、フォローアップ計画が最新の地域基準および施設方針に適合していることを確認してください。

**⚠️ リスク ⚠️**: 緊急時の侵襲的処置、化学療法レジメンの調整、およびセンシティブな終末期判断を軽率に行うと、患者の安全やプライバシーを損なう恐れがあります。

**対策**: これらのシナリオに対して明確な警告を追加し、緊急時は救急医療へ誘導し、適切な臨床経験または指導下での教育ニーズを有するユーザーのみにアクセスを制限します。

## プロジェクト構造

```
Internal-Medicine-PMPH-10edition/
├── SKILL.md                  # 核心設定 — 423スキルレジストリ
├── README.md                 # 本ドキュメント — プロジェクト説明と使用ガイド
├── <skill-name>/             # 各スキルの詳細定義
│   └── SKILL.md              #   スキル詳細（適応、手順、参考文献）
├── scripts/                  # 実行可能ユーティリティスクリプト
│   ├── list-skills.sh        #   スキルキーワード検索
│   └── build-index.py        #   スキルインデックス生成
├── config/                   # 設定ファイル
│   └── skills-index.json     #   全423スキルのJSONインデックス
└── tests/                    # 検証とテスト
```

## スキル分類一覧

| 分類 | スキル数 | 説明 |
|------|---------|------|
| ❤️ 心血管疾患 | 56 | 冠動脈疾患、心不全、不整脈、心筋症、高血圧、弁膜症など |
| 🫁 呼吸器疾患 | 45 | 肺炎、COPD、喘息、肺塞栓症、間質性肺疾患、胸膜疾患など |
| 🫃 消化器疾患 | 50 | 胃炎、潰瘍、炎症性腸疾患、肝硬変、膵炎、腹水など |
| 🧬 内分泌・代謝疾患 | 46 | 糖尿病、甲状腺疾患、下垂体・副腎疾患、痛風、電解質異常など |
| 🫘 腎疾患 | 29 | 糸球体腎炎、腎不全、透析、蛋白尿、AKIなど |
| 🩸 血液疾患 | 37 | 白血病、貧血、凝固異常、多発性骨髄腫、リンパ腫、MDSなど |
| 🦿 リウマチ・免疫疾患 | 12 | RA、SLE、シェーグレン症候群、全身性硬化症、血管炎など |
| 🦠 感染症・結核 | 20 | 市中感染、院内感染、結核、真菌感染、ウイルス性肝炎など |
| 💊 中毒・物理化学的損傷 | 15 | 薬物中毒、有機溶剤中毒、一酸化炭素中毒、熱中症、溺水など |
| 🎗️ 腫瘍・総合 | 18 | 肺癌、胃癌、大腸癌、膵癌、腫瘍マーカー・標的治療など |
| 📋 慢性疾患管理・地域連携診療 | 20 | 高血圧階層化管理、糖尿病慢性期フォロー、脂質異常症長期管理など |
| 🔬 臨床スキル・手技 | 25 | 胸腔穿刺、腹腔穿刺、骨髄穿刺、心肺蘇生、電気的除細動など |
| 💉 薬物治療・安全性 | 20 | 抗凝固薬管理、抗菌薬適正使用、グルココルチコイド標準使用など |
| 📡 検査・画像診断 | 15 | 心電図解析、心エコー解釈、血液ガス分析、検査値判定など |
| 📚 教育リソース・品質管理 | 15 | 教科書構成、シラバス解説、核心的出題ポイント、臨床思考トレーニングなど |

## クイックスタート

### インストール

CLI：
```bash
openclaw skills install internal-medicine-pmph-10edition
```

Prompt：
```bash
インストール前に、ClawHubのスキルメタデータとセットアップ要件を確認してください。
サードパーティ製パッケージやCLIのインストールを要求された場合は、そのソース、メンテナー、パッケージ内容を検証してからインストールコマンドを実行してください。
それらの確認が完了した後にのみ、ClawHubからスキル「Internal-Medicine-PMPH-10edition」（xllgreen/internal-medicine-pmph-10edition）をインストールしてください。
スキルページ：https://clawhub.ai/xllgreen/internal-medicine-pmph-10edition
作業はこのスキルにのみ限定してください。
インストール後、確認済みのスキルメタデータに基づいてセットアップを完了するのを手伝ってください。
ClawHubから確認できるメタデータのみを使用し、不足している要件を独自に発明しないでください。
より広範な環境変更を行う前には確認を取ってください。
```

### インストール後の使用
agentに以下の指示を伝えてください：
```bash
毎回の回答前に、対応する医学スキルを参照して確認してください。
```

### スキル検索

```bash
# キーワード検索
bash scripts/list-skills.sh search 心不全

# スキル一覧表示
bash scripts/list-skills.sh list
```

### 使用方法

各スキルは4つのパートで構成されています：
1. **適応** — いつこのスキルを発動するか
2. **手順** — 標準化された操作手順
3. **注意事項** — 禁忌と警告
4. **参考文献** — 詳細な補足資料

### 質問戦略

#### 1. **概念**
Question:
```bash
内科学における感染性心内膜炎の定義は？
```
Answer：
```bash
内科学（第10版）の定義：
**感染性心内膜炎（infective endocarditis, IE）** とは、病原微生物（細菌、真菌など）が血行性に心内膜、心臓弁膜、または隣接する大動脈内膜に直接侵入し、形成される**疣贅（vegetation）** とそれに伴う臨床症候群である。疣贅は血小板、フィブリン、病原微生物、炎症細胞から構成される。
重要ポイント：
- **核心的病態**：微生物が損傷を受けた弁膜または心内膜表面に付着 → 疣贅形成
- **好発部位**：僧帽弁 > 大動脈弁（左心系が主体）
- **臨床的三徴**：発熱 + 心雑音 + 塞栓・血管現象
- **分類**：経過により急性と亜急性；弁の種類により自己弁IE、人工弁IE、右心IE
```

#### 2. **臨床ケース分析**
Question:
```bash
60歳女性。反復する咳嗽・喀痰25年、動悸・呼吸困難・間欠的下肢浮腫3年、1週前より増悪し悪寒・発熱を伴い入院。身体所見：体温38°C、呼吸促迫、口唇チアノーゼ、両肺打診で過共鳴音、中下肺野に湿性ラ音、心拍数110/分、整、雑音なし、両下肢に高度浮腫。診断は？
```
Answer：
```bash
これは典型的な**COPD → 慢性肺性心 → 右心不全**への進展経過である。
**完全診断：**
1. **慢性閉塞性肺疾患（COPD）急性増悪**
   - 根拠：25年の慢性咳嗽・喀痰歴 + 肺気腫徴候（過共鳴音） + 発熱・呼吸促迫を伴う急性増悪
2. **慢性肺性心（代償不全期）**
   - 根拠：COPDを基礎 + 3年の動悸・呼吸困難・下肢浮腫歴（長期の右心負荷増大を示唆）+ 現在の両下肢高度浮腫・口唇チアノーゼ
**病態生理連鎖：**
COPD → 低酸素性肺血管収縮 + 肺毛細血管床減少 → 肺高血圧症 → 右心室後負荷増大 → 右室肥大・拡大 → 右心不全 → 体循環うっ血（下肢浮腫、チアノーゼ）
**鑑別除外：**
- 整脈、雑音なし → リウマチ性弁膜症、心房細動が心不全原因であることを除外
- 浮腫は対称性 → 腎原性を除外（後者は眼瞼・顔面浮腫を伴うことが多い）
```
#### 3. **試験問題**
Question:
```bash
腸結核の最も頻度の高い発生部位は：
A. 十二指腸
B. 空腸
C. 回盲部
D. 横行結腸
E. S状結腸
```
Answer：
```bash
**C. 回盲部**
これは腸結核の最も特徴的な好発部位であり、その理由は：
- 回盲部はリンパ組織（パイエル板）が最も豊富で、結核菌が定着しやすい
- 蠕動が緩やかで内容物の滞留時間が長く、細菌侵入を促進する
従って、腸結核とクローン病の鑑別もこの部位を中心に行われる——回盲部に輪状・不整形潰瘍、限局性分布、抗酸染色陽性がみられる場合は腸結核が示唆され、縦走潰瘍、分節性分布、瘻孔を伴う場合はクローン病がより示唆される。
```

## 著者について

**xllgreen (https://xllgreen.github.io)** — 九江学院臨床医学院 学生・テック愛好家

## テクニカルサポート
<br>
PDF2Appプロジェクト：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基礎技術研究有限公司 All Rights Reserved
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## ライセンス

本プロジェクトの内容は、人民衛生出版社『内科学』第10版に基づいて編集されたものであり、学習参考目的にのみ提供されます。

## Star History

<a href="https://www.star-history.com/?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left" />
 </picture>
</a>
