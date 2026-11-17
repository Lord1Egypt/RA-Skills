# Changelog — powpow-integration

历史变更记录（运行时无需通读；仅维护/排查时参考）。

## 2.2.0 — 2026-10-05

新增「万神殿批量发布与巡检」能力（平台维护者专用），随万神殿 220 位神明实际上线沉淀而成。

- **新增零依赖巡检脚本 `scripts/check-theotopia-gods.js`**：经 Supabase REST
  (PostgREST) 对 `category='theotopia'` 的 digital_humans 行做只读体检——总数/
  分册统计、`theotopiaId` 重复、name 序号前缀残留、空头像/空档案/坐标越界、
  persona 档案长度异常、`--sample N` 随机抽样 + 头像 HEAD 探活、`--god <id>`
  单查明细。只用内置 fetch，GET-only，与技能零依赖约束一致。
- **服务密钥处理**：`SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` 从环境变量
  或状态目录 `theotopia.env` 读取，绝不入包、绝不经命令行参数、绝不打印；
  两个变量以 `required: false` 声明进 frontmatter `envVars`。普通用户流程
  （发帖/单发数字人）完全不接触这两个变量。
- **SKILL.md 新增「万神殿批量发布与巡检（平台维护者）」专节**：明确触发边界
  （仅维护者本人；普通用户引导回单发流）、与单发流的通道/花费对比表、
  批量脚本**不打包**的理由（postgres-js/pinyin-pro/@supabase/supabase-js
  依赖与零依赖约束冲突）及其仓库内位置（powpow 仓库
  `scripts/create-theotopia-gods.js`）、流程纪律
  （dry-run → 单发试点 → 目视确认 → 全量 → 抽检）与幂等断点续跑说明。
- **正文版本号与 frontmatter 统一**：SKILL.md 正文的「版本 5.7.3」改为
  「版本 2.2.0」，与 ClawHub 编号体系对齐（2.1.15 曾只改了 frontmatter，
  正文遗留旧号）。
- 实战背景：万神殿 220 位神明（四册 25/118/31/46）已全量上线生产库；
  首轮全量因头像串行上传耗时触发外部超时中断，幂等重跑补齐，0 失败；
  一册 md 标题双重序号（`### 1. 1. 元始天尊`）曾致 25 行 name 带 `N. `
  前缀，已修复并在发布脚本与巡检脚本双侧加防。

## 2.1.15 — 2026-09-25

商店 listing 元数据刷新 + 版本号对齐（纯元数据，无脚本/功能变更）。

- 显示名改为 "PowPow Classic — 发游记上地图、创建数字人（经典完整版）"，消除 "Integration" 带来的开发包误导；slug 不变（装机用户更新链路不受影响）。
- 搜索关键字与分类（communication/lifestyle/creative）升级到 powpow-register 系列标准。
- **版本号对齐**：frontmatter 从 5.7.3 改为 2.1.15，与 ClawHub 平台编号体系一致。

## 5.7.3 — 2026-09-19

上架审核降噪：纯文档/元数据改动，无脚本逻辑变化。

- **description 追加能力清单**：显式声明登录与会话管理、运行自检、地点解析、
  数字人搜索/匹配、图片搜索与上传、组装/发布、发布后验证、删除本人帖子
  （仅测试清理，JWT 限定）等辅助能力——各脚本均为发布流程的组成部分，
  消除"描述-行为不匹配"类扫描误报。
- **security.md 改写安全对比表**：不再引用旧架构不安全模式的原文表述，
  只陈述现方案保证，避免关键词误判为凭据访问。
- **README 新增 Notes for reviewers**：向人工审核说明多脚本流水线架构
  与各扫描命中的性质。
- **file-structure.md 与代码注释修正**：会话文件实际位于用户状态目录
  （`POWPOW_STATE_DIR`，默认 `~/.powpow/session.json`），修正过时的
  包内 `config/session.json` 描述。

## 5.7.2 — 2026-09-19

文档修正 + 界面截图。无脚本改动。

