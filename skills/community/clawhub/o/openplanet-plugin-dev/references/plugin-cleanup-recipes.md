# Plugin cleanup & visibility — command recipes (MP4)

## Folder layout facts (verified this session)
- Openplanet reads `Openplanet4/Plugins/` AND `Openplanet4/Plugins-Developer/` at boot.
- `Plugins-Developer/` = separate "Developer" section, NOT in the standard F3 menu.
- `Plugins-Archive/` = skipped entirely by Openplanet (use to disable without deleting).
- Same plugin in both `Plugins/` and `Plugins-Developer/` -> loads TWICE.

## Backup before any bulk move
```bash
cd /c/Users/tomekdot/Openplanet4
mkdir -p "backup-$(date +%Y%m%d-%H%M)"
cp -r Plugins "backup-$(date +%Y%m%d-%H%M)/Plugins"
cp -r Plugins-Developer "backup-$(date +%Y%m%d-%H%M)/Plugins-Developer"
```

## Merge Plugins-Developer -> Plugins (keep name if not already present)
```bash
cd /c/Users/tomekdot/Openplanet4
for d in Plugins-Developer/*/; do
  name=$(basename "$d")
  [ ! -d "Plugins/$name" ] && mv -f "$d" "Plugins/$name"
done
```

## Archive all red (TM2020-only) plugins at once
```bash
cd /c/Users/tomekdot/Openplanet4
mkdir -p Plugins-Archive
for p in TrackGeneratorExtended pursuit-plus-new green-split-dev pursuit-plus \
         drift-bar-dev rounds-tracker-dev pomodoro-plugin-dev aperion-galaxy-dev \
         pursuit-companion-dev player-stats green-timer; do
  [ -d "Plugins/$p" ] && mv -f "Plugins/$p" "Plugins-Archive/$p"
done
```

## Disable gotchas (what does NOT work)
- `info.toml [meta] disabled = true` -> IGNORED, plugin still loads.
- `Settings.ini Plugin_<name>=false` -> IGNORED for folder plugins (only .op zips
  with a site ID respect it). Appending `=false` lines to Settings.ini does nothing
  for folder plugins -- verified: they still loaded with 30+ ERR.
- WORKS: move folder to `Plugins-Archive/`, OR toggle off in-game (F3 -> Plugins)
  which writes `Plugins-<name>=false` into `Openplanet4.json`.

## Verify clean panel (after kill + relaunch)
```bash
grep "ERR :" Openplanet.log | grep -oP "Plugins/[^/]+/" | sort | uniq -c | sort -rn
# empty output = all clean
```

## Brace balance check (after editing void-returning UI calls)
```bash
python -c "s=open('Main.as',encoding='utf-8').read();print(s.count('{'),s.count('}'))"
# must be equal; use `python` (python3 is NOT installed here)
```

### Template: ui-window-template.as

```angelscript
// ============================================================================
// Plugin Template — Bare minimum Openplanet plugin with UI window
// ============================================================================

// ============================================================================
// SETTINGS — appear in Openplanet → Settings → Plugin Name
// ============================================================================

[Setting name="Show window" description="Toggle the main window"]
bool S_ShowWindow = true;

[Setting name="Window X"]
float S_WindowX = 0.0f;

[Setting name="Window Y"]
float S_WindowY = 0.0f;

// ============================================================================
// MAIN — entry point, runs on yield loop
// ============================================================================

void Main() {
    print("Plugin loaded!");
    while (true) {
        // Periodic work here
        yield();  // REQUIRED — without this the game hangs
    }
}

// ============================================================================
// RENDERMENU — overlay menu items (called when overlay is open)
// ============================================================================

void RenderMenu() {
    if (UI::MenuItem(Icons::Clock + " My Plugin", "", S_ShowWindow)) {
        S_ShowWindow = !S_ShowWindow;
    }
}

// ============================================================================
// RENDERINTERFACE — main UI (called when overlay is open)
// ============================================================================

void RenderInterface() {
    if (!S_ShowWindow) return;

    UI::SetNextWindowPos(S_WindowX, S_WindowY, UI::Cond::Appearing);
    UI::SetNextWindowSize(300, 200, UI::Cond::FirstUseEver);

    if (!UI::Begin("My Plugin", S_ShowWindow, UI::WindowFlags::NoSavedSettings)) {
        UI::End();
        return;
    }

    // Save window position for persistence
    vec2 pos = UI::GetWindowPos();
    S_WindowX = pos.x;
    S_WindowY = pos.y;

    // --- Content ---
    UI::Text("Hello from Openplanet!");
    UI::TextColored(vec4(0.3f, 1.0f, 0.5f, 1.0f), "Plugin is running.");
    UI::TextDisabled("Frame: " + tostring(Time::FrameCount));

    UI::Separator();

    if (UI::Button("Click me", vec2(100, 30))) {
        print("Button clicked!");
    }

    UI::End();
}

// ============================================================================
// CALLBACKS — optional
// ============================================================================

void OnEnabled() {
    print("Plugin enabled!");
}

void OnDisabled() {
    print("Plugin disabled!");
}
```

