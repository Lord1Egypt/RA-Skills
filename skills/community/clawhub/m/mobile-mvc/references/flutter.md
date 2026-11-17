# Flutter controller pattern

Load this when a Flutter screen keeps its logic in a `State` class, or uses `ChangeNotifier` or
`ValueNotifier` controllers. The model is the framework's own controllers (`TextEditingController`,
`ScrollController`): a plain object that holds state and logic, notifies listeners, and is owned and
disposed by a `State`.

## Before: logic in State

```dart
// BAD: networking, validation and formatting in the State; untestable without pumping widgets
class _PairingScreenState extends State<PairingScreen> {
  bool _loading = false;
  String? _error;

  Future<void> _pair(String code) async {
    if (code.length != 8) {
      setState(() => _error = 'Invalid code');
      return;
    }
    setState(() => _loading = true);
    final response = await http.post(Uri.parse('https://api.example.com/pair'), body: code);
    setState(() => _loading = false);
    if (response.statusCode != 200) setState(() => _error = 'Pairing failed');
  }
}
```

## After: controller plus thin widget

```dart
enum PairingStatus { idle, pairing, paired, failed }

class PairingController extends ChangeNotifier {
  PairingController(this._repository);

  final PairingRepository _repository;
  PairingStatus _status = PairingStatus.idle;
  String? _errorKey;
  bool _disposed = false;

  PairingStatus get status => _status;
  String? get errorKey => _errorKey;
  bool get canSubmit => _status != PairingStatus.pairing;

  static bool isValidCode(String code) => RegExp(r'^[A-Z0-9]{8}$').hasMatch(code);

  Future<void> pair(String code) async {
    if (!isValidCode(code)) {
      _set(PairingStatus.failed, 'invalidCode');
      return;
    }
    _set(PairingStatus.pairing, null);
    try {
      await _repository.pair(code);
      _set(PairingStatus.paired, null);
    } on PairingException {
      _set(PairingStatus.failed, 'pairingFailed');
    }
  }

  void _set(PairingStatus status, String? errorKey) {
    if (_disposed) return;
    _status = status;
    _errorKey = errorKey;
    notifyListeners();
  }

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }
}
```

- State is private; the widget reads getters and calls methods.
- The controller does not import `material.dart` widgets or hold a `BuildContext`. It exposes error keys
  or enums; the widget maps them to localized strings.
- `notifyListeners()` after `dispose()` throws, which is why async methods check `_disposed`.

```dart
class _PairingScreenState extends State<PairingScreen> {
  late final PairingController _controller = PairingController(widget.repository);
  final _codeField = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    _codeField.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    await _controller.pair(_codeField.text);
    if (!mounted) return;
    if (_controller.status == PairingStatus.paired) Navigator.of(context).pop(true);
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: _controller,
      builder: (context, child) => Column(
        children: [
          child!,
          if (_controller.errorKey != null) Text(localizeError(context, _controller.errorKey!)),
          FilledButton(
            onPressed: _controller.canSubmit ? _submit : null,
            child: const Text('Pair'),
          ),
        ],
      ),
      child: TextField(controller: _codeField),
    );
  }
}
```

- `ListenableBuilder` rebuilds only its builder. Static subtrees go in `child` so they are not rebuilt.
- Navigation and snack bars stay in the widget, after a `mounted` check.

## ValueNotifier for a single value

```dart
// BAD: whole screen rebuilds for a counter
setState(() => _secondsLeft--);

// GOOD
final _secondsLeft = ValueNotifier<int>(60);

ValueListenableBuilder<int>(
  valueListenable: _secondsLeft,
  builder: (context, value, _) => Text('$value s'),
)
// dispose: _secondsLeft.dispose();
```

`ValueNotifier` notifies only when the new value is not `==` to the old one. Mutating a list inside a
`ValueNotifier<List<T>>` does not notify; assign a new list.

## Ownership rules

- Whoever creates a controller disposes it. A widget that receives a controller from its parent never
  disposes it.
- Optional external controller, like `TextField`:

```dart
class DeviceList extends StatefulWidget {
  const DeviceList({super.key, this.controller});
  final DeviceListController? controller;
  @override
  State<DeviceList> createState() => _DeviceListState();
}

class _DeviceListState extends State<DeviceList> {
  DeviceListController? _internal;
  DeviceListController get _effective => widget.controller ?? (_internal ??= DeviceListController());

  @override
  void didUpdateWidget(DeviceList oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.controller != null && _internal != null) {
      _internal!.dispose();
      _internal = null;
    }
  }

  @override
  void dispose() {
    _internal?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => ListenableBuilder(
        listenable: _effective,
        builder: (context, _) => Text('${_effective.count} devices'),
      );
}
```

- Never create a controller in `build`. It is recreated on every rebuild and never disposed.
- Manual `addListener` calls have a matching `removeListener` in `dispose`, and in `didUpdateWidget`
  when the listened object changes.

## Testing controllers

Controllers are plain Dart, so they are tested with `test`, not `testWidgets`.

```dart
test('invalid code fails without calling the repository', () async {
  final repo = FakePairingRepository();
  final controller = PairingController(repo);
  var notifications = 0;
  controller.addListener(() => notifications++);

  await controller.pair('abc');

  expect(controller.status, PairingStatus.failed);
  expect(controller.errorKey, 'invalidCode');
  expect(repo.calls, 0);
  expect(notifications, 1);
});
```

## When to go further

A `ChangeNotifier` controller with an injected repository is already a small ViewModel. When several
widgets need it, or it must survive navigation, provide it through the project's state management
(provider, Riverpod, Bloc) instead of passing it by hand. See `mobile-mvvm` and `mobile-mvi`.
