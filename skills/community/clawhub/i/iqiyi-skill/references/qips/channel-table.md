# channel-table：channelId 完整映射

数据源：`core/src/channel.ts` 的 `channelInfoMapping`（第 40–676 行）。

## 常规频道（`ple = XCard`，直接 `qips://vtype=6;target=2;channelid=<id>;` 即可）

| channelId | 名称 | key | 可匹配 path（第一个为规范路径） |
|----------:|------|-----|------------------------------|
| 1 | 电影 | dianying | `movie` / `dianying` / `电影` |
| 2 | 电视剧 | dianshiju | `tv` / `series` / `drama` / `dianshiju` / `电视剧` |
| 3 | 纪录片 | jilupian | `documentary` / `jilupian` / `纪录片` |
| 4 | 动漫 | dongman | `comic` / `dongman` / `动漫` |
| 6 | 综艺 | zongyi | `variety` / `show` / `zongyi` / `综艺` |
| 8 | 游戏 | youxi | `game` / `games` / `youxi` / `游戏` |
| 12 | 知识 | edu | `knowledge` / `education` / `edu` / `zhishi` / `jiaoyu` / `知识` / `教育` |
| 15 | 儿童 | shaoer | `cartoon` / `children` / `child` / `kids` / `ertong` / `儿童`（域名 `child.iqiyi.com`）|
| 17 | 体育 | sports | `sports` / `pe` / `tiyu` / `体育`（外链 `https://sports.iqiyi.com/`）|
| 19 | 直播 | zhibo | `live` / `vlog`（外链 `https://live.iqiyi.com/center`）|
| 35 | 微剧 | weiju | `microdrama` |
| 37 | 漫剧 | manju | `comicdrama` |
| 50 | 热点 | hot | `suike` |
| 102 | VIP 会员 | vip | `vip`（域名 `vip.iqiyi.com`）|
| 1008 | 教育 | education | — |
| 1016 | 最新最热 | newhot | `newhot` |

## 片库 / 免费专区（`ple = FilmLib`）

| channelId | 名称 | 说明 |
|----------:|------|------|
| 27 | 微剧片库 | 直接进入片库形态 |
| 302 | 免费专区片库 | path=`list/free` |
| 1009 | 全部片库（首页入口） | path=`all` |

> 片库带 `tagName` 过滤使用 **`vtype=6;target=2;`**，`third_play_url` 为 `encodeURIComponent(JSON.stringify({ tagName: "<关键字>" }))`（PCA：`PCALauncher.play` `case "6"`，`934` 行注释示例）。明文非 JSON 的 `third_play_url` 在 `WebLauncher` / `PCALauncher` 的 `vtype=6` 分支中也会落到 `FilmLib` 上下文（见 `launcher.ts` 各自 `case "6"`）。

## 短视频 / 短剧 / 新片等（非 XCard）

| channelId | 名称 | ple | 备注 |
|----------:|------|-----|------|
| 300 | 免费 | ShortVideoPlayer | path=`free` |
| 1006 | 短剧 | — | path=`minidrama` |
| 1007 | 新片（Feeds 流） | NewVideos | — |
| 1012 | 短视频 | ShortVideoPlayer | path=`shortvideo`，context 带 `tab`（`follow`/`choice`/`yule`/`fun`/`auto`/`news`/`baby`/`health`/`tech`/`music`/`life`）|
| 1019 | 关注（短视频） | ShortVideoPlayer | path=`following` |
| 11 | 公开课 | — | path=`openClass` |
| 16 | 微电影 | — | 无 path |
| 111 | 爱奇艺出品 | — | 无 path |

## 搜索 / 个人中心 / 播单 / 作者 / 明星（**带 `getContext` 的特殊频道**）

