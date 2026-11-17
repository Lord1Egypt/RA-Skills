# Composer — Dependencies and Autoloading

## install vs update

- `composer install` reads `composer.lock` and reproduces exactly those versions. `composer update` re-resolves `composer.json` and rewrites the lock.
- Applications commit `composer.lock`; libraries do not (a library's lock is never read by its consumers, and committing it makes contributors chase a phantom).
- CI and production run `composer install --no-dev --optimize-autoloader`, never `update`. A deploy that resolves dependencies is a deploy that can ship a version nobody tested.
- Bump one package: `composer update vendor/pkg --with-dependencies`. Bare `composer update` in a PR mixes an intentional change with fifty unrelated ones and makes the diff unreviewable.
- `composer install` warning that the lock is out of date means someone edited `composer.json` by hand: `composer update --lock` regenerates the hash without changing versions.

## Version Constraints

| Constraint | Allows | Use |
|---|---|---|
| `^1.2.3` | `>=1.2.3 <2.0.0` | The default for semver packages |
| `^0.3.1` | `>=0.3.1 <0.4.0` | Caret treats the first non-zero segment as major below 1.0 |
| `~1.2.3` | `>=1.2.3 <1.3.0` | Patch-only, for packages you do not trust to respect semver |
| `~1.2` | `>=1.2 <2.0.0` | Equivalent to `^1.2` — the two-segment form surprises people |
| `1.2.*` | `>=1.2 <1.3` | Same as `~1.2.3` in practice |
| `>=1.0 <1.5 \|\| ^2.0` | Explicit range plus an alternative | Supporting two majors in a library |
| `dev-main` | A branch | Never in a release; add `"minimum-stability"` consciously |

- `composer why vendor/pkg` shows who requires it; `composer why-not vendor/pkg 2.0` explains exactly what blocks an upgrade. These two commands answer most "it will not update" questions.
- `composer outdated --direct` lists only what you declared, which is the actionable list; the full output includes transitive noise.
- `"config": {"platform": {"php": "8.2.0"}}` makes resolution target the SERVER's PHP, not the developer's. Without it, a laptop on 8.4 resolves packages the 8.2 production box cannot run.

## Autoloading

- PSR-4 maps a namespace prefix to a directory: `"App\\": "src/"` means `App\Billing\Invoice` lives at `src/Billing/Invoice.php`. The class name must match the file name exactly, INCLUDING case — code that works on macOS fails on Linux (`debugging.md`).
- `composer dump-autoload` is required after adding a namespace mapping, after adding a `classmap` path, and in production where the classmap is authoritative. In plain PSR-4 development, a new file needs no dump.
- Production: `--optimize-autoloader` (`-o`) builds a classmap so lookups skip filesystem probing; `--classmap-authoritative` (`-a`) additionally declares that anything not in the map does not exist — faster still, and fatal if you generate classes at runtime.
- The `files` autoload entry is `require`d on EVERY request before anything else. One helpers file is fine; a dozen is measurable startup cost (`performance.md`).
- `autoload-dev` keeps test namespaces out of the production classmap. A `Tests\` prefix under `autoload` is how test fixtures end up shipped.
- "Class not found" checklist, in order: namespace declaration matches the directory · file name matches the class name and case · the prefix is in `composer.json` · `composer dump-autoload` has run · the file is not excluded by a `.gitignore` that also excluded it from the deploy artifact.

## Scripts and Plugins

- `composer install` runs the package's scripts and plugin code with your user's privileges. `--no-scripts` and `--no-plugins` when installing anything you have not vetted.
- Composer 2.2+ requires plugins to be listed under `config.allow-plugins`; the prompt exists because a plugin is arbitrary code at install time. Answer it deliberately, not with a blanket `true`.
- `composer audit` reports known advisories against the installed lock. Run it in CI on every build, not only when someone remembers.
- `post-install-cmd` / `post-update-cmd` are the right hook for cache warming; nothing there may require network access, or an offline deploy breaks.

## Private and Mirrored Repositories

- Private Packagist or a `vcs` repository entry with an SSH URL; credentials through `COMPOSER_AUTH` or `auth.json` outside the repository, never in `composer.json`.
- A `path` repository with `"options": {"symlink": true}` is how you develop a library against its consumer without publishing.
- `--prefer-dist` (default) downloads zip archives and is fast; `--prefer-source` clones git and is what you want when you need to patch a dependency locally.
- Vendor directories are not committed in modern practice; if a deployment target has no network, build the artifact in CI and ship `vendor/` inside it.

## Performance and Failure Modes

- Memory: `COMPOSER_MEMORY_LIMIT=-1 composer update` when resolution dies on `memory_limit`. Resolution is exponential in the worst case; a hard-to-solve tree is usually one package with an over-wide constraint.
- `composer.lock` merge conflicts: never hand-merge the JSON. Take either side, then re-apply your intent (`composer require vendor/pkg:^2.1`) and commit the regenerated lock.
- `--no-dev` in production is also a security measure: dev dependencies bring in test doubles and code-generation tools that have no business on a web server.
- `composer validate --strict` in CI catches a malformed `composer.json` before it reaches a consumer.

## Related

- Dependency ceilings during a PHP upgrade: `versions.md`
- Autoloader cost and preloading: `performance.md`
- Supply-chain posture: `security.md`
