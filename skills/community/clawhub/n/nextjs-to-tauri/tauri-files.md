# `src-tauri/` templates

Copy-paste, then replace `<placeholders>`. Pin versions to whatever the "verify latest" step in SKILL.md reports — the numbers here were current 2026-06 and **will** drift.

---

## `tauri.conf.json`

`mainBinaryName` (no spaces) gives a clean portable-exe filename while `productName` stays the display name. `webviewInstallMode: downloadBootstrapper/silent` auto-installs WebView2. Drop the `plugins.updater` block (and `createUpdaterArtifacts`) if you don't ship auto-update.

```json
{
  "$schema": "../node_modules/@tauri-apps/cli/config.schema.json",
  "productName": "<App Title>",
  "mainBinaryName": "<AppName>",
  "version": "0.1.0",
  "identifier": "com.<owner>.<app>",
  "build": {
    "frontendDist": "../out",
    "devUrl": "http://localhost:3000",
    "beforeDevCommand": "yarn dev",
    "beforeBuildCommand": "yarn build:tauri"
  },
  "app": {
    "windows": [
      {
        "label": "main",
        "title": "<App Title>",
        "url": "/en/",
        "width": 1280,
        "height": 832,
        "minWidth": 720,
        "minHeight": 480,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "security": { "csp": null }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "createUpdaterArtifacts": true,
    "category": "Productivity",
    "shortDescription": "<one line>",
    "longDescription": "<a sentence or two>",
    "icon": ["icons/32x32.png", "icons/128x128.png", "icons/128x128@2x.png", "icons/icon.icns", "icons/icon.ico"],
    "windows": {
      "webviewInstallMode": { "type": "downloadBootstrapper", "silent": true }
    }
  },
  "plugins": {
    "updater": {
      "endpoints": ["https://github.com/<owner>/<repo>/releases/latest/download/latest.json"],
      "pubkey": "<contents of src-tauri/app.key.pub>"
    }
  }
}
```

- `url: "/en/"` — set to your default locale dir (single-locale apps: `"/"`). Why a trailing slash: SKILL.md gotcha #1.

---

## `Cargo.toml` (`[dependencies]` + profile)

Single-instance is desktop-only, so target-gate it. `tray-icon` feature is required for the system tray. The release profile shrinks the binary.

```toml
[dependencies]
serde_json = "1.0"
serde = { version = "1.0", features = ["derive"] }
log = "0.4"
tauri = { version = "2", features = ["tray-icon"] }
tauri-plugin-log = "2"
tauri-plugin-opener = "2"
tauri-plugin-updater = "2"
tauri-plugin-window-state = "2"

[target.'cfg(not(any(target_os = "android", target_os = "ios")))'.dependencies]
tauri-plugin-single-instance = "2"

[profile.release]
codegen-units = 1
lto = true
opt-level = "s"
panic = "abort"
strip = true
```

Also fill in the `[package]` `description` / `authors` / `license` / `repository` (the scaffold leaves placeholders).

---

## `src/lib.rs`

