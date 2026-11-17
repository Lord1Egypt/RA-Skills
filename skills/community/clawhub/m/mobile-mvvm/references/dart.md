# MVVM with Dart and Flutter (Riverpod, or provider)

Load this when building or reviewing a Flutter screen and its state holder. Assumes Dart 3, Flutter
stable and Riverpod 3. In Riverpod the "ViewModel" is a `Notifier` or `AsyncNotifier`; with the simpler
`provider` package it is a `ChangeNotifier`.

The feature: a device list loaded from a repository, pull to refresh, an "online only" filter, favorites
with optimistic update and rollback, and a snackbar when something fails.

## Domain and data contract

```dart
@immutable
class Device {
  const Device({required this.id, required this.name, required this.isOnline, this.isFavorite = false});

  final String id;
  final String name;
  final bool isOnline;
  final bool isFavorite;

  Device copyWith({bool? isFavorite}) =>
      Device(id: id, name: name, isOnline: isOnline, isFavorite: isFavorite ?? this.isFavorite);
}

class DeviceException implements Exception {}

abstract interface class DeviceRepository {
  Future<List<Device>> fetchDevices();
  Future<void> setFavorite(String id, {required bool favorite});
}

final deviceRepositoryProvider = Provider<DeviceRepository>(
  (ref) => HttpDeviceRepository(ref.watch(httpClientProvider)), // data layer
);
```

- Use `freezed` or `equatable` for value equality and `copyWith` in real code; it is written by hand
  here to keep the example dependency-free.

## State

```dart
enum UserMessage { refreshFailed, favoriteFailed }

@immutable
class DeviceListState {
  const DeviceListState({this.devices = const [], this.onlineOnly = false, this.userMessage});

  final List<Device> devices;
  final bool onlineOnly;
  final UserMessage? userMessage;

  List<Device> get visibleDevices => onlineOnly ? devices.where((d) => d.isOnline).toList() : devices;

  DeviceListState copyWith({
    List<Device>? devices,
    bool? onlineOnly,
    ValueGetter<UserMessage?>? userMessage, // a getter, so callers can set the field back to null
  }) =>
      DeviceListState(
        devices: devices ?? this.devices,
        onlineOnly: onlineOnly ?? this.onlineOnly,
        userMessage: userMessage != null ? userMessage() : this.userMessage,
      );
}
```

## Notifier (the ViewModel)

```dart
final deviceListProvider =
    AsyncNotifierProvider.autoDispose<DeviceListNotifier, DeviceListState>(DeviceListNotifier.new);

class DeviceListNotifier extends AsyncNotifier<DeviceListState> {
  DeviceRepository get _repository => ref.read(deviceRepositoryProvider);

  @override
  Future<DeviceListState> build() async {
    final devices = await ref.watch(deviceRepositoryProvider).fetchDevices();
    return DeviceListState(devices: devices);
  }

  Future<void> refresh() async {
    try {
      final devices = await _repository.fetchDevices();
      if (!ref.mounted) return;
      _update((s) => s.copyWith(devices: devices));
    } on DeviceException {
      if (!ref.mounted) return;
      _update((s) => s.copyWith(userMessage: () => UserMessage.refreshFailed));
    }
  }

  void setOnlineOnly(bool value) => _update((s) => s.copyWith(onlineOnly: value));

  Future<void> toggleFavorite(String id) async {
    final current = state.value;
    if (current == null) return;
    final newValue = !current.devices.firstWhere((d) => d.id == id).isFavorite;
    _update((s) => s.copyWith(devices: _withFavorite(s.devices, id, newValue)));
    try {
      await _repository.setFavorite(id, favorite: newValue);
    } on DeviceException {
      if (!ref.mounted) return;
      _update((s) => s.copyWith(
            devices: _withFavorite(s.devices, id, !newValue),
            userMessage: () => UserMessage.favoriteFailed,
          ));
    }
  }

  void userMessageShown() => _update((s) => s.copyWith(userMessage: () => null));

  void _update(DeviceListState Function(DeviceListState) transform) {
    final current = state.value;
    if (current != null) state = AsyncData(transform(current));
  }
}

List<Device> _withFavorite(List<Device> devices, String id, bool favorite) => [
      for (final d in devices) d.id == id ? d.copyWith(isFavorite: favorite) : d,
    ];
```

Notes:
- `build` loads the first time the screen watches the provider; `autoDispose` frees it when the screen leaves.
- `ref.watch` in `build` for dependencies, `ref.read` in methods.
- After every `await`, check `ref.mounted` before touching `state`; the screen may be gone.
- `_update` always transforms the latest state, so a filter toggled during a refresh is not overwritten.
- A failed refresh keeps the data and shows a message instead of replacing the list with an error page.
- With code generation (`@riverpod` annotations) the provider is generated; the class body is the same.

## Screen

