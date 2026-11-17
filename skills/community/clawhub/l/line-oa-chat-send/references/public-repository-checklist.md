# Making the repository public

Follow this in order. Publication is irreversible in practice: anything reachable
in Git history stays reachable once it has been fetched, and removing it later
does not un-publish it.

## 1. Audit all reachable history, not just the current files

Old commits and merged pull requests remain visible after publication. Scan the
full history, not the working tree.

Look for:

- credentials, tokens, and authentication headers
- tunnel or share URLs (they are bearer secrets)
- browser-profile data, cookies, or session artefacts
- host-specific runtime paths that reveal infrastructure

When reporting findings, report **commit IDs and pattern categories only** —
never the matched values. A report that quotes the secret has republished it.

Remove or rewrite genuinely sensitive history before publication. Rewriting
history after the fact is far more disruptive than doing it now.

## 2. Apply public-facing settings before changing visibility

- Remove collaboration surfaces that are not in use.
- Enable automatic deletion of merged branches.
- Disable Actions that have not been reviewed for a public context. A workflow
  that was safe in a private repository can leak in a public one, and public
  forks change who can trigger what.

## 3. Change visibility

## 4. Verify from outside

Fetch the repository and its README through an **unauthenticated** request. A
browser already signed in proves nothing.

## 5. Enable public-repository security controls

- secret scanning
- push protection
- Dependabot

GitHub may enable some of these automatically and may reject others depending on
plan and org policy, so **read the resulting state back** rather than assuming
the request applied.

## 6. Licensing is a separate decision

Treat it as a legal question, not a checklist item. Do not choose a licence
without the user's direction.

## Notes specific to this repository

- The ClawHub workflow publishes on tag push and needs its token secret to exist
  in the repository's Actions secrets. Confirm the secret's scope before the
  repository becomes public.
- `scripts/` contains no credentials by design: the browser profile lives outside
  the repository, and the runtime directory is created at run time. Confirm that
  no run has written a profile, a runtime directory, or a timing log inside the
  working tree.
- Phase-timing logs contain durations only, but they live in the private runtime
  directory and should never be committed regardless.
