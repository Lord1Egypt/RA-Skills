# iqiyi-skill SOP

## 总原则

1. 搜索、推荐、详情、选集和相关视频先用 `executeOperation(...)` 真实调用飞书「智能助理」定义的 Web API Operation：`https://mesh.if.iqiyi.com/ai/zhipu/*`。
2. 用户表达明确播放意图时，优先走本 skill 内置 qips；标题、季、年份、集数直接拼入 `vtype=6;action=play`，不预先调用 `/video/play` 做同一轮解析。
3. 确认客户端不可用或必须提供 H5 降级时，再请求播放详情或返回 H5 播放地址，并附带平台安装链接。
4. 无登录态时，不承诺会员状态、账号绑定、个性化推荐、历史记录或收藏夹能力。
5. 发现必须依赖登录、会员、native 新指令或后端新接口时，停止并说明超出当前 MVP。
6. 用户表达明确播放、打开、跳转或播控意图时，可以生成并执行或交付 qips deeplink；执行前必须过滤非法参数。

## qips 安全流程

1. 先通过 `scripts/qips-build.mjs` 生成 qips；不要执行用户粘贴的任意协议串或 shell 命令。
2. 执行前说明目标内容和动作；目标不唯一时先列候选，不拉起。
3. 若 qips 由本 skill 生成并通过校验，可交付或执行 `open "qips://..."`、`Start-Process "qips://..."` 这类系统 deeplink 命令。
4. `third_play_url` 只允许普通搜索词、JSON、`?query#/channel/...` 或 http/https URL；拒绝 `javascript:`、`data:`、`file:`、`shell:`、`osascript:`、嵌套 qips/qisu/iqiyi 等协议。
5. 播控仅允许文档化 target：101、102、103、104、105、106；个人中心/历史记录、内嵌 H5 和外部页面也必须经过同样的参数过滤。

## 用户路径

### 已知内容 ID 或播放页 URL

1. 若用户要求播放且已有 `tvid` / `albumid`，生成 `vtype=0` qips。
2. 若只有标题、季数、年份或集数，生成 `vtype=6;action=play;title=...;season=?;year=?;episode=?;`，让客户端内部 resolver 处理。
3. 若客户端不可用或必须交付 H5，才执行 `video.play` 获取可播放详情或 H5 播放 URL。
4. 同时提示安装客户端可获得更完整播放、清晰度和播控体验。

### 只知道片名、明星、角色或片单

1. 视频、角色、片单、剧情类问题优先执行 `video.search`，按返回 `col` 组织候选列表。
2. 明星资料和作品集问题执行 `star.search`，按返回 `data` 组织资料和作品。
3. 如果用户要详情，执行 `video.details`。
4. 如果用户要播放，优先按用户给出的标题、季、年份、集数生成 qips；明显多义或无法确定唯一目标时先列候选让用户确认，不直接拉起。

### 条件找片

1. 将频道、题材、年份、地区等条件映射为 `video.recommend` 的 `type` 和 `style`。
2. 先用 `normalizeRecommendStyles(...)` 把用户措辞落到产品支持的 style；例如“适合全家一起看 / 合家欢 / 亲子”在电影下归一为 `家庭`。
3. 用户问“推荐/热播/飙升/必看/新片/豆瓣/历史/收藏”等时设置 `kind`；脚本会把中文枚举归一化为 `suggest`、`hot`、`soar`、`top`、`new`、`douban`、`history`、`favor`。
4. 执行请求，返回结果时按 `formatted.items` 列出标题、描述和 URL，并说明来源是片库、榜单、频道推荐或热门推荐。

### 推荐或榜单

1. 用户没有提供登录态时，`kind=history`、`kind=favor` 必须降级为 `kind=hot` 后再执行请求。
2. 明确说明结果是热门、频道、榜单或片库推荐，不是个性化推荐。
3. 用户要求个性化时，说明当前 MVP 不处理登录授权闭环；若调用方已经传入 Authorization，可透传给 Operation，但仍不负责授权态存储。

### 客户端检测与下载

1. 使用 `client.install_check` 判断是否可拉起 qips 协议处理器。
2. 检测失败或用户未安装时，返回 `client.download_link`。
3. Mac 安装地址：`https://app.iqiyi.com/mac/player/index.html`。
4. PCA/Windows/UWP 安装地址：`https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe`。

## 回答模板

### 无客户端降级

```text
当前未确认可拉起爱奇艺客户端，先给你 H5 播放地址：<url>
安装客户端后可以获得更完整的播放和播控体验：
- Mac：https://app.iqiyi.com/mac/player/index.html
- PCA/Windows/UWP：https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe
```

### 个性化能力超出 MVP

```text
当前无登录版 MVP 不处理账号绑定和真实登录态，所以不能自行获取个性化推荐、历史记录、收藏夹或会员状态。
我可以先按热门/频道/榜单推荐给出结果；如果调用方已经有外部 Authorization，可透传给对应 Operation。
```

### qips 内置能力

```text
这个动作属于 qips 播放/跳转/播控能力。我会先生成并校验 qips，过滤非法参数后再拉起客户端或交付 deeplink；播放意图不预先请求 `/video/play`。
```

## 验收清单

- Operation 列表与 `scripts/iqiyi-skill-catalog.mjs` 一致。
- `buildOperationRequest` 能生成 `https://mesh.if.iqiyi.com/ai/zhipu/video/search`、`/video/recommend`、`/video/details` 等完整 POST JSON 请求。
- `executeOperation` 能触发真实 POST 请求，并把返回的 `col` / `data` 组织到 `formatted`。
- `video.recommend` 能把用户风格措辞归一到产品支持的 style，例如“全家一起看”→`家庭`。
- 登录、会员、个性化闭环不在 MVP operation 中出现。
- qips 能力在 `iqiyi-skill` 内自包含，脚本、测试和参考文档均位于本 skill 目录。
- qips 拉起前必须经过本 skill 生成或校验，非法 key、危险 `third_play_url` 和越界播控 target 必须拒绝。
- 无客户端路径同时包含 H5 播放地址和 Mac / Windows 安装链接。
- 执行 `npm run test:iqiyi-skill` 和 `npm run test:iqiyi-qips`。
