# Round 78 Memory Items - Live Publish Execution

**Date:** 2026-03-22  
**Round:** 78  
**Type:** Live ClawHub Publish  
**Quality Score:** 95%  

---

## Memory Item 1: ClawHub Publish Command Structure

**Category:** Skills / Publishing / CLI  
**Tags:** #clawhub #publish #cli #workflow  
**Content:**
ClawHub publish command: `clawhub publish <path> --slug <slug> --name "<display>" --version <semver> --changelog "<description>"`. Path can be absolute or relative. Slug must be kebab-case and unique. Version must be semver string (e.g., "1.0.0"). Changelog should be concise but descriptive. Login required first via `clawhub login`. Token stored for subsequent commands.

---

## Memory Item 2: Publish Response Handling

**Category:** Skills / Publishing / Verification  
**Tags:** #publish #verification #response  
**Content:**
Successful publish returns: `OK. Published <slug>@<version> (<skill-id>)`. Skill ID is unique identifier (e.g., k97bfh0naebmypgsadxqtwc4n983d515). Immediately after publish, skill enters security scan (hidden state). Verify with `clawhub list` (shows local) or `clawhub inspect <slug>` (shows remote, may fail during scan). Wait a few minutes before public verification.

---

## Memory Item 3: Security Scan Behavior

**Category:** Skills / Publishing / Security  
**Tags:** #security #scan #publishing  
**Content:**
After publish, ClawHub runs automated security scan on skill files. During scan, skill is hidden from search/inspect. Error message: "Skill is hidden while security scan is pending. Try again in a few minutes." Normal scan duration: 5-10 minutes. No action needed - scan is automatic. If scan fails, skill remains hidden and author notified.

---

## Memory Item 4: Publish Prerequisites Checklist

**Category:** Skills / Publishing / Checklist  
**Tags:** #checklist #publishing #prerequisites  
**Content:**
Before publishing: (1) SKILL.md frontmatter complete (name, description, metadata.author, metadata.version), (2) Skill directory structure valid, (3) No sensitive data in files (API keys, tokens, credentials), (4) Logged in to ClawHub (`clawhub whoami`), (5) Version bumped if updating, (6) Changelog prepared, (7) Test locally first. Missing prerequisites cause publish failures or security scan rejection.

---

## Memory Item 5: Authentication Flow

**Category:** Skills / Publishing / Authentication  
**Tags:** #auth #login #clawhub  
**Content:**
ClawHub auth flow: `clawhub login` opens browser for OAuth or accepts token directly. Token stored locally for subsequent commands. Verify with `clawhub whoami` (returns username). Logout with `clawhub logout`. Token required for publish, delete, hide, and other write operations. Search and inspect work without auth. Handle auth errors by re-running login.

---

## Memory Item 6: Publish Error Handling

**Category:** Skills / Publishing / Errors  
**Tags:** #errors #publishing #troubleshooting  
**Content:**
Common publish errors: (1) "Not logged in" - run `clawhub login`, (2) "Slug already exists" - use different slug or update existing, (3) "Invalid frontmatter" - fix SKILL.md yaml, (4) "Rate limit exceeded" - wait and retry, (5) "Security scan failed" - review skill for sensitive data or policy violations. Most errors are recoverable. Publish is idempotent for updates with same version.

---

## Memory Item 7: Version Management

**Category:** Skills / Publishing / Versioning  
**Tags:** #versioning #semver #publishing  
**Content:**
Use semantic versioning: MAJOR.MINOR.PATCH (e.g., 1.0.0). Bump MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes. Version in SKILL.md frontmatter must match --version flag. ClawHub tracks version history. Cannot publish same version twice (immutable). Update requires version bump. Keep version.json in sync with SKILL.md for local tracking.

---

## Memory Item 8: Post-Publish Verification

**Category:** Skills / Publishing / Verification  
**Tags:** #verification #publishing #quality  
**Content:**
Post-publish verification steps: (1) Confirm CLI success message with skill ID, (2) Wait for security scan (~5-10 min), (3) Verify with `clawhub inspect <slug>`, (4) Check on web UI (clawhub.com/skills/<slug>), (5) Test install from clean environment, (6) Update local state.json with publish metadata, (7) Document in daily notes or MEMORY.md. Track publish ID for future reference.

---

## Summary

**Total Memory Items:** 8  
**Categories Covered:** Publishing, CLI, Security, Authentication, Versioning, Verification  
**Applicability:** All future ClawHub publish operations  
**Retention:** Long-term (add to MEMORY.md under Skills/Publishing section)