| channelId | 名称 | ple | context 关键字段 | 推荐 qips（vtype=7 形态，encode 前）|
|----------:|------|-----|----------------|------|
| 115 | 搜索结果页 | Search | `query`；Ai 搜场景可加 JSON：`fromAiSuggest`、`query` | `vtype=6;target=2;channelid=115;third_play_url=<搜索词>;` 或 `third_play_url={"fromAiSuggest":true,"query":"xxx"}`（encode 前） |
| 116 | 个人中心 | Mine | `tab_id`（JSON） | `vtype=6;target=2;channelid=116;third_play_url={"tab_id":"lishi"}` 等 |
| 1011 | 播单 | PlayList | `bodanId`（number）| `vtype=7;third_play_url=?bodanId=<id>#/channel/1011/` |
| 1015 | 作者空间页 | Creator | `userId`（number）| `vtype=7;third_play_url=?userId=<id>#/channel/1015/` |
| 1018 | 明星页 | Star | `starId`（number）| `vtype=7;third_play_url=?starId=<id>#/channel/1018/` |

> 上表播单 / 作者 / 明星等「频道 + URL-hash 上下文」可使用 `vtype=7` + `third_play_url=?…#/channel/<id>/`。`ChannelInfo.toQipsUrl()` 对频道上下文输出 `vtype=6` + JSON（`pageInfo.ts`）。**片库**见本节上方「片库 / 免费专区」段。

个人中心子页（`third_play_url` = `encodeURIComponent(JSON.stringify({ tab_id: "<值>" }))`）：

| tab_id | 说明 |
|--------|------|
| lishi | 历史 |
| zaizhui | 在追 |
| yuyue | 预约 |
| guanzhu | 关注 |
| dianzan | 点赞 |
| kecheng | 课程 |
| shoucang | 收藏 |

## 专题页 / 特色专题页

| channelId 范围 | 名称 | key | ple |
|----------------|------|-----|-----|
| 200–209 | 专题页 | topic | XCard（部分为空）|
| 210–220 | 特色专题页 | topic0..topic10 | — |

## 通用 Web 内嵌页（`ple = Web`，依赖 `third_play_url` 承载 http(s) URL）

| channelId | 名称 | 预置 url（若有） |
|----------:|------|-----------------|
| 260 | 新片 | `https://www.iqiyi.com/newOnlinePCW` |
| 261 | 风云榜 | `https://www.iqiyi.com/ranks1PCW/home` |
| 262 | 云影院 | `https://www.iqiyi.com/cloudCinemaPCW1` |
| 263 | 通用页面 | 需显式传 `third_play_url=<url>` |
| 264 | 天气 | `https://www.iqiyi.com/weatherPCW` |
| 265–279 | 通用页面 | 需显式传 `third_play_url=<url>` |
| 270 | 默认内嵌页容器 | 由 launcher 兜底使用 |
| 1014 | 传奇游戏库 | `https://pc.game.iqiyi.com/pcaHome?startfrom=pcw_base_cq` |
| 1017 | 体育（embed） | `https://sports.iqiyi.com/` |

## 全部频道 / 发现 / 播放页（内部用）

| channelId | 名称 | ple | 备注 |
|----------:|------|-----|------|
| 99998 | 全部频道 | AllChannels | `silentNavigation=true`，跳转不更新路径 |
| 99999 | 发现页 | Discover | — |
| 10002 | 半屏播放 | XPlayer | 播放器内部入口 |
| -1 | 儿童（家长中心） | ParentCenter | — |

## 儿童模式子频道（`ple = XCard`）

`150001` / `150002` / `150003` / `150004` / `150005` / `150006` / `150007` / `150008` / `150009` / `1500010` / `1500011` 均为儿童模式下的 `shaoer` 子频道。

## 匹配优先级（`ChannelInfo.parse` 逻辑）

当给定 URL 需要反推 channelId 时，顺序为：
1. 频道自定义 `isMatch`（目前仅 `1012` 短视频使用）
2. `domain` 命中非 `www.iqiyi.com` 的子域名
3. `path` 数组命中 pathname 的第一段（去掉 `.html` 与前导 `/`）
4. `key` 严格等于 path
5. 全部失败 → 落到 `channelId = 100`（首页）
