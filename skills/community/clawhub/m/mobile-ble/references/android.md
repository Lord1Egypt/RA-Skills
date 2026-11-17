# Android BLE

Load this for any Kotlin or Java BLE code on Android. Facts below were checked against the
developer.android.com reference and behaviour-change pages; re-check them when `targetSdk` moves.

## Permissions by API level

| API level | Scan | Connect, read, write | Notes |
|---|---|---|---|
| 31 and higher | `BLUETOOTH_SCAN` (runtime) | `BLUETOOTH_CONNECT` (runtime) | `neverForLocation` removes the location need; some beacons are filtered |
| 29-30 | `ACCESS_FINE_LOCATION` + `BLUETOOTH_ADMIN` | `BLUETOOTH` | Background scanning from a service also needs `ACCESS_BACKGROUND_LOCATION` |
| 28 and lower | `ACCESS_COARSE_LOCATION` or fine + `BLUETOOTH_ADMIN` | `BLUETOOTH` | |

- `BLUETOOTH_ADVERTISE` only if the phone advertises (peripheral role).
- `startScan` returns no results without the location permission on API 30 and lower, with no error.
- `<uses-feature android:name="android.hardware.bluetooth_le" android:required="false"/>` keeps the app
  installable on devices without BLE; then check `PackageManager.FEATURE_BLUETOOTH_LE` at runtime.

```kotlin
private val blePermissions: Array<String> =
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
    } else {
        arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
    }

private val launcher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { result ->
    viewModel.onPermissionsResult(granted = result.values.all { it })
}

fun requestBle() = launcher.launch(blePermissions)
```

Bluetooth off is a separate state. Ask the user to enable it with `BluetoothAdapter.ACTION_REQUEST_ENABLE`
(needs `BLUETOOTH_CONNECT` on API 31+), and listen for `BluetoothAdapter.ACTION_STATE_CHANGED`.

## Scanning

```kotlin
class Scanner(private val adapter: BluetoothAdapter, private val scope: CoroutineScope) {
    @RequiresPermission(Manifest.permission.BLUETOOTH_SCAN)
    fun scan(service: UUID, timeout: Duration = 10.seconds): Flow<ScanResult> = callbackFlow {
        val scanner = adapter.bluetoothLeScanner ?: run { close(BluetoothOffException()); return@callbackFlow }
        val cb = object : ScanCallback() {
            override fun onScanResult(callbackType: Int, result: ScanResult) { trySend(result) }
            override fun onScanFailed(errorCode: Int) { close(ScanFailedException(errorCode)) }
        }
        val filters = listOf(ScanFilter.Builder().setServiceUuid(ParcelUuid(service)).build())
        val settings = ScanSettings.Builder().setScanMode(ScanSettings.SCAN_MODE_BALANCED).build()
        scanner.startScan(filters, settings, cb)
        val timer = scope.launch { delay(timeout); close() }
        awaitClose { timer.cancel(); scanner.stopScan(cb) }
    }
}
```

- `getBluetoothLeScanner()` returns null while Bluetooth is off.
- Scan modes: `SCAN_MODE_LOW_POWER` (default, and forced when the app is not in the foreground),
  `SCAN_MODE_BALANCED`, `SCAN_MODE_LOW_LATENCY` (foreground only), `SCAN_MODE_OPPORTUNISTIC`.
- `onScanFailed` codes include `SCAN_FAILED_ALREADY_STARTED` (1) and `SCAN_FAILED_SCANNING_TOO_FREQUENTLY` (6).
  Throttling can also show up as a scan that simply returns nothing. The limit is not documented; the widely
  reported figure is five starts in 30 seconds. Debounce user-triggered rescans.
- Process not running: `startScan(filters, settings, pendingIntent)` delivers results through the
  `PendingIntent` with `EXTRA_LIST_SCAN_RESULT`. The peripheral must be advertising. From a receiver, start
  short work with WorkManager; Android 12+ blocks starting a foreground service from the background.

## The GATT operation queue

