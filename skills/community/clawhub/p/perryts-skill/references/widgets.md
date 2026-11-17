# Widgets (Home Screen)

## Overview

`Widget()` declarations compile to platform-native home screen widgets:
- **iOS**: WidgetKit extensions
- **Android**: App Widgets (BroadcastReceiver + RemoteViews)
- **watchOS**: Complications
- **Wear OS**: Tiles

```typescript
import { Widget, Text, VStack, HStack } from 'perry/ui'
```

## Build Targets

```bash
perry compile src/widget.ts --target ios-widget -o MyWidget
perry compile src/widget.ts --target android-widget -o MyWidget
perry compile src/widget.ts --target watchos-widget -o MyWidget
perry compile src/widget.ts --target wearos-tile -o MyTile
```

## Widget Declaration

```typescript
Widget({
  kind: "com.example.weather",
  displayName: "Weather",
  description: "Current weather conditions",
  entryFields: [
    { name: "city", type: "string", defaultValue: "San Francisco" },
    { name: "unit", type: "string", defaultValue: "celsius" }
  ],
  render: (entry) => VStack([
    Text(entry.city),
    Text(`${entry.temperature}°`)
  ]),
  config: {
    backgroundColor: { r: 0.1, g: 0.1, b: 0.2, a: 1 }
  }
})
```

## Entry Fields

```typescript
entryFields: [
  { name: "title", type: "string", defaultValue: "Hello" },
  { name: "count", type: "number", defaultValue: 0 },
  { name: "enabled", type: "boolean", defaultValue: true },
  { name: "items", type: "array", defaultValue: [] },
  { name: "nested", type: "object", properties: [ /* ... */ ] },
  { name: "optional", type: "string", optional: true }
]
```

## Conditional Rendering

```typescript
render: (entry) => {
  if (entry.count > 0) {
    return VStack([Text(`${entry.count} items`)])
  }
  return VStack([Text("No items")])
}
```

## Timeline Provider

```typescript
Widget({
  kind: "com.example.calendar",
  // ...
  provider: () => {
    const now = new Date()
    return {
      date: now,
      // Return timeline entries for widget updates
    }
  }
})
```

## Family-Specific Rendering

```typescript
render: (entry, family) => {
  switch (family) {
    case "small":  return Text(entry.value)
    case "medium": return HStack([Text(entry.label), Text(entry.value)])
    case "large":  return VStack([Text(entry.title), /* full layout */])
  }
}
```

## Multiple Widgets

Multiple `Widget()` declarations in one file create separate platform widgets from a single source.

## Platform Notes

| Platform | Format | Refresh |
|----------|--------|---------|
| iOS | WidgetKit | Timeline-based, ~15 min minimum |
| Android | AppWidgetProvider | AlarmManager / WorkManager |
| watchOS | Complication | Timeline-based |
| Wear OS | Tile | Scheduled updates |
