# pipaclaw-skills-hub

This directory is the public repository boundary for `pipaclaw-skills-hub`.

It should contain only publishable skill packages:

- `SKILL.md`
- `agents/`
- `references/`
- optional lightweight public helper scripts such as `scripts/*.sh`
- skill subdirectories such as `ppt-maker/`

It should not contain implementation-specific material:

- backend services
- backend implementations or thick local runtimes
- test scripts
- sample customer files
- private assets or reverse-engineered templates
- `node_modules`, build output, or generated artifacts

Current public skills:

- `social-account-ops`
- `ppt-maker`
- `promo-video-maker`

Repository layout:

```text
pipaclaw-skills-hub/
├── AGENTS.md
├── LICENSE
├── README.md
├── SKILL.md
├── .gitignore
├── agents/
├── references/
├── social-account-ops/
├── ppt-maker/
└── promo-video-maker/
    ├── references/
    └── scripts/
```

Repository rule:

- social account operations are exposed through exactly one public skill: `social-account-ops`
- diagnosis, planning, writing, and retro are internal phases inside that one skill, not separate public packages

Recommended publish flow:

1. Treat this `skills/` directory as the GitHub repo root.
2. Keep execution backends in separate private or implementation repos.
3. Review each skill package for customer data, generated assets, and any helper script that has grown beyond public-safe transport logic.
4. Follow [PUBLISHING.md](/Users/xiexiongjie/code/skills-hub/skills/PUBLISHING.md) for login, version bumps, proxy handling, and ClawHub publish commands.
5. Use [bin/clawhub-release](/Users/xiexiongjie/code/skills-hub/skills/bin/clawhub-release) as the standard release entrypoint.
