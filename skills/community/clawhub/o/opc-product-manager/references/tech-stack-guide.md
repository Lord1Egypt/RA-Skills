# Tech Stack Guide

> Opinionated stack recommendations for solo builders. Not a comparison — a decision.
> Load with `read_file("references/tech-stack-guide.md")` during Phase 2 (Spec Generation) and Tech Stack mode.

---

## Principles

These stacks are optimized for:

1. **Fast to build** — minimal boilerplate, good AI agent support, strong ecosystem
2. **Cheap to run** — free tiers, predictable pricing, no surprise bills
3. **Easy to deploy** — one command or git push, no DevOps knowledge needed
4. **Solo-friendly** — one person can build, maintain, and debug this

---

## Stacks by Product Type

### Web App (`web_app`)

**SaaS tools, dashboards, marketplaces, CRUD apps with a frontend.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Frontend | **Next.js 14+** (App Router) | Full-stack in one framework, excellent AI agent support, huge ecosystem |
| Backend | Next.js API Routes / Server Actions | No separate backend needed for most apps |
| Database | **Supabase** (Postgres) | Free tier generous, built-in auth + storage + realtime, SQL access |
| Auth | **Supabase Auth** | Magic link or OAuth out of the box, no custom auth code |
| Deployment | **Vercel** | Git push to deploy, free tier covers most solo projects |
| Key packages | `@supabase/supabase-js`, `tailwindcss`, `shadcn/ui`, `zod` |
| Estimated cost | Free ($0/mo for launch, $25/mo if scaling) |

**Alternative**: If you prefer Python → FastAPI backend + React frontend + Supabase + Railway ($5/mo).

---

### API Service (`api_service`)

**Backend APIs, webhook handlers, microservices, data processing pipelines.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Runtime | **Python 3.11+** with **FastAPI** | Fastest to write, excellent AI agent support, async by default |
| Database | **SQLite** (small/local) or **Supabase Postgres** (scale) | SQLite = zero config; Supabase = when you need remote access |
| Auth | API keys (simple) or **Supabase Auth** (if user-facing) | Don't over-engineer auth for internal APIs |
| Deployment | **Railway** or **Fly.io** | Railway: git push deploy, generous free tier. Fly.io: global edge. |
| Key packages | `fastapi`, `uvicorn`, `pydantic`, `httpx`, `sqlalchemy` (if Postgres) |
| Estimated cost | $0-5/mo (Railway free tier) to $20/mo |

**Alternative**: If you prefer TypeScript → Hono + Bun + Cloudflare Workers ($0/mo).

---

### CLI Tool (`cli_tool`)

**Command-line tools, scripts, developer utilities.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Language | **Python 3.11+** | Widest reach, easiest to distribute, excellent stdlib |
| CLI framework | **Click** or **argparse** (stdlib) | Click for rich CLI; argparse for zero-dependency |
| State/config | **SQLite** (if persistent state) or JSON files | SQLite for structured data; JSON for simple config |
| Distribution | **pip** (PyPI) or single-file script | PyPI for public tools; single file for personal tools |
| Key packages | `click`, `rich` (pretty output), `httpx` (HTTP), `pathlib` |
| Estimated cost | $0 |

**Alternative**: If you prefer TypeScript → Node.js + Commander.js + tsx.

---

### Browser Extension (`browser_extension`)

**Chrome extensions, Firefox add-ons.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Framework | **Plasmo** or vanilla JS with Manifest V3 | Plasmo handles boilerplate; vanilla for simple extensions |
| UI | **React** (via Plasmo) or plain HTML/CSS | React for complex popup/options UI; plain for simple |
| Storage | **chrome.storage API** | Built-in, no external DB needed |
| Background | **Service workers** (Manifest V3) | Required for modern Chrome extensions |
| Distribution | Chrome Web Store ($5 one-time fee) |
| Key packages | `plasmo`, `react` (optional), `@anthropic-ai/sdk` (if AI-powered) |
| Estimated cost | $5 one-time (Chrome Web Store) |

---

### Mobile App (`mobile_app`)