```kotlin
sealed interface GattResult {
    data class Ok(val value: ByteArray = ByteArray(0)) : GattResult
    data class Error(val status: Int) : GattResult
    data object NotStarted : GattResult
    data object Timeout : GattResult
}

class GattQueue {
    private val mutex = Mutex()
    private val pending = AtomicReference<CompletableDeferred<GattResult>?>(null)

    // start() issues the platform call and returns true if it was accepted.
    suspend fun run(timeout: Duration, start: () -> Boolean): GattResult = mutex.withLock {
        val deferred = CompletableDeferred<GattResult>()
        pending.set(deferred)
        try {
            if (!start()) return GattResult.NotStarted
            withTimeoutOrNull(timeout) { deferred.await() } ?: GattResult.Timeout
        } finally {
            pending.set(null)
        }
    }

    // Called from the binder thread by BluetoothGattCallback.
    fun complete(result: GattResult) { pending.get()?.complete(result) }
}
```

```kotlin
private val callback = object : BluetoothGattCallback() {
    override fun onCharacteristicWrite(g: BluetoothGatt, c: BluetoothGattCharacteristic, status: Int) =
        queue.complete(if (status == BluetoothGatt.GATT_SUCCESS) GattResult.Ok() else GattResult.Error(status))

    override fun onCharacteristicRead(g: BluetoothGatt, c: BluetoothGattCharacteristic, value: ByteArray, status: Int) =
        queue.complete(if (status == BluetoothGatt.GATT_SUCCESS) GattResult.Ok(value.copyOf()) else GattResult.Error(status))

    override fun onDescriptorWrite(g: BluetoothGatt, d: BluetoothGattDescriptor, status: Int) =
        queue.complete(if (status == BluetoothGatt.GATT_SUCCESS) GattResult.Ok() else GattResult.Error(status))

    override fun onMtuChanged(g: BluetoothGatt, mtu: Int, status: Int) {
        if (status == BluetoothGatt.GATT_SUCCESS) negotiatedMtu.set(mtu)   // AtomicInteger, default 23
        queue.complete(if (status == BluetoothGatt.GATT_SUCCESS) GattResult.Ok() else GattResult.Error(status))
    }

    override fun onServicesDiscovered(g: BluetoothGatt, status: Int) =
        queue.complete(if (status == BluetoothGatt.GATT_SUCCESS) GattResult.Ok() else GattResult.Error(status))
}
```

- A disconnect must fail the pending operation: call `queue.complete(GattResult.Error(status))` from
  `onConnectionStateChange` before closing, so the caller does not wait for the timeout.
- Timeouts: 5-10 s for reads and writes and 15-30 s for service discovery are common starting points.
  Agree values with the firmware team; a slow device is a protocol fact, not a guess.
- Never call the next GATT method from inside a callback directly. Return to the queue.

## Android 13+ signatures (API 33)

| Deprecated in 33 | Use instead |
|---|---|
| `boolean writeCharacteristic(c)` | `int writeCharacteristic(c, byte[] value, int writeType)` returning `BluetoothStatusCodes` |
| `boolean writeDescriptor(d)` | `int writeDescriptor(d, byte[] value)` |
| `onCharacteristicChanged(gatt, c)` | `onCharacteristicChanged(gatt, c, byte[] value)` |
| `onCharacteristicRead(gatt, c, status)` | `onCharacteristicRead(gatt, c, byte[] value, int status)` |
| `onDescriptorRead(gatt, d, status)` | `onDescriptorRead(gatt, d, int status, byte[] value)` |

Return values of the new write: `SUCCESS`, `ERROR_MISSING_BLUETOOTH_CONNECT_PERMISSION`,
`ERROR_PROFILE_SERVICE_NOT_BOUND`, `ERROR_GATT_WRITE_NOT_ALLOWED`, `ERROR_GATT_WRITE_REQUEST_BUSY` (201),
`ERROR_UNKNOWN`.

