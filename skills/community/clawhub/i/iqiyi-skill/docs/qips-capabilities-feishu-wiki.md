# 爱奇艺 qips 协议：跳转与播放能力说明（对外）

本文说明 **`qips://` / `qisu://` 协议**在爱奇艺 PC 客户端（PCA）及内嵌 Web（`@iqiyi/qysdk`）中可实现的**页面跳转、片库与频道上下文、点播/直播/第三方播放、播控与按标题开播**等能力。协议由客户端 `PlayInfo`、`Launcher`（含 `WebLauncher` / `PCALauncher`）解析并执行。

更细的拼写示例、与源码行号对齐的说明见仓库内 **`.cursor/skills/iqiyi-skill/SKILL.md`** 及 **`references/qips/`** 目录下参考文档。

---

## 1. 协议与运行环境

| 项目 | 说明 |
|------|------|
| 协议前缀 | `qips://` 与 `qisu://` 等价，系统或壳层注册后可由 **`Start-Process "qips://..."`**（Windows）或 **`open "qips://..."`**（macOS）拉起客户端。 |
| 移动端协议兼容 | `iqiyi://...` 可由客户端 **`parseIqiyiProtocol`** 转为 qips 参数后再走同一套逻辑；**对外新接建议直接拼 qips**。 |
| 典型环境 | **PCA**、**PCW 浏览器**、PWA；业务侧多通过 **`Launcher.navigate` / `Launcher.play`** 传入 qips 字符串或等价对象。 |
| 语法要点 | `qips://key=value;key2=value2;` — 分号分隔，**末尾保留分号**；各 **value 需 `encodeURIComponent`**（含中文、URL、整段 JSON）。 |

---

## 2. 能力总览（按场景）

下表为「用户/产品能做什么」与 **`vtype` 主入口** 的对应关系；同一意图在部分场景下还有 **`vtype=6` + JSON** 与 **`vtype=7` URL-hash** 两种频道上下文形态（见第 4、5 节）。

| 场景 | 能力说明 | 主要 `vtype` |
|------|----------|--------------|
| 点播正片 | 用 **`tvid`**（及可选 **`albumid`**）起播；支持 **`start_pos`** 续播、**`playrecord`**、**`ischarge`**、来源打点 **`s2/s3/s4`** | `0` |
| 直播 | 用 **`vid`** 或 **`tvid`** 进入直播播放 | `1` |
| 第三方站点播放 | **`thirdid` + `third_play_url`** 或 **`siteId` + `third_play_url`**；可带 **`third_name`**、**`third_docid`**、**`tvsubname`**、**`ischarge`** 等 | `2` |
| 秀场 | **`roomid`** | `3` |
| 仅拉起客户端 | 业务定制，不强制起播 | `4` |
| 跳频道首页 | **`target=2` + `channelid`**，无 `third_play_url` 时为常规 **`XCard`** 频道 | `6` |
| 片库（筛选、片库形态频道） | **`target=2` + `channelid` + `third_play_url`**（JSON **`tagName`** 或明文关键字）；**片库契约仅约定在 `vtype=6`** | `6` |
| 全站搜索页 | **`channelid=115`**：`third_play_url` 可为搜索词明文（encode）；或 `encodeURIComponent(JSON.stringify({ fromAiSuggest, query }))` 指定是否走 Ai 搜 | `6` |
| 个人中心子页 | **`channelid=116`**，`third_play_url` 为 JSON（如 **`dest`**：历史/收藏/订阅/课程/下载/账号设置等） | `6` |
| 播单 | **`channelid=1011`** + **`bodanId`**：可用 **`vtype=6` + JSON**（与 `ChannelInfo.toQipsUrl` 一致）或 **`vtype=7` URL-hash** | `6` / `7` |
| 作者空间 / 明星页 | **`userId`（1015）** / **`starId`（1018）**：**`vtype=6` JSON** 或 **`vtype=7` URL-hash** | `6` / `7` |
| 短视频频道 Tab | **`channelid=1012`** + JSON **`tab`**（如精选、关注、娱乐等枚举） | `6` |
| 内嵌 H5 | **`third_play_url` 为 http(s)**，走 **`Web`** 形态；指定 **`channelid`**（如 263 通用页、270 容器、体育/新片等预置或自定义 URL） | `6` |
| 按剧名/季/集开播 | 不知 **`tvid`** 时 **`action=play` + `title`**（可选 **`season` / `year` / `episode`**），由客户端 **`getPlayInfoAsync`** 解析后再起播 | `6` |
| 播放中播控 | **`target=101..106`**：播放/暂停、上/下一集、快进/快退（映射到本地按键） | `6` |
| 带 hash 的频道深链 | **`third_play_url=?查询#/channel/频道id/`**；query 内 **`bodanId` / `userId` / `starId` / `data_url`** 等由客户端解析 | `7` |

