# Dart and Flutter review reference

Load this when the change contains `.dart` files. Assume Dart 3 with sound null safety.

## Quick scan

| Pattern | Why | Usual severity |
|---|---|---|
| `context` used after `await` without a `mounted` check | Uses a dead element, wrong navigator, crash | Major |
| `setState` after an `await` without `if (!mounted) return;` | Exception on disposed State | Major |
| `.listen(` with the subscription not stored and cancelled | Leak, callbacks on disposed widget | Major |
| `TextEditingController(`, `AnimationController(`, `ScrollController(`, `FocusNode(` without `dispose` | Leak | Major |
| `FutureBuilder(future: fetch()` in `build` | Refetches on every rebuild | Major |
| `!` on values from network, platform or JSON | Crash | Major |
| `catch (e) {}` / `catch (_) {}` | Swallowed error | Major |
| Widget-returning helper methods (`Widget _buildHeader()`) in large widgets | Loses const and rebuild granularity | Minor |
| `ListView(children: list.map(...).toList())` for long lists | Builds every item up front | Major for unbounded lists |
| Missing `const` on constructors and widgets | Extra rebuild work | Nit (the linter usually catches it) |
| `print(` / `debugPrint(` with tokens, emails, device IDs | Personal data in logs | Major, see `mobile-security` |

## Async and lifecycle

```dart
// BAD
Future<void> _save() async {
  await repo.save(form);
  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Saved')));
}

// GOOD
Future<void> _save() async {
  await repo.save(form);
  if (!mounted) return; // inside State; use context.mounted when only a BuildContext is available
  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Saved')));
}
```

- Every controller, `FocusNode`, `StreamSubscription`, `Timer` and `AnimationController` created by a
  `State` is disposed or cancelled in `dispose()`.
- `StreamController`s are closed by their owner.
- Fire-and-forget futures are explicit: wrap in `unawaited(...)` and enable the `unawaited_futures` or
  `discarded_futures` lint.

## Concurrency

- CPU-heavy work (large JSON, image processing, crypto) runs in `Isolate.run` or `compute`.
- Data sent to isolates is sendable; closures passed to `Isolate.run` do not capture large objects or
  `BuildContext`.

## Widgets and performance

- `build` is pure and cheap: no network calls, no controller creation, no future creation.

```dart
// BAD: new future each rebuild, request fires repeatedly
@override
Widget build(BuildContext context) => FutureBuilder(future: api.fetchUser(), builder: _builder);

// GOOD: future created once
late final Future<User> _user = api.fetchUser();

@override
Widget build(BuildContext context) => FutureBuilder(future: _user, builder: _builder);
```

- Split large widgets into small `StatelessWidget` classes with `const` constructors rather than private
  methods returning widgets.
- Keys: `ValueKey(item.id)` on stateful list items that can reorder. `GlobalKey` only when cross-tree access
  is really needed.
- Long or unbounded lists use `ListView.builder` / `SliverList.builder`.
- Large images are decoded at display size (`cacheWidth` / `cacheHeight` or `ResizeImage`).
- State is scoped as low as possible; a `setState` at the top of a screen rebuilds everything below it.

## State management

- Riverpod: `ref.watch` in `build`, `ref.read` in callbacks, `ref.listen` for side effects such as
  navigation and snackbars. Providers that hold screen state use `autoDispose` unless they must persist.
- Bloc: no `emit` after the handler completes or after `close`; long streams use `emit.forEach` /
  `emit.onEach`. UI side effects go through `BlocListener`, not `BlocBuilder`.
- Business logic does not live in widgets.

## Errors and null safety

- Catch specific types (`on SocketException`, `on FormatException`, domain exceptions). Never catch `Error`
  subclasses such as `StateError` or `TypeError` to keep going; they indicate bugs.
- JSON parsing validates types instead of `as` casts on untrusted data.
- Sealed classes plus exhaustive `switch` for result and state types; the compiler then flags missing cases.

## Platform integration

- Platform channels use Pigeon or a typed wrapper; channel names and method names are not stringly duplicated.
- Native side handlers run on the platform main thread unless a background task queue is configured;
  heavy native work is moved off it.
- New permissions, `Info.plist` keys or `AndroidManifest.xml` entries are called out in the MR.

## Accessibility and i18n

- Icon-only buttons have a `tooltip` or `Semantics(label: ...)`.
- Text uses theme styles and respects text scaling; no fixed-height containers around text.
- Strings come from `AppLocalizations` (gen-l10n) with ICU plurals, not string concatenation.
- `EdgeInsetsDirectional` and `AlignmentDirectional` for RTL support.

## Testing

- Unit tests with `package:test`; mocks with `mocktail`; prefer fakes for repositories.
- Widget tests use `pump(duration)` for timed behaviour; `pumpAndSettle` never returns with infinite
  animations such as a looping progress indicator.
- Golden tests run on one pinned platform in CI because font rendering differs.
- Time-dependent logic uses `fakeAsync` or an injected clock.
