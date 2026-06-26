# Skill Ecosystem Quality Notes · 2026-04-27

This note records what was learned by opening the current skill directories with MCP Chrome. It is research input only: **ClawHub remains the recommended install channel for IFQ Design Skills**.

## Sources Checked

- `https://clawhub.ai/skills?sort=downloads&dir=desc&nonSuspicious=true`
- External all-time skill index and audit surface
- External OpenClaw skill index
- Detail pages for ClawHub `self-improving-agent`, `multi-search-engine`, `agent-browser`, and the external `frontend-design` skill

## Top-Skill Signals

ClawHub by downloads, with suspicious entries hidden: self-improvement/memory, typed ontology, multi-search, ad/app analytics, browser automation, phone automation, image generation, notes/PKM, API gateway, and document automation skills dominate the first page. The useful pattern for IFQ is not their domains; it is their tight use-case wording, visible install path, and explicit authority boundary.

External all-time / audit surface: the highest-signal design-adjacent entries are `frontend-design`, `web-design-guidelines`, `remotion-best-practices`, `vercel-react-best-practices`, `vercel-composition-patterns`, `shadcn`, and `ui-ux-pro-max`. Strong infrastructure entries group many related skills under one source, which reinforces the value of a small core plus optional full-repo helpers.

External OpenClaw downloads: browser automation, workspace/API gateways, local app automation, search, document conversion, workflow automation, and long-term memory are the repeat winners. Their common shape: one clear capability, exact setup text, and no surprise permissions.

## Extracted Rules

1. Use a pushy, specific description. The top design skill says when to use it and explicitly rejects generic AI aesthetics.
2. Show install paths as exact commands, but keep environment changes scoped and ask before broader setup.
3. Keep the core loop zero-install. Dependencies, browser automation, export helpers, and account auth must be opt-in.
4. Publish with visible security posture: no install hooks, no dependency tree in the safe bundle, no secrets, no script-side outbound network, no runtime code generation.
5. State data boundaries. Search and browser skills explain cookies, session state, rate limits, and what is never written to disk.
6. Prefer deterministic workflows: snapshots, refs, exact routing, template-first output, and after-change verification.
7. Make quality checks executable. Static gates should fail before ClawHub / VirusTotal has to find the same issue.
8. Keep the skill narrow. Top skills are remembered for one capability, then document extensions and integrations separately.
9. Avoid raw research notes that look like requested authorities. Published bundles should describe lessons learned without naming sensitive third-party domains that can be misread as IFQ capabilities.

## IFQ Application

- IFQ keeps the ClawHub-safe bundle as a template/reference asset with bundled validation, preview, and pack scripts.
- Browser is optional. If unavailable, IFQ falls back to local fonts and HTML-only output.
- Export, Playwright, ffmpeg, PDF, and PPTX helpers stay in the full GitHub repo rather than the ClawHub-safe bundle.
- Anti-AI-slop is a hard pre-flight rule, not a style suggestion.
- Safety rules are data-driven in `scripts/script-safety-rules.json`; `scripts/smoke-test.mjs` stays a plain offline validator so ClawHub static analysis does not confuse self-checks with runtime behavior.
- Every release should pass `npm run validate` and `npm run pack`, then inspect the generated archive before upload.

## 2026-04-29 Live ClawHub / OpenClaw Check

Recent ClawHub pages make the install path and scanner result part of the product surface, not a hidden maintainer concern. The listing exposes an OpenClaw prompt flow, direct CLI commands, VirusTotal/OpenClaw scan summaries, download counts, versions, files, and the rendered `SKILL.md`/README content.

Implications for IFQ:

- Treat first-run onboarding as a product feature: a user should know the exact first prompt and expected evidence before installing.
- Keep scanner categories easy to read from metadata: purpose, instruction scope, install mechanism, credentials, and persistence/privilege.
- Publish inspectable demos in the manifest so reviewers can verify that routes lead to real artifacts, not just broad claims.
- Keep `SKILL.md` short and progressive; detailed workflow belongs in `references/` so OpenClaw loading remains cheap.
- Preserve exact OpenClaw install commands and local validation commands in both docs and `clawhub.json`.
