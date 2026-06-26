#!/usr/bin/env bash
set -euo pipefail

root="${1:-my-saas}"
mkdir -p "$root"/{public,prisma/migrations,tests/unit,tests/integration,tests/e2e,scripts}
mkdir -p "$root"/src/{app,components,features,lib,server,hooks,types}
mkdir -p "$root"/backend/fastapi/{app,tests}
mkdir -p "$root"/docs/{decisions,notes}
mkdir -p "$root"/.gemini/commands
mkdir -p "$root"/skills/{nextjs,clerk,prisma,shadcn,stripe,resend,posthog,sentry,r2,fastapi,api-security,vercel}

touch "$root"/prisma/schema.prisma

touch "$root"/prisma/seed.ts

touch "$root"/backend/fastapi/pyproject.toml

touch "$root"/docs/{requirements.md,scope.md,architecture.md,conventions.md,integrations.md,db-schema.md}

touch "$root"/docs/notes/brainstorming.md

cat > "$root/skills/nextjs/SKILL.md" <<'EOF'
---
name: nextjs
description: Use this skill for Next.js App Router work including pages, layouts, route handlers, server actions, metadata, loading/error states, and server/client component boundaries.
---

# Purpose
Next.js App Router の実装を一貫した方針で行う。

# Use when
- 新しいページを追加するとき
- layout を作る/修正するとき
- route handler を追加するとき
- server action を実装するとき
- server component / client component の切り分けが必要なとき

# Do not use when
- Python API のみを触るとき
- DBスキーマ変更だけが目的のとき
- UIコンポーネント単体設計だけなら shadcn Skill を優先

# Project assumptions
- App Router を採用
- TypeScript strict
- 認証は Clerk
- DB は Prisma
- UI は shadcn/ui
- 原則として backend logic は Next.js 側に置く

# Rules
- app router のファイル規約に従う
- server component をデフォルトにし、必要時のみ client component にする
- 単純CRUDのために FastAPI を増やさない
- route handlers は外部公開APIやwebhook用途を優先する
- フォーム処理は server action を第一候補とする
- metadata, loading, error, not-found の要否を検討する

# Workflow
1. 対象ルートと責務を確認
2. page/layout/loading/error の必要性を判断
3. server/client 境界を決める
4. データ取得方法を決める
5. 認証・認可を確認する
6. 実装
7. テストまたは動作確認

# Checklist
- server/client 境界は妥当か
- 認証保護が必要な画面に guard があるか
- エラー状態が考慮されているか
- metadata が必要なら設定したか
- 不要な use client を増やしていないか

# Common pitfalls
- なんでも client component にする
- route handler と server action の責務が混ざる
- 権限チェックなしで dashboard を出す
- fetch と Prisma の責務を混在させる

# Output expectations
- 変更ファイル一覧
- 実装内容の要約
- 必要なテストまたは動作確認
- 必要なら docs 更新
EOF

cat > "$root/skills/clerk/SKILL.md" <<'EOF'
---
name: clerk
description: Use this skill when implementing authentication, user sessions, protected routes, Clerk middleware, webhook-based user sync, or account/profile flows with Clerk.
---

# Purpose
認証・セッション管理を Clerk 中心で安全に実装する。

# Use when
- サインイン/サインアップ導線を作る
- 認証付きページを追加する
- middleware で保護する
- Clerk webhook を処理する
- ユーザープロフィール連携を作る

# Do not use when
- 課金だけを触るとき
- DBスキーマだけを変えるとき

# Project assumptions
- 認証の source of truth は Clerk
- Prisma には業務用 user/profile/organization データのみ保持
- Clerk の完全な auth state を Prisma に複製しない

# Rules
- 認証判定は Clerk で行う
- 権限/ロールが必要な場合は app DB に最小限の拡張情報だけ持つ
- webhook で必要な同期だけ行う
- middleware 保護と server-side 保護の両方を意識する
- 認可ロジックは「ログインしているか」と「何をしてよいか」を分ける

# Workflow
1. ルートの保護要件を確認
2. Clerk middleware の適用有無を確認
3. UI ルートと server-side チェックを実装
4. 必要なら webhook で user sync
5. 権限・プロフィールを app DB に反映

# Checklist
- 非ログイン時の挙動が定義されているか
- サーバー側でも認証確認しているか
- Clerk webhook の署名検証があるか
- DBに auth 本体を重複保存していないか

