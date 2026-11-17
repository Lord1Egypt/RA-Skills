# 控制命令 (control)

> AI-facing usage guide for `kugou-cli control` — the local PC/Mac Kugou client control subcommands.

本模块通过本机 HTTP server 控制 PC/Mac 酷狗客户端，支持播放控制、收藏管理、歌单创建等操作。输出格式为原始 JSON（详见 [references/output-format.md](./output-format.md)）。

**前置条件**: CLI 已登录（`kugou-cli auth login`）+ 酷狗客户端正在运行。仅支持 Windows / macOS（Linux 运行时会报错，见下方错误场景）。

---

## 命令列表

### 读操作（read）

| 命令 | 说明 |
|------|------|
| `kugou-cli control start` | 显式触发握手/唤起客户端（用于预热或调试） |
| `kugou-cli control status` | 获取客户端状态（协议版本、登录态、能力列表） |
| `kugou-cli control current` | 获取当前播放歌曲（歌名、进度、音量、收藏状态） |

### 播放器控制（player）

| 命令 | 说明 |
|------|------|
| `kugou-cli control play` | 播放歌曲（按 mixsongid） |
| `kugou-cli control play-playlist` | 播放整个歌单（按 global_collection_id） |
| `kugou-cli control continue-play` | 拉取"另一设备续播"列表并开始播放 |
| `kugou-cli control player` | 播放器控制（播放/暂停/切歌/停止） |
| `kugou-cli control seek` | 进度控制（快进/快退/跳转） |
| `kugou-cli control volume` | 音量控制（增减/设置/静音） |

### 账户操作（account）

| 命令 | 说明 |
|------|------|
| `kugou-cli control favorite song` | 收藏/取消收藏歌曲 |
| `kugou-cli control favorite songlist` | 收藏/取消收藏歌单 |
| `kugou-cli control playlist create` | 创建本地歌单（带歌曲列表） |

### 系统操作（utility）

| 命令 | 说明 |
|------|------|
| `kugou-cli control open` | 打开客户端内页面（主界面/歌手/专辑/歌单/搜索） |
| `kugou-cli control doctor` | 诊断 `control start` 失败的根因（HVCI / VBS / launcher / home-dir） |

---

## 1. start — 显式触发握手

触发酷狗客户端的 URL scheme 唤起，等待客户端建立本机 HTTP 通道并返回状态。仅用于预热通道或调试连通性，不调用任何 `/v1/...` 业务接口。

```bash
kugou-cli control start
```

**输出示例**（成功）:
```json
{"handshake":"ok","addr":"http://127.0.0.1:52144"}
```

**输出示例**（失败）:
```
kugou-cli control: not logged in, run `kugou-cli auth login` first: auth file not found
```

**`start` 失败时优先跑 `control doctor` 诊断根因**（见下文 §N）。常见场景：
- Win11 Memory Integrity (HVCI) 开着 + 客户端 v20.1.40：HVCI 拦截客户端启动时访问的内存，触发 NTSTATUS 0xC0000005 → 关 HVCI 后重试
- PowerShell 被裁掉（Windows Sandbox / AppContainer）：URL scheme 触发失败 → 自动 fallback 到 `cmd /c start`
- $HOME / $USERPROFILE 未设置或不可写：握手文件无法落地 → 设置有效环境变量

---

## 2. status — 获取客户端状态

查询本地酷狗客户端的协议版本、登录态和能力列表。

```bash
kugou-cli control status
```

**输出示例**:
```json
{
  "code": 0,
  "data": {
    "version": "1.0.0",
    "login": true,
    "capabilities": ["play", "pause", "seek", "volume", "favorite", "playlist"]
  }
}
```

---

## 3. current — 获取当前播放

查询当前播放歌曲详情，包括歌名、歌手、进度、音量和收藏状态。

```bash
kugou-cli control current
```

**输出示例**:
```json
{
  "code": 0,
  "data": {
    "song_name": "晴天",
    "singer_name": "周杰伦",
    "mixsongid": "32100650",
    "position_ms": 45000,
    "duration_ms": 240000,
    "volume": 65,
    "favorited": false
  }
}
```

---

## 4. play — 播放歌曲

在客户端播放一首歌曲。`--mixsongid` 必填，其余字段可选（仅用于客户端展示，不影响播放命中）。

```bash
kugou-cli control play --mixsongid 32100650 --song-name "晴天" --singer-name "周杰伦"
kugou-cli control play --mix-song-id 32100650 --mode "append_queue"
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--mixsongid` | 歌曲 mixsongid（必填），也支持 `--mix-song-id` 别名 |
| `--song-name` | 歌曲显示名（可选） |
| `--singer-name` | 歌手显示名（可选） |
| `--mode` | 播放模式：`append_queue`（追加队列）、`next_play`（下一首播放） |

