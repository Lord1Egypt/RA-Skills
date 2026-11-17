# Java pattern implementations (Android)

Load this when implementing or reviewing patterns in Java Android code. Java lacks named arguments,
class delegation and (on many toolchains) pattern matching for `switch`, so some patterns that are
over-engineering in Kotlin are the right tool here. Examples use Java 17 language features that D8
desugars for all API levels (records, `instanceof` patterns, switch expressions).

## Builder (justified in Java)

```java
public final class NotificationSpec {
    private final String title;
    private final String channel;
    private final boolean silent;

    private NotificationSpec(Builder b) {
        this.title = b.title;
        this.channel = b.channel;
        this.silent = b.silent;
    }

    public static Builder builder(String title) { return new Builder(title); }

    public static final class Builder {
        private final String title;        // required values go in the builder constructor
        private String channel = "default";
        private boolean silent;

        private Builder(String title) { this.title = Objects.requireNonNull(title); }

        public Builder channel(String channel) { this.channel = channel; return this; }
        public Builder silent(boolean silent) { this.silent = silent; return this; }
        public NotificationSpec build() { return new NotificationSpec(this); }
    }
}

NotificationSpec spec = NotificationSpec.builder("Low battery").channel("alerts").build();
```

- Two or three fields: a `record` or a constructor is enough. Builders pay off with many optional fields.
- When the class moves to Kotlin, delete the builder and use default arguments plus `@JvmOverloads`
  for remaining Java callers.

## Singleton through DI (Hilt)

```java
@Singleton
public final class SessionStore {
    private final Context context;

    @Inject
    public SessionStore(@ApplicationContext Context context) { this.context = context; }
}

@Module
@InstallIn(SingletonComponent.class)
public abstract class DataModule {
    @Binds
    abstract DeviceRepository bindDeviceRepository(DefaultDeviceRepository impl);
}
```

```java
// BAD: global lazy singleton, not thread-safe, keeps whatever Context the first caller passed
public static Analytics getInstance(Context c) {
    if (instance == null) instance = new Analytics(c);
    return instance;
}
```

## Factory

```java
public final class Exporters {
    private Exporters() {}

    public static Exporter forFormat(ExportFormat format, FontProvider fonts) {
        return switch (format) {
            case PDF -> new PdfExporter(fonts);
            case CSV -> new CsvExporter(';');
        };
    }
}
```

A switch expression over an enum is exhaustive at compile time; a new enum constant breaks the build
instead of falling through silently.

## Strategy

```java
@FunctionalInterface
public interface BackoffPolicy {
    long delayMillis(int attempt);

    BackoffPolicy FIXED = attempt -> 1_000L;
    BackoffPolicy EXPONENTIAL = attempt -> 500L << Math.min(attempt, 6);
}

public final class Uploader {
    private final BackoffPolicy backoff;
    public Uploader(BackoffPolicy backoff) { this.backoff = backoff; }
}
```

Kotlin callers can pass a lambda directly because the interface has a single abstract method.

## Observer (LiveData)

```java
public final class ConnectionViewModel extends ViewModel {
    private final MutableLiveData<ConnState> state = new MutableLiveData<>(new ConnState.Disconnected());

    public LiveData<ConnState> getState() { return state; } // read-only type outward
}

// Fragment
viewModel.getState().observe(getViewLifecycleOwner(), this::render);
```

- `postValue` from background threads keeps only the latest value. Fine for state, wrong for events.

## Adapter

```java
// DTO -> domain at the data-layer edge.
final class DeviceMapper {
    private DeviceMapper() {}

    static @Nullable Device toDomain(DeviceDto dto) {
        if (dto.serial == null) return null;
        return new Device(dto.serial, dto.name != null ? dto.name : "", dto.firmware);
    }
}
```

## Decorator

```java
public final class TimedDeviceApi implements DeviceApi {
    private final DeviceApi inner;
    private final Metrics metrics;

    public TimedDeviceApi(DeviceApi inner, Metrics metrics) {
        this.inner = inner;
        this.metrics = metrics;
    }

    @Override
    public FirmwareInfo firmwareInfo(String id) throws IOException {
        long start = SystemClock.elapsedRealtime();
        try {
            return inner.firmwareInfo(id);
        } finally {
            metrics.record("firmwareInfo", SystemClock.elapsedRealtime() - start);
        }
    }

    @Override
    public List<DeviceDto> devices() throws IOException { return inner.devices(); } // manual forwarding
}
```

## State machine (connection)

```java
public interface ConnState {
    record Disconnected() implements ConnState {}
    record Connecting(int attempt) implements ConnState {}
    record Connected(int mtu) implements ConnState {}
    record Failed(ConnError error) implements ConnState {}
}

public interface ConnEvent {
    record Connect() implements ConnEvent {}
    record LinkUp(int mtu) implements ConnEvent {}
    record LinkLost(ConnError error) implements ConnEvent {}
    record Disconnect() implements ConnEvent {}
}

public final class ConnectionReducer {
    private static final int MAX_ATTEMPTS = 3;

    private ConnectionReducer() {}

    public static ConnState reduce(ConnState state, ConnEvent event) {
        if (state instanceof ConnState.Disconnected || state instanceof ConnState.Failed) {
            return event instanceof ConnEvent.Connect ? new ConnState.Connecting(1) : state;
        }
        if (state instanceof ConnState.Connecting c) {
            if (event instanceof ConnEvent.LinkUp up) return new ConnState.Connected(up.mtu());
            if (event instanceof ConnEvent.LinkLost lost) {
                return c.attempt() < MAX_ATTEMPTS ? new ConnState.Connecting(c.attempt() + 1) : new ConnState.Failed(lost.error());
            }
            if (event instanceof ConnEvent.Disconnect) return new ConnState.Disconnected();
            return state;
        }
        if (state instanceof ConnState.Connected) {
            if (event instanceof ConnEvent.LinkLost) return new ConnState.Connecting(1);
            if (event instanceof ConnEvent.Disconnect) return new ConnState.Disconnected();
            return state;
        }
        throw new IllegalStateException("Unhandled state " + state);
    }
}
```

- Records give `equals` / `hashCode`, so tests compare states directly.
- If the project's AGP and D8 support sealed types, declare `sealed interface ConnState permits ...`.
  Pattern matching for `switch` is a Java 21 feature; confirm toolchain support before using it.
- GATT callbacks arrive on binder threads. Apply events on one thread: a single-thread executor, or a
  `synchronized` method that reduces and then calls `postValue`.

## Command (serialized GATT queue)

```java
public final class GattQueue {
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private final GattExecutor executor;

    public GattQueue(GattExecutor executor) { this.executor = executor; }

    // One command at a time: executeBlocking issues the call and waits (with a timeout) for its callback.
    public Future<byte[]> submit(GattCommand command) {
        return worker.submit(() -> executor.executeBlocking(command, 5, TimeUnit.SECONDS));
    }

    public void close() { worker.shutdownNow(); }
}
```

- `executeBlocking` typically uses a `CountDownLatch` or `CompletableFuture` completed from the
  `BluetoothGattCallback`. Always wait with a timeout.
- The owner calls `close()` when the connection ends, or the worker thread leaks.

## Delegation

Java has no class delegation. Prefer composition with explicit forwarding (as in the decorator) over
extending a concrete class. For callbacks to an owner, pass a listener interface and clear it when the
owner's lifecycle ends:

```java
public void setListener(@Nullable ScanListener listener) { this.listener = listener; }

@Override public void onDestroyView() {
    scanner.setListener(null);
    super.onDestroyView();
}
```