# Common pitfalls
- Clerk と Prisma の両方を auth 正本にする
- middleware だけで十分だと思い込む
- webhook なしで user 同期前提の実装をする

# Output expectations
- 保護対象ルート
- 認証/認可の実装内容
- webhook の有無
- 必要な docs 更新
EOF

cat > "$root/skills/prisma/SKILL.md" <<'EOF'
---
name: prisma
description: Use this skill for Prisma schema changes, migrations, database access patterns, seed scripts, and query/model design with PostgreSQL.
---

# Purpose
Prisma と PostgreSQL の変更を安全に行う。

# Use when
- schema.prisma を変更するとき
- migration を作るとき
- 新しい model/relation を作るとき
- query を追加するとき
- seed を更新するとき

# Do not use when
- UI変更のみのとき
- 認証フローのみのとき

# Project assumptions
- DB は Neon PostgreSQL
- ORM は Prisma
- DB変更時は migration 必須
- DB access は Prisma client 経由を基本とする

# Rules
- schema 変更だけで終わらせず migration を作る
- 命名規則を統一する
- nullable は安易に増やさない
- index / unique / relation を明示的に考える
- 課金や権限に関わる状態は曖昧にしない

# Workflow
1. 要件からデータモデルを整理
2. schema.prisma を更新
3. migration を作成
4. seed / 型 / 参照コードを更新
5. 既存データ影響を確認
6. テスト

# Checklist
- migration があるか
- relation は妥当か
- enum/unique/index の見落としはないか
- 削除時の挙動が定義されているか
- webhook 由来の外部IDを保存するならカラム設計があるか

# Common pitfalls
- Prisma schema だけ変えて migration を作らない
- 後から困る external_id を保存しない
- Stripe / Clerk 由来の識別子を曖昧にする

# Output expectations
- schema 変更点
- migration の有無
- 影響範囲
- テスト/確認項目
EOF

cat > "$root/skills/shadcn/SKILL.md" <<'EOF'
---
name: shadcn
description: Use this skill when building or modifying UI with Tailwind CSS and shadcn/ui components, including forms, dialogs, tables, cards, and design consistency work.
---

# Purpose
shadcn/ui と Tailwind で統一感のあるUIを作る。

# Use when
- 新しいUIを作る
- フォームやダイアログを作る
- テーブルやカードを整える
- デザイン整合性を保つ

# Do not use when
- DBやAPIのみを触るとき
- Pythonバックエンドだけの作業

# Project assumptions
- UIは shadcn/ui ベース
- Tailwind utility-first
- 既存コンポーネントを優先して再利用する

# Rules
- まず既存UIを探して再利用する
- コンポーネントの責務を分ける
- アクセシビリティを意識する
- 状態ごとの見た目を作る
- 空状態/エラー状態/ローディング状態を省略しない

# Workflow
1. 既存UIを確認
2. 再利用できるか判断
3. 状態ごとのUIを設計
4. 実装
5. モバイル確認

# Checklist
- ラベルと入力が対応しているか
- キーボード操作を妨げないか
- 余白・サイズ・階層が既存画面と一致しているか
- モバイルで破綻しないか

# Common pitfalls
- 似たコンポーネントを量産する
- Tailwind class を各所に重複させる
- 空状態とエラー状態を作らない

# Output expectations
- 変更コンポーネント一覧
- 状態パターン
- UI確認項目
EOF

cat > "$root/skills/stripe/SKILL.md" <<'EOF'
---
name: stripe
description: Use this skill for Stripe checkout, billing portal, subscriptions, webhook handling, payment state synchronization, and product/price integration.
---

# Purpose
Stripe連携を安全に実装する。

# Use when
- Checkout を作る
- Billing Portal を作る
- subscription 状態を扱う
- webhook を処理する
- price / product ID を使う

# Do not use when
- 認証だけの作業
- UIの見た目調整だけの作業

# Project assumptions
- 支払い状態の source of truth は Stripe webhook
- アプリDBには必要最小限の billing state を保存
- success URL のみで課金成功確定にしない

# Rules
- 決済結果は webhook で反映する
- product/price ID は環境変数や設定ファイルで管理する
- idempotency と再送を意識する
- ユーザー/組織との紐づけを明確にする
- テストモードと本番モードを混同しない

# Workflow
1. 商品・価格・課金モデルを確認
2. checkout / portal 導線を実装
3. webhook 署名検証を実装
4. DBへ billing state を同期
5. UIの制限解除条件を webhook state に連動させる

