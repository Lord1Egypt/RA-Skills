---
name: luan-xhs-skill
description: "End-to-end Xiaohongshu operations including positioning, topic research, content production, publish execution, and post-incident recovery. Reusable across verticals with templates and a concrete 陪你看剧 case preset. Use when the user asks to publish or manage Xiaohongshu posts, prepare Xiaohongshu drafts, log in to the creator platform, reply to Xiaohongshu comments, troubleshoot Xiaohongshu web publishing flows, or control publish visibility/private mode/scheduled publishing."
---

# Openclaw 小红书运营技能（通用版）

目标：构建可复用的“小红书运营”流程，让任何账号类型都能复用同一套动作框架。

## 适用范围（默认即通用流程）

- 账号定位与内容方向
- 选题产出与争议点挖掘
- 竞品/同类账号对标
- 小红书发布前演练与内容交付
- 发布后快速复盘（互动结构、评论回复、热点追踪）
- 小红书创作服务平台登录、会话恢复、网页端直发
- 小红书视频笔记发布与视频上传问题排查

将每类账号的行业细节作为“案例模块（case module）”挂载到通用流程中。

## 常用术语

- `选题`：可发布、可讨论、可转发的内容切入点
- `引流钩子`：标题/开头一句用于触发停留与点击
- `结构化输出`：标题、正文、互动问句、话题、标签五元组
- `快照`：用于验证页面状态的关键证据快照
- `回放`：流程失败后重试或改道执行

## 0) 启动与环境校验（所有任务都遵循）

执行前先按 `references/xhs-runtime-rules.md` 中“运行规则”执行，优先遵循失败可复用顺序。

- **发布相关默认优先走创作服务平台：`https://creator.xiaohongshu.com`**，不要先在社区首页 `www.xiaohongshu.com` 判断发布登录态。
- 默认读取 `_meta.json`，当 `config.useProxy=false` 时先调用 `scripts/disable_proxy.js` 清空代理环境变量；否则很容易触发风控或登录态异常。
- 以 `evaluate` 为先，关键节点少量 `snapshot`，单步动作最多重试一次。
- 失败后保留已获结果，切稳健路径并汇报。
- 涉及直接发布时，优先使用已验证脚本：
  - `scripts/xhs_login_sms.js`：短信验证码登录；若平台切成强制扫码，会明确报 `QR_REQUIRED`
  - `scripts/xhs_login_qr.js`：创作平台专用二维码登录并保存会话
  - `scripts/xhs_publish_with_saved_session.js`：使用保存会话直接发布图文
  - `scripts/xhs_publish_video.js`：使用保存会话直接发布视频（已验证可用）
  - `scripts/xhs_make_text_cover.py`：无素材时生成兜底封面

## 1) 技能默认行为（所有任务都遵循）

- **先读本技能目录下的 `persona.md`**（小红书平台专用人设/语气/发布与回复风格）。所有对外文案（发帖/评论回复/私信话术）都必须遵循。
- 优先输出可执行的 SOP 而非一次性内容稿。
- 语言优先“能对话”而不是“写报告”：短句、口语、站位明确、可引导评论。
- 所有输出默认保留“可追问点”，用于评论区继续延展。
- **默认文案风格要像正常真人发帖。** 除非用户明确要求，不要自动注入 `行行行 / 我不说太多 / 我继续打工了 / 我去躺会儿 / 电子宠物` 这类人设口头禅或自我表演。
- 用户明确要求“发出去 / 帮我发 / 直接发布”时，可以走直发链路；用户只要求“准备 / 预览 / 演练”时，默认停在发布前。

## 2) 账号定位（可复用）

每个账号先确认 4 个变量：

- 目标用户：年龄/场景/痛点（如「下班后碎片时间」「追星讨论人群」）
- 内容价值主张：每篇给用户什么（观点、情绪价值、实操建议）
- 差异化角度：同类账号不做什么、你做什么
- 风格规范：语气、长度、冲突边界（避免过激）

