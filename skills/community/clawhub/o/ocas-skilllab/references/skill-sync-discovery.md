# Skill-sync discovery pattern (references)

Reusable building blocks for the unified `skill-sync-all.sh`
<<<<<<< Updated upstream
(at `<hermes-home>/profiles/indigo/scripts/skill-sync-all.sh`). Embedded here so
=======
(at `$HERMES_HOME/../indigo/scripts/skill-sync-all.sh`). Embedded here so
>>>>>>> Stashed changes
the pattern survives even if the script is moved or rewritten.

## 1. Discovered-skills helper (no hard-coded lists)
Finds every `SKILL.md` for a prefix across BOTH `indigo` and `koda` profiles,
any depth, while EXCLUDING nested skills and data/plugin dirs.

```bash
discovered_skills() {
  local pat="$1"
  find "$INDIGO" "$KODA" -name SKILL.md -path "$pat" -not -path '*/.git/*' -not -path '*/.archive/*' 2>/dev/null \
    | while read -r f; do
        local d; d="$(dirname "$f")"
        local p="$d"; local bad=0
        while [ "$p" != "$INDIGO" ] && [ "$p" != "$KODA" ] && [ "$p" != "$(dirname "$INDIGO")" ]; do
          if [ -f "$p/SKILL.md" ] && [ "$p" != "$d" ]; then bad=1; break; fi
          p="$(dirname "$p")"
        done
        echo "$d" | grep -qE '/(commons|\.claude|node_modules)/' && bad=1
        [ "$bad" = "0" ] && echo "$f"
      done | sort -u
}
```
Call as `discovered_skills '*/ocas-*'` etc. The ancestor-SKILL.md check prevents a
`SKILL.md` nested inside another skill's repo from being treated as a separate
skill; the `commons/.claude/node_modules` exclude drops data/plugin nests.

## 2. Reconcile a local skill with an existing remote (SAFE)
Do NOT `git checkout -B main origin/main` — a remote that is itself a meta-repo
will pull nested sibling skills into the working tree and pollute the commit
(the 2026-07-15 `ocas-10xeng` incident: merged a legacy meta-repo's siblings →
committed `ocas-10xeng/ocas-10xeng-review/…` → pushed → required `force-with-lease` cleanup).

```bash
git -C "$d" remote add origin "git@github.com:<agent-handle>/$rmt_name.git" 2>/dev/null
git -C "$d" fetch origin 2>/dev/null
git -C "$d" add -A; git -C "$d" commit -q -m "chore: initial commit of $base" 2>/dev/null || true
git -C "$d" pull --rebase origin main 2>/dev/null || true   # layer local on remote; no overwrite
git -C "$d" push -u origin "$(git -C "$d" rev-parse --abbrev-ref HEAD)"
```
Before pushing, sanity-check the remote has no nested SKILL.md:
`git ls-tree -r --name-only origin/main | grep -cE '(^|/)SKILL.md'` should be 1.
If pollution was already pushed: remove the subdirs, commit, then
`git push --force-with-lease` (safe — only overwrites if remote unchanged since fetch).

## 3. Prefix-strip new repo names with dual-existence check
(User directive: "Prefixes can always be stripped on GitHub".)
```bash
local repo="${base#ocas-}"          # strip prefix for the NEW repo name
local rmt_exists="n" rmt_name="$repo"
if   gh repo view "<agent-handle>/$repo" >/dev/null 2>&1; then rmt_exists="y"; rmt_name="$repo"
elif gh repo view "<agent-handle>/$base" >/dev/null 2>&1; then rmt_exists="y"; rmt_name="$base"; fi
# only `gh repo create <agent-handle>/$repo` when rmt_exists=n
```
Checking BOTH the stripped and legacy prefixed name prevents creating a second
repo when migrating prefixed→stripped naming.