# Dashboard Builder

**The meta-skill.** This is the one that ties everything together.

Dashboard Builder lets your AI agent create a unified, dark-mode personal dashboard where all your NormieClaw skills live under one roof. Instead of 21 separate tools, you get one beautiful app — sidebar navigation, skill pages, home overview with widgets, and a real database behind it all.

Think of it as your personal OS, built by your agent, deployed in minutes.

## What You Get

- **Sidebar-based personal OS** — Every installed skill = a page in the sidebar
- **Home overview** — Widgets from all your skills in a single glance
- **Dark mode** — Teal-and-orange design system. Looks gorgeous.
- **Real database** — Supabase (Postgres) with proper auth, RLS, and schema
- **Plugin architecture** — Add or remove skills without touching the core
- **One-click deploy** — Vercel or Docker, your choice

## How It Works

1. Your agent reads the `SKILL.md` (the brain)
2. It scaffolds a Next.js project with all templates
3. It reads manifest files from your installed skills
4. It generates pages, widgets, and database migrations
5. It deploys to Vercel (or Docker for self-hosting)

You go from zero to deployed dashboard in a single conversation.

## Compatible Skills

Dashboard Builder works with all 21 NormieClaw skills:

| Category | Skills |
|----------|--------|
| **Finance** | Expense Report Pro, Budget Buddy Pro, Stock Watcher Pro, InvoiceGen |
| **Productivity** | Supercharged Memory, NoteTaker Pro, DocuScan, Security Team, Daily Briefing |
| **Work** | Content Creator Pro, Email Assistant, HireMe Pro |
| **Health** | Health Buddy Pro, Trainer Buddy Pro |
| **Learning** | Knowledge Vault, Tutor Buddy Pro |
| **Lifestyle** | Meal Planner Pro, Travel Planner Pro, Relationship Buddy, Plant Doctor, Home Fix-It |

Start with one skill. Add more whenever you want. The dashboard grows with you.

## Quick Start

Tell your agent:

> "Build my NormieClaw dashboard with Expense Report Pro and Budget Buddy Pro"

That's it. Your agent handles the rest.

## Requirements

- Node.js 18+
- A Supabase account (free tier works)
- A Vercel account (for cloud deploy) or Docker (for self-hosting)

## What's Inside

```
dashboard-builder/
├── SKILL.md # The brain — exhaustive agent instructions
├── SETUP-PROMPT.md # First-run setup guide
├── SECURITY.md # Security requirements and practices
├── README.md # This file
├── config/
│ └── dashboard-config.json # Default theme and settings
├── templates/ # Production-ready starter code
│ ├── layout.tsx
│ ├── sidebar.tsx
│ ├── home-overview.tsx
│ ├── page-template.tsx
│ ├── stat-card.tsx
│ ├── data-table.tsx
│ ├── chart-wrapper.tsx
│ ├── supabase-client.ts
│ ├── supabase-server.ts
│ ├── middleware.ts
│ └── globals.css
├── scripts/
│ ├── scaffold-project.sh # One-shot project creation
│ ├── run-migrations.sh # DB migration generator
│ └── add-skill.sh # Add a skill to existing dashboard
├── examples/
│ ├── single-skill-setup.md
│ ├── multi-skill-setup.md
│ └── full-ecosystem.md
└── dashboard-kit/
 └── ARCHITECTURE-SPEC.md # Complete technical specification
```

## License

Part of the NormieClaw ecosystem. Visit [normieclaw.ai](https://normieclaw.ai) for more.
