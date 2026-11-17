# vtype-recipes：qips 场景食谱

数据源：`core/src/play.ts`（`PlayInfo` 构造与 `vtype` 自动推断，95–107 行）、`core/src/launcher.ts`（`WebLauncher.play` 174–277 行、`PCALauncher.play` 918–1041 行、按标题开播 937–950 行）、`core/src/simulateKeyEvent.ts`（`controlMapping`）、`core/src/iqiyi2qips.ts`（`iqiyi://` 参数映射）。

## 通用格式

```
qips://key1=value1;key2=value2;...;
```
- 分号分隔，**末尾保留分号**
- value `encodeURIComponent`（中文、URL、JSON 均需转义）
- `qisu://` 同义

## vtype 矩阵

| vtype | 语义 | 必需 | 常用可选 |
|------:|------|------|----------|
| 0 | 点播 | `tvid` | `albumid` / `start_pos` / `playrecord` / `ischarge` / `s2` / `s3` / `s4` |
| 1 | 直播 | `vid`（或 `tvid`）| — |
| 2 | 第三方播放 | `thirdid`+`third_play_url`（或 `siteId`+`third_play_url`）| `third_name` / `third_docid` / `tvsubname` / `ischarge` |
| 3 | 秀场 | `roomid` | — |
| 4 | 只拉起不播放 | — | 业务定制 |
| 6 | 跳频道 / 播控 / H5 内 ChannelInfo 序列化 | `target`（+ 视场景 `channelid` / `action` / `third_play_url`）| 见下方分场景 |
| 7 | 带上下文跳频道（URL-hash：`?…#/channel/<id>/`）| `third_play_url=?<query>#/channel/<channelId>/` | — |

> 客户端会自动推断 `vtype`：有 `thirdid + third_play_url` 推为 `2`；有 `tvid` 推为 `0`。`vtype=7` 须显式写出。能显式写就显式写，避免歧义。

---

## vtype=6 + target=2 跳转场景

### 1) 跳常规频道（`ple=XCard`）

```
qips://vtype=6;target=2;channelid=1;
```
- `channelid` 查 [`channel-table.md`](channel-table.md)（1=电影、2=电视剧、4=动漫、17=体育、15=儿童 …）
- 不需要 `third_play_url`

### 2) 片库（`ple=FilmLib`）：仅 `vtype=6;target=2;`

片库跳转与打点统一走 **`vtype=6`**，由 `WebLauncher.play` / `PCALauncher.play` 的 **`case "6"`** 解析 `third_play_url` 后得到 `ChannelInfo`，其中 **`ple = PleType.FilmLib`**，`context` 携带筛选字段（如 `tagName`）。

**必备：**`vtype=6`、`target=2`、目标域 **`channelid`**（电影 `1`、电视剧 `2`、免费专区片库 `302`、`1009` 全部片库、`27` 微剧片库等，查 [`channel-table.md`](channel-table.md)）。

**`third_play_url`（二选一，均需整条 value 做 `encodeURIComponent`）：**

1. **JSON（推荐）**  
   `{"tagName":"<关键字>"}`  
   例（电视剧片库 +「免费」）：

```
qips://vtype=6;target=2;channelid=2;third_play_url=%7B%22tagName%22%3A%22%E5%85%8D%E8%B4%B9%22%7D;
```

   - PCA：`third_play_url` 若以 `%7B%22` 开头且以 `%22%7D` 结尾会先 `safeDecodeURIComponent` 再 `JSON.parse`（`PCALauncher.play` 约 `956–980` 行），随后与其它 `channelid` 分支一起落到 `ple = PleType.FilmLib` 并 `channelContext` 入栈（约 `986–1012` 行）。
   - 源码注释中的完整示例：`qips://vtype=6;target=2;channelid=2;third_play_url=%7B%22tagName%22%3A%22…%22%2C%22s2%22%3A%22…%22%7D;`（可在 JSON 内并列业务/打点字段，仍以 `case "6"` 解析）。

2. **明文关键字**  
   非 `http`、非 `{`/`[` 开头的字符串视为 **`tagName` 本体**（encode 后作为 `third_play_url`）：`WebLauncher` `case "6"` 约 `214–216` 行设 `pageParams = { tagName: thirdUrl }`；`PCALauncher` 在 JSON 解析未产出 `channelContext` 时用 `channelContext ?? { tagName: thirdUrl }`（约 `999–1001` 行）。

**落地结果：**`switch(new ChannelInfo({ channelId, ple: FilmLib, context }))`（PCA 经 `Handler.call(CmdKey.SwitchChannel, …)`）。

### 3) 搜索结果页（channelid=115）

