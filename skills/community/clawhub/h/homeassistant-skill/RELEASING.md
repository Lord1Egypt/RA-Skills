# Releasing

Use an existing authenticated GitHub and ClawHub account that owns this skill.
Release work does not require a Home Assistant token or access to a live home.

1. Fetch `origin` and confirm the release builds on its current `main`.
2. Update `metadata.version` in `SKILL.md` and add a dated changelog entry.
3. Install the optional local test dependency and run:

   ```bash
   python -m pip install -r requirements-websocket.txt
   python -m unittest discover -s tests -v
   python -m compileall -q scripts tests
   git diff --check
   ```

4. Review the exact file list for credentials, personal data and unrelated files.
   Commit the update, push `main`, and wait for the CI matrix to pass.
5. Create a GitHub release with tag `vVERSION` targeting that commit and use the
   changelog entry for its notes. Never move an existing release tag.
6. Stage a bundle containing `SKILL.md`, `skill-card.md`, `LICENSE`, `README.md`,
   `CHANGELOG.md`, `SECURITY.md`, `RELEASING.md`,
   `requirements-websocket.txt`, `references/` and `scripts/*.py`. Exclude `.git`,
   caches, environments, private reports and credentials. Tests and CI remain in
   GitHub; the installed bundle contains runtime files and their documentation.
   Current ClawHub strips the local `skill-card.md` and generates its own card.
   Compare the other published files exactly and inspect the generated card for
   correct version, license, requirements and risk disclosures.
7. Preview the exact staged bundle, then publish it:

   ```bash
   clawhub skill publish PATH --slug homeassistant-skill --name "Home Assistant Skill" \
     --version VERSION --tags latest --changelog "Release summary" \
     --source-repo https://github.com/anotb/homeassistant-skill \
     --source-commit COMMIT --source-ref vVERSION --source-path . --dry-run --json
   ```

   Remove `--dry-run` only after the preview matches the intended version and files.
   Use the same arguments for the upload. Do not publish all local skills with `sync`.
8. Inspect the exact version and latest tag, download the published bundle to a
   fresh directory, compare its file hashes with staging, and check moderation.
   Report pending or blocked scans accurately; upload success alone does not prove
   users can install the release.

If one destination fails, report which version is available where. Do not delete
or overwrite a published version to hide an incomplete release. Fix it or publish
a new version once the cause is understood.
