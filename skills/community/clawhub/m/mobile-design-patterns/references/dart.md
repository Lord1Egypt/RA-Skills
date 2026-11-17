# Dart and Flutter pattern implementations

Load this when implementing or reviewing patterns in Dart. Assumes Dart 3 (sealed classes, records,
patterns, class modifiers) and Flutter. DI examples use Riverpod; the patterns are the same with
`get_it` or plain constructor injection.

## Repository

```dart
// Interface because widget and notifier tests override it with a fake.
abstract interface class DeviceRepository {
  Stream<List<Device>> watchDevices();
  Future<void> refresh();
}

final class OfflineFirstDeviceRepository implements DeviceRepository {
  OfflineFirstDeviceRepository(this._api, this._dao);

  final DeviceApi _api;
  final DeviceDao _dao;

  @override
  Stream<List<Device>> watchDevices() =>
      _dao.watchAll().map((rows) => [for (final row in rows) row.toDomain()]);

  @override
  Future<void> refresh() async {
    final dtos = await _api.devices();
    await _dao.upsertAll([for (final dto in dtos) dto.toRow()]);
  }
}
```

- The UI listens to the local database stream; `refresh()` only writes into it.
- JSON DTOs and database rows never reach widgets.

## Factory

```dart
sealed class Message {
  const Message();

  factory Message.fromJson(Map<String, Object?> json) => switch (json) {
        {'type': 'text', 'body': String body} => TextMessage(body),
        {'type': 'image', 'url': String url} => ImageMessage(Uri.parse(url)),
        _ => throw FormatException('Unknown message type: ${json['type']}'),
      };
}

final class TextMessage extends Message {
  const TextMessage(this.body);
  final String body;
}

final class ImageMessage extends Message {
  const ImageMessage(this.url);
  final Uri url;
}
```

- Map patterns check key presence and value types, so malformed JSON fails at the edge instead of
  with a cast error deep in the UI.
- Named constructors (`Device.placeholder()`) cover simple alternative constructions without a factory.

## Builder replaced by named parameters

```dart
final class ScanOptions {
  const ScanOptions({
    this.timeout = const Duration(seconds: 10),
    this.serviceFilter,
    this.lowLatency = false,
  });

  final Duration timeout;
  final String? serviceFilter;
  final bool lowLatency;

  ScanOptions copyWith({Duration? timeout, String? serviceFilter, bool? lowLatency}) => ScanOptions(
        timeout: timeout ?? this.timeout,
        serviceFilter: serviceFilter ?? this.serviceFilter,
        lowLatency: lowLatency ?? this.lowLatency,
      );
}

const options = ScanOptions(lowLatency: true);
```

- A hand-written `copyWith` cannot reset a nullable field to `null`. Code generation such as `freezed`
  handles that, or use a sentinel.

## Singleton replaced by DI scopes

```dart
final httpClientProvider = Provider<http.Client>((ref) {
  final client = http.Client();
  ref.onDispose(client.close);
  return client;
});

final deviceRepositoryProvider = Provider<DeviceRepository>(
  (ref) => OfflineFirstDeviceRepository(ref.watch(deviceApiProvider), ref.watch(deviceDaoProvider)),
);

// Test
final container = ProviderContainer(
  overrides: [deviceRepositoryProvider.overrideWithValue(FakeDeviceRepository())],
);
addTearDown(container.dispose);
```

- No top-level mutable variables holding clients or tokens.
- `late final` globals initialized in `main()` are a service locator in disguise; tests cannot replace them.

## Strategy

```dart
typedef BackoffPolicy = Duration Function(int attempt);

Duration fixedBackoff(int attempt) => const Duration(seconds: 1);
Duration exponentialBackoff(int attempt) => Duration(milliseconds: 500 * (1 << (attempt > 6 ? 6 : attempt)));

final class Uploader {
  Uploader({BackoffPolicy backoff = exponentialBackoff}) : _backoff = backoff;
  final BackoffPolicy _backoff;
}
```

A `typedef` of a function type covers most strategies. Use an interface when the strategy has several methods.

