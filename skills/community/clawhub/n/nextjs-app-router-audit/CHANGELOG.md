# Changelog

## Unreleased
- Add `legacy-next-head` rule (ERROR): `next/head` is a no-op in the App Router.
- Add `legacy-next-image` rule (WARN): flag `next/legacy/image` usage.

## 0.1.0
- Initial scanner with 11 rules across RSC boundaries, waterfalls, Core Web
  Vitals and SEO.
- `--json` output and CI-friendly non-zero exit on errors.
- GitHub Actions workflow self-testing the scanner against a fixture app.
