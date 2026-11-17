---
name: modelselector-openclaw
description: "Use when the OpenClaw Control UI chat model picker is one long flat provider-grouped list and picking a model is slow, when you have many providers each with many models, when the user wants a two-column provider/model picker (left = provider navigation, right = only that provider's models), when the per-chat account row (e.g. deepseek:default) should be hidden, or when a previously installed picker enhancement disappeared after an upgrade. Installs, repairs, verifies or uninstalls a browser-side enhancement injected into the Control UI's index.html."
license: MIT
compatibility: "Any host that loads a standard SKILL.md and can run PowerShell 5.1+ (or pwsh): DeepSeek Harness (dsh), OpenClaw, Claude Code, Cursor, Dify, Ollama, custom agents. Target is the OpenClaw Control UI web app (browser side). Windows recommended - npm global path auto-detection is built in; -Dist covers non-standard layouts."
allowed-tools: Bash Read Write
metadata:
  author: "Pondsi"
  version: "1.6.0"
  attribution: "Pondsi - attribution is mandatory for any use, including modified variants"
  license: "MIT"
---

# ModelSelectorOpenClaw

## English

**Pick the right model in two clicks, even with dozens of providers and hundreds of models.**

The OpenClaw Control UI renders its model picker as one long flat list, grouped by
provider. With many providers — each carrying many models — finding a model means a lot
of scrolling and eyeballing. This skill turns that list into a **two-column master-detail
picker with a provider navigation column**:

```
┌─────────────┬────────────────────────────────┐
│ All         │  [ search ]                     │
│ ▸ DeepSeek  │  deepseek-v4-flash              │
│ ▸ Qwen      │  deepseek-v4-pro                │
│ ▸ GLM       │  deepseek-reasoner              │
│ ▸ Mistral   │  … only this provider's models  │
└─────────────┴────────────────────────────────┘
```

- **Left column = provider navigation.** Click a provider, the right column shows only
  that provider's models. Auto-follows the provider of the model currently in use.
- **Right column = that provider's models only**, in its own scroll container. The two
  columns scroll independently (structural CSS Grid, not absolute positioning hacks).
- **Hides the official per-chat account row** (`.chat-model-account`, e.g.
  `deepseek:default`) inside the menu — it is unrelated to picking a provider/model.
- **Theme-accurate**: uses official design tokens (`--bg-hover`, `--accent`, `--border`),
  so dark / light / custom themes follow automatically.
- **Zero self-excitation**: every DOM write is state-gated; no mutation loops.
- **Responsive**: the provider column narrows with `clamp(84px, 26%, 132px)`; the native
  flat list is used only below 340px viewport width. The official search filter keeps the
  two-column layout and simply hides provider groups with no visible match.
- **Resizable with a remembered size**: a grip in the bottom-right corner resizes the picker
  horizontally **and** vertically (min 360×220, clamped to the viewport); the size is saved
  to `localStorage` and restored on the next open, and a double-click on the grip resets it.
  Long model names also carry a hover tooltip.
- **Instance-safe**: if the app mounts several pickers (main chat, side/session views,
  cached views), only the rendered one is enhanced — a hidden sibling can never steal it.
- **Self-healing**: the stylesheet is re-injected if the document loses it, and a
  state-gated 1-second heartbeat re-runs the pass, so any silent loss recovers within a
  second.
- **Self-updating**: an already-open tab notices server-side updates by itself and reloads
  (never downgrades, never interrupts typing), so a patched install never looks stale.

