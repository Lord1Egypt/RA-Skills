# Changelog

## 0.2.0 (2026-03-11)

### Added
- `SKILL.md` for `scan_skill` and `review_skill` (ClawHub compatible)
- `malicious_patterns.json` with 4 detection categories:
  - `dangerous_keywords` (22 patterns)
  - `sensitive_files` (4 paths)
  - `suspicious_urls` (2 URLs)
  - `suspicious_patterns` (4 regex rules)
- `tsconfig.json` (ESNext + NodeNext)
- Test fixtures and verification script (`test/verify.ts`)
- `.gitignore` and `README.md`

### Changed
- Replaced deprecated `vm2` with Node built-in `node:vm` module
- Enhanced `keyword_scanner.ts` to support all 4 pattern categories
- Fixed `ast_scanner.ts` ESM compatibility with `@babel/traverse`
- Improved `callee.name` access with proper type narrowing

### Security
- Removed `vm2` dependency (CVE-2023-37466 and other sandbox escape vulnerabilities)

## 0.1.0

### Added
- Initial implementation
- AST scanner with Babel
- Keyword scanner
- VM sandbox runner (vm2)
- Runtime guard
- AI review via LLM
- Signature verification
