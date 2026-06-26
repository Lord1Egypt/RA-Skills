# Security

IFQ Design Skills is designed as a low-risk, local-first skill bundle.

## Runtime Boundaries

- Filesystem: read/write only inside the active workspace.
- Shell: bundled Node scripts only: `npm run validate`, `npm run evals:validate`,
  `npm run verify:lite`, `npm run preview`, `npm run anti-slop`, and `npm run pack`.
- Browser/network: optional outbound HTTPS reads for facts, fonts, and legal
  image assets. No inbound server is required.
- Secrets: no required environment variables, no credential storage, no hidden
  background processes.
- OpenClaw metadata: `metadata.openclaw.requires.bins` declares only `node`,
  required env/config gates are empty, and plugins are limited to filesystem +
  shell with optional browser/memory.
- ClawHub package posture: zero dependencies, no install hooks, no binary
  assets, no dynamic execution, no script-side outbound network primitives, and
  no private asset indexes in the published archive.

## Automated Security Gates

The skill ships with automated preflight checks that run before every publish:

- **Script safety deny-list** (`scripts/script-safety-rules.json`): 18 rules across
  3 groups — runtime-primitives (eval, Function, child_process, dynamic import,
  destructive fs), script-connectivity (http/https/net/tls/dns, axios, node-fetch,
  undici, fetch, WebSocket), and secret-hygiene (5 token/key patterns).
- **Secret leakage scan**: all text files scanned for API keys, PATs, cloud
  credentials, and private key blocks.
- **Package safety**: zero dependencies, zero npm lifecycle hooks, only allowed
  script names.
- **ClawHub cleanliness**: clawhub.ignore.txt excludes VCS metadata, agent state,
  .env files, personal assets, and build artifacts.
- **Font loading protocol**: Google Fonts must use Tier B non-blocking pattern
  (media="print" + onload swap) for CN/offline friendliness.
- **Template runtime isolation**: no remote JS/CSS runtimes in forkable templates;
  no floating @latest references.

Run `npm run validate` to execute all 19 automated checks in one pass.

## Operator Hardening

- Run `npm run validate` and `npm run pack` before publishing a bundle.
- When using OpenClaw on real messaging channels, run `openclaw security audit`
  after gateway/config changes and keep tools scoped to the smallest useful
  permission set.
- Treat third-party skills and external web content as untrusted input. Read
  skills before enabling them, prefer sandboxed agents for risky workflows, and
  keep secrets out of prompts, logs, generated HTML, and repository files.
- After downloading a ClawHub skill, inspect its SKILL.md, scripts, and
  package.json before enabling it. OpenClaw's built-in scanner checks for
  dangerous code patterns, but manual review is the strongest gate.

## Reporting

Please report suspected vulnerabilities by opening a private security advisory
on GitHub if available, or by contacting the maintainer listed in the repository
profile. Do not publish exploit details before maintainers have had a chance to
investigate.

## Scope

In scope: unsafe package scripts, secret leakage, unexpected network behavior,
path traversal, unsafe archive contents, or misleading permission metadata.

Out of scope: generated user content, third-party websites used as optional
reference sources, and export helpers that live outside the ClawHub-safe bundle.