> 🎵 **AI 必读**：命令成功后**必须**调 `control current` 拿到当前歌曲名/歌手，告知用户。**不要**直接展示 `--song-name` / `--singer-name` 参数——那只是客户端展示标签，与实际播放可能不一致。

**输出示例**:
```json
{"code":0,"data":{"accepted":true}}
```

---

## 5. player — 播放器控制

发送传输控制动作到播放器（播放/暂停/切歌等）。

```bash
kugou-cli control player --action pause
kugou-cli control player --action next
kugou-cli control player --action resume
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--action` | 动作（必填）：`play` `resume` `pause` `toggle` `next` `prev` `previous` `stop` |

`prev` 和 `previous` 视为同义词。

> 🎵 **AI 必读**：使用 `next` / `prev` / `previous` **切歌后**必须调 `control current` 拿到当前歌曲名/歌手，告知用户。`play` / `pause` / `resume` / `toggle` / `stop` 等切换播放状态的动作不需要告知曲目（曲目未变）。

**输出示例**:
```json
{"code":0,"data":{"accepted":true}}
```

---

## 5.1 continue-play — 拉取另一设备续播列表并播放

拉取云端"另一设备最近播放"的续播列表（酷狗首页的"续接播放"入口），并在本地客户端开始播放。

```bash
# 默认：替换当前队列，从头播放
kugou-cli control continue-play

# 不打断当前播放：把续播列表追加到本地队列尾部
kugou-cli control continue-play --mode append_queue

# 把续播列表插到当前曲目之后立即播放
kugou-cli control continue-play --mode next_play
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--mode` | 队列策略：空（默认，替换队列）/ `append_queue`（追加队列尾部）/ `next_play`（下一首播放） |

> 🎵 **AI 必读**：命令成功后**必须**调 `control current` 拿到当前歌曲名/歌手，告知用户。

**前置条件**:
- 已登录：`kugou-cli auth login`
- 客户端内已登录（否则返回 409/4091"login required"，见错误场景 §2）
- 本地客户端必须运行（`kugou-cli control start` 健康）

**输出示例**:
```json
{"code":0,"data":{"accepted":true}}
```

---

## 6. seek — 进度控制

控制当前播放歌曲的进度。

```bash
# 快进 30 秒
kugou-cli control seek --action forward --offset-ms 30000

# 快退 10 秒
kugou-cli control seek --action rewind --offset-ms 10000

# 跳转到 2 分钟位置
kugou-cli control seek --action set --position-ms 120000
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--action` | 动作（必填）：`forward` `rewind` `set` |
| `--offset-ms` | 偏移量（毫秒，forward/rewind 时必填） |
| `--position-ms` | 绝对位置（毫秒，action=set 时必填） |

---

## 7. volume — 音量控制

调整客户端音量或静音状态。

```bash
# 音量增加 5 格
kugou-cli control volume --action up --delta 5

# 音量减少 10 格
kugou-cli control volume --action down --delta 10

# 设置音量到 42
kugou-cli control volume --action set --volume 42

# 静音
kugou-cli control volume --action mute

# 取消静音
kugou-cli control volume --action unmute

# 切换静音状态
kugou-cli control volume --action toggle_mute
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--action` | 动作（必填）：`up` `down` `set` `mute` `unmute` `toggle_mute` |
| `--delta` | 音量变化量（up/down 时必填） |
| `--volume` | 绝对音量 0-100（action=set 时必填；CLI 不做范围校验，由客户端夹取） |

---

## 8. favorite song — 收藏歌曲

收藏或取消收藏一首歌曲。

```bash
# 收藏歌曲
kugou-cli control favorite song --mixsongid 32100650 --song-name "晴天" --singer-name "周杰伦"

# 取消收藏
kugou-cli control favorite song --action remove --mixsongid 32100650
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--action` | 操作（默认 `add`）：`add` `remove` |
| `--mixsongid` | 歌曲 mixsongid（必填） |
| `--song-name` | 歌曲显示名（可选） |
| `--singer-name` | 歌手显示名（可选） |

---

## 9. favorite songlist — 收藏歌单

收藏或取消收藏一个歌单。