### Template: plugin-skeleton.as

```angelscript
// ============================================================================
// Minimal Openplanet Plugin Skeleton
// Copy this to Openplanet4/Plugins/<your-plugin>/Main.as
// ============================================================================

// --- Settings ---
[Setting name="Show window on start"]
bool S_ShowOnStart = true;

// --- State ---
bool S_WindowOpen = false;

void Main() {
    S_WindowOpen = S_ShowOnStart;
    while (true) {
        // Main loop — update state, fetch data, etc.
        yield(); // Required — allows other callbacks to fire
    }
}

void RenderMenu() {
    if (UI::MenuItem(Icons::Star + " My Plugin", "", S_WindowOpen)) {
        S_WindowOpen = !S_WindowOpen;
    }
}

void RenderInterface() {
    if (!S_WindowOpen) return;

    UI::SetNextWindowPos(100, 100, UI::Cond::Appearing);
    UI::SetNextWindowSize(300, 0, UI::Cond::FirstUseEver);

    if (!UI::Begin("My Plugin", S_WindowOpen, UI::WindowFlags::NoSavedSettings)) {
        UI::End();
        return;
    }

    UI::Text("Hello from My Plugin!");
    UI::TextDisabled("Version 1.0.0");
    UI::Separator();

    if (UI::Button("Click me")) {
        print("Button clicked!");
    }

    UI::End();
}
```

---

## Validation Notes (lessons learned — for Hermes agent)

What this agent learned while building, debugging, and consolidating Openplanet plugins on this machine:

- **`execute_code` runs NATIVE Windows Python, not MSYS.** Cygwin-style paths like `/c/Users/...` fail with `FileNotFoundError`. Always use `C:/Users/...` (drive letter + forward slashes) or `r"C:\Users\..."` in `execute_code`. (Terminal commands use git-bash, which DOES translate `/c/`, so the two contexts disagree — never copy a `/c/` path from a terminal command into an `execute_code` script.)
- **`cp -r src dst` NESTS when `dst` already exists.** Copying into an existing skill directory created `openplanet-plugin-dev/openplanet-plugin-dev/`, leaving a stale 1715-line `SKILL.md` on top. Always `rm -rf dst` before copying, or copy the *contents*. (Hit during the AppData mirror step.)
- **MoA reference-provider key error (`Provider 'moa' is set in config.yaml but no API key was found`) exhausts reference calls mid-session.** Don't depend on MoA/Gemini references mid-session; fall back to local tool evidence (`terminal`, `read_file`, `diff`) as the source of truth.
- **ManiaPlanet 4 (MP4) has a stricter ManiaScript API than TM2020.** The same `.op` compiles on one game and fails on the other — verify per game.
- **Validate plugins without stealing focus:** grep `Openplanet.log` for `ERR :` + `Plugins/<name>/` (should be empty), `laggy` (should be empty), and the plugin's `TRAC` load line.
- **cua-driver `bring_to_front` raises z-order but does NOT steal keyboard focus.** The in-game reload loop on MP4 is F3 (Openplanet overlay) → Ctrl+Shift+R.
- **Deep TM2020 plugins (e.g. pomodoro, apeiron-galaxy) may be red or laggy on MP4.** Check them individually; archive the ones you don't need.

*Last updated: 2026-07-08. v2.3.1 — inlines all `references/` and `templates/` files into a single SKILL.md (no external file dependencies). Retains MP4 supplement, Grid Explorer & Tracker v2.9.3, and ChatBot RAG v1.4.1 patterns.*