```kotlin
// Enable notifications: local flag plus the CCCD write on the peripheral
@RequiresPermission(Manifest.permission.BLUETOOTH_CONNECT)
suspend fun enableNotifications(c: BluetoothGattCharacteristic): GattResult {
    if (!gatt.setCharacteristicNotification(c, true)) return GattResult.NotStarted
    val cccd = c.getDescriptor(CCCD_UUID) ?: return GattResult.NotStarted   // 00002902-0000-1000-8000-00805f9b34fb
    val value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
    return queue.run(5.seconds) {
        if (Build.VERSION.SDK_INT >= 33) {
            gatt.writeDescriptor(cccd, value) == BluetoothStatusCodes.SUCCESS
        } else {
            @Suppress("DEPRECATION") run { cccd.value = value; gatt.writeDescriptor(cccd) }
        }
    }
}
```

Use `ENABLE_INDICATION_VALUE` for indications. Notifications are not queued operations once enabled, but
the CCCD write is.

## Threading

- With `connectGatt(context, autoConnect, callback, transport)` callbacks run on an unspecified
  background thread (binder). The overload with a `Handler` lets you choose; API 37 adds an `Executor`.
- Pick one serial context to own link state, for example `Dispatchers.Default.limitedParallelism(1)` or a
  `HandlerThread`. Push callback data into a `Channel` and process it there.
- Copy byte arrays from callbacks before handing them off (`value.copyOf()`).
- `MutableStateFlow` is safe to update from any thread, but read-modify-write sequences are not; use
  `update { }` or the serial context.

## Connecting, closing and status 133

```kotlin
@RequiresPermission(Manifest.permission.BLUETOOTH_CONNECT)
fun open(device: BluetoothDevice, auto: Boolean): BluetoothGatt =
    if (Build.VERSION.SDK_INT >= 37) {
        // API 37: build BluetoothGattConnectionSettings (check the builder API for your compileSdk)
        device.connectGatt(settingsFor(auto), executor, callback)
    } else {
        @Suppress("DEPRECATION")
        device.connectGatt(context, auto, callback, BluetoothDevice.TRANSPORT_LE)
    }
```

- Always pass `TRANSPORT_LE` for BLE peripherals; dual-mode phones otherwise may try classic first.
- `connectGatt` returns a new client. Exactly one live `BluetoothGatt` per device; close the old one first.
- Status values in `onConnectionStateChange`: `GATT_SUCCESS` (0), `GATT_INSUFFICIENT_AUTHENTICATION` (5),
  `GATT_INSUFFICIENT_ENCRYPTION` (15), `GATT_CONNECTION_CONGESTED` (143), `GATT_CONNECTION_TIMEOUT` (147, API 35),
  `GATT_FAILURE` (257). 133 (0x85) and other values outside this list are stack or controller codes with no
  public constant. Log the
  number; do not map it to a user message beyond "could not connect".
- Retry policy for 133 and other connect failures: `close()`, wait with exponential backoff (for example
  1, 2, 4, 8 s, cap 30 s), retry up to a limit, then report failure and stop.
- Too many open clients exhaust the stack. Close on every path: disconnect, failure, timeout, scope cancel.

```kotlin
class DeviceLink(...) : AutoCloseable {
    override fun close() {
        queue.complete(GattResult.Error(-1))
        gatt?.disconnect()
        gatt?.close()
        gatt = null
    }
}
```

## autoConnect

- `autoConnect = false`: direct connect, fails if the device is absent, no automatic reconnect. Use for the
  first, user-initiated connection.
- `autoConnect = true`: the stack reconnects when the device is available again, including after a
  peripheral-initiated disconnect or loss of range. Slower to establish. Use for known devices.
- Below Android 10 only one connection request runs at a time; from Android 10 requests are batched.
- The connection is closed if the process is killed. Reconnect after restart from a service or CDM event.

## MTU, connection priority, PHY

- `requestMtu(517)` once, after connecting and before heavy traffic. From Android 14 the stack requests 517
  on the first request from any client and ignores later requests. Use the `mtu` in `onMtuChanged`.
- Payload per write or notification is `mtu - 3`.
- `requestConnectionPriority(CONNECTION_PRIORITY_HIGH)` for bulk transfer such as DFU, then
  `CONNECTION_PRIORITY_BALANCED`. `CONNECTION_PRIORITY_LOW_POWER` for idle links. `CONNECTION_PRIORITY_DCK`
  (API 34) is for digital car keys only.
- `setPreferredPhy` (2M PHY) can speed up transfers if both sides support it; result in `onPhyUpdate`.

