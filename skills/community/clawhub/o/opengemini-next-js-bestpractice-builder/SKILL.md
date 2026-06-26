---
name: opengemini-nextjs-bestpractice-builder
description: Build opinionated SaaS projects for solo developers with OpenClaw as orchestrator and Gemini CLI as planning and generation copilot, using a fixed best-practice stack: Next.js App Router, Tailwind, shadcn/ui, Neon PostgreSQL, Prisma 6, Clerk, Resend, Stripe, Cloudflare R2, PostHog, Sentry, Vercel, and FastAPI only for Python-required workloads. Use when the user wants to brainstorm, define, scaffold, document, structure, or implement a SaaS with this exact stack and project layout.
---

# Purpose
固定スタックの個人開発SaaSを、ブレない設計と実装ルールで立ち上げる。
技術説明ではなく、実装時の行動基準とプロジェクト構造を強制するための Skill。

# Use when
- Next.js + FastAPI 境界を持つ SaaS を新規に作るとき
- 固定スタックで要件定義から scaffold まで一貫して進めたいとき
- Gemini CLI を使って docs・設計・実装計画を高速化したいとき
- 個人開発向けに現実的で保守しやすい構成を最初から敷きたいとき

# Do not use when
- 技術選定を自由に変えたいとき
- Python が主役のバックエンドを作るとき
- 単なる小規模LPや静的サイトだけを作るとき
- この固定 stack を外す予定が強いとき

# Project assumptions
- Frontend は Next.js App Router
- UI は Tailwind + shadcn/ui
- DB は Neon PostgreSQL
- ORM は Prisma 6
- Auth は Clerk
- Email は Resend
- Payments は Stripe
- Storage は Cloudflare R2
- Analytics は PostHog
- Error Monitoring は Sentry
- Deploy は Vercel
- FastAPI は Python-required workloads のみ

# Rules
- docs を先に作り、実装を後追いさせる
- `GEMINI.md` に source of truth を明記する
- Next.js をデフォルト backend とし、FastAPI を乱用しない
- Clerk auth を Prisma に複製しない
- Stripe 成功判定は webhook 起点にする
- R2 にファイル本体を保存し、DBには metadata だけを置く
- 各 project-level skill は共通テンプレートの型にそろえる
- 各 skill は技術説明ではなく実装時の行動規範として書く
- Prisma は 6 系を固定で使う。7 系へ勝手に上げない
- 開発DBはローカル可だが、本番DBは Neon PostgreSQL を前提にする

# Workflow
1. product goal と MVP を整理する
2. `references/project-bootstrap-checklist.md` を確認する
3. `scripts/bootstrap_tree.sh` で理想構成を作る
4. `scripts/generate_gemini_md.sh` で `GEMINI.md` を作る
5. `scripts/generate_project_docs.sh` で docs を生成する
6. docs を source of truth にして実装へ進む
7. project-level skills を必要に応じて補強する

# Checklist
- `GEMINI.md` があるか
- `docs/requirements.md` から `docs/db-schema.md` まで揃っているか
- `skills/*/SKILL.md` が共通テンプレートに沿っているか
- FastAPI を使う理由が説明できるか
- Stripe / Clerk / R2 の危険なアンチパターンを避けているか
- Vercel deploy 前提の env 設計が見えているか
- Prisma 6 を固定しているか
- 本番DBが Neon を前提に設計されているか

# Common pitfalls
- Next.js で足りる処理まで FastAPI に逃がす
- docs を雑に作って source of truth が死ぬ
- skill を技術メモ化して、行動基準として使えなくする
- Clerk と Prisma の役割を混ぜる
- Stripe webhook を軽視して success redirect に依存する
- file upload を DB 中心で考える
- Prisma 7 に上げて接続・設定周りでハマる

# Output expectations
- `GEMINI.md`
- docs 一式
- 理想ディレクトリ構成
- project-level skills 一式
- stack に沿った実装 plan または scaffold
- 必要なら GitHub / Vercel まで進めるための準備状態