## Observer

```dart
final class ConnectionMonitor {
  final _controller = StreamController<ConnState>.broadcast();
  ConnState _state = const Disconnected();

  ConnState get state => _state;
  Stream<ConnState> get states => _controller.stream;

  void _emit(ConnState next) {
    _state = next;
    _controller.add(next);
  }

  Future<void> dispose() => _controller.close();
}
```

- Broadcast streams do not replay the latest value. Expose a `state` getter, or start the stream with it.
- Listeners store the `StreamSubscription` and cancel it in `dispose()`.
- In widgets prefer the state-management tool's observer (`ref.watch`, `BlocBuilder`) or `ValueListenableBuilder`
  over raw `StreamBuilder` plumbing.

## Adapter

```dart
// Callback API -> Future.
Future<PrintReceipt> printReceipt(LegacyPrinter printer, PrintJob job) {
  final completer = Completer<PrintReceipt>();
  printer.submit(job, onDone: completer.complete, onError: completer.completeError);
  return completer.future;
}

// Listener API -> Stream, registered only while someone listens.
Stream<bool> adapterEnabled(BluetoothAdapterWrapper adapter) {
  late final StreamController<bool> controller;
  void listener(bool enabled) => controller.add(enabled);
  controller = StreamController<bool>(
    onListen: () => adapter.addListener(listener),
    onCancel: () => adapter.removeListener(listener),
  );
  return controller.stream;
}
```

- Guard against the callback firing twice: `if (!completer.isCompleted) completer.complete(value);`.
- Platform channels are adapters too: generate them with Pigeon instead of hand-written method names.

## Decorator

```dart
final class TimedDeviceApi implements DeviceApi {
  TimedDeviceApi(this._inner, this._metrics);

  final DeviceApi _inner;
  final Metrics _metrics;

  @override
  Future<FirmwareInfo> firmwareInfo(String id) async {
    final watch = Stopwatch()..start();
    try {
      return await _inner.firmwareInfo(id);
    } finally {
      _metrics.record('firmwareInfo', watch.elapsed);
    }
  }

  // Dart has no automatic forwarding: every other member is forwarded by hand.
  @override
  Future<List<DeviceDto>> devices() => _inner.devices();
}
```

For HTTP concerns (auth headers, logging, retry) use the client's interceptor mechanism (for example `dio`
interceptors) rather than decorating every API class.

## Facade

```dart
final class DeviceSession {
  DeviceSession(this._ble, this._queue, this._machine);

  final BleClient _ble;
  final CommandQueue _queue;
  final ConnectionMachine _machine;

  Future<void> open(String deviceId) async {
    _machine.send(const Connect());
    await _ble.connect(deviceId);
    final mtu = await _queue.enqueue(() => _ble.requestMtu(deviceId, 247));
    await _queue.enqueue(() => _ble.discoverServices(deviceId));
    await _queue.enqueue(() => _ble.enableNotifications(deviceId, telemetryCharacteristic));
    _machine.send(LinkUp(mtu));
  }
}
```

`BleClient` is the app's own adapter over whichever BLE plugin the project uses. MTU requests are an
Android concept; on iOS the plugin typically reports the negotiated value instead.

## State machine (connection)

