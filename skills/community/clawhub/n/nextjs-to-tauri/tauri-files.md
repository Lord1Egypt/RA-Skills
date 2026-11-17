# `src-tauri/` templates

Copy-paste, then replace `<placeholders>`. The `2` / `^2` ranges below keep this playbook on Tauri 2; the lockfiles pin resolved versions. Follow SKILL.md to select compatible stable 2.x releases, rather than copying a higher upstream major into these templates.

---

## `tauri.conf.json`

`mainBinaryName` (no spaces) gives a clean portable-exe filename while `productName` stays the display name. `webviewInstallMode: downloadBootstrapper/silent` auto-installs WebView2. For a build without auto-update, apply the cross-file checklist below rather than removing only the config block.

Choose the WebView2 deployment mode for the target environment. `downloadBootstrapper` requires network access during installation; `offlineInstaller` bundles the runtime installer; `skip` makes an existing runtime a prerequisite. Silent modes may install the runtime without an interactive prompt. Bundling avoids the download, not the runtime installation.

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
        "url": "/<default-locale>/",
        "dragDropEnabled": false,
        "width": 1280,
        "height": 832,
        "minWidth": 720,
        "minHeight": 480,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "security": {
      "csp": {
        "default-src": "'self'",
        "script-src": "'self'",
        "style-src": "'self' 'unsafe-inline'",
        "img-src": "'self' asset: http://asset.localhost data: blob:",
        "font-src": "'self' data:",
        "connect-src": "'self' ipc: http://ipc.localhost",
        "object-src": "'none'",
        "base-uri": "'self'"
      }
    }
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

The production CSP starts with bundled resources and Tauri IPC; Tauri adds hashes/nonces for bundled scripts at compile time. Inline styles support the sample UI library. Add only the application's actual remote origins, workers or WebAssembly requirements and verify the packaged app; do not replace the policy with `null` to hide a blocked resource. See [Tauri CSP](https://v2.tauri.app/security/csp/).

- `url` — the app's **default locale directory**, e.g. `"/en/"` when the default locale is `en` (single-locale apps: `"/"`). It is a configurable value, not a fixed locale: point it at whichever locale the app should start in and keep it in sync with the app's `DEFAULT_LOCALE` (frontend-integration.md) — the app opens there until the user picks another language. Why a trailing slash: SKILL.md gotcha #1.
- `dragDropEnabled: false` enables the frontend HTML5 drop zone on Windows. With the default value, the webview handles file drops before frontend handlers receive them. Applications without a frontend drop zone can retain the Tauri default.

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
tauri-plugin-process = "2"
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

## Linux EGL 与 AppImage 兼容性

`EGL_BAD_ALLOC` 不一定是前端路由故障。先在目标机器区分两类原因：

- **WebKit DMABUF**：确认 `WEBKIT_DISABLE_DMABUF_RENDERER=1` 在 Builder 初始化前生效后是否恢复；只在受影响环境采用，并尊重已有环境设置。
- **AppImage 库冲突**：若错误仍在，对隔离的解包副本测试去掉 bundled `libwayland-*` 后能否恢复。确认原因后再选择构建时排除冲突库，或采用下方示例的一次性宿主库 preload；架构、库路径和重启 sentinel 都需验证。

不要把禁用全部 compositing 当作通用修复，它会改变渲染路径，也不能解决动态库冲突。默认模板不设置 `WEBKIT_*`。确认 DMABUF 故障后可在启动环境设置 `WEBKIT_DISABLE_DMABUF_RENDERER=1`；确认 AppImage 库冲突后，用 `APP_USE_SYSTEM_WAYLAND=1` 显式启用下方 helper。helper 只选择当前 CPU 架构的宿主库，并用 sentinel 避免重启循环。

