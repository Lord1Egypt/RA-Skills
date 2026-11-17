# Static Analysis, Coding Standards, and Automated Refactoring

Tests prove the paths you thought of; an analyzer covers every path in the file. In PHP the analyzer earns its keep specifically because the language will coerce, return `false`, and juggle rather than stop.

## Adopting PHPStan on an Existing Codebase

```neon
# phpstan.neon
parameters:
    level: 6
    paths: [src, tests]
    phpVersion: 80300
    treatPhpDocTypesAsCertain: false
```

1. Start at the level where the run finishes: `vendor/bin/phpstan analyse --level 0`, then raise until the output is large but not absurd.
2. Freeze the debt: `phpstan analyse --generate-baseline`. The baseline is a file of currently-ignored errors; new code is checked from day one while the legacy stays quiet.
3. Ratchet: raise the level, regenerate, and require that the baseline only ever SHRINKS. Baseline line count is the honest progress metric — the level number alone says nothing about how much is ignored.
4. Run it in CI with the same version as the local hook. Two versions means an error that only appears in one place, which teaches the team to distrust the tool.
5. `--memory-limit=1G` on large codebases; analysis is memory-hungry by nature.

- Levels are cumulative: low levels catch undefined variables and unknown methods, high levels demand full array-shape and generic annotations. The value curve is steepest in the middle.
- `treatPhpDocTypesAsCertain: false` stops the analyzer from calling your defensive null checks redundant when the docblock claims a type the runtime does not guarantee.
- Psalm is the alternative with the same shape (`psalm.xml`, `--set-baseline`, error levels counted the other way round: 1 is strictest). Its distinctive feature is taint analysis (`--taint-analysis`), which traces user input to a sink and finds injection paths no linter sees (`security.md`).

## Annotating What PHP Cannot Express

PHP has no generics, so `array` tells the analyzer nothing. Docblocks carry the shape:

```php
/** @param list<int> $ids @return array<string, Invoice> */
function loadByReference(array $ids): array {}

/** @return array{id: int, email: string, verified: bool} */
function toRow(User $u): array {}

/** @template T of object @param class-string<T> $class @return T */
function make(string $class): object {}
```

- `list<T>` (sequential integer keys) versus `array<int, T>` (any integer keys) is a real distinction and it is exactly the one that breaks JSON encoding (`arrays.md`, `json.md`).
- `array{…}` shapes turn a key typo into a build failure. Use them for anything crossing a function boundary.
- `class-string<T>`, `non-empty-string`, `positive-int`, `int<0, 100>` narrow beyond native types and cost nothing at runtime.
- Native types where the language allows them, docblocks only for what it cannot express. A docblock duplicating a native type is a lie waiting to happen when the signature changes.
- `@psalm-assert`/`@phpstan-assert` on a validator lets the analyzer narrow the type after your check runs — the mechanism that makes custom guards useful.

## Coding Standards

- PER Coding Style is the current evolution of PSR-12, which superseded PSR-2. Pick one, put it in a config file, and stop discussing it.
- PHP-CS-Fixer (`.php-cs-fixer.dist.php`) rewrites; PHP_CodeSniffer (`phpcs.xml`) reports and `phpcbf` fixes a subset. Running both means two tools arguing about the same lines — choose one as the authority.
- Formatting belongs in a pre-commit hook and in CI as a `--dry-run` check, never as review comments. A human reviewing whitespace is a wasted review.
- The standard is a config value, not a truth: `style` in `config.yaml` selects it (SKILL.md Configuration).

## Rector

- Rector applies rule sets mechanically: `rector process --dry-run` first, always.
- The highest-value sets: `LevelSetList::UP_TO_PHP_83` for version migrations, `SetList::CODE_QUALITY`, `SetList::TYPE_DECLARATION` for adding native types to an untyped codebase.
- It is a refactoring tool, not an oracle: review the diff, run the suite, and commit each set separately so a regression is bisectable.
- Adding native types with Rector then raising the analyzer level is the fastest legal route out of an untyped legacy codebase — in that order, because types make the analyzer useful.

## What to Run in CI, in Order

```bash
composer validate --strict
composer audit
vendor/bin/php-cs-fixer fix --dry-run --diff
vendor/bin/phpstan analyse --no-progress
vendor/bin/phpunit
```

Cheapest and most deterministic first: a formatting failure should not wait behind an eight-minute test suite. Each step gets its own CI job only if the suite is slow enough to justify the parallelism cost.

## Reading Analyzer Output Honestly

- "Cannot call method on `Foo|null`" is almost never a false positive; it is the null you have not handled yet.
- "Comparison using `===` between `int` and `string` will always evaluate to false" is the analyzer finding a real dead branch — go read the code, do not add an ignore.
- Genuine false positives get a narrow, commented inline ignore (`@phpstan-ignore-next-line` with a reason), never a broad `ignoreErrors` regex that silences a whole class of real bugs later.
- An error you do not understand is information about the code, not about the tool. The urge to configure it away is the signal to read the line again.

## Related

- The type semantics the analyzer is enforcing: `types.md`
- Tests as the complementary safety net: `testing.md`
- Version migrations Rector automates: `versions.md`
