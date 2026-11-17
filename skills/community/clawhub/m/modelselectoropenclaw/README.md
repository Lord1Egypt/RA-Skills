# ModelSelectorOpenClaw

**Two-column model picker for the OpenClaw Control UI — pick the right model in two clicks, even with dozens of providers and hundreds of models.**

<p>
<img alt="license" src="https://img.shields.io/badge/license-MIT-blue">
<img alt="platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20pwsh-lightgrey">
<img alt="hosts" src="https://img.shields.io/badge/hosts-dsh%20%7C%20OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-informational">
<img alt="version" src="https://img.shields.io/badge/version-1.6.0-green">
</p>

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文) | [한국어](#한국어) | [Русский](#русский) | [日本語](#日本語) | [Español](#español) | [Français](#français)

---

## English

### The problem

OpenClaw's Control UI renders its model picker as **one long flat list, grouped by
provider**. That is fine with two providers and five models. With the way real setups look
today — a local Ollama, a couple of cloud APIs, an aggregator, each carrying dozens of
models — the list becomes a scroll marathon. Every switch means scrolling past providers
you do not want, and the model you need is buried in the middle.

### What this skill does

It adds a **provider navigation column** to the picker and keeps the right side focused:

```
┌─────────────┬────────────────────────────────┐
│ All         │  [ search ]                     │
│ ▸ DeepSeek  │  deepseek-v4-flash              │
│ ▸ Qwen      │  deepseek-v4-pro                │
│ ▸ GLM       │  deepseek-reasoner              │
│ ▸ Mistral   │  … only this provider's models  │
└─────────────┴────────────────────────────────┘
```

| | Native picker | With this skill |
|---|---|---|
| Finding a model with 5 providers × 30 models | Scroll the whole flat list | Click provider → pick model |
| Provider switching | Implicit (by group heading) | Explicit left-hand navigation |
| Scroll behaviour | One long scroll | Two independent columns |
| Per-chat account row (`deepseek:default`) | Always shown in the menu | Hidden (unrelated to picking) |
| Theme | Native | Native tokens — dark/light/custom follow automatically |

### Selling points

- **Provider-first navigation.** The left column lists every provider; clicking one shows
  only that provider's models on the right. Two clicks, no hunting.
- **Scales to any number of models.** Ten providers with hundreds of models behaves the
  same as two — the right column never mixes providers.
- **Auto-follows the current model.** Open the picker and the provider of the model you are
  using is already selected and highlighted.
- **Independent scrolling.** Structural CSS Grid gives each column its own scroll container;
  no scroll coupling, no "right column scrolls first" weirdness.
- **Hides the account row.** The official per-chat account control (`deepseek:default`)
  sits in the menu but has nothing to do with choosing a model — it is hidden.
- **Theme-native.** Only official design tokens are used (`--bg-hover`, `--accent`,
  `--border`, `--scrollbar-*`), so every theme looks right with no patch feel.
- **No self-excitation.** Every DOM write is state-gated; the MutationObserver cannot loop.
- **Responsive.** The provider column narrows with `clamp(84px, 26%, 132px)`; the native
  flat list returns only below 340px viewport width or while the official search filter is
  active.
- **Resizable, size remembered.** Drag the bottom-right grip to size the picker in both
  directions; the size persists for the next open, and long model names carry a hover
  tooltip (double-click the grip to reset).
- **Self-updating.** An already-open tab notices server-side updates on its own and reloads
  (never downgrades, never interrupts typing) — a patched install never looks stale.

### Install

Run the patch script from this skill's `scripts/` directory:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/pcl-patch.ps1
```

The script auto-detects the Control UI directory (npm root -g, common prefixes, the
`openclaw` CLI on PATH). Non-standard layout: `-Dist "<...>\dist\control-ui"`.
When it prints `[PCL] 完成` / `Done`, reload the Control UI tab once and open the model
picker. After that, future patches are picked up automatically (see *Self-updating*).

### Verify

Browser console, one line:

```js
window.pclModelPickerDiag()
```

Expect a rendered instance with `state: "two-col"`, `rail: true`, `chips` = provider count + 1,
`twoCol: true`, and `stylePresent: true`.
`two-col-filtering` means the official search box is filtering (layout stays two-column);
`fallback-narrow` means the viewport is below 340px.
Self-heal events: `window.pclModelPickerLog()`. Force an update check with
`await window.pclModelPickerCheckUpdate()`.

### Uninstall

```powershell
powershell -ExecutionPolicy Bypass -File scripts/pcl-patch.ps1 -Remove
```

### Is it safe?

Yes — and the footprint is deliberately tiny:

| Operation | Scope control |
|-----------|---------------|
| Append/replace **one** `<script>` line in `index.html` | first run backs up `index.html.bak-pcl`; idempotent; `-Remove` reverts |
| Copy `pcl-model-picker.v8.js` into `assets/` | versioned filename + content fingerprint in the URL |
| Delete older `pcl-model-picker.v*.js` | keeps the newest **two**, deletes only that pattern |

- **No packaged code is modified** — no OpenClaw JS/CSS/service-worker file is touched.
- **No external network, no telemetry.** The injected script runs in your browser only; its
  only request is a **same-origin** `fetch('./')` used to detect server-side updates — no
  third party is contacted and nothing leaves the machine.
- **Scope:** the model picker's DOM/CSS. No session data, config, or credentials.
- **Reversible:** `-Remove`, or reinstall OpenClaw and the stock UI is back.
- **Lost on upgrade by design:** npm overwrites `dist/`; re-run the script to restore.

### After an OpenClaw upgrade

Re-run the same command. It is idempotent and re-injects; nothing to clean up first.

On Windows you can make this automatic: the GitHub package ships
[`platform/pcl-watchdog.ps1`](https://github.com/Pondsi/ModelSelectorOpenClaw/blob/main/platform/README.md), which detects the wipe and re-runs the
installer (scheduled task `BigLobster-PclModelPickerRepair`). The browser side then reloads
by itself, so an upgrade heals with no manual step.

### Which package should I install?

| | GitHub release | ClawHub artifact |
|---|---|---|
| Contents | Full project (skill + `platform/` watchdog + `.github/` templates) | Portable core (`SKILL.md`, docs, `scripts/`, `sponsors/`) |
| Use when | You want the repo, auto-repair, issue templates, history | Your agent installs skills from ClawHub |
| Version | Same tag (`v1.5.1`) | Same tag (`v1.5.1`) |

Both contain the same installer and enhancement script; the GitHub repo additionally ships
Windows-only tooling (the auto-repair watchdog) and GitHub-only files (issue templates,
security policy).

### License & support

MIT with **mandatory attribution** — any use, including modified variants, must credit
**Pondsi**. See [LICENSE](LICENSE). If this saved you time, see [SPONSORS.md](SPONSORS.md).

---

## 简体中文

### 这是什么

给 OpenClaw Control UI（网页控制台）的**模型选择器**加一列「供应商导航」：左列点供应商，
右列只显示该供应商的模型。**两步选定模型**，不用再在几十上百个模型的长列表里翻找。

### 它解决什么问题

官方选择器是「按供应商分组的扁平长列表」。供应商少、模型少时没问题；但现实里往往是
本地 Ollama + 几个云 API + 聚合站，每家几十个模型 —— 列表变成滚动马拉松，想要的模型
被埋在中间，每次切换都要划过一堆不相干的分组。

```
┌─────────────┬────────────────────────────────┐
│ 全部         │  [ 搜索 ]                       │
│ ▸ DeepSeek  │  deepseek-v4-flash              │
│ ▸ Qwen      │  deepseek-v4-pro                │
│ ▸ GLM       │  deepseek-reasoner              │
│ ▸ Mistral   │  ……仅该供应商的模型              │
└─────────────┴────────────────────────────────┘
```

| | 官方选择器 | 安装本技能后 |
|---|---|---|
| 5 家供应商 × 30 个模型时找模型 | 整条长列表滚到底 | 点供应商 → 选模型 |
| 切换供应商 | 隐含在分组标题里 | 左列显式导航 |
| 滚动 | 一条长滚动 | 两列各自独立滚动 |
| 「此聊天使用的账户」行 | 菜单里始终显示 | 隐藏（与选模型无关） |
| 主题 | 官方样式 | 官方 token，深浅/自定义主题自动跟随 |

### 卖点

- **供应商优先导航**：左列列出所有供应商，点一下右侧只留这一家的模型，两步直达。
- **模型再多也不乱**：十家供应商、上百个模型，右列永远只显示当前供应商。
- **自动跟随当前模型**：打开选择器，正在用的模型所属供应商已选中并高亮。
- **两列独立滚动**：CSS Grid 结构性方案，各滚各的，不会出现「先滚右列」的怪现象。
- **隐藏账号行**：官方菜单里那行 `deepseek:default` 与选模型无关，直接隐藏。
- **主题无补丁感**：全部走官方设计 token，深浅色与自定义主题自动跟随。
- **零自激**：所有 DOM 写操作带状态门控，不会触发观察器死循环。
- **响应式**：左列宽度 `clamp(84px, 26%, 132px)` 自适应；只有视口低于 340px 或官方
  搜索过滤时才退回原生布局。
- **可拉伸、记尺寸**：拖右下角手柄即可左右 + 上下调整大小，尺寸记住、下次打开自动恢复；
  长模型名另有悬停提示（双击手柄复位）。
- **自更新**：已经打开的标签页会自己发现服务端更新并自动重载（不降级、不打断输入），
  打完补丁不会再出现「看着像没生效」。

### 安装

在技能的 `scripts/` 目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/pcl-patch.ps1
```

脚本自动检测 Control UI 目录（npm 全局 root / 常见前缀 / PATH 中的 openclaw CLI）；
非标准布局加 `-Dist "<...>\dist\control-ui"`。看到 `[PCL] 完成` 后，刷新一次控制台页面
即可；此后的补丁会被已打开的页面**自动感知并重载**（见「自更新」）。

### 验证（一行）

浏览器控制台：

```js
window.pclModelPickerDiag()
```

期望已渲染实例显示 `state: "two-col"`、`rail: true`、`chips` = 供应商数 + 1、`twoCol: true`、`stylePresent: true`。
`two-col-filtering` 表示官方搜索框正在过滤（仍保持双列）；`fallback-narrow` 表示视口小于 340px。
自愈事件：`window.pclModelPickerLog()`。强制检查更新：`await window.pclModelPickerCheckUpdate()`。

### 卸载

```powershell
powershell -ExecutionPolicy Bypass -File scripts/pcl-patch.ps1 -Remove
```

### 是否安全

是。改动范围被脚本硬性限定，且全部可逆：

| 操作 | 范围控制 |
|------|----------|
| 在 `index.html` 末尾追加/替换**一行** `<script>` | 首次运行备份 `index.html.bak-pcl`；幂等；`-Remove` 还原 |
| 向 `assets/` 复制 `pcl-model-picker.v8.js` | 带版本号文件名 + URL 内容指纹 |
| 清理旧版本 js | 只删 `pcl-model-picker.v*.js`，**保留最近两版** |

- **不修改** OpenClaw 任何打包代码（JS/CSS/Service Worker 全部原样）
- **纯本地**：无外部网络、无遥测；增强脚本只在你的浏览器里运行，唯一请求是同源 `fetch('./')`（用于感知服务端更新并重载页面），不联系任何第三方、数据不出本机
- **作用面**：只改模型选择器的 DOM/CSS，不碰会话数据、配置、密钥
- **随时可退**：`-Remove`，或重装 OpenClaw 自动还原官方界面
- **升级后需重跑**：npm 会覆盖 `dist/`，这是预期行为

### OpenClaw 升级后

重跑同一条命令即可，脚本幂等。

Windows 上可以让它全自动：GitHub 包自带 [`platform/pcl-watchdog.ps1`](https://github.com/Pondsi/ModelSelectorOpenClaw/blob/main/platform/README.md)，
发现注入被覆盖就自动重跑安装器（计划任务 `BigLobster-PclModelPickerRepair`）；浏览器端再
自行重载，升级后无需任何手动操作。

### 该装哪个包？

| | GitHub 仓库 | ClawHub 制品 |
|---|---|---|
| 内容 | 完整项目（技能 + `platform/` 看门狗 + `.github/` 模板） | 可移植核心（`SKILL.md`、文档、`scripts/`、`sponsors/`） |
| 适合 | 想看仓库、要自动修复、提 issue、跟历史 | Agent 从 ClawHub 装技能 |
| 版本 | 同一 tag（`v1.5.1`） | 同一 tag（`v1.5.1`） |

两者含相同的安装脚本与增强脚本；GitHub 仓库额外包含 Windows 专属工具（自动修复看门狗）与
GitHub 专属文件（issue 模板、安全策略）。

### 许可证与支持

MIT + **强制署名**：任何使用（含修改后的变体）都必须标注 **Pondsi**。详见 [LICENSE](LICENSE)。
如果它帮你省了时间，欢迎看看 [SPONSORS.md](SPONSORS.md)。

---

## 繁體中文

**為 OpenClaw Control UI 的模型選擇器加上「供應商導覽欄」**：左欄點供應商，右欄只顯示該
供應商的模型，兩步選定模型，供應商與模型再多也不用在長列表裡翻找。

- 左欄：供應商導覽（開啟時自動跟隨目前模型所屬供應商）
- 右欄：僅顯示該供應商模型，與左欄各自獨立捲動
- 隱藏官方選單中與選模型無關的「此聊天使用的帳號」列
- 完全使用官方設計 token，深色／淺色／自訂主題自動跟隨
- 視窗低於 340px 或官方搜尋過濾時才退回原生版面

安裝、驗證、卸載與安全範圍說明**見 [English](#english) 與 [简体中文](#简体中文) 段落**（指令完全相同，無需重複）。

---

## 한국어

**OpenClaw Control UI 모델 선택기에 공급자 탐색 열을 추가합니다.** 왼쪽에서 공급자를 고르면
오른쪽에는 그 공급자의 모델만 표시되어 두 번의 클릭으로 모델을 고를 수 있습니다. 공급자와
모델이 아무리 많아도 긴 목록을 뒤질 필요가 없습니다.

- 왼쪽 열: 공급자 탐색(현재 사용 중인 모델의 공급자를 자동으로 따라감)
- 오른쪽 열: 선택한 공급자의 모델만, 각 열이 독립적으로 스크롤
- 모델 선택과 무관한 공식 「이 대화에서 사용하는 계정」 행 숨김
- 공식 디자인 토큰만 사용 — 밝은/어두운/사용자 테마 자동 대응
- 창 너비 340px 미만이거나 공식 검색 필터 사용 시에만 기본 레이아웃으로 복귀

설치·확인·제거·안전 범위는 **[English](#english)** 및 **[简体中文](#简体中文)** 절을 참고하십시오(명령은 동일합니다).

---

## Русский

**Добавляет колонку навигации по провайдерам в выбор модели OpenClaw Control UI.**
Слева выбираете провайдера — справа остаются только его модели: выбор модели за два клика
даже при десятках провайдеров и сотнях моделей.

- Левая колонка — навигация по провайдерам (автоматически следует за провайдером текущей модели)
- Правая колонка — только модели выбранного провайдера, независимая прокрутка
- Скрывает служебную строку «аккаунт для этого чата», не связанную с выбором модели
- Только официальные design-токены — тёмная/светлая/своя тема подхватывается автоматически
- Нативный список возвращается только при ширине окна менее 340px или при активном поиске

Установка, проверка, удаление и границы изменений — в разделах
**[English](#english)** и **[简体中文](#简体中文)** (команды идентичны).

---

## 日本語

**OpenClaw Control UI のモデル選択に「プロバイダー欄」を追加します。** 左でプロバイダーを
選ぶと、右にはそのプロバイダーのモデルだけが表示され、2 クリックでモデルを選択できます。
プロバイダーもモデルも多い環境でも、長いリストを探し回る必要はありません。

- 左列：プロバイダーのナビゲーション（現在使用中のモデルのプロバイダーを自動追従）
- 右列：選択したプロバイダーのモデルのみ、各列が独立してスクロール
- モデル選択と無関係な公式の「このチャットで使用するアカウント」行を非表示
- 公式デザイントークンのみ使用 — ダーク／ライト／カスタムテーマに自動追従
- ウィンドウ幅 340px 未満、または公式検索フィルター使用時のみ標準レイアウトに戻ります

インストール・確認・アンインストール・変更範囲は
**[English](#english)** と **[简体中文](#简体中文)** の各節をご覧ください（コマンドは同一です）。

---

## Español

**Añade una columna de navegación de proveedores al selector de modelos de OpenClaw
Control UI.** A la izquierda eliges el proveedor y a la derecha solo aparecen sus modelos:
seleccionar un modelo en dos clics, incluso con decenas de proveedores y cientos de modelos.

- Columna izquierda: navegación por proveedores (sigue automáticamente el proveedor del modelo actual)
- Columna derecha: solo los modelos del proveedor elegido, con desplazamiento independiente
- Oculta la fila oficial «cuenta usada en este chat», ajena a la elección de modelo
- Solo tokens de diseño oficiales: temas claro/oscuro/personalizados se adaptan solos
- La lista nativa vuelve solo con ventanas de menos de 340px o con el filtro de búsqueda activo

Instalación, verificación, desinstalación y alcance de los cambios: secciones
**[English](#english)** y **[简体中文](#简体中文)** (los comandos son idénticos).

---

## Français

**Ajoute une colonne de navigation par fournisseur au sélecteur de modèles d'OpenClaw
Control UI.** À gauche vous choisissez le fournisseur, à droite seuls ses modèles
apparaissent : sélection en deux clics, même avec des dizaines de fournisseurs et des
centaines de modèles.

- Colonne de gauche : navigation par fournisseur (suit automatiquement le fournisseur du modèle courant)
- Colonne de droite : uniquement les modèles du fournisseur choisi, défilement indépendant
- Masque la ligne officielle « compte utilisé dans ce chat », sans rapport avec le choix du modèle
- Uniquement des design tokens officiels : thèmes clair/sombre/personnalisés suivent automatiquement
- La liste native revient uniquement sous 340px de large ou pendant le filtre de recherche officiel

Installation, vérification, désinstallation et périmètre des modifications : voir les
sections **[English](#english)** et **[简体中文](#简体中文)** (commandes identiques).

---

## Other Ways to Support / 其他支持方式

- ⭐ Star this repo — it helps others discover ModelSelectorOpenClaw
- 🐛 Report issues or suggest features
- 🔧 Submit patches or improvements
- 📣 Share with friends and colleagues

See [SPONSORS.md](SPONSORS.md) · MIT License with mandatory attribution — see [LICENSE](LICENSE).

Pondsi (+MiMo-v2.5 +deepseek-v4.1-flash-expires-on-0910 +GLM5.3-flash) — automatically committed by OpenClaw