来源：[Tauri EGL issue](https://github.com/tauri-apps/tauri/issues/9394)、[AppImage 兼容案例](https://github.com/espressif/idf-im-ui/issues/755)、[宿主库 preload 实现](https://github.com/refactoringhq/tolaria/commit/8c286a4856637d662f05428f679faa4aee607c66)。

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

// Optional AppImage workaround: enabled only by APP_USE_SYSTEM_WAYLAND=1
// after reproducing a bundled Wayland/host-library conflict (gotcha #12).
#[cfg(target_os = "linux")]
fn ensure_system_libwayland() {
    use std::os::unix::process::CommandExt;
    use std::path::Path;

    if std::env::var("APP_USE_SYSTEM_WAYLAND").ok().as_deref() != Some("1")
        || std::env::var_os("APPIMAGE").is_none()
    {
        return; // explicit opt-in, only inside an AppImage
    }
    if std::env::var_os("APP_LIBWAYLAND_REEXEC").is_some() {
        return; // already re-exec'd — avoid an infinite loop
    }

    let candidates: &[&str] = match std::env::consts::ARCH {
        "x86_64" => &[
            "/usr/lib/x86_64-linux-gnu/libwayland-client.so.0",
            "/lib/x86_64-linux-gnu/libwayland-client.so.0",
            "/usr/lib64/libwayland-client.so.0",
        ],
        "aarch64" => &[
            "/usr/lib/aarch64-linux-gnu/libwayland-client.so.0",
            "/lib/aarch64-linux-gnu/libwayland-client.so.0",
            "/usr/lib64/libwayland-client.so.0",
        ],
        _ => return,
    };
    let Some(sys_lib) = candidates.iter().copied().find(|p| Path::new(p).exists()) else {
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

    // Leave WebKit renderer settings unchanged by default. Diagnose Linux failures
    // before setting WEBKIT_DISABLE_DMABUF_RENDERER in the launch environment.

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
        .plugin(tauri_plugin_process::init())
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
  "permissions": ["core:default", "opener:default", "updater:default", "process:allow-restart"]
}
```

---

## `update-version.cjs`

Single source of truth = root `package.json` version. Run `yarn update-version` before building (CI does this).

The `.cjs` extension runs this helper as CommonJS in both CommonJS and ESM projects.
For an existing `src-tauri/update-version.js`, rename it to `.cjs` and update the
`update-version` npm script. Workflow calls to `yarn update-version` stay valid.

The helper updates `src-tauri/tauri.conf.json`'s version from the project `package.json` and preserves other fields. Run it as part of the authorized project migration and include its result in the normal diff review.

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

`package.json` scripts to add: `"tauri": "tauri"`, `"update-version": "node src-tauri/update-version.cjs"`, and `"build:tauri": "cross-env TAURI_BUILD=1 next build"` (the flag that turns on `trailingSlash` — gotcha #1; `yarn add -D cross-env`).

## Updater signing keys

Read only when shipping updates. Reuse the existing key and client trust chain; generate a new key only for an unconfigured application:
```bash
yarn tauri signer generate --ci -p "" -w src-tauri/app.key   # private key — gitignore it, NEVER commit (gotcha #7)
cat src-tauri/app.key.pub   # paste this base64 into tauri.conf.json plugins.updater.pubkey
```
> **Signing secrets the release workflow needs:** the private key has to be stored as a
> repository secret named `TAURI_SIGNING_PRIVATE_KEY` (plus
> `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` when the key has a password). Without them the CI
> signing step fails and **no updater artifacts are produced**. The private key file
> itself must never be committed.
>
> Do **not** add `-f` to `signer generate`: it force-overwrites an existing key file,
> which would invalidate the key already published in `plugins.updater.pubkey`.
>
> Set the secrets when credentials and authorization are available; otherwise hand off the exact missing setup:
```bash
gh secret set TAURI_SIGNING_PRIVATE_KEY < src-tauri/app.key   # bash / Git Bash
# only if you generated the key WITH a password (not `-p ""`):
gh secret set TAURI_SIGNING_PRIVATE_KEY_PASSWORD
```
**PowerShell** has no `<` redirection — pipe instead:
```powershell
Get-Content src-tauri/app.key -Raw | gh secret set TAURI_SIGNING_PRIVATE_KEY
```
Manual path: repo → Settings → Secrets and variables → Actions → New repository secret.

## Optional updater: keep the layers consistent

If updates are not part of the product, remove the updater/process JS dependencies, hooks and mount calls; matching Cargo dependencies and Rust plugin registrations; `updater:default` / `process:allow-restart` permissions; and `plugins.updater` / `bundle.createUpdaterArtifacts`. Keep any process API still used by other features.

The supplied tag workflow expects signed updater artifacts and verifies `latest.json`. A no-updater build must also drop those signing inputs and feed-specific verification, while retaining tests, package/version checks and checksums for its actual assets. Manual build-only runs do not create a release. Do not remove a published updater endpoint from an existing application without considering installed clients.

## `.gitignore` (gotcha #3)

```
src-tauri/target
src-tauri/gen/schemas
# the private signing key only; its .pub half is public and meant to be committed (gotcha #7)
src-tauri/*.key
```
