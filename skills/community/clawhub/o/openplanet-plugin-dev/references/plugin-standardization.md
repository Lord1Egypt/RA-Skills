# Openplanet Plugin Standardization & Menu-Hook Hygiene

Condensed knowledge bank + workflow for bringing a batch of Openplanet plugins
to a consistent state: each gets a Trackmania menu entry (`RenderMenu`) that
toggles its main window, and no window is hidden behind a dead toggle.

> Session provenance: derived while standardizing 15 plugins
> (`maniacalendar-dev`, `chatbot-RAQ-dev`, `vehicle-detector-dev`, `chase-mode-overlay`,
> `czatsky-vehicle`, `pursuit-chatbot-dev`, `pomodoro-plugin-dev`, `grid-explorer-dev`,
> `plugin-restart`, `pursuit-suite`, `fpv`, `TM2TrackGen`, `sync-galaxy`, `sync-galaxy-dev`,
> `shadows-dev`). This is the class-level pattern; do not re-derive it per plugin.

## CRITICAL PITFALL - hook scope

Openplanet auto-hooks lifecycle functions by **name in the GLOBAL namespace only**:

- `void Main()`
- `void Render()`
- `void RenderMenu()`   <- the one most often broken
- `void RenderInterface()`
- `void OnSettingsChanged()` / `OnSettingsLoad` / `OnSettingsSave`
- `void OnEnabled()` / `OnDisabled()` / `OnDestroyed()`

These will be **silently never called** if declared:

- inside a `class { }` block (e.g. `class SocialUI { void RenderMenu(){} }`),
- **or inside a `namespace X { }` block** (e.g. `namespace TM2TG { void RenderMenu(){} }`).

A `namespace` is NOT global scope for Openplanet's hook scanner. This was hit for
real in `TM2TrackGen`: a `RenderMenu` added directly before `void RenderInterface()`
landed *inside* `namespace TM2TG`, so it never appeared in the menu.

**Fix when the plugin wraps everything in a namespace:** declare the hooks
*outside* the namespace, or add a separate global `RenderMenu()` that forwards to
the namespaced logic. Pattern that works:

```angelscript
namespace TM2TG {
    void DrawUI() { /* real UI, called by the global hook below */ }
}

bool Setting_ShowWindow = true;

// GLOBAL - Openplanet hooks this
void RenderMenu() {
    if (UI::MenuItem(Icons::Wrench + " TM2 Track Generator", "", Setting_ShowWindow)) {
        Setting_ShowWindow = !Setting_ShowWindow;
    }
}
void RenderInterface() {
    if (!Setting_Enabled || !Setting_ShowWindow) return;
    TM2TG::DrawUI();
}
```

### Hidden window behind a class member

When the only window flag is a class field (e.g. `SocialUI.showWindow`), the
menu toggle cannot live inside the class. Add a **global** bool + a **global**
`RenderMenu`, then gate the class `Render()` with the global flag:

```angelscript
SocialModule@ g_socialModule;
bool g_ShowSocialUI = true;          // GLOBAL

void RenderMenu() {                   // GLOBAL
    if (UI::MenuItem(Icons::Comments + " Toggle Pursuit Social", "", g_ShowSocialUI)) {
        g_ShowSocialUI = !g_ShowSocialUI;
    }
}
// inside class SocialUI::Render():
void Render() {
    if (!showWindow || !g_ShowSocialUI) return;   // merged gate
    ...
}
```

## Standardization workflow (batch)

For each plugin, recursive-scan `.as` for these signals and classify:

| Signal | Meaning | Action |
|---|---|---|
| `void RenderMenu()` present + `UI::MenuItem(..., flag)` toggles a bool | Already standardized | none |
| no `void RenderMenu()` | Missing menu | add global `RenderMenu()` toggling the window bool |
| `if (UI::MenuItem("...", "", false)) { }` (literal `false`, empty body) | Dead menu (toggle does nothing) | replace with a real `bool g_ShowX = true;` + `g_ShowX = !g_ShowX;` |
| window drawn unconditionally (no `if (!flag) return;` before `UI::Begin`/`UI::BeginChild`) | Hidden window | add a flag + gate `Render()` on it |
| `RenderMenu`/`Render` appears but indented / inside `class`/`namespace` | Not hooked | move to global scope |

### Scan recipe (one pass, before trusting any prior "done" claim)

```python
import os, re
base = r"C:\Users\tomekdot\Openplanet4\Plugins"
for root,_,fs in os.walk(base):
    for f in fs:
        if not f.endswith(".as"): continue
        s = open(os.path.join(root,f), encoding="utf-8", errors="replace").read()
        lines = s.splitlines()
        for i,l in enumerate(lines,1):
            if re.match(r'\s*void\s+RenderMenu\s*\(\s*\)', l):
                indent = len(l)-len(l.lstrip())
                scope = "GLOBAL-OK" if indent==0 else f"indent{indent}-BROKEN"
                # also check it is not inside 'namespace X {' / 'class X {'
```

### Verify-before-trust (MiA / prior-session context)

When the conversation arrives with other agents' "DONE" edits (mixture-of-agents
summaries, prior-compaction claims), **assume nothing persisted**. Before acting:

1. **Byte-diff working tree vs backup.** `sha256` each `.as` in both trees; only
   the files you yourself edited should differ. If a claimed edit's file is
   byte-identical to backup, it never landed.
2. **Re-grep actual file contents** for the tokens you expect, rather than
   trusting a "X lines changed" report from another agent.
3. Prefer your own `execute_code` regex scans as the single source of truth.

This caught a real situation: a prior MiA pass reported "DONE" on 15 plugins, but
the tree was byte-identical to backup - zero edits had actually persisted.

## Post-edit verification (always, before declaring done)

After programmatic multi-file edits:

```python
for rel in edited_files:
    s = open(path).read()
    assert s.count("{") - s.count("}") == 0, f"brace imbalance in {rel}"
    assert NEW_TOKEN in s, f"edit missing in {rel}"
```

- Brace balance `{}` must be `0` in every touched file (AngelScript won't parse otherwise).
- Confirm the inserted `void RenderMenu()` token and its toggled flag are present.

## Window-bool conventions seen in this batch

| Plugin | Window flag |
|---|---|
| maniacalendar-dev | `g_WindowOpen` |
| chatbot-RAQ-dev | `g_ShowChatWindow` |
| vehicle-detector-dev | `S_ShowWindow` (+ `S_ShowHudOverlay`, `S_ShowDetectionWindow`) |
| chase-mode-overlay | `S_Enabled` (also gates render) |
| czatsky-vehicle | `g_ShowWindow` (added - was hidden) |
| pursuit-chatbot-dev | `g_windowVisible` |
| pomodoro-plugin-dev | `g_showOverlay` |
| grid-explorer-dev | `S_ShowInfoWindow` |
| plugin-restart | `S_IsEnabled` |
| pursuit-suite | `g_ShowSocialUI` (added, global) |
| fpv | `S_Enabled` |
| TM2TrackGen | `Setting_ShowWindow` (needs global-hook fix - see pitfall) |
| sync-galaxy / -dev | `S_ShowWindow` |
| shadows-dev | `shadowsDisabled` |