---

## 3. 按 `vtype` 的参数与行为

### `vtype=0`（点播）

- **必需**：`tvid`
- **常用可选**：`albumid`、`start_pos`（秒）、`playrecord`、`ischarge`、`s2`、`s3`、`s4`
- **说明**：已知视频 ID 时**最稳定**的起播方式。Web 可将整段 qips 放在页面 **`?qips=`** 中由 `WebLauncher` 消费。

### `vtype=1`（直播）

- **必需**：`vid` 或 `tvid`

### `vtype=2`（第三方播放）

- **必需**：`thirdid` + `third_play_url`，或 `siteId`（非 iqiyi）+ `third_play_url`
- **常用可选**：`third_name`、`third_docid`、`tvsubname`、`ischarge`

### `vtype=3`（秀场）

- **必需**：`roomid`

### `vtype=4`（只拉起）

- 业务定制；用于只唤起应用或壳层逻辑、不强制进入某一播放态的场景（具体以客户端实现为准）。

### `vtype=6`（频道 / 片库 / 搜索 / 我的 / 内嵌 / 播单 JSON / 按标题播 / 播控）

- **`target=2`**：频道导航；配合 **`channelid`** 与可选 **`third_play_url`** 覆盖第 2 节中除「仅 `vtype=7` URL-hash」以外的绝大部分**站内跳转**。
- **`action=play`**：自然语言标题开播（无 `tvid` 时）。
- **`target=101..106`**：播控（见下表）；**仅在当前为播放页上下文时生效**，否则可能被忽略。

| `target` | 能力 |
|---------|------|
| 101 | 播放 / 播放暂停切换 |
| 102 | 暂停 / 播放暂停切换 |
| 103 | 上一集 |
| 104 | 下一集 |
| 105 | 快进 |
| 106 | 快退 |

### `vtype=7`（URL-hash 带上下文跳频道）

- **必需**：`third_play_url`，形态为 **`?key=value&…#/channel/<channelId>/`**（整段 value 需 URL 编码后写入 qips）。
- **典型用途**：播单、作者、明星等 **`bodanId` / `userId` / `starId` / `data_url`** 与频道 ID 的**组合深链**；**片库筛选以 `vtype=6` 为准**（见第 4 节）。

---

## 4. 片库（`FilmLib`）— 仅使用 `vtype=6`

- **固定形态**：`qips://vtype=6;target=2;channelid=<片库或内容域频道>；third_play_url=<…>;`
- **`third_play_url`**（二选一，均需 encode）  
  1. **JSON（推荐）**：`{"tagName":"筛选关键字"}`，可与业务打点字段同置于 JSON。  
  2. **明文**：非 `http`、`{`、`[` 开头的字符串视为 **`tagName` 本体**。
- **常见 `channelid`**：`1` 电影、`2` 电视剧、`302` 免费专区片库、`1009` 全部片库、`27` 微剧片库等（与内容域一致，详见第 5 节表）。

---

## 5. 频道 ID 速查（对外常用子集）

完整映射与 path/key 见仓库 **`.cursor/skills/iqiyi-skill/references/qips/channel-table.md`**。下表为集成时最常查的 **channelId**。

### 5.1 常规内容频道（`vtype=6;target=2;channelid=…;`）

| channelId | 名称 |
|----------:|------|
| 1 | 电影 |
| 2 | 电视剧 |
| 3 | 纪录片 |
| 4 | 动漫 |
| 6 | 综艺 |
| 8 | 游戏 |
| 12 | 知识 |
| 15 | 儿童 |
| 17 | 体育 |
| 19 | 直播频道入口 |
| 35 | 微剧 |
| 37 | 漫剧 |
| 50 | 热点 |
| 102 | VIP 会员 |
| 1008 | 教育 |
| 1016 | 最新最热 |

### 5.2 片库形态（`FilmLib`，仍用 `vtype=6;target=2`）

| channelId | 名称 |
|----------:|------|
| 27 | 微剧片库 |
| 302 | 免费专区片库 |
| 1009 | 全部片库（首页入口） |

### 5.3 搜索 / 个人中心 / 播单 / 作者 / 明星