> ## Disclosure (Intended Behavior)
>
> This skill patches the local OpenClaw installation. By design it performs exactly these
> local file operations inside the OpenClaw package directory
> (`<npm-global>/node_modules/openclaw/dist/control-ui/`):
>
> | Operation | Scope control |
> |-----------|---------------|
> | Append/replace ONE `<script>` line at the end of `index.html` | first run saves `index.html.bak-pcl` next to it; idempotent; `-Remove` reverts |
> | Copy `pcl-model-picker.v8.js` into `assets/` | versioned filename + content fingerprint in the URL |
> | Delete older `pcl-model-picker.v*.js` files | keeps the latest TWO versions, deletes only files matching `pcl-model-picker.v*.js` |
> | Poll `./` (same-origin app shell) every 5 min for update detection | browser-side only; same-origin `fetch('./',{cache:'no-store'})`; no external host, no telemetry |
>
> Nothing else is touched: no packaged JS/CSS/SW files are modified, no external network
> access, no telemetry. The injected script runs in the **browser** only, on the model picker
> DOM; its only network call is a **same-origin** `fetch('./')` (cache: no-store) used to
> notice server-side updates and reload the tab — no external host is contacted and no data
> leaves the machine.
> The patch is lost when OpenClaw is upgraded (npm overwrites `dist/`); re-run to restore.
> **Installing means accepting these local file modifications.**

## Install