```bash
# 收藏歌单（action=add 时必填 --list-name 与 --owner-user-id）
kugou-cli control favorite songlist --list-name "精选" --global-collection-id abcdef --owner-user-id 1286024014

# 取消收藏（--global-collection-id 必填；--list-name / --owner-user-id 不允许传）
kugou-cli control favorite songlist --action remove --global-collection-id abcdef
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--action` | 操作（默认 `add`）：`add` `remove` |
| `--global-collection-id` | 歌单全局 ID（即协议层的 `list_gid`，`add` / `remove` 都必填） |
| `--list-name` | 歌单显示名（**`action=add` 时必填**） |
| `--owner-user-id` | 歌单所有者 ID（**`action=add` 时必填**；`action=remove` 时不允许传） |
| `--list-icon` | 歌单图标 URL（可选） |
| `--list-intro` | 歌单简介（可选） |
| `--list-tags` | 歌单标签（可选） |

> **校验**：CLI 在本地做严格校验，缺任一必填项都会 exit 1 报错：
> - `--global-collection-id`：**`add` 和 `remove` 两种 action 都必填**（用于标识目标歌单）
> - `--list-name`：仅 `--action=add` 必填
> - `--owner-user-id`：仅 `--action=add` 必填；`--action=remove` 时**禁止**传（避免向取消请求带过时元数据）

---

## 10. playlist create — 创建歌单

