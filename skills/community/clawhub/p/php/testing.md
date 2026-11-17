# Testing — PHPUnit Without False Green

## Configuration Worth Copying

```xml
<phpunit bootstrap="vendor/autoload.php"
         colors="true"
         failOnWarning="true"
         failOnNotice="true"
         failOnDeprecation="true"
         beStrictAboutOutputDuringTests="true"
         beStrictAboutTestsThatDoNotTestAnything="true"
         cacheDirectory=".phpunit.cache">
  <testsuites>
    <testsuite name="unit"><directory>tests/Unit</directory></testsuite>
    <testsuite name="integration"><directory>tests/Integration</directory></testsuite>
  </testsuites>
</phpunit>
```

- `failOnDeprecation` is what turns the next PHP upgrade from a wall into a list (`versions.md`).
- `beStrictAboutOutputDuringTests` catches the stray `var_dump` that would otherwise reach production, and the accidental output that breaks `header()` in the real app.
- Separate unit and integration suites so the fast one can run on every save and the slow one on push.

## assertSame, Not assertEquals

- `assertEquals` compares with `==`, so `assertEquals(1, "1")`, `assertEquals(0, "")` on older semantics, and `assertEquals(1.0, 1)` all pass. A test suite built on it cannot catch the type bugs that are PHP's most common defect class (`types.md`).
- `assertSame` for scalars and identity, `assertEquals` only where you deliberately want value equality on objects, `assertEqualsCanonicalizing` when array ORDER is genuinely irrelevant.
- `assertNull`, `assertFalse`, `assertTrue` over `assertEquals(null, …)` — they distinguish `null` from `false` from `0`.
- Floats: `assertEqualsWithDelta($expected, $actual, 0.0001)`; `assertSame` on floats is a flake generator.

## Test Structure

- One behavior per test, named for the behavior: `testRefundFailsAfterThirtyDays`, not `testRefund2`.
- Arrange / act / assert, with the arrangement small enough to read. A twenty-line setup means the unit under test has too many collaborators.
- Data providers must be `static` in PHPUnit 10 and later, and attributes replaced annotations: `#[DataProvider('cases')]` instead of `@dataProvider`. A provider that is not static, or an annotation on a version that no longer reads them, silently produces zero cases — the test "passes" without running.
- Name the provider rows (`yield 'expired card' => [...]`) so a failure message tells you which case broke.
- `--order-by=random` (with the printed seed for reproduction) exposes inter-test coupling. A suite that only passes in declaration order has shared state.

## State That Leaks Between Tests

PHPUnit runs the whole suite in one process. Everything global survives from test to test:

- Static properties and singletons — reset them in `tearDown`, or stop using them.
- `date_default_timezone_set`, `setlocale`, `ini_set`, `putenv` — restore in `tearDown`.
- The container/service locator if your bootstrap builds it once.
- `$_SERVER`, `$_GET`, `$_SESSION` mutated by a test.
- `@runInSeparateProcess` isolates a test at a heavy cost (a full bootstrap per test); use it as a diagnosis for leakage, then fix the leak instead of keeping the annotation.

## Doubles

- `createStub()` when you only need canned return values; `createMock()` when you also assert on interactions. Both auto-double every method to return `null`, so a method you forgot to configure returns `null` and the failure appears somewhere else.
- Mock the INTERFACE, not the concrete class: `final` classes cannot be doubled at all, and doubling a concrete class couples the test to its implementation.
- Partial mocks (`onlyMethods([...])` on a real object) mean the unit under test is doing two jobs — the split is usually the real fix.
- Never mock what you do not own. Wrap a third-party client in your own interface and double that; otherwise a library upgrade breaks tests that still "pass" against a signature nobody has.
- Time: inject a clock (PSR-20 `ClockInterface`) rather than calling `time()`. A test that sleeps, or that fails at midnight UTC, comes from a hardcoded now (`datetime.md`).
- Randomness and UUIDs: inject a generator. The same argument as time.

## Database Tests

- Wrap each test in a transaction and roll back in `tearDown` — orders of magnitude faster than truncating tables, and it leaves the database clean when a test fails midway.
- Test against the SAME engine as production. SQLite in memory is fast and diverges on strict modes, date functions, JSON support, and foreign-key enforcement; a green suite on SQLite tells you nothing about a MySQL-specific query (`database.md`).
- Migrations run once per suite, not per test. If your migrations are slow, that is a signal about the migrations.
- Factories over fixture files: a fixture set grows until nobody knows which test depends on which row, and a change to one row breaks twenty unrelated tests.

## Coverage and What It Means

- Coverage needs a driver: `pcov` is markedly faster for line coverage; Xdebug is required for branch and path coverage. `XDEBUG_MODE=coverage` must be set — without it PHPUnit reports zero and does not always say why.
- Line coverage measures execution, not verification: a test with no assertions that walks the whole file reports 100%. `beStrictAboutTestsThatDoNotTestAnything` catches the worst of it.
- A coverage target enforced in CI selects for tests that touch lines. Use coverage to FIND untested areas, and mutation testing (Infection's MSI) to judge whether the tests that exist actually detect changes.
- Cover the boundaries the domain cares about — money rounding, timezone edges, permission checks — before chasing a percentage.

## Running and Triaging

- `--filter 'RefundTest::testExpired'`, `--group slow`, `--exclude-group integration`, `--testdox` for readable output.
- `--stop-on-failure` while fixing; full run before pushing.
- A test that fails only in CI: check the PHP version, the timezone, the locale, the filesystem case sensitivity, and the test order seed. That list solves nearly all of them (`debugging.md`).
- Write the failing test BEFORE the fix. A test that was never seen red proves nothing about the fix that followed it.

## Related

- What to assert about types: `types.md`
- Static analysis as the other half of the safety net: `static-analysis.md`
- Making deprecations visible before an upgrade: `versions.md`
