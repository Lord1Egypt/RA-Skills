# MR template and reviewer etiquette

Load this when writing or improving an MR or PR description, or when reviewing or answering review
comments. Copy the template into `.gitlab/merge_request_templates/Default.md` (GitLab) or
`.github/pull_request_template.md` (GitHub) to make it the project default.

## Title

- Same rules as a commit subject: `<type>(<scope>): <imperative summary> (<TICKET>)`.
- It becomes the squash commit, so it must stand alone in `git log --oneline`.
- Draft work: prefix `Draft:` on GitLab, or open as a draft PR on GitHub (`gh pr create --draft`).

```text
# BAD
PROJ-123
Fixes
Feature/AH/PROJ-123 pairing

# GOOD
feat(onboarding): add QR pairing screen (PROJ-123)
```

## Full template

~~~markdown
## Summary
<!-- One or two sentences: what changes for the user or the codebase, and why now. -->

## Ticket
<!-- PROJ-123. Add "Closes #123" if the tracker should close it on merge. -->
<!-- Stacked: "Depends on !122" (GitLab) or "Depends on #122" (GitHub). -->

## Changes
<!-- Grouped by intent, not by file. Mention what reviewers should look at first. -->
- 
- 

## Screenshots / recordings
<!-- Required for any user-visible change. Before and after. Light and dark if theming is touched. -->
| | Android | iOS |
|---|---|---|
| Before | | |
| After | | |

## Testing
<!-- What proves this works. -->
- Unit tests:
- UI / instrumentation tests:
- Manual: device, OS version, steps, result
- Not tested (and why):

## Risk and rollback
- Risk: <!-- what could break, which users, which app versions -->
- Migration: <!-- database, preferences, keychain, payload format; none if none -->
- Rollback: <!-- revert this MR | turn off flag X | server-side switch -->

## Platform and compliance notes
<!-- Delete lines that do not apply. -->
- New permissions / manifest entries:
- `Info.plist` keys / entitlements / background modes:
- `minSdk` / `targetSdk` / `compileSdk` / deployment target:
- Privacy manifest (`PrivacyInfo.xcprivacy`) / data safety form impact:
- Telemetry or analytics payload changes (personal data?):
- New third-party dependency (license, size, maintenance):

## Checklist
- [ ] Self-reviewed the full diff
- [ ] Commits follow Conventional Commits; breaking changes marked
- [ ] Build, lint and tests pass locally for Android and iOS (or the affected platform)
- [ ] New logic in domain and data layers has unit tests
- [ ] No secrets, tokens, keys or personal data in code, logs or fixtures
- [ ] Strings localized; accessibility labels added for new controls
- [ ] Screenshots for both platforms attached
- [ ] Docs, changelog or release notes updated if needed
~~~

## Filling it in well

- Summary is about behaviour, not files. "Users can pair by scanning a QR code" beats
  "Added PairingFragment.kt".
- Changes lists decisions a reviewer might question: "Kept the old pairing flow behind
  `legacy_pairing` flag until 3.3".
- Testing names real devices and OS versions. "Tested on emulator" alone is weak for BLE, camera,
  background work or push notifications.
- Risk is never "none" for a change that touches persistence, networking, BLE or auth. Say what was
  considered.
- Remove empty sections rather than leaving template comments in the final description.

## Reviewer etiquette

### When reviewing

- Respond within one working day, even if only to say when a full review will happen.
- Read the description and ticket first; review against intent.
- Review the whole change before commenting, so early comments are not invalidated by later code.
- Label every comment so the author knows what blocks:

| Label | Meaning | Blocks merge |
|---|---|---|
| `issue:` | A defect or a broken requirement | Yes |
| `suggestion:` | A better approach, with reason | Only if marked `(blocking)` |
| `question:` | Need information to judge | Until answered |
| `nit:` | Preference or polish | Never |
| `praise:` | Something done well, say why | Never |
| `todo:` | Small required follow-up | Yes |

- Propose the fix. Both GitLab and GitHub support suggestion blocks the author can apply in one click:

~~~markdown
suggestion: keep the scan timeout in one place.
```suggestion
private const val SCAN_TIMEOUT_MS = 10_000L
```
~~~

- Comment on the code, not the person: "this call can run on a binder thread", not "you forgot threading".
- Out-of-scope problems: mention once, suggest a ticket, do not block.
- Approve when remaining items are nits. Do not hold an MR hostage for preferences.

### When being reviewed

- Reply to every thread. A silent resolve looks like the comment was ignored.
- Short replies that point to the change: "Done in a1b2c3d", "Moved to `BackoffPolicy`, see fixup e4f5a6b".
- Disagree with reasons and evidence, once. If still unresolved, agree on a decision maker or a
  follow-up ticket, not a long thread.
- Push fixes as fixup commits during review so reviewers can see what changed since their last pass.
- Re-request review after a round of fixes; do not assume reviewers watch the MR.

### Resolving threads

- Blocking threads (`issue:`, `todo:`, `question:`) are resolved by the reviewer who opened them,
  after checking the fix.
- Nits and applied suggestions can be resolved by the author with a reply.
- Turn on "all threads must be resolved" (GitLab) or "require conversation resolution" (GitHub branch
  protection) so the rule is enforced, not remembered.
