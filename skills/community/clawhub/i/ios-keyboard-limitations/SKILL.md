---
name: ios-keyboard-limitations
description: iOS keyboard extension technical limitations and workarounds. Use when planning or building iOS custom keyboards with voice/audio features, dictation, or system integration needs. Covers memory limits, sandbox restrictions, microphone access, app launching, and viable alternative architectures.
---

# iOS Keyboard Extension Limitations

When building iOS custom keyboards with voice/audio features, these are the hard limitations discovered through the PolyVoice project.

## 🔴 Hard Limitations (Cannot be worked around)

### 1. Microphone Access — DISALLOWED
**Keyboard extensions cannot access the microphone.**

- `AVAudioRecorder` will fail with permission error
- `SFSpeechRecognizer` is unavailable
- No Siri integration from keyboard context

**Why:** Apple security model — keyboards run in sandbox and could keylog audio.

### 2. Open Other Apps — BLOCKED
**Keyboards cannot programmatically open the main app or any other app.**

- `UIApplication.shared.open()` returns false
- URL schemes don't work (`myapp://`)
- ` ExtensionContext.open()` not available

**Why:** Prevents malicious keyboards from launching apps without user consent.

### 3. Memory Limit — ~50MB
**Keyboard extensions have strict memory limits (~30-60MB).**

- App terminated silently if exceeded
- No crash log, just disappears
- Heavy audio processing = instant death

**Mitigation:**
- Record at 16kHz mono (not 44.1kHz)
- Use 32kbps bitrate max
- Immediate file cleanup after processing
- 60-second max recording hard limit

### 4. No Persistent Storage
**UserDefaults unavailable, only App Groups.**

- Standard `UserDefaults` doesn't persist
- Must use `UserDefaults(suiteName: "group.com.company.app")`
- Requires App Group capability in both targets

### 5. Network Requires "Full Access"
**API calls fail without user enabling "Allow Full Access" in Settings.**

- User must explicitly enable: Settings → General → Keyboard → [Keyboard Name] → Allow Full Access
- Most users won't do this
- Cannot prompt or explain from keyboard UI effectively

## 🟡 Partial Workarounds (User friction)

### The "Open App" Workaround
**Goal:** Let user tap a button to open main app for recording.

**Attempt:**
```swift
// This does NOT work
extensionContext?.open(URL(string: "myapp://record")!)
```

**Reality:** Must use `UIApplication.shared.open()` outside extension context, but keyboards can't call this.

### The Manual Switch Pattern
**What actually works (with friction):**

1. **User taps button in keyboard** → Shows alert: "Open PolyVoice to record?"
2. **User manually switches to main app** (Home button, swipe, etc.)
3. **Main app detects active session** (via App Groups / shared state)
4. **Main app auto-records** on appear
5. **Auto-stops on silence** (2 seconds)
6. **Auto-copies** to clipboard
7. **User manually switches back** to target app
8. **Keyboard auto-pastes** on reappear

**User flow:**
```
Keyboard → Tap mic → [Manual: Switch to app] → App auto-records → 
[Manual: Switch back] → Keyboard auto-pastes
```

**Friction points:**
- Two manual app switches
- Context switching breaks flow
- Users forget to return
- Clipboard may be overwritten

## 🟢 Alternative Architectures

### Option 1: Share Extension (Better for Audio)
**Use Share Sheet instead of keyboard.**

- Full app capabilities
- Can record audio
- Can process and return text

**Limitation:** Not a keyboard — user must open share sheet per text field.

### Option 2: Full App Mode
**Don't use keyboard extension — use main app only.**

- User opens app
- Records dictation
- Copies result
- Switches to target app
- Pastes manually

**Benefit:** No memory limits, full mic access, reliable.  
**Cost:** More friction than keyboard.

### Option 3: Siri Shortcuts Integration
**Provide Siri Shortcuts for voice-to-text.**

- "Hey Siri, dictate with PolyVoice"
- Returns text to current app
- Fully supported by Apple

**Limitation:** Not instant, requires Siri setup.

## 📊 Decision Matrix

| Approach | Mic Access | Memory | User Friction | Apple Approved |
|----------|-----------|---------|---------------|----------------|
| Keyboard extension | ❌ No | ⚠️ 50MB | Low (if no audio) | ✅ Yes |
| Keyboard + audio workaround | ❌ No | ⚠️ 50MB | 🔴 High | ✅ Yes |
| Share extension | ✅ Yes | ✅ Full | 🟡 Medium | ✅ Yes |
| Full app only | ✅ Yes | ✅ Full | 🟡 Medium | ✅ Yes |
| Siri Shortcuts | ✅ Yes | ✅ Full | 🟡 Medium | ✅ Yes |

## 🎯 Recommendation

**For voice dictation/AI transcription:**

1. **Don't build a keyboard extension** — the limitations make it frustrating
2. **Use Share Extension** — Apple-supported, full capabilities
3. **Or full app** — simplest to build, most reliable
4. **Add Shortcuts** — for power users who want speed

**For non-audio keyboards (emoji, translation, etc.):**

Keyboard extension works great. Just avoid audio features.

## 📚 References

- Apple's official docs: https://developer.apple.com/documentation/uikit/keyboards_and_input/creating_a_custom_keyboard
- Custom Keyboard Programming Guide (WWDC sessions)
- PolyVoice project learnings (~/Projects/polyvoice-keyboard/)
