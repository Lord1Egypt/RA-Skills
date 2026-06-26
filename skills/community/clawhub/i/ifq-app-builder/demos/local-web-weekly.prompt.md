---
templateId: T-local-web-nextjs
ifqMode: A-10
stack: nextjs-15 + postgres + docker-compose
artifact: docker image + compose
locale: ['zh-CN', 'en']
---

# local-web-weekly — A-10 / T-local-web-nextjs

Mode A-10, template T-local-web-nextjs. A self-hosted weekly engineering report prompt bundle.

## S1 — WHO + WHAT

研发经理每周收集团队成员提交的周报，按项目、风险、下周计划和阻塞项生成一份部门视图。输入是浏览器表单与 CSV 导入，输出是可筛选的周报列表、项目汇总和导出的 `.csv`。

## S2 — WHERE

公司内网自托管 Web 应用，Docker Compose 一键启动，PostgreSQL 持久化，LDAP 登录。部署在内网 Linux 服务器，不需要公网访问。Locales: zh-CN 与 en。

## S3 — HOW SUCCESS LOOKS

`docker compose up -d` 后 2 分钟内可登录；团队成员能提交周报，经理能按项目筛选并导出 CSV；产物为 `ifq-weekly-web:1.0.0` docker image 与 `docker-compose.yml`；非目标：不做公网 SaaS、不做聊天机器人、不接企业微信消息。

## Acceptance (binary, yes/no observable)

- [ ] `docker compose up -d` 后 Web、Postgres、migration 全部 healthy。
- [ ] LDAP 测试账号能登录，未授权账号被拒绝。
- [ ] 成员可创建、编辑、提交本周周报，提交后经理可见。
- [ ] 经理可按项目筛选并导出 `.csv`，导出文件包含 UTF-8 BOM 以兼容 Excel。
- [ ] zh-CN 与 en 均存在，主流程无硬编码单语言残留。

## Scaffold (run order)

1. Scaffold Next.js 15 App Router + TypeScript.
2. Add PostgreSQL schema and migration for users, reports, projects, audit log.
3. Add LDAP auth adapter with environment-based config.
4. Add `src/i18n/zh-CN.json` and `src/i18n/en.json`.
5. Build submit, manager review, export, and admin project pages.
6. Add Dockerfile and `docker-compose.yml`.
7. Run migration, seed sample data, then verify main flow.

## Packaging

- Image: `docker build -t ifq-weekly-web:1.0.0 .`.
- Runtime: `docker compose up -d` with `web`, `db`, and `migration` services.
- Backup: `docker compose exec db pg_dump -U app app > backup.sql`.

## Security baseline

- All mutations enforce server-side role checks; deny by default.
- Session cookies are HttpOnly, SameSite=Lax, Secure behind the internal TLS proxy.
- Database access uses parameterized queries only; no string-concat SQL.
- LDAP bind password is supplied by environment variable outside the repo.
- Structured logs never print passwords, session cookies, or LDAP bind secrets.

## IFQ ambient

Use warm paper background only in low-density pages; manager tables stay dense and operational. Add mono field-notes timestamps, rust accent for submit/export, and one quiet footer colophon.

## Agent execution contract

- Do not ask for real LDAP credentials in the prompt-bundle phase.
- Use placeholder env var names and document them; never invent live secrets.
- Claim deployment success only after `docker compose ps` is healthy and the app responds locally.

— shaped with ifq.ai/app-builder · A-10 · T-local-web-nextjs