## Bonding

- Many peripherals trigger bonding themselves when a protected characteristic is accessed
  (`GATT_INSUFFICIENT_AUTHENTICATION` or `_ENCRYPTION`). Prefer that to calling `createBond()` blindly.
- `createBond()` is asynchronous. Listen for `BluetoothDevice.ACTION_BOND_STATE_CHANGED` and `EXTRA_BOND_STATE`
  (`BOND_BONDING`, `BOND_BONDED`, `BOND_NONE`). Queue no GATT work while `BOND_BONDING`.
- Android 16: when a bonded device cannot be authenticated on reconnect, the system disconnects, keeps the
  bond and shows a dialog. Apps targeting 16 can receive `ACTION_KEY_MISSING` and `ACTION_ENCRYPTION_CHANGE`.
  OEM behaviour varies; keep the older bond-loss handling when `ACTION_KEY_MISSING` is not broadcast.
- Android 16: `CompanionDeviceManager.removeBond(int)` removes the bond for a CDM-associated device.
- Android 17: the system may re-pair automatically after bond loss. `ACTION_PAIRING_REQUEST` carries
  `EXTRA_PAIRING_CONTEXT`, and `ACTION_KEY_MISSING` is sent only if automatic re-pairing fails.
- `BluetoothDevice.setPin` is deprecated in API 37 and needs `BLUETOOTH_PRIVILEGED` for apps targeting 37.

## Background and foreground services

- Android 12+: no foreground service start from the background except listed exemptions, one of which is
  an app using Companion Device Manager that declares `REQUEST_COMPANION_START_FOREGROUND_SERVICES_FROM_BACKGROUND`
  (preferred) or `REQUEST_COMPANION_RUN_IN_BACKGROUND`.
- Android 14+: declare `android:foregroundServiceType="connectedDevice"` and `FOREGROUND_SERVICE_CONNECTED_DEVICE`.
  The runtime prerequisite is one of: a granted `BLUETOOTH_CONNECT`, `BLUETOOTH_ADVERTISE` or `BLUETOOTH_SCAN`
  (or the other options listed for this type, such as `CHANGE_NETWORK_STATE`).
- Android 15: `connectedDevice` is not in the list of types a `BOOT_COMPLETED` receiver may not launch
  (that list is `dataSync`, `camera`, `mediaPlayback`, `phoneCall`, `mediaProjection`, `microphone`).
  The 6-hour limit applies to `dataSync` and `mediaProcessing`, not to `connectedDevice`.
- Android 16: jobs that run while a foreground service is running now count against the job runtime quota.
  Do not rely on WorkManager running long while your BLE service is up.

```kotlin
class DeviceLinkService : LifecycleService() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        super.onStartCommand(intent, flags, startId)
        ServiceCompat.startForeground(
            this, NOTIFICATION_ID, buildNotification(),
            ServiceInfo.FOREGROUND_SERVICE_TYPE_CONNECTED_DEVICE,
        )
        return START_STICKY
    }
}
```

Start it from a visible activity (for example when the user taps "Connect"), not from a BLE callback.

## Companion Device Manager

- `associate(AssociationRequest, Executor, Callback)` shows a system picker; the user selects the device.
- `startObservingDevicePresence(ObservingDevicePresenceRequest)` (API 36; the `String` address overload,
  API 31, is deprecated in 36) wakes your `CompanionDeviceService` when the device comes in or out of range.
  Requires `REQUEST_OBSERVE_COMPANION_DEVICE_PRESENCE`.
- Limits from the docs: limited filtering and no support for random MAC addresses. Peripherals with rotating
  addresses should use a Resolvable Private Address and be bonded so the OS can resolve it.
- Android 16: the app no longer gets `RESULT_DISCOVERY_TIMEOUT`; the user sees a dialog and the app receives
  `RESULT_USER_REJECTED` when it is dismissed.

## Logging

- `BluetoothDevice.getAddress()` is a stable identifier on Android. Redact it in logs (`AA:BB:..:EF`) and do
  not send it to analytics.
- Use a debug-only HCI snoop log (Developer options) for packet-level debugging, never production logging.