# Checklist
- webhook 検証があるか
- success redirect 依存になっていないか
- Stripe customer ID を保存しているか
- subscription status の扱いが明確か

# Common pitfalls
- success page だけで有料化する
- webhook 再送を考慮しない
- customer / subscription / price のID管理が曖昧

# Output expectations
- Checkout/Portal/Webhook の実装範囲
- 保存する billing state
- テスト観点
EOF

cat > "$root/skills/resend/SKILL.md" <<'EOF'
---
name: resend
description: Use this skill when sending transactional email, onboarding email, passwordless or verification-related messaging, or templated app notifications via Resend.
---

# Purpose
Resend を使ったアプリメール送信を整理する。

# Use when
- トランザクションメールを送る
- オンボーディングメールを送る
- 通知メールやテンプレメールを作る

# Do not use when
- 認証の中核管理だけを触るとき
- UIだけを作るとき

# Project assumptions
- メールは transactional を中心に扱う
- 送信ロジックは server-side に置く

# Rules
- 送信用途を transactional に限定して整理する
- メール文面はテンプレート化する
- 宛先・件名・本文生成の責務を分ける
- ローカル/本番の送信動作差を意識する

# Workflow
1. 送信トリガーを整理
2. テンプレートを定義
3. 送信処理を server-side に実装
4. 失敗時ログと再送方針を確認

# Checklist
- 送信元ドメイン設定前提を満たすか
- 再送時の影響を考慮しているか
- エラー時のログがあるか

# Common pitfalls
- 文面をコードにベタ書きする
- 再送影響を考えない

# Output expectations
- 送信トリガー
- テンプレ一覧
- エラー処理方針
EOF

cat > "$root/skills/posthog/SKILL.md" <<'EOF'
---
name: posthog
description: Use this skill when implementing product analytics, feature flags, event naming, funnel tracking, or server/client analytics integration with PostHog.
---

# Purpose
計測イベントを一貫して設計する。

# Use when
- 主要イベントを計測する
- Funnel を作る
- feature flag を使う

# Do not use when
- UIだけを直すとき
- DB変更だけをするとき

# Project assumptions
- 重要イベントだけを絞って送る
- PII は最小限にする

# Rules
- イベント名を人間が読める命名にする
- server/client どちらで送るかを決める
- 重要イベントだけを絞って入れる
- PII を安易に送らない

# Workflow
1. 計測したい行動を定義
2. イベント名を決める
3. server/client の送信場所を決める
4. 二重送信を防ぐ

# Checklist
- イベント名が統一されているか
- 二重送信していないか
- 課金や登録完了など主要イベントがあるか

# Common pitfalls
- イベントを増やしすぎる
- 命名がブレる

# Output expectations
- イベント一覧
- 実装箇所
- 計測意図
EOF

cat > "$root/skills/sentry/SKILL.md" <<'EOF'
---
name: sentry
description: Use this skill when adding error monitoring, exception capture, tracing, performance monitoring, or structured production diagnostics with Sentry.
---

# Purpose
本番障害の追跡性を上げる。

# Use when
- エラー監視を入れる
- 例外捕捉を強化する
- tracing を追加する

# Do not use when
- 単純なUI作業だけのとき

# Project assumptions
- PII は最小限
- フロント/サーバー両方で必要箇所を監視

# Rules
- 握りつぶす例外を減らす
- 重要な境界で context を付与する
- PII を不用意に送らない
- フロント/サーバー双方の監視対象を意識する

# Workflow
1. 重要フローを特定
2. 例外捕捉点を決める
3. 文脈情報を整理
4. ノイズを抑える

# Checklist
- 重要処理で例外が捕捉されるか
- user id / org id など最小限の文脈が付くか
- ノイズだらけのログになっていないか

# Common pitfalls
- なんでも送ってノイズ化する
- 文脈が足りず調査不能になる

# Output expectations
- 監視対象
- 例外捕捉箇所
- 文脈情報
EOF

cat > "$root/skills/r2/SKILL.md" <<'EOF'
---
name: r2
description: Use this skill for file upload flows, signed URL generation, object key design, metadata handling, and Cloudflare R2-backed storage patterns.
---

# Purpose
ファイル保存を DB ではなく R2 に安全に寄せる。

# Use when
- ファイルアップロードを実装する
- signed URL を扱う
- metadata 設計をする

# Do not use when
- DB設計のみをする
- UIだけを触るとき