输出：

- 人设关键词（3-5）
- 内容支柱（3 个）
- 口头禅/固定句式（2-3 个）
- 不能碰底线（红线）清单（剧透、人身攻击、虚假承诺）

## 3) 通用选题与对标流程

### A. 平台侧抓取信号（可并行）

1. 先在小红书抓同题材高互动内容（点赞/收藏/评论高于近期平均值）
2. 记录可复用字段：`title`, `hook`, `angle`, `结构标签`, `评论信号`, `互动CTA`, `标签组`
3. 汇总前 10-20 条到候选池

### B. 需求侧补充信号（行业/场景）

1. 按主题去主流平台/社媒抓“评论区观点分歧”
2. 抽取支持/反对/中性观点各一组
3. 输出可发文争论点（争议但可控）

### C. 形成选题清单（每轮至少 3 条）

每条选题包含：

- 选题标题（20 字内可选）
- 观点标签（支持/反对/中性）
- 预计互动钩子
- 证据来源（哪组高互动数据）
- 风险提示（是否容易踩线）

## 3.5) 搜索并浏览（新增操作类型）

按 `references/xhs-runtime-rules.md` 的搜索与评论入口章节执行。

- 只允许从搜索结果页进入帖子；
- 优先通知/回复场景前先对位校验。
- 连续失败回退策略见引用文件。

## 4) 通用内容模板（小红书）

每次产出至少 2 个备选：

- 标题（争议/立场/反问，≤20字优先）
- 默认避免强行玩梗、自说自话、莫名嘴硬；先把图/视频里真正值得说的内容写出来。
- 开头钩子（1-2 句）
- 正文（3 段：观点→证据→反方）
- 互动提问（1 句）
- 话题（5-8 个）
- 风险标注（是否剧透 / 引战边界 / 版权风险）

## 5) 通用发布链路

详细发布执行路径请直接按 `references/xhs-publish-flows.md` 执行，避免重复维护。

### 默认策略

- **用户明确说“发出去 / 直接发布 / 帮我发”时，允许直发，不必默认停在发布前。**
- 用户只说“演练 / 预览 / 帮我准备一下”时，才停在发布按钮前。
- 发布前必须满足三要素：**封面、标题、正文**。
- **没有现成图片时，不要卡住。** 先用 `scripts/xhs_make_text_cover.py` 生成一张简洁兜底封面，再按图文链路发布。
- 优先发布 **图文笔记**；用户明确要求视频时，优先走 `scripts/xhs_publish_video.js`。
- 视频发布不要误判：只有页面出现 `视频文件 / 重新上传 / 设置封面 / 标题框 / 正文编辑器 / 暂存离开 / 发布` 这一整组信号，才算真正进入视频编辑页。

### 已验证的稳定链路

1. 先在 `creator.xiaohongshu.com/new/home` 验证会话是否有效。
2. 如果跳到登录页，先判断登录方式：
   - 普通短信页：走 `scripts/xhs_login_sms.js`
   - 若页面出现“APP扫一扫登录 / 为保护账号安全 / 请使用已登录该账号的小红书APP扫码登录身份”，直接改走 `scripts/xhs_login_qr.js`。
3. 进入 `creator.xiaohongshu.com/publish/publish` 后，**主动切到“上传图文”**，不要假设默认 tab 正确。
4. 上传图片后，等待标题框 `填写标题会有更多赞哦` 和正文编辑器 `.tiptap.ProseMirror` 出现，再填内容。
5. 点“发布”后，**必须再去“笔记管理”确认标题已出现**，以此作为成功标准；仅看到 `published=true` 还不够。

### 推荐脚本入口

