# api-usage：开发者 SDK 调用契约

面向开发者。数据源：`core/src/apis.ts`（`Launcher` 门面，504–570 行）、`core/src/play.ts`（`PlayInfo`）、`core/src/pageInfo.ts`（`ChannelInfo`）、`core/src/launcher.ts`（`WebLauncher` / `PWALauncher` / `PCALauncher`）。

## 全局门面 `Launcher`（`window.QySdk.Launcher`）

业务层在上层页面通常只用 `Launcher`，它会自动分派到当前环境（Web / PWA / PCA）的 adapter。

```ts
interface Launcher {
    play(info: string | IPageInfo): void;
    navigate(info: string | IPageInfo, options?: {
        prefer?: "new" | "page";
        historyType?: "disabled" | "replace" | "default";
        source?: string;
        pos?: number;
    }): void;
    replay(info?: QipsParams | PlayInfo | string): void;
    goto(params: IGotoParams & { /* 弹窗参数 */ }): void;
    back(): void;
    push(value: ChannelInfo): void;
    readonly history: ChannelInfo[];
    readonly current: IPageInfo;
    readonly currentChannel: ChannelInfo;
    readonly hasHistory: boolean;
    onPlayOccur(handler, thisArg?, options?, disposableArray?): void;
    onChannelChanged(handler, thisArg?, options?, disposableArray?): void;
    onNavigateOccur(handler, thisArg?, options?, disposableArray?): void;
}
```

### 典型调用

```ts
import { Launcher } from "@iqiyi/qysdk";

Launcher.navigate("qips://vtype=6;target=2;channelid=2;");

Launcher.play("qips://vtype=0;tvid=1234567890;start_pos=120;");

Launcher.navigate({ channelId: 2, ple: PleType.XCard });

Launcher.replay();

Launcher.replay({ tvid: 9876543210 });
```

> 规则：`play` / `navigate` / `replay` 入参可以是 qips 字符串、`iqiyi://` 字符串、播放页 URL、`QipsParams` 对象或 `ChannelInfo` / `PlayInfo` 实例。

---

## `PlayInfo`（`core/src/play.ts`）

### 构造

```ts
new PlayInfo(info: string | QipsParams, options?: IPingback)
```

入参形态：
1. **qips 字符串**：`qips://...` 或 `qisu://...`
2. **iqiyi:// 字符串**：内部调 `parseIqiyiProtocol` 转 qips
3. **播放页 URL**：如 `https://www.iqiyi.com/v_xxx.html?tvid=...`
4. **体育地址**：由 `isSportsUrl` 识别，只记到 `webUrl`
5. **其他 http(s) / game 协议**：存到 `webUrl`
6. **`QipsParams` 对象**：直接作为 `_opt`

`options`（第二参）可覆盖打点字段 `s2/s3/s4` 等。

### `vtype` 自动推断（当未显式传时）

| 条件 | 推断 vtype |
|------|-----------|
| `thirdid` 或（`siteId` 且不是 `"iqiyi"`）且 `third_play_url` 非空 | `2` |
| 有 `tvid` | `0` |
| 都不满足 | 丢弃 `_opt` |

> 注意：**`vtype=7`**（播单等 URL-hash）**无法**靠上表自动推断，须显式写 `vtype=7`。

### 常用方法

| 方法 | 说明 |
|------|------|
| `toQipsUrl()` | 序列化为 `qips://k=v;...;`，自动 encodeURIComponent，`vtype=2 && third_name && !tvsubname` 时会补 `tvsubname` |
| `prop<T>(key, value?, skipForExisted?)` | 读 / 写 / 删除单个字段（`value=undefined` 删除；`skipForExisted=true` 只在字段空时写） |
| `appendProps(obj, skipForExisted?)` | 批量 merge |
| `toWebUrl(url, keepOriginalKey?)` | 将 PlayInfo 拼到给定 URL 的 query 上（打点字段默认转为 `vfrm/vfrmblk/vfrmrst`）|
| `PlayInfo.parse(location)` | 从 `{pathname, search}` 静态解析当前播放页 URL |

### 重要属性

- `tvId` / `albumId`：按 `vtype` 返回正确的 id（直播走 `vid`、秀场走 `roomid`）
- `vtype`（string）/ `channelId`
- `pingback` / `webPingback` / `webPingbackQuery`
- `webUrl` / `isOutWeb`（体育或 `vtype=2` 视为外跳）
- `query`：导出除 `tvid` 外所有非空字段
- `source`：`PageSource` 枚举（`location` / `navigator` / `qips` / `webapp` 等）

---

## `ChannelInfo`（`core/src/pageInfo.ts`）

### 构造

```ts
new ChannelInfo({
    channelId: number;
    ple?: PleType;
    context?: object | string;
    pingback?: IPingback;
    source?: PageSource;
    pos?: number;
})
```
- `context` 若是字符串且以 `{` / `[` 开头会 `JSON.parse`；否则会被同时填到 `query` 和 `tagName`
- 默认 `ple = PleType.XCard`

### 常用