> ✅ **创建歌单的首选路径**。Agent 在用户同意创建歌单时**必须**先尝试本命令；只有当客户端不可用（Linux / 客户端未运行 / 握手失败 / 调用失败）时才回退到云端备选 [`music create-playlist`](./music.md#71-接口说明云端备选仅在-70-第-4-条任一条件成立时使用)。完整决策逻辑见 [music.md §7 创建歌单](./music.md#7-创建歌单)。

在本地客户端创建一个新歌单，并可选地添加歌曲。

```bash
kugou-cli control playlist create --name "周杰伦精选" --mixsongids "32100650,32068120"
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--name` | 歌单名称（必填） |
| `--mixsongids` | 歌曲 mixsongid 列表，逗号分隔（必填，至少含一个有效 ID） |

`--mixsongids` 示例：`"32100650,32068120"` 或 `"32100650, 32068120"`（空格会被忽略）。

**前置条件**（与 control 其他子命令一致，详见 [§前置条件总结](#前置条件总结)）：
- CLI 已登录（`kugou-cli auth login`）
- 本地酷狗客户端（Windows / macOS）正在运行且握手健康（`kugou-cli control start`）
- 客户端内已登录（否则会收到 409/4091 `login required`，见 [§错误场景 2](#场景-2客户端未登录http-409--code-4091)）

**输出示例**:
```json
{
  "code": 0,
  "data": {
    "accepted": true,
    "count": 2,
    "global_collection_id": "全局歌单id",
    "name": "歌单名",
    "songlist_id": 123456
  },
  "message": "ok",
  "request_id": "ec-124-1786072145"
}
```

> **字段语义说明（重要）**：
> - `data.global_collection_id`：字符串形态的歌单全局 ID（协议层 `list_gid`），**可直接传给 `control play-playlist --global-id`**（详见 [§12 play-playlist](./control.md#12-play-playlist--播放整个歌单)）
> - `data.songlist_id`：数字形态的本地客户端歌单 ID，**不能直接传给 `play-playlist --global-id`**，仅在客户端 UI 内展示用
>
> 实际响应字段由客户端版本决定，**两条不一定同时存在**——某些客户端版本可能只返回 `songlist_id` 而无 `global_collection_id`。Agent 在用户同意播放时优先取 `global_collection_id`；若缺失，按下方"ID 流转提示"回退。

### 创建成功后必须主动询问用户是否播放

> 🎵 **AI 必读**：本命令返回成功（`code: 0`）后，Agent **必须主动询问用户**"是否要播放这个歌单"，等用户明确回复后再决定下一步。详见 [music.md §7.0 调用原则 第 5 条](./music.md#70-调用原则ai-必读)。

用户同意时优先调用：

```bash
# 客户端路径：默认清空当前队列、按歌单顺序从头播放
kugou-cli control play-playlist --global-id "<global_id>"

# 不打断当前播放：把新歌单追加到队列尾部
kugou-cli control play-playlist --global-id "<global_id>" --playlist-mode append_queue
```

> **ID 流转提示**：本命令 `data.songlist_id` 是数字 ID，而 `control play-playlist --global-id` 需要的是字符串 `global_collection_id`（协议层 `list_gid`），二者不可直接互转。Agent 在用户同意播放时按以下顺序获取可用 ID：
> 1. **优先**：取响应里 `data.global_collection_id`（字符串）→ 直接传给 `play-playlist --global-id`
> 2. **回退一**：客户端未返回 `global_collection_id` 时，用响应里的歌单名（`data.name`）跑 `kugou-cli music search-playlist "<name>"`，从结果里挑一个匹配的 `global_id` 传给 `play-playlist`
> 3. **回退二**：以上两步都拿不到时，告诉用户"刚创建的歌单 ID 无法用于播放命令，请在客户端 UI 内打开播放"（**不要**编造或猜 ID）
> 4. **绝对禁止**：把数字 `songlist_id` 当成 `global_id` 用——类型不匹配，客户端协议层会拒绝

> **播放路径全部失败的回退**：若用户同意播放，但客户端仍不可用（control play-playlist 因客户端未运行 / ID 拿不到而失败），Agent **不要**循环重试。按 [music.md §7.2 云端歌单的播放](./music.md#72-云端歌单的播放控制浏览器打开-h5-链接) 走"先探后告知"的浏览器路径：用浏览器工具打开云端 `song_list_url` 尝试点击播放，工具不可用时明确告知用户手动打开。

---

## 11. open — 打开客户端页面

在酷狗客户端中打开指定页面（非静默，客户端主窗口会切换到对应视图）。`silent` 字段硬编码为 `false`。

```bash
# 打开主界面
kugou-cli control open --target-type main

# 打开歌手页
kugou-cli control open --target-type singer --singer-id 12345

# 打开专辑页（可选 --mixsongid 作为专辑根曲）
kugou-cli control open --target-type album --album-id 67890 --mixsongid 8888

# 打开歌单页
kugou-cli control open --target-type songlist --global-collection-id "collection_3_938985631_304_0"

# 打开搜索结果页
kugou-cli control open --target-type search --keyword "周杰伦"
```

**target-type 和必填参数**:

| target-type | 必填参数 | 说明 |
|-------------|----------|------|
| `main` | 无 | 打开主界面 |
| `singer` | `--singer-id` | 歌手页 |
| `album` | `--album-id` | 专辑页 |
| `songlist` | `--global-collection-id` | 歌单页（协议 wire 字段 `list_gid`） |
| `search` | `--keyword` | 搜索结果页 |

**通用可选参数**:

| 参数 | 说明 |
|------|------|
| `--mixsongid` | 可选 mixsongid（如 `album` 时作为专辑根曲） |

---

## 12. play-playlist — 播放整个歌单

按歌单的 `global_collection_id`（即协议层的 `list_gid`）让本地酷狗客户端联网拉歌单后播放。本命令只传 `list_gid` 给客户端，**无需 CLI 端联网预翻页**——歌单内容由客户端在收到请求后异步拉取（CLI 不需要外网/代理）。

**`--global-id` 的合法来源**（按推荐顺序）：

1. **`music search-playlist` / `recommend-playlist` 响应的 `global_id` 字段**（最稳，跨客户端兼容）
2. **`control playlist create` 响应的 `data.global_collection_id` 字段**（仅当客户端版本返回该字段时可用——见 [§10 输出字段语义](./control.md#10-playlist-create--创建歌单)）
3. `music playlist-songs <global_collection_id>` 直接使用你已有的字符串 ID

**不要**：把 `control playlist create` 响应里的数字 `data.songlist_id` 当成 `global-id` 用（类型不匹配，会被客户端协议层拒绝）。

```bash
# 默认：清空当前队列，按歌单顺序从头播放
kugou-cli control play-playlist --global-id "collection_3_938985631_304_0"

# 不打断当前播放：歌单追加到队列尾部
kugou-cli control play-playlist --global-id "..." --playlist-mode append_queue

# 把歌单插到当前曲目之后立即播放
kugou-cli control play-playlist --global-id "..." --playlist-mode next_play
```

**参数**:

| 参数 | 说明 |
|------|------|
| `--global-id` | 歌单全局 ID（必填），即协议层的 `list_gid`，例如 `collection_3_938985631_304_0`。必须是字符串（不要传数字 `songlist_id`）|
| `--playlist-mode` | 队列策略：`auto`（默认）/ `append_queue` / `next_play` |

**playlist-mode 详解**:

| 取值 | wire 上的 `play_mode` | 客户端行为 | 适用场景 |
|------|----------------------|----------|----------|
| `auto`（默认） | **省略** | 客户端默认 = 清空当前队列后按歌单顺序从头播放 | 切到歌单里从头听 |
| `append_queue` | `"append_queue"` | 歌单追加到播放队列尾部，不打断当前播放 | 不打断当前歌曲，排队播放 |
| `next_play` | `"next_play"` | 歌单插入到当前曲目之后立即播放，后续队列顺延 | 听完这首就想听歌单 |

> 🎵 **AI 必读**：命令成功后**必须**调 `control current` 拿到当前歌曲名/歌手，告知用户。本命令是异步的——客户端拉歌单歌曲可能要等几秒；如 `control current` 一开始返回 `code: 非 0`，等 1-2 秒再试一次。

**前置条件**:

- 已登录：`kugou-cli auth login`
- 酷狗桌面客户端在后台运行，且握手健康：`kugou-cli control start`

**典型联动**:

```bash
# 搜歌单 → 取 global_id → 播放
GID=$(kugou-cli music search-playlist "周杰伦" | jq -r '.data.list[0].global_id')
kugou-cli control play-playlist --global-id "$GID"

# 立即听下一首（不打断当前曲目）
kugou-cli control play-playlist --global-id "$GID" --playlist-mode next_play
```

---

## 错误场景

### 场景 1：CLI 未登录（登录态缺失）

未登录时，任意 `control` 子命令都会在入口被拦截。

**触发**:
```bash
kugou-cli control status
```

**stderr**:
```
kugou-cli control: not logged in, run `kugou-cli auth login` first: auth file not found
```

**stdout**: 无

**exit code**: 1

**修复**: 运行 `kugou-cli auth login` 完成 CLI 扫码登录。

---

### 场景 2：客户端未登录（HTTP 409 / code: 4091）

`favorite song`、`favorite songlist`、`playlist create` 等需要账号的操作，如果客户端本身未登录（cookie/token 过期或从未登录），协议层返回 `code: 4091`。

**触发**:
```bash
kugou-cli control favorite song --mixsongid 32100650
```

**stdout**（协议响应原样输出）:
```json
{"code":4091,"msg":"login required"}
```

**stderr**（CLI 追加的提示）:
```
HTTP 409
请在酷狗客户端内登录后重试
```

**exit code**: 0（CLI 正常退出，调用方从 stdout 的 `code` 字段自行判断）

**注意**: CLI 不会 exit 1，也不会提示去运行 `kugou-cli auth login`（那是 CLI 登录，跟客户端登录是两件独立的事）。

**修复**: 在酷狗客户端 UI 内扫码登录客户端。

---

### 场景 3：客户端未安装或未启动（握手超时）

握手在 6 秒内未完成，说明酷狗客户端未安装、未运行或未响应 URL scheme 唤起。

**触发**:
```bash
kugou-cli control status
```

（假设客户端未运行）

**stderr**:
```
is Kugou client installed?
```

**stdout**: 无

**exit code**: 1

**排查步骤**:
1. 确认酷狗客户端已安装（Windows: `KuGou.exe`，Mac: `/Applications/KuGou.app`）
2. 确认客户端已启动并运行
3. Windows 用户确认 URL scheme `kugou://` 已注册（可在 PowerShell 中试 `start kugou://workbuddy`）
4. Mac 用户在 Safari 地址栏试 `mackugou://workbuddy` 确认 LaunchServices 注册正常

---

### 场景 4：Linux 不支持

在非 Windows / macOS 系统上运行任意 `control` 子命令，会被运行时拦截。

**触发**（在 Linux 上）:
```bash
kugou-cli control status
```

**stderr**:
```
kugou-cli control: linux is not supported
```

**stdout**: 无

**exit code**: 1

**说明**: 酷狗客户端仅提供 Windows 和 macOS 版本，因此 control 命令也仅在这两个平台可用。所有非 Windows/macOS 系统都会被拒绝，包括 Linux、FreeBSD、OpenBSD 等。

---

## 典型 AI Agent 工作流

以下为通过 `control` 命令控制本地酷狗客户端的典型流程。

### 完整示例：搜索并播放歌曲

```
# 1. 搜索歌曲（music 命令，返回 mix_song_id）
$ kugou-cli music search "周杰伦 晴天"
{
  "data": {
    "list": [{
      "song_name": "晴天",
      "mix_song_id": "32100650",
      "artist_name": "周杰伦"
    }]
  }
}

# 2. 让客户端播放这首歌
$ kugou-cli control play --mixsongid 32100650 --song-name "晴天" --singer-name "周杰伦"
{"code":0,"data":{"accepted":true}}

# 3. 暂停播放
$ kugou-cli control player --action pause
{"code":0,"data":{"accepted":true}}

# 4. 查看当前播放状态
$ kugou-cli control current
{
  "code": 0,
  "data": {
    "song_name": "晴天",
    "position_ms": 30000,
    "volume": 65
  }
}

# 5. 收藏当前歌曲
$ kugou-cli control favorite song --mixsongid 32100650
{"code":0,"data":{"accepted":true}}

# 6. 搜索更多歌曲并创建歌单
$ kugou-cli music search "周杰伦"
# 假设返回多个结果，mix_song_id 分别为 32100650、32068120、31598745

$ kugou-cli control playlist create --name "周杰伦精选" --mixsongids "32100650,32068120,31598745"
{"code":0,"data":{"songlist_id":"abc123","name":"周杰伦精选","count":3}}
```

### 与 music 命令的配合

`music search` 返回的 `mix_song_id`（或 `mix_song_id`）可直接传给 `control play --mixsongid`，无需任何 ID 转换。

```
music search "歌手"  →  提取 mix_song_id  →  control play --mixsongid <id>
                                        →  control favorite song --mixsongid <id>
                                        →  control playlist create --mixsongids <id1>,<id2>
```

---

## 前置条件总结

| 条件 | 说明 |
|------|------|
| CLI 已登录 | `kugou-cli auth login`（扫码登录，存储登录态） |
| 酷狗客户端运行中 | 客户端内置 HTTP server 必须启动（`control start` 会自动触发） |
| 客户端已登录 | 在酷狗客户端 UI 内扫码登录（影响 `favorite`/`playlist create` 等操作） |
| Windows / macOS | Linux 不支持（运行时检查） |

---

## 13. Client Detection (`control detect`)

> **零副作用探测**，**不启动客户端、不抢焦点**——和 `control start` 不同，本命令只读 OS 端的"URL scheme 注册"等信号。

### 用法

```bash
kugou-cli control detect              # 默认 JSON 输出
kugou-cli control detect --json=false  # 人类可读一行
```

### 退出码（Agent 编程消费）

| 退出码 | 含义 |
|---|---|
| `0` | 客户端已安装（`installed: true`） |
| `1` | 探测过程出错（系统权限等） |
| `2` | 客户端没装（`installed: false`） |

> Linux/BSD 上 `installed: false` 但 `error: ""` —— 不支持是正常情况，不是错误。

### JSON 输出示例（Windows，有客户端）

```json
{
  "installed": true,
  "scheme_registered": true,
  "scheme": "kugou",
  "exe_path": "C:\\Program Files\\KuGou\\KGMusic\\KuGou.exe",
  "version": "20.1.40.27866",
  "handshake_exists": true,
  "handshake_path": "C:\\Users\\alice\\.config\\kugou-cli\\handshake.json",
  "platform": "windows",
  "checked_at": "2026-08-11T15:25:01+08:00",
  "strategies": {
    "scheme_registry":  {"ok": true, "evidence": "HKCR\\kugou\\shell\\open\\command -> ..."},
    "install_path_scan": {"ok": true, "evidence": "C:\\Program Files\\KuGou\\KGMusic\\KuGou.exe exists"},
    "handshake_file":    {"ok": true, "evidence": "...handshake.json present"}
  }
}
```

### 与 `control start` 的区别

| 维度 | `control detect` | `control start` |
|---|---|---|
| 副作用 | **零**（只读 OS 信号） | 会启动客户端 + 抢焦点 |
| 触发客户端启动？ | ❌ | ✅（若握手文件不存在） |

### 在 AI 工作流里的位置

详见 [SKILL.md §5](../SKILL.md) —— **首次**要向用户展示歌曲列表/歌单列表前探测一次，记下 `client_available`；后续展示复用本次结果。

`control detect` **不**替代 `control start` —— 后者仍负责建立 handshake + 启动客户端，是 `control play` 等命令的前置。

---

## 14. Doctor (`control doctor`)

> 诊断 `control start` 失败的根因——`detect` 只看"客户端有没有装"，`doctor` 看"为什么拉不起"。

`control start` 的"6 秒握手超时"对**完全没装客户端**、**Win11 HVCI 不兼容导致客户端启动后立即崩**、**PowerShell 被裁掉**、**$HOME 不可写**这些情况长得一模一样——都是同一个错误。`doctor` 把这些信号分开成结构化字段，AI agent 能直接据此判断该走哪个分支。

### 用法

```bash
kugou-cli control doctor               # 默认 JSON 输出
kugou-cli control doctor --json=false   # 一行人类可读
```

**副作用极小**：不启动客户端、不抢焦点、不触发 URL scheme。唯一的磁盘动作是 `$HOME` 可写性探测——可能创建 `~/.config/kugou-cli` 目录并写入后立即删除一个临时文件（CLI 握手本来也要用这个目录）。安全在任何时候跑。

### 退出码

| 退出码 | 含义 | 何时 |
|---|---|---|
| `0` | OK，无 fatal 无 hint | 环境正常，可直接 `control start` |
| `1` | FATAL，必须修 | `client.installed=false` 或 `home_dir_accessible=false` |
| `2` | 非 fatal，有 hint | `hints` 数组非空——start 仍可能成功，但建议看 hint |

### JSON 输出字段

| 字段 | 类型 | 含义 |
|---|---|---|
| `platform` / `goos` | string | `runtime.GOOS`（`windows` / `darwin` / `linux`） |
| `checked_at` | RFC3339 | 检查时间 |
| `client.installed` | bool | `Detect()` 的总判定 |
| `client.exe_path` | string | 客户端可执行文件绝对路径（HKCR scheme handler 或 install 路径扫描） |
| `client.version` | string | HKLM Uninstall `DisplayVersion`（Win）；空表示无法读到 |
| `client.scheme_registered` | bool | `HKCR\kugou` 注册项 |
| `client.handshake_path` | string | 握手文件期望位置 |
| `client.handshake_exists` | bool | 握手文件是否已存在 |
| `environment.hvci_enabled` | bool \| null | Win11 Memory Integrity（`HKLM\...\HypervisorEnforcedCodeIntegrity\Enabled`），非 Win 平台为 `null` |
| `environment.vbs_enabled` | bool \| null | VBS（`HKLM\...\DeviceGuard\EnableVirtualizationBasedSecurity`） |
| `environment.powershell_available` | bool \| null | `powershell.exe` 是否在 PATH |
| `environment.explorer_available` | bool \| null | `explorer.exe` 是否在 PATH |
| `environment.in_job_object` | bool \| null | 当前进程是否在 Job Object 里（Win 才有意义）。`true` 意味着 kugou-cli 派生的进程可能被 sandbox reap |
| `environment.job_breakaway_allowed` | bool \| null | Job 是否允许 `CREATE_BREAKAWAY_FROM_JOB`（设置 `JOB_OBJECT_LIMIT_BREAKAWAY_OK` / `SILENT_BREAKAWAY_OK`）。`false` = 派生链逃不出 Job，CLI 因此**不再**设置该标志；`null` 字段省略 = 不在 Job 或读不到 Job flag |
| `environment.job_kill_on_close` | bool \| null | Job 是否设置 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`。`true` = Job 关闭时其内进程被内核终止——这是"客户端启动后又消失"的真正原因；`null` = 不在 Job 或读不到 |
| `environment.process_integrity_level` | string | Token 完整性级别：`Low`（AppContainer / LPAC）/`Medium`（普通）/`High`（elevated）/`System`/`Unknown`。`Low` 意味着 Job breakaway 也救不了 |
| `environment.parent_process` | string | `pid=N path=...` —— 当前进程的父进程，用于识别是否跑在 sandbox runner 下 |
| `environment.grandparent_process` | string | `pid=N path=...` —— 祖父进程，二级排查（"spawned by shell" vs "spawned directly by sandbox"） |
| `environment.home_dir` | string | 解析后的 `$HOME`/`$USERPROFILE` |
| `environment.home_dir_accessible` | bool | `.config/kugou-cli/` 是否可创建+写 |
| `hints` | string[] | 给用户的修复建议（HVCI 关、$HOME 设置、PowerShell 缺失等） |
| `fatal` | bool | 是否 fatal |
| `fatal_reason` | string | fatal 时的简短原因 |

**三态指针规则**：`null` = 该平台不探测或探测失败；`true`/`false` = 已探测且确定。

### JSON 输出示例（Win11 + HVCI 开 + 客户端 v20.1.40）

```json
{
  "platform": "windows",
  "goos": "windows",
  "checked_at": "2026-09-11T16:14:30+08:00",
  "client": {
    "installed": true,
    "exe_path": "C:\\Program Files\\KuGou\\KGMusic\\KuGou.exe",
    "version": "20.1.40.27854",
    "scheme_registered": true,
    "handshake_path": "C:\\Users\\alice\\.config\\kugou-cli\\handshake.json",
    "handshake_exists": false
  },
  "environment": {
    "hvci_enabled": true,
    "vbs_enabled": true,
    "powershell_available": true,
    "explorer_available": true,
    "home_dir": "C:\\Users\\alice",
    "home_dir_accessible": true
  },
  "hints": [
    "Win11 Memory Integrity (HVCI) is enabled — Kugou client v20.x is known to crash with NTSTATUS 0xC0000005 under HVCI",
    "workaround: Settings → Privacy & Security → Windows Security → Device Security → Core Isolation → Memory Integrity → Off, then reboot",
    "client version 20.1.40.27854 is on the known-HVCI-crash list even with Memory Integrity on; upgrading to v20.2+ is recommended",
    "no handshake file yet — `control start` will fire the URL scheme; if it times out, the most likely cause is the client crashing on launch (see HVCI hint above)"
  ],
  "fatal": false
}
```

### 在 AI 工作流里的位置

```text
agent wants to call control play
  └─ first: run control doctor
       ├─ fatal=1 → tell user to install client / fix $HOME, abort
       └─ fatal=0 → proceed
            ├─ hints contain "HVCI" → warn user before start, ask before disabling HVCI
            ├─ hints contain "Job Object" or "AppContainer" → sandbox reap 问题,
            │   kugou-cli 改不了,需要 sandbox 平台方配合或绕开 sandbox 启动
            └─ no hints → just run control start, then control play
```

### Sandbox reap 诊断速查

`control start` 失败的"6 秒超时"对多种原因长得一模一样，**`doctor` 的 `environment` 字段把它们分开**：

| `in_job_object` | `job_breakaway_allowed` | `job_kill_on_close` | `process_integrity_level` | 隔离类型 | 结果 |
|---|---|---|---|---|---|
| `false` | (省略) | (省略) | `Medium` | 无 Job 隔离 | ✅ 客户端正常存活 |
| `true` | `true` | 任意 | 任意 | Job 隔离，允许 breakaway | ✅ CLI 请求脱离 Job，客户端存活 |
| `true` | `false` | `true` | 任意 | Job 隔离，不允许脱离且关闭即终止 | ⚠️ 客户端能启动，但 Job 关闭（宿主结束命令）时被终止 |
| `true` | `false` | `false` | 任意 | Job 隔离，不允许脱离但不强杀 | ⚠️ 客户端可能存活，但不保证 |
| `true` | (省略) | (省略) | 任意 | Job 隔离，读不到 flag | ⚠️ 未知，按最坏情况处理 |
| (省略) | (省略) | (省略) | `Low` | **AppContainer / LPAC**（不走 Job） | ❌ Job breakaway 救不了 |
| (省略) | (省略) | (省略) | (省略) | 非 Windows 平台 | N/A |

> **重要（2026-09-11 修正）**：当 `job_breakaway_allowed=false` 时，CLI **不会**再设置 `CREATE_BREAKAWAY_FROM_JOB`——因为在禁止脱离的 Job 里请求脱离会让 `CreateProcess` 直接返回 `ERROR_ACCESS_DENIED`，客户端根本起不来。旧版无条件设置该标志，反而在最需要它的 Job 隔离环境里把启动搞挂了。现在客户端会正常启动并在**当前命令**存续期间存活；能否跨命令存活由宿主的 Job 生命周期决定（`job_kill_on_close`）。
>
> **实用结论**：在 `breakaway=false` 的宿主里，把 `control start` 和真正的控制命令**串在同一条命令里执行**（例如 `control start && control play ...`）即可播放——它们共享同一个 Job，客户端在这条命令期间一直活着。分成两条独立命令时，前一条启动的客户端在后一条里可能已被回收。

> 字段省略 (`omitempty`) = 该平台不探测，或探测失败导致值是 nil。要区分这两种情况，看 `platform` 字段：非 Windows 上所有 Win-only 字段都省略。

父进程链 (`parent_process` / `grandparent_process`) 用于识别"我是被什么 spawn 出来的"，对识别具体 sandbox runner（workbuddy / opencode / cloud-agent 等）有用，但 doctor 不内置 sandbox 名到 hint 的映射——这部分逻辑放在调用方，doctor 只负责给出**真实数据**。

### 与 `control detect` 的区别

| 维度 | `control detect` | `control doctor` |
|---|---|---|
| 副作用 | 零（只读 OS 信号） | 极小（读 HVCI/VBS/launcher/Job，外加一次 `~/.config/kugou-cli` 可写性探测：建目录+写删临时文件） |
| 输出焦点 | "客户端有没有装？" | "为什么 `control start` 会失败？" |
| 退出码 | 0/1/2（installed 维度） | 0/1/2（fatal+hint 维度） |
| 应在何时跑 | AI agent 每次冷启动前 | `control start` 失败后 |

---

## 相关文档

- [references/output-format.md](./output-format.md) — 输出格式与展示规范
- [references/music.md](./music.md) — music 命令使用指南
- [references/auth.md](./auth.md) — auth 命令使用指南

> 客户端协议规范由酷狗客户端内部定义，不在用户可访问的文档范围内。本文档只描述 CLI 端可观察的行为。
