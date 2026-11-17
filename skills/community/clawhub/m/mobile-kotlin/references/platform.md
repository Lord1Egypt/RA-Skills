# Platform changes reference

Load this when touching Activities, window insets, back handling, services, permissions, or when the
project's `targetSdk` changes. Only behavior tied to `targetSdk` is listed; bumping it opts the app in.

For an SDK level not listed here, read the official behavior-changes page for that release before changing
code. Do not assume.

## Edge-to-edge (targetSdk 35+)

- On Android 15+ devices, apps targeting SDK 35 are drawn edge-to-edge. Status and navigation bar color APIs
  no longer have an effect.
- The `windowOptOutEdgeToEdgeEnforcement` opt-out is deprecated and ignored when targeting SDK 36. Do not rely
  on it.
- Call `enableEdgeToEdge()` in `onCreate` before `setContent` so older versions behave the same way.

Compose:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    enableEdgeToEdge()
    super.onCreate(savedInstanceState)
    setContent { AppTheme { AppRoot() } }
}

@Composable
fun SettingsScreen(modifier: Modifier = Modifier) {
    Scaffold(modifier = modifier, topBar = { TopAppBar(title = { Text("Settings") }) }) { innerPadding ->
        LazyColumn(contentPadding = innerPadding) { /* ... */ }
    }
}
```

- Material 3 `Scaffold`, `TopAppBar` and `NavigationBar` consume insets. Pass `innerPadding` to scrolling
  content as `contentPadding` so items scroll under the bars but end above them.
- Without a `Scaffold`: `Modifier.safeDrawingPadding()`, `Modifier.windowInsetsPadding(WindowInsets.safeDrawing)`,
  and `Modifier.imePadding()` for text fields above the keyboard.
- Backgrounds draw behind the bars; touch targets and text stay inside the insets.

Views:

```kotlin
ViewCompat.setOnApplyWindowInsetsListener(binding.list) { view, insets ->
    val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
    view.updatePadding(bottom = bars.bottom)
    insets
}
```

## Predictive back

- `onBackPressed()` is deprecated. For apps targeting SDK 36 on Android 16+, predictive back is on by default
  and `onBackPressed()` is no longer called, nor is `KEYCODE_BACK` dispatched.
- Compose: `BackHandler(enabled = condition) { }`. For a custom animation driven by the gesture,
  `PredictiveBackHandler { progress -> }` collects the back events.
- Views: `onBackPressedDispatcher.addCallback(owner) { }` and toggle `isEnabled` as state changes.

```kotlin
// GOOD: enabled only while there is something to intercept
BackHandler(enabled = state.hasUnsavedChanges) { showDiscardDialog = true }
```

- A callback that is always enabled breaks back-to-home. Enable it only while it has work to do.
- Navigation libraries (Navigation Compose, Navigation 3) already handle back for their back stack.

## Foreground services

- Targeting SDK 34+: every foreground service declares `android:foregroundServiceType` in the manifest,
  holds the matching `FOREGROUND_SERVICE_<TYPE>` permission, and passes the type when starting.

```kotlin
ServiceCompat.startForeground(
    this,
    NOTIFICATION_ID,
    notification,
    ServiceInfo.FOREGROUND_SERVICE_TYPE_CONNECTED_DEVICE,
)
```

- A BLE gateway service usually fits `connectedDevice`. Pick the type that matches what the service actually
  does; a wrong type is a Play policy problem, not only a crash risk.
- Targeting SDK 35+: `dataSync` and `mediaProcessing` services have a daily time limit. Implement
  `Service.onTimeout(startId, fgsType)` and stop the service there.
- Targeting SDK 35+: some types (including `dataSync`, `camera`, `microphone`, `mediaPlayback`) can no longer
  be started from a `BOOT_COMPLETED` receiver.
- Deferrable or retryable work belongs in WorkManager. Prefer it over a foreground service whenever the user
  does not need to see ongoing work.

## Large screens and orientation (targetSdk 36+)

- On displays with smallest width 600dp or more, manifest orientation, resizability and aspect-ratio
  restrictions are ignored for apps targeting SDK 36. Games are excluded.
- Code must handle any size and orientation: state in ViewModels and `rememberSaveable`, layouts adapting to
  window size classes, no hardcoded portrait assumptions in camera or scanning screens.

## Other target-dependent rules still often missed

- Runtime-registered broadcast receivers (targetSdk 34+) pass `RECEIVER_EXPORTED` or `RECEIVER_NOT_EXPORTED`.
  Use `ContextCompat.registerReceiver` for backward compatibility.
- `PendingIntent` (targetSdk 31+) must specify `FLAG_IMMUTABLE` or `FLAG_MUTABLE`. Default to immutable.
- Bluetooth (targetSdk 31+): `BLUETOOTH_SCAN` and `BLUETOOTH_CONNECT` are runtime permissions. Add
  `android:usesPermissionFlags="neverForLocation"` to `BLUETOOTH_SCAN` only if scan results are never used to
  derive location.
- Notifications (targetSdk 33+): `POST_NOTIFICATIONS` is a runtime permission. Request it in context.
- Exported components (`exported="true"`) are an attack surface. See `mobile-security`.

## Manifest and permission changes

- Every new permission, service type, or exported component is called out explicitly in the change summary.
- Request runtime permissions at the point of use with `rememberLauncherForActivityResult(
  ActivityResultContracts.RequestPermission())` or `RequestMultiplePermissions()`, and handle denial.