# Source of truth order

When generating or updating project files, treat these as the source of truth in order:
1. `docs/requirements.md`
2. `docs/scope.md`
3. `docs/architecture.md`
4. `docs/conventions.md`
5. `docs/decisions/*.md`
6. `docs/notes/brainstorming.md` is reference only

## Fixed stack policy

- Frontend: Next.js App Router
- UI: Tailwind + shadcn/ui
- DB: Neon PostgreSQL
- ORM: Prisma 6
- Auth: Clerk
- Email: Resend
- Payments: Stripe
- Storage: Cloudflare R2
- Analytics: PostHog
- Error Monitoring: Sentry
- Deploy: Vercel
- Backend: FastAPI only for Python-required workloads

## Backend boundary

Default backend logic lives in Next.js route handlers or server actions.
FastAPI exists only for AI, batch jobs, heavy processing, or Python-specific integrations.

## Never do

- Do not duplicate Clerk auth state into Prisma as a full auth system
- Do not treat Stripe success redirect as source of truth; use webhook state
- Do not store uploaded files in PostgreSQL
- Do not add FastAPI endpoints for simple CRUD unless explicitly required
- Do not upgrade to Prisma 7 by default

## Target project structure

Generate or align toward this structure:

```text
my-saas/
├─ GEMINI.md
├─ src/
│ ├─ app/
│ ├─ components/
│ ├─ features/
│ ├─ lib/
│ ├─ server/
│ ├─ hooks/
│ └─ types/
├─ backend/
│ └─ fastapi/
│ ├─ app/
│ ├─ tests/
│ └─ pyproject.toml
├─ prisma/
│ ├─ schema.prisma
│ ├─ migrations/
│ └─ seed.ts
├─ public/
├─ tests/
│ ├─ unit/
│ ├─ integration/
│ └─ e2e/
├─ docs/
│ ├─ requirements.md
│ ├─ scope.md
│ ├─ architecture.md
│ ├─ conventions.md
│ ├─ integrations.md
│ ├─ db-schema.md
│ ├─ decisions/
│ └─ notes/
│   └─ brainstorming.md
├─ .gemini/
│ └─ commands/
├─ skills/
│ ├─ nextjs/SKILL.md
│ ├─ clerk/SKILL.md
│ ├─ prisma/SKILL.md
│ ├─ shadcn/SKILL.md
│ ├─ stripe/SKILL.md
│ ├─ resend/SKILL.md
│ ├─ posthog/SKILL.md
│ ├─ sentry/SKILL.md
│ ├─ r2/SKILL.md
│ ├─ fastapi/SKILL.md
│ ├─ api-security/SKILL.md
│ └─ vercel/SKILL.md
└─ scripts/
```

## What this skill should produce

For a new project, aim to create at least:
- `GEMINI.md`
- `docs/requirements.md`
- `docs/scope.md`
- `docs/architecture.md`
- `docs/conventions.md`
- `docs/integrations.md`
- `docs/db-schema.md`
- `docs/notes/brainstorming.md`
- `prisma/schema.prisma`
- base app structure under `src/`
- base FastAPI structure under `backend/fastapi/`
- `.env.example`
- integration or implementation plan for Clerk, Stripe, Resend, PostHog, Sentry, and R2

## References

Read when needed:
- `references/doc-templates.md`
- `references/integration-rules.md`
- `references/project-bootstrap-checklist.md`
- `references/project-skill-template.md`

## Publish readiness notes

This skill is strongest when used with Gemini CLI plus OpenClaw file and shell control, and optionally ACP for large implementation loops.
The project-level `skills/*/SKILL.md` files should be implementation policies, not generic framework notes.

Before publishing or using this for a real project, verify:
- Gemini CLI is installed and authenticated
- the generated `skills/*/SKILL.md` files follow the shared template shape
- project docs are generated before major implementation starts
- FastAPI is only introduced when Python is actually required
- deployment assumptions match Vercel reality for the target project
- Prisma is pinned to 6.x
- production DB assumptions match Neon reality
