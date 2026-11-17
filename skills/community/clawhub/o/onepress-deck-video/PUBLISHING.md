# Publishing to ClawHub

Publish under the **`getonepress` org** — the local CLI is logged in as the
personal account `guiyanzhong`, and `clawhub publish` without `--owner`
silently publishes to the personal namespace (duplicate listing, wrong owner).

```bash
clawhub publish . --owner getonepress --version X.Y.Z
```

Checklist:

1. Bump `version:` in `SKILL.md` frontmatter and add a `CHANGELOG.md` entry.
2. Commit and push to `github.com/getonepress/onepress-deck-video` first — the
   published version should match the repo.
3. Run the publish command above. New versions stay **pending security scans**
   before going public — the public page keeps showing the last approved
   version until the scan clears (can take days; check the publisher dashboard
   if it stalls).
4. Verify afterwards: `clawhub search onepress-deck-video` should show only
   `@getonepress`. If a `@guiyanzhong` duplicate appears, hide it:
   `clawhub hide guiyanzhong/onepress-deck-video --reason "duplicate of @getonepress" --yes`.
