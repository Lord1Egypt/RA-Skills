# Skill Library Sync Audit Procedure

When asked to audit sync state of all OCAS skills, or when running a scheduled sync check, use this workflow:

Trigger phrases: "sync all ocas skills", "audit skill repos", "are all skills pushed?", "skill library sync status".

This is NOT a separate command — it's the pattern `forge.audit` + `forge.sync` applied library-wide.

## Procedure

1. List all local ocas-* skills: `ls ~/.hermes/skills/ocas-*/`
2. List all remote repos: `gh repo list <agent-handle> --json name`
3. For each local skill:
   a. Check if `.git` exists → if not, needs repo creation
   b. Check dirty state: `git status --porcelain`
   c. Check ahead/behind: `git log origin/main..HEAD / git log HEAD..origin/main`
4. Fix dirty trees: `git add -A`, `git commit`, `git push`
5. Create missing repos: `gh repo create --source=. --push`
   (default private; only public if user explicitly asks)
6. Report: clean count, fixed count, newly created count

## Naming Convention

- All OCAS skill repos use the `ocas-` prefix
- If a duplicate exists without the prefix, keep `ocas-vpn`, delete the other
- Normalize `master` → `main` on push

See `references/builder_workflows.md` for the detailed compliance audit workflow and `references/github_repo_guardrails.md` for repo creation guardrails.