- `toQipsUrl()`：固定输出 `qips://vtype=6;target=2;channelid=<id>;third_play_url=<JSON(encoded)>;<pingback...>`（见 `pageInfo.ts:250-252`）
- `toWebUrl()`：返回 `https://www.iqiyi.com/<channel.path[0]>`
- `ChannelInfo.parse(location, sender)`：从 URL 反推频道，遵循 `isMatch` → `domain` → `path` → `key` 的匹配顺序

---

## Launcher 实现三件套

业务层一般不直接用这三个类，但在需要理解行为分支时可对照：

| 环境 | 类 | 文件位置 | 关键差异 |
|------|----|---------|----------|
| PCW（PC 浏览器）| `WebLauncher` | `launcher.ts:17-569` | 播放页用 `location.href` 跳转；频道切换通过 `history.pushState` 或 `location.href` 同步 URL |
| PWA | `PWALauncher extends WebLauncher` | `launcher.ts:571-688` | `toPlayerByEvent` 按 `isOutWeb` 决定是否开新窗口；播控交互略有不同 |
| PCA（客户端内 H5）| `PCALauncher` | `launcher.ts:690-1310` | 频道切换走 `Handler.call(CmdKey.SwitchChannel)`；播放走 `Handler.call(CmdKey.Play)`；播放页内收 qips 通过 `syncByStorage(CmdKey.SwitchChannel, qips)` 同步 |

### `play(context, options, sender)` 的 vtype 分派（简化）

| vtype | WebLauncher 行为 | PCALauncher 行为 |
|------:|-----------------|-----------------|
| `2` | `goto({url: third_play_url, target:"_blank"})` | `Handler.call(CmdKey.ThirdPlay, {url})` |
| `6` + `target in [101,110)` | — | 进入播控（由 `playController` 派发到 `controlMapping`）|
| `6` + `action="play"` | — | 调 `getPlayInfoAsync` 拿到真实 tvid 后再 `playByQips` |
| `6` + `target=2` | 视 `third_play_url` 形态分派为 `PleType.Web` / `FilmLib` / `Search` / `Mine` / `PlayList` / `Creator` / `Star` / `ShortVideoPlayer` / `XCard`（片库见 `vtype-recipes` §2）| 同左 |
| `7` | 解析 `third_play_url` 反查 `channelId`，`switch`（URL-hash） | 同左 |
| `0` / `1` / `3` / `4` / 默认 | 走 `switch` 进入播放器 | `playByQips` → `Handler.call(CmdKey.Play)` |

### `switch(value, options, sender)`

- 入参为 `ChannelInfo` 或 `PlayInfo`（内部再判断）
- `options.prefer="new"` 会新开窗口/Tab（URL 上带 `qips=<encoded>`）
- `options.historyType`：`"disabled"` 不入栈、`"replace"` 替换当前项、`"default"` 按类规则（同频道内部变化不入栈；Mine/Creator/Star 连续跳转会替换）
- PCA 内若在播放器上下文，不 push 频道而是通过 `syncByStorage` 通知主窗口

### `replay(info?, sender?)`（仅 PCALauncher 实现）

- `info=null`：读取缓存 `CacheKey.CurPlayUrl`，无缓存则报错
- `info=string` 或 `PlayInfo`：直接以新值开播
- `info=QipsParams`：merge 到缓存上再开播

---

## `Launcher.navigate` 推荐用法

最通用入口。若已经拿到 qips 字符串：

```ts
Launcher.navigate("qips://vtype=6;target=2;channelid=115;third_play_url=%E6%B5%B7%E8%B4%BC%E7%8E%8B;", {
    source: "navigator",
});
```

指定 Ai 搜路径（`fromAiSuggest` + `query`，整段 JSON 再 encode）：

```ts
Launcher.navigate(
    "qips://vtype=6;target=2;channelid=115;third_play_url=%7B%22fromAiSuggest%22%3Atrue%2C%22query%22%3A%22%E6%B5%B7%E8%B4%BC%E7%8E%8B%22%7D;",
    { source: "navigator" },
);
```

若在 PCA 内从外部信道（如原生事件 `EventKey.ChannelChanged`）拿到 `qips` 字段，直接转发：

```ts
if (value.qips) {
    return Launcher.navigate(value.qips, {
        source: value.source,
        pos: value?.addition?.pos,
    });
}
```
（见 `launcher.ts:761-766`）

---

## 事件订阅

| 事件 | 触发时机 |
|------|---------|
| `Launcher.onPlayOccur(handler)` | `toPlayerByEvent` 触发时 |
| `Launcher.onChannelChanged(handler)` | `CacheKey.ChannelInfo` 变更时（频道切换成功后）|
| `Launcher.onNavigateOccur(handler)` | 任何 `switch` / `toPlayerByEvent` 都会 fire，含 `stopwatch` / `pingback` |

---

## 最短决策树

1. 只需要拼协议 / 拉起系统 deeplink？→ **不要**调 SDK，直接走 `Start-Process "qips://..."`。
2. 在 H5 业务代码里触发跳转 / 开播？→ `Launcher.navigate(qipsOrObject)`。
3. 明确要新开窗口/Tab？→ `Launcher.navigate(..., { prefer: "new" })`。
4. 要重播当前内容？→ `Launcher.replay()`。
5. 要返回上一页？→ `Launcher.back()`。
6. 监听跳转 / 播放？→ `Launcher.onNavigateOccur` / `onPlayOccur` / `onChannelChanged`。
