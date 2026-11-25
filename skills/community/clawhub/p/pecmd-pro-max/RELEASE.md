# Release Checklist

1. Update the version in `SKILL.md`, both README badges, `CHANGELOG.md`, and the `修复版本` line in `AUDIT.md`.
2. Run `python -I tools/verify_skill.py`. It enforces link/fence integrity, line counts, manifest hashes, exactly 136 audit IDs, and exactly 26 P0 rows.
3. Commit the release changes and push `main`.
4. Create an annotated tag: `git tag -a v<version> -m "PECMD Pro Max <version>"`.
5. Push the tag: `git push origin v<version>`.
6. The `Publish to ClawHub` workflow runs the verifier, checks that the tag equals the `SKILL.md` version, then publishes to ClawHub. Do not publish from a tag whose frontmatter differs.
7. Confirm the workflow result with `gh run list --workflow publish-to-clawhub.yml`.

Notes:

- Tags must be newer than every existing tag. Check with `git tag --sort=-version:refname | head`.
- The release workflow is the only supported publish path; do not run `clawhub publish` manually from a dirty working tree.
