# 🏯 Imperial Orchestrator

[中文](../README.md) | [English](./README.en.md) | **[日本語](./README.ja.md)** | [한국어](./README.ko.md) | [Español](./README.es.md) | [Français](./README.fr.md) | [Deutsch](./README.de.md)

---

OpenClaw 高可用マルチロールモデルオーケストレーション Skill —— 三省六部制インテリジェントルーティング。

> **設計インスピレーション**: ロールアーキテクチャは古代中国の[三省六部制](https://github.com/cft0808/edict)の朝廷統治パターンに基づき、[PUA](https://github.com/tanweai/pua)のディープAIプロンプトエンジニアリング技術を融合しています。

## コア機能

- **三省六部** ロールオーケストレーション：10のロール、それぞれ明確な責務
- **自動発見** openclaw.jsonから46+モデルを読み取り
- **インテリジェントルーティング** ドメイン別自動振り分け（コーディング/運用/セキュリティ/ライティング/法務/財務）
- **Opus優先** コーディング/セキュリティ/法務タスクは最強モデルを優先使用
- **クロスプロバイダーフェイルオーバー** auth サーキットブレーカー → ベンダー間降格 → ローカルサバイバル
- **リアル実行** API呼び出し + トークン計算 + コスト追跡
- **ベンチマーク** 同一タスクを全モデルに投入、スコアリング＆ランキング
- **多言語対応** 7言語サポート：zh/en/ja/ko/es/fr/de

## クイックスタート

```bash
# 1. モデル発見
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. モデル検証
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. タスクルーティング
python3 scripts/router.py --task "Goで並行安全なLRU Cacheを書いて" --state-file .imperial_state.json

# ワンコマンド
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"
```

## ロール体系：三省六部

各ロールには、アイデンティティ、責務範囲、行動規則、協調意識、レッドラインの5つの次元を含む深層システムプロンプトが装備されています。

### 中枢

| ロール | 官職 | 朝制対応 | コアミッション |
|--------|------|----------|----------------|
| **router-chief** | 中枢総管 | 天子/中枢院 | システムのライフライン——分類、ルーティング、ハートビート維持 |

### 三省

| ロール | 官職 | 朝制対応 | コアミッション |
|--------|------|----------|----------------|
| **cabinet-planner** | 内閣首輔 | 中書省 | 方略起草——混沌を秩序あるステップに分解 |
| **censor-review** | 都御史 | 門下省/都察院 | 封駁審査——品質の最後の門番 |

### 六部

| ロール | 官職 | 朝制対応 | コアミッション |
|--------|------|----------|----------------|
| **ministry-coding** | 工部尚書 | 工部 | 工事興修——コーディング、デバッグ、アーキテクチャ |
| **ministry-ops** | 工部侍郎（営繕司） | 工部·営繕司 | 駅站維持——デプロイ、運用、CI/CD |
| **ministry-security** | 兵部尚書 | 兵部 | 辺境防衛——セキュリティ監査、脅威モデリング |
| **ministry-writing** | 礼部尚書 | 礼部 | 文教礼儀——コピーライティング、ドキュメント、翻訳 |
| **ministry-legal** | 刑部尚書 | 刑部 | 律法刑獄——契約、コンプライアンス、条項 |
| **ministry-finance** | 戸部尚書 | 戸部 | 銭糧賦税——価格設定、利益率、決済 |

### 急遞舗

| ロール | 官職 | 朝制対応 | コアミッション |
|--------|------|----------|----------------|
| **emergency-scribe** | 急遞舗令 | 急遞舗 | システムを絶対にダウンさせない最後の保障 |

## 運用ルール

1. **401 サーキットブレーカー** — auth失敗は即座に`auth_dead`マーク、authチェーン全体をクールダウン、クロスプロバイダー切替を優先
2. **ルーターは軽量に** — router-chiefに最重のプロンプトや最脆弱なプロバイダーを割り当てない
3. **クロスプロバイダー優先** — フォールバック順序：同ロール別プロバイダー → ローカルモデル → 隣接ロール → 急遞舗
4. **降格してもダウンしない** — 最強モデルが全滅しても、アーキテクチャ提案・チェックリスト・擬似コードで応答

## プロジェクト構造

```
config/
  agent_roles.yaml          # ロール定義（責務、能力、フォールバックチェーン）
  agent_prompts.yaml        # 深層システムプロンプト（アイデンティティ、ルール、レッドライン）
  routing_rules.yaml        # ルーティングキーワードルール
  failure_policies.yaml     # サーキットブレーカー/リトライ/降格ポリシー
  benchmark_tasks.yaml      # ベンチマークタスクライブラリ
  model_registry.yaml       # モデル能力オーバーライド
  i18n.yaml                 # 7言語適応
scripts/
  lib.py                    # コアライブラリ（発見、分類、状態管理、i18n）
  router.py                 # ルーター（ロールマッチング + モデル選択）
  executor.py               # 実行エンジン（API呼び出し + フォールバック）
  orchestrator.py           # フルパイプライン（ルーティング → 実行 → レビュー）
  health_check.py           # モデル発見
  model_validator.py        # モデル探索
  benchmark.py              # ベンチマーク + リーダーボード
  route_and_update.sh       # 統合CLIエントリポイント
```

## インストール

### 前提条件：OpenClaw のインストール

```bash
# 1. OpenClaw CLI をインストール（macOS）
brew tap openclaw/tap
brew install openclaw

# または npm 経由でインストール
npm install -g @openclaw/cli

# 2. 設定を初期化
openclaw init

# 3. モデルプロバイダーを設定（~/.openclaw/openclaw.json を編集）
openclaw config edit
```

> 詳細なインストール手順は [OpenClaw 公式リポジトリ](https://github.com/openclaw/openclaw) を参照してください

### Imperial Orchestrator スキルのインストール

```bash
# オプション 1：GitHub からクローン
git clone https://github.com/rexnode/imperial-orchestrator.git
cp -r imperial-orchestrator ~/.openclaw/skills/

# オプション 2：グローバルスキルディレクトリに直接コピー
cp -r imperial-orchestrator ~/.openclaw/skills/

# オプション 3：ワークスペースレベルのインストール
cp -r imperial-orchestrator <your-workspace>/skills/
```

### インストールの確認

```bash
# モデルの検出とプローブ
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state .imperial_state.json

# ルーティングの動作確認
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/router.py \
  --task "Write a Hello World" \
  --state-file .imperial_state.json
```

## セキュリティ

- プロンプトにシークレットを送信しない
- 探索リクエストは最小限に
- プロバイダーヘルスとモデル品質は分離管理
- コンフィグに存在するモデル ≠ 安全にルーティング可能

## ライセンス

MIT