```
（搜索词明文）
qips://vtype=6;target=2;channelid=115;third_play_url=%E6%B5%B7%E8%B4%BC%E7%8E%8B;

（指定是否走 Ai 搜：`fromAiSuggest` + `query`，整段 JSON 再 encode）
qips://vtype=6;target=2;channelid=115;third_play_url=%7B%22fromAiSuggest%22%3Atrue%2C%22query%22%3A%22%E6%B5%B7%E8%B4%BC%E7%8E%8B%22%7D;
```
- 普通搜索：`third_play_url` 为搜索词字符串，经 `encodeURIComponent` 后写入 qips
- **Ai 搜 / 与端上「是否走 Ai 搜」一致时**：`third_play_url=encodeURIComponent(JSON.stringify({ fromAiSuggest: <boolean>, query: "<搜索词>" }))`，其中 `fromAiSuggest` 为 `true` / `false` 由业务决定是否为 Ai 联想/ Ai 搜索路径

### 4) 个人中心子页（channelid=116）

```
qips://vtype=6;target=2;channelid=116;third_play_url=%7B%22tab_id%22%3A%22lishi%22%7D;
```
- JSON **仅使用 `tab_id`**；允许取值与 path 对照见 [`channel-table.md` 个人中心段](channel-table.md)

### 5) 播单的 `vtype=6` 形态（与 `ChannelInfo.toQipsUrl` 一致）

```
播单
qips://vtype=6;target=2;channelid=1011;third_play_url=%7B%22bodanId%22%3A7569738292687702%7D;
```
- `ChannelInfo.toQipsUrl()` 输出同为 `vtype=6` + JSON（`pageInfo.ts`）。
- 播单若使用 URL-hash 形态，见下文 **`vtype=7`**。

### 6) 作者空间 / 明星页（`vtype=6` JSON；URL-hash 形态见 `vtype=7` 段）

```
作者（channelid=1015）
qips://vtype=6;target=2;channelid=1015;third_play_url=%7B%22userId%22%3A1234567890%7D;

明星（channelid=1018）
qips://vtype=6;target=2;channelid=1018;third_play_url=%7B%22starId%22%3A987654321%7D;
```

### 7) 短视频 Tab（channelid=1012）

```
qips://vtype=6;target=2;channelid=1012;third_play_url=%7B%22tab%22%3A%22choice%22%7D;
```
- `tab` 取值：`follow` / `choice` / `yule` / `fun` / `auto` / `news` / `baby` / `health` / `tech` / `music` / `life`

### 8) 内嵌 H5（channelid=263 或 270）

```
qips://vtype=6;target=2;channelid=263;third_play_url=https%3A%2F%2Fwww.iqiyi.com%2FsomePromoPage;
```
- `third_play_url` 以 `http`/`https` 开头时，launcher 会走 `PleType.Web` 分支并承载为内嵌页
- 若地址含 iqiyi.com，pingback（`s2/s3/s4`）会被自动附加到 URL query

### 9) 带打点参数

所有跳转/播放都可追加来源打点：

```
qips://vtype=6;target=2;channelid=2;s2=<rpage>;s3=<block>;s4=<rseat>;
```
- `s2` / `s3` / `s4` 会在播放器侧转为 `vfrm` / `vfrmblk` / `vfrmrst`

---

## vtype=6 + action=play：按标题自然语言开播

当不知道 `tvid` / `albumid`，只知道中文名时使用：

```
qips://vtype=6;action=play;title=%E5%BA%86%E4%BD%99%E5%B9%B4;season=2;episode=5;
```
- 必填：`title`（中文需 encode）
- 可选：`season`（number）、`year`（string）、`episode`（number）
- 客户端调用 `getPlayInfoAsync({ title, season, year, episode })`，拿到 `intent.args` 后重新构造 `PlayInfo` 并开播
- 源码位置：`launcher.ts:937-950`

---

## vtype=6 + target=101..106：播控

数据源 `core/src/simulateKeyEvent.ts` 的 `controlMapping`（launcher 在播放页收到 `target > 100 && target < 110` 时不跳频道，改为执行键盘模拟）。

| target | 语义 | 底层按键 |
|-------:|------|---------|
| 101 | 播放 / 切换播放-暂停 | Space |
| 102 | 暂停 / 切换播放-暂停 | Space |
| 103 | 上一集 | Ctrl + ArrowLeft |
| 104 | 下一集 | Ctrl + ArrowRight |
| 105 | 快进 | ArrowRight |
| 106 | 快退 | ArrowLeft |

示例：

```
暂停
qips://vtype=6;target=102;

下一集
qips://vtype=6;target=104;

快进
qips://vtype=6;target=105;
```