```dart
enum ConnError { timeout, rejected, bluetoothOff }

sealed class ConnState { const ConnState(); }
final class Disconnected extends ConnState { const Disconnected(); }
final class Connecting extends ConnState { const Connecting(this.attempt); final int attempt; }
final class Connected extends ConnState { const Connected(this.mtu); final int mtu; }
final class Disconnecting extends ConnState { const Disconnecting(); }
final class Failed extends ConnState { const Failed(this.error); final ConnError error; }

sealed class ConnEvent { const ConnEvent(); }
final class Connect extends ConnEvent { const Connect(); }
final class LinkUp extends ConnEvent { const LinkUp(this.mtu); final int mtu; }
final class LinkLost extends ConnEvent { const LinkLost(this.error); final ConnError error; }
final class Disconnect extends ConnEvent { const Disconnect(); }
final class Closed extends ConnEvent { const Closed(); }

ConnState reduce(ConnState state, ConnEvent event, {int maxAttempts = 3}) => switch ((state, event)) {
      (Disconnected() || Failed(), Connect()) => const Connecting(1),
      (Connecting(), LinkUp(:final mtu)) => Connected(mtu),
      (Connecting(:final attempt), LinkLost(:final error)) =>
        attempt < maxAttempts ? Connecting(attempt + 1) : Failed(error),
      (Connected(), LinkLost()) => const Connecting(1),
      (Connecting() || Connected(), Disconnect()) => const Disconnecting(),
      (Disconnecting(), Closed() || LinkLost()) => const Disconnected(),
      _ => state, // illegal transition: ignored, logged by the caller
    };

final class ConnectionMachine {
  final _states = StreamController<ConnState>.broadcast();
  ConnState state = const Disconnected();
  Stream<ConnState> get states => _states.stream;

  void send(ConnEvent event) {
    final next = reduce(state, event);
    if (identical(next, state)) return;
    state = next;
    _states.add(next);
  }
}
```

- An isolate is single-threaded, so `send` cannot race. It must stay synchronous: an `await` inside it
  would let another event interleave.
- These classes do not override `==`. Tests use matchers, or add `==` / `hashCode` (or `equatable`, `freezed`).

```dart
test('link lost while connected starts reconnect', () {
  final next = reduce(const Connected(185), const LinkLost(ConnError.timeout));
  expect(next, isA<Connecting>().having((s) => s.attempt, 'attempt', 1));
});
```

## Command

```dart
final class CommandQueue {
  Future<void> _tail = Future.value();

  // Runs commands strictly one after another; a failing command does not block the next.
  Future<T> enqueue<T>(Future<T> Function() command) {
    final result = _tail.then((_) => command());
    _tail = result.then<void>((_) {}, onError: (Object _, StackTrace __) {});
    return result;
  }
}
```

- Add a timeout per command (`command().timeout(...)`) when the underlying operation can hang.
- Undo / redo: commands with `apply` and `revert`, two stacks, redo cleared on every new command.

## Router (go_router)

```dart
GoRouter buildRouter(AuthState auth) => GoRouter(
      initialLocation: '/devices',
      refreshListenable: auth,
      redirect: (context, state) {
        final loggingIn = state.matchedLocation == '/login';
        if (!auth.isLoggedIn) return loggingIn ? null : '/login';
        if (loggingIn) return '/devices';
        return null;
      },
      routes: [
        GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
        GoRoute(
          path: '/devices',
          builder: (context, state) => const DeviceListScreen(),
          routes: [
            GoRoute(
              path: ':id',
              builder: (context, state) => DeviceDetailScreen(id: state.pathParameters['id']!),
            ),
          ],
        ),
      ],
    );
```

- Auth gating and deep-link handling live in `redirect`, not in each screen.
- Screens take callbacks or call `context.go(...)` with paths built in one place, not string literals
  scattered across widgets.

## Result type

```dart
sealed class Result<T> {
  const Result();
}

final class Ok<T> extends Result<T> {
  const Ok(this.value);
  final T value;
}

final class Err<T> extends Result<T> {
  const Err(this.error);
  final AppError error;
}

String label(Result<Device> r) => switch (r) {
      Ok(:final value) => value.name,
      Err(:final error) => error.message,
    };
```

- Return `Result` for expected failures (network, validation, pairing). Let `Error` subclasses
  (`StateError`, `ArgumentError`) propagate; they are bugs.

## Delegation

Dart has no `by` keyword. Options, in order of preference:

- Composition with explicit forwarding (as in the decorator above).
- Callbacks passed to the constructor for owner notifications, instead of a delegate interface.
- `mixin` for small reusable behaviour that needs no state from a specific superclass.

```dart
mixin Disposables {
  final _subscriptions = <StreamSubscription<Object?>>[];
  void track(StreamSubscription<Object?> s) => _subscriptions.add(s);
  Future<void> disposeAll() => Future.wait(_subscriptions.map((s) => s.cancel()));
}
```
