# Performance reference

Load this when fixing jank, slow startup, memory growth or app size, or when writing lists, images and
animations. Measure first; most "optimizations" without a profile add complexity and change nothing.

## Measure

1. Run on a real, preferably low-end, device in profile mode: `flutter run --profile`.
   Debug mode is many times slower and its numbers are meaningless.
2. Open DevTools:
   - Performance view: frame chart, UI vs raster thread time, "Track widget builds".
   - CPU profiler: hot Dart functions on the UI isolate.
   - Memory view: heap snapshots and diffs to find leaked State objects and controllers.
3. Find which thread is slow.

| Slow thread | Usual cause | Fix direction |
|---|---|---|
| UI (Dart) | Too many rebuilds, heavy `build`, sync parsing | Narrow rebuilds, `const`, isolates |
| Raster | `saveLayer` (opacity, clips, shader masks), huge images, blur | Cheaper effects, decode at size |

4. Fix one thing, re-measure, keep the change only if the numbers improved.

## Rebuild scope

```dart
// BAD: the whole screen rebuilds every second for one label
setState(() => _elapsed++);

// GOOD: only the label listens
ValueListenableBuilder<int>(
  valueListenable: _elapsed,
  builder: (context, value, _) => Text('$value s'),
)
```

- `const` widgets are skipped on rebuild. Enable `prefer_const_constructors`.
- Pass a `child` to `AnimatedBuilder`, `ValueListenableBuilder` and `Consumer` for the part that does
  not change.
- Select narrowly: `ref.watch(p.select((s) => s.count))`, `context.select((C c) => c.state.count)`.
- `MediaQuery.sizeOf(context)`, `MediaQuery.paddingOf(context)` instead of `MediaQuery.of(context)`,
  which rebuilds on any media change (keyboard, text scale, insets).

## Lists

```dart
// BAD: builds all 5 000 rows up front
ListView(children: [for (final d in devices) DeviceTile(device: d)]);

// GOOD: builds only visible rows
ListView.builder(
  itemCount: devices.length,
  itemExtent: 72, // or prototypeItem, when rows have a fixed height
  itemBuilder: (context, i) => DeviceTile(key: ValueKey(devices[i].id), device: devices[i]),
);
```

- `SliverList.builder` inside `CustomScrollView` for mixed scrolling content.
- Never `shrinkWrap: true` on a long list inside another scrollable; it lays out every child.
- Paginate network data; do not hold 10 000 models in memory to show 20.

## Images

```dart
// BAD: 4000x3000 photo decoded at full size for a 48 px avatar (about 48 MB of pixels)
Image.network(url, width: 48, height: 48);

// GOOD: decoded at display size in physical pixels
final dpr = MediaQuery.devicePixelRatioOf(context);
Image.network(url, width: 48, height: 48, cacheWidth: (48 * dpr).round());
```

- `ResizeImage` does the same for any `ImageProvider`.
- Precache hero or first-screen images with `precacheImage` when the screen is about to appear.
- Prefer vector assets or correctly sized raster variants (`2.0x`, `3.0x`) over one huge PNG.

## Animations and effects

```dart
// BAD: Opacity rebuilt every frame, saveLayer each frame
AnimatedBuilder(
  animation: _controller,
  builder: (context, _) => Opacity(opacity: _controller.value, child: const Card()),
);

// GOOD: opacity handled in the render layer, child not rebuilt
FadeTransition(opacity: _controller, child: const Card());
```

- Implicit animations (`AnimatedOpacity`, `AnimatedContainer`) for simple state changes.
- Expensive: `Opacity` on large subtrees, `ShaderMask`, `ColorFilter`, `BackdropFilter`,
  `Clip.antiAliasWithSaveLayer`. Use them on small areas.
- For a translucent image, set the colour or opacity on the image or decoration instead of wrapping it.
- `RepaintBoundary` isolates a frequently repainting widget (a progress ring, a live chart) from static
  neighbours. Add it only when DevTools shows repaints spreading; it costs memory for an extra layer.

## Work off the UI isolate

- Parse large JSON, decode files, compute hashes and run crypto in `Isolate.run`.
- Long-lived background processing (a stream of BLE packets to decode) can use a long-lived isolate with
  `Isolate.spawn` and ports. Most apps never need it.
- Avoid synchronous file I/O (`readAsStringSync`) on the UI isolate.

## Startup

- Keep `main()` small: initialize only what the first frame needs, defer the rest.
- Do not `await` analytics, remote config or non-critical SDK init before `runApp`.
- Measure with `flutter run --profile --trace-startup` and compare against the previous release.

## Memory and leaks

- Dispose controllers, cancel subscriptions and timers (see the main skill, rule 9).
- `autoDispose` providers and `BlocProvider(create:)` scope state to the screen that needs it.
- Image cache size is limited by `PaintingBinding.instance.imageCache`; raising it hides problems.
- Use DevTools memory diffs: navigate into and out of a screen several times; a growing count of its
  `State` class is a leak.

## App size

- `flutter build appbundle --analyze-size --target-platform android-arm64` (or `ipa`) and inspect in DevTools.
- Remove unused packages and fonts; subset icon fonts (tree shaking of icons is on by default in release).
- `--split-debug-info` moves symbols out of the binary; keep them for crash symbolication.

## Rendering engine

- Impeller is the default renderer on iOS and on modern Android devices; shader compilation jank warm-up
  steps written for the old Skia backend are not needed there. Check the Flutter release notes before
  copying older advice.