# Project assumptions
- バイナリはR2
- メタデータはDB

# Rules
- バイナリ本体を PostgreSQL に保存しない
- object key 命名規則を統一する
- 公開/非公開アクセス方針を先に決める
- メタデータはDBに保持する

# Workflow
1. アクセス方針を決める
2. key 設計を決める
3. upload と metadata 保存を分ける
4. 削除整合を確認する

# Checklist
- key 設計が衝突しないか
- アクセス制御があるか
- 削除時に DB と Storage の整合がとれるか

# Common pitfalls
- DBにバイナリ保存する
- key が雑で衝突する

# Output expectations
- key 設計
- upload フロー
- metadata モデル
EOF

cat > "$root/skills/fastapi/SKILL.md" <<'EOF'
---
name: fastapi
description: Use this skill only for Python-required backend workloads such as AI pipelines, batch jobs, heavy processing, or Python-native integrations exposed through FastAPI.
---

# Purpose
FastAPI を必要最小限に保つ。

# Use when
- Pythonライブラリ必須
- AI処理
- 重い非同期処理
- バッチ/ワーカーAPI

# Do not use when
- 単純CRUD
- 認証付き通常画面API
- Next.js で十分な処理

# Project assumptions
- FastAPI は補助的 backend
- 主 backend は Next.js 側

# Rules
- FastAPI を万能バックエンドにしない
- 公開境界と内部境界を明確にする
- 認証・署名・レート制限を意識する
- Next.js 側と責務を分ける

# Workflow
1. Python が本当に必要か確認
2. 入出力境界を定義
3. 認証と制限を定義
4. Next.js 側との責務を固定

# Checklist
- 本当に Python が必要か
- 同じ処理を Next.js に置けないか
- 入出力スキーマが定義されているか

# Common pitfalls
- 何でも FastAPI に逃がす
- 境界が曖昧

# Output expectations
- FastAPI 側で持つ責務
- API 入出力
- Next.js との境界
EOF

cat > "$root/skills/api-security/SKILL.md" <<'EOF'
---
name: api-security
description: Use this skill when building any route handler, webhook, external API integration, internal API boundary, authorization rule, or security-sensitive request flow.
---

# Purpose
API境界の安全性を保つ。

# Use when
- route handler を作る
- webhook を作る
- 外部APIを繋ぐ
- 認可や入力検証が必要

# Do not use when
- UIだけを触るとき

# Project assumptions
- 認証と認可を分ける
- 入力検証は必須

# Rules
- 認証と認可を分けて考える
- webhook は署名検証する
- 入力検証を必須にする
- 秘密情報をログに出さない
- 最小権限で設計する

# Workflow
1. 誰が呼ぶAPIかを定義
2. 入力スキーマを決める
3. 認証と認可を分ける
4. 署名やレート制限要否を確認

# Checklist
- 誰が呼べるAPIか明確か
- 入力バリデーションがあるか
- エラー時に秘密が漏れないか
- rate limit の要否を検討したか

# Common pitfalls
- 認証だけ見て認可を忘れる
- webhook 署名検証を省く

# Output expectations
- セキュリティ境界
- バリデーション
- 保護方式
EOF

cat > "$root/skills/vercel/SKILL.md" <<'EOF'
---
name: vercel
description: Use this skill when configuring deployment, environment variables, preview environments, production settings, domain setup, and Vercel-specific deployment behavior.
---

# Purpose
Vercel への安定デプロイを保つ。

# Use when
- deployment 設定をする
- env var を整理する
- preview / production 差分を調整する
- callback URL や webhook URL を確認する

# Do not use when
- ローカルUI調整だけのとき

# Project assumptions
- Vercel が Next.js の標準デプロイ先
- Preview / Production を分けて考える

# Rules
- 環境変数は整理して管理する
- Preview / Production の差異を意識する
- webhook URL や callback URL の環境差分を確認する
- ビルド時と実行時の差を意識する

# Workflow
1. 必須 env を洗い出す
2. preview / production 差分を確認
3. auth/callback/webhook URL を確認
4. deploy 後の確認項目を回す

# Checklist
- 必須 env が揃っているか
- Preview でも auth/callback が壊れないか
- 本番ドメイン前提の値を直書きしていないか

# Common pitfalls
- callback URL の環境差分を忘れる
- env の入れ忘れ

# Output expectations
- 必須 env 一覧
- deploy 設定
- post-deploy checks
EOF

echo "Bootstrapped $root"