| channelId | 名称 | 典型上下文 |
|----------:|------|------------|
| 115 | 搜索结果 | `third_play_url` = 搜索词（encode）；或 JSON：`fromAiSuggest`、`query`（再走 encode） |
| 116 | 个人中心 | JSON：`dest` = history / collectionAppoint / subscription / course / download / accountSet |
| 1011 | 播单 | JSON `bodanId` 或 `vtype=7` hash 形态 |
| 1015 | 作者 | JSON `userId` 或 `vtype=7` |
| 1018 | 明星 | JSON `starId` 或 `vtype=7` |

### 5.4 短视频与其它

| channelId | 名称 | 备注 |
|----------:|------|------|
| 1012 | 短视频 | JSON **`tab`**：follow / choice / yule / fun / auto / news / baby / health / tech / music / life |
| 1019 | 关注（短视频） | — |
| 300 | 免费（短视频播放器形态） | `ShortVideoPlayer` |
| 1006 | 短剧 | — |
| 1007 | 新片 Feeds | — |

### 5.5 内嵌 Web（`third_play_url` 为 http(s)）

| channelId | 名称 |
|----------:|------|
| 260 | 新片 |
| 261 | 风云榜 |
| 262 | 云影院 |
| 263 | 通用内嵌页（须自带 URL） |
| 264 | 天气 |
| 265–279 | 通用内嵌页 |
| 270 | 默认内嵌容器 |
| 1014 | 传奇游戏库 |
| 1017 | 体育 embed |

### 5.6 专题与内部

| 范围 / channelId | 说明 |
|------------------|------|
| 200–209 | 专题页 |
| 210–220 | 特色专题 |
| 99998 | 全部频道 |
| 99999 | 发现 |
| 10002 | 半屏播放（内部） |
| -1 | 儿童家长中心 |
| 150001–1500011 | 儿童模式下少儿子频道 |

---

## 6. 打点与 `iqiyi://` 映射（摘要）

- **跳转与播放**均可追加 **`s2` / `s3` / `s4`**（来源页/块/位），在播放链路中可转为 **`vfrm` / `vfrmblk` / `vfrmrst`**。
- **`iqiyi://`** 常见字段映射：`tvid`、`aid→albumid`、`ctype→vtype`、`cid→channelid`、`_pc→ischarge`、续播进度与 **`playrecord`**、统计里的 **`s2/s3/s4`** 等；无 **`tvid`** 时老协议可能判非法，**新接优先 qips**。

---

## 7. 集成方式提示

- **壳层 / 运营**：拼好 qips 字符串，通过系统已注册的 **`qips://`** 处理器拉起；Windows 可用 **`Start-Process "qips://…"`**。
- **H5 / 业务 JS**：使用 **`Launcher.navigate(qips)`** 或 **`Launcher.play(qips)`**（以 `@iqiyi/qysdk` 文档为准），由当前环境适配到 `WebLauncher` 或 `PCALauncher`。

---

## 8. 能力与边界（对外需知）

1. **播控 `target=101..106`**：依赖当前是否在**播放页**；非播放页可能被忽略。  
2. **`vtype=7`**：`third_play_url` 必须含 **`#/channel/<id>/`** 片段以便解析频道；解析失败时 **`channelId` 可能回退为 1**（以客户端实现为准）。  
3. **`vtype` 推断**：存在 **`tvid`** 易推断为点播等；**`vtype=7` 须显式写出**。**生产环境建议显式写出 `vtype`**，避免歧义。  
4. **频道与能力随版本演进**：未列出的 channelId 以 **`channel.ts` 的 `channelInfoMapping`** 与产品文档为准；本文与仓库内 skill 同步维护时以 **reference 表** 为准。

---

## 9. 相关文档（仓库内）

| 文档路径 | 用途 |
|-----------|------|
| `.cursor/skills/iqiyi-skill/SKILL.md` | Agent 执行 qips 的契约、自检与执行模板 |
| `.cursor/skills/iqiyi-skill/references/qips/vtype-recipes.md` | 各 `vtype` 示例 qips 与字段细则 |
| `.cursor/skills/iqiyi-skill/references/qips/channel-table.md` | channelId 全量表与 path/key |
| `.cursor/skills/iqiyi-skill/references/qips/api-usage.md` | `PlayInfo` / `ChannelInfo` / `Launcher` 开发者用法 |
| `.cursor/skills/iqiyi-skill/references/qips/launch-checklist.md` | 本机拉起验收用例 |
