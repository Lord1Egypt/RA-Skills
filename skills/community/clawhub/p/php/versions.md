# Versions and Upgrades

## Support Policy

- Each `8.x` release gets roughly two years of active bug-fix support, then one more year of security-only fixes — about three years of life from release, with end dates aligned to the end of a calendar year. Releases land in November.
- Running an unsupported version is not a style problem: no security patches reach it, and the extension ecosystem stops building for it within a year.
- Verify the current status before making a plan; the release calendar is on php.net's supported-versions page (checked 2026-07: the 8.1 line is past end of life, 8.2 is in its security-only year, 8.3 and later are supported).
- Distribution packages lag: Debian/Ubuntu ship whatever was current at freeze. `php -v` on the SERVER is the number that matters, not the one on the laptop (`php-ini.md`).

## The Upgrade Procedure

Order matters — the point is to make the OLD version tell you what the new one will reject.

1. **Surface deprecations on the version you are on.** Set `error_reporting = E_ALL` and run the full test suite plus a representative traffic replay. In PHPUnit, `failOnDeprecation="true"` in `phpunit.xml` turns them into failures instead of scrollback (`testing.md`).
2. **Raise the analyzer's target.** `phpstan.neon` with `phpVersion: 80300` reports incompatibilities statically, across paths no test covers. Do this before touching a server (`static-analysis.md`).
3. **Let Rector do the mechanical part.** `rector process --set=php83` handles implicit-nullable parameters, deprecated string interpolation, and dozens of similar rewrites. Review the diff; Rector is a refactoring tool, not an oracle.
4. **Check the dependency floor.** `composer why-not php 8.3` names every package blocking the move. Update those first, on the old PHP, as separate merges (`composer.md`).
5. **Check extensions and INI.** Removed extensions and renamed ini directives break at startup, not at runtime — `php -m` and `php --ini` on a staging box with the new version.
6. **Run both in CI.** A matrix over old and new for one release cycle catches the code path your migration missed.
7. **Deploy to one node.** Compare error rates and p95 for a full traffic cycle before the rest.

## Where Upgrades Actually Break

| Class of break | Detected by | Example |
|---|---|---|
| Deprecations becoming errors | Old version with `E_ALL` | Implicit nullable parameters (`php >=8.4`) |
| Warnings becoming `Error`s | Test suite | Method call on null (`php >=8.0`) |
| Changed semantics, no diagnostic | Traffic replay, characterization tests | `0 == "foo"` flipping to `false` (`php >=8.0`) |
| Changed output format | Byte-comparison tests | `htmlspecialchars` escaping `'` by default (`php >=8.1`) |
| Removed extension or ini directive | `php -m`, `php --ini` on staging | Extensions dropped in the 8.x line |
| Dependency ceiling | `composer why-not` | A package with `"php": "<8.2"` |

The dangerous row is the third: no error appears anywhere, and a validation branch quietly changes meaning. Characterization tests around comparison-heavy code are the only defense.

## Choosing a Floor for New Code

- Library: support the oldest version with security support, and declare it honestly in `composer.json` (`"php": ">=8.2"`). A narrower floor shrinks your install base for features you can polyfill.
- Application: track the newest version your hosting supports. There is no user-visible cost and you get the performance work each release ships.
- The floor is a config value here, not a hardcoded assumption: `min_php` in `config.yaml` gates which Version Floors features may be emitted unguarded (SKILL.md Configuration).
- Polyfills (`symfony/polyfill-php83`) let you use new FUNCTIONS on an older runtime; they cannot backport SYNTAX. `str_contains` polyfills; enums and `readonly` do not.

## Running Several Versions Locally

- `php83 -v`, `php84 -v` from Homebrew or `ondrej/php`; switch per project rather than globally.
- The CLI binary and the FPM pool are separate installs with separate ini sets — a project that passes on the CLI can still fail in the browser (`php-ini.md`).
- Composer resolves against the PHP running Composer, not the deployment target. Pin it: `"config": {"platform": {"php": "8.2.0"}}` (`composer.md`).
- In containers, the image tag IS the version pin; `php:8.3-fpm-alpine` and `php:8.3-fpm` differ in libc and in which extensions build cleanly.

## Extensions Worth Verifying After Every Move

`ext-mbstring` (all text handling), `ext-intl` (locale formatting and collation), `ext-pcntl` (signals in workers, POSIX only), `ext-opcache` (silently absent means every request recompiles), `ext-pdo_*` for your driver, and the JIT-related opcache options. `php -m` on the deployed image, in the deploy pipeline, not by hand.

## Related

- The features each floor unlocks: `modern.md`
- Analyzer configuration and Rector sets: `static-analysis.md`
- Dependency constraints and platform pinning: `composer.md`
