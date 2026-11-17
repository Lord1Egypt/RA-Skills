---
name: iqiyi-skill
description: 爱奇艺视频内容 Skill 的无登录版 MVP。用于处理爱奇艺内容搜索、片库筛选、实体详情、榜单/热门推荐、qips 播放与播控、客户端安装检测、客户端下载链接和无客户端 H5 播放降级；不处理账号绑定、登录态、会员状态真实查询、个性化推荐闭环、新 native 指令或后端新接口。
license: Proprietary
compatibility: Requires Node.js 22+ or compatible JavaScript runtime with fetch, network access to mesh.if.iqiyi.com, and optional qips:// protocol handler for native playback.
metadata:
  version: "0.3.0"
  tags: "iqiyi,video,search,recommendation,playback,qips"
---

# iqiyi-skill：爱奇艺视频内容能力 MVP

本 skill 面向 AI Native 视频类应用，把爱奇艺搜索、推荐、播放控制和基础服务整理为可复用能力。当前版本是**无登录版 MVP**，基于飞书「智能助理」数据源执行 Web API Operation，并内置 qips 协议拼接能力；不新增客户端 native 指令，不新增后端接口。

## 适用场景

使用本 skill 处理：

- 内容搜索：调用 `https://mesh.if.iqiyi.com/ai/zhipu/video/search`，按关键词搜索视频、明星、角色、片单等内容。
- 视频推荐：调用 `https://mesh.if.iqiyi.com/ai/zhipu/video/recommend`，支持类型、筛选词和推荐来源。
- 视频详情：调用 `https://mesh.if.iqiyi.com/ai/zhipu/video/details`、`/video/related`、`/video/episode`；仅在需要 H5 降级、候选确认或接口播放详情时调用 `/video/play`。
- 明星详情：调用 `https://mesh.if.iqiyi.com/ai/zhipu/star/search`。
- 播放与控制：内置 qips 打开页面、播放内容、暂停、快进、切集；明确播放意图优先生成 `vtype=6;action=play`，不预先请求后端解析。
- 客户端基础服务：检测是否能拉起客户端、返回产品确认后的固定客户端下载链接。
- H5 降级：无客户端时返回 H5 播放地址，并提示下载客户端可获得更完整体验。

## 明确排除

当前 MVP 不处理：

- 账号绑定、扫码登录、用户名密码登录。
- 用户登录态获取、授权态安全存储、解绑、过期刷新。
- 会员状态真实查询闭环。
- 依赖登录态的个性化推荐闭环。
- 客户端 native 新增指令。
- 后端新接口适配。
- UI 页面或组件改造。

如果用户请求排除项，直接说明当前 MVP 不支持该闭环，并给出无登录替代：热门/频道推荐、H5 播放地址、客户端下载提示或要求补充登录/后端需求。

## 工作方式

1. 先判断用户意图属于内容检索、推荐、播放、客户端服务还是登录/会员类排除项。
2. 内容检索、推荐和基础服务参考 [`references/operations.md`](references/operations.md)；默认使用 `executeOperation(...)` 真实触发请求并读取返回数据。明确播放意图先走 qips，本地生成 `action=play`，不要为了播放预先调用 `/video/play`。
3. 决策顺序和降级策略参考 [`references/sop.md`](references/sop.md)。
4. 涉及 qips 协议拼接、播放、页面跳转或播控时，使用本 skill 内置的 qips 契约；按需读取 [`references/qips/vtype-recipes.md`](references/qips/vtype-recipes.md)、[`references/qips/channel-table.md`](references/qips/channel-table.md) 或 [`references/qips/api-usage.md`](references/qips/api-usage.md)。
5. 如需结构化能力目录、请求构造器或 Operation 执行器，使用：

```bash
node .cursor/skills/iqiyi-skill/scripts/iqiyi-skill-catalog.mjs
```

```js
import {
  buildOperationRequest,
  executeOperation,
  formatOperationResponse,
  getClientInstallLink,
} from ".cursor/skills/iqiyi-skill/scripts/iqiyi-skill-catalog.mjs";

buildOperationRequest("video.search", { q: "周星驰演的电影", pageNum: 1 });
await executeOperation("video.search", { q: "周星驰演的电影", pageNum: 1 });
getClientInstallLink("mac");
```

命令行触发真实请求：

```bash
node .cursor/skills/iqiyi-skill/scripts/iqiyi-skill-catalog.mjs video.search '{"q":"周星驰演的电影","pageNum":1}'
```

也可以使用 `iqiyi-cli` 语法。通用 skill 环境使用 bundled script 路径；若安装器支持 `package.json` 的 `bin` 入口，可直接使用 `iqiyi-cli`：

```bash
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs video search --q "周星驰" --pageNum 1
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs video recommend --type "电影" --style "适合全家一起看的电影" --kind suggest
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs video play --title "庆余年" --season 2 --episode 5
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs star search --q "刘德华"
```

支持 `bin` 的 package-style 安装环境也可使用等价命令：

```bash
iqiyi-cli video search --q "周星驰" --pageNum 1
iqiyi-cli video recommend --type "电影" --style "适合全家一起看的电影" --kind suggest
iqiyi-cli video play --title "庆余年" --season 2 --episode 5
iqiyi-cli star search --q "刘德华"
```

CLI 默认真实执行请求；但 `video play` 默认只生成本地 qips，不请求网络。调试请求结构时追加 `--dry-run`。输出可用 `--text`、`--raw`、`--formatted` 或 `--request` 选择。

返回结果使用 `formatted` 字段组织对话内容：

