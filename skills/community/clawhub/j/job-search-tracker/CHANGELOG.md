# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] — 2026-06-08

### Changed
- Rewrote **Data Handling and Privacy** section in SKILL.md to accurately describe assistant-mediated use of Gmail, LinkedIn, browser, and web-search tools, rather than understating tool usage. The skill instructs the assistant to invoke those tools when connected; this version is explicit about scope, consent rules, and what stays local
- Narrowed the activation triggers in the `description` frontmatter to require explicit job-search context (e.g., a named company in a hiring context) and reduce over-activation on generic email, calendar, or follow-up phrases

### Added
- **Permissions and Privacy** section in README.md so users see the scope of access (Gmail, LinkedIn, browser, web search, local files) before installing, along with a "tracker-only mode" path for users who'd rather not connect Gmail or LinkedIn

## [1.1.1] — 2026-06-08

### Added
- **Data Handling and Privacy** section (later rewritten in 1.1.2 to remove an intent-code divergence that misrepresented tool usage)

## [1.1.0] — 2026-05-12

### Added
- **Resume Recommender**: reads resume variants from a `resumes/` directory and matches each variant's self-description against new job postings to suggest the best fit
- **Tone Check** pass on user-drafted emails and cover letters with flag categories for desperate signals, templated signals, negative framing, and length issues; produces targeted phrase-level revision suggestions rather than full rewrites
- **Salary Negotiation** flow triggered on "got an offer" with offer triage, counter-offer analysis (gap to target, which components have room), counter-offer drafting, and pressure-tactic flagging (exploding offers, verbal-only, below-range, total-comp framing)
- Three new Common Workflows: "I got an offer," "Which resume should I send?," and "Does this sound desperate?"

### Changed
- Frontmatter now includes `version` and `metadata.openclaw.emoji` fields
- Trigger description expanded to cover offer, negotiation, resume, and tone-check phrases

### Removed
- License section removed from README (license now managed at the ClawHub platform level)

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Application tracking in a single `applications.md` markdown file
- Stale-application detection with configurable thresholds (no response in 7+ days, overdue follow-ups, interviews in 48 hours)
- Dashboard view with pipeline summary, recent activity, and items needing attention
- Drafting help for cover letters, follow-up emails, and thank-you notes using tracker context
- Interview prep: company research briefs, role-specific prep, and mock questions
- Optional Gmail integration for auto-detecting application confirmations and pulling email context
- Optional LinkedIn integration for tracking Easy Apply submissions and company research
- Common Workflows for the most frequent job-search interactions