Run the patch script from this skill's `scripts/` directory:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/pcl-patch.ps1
```

- The script auto-detects the Control UI directory (npm root -g, common prefixes, or the
  `openclaw` CLI on PATH). Non-standard layout: pass `-Dist "<...>\dist\control-ui"`.
- Done when it prints `[PCL] 完成` / `Done` plus the injected tag line.
- Then reload the Control UI tab once (**F5 is enough**). From this version on, later patches
  are picked up automatically: the injected script polls the app shell and reloads the tab
  when the server is newer (never downgrades, never interrupts typing).
- Verify: open the chat model picker — provider chips on the left, that provider's models
  on the right, no account row above the list.

## Verify in one line

In the Control UI browser console:

```js
window.pclModelPickerDiag()
```

Returns `{version, selfFp, innerWidth, stylePresent, storedSize, heartbeats, lastEvent, pickers, menus, instances[]}`.
`instances[]` reports each picker instance (`state`, `twoCol`, `filtering`, `rendered`, `rail`,
`chips`). `state` is `two-col` when active, `two-col-filtering` while the official search
filter is on (layout stays two-column), `fallback-narrow` below 340px.
The document also carries `<html data-pcl-model-picker="v8">`.
Self-heal events: `window.pclModelPickerLog()`. To force an update check:
`await window.pclModelPickerCheckUpdate()`.

## After an OpenClaw upgrade

npm overwrites `dist/control-ui/`, so the tag and the asset disappear. Re-run the same
command; it is idempotent and re-injects. Done when the script reports the tag replaced.

The GitHub repository additionally ships an optional Windows auto-repair watchdog
(`platform/pcl-watchdog.ps1`) that detects this wipe and re-runs the installer on a
schedule. It is **not** part of this ClawHub artifact.

## Uninstall

```powershell
powershell -ExecutionPolicy Bypass -File scripts/pcl-patch.ps1 -Remove
```

Removes the tag from `index.html` and all `pcl-model-picker.v*.js` assets. The backup
`index.html.bak-pcl` stays on disk for reference.

## Cache rule (do not violate)

Control UI's Service Worker is **cache-first for `/assets/`** and the HTTP response is
`immutable`. The installer therefore puts a content fingerprint in the injected URL
(`./assets/pcl-model-picker.v8.js?h=<sha256-8>`) and bumps the filename on content changes.
If you edit the JS yourself, re-run `pcl-patch.ps1` (it recomputes the fingerprint) or rename
the file to the next version. Since 1.2.0 a missed reload is self-healing: open tabs detect
the newer build and reload themselves.

## Troubleshooting

- **Picker looks default again after it worked**: check `window.pclModelPickerDiag()`.
  `stylePresent: false` or a `lastEvent` of `style-injected` means the document had lost the
  stylesheet and the heartbeat just restored it. `state: "fallback-narrow"` means the
  viewport is below 340px (zoom/high DPI/split view). If `instances[]` shows a rendered
  instance with `twoCol: false` for more than a second, the script is not running — re-run
  the patch script. If the server was patched but the tab is old, the tab reloads itself
  within ~5 minutes (or run `await window.pclModelPickerCheckUpdate()`).
- **Only one of two open composers is enhanced**: expected. Only the rendered picker is
  enhanced; a hidden composer's picker is skipped until it is shown.
- **Enhancement gone after an OpenClaw upgrade**: npm restored the stock `index.html`.
  Re-run the patch script, then reload.
- **Layout changes did not apply after editing the JS**: the fingerprint/version rule above
  was skipped; re-run `pcl-patch.ps1`.
- **Script cannot find the Control UI**: pass `-Dist` explicitly. On Linux/macOS use pwsh
  and the POSIX candidate paths (already built in).
- **Restock check**: `Select-String pcl-model-picker <dist>\index.html` should show exactly
  one `<script defer src="./assets/pcl-model-picker.v7.js?h=…">` line.

## Files

- `scripts/pcl-patch.ps1` — idempotent installer/remover (auto-detects the install dir)
- `scripts/pcl-model-picker.v8.js` — the browser-side enhancement (IIFE, no dependencies)

MIT License with mandatory attribution — credit **Pondsi**. See [LICENSE](LICENSE).

---

## 简体中文

（概要 —— 安装 / 验证 / 卸载命令与 **English** 节完全一致，不再重复）

把 Control UI 聊天输入框的模型选择器，从官方「按供应商分组的扁平长列表」升级为
「**左列供应商导航 + 右列仅显示该供应商模型**」的双列 master-detail 布局，并隐藏菜单内与
选模型无关的「此聊天使用的账户」行。纯浏览器端增强：只向 `index.html` 注入一行 `<script>`
并新增一个独立 JS 文件，随时可一键卸载。

- **可拉伸 + 记住尺寸**（v1.5.0）：拖右下角手柄即可左右 + 上下调整菜单大小，尺寸记住、
  下次打开自动恢复；双击手柄复位。
- **长模型名可读**：悬停显示完整名称，拉宽即可一眼看全。
- 两列各自独立滚动（结构性 CSS Grid）；主题跟随官方设计 token；所有 DOM 写操作带状态门控，零自激。
- 样式自愈 + 1 秒心跳；已打开的页面会自动感知服务端更新并重载（不降级、不打断输入）。

## 繁體中文

（摘要 —— 安裝 / 驗證 / 卸載指令與 **English** 節完全相同，不再重複）

將 Control UI 聊天輸入框的模型選擇器，從官方「依供應商分組的扁平長清單」升級為
「**左欄供應商導覽 + 右欄僅顯示該供應商模型**」的兩欄 master-detail 版面，並隱藏選單內與
選模型無關的「此聊天使用的帳號」列。純瀏覽器端增強，可一鍵卸載。

- **可拉伸 + 記住尺寸**（v1.5.0）：拖右下角控點即可左右 + 上下調整大小，尺寸記住、
  下次開啟自動回復；雙擊控點復位。
- 名稱過長時以滑鼠懸停顯示完整名稱。
- 兩欄各自獨立捲動；主題跟隨官方設計 token；零自激。

## 한국어

(요약 — 설치/확인/제거 명령은 **English** 절과 완전히 동일하며 반복하지 않습니다)

Control UI 채팅 입력란의 모델 선택기를 공식 「공급자별로 묶인 평면 목록」에서
「**왼쪽 열 = 공급자 탐색 + 오른쪽 열 = 해당 공급자의 모델만**」 2열 master-detail
레이아웃으로 바꾸고, 모델 선택과 무관한 「이 대화에서 사용하는 계정」 행을 숨깁니다.
브라우저 측 향상만 하며 언제든 제거할 수 있습니다.

- **크기 조절 + 크기 기억**(v1.5.0): 오른쪽 아래 손잡이를 끌어 가로·세로로 조절하며,
  크기가 기억되어 다음에 열 때 복원됩니다(손잡이 두 번 클릭 = 기본값).
- 이름이 긴 모델은 마우스를 올리면 전체 이름이 표시됩니다.
- 두 열은 각각 독립적으로 스크롤되고, 테마는 공식 디자인 토큰을 따르며, DOM 쓰기는 상태 게이트로 억제됩니다.

## Русский

(кратко — команды установки/проверки/удаления идентичны разделу **English**)

Превращает выбор модели в Control UI из официального «плоского списка, сгруппированного по
провайдерам» в двухколоночный master-detail макет «**слева — навигация по провайдерам,
справа — только модели выбранного провайдера**» и скрывает служебную строку «аккаунт для
этого чата». Это чисто браузерное улучшение, удаляется одной командой.

- **Изменяемый размер с запоминанием** (v1.5.0): потяните ручку в правом нижнем углу,
  чтобы менять ширину и высоту; размер запоминается и восстанавливается при следующем
  открытии (двойной щелчок по ручке — сброс).
- Длинные имена моделей показываются полностью при наведении.
- Колонки прокручиваются независимо; тема следует официальным токенам; запись в DOM подавлена.

## 日本語

（要旨 —— インストール / 検証 / アンインストールのコマンドは **English** 節と同一です）

Control UI のチャット入力欄のモデル選択を、公式の「プロバイダー別に並んだ平坦なリスト」から
「**左列＝プロバイダー移動 / 右列＝そのプロバイダーのモデルのみ**」の 2 列 master-detail
レイアウトに変え、モデル選択と無関係な「このチャットで使用するアカウント」行を非表示にします。
ブラウザー側のみの拡張で、いつでもワンコマンドで削除できます。

- **サイズ変更＋サイズ記憶**（v1.5.0）：右下のグリップをドラッグして左右・上下にサイズ変更でき、
  次回開いたときに復元されます（グリップをダブルクリックでリセット）。
- 長いモデル名はホバーで全体を表示します。
- 2 列は独立してスクロールし、テーマは公式デザイントークンに追従、DOM 書き込みは状態ゲートで抑制。

## Español

(Resumen — los comandos de instalación/verificación/desinstalación son idénticos a la sección **English**)

Convierte el selector de modelos del chat de Control UI, de la «lista plana agrupada por
proveedor» oficial, en un diseño master-detail de dos columnas: «**izquierda = navegación por
proveedor, derecha = solo los modelos de ese proveedor**», y oculta la fila «cuenta usada en
este chat». Es una mejora puramente del navegador; se desinstala con un comando.

- **Redimensionable y recordado** (v1.5.0): arrastra el tirador de la esquina inferior derecha
  para cambiar ancho y alto; el tamaño se guarda y se restaura al volver a abrir (doble clic
  en el tirador = restablecer).
- Los nombres largos se muestran completos al pasar el cursor.
- Las columnas se desplazan de forma independiente; el tema sigue los tokens oficiales.

## Français

(Résumé — les commandes d'installation/vérification/désinstallation sont identiques à la section **English**)

Transforme le sélecteur de modèles du chat de Control UI, de la « liste plate groupée par
fournisseur » officielle, en une disposition maître-détail à deux colonnes : « **gauche =
navigation par fournisseur, droite = uniquement ses modèles** », et masque la ligne « compte
utilisé dans ce chat ». Amélioration purement côté navigateur, désinstallable en une commande.

- **Redimensionnable et mémorisé** (v1.5.0) : faites glisser la poignée en bas à droite pour
  régler largeur et hauteur ; la taille est mémorisée et restaurée à la prochaine ouverture
  (double-clic sur la poignée = réinitialiser).
- Les noms longs s'affichent en entier au survol.
- Les colonnes défilent indépendamment ; le thème suit les tokens officiels.

---

Pondsi (+MiMo-v2.5 +deepseek-v4.1-flash-expires-on-0910 +GLM5.3-flash) — automatically committed by OpenClaw