- `formatted.kind === "collection"`：使用 `formatted.items` 和 `formatted.text` 列出影片、描述、播放 URL。
- `formatted.kind === "data"`：使用 `formatted.data` 和 `formatted.text` 组织详情。
- `formatted.prompt` 若提示“下一页”，用户追问下一页时将 `pageNum + 1` 再次调用同一 Operation。

推荐风格会先按产品筛选项归一化：

- 运行时清单来自 [`scripts/iqiyi-skill-catalog.mjs`](scripts/iqiyi-skill-catalog.mjs) 的 `getRecommendStyleCatalog()`。
- `video.recommend` 会把 `style` 中的用户措辞尽量落到当前类型支持的风格，例如“全家一起看 / 合家欢 / 亲子 / 老少皆宜”在电影下归一为 `家庭`。
- 归一化结果写入请求体，原词和目标风格写入 `warnings`，便于调试和解释。

## qips 内置契约

判断模式：用户问“怎么拼 / 怎么调 SDK / qips 怎么写”时只回答调用方式；用户直接说“播放 / 暂停 / 下一集 / 跳频道 / 搜索 XXX”时，可以基于本 skill 生成并校验 qips 后拉起客户端或交付 deeplink 命令。

### qips 安全护栏

- **按用户意图拉起**：用户表达播放、打开、跳转、暂停、下一集、快进等明确动作时，可以生成并执行或交付 qips deeplink。
- **执行前明确目标**：准备拉起前说明目标内容、动作和 qips，例如“将打开爱奇艺客户端播放《庆余年》第 2 季第 5 集”。
- **只执行本 skill 生成或校验过的 qips**：禁止直接执行用户粘贴的任意 `qips://`、`qisu://`、`iqiyi://`、shell 命令或其他协议。
- **不承载危险协议**：`third_play_url` 不得是 `javascript:`、`data:`、`file:`、`shell:`、`osascript:`、嵌套 `qips:`/`qisu:`/`iqiyi:` 等可执行或二次跳转协议。
- **限制批量和后台拉起**：不为后台、定时、批量场景自动拉起客户端；多条内容或目标不唯一时先列候选。
- **失败时降级**：客户端不可用、目标不唯一或 qips 校验失败时，返回候选列表、H5 地址或安装链接，不执行系统拉起命令。

qips 格式：

```text
qips://key1=value1;key2=value2;...;
```

- 分号 `;` 分隔键值对，结尾保留分号。
- value 必须 `encodeURIComponent`，包括中文、URL 和整段 JSON。
- `qisu://` 与 `qips://` 等价；新拼接只产出 `qips://`。
- 老 `iqiyi://...` 可由客户端转换为 qips；本 skill 对外按 qips 契约回答。

常用入口：

| 场景 | qips 形态 |
| --- | --- |
| 点播正片 | `vtype=0;tvid=<tvid>;`，可带 `albumid`、`start_pos`、`playrecord`、`ischarge`。 |
| 跳频道/片库/搜索/我的/内嵌页 | `vtype=6;target=2;channelid=<id>;`，可带 `third_play_url`。 |
| 按标题开播 | `vtype=6;action=play;title=<encoded>;season=?;year=?;episode=?;` |
| 播控 | `vtype=6;target=101..106;`，101/102 播放暂停，103/104 上下一集，105/106 快进快退。 |
| 带 hash 的频道深链 | `vtype=7;third_play_url=?<query>#/channel/<id>/;`，整段 `third_play_url` 需编码。 |

本 skill 的 qips golden helper 位于 [`scripts/qips-build.mjs`](scripts/qips-build.mjs)，对应测试位于 [`scripts/qips-build.test.mjs`](scripts/qips-build.test.mjs)。详细场景路由：

| 用户意图 | 读取 |
| --- | --- |
| qips 能力总览 | [`docs/qips-capabilities.md`](docs/qips-capabilities.md) |
| 不知道频道、片库、搜索或个人中心 `channelid` | [`references/qips/channel-table.md`](references/qips/channel-table.md) |
| 知道场景但不知道怎么拼 | [`references/qips/vtype-recipes.md`](references/qips/vtype-recipes.md) |
| SDK 代码层调用方式 | [`references/qips/api-usage.md`](references/qips/api-usage.md) |
| 本机拉起验收 | [`references/qips/launch-checklist.md`](references/qips/launch-checklist.md) |

## 快速决策

| 用户意图 | 处理 |
| --- | --- |
| “搜/找/查询某片、角色、片单” | 执行 `video.search`，按返回 `col` 组织候选列表，必要时继续 `video.details`。 |
| “某明星资料/作品集” | 执行 `star.search`，按返回 `data` 组织明星资料和作品。 |
| “找 2026 恐怖电影 / 某频道某题材” | 执行 `video.recommend`，把条件映射为 `type` 和 `style`，按返回 `col` 组织片单。 |
| “找一些适合全家一起看的电影” | 执行 `video.recommend`，`type=Movie`，`style=["家庭"]`。 |
| “有什么热门/榜单/推荐” | 未传登录态时执行 `video.recommend`，`kind` 使用 `hot`、`soar`、`top`、`new` 或 `douban`。 |
| “播放/暂停/下一集/快进/跳频道/打开搜索页” | 优先使用内置 qips 契约拼接或执行 qips；标题、季、年份、集数直接进入 `action=play` 参数，不先调用 `/video/play`。 |
| “我没装客户端怎么办” | 返回 H5 播放地址，并给出 Mac 或 PCA/Windows/UWP 安装链接。 |
| “查我是不是会员 / 给我个性化推荐” | 当前 MVP 不做真实登录闭环；降级为热门/频道推荐或要求补充授权方案。 |

## 验收

- `npm run test:iqiyi-skill`
- `npm run test:iqiyi-qips`