**iOS and Android apps.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Framework | **React Native** + **Expo** | One codebase, both platforms, Expo simplifies everything |
| Backend | **Supabase** | Same reasons as web app — auth, DB, storage, realtime |
| Auth | **Supabase Auth** with Expo auth helpers | Social login + magic link out of the box |
| Deployment | **Expo EAS** (build + submit to stores) | No Xcode/Android Studio needed for builds |
| Key packages | `expo`, `expo-router`, `@supabase/supabase-js`, `nativewind` |
| Estimated cost | $0-25/mo (Expo free tier → EAS Build costs at scale) |

**Alternative**: If you prefer native → Swift (iOS only) or Kotlin (Android only). Only if single-platform.

---

### Static Site (`static_site`)

**Landing pages, portfolios, documentation, blogs.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Framework | **Astro** or **Next.js static export** | Astro: content-focused, minimal JS. Next.js: if you might add dynamic features later. |
| Styling | **Tailwind CSS** | Fast to write, consistent, great AI agent support |
| Content | Markdown files or **MDX** | Easy to write and maintain |
| Deployment | **Vercel** or **Cloudflare Pages** | Both free, both fast |
| Key packages | `astro`, `tailwindcss`, `@astrojs/mdx` |
| Estimated cost | $0 |

**Note**: For landing pages specifically, consider using **opc-landing-page-manager** which generates self-contained HTML with inline CSS (no build step needed).

---

### Automation (`automation`)

**Workflow automation, bots, scrapers, scheduled jobs, integrations.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Language | **Python 3.11+** | Best library ecosystem for automation (HTTP, parsing, APIs) |
| Scheduling | **APScheduler** or system cron | APScheduler for in-process; cron for simple intervals |
| HTTP | **httpx** (async) or **requests** | httpx for async/modern; requests for simple scripts |
| Parsing | **BeautifulSoup4** + **lxml** (web scraping) | Standard toolkit |
| Deployment | **Railway** (always-on) or **GitHub Actions** (scheduled) | Railway for persistent bots; GH Actions for cron-style |
| Key packages | `httpx`, `apscheduler`, `beautifulsoup4`, `pydantic` |
| Estimated cost | $0-5/mo |

---

### AI Agent (`ai_agent`)

**AI-powered agents, chatbots, assistants, RAG systems.**

| Layer | Recommendation | Why |
|-------|---------------|-----|
| Language | **Python 3.11+** | Best AI/ML ecosystem, all SDKs available |
| AI SDK | **anthropic** (Claude API) | Best agent capabilities, tool use support |
| State | **Supabase** (Postgres + pgvector for RAG) or SQLite | Supabase if you need vector search; SQLite for simple state |
| Framework | **Claude Agent SDK** or direct API | Agent SDK for multi-step workflows; direct API for simple use |
| Deployment | **Railway** or **Modal** | Railway for persistent; Modal for serverless/GPU |
| Key packages | `anthropic`, `supabase`, `pydantic`, `tiktoken` |
| Estimated cost | $5-50/mo (mostly API usage) |

---

## When to Deviate

Override these defaults when:
- You have an existing codebase in a different language/framework
- Your team (even if it's one person) has deep expertise in an alternative
- A specific integration only has SDK support for a different language
- Performance requirements demand a specific runtime (e.g., Rust for CPU-intensive CLI)

## Don't Do This

These patterns are over-engineering for solo founders:

- **Don't use microservices.** One service. One repo. One deploy.
- **Don't self-host databases.** Use managed services (Supabase, PlanetScale, Neon).
- **Don't build custom auth.** Use Supabase Auth, Clerk, or Auth.js. Custom auth is a security liability.
- **Don't use GraphQL for simple CRUD.** REST is simpler, faster to build, better AI agent support.
- **Don't use Kubernetes.** If you need K8s, you need a team — it's not a solo project.
- **Don't use multi-region deployment.** Single region is fine until you have thousands of users.
- **Don't pre-optimize for scale.** Build for 100 users. If 10,000 show up, that's a good problem.
- **Don't add caching (Redis, Memcached) to V1.** Database is fast enough. Add caching when you have evidence it's needed.
- **Don't use a message queue for V1.** Direct function calls are fine. Add Celery/Bull when you need async processing at scale.

---

*Reference for opc-product-manager.*
