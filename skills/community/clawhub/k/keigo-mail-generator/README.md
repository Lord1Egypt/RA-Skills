# keigo-mail-generator 

**This README is available in both English and Japanese. English part is included in the latter part of the document.** 

/////////////////////////////////////////////////////////////////
////////////**日本企業向けビジネス敬語メール生成専門スキル**////////////
////////////////////////////////////////////////////////////////

---

## 📋 概要 / Overview
敬語メール作成`keigo-mail-generator`の紹介
* 本スキルは、独自のフレームワークを通じてメールの構成案を提供することで、LLM（大規模言語モデル）による出力の安定性を高め、質の高い敬語メールの草案作成を補助します。
* メールの言い回しや内容に特有のこだわりがある業界でも、カスタムテンプレートを活用することで、ニーズに合わせた最適なメール出力を設計することが可能です。
* また、IDを通じて保存済みの署名を自動的に照合・抽出する機能を備えているため、作成時間を短縮するだけでなく、誤字脱字といったミスも大幅に减らすことができます。

実務におけるプロフェッショナルなコミュニケーションを、AIでより確実に、より効率的にサポートします。

### 📺 デモ動画 / Demo Video
[デモ動画はこちら：敬語メール作成 (OpenClaw Skill) デモ動画](https://www.youtube.com/watch?v=_UD1pcth0Dc)

---

## セキュリティとプライバシー / Security & Privacy
本スキルはローカルLLM `gemma4:26b-a4b-it-q8_0` でテストされていました。  
ローカルLLMを使用する場合、**すべてのデータ（署名情報やメール内容を含む）はユーザーの環境内で完全に処理・保存**されます。OpenAI、Anthropic、Groqなどの外部LLMサーバーへ一切データを送信しません。  
ユーザーの機密情報と知的財産を厳格に保護します。

---

## ✨ 特徴 / Features 
- 非常に自然で正確なビジネス敬語表現
- ユーザー署名の自動管理と永続化機能（LINE、Telegram、Slackに対応。WeChatはsender_idメタデータが含まれないため非対応）
- 「社内テンプレ参照」による社内テンプレートの自然な反映
- 謝罪の度合いに応じた適切な表現（軽め・中程度・重め）

---


## 🚀 使い方 / How to Use 
OpenClaw に送信するコマンド内に「メール」または「keigo mail」などのキーワードを含めることで、SKILL を起動します。

### 示例1: ユーザー署名を含む指令（初回登録時）

**入力例:**
> 「木村不動産の田中太郎です、携帯090-8765-4321。遅延のお詫びメールを山田様宛に書いてください。」

**結果:**  
スキルはユーザーの署名情報（氏名、会社名、携帯）を `user_signatures.db` に記録し、メールのドラフトを生成する。

---


### 示例2: シンプルな指令（保存済みの署名を使用）

**入力例:**
> 「お詫びメールを書いて。納期遅れの件で、株式会社XYZの鈴木様宛。」

**結果:**  
スキルは以前に保存されたユーザーの署名情報を自動的に使用してメールのドラフトを生成します。署名情報を毎回入力する必要はありません。

---


### 示例3: 署名情報の更新・削除（署名データベースからデータを削除するにはキーワード「rm」を使用してください）

**入力例:**
> 「私の情報はこちら：野村不動産の田中太郎、携帯090-1234-5678、email：tanaga@abc.com。桜鑑賞のお誘いメールを鈴木様宛に書いて」
**結果:**  
スキルは更新された署名情報（会社名、携帯、email）を user_signatures.db に上書き保存し、メールのドラフトを生成する。

**入力例:**
> 「私の情報はこちら：携帯：rm、email：rm。鈴木様に映画のお誘いメールを書いて」
**結果:**  
ユーザーの携帯・メール情報を user_signatures.db から削除し、最新の署名でメール下書きを作成します。

---


### 示例4: 社内テンプレートの使用

**注意点:**  
日本では業界ごとにメールのトーン、表現、礼儀が異なる場合が多いです。本スキルは業界特有のテンプレートを読み込んで、より自然で適切なメールを生成できます。

ここでは**不動産業界**を例に説明します。`rag_templates/` フォルダに2つのサンプルテンプレートを用意しています。  
ユーザーはご自身の業界や会社スタイルに合わせてテンプレートを自由に修正・追加してください。

**入力例:**
> 「社内テンプレ参照で、新規営業のメールを書いて。」

**結果:**  
スキルは `rag_templates/` フォルダから関連テンプレート(*.txt, *.md)を検索し、メール本文に自然に反映します（この例では不動産業界らしい表現を使用）。

---


### 示例5: 謝罪の度が重めの指令

**入力例:**
> 「弊社の重大な不手際により多大なご迷惑をおかけしました件について、謝罪の度合いが重めのメールを山田様宛に書いて」

**結果:**  
スキルはメールのドラフトを生成します。謝罪の度合いが重いため、心よりお詫び申し上げます」「深くお詫び申し上げます」などの強い表現を適切に使用し、誠意が十分に伝わる内容にします。また、ユーザーの署名情報もメールの末尾に正しく挿入します。

---


## 🛠 推奨環境 / Recommended Setup 
- **テスト済みモデル**: `gemma4:26b-a4b-it-q8_0`  
  - `gemma4:26b-a4b-it-q8_0` またはそれ以上の高性能モデルを使用することを強く推奨します。モデルの性能は、本スキルの出力品質、自然さ、安定性に大きく影響します。  同じパラメータ規模の場合、**MoEモデルを優先的に使用**してください。Denseモデルより大幅に高速で効率的です。
  - OpenClaw設定(openclaw.json): `"thinkingDefault": "medium"`, `"contextWindow": 120000`
- **OpenClawバージョン**: v2026.4.16
- **推奨ハードウェア環境**: Mac Studio / Mac Mini、64GBメモリ以上（快適な動作のために推奨）

---

## 📊 テスト結果 / Test Results 
**テスト環境：**
- モデル: `gemma4:26b-a4b-it-q8_0`（Ollama経由）
- OpenClaw設定(file: openclaw.json): `"thinkingDefault": "medium"`, `"contextWindow": 120000`
- OpenClawバージョン: v2026.4.16 (running in Docker 4.69.0)
- ハードウェア: Mac Studio M3 Ultra、256GBメモリ

**メール生成時間：**
- 初回メール生成（コールドスタート / モデル＋スキル読み込み時）：**約20〜30秒** 
- 2回目以降の通常メール生成（署名更新なし）：**約10〜25秒**
- 署名更新時または「社内テンプレ参照」使用時のメール生成：**約20〜40秒**
---

## 📁  フォルダ構成 (Project Structure)

keigo-mail-generator/
├── SKILL.md
├── README.md                           
├── scripts/                            # ツールスクリプト用ディレクトリ
│   └── process_signature.py            # ユーザーの署名情報を処理するためのコアスクリプト（SQLite データベース操作）
├── rag_templates/                      # テンプレートフォルダー
│   ├── cold-outreach.txt               # 参考テンプレート：新規営業
│   └── property-viewing-invitation.txt # 参考テンプレート：内見案内誘導
└── users/                              # ユーザーデータディレクトリ（実行時に自動生成）
    └── user_signatures.db              # ユーザー署名データベース（初回書き込み時に自動生成）





////////////////////////////////////////////////////////////////
////**Professional Japanese Keigo Business Email Generator**////
////////////////////////////////////////////////////////////////

---

## 📋 Overview 
Introduction to keigo-mail-generator
Enhanced Stability & Quality: By providing a structured framework for email composition, this skill significantly enhances the output stability of Large Language Models (LLMs), assisting in the creation of high-quality Japanese business email drafts.

Industry-Specific Customization: Even for industries with highly specialized phrasing or content requirements, users can design optimized email outputs tailored to their specific needs using custom templates.

Automated Signature Management: The skill features automated matching and extraction of saved user signatures based on unique IDs. This not only accelerates the drafting process but also substantially reduces manual entry errors, such as typos or omissions.

Empowering professional business communication with AI—ensuring greater reliability and efficiency in every interaction.

### 📺  Demo Video
https://www.youtube.com/watch?v=_UD1pcth0Dc


---

## Security & Privacy 
This skill has been tested with the local LLM `gemma4:26b-a4b-it-q8_0`.  
When used with a local LLM, **all data (including user signatures and email content) is processed and stored entirely locally**. No data is sent to any external LLM servers (such as OpenAI, Anthropic, Groq, etc.).  
User sensitive information and intellectual property are strictly protected.

---

## ✨ Features 
- Highly stable Japanese business honorifics (丁寧語 + 尊敬語 + 謙譲語)
- Automatic user signature management and persistence (supported on LINE, Telegram, and Slack; not supported on WeChat due to missing sender_id metadata)
- Support for “社内テンプレ参照” (internal template injection)
- Smart distinction of apology levels (light / medium / heavy)

---

## 🚀 How to Use 
To activate the SKILL, include trigger words such as 'メール' or 'keigo mail' in the commands sent to OpenClaw.


### Example 1: Command with User Signature (First-time registration)
**Input:**
> 「木村不動産の田中太郎です、携帯090-8765-4321。遅延のお詫びメールを山田様宛に書いてください。」

**Result:**  
The skill will generate the email draft and **record** the user’s signature information (name, company name，mobile) into `user_signatures.db` for future use.

---


### Example 2: Simple Command (Uses saved signature)
**Input:**
> 「お詫びメールを書いて。納期遅れの件で、株式会社XYZの鈴木様宛。」

**Result:**  
The skill will automatically use the previously saved user signature to generate the email draft. 

---


### Example 3: Command for Updating/Removing Signature Information (use 'rm' keyword to remove data from signature database)
**Input:** 
> 「私の情報はこちら：野村不動産の田中太郎、携帯090-1234-5678、email：tanaga@abc.com。桜鑑賞のお誘いメールを鈴木様宛に書いて」

**Result:**  
The skill updates signature information (company name, mobile, email) in user_signatures.db, and generates the email draft with updated signature information.

**Input:** 
> 私の情報はこちら：携帯：rm、email：rm。鈴木様に映画のお誘いメールを書いて

**Result:**  
The skill removes user's mobile and email info from user_signatures.db, and generates the email draft with updated signature info. 

---



### Example 4: Using Internal Template
**Note:**  
Different industries in Japan often have their own unique email tone, phrasing, and etiquette. This skill supports loading industry-specific templates to generate more appropriate and natural emails.

For example, here we use the **real estate industry (不動産業界)** as a demonstration. Two sample templates have been placed in the `rag_templates/` folder.  
Users can freely modify or add their own templates to better suit their specific industry or company style.

**Input:**
> 「社内テンプレ参照で、新規営業のメールを書いて。」

**Result:**  
The skill searches the `rag_templates/` folder for text file (*.txt, *.md) and naturally incorporate matching internal templates (for example, real estate industry style) to the email draft.

---



### Example 5: Command for a Strong Apology Email
**Input:**
> 「弊社の重大な不手際により多大なご迷惑をおかけしました件について、謝罪の度合いが重めのメールを山田様宛に書いて」

**Result:**  
The skill generates the email draft. Since a strong level of apology is required, it appropriately uses strong expressions such as "We sincerely apologize from the bottom of our hearts" and "We deeply regret our actions" to ensure the message conveys sufficient sincerity. In addition, the user's signature information is correctly inserted at the end of the email.

---



## 🛠 Recommended Setup

- **Tested Model**: `gemma4:26b-a4b-it-q8_0`  
  - It is strongly recommended to use `gemma4:26b-a4b-it-q8_0` or an even stronger model. Model performance is fundamental to the skill’s output quality,naturalness, and stability. At the same parameter size, **MoE models are highly recommended** over dense models, as they offer significantly better speed and efficiency.
  - OpenClaw設定(openclaw.json): `"thinkingDefault": "medium"`, `"contextWindow": 120000`
- **OpenClaw Version**: v2026.4.16
- **Hardware Environment**: Mac Studio / Mac Mini、64GB memory or above (recommended for optimal performance)

---


## 📊 Test Results 

**Tested Environment:**
- Model: `gemma4:26b-a4b-it-q8_0` (via **Ollama**)
- OpenClaw Configuration (file: openclaw.json): `"thinkingDefault": "medium"`, `"contextWindow": 120000`
- OpenClaw Version: v2026.4.16 (running in Docker 4.69.0)
- Hardware: Mac Studio M3 Ultra, 256GB Memory

**Email Generation Time:**
- First email generation (cold start / loading model + skill): **20 ~ 30 seconds**
- Subsequent email generation (no signature update): **~10 ~ 25 seconds**
- Email generation with signature update or “社内テンプレ参照”: **20 ~ 40 seconds**


---

## 📁 Project Structure / フォルダ構成


keigo-mail-generator/
├── SKILL.md
├── README.md                           # This file
├── scripts/                            # Directory for tool scripts
│   └── process_signature.py            # Core script for processing user signature information (SQLite database operations)
├── rag_templates/                      # Template folder
│   ├── cold-outreach.txt               # A sample template for cold outreach / new business development
│   └── property-viewing-invitation.txt # A sample template for property viewing invitation
└── users/                              # User data directory (automatically created at runtime)
    └── user_signatures.db              # User signature database ((will be automatically created on first write))


## ⚠️ 免責事項 / Disclaimer
**日本語** 
本スキルは個人利用および社内利用を目的として「現状のまま」提供されます。  
生成されたメールはAIによるドラフトに過ぎません。送信前に内容を必ず自分で確認・修正し、正確性、適切性、法的適合性を責任を持って判断してください。

本スキルの生成したメールに起因する一切の結果（業務上の誤解、法的紛争、信用失墜など）について、作者は一切の責任を負いません。

**English** 
This skill is provided as-is for personal and internal company use.  
The generated emails are AI-assisted drafts only. Users are fully responsible for reviewing, modifying, and ensuring the accuracy, appropriateness, and legal compliance of any email before sending.  

The author is not liable for any consequences arising from the use of emails generated by this skill, including but not limited to business misunderstandings, legal disputes, or reputational damage.

---