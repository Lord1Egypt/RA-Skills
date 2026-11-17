---
name: mobile-flutter
description: "Writes idiomatic modern Dart 3 and Flutter: records, patterns and sealed classes, async and Streams, Isolate.run, small const widgets, keys, context.mounted after await, disposing controllers, Riverpod or Bloc, go_router, Pigeon platform channels, flavors, lints and unit, widget, golden and integration tests. Use when writing, refactoring or reviewing Dart or Flutter code, screens, providers, blocs, routes or tests."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Dart and Flutter

Write Dart and Flutter code the way a senior Flutter engineer would: Dart 3 types that make illegal states
unrepresentable, widgets that rebuild only what changed, async code that respects the widget lifecycle,
and one consistent state management approach per app.

## When to use

- Writing a new screen, widget, provider, bloc, repository, route or platform channel in a Flutter app.
- Refactoring pre-Dart 3 code (enums plus nullable fields, `Map<String, dynamic>` everywhere, `is` chains).
- Fixing jank, leaks, "setState() called after dispose()" or "Looking up a deactivated widget's ancestor".
- Setting up `analysis_options.yaml`, flavors, `--dart-define-from-file`, Pigeon or the test pyramid.

Not for: reviewing a whole MR (use `mobile-code-review`), a security audit (use `mobile-security`),
or choosing an architecture from scratch (use `mobile-mvvm`, `mobile-mvi`).

## Workflow

1. Read the project setup before writing code.
   - `pubspec.yaml`: SDK constraint, state management package, router, codegen (`build_runner`, `freezed`).
   - `analysis_options.yaml`: which lint set is active.
   - Match the existing patterns. Never add Bloc to a Riverpod app or the other way round.
2. Model the data and state first with sealed classes, records and extension types (rules 1 to 3).
3. Write the logic outside widgets: repository, then Notifier or Bloc. Load
   [state management](references/state-management.md) for Riverpod and Bloc details.
4. Write the UI as small `const` widget classes. Check every `await` in UI code for a `mounted` check,
   and every controller, subscription and timer for a `dispose`.
5. Native code goes through Pigeon. Load [platform channels](references/platform-channels.md).
6. Add tests at the lowest level that proves the behaviour. Load [testing](references/testing.md).
7. If performance is in scope, measure in profile mode first. Load [performance](references/performance.md).
8. Run `dart format .`, `flutter analyze` and `flutter test`. Fix every warning before handing over.

## Rules

### 1. Closed state is a sealed class, matched with an exhaustive switch

The compiler flags every `switch` that misses a new subtype. No `default`, no stale branches.

```dart
// BAD: impossible combinations compile (isLoading && error != null)
class DeviceState { bool isLoading = false; Device? device; String? error; }

// GOOD
sealed class DeviceState {}
final class DeviceLoading extends DeviceState {}
final class DeviceReady extends DeviceState { DeviceReady(this.device); final Device device; }
final class DeviceFailed extends DeviceState { DeviceFailed(this.error); final Object error; }

Widget build(BuildContext context) => switch (state) {
  DeviceLoading() => const CircularProgressIndicator(),
  DeviceReady(:final device) => DeviceCard(device: device),
  DeviceFailed(:final error) => ErrorView(error: error),
};
```

- Add `when` guards for sub-cases: `Connecting(:final attempt) when attempt > 3 => ...`.
- Do not add `_ =>` to a switch over a sealed type. It hides the next missing case.

### 2. Records and patterns replace throwaway classes and unchecked maps

```dart
// BAD: unchecked casts on untrusted JSON, crash on a wrong type
final lat = json['lat'] as double;
final lng = json['lng'] as double;

// GOOD: destructure and validate in one step
({double lat, double lng}) parseLocation(Map<String, Object?> json) {
  if (json case {'lat': final double lat, 'lng': final double lng}) {
    return (lat: lat, lng: lng);
  }
  throw const FormatException('Invalid location');
}
```

- Use records for multiple return values: `final (count, name) = pair();`.
- Records are fine for private, local data. Public domain models stay named classes.
- Use dot shorthands (`mainAxisAlignment: .center`) and null-aware elements (`[a, ?maybeB]`) when the
  SDK constraint allows them and the codebase already uses them.

### 3. Class modifiers and extension types state the API contract

```dart
// BAD: any String goes, device and user IDs are interchangeable
Future<void> connect(String deviceId, String userId);

// GOOD: zero-cost wrappers, mixing them up is a compile error
extension type const DeviceId(String value) {}
extension type const UserId(String value) {}
Future<void> connect(DeviceId device, UserId user);
```

| Modifier | Use for |
|---|---|
| `final class` | Value and state classes; no subclassing or implementing outside the library |
| `abstract interface class` | Repository and service contracts that are only implemented |
| `base class` | Classes with invariants that subclasses must inherit, never re-implement |
| `sealed class` | Closed hierarchies matched with `switch` |
| `mixin class` | Rare; only when a type must be both a mixin and a class |

- Extension types are compile-time only. They are not a validation or security boundary: `id as String`
  still works. Validate in a factory if the format matters.

### 4. Every stream has one owner who closes it

```dart
// BAD: single-subscription stream exposed to many listeners -> "Stream has already been listened to"
final _controller = StreamController<ScanResult>();

// GOOD: broadcast for fan-out, closed by the owner
final _results = StreamController<ScanResult>.broadcast();
Stream<ScanResult> get results => _results.stream;
Future<void> dispose() => _results.close();
```

- Single-subscription: one listener, buffers until listened (file reads, HTTP bodies, `async*`).
- Broadcast: many listeners, drops events nobody hears (connection state, scan results).
- Prefer `async*` generators. Cancelling the subscription stops the generator at the next `yield`.
- Fire-and-forget futures are explicit: `unawaited(analytics.log(event));`.

### 5. CPU-heavy work leaves the UI isolate

```dart
// BAD: 5 MB JSON decoded on the UI isolate, frames drop
final data = jsonDecode(body);

// GOOD
final data = await Isolate.run(() => jsonDecode(body) as Map<String, Object?>);
```

- The closure must not capture `BuildContext`, widgets or large objects; everything captured is copied.
- `Isolate.run` is not available on web. Use `compute` in code that must run on web too.
- `async` alone does not move work off the UI thread. Only isolates do.

### 6. Widgets are small const classes, not helper methods

```dart
// BAD: rebuilt with the parent every time, no const, no own Element
Widget _buildHeader() => Padding(padding: const EdgeInsets.all(16), child: Text(title));

// GOOD
class DeviceHeader extends StatelessWidget {
  const DeviceHeader({super.key, required this.title});
  final String title;

  @override
  Widget build(BuildContext context) =>
      Padding(padding: const EdgeInsets.all(16), child: Text(title));
}
```

- `build` is pure and cheap: no futures, no controllers, no I/O.
- Create futures once (`late final _user = repo.fetchUser();`), never inside `FutureBuilder(future: ...)` in `build`.
- Read only what you need: `MediaQuery.sizeOf(context)` instead of `MediaQuery.of(context).size`.

### 7. Keys only where identity matters

```dart
// BAD: stateful rows lose or swap state on reorder and delete
ListView.builder(itemBuilder: (context, i) => DeviceTile(device: devices[i]));

// GOOD
ListView.builder(
  itemCount: devices.length,
  itemBuilder: (context, i) => DeviceTile(key: ValueKey(devices[i].id), device: devices[i]),
);
```

- `ValueKey(id)` for list items that can reorder, insert or delete. Never `ValueKey(index)`.
- `GlobalKey` only for real cross-tree access (`Form` validation, a `Navigator` key for go_router).
  It is expensive and a widget with a `GlobalKey` must not appear twice in the tree.
- Never create keys in `build` (`GlobalKey()` or `UniqueKey()`); the state resets on every rebuild.

### 8. Check `mounted` after every `await` before using context or state

```dart
// BAD: the widget may be gone; wrong navigator or a crash
onPressed: () async {
  await repo.save(form);
  context.pop();
},

// GOOD
onPressed: () async {
  await repo.save(form);
  if (!context.mounted) return;
  context.pop();
},
```

- Inside a `State`, use `if (!mounted) return;` before `setState` or `context`.
- In a Riverpod notifier, use `if (!ref.mounted) return;`. In a Cubit, `if (isClosed) return;`.
- Keep `use_build_context_synchronously` enabled; it is in `flutter_lints`.

### 9. Whatever a State creates, it disposes

```dart
// BAD: created in build, never disposed, text lost on rebuild
Widget build(BuildContext context) => TextField(controller: TextEditingController());

// GOOD
final _controller = TextEditingController();
late final StreamSubscription<int> _sub;
Timer? _poll;

@override
void initState() {
  super.initState();
  _sub = widget.battery.listen(_onLevel);
}

@override
void dispose() {
  _poll?.cancel();
  _sub.cancel();
  _controller.dispose();
  super.dispose();
}
```

- Covers `TextEditingController`, `ScrollController`, `PageController`, `FocusNode`, `AnimationController`,
  `StreamSubscription`, `Timer`, `ChangeNotifier`s the State created.
- Do not dispose objects passed in from outside; their owner does.
- Avoid `late final _sub = stream.listen(...)`: it subscribes lazily, possibly for the first time in `dispose`.

### 10. One state management approach per app, used the same way everywhere

Riverpod:
```dart
// BAD: read in build never rebuilds; watch in a callback rebuilds for nothing
final todos = ref.read(todosProvider);
onPressed: () => ref.watch(todosProvider.notifier).add(todo),

// GOOD
final todos = ref.watch(todosProvider);                     // build: rebuild on change
onPressed: () => ref.read(todosProvider.notifier).add(todo), // callbacks: one-off read
ref.listen(todosProvider, (prev, next) { /* snackbar, navigation */ });
```

Bloc:
```dart
// BAD: side effect inside builder, runs on every rebuild
BlocBuilder<LoginBloc, LoginState>(builder: (context, state) {
  if (state is LoginSuccess) context.go('/home');
  return const LoginForm();
})

// GOOD
BlocListener<LoginBloc, LoginState>(
  listenWhen: (previous, current) => current is LoginSuccess,
  listener: (context, state) => context.go('/home'),
  child: const LoginForm(),
)
```

- Riverpod: screen state uses `autoDispose` (default with `@riverpod` codegen). Narrow rebuilds with
  `ref.watch(provider.select((s) => s.count))`.
- Bloc: `Cubit` for simple method-driven state, `Bloc` when events need transformers (debounce, restartable).
- No business logic, API calls or repositories in widgets.

### 11. Routing is declarative, auth lives in one redirect, deep link input is untrusted

```dart
// BAD: auth check copied into every screen, the protected screen flashes before it runs
@override
void initState() {
  super.initState();
  if (!auth.isLoggedIn) WidgetsBinding.instance.addPostFrameCallback((_) => context.go('/login'));
}

// GOOD: one redirect, re-evaluated whenever auth notifies
GoRouter(
  refreshListenable: auth,
  redirect: (context, state) {
    final atLogin = state.matchedLocation == '/login';
    if (!auth.isLoggedIn) return atLogin ? null : '/login';
    if (atLogin) return '/';
    return null;
  },
  routes: [...],
);
```

- `redirect` returns `null` for "stay". Always guard the target route to avoid redirect loops.
- Path and query parameters arrive from outside the app via deep links. Parse and validate them; a
  malformed ID shows an error screen, never a crash or a privileged action.
- App Links (Android `assetlinks.json`, `autoVerify`) and Universal Links (Associated Domains
  entitlement) are platform config. Call out every manifest, `Info.plist` and entitlement change.
- Typed routes with `go_router_builder` are optional; adopt them app-wide or not at all.

### 12. Build config comes from flavors and dart-defines, secrets do not

```dart
// BAD: shipped in the binary, readable with `strings`, obfuscation does not hide it
const apiKey = String.fromEnvironment('PAYMENT_SECRET_KEY');

// GOOD: only non-secret config at build time
const apiBaseUrl = String.fromEnvironment('API_BASE_URL');
// flutter run --flavor staging --dart-define-from-file=config/staging.json
```

- `--flavor` selects the Android product flavor and the Xcode scheme; both must exist natively.
- `String.fromEnvironment` only works in a `const` context. Fail fast if a required value is empty.
- Secrets that must stay secret live on a server; the app gets short-lived tokens at runtime and stores
  them in the Keychain or Android Keystore backed storage.
- Release builds: `--obfuscate --split-debug-info=<dir>`; keep the symbol files to symbolize crashes.

### 13. Platform channels are generated with Pigeon

```dart
// BAD: stringly typed, untyped Map, typos fail at runtime
final level = await const MethodChannel('device').invokeMethod('getBatery');

// GOOD: pigeons/device_api.dart, generated Dart, Kotlin and Swift stay in sync
@HostApi()
abstract class DeviceApi {
  DeviceInfo getDeviceInfo();
  @async
  bool requestPairing(String deviceId);
}
```