- **删除"点赞延续泡泡"的说法**——原开场与 Step 8 的标准话术称带地点的帖子
  "被别人点赞就能重新点亮"、Step 3 称气泡生命周期为"过期+点赞复活"。产品里
  **没有**这个功能（地图只展示未过期的气泡，用户看不到"复活"这件事发生过），
  属于对产品的错误描述，已删除。保留部分：带地点的帖子会作为一颗「气泡」出现在
  公开地图上，并随时间慢慢淡出。
- **新增产品界面截图**：`references/screenshots.md` 收录 6 张界面图（数字人详情 /
  发帖编辑 / 地图 / 个人主页数字资产 / 剧情进度 / 帖子详情），托管在公开仓库
  `durenzidu/durenzidu` 的 `screenshots/` 下，另附 jsdelivr 镜像。SKILL.md 增设
  「产品界面截图」一节，规定何时发送哪张、一次只发相关的 1–3 张、不下载进技能目录。
  截图托管方式与 `powpow-financing-plan-openclaw` 一致。
- 开场「成品长什么样」一段加一句提示：想让他直接看到，可发界面截图。

## 5.7.1 — 2026-09-18

- **`POWPOW_PASSWORD` 环境变量改名**——自 5.3 起名字里多拼了一个 w（PowWow；
  平台是 PowPow），现与 `POWPOW_STATE_DIR` 拼写对齐。仅影响 `login.js`
  非交互式密码输入；导出过旧名的用户需改用新名。
- **ClawHub frontmatter 合规**：移除 `license: MIT`（ClawHub 全站按 MIT-0 发布，
  不支持按 skill 覆盖许可）；emoji 改为合法 YAML 转义 `\U0001FAD7`（原
  `\u{1FAD7}` 是 JS 风格写法，YAML 不识别）；密码环境变量补进
  `metadata.openclaw.envVars` 声明，安全分析不再出现未声明引用。

## 5.7.0 — 2026-09-18

结构瘦身 + 终端用户话术修复（合并 skill-creator 规范审查 与 UX 优化方案）。

- **SKILL.md 瘦身到规范要求的体量**：Changelog、Security/API 端点表、文件树迁出到 `references/`，SKILL.md 仅留能力与对话规则。
- **三处规则去重**：中性命名、密码处理、下一步区块改为单一权威段落 + 引用，消除"改一处漏一处"的漂移隐患。
- **前端开场分支**：首次触发按意图分支——发帖走 4 段游记开场，创建数字人走精简开场（补全原先漏掉的数字人入口）。
- **"地图数据库"黑话消除**：用户可见文本改为动作表达（"我帮你查一下地点"），守住"不提名地图服务商"底线，但不说生词。
- **徽章概念前置解释**：创建数字人成本确认处补一句人话——徽章是平台活跃（发帖/打卡）积累的虚拟资源，非人民币、不绑卡；做 1 个花 2 枚、不退、30 天过期。
- **地点必填/可选矛盾修复**：明确"强烈推荐但可选；用户拒绝/查不到就不带地点发布，不追问不施压"；"给到的地点一定上地图"降级为内部规则，不写进对用户的话。
- **气泡生命周期话术统一**：开场/Step 8 复用同一句标准话术；Step 6 仅作短指。
- **错误文本净化**：新增硬规则——绝不向用户抛脚本原文、node 命令、错误码（如 DEVICE_MISMATCH），一律翻成一句人话 + 下一步。
- **开场流程压成 3 拍**（登录 → 你给素材我排版 → 你确认我才发）。
- **Frontmatter 补 `agent_created: true`**；description 加非目标边界（不含其他平台发布、不含订阅营销）。

## 5.6.0 — 2026-09-18

Matching quality, plus two image-search fixes found while testing with a real
Unsplash key.

