# PRD: Guard Scanner V2 Architecture & Policy Enforcement

## 1. Objective
guard-scanner を「話題性のある pattern scanner」から、「仕様が一貫し、検知能力が証明可能で、agent security pipeline に組み込める実用ツール（Security policy and analysis layer）」へと進化させる。

## 2. Product Positioning (新ポジショニング)
**"Security policy and analysis layer for agent skills and MCP-connected workflows."**

**[禁止表現]**
- ❌ The first open-source...
- ❌ Zero dependencies (※ `ws` 依存が存在するため事実誤認)
- ❌ Catches what others can't (※ ベンチマーク証明なしの過剰主張)

**[推奨表現]**
- ✅ Lightweight & Policy-aware
- ✅ OpenClaw / MCP-friendly
- ✅ Complementary to existing malware scanners
- ✅ Combines static scans with runtime guardrails

## 3. Core Initiatives

### P0: Single Source of Truth (SSOT) の確立
README, SKILL.md, openclaw.plugin.json, package.json に分散・矛盾している能力値（検知パターン数、カテゴリ数、依存関係）を完全に統一する。
- **実装**: `docs/spec/capabilities.json` を唯一の正解（Canonical Source）とする。
- **CI連携**: `capabilities.json` と 各ドキュメント（README等）の数字が一致しない場合は CI/CD で fail させる仕組みを構築する。

### P0: Security Claim (境界) の再定義
「何でも検知できる」というMarketing Claimを廃し、セキュリティバウンダリを厳密に定義する。
- 冒頭に **"Not a complete defense (銀の弾丸ではない)"** と明記する。
- 静的スキャン（Static-only）で検知できるものと、ランタイム（Runtime hook）や外部通信（VT等）が必要なものを明確に分ける。

### P1: Rule Explainability (検知根拠の透明化)
パターンマッチによるFalse Positive（誤検知）のトリアージコストを下げるため、全 finding に説明メタデータを付与する。
- 追加フィールド: `rationale` (なぜ危険か), `exploit precondition` (成立条件), `likely false-positive cases` (誤検知しやすいケース), `remediation hint` (修正案)。
- SARIF および JSON 出力にこれらを統合する。

### P1: Threat Model Layer (脅威モデリング)
単なるパターンマッチの前に、対象Skillの「権限サーフェス（Threat Model）」を生成する。
- ファイルシステムアクセス権、ネットワーク通信能力、クレデンシャル参照の有無などを評価し、Risk Score の算出ロジックに組み込む（Context-aware validation）。

### P1: Runtime Guard Hardening
`before_tool_call` フックを高度な Policy Engine へと昇華させる。
- `monitor` / `enforce` / `strict` モードの挙動定義を厳密に文書化し、Audit log のスキーマバージョニングを導入する。

### P2: Benchmarking (自前ベンチマークの構築)
競合（他社製品）との比較ではなく、自前のテストデータセット（Benign skills, Malicious skills, Indirect PI samples 等）を用意する。
- `precision` (適合率) と `recall` (再現率) を測定し、「パターン数」ではなく「精度」を前面に押し出す。

## 4. Ecosystem Integration Modes
guard-scanner の動作モードを以下の5つに整理・明文化する。
1. **Offline static scan** (CLIベースの静的スキャン)
2. **Runtime guard mode** (OpenClaw hook / 実行前ブロック)
3. **MCP service mode** (他エージェントからの再利用)
4. **Asset audit mode** (npm/GitHub レジストリ監査)
5. **CI mode** (Fail-on-findings / SARIF出力)