```dart
class DeviceListScreen extends ConsumerWidget {
  const DeviceListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.listen(deviceListProvider.select((s) => s.value?.userMessage), (_, message) {
      if (message == null) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message.text(context))));
      ref.read(deviceListProvider.notifier).userMessageShown();
    });

    final asyncState = ref.watch(deviceListProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text(context.l10n.devicesTitle), // context.l10n: the app's AppLocalizations extension
        actions: [
          Switch(
            value: asyncState.value?.onlineOnly ?? false,
            onChanged: (value) => ref.read(deviceListProvider.notifier).setOnlineOnly(value),
          ),
        ],
      ),
      body: switch (asyncState) {
        AsyncData(:final value) => RefreshIndicator(
            onRefresh: () => ref.read(deviceListProvider.notifier).refresh(),
            child: ListView.builder(
              itemCount: value.visibleDevices.length,
              itemBuilder: (context, index) {
                final device = value.visibleDevices[index];
                return DeviceTile(
                  key: ValueKey(device.id),
                  device: device,
                  onFavoriteTap: () => ref.read(deviceListProvider.notifier).toggleFavorite(device.id),
                );
              },
            ),
          ),
        AsyncError() => ErrorView(onRetry: () => ref.invalidate(deviceListProvider)),
        _ => const Center(child: CircularProgressIndicator()),
      },
    );
  }
}

extension on UserMessage {
  String text(BuildContext context) => switch (this) {
        UserMessage.refreshFailed => context.l10n.devicesRefreshFailed,
        UserMessage.favoriteFailed => context.l10n.devicesFavoriteFailed,
      };
}
```

- `ref.listen` performs the one-off effect and acknowledges it; `ref.watch` only renders.
- `DeviceTile` is a separate `StatelessWidget` with a `const` constructor, not a helper method.

## Saved state

Riverpod state is lost on process death. For small widget-owned input, use Flutter state restoration
(requires `restorationScopeId` on `MaterialApp`):

```dart
class _SearchFieldState extends State<SearchField> with RestorationMixin {
  final _query = RestorableTextEditingController();

  @override
  String? get restorationId => 'device_search';

  @override
  void restoreState(RestorationBucket? oldBucket, bool initialRestore) {
    registerForRestoration(_query, 'query');
  }

  @override
  void dispose() {
    _query.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => TextField(controller: _query.value);
}
```

## Tests

```dart
class FakeDeviceRepository implements DeviceRepository {
  FakeDeviceRepository(this.devices);

  List<Device> devices;
  Exception? fetchError;
  Exception? favoriteError;

  @override
  Future<List<Device>> fetchDevices() async {
    if (fetchError case final error?) throw error;
    return devices;
  }

  @override
  Future<void> setFavorite(String id, {required bool favorite}) async {
    if (favoriteError case final error?) throw error;
  }
}

void main() {
  const online = Device(id: '1', name: 'Gateway', isOnline: true);
  const offline = Device(id: '2', name: 'Sensor', isOnline: false);

  late FakeDeviceRepository repository;
  late ProviderContainer container;

  setUp(() {
    repository = FakeDeviceRepository([online, offline]);
    container = ProviderContainer(overrides: [deviceRepositoryProvider.overrideWithValue(repository)]);
    addTearDown(container.dispose);
    container.listen(deviceListProvider, (_, _) {}); // keeps the autoDispose provider alive
  });

  DeviceListNotifier notifier() => container.read(deviceListProvider.notifier);
  DeviceListState current() => container.read(deviceListProvider).value!;

  test('loads devices', () async {
    final state = await container.read(deviceListProvider.future);
    expect(state.devices.map((d) => d.id), ['1', '2']);
  });

  test('online only hides offline devices', () async {
    await container.read(deviceListProvider.future);
    notifier().setOnlineOnly(true);
    expect(current().visibleDevices.map((d) => d.id), ['1']);
  });

  test('refresh failure keeps data and shows message until acknowledged', () async {
    await container.read(deviceListProvider.future);
    repository.fetchError = DeviceException();

    await notifier().refresh();

    expect(current().devices, hasLength(2));
    expect(current().userMessage, UserMessage.refreshFailed);
    notifier().userMessageShown();
    expect(current().userMessage, isNull);
  });

  test('favorite failure rolls back', () async {
    await container.read(deviceListProvider.future);
    repository.favoriteError = DeviceException();

    await notifier().toggleFavorite('1');

    expect(current().devices.first.isFavorite, isFalse);
    expect(current().userMessage, UserMessage.favoriteFailed);
  });
}
```

- Override the repository provider, not the notifier; the notifier is the unit under test.
- `container.listen` keeps an `autoDispose` provider alive between reads in a test.

## Simpler option: ChangeNotifier with provider

Fine for small apps or teams new to Flutter. Same layering, more manual work.

```dart
class DeviceListController extends ChangeNotifier {
  DeviceListController(this._repository);

  final DeviceRepository _repository;
  DeviceListState _state = const DeviceListState();
  bool _isLoading = false;
  bool _disposed = false;

  DeviceListState get state => _state;
  bool get isLoading => _isLoading;

  Future<void> load() async {
    _isLoading = true;
    notifyListeners();
    try {
      final devices = await _repository.fetchDevices();
      _state = _state.copyWith(devices: devices);
    } on DeviceException {
      _state = _state.copyWith(userMessage: () => UserMessage.refreshFailed);
    } finally {
      _isLoading = false;
      if (!_disposed) notifyListeners();
    }
  }

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }
}

// Wiring
ChangeNotifierProvider(
  create: (context) => DeviceListController(context.read<DeviceRepository>())..load(),
  child: const DeviceListScreen(),
);

// In build: context.watch<DeviceListController>().state
// In callbacks: context.read<DeviceListController>().load()
```

- `notifyListeners()` after `dispose()` throws, so async methods guard it.
- Test it as a plain Dart object: construct with a fake, call `load()`, assert `state`.
