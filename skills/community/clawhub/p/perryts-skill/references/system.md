# System APIs

## Overview

```typescript
import { openURL, isDarkMode, getDeviceIdiom, getDeviceModel } from 'perry/system'
import { preferencesSet, preferencesGet } from 'perry/system'
import { keychainSave, keychainGet, keychainDelete } from 'perry/system'
import { notificationSend, notificationOnTap } from 'perry/system'
import { audioStart, audioStop, audioGetLevel } from 'perry/system'
```

## openURL

```typescript
openURL("https://perryts.com")
openURL("mailto:hello@perryts.com")
openURL("tel:+1234567890")
```

Platform: macOS (`NSWorkspace`), iOS (`UIApplication.shared.open`), Android (`Intent.ACTION_VIEW`), GTK4 (`gtk_show_uri`), Windows (`ShellExecute`).

## isDarkMode

```typescript
if (isDarkMode()) {
  // apply dark theme
}
```

Returns `boolean`. Listens to system appearance changes.

## getDeviceIdiom / getDeviceModel

```typescript
const idiom = getDeviceIdiom()    // "phone", "tablet", "desktop", "tv", "watch"
const model = getDeviceModel()    // "iPhone15,2", "Pixel 8", etc.
```

## Preferences (Key-Value Storage)

```typescript
preferencesSet("theme", "dark")
const theme = preferencesGet("theme")  // "dark"
```

| Platform | Storage |
|----------|---------|
| macOS/iOS | NSUserDefaults |
| Android | SharedPreferences |
| Windows | Registry |
| Linux | GSettings |

## Keychain (Secure Storage)

```typescript
await keychainSave("api_token", "secret123")
const token = await keychainGet("api_token")
await keychainDelete("api_token")
```

| Platform | Storage |
|----------|---------|
| macOS/iOS | Keychain Services |
| Android | Android Keystore |
| Windows | Credential Manager |
| Linux | libsecret |

## Notifications

### Local Notifications
```typescript
notificationSend("New message", "You have 3 unread messages")
notificationOnTap((data) => {
  console.log("Notification tapped:", data)
})
notificationCancel(id)
```

### Push Notifications
```typescript
import { notificationRegisterForPush } from 'perry/system'
const deviceToken = await notificationRegisterForPush()
```

Platform support: APNs (iOS/macOS), Firebase Cloud Messaging (Android).

| Platform | Local | Push |
|----------|-------|------|
| macOS | NSUserNotificationCenter | APNs |
| iOS | UNUserNotificationCenter | APNs |
| Android | NotificationCompat | FCM |
| Windows | ToastNotification | — |
| Linux | libnotify | — |

## Audio Capture

```typescript
audioStart()                           // Start capturing
const level = audioGetLevel()          // A-weighted dB level
const peak = audioGetPeak()            // Peak level
const waveform = audioGetWaveform(128) // 128 sample waveform
audioStop()                            // Stop capturing
```

48kHz mono capture. A-weighted dB metering.

| Platform | Backend |
|----------|---------|
| macOS/iOS | AVAudioEngine |
| Android | AudioRecord |
| Linux | PulseAudio |
| Windows | WASAPI |
| Web | getUserMedia |

## Media Playback

```typescript
import { createPlayer, play, pause, stop, seek, setVolume, setRate,
         getCurrentTime, getDuration, getState, isPlaying,
         onStateChange, onTimeUpdate, setNowPlaying, destroy } from 'perry/media'

const player = createPlayer()
await play(player, "https://example.com/song.mp3")

onStateChange(player, (state) => console.log("State:", state))  // Loading/Ready/Playing/Paused/Ended/Error
onTimeUpdate(player, (time) => console.log("Time:", time))

setNowPlaying(player, {
  title: "My Song",
  artist: "Perry",
  album: "Greatest Hits",
  artwork: "https://example.com/art.jpg"
})
```

### MediaState Enum
`Idle`, `Loading`, `Ready`, `Playing`, `Paused`, `Ended`, `Error`

### Platform Implementations

| Platform | Player | Now Playing |
|----------|--------|-------------|
| macOS/iOS/tvOS/visionOS | AVPlayer | MPNowPlayingInfoCenter + MPRemoteCommandCenter |
| Android | MediaPlayer + MediaSessionCompat | Lock screen, Bluetooth, Android Auto |
| Linux | GStreamer playbin | MPRIS D-Bus |
| Windows | WinRT MediaPlayer | SystemMediaTransportControls |
| watchOS | AVPlayer | Now Playing complication |
| HarmonyOS | AVPlayer (NAPI) | — |
| Web | `<audio>` | Media Session API |

### Belt-and-braces Ended Detection
Both the native end-of-playback event AND `currentTime ≥ duration - 0.25s` fallback fire the `Ended` state — handles cases where the native event drops.

## Clipboard

```typescript
import { clipboardGet, clipboardSet } from 'perry/ui'
clipboardSet("Hello")
const text = clipboardGet()
```

## Environment Variables

```bash
PERRY_RUNTIME_DIR     # Override runtime library search path
PERRY_LIB_DIR         # Override library directory
PERRY_GEN_GC          # GC mode: "0"/"off"/"false" = full mark-sweep
PERRY_GC_DIAG         # Print per-cycle GC diagnostics
PERRY_WRITE_BARRIERS  # Enable codegen-emitted write barriers
PERRY_HARMONYOS_P12   # Path to .p12 keystore (HarmonyOS signing)
PERRY_HARMONYOS_CERT  # Path to cert file (HarmonyOS signing)
```