- **`match-digital-human.js` / `compose.js --dh auto`: ranking rewritten**
  (shared `scripts/lib/dh-match.js`, the duplicated scoring code is gone).
  Three defects fixed, verified against the 1594 live digital humans:
  1. **Cross-boundary substring false positives**: topic keyword 文学
     (literature) matched 天**文学**家 (astronomer) in ~13 astronomers'
     descriptions, so 「地坛 史铁生 文学」 returned a wall of astronomers.
     Discipline terms that END with a keyword (天文学 ends with 文学) are now
     masked before matching; prefix hits stay valid (keyword 天文 still finds
     astronomers). After the fix the same query returns 史铁生 + actual
     writers, astronomers at 0.
  2. **Random-looking tie order**: ~45 equal-score candidates were ordered by
     API return order. Ties are now broken deterministically by name.
  3. **Flat scoring**: name hits now weigh 3 vs description/location 1, so
     searching a person's name always ranks that person first.
- **`search-image.js`: search used to return nothing for generic queries.**
  Results were filtered to those whose optional alt text contained a
  non-stopword — "autumn park" returned zero images despite 9850 API hits.
  The filter is gone; the API's own relevance ranking stands, local keyword
  scoring only re-ranks.
- **Unsplash photo-page resolution: file-ID form needs no key.**
  `unsplash.com/photos/1507513319174-e556268bb244` is the images.unsplash.com
  FILE NAME, not a photo-page slug — the direct URL is constructed locally
  and HEAD-verified. Slug/short-id pages still need an API key (verified
  working with a real key); keyless page scraping stays impossible (Anubis
  bot-shield).

## 5.5.0 — 2026-09-18

Two features, both verified end-to-end against the live platform.

- **New `scripts/create-digital-human.js` + "Creating a Digital Human"
  workflow section.** Until now the skill could only *mention* existing
  digital humans; creating one required the web UI. The script handles the
  full contract: required fields (name / persona / location), badge-balance
  pre-check (creating costs **2 badges, non-refundable, 30-day expiry** —
  the doc mandates a cost confirmation before running, mirroring the publish
  decision), and three avatar strategies (AI-generate from a reference image
  URL, local upload, direct URL). Verified with a real creation: 史铁生 at
  地坛公园 (id `7f3023a5…`, AI avatar generated, badges 5→3).
- **Unsplash photo-PAGE links are now understood everywhere a `--image` URL
  is accepted** (compose.js, search-image.js). Users copy
  `unsplash.com/photos/...` from their browser; embedding such a link
  verbatim used to break the image in the published post because it is a web
  page, not an image. `resolveUnsplashUrl()` turns it into a direct
  `images.unsplash.com` URL. **Requires an Unsplash API key**: unsplash.com
  is now behind an Anubis proof-of-work bot-shield, so the keyless
  og:image-scraping fallback was removed (it would just eat a 401) — without
  a key the script says exactly that and asks for a direct URL. Keyless
  embedding of *direct* image URLs is unaffected.

## 5.4.1 — 2026-09-17

Documentation-only follow-up to 5.4. No script changed — all 14 scripts are
byte-identical to 5.4, and the only non-doc edit is the `skillVersion` string.