Single-instance registered **first** (gotcha #5). Tray + single-instance gated to `#[cfg(desktop)]`. Drop any plugin/block you don't need.

```rust
use tauri::Manager;

#[cfg(desktop)]
fn focus_main_window(app: &tauri::AppHandle) {
    if let Some(window) = app.get_webview_window("main") {
        let _ = window.show();
        let _ = window.unminimize();
        let _ = window.set_focus();
    }
}

// Layer-B fix (gotcha #12): AppImages prepend their own libwayland-*.so to the
// loader path. On rolling distros (Manjaro/Arch/CachyOS) the host's newer
// Mesa/libEGL is loaded but forced to use the bundled (older) libwayland symbols
// — an ABI mismatch that aborts at EGL display init (EGL_BAD_ALLOC) BELOW WebKit,
// where no WEBKIT_* var can reach. Re-exec once with the host libwayland-client
// in LD_PRELOAD so the loader overrides the stale bundled copy. AppImage-only;
// .deb/.rpm already use system libs. (yaak / tolaria do the same.)
#[cfg(target_os = "linux")]
fn ensure_system_libwayland() {
    use std::os::unix::process::CommandExt;
    use std::path::Path;

    if std::env::var_os("APPIMAGE").is_none() {
        return; // only inside an AppImage
    }
    if std::env::var_os("APP_LIBWAYLAND_REEXEC").is_some() {
        return; // already re-exec'd — avoid an infinite loop
    }

    const CANDIDATES: &[&str] = &[
        "/usr/lib/x86_64-linux-gnu/libwayland-client.so.0",
        "/usr/lib64/libwayland-client.so.0",
        "/usr/lib/libwayland-client.so.0",
        "/lib/x86_64-linux-gnu/libwayland-client.so.0",
    ];
    let Some(sys_lib) = CANDIDATES.iter().copied().find(|p| Path::new(p).exists()) else {
        return; // no host libwayland to preload; run as-is
    };

    let preload = match std::env::var_os("LD_PRELOAD") {
        Some(existing) if !existing.is_empty() => {
            format!("{}:{}", sys_lib, existing.to_string_lossy())
        }
        _ => sys_lib.to_string(),
    };
    let exe = match std::env::current_exe() {
        Ok(p) => p,
        Err(_) => return,
    };
    // exec() replaces the process on success; only returns on failure.
    let err = std::process::Command::new(exe)
        .args(std::env::args_os().skip(1))
        .env("LD_PRELOAD", preload)
        .env("APP_LIBWAYLAND_REEXEC", "1")
        .exec();
    eprintln!("libwayland re-exec failed: {err}");
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Must run before any GTK/WebView init so LD_PRELOAD is in place post-re-exec.
    #[cfg(target_os = "linux")]
    ensure_system_libwayland();

    // WebKitGTK's DMABUF renderer crashes with EGL_BAD_ALLOC on many Linux GPU/
    // driver combos (VMs, hybrid graphics, NVIDIA). Force the non-DMABUF renderer
    // BEFORE any GTK/WebView init — only if the user hasn't set it, to respect
    // their/the distro's preference. GPU-buffer SHARING only — still accelerated,
    // near-zero cost. (gotcha #12, layer A)
    //
    // Do NOT also default WEBKIT_DISABLE_COMPOSITING_MODE=1 to chase a *persisting*
    // EGL line — that's the layer-B libwayland clash (handled above), and forcing
    // software rendering there only degrades the UI without fixing it.
    #[cfg(target_os = "linux")]
    if std::env::var_os("WEBKIT_DISABLE_DMABUF_RENDERER").is_none() {
        std::env::set_var("WEBKIT_DISABLE_DMABUF_RENDERER", "1");
    }

    let mut builder = tauri::Builder::default();

    #[cfg(desktop)]
    {
        builder = builder.plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            focus_main_window(app);
        }));
    }

    builder
        .plugin(tauri_plugin_window_state::Builder::default().build())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }

            #[cfg(desktop)]
            {
                use tauri::menu::{MenuBuilder, MenuItemBuilder};
                use tauri::tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent};

                let show = MenuItemBuilder::with_id("show", "Show").build(app)?;
                let quit = MenuItemBuilder::with_id("quit", "Quit").build(app)?;
                let menu = MenuBuilder::new(app).items(&[&show, &quit]).build()?;

                TrayIconBuilder::with_id("main-tray")
                    .icon(app.default_window_icon().unwrap().clone())
                    .tooltip("<App Title>")
                    .menu(&menu)
                    .show_menu_on_left_click(false)
                    .on_menu_event(|app, event| match event.id().as_ref() {
                        "show" => focus_main_window(app),
                        "quit" => app.exit(0),
                        _ => {}
                    })
                    .on_tray_icon_event(|tray, event| {
                        if let TrayIconEvent::Click {
                            button: MouseButton::Left,
                            button_state: MouseButtonState::Up,
                            ..
                        } = event
                        {
                            focus_main_window(tray.app_handle());
                        }
                    })
                    .build(app)?;
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

## `capabilities/default.json`

Only frontend→Rust IPC needs permissions. Rust-only plugins (window-state, single-instance, tray) need none here.

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "enables the default permissions",
  "windows": ["main"],
  "permissions": ["core:default", "opener:default", "updater:default"]
}
```

---

## `update-version.js`

Single source of truth = root `package.json` version. Run `yarn update-version` before building (CI does this).

```js
/* eslint-disable @typescript-eslint/no-require-imports */
const fs = require("fs");
const path = require("path");
const pkg = JSON.parse(fs.readFileSync(path.resolve(__dirname, "../package.json"), "utf8"));
const confPath = path.resolve(__dirname, "tauri.conf.json");
const conf = JSON.parse(fs.readFileSync(confPath, "utf8"));
conf.version = pkg.version;
fs.writeFileSync(confPath, JSON.stringify(conf, null, 2) + "\n", "utf8");
console.log(`Updated tauri.conf.json version -> ${pkg.version}`);
```

`package.json` scripts to add: `"tauri": "tauri"`, `"update-version": "node src-tauri/update-version.js"`, and `"build:tauri": "cross-env TAURI_BUILD=1 next build"` (the flag that turns on `trailingSlash` — gotcha #1; `yarn add -D cross-env`).

## `.gitignore` (gotcha #3)

```
src-tauri/target
src-tauri/gen/schemas
src-tauri/*.key
src-tauri/*.key.pub
```
