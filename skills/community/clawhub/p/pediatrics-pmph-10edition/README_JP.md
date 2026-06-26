# 小児科学 Pediatrics-PMPH-10edition
<div align="center">

> *「21世紀 医学生ガイド」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 人民衛生出版社『小児科学』第10版に基づく臨床スキルハンドブック — 184 の小児科核心臨床スキル
<br>
<br>

教科書を丸ごと読む必要はありません<br>
質問を入力するだけで、教科書から解決策を即座に見つけられます

<br>

**他の言語 / Other Languages:**

[中文](README.md) · [English](README_EN.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## プロジェクト概要

本プロジェクトは、小児科学、新生児医学、小児の発育と栄養、感染症対策、遺伝代謝疾患の診療、救急・集中治療などの中核領域を体系的に統合し、**184 の重要臨床スキル**を **15 カテゴリ**に分類して収録しています。

**対象読者**：小児科医、医学生、新生児医療チーム、公衆衛生従事者、初期研修医

**参考教科書**：人民衛生出版社『小児科学』第 10 版

**⚠️リスク⚠️**：高リスクの臨床治療、手技、投薬指導は、一般環境でのインストールや監督なしでの使用に適さない可能性があります。

**緩和策**：資格を持つ小児科医、新生児科医、小児集中治療医、または監督下の医学教育環境でのみ使用可能。出力を実行する前に臨床医の確認を必須としてください。

**⚠️リスク⚠️**：指導内容が現在の地域のガイドライン、施設プロトコル、または患者固有の禁忌と矛盾する可能性があります。

**緩和策**：使用前に、計画、手順、閾値、フォローアップ計画が最新の地域基準および施設ポリシーに準拠していることを確認してください。

**⚠️リスク⚠️**：緊急処置、侵襲的介入、新生児蘇生、小児薬用量計算、および発達・行動に関するセンシティブな話題が軽率に扱われると、患者の安全やプライバシーを損なう可能性があります。

**緩和策**：これらのシナリオに明確な警告を追加し、緊急時は救急/ICUケアへ誘導し、適切な臨床または監督下の教育ニーズを持つユーザーのみにアクセスを制限してください。

## プロジェクト構造

```
Pediatrics-PMPH-10edition/
├── SKILL.md                  # 核心設定 — 184 スキルレジストリ
├── README.md                 # 本ドキュメント — プロジェクト概要と使用ガイド
├── <skill-name>/             # 各スキルの詳細定義
│   └── SKILL.md              #   スキル詳細（使用タイミング、手順、参考資料）
├── scripts/                  # 実行可能スクリプト
│   └── .gitkeep
├── config/                   # 設定ファイル
│   └── .gitkeep
└── tests/                    # 検証とテスト
    └── .gitkeep
```

## スキルカテゴリ一覧

| カテゴリ | スキル数 | 説明 |
|----------|----------|------|
| 👶 新生医学・周産期医学 | 18 | 黄疸、RDS、溶血、出血、NEC、ROP、BPD |
| 📏 発育・発達と栄養 | 18 | 体格評価、離乳食、睡眠、微量栄養素 |
| 💉 予防接種と感染症対策 | 20 | 予防接種スケジュール、麻疹、手足口病、結核、川崎病 |
| 🫁 呼吸器疾患 | 12 | 肺炎、喘息、マイコプラズマ、気管支鏡、血液ガス分析 |
| ❤️ 心血管疾患 | 10 | 先天性心疾患分類、心不全、心筋炎、Duke基準 |
| 🫃 消化器・肝胆道疾患 | 12 | 腸重積、ヒルシュスプルング病、IBD、胆道閉鎖、GERD |
| 🫘 泌尿器・腎疾患 | 10 | 血尿、腎炎、ネフローゼ症候群、AKI、RTA |
| ⚖️ 内分泌・代謝疾患 | 13 | GHD、思春期早発症、甲状腺機能低下症、糖尿病、DKA |
| 🩸 血液・腫瘍疾患 | 9 | ITP、AIHA、血友病、サラセミア、LCH |
| 🧠 神経・精神行動障害 | 12 | てんかん、熱性けいれん、ADHD、GBS、重症筋無力症 |
| 🚑 救急・集中治療 | 10 | CPR、外傷、溺水、呼吸不全、脱水 |
| 🧬 遺伝・先天疾患 | 7 | 三段階予防、遺伝病分類、CHARGE、DMD/BMD |
| 🔬 検査・画像診断 | 11 | 髄液、PKU、CAH、くる病、MRI、超音波 |
| 📚 教科書・根拠に基づく医療 | 7 | 教科書権威性評価、改訂原則、文献紹介 |
| 🏋️ 総合的健康管理 | 9 | 運動、食事、免疫系、薬剤用量、身体診察 |

## クイックスタート

### インストール

CLI：
```bash
openclaw skills install pediatrics-pmph-10edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Pediatrics-PMPH-10edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### スキルを探す

```bash
# キーワード検索
bash scripts/skill-search.sh 新生児黄疸

# スキルレポート生成
bash scripts/skill-report.sh
```

### 使用方法

各スキルは以下の4つのセクションで構成されています：
1. **使用タイミング** — このスキルを適用する臨床状況
2. **実行手順** — 標準化された操作フロー
3. **注意事項** — 禁忌と警告
4. **参考文献** — 補足資料

### 質問ストラテジー

#### 1. **概念**

Question:
```bash
新生児生理的黄疸の概念
```

Answer：
```bash
## 新生児生理的黄疸の概念

**新生児生理的黄疸**とは、ビリルビン代謝の特性に起因して新生児期に一過性に血清非抱合型ビリルビンが上昇する状態で、通常は特別な治療を必要とせず自然に消退する良性の経過をたどります。

### 診断基準

| パラメータ | 正期産児 | 早産児 |
|-----------|---------|-------|
| 出現時期 | 生後2～3日 | 生後3～5日 |
| ピーク | 生後4～5日 | 生後5～7日 |
| 消退 | 生後5～7日 | 生後7～9日 |
| 血清ビリルビン最高値 | < 221 μmol/L (12.9 mg/dL) | < 256 μmol/L (15 mg/dL) |
| 1日上昇幅 | < 85 μmol/L (5 mg/dL) | < 85 μmol/L (5 mg/dL) |

### 主要な鑑別

- **生理的黄疸**：上記タイムウィンドウと閾値に合致、全身状態良好
- **病的黄疸**：出現が早すぎる（<24h）、程度が強すぎる、遷延する、上昇が速すぎる、直接ビリルビン高値
- **母乳性黄疸**：生後1週以降に出現、2～3週でピーク、母乳中断3日で有意に低下

### 管理

特別な治療は不要。十分な授乳を確保し胎便排出を促進。TSBが介入閾値に近づく場合は光線療法の評価を開始。

---

**関連スキル：** [新生児黄疸リスク評価と生理的黄疸診断](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md)
```

#### 2. **臨床ケース分析**

Question:
```bash
正期産児、胎齢38週、経膣分娩、出生体重3.2kg。生後24時間以内に皮膚黄染が出現し急速に増悪。生後36時間でTSB 15 mg/dL、非抱合型ビリルビン優位。母血液型O型Rh(+)、児血液型A型Rh(+)。最も考えられる診断は？
```

Answer：
```bash
## 症例分析

**最も考えられる診断：ABO血液型不適合による新生児溶血性疾患（ABO-HDN）**

### 診断根拠

| 臨床特徴 | 意義 |
|---------|------|
| **生後24時間以内の黄疸** | 病的黄疸 — 出現時期が早すぎる |
| **TSB 15 mg/dL（257 μmol/L）** | 生理的範囲（ピーク<12.9 mg/dL）を有意に超過 |
| **非抱合型ビリルビン優位** | 溶血性黄疸に一致 |
| **母O型 + 児A型** | ABO-HDNで最も一般的な組み合わせ（母抗A IgGが胎盤通過） |
| **Coombs試験陽性** | 免疫介在性溶血の確定的証拠 |

### 管理

1. **直ちに光線療法を開始** — 高強度青色光（425～475 nm）
2. **TSBをq4～6hで監視** — 交換輸血の要否評価
3. **血算＋網赤血球数** — 貧血重症度評価
4. **IVIG 0.5～1 g/kg** — 溶血の遮断
5. **交換輸血** — TSBが交換輸血閾値以上、または光線療法無効の場合

---

**関連スキル：** [新生児黄疸リスク評価と生理的黄疸診断](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md) · [ビリルビン脳症の病期分類と診断](bilirubin-encephalopathy-staging-and-diagnosis/SKILL.md)
```

#### 3. **試験問題**

Question:
```bash
生後8か月の乳児。3日間の発熱後、解熱してから発疹が出現。最も考えられる診断は？
A. 麻疹
B. 風疹
C. 突発性発疹
D. 猩紅熱
E. 水痘
```

Answer：
```bash
**答え：C. 突発性発疹（Exanthem subitum）**

### 鑑別診断

| 疾患 | 発熱と発疹の関係 | 発疹の特徴 | その他の特徴 |
|------|----------------|-----------|------------|
| A. 麻疹 | 発熱**中**に発疹 | 暗紅色斑丘疹、セファロカウダルに進展 | Koplik斑、カタル症状 |
| B. 風疹 | 発熱**中**に発疹 | 淡紅色斑丘疹、顔面→全身へ急速進展 | 耳介後部/後頭部リンパ節腫脹 |
| **✅ C. 突発性発疹** | **解熱後に発疹** | 薔薇色斑丘疹、体幹→顔面→四肢、1～2日で消退 | 高熱（39～40℃）、全身状態良好 |
| D. 猩紅熱 | 発熱**中**に発疹 | 粟粒大の発赤性皮疹、皮膚皺襞部にPastia線 | 苺舌、咽頭炎 |
| E. 水痘 | 発熱**中**に発疹 | 遠心性分布の「四世代」病変（斑→丘→水疱→痂皮） | 強いそう痒感 |

### なぜ C か？

問題のキーとなる手がかり：
- **生後8か月** → 突発性発疹の最も一般的な年齢（6～18か月）
- **3日間の発熱後、解熱して発疹** → **「解熱発疹」は突発性発疹の古典的特徴**であり、他の発疹性疾患（発熱中に発疹が出現）と明確に区別される
- 薔薇色斑丘疹、体幹から始まり拡大 → 突発性発疹の発疹パターンに一致

### 管理

自己限局性であり、特異的抗ウイルス療法は不要。対症療法が中心：
- 高熱時は解熱剤（物理的冷却、アセトアミノフェン/イブプロフェン）
- 十分な水分摂取の確保
- 熱性けいれんに注意

---

**関連スキル：** [小児感染症の診断と予防](er-tong-chuan-ran-bing-zhen-duan-yu-fang-zhi/SKILL.md)
```

## 著者について

**小绿绿 xllgreen(https://xllgreen.github.io)** — 九江学院臨床医学院 医学生 · テック愛好家

## テクニカルサポート
<br>
PDF2App プロジェクト：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基礎技術研究有限公司 著作権所有
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## ライセンス

本プロジェクトの内容は人民衛生出版社『小児科学』第10版に基づいて整理されており、学習参考のみを目的としています。

## Star History

<a href="https://www.star-history.com/#">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=&type=date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=&type=date" />
 </picture>
</a>