> 仅在播放页上下文有效；非播放页收到播控 qips 会被忽略。

---

## vtype=0 点播

最短形：

```
qips://vtype=0;tvid=1234567890123;
```

带完整字段：

```
qips://vtype=0;tvid=1234567890123;albumid=98765432101;start_pos=120;playrecord=true;ischarge=false;s2=<rpage>;s3=<block>;s4=<rseat>;
```
- `start_pos` 单位：秒
- `playrecord`：`true` 走播放记录续播；`1` 会被解析为 `albumid !== tvid` 的布尔值
- `albumid` 为 `-1` 或 `0` 会被丢弃（见 `play.ts:112`）

若 Web 环境新开播放页，可以把 qips 作为 query 传：

```
https://www.iqiyi.com/?qips=<encodeURIComponent(qips://vtype=0;tvid=...;)>
```
（`WebLauncher.onload` 在 `location.search.qips` 命中时会执行）

---

## vtype=2 第三方播放

```
qips://vtype=2;thirdid=1606437380862314;third_play_url=https%3A%2F%2Fv.youku.com%2Fv_show%2Fid_XNTkzMTgyNzI5Ng%3D%3D.html;third_name=%E6%8A%A4%E5%BF%83;third_docid=b37ef222e4fe0062bf81ba2749ab3fbc;ischarge=false;tvsubname=%E6%8A%A4%E5%BF%8301;
```
- 也可以用 `siteId`（非 `iqiyi` 即可）替代 `thirdid`
- `third_name` 存在但没写 `tvsubname` 时，`toQipsUrl` 会自动补 `tvsubname`

---

## vtype=7 带上下文跳频道（URL-hash）

`third_play_url` 为 URL-like：`?<query>#/channel/<channelId>/`。`WebLauncher` / `PCALauncher` 的 **`case "7"`** 会 `safeDecodeURIComponent`，用 `getChannelIdFromUrl` 从 hash 取 **`channelId`**，用 `queryToJson` 从 query 取 **`pageParams`**，再 `switch(new ChannelInfo({ channelId, ple, context: pageParams }))`。本节只描述 **URL-hash** 的拼法与字段规则。

### 播单（channelid=1011）

```
qips://vtype=7;third_play_url=%3FbodanId%3D7569738292687702%23%2Fchannel%2F1011%2F;
```
decode 后 `third_play_url` = `?bodanId=7569738292687702#/channel/1011/`

### 字段规则

- **`third_play_url` 必填**，且必须包含 `/channel/<id>/` 段（`getChannelIdFromUrl` 反解 `channelId`；找不到时 fallback `channelId=1`）
- query 段携带业务键值，常见如 **`bodanId`**（播单）、**`userId`**（作者）、**`starId`**（明星）、**`data_url`** 等；组合与 `ple` 推断以 `launcher.ts` `case "7"` 为准（约 `247–266` 行 `WebLauncher`，约 `1013–1028` 行 `PCALauncher`）
- 反解辅助：`utils.ts:getChannelIdFromUrl`

---

## iqiyi:// 协议兼容

如果只有老的 `iqiyi://` 字符串，`parseIqiyiProtocol` 会将其转换为 qips 参数再交给 `PlayInfo` 使用。映射规则：

| iqiyi:// 字段（`biz_params`）| qips 字段 |
|------------------------------|-----------|
| `tvid` | `tvid` |
| `aid` | `albumid` |
| `ctype` | `vtype` |
| `cid` | `channelid` |
| `_pc`（`1`/`0`）| `ischarge`（boolean）|
| `biz_extend_params.progress` | `start_pos`（单位：秒）|
| `biz_extend_params.isCheckHistory`（`1`/`0`）| `playrecord`（boolean）|
| `biz_statistics` 中 `vv='{...}'` 的 `s2` / `s3` / `s4` | `s2` / `s3` / `s4` |

转换规则：
1. `pluginParams` 双重 decode
2. JSON.parse 后取 `biz_params`
3. 若无 `tvid`，直接返回 `null`（视为非法）

源码：`iqiyi2qips.ts:10-180`

---

## 选择策略

- **普通频道：`vtype=6;target=2;channelid=<id>;`**
- **片库：仅 §2（`vtype=6;target=2;` + `third_play_url`）**
- **播单等 URL-hash：`vtype=7` + `third_play_url=?<query>#/channel/<id>/`**
- **明确知道视频 ID 用 `vtype=0`**（最稳）
- **只有视频名称时用 `vtype=6;action=play`**（让客户端反查）
- **播控用 `vtype=6;target=101..106;`**
- **第三方视频用 `vtype=2`**