- Native handlers run on the platform main thread by default. Move heavy work off it.
- Native code validates every argument from Dart like any other external input.

### 14. Lints are strict and warnings are not ignored

```yaml
# BAD: default template, never touched, casts from dynamic unchecked
include: package:flutter_lints/flutter.yaml

# GOOD
include: package:flutter_lints/flutter.yaml
analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
linter:
  rules:
    - prefer_const_constructors
    - prefer_final_locals
    - unawaited_futures
    - discarded_futures
    - cancel_subscriptions
    - close_sinks
    - avoid_dynamic_calls
```

- `very_good_analysis` is a reasonable stricter alternative. Pick one set, do not mix.
- `// ignore:` needs a reason comment next to it.
- Use `package:logging` or a logger behind an interface, not `print`. Never log tokens or device IDs.

### 15. Tests are deterministic and at the lowest useful level

```dart
// BAD: real time, slow and flaky
await Future<void>.delayed(const Duration(seconds: 2));
expect(cubit.state, 2);

// GOOD: virtual time
fakeAsync((async) {
  final values = <int>[];
  countdown(2).listen(values.add);
  async.elapse(const Duration(seconds: 3));
  expect(values, [2, 1, 0]);
});
```

- Unit tests for notifiers, blocs and repositories; widget tests for screens; few `integration_test` flows.
- `pumpAndSettle` times out on endless animations (a looping progress indicator). Use `pump(duration)`.

## Anti-patterns

- `setState` at the top of a screen for a value one small widget shows. Push state down or use a listenable.
- `Widget _buildX()` helper methods in place of widget classes.
- `!` on values from JSON, platform channels or route parameters.
- `catch (e) {}` or catching `Error` (`StateError`, `TypeError`) to keep going; those are bugs.
- `late` fields that may never be initialized on some path.
- `dynamic` and `Map<String, dynamic>` leaking past the data layer. Map to typed models at the edge.
- A provider or bloc that holds a `BuildContext`, a widget or a controller.
- Mixing Riverpod, Bloc, Provider and GetX in one app.
- `Opacity` animated every frame; use `FadeTransition` or `AnimatedOpacity`.
- `RepaintBoundary` sprinkled everywhere "for performance" without a profile showing it helps.
- Secrets, API keys or signing material in `--dart-define`, `.env` assets or source.
- Golden tests run on every developer machine; font rendering differs across platforms.

## Checklist

- [ ] Matches the app's existing state management, router and codegen choices
- [ ] Closed state modelled as sealed classes; switches exhaustive without `_`
- [ ] Untrusted JSON and route parameters parsed with patterns or validated, no blind `as` or `!`
- [ ] Every `StreamController` closed; broadcast only where there are many listeners
- [ ] CPU-heavy work in `Isolate.run` or `compute`
- [ ] Widgets are classes with `const` constructors; `build` has no side effects or futures
- [ ] `ValueKey(id)` on reorderable list items; no keys created in `build`
- [ ] `mounted` / `context.mounted` / `ref.mounted` / `isClosed` checked after each `await`
- [ ] Controllers, focus nodes, subscriptions and timers disposed or cancelled
- [ ] `ref.watch` in build, `ref.read` in callbacks, side effects in `ref.listen` or `BlocListener`
- [ ] Auth redirect central, guarded against loops; deep link parameters validated
- [ ] No secrets in dart-defines or assets; manifest, plist and entitlement changes called out
- [ ] Platform channels generated with Pigeon; native work off the main thread
- [ ] `flutter analyze` clean with strict lints; `dart format` applied
- [ ] New logic covered by deterministic unit or widget tests; `flutter test` passes

## Related skills

- `mobile-code-review` -- review a Flutter MR against these rules
- `mobile-security` -- secure storage, certificate pinning, deep link and logging audits
- `mobile-mvvm`, `mobile-mvi` -- architecture behind Riverpod notifiers and Blocs
- `mobile-design-patterns` -- repository, adapter and strategy patterns in Dart
- `mobile-kotlin`, `mobile-swift` -- native side of Pigeon channels and plugins
- `mobile-ci-cd` -- flavors, signing, obfuscation symbols and golden tests in CI
- `mobile-ble` -- Bluetooth Low Energy in Flutter and on the native side
- `mobile-testing` -- cross-platform test strategy and goldens
- `mobile-performance` -- DevTools profiling, raster and UI thread jank