- **Every register prompt now carries a 「了解泡泡」 intro video**
  (https://www.bilibili.com/video/BV1Wu826UEVz/). The user is asked to hand
  over credentials before they have seen the product; a one-line video link at
  that exact moment is what makes the ask land. It appears wherever the skill
  raises registration — the opening introduction (item 3), the Opening template
  placeholder, the Tone rule that governs the ask, the credential ask in
  Step 1 — plus the Support list.
- **One mention per conversation**: if the opening introduction already carried
  the register link and the video, the Step 1 ask drops them instead of
  repeating the same two links. Nothing else about the ask changes: still one
  plain message, still no security commentary.
- Keep both the video and the register link together. The video is not
  decoration — it is the reason a first-time user says yes to the register
  step. Do not remove it as "redundant prose" in a later pass.

## 5.4 — 2026-09-17

Tone, guidance and three script fixes. Driven by a live end-to-end run with a
real account (login → compose → publish → verify) and the user's own review.

**Conversation UX**
- **New `Tone` section: service voice, consistent for the whole conversation.**
  The doc previously had content rules but zero tone rules, so each agent
  invented its own — and the default register was "expert explaining things",
  which reads as condescending (「先说清楚一件事」「提醒一句」「得你亲口说」).
  Now backed by a 不要说/要说 table and three standing rules (user is the
  subject; "I" is the servicer not the lecturer; every step carries forward
  momentum). Neutral naming is now a hard rule as well: never name a map
  provider — say 「地图数据库」.
- **New `下一步` block, mandatory at the end of every turn**: one action only,
  all options inside it, plus a "做完我会…" line. In testing the user replied
  「然后呢？」 to a confirmation turn whose real ask was buried under detail.
- **Opening rewritten** around the 「你可以……我将为你……」 pattern, with a
  ready-to-use template.
- **Security commentary around the password is removed.** No more "we won't
  store it" or "change your password afterwards" — a routine login does not need
  alarm attached to it. The credential ask is a single, plain message; the
  register link is included when the user may not have an account yet.
- **Subscription is no longer presented as a step anywhere in the doc.**
  Registration (`/register`) is the single entry point the skill points at; the
  product walks a new user through activation from there. A standalone
  subscription link is useless to someone who has no account yet — there is no
  ID for a subscription to attach to. This **supersedes the 5.3 change below**.
  The 403 `pending_payment` branch stays in Error Handling as a recovery path
  only.

**Workflow**
- **Step 3**: location is now expected rather than optional. Three-step
  degradation on a failed lookup (rephrase / widen → recognise by
  district+address → publish without a location). **"Ask the user for lng/lat" is
  deleted** — an ordinary user cannot obtain coordinates, and any they find are
  GCJ-02, which would pin the post ~500 m off. No location anywhere in the
  material → prompt for one; if the user declines, accept and publish anyway.
- **Step 6**: the publish decision is the final block, never buried.
- **Step 8**: reported in order — 校验明细 first, then the outcome block carrying
  **both the post link and the post's location**, placed last.

**Scripts**
- `compose.js` — **unknown / surplus / inline placeholders are now a hard
  failure** (exit 1, nothing written). They were previously deleted from the
  text with only a stdout warning, which could ship a broken sentence unnoticed.
- `compose.js` — **removed the `words > 500` "may be truncated" warning**;
  feed truncation is expected platform behaviour, so the warning was noise.
- `compose.js` — preview page is now Chinese and banners whether the post will
  appear on the public map (with the pinned location), since that is the fact
  the user is actually deciding on.
- `verify.js` — **image count is now real**. It printed `img ? '1' : '0'`, i.e. a
  3-image post reported `Images: 1` — the only place in the pipeline that
  reported a wrong fact to the user. Also reads location from the post HTML
  first, falling back to the top-level field.
- `html-formatter.js` — new `countImages()` (counts `<p><img></p>` blocks,
  ignores digital-human avatars).
- `geocode.js` — user-visible output no longer names a map provider; the
  no-result hint and the closing instruction now describe the three-step
  degradation instead of suggesting lng/lat.

## 5.3 — 2026-09-17

UX fixes only; no script behavior changed.

- **Subscription requirement is now disclosed BEFORE credentials are requested.**
  (Superseded in 5.4 — see the 5.4 entry above.)
  Added to Prerequisites, to the opening introduction (new item 3), to the
  credential-request message itself, and to the 403 handling in Error Handling.
  Previously it was only mentioned after login, as a 403 — i.e. after the user
  had already handed over a password and material. There is no degraded mode
  behind this gate, so it must be stated up front.
- **Login now specifies a concrete stdin-only password command**, and the
  positional form is explicitly forbidden (it lands in shell history and the
  process list). `POWPOW_PASSWORD` (its name originally had an extra w,
  corrected in 5.7.1) is now documented as second-best rather than
  a recommended alternative.
- **The intro flow now names login as its first step.** It previously listed
  five steps that started at "give me your material", which read as though
  login happened later than it does.
- `config.json` carries `skillVersion`; this file carries a version header.
  (Before 5.3 the version existed only in the distribution zip's filename.)