- 短信登录：`node scripts/xhs_login_sms.js --phone 13xxxxxxxxx`
- 二维码登录：`node scripts/xhs_login_qr.js`
- 图文发布：`node scripts/xhs_publish_with_saved_session.js --title "标题" --body "正文" --image /path/to/image.png`
- 视频发布：`node scripts/xhs_publish_video.js --video /path/to/video.mp4 --title "标题" --body "正文"`
- `--body` 若传入字面量 `\n`，脚本会自动转成真实换行，避免把 `\n` 原样发进正文。
- 可见性：`--visibility public|private|mutual`
- 定时发布：`--schedule`（启用平台默认时间）或 `--schedule-at "YYYY-MM-DD HH:mm"`（若页面接受则按指定时间）
- 无图兜底：`python3 scripts/xhs_make_text_cover.py --title "标题" --output /tmp/xhs_cover.png`

## 6) 评论与回复（轻量）

评论检查与回复统一遵循 `references/xhs-comment-ops.md`，并结合 `examples/reply-examples.md` 作文案风格。

- 默认优先走通知页，先对位后输入后发送。
- 默认 one-send-per-turn（如无明确要求不连发）。
- 长度、隐性承诺、风控停损点等风险控制项请以引用文件为准。

## 7) 失败与修复（必须遵循）

- 自动化失败先重试一次（同策略）。
- 仍失败则改道：换到“更稳妥同义路径”。
- 不做无效重复动作；保留当前进度可复用，报告一次用户需手动的单一动作。
- 发布失败优先按这个顺序排查：**代理 → 创作服务平台登录态 → 登录方式是否被平台切成强制扫码 → 发布页 tab 是否正确 → 发布后是否在笔记管理出现**。

## 8) 通用提取示例（Evaluate）

通用字段提取脚本示例见 `references/xhs-eval-patterns.md`。

## 9) 具体案例：陪你看剧（保留为特例）

### 使用方式

本技能主文件保留通用框架；垂直行业经验放在 `examples/` 目录，按内容类型选用：

- 先按《通用流程》跑一遍
- 再加载对应案例文件补齐行业特殊动作

当前已可用案例：

- `examples/drama-watch/case.md`（陪你看剧账号）

每个内容类型按目录组织，文件命名可为：

- `examples/<vertical>/<vertical>.md`（推荐）
- 或 `examples/<vertical>/README.md`

- `examples/lifestyle/`（待补充）
- `examples/cosmetics/`（待补充）
- `examples/fitness/`（待补充）

---

## 实操经验（持续有效）

- **发布鉴权以创作服务平台为准，不以社区首页为准。** 社区首页可能“看起来能浏览”，但创作平台仍是未登录状态。
- **默认关代理再跑发布。** 当前技能配置 `useProxy=false`；若环境里挂着 `HTTP_PROXY/HTTPS_PROXY`，先清掉再访问小红书。
- 创作服务平台的发布页默认可能落在“上传视频”，所以做图文时要**主动切“上传图文”**。
- 视频页里真正的可用上传控件是 `input.upload-input`，即使不可见也能直接 `setInputFiles()`。
- 视频上传成功后，页面不一定马上出现标题框；要先看是否出现 `视频文件 / 重新上传 / 设置封面 / 智能标题 / 暂存离开 / 发布` 这些编辑信号。
- 视频发布按钮经常会先出现但处于 disabled，通常是因为**标题/正文还没填**，不是上传失败。
- 文案输入前先做正文归一化：把字面量 `\n` 转成真实换行，避免把转义字符直接写进小红书正文。
- 发布话题优先用 UI 选题，不建议纯文本粘贴大量 `#话题`。
- `evaluate` 批量改写富文本时，尽量少改版式，避免丢失 topic entity。
- **`published=true` 不是最终成功信号**；必须进入“笔记管理”并看到目标标题出现，才算发布成功。
- 没有现成封面时，直接生成兜底封面比卡在“缺图”更稳。
- 若出现新类型评论节奏问题，优先减少每小时回复密度而非提高频率。

## 运营成熟路径（可选）

- 标题池：按“站队/反问/冲突”各保留 10 条可复用模板
- 话题池：按账号调性建立常用关键词与同义替换列表
- 复用机制：每次复盘后把可复用表达同步进案例文件
