# Changelog / 变更日志

All notable changes to the `meta-analysis` skill are recorded here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), versioning follows [Semantic Semantic Versioning](https://semver.org/).

---

## [2.20.1] — 2026-10-09 — 工作台快速通道 504 根治 + skillname 落库口径统一

### Archived — 架构整理（2026-10-08）

- 根目录 `RELEASE_REVIEW.md`（2026-09-01 发布评审清单，一次性用途，零引用）归档至 `_archive/`。

### Fixed — 工作台快速通道 504（流程C「启动失败：<!DOCTYPE html>…」）

- **根因**：Block C 快速通道（`POST /api/start_data`，draft/raw_csv）在请求内同步跑
  `_advance`（C1 初稿含 LLM 扩写，实测 47~70s），恰好压在 Cloudflare 网关 ~60s 超时线上，
  时好时坏 504；前端把网关 HTML 错误页前 300 字符当错误详情展示，故用户看到乱码报错。
  线上复现：同一请求 56.7s 成功 / 60.8s 504。
- **方案 A（根治·异步化）**：`fullflow.run_fastpath` 新增 `defer_advance`——raw_csv/draft
  建会话、落 `starting:{status:advancing}` 即返回（实测 0.24s / 0.81s），计算转后台任务执行
  （新增 `advance_started_session`，终态写 done/error + elapsed_sec，异常全兜底）；
  `build_state` 透出 `starting`。前端检测到 advancing → 每 3s 轮询会话直到 done/error
  再渲染，进度条显示「后台计算中 Ns」。
- **方案 B（兜底）**：前端对 504/502 不再判失败，提示「已在服务器继续处理，可从历史会话打开」。
- **验证**：本地双端口冒烟——draft：0.24s 返回 advancing → 47.5s done → 停 C1.draft 软停闸、
  初稿产出；raw_csv：0.81s → 22.3s done → 停 B1.meta_analysis。pdf 模式不经后台推进，行为不变。
- 落点：`adapters/fullflow.py` + 工作台 `server.py`/`workbench.html`（工作台前端不进技能
  发布包，随线上应用更新）。**线上 meta.app 需重新发布后生效（等确认）。**

### Changed — `skillname` 落库口径统一为 `meta-analysis`（2026-10-05）

- **标准（用户裁定）**：coze 端写飞书日志表的 `skillname` 恒等于技能的 `name` / `slug` =
  **`meta-analysis`**，**不得简写为 `meta`**。
- **修正**：`adapters/coze/src/graphs/nodes/feishu_write_node.py` 文件头注释（原写 `'meta'`）
  与 `adapters/coze/coze_contract.md` 飞书写入段（原写 `` `skillname`（`meta`，2026-08-19 由
  samplesize 更正） ``）已统一为 `meta-analysis`。代码常量 `SKILL_NAME = "meta-analysis"` 本就
  正确，**无逻辑改动**，仅消除文档 / 注释漂移。
- **`meta` 的两处合法残留**（均与技能名无关）：① WorkBuddy 应用 `domainPrefix`（已登记白名单
  特例，`https://meta.app.workbuddy.host/`）；② R 包名 `meta`。
- **生效条件**：`adapters/coze/` 为远端镜像（目录级排除、不进发布包、不受 git 跟踪），本地修正
  **不会自动上线**——需人工重新部署 coze 镜像后，线上 `skillname` 才确定落 `meta-analysis`。
- **统计口径提示**：CHANGELOG 早期条目中按 `skillname=meta` 统计的 322 条属旧口径，按技能名
  统计调用量时需与 `meta-analysis` 记录归并。

## [2.20.0] — 2026-09-27 — 全流程支持：从选题到投稿的端到端 Meta 分析

### Added

- **选题 → 投稿全流程支持**：meta-analysis 技能现覆盖系统评价/Meta 分析的完整生命周期——① 选题方向判断（topic assessment，含查新与可行性评估）② 文献检索与整理（Europe PMC / OpenAlex / biorxiv/medrxiv 多源检索、去重、筛选）③ 数据提取（A4 数值提取通道）④ 统计分析（23 种分析 + 图形，R 引擎云端计算）⑤ 研究质量评估（RoB 2.0 / AMSTAR-2 / GRADE）⑥ 论文撰写（writing-advisor，11 节结构化初稿）⑦ 投稿建议（期刊匹配与投稿策略）。用户从零开始到投稿-ready 一站式完成。

## [2.17.2] — 2026-09-27 — 开发期结束：coze 路由回切 ct-meta 主 / ct-meta2 备

### Changed

- **删除 `adapters/DEV_POLICY.json`**：开发期策略文件已移除，coze_client 路由恢复生产态 —— `DEFAULT_ENDPOINT = https://ct-meta.coze.site/run`（主），`FALLBACK_ENDPOINT = https://ct-meta2.coze.site/run`（备）。token 按端点分别取用（ct-meta 用旧 JWT aud=oxwSsfwdtRRfByYIM8Xg3U4RQH5OgEjO；ct-meta2 用新 JWT aud=5v9HMQWtTSzxrEeZjI7kJJEzeMPrHXny）。
- **回退逻辑恢复**：主端点 token 鉴权失败（401/403 + token 关键字）时自动回退到 ct-meta2，附 `_coze_endpoint_notice` 提示。

## [2.17.1] — 2026-09-27 — 文档瘦身（SKILL.md 334→200 行，章节外迁 + README 结构对齐）

### Changed

- **SKILL.md 行数从 334 → 200（-40%）**：大量章节从 SKILL.md 移入独立 references 文件，内容零丢失。
  - §2.3 上游编排细节 + §2.4 CCM/全流程模式 → `references/chat_orchestration.md`（writing-advisor、evidence-upload、A-stage contract、type-confirmation model、完整 CCM 归档）
  - §2.5 工作台元数据 + 发布命令 + 能力表 → `references/workbench.md`（含 appId/share-link/publish-toolchain/local-launch 全套）
  - §5.1 跨轮连续性 + endpoint capability boundaries → `references/cross_turn.md`
  - §4/§5/§6/§7/§8 保留摘要骨架（约 30 行），细节指向 ADVANCED.md / data_templates.md / bug_report_endpoint.md
  - §3 初始化精简为 2 行指向 ADVANCED.md

- **README §2 大类顺序重排 + §1 示例对齐**（详见 README commit）：⑦ 系统评价流程 → ①，①–⑥ 顺延为 ②–⑦；§1 示例删 grill-me + PRISMA 旧示例，新增⑤⑥⑦三示例，7 个示例与 7 大类一一对应。中英双语同步。

## [2.17.0] — 2026-09-27 — 屏蔽收口 + 发布前检查整改：A4 旁路闸门、CCM 停用、工作台四项修复

### Changed

- **发布前检查整改（§16.8）**：`publish_inject.py` 重新注入共享件——`scripts/i18n.py` 修复**陈旧快照缺陷**（meta 旧副本缺 `resolve_user_language` / `detect_text_language`，而 `coze_client.py` / `build_request.py` 的出站语言判定已上移依赖它们），同步 `office_to_md.py`（+xlsx 支持）与 `drug_name_resolver` / `excel_style` / `keyword_breadth` / `source_guard` / `merge_spec` / term_map / drug_name_map；`shared_sync_check` 由 4 漂移 → **全部一致 ✓**。已知豁免 2 项：`r_libs`（.venv 内 cffi `get_other_libs` 子串误报，零真实引用）、`kw_localize`（block_a 设计为运行时回落 ct-base 权威；本次注入后自带 bundled 副本）。`i18n_messages` 缺失的 39 键全为 `hub.*`（Hub 导航，meta 零引用）——合法裁剪。

- **CCM 对话上下文菜单全面停用（2026-09-27，用户裁定）**：技能执行面收敛为两种——① 网页应用（meta.app，菜单式引导）② 上下文对话（agent 自然语言叙述阶段状态 + 开放提问）。A/B/C 所有节点的人工闸**不再在聊天中渲染 flow_menu 菜单 / L0 导航条 / flow_menu_widget 可点卡片**。`flow_menu.py` / `flow_menu_widget.py` 降级为开发者 CLI 工具，fullflow 状态机、红线闸、审计留痕全部不变。改动面：SKILL.md §2.4 顶部加 DISABLED 横幅（含替代行为规范：到达人工闸时以散文陈述进度并直接提问，或引导至网页应用），原 CCM 实现段标 [ARCHIVED]、widget 子条目就地标 ⛔ disabled；`references/conversation_flow_menu.md` 头部加停用横幅（保留作设计归档，供日后重新启用）。解冻 = 撤两处横幅（本文 + SKILL.md）。
- **A4 自动数值提取全面屏蔽——旁路收口（2026-09-27，用户指令）**：主开关 `features.a4_extraction=False`（2026-09-17 裁定）已让 A4 节点降级为纯 PDF 下载、`_a4_extract_pdf` 短路，但排查发现 **3 处直连 `pdf_extractor.extract()` 的后端旁路不受开关控制**：`POST /api/upload_pdf`、`POST /api/upload_pdf_auto`（补传 PDF 即时抽 2×2 表）、`POST /api/start_data data_mode="pdf"`（PDF 快速通道；前端入口 `fastpath_pdf` 虽已隐藏，但直接打 API 仍可触发抽取）。三处统一加 `features.a4_extraction_enabled()` 闸门（关闭时 409 + 指引改用「自备原始数据」通道）；TestClient 实测三条全返 409。解冻 = 把 `FEATURES["a4_extraction"]` 改回 True（或 `CT_FEATURE_A4_EXTRACTION=1`），旁路自动恢复。`features.py` 注释同步收口说明。
- **工作台（meta.app）2026-09-27 六项改动，同日多次覆盖发布（appId 不变、链接 `https://meta.app.workbuddy.host/`）**：
  - 顶栏「审计」按钮冻结——去 onclick、加 `disabled`，面板恒收起（保留 localStorage 恢复语句为注释，解冻一行还原）。
  - 「反馈」对话框携带上下文（参考 ct-samplesize §20.3.5）：`wbBugDiag` 补 lang/backend/url/ts；`wbOpenBug` 把【上下文（发送前可删改）】预填进描述框；server `/api/bug-report` 借白名单内 `engine_status`（截 600 字符）携带 diagnostics（此前整字段丢弃）；`bug_report.SKILL_VERSION` 改为运行时读 SKILL.md frontmatter（原硬编码 1.0.0 漂移）；`build_publish.py` 白名单 + REQUIRED 纳入 `SKILL.md`。
  - 「反馈」按钮加 bug SVG 图标（`svg.wb-ico`，同审计按钮规格）；`data-i18n` 从按钮移到内层 span，防 `wbLocalize()` textContent 赋值抹掉图标。
  - 选题可行性速览 TDZ 修复（见 Fixed）。
  - 快速通道主题改**选填**（用户裁定方案 A）：raw_csv / draft 空主题放行（Block B 计算零依赖主题，Block C 有 no_topic 警告条兜底）；server 校验按 data_mode 分支（standard/pdf 仍必填）+ `topic: Form("")`（否则 FastAPI 先 422）；前端 `doStart()` 必填拦截限定 standard，模式切换显示 `#topic-opt-hint` 提示行。
  - 选题速览面板加「ℹ️ 简化分析说明」提示条：明示网页应用提供简化分析（命中数探针 + 本地确定性评分），完整评估（PICO / R1–R6 / PROSPERO 查重 / AMSTAR-2 / 11 节报告）需安装技能在对话中进行。

### Fixed

- **选题可行性速览 JS TDZ 崩溃（2026-09-27，线上报障）**：`Cannot access 'radarHtml' before initialization`——09-24 加雷达图时 `const radarHtml` 声明在 `scoreHtml` IIFE **之后**，而 IIFE 模板字符串引用它，求值即抛；仅当 A1 探针返回 `topic_analysis.scores` 时触发。修复：声明提前至 `scoreHtml` 之前、删除后部重复声明（全文恰 1 处），留警示注释。线上验证首页 MD5 一致。
- **发布版接入 ct-base §12 后台大模型 LongCat-2.0 + 修复「后端未连接」误报（2026-09-25）**：
  - **背景**：云端 sandbox 无 `~/.workbuddy/models.json` 与 LLM 环境变量 → `topic_translate._candidates()` 为空 → 中文主题自动翻译在发布版上**静默失效**（境外库 0 命中老坑的另一种形态）。按 ct-base `references/workbench_ui.md` §12（家族统一 LongCat-2.0，2026-09-25 起）接入：新增 `adapters/llm_loader.py`（ct-base 拷贝）+ `config/llm_key.py`（XOR 混淆公用 key，不落明文），`_candidates()` 末尾追加 LongCat-2.0 兜底候选（`LONGCAT_API_KEY` 环境变量 > 混淆文件；本地 models.json 命中更快源时行为不变）。两文件入 `WHITELIST_FILES` + `REQUIRED_IN_PAYLOAD` 自检（漏发=静默丢功能类）。验证：载荷级模拟 sandbox（`WORKBUDDY_MODELS_JSON=/nonexistent`）起服，`/api/topic_help` 返回 LongCat 翻译的英文检索式；线上中文主题实测 `semaglutide cardiovascular outcomes…` ✓。
  - **「后端未连接」误报**：sandbox 冷启动首请求 >2s，而前端 `wbProbeBackend` 是**单次 2s 超时探测**、失败后永不再试 → 页面永显离线（`/health` 实测热态 0.45s、服务本身正常）。修复：探测改为带退避的多次重试（2s→3s→5s→8s，间隔 400ms，任一成功即「后端就绪」），并给状态 pill 加「点击重新探测」兜底。线上回归：新逻辑已在首页、`/health`、`/api/features`、翻译链路全绿。
  - 重发布：沿用 appId 覆盖，链接不变 `https://meta.app.workbuddy.host/`（载荷 35 文件、自检 + py3.11 守卫通过）。

- **重新发布应用（2026-09-25）+ 线上 3.11 语法回归修复**：首次部署失败——线上 import `block_c.py:882` 抛 `SyntaxError: unterminated string literal`（C1 摘要段的 f-string 把三元条件在 `{ }` 内折行续写，PEP 701 跨行表达式仅 3.12+ 合法；本地 3.13 编译通过故未拦截）。修复：条件表达式提出 f-string 存 `_synth_part` 变量。
  - **守门盲区补齐**：`check_py311.py` 此前只查「表达式内反斜杠」，漏掉跨行与同引号两类 PEP 701 放宽。已增 `fstring-expr-multiline` / `fstring-expr-same-quote` 规则（三引号外层自动跳过 same-quote，避免合法嵌套单引号误报），并用本次事故代码做复现自测：旧版 0 检出、新版精准命中 1。全树重扫：源码树 0 问题（唯一命中即该未同步的旧载荷副本，重建后清零）。
  - **发布结果**：重建载荷（33 文件自检全过 + py3.11 守卫通过）→ 本地冒烟（`python main.py` 起服、`/health` ok、首页 200）→ 沿用 appId `wbapp_hNZl928SI6wByvJt2COtcC` 覆盖发布成功，链接不变 `https://meta.app.workbuddy.host/`。线上回归：`/health` ok、`/` 200、`/api/features` 正常下发（a4_extraction=false）、别名域 `meta.app.workbuddy.link` 200。

- **代码完备性检查（2026-09-17，针对原版目录 `meta-analysis`，不含副本）**：系统性核验全链路，结论如下：
  - **发布载荷同步回归修复（9/17–9/19 白名单模式引入）**：白名单取代整目录同步时漏列发布入口 `main.py` 与 6 个 `adapters/` 依赖（`registry_probe` / `prospero_probe` / `quality_advice` / `interpretation` / `topic_assess` / `session_store`），导致 `build_publish` 自检报「载荷缺少 main.py」、线上 `python main.py` 起不来。已补齐 `main.py`（根级，加 `adapters/`、`adapters/workbench/` 到 `sys.path` 后 `import server` 跑 uvicorn）并加入 `WHITELIST_FILES`；本地模拟线上 `PORT=8899 python main.py` 启动成功、`/health` 返回 `{"ok":true,"version":"0.1.0"}`。
  - **A/B/C 全节点 schema 字段一致性（#25）**：逐一核对 `form_schema.py` 各节点 `panel.path` 与后端 `_mk_stage` 实际写入字段，全部对得上——A1 读 `stage.picos/missing_dimensions/registry_probe/feasibility` + `editable.report/include_reviews/sources`（EDITABLE_KEYS 含三项）；A2 读 `nha.coverage/summary/decisions`；A3 读 `stage.n_screened/n_downloaded/n_failed/n_needs_upload` + `editable.pdf_dir`；B4 读 `editable.report`；C1 读 `editable.manuscript/sections`；C2/C3/C4 读 `path="stage"`（前端 `workbench.html:1869` 映射 `stage→stage_result`，数据可正常显示，非「读错键」）。
  - **测试套件可运行性（#26，离线）**：`check_py311`（py3.11 兼容守门）扫描 `adapters/` 124 文件 0 问题；`test_interpretation` 19/19、`test_envelope_guard` 47/47、`test_flow_menu` 198/0、`test_rewind_rollback`（回滚子集 PASS）、`test_pdf_extractor` 16/16 全绿。⚠️ `test_fullflow.py` 当前 6 失败（默认 A4 隐藏）/ 4 失败+1 错误（开 A4）：根因为测试滞后于多次架构变更（`B1.meta→B1.meta_analysis` 改名、A4 默认隐藏、决策端点报错文案变更），其中「`stage_id 不匹配`」是生产端点正确拒绝非法 `stage_id=None`，非代码 bug——该测试需按当前流程刷新（不在本完备性检查范围内，单列待办）。
  - **残留脏文件（已清理 2026-09-25）**：删除 `adapters/block_a.py.new`（3303 行，较 `block_a.py` 少 123 行，缺 `import prospero_probe`、`_try_coze_topic_assessment` 等，属合并残留）与 `adapters/run_analysis.py.bak`（备份副本）。两者均未被 git 跟踪、不在 `WHITELIST_FILES`，删除后正本 `py_compile` 通过，无功能影响。

- **工作台 ↔ 上下文一致性审计：13 项 + 写日志时顺带发现 1 项，全部处理（2026-09-22）**：
  对「网页工作台」与「CCM 上下文菜单」两条入口做逐项比对，发现两侧对同一状态机的口径存在
  13 处不一致（2×P0 / 6×P1 / 5×P2）；另在整理本轮日志时发现第 14 处同类漂移（R 引擎指纹，见下）。
  裁定原则：**能补入口就补入口，补不了才收配置；不删功能，只求两侧一致。**
  - **P0 · `B1` stage id 漂移（影响最大）**：真源是 `block_b.B1 = "B1.meta_analysis"`，但
    `form_schema.STAGE_ORDER` / `TITLE_EN` / `flow_menu._EN_SHORT` 三处写成 `B1.meta`。
    因 `SCHEMA` 有 `B1.meta` 别名兜底，**页面渲染完全正常、bug 被长期掩盖**，真正崩的是三处次生故障：
    ① `build_progress` 停在 B1 时取不到 → **整条时间轴没有 current 节点**（「合并计算」反显示 pending）；
    ② `rewind_candidates` 的索引退化成 `len(order)` → **把 B4/C1/C3/C4 等未到达的下游节点混进「打回」候选**（有真实误操作风险）；
    ③ EN 模式该节点短名回落中文。修法：以 `BLOCK_*_SEQUENCE` 为唯一真源，三处统一为 `B1.meta_analysis`，
    保留 `B1.meta` 反向别名供旧会话/旧信封使用。
    - **能长期潜伏的根本原因**：`tests/test_flow_menu.py` 的 `mk_session` **直接迭代 `STAGE_ORDER` 造会话** ——
      夹具与实现共用同一个错常量、互相自洽，断言永远通过。已改为从真源取 id。
    - **新增 9 条回归锁**：STAGE_ORDER ↔ 真实 id 双向包含、`_EN_SHORT` 键集合覆盖、每个真实 id 有专属 schema、
      停 B1 时时间轴有且仅有一个 current、菜单标题非空无 `None`、EN 短名不含中文。
  - **P0 · SKILL.md 发布认领地指向已不存在的目录**：`workbench_owner_workspace` 由
    `2026-09-14-14-30-18`（**该目录已不存在**）改为 `2026-09-17-09-54-01`（`.wbapp_hNZl928SI6wByvJt2COtcC.genie` 实际所在），
    并注明：从旧路径发布会失败或被迫新建 app → 拿到后缀域名（正是原文自己警告的偏离）。
  - **P1 · 软停「跳过」三处口径不一**：CLI 有、网页 `SHOW_SKIP=false` 隐藏、`nha.options` 从不含 `skipped`。
    网页恢复 `SHOW_SKIP = true`，且按钮**由后端 `options` 驱动**（`opts.includes("skipped")`，`opts = STATE.await.options`）
    → 软停显示、红线自动不显示，与状态机同源，不会再出现「UI 给了按钮但后端拒收」。
    *（复核更正：`fullflow._view` 其实一直按闸门类型正确计算 options，只是 `nha.options` 这一路不带，原审计措辞过重。）*
  - **P1 · 网页补 A3 `pdf_dir` / A1 `sources` 入口**（此前仅 CLI 有）：新增 panel kind **`inputs`** ——
    通用「可编辑键」渲染器，按 `revision_key` + `value_path` 生成文本框，支持 `list: true`（数组 ↔ 逗号分隔）与 `bool`。
  - **P1 · CLI 补 `revised` 选项**：`flow_menu._fallback_options` 此前注释「revised 不在此生成」，
    但网页侧 C1/B4 是**可以**字段级修订的 → 反向不对等。改为按 `machine_options` 的 `allowed` 集合生成。
  - **P1 · B1 修订权两侧都残** + **`EDITABLE_KEYS` 9 个死键**：新增通用**未绑定可编辑键兜底面板**
    （`renderUnboundEditable`）—— 凡 schema 已声明但面板未绑定的可编辑键，自动列成可编辑 JSON 区；
    同时把 `EDITABLE_KEYS` 收口到**只声明真被消费的键**（原 B2 五键 + C2/C3/C4 两侧都没有任何入口，
    且与 `fullflow` 自订的「声明即须被消费」规则冲突）。**理由：留着是死配置，下一个人会以为功能存在。**
  - **P2 · A2 时间轴标签**「检索」→「文献集」，与 `STAGE_ORDER` / CLI 的「文献集（检索 + 初筛）」一致
    （该节点已按 2026-09-10 裁定把「检索」+「初筛」合并）。
  - **P2 · 网页 EN 模式全量本地化（本轮工作量最大）**：语言开关原本只翻顶栏 11 个框架串，
    EN 下节点标题 / intro / 面板标签 / 提示条**全是中文**（CLI 侧是真双语）→ 两侧严重不对等。
    复用 `topic_translate.py` 通道，把 schema 界面文案**整会话一次批量**本地化：
    `title` 走人工维护的 `TITLE_EN`（零延迟、不占额度），`intro` / panel `label`·`hint` / `placeholder` /
    字段与列标签走自动翻译；`build_state(sess, lang)` 下发本地化副本 + `stage_titles`(zh/en) + `i18n.state`；
    `/api/session` 加 `lang`、**缓存键按语言分开**（否则切 EN 拿到中文那份）；语言偏好 `localStorage` 持久化
    且同步顶栏开关高亮；动作端点（decide/rewind/上传）不带 `lang`，回传的中文 schema 会在 EN 下把节点打回中文 →
    新增 `absorbState(s)`：先按收到的渲染，再后台按当前语言重取覆盖；翻译不完整时**显式提示**
    （`i18n.state !== "en"`），**绝不静默半翻译**。
    - **踩坑**：首版 `_UI_MAX_TOKENS=3000` 撑不住 40 条批，返回**残缺 JSON**（`finish_reason=length`）→
      解析失败 → 旧循环把 7 个候选**逐个试遍**（每个都等到超时）→ 实测一次 EN 切换 **603 秒**且标签全没翻。
      实测：10 条/3000 → 4.1s ✓；20 条/3000 → 11.8s **length 0/20**；40 条/8000 → 12.0s ✓。
      **三处修法**：① `_UI_MAX_TOKENS` → 8000，并按**字符预算**分批（长 intro 撑长输出，光限条数不够）；
      ② 拿到内容但解析失败时**直接二分重试**，不再空转候选；③ 加**整次调用时间预算**（90s），
      无论怎么失败都不会卡住语言开关。结果：首切 **603s → 24.9s（159/159 全翻）**，二次走磁盘缓存 0.01s，
      `build_state('en')` 0.14s，zh 路径 0.00s 零行为变化。
  - **P2 · 发布载荷白名单漏模块（静默丢功能的隐患）**：`publish-kit/build_publish.py` 的 `WHITELIST_FILES`
    **缺** `topic_translate.py` 与 `evidence_upload.py`。危险在于两者都是**函数内惰性 import** →
    漏了不会让服务起不来，而是**静默丢功能**（中文主题检索不到文献、C1 上传端点直接 500、EN 界面全回落中文）。
    两个模块补入白名单，**同时**加入 `REQUIRED_IN_PAYLOAD`（构建后自检，缺了就报错 ——
    宁可构建失败也不发一个「看起来正常但少了能力」的载荷）。随后重建 `publish/` 快照（208 files，自检 7/7 ✓，py3.11 守卫 ✓）。
  - **P2 · B1 解读卡只在 coze 分支有数据**：`_interpretation` / `_quality_advice` 此前只在 coze 成功分支产出，
    local / 演示 / `auth_blocked` 路径恒空 → 面板永远显示「（解读引擎未生成内容）」。新增
    `_stats_from_pairwise(pw, effect_measure)`，把本地产出的 pairwise 结果（log 尺度 TE/CI，**含 exp 还原**）
    桥接成 `interpretation.interpret_result` 期望的 stats 形状，local 与 demo 两条路径都接上 → 三条路径口径一致。
  - **P2 · R 引擎指纹滞后于 SKILL.md 版本（写本轮 CHANGELOG 时顺带发现）**：`run_task.R` 的
    `.MA_ENGINE_VERSION` 停在 `2.15.0`，而 SKILL.md frontmatter 已是 `2.16.0` —— 按该字段自己的既定口径
    （**与 SKILL.md 版本对齐**）应立即跟平，否则又回到「按指纹查 CHANGELOG 却对不上」的老问题。
    代码注释里「仅 R 引擎变更时才前进」与「与 SKILL.md 对齐」两句本身会打架（就是这次偏离的成因），
    已改为**对齐优先**并注明：bump SKILL.md 版本号时本值必须同一次改动一起改。该字段无程序化消费方，改动零风险。
  - **P2-12 收尾：历史快照已删除（2026-09-22，用户裁定「清理掉」）**：删掉 `publish/`（11 MB）、
    `publish-backup/`（3.2 MB）、`publish-backup.rar`（3.1 MB）、`publish-preclean-20260917/`（58 MB），
    合计 **≈75 MB**。四者均为 git 未跟踪、**零代码引用**（全树 grep 验证），且落后于主线
    （缺 `topic_translate.py` / `evidence_upload.py` / `reasons_en`）——留着只会被误当成可发布的包。
    - **`publish-backup.rar` 是这次排查才发现第 5 个成员**（此前只登记了三套目录），顺手一起清掉。
    - **更正一处我自己的误记**：原打算把 `publish-kit/` 也当快照删掉，**这是错的** ——
      `build_publish.py`（重建载荷，全仓唯一副本）、`install_genie.py`（写 `.wbapp_<appId>.genie`
      + `applications.yaml`，是**复用同一 appId / 保持分享链接不变**的前提）、`check_py311.py`、
      `smoke_e2e.py` 都在这里，还有 appId 标记的权威副本。删了会丢掉整条发布工具链。
      `publish-kit/` 的定位见其 docstring：「publish infrastructure folder，结构上被排除在所有对外产物之外，
      所以标记跟着技能走」。**已保留**，并把误挂在它上面的 `DO_NOT_DEPLOY.md` 改名为 `README.md` 重写
      （原文把它描述成「整树历史快照」，与事实不符）。SKILL.md 的 ⛔ NOT deployable 行同步更正为
      「工具链（保留）」+「已删除的四个快照」两行。
    - 保留的仅有的不可再生元数据：appId 标记、`MANIFEST.sha256`、`publish-backup` 的旧
      `app.config.json` → 备份在 `2026-09-20-10-18-57/_deleted_snapshots_meta_20260922/`（7 KB）。
    - **踩坑（值得记）**：删除失败两次都不是权限问题 —— ① `rm -rf` 被 safe-delete 垫片接管并
      fail-closed；② 直接调 `genie-trash` 仍报 `0x80070002 系统找不到指定的文件`。根因是
      **`~/.workbuddy/skills/meta-analysis` 是指向内网文件共享 `//<内网文件服务器>/c$/...` 的符号链接**，
      而 **Windows 回收站对网络路径不存在**，故该盘符下任何 trash 调用必然失败。
      绕法：先 `mv` 到本地 workspace（`C:\Users\Wintone\WorkBuddy\...`，本地盘，回收站可用）再 trash。
      另注：`genie-trash` 只接受**反斜杠 Windows 绝对路径**，传 POSIX `/c/...` 会静默失败。
  - **回归**：`tests/test_flow_menu.py` **186 PASS/3 FAIL → 198 PASS/0 FAIL**（顺带补上 `_STAGE_RESULTS` 缺失的
    `A3.pdf_download` 夹具条目，修掉 2 项长期红灯）；`adapters/tests` 核心 5 套 **124 passed / 2 skipped**；
    `tests/`（interpretation / envelope_guard）**66 passed**。
    默认配置下尚存的 20 failed + 1 error 已逐项定性为**既有漂移、非本轮引入**：
    A4 闸门/开关漂移 15（`features.a4_extraction=False` 是默认值；置 `CT_FEATURE_A4_EXTRACTION=1` 重跑失败集立刻变成另一组 21→9）、
    coze 契约漂移 5（`test_pipeline_client` 只 import `coze_client`）、环境噪音 1（`test_pdf_extractor` 清理临时文件时网络盘 safe-delete 失败）。
    反证：这 4 个失败文件对 `EDITABLE_KEYS` / `STAGE_ORDER` / `form_schema` 的引用次数**均为 0**。

### Added

- **C1 英文初稿接地真实文献 + 消除中文残留 + 扩写正文（2026-09-22）**：
  演示/快速通道跑出的初稿此前是**中英混杂的骨架**：正文 648 词、Methods 与 References
  大量 `(to be added)`、标题直接把中文主题塞进英文句子。本轮三件事一起做（**648 → 1980 词**）。
  - **真实文献接地（核心）**：复用 skill 内已有的 `literature_probe.py`（零依赖 Europe PMC），
    新增 `search_evidence()` / `to_search_query()` / `_extract_rich()` / `_rank()` / `_dedup()`。
    draft 路径无 A2 文献集时按主题**真实检索**，两层：primary（RCT）+ synthesis（综述），
    喂给 C1 填充 Background 引用、Methods 检索式/数据库/日期/命中数、Results 特征表、References。
    - 只落地**书目事实**（作者/年份/刊名/设计/DOI/PMID/被引数）；**绝不臆造样本量与结局数字**，
      特征表缺该列就不列该列。检索失败静默降级，不是硬闸门。
    - 踩过的坑（已修）：`PUBLICATION_TYPE:"..."` 无效（命中 0）→ 正确字段是 `PUB_TYPE:"..."`；
      `PUB_TYPE:"Meta-Analysis"` 也不是合法值（API 报错）→ synthesis 层改用 `"Systematic Review"`；
      **`sort=CITED desc` 会压过相关性**，返回"心脏病统计年报"这类高被引噪声 → 禁用，用默认相关序；
      两次查询间隔 <1s 会被限流（第二次返回无 hitCount 的响应）→ 间隔 1s + 静默失败重试一次；
      完整题名当查询会把命中从 138 压到 6 → `to_search_query()` 只取主标题并去停用词/括号。
    - primary 层先按 `study_type` 严格过滤出真 RCT **再**做相关性排序（顺序反了会把 10 条砍成 3 条）；
      跨层按 DOI/标题去重（Cochrane 综述此前在两层各出现一次）。
  - **消除中文残留**：新增 `topic_en` 入参（前端「英文题名」输入框 + `run_fastpath` + `run_block_c`
    + `c1_draft`）；演示路径内置 `block_b.DEMO_TOPIC_EN`。无英文题名时**不臆造翻译** —— 标题保留
    原题、正文指代用 "the research question"，并给一行英文提示。中文串改为英文：`b2_grade` 新增
    `reasons_en`（与中文 reasons 同步 append，一一对应）、`_OVERCLAIM_LABEL_EN`（12 类模式英文
    标签，随 hit 以 `label_en` 下发）、demo 的 NMA note。OC 的 `evidence` 是被扫描的**原文证据**
    （源文本为中文时保留中文），加 "(verbatim excerpt…)" 标注。
  - **扩写**：Background 四段式（重要性 / Existing syntheses 真实引用 / Recent primary evidence
    真实引用 / 目的）；Methods 补 Eligibility criteria、Search yield、亚组与敏感性分析、Software、
    Data availability；Results 加纳入研究特征表；Discussion 加 Comparison with existing syntheses、
    Future research；References 15 条真实条目（作者带 initials）。
  - **顺带修的数据不自洽**：`n_stud` 曾取 studies_list 长度 → "检索到 15 篇"被写成"纳入 15 项研究"，
    与 B1 的 k=6 矛盾。现以 k 为准；检索条数只用于描述"证据集"，且不再挂在 "Included studies" 后。
    `_plur` 修 "meta-analysis" → "meta-analyses"（此前按"以 s 结尾"被跳过，输出 "3 meta-analysis"）。
  - 回归：`test_block_b` 20 OK(sk2)、`test_block_c` 26 OK、`test_writing_advisor` 52 OK、
    `test_interpretation` 19 OK、`test_envelope_guard` 47 OK、`test_flow_menu` 186P/3F（基线一致）。
    端到端：中文主题 + 不传信封 → C1.draft，1980 词、15 条真实参考文献、中文残留 0 处（除原文引文）。

- **「自备 B 信封 → 跳至 C」未给信封时改用内置演示信封（2026-09-22）**：
  此前该入口上传/粘贴都为空会直接 400，用户想先看看 Block C 长什么样只能先跑完 A+B。
  现在与「自备原始数据」一致：未提供信封 → 用内置示例继续流程，把 C 全流程跑完看效果。
  - `block_b.py`：新增 `DEMO_B_STUDIES`（6 项 2×2 RCT）、`DEMO_B_CLAIMS_TEXT`、`demo_b_env()`。
    **数值不硬编码**：B1 走 `b1_pairwise_python`、B2 走 `b2_grade`、B3 走 `detect_overclaims`、
    B4 走 `b4_quality_gate` 现算 → 合并效应量 / GRADE / 过度声明 / 质量门四者恒自洽
    （改了示例研究，下游摘要跟着变）。产出信封与 `run_block_b` 同构
    （`stages` B1-B4 全 completed、`done=True`、`_demo` 标记）。
    演示值：k=6、OR=0.68（95% CI 0.50–0.92, p=0.013）、I²=34.5%、GRADE=Moderate、
    B3 命中 1 条（medium）→ **B4 `critical=False`，不阻断 C 流程**。
  - `workbench/server.py`：`/api/start_data` 的 `draft` 分支改为「粘贴 → 上传 → 内置演示」
    三级兜底，并透传 `demo=True`；`fullflow.run_fastpath` 的 draft 分支据此把 A 信封
    A4 的 note 标为「内置示例 B 信封（演示），跳至 Block C 撰稿」。
  - `workbench/workbench.html`：B 信封区块补 🟡 演示模式说明（与「原始数据」区块同款）。
  - 验证：26 项结构/自洽/幂等断言全 PASS；线上 HTTP 实跑新建会话 →
    C1 初稿 4621 字 → C2（hits 1）→ C3 → C4 → done，**Block C 四步全部走通**。

- **C 流程启动「没检索到文献」显式提示（2026-09-22，用户要求）**：
  此前 C1 在 Europe PMC 检索失败 / 0 命中 / 中文主题没填英文题名时是**静默降级**——
  稿子照出，背景/讨论用通用表述、参考文献是 `(to be added)` 占位符，用户却以为
  正文已经引了真文献。这在此场景是危险误导，故不再静默，一律显式回传状态 + 提示条。
  - `block_c.evidence_status(evidence, topic_en, topic, error, has_studies, n_upstream)`：
    唯一真源，判据分三层——**「有没有可引用的真文献」才是用户真正关心的结论**。
    完整 A 流程稿子拿的是 A2 文献集（`has_studies=True`），此时补检索失败/没跑都不报
    warn（否则每次正常流程都误报）；只有「上游无文献 **且** 补检索也没拿到」才是真的没接地。
    产出 `reason`（`ok|upstream_only|no_topic|no_topic_en|error|no_hit|not_searched`）、
    `level`（`ok|info` 蓝 / `warn` 红）、`notice`（中文提示文案，含影响与处理路径）。
  - `fullflow.run_fastpath`：检索失败把 `_ev_err` 透传 `evidence_error`；`run_block_c` /
    `c1_draft` 接 `evidence_error` 落到 `stage_result.evidence_status`。
  - `workbench/server.py`：`_session_notices()` 从 `await.stage_result.evidence_status`
    （回退读 C 信封 `C1.draft` 阶段）取结论，仅在停驻 C 块时下发 `STATE.notices`；
    `level=="ok"` 映射成 `info`（成功不显红）。
  - `workbench/workbench.html`：`renderNode` 顶部按 `STATE.notices` 渲染 `.notice`
    红/蓝提示条（标题 + 正文，保留 `\n` 折行），并往底部信息栏补一行（去重防刷屏）。
  - 验证（纯模板路径，无 LLM/浏览器）：5 分支全对——
    中文主题无英文题名→`no_topic_en`/warn；有英文题名未检索→`not_searched`/warn；
    检索失败→`error`/warn；0 命中→`no_hit`/warn；命中→`ok`/info。三模块导入全绿。

- **UI 文案 + 选题探针降级态修复（2026-09-22）**：
  - 开始页单选项 `已备好原始数据 → 跳至 B 合并` → **`已备好原始数据 → 跳至 B 合并计算`**（workbench.html:1378）。
  - 选题按钮 `🧭 帮助选题` → **`🧭 先帮我选题`**（按钮文本 + `data-label` + 空主题 flash 提示）；
    CLI 菜单 `opt_probe` 中文 `帮助选题（可行性速览）` → `先帮我选题（可行性速览）`（scripts/flow_menu.py:148）。
  - **选题探针「探针不可用 篇」误导修复**：用户反馈「PubMed 系统评价 / Meta（近 5 年）探针不可用 篇，
    选题时检索不到结果？」。实测探针本身正常（线上 `/api/topic_help` 实测 Cochrane 120 / PubMed 2787 命中）；
    「不可用」只在 Europe PMC 调用失败时出现，但旧 UI 只印**不透明的「探针不可用」**且无任何原因、
    无重试入口，看起来像「选题检索不到结果」的死功能。修复（`renderTopicHelp`）：
    - `hit_count=None` 且有 `error` → 显示「暂不可达」并把真实错误写进 `title` 悬停提示；
    - 任一探针出错 → 在结果面板下补一行 warn 说明（原因 + 「点↻ 重试选题速览可重查；选题可行性只是
      参考，不影响后续流程，也可直接启动」）；
    - 新增「↻ 重试选题速览」按钮（`topicHelp(LAST_TOPIC)` 复用已填主题重查，不需回到首页）。
  - 验证：`node --check` 整段 app 脚本通过；线上 `/api/topic_help` 实跑命中正常；
    单测模拟 BASE 指向不可达地址 → payload 正确带回 `error`（"Europe PMC request failed after 3 retries: …"），
    UI 据此走「暂不可达 + 原因 + 重试」分支。

- **选题探针「中文主题 0 命中」根因修复：缺中→英检索词这一环（2026-09-22，用户反馈）**：
  用户反馈「选题可行性速览：SGLT2 抑制剂在慢性肾脏病（CKD）中的肾保护与心血管获益
  该选题没有命中任何文献，是否因为需要先做中英文自动翻译而缺失了这一环？」**确认 Root Cause 正是它**。
  实测（2026-09-22）：中文主题直送 Europe PMC → Cochrane **0 篇**、PubMed 无可用计数；
  换英文检索词 `SGLT2 inhibitors chronic kidney disease renal protection cardiovascular outcomes`
  → Cochrane **6**、PubMed **1904**。`literature_probe.py` 此前**无任何翻译步骤**，
  `dedup_probe → probe → _build_query` 把原始 `topic` 直接当查询串；Europe PMC 索引的是英文摘要，
  中文串几乎必然 0 命中——而这会被误读为「该选题无人做过（新颖）」，是**危险的假信号**
  （与 C 流程那个「静默降级」同类）。修复：
  - `literature_probe._has_cjk(text)`：CJK 字符检测（U+3400–9FFF / F900–FAFF / FF00–FFEF / 3040–30FF）。
  - `probe(..., topic_en=None)`：**英文检索词优先**（`q_topic = topic_en or topic`）；`ct_handoff` 同步用英文串。
  - `dedup_probe(..., topic_en=None)`：中文主题 **且** 未给英文检索词 → **直接跳过网络请求**，
    两层 `hit_count=None` + `untranslated=True`，附 `notice`（说清「不是没文献，是没翻译」+ 处理路径），
    避免跑出误导性的「Cochrane 0 篇 = 新颖」；给英文检索词则正常直连 Europe PMC。
  - `workbench/server.py`：`TopicHelpReq.topic_en`（可选）；`api_topic_help` 透传。
  - `workbench/workbench.html`：开始页「英文题名」框（`#topic_en`）纳入选题速览请求；
    速览页新增「未命中文献的原因」警示卡（含内联英文检索词输入 + 「用英文重查 →」）；
    命中列在未翻译时显示「需英文检索词」而非「探针不可用」；空标题文献面板在未翻译时隐藏；
    `renderStart(prefill, prefillEn)` / `startWithTopic` / `返回修改` 保留英文检索词。
  - 验证：`node --check` 通过；单元直调（中文→拦下 untranslated/notice；中文+英文→Cochrane 6 /
    PubMed 1904）；`TopicHelpReq` 直调 + 线上 `POST /api/topic_help` A/B 两组端到端一致。
  - **附带发现（非本次引入）**：`tests/test_block_a.py::TestA4RedLineGate` 4 项 +
    `tests/test_fullflow.py::TestBackwardCompat::test_block_a_no_pause_at` 1 项失败——A4 闸门
    实际返回 `done=True` 而测试仍期望 `extraction_review` 阻断。`block_a.py` 仅 import
    `coze_client`/`features`，**不依赖 literature_probe/server**，故与本修复无关，属既有漂移，待单独排查。

- **改为「自动翻译关键词」：网页端补齐与技能上下文同等的 LLM 能力（2026-09-22，用户纠正上一条）**：
  用户指出上一条的处置**逻辑不对**——「技能上下文方式的时候是可以做自动翻译的，网页端也应该一样，
  对关键词做自动翻译」。确认：技能（Agent）上下文里 LLM 就在回路中，翻译是天然能力；而网页端
  FastAPI 服务是**独立进程**、Agent 不在回路里，此前只能让用户手填英文题名，等于把机器该干的活
  推给用户。故新增服务端翻译通道，**「英文检索词 + 警示」降级为上一条的兜底而非首选**：
  - **`adapters/topic_translate.py`（新增，零第三方依赖）**：复用 WorkBuddy 本机
    **OpenAI 兼容模型端点**（`~/.workbuddy/models.json`，或 `LLM_BASE_URL`/`OPENAI_BASE_URL` 等
    环境变量）做一次极小翻译调用。`translate_to_english(text) -> str|None`。
    - 候选梯队 `deepseek-v4-flash`→`qwen3.8-max`→`LongCat-2.0`→其余有 url 的模型；
      逐个降级，任何异常都吞掉返回 None（绝不中断流程）。环境变量指定的端点最高优先。
    - **实测（2026-09-22）**：三者对同一中文主题给出**完全一致**的英文检索式；
      `deepseek-v4-flash` 最快（约 1.3s）。
    - **坑（必须记住）**：`max_tokens=80` 会让 reasoning 模型把预算耗在思考上、`content` 返回空串 →
      定 `_MAX_TOKENS=512`；输出须过 `_looks_english()`（非空 / 有拉丁字母 / **无 CJK** / 非拒答 /
      长度 2–300），并 `_strip_noise()` 去引号与 `English:` 前缀。
    - **缓存**：进程内 + 磁盘（`%LOCALAPPDATA%\meta-analysis-wb\translate_cache.json`），
      同一主题只翻一次，省 token 且避开限流。
  - `literature_probe.dedup_probe(..., topic_en=None)`：中文且无英文 → **先自动翻译**；成功则以英文
    检索（`auto_translated=True`、`topic_en_source="auto"`、命中真实命中数 + info 提示）；
    **只有自动翻译也不可用**时才拦下并索要英文（保留上一条的降级路径）。
  - `fullflow.run_fastpath` draft 分支：`topic_en` 缺失且主题为中文时同样自动翻译并落库
    （`sess.data["topic_en_source"]="auto"`），使 **C 流程**也从同一能力受益。
  - `workbench/workbench.html`：速览页在 `auto_translated` 时显示「🌐 关键词已自动翻译」卡片
    （展示英文检索式 + 可修订输入 + 「用此英文重查 →」）；`renderTopicHelp` 把 `r.topic_en`
    回写 `LAST_TOPIC_EN`，使「用此选题启动流程」把英文题名带进开始页（避免 C 流程重复翻译）。
  - **验证**：新增 `tests/test_topic_translate.py`（12 项离线断言：CJK 检测 / 清洗 / 合规校验 /
    无端点降级 / 候选解析 / 缓存 / 探针「翻译不可用时**不触网**即拦下」/ 「翻译可用时两层都用英文」）
    → **12 passed**。线上 `POST /api/topic_help`：中文无英文→`auto_translated=True`/source=auto/
    Cochrane 5+PubMed 1712；手填英文→source=user。C 流程 `run_fastpath(draft, demo=False)` →
    `topic_en_source=auto`、检索 ok（primary 135 / synthesis 157 命中，实取 10/5）。
  - 回归：`test_block_b`(20) + `test_block_c`(26) 全绿；`test_fullflow` 6 项失败**均为既有 A4
    `extraction_review` 闸门漂移**（`await.gate` 为 None，与翻译改动无关），与遗留清单一致。

- **C1 支持上传作者自备文献（Excel 清单 / PDF 打包）作为初稿证据（2026-09-22，用户要求）**：
  用户提出「C1 这里应该提供一个功能，允许用户上传自己收集和修改过的 Excel 文件列表或者 PDF 打包」。
  此前 C1 的证据只有两个来源——上游 A2 文献集、Europe PMC 自动检索；而真实写稿时作者手上**往往
  已有自己筛过/改过的清单**（裁决表 Excel、Zotero/EndNote 导出的 RIS、下载好的 PDF 全文），
  那是最权威的证据集却没有任何入口，用户只能眼看着初稿引用检索来的（可能不相关的）文献。
  - **`adapters/evidence_upload.py`（新增，无新增第三方依赖）**：把上传文件解析成与
    `literature_probe.search_evidence()` **同构**的 evidence dict（`primary`/`synthesis` 两层），
    `block_c` 无需区分来源即可消费。支持：
    - 表格清单 `.xlsx/.xls/.csv/.tsv`（**中英文列名**均可，含表头自动识别 + 「包含匹配」容错）；
    - 文献管理器导出 `.ris` / `.bib`（BibTeX 的 `author={Family, Given and ...}` 单独解析，
      否则会被逗号切成 4 个假作者）；
    - 纯文本清单（一行一篇）；PDF 打包 `.zip`（内含 PDF / RIS / 表格，递归展开）或直接多个 `.pdf`
      （复用 `block_a._extract_pdf_title/_extract_pdf_doi` 同一套口径，不另写第二套标题识别）。
    - 设计类型归一（`随机对照试验`/`Meta分析`/`RCT` → 英文短标签），据此切 primary/synthesis 两层。
    - 只取文件里真实写着的书目事实；**缺字段绝不臆造**（缺作者 → 正文按 `Anonymous`，缺年份 → `n.d.`）。
    - 安全上限（文件数 500 / PDF 数 300 / 解压总量 400MB / 单文本 8MB）防 zip 炸弹。
  - **证据优先级（`fullflow._run_block` C 分支）：作者自备 > A2 文献集 > Europe PMC 自动检索**。
    有自备文献时**不再联网检索**（既不浪费一次查询，也避免检索结果盖掉用户的清单）；
    并清掉历史那次检索失败记录——否则稿子明明引的是用户清单、提示条却在报「Europe PMC 检索失败」。
  - `block_c.c1_draft`：`source=="user_upload"` 时以**用户清单为参考文献基准**，A2 中不重复的条目
    `_merge_studies` 追加在后（DOI/标题去重）；出处说明写清「作者上传的清单」+ 上传日期；
    方法学**不再谎称**「检索了某库/检索期」→ `Databases searched: author-supplied reference list
    (uploaded by the author)` / `search period: not applicable`。
  - `block_c.evidence_status`：新增 `user_files` / `level="info"` 分支 + `title` 按来源变化
    （「作者自备文献」vs「检索状态」）+ `preview`（前 20 条已识别条目，供上传后核对）；
    缺作者/年份的条数会明说（否则参考文献里冒出 `Anonymous` 会被当成程序 bug）。
  - `workbench/server.py`：`POST /api/c1_upload_evidence`（多文件 multipart）+ `POST /api/c1_clear_evidence`；
    **停驻 C 块才自动 `rewind` 重跑 C1**（其余时刻只落库）——贸然回退会绕过 B 的人工闸，破坏
    「红线闸必须人工放行」；`_session_notices` 标题改为取 `evidence_status.title`。
  - `workbench/workbench.html` + `form_schema.py`：C1 节点新增「初稿证据来源」面板
    （两个上传入口 + 当前证据来源状态 + 已识别条目预览 + 「撤销上传，改回自动检索」）。
  - **踩到的坑（已修）**：① 上传暂存加序号前缀 → UI 显示成 `0_清单.xlsx`，改为每文件独立子目录；
    ② `evidence.query` 与参考文献出处里带中文文件名 → **中文渗进英文稿件正文**，改为英文标签、
    出处只留上传日期；③ pandas `dtype=str` 读表时空单元格仍是 NaN，`str(NaN)=="nan"` →
    参考文献里出现一条标题叫 `nan` 的条目（**单测实测踩到**），`_clean_cell` 统一把
    None/NaN/NaT/`<NA>` 归空串。
  - **验证**：新增 `tests/test_evidence_upload.py`（13 项离线断言：中英文列名/中文类型归一/空标题行
    跳过/缺标题列报错/DOI 大小写去重/RIS/BibTeX 作者/纯文本 DOI 里的数字不得当年份/两层切分/
    evidence 字段同构与 `evidence_status` 结论/zip 递归与体积守卫/作者形态/合并去重）→ **13 passed**。
    线上 HTTP 端到端（`launch_workbench.py` 重启后实跑）：draft 会话 → 上传 `mylist.xlsx`+`myrefs.ris`
    → `reran=True`、参考文献 3 条全部来自上传清单、`reason=user_files`、提示条标题为「作者自备文献」；
    上传 `bundle.zip`（RIS+PDF+不支持的 docx）→ 识别 2 篇、PDF 正确抽出标题/作者/年份/DOI、docx 计入
    errors；`/api/c1_clear_evidence` → 回到 `reason=ok / source=auto_search`；停在 B1 时上传 →
    `reran=False` 且仍停 B1（不绕闸）。回归 `test_block_b`(20)+`test_block_c`(26)+`test_topic_translate`(12)
    +`test_evidence_upload`(13) = **69 passed / 2 skipped**。
  - **勘误（2026-09-22 复核）**：此处原记「demo 下稿件标题仍是用户自己的中文选题」——**实测为误**。
    `c1_draft` 的 `_title = topic_en or topic`，demo 下 `topic_en` 已被置为 `DEMO_TOPIC_EN`，
    故标题**就是** omega-3 示例题名，整份稿（标题/统计量/参考文献）自洽。真正的缺口是：页面
    没有任何标记说明「这是演示数据」，用户会把示例稿当成自己的分析结果 —— 已修，见下条。

- **演示会话显式标记：页面明说「本次用的是内置示例信封」（2026-09-22，用户要求）**：
  「已备好 B 信封 → 跳至 C 撰稿」不传信封时会用内置示例信封兜底跑完 Block C —— 但页面
  此前**没有任何标记**，用户会把自己看到/编辑的初稿当成真实分析结果（而它的标题、效应量、
  GRADE、参考文献全是 omega-3 示例主题的，与用户输入的主题无关）。
  - `run_fastpath(demo=True)` → 落库 `sess.data["demo"]=True`（**落库而非只放内存**：重载会话
    后标记仍在）；`build_state` 下发 `session.demo`；`_session_notices` 新增 demo 提示条。
  - **演示提示不受 C 块门控** —— 「这是演示数据」对每个节点都成立，用户在任何节点翻看都该看到。
  - 前端：标题栏常驻「⚠ 演示数据」角标（提示条会被面板滚出视野，角标不会）+ 节点顶部
    红色提示条（含用户自己的主题名，点明「与你输入的主题无关」）+ 开始页演示说明补一句
    「标题/统计量/参考文献都取自示例主题」。
  - 验证（线上 HTTP + 重载）：不传信封 → `session.demo=True`+demo 提示条；上传信封 →
    `demo=False`、无 demo 提示；`/api/session` 重载后标记与提示条**仍在**。

### Changed

- **性能专项：把「每一步都慢」从管道层根治（2026-09-20，用户裁定「12345都做」）**：
  前一轮已定位「慢的是管道不是计算」——skill 目录挂在 **SMB 网络盘**（软链接 →
  `\\<内网文件服务器>\c$\...`），后端 venv 也在网络盘，会话文件含 50% 纯冗余副本，且单进程 GIL
  让并发请求串行放大。本轮按①~⑤全部落地。**实测：冷启动 60–90 s → 7.3–8.3 s；单次
  `save()` 258.9 ms → 13.5 ms（19×）；会话 2382 KB → 715 KB（-70%）；A2 节点 `#center`
  340 KB → 110 KB、DOM 节点 6550 → 2392；`/api/session` ver 命中 1 MB → **56 B**；
  并发 10 中位延迟 1552 ms → 407 ms；步骤切换 144 ms → 70 ms。** 语义零变化。

  - **① 运行环境挪本地（`workbench/launch_workbench.py` 重写）**：新增
    `%LOCALAPPDATA%\meta-analysis-wb\venv` 本地副本，`pick_python()` **优先本地**、缺失才回退
    网络盘 `.venv`；新增 `--sync-venv`（`robocopy /E /MT:32 /R:1 /W:1`）一次性从网络盘复制。
    量化：`import server` 从 **44.2 s → 7.6 s（5.8×）**。同时**删掉**启动前那次多余的
    `import fastapi, uvicorn` 健康检查（网络盘上白花约 30 s），改为
    `_open_browser_when_ready()` 轮询端口 **LISTENING**（0.3 s 一次，上限 180 s）后再开浏览器，
    取代原来的固定 2 s sleep ——既不再空等、也不会在服务未就绪时打开白页。
  - **② 消除会话文件冗余（`adapters/fullflow.py`）**：实测 2382 KB 会话里 **50.3% 是纯副本**
    ——`envelope.final` ≡ `stages[-1]`（前端从不消费）、`last_view.await.{stage_result,nha,
    editable_payload}` ≡ 该块 `envelope.final` 三字段。新增 `_dehydrate()`（落盘前摘副本，
    仅保留 `_final_idx` / `_derive_from` 派生标记）与 `_rehydrate()`（加载时原样补回，内存语义
    完全不变）；`_same()` 采用「身份 → `==` → 逐字节」三级短路。**对外只改了磁盘格式**：
    新增公共读入口 `load_session_data(path)`，外部读会话必须走它或 `FullflowSession.load`。
    结果：2382 KB → **735 KB（-69%）**，全部 **34 个真实会话** 往返（dehydrate→rehydrate）
    逐字节无损。
    - ⚠️ **兼容性约定（写进模块 docstring 与 CHANGELOG）**：任何直接 `json.load()` 读会话文件
      的代码都可能拿到缺字段的中间态。已核查生产路径 —— `export_screening_xlsx` 走
      `FullflowSession.load`，`deploy_retest.py` 只读仍未删的 `envelope.stages`，均安全。
    - 顺带修掉一处性能陷阱：旧格式文件首存时 `_dehydrate` 要硬做 `_canon_json()` 对比
      （35 ms，占单次 save 的 87%）。`_rehydrate` 增加**引用归一化**（加载后令
      `env["final"] is stages[k]`），使后续所有 `save()` 走身份短路 → 稳定在 ~13.5 ms。
  - **③ `save()` 本地落地 + 后台回写（新增 `adapters/session_store.py`，约 370 行）**：单写者
    后台线程模型。`write_text()` **首次写同步落网络盘**（文件须先存在），其后写入仅进本地镜像
    + 队列（主流程零等待）；后台线程按序合并（`_QUEUE[cp] = (net, text, seq)`）回写，失败指数
    退避重试。`read_text()` 命中进程内存副本或本地镜像；若发现**他进程**改过文件则主动弃用内存
    副本（避免多进程读到陈旧态）。另含 `flush(timeout)`、`atexit` 兜底、原子写
    （`_atomic_write_bytes`）、`rev()`（revision+size 供 ver 计算）。崩溃后可从镜像续跑。
    结果：后续 `save()` **8–21 ms（均 13.5 ms）** vs 旧同步写 258.9 ms。
  - **④ 详情行懒渲染 + 局部更新（`workbench/workbench.html`）**：`renderRowlist` 不再无条件为
    每行渲染 `tr.rl-detail`（旧实现 104 行 → 104 个隐藏详情行全渲染，12 字段 ×104）；改为
    `A3_EXPANDED.has(i) ? buildDetailRow(...) : ""` 按需现场构建。`a3ToggleExpand(i)` 改为
    **只动被点的那一行**——展开时 `insertAdjacentHTML("afterend", html)` 插入，收起时
    `det.remove()` 真正摘除节点；不再 `reRenderRowlist` 整表 `outerHTML` 重建。
    结果：`#center` 340 KB → 110 KB、DOM 节点 6550 → 2392、静态详情行 213 → 0；
    展开响应 40–60 ms → ~2 ms。
  - **⑤ 前端合并请求、消除并发放大（`workbench/workbench.html` + `workbench/server.py`）**：
    后端 `/api/session` 增加 `ver` 提示——客户端版本串与当前一致即返回
    `{"unchanged": true}`（**56 B**，不再下发 1 MB）；`_session_ver()` 用 revision+mtime+size
    替代原 mtime-only 缓存键。前端新增 `_SESSION_INFLIGHT`（in-flight 去重，并发调用复用同一
    Promise）与 `_SSE_ACTIVE` 计数（`fetchSession()` 先等 SSE 流排空再拉取）；原 `reloadSession()`
    拆为 `fetchSession()` + `applySession(s)`，`applySession` 遇 `unchanged` 直接跳过整轮重渲染。
    `build_state` 另对「当前 await 节点」跳过重复下发 `stage_result`（省约 334 KB）。
    结果：并发 10 中位延迟 **1552 ms → 407 ms**；ver 命中响应 56 B；步骤切换 144 → 70 ms。

  - 验证与回归：`py_compile` ×3 + 内联 JS `node --check` 通过；CDP 驱动真实 Chrome 实测
    前端指标；真实网络盘实测写盘耗时。回归 `test_block_b` 20 OK、`test_block_c` 26 OK、
    `test_writing_advisor` 52 OK、`test_rewind_rollback` PASS、`test_flow_menu` 186P/3F（与
    基线一致）、`test_interpretation` 19 OK、`test_envelope_guard` 47 OK。
    `test_fullflow`(6F) / `test_block_a`(3F/1E) 为**既有基线失败**（源自 09-19 语义变更），
    与本轮无关。
  - 环境坑（留存备查，脚本在 `2026-09-20-10-18-57/_tmpio/`）：`robocopy` 经 `cmd //c` 会因引号
    吞掉 UNC 路径 → 改由 Python `subprocess.run([...])` 直调；`netstat` 输出是 GBK → 需
    `.decode("latin-1")`；Win11 26xxx 已移除 `wmic` → `pids_by_cmd` 降级为 no-op、只按监听端口
    PID 杀进程；`DETACHED_PROCESS` 子进程会被回收（后台起后端会 8 s 后死掉）→ 最终以后台任务
    托管方式启动 `launch_workbench.py --no-browser` 才稳定。

- **B3「过度声明检测」页补齐用途 / 原理说明，并修好「已过节点点不开」（2026-09-20）**：
  用户反馈「这一页是否对用途和原理做更清楚地说明」。原页面只有一句
  「基于统计量的过度声明模式扫描（被 B4/C2 复用）」+ 两个数字面板，看不出**查什么、怎么判、
  扫的是哪段文本、0 命中算不算数**。同时核查发现两处硬伤（后者为既有 bug）。
  - `block_b.py`：抽出 `_overclaim_context()` —— 把 B1 的 pooled 统计量（效应量 / CI / p / k / I²）
    归一为「模式辅助判定」上下文，**单点实现**，供判定与页面展示共用，杜绝判据与说明两处各写一套。
    `detect_overclaims()` 改为消费该上下文（改造前后 144 组「16 种文本 × 9 种 stats 形状」对拍
    输出**逐字节一致**，含缺 CI / 缺 p / 非数值 / 向量型 CI 等异常）。新增
    `overclaim_pattern_legend()`（12 类模式图例，含分级与「计入前提」）与
    `overclaim_stats_digest()`（本次实际可用的统计条件 + 四条辅助判定的满足情况）。
  - `block_b.py`：B3 `stage_result` 新增 `by_severity` / `n_high|n_medium|n_low`（同一个
    `_by_sev` 派生，嵌套与平铺两套读法不漂移）、`patterns`、`scan`（文本来源 / 比对范围 /
    字符数 / 篇数 / 状态提示 / 前 600 字预览）、`stats_used`、`downstream`。
    `run_block_b(..., claims_meta=None)` 新增可选入参（缺省不影响旧调用）。
    **原字段 `n_patterns` / `n_hits` / `hits` 原样保留** → B4、C2 及历史会话零影响。
  - `fullflow.py`：`_build_claims_text(sess, with_meta=False)` 新增 `with_meta`，同时回收
    「这段被扫文本从哪来」的事实（选题 / A2 前 20 篇标题摘要 / 各计数）；默认仍返回纯字符串，
    向后兼容。**关键诚实性修正**：文本为空时明确写出「0 命中 ≠ 无风险（上游没产出可比对文本）」，
    否则「扫了没发现」与「压根没扫」在页面上长得一模一样。
  - `workbench/form_schema.py`：B3 面板由 2 个扩为 8 个——「用途 / 原理（30 秒读完）」notice、
    检测概览（3 列）、**本次扫描的文本**、文本预览、本次可用的统计判定条件（含四条辅助判据）、
    命中项（空态文案改为「0 命中 ≠ 无风险」的解释）、**12 类检测模式图例（到底查了什么）**、
    命中后的去向；intro 重写并纠正原「自动节点，无需人工操作」与实际会软停复核的矛盾。
  - `workbench/workbench.html`：`renderRowlist` 支持 schema 的 `empty_text`（「0 命中」是有效
    结果，不该显示成取不到数据的「（无数据）」）；`.notice .d` 加 `white-space:pre-line`
    以支持多行说明（既有单行调用不受影响）。
  - **既有 bug 修复（`workbench/server.py::build_state`）**：阶段状态的**真源**是
    `st["stage"]["status"]`（B/C 块 `_mk_stage` 只写这一处，A 块另在顶层写一份），旧实现只读
    顶层 `st.get("status")` → B/C 各阶段恒为 `None`，两处后果：① 前端左栏按
    `status==="completed"` 才允许点开，于是**任何已过阶段（含 B3）都点不开、无法回看**；
    ② `stage_results` 恒为空 → 即便打开也是「全 —」空面板。改为「先内层后顶层」合并读，
    兼容两种写法。实测同一会话：修复前 `stage_results` 仅 `A4`、`progress.status` 全 None；
    修复后 5 个阶段状态齐备、`B1/B2/B3/B4` 结果全部可回看。
  - 验证：`detect_overclaims` 对拍 144 组全一致；离线端到端（coze 打桩）跑通 `run_block_b`，
    信封内 B3 带齐 11 个键、分级计数嵌套/平铺一致、空文本路径给出「0 命中 ≠ 无风险」警示；
    B3 schema 全部面板字段在真实 payload 上均可解析出值；前端内联脚本 `node --check` 通过。
    回归：`adapters/tests/test_block_b.py` 20 OK、`test_block_c.py` 26 OK、`test_fullflow.py`
    6 FAIL（**既有**，见下）、`tests/test_flow_menu.py` 186 PASS/3 FAIL（与改前基线一致）、
    `test_interpretation.py` 19 OK、`test_envelope_guard.py` 47 OK、`test_phase2_rewind_revise.py` OK。
    ⚠️ `test_fullflow.py` 那 6 条失败**与本次改动无关**：失败签名都是「A 块跑完直接停在
    `B1.meta_analysis`（`await_data=True`）」而非期望的 `extraction_review` 红线闸 ——
    源于 2026-09-19「A4 默认隐藏 + A3 之后强制进 B1」的语义变更，测试未同步更新，待补。

- **打回/回退提速 ③：回退进 A 块按「检索指纹」复用上次检索结果 + 强制刷新开关（2026-09-20）**：
  用户裁定：「指纹复用+强制刷新开关（推荐）」。此前回退进 A 块**必跑真实全库检索**——
  `rewind()` 把 envelope 清成 None 使 `cached_env` 恒失效，`invalidate_decisions` 又清掉
  A2 的 approved 使 `start_stage="A3"` 条件不成立，于是即使检索式一字未改也要重跑
  A1 的 ct-registry 查重探针（timeout 180s）+ A2 的 ct-literature 多库检索（约 2 分钟）。
  - `block_a.py`：新增 `a2_search_fingerprint()`——对**全部会改变检索结果的输入**
    （优化翻译后检索式 / max_results / year_from / include_reviews / 数据源子集）
    取 sha256 前 16 位；写入 A2 `stage_result.search_fingerprint` 与 `_search_reused`（审计：
    可回溯这次结果是复用还是重跑）。`run_block_a` 在 `start_stage is None` 且带
    `cached_envelope` 时比对指纹：一致 → 复用 studies / A1 探针 / coverage 审计字段，
    只重跑规则初筛并在 A2 闸重新停下；不一致 → 照旧真实联网检索（绝不静默给旧结果）。
    A1 闸停靠时把缓存的 A2 阶段以 `status="pending"` 一并带进信封，使「打回 A1 → 未改就批准」
    之后 A2 仍能复用（否则得再等 2 分钟）；pending 状态保证它不会被当成已完成结果展示。
  - `fullflow.py`：`FullflowSession.rewind()` 对 **A 块**改为「保留信封、状态置 pending」
    （B/C 仍原样清空）；新增 `rewind_fullflow(..., force_refresh=False)`，置 True 时清空该信封。
    `_run_block` 的 A 分支改为**始终**透传 `cached_envelope`（原先仅在 `start_stage` 为真时传），
    顺带修好另一条白等路径——只回传裁决（screened）的 A2 修订此前也会整块重跑检索。
  - `workbench/server.py`：`RewindReq.force_refresh: bool = False`，`/api/rewind` 与
    `/api/rewind_stream` 均透传；流式提示语改为说明复用/强制刷新两种行为。
  - `workbench/workbench.html`：回退确认框新增「强制重新联网检索（忽略上次检索结果）」勾选，
    随 `force_refresh` 提交；提示语与日志同步说明何时复用、何时重跑。
  - 验证（联网函数全部打桩为 `AssertionError`，证明复用路径确实零联网）：
    ① 回退 A2 默认 → `_search_reused=True`、104 篇复用、停在 A2，日志两条「复用…（跳过联网）」；
    ② 回退 A2 + `force_refresh=True` → 打到联网桩并被捕获为 error，日志「丢弃上次检索结果」；
    ③ 回退 A1 默认 → A1 探针复用、停在 A1，信封内 A2 为 `pending` 且 `stage_results` 不含它；
    批准 A1 后 `_search_reused=True`、A2 仅出现一次（无重复 stage id）。
    API 管线：`RewindReq` 默认 False / 显式 True 均正确，两个端点 kwargs 透传核验通过。

- **打回/回退提速 ①②（2026-09-20）**：
  用户反馈「打回/回退 时的速度非常慢，似乎可以优化？」。实测剖析后确认，**慢的不是计算本身**，
  而是两处纯浪费；与回退目标无关的固定开销约占 8~13 s，回退到 B/C 另加 ~1~2.5 min 重复劳动。
  - **① `FullflowSession.save()` token 级写出（6x）**：`json.dump(obj, f, indent=2)` 是 token 级
    写出——一份 2.3 MB 会话（A2 含 104 篇 studies + abstracts）触发 **110,356 次 `write()`**。
    本机 skill 目录经 UNC 挂载（`\\<内网文件服务器>\c$\...\.workbuddy\skills\`），存在 I/O 拦截：
    单次写 1 MB ≈ 200 ms（系统 temp 仅 1.1 ms），故 `save()` 实测 **2,394 ms/次**；
    而一次打回需落盘 **3~5 次**（`rewind` → `invalidate_decisions` → 各阶段推进 → 审计留痕），
    纯 I/O 就吃掉 8~13 s。改为 `json.dumps` 后单次 `f.write`：实测 **382 ms/次（6.3x）**，
    **产出字节与优化前逐字节一致（md5 相同）**，`indent=2` / `ensure_ascii=False` 语义不变，
    会话文件仍可人工阅读比对。
  - **② 回退到 B/C 时误清 `handoff`（功能缺陷 + 白重算）**：`rewind()` 原先无条件
    `self.data["handoff"] = {}`，但 `handoff` 的**全部键都由 A 块产出**
    （`studies_for_b`：A3 上传 / A4 抽取；`ref_sections`：已落盘 PDF 的章节切片；
    `merged_json`：A2 检索产物），对 B/C 而言它是**上游**产物而非待作废的下游结果。后果：
    - **丢数据**：`_run_block("B")` 读 `handoff.studies_for_b` 得 0 行 → B1 停在
      「待补数据」，用户必须重新上传 —— 回退等于白退（本地 75 个会话中 7 个命中该路径）；
    - **白重算**：Block C 的 `_extract_c_grounding` 见 `ref_sections` 为空 → 重抽全部已缓存
      PDF 章节，实测 **~2.7 s/篇**（59 篇 ≈ 2.5 min，84 篇缓存 ≈ 223 s）。
    修复：`handoff` 只在回退进 **A 块**时清空（A 会重跑并重新产出这些键）。
  - 验证：`test_flow_menu.py` 186 PASS / 3 FAIL（与改动前基线一致，3 条失败为既有：
    2 条菜单文案含 `None` 字面量、1 条 rewind 非法目标 rc 断言）；`test_envelope_guard.py`
    47 OK；`test_interpretation.py` 19 OK；`test_a4_b1_handoff.py` 的 handoff 机制段 [3] 全 PASS
    （其 [2]/[4] 失败为环境缺本地 R 引擎，既有限制）。新旧 `save` 在同一 data 对象上
    输出 md5 相同。回退 B1/C1 后 `studies_for_b` 2→2 保留、回退 A2 后 handoff 仍清空。

- **A3 成果导出：把「文件名」直接做成可点链接（2026-09-20）**：
  用户要求：「📥 PDF 全文下载进度 / ⬇ 下载确认清单（Excel）这里需要给出链接方便操作，
  可以直接将文件名做成链接」——即导出出口不该只有动词按钮，文件名本身要是那个链接。
  - `workbench.html`：新增 `a3ExportLinks(nDl)`，锚文本由动词短语
    （「⬇ 下载全部 PDF（zip）/ ⬇ 下载确认清单（Excel）」）改为**实际落盘文件名**
    （`📦 A3_PDF全文_3篇.zip` / `📊 A3_PDF下载清单.xlsx`），点击即下载；
    三处出口（A3 节点「成果导出」面板、done 页成功分支、done 页查询失败重试分支）
    统一复用该函数，杜绝三份文案漂移。
  - `dlA3(kind, name)` 新增文件名参数：`a.download` 取界面显示名，
    **所见即所得**（此前 `a.download` 恒为 `A3_PDF全文.zip`，会覆盖后端
    `Content-Disposition` 的 `A3_PDF全文_{n}篇.zip`，用户点「3 篇」却存成无名 zip）；
    仍走 fetch+blob，保留非 2xx 时 flash 友好提示（不跳裸 JSON 错误页）。
  - 顺手删除 A3 节点内已失效的 `_sp` 死变量（此前改走 `dlA3` 后已无人引用）。
  - `block_a.py`：`export_a3_download_list_xlsx` 把清单内两列写成**可点超链接**——
    「PDF 文件」→ 本地 `file:///` URI（点文件名直接打开 PDF）、
    「DOI」→ `https://doi.org/`（蓝字下划线）；新增 `_file_uri()`：
    盘符冒号保字面量（编成 `%3A` Excel 打不开）、中文/空格百分号编码；
    DOI 前缀归一（剥掉来源自带的 `https://doi.org/`，否则拼成 `https://doi.org/https://...`）。
  - 验证：`_file_uri` 单测（中文/空格 → `file:///C:/Users/.../%E4%B8%AD%E6%96%87%E5%90%8D.pdf`）；
    导出实测两个真实会话——`ff-364dd78250eb`（3 篇，无 DOI）得 3 个 G 列链接；
    `ff-0558b5da7736`（2 篇 + 完整 URL 形式 DOI）得 4 个链接且 DOI 已归一为单层；
    `ff-65e2e0076337`（59 篇）得 61 个链接无异常；
    内联脚本 `node --check` 通过、`a3ExportLinks(3)` / `a3ExportLinks(null)` 渲染输出人工核对。

- **A3 之后强制进入 B1（无论是否提取数据）（2026-09-19）**：
  用户要求：A 流程「PDF 下载（A3）」节点完成后，不再停在「下载完成即终点」页，而是**强制进入 Block B（B1 合并计算）**，无论 A4 是否提取 / 是否上传过数据。
  - `fullflow.py`：移除两处「无数据 → done」终止——① `_advance` 中 `letter=="B"` 且无 `studies_for_b` 时直接置 done 的守卫；② A 块完成且无数据时返回 done 的分支。改为 A 完成后一律 `cursor→B` 并续跑。
  - `block_b.py`：`run_block_b` 在 `studies` 为空时返回 B1 以 `await_data` 停靠（不调 coze、不级联到 C），提示在 B1 内上传 / 录入 2×2 数据。
  - `server.py`：新增 `POST /api/b_upload_data`（复用 `block_a.parse_raw_csv` 解析 CSV/Excel/粘贴文本）→ 写 `handoff.studies_for_b` → cursor 复位到 B → 重算 B1。
  - `workbench.html`：`renderNode` 在 `aw.nha.await_data` 时改走 `renderB1UploadPanel()`（取代默认审批动作），新增 `b1UploadData()` 调 `/api/b_upload_data` 并刷新。
  - 验证：模块级 + 线上 HTTP 双验证——无数据→B1 `pause`/`await_data=True`；上传 2×2→B1 重算（k=2）并续跑至 B2。

### Fixed

- **英文稿件里的中文渗漏 + 一处「假引文」（2026-09-22，用户反复反馈「里面还有中文」）**：
  C1 初稿是英文稿件，但多处把**用户提供的中文值**直接拼进英文句子，且有一处把中文
  **模式名**冒充成引文。逐条修，规则统一为「不臆造翻译、不静默丢弃、显式标记源语言」：
  1. **过度声明段（假引文 + 中文）**：`block_b.detect_overclaims` 的 `hits[].evidence`
     存的是**12 类模式的中文简称**（如「亚组结论外推总体」），**不是**被扫描到的原文片段。
     旧实现把它当引文引用、还标注 `(verbatim excerpt from the scanned source text)` ——
     引文是假的，中文是真的漏进正文。现改为：用 `label_en`；`evidence` 仅在其本身为
     ASCII 时才作括注，否则指向 B3 的 `scan` 记录（那里才是原文落点）。旧信封无
     `label_en` 时退到语言中立的模式编号（`pattern OC1`），不再回落中文。
  2. **GRADE 降级理由**：旧信封只有中文 `reasons`（无 `reasons_en`）时，中文直接进 Methods。
     现过滤中文项并补一句「N further rationale(s) omitted here (recorded in the source
     language in the GRADE assessment)」——不静默丢信息。
  3. **PICOS / 检索期 / 数据库**：中文值拼进英文句子会产生「慢性肾脏病患者 is a question
     with an uncertain aggregate effect」这类**不合语法**的中英混杂。现分两路：
     字段**列示**处（PICOS / Eligibility / Search strategy）原样保留 + 标 `[source language]`；
     英文**叙述句**里（摘要背景、讨论）不内联，改用通用表述。Methods 末尾统一加
     `Note on field language` 列出哪些字段是源语言、投稿前需补英文。
  4. 顺带删掉 `c1_draft` 内**遮蔽模块级 `_has_cjk` 的同名本地定义** —— 它会让本行之前
     定义/调用的嵌套函数引用到「尚未绑定的局部变量」而 `NameError`（改 oc 渲染时踩到）。
  - 逐输入组合扫描（全英文 / 旧信封 / 中文 PICOS / 中文 studies / 中文 search_info）：
    除**设计如此**的中文标题外，英文叙述句已零中文；剩余中文只出现在带 `[source language]`
    标记的字段列示与脚注里。
  - 新增 3 条断言锁住该不变量（`test_block_c.py`）：英文 label 生效且无 CJK、旧信封退到
    模式编号且无 CJK、ASCII evidence 仍作括注不丢信息。
  - **未改（如实记录）**：参考文献里中文论文的**原始中文标题 / 中文作者名**保留不动 ——
    那是被引文献的原始著录，翻译/罗马化会变成臆造。投稿前需作者自行补英文题名。

- **「跳至 C 撰稿」不传信封时仍被前端拦下，演示兜底根本走不到（2026-09-22）**：
  后端已实现三级兜底（粘贴 `b_env_text` → 上传 `.json` → 内置示例信封），但
  `workbench.html` 的 `doStartData()` draft 分支在提交前强校验
  `if (!files.length) { flash("请先选择 B 信封 JSON 文件", "err"); return; }`，
  把后两条路**全挡在浏览器里**，用户点「启动流程」只看到一句红字。
  - 修法：与 `raw_csv` 分支对齐 —— 优先读粘贴框、其次上传文件，**两者都空则放行**，
    由后端兜底取内置示例信封，并给一行「未提供 B 信封，将用内置示例信封演示 Block C
    全流程」的提示（不再 return 中断）。
  - 顺手补齐粘贴框：draft 区块原先**只有文件选择**，但提示文案已写着「未上传
    **也未粘贴**」——文案是空头承诺，且后端的 `b_env_text` 入参（2026-09-22 新增）
    没有对应 UI 可填。现新增 `data_benv_text` textarea（与 raw_csv 粘贴框同款样式），
    提示改写为「粘贴与上传二选一，两者都留空则走下方演示信封」。
  - 验证（三条路径 + 真实浏览器）：
    | 路径 | 结果 |
    |---|---|
    | 不传任何东西 | 200，落在 `C1.draft`/pause，稿件 4620 字 |
    | 粘贴 `b_env_text`（真实会话 envelope，2716 B） | 200，`C1.draft`/pause，4229 字 |
    | 上传 `.json` 文件 | 200，`C1.draft`/pause，4229 字 |
    | 真实 Chrome 点「启动流程」（文件空 + 粘贴空） | **`C1.draft`/pause，4656 字，未拦截** |
  - 浏览器验证脚本 `_tmpio/cdp_draft.py`（CDP：填主题 → 选 draft → 不传 → 点击 → 断言落点），
    可复用为快速通道的前端回归。

- **稿件把 I² = 34.5% 渲染成「I² = 3453%」：消费端二次 ×100（2026-09-22）**：
  在 coze 代码镜像 `adapters/coze` 内核对后确认——**`pairwise.I2` 在所有进入生产计算的
  引擎下统一为百分数（0–100）**，不是比例：
  - `coze_contract.md` §4 明写 `stats.heterogeneity.I2` **恒为百分数**，「netmeta/netcomb
    原生返回比例（0–1），引擎侧已 ×100 换算，**消费端不要二次换算**」；
  - `run_task.R:511`（NMA）/ `:1256`（CNMA）确有 `I2 * 100`；pairwise 直接取 `fit$I2`
    （meta/metafor 原生即百分数）；
  - `_coze_stats_to_pairwise`（`block_b.py:374`）原样透传 → `pairwise.I2` = 百分数。
  但 `block_c.py` 三处又乘了一次 100：`i2_line`（**被摘要/方法/结论/局限性四处复用**）、
  局限性句 `i2 * 100`、给 LLM 的 `stats_line` 内 `I2=`——实测把 34.5% 印成 **3453%**，
  且局限性阈值写成 `i2 > 0.25`（百分数口径下几乎恒真，等于永不区分异质性高低）。
  修法：三处去掉 `* 100`，阈值改 `i2 > 25`。
  连带统一本地 oracle：`b1_pairwise_python` 原产出**比例**（`(Q-df)/Q`），与
  `_coze_stats_to_pairwise` 明文声明的「同构」不符，导致 `b2_grade` 的
  `I2 >= 75/50/25` 判据在 oracle 数据下**全部假阴性**（不一致性降级永不触发），
  理由文案还会印成「I²=0%」。已在 oracle 侧归一为百分数（与契约同构），
  并同步更新 `test_block_b.py` 断言（`0..1` → `0..100`）。
  - 验证：端到端重跑演示信封 → 稿件 `I² = 35%`、GRADE 理由「不一致性中等（I²=35% → -0.5）」
    （**修复前该降级是假阴性**）、给 LLM 统计行 `I2=35%`；反向断言稿件中 4 位百分数为 0 条。
  - 回归：`test_block_b` 20 OK(skipped 2)、`test_block_c` 26 OK、`test_writing_advisor` 52 OK、
    `test_interpretation` 19 OK、`test_envelope_guard` 47 OK。
  - 全局扫描已确认：`block_b` 判据（75/50/25）、R 引擎侧（`run_task.R:925`、`meta_analysis_core.R:167-169`）
    与契约 warnings 全部同为百分数口径，无残留 `* 100`。

- **C1 初稿把 log OR 当成 OR 写进稿件（2026-09-22）**：
  效应量的**分析尺度 / 报告尺度**混用：pairwise 的 `TE_random` / `ci_random` 在比值类
  （OR/RR/HR…）上是**对数尺度**（存的是 log OR），稿件里必须取 exp 才能印。旧代码直接
  把 `-0.38` 印成「OR = -0.38（95% CI -0.69–-0.08）」，并拿 log OR 去比无效线 1.0，
  导致方向判定与「CI 是否跨无效线」同时出错。
  - `block_c.py::c1_draft`：新增尺度归一层（比值类集合与 `interpretation._RATIO_SM`
    同一约定）。`eff_line` 改用报告尺度；`direction` / `_ci_cross` 改在**分析尺度**上
    与无效线 `0` 比较（log(1)=0、差值类 0 → 恒为 0）；`_wa_stats.pooled` 按
    `writing_advisor` 既有约定修正为 `estimate_exp`/`ci_lower`/`ci_upper` 报告尺度、
    `estimate` 分析尺度。缺 CI 时降级为 `95% CI n/a`，不再抛 `TypeError`。
  - `block_c.py::build_narrative_prompt`：交给 LLM 的统计行同步换算到报告尺度
    （含 I² 转百分比），否则 LLM 会照着 log OR 写正文。
  - 验证：演示信封实跑 → 稿件由 `OR = -0.38 (95% CI -0.69–-0.08)` 变为
    `OR = 0.68 (95% CI 0.50–0.92, p = 0.013)`，方向 `decreased` 正确。
  - `tests/test_block_c.py::test_sections_and_numbers` 同步更新：该断言原先锁定的正是
    bug 行为（`assertIn("OR = 0.48")`），现改为断言报告尺度 `OR = 1.62` / CI `1.23–2.12`
    并反向断言不再出现 `OR = 0.48`。`test_block_c` 26 OK、`test_block_b` 20 OK。

- **清掉两处「声明与实现不一致」的陷阱：死修订键 + 修订模式覆盖只读声明（2026-09-20）**：
  两处已存在但本轮才被发现的问题，均为「写了 A、实际做 B」，比直接不提供该能力更容易误判。
  - **① `fullflow.EDITABLE_KEYS` 移除 `"B3.overclaim": ["claims_text"]`（死配置）**：
    `claims_text` 是 B3 的**输入**（由 `_build_claims_text` 从选题 + A2 文献标题/摘要派生），
    **不在** B3 的 `stage_result` 里 → 两处消费点
    （`fullflow.py` 构建 `editable_payload` 的 `{k: sr[k] for k in EDITABLE_KEYS.get(sid,[])}`）
    取不到该键，`editable_payload` 恒为 `{}`；且 `_run_block` 的 B 分支每次都重拼文本、
    从不读 `latest_revision("B3.overclaim")` → **即便收录，用户改完提交也传不到下游**。
    已核实无第三方依赖：`scripts/flow_menu.py` 只在标签表里出现 `B3`，没有以 `claims_text`
    为 `key` 的 revise 菜单项（`_filter_options` 只**过滤**已声明选项，不会从字典自动生成）。
    B3 按裁定保持 `gate_type="auto"`（不可修订），故该键本就不该存在。
    另在 `EDITABLE_KEYS` 上方写明收录规则（**既要在 `stage_result` 里真实存在，又要在
    `_run_block` 里被 `latest_revision()` 真正消费**）与将来若要开放「人工补充待扫描文本」
    需同时做的三件事，避免再次出现同类陷阱。
  - **② `workbench/workbench.html` 修订模式不再覆盖 schema 的 `editable: false`**：
    `viewStage(sid, true)` 原先无条件 `Object.assign({}, p, {editable: true})`，把「打开可编辑
    修订」当成「所有面板都可编辑」，**覆盖了 schema 里明确声明的只读** → B3 的「命中项」/
    「12 类检测模式图例」rowlist、C2「命中项」、「通用确认节点」的原始数据 json 会变成输入框，
    并往 `DRAFT` 灌进一批没有对应 `revision_key` 的无意义键。
    改为**只尊重显式 `false`**（`p.editable === false ? false : true`）：显式只读的一律只读；
    未声明的仍放开 —— 这一点是必须的，**B1 正是靠它获得修订能力**（`EDITABLE_KEYS` 收录了
    `pairwise`/`nma`，但 B1 的面板都没有写死 `editable`/`revision_key`），若改成「只有显式
    `true` 才可编辑」会**打断 B1/B2 的修订**。
    - 已知副作用（**有意接受**）：C3「核验结果」/C4「QA 结果」两个面板本就显式声明
      `editable: false`，修复后其修订模式变为纯只读 —— 即「✎ 继续 / 修订」进去只能
      「提交修订」（空 revision）触发重算，不能再手改原始校验 JSON。作者原意即只读
      （面板文案写着「核验结果」，且通用兜底节点明写「只读」），故按声明执行。
      另注：C3/C4 的 `EDITABLE_KEYS`（`references`/`manuscript`）**在同名 schema 里没有绑定面板**，
      属另一处「声明与实现不一致」，本轮未动，已记录待定。
  - 验证（规则级，纯函数、不依赖数据）：遍历 11 个节点全部 44 个 panel，按新规则计算
    「修订模式有效 editable」→ 显式 `false` 的 6 个面板（B3×2 / C2×1 / C3 / C4 / 通用兜底）
    **全部保住只读，被误覆盖数 = 0**；A2「逐条裁决」显式 `true` 仍为可编辑。
  - 验证（渲染级，真实 Chrome + CDP，`_tmpio/cdp_revise.py`）：注入 `form_schema` 的**真实
    schema** 后逐个跑 `viewStage(sid, true)`，统计产出的 `[data-rk]` 可编辑键 →
    B3 = `['preview','downstream']`（`hits`/`patterns` 已剔除）、C2 = `[]`、C3 = `[]`、C4 = `[]`、
    **B1 = `['pairwise','nma']`（未回归）**、A1 = `['include_reviews','report']`、
    B4 ⊇ `report`、C1 ⊇ `manuscript`，8/9 断言 PASS。
    （唯一未过的 A2 断言是**测试数据造成的假阴性**：A2「逐条裁决」面板 `path="nha.decisions"`，
    而 `viewStage` 的 ctx 里 `nha` 恒为 `{}` → `renderRowlist` 对空数组提前 return、不产出
    任何 `[data-rk]`；规则级校验已确认其声明为 `True` → 有效值仍为 `True`。）
  - 回归：`tests/test_flow_menu.py` **186 PASS / 3 FAIL（与基线逐条一致）**、
    `adapters/tests/test_block_b.py` 20 OK、`tests/test_envelope_guard.py` 47 OK、
    `adapters/tests/test_fullflow.py` 6 FAIL（**既有基线**，源自 09-19 语义变更）、
    `tests/test_a4_b1_handoff.py` 本地 R 引擎缺失导致的既有失败。`py_compile` + 内联 JS
    `node --check` 通过。HTML 仍由 `index()` 每请求现读，**无需重启后端**。

- **工作台：等待中的红线闸标题错标成「🟡 软停」（2026-09-20）**：
  `workbench/workbench.html` 的 `renderNode()` 判的是 `sc.gate_type === "red"`，而
  `form_schema.py` 只会产出 `"redline"` / `"soft"` / `"auto"` 三个值 —— **该红色分支是死代码**，
  于是三选一永远落到 else。后果：**当前正在等待用户放行的红线闸（B4 质量门 / C3 参考核验 /
  C4 投稿前终闸）标题 pill 显示成「🟡 软停」**，把「必须人工显式放行」的终闸渲染成普通软停，
  是最不该出错的时刻出错。铁证：同一文件 `viewStage()` 的同类判据用的是正确的 `"redline"`，
  说明这是笔误而非设计。修复：`"red"` → `"redline"`，并把三值含义写进注释。
  注：`auto` 与 `soft` 在此处（停靠点视图）都落「🟡 软停」是**正确**的——二者此刻确实都在
  等人确认；`auto` 的语义按本轮裁定统一为「自动计算 + 软停复核」（见 Changed 段），
  故 B1/B2/B3 维持 `auto` 不动，仅修此笔误。
  验证：真实 Chrome（CDP）驱动，给 `renderNode()` 分别喂 `redline` / `soft` / `auto` / 未知值，
  断言标题 pill 文本 → `redline` 得到「🔴 红线闸」、`soft`/`auto` 得「🟡 软停」、未知值安全
  回退「🟡 软停」，**ALL PASS**（修复前 `redline` 会输出「🟡 软停」）。内联 JS `node --check`
  通过。HTML 由 `index()` 每请求现读且 `Cache-Control: no-store` → **无需重启后端**即生效。

- **线上服务起不来：`block_c.py` 用了 Python 3.12+ 才允许的 f-string 反斜杠（2026-09-19）**：
  现象：本地全链路全绿，重新发布后线上 60s 内不可达，日志报
  `block_c.py:324 SyntaxError: f-string expression part cannot include a backslash`。
  根因：线上运行时是 **Python 3.11**，本地开发是 **3.13** —— `manuscript` 的 f-string 在
  **表达式部分**用了 `\n` 与行尾续行 `\`（PEP 701 自 3.12 才放开），3.11 在 import 阶段即
  SyntaxError，而本地 `py_compile` 永远发现不了（本地能编译 ≠ 线上能运行）。
  修复：
  - `block_c.py`：三段「写作辅助」段落（本研究优势 / 局限性 / 讨论要点）预拼为 `wa_block`
    移到 f-string **外部**，模板内只留 `{wa_block}`；
  - 同处顺手修掉文案重复：`eff_line` 原为「`OR 合并效应 = 0.57 (...)`」，而调用方模板已带
    「主要合并效应」前缀 → 输出成「主要合并效应 OR 合并效应 = ...」；现改为 `OR = 0.57 (...)`。
  防复发（新增工具链守卫）：
  - 新增 `adapters/workbench/publish-kit/check_py311.py`：tokenize 级扫描 f-string **表达式区间**
    内的反斜杠（注：`ast.parse(feature_version=...)` 不可用——它不回溯 f-string 的 tokenizer
    限制、会给出假阴性）+ PEP 695 泛型语法粗筛；
  - `build_publish.py` 构建末尾调用该守卫，发现问题即 `sys.exit` **阻断发布**。
  验证：守卫自检（坏样本 2 处 → 退出 1；好样本 → 0）；本地 + 线上端到端各 7/7；
  Playwright 真实 UI 链路（演示启动 → B1→B2→B3→B4 → C1）确认初稿正文 1061 字符可编辑呈现。

- **done 页两个成果导出按钮「点了没反应 / 跳裸 JSON」（2026-09-19）**：
  根因两层：① `renderDone()` 在 done 态下无条件渲染「⬇ 下载全部 PDF（zip）/ ⬇ 下载确认清单（Excel）」
  两个 `<a href>` 按钮，但 done 态 `stage_results` 不含 A3 `per_doc`，前端无法判断后端是否真有可导出
  成果；无成果的会话（如 `ff-1e6bf5d7fb76`：A2 skipped、A3 空过）后端正确返回 400，按钮却依然显示。
  ② `<a href>` 直跳下载端点，出错时浏览器导航到裸 JSON 错误页（`{"detail":...}`），用户看起来就是
  「按钮不起作用」。
  修复（server.py + workbench.html，需重启服务）：
  - server.py 新增 `GET /api/a3_export_status`：复用 `block_a._a3_result_of` + `_downloadable_docs`
    返回 `{n_docs, n_downloaded}`（done 态前端本地判断不了，直接问后端事实）；
  - workbench.html 新增 `dlA3(kind)`：fetch + blob 下载，`Content-Disposition` 失败时回退固定文件名
    （A3_PDF全文.zip / A3_PDF下载清单.xlsx），非 2xx 时解析 `detail` 弹友好 flash + 底部日志；
  - `renderDone()` 改为先渲染骨架，异步查 `/api/a3_export_status`：有成果（n_docs>0）才渲染两个
    按钮（并显示真实篇数），无成果渲染中性解释（原因 + 如何重跑下载），查询失败也保留可重试按钮；
  - A3 流程内「成果导出」面板的两按钮同步改为 `dlA3`（原来同样存在裸 JSON 问题）。
  验证：`/api/a3_export_status` 对 `ff-1e6bf5d7fb76` 返回 {0,0}（会话确实无可导出——A2 被跳过、
  A3 无下载明细，runs 根目录 doc1-10.pdf 为 9 月 3 日其他会话产物，与本会话无关）；对含下载结果的
  `ff-364dd78250eb` 返回 {3,3}，zip 实测 HTTP 200 / 5.5MB（3 篇 PDF + 下载清单.csv），xlsx HTTP 200。

- **流程 done 态误报「Block C 终闸已放行」（2026-09-19）**：
  `renderDone()`（workbench.html）原先用 `docs.length > 0 && /PDF 全文下载已完成|不提供数据提取/.test(prompt)`
  区分「下载-only 终点」与「全链路完成」。但 done 态下 A3/A4 的 `per_doc` 根本没进
  `stage_results`（信封 `stages` 只列 A1/A2，A3.pdf_download 永远不在其中），
  导致 `docs` 恒为空 → `docs.length>0` 恒为 false → **下载-only 终点（仅 A 块跑过、
  B/C 从未运行）被误判成「Block C 终闸已放行 / C1→C3→C4 全部通过」**，与事实相悖。
  修复：改用事实信号 `STATE.progress` 里 B/C 块是否实际出现过（A-only → 下载终点；
  B/C 跑过 → 真实全链路完成），不再依赖脆弱的 `docs.length` / 提示文案猜测；
  并对「0 篇可打包」情况给中性说明。仅改 workbench.html，刷新即生效，未重启。
  验证：用户 done 会话 `ff-1e6bf5d7fb76`（progress 仅 A）→ 现正确显示「PDF 全文下载已完成」；
  真实跑到 C 的会话 `ff-413a0335d09a`（progress 含 A/B）→ 仍正确显示 C 终闸放行。

- **A4「下载 PDF」界面部分文章状态显示英文 `deferred`（2026-09-19）**：
  `renderA4Downloads()`（数据提取关闭时的持久化下载清单视图）的 `stMap` 漏列
  `deferred` 状态，导致该状态走兜底分支、直接把后端原值 `deferred` 当文案显示成
  英文。这些文章**并非失败**，而是因本轮回填的实际下载上限（`max_attempts`）已耗尽、
  留待下一轮自动获取。修复：① `stMap` 补 `deferred: ["#6b7785", "未下载·达上限"]`；
  ② 统一另三处状态映射（实时下载日志 `addRow` MAP、`renderA4LiveDoc` MAP×2、
  `A4DOC_STATUS`）的 `"延后(配额)"` → `"未下载·达上限"`，消除歧义、四视图术语一致；
  ③ 该视图对 deferred 篇目追加说明条，解释原因并指引「下一轮 A4 下载阶段自动获取」或
  「待上传 / 补抽取 PDF」手动上传两条路径。仅改 workbench.html，刷新即生效。

- **A2「文献集」单击标题展开的摘要被截断为一行带省略号（2026-09-19）**：
  详情行 `abstract_snippet`（标签「摘要」）原本按普通 `.rl-df` 渲染，
  受 `white-space:nowrap; overflow:hidden; text-overflow:ellipsis` 影响被截成
  单行省略号。新增 `para` 字段型：标签独占一行、正文整段显示在下方
  （`form_schema.py` 给该字段加 `"type":"para"`；`workbench.html` 的
  `renderRowlist` 与 CSS `.rl-df.para` 配套实现），其余字段（刊名/年份等）
  维持内联不变。

### Changed

- **左侧「流程进度」字号放大（2026-09-19）**：
  用户反馈左栏时间轴的 `A1 / A2 …` 阶段代号过小。统一放大三处
  （workbench.html，仅 CSS，刷新即生效）：
  `.tl li .seq`（A1/A2 代号）`10.5px → 13px`、`min-width 22px → 27px`；
  `.tl li .lbl`（阶段名，选题/检索/合并计算…）`13px → 15px`；
  `.tl li .tag`（状态签）`11px → 12.5px`；左栏卡片标题
  `#wb-pane-left > h3` `12px → 13.5px`（**仅左栏**，中/右栏卡片标题不变）。
  行高变大后同步微调状态点/连接线位置：`.tl li .dot` `top:14px → 15px`、
  `.tl li::after` `top:27px → 29px`，保持圆点与连接线对齐。

- **隐藏「⏭ 跳过」决策按钮 + 取消/返回按钮改中性样式（2026-09-19）**：
  用户反馈「跳过按钮」功能不清晰，两类来源：
  ① 软停节点的 `⏭ 跳过` 决策按钮（引擎 `skipped` 动作，语义≈「本会话不再在此停靠」，
  与「批准」重叠）→ 在 `renderActions` 内用 `const SHOW_SKIP = false` 守卫隐藏，
  **后端 `skipped` 动作保留**，改 `true` 即恢复；软停节点始终有 `✓ 批准` 可走，流程不被阻断。
  ② 四处取消/返回按钮（打回选择器取消、只读/修订视图「← 返回」「取消」）原套用橙色
  `.btn-skip` 样式、与跳过按钮视觉混淆 → 全部改为中性 `.btn-ghost`。`.btn-skip` CSS 规则
  保留备用（skip 恢复时自动生效）。仅改 workbench.html，无需重启。

- **步骤切换 / 刷新提速：`/api/session` 按文件 mtime 加状态缓存（2026-09-19）**：
  工作台会话文件已达 ~2.4MB（A2 文献集 104 篇 studies + abstracts），原先每次
  `/api/session` 都要「读盘 2.4MB → 解析 → 重建 stage_schema/stage_results →
  再序列化 2.4MB 下发」，实测 ~0.88s/次；任何一次**刷新页面 / reloadSession**
  都白吃这一轮。改为按 `(path, mtime_ns)` 记忆 `build_state` 结果：文件未变即命中
  缓存跳过整段重活。实测重复调用 **0.88s → 0.05s（约 17×）**。
  用纳秒 mtime（NTFS 100ns 分辨率）防「同秒写盘」误命中；`mutating` 端点另可
  `_invalidate_session` 双保险（本次仅依赖 mtime，未显式调用）。
  > 纯后端改动，需重启 uvicorn 生效（约 85s 慢导入期）。

- **慢操作明确「请耐心等待几分钟」提示（2026-09-19）**：
  真正耗时的操作（多库检索、PDF 全文下载）是网络 / R 计算受限，无法提速，但原先
  前端提示语（「约 15–60 秒」「耗时较长」）严重低估，易误判为卡死。按用户要求，
  在三个 SSE 流式端点的 `stage_hint` 加显式长等待提示：
  - `/api/start_stream`：检索「单库超时上限 5 分钟，整体通常需要几分钟，请耐心等待，不要关闭或刷新页面」
  - `/api/rewind_stream`：回退重算「可能联网重新检索 / 下载全文，需几分钟，请耐心等待，不要关闭或刷新页面」
  - `/api/decide_stream`：上下文感知——含修订 → 重算下游可能数分钟；
    批准 A1/A2 → 后续可能联网检索或逐篇下载 PDF，达数分钟；
    其余 → 部分步骤可能耗时数分钟；均提示「不要关闭或刷新页面」。

### Changed (prior)

- **长标签不再折行：`.kv` 标签列由死宽 140px 改为自适应（2026-09-18 第六次修订）**：
  用户反馈 A2「未翻译残留」面板的标签「需自行翻译为英文的片段（非空 = 境外库会漏检）」
  **仍然折行**（24 字塞进 140px 标签列 → 折成 3 行）。改为
  `grid-template-columns:minmax(140px, max-content) minmax(0, 1fr)` + `.kv .k{white-space:nowrap}`：
  标签 nowrap 后其 min-content 即全文宽度，轨道自动取该面板**最长标签**的宽度
  （实测 Microsoft YaHei 13px 下该标签 **291px**），同面板内所有值仍左对齐同一列。
  短的标签面板不受影响（「待下载（初筛通过）」117px < 140px 下限，仍走 140px）。
  ≤560px 极窄屏降级回 `minmax(120px,40%)` + 允许折行，避免 nowrap 把网格撑出面板。
  > 本次只动 `workbench.html`（CSS），**刷新即生效，无需重启**。

- **A2「文献集」概览面板改 3 列网格（2026-09-18 第五次修订）**：`kind:"object"` 原先固定
  `grid-template-columns:140px 1fr` —— 每个字段独占一整行，检索概览 6 项 = 6 行、初筛统计 5 项 = 5 行。
  改为**由 schema 的 `cols:3` 触发** 3 列网格（新增 `.kv3` / `.kv3-cell`）：
  1. **检索概览**（`cols:3`，6 项）→ **3 × 2 两行**；
  2. **初筛统计**（`cols:3`，5 项）→ **3 + 2 两行**；
  3. **单项单行不折行** —— `.kv3-cell` 用 `grid-template-columns:max-content minmax(0,1fr)`，
     标签列 `max-content + white-space:nowrap`，值列同样 nowrap（超长才 `ellipsis` 兜底）；
  4. **默认形态不动** —— 仅 `cols:3` 的面板走新网格；未标 `cols` 的（如「未翻译残留」，
     标签是「需自行翻译为英文的片段（非空 = 境外库会漏检）」24 字）继续用 140px 标签列的纵排，
     避免被 nowrap 截断。
  5. 响应式：≤900px 降 2 列、≤560px 降 1 列。
  > 注意：`form_schema.py` **不像** `workbench.html` 那样每次请求重读，改完**必须重启 uvicorn**
  > （见 `workbench_server.log` 的 restart 标记）。

- **「数据准备状态」选项改单行并排（2026-09-18 第四次修订）**：原先 `#datamode-seg` 是
  `grid-template-columns:1fr 1fr`（2×2），当前特性开关下实际只有 3 个选项
  （`/api/features` → `a4_extraction:false`、`fastpath_pdf:false`，故「已备好全文 PDF」不渲染），
  于是第三项单独占半行、卡片被无谓拉高约 34px。改为
  `display:flex; flex-wrap:nowrap` + `.seg-opt{flex:1 1 0; min-width:0}`：
  **任意选项数（3 项或特性全开 4 项）都均分同一行**，不再依赖写死的列数；
  容器 `align-items:stretch` 让各选项等高对齐。≤560px 断点回归纵向堆叠
  （`flex-wrap:wrap` + `flex-basis:100%`），避免窄屏挤成文字墙。
  实测 `.start` 卡片 920px 宽下每项约 288px，三行文案均单行不折行。

- **左栏加阶段顺序标签 + 右栏审计日志默认收起（2026-09-18 第三次修订）**：
  1. **时间轴顺序标签**：`renderTimeline()` 在行首增加 `<span class="seq">`，取自 `stage_id` 前缀
     （`String(sid).split(".")[0]` → `A1 / A2 / A3 / B1 … C4`）；等宽字体 +`min-width:22px` 保证标签左对齐，
     颜色随状态走（future `--wb-muted`、done `--wb-sub`、await `--wb-warn`、gate `--wb-err`）。
     好处是截图/口头沟通可以直接引用「A3」「B4」而不必描述中文名。
  2. **审计日志默认收起**：`<body class="… wb-audit-off">`，右侧 `<aside id="wb-pane-right">` 默认
     `display:none`；`.layout` 第三轨由 `340px` 改为 `auto`，配合 `#wb-pane-right{width:340px}`
     （仅在 `min-width:1081px` 内声明，避免破坏 ≤1080px 的两栏断点），收起时整轨塌缩为 0。
     实测中央工作区宽度 **718px → 1074px（+356px）**。
  3. **顶栏新增「审计」开关**（`#wb-audit` + `wbToggleAudit()`，文案入 I18N `auditBtn`）：
     面板收起时一键唤回，偏好记忆在 `localStorage.wb_audit`；面板可见时按钮点亮（`.wb-btn.on`）。
     业务 JS 全部保持写入 `#audit`，DOM 与 `STATE.audit` 不变，**审计数据不丢**。
  4. **A3/A4 裁决表兼容**：既有 `body.a3-active .layout{280px … 0px}` 规则与新规则特异度相同且位置更靠前，
     故新规则用 `:not(.a3-active)` 让位，保持裁决表原有宽度；同时 `body.a3-active #wb-audit{display:none}`
     避免「按钮点亮但面板被强制收起」的错位。
  5. **表单可用宽度提升**：`.start` 上限 680 → **920px**（原先受 340px 右栏挤压，现真正吃得下）。
- **开始页整页缩短约三分之一（2026-09-18 二次修订）**：原分区化后表单区约 1180px、需滚动才看全；
  本轮做**纵向压缩**，改后 `.start` 实测 **671px**、整页 `doc_h` **904px**（1440×1000 窗口一屏放得下）。
  具体做法：
  1. **省掉一张分区卡** ——「合并效应量尺度」并入底部 `.actions-bar` 操作条
     （`[效应量] [select] ……… [启动流程] [帮助选题]`），单行 61px；
  2. **选项改双列** —— `#datamode-seg` 由 4 行纵排改为 **2×2 网格**（`.seg-opt` 在网格内
     `margin:0 !important` 归零、改由容器 `gap` 控距，因基类带 `!important` 故须同权覆盖），
     选项文案同步收短（「标准全流程（含 PDF 下载）」等，保证单行不折行）；
     原始数据录入方式行改用 `.fs-radio-row`，与网格同款紧凑规则；
  3. **复选框双列** —— NMA / 包含综述两行改用 `.fs-chk2`，两行的长说明压成一句
     （「3 种及以上干预同台比较时勾选。」/「伞评 / 范围综述才需要。」），省约 100px；
  4. **文案瘦身** —— 8 处 2 行说明改 1 行；字段标签去掉括号内的长解释
     （「检索上限（最多拉取多少篇文献记录用于初筛）」→「检索上限」）；
     B 信封 / 全文 PDF 两处冗余的「上传 XXX」标签行删除（按钮文字已表达）；
  5. **间距压缩** —— `.fs` 内边距 15/16→12/14、下间距 14→9；`.fs-hd` 13/10→8/7、字号 13→12.5；
     `.hint` 11.5px/1.45；`.actions-bar` 内边距 11/13；`.start` 宽度 620→680（一行装更多字，行数更少）。
  元素 id 与 `updateDataMode()` / `updateRawInput()` / `updateDemoByEM()` 契约**全部保持**，
  `#em` 仅按 id 取用故可安全移位（已 grep 确认）。
- **开始页「选单框架」分区化（2026-09-18）**：原先是一条平铺到底的长表单，现按语义切成
  **分区卡** `<section class="fs">`（品牌色条 + 分区标题 + 右侧副标签 + 分隔线）：
  研究主题 / 数据准备状态 / 检索与筛选设置 / 原始数据 / B 信封 / 全文 PDF / 合并效应量尺度。
  「检索上限 + 起始年」改双列网格 `.fs-grid2`（窄屏 ≤560px 回落单列）；操作区独立为
  `.actions-bar` 浅底条。所有元素 id 与 `updateDataMode()` / `updateRawInput()` /
  `updateDemoByEM()` 的挂载契约保持不变。
- **工作台前端视觉精修（2026-09-18）**：在 ct-base/workbench_ui.md 规范内提升界面层次与精致度 ——
  页面底色叠加极淡品牌光晕、卡片层叠阴影 + 悬停轻抬 + 顶部品牌高光、时间轴升级为带连接线的步进器、
  卡片标题 / 节点标题加圆角品牌色块标记、按钮悬停轻抬、空态改为图标居中提示、通用面板左侧 4px 品牌色条、
  统一键盘焦点描边。全程仅用既有 `--wb-*` 令牌与 `color-mix(令牌)` 派生，不新造别名 / 不写裸色 / 不用 emoji，
  标准 Chrome 与四区结构不变（`adapters/workbench/workbench.html`）。
- **表单控件精修（2026-09-18）**：`input[type=radio|checkbox]` 统一 `accent-color:var(--wb-brand)`；
  `.seg-opt` 单选行升级为「整行可点卡片」（hover 高亮、选中态品牌软底 + 左侧色条、`:has(input:focus-visible)` 焦点环）；
  `label.chk` 复选行同款；`select` 去原生外观 + 内联 SVG 下拉箭头；输入框聚焦环改用
  `color-mix(--wb-brand 16%, transparent)` 派生（替换裸 `rgba`），并补齐 hover / placeholder 态。
  同批把增强层内所有裸 `rgba(...)` 投影改为 `color-mix(var(--wb-ink)…, transparent)`，
  顶栏抗色改用 `--wb-on-topbar` 派生，满足 §4.1「不裸写色值」。

### Fixed

- **「打回 / 回退」按钮无效 —— 停在原地不动（2026-09-18 · 用户报告「仍然不起作用，一直停在这里」）**：

  **症状**：在 A2 点「✕ 打回 / 回退」→ 选 `A1.topic_selection` → 信息栏只多一行
  `✕ 打回到 A1.topic_selection（下游块将重算）`，然后界面长时间无反馈，最后仍然停在 A2，
  看上去「按钮没反应 / 卡死」。

  **根因（凭据重放）**：`FullflowSession.rewind()` 刻意**保留 `human_decisions`**（审计不丢），
  而 `decisions_for_block()` 会把历史 `approved` 当凭据重放给块层 → `block_a._soft_stop()` 判定
  「`sid ∈ pause_at` 且 `_any_approve(decisions, sid)`」为真 → **回退点那道闸被自己的旧批准直接放行**。
  于是「打回到 A1」静默跳过 A1、整块 Block A 真实检索重跑（约 2 分钟），又停在 A2 —— 与回退前
  完全同一屏，用户看到的自然是「打回无效」。会话文件里也留着痕迹：`cursor` 停在
  `A2.literature_search`，而 `human_decisions` 里 A1 仍是 `approved`。

  **修复（`adapters/fullflow.py`）**：
  1. 新增 `_stage_order_key(stage_id)` → `(块序, 阶段序号)` 可比较键（`A2.…`→`(0,2)`；块字母 `A`→`(0,0)`，
     表示整块起点）。
  2. 新增 `FullflowSession.invalidate_decisions(from_stage_id)`：把「该阶段及其之后」的人工凭据
     打上 `invalidated = {by:"rewind", to:<目标>, at:<时间>}` 标记。**只打标、不删记录** ——
     审计仍能看出「谁在何时批准过、被哪次回退作废」。
  3. `decisions_for_block()` / `revisions_for_block()` / `latest_revision()` 一致忽略已作废项，
     避免旧 revision（人工 Excel 裁决、手改检索式）在回退后被重新注入覆盖新决策。
  4. `rewind_fullflow()` 在 `rewind()` 之后调用 `invalidate_decisions(target_stage_id)`；
     失败回滚快照机制不变（重跑崩了仍整体还原，含作废标记）。

  **实测（会话副本 dry-run）**：`rewind_fullflow(path, "A1.topic_selection")` →
  `cursor = {block:"A", stage_id:"A1.topic_selection", await_kind:"pause"}`，
  A1 的旧 `approved` 被标注作废，流程真正停在 A1 等人工确认（49.5s，为 A1 的 ct-registry 查重探针）。

- **回退期间界面「假死」（2026-09-18）**：`/api/rewind` 是阻塞式端点，回退会整块重跑
  （打回到 A1 实测约 2 分钟），期间前端只能转圈、日志停在「打回到 X」那一行，无法区分
  「在跑」和「卡死」。新增 **`POST /api/rewind_stream`**（语义与 `/api/rewind` 完全一致，
  复用既有 `_stream_blocking` —— SSE 阶段提示 + 每 2s 心跳 + 子进程实时行），前端
  `rejectAndRewind()` 改走该端点，信息栏持续可见进度；审计留痕逻辑同步搬进 `_call`
  （与重跑结果同一原子过程内）。

- **打回审计备注丢失回退目标（2026-09-18）**：原 `api_rewind` 的备注拼接为
  `(note or "") + (f" 打回并回退到 {target}" if not note else "")` —— **只要用户填了备注，
  「回退到哪个阶段」这个关键信息就完全不落审计**（还会残留前导空格）。抽出 `_rewind_note()`：
  `用户备注 · 打回并回退到 <目标>`，目标恒在；`/api/rewind` 与 `/api/rewind_stream` 共用。

- **文件选择按钮「绿底灰字」不可读（2026-09-18 · 用户报告）**：
  `.start label{display:block;font-size:12px;color:var(--wb-sub);margin:12px 0 4px;}` 是
  **类+元素**选择器（特异度 0,1,1），会**盖过** `.btn-mini{color:#fff}`（0,1,0）——
  于是 `📄 选择数据文件` / `📄 选择 B 信封 JSON` / `📄 选择 PDF 文件` 等文件选择按钮被染成
  **灰字压在实心绿底上**，几乎不可读。修复：把该规则收窄为
  `.start label:not(.btn-mini):not(.seg-opt):not(.chk)`（只管纯文本 label），
  按钮型 / 单选行 / 复选行 label 各自持色；同时把 `.btn-mini.file` 底衬加深一档
  `color-mix(in srgb, var(--wb-ok) 88%, var(--wb-ink))` 提升白字对比度。
  （踩坑与修法已回写 ct-base §4.4.1。）
- **左栏「流程进度」空白（2026-09-18）**：开始页 `STATE` 为 `null` 时
  `renderTimeline()` 内 `STATE.stage_schema` 直接解引用抛 `TypeError`，导致时间轴渲染中断、左栏卡片全空。
  已加 `((STATE && STATE.stage_schema) || {})` 容错；并把初始化 / 「新建」入口由 `renderStart()`
  改为统一入口 `render()`，使时间轴／审计日志在开始页也一次画全（现显示 12 阶段步进器全貌）。
- **SKILL.md 新增铁律 #6「No duplicate fire」+ anti-pattern 显式禁令（2026-09-17 飞书 searchlog 实证）**：
  飞书 CTDB searchlog 显示单次用户请求被 agent 重复 fire 多达 12 次（Cluster 1: 12 次相同 querystr，
  Cluster 2: 8 次），间隔 5~7s（Bash 未返回即重发）或 1~2min（焦虑重试）。所有 26 次调用均 status=ok，
  问题不在 Python 代码（coze_client.py 零 retry），而是 LLM agent 等待焦虑绕过了 §0.5 call-count invariant。
  修复：Five iron rules → Six iron rules，#6 明确「once run_meta.py is in-flight, wait for the result」；
  anti-patterns 段新增 ❌ Impatient duplicate fire 禁令，标注 2026-09-17 field incident。

- **ABC 审查修复 3 高 + 5 中风险（2026-09-17）**：
  🔴 `fullflow._run_block` 漏传 `claims_text` → B3 过度声明文本模式全部失效 → 修复透传；
  🔴 `fullflow._extract_c_grounding` 虚报 `rob_summary = None`（从未赋值）→ 从 B2 节点正确抽取；
  🔴 `flow_menu.A_STAGES` 缺 `A3.pdf_download` → A3 菜单无摘要/无选项 → 补入 `_a3_summary`/`_a3_options`；
  🟡 `EDITABLE_KEYS` 仅覆盖 A1/A2/A4/B4/C1 → B1/B2/B3/C2/C3/C4 修订被误标 blocked → 补全 12 节点；
  🟡 `DEFAULT_PAUSE_AT` 缺 `B2.grade`/`B3.overclaim` → GRADE/过度声明无复核入口 → 补入；
  🟡 `block_c.c3_reference_verify` 中 `references=[]` 与 `None` 语义不一致 → 合并处理；
  🟡 `block_c.py:469-501` 缩进错误（`verify_references` 调用行意外缩进 8 空格）→ 修复；
  🟡 `block_c.c1_draft`/`build_narrative_prompt`/`run_block_c` 签名新增 `ref_sections` → 章节切片透传。

### Added

- **C 档新增 `ref_sections` 参数：参考已纳入文献 PDF 写作风格（2026-09-17）**：
  全链路透传已纳入 meta 分析的 PDF 的章节切片，供写稿时参考同类文献的讨论段/方法段写法。
  仅处理英文 PDF（中文分节锚点不保证稳定）。具体改动：
  1. `pdf_extractor.extract_sections(pdf_path, max_chars_per_section=6000)` — 新增函数，按章节切片 PDF 全文
     （abstract / introduction / methods / results / discussion / conclusion）；CLI `--sections` 冒烟入口。
  2. `block_a._a4_extract_section_texts(studies, pdf_dir, max_per_pdf=6000)` — 对已落盘 PDF 批量抽取章节切片，
     返回 `{study_key: {title, doi, sections}}`，PDF 下载位置记录在 `pdf_cache/` 目录。
  3. `fullflow._extract_c_grounding` — 透传 `ref_sections` 字段给 `run_block_c`。
  4. `block_c.c1_draft` / `build_narrative_prompt` / `run_block_c` — 均新增 `ref_sections` 参数；
     C1 输出附带 `_ref_sections` 元数据；LLM 扩写叙述时附带参考段落。
  5. `writing_advisor.advise_publication` / `_discussion_template` / `_reviewer_questions` — 均新增
     `ref_sections` 参数；讨论段模板在末尾追加「同类文献讨论段参考」块（标注「仅作写作风格/结构借鉴，
     不可直接复制，也不可将其数据视为你的研究结果」）；审稿人问题追加一条参考同类文献的追问。
  6. `run_analysis.run_analysis` — 函数签名新增 `ref_sections` 参数，透传给 `advise_publication`；
     CLI 新增 `--ref-sections <json_path>` 参数。
  截断上限：单节 ≤ 6000 字符；LLM prompt 中每篇截 ≤ 1500 字符，最多取 3 篇，总计 ≤ 4000 字符。
  新增 CLI 冒烟入口：`python pdf_extractor.py --sections <pdf>`。
  验证：12 项导入链检查 + py_compile 6/6 全部通过。

- **Block C 初稿升级为「可直接投稿的完整初稿」（C 档，2026-09-17 用户要求）**：
  原 C1 `c1_draft` 仅产出 ~872 字符骨架（背景/讨论/结论为「（待撰写）」空占位），与
  「直接投稿完整初稿」预期差距大。本次：① 扩展 `c1_draft` 入参接收上游真实素材
  （studies_list / prisma_flow / picos / search_info / rob_summary / merged_json），方法段填真实
  数据库+日期+检索式+PICOS+RoB 工具、结果段填 PRISMA 筛选数与研究特征、参考文献由 A2 DOI 直接落表交 C3 核验；
  ② 接通此前孤立的 `writing_advisor` 引擎（strengths/limitations/discussion_template/reviewer_questions/journal_fit 注入讨论段与投稿建议）；
  ③ 新增 `build_narrative_prompt` + `c1_expand_narrative` 接口，由编排层注入 LLM 写出背景/讨论/结论/摘要叙述（本地单测不注入 llm，保持确定性）；
  ④ `fullflow` 新增 `_extract_c_grounding` 把 Block A 信封的文献集/PICOS/PRISMA 流/检索源透传给 `run_block_c`（draft 快进模式无 A 时优雅降级）；
  ⑤ `SKILL.md` 注册 `writing_advisor` 触发器与能力说明（解 D-DEP-1）。
  实测：3 项研究 + 真实素材下 char_count 872 → 1873；接 LLM 扩写后产出完整初稿。
  `test_block_c` + `test_writing_advisor` 78/78 通过；`fullflow` 导入正常。
  注：`tests/test_flow_menu.py` 的 A4 节点 harness 因 9/17 A3/A4 重构后 `form_schema.STAGE_ORDER`
  与测试预期漂移（pre-existing，与本改动无关），须另行修复。

- **首页粘贴示例随「合并效应量尺度」联动（2026-09-17 用户要求）**：
  用户指出「根据要分析的效应量不同，数据格式 demo 应该有不同变化」—— 此前 5 个效应量共用一套
  2×2 示例，选 MD/SMD/HR 时示例文不对题。现按效应量分套，且**后端解析器一并扩展**
  （否则示例只是摆设，点了会解析失败）：
  1. **示例分套**（`block_a.DEMO_RAW_CSV_BY_EM` 与 `workbench.html` 的 `DEMO_BY_EM`，两处需同步）：
     · OR/RR（二分类）→ `study,ai,bi,ci,di` 四格计数；
     · MD/SMD（连续）→ `study,mean_exp,sd_exp,n_exp,mean_ctrl,sd_ctrl,n_ctrl`；
     · HR（生存）→ `study,hr,ci_low,ci_high`。
     前端在 `#em` 变化时同步更新粘贴框 placeholder 与「列名规则」说明
     （`updateDemoByEM()`，`renderStart` 末尾初始化）；`/api/start_data` 的演示路径按
     `effect_measure` 取对应示例。
  2. **解析器扩展**（`block_a.parse_raw_csv`）新增两条识别路径：
     · **连续结局**：识别 `mean_exp/sd_exp/n_exp/mean_ctrl/sd_ctrl/n_ctrl`（含 `mean1/sd1/n1`、
       中文「试验组均值 / 标准差 / 样本量」等别名），按契约默认列名原样产出
       （`block_b._norm_b1_rows` 对未知列原样透传，直达 R 引擎 `escalc` / `metacont`）；
     · **生存结局**：识别 `hr` +（`se` 或 `ci_low/ci_high`）→ 换算为对数尺度
       `te = ln(HR)`、`sete = (ln UL − ln LL) / 2·1.96`；亦支持直接给 `loghr + se`。
  **验证**：五套示例全部解析成功（HR 得 `te = ln(0.72) = -0.3285`、`sete = 0.1092` 由 CI 正确反推）。
  前端真渲染 **8/8**：5 个效应量均有示例、三类格式正确、MD 与 SMD 数值不同、列名说明随动、
  0 JS 错误。

- **首页「自备原始数据 → 直接进 B」支持演示模式：未提供数据时用内置示例跑通（2026-09-17 用户要求）**：
  用户在首页选该通道但既未上传文件也未粘贴数据时，原先被 400 拦截；现改为**用内置示例数据
  继续流程**，便于先看合并计算结果。
  1. `adapters/block_a.py`：新增 `DEMO_RAW_CSV` + `demo_raw_rows()` —— 内容与首页粘贴框
     placeholder 展示的示例**逐字一致**（`study,ai,bi,ci,di` / Study A / Study B），两处需同步修改。
  2. `adapters/fullflow.py`：`run_fastpath()` 新增 `demo: bool = False`；为真时把 A 块
     stage_result 的说明改为「内置示例数据（演示），跳至 Block B 分析」，便于事后区分演示与真实数据。
  3. `workbench/server.py`（`/api/start_data`）：raw_csv 分支在既无 `raw_text` 也无数据文件时
     改用 `demo_raw_rows()` 并传 `demo=True`，不再返回 400。
  4. `workbench.html`：`doStartData("raw_csv")` 未提供数据时不再拦截（提示「将用示例数据演示」
     并继续提交）；数据准备区新增醒目说明「🟡 **演示模式**：既未上传文件也未粘贴数据时，将用
     上方示例（Study A / Study B）继续流程，跑通『合并计算 → GRADE → 质量门』以便先看效果」。
  **验证**：`py_compile` + 内联 JS `node --check` 通过；`demo_raw_rows()` 解析出 2 行。
  **本地与线上端到端实测均 PASS**：`POST /api/start_data`（`raw_csv`、不带任何数据）→ HTTP 200、
  A 块 note =「内置示例数据（演示）」、进度 `A4 → B1.meta_analysis → B2.grade → B3.overclaim →
  B4.quality_gate` 并停在 B4 质量门（`kind=gate`）—— 即示例数据**完整跑通了 Block B（合并计算
  与 GRADE）**，这同时实证了 B 部分 R 引擎在当前部署下可用。首页演示提示渲染正确、0 JS 错误。

- **A3 成果导出：PDF 打包下载 + Excel 确认清单（2026-09-17 用户要求）**：
  用户反馈「下载完却没有任何 PDF 与确认文档的出口」。现补齐成果出口（批准 / 确认后即可取走）：
  1. **后端**（`adapters/block_a.py`）：新增 `_a3_result_of()`（取 A3 结果，兼容旧会话把下载结果
     挂在 A4 的历史落点）、`_downloadable_docs()`（过滤 skip、校正已失效的 PDF 路径）、
     `_safe_filename()`、`export_a3_download_list_xlsx()`（openpyxl 生成确认清单，列为 序号 /
     标题 / DOI / 年 / 刊名 / 状态 / PDF 文件名 / 说明；表头写作「#（篇目序号）」以解释
     因排除篇目导致的跳号）、`a3_pdf_zip()`（按 `NN_标题.pdf` 归档、同名自动加序号，
     并附「下载清单.csv」，带 BOM 便于 Excel 直开）。
  2. **接口**（`server.py`）：`GET /api/a3_export_list`（xlsx）、`GET /api/a3_download_pdfs`
     （zip，文件名含篇数）；无数据时返回 400 + 明确中文提示。
  3. **前端**（`workbench.html`）：A3 节点新增「⬇ 成果导出」面板（显示「已下载 N / M 篇」+
     两个下载入口）；**并修掉完成页的误导文案** —— A3 下载完成即终点时原先仍显示
     「流程已完成（Block C 终闸已放行）· 稿件经 C1→C3→C4 全部通过」（实际并未跑 C），
     现按 `await.prompt` 区分两种完成态：下载路径改为「PDF 全文下载已完成 —— 流程到此结束」
     + 同一套成果导出 + 通往 B 的指引；Block C 路径保留原提示。
  **验证**：`py_compile` + 内联 JS `node --check` 通过。端点实测（构造 2 个真 PDF 文件）：
  xlsx 5666 字节、表头与状态/说明列正确、5 行（skip 已剔除）；zip 含 2 个 PDF + 清单 csv。
  前端真渲染 **9/9**：A3 导出面板与两条下载链接在位、保留跳 B 面板、完成页不再误报 Block C
  且含两个下载入口、0 JS 错误。线上：首页 5 个标记命中、两个端点均返回 400 + 明确提示。

- **A2「未完整翻译 → 请自行翻译为英文检索词」的醒目提示（2026-09-17，用户要求）**：
  背景：翻译模块在沙箱内不可用时，上一轮已改为如实标 `fully_translated=false`，但页面只有一行
  `false`、没有可操作指引，用户看到后不知道下一步该做什么。本次补齐「提示 + 出口」：
  1. `adapters/workbench/form_schema.py`：A2 新增条件面板
     `{kind:"notice", level:"warn", when:{path:"nha.coverage.fully_translated", equals:false}}`
     —— 标题「⚠️ 检索式未完整翻译为英文 —— 请自行填写英文检索词后重跑」，正文点明
     「中文检索词直接送 OpenAlex / Europe PMC 会明显漏检」并给出示例
     （`SGLT2 inhibitors chronic kidney disease`）+ 明确指出操作位置。
  2. 同文件：`fully_translated` 字段加 `alert_if_not: true`（为 false 时标红）；「未翻译残留」
     字段改名「需自行翻译为英文的片段（非空 = 境外库会漏检）」；「优化翻译后检索式」textarea
     增加 `hint` 操作指引。
  3. `adapters/workbench/workbench.html`：`renderPanel` 新增 `kind:"notice"` 分支（支持 `when`
     条件渲染，不成立时整块不输出）+ `.notice.warn/.info` 样式；`hint` 支持范围从 rowlist 扩展到
     textarea。
  4. `adapters/block_a.py`：`translation_hits`（模块不可用 / 翻译后仍残留 两条路径）与 A2
     `prompt` 文案统一改为明确指令「请自行翻译为英文检索词，填入『优化翻译后检索式』后重跑」。
  **验证**：`py_compile` + 内联 JS `node --check` 通过；构造 `fully_translated=false/true` 两个
  会话做**真渲染对比**：false 用例出现红色提示块（含「请自行填写英文检索词」）、字段标红、
  textarea 指引齐备；true 用例提示块与标红**均不出现**（条件渲染生效）；两例均 0 JS 错误。
  载荷版（发布对象）复测 9/9 断言全过；线上 `/api/session` 实时返回 `panels[0].kind=notice`，
  前端 4 个源码标记全部命中，无头 Chromium 0 JS 错误、后端 pill「就绪」。

### Changed

- **质量门内容可解释化 + 删除 B→C 的「通用确认节点」（2026-09-17 用户要求）**：
  用户反馈「质量门：GRADE + 过度声明这一步显示的内容最好加以解释；之后的通用确认节点没有必要，
  直接进入 C 即可」。
  1. **质量门可解释化**：
     · `block_b.b4_quality_gate()` 的 report 增补**顶层标量**明细 —— `grade_downgrades`（累计
       降级档数）、`grade_reasons_text`（降级理由，分号连接）、五个维度各自的评级
       （`domain_risk_of_bias` / `domain_inconsistency` / `domain_indirectness` /
       `domain_imprecision` / `domain_publication_bias`）、`overclaim_hits`。全部展开为顶层字段，
       前端 object 面板直接可读，不依赖嵌套 path 支持。
     · `form_schema` 的 B4 重写：intro 改为**逐条解释**（最终放行闸 / GRADE 五维度降级逻辑 /
       过度声明检测 / critical 判定规则）；面板由「一坨 JSON」拆为 6 块 —— GRADE 证据质量、
       GRADE 五个维度评级、过度声明检测、闸门判定、过度声明明细、完整报告（仍可编辑兜底）。
       ⚠️ intro 按**纯文本**渲染（前端不解析 Markdown）→ 已去掉星号，并在文案里注明该约定。
  2. **B→C 直通**：`_advance()` 中当 **Block B 完成**时不再插入 `handoff_confirm`
     （其 `stage_id=None` → 前端显示「通用确认节点」），直接推进 Block C。
  **验证**：`py_compile` 通过；端到端（本地 + 线上各一轮）**ALL PASS**：
  演示启动 → `B1.meta_analysis (pause)` → 批准 → `B4.quality_gate (gate)`（report 含
  `grade=Low / 降级 1.5 档 / 理由=「样本研究少（k=2 → -1）；偏倚风险中等（→ -0.5）」/
  五维度 some·not serious·none·serious·none`）→ 批准 → **`C1.draft (pause)`**
  （提示「请人工审阅初稿结构与事实准确性」），全程无「通用确认节点」。
  前端真渲染 **10/10**：解释性引言齐备、6 个面板齐全、证据等级 / 降级理由 / 五维度 / critical
  均正确显示、0 JS 错误。
  **遗留**：其它节点的 `intro` 仍含 Markdown 星号（同样不会被渲染），待统一清理。

- **下载完成后不再插入「通用确认节点」，直接收尾或进 B（2026-09-17 用户反馈）**：
  用户反馈「下载 PDF 之后那个『通用确认节点 🟡 软停』没有意义了，应该直接跳到 B 节点」。
  根因：Block A 完成时 `_view()` 统一返回 `handoff_confirm`（其 `stage_id=None`），前端因无对应
  schema 而走通用兜底 → 渲染成「通用确认节点 🟡 软停」。在「检索 + 下载」这条链路上，它只是
  一次多余的确认点击。
  修改（`adapters/fullflow.py`）：`_advance()` 中当 **Block A 已完成且 `features.a4_extraction`
  关闭**时不再走 `handoff_confirm`：
  ① 若已有可算数据（A3「上传数据」接缝写入 `studies_for_b`）→ **直接递归推进 Block B**；
  ② 无可算数据 → 直接返回 done 视图（含「可在该节点取走成果 / 上传数据跳 B」的指引）。
  A4（数据提取）启用时行为不变，仍保留交接确认，不误伤原 B/C 流程。
  同时把 `_apply_a3_upload()` 从「仅 `letter=="B"` 时调用」改为**无条件先试**（无 A3 revision 时
  no-op）—— 否则用户点「上传并跳到 B」时 cursor 仍在 A 块，会出现「上传了数据却被判为无数据」。
  **验证**：`py_compile` 通过；三场景行为单测 **ALL PASS**：① A3 完成未上传 → `await.kind = done`
  （非 handoff_confirm）且 cursor 落 done；② A3 上传数据 → `studies_for_b` 接上且不再插入交接确认
  （直进 B）；③ 开启 `a4_extraction` → 仍保留交接确认。线上 smoke：health / features / session /
  index 均 200。

- **A3 恢复为独立节点（PDF 下载）；A4 数据提取转为隐藏备用；B/C 开放首页与 A3 直达（2026-09-17 用户裁定）**：
  承接上一轮「只提供检索 + PDF 下载」，本轮按用户要求改结构：**A3 真正独立成阶段**（不再是 A4 的
  展示别名），A4 退为隐藏备用，B/C 从「保留但不可达」改为**多入口可达**。
  1. **阶段拆分**（`adapters/block_a.py`）：新增 `A3 = "A3.pdf_download"` 与独立阶段函数
     `a3_pdf_download()`（复用 `a4_auto_fetch_and_extract`，只下载不抽取）；`BLOCK_A_SEQUENCE`
     变为 `[A1, A2, A3, A4]`。原 `A3` 常量更名 `A3_LEGACY = "A3.screening"` 并同步 3 处旧会话
     兼容引用（导出裁决表 / `_a3_legacy_guard` / Excel 回写）。`run_block_a`：A2 软停后插入 A3
     软停段（**置于 `a4_only` 之外** —— 复用缓存时同样要执行下载；已批准则跳过，避免重下）；
     A4 段整体以 `features.a4_extraction_enabled()` 包裹。
  2. **编排与推进**（`adapters/fullflow.py`）：`DEFAULT_PAUSE_AT` 增 `A3.pdf_download`；
     `EDITABLE_KEYS` 增 `A3.pdf_download: [pdf_dir, extracted_rows]`；`start_stage` 续跑条件改为
     `∈ {A3, A4}`；新增 `_apply_a3_upload()`（把人工上传的 `extracted_rows` 接成 `studies_for_b`，
     **刻意排在「无数据则终止」判断之前**）；`_view` 的 A 块数据收集扩展到 A3 与 revision 接缝。
  3. **schema 与开关**（`form_schema.py` / `features.py`）：`STAGE_ORDER` 改为动态构造（A3 恒在、
     A4 仅开关打开时出现）；`SCHEMA` 增 `"A3.pdf_download"`（下载版）、`"A4.data_extraction"`
     恢复提取版；`schema_for()` 增旧会话兼容（A4 关闭期间，历史停在 A4 的会话按下载版渲染）。
     开关变为 `fastpath_raw_csv=True`、新增 `fastpath_draft=True`（`fastpath_pdf` 仍 False）。
  4. **接口与前端**：新增 `POST /api/a3_jump_to_b`（解析上传/粘贴的 CSV/Excel → 写 revision →
     推进 Block B）；`workbench.html` 时间轴按开关构造、A3 节点新增「上传数据 → 跳到 B」面板
     （`a3JumpToB`）、决策按钮改「✓ 完成下载」、首页新增「自备 B 信封 JSON → 直达 C」入口与
     `draft-only` 上传区（`doStartData("draft")`）。
  **验证**：`py_compile` + 内联 JS `node --check` 通过。真渲染（本地 A3 态用例）**10/10**：
  首页 3 条通道、A3 标题「PDF 全文下载 🟡 软停」、下载清单 4 卡、跳 B 面板在位、按钮
  「✓ 完成下载」、时间轴含 PDF 下载且无「数据提取」、0 JS 错误。接缝单测：`parse_raw_csv`
  解析 2 行 → `_apply_a3_upload` 接上 `studies_for_b`（2 行）且终止条件不再命中；未上传时仍按
  「下载完成即终点」终止 —— ALL PASS。线上：`/health` 200、`/api/features` 四键正确、
  首页 7 个源码标记命中且旧 A4 标签已移除、时间轴「选题 / 检索 / PDF 下载 / 合并计算 …」、
  0 JS 错误。

- **网页功能调整：只提供「A2 检索 + PDF 下载」，A4 数据提取暂时隐藏（2026-09-17 用户裁定）**：
  新增集中功能开关 `adapters/features.py`（单一真源，前后端共用；支持环境变量临时覆盖；
  **隐藏 ≠ 删除** —— 相关代码全部保留，改回 True 即恢复）：
  `a4_extraction=False` / `fastpath_pdf=False` / `fastpath_raw_csv=False`。
  1. **A4 节点降级**（`form_schema.py`）：A4 由「数据提取核验（🔴 红线）」变为「PDF 全文下载」
     （`gate_type` redline→soft），面板换成「下载概览 + 逐篇下载清单」（新 kind `a4downloads`）；
     原 schema 原样保留为 `_A4_EXTRACTION_SCHEMA`，开关打开即自动切回。
  2. **不再抽取**（`block_a.py`）：`_a4_extract_pdf` 在开关关闭时直接走既有「未抽取」降级路径 ——
     PDF 照常落盘，`extracted_rows` 恒空；`a4_stream` 结果新增 `n_failed` / `n_needs_upload` 计数
     供「下载概览」直接展示。
  3. **流程终点**（`fullflow.py`）：A4 批准后若确无可算数据（无 `studies_for_b`）→ 置 done、
     不进 Block B（B/C 节点定义保留）；`run_fastpath` 对两条快速通道在接口层直接拒绝，
     避免绕过 UI 生成「走了半截又无法继续」的会话。
  4. **前端**（`workbench.html`）：启动时经 `GET /api/features`（新端点）取开关；开始页只剩
     「标准全流程（检索 → 初筛 → PDF 下载）」；时间轴去掉已并入 A2 的旧 A3 条目、A4 标签改
     「PDF 下载」；新增 `renderA4Downloads()`（只呈现下载状态，无抽取行 / 原文对照 / 剔除 /
     上传 / 批量匹配）；A4 决策按钮改「✓ 完成下载」并走普通 decide；A4 实时预览面板按开关隐藏
     （原渲染函数保留未删）。
  **验证**：`py_compile` + 内联 JS `node --check` 通过。真渲染（本地构造 A4 下载态会话）：
  开始页 1 个选项、A4 标题「PDF 全文下载 🟡 软停」、下载清单 4 卡（5 条 per_doc 去掉 1 条 skip）、
  状态 pill 正确、**无任何提取 UI**、按钮「✓ 完成下载」、时间轴含「PDF 下载」、0 JS 错误
  —— 10/10 断言通过。行为单测：无提取数据 → 终止于 done（含提示文案）；有自备数据 → 不拦截；
  开启开关 → 恢复提取语义；两条快速通道接口拒绝 —— 全 PASS。线上回归：`/health` 200、
  `/api/features` 三项 false、首页 7 个源码标记命中且旧 A3 已移除、线上会话时间轴显示
  「选题 / 检索 / PDF 下载 / 合并计算 …」、0 JS 错误。

- **飞书版本字段落点统一：一律写 `resultstr`，`querystr` 不再存版本信息（2026-09-17，对齐 ct-base `coze_io_contract.md` §2.1/§2.2）**：
  此前本技能把 `skill_version` 写进 `querystr`（客户端入参侧），与 ct-advisor 的落点不一致、无法统一检索。
  coze 端改动（**需重新上传部署包才生效**）：
  1. `src/graphs/nodes/feishu_write_node.py`：`build_querystr()` **移除** `skill_version` 参数
     （querystr 只留 `task`/`data`/`params`/`figure`）；`build_resultstr()` 新增可选参数
     `runtime_sec` / `skill_version` / `coze_version`，仅非空时并入 result dict **顶层**
     （为空 → 不写键，与历史格式逐字节一致）。
  2. 新增 `src/graphs/nodes/_version.py::COZE_VERSION`（单一真源，现 `5.3.9`）：飞书
     `coze_version` 列与响应信封标记 `_coze_version` 共用，杜绝两处漂移。
  3. `src/graphs/nodes/feishu_save_node.py`：按 `state.received_at` 计算 `runtime_sec`
     （`round(t,3)`，缺失则不写），并把 `skill_version` + `coze_version` 一并写入 resultstr。
  4. `src/graphs/state.py`：`GlobalState`/`GraphInput`/`FeishuSaveNodeInput` 新增可选
     `received_at` 字段（秒级 float），`skill_version` 描述改指 `resultstr`。
  5. `src/main.py`：`/run` / `/async_run` / `/stream_run` 入口在 `request.json()` 后即刻注入
     `payload["received_at"] = time.time()`（§2.2 取值起点；只进飞书、不出参）。
  6. `src/graphs/nodes/meta_analysis.py`：`_COZE_ENVELOPE_VERSION` 改为引用 `_version.COZE_VERSION`。
  7. 契约同步：`adapters/coze/coze_contract.md`（§2 契约合规字段 + 飞书写入段落新增「版本字段落点」表）。
  **验收**：`py_compile` 五个文件通过；`build_querystr` 输出断言无版本键、`build_resultstr`
  全空元信息与历史格式逐字节一致、全字段时 `runtime_sec=1.235`/`skill_version`/`coze_version` 均在顶层。

### Fixed

- **C1 初稿节点「看不到论文初稿」（2026-09-17 用户反馈）**：
  根因：`form_schema` 的 `C1.draft` 只有一个面板读 `editable.sections`（**章节名列表**），
  而真正存放正文的 `editable.manuscript` **从未被展示** —— 后端一直在产出它
  （`block_c.c1_draft()` 返回 `{manuscript, sections, char_count}`，`EDITABLE_KEYS["C1.draft"]`
  也含 `manuscript`），只是前端没读，所以用户只看到一串章节名。
  修复：C1 面板改为 ——「**论文初稿正文（可直接编辑）**」用 `kind: "textarea"`
  绑定 `editable.manuscript`（`revision_key: "manuscript"`，改动随「批准 / 放行」作为 revision
  提交，可直接在框内补写讨论与结论）；原「章节清单」降为辅助面板（`kind: "json"`，供 C3
  结构核验对照）；intro 补说明（摘要 / 背景 / 方法 / 结果已填真实数字，讨论与结论为待撰写占位）。
  **验证**：`py_compile` 通过。本地 + 线上各跑一轮完整链路（演示 → B1 → 批准 → B4 → 批准 → C1）
  并渲染，**各 7/7**：标题「初稿撰写」、出现「论文初稿正文（可直接编辑）」面板、textarea
  **771 字符**且含真实统计数字（`OR = 0.57 (95% CI -0.05–1.19, p = 0.074); I² = 38%;
  τ² = 0.08; GRADE = Low`）、章节清单 `["摘要","1. 背景","2. 方法","3. 结果","4. 讨论","5. 结论","参考文献"]`、
  按钮含「批准 / 放行」、0 JS 错误。

- **进 B 停在「合并计算」而非直冲质量门 +「质量报告 null」（2026-09-17 用户反馈，两处修复）**：
  用户反馈「现在选择 B 以后不是跳到合并计算，而是后面的质量门，这个不对；B4 质量门的产出也修一下」。
  1. **B1 成为停靠点**：`DEFAULT_PAUSE_AT` 增 `"B1.meta_analysis"` —— 进 B 后先停在**合并结果**
     让人核对（B2 GRADE / B3 过度声明仍为自动分析，不停）；`block_b` 为 B1 补上 `nha.prompt`
     （此前为 `None` → 停靠时提示语为空）。同时 `form_schema` 注册 `"B1.meta_analysis"` 别名
     （历史键名写作 `"B1.meta"`，而前端按 stage_id 取 schema → 两个 id 复用同一份定义，
     避免漂移），前端时间轴 id 同步为 `B1.meta_analysis`（此前与后端不一致）。
  2. **修「质量报告 null」**：根因是 `b4_quality_gate()` 返回**平铺** dict
     （`grade` / `n_overclaim` / …），而前端 B4 面板读 `editable.report`
     （`EDITABLE_KEYS["B4.quality_gate"]=["report"]`，`_view` 从 stage_result 同名键取）→ 取不到。
     修复：`_mk_stage(B4, 3, "await_human", {**b4_rep, "report": dict(b4_rep)}, nha4)`
     —— 同时提供平铺键与嵌套 `report`，两种读法都兼容。
  **验证**：`py_compile` 通过；端到端（本地 + 线上各一轮）**ALL PASS**：
  · 演示启动 → `await = B1.meta_analysis (pause)`，提示语完整，`pairwise` 含
    `k=2, OR, TE=0.569, CI=[-0.0549, 1.1929], I²=0.378, τ²=0.0766, Q=1.6078`；
  · 批准 B1 → `await = B4.quality_gate (gate)`，`stage_result.report` 与 `editable_payload.report`
    均为完整 dict（`grade=Low / n_overclaim=0 / critical=false`）。
  前端真渲染 **9/9**：B1 展示合并效应量 / 95% CI / I² / τ²、按钮含「批准 / 放行」、
  时间轴「合并计算 ⏸ 待确认」；B4 质量报告显示完整 JSON（**不再 null**）并显示 GRADE 分级、
  0 JS 错误。
  **遗留（纯显示细节，未定位来源）**：B4 节点标题后缀仍显示「🟡 软停」，而它实际是 🔴 红线闸。

- **B1 合并计算的 `data` 格式错误 —— 出站校验拦截，合并计算从未真正发出（2026-09-17 排查发现）**：
  在验证「演示模式」端到端时发现 `B1.pairwise` 恒为
  `{"k": 0, "error": "coze_error: 出站信封校验未通过：[E03_DATA_NOT_OBJECT] data 必须是对象
  （{rows:[...]}），当前为 list"}` —— 即 `block_b._build_b1_coze_env()` 把 `data` 直接传了裸 list，
  被出站契约校验拦下，**R 引擎从未收到数据、合并计算静默落空**（B 块容错继续推进，表面看流程
  照常走到 B4，故长期未被发现）。
  修复：`"data": {"rows": _norm_b1_rows(studies)}`。
  **验证**（本地 + 线上各跑一次 `raw_csv` 演示）：
  · **SMD**（连续）：`k=2, engine=coze, TE=0.1326, se=0.5930, CI=[-1.0298, 1.2949], p=0.8231,
    tau²=0.663, I²=0.9425, Q=17.3889`；
  · **HR**（生存）：`k=2, TE=-0.2664（≈ HR 0.766）, se=0.0751, CI=[-0.4136, -0.1192], p=0.0004`；
  · B2 GRADE 随之产出：`grade=Low, downgrades=1.5, reasons=["样本研究少（k=2 → -1）",
    "偏倚风险中等（→ -0.5）"]`。

- **【已解决】B4 质量门页面「质量报告 null」**（2026-09-17 发现 → 同日修复，保留排查记录）：
  线上演示会话停在 `B4.quality_gate` 时，质量报告面板渲染为 `null`。当时已确认 `form_schema` 的
  B4 面板读 `editable.report`（由 `_view()` 从停靠阶段 `stage_result` 同名键取），而
  `block_b.b4_quality_gate()` 确实产出 `report` 字典 —— 根因即二者**层级不匹配**（后端平铺
  返回 `grade`/`n_overclaim`/…，前端读嵌套 `editable.report`）。
  **修复见上方「进 B 停在『合并计算』而非直冲质量门 +『质量报告 null』」条目**
  （`_mk_stage(B4, …)` 处同时提供平铺键与嵌套 `report`）。

- **裁决表「剔除」与「低置信」配色区分（2026-09-17 用户反馈：建议剔除用红）**：
  用户反馈两者颜色应不同。根因有两层：
  ① **底色本身太接近** —— 原用全局 `--wb-warn-bg:#fffbeb`（浅黄）与 `--wb-err-bg:#fef2f2`（浅红），
     都是近白色，浅色主题下几乎无法分辨；
  ② **三态底色实际根本没生效** —— 通用斑马纹 `table.grid tbody tr:nth-child(even)`（特异性 0-2-2）
     高于 `.rl-row.dec-*`（0-2-0），把所有裁决行统一刷成了 `--wb-row-alt`（#f6f9fd），即「三行同色」。
  修复（`workbench.html`）：① 为裁决表另立专用变量 `--wb-dec-{include,exclude,uncertain}-bg`
  （浅色 `#e8f8ef` / `#fdd8d8` / `#fdf0c9`，暗色主题同步一套），不复用被各类提示块共享的全局底色；
  ② 选择器提升为 `table.rl tbody tr.rl-row.dec-*`（0-3-3）压过斑马纹；
  ③ 三态行各加 3px 左侧色条（绿 / 红 / 琥珀）—— 色条是最可靠的区分手段，不受底色明暗影响；
  ④ 裁决下拉框 `.rl-sel-*` 底色同步改用专用色。
  **验证**：本地真渲染 **9/9**：三态行底色分别为 `rgb(232,248,239)` / `rgb(253,216,216)` /
  `rgb(253,240,201)`（互不相同）、左侧色条红/琥珀正确、下拉框三色区分、三态标签齐全、0 JS 错误。
  线上 **6/6**：CSS 变量与带作用域规则均已上线，真实 A2 会话的 include（7 行）与 uncertain（9 行）
  底色确实不同。

- **下载进度面板文案去除全部「抽取」表述（2026-09-17 用户反馈）**：
  A2 批准后进入下载期间显示的实时进度面板仍沿用旧文案「📥 A4 数据提取进度（逐篇下载 / 抽取）」
  +「正在按篇并行下载全文 PDF 并抽取 2×2 表…」——属 A3 拆分时的遗漏。现按开关分两套：
  数据提取关闭时，标题改「📥 PDF 全文下载进度」、说明只讲下载；状态徽标由
  「✓ 已抽取 / 🔬 抽取中 / ⚠ 已下·待补抽 / ✕ 需上传」改为「✓ 已下载 / ⬇ 下载中 / ✕ 未获取到」；
  末尾指引由「回到 A4 节点点『批准 / 放行』继续」改为「回到『PDF 下载』节点点『完成下载』
  结束流程（或上传数据跳到 B）」。**保留**「上传已有 PDF 补传」入口 —— 它服务于下载环节
  （付费墙 / 抓取失败时人工补齐），不属数据提取。
  顺带修掉启动提示里的过期阶段名（`server.py` 的 `stage_hint`）：
  「A3 初筛 → A4 数据提取」→ 按开关显示「A3 PDF 下载[ → A4 数据提取]」。
  **验证**：`py_compile` + 内联 JS `node --check` 通过；本地与线上真渲染各 **8/8**：
  面板标题 / 说明 / 徽标 / 末尾指引全部为下载语义、文本中**「抽取」「2×2」零出现**、
  补传入口保留、0 JS 错误。

- **首页「自备全文 PDF → 跳到 A4」入口彻底移除 + 根路径禁缓存（2026-09-17 用户反馈）**：
  用户反馈该选项仍可见，但实测线上首页渲染结果已是 3 条通道（标准 / 自备原始数据 / 自备 B
  信封）、无 pdf 入口 —— 判定为**浏览器或中间层复用了旧 HTML**（根路由此前未设任何缓存头），
  用户看到的是发布前的页面。两处修掉根因：
  1. `workbench.html`：pdf-only 区块由「静态 HTML + `display:none`」改为**条件渲染**
     （`${FEATURES.fastpath_pdf ? … : ""}`）—— 关闭时连 DOM 都不生成，消除「隐藏但存在」的
     歧义（此前查看源码仍能搜到「跳到 A4」文案）；同时把该区块内的过期描述
     （原写「停在 A4 数据提取红线」，而 A4 已转为隐藏备用）改为中性表述。
  2. `server.py` 根路由：响应加 `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
     与 `Pragma` / `Expires` —— 界面随功能开关（features）变化，旧 HTML 会让用户看到已下线入口
     且极难自查是缓存问题。
  **验证**：`py_compile` + 内联 JS `node --check` 通过。本地与线上真渲染各 **7/7**：仅 3 条通道、
  `pdf-only` 区块与 `data_pdfs` 输入**均不存在于 DOM**、可见文本无「A4 / 全文 PDF」、
  响应头 `no-store` 生效、0 JS 错误。

- **A2「检索状态」误报 error + 沙箱内检索式静默不翻译（2026-09-17，线上会话复现）**：
  现象：A2 检索概览显示 `检索状态 = error`（红字告警），但合并总数 16、核心二源其实都有数据。
  线上会话明文：`by_source={'openalex':13,'europepmc':3}`、`core_missing=['OpenAlex','EuropePMC']`、
  `cli_status='error'`、`translated_query` 是**中文原文**却 `fully_translated=true`。两个独立缺陷：
  1. **来源名大小写失配**（`adapters/block_a.py`）：coze 统一端返回的 `studies.source` 是小写
     raw key（`openalex`/`europepmc`），而 `CORE_SOURCES=("OpenAlex","EuropePMC")` 逐字符串比对
     → 核心二源被判「全部缺位」→ 降级 error（本地走 `fetch_*` 返回规范名，故从未暴露）。
     新增 `_canon_source()` 归一（忽略大小写/空格/连字符/下划线），并保留 `by_source_raw` 审计留痕。
  2. **翻译模块在沙箱内不可用 + 谎报完整翻译**：`_CT_BASE_SCRIPTS` 硬编码本机技能树路径
     `~/.workbuddy/skills/ct-base/scripts`，发布载荷沙箱中不存在 → `import kw_localize` 必失败 →
     中文检索式原样送国际库（命中偏少），且 `fully_translated` 仍返回初始值 `True`，把漏检伪装成正常。
     新增 `_kw_localize_scripts_dir()`（ct-base 权威 → ct-literature 同源副本 → 载荷
     `bundled/ct-literature/scripts` 逐级回落）与 `_bundled_skill_dir()`；`_ct_scripts_dir()`
     同样加 bundled 兜底（`doc_type_filter` 文献类型预填 / `export_xlsx` 合并表导出一并受益）。
     模块不可用时，原文含中文则如实标 `fully_translated=False` + `untranslated`。
  **验证**：① 复现线上数据 → `search_status` error→`ok`、`core_missing` 2 项→`[]`；边界回归：
  真缺源仍报 partial/error（闸门未修坏）、未知来源不被吞。② 沙箱等价（技能树不可用 + 载荷布局）
  → 回落 `publish/bundled/ct-literature/scripts`，中文主题真翻译成功、term_map 离线命中
  （`非小细胞肺癌 → non-small cell lung cancer (NSCLC)`）。③ 载荷冒烟 `/health` 200；
  线上 `/health` 200 + 无头 Chromium 渲染 0 JS 错误、后端 pill「就绪」。
  ⚠️ 旧会话的 coverage 已持久化（`build_state` 只回读、不重算）→ **需在本节点重跑检索**才会看到 ok。

- **`build_publish.py` 两处加固（2026-09-17）**：
  1. `adapters/workbench/app.config.json` 纳入 `WHITELIST_FILES`——此前不在白名单（22 项里没有），
     发布后载荷内 `deployedAt` 永远滞后于源、只能手工复制（本次实测：源已改，构建仍 `copied=0`）。
  2. 复制跳过条件由「size 相同 + 源 mtime 不新于目标」改为**内容比对**（`read_bytes()`）：
     同长度变更（改一个数字 / 时间戳 / 同长度词）会被旧逻辑静默漏同步。
  **验证**：`py_compile` 通过；run1 `copied=1 skipped=22`、run2 `copied=0 skipped=23`（幂等）；
  载荷 204 文件、清理 0 项、保护闸 0、自检全过。

- **工作台 A2「文献集」节点一进入即崩、并被误报为「无法连接后端」（2026-09-17，线上回归）**：
  现象：A1 批准后推进到 A2.literature_search 立刻报
  `✕ 无法连接后端（Cannot read properties of undefined (reading 'length')）`，而 `/health` 200、
  coze 端在线 —— 后端其实是好的，误导性文案把排查方向带偏。两层根因：
  1. `adapters/workbench/form_schema.py`：A2 的「逐条裁决」rowlist **缺 `columns`**
     （2026-09-10 A2+A3 合并重写 schema 时漏掉；B3/C2 同类面板都有）。A2 是首个含表格的
     节点，故一进 A2 必崩。
  2. `adapters/workbench/workbench.html · renderRowlist`：`p.columns` 为 undefined 时仍取
     `cols.length` → 抛 TypeError；`streamPost` 的 `.catch` 把任何 TypeError 都当网络错误，
     渲染异常于是被显示成「无法连接后端」。
  修复：
  1. 后端补 6 列：标题(可展开) / 年 / 刊名 / 文献类型(下拉可编辑) / 裁决(下拉可编辑) / 理由；
     口径对齐导出裁决表（`col.decision`/`col.reason`/`col.doc_type_confirmed`），文献类型
     内部值沿用 `block_a.DOC_TYPE_ORDER`（original/review/guideline/protocol/unknown）。
  2. 前端 `renderRowlist` 加兜底：`columns` 缺失或非数组 → 回退「按数据自动出列」。
  3. 前端新增 `isNetError(e)`：仅真正的网络层失败才提示「无法连接后端」，其余异常原样显示
     「处理响应失败：<msg>」，避免根因被文案掩盖。
  **验收**：`/api/session` 契约（rowlist.columns=6、decisions=6 行）；无头 Chromium 真渲染
  pageerror=0、表头 6 列、6 数据行 + 12 个可编辑下拉、无「无法连接后端」文案；源与载荷
  双份 MD5 一致（form_schema `3ca878792312`、workbench `03229232890d`）。

- **`publish-kit/build_publish.py` 删除范围收敛为受控清理 + 保护闸；载荷一次性清掉 362 项历史垃圾（2026-09-17）**：
  背景：publish/ 里堆了 566 个文件，其中 343 个是**旧版递归误生成的嵌套副本**
  （`publish/adapters/workbench/publish/**`）+ 19 个 junk，每次构建都要全树扫删一遍
  （`--dry-run` 会删 362 项），风险随垃圾量放大；且旧版 SAFE-DELETE 用的是含 `runs/`、
  `output/`、`tests/`、`pdfs/` 这类**路径片段**的宽正则、又无保护清单，随时可能误伤合法
  文件（09-16 已发生过一次删掉 190+ 合法文件的事故）。
  改动：
  1. 载荷清理：删除 343 嵌套副本 + 19 junk，载荷 566 → **204 文件（10.0 MB）**；删除前
     整包备份（`backups/meta-workbench-publish-preclean-*.zip`，30.4 MB），并以 md5 基线
     闭环校验「消失项恰好等于应删集合、多删 0 / 漏删 0 / 204 项逐字节一致」。
  2. `build_publish.py` 三级受控清理：**目录级**只删点名目录（`NESTED_JUNK_DIRS` —— 嵌套
     副本与误拷入的 `runs/`，删前校验目录内无保护文件）；**文件级**只认明确垃圾形态
     （`__pycache__`、`*.pyc/*.pyo`、`*.log`、`*.bak*`、`*.ctbase_bak_*`、`*.dat`、
     `dist/coze_deploy_bundle*`），**取消路径片段宽正则**；**保护闸**（`PROTECTED_FILES` =
     白名单源 + `main.py`/`app.config.json`）一律拒删，命中即告警（正常应为 0）。
  3. 新增构建后自检（fail loud）：`main.py` / `requirements.txt` / workbench 三件套缺失即
     报错退出，杜绝「构建成功但载荷已残」的静默故障。
  **验收**：新脚本 `--dry-run` 与连续两次正式构建均 **清理 0 项、保护闸 0、载荷 204 文件
  且内容零变化**（幂等）；清理后的载荷起真实服务通过 `/health` + `/api/session`
  （A2 rowlist.columns=6）+ 根路径 HTML 117,790 字符。

- **ctsearch_client.search_literature 增加请求级去重闸门（2026-09-16，飞书 searchlog 复盘）**：
  后台 searchlog（CTDB_searchlog (4).xlsx）显示 2026-09-15 选题门控「简单分析」路径出现
  「同参重复 coze 调用」burst——2 个不同查询（PD-1 × openalex/europepmc）各被原样重发
  4 轮、间隔约 2 分钟，coze 每次都真跑检索并落库。根因：调用方把偶发失败/解析空
  （`_parse_coze_stream` 失败返 `[]` 被误当「检索无结果」）判成没查到 → 同参重试 →
  重复出站。修复（对齐 coze_client._DEDUP_CACHE 已验证模式）：
  1. `search_literature` 出站前加去重闸门：键 = source+keyword+year_from+year_to+max_results；
     窗口默认 300s（env `CT_SEARCH_DEDUP_WINDOW`，≤0 关闭）；命中直接回放缓存（`from_cache:True`）。
  2. 缓存**跨进程生效**（内存 dict + 临时目录文件双写，env `CT_SEARCH_DEDUP_DIR` 覆盖）——
     发布沙箱每次 CLI 是独立进程，纯内存拦不住。
  3. 只缓存成功（works 非空且无 error）——偶发失败不入，避免毒化窗口内真实重试。
  4. 流式空结果不再被当作成功：`projects==[]` 视为失败继续走 /run 回退，杜绝
     「解析失败伪装成检索为 0 → 上层误判重试」。
  本机 3 项验收通过：同参二次调用 from_cache=True；换 max_results=6 不串味；跨进程命中磁盘缓存。
  技能与已发布应用（meta.app.workbuddy.link）两份代码同步（MD5 一致）。

- **pdf_extractor v0.4.1：基于 78 篇真实 PDF 实证改进数据抓取能力（2026-09-14，用户指令「利用 pdf_cache 改进 PDF 信息识别和抓取」）**：
  对 `adapters/pdf_cache` 中 78 篇有效 PDF（排除 <5KB 的 stub/error 页）做批量 benchmark，发现并修复：

  **诊断发现**：
  1. **表格模板全面失效**：`T_DICHOT`=0、`T_CONT_TABLE`=0 命中。`_rebuild_borderless_table` 把正文段落拼成 2 列伪表（min_cols=2 太低，2 列布局的期刊正文被误识别为表格），99% 模板不匹配
  2. **综述类文献 43% 零行**：20 篇 review 中 16 篇 0 行——meta 论文用表格汇总证据，不在正文写 HR/OR 叙述句
  3. **1767 个页面 unresolved**：所有 tier 层都不命中

  **修复**：
  1. **`_rebuild_borderless_table` 伪表过滤**：min_cols 2→3（真实数据表几乎都 ≥3 列）；列间距阈值 20pt→12pt（避免 5 列表被压成 2 列）；新增数值行占比过滤（<50% 视为正文段落，不产出伪表）→ unresolved 从 1767 降至 548（-69%）
  2. **新增 `t_forest_table` 模板**（森林图/效应量汇总表）：识别 meta 论文最常见表格式（首列研究名 + 效应列含 (lo-hi) CI + 可选权重列），+142 行命中
  3. **新增 `t_meta_table` 模板**（纳入研究特征表）：识别 Table 1/2 格式（Study/Year/Design/n/Age），v0.4.1 硬化过滤参考文献/编号引用/期刊缩写/子组标签，+334 行命中
  4. **新增 `_narrative_pooled_effects` 叙述模板**（pooled/overall 句式）：覆盖 "The pooled OR was 1.25 (95% CI 1.08 to 1.45)" 等 meta 论文高频句式，+6 行
  5. **新增 `_narrative_subgroup_effects` 叙述模板**（subgroup 句式）：覆盖 "In the subgroup of patients with diabetes, the OR was 1.45..." 等

  **改进结果**：
  - 总抽取行数：1037 → 1260（+21%）
  - 有行文档：43 → 46
  - 零行文档：33 → 30
  - Unresolved 页面：1767 → 548（-69%）

  **已知局限**：
  - T_META_TABLE 仍有少量噪声（参考文献行、期刊缩写被误匹配），通过 v0.4.1 的过滤规则持续收窄
  - T_DICHOT 在真实 meta PDF 上仍为 0——meta 论文多用效应量表而非 2×2 计数表，这是预期行为
  - 扫描件（8 页）仍不支持，属 P2 范围

  **关键文件**：`adapters/pdf_extractor.py`（v0.4.1）、`adapters/tests/test_pdf_extractor.py`（已有测试用例保持通过）

- **系统自审修复：网络 Meta 研究数/对比数口径错误 + 一致性缺陷 6 项（2026-09-14，用户发起「系统检查相关流程与代码有无错误」后落地）**：
  对 CNMA 接入与 CINeMA 解读层做全链路审计（R 引擎 → 解读 → 质量 → 渲染 → 写作建议），逐项复核后修复：

  1. **【高】`stats.k` 在 arm-based 多臂研究下被高估**：`stats.k = nrow(prep)`，而 `prep` 是**对比级**数据——`.nma_prep` 会把三臂研究展开为 C(3,2)=3 行。实测「2 项研究（1 个三臂 + 1 个两臂）」→ `k = 4`，真实研究数 = 2；同一份产物里 `stats.k`(=4) 与 `extra.network.n_studies`(=2，取 `fit$k`) **自相矛盾**。
     - 影响链：报告结论写错研究数 → CINeMA「不精确性」域 `k < 3` 判据**漏报** → `k < 5` 警告数值错。
     - **Linde2016 实测：`k` 由 `124` 修正为 `93`**（124 是对比行数）——这也解释了此前「调研脚本报 93、引擎报 124」的困惑（此前误归因为"调研期做过研究级过滤"，实为本缺陷）。
     - 修复：新增 `.k_studies()` / `.k_comparisons()`（按 `studlab` / treat-pair 去重）；`nma` 与 `cnma` 的 `stats.k`、`extra.network.n_studies`、`n_comparisons` 及 `notes` 全改走去重口径。
  2. **【中】CNMA 的 `stats.heterogeneity` 缺 `Q`/`df`/`p`** —— 实只回 `tau`/`tau2`/`I2` 三字段，而 `coze_contract.md` §4 已声明网络 Meta 返回 6 字段 → 文档不实、加性模型的异质性检验丢失。补 `Q.additive` / `df.Q.additive` / `pval.Q.additive`（`df ≤ 0` 判 `null`）。
  3. **【中】CHANGELOG 字段路径笔误**：`stats.extra.components.additivity` → 实际为 `stats.extra.additivity`（与 `coze_contract.md` §4 一致）。
  4. **【中】CNMA 缺 `prop_direct`** → CINeMA「间接性」域对 CNMA 恒为 `unclear`，与 NMA 不对等。改从 `nc$x`（netcomb 保留的入参 netmeta 对象）取，`nma`/`nma_rank`/`cnma` 三个网络任务口径统一。
  5. **【低】`interpretation.py` 死变量** `n_cmp_tbl`（赋值后从未使用，且注释声称"唯一对比数见结论后半句"而代码并未使用）→ 删除并改正注释。
  6. **【中】`writing_advisor` 质量等级语义混用**：网络 Meta 改走 CINeMA 六域后 `grade` 值域变为 `major_concerns` 等，但 `grade_reported` 仍输出裸值。新增 `grade_framework` 参数 → 输出 `CINeMA: major_concerns` 形式；`_prisma_checklist` 补 `cnma` / `nma_rank` 条目（此前只有 `nma` 会追加一致性检验，且一律写 GRADE）；`_discussion_template` 不再对网络 Meta 套用"单一合并效应量"措辞。
  7. **【中】引擎指纹与技能版本撞号**：`.MA_ENGINE_VERSION = "2.11.0"` 与 CHANGELOG `## [2.11.0]`（2026-09-10 CCM 对话菜单）**同名异义** → 按指纹去 CHANGELOG 查部署记录会查到无关条目，误判线上生效。改为**与 `SKILL.md` 版本对齐**（`2.15.0`）；该字段**无程序化消费方**（全库 grep 确认，纯人读探针），改口径无破坏风险。

  - **回归覆盖缺口一并堵上**：原 18 例全是「1 研究 1 对比行」构造数据，缺陷逃过回归。新增 `caseF_multiarm_armbased` / `caseG_multiarm_cnma`（2 研究 / 含一个三臂），并把「`stats.k` == `extra.network.n_studies`」写成回归断言。回归 **20/20 通过**。
  - **文档同步**：`SKILL.md §5`（补唯一研究数/唯一对比数口径、`prop_direct` 三任务通用）、`coze_contract.md` §4（`n_comparisons`/`n_studies` 去重口径说明 + `prop_direct` 适用范围）。

### Removed

- **废弃 `adapters/coze/rendering.py` 死载荷（2026-09-14，用户「不需要的代码就废弃」指令）**：
  该文件随部署包发布（`_deploy/meta_analysis_coze_mirror_2026-09-08.zip` 与 `..._2026-09-09.zip` 均含），但**包内没有任何模块引用它**——证据：
  - AST 解析全包 **29 个 `.py`**，`import rendering` 命中 **0**（含 `src/main.py` 的 85 条 import、`graphs/nodes/meta_analysis.py` 的 28 条）；
  - 动态导入（`importlib` / `__import__` / 模块名字符串拼接）命中 **0**；
  - `scripts/pre_deploy_check.py` **无必需文件清单校验**（只校验 3 个 pyproject 依赖）；`scripts/pack.sh` 仅执行 `uv lock`；`docker/.dockerignore`、`pyproject.toml`、`.gitignore` 均未声明该文件。
  - **根因**：coze 云端服务只做流式转发、**不渲染 HTML**；报告渲染发生在**本机 agent 侧**（`adapters/rendering.py`，有 `render_case_report.py` / `run_analysis.py` / `run_real_meta.py` 三个真实消费方）。镜像副本自 **2026-08-31** 起未再跟进，与本地版已分叉：镜像 **38 KB / 852 行** vs 本地 **75 KB / 1509 行**，且缺「结果解读」「发表建议」「CINeMA」三张卡 —— 保留它既无功能价值，又会误导「改它可影响线上呈现」。
  - **处置**：文件已移出技能目录（可逆备份 → `_removed/coze_rendering.py.removed_20260914`，MD5 `508bf76e9d3a0b84706ae9131096cb6f`）；本地 `adapters/rendering.py` **保留不动**。
  - **移除后验证**：coze 包内 **29/29 `.py` 语法自检通过**、`import rendering` 命中仍为 **0**、本地渲染三消费方完好。

### Added

- **C 入口独立启动：`run_fastpath("draft")` + `/api/start_data?data_mode=draft`（2026-09-15，用户「ABC 三阶段各自可独立启动」裁定落地）**：
  补齐 A/B/C 独立启动架构的最后一环——从 C 起（自备 Block B 信封，跳过 A+B，停在 C1 软停闸）。
  - `adapters/fullflow.py`：`run_fastpath` 新增 `data_mode="draft"` 分支（`b_env` 必填校验，用户裁定 2026-09-15：C2/C3/C4 需 Block B 上下文）；A/B 块均标 done，cursor 指向 C，`_advance` 跑 Block C 停在 C1 软停。
  - `adapters/workbench/server.py`：`/api/start_data` 新增 `b_env_text` Form 参数 + `data_mode="draft"` 分支（两种录入：粘贴 JSON / 上传 `.json` 文件，复用 `json.loads` + `utf-8-sig` 解码）。
  - 菜单层零改动：flow_menu 对任意暂停节点渲染菜单，C1 软停在 `_fallback_options` 兜底下产出 `[批准/跳过/打回]`。
  - 验证：`_verify_draft_entry.py` 停在 `cursor={'block':'C','stage_id':'C1.draft','await_kind':'pause'}`，菜单正确；回归 `tests/test_flow_menu.py` 189 PASS / 0 FAIL。
  - 文档：`references/menu_logic_reference.md` §9 更新为已实现状态。

- **结果解读 / 质量评估层补齐网络 Meta（NMA / CNMA）覆盖：CINeMA 六域 + 修两处静默失效（2026-09-14，用户发起「结果解释分析是否覆盖 netmeta 结果」核查后落地）**：
  核查发现**三层对 netmeta 类结果全部失效，且均为静默失败**——用户拿到 NMA/CNMA 报告时「📊 结果解读」卡为空、「📋 质量评估」卡为空、报告顶部 hero 留白，而这三样正是 2026-09-13 新加的核心增值功能，此前**只对通用 pairwise 类任务生效**。
  - **根因不是漏加分支，而是数据形状不兼容**：`interpretation.py` 按标量写死 `pooled.get("estimate")`，而 netmeta 的 `pooled` 是**多对比向量**（`estimate: [-0.28, -0.543, ...]`）→ `float(list)` 抛 `TypeError` → 被上层 `except` 吞掉 → `est=None` → 所有依赖它的判定（结论 / 效应量极端 / CI 跨度）**静默跳过**。
  - **R 引擎** `adapters/coze/src/r_engine/run_task.R` 补网络诊断数据（缺失一律 `null`，**绝不填 0**）：
    - 新增辅助函数 `.cin_num1` / `.cin_het` / `.cin_incoh` / `.cin_network` / `.cin_incoh_cnma` / `.cin_network_cnma`；
    - `nma` / `nma_rank`：补 `stats.heterogeneity`（`tau`/`tau2`/`I2`/`Q`/`df`/`p`，**I² 由 netmeta 的 0–1 比例换算为百分数**，对齐 pairwise 契约）+ `stats.extra.inconsistency`（全局不一致性 `Q.inconsistency`/`pval.Q.inconsistency`，**netmeta 对象自带、无需额外调用** + `netsplit()` 逐对比「直接 vs 间接」差异表 + `Q_total`/`Q_heterogeneity`）+ `stats.extra.network`（干预数/对比数/研究数/设计数/直接证据占比）；
    - `cnma`：补 `stats.extra.inconsistency`（`netcomb` 无 `Q.inconsistency`，改用 **加性假设检验 `Q.additive`/`Q.standard`/`Q.diff` 作为成分模型层的不一致性判据**）+ `stats.extra.network`。
  - **`adapters/interpretation.py`** 新增 `_interpret_netmeta()`（`_NETMETA_TASKS = {nma, nma_rank, cnma}` 路由）：
    网络结构摘要、各对比/成分效应（`log` 尺度 → 比值尺度还原）、**不一致性**（`Q.inconsistency` + 逐对比）、**加性假设 `Q.diff`**、**不可识别成分**、传递性假设、SUCRA 缺位提示（未算排序时明示「若结论涉及『哪种干预更优』需补做 `nma_rank`」）。
  - **`adapters/quality_advice.py`**：
    - 新增 **`cinema_grade()` / `_evaluate_quality_cinema()`**，按 **CINeMA 六域**输出（研究内偏倚 / 报告偏倚 / 间接性 / 不精确性 / 异质性 / 不一致性），每域给出 `no_concerns` / `some_concerns` / `major_concerns` / `unclear` + 依据文字；`unclear` 明示「统计侧拿不到数据、须人工补」，**不猜**；netmeta 类走 CINeMA、pairwise 类维持原 GRADE（`framework` 字段标注）；
    - 修 `b2_grade` 的向量型 `ci` 比较崩溃（`list < float`）；修 `b4_quality_gate` **返回元组 `(report, nha)` 却被当 dict 使用**——该 `AttributeError` 由上层 `except` 吞掉，**质量评估引擎自上线起从未真正工作过**（含 pairwise）；
    - 缺 `pooled` 的 task（`diagnostic_meta` / `dose_resp` / `bayesian_pairwise`）补「评估不完整」透明度标注，避免仅凭研究数给出 `High` 的过度乐观评级。
  - **`adapters/rendering.py`**：`_render_hero` 对向量型 `pooled` 由「直接 `return ""`」改为渲染 `_render_hero_network()`（结构 + 可达估计数 + 显著性概况，跳过 CNMA 参考组自身的 `est=lo=hi=0` 占位项）→ 消除报告顶部留白；「📋 质量评估」卡支持 CINeMA 六域明细展开与中文评级文案（`_CINEMA_DOMAIN_CN` / `_CINEMA_RATING_CN`）。
  - **文档同步**：`coze_contract.md` §4 出参（`stats.heterogeneity` / `stats.extra.inconsistency` / `stats.extra.network` / `stats.extra.additivity`）；`SKILL.md §5` 能力边界表新增「Network diagnostics + CINeMA」条；`references/component_nma.md` 新增 §4.5「网络证据质量：CINeMA 六域」。`.MA_ENGINE_VERSION` 2.10.0 → **2.11.0**。（注：原写作 `stats.extra.components.additivity` 为笔误，实际字段路径是 `stats.extra.additivity`，与 `coze_contract.md` §4 一致——2026-09-14 自审修正。）
  - **回归验证（本地端到端，18/18 通过）**：`regress_all.py` 覆盖 18 个代表用例（含 `nma` case3 / `cnma` case47 / Linde2016 / `pairwise_meta` / `subgroup_analysis` / `metareg` / `diagnostic_meta` / `dose_resp` / `bayesian_pairwise` 等）；**非网络任务零回归**（修复前 3 例抛 `TypeError`，修复后全部正常且带"评估不完整"标注）。
    解读层实测：`nma` 由「`conclusion` 空 + 0 条 caveats」变为含网络结构/不一致性/逐对比差异的完整解读；`cnma` 含成分效应 + 加性假设 + 不可识别成分。
    **单位口径修正（实测发现）**：Linde2016 的 `I²` 原显示 `0`（实为 `0.1833` 比例未换算）→ 修正后 `18.3324`，`τ=0.149` 与 I² 不再自相矛盾。

- **新增 `cnma` 任务：成分网络 Meta（CNMA）（2026-09-14，ct-update P1 `meta-analysis::B` 落地）**：
  经调研确认 `netmeta` **原生**提供完整 CNMA 函数族（`netcomb` / `discomb` / `netcomplex` /
  `netcomparison` / `createC`），**无需引入任何新依赖**——2026-09-14 双端实测：本地与 coze
  容器均为 `netmeta 3.6.1`。此前「CNMA 未实现」的判断有误（其依据「netmeta 只做 arm-based
  NMA」不成立）。
  - `adapters/coze/src/r_engine/run_task.R` 新增 `cnma` 分支（数据契约复用 `.nma_prep`；
    治疗标签以 `sep_comps` 拼接成分，如 `A+B`）：
    - 连通网络走 `netcomb()`（加性成分模型）；`params.interaction=true` 时以 `createC(fit)`
      传入 `C.matrix` 拟合交互模型；
    - **断开网络**下 `netmeta()` 会直接拒绝（`Network consists of N separate sub-networks.`），
      自动改走 `discomb()`（断开网络 CNMA），并置 `cnma:disconnected_network` 告警；
    - 产出：成分效应 `stats.extra.components`、组合效应 `stats.pooled`、**加性假设检验**
      `stats.extra.additivity`（`Q_diff`/`df_diff`/`p_diff`/`additive`）、成分设计矩阵
      `stats.extra.design`、不可识别成分 `stats.extra.unidentifiable`、每成分证据量
      `stats.extra.comp_k`、CNMA vs 标准 NMA 对照 `te_cnma`/`te_nma`；
    - 默认出图 `forest`（成分效应森林图，S3 派发至 `forest.netcomb`）+ `netgraph`。
  - 新参数（`coze_contract.md` §2/§3 已同步）：`sep_comps`（单个字符，默认 `+`；非法值回退
    并告警）/ `inactive`（非活性·锚定成分）/ `interaction`（交互模型，默认 false）。
  - `.MA_ENGINE_VERSION` 2.9.18 → **2.10.0**。
  - **防御性设计（源自实测约束）**：
    1. 不可识别成分**如实返回 `null`，绝不填 0**（`netmeta` 默认 `na.unident=TRUE`；断网
       `discomb` 场景实测成分全不可识别），并置 `cnma:unidentifiable_components` 告警；
    2. 自由度 ≤ 0（不可检验）时 Q 统计量置 `null`——实测 `discomb` 断网场景 `Q.additive`
       会给出 `1.16e-30` 这类浮点退化值，看似有效数值、实为不可检验，直接判定为缺失；
    3. 治疗标签不含分隔符时置 `cnma:no_combination_labels` 告警，并提示可能误用 `nma`；
    4. 非 ASCII 标签置 `cnma:non_ascii_labels` 告警（netmeta 网络构建期对 locale 敏感）；
    5. NA → `null` 显式转换：jsonlite 的 `na` 参数默认为 `"string"`，与已设的
       `null = "null"` **不是同一开关** → NA 被序列化成字符串 `"NA"`（数字字段混入字符串，
       消费端无法按数值处理）。本分支输出已递归转换。**该问题为全引擎共性，其余 task 分支
       本次未改动，待单独评估后统一修复。**
  - **回归验证（本地端到端，5/5 通过）**：
    1. 加性 CNMA（合成，6 研究 / 6 治疗 / 3 成分）：`Q.diff=1.1469, df=2, p=0.5636`（加性
       假设可接受），成分效应 A/B/C = -0.280 / -0.263 / -0.241，与调研期独立脚本**逐位一致**；
    2. 断开网络（`discomb`）：成分全不可识别 → 全部 `null`，并触发 `no_combination_labels`
       / `disconnected_network` / `unidentifiable_components` 三重告警；
    3. 无组合标签（纯单成分治疗）：触发 `no_combination_labels` + `unidentifiable_components`；
    4. 二分类 OR + `inactive=["P"]`：成分数由 3 正确降为 **2**（锚定成分被排除）；
    5. **Linde2016 真实数据集**（124 对比 / 22 治疗 / **19 成分** / 耗时 39 s）：成分效应全部
       可识别；3 个真实组合治疗（`"Face-to-face CBT + SSRI"` 等）正确拆解为两成分——同时
       验证了「分隔符带空格自动 trim」；**加性假设被拒绝**（`Q.diff=6.5309, df=2,
       p=0.0382 < 0.05`）→ `cnma:additivity_violated` 告警如期触发，证明该诊断不是摆设。
    5 例均产出 forest + netgraph SVG（Linde 例：forest 19.8 KB / netgraph 67.3 KB）。
    > 注：调研期报告中 Linde2016 记为「93 研究 / 18 成分 / Q.diff p=0.083」，与本次
    > 「124 / 19 / p=0.0382」不一致，差异源于**所用数据子集不同**（调研期为验证目的做过
    > 研究级过滤）；本次为 `Linde2016` 全量 124 条对比行，结果可复现。
  - 文档同步：`coze_contract.md` §2（新参数）/ §3（task 枚举）/ §4（专属出参字段）；
    `SKILL.md §5` 能力边界表（原「CNMA 未实现」条目改写为已实现）；
    **新增 `references/component_nma.md`**（方法学选型 / `Q.diff` 解读 / 6 条常见坑 / 最小复现）；
    `classify.py`（新增 CNMA 关键词识别，且**前置**于 NMA 判定以免被抢）；
    `build_request.py`（`DEFAULT_PLOTS["cnma"]`）；`adapters/coze_contract_validate.py` 与
    `tests/deploy_retest.py`（`VALID_TASKS` / 完备性策略 / k≥2 拦截白名单加 `cnma`）；
    `adapters/coze_cases/case47_cnma_additive.json`（新增联调用例，契约校验无 fatal）。

- **能力边界表补全：RoB / PRISMA / GRADE 任务可发现性（2026-09-14，ct-update P1 复核）**：
  `run_task.R` 早已实现 `rob2`（RoB2 交通灯，自绘 ggplot，无 robvis 依赖）/ `rob_summary`
  （堆叠条形摘要）/ `prisma_checklist`（PRISMA 2020，27 项）/ `prisma_flow`
  （`metagear::plot_PRISMA` 四阶段流程图）/ `grade` / `tsa` / `power` / `nnt` / `gosh` /
  `ipd_meta` / `metainc`，但 `SKILL.md §5` 的 "Endpoint capability boundaries" 表**只列了
  pairwise/nma/survival/diagnostic**，导致这些已实现任务在能力边界上不可发现（易被误判为该技能缺口）。
  本次仅**补文档、不改引擎**（引擎位于 `adapters/coze/`，由作者人工维护）。
  同时显式标注：**component NMA (CNMA) 未实现**（netmeta 仅覆盖 arm-based NMA），
  请求 CNMA 必须声明缺口、**不得静默降级为 `nma`**。
  → ⚠️ **该「未实现」判断已于同日被推翻并落地实现**（见上方 `cnma` 条目：netmeta 3.6.x
  原生支持 CNMA，无需新依赖）。此处保留原文仅为记录判断演变，**以 `cnma` 条目为准**。

- **结果解读引擎 + 质量评估引擎（P0 + P1，2026-09-13）**：
  新增 `adapters/interpretation.py`（结果解读引擎）和 `adapters\quality_advice.py`（质量评估引擎），
  把 meta 技能从"计算工具"提升为"统计顾问"：
  - `interpretation.py`：基于 stats 自动生成结构化解读——一句话结论（显著/不显著/CI 跨零）、
    注意事项（异质性分档、发表偏倚、研究数过少、效应量极端、CI 跨度）、
    建议（亚组分析、敏感性分析、剪补法）、审稿人可能追问的问题。
    判定规则覆盖 I² 三档（≥75%/50-75%/＜25%）、Egger p（显著/不显著/研究数不足）、
    k 三档（<3/<5/≥5）、效应量极端（OR>10/<0.1, SMD|d|>3）、CI 跨无效值。
  - `quality_advice.py`：把 block_b 中 B2 GRADE / B3 过度声明 / B4 质量门解耦为独立函数，
    供 run_analysis（独立分析路径）和 fullflow（完整流水线）共用。
    自动推断偏倚风险、发表偏倚、不精确性，输出 GRADE 等级 + 过度声明列表 + 质量门评估。
  - `run_analysis.py`：B1 完成后自动调用两个引擎，结果体贴 `_interpretation` + `_quality_advice`。
  - `rendering.py`：HTML 报告 hero 卡下方新增"📊 结果解读"卡，展示结论、注意事项、建议、
    审稿人问题、GRADE 等级、过度声明数量。
  - 新增 `tests/test_interpretation.py`（19 例全绿）。全量 **66 例通过**。

- **出站信封前置校验 + 自动修复（2026-09-13，用户诉求）**：新增 `adapters/coze_contract_validate.py`，
  在 POST 到 coze 之前按 `coze_contract.md` 校验请求信封，拦截装错的信封（无论来源：LLM 手搓 /
  用户裸 POST / `build_request` 回归）。自动修复最常见的结构错误——并行顶层数组
  `data.yi/sei/slab`（或 2×2 四列）→ `data.rows[]` 行对象数组；`model:"random"→"REML"`、
  `"fixed"→"FE"`；`measure→sm`。致命不合规（缺 rows 且无并行数组 / 未知 task / 非法 model）→
  抛 `EnvelopeValidationError`，由 `run_analysis` 转 `_source:envelope_invalid` + `_error_analysis`
  结构化错误，**绝不把装错的信封发到云端**。校验点在 `coze_client.run_meta` 与 `run_stage`（stage 路径）
  出站前统一接入。

- **coze error 针对性诊断（2026-09-13，用户诉求）**：新增 `adapters/coze_error_analyze.py`，
  coze 返回 `status=="error"`（HTTP 200 ≠ 任务成功，对齐 LRN-20260817-002）时，把 `notes`/`warnings`
  按已知签名（data.rows 为空 / 缺效应量 SE / 缺列 / 缺 R 包 / NMA 需 ≥2 arm / 未知 task / 数据值异常）
  映射成`{code, summary, causes, fixes}`结构化诊断，附 `_error_guidance` 多行文本。`run_analysis`
  在 `status==error` 响应上自动附加；`run_meta.py` CLI 转印 `META_ERROR_GUIDANCE`。

- **测试**：新增 `tests/test_envelope_guard.py`（9 例，标准库），覆盖真实 bug 信封自动修复、
  修复后复验通过、合规信封无致命、缺 rows 致命拦截、coze error 各签名命中。

- **错误诊断细化 + 数据预检（2026-09-13，飞书 searchlog 实证驱动）**：用 `ct-update` 的
  `bugreport_download` 端点拉取 searchlog 表 `tblQ8OQ0rXsXQWkh`，筛 `skillname=meta` 共 322 条，
  其中 42 条 coze `status:error`。分析发现 **31 条（74%）落入 `COZE_E99_GENERIC` 兜底**，无针对性
  指引。据此：
  - `coze_error_analyze.py` 新增 7 个具体签名（E09–E15）+ NMA 非数值专项（E16），覆盖全部 42 条，
    generic 归零：E09 `sm` 与数据类型不匹配 / E10 必需列为 NULL（mean/n）/ E11 数据含 NA /
    E12 数据格式无法识别 / E13 NMA 网络不连通 / E14 该 task 需预计算效应量列 / E15 列数不对齐 /
    E16 NMA 数值列非数值。每条带 `causes` + 可操作 `fixes`。
  - `coze_contract_validate.py` 新增**警告级**数据预检（不阻断合法发送）：W07 `data.rows` 内
    NA/空值扫描（对应 9 条 `missing value where TRUE/FALSE needed`）。让用户出站前即时修，而非等 coze 报错。
  - 测试扩至 21 例（+12：9 个新签名命中 + W06/W07 正反向 4 例）。仍 0 条错误落 generic。

- **出站前预防性阻断（数据完备性，2026-09-13 续，用户诉求「明确不完备就直接打回」）**：
  在 `coze_contract_validate.py` 新增 `_check_data_completeness`（**致命 E07_DATA_INCOMPLETE**），
  按 task 的「数据形状」策略（`_COMPLETENESS_POLICY`）在 POST 前拦下**明确不完备**的请求，并
  **点名缺哪些列、每列用途**，由 `coze_client` 直接打回（绝不发到云端）。覆盖：`single_group_meta`
  （均数 mean+n / 比例 event+n 任一完备，缺则拦）、`pairwise_meta`/`subgroup_analysis`/`metareg`/
  等 strict_shape 家族（二分类四格表 / 连续型六列 / 发生率人时 / 预计算效应量 四选一，缺必需列即拦；
  `metareg` 额外需至少一个协变量列）、`forest_plot` 等 es_only 任务（缺 te/sete 即拦）、`nma` 轻量校验
  （需研究标识 + 干预臂 + 结局三件套）。设计权衡：**只对明确不完备抛 fatal**，冷门/未枚举格式不阻断
  （交 coze 端校验），宁可放过、绝不误杀合法请求；`render_guidance` 对 E07 额外输出「⚠ 数据明显不完备：
  请求已被【直接打回】」醒目横幅；`run_analysis` 的 `envelope_invalid` 分支现直接回传 `_error_guidance`
  供 CLI 打印 `META_ERROR_GUIDANCE`。（注：原 W06 警告级单组检查已升级为 E07 致命阻断。）
  - 测试：复用并扩展 `tests/test_envelope_guard.py`，纳入 `TestPreventiveBlock`（单组缺列 / pairwise
    无形状 / 二分类缺 n_ctrl / es_only 缺 sete / metareg 缺协变量 / nma 缺结构 均被 E07 阻断且明确
    ok=False；合法四格表/连续型/metareg 带协变量/nma 对比格式 均放行）。全量 **32 例通过**。

- **E11 单研究伪合并拦截 + quality 门防御（2026-09-13 续，飞书 searchlog 成功记录异常分析驱动）**：
  下载全量 680 条 searchlog → 筛 meta 323 条 → 281 条成功 → 逐条解析 `stats.pooled` / `heterogeneity` /
  `quality_gate`。发现 **111 条（39.5%）"表面成功实则可疑"**，6 类异常：F2 极端效应量（60条）、F5 红灯仍呈现（31条）、
  F3 CI 过宽（26条）、F4 CI Inf/NaN（20条）、F6 高异质+极小证据体（4条）、F1 k=1 伪合并（1条）。据此：
  - `coze_contract_validate.py` 新增 `_check_single_study`（**致命 E11_SINGLE_STUDY**）：对 pairwise_meta /
    single_group_meta / subgroup_analysis 等 task，rows < 2 直接拦截（k=1 的"合并"实为单研究效应，统计无意义）。
  - `run_analysis.py` 新增 **本地 quality 门防御**：即使顶层 status=ok，也检查 `stats.quality_gate.status`，
    red 时强制标记 `_pooled_suppress=True` + 追加 `_quality_gate_red_warning` + 顶层 status 降级为 warn。
    **消费端（渲染层/CLI）不应呈现红灯记录的合并效应**。

- **F2 效应量极端防御 + W08 零单元格预警（2026-09-13 续，飞书 searchlog 111 条成功异常中 60 条）**：
  上一轮 `analyze_success.py` 已标记 60 条极端效应量（OR>10/<0.1、SMD>3），但 `run_analysis` 仅
  flag + 记文件，未给用户任何提示。现新增 `_check_effect_size_extreme()` 判定函数（OR/RR/PLO/PLOGIT
  阈值 >10 或 <0.1；SMD/MD/ZCOR 阈值 |d|>3），命中时顶层 status 降为 warn、结果贴
  `_effect_size_extreme_warning`。**极端可能真实，故不阻断**——只给用户看提示，用户确认后再决定是否切
  Peto 法重跑（不自动重跑）。文字指引已修正：coze 端已内置 Haldane 自动校正（event+0.5, n+1），
  无需建议用户手动加 0.5；改为提示"若仍不理想可改用 Peto 法"。
  - `coze_contract_validate.py` 新增 **W08_ZERO_CELL 警告**：扫描二分类四格表中 event_exp/event_ctrl=0
    的行（用 `is not None` 避免 Python truthiness 把 0 当 falsy 跳过），预警 OR 可能极端并建议 Peto 法。
    仅警告不阻断。
  - 测试扩至 47 例（+2：W08 正反向）。
  - coze 端修复标注：bug 根源在 `run_task.R` 第 1433 行 `list(status = if (length(warns)) "warn" else "ok", ...)`，
    quality_gate=red 不影响顶层 status。修复：在第 1433 行前插入 `if (!is.null(stats$quality_gate) &&
    stats$quality_gate$status == "red") warns <- c(warns, "quality_gate:red")`，确保红灯强制顶层 warn。
    **待下次 coze 部署时生效**（本地防御已立即生效）。
  - 测试扩至 **35 例全绿**（+3：E11 单组/配对 k=1 拦截 + 配对 2 行放行）。

- **A2 菜单二轮调整（2026-09-11 二次裁定）**：`[1] 批准并导出合并表` → **「批准并下载 PDF」**
  （明示批准触发 A4 自动落盘：OA 下载 + 本地 `pdf_dir` 优先抽取）；**恢复 `[4] 传回修改后的合并表`**
  —— 修复接缝：[4] 由原 `kind=file`（纯展示，`build_decision` 不可执行）改为
  **`kind=revise, key=screened`**（`EDITABLE_KEYS` 本就收录），传回内容经
  `apply_screening_upload` 解析后走**标准 decide 通路**落 `screened` 修订并重跑下游；
  `[3] 导出检查（不改变状态）` 保持 file/export（agent 侧动作）。A2 选项 4 项；
  `file_io_v` 交接文案、`a1_need_topic` 提示同步。测试 189 PASS。

- **A4 首次出现提示：要求提供本地 PDF 路径**（2026-09-11，用户裁定）：③ 数据抽取（A4）
  菜单首次出现时提示用户发送本地 PDF 所在文件夹/文件路径；路径经新增修订键
  `pdf_dir`（EDITABLE_KEYS["A4.data_extraction"]）登记，`_run_block` 注入
  `run_block_a(pdf_dir=…)` → 覆盖 A4 PDF 缓存目录，本地已有 PDF 优先被抽取，
  减少付费墙漏检。已登记后提示行改为展示路径值；启动配置可预置 `cfg.pdf_dir` 跳过提示。
  触及文件：`scripts/flow_menu.py`（pdf_hint/pdf_dir_set 文案 + `_a4_summary` 提示行）、
  `adapters/fullflow.py`（EDITABLE_KEYS + 注入）、`adapters/block_a.py`
  （`run_block_a` 新增 `pdf_dir` 形参）。测试 187 PASS。

- **论文撰写辅助 · writing_advisor 引擎（P2a 本地基线，2026-09-14）**：新增
  `adapters/writing_advisor.py`（论文撰写与发表建议引擎）+ `references/field_templates.json`
  （领域知识库：oncology/cardiology/general 真实种子 + 8 个 stub 领域），把 Block C 的
  「发表建议」子能力落地为可单测的自包含模块（不依赖 coze / LLM，离线可交付）：
  - 领域推断 `infer_field`（关键词纯规则，确定性强可单测；未命中→general）。
  - 基于 stats + 领域模板生成结构化建议：优势 / 限制段要点 / 填空式讨论段模板 /
    审稿人可能追问 / 期刊推荐表（field_templates 静态种子，IF 带 * 为近似值）/
    PRISMA 核查 / 报告规范 / 数据可用性 / 参考核验（结构层：DOI 格式校验）。
  - 混合架构（v2）：默认 `use_network=True` 预留 P2b 网络增强 seam
    （`_fetch_openalex_journals` 查 OpenAlex sources 实时指标 + `_verify_refs_online`
    接 verify_citations 在线核验 + 复用 `.merged.json` 证据接地），网络失败静默降级静态/结构层，
    不阻断主流程。
  - `rendering.py`：HTML 报告「📊 结果解读」卡之后新增「📝 发表建议」卡
    （期刊推荐表 / 优势 / 限制段要点 / 审稿人问题 / 讨论段模板折叠 / PRISMA 核查 /
    报告规范 / 数据可用性 / 参考核验，双语文案 zh+en）；`out["_publication_advice"]` 缺省不渲染。
  - `run_analysis.py`：B1 完成后（仅当 `advise=True`）自动调用 `advise_publication`，
    复用 `_interpretation` + `_quality_advice`（GRADE 透传），结果贴 `_publication_advice`，异常静默跳过。
  - 新增 `tests/test_writing_advisor.py`（14 例全绿）：领域推断 / 全字段齐备 / 静态种子来源 /
    缺 stats 不崩 / 讨论段数字填空 / `use_network=False` / 结构层参考核验。
  - 附（关键 bug 修复）：原 `run_analysis.py` 缺失 `def run_analysis`，编排块误嵌于
    `_check_effect_size_extreme` 内，致 `import run_meta` 直接 ImportError、整条计算轨不可用；
    已恢复 `def run_analysis(...)`，并在 `_quality_advice` 之后、`render_html_report` 之前接线 advise。

- **论文撰写辅助 · writing_advisor 引擎 P2b 网络增强（2026-09-14）**：默认 `use_network=True` 时
  复用兄弟技能 `ct-literature` 的 `http_utils`（OpenAlex 礼貌池 + 指数退避，优先 keyed 池
  `OPENALEX_API_KEY`，无 key 走 keyless 100/day）+ `verify_citations`（DOI/PMID/OpenAlex 三重解析
  + 标题作者一致性，抑制幻觉引用），并通过 `.merged.json` 做证据接地：
  - `_fetch_openalex_journals`：按领域种子期刊名查 OpenAlex `sources`，以 `summary_stats.2yr_mean_citedness`
    覆盖近似 IF（标记 `if_proxy`）、并补充 `h_index` / `cited_by_count` / `apc_prices`（USD 格式化）/
    `is_oa`；名称不匹配或单刊失败保留静态种子。
  - `_verify_refs_online`：逐条 `verify_one` 在线核验，状态词表 verified / bot_blocked / mismatch /
    unresolved / no_identifier / suspicious；出版方 403 记为 bot_blocked（疑似真实，非缺失）；
    单条异常退化为结构层校验，整批不阻断。
  - 证据接地：入参 `merged_json`（路径或 dict）报告真实检索语料规模，与 `stats.k` 对齐（`k_match`）；
    未显式给 references 时从其 works 抽 DOI 走在线核验。
  - `rendering.py`：来源=openalex 时期刊表脚注改为「OpenAlex 实时（IF* 为 2yr_mean_citedness 代理）」；
    参考核验卡支持在线状态词表 + 一致性标记；新增「🔎 证据接地（merged.json）」行。
  - 降级保证：ct-literature 缺失 / 断网 / 配额耗尽 → 自动回退静态种子 + 结构层核验（`network_ok=False`），
    不抛、不阻断。`adapters/tests/test_writing_advisor.py` 由 14 例扩至 **26 例**（注入假模块离线验证）；
    回归 `test_interpretation` + `test_envelope_guard` 共 **92 例无回归**。

- **论文撰写辅助 · writing_advisor 引擎 P2c 打磨（2026-09-14）**：三项「联网可选、失败降级」增强，
  与 P2b 同构；`use_network=True`（默认）生效，任一失败静默回退，不抛不阻断。
  - **领域自动归类增强（OpenAlex concepts）**：规则命中优先级不变（确定性强、可单测）；
    未命中且有语料时，取 `.merged.json` 的 `works[].concepts` / `keywords` 概念名做词频投票
    （`_concept_names` → `_vote_field_from_concept_names`，映射复用现有 `_FIELD_KEYWORDS`，
    泛概念如 Medicine/Biology 不误命中）；仍不命中且联网则用 OpenAlex 作品搜索取概念；
    最终兜底 `general`。新增 `_infer_field_ex(topic, field, merged_json, use_network)`，
    输出 `field_source ∈ rule | corpus | openalex | default` **透明标注来源**。
    实测真实语料（psychiatry 相关 `works`）→ `corpus` 命中 psychiatry（58 票）。
  - **报告规范在线核验（EQUATOR 无免费 API 的稳健替代）**：`_reporting_standards(task, use_network)`
    维护 PRISMA 2020 / MOOSE 权威登记（名称 + 出处 DOI + URL），联网时用 `verify_citations`
    核验出处 DOI 真实存在，输出 `prisma_source ∈ verified_online | static`。
    ⚠️ 判据修正：早期误用 `status == "verified"`，导致出版方 403 的 `bot_blocked`（DOI 真实、
    仅拦爬虫）被误判为失败、`prisma_source` 低估为 static；已改用 `citation_verified`
    （ok / bot_blocked 均表示 DOI 已解析到真实资源）→ 真实网络下正确得到 `verified_online`。
  - **Semantic Scholar 高引推荐（有 key 才用）**：`_highly_cited(topic, field, use_network, limit=5)`
    沿用 ct-literature 既有策略——`load_s2_key()` 无 key 直接跳过（不发注定 429 的请求），
    有 key 时按主题/领域查高引论文 top 5（title/year/citations/venue/doi）并排序；
    状态词表 ok | skipped_no_network | skipped_no_client | skipped_no_key | skipped_no_query | degraded，
    经输出键 `s2_status` 暴露。
  - `rendering.py`：发表建议卡增加 `field_source` 来源标注、`prisma_source` 脚注与出处链接、
    高引推荐列表（折叠 `<details>`）。
  - 降级保证不变：ct-literature 缺失 / 断网 / 无 S2 key → 静态清单 + 规则领域 + 跳过高引。
    `adapters/tests/test_writing_advisor.py` 由 26 例扩至 **52 例**（P2c 新增 26 例，全部离线 mock）；
    连同 `test_interpretation` + `test_envelope_guard` 共 **118 例通过**。

- **Block C（论文撰写与修改）全流程完备性审查与修复（2026-09-14）**：对 C1→C4 做端到端审查，
  发现并修复 **8 类缺陷（含 2 处红线级）**；`adapters/tests/test_block_c.py` 由 15 例扩至 **26 例**。
  - 🔴 **C3 断网误判「疑似虚构」**：`ref_verify._get` 把所有异常吞成 `None` → `not_found`，
    离线/API 不可达时**真实文献被判虚构并置 critical**（红线误杀）。新增 `_get2` 区分
    **明确未收录（HTTP 404）** 与 **网络/接口不可达**，后者新增状态 `unverified_offline`
    （C3 计 `n_unverified`、**不判 critical**，note 提示「须联网重试」）；`_get` 降为兼容包装。
  - 🔴 **C4 QA 红线泄漏**：`references=None`（零条参考被真实核验）时，「参考完整性核验通过（C3）」
    仍报 `pass=True`。改为按 C3 新增的 `refs_verified`（= 有参考 ∧ 无 critical ∧ 全部完成真实核验）
    判定，未核验时 `pass=False` + 「不可投稿」。
  - 🔴 **C3 忽略上游 `is_retracted` 标注**：已知撤稿文献若缺 DOI/PMID，API 无法判定 → 撤稿文献
    可绕过 `reference_verification` 红线。`verify_references` 现采纳入参 `is_retracted` 提示并置
    `status=retracted`（含无标识条目）。
  - **C3 英文稿误判缺章**：章节核验只认中文（`s.title()` 对中文无变化）→ 英文章节名全被判缺失并置
    critical。改为 `_SECTION_PAIRS` 中英对照、**任一侧命中即视为存在**；`_REQUIRED_SECTIONS` 由其
    派生（消除原死代码）。另加兜底：只给 `manuscript` 未给 `sections` 时从正文 `## 标题` 识别。
  - **C 阶段 `prev_stage_id` 跨块泄漏**：`block_c` 复用 `block_b._mk_stage`（内部取
    `BLOCK_B_SEQUENCE`/`BLOCK_B_TOTAL`）→ C2/C3/C4 的 `prev_stage_id` 指向 `B1/B2/B3`（溯源错误）。
    本块自行实现 `_mk_stage`（用 `BLOCK_C_SEQUENCE`/`BLOCK_C_TOTAL`），与 block_a/block_b 同构。
  - **C3 静默丢弃无标识参考**：去重键 `"{doi}|{pmid}"` 使多条无 DOI/PMID 的参考折叠为同一 key
    `"|"` 而被跳过。改为只对有标识条目去重，无标识用下标唯一化。
  - **C3 `notes` 计算后被丢弃**：`notes`（核验结论说明）构建后未进返回 dict，与 docstring 声明的
    `{report, critical, notes, coze_ready, ...}` 不符。现返回 `notes` 并新增 `refs_verified`
    （`coze_ready` 保留为向后兼容别名，coze 依赖已于 P2b 移除）；`note` 改为随结论动态生成。
  - **死代码/坏味**：`c3["critical"] or True` 恒真三元（C3 为红线闸，恒需人工批准）→ 直写 `await_human`。
  - **SPEC 漂移**：`contracts/pipeline_stage/v1.0.0/SPEC.md` §9 的阶段 ID 与实现及全部 fixtures
    （`fullflow.GATE_TO_STAGE` / `flow_menu` / `form_schema` / `driver_demo` / `cases/fullflow_session_*.json`）
    长期不一致（SPEC 写 `C2.manuscript_review`/`C3.ref_verification`/`C4.grade_table_ev` 与 5 段 B，
    实际为 `C2.ai_review`/`C3.ref_verify`/`C4.evidence_qa` 与 4 段 B）；§3 示例同步更正为 `C2.ai_review`。
  - 附：`scripts/smoke_human_gates.py` 的 `fake_a2` 形参漂移（缺 `sources`）致脚本中断在 A2、C3/C4
    覆盖无法执行 → 签名对齐后 **ALL PASS**。
  - 验证：`test_block_c` 15→**26 例全绿**；`adapters/tests` 全量失败数 11→8（余 8 项为既有 coze 契约层
    与缺 `fastapi`/`reportlab` 环境问题，与本模块无 import 交集）；`deploy_retest` G3 **GO**；
    真实网络端到端：PRISMA 2020（`10.1136/bmj.n71`）等 2 篇 → `status=ok`、`refs_verified=True`、
    QA 全 PASS，闸门 `C3→C4→done` 正确推进。

### Changed

- **A2 菜单收敛为 3 项（2026-09-11 用户裁定）**：移除「[4] 传回合并表」（上传入口撤销，
  用户离线修改后直接走 ③ 数据抽取/A4 修订）；`[1]` 标签改为「批准并导出合并表」
  （明示批准即自动落盘 Excel）；`[3]` 标签改为「导出检查（不改变状态）」（明示只读、
  不推进状态机）。摘要「文件交接」行同步改为「仅供检查；如需修改，到 ③ 数据抽取（A4）
  修订」；A1 缺选题提示文案同步。底层 `apply_screening_upload` 解析器保留（编程式
  调用仍可用），仅撤销菜单入口。回归 `tests/test_flow_menu.py` 185 PASS。
- **飞书汇总留痕降耗（协同变更，meta-analysis 侧零代码）**（2026-09-11）：
  下游 ct-literature v1.1.2 的飞书汇总调用改用 `mode="log_only"`
  （Coze 端 `ct-registry/adapters/coze` v0.2.0 `route_by_mode` 直连 `feishu_write_node`，
  跳过检索节点，仅写审计记录）。meta-analysis 经 `tool_card` 传入的常规检索调用
  不带 `mode`，行为完全不变。

### Added

- **A1 菜单新增「帮助选题（可行性速览）」**（现为 A1 第 4 项，`scripts/flow_menu.py`，2026-09-11）：
  选题阶段即可按需触发一次注册库探针（`block_a.a1_registry_check`），把
  `registry_probe` / `feasibility` 写回 A1 `stage_result`，菜单摘要随即补出
  「注册库探针」行（条数 + 拥挤度 + 风险预警），辅助用户在放行 ② 前先评估可行性。
  - 新增 CLI 子命令 `probe`（`flow_menu.py probe --apply`），默认 dry-run；
    `--max N` 控制探针样本上限。
  - 非状态机决策项（不推进流程、不进 `human_decisions`）；选题缺失时菜单自动隐藏。
  - 探针异常（`ct-registry` 缺失 / 网络失败）优雅降级为 `status=error`，不阻断 A1。

### Changed

- **A1 缺选题时不再渲染可操作选项**（2026-09-11 逻辑修正）：选题菜单在尚无有效选题（`_a1_topic_missing`）时，只渲染提示行（`a1_need_topic`，引导用户先发主题文字），**不渲染** `[1]批准 / [2]改PICOS / [3]改检索范围 / [4]可行性速览`——避免"还没选题就出现批准选项"的怪异状态。选题确认后菜单才给出完整 4 项。测试：`tests/test_flow_menu.py` 178 PASS（新增「A1 缺选题 → 不渲染任何可操作选项」断言）。
- **A1 移除「上传裁决表并放行」入口**（2026-09-11 用户裁定）：该入口**只保留在 A2 合并节点**
  （`[4] 传回合并表`），不再出现在 A1。A1 现收敛为 4 项：
  `[1]批准 [2]改PICOS [3]改检索范围 [4]可行性速览`。A1 缺选题提示文案同步改为指引用户在
  进入 ② 后用 A2 节点上传。测试：`tests/test_flow_menu.py` 177 PASS（A1 选项 5 → 4）。
- **A1 选项 3「改检索范围」扩展为同时控「综述 + 数据源」**（2026-09-11 用户裁定）：
  除 `include_reviews`（原始研究-only ↔ 含综述类）外，新增 `sources` 检索数据源增减。
  - 菜单项 `[3]` 现声明 `keys=["include_reviews","sources"]`，agent 收集两值；
    `build_decision` 对多键修订一次性占位两键。
  - `sources` 进入 `EDITABLE_KEYS["A1.topic_selection"]`；`fullflow._run_block` 读
    `latest_revision("A1.topic_selection").sources` 注入 `run_block_a(sources=…)` →
    `a2_literature_search` → `a2_build_tool_card` 的 `params.sources`，透传 ct-literature。
  - 可选池 `block_a.AVAILABLE_SOURCES` = OpenAlex / EuropePMC / bioRxiv / medRxiv /
    SemanticScholar / arXiv（与 ct-literature `fetch_coze_unified._SOURCE_DISPLAY`
    单一真源一致）。
  - A1 摘要「检索范围」行追加数据源列表（`检索范围：<模式> ｜ 数据源：OpenAlex、EuropePMC`）。
  - 测试：`tests/test_flow_menu.py` 182 PASS（新增「选项3 声明双键」「sources∈EDITABLE_KEYS」
    「decide→双键占位」「scope 行含数据源」4 条断言）。
- **检索数据源（`sources`）现已真正被 ct-literature 消费**（2026-09-11 实测修复）：
  此前 `params.sources` 会被静默丢弃——`tool_mapping_meta.json` 的 `arg_map` 未把
  `sources` 映射到 CLI，且 ct-literature 根本没有 `--sources` 参数。三处已补齐：
  - `tool_mapping_meta.json`：`arg_map` 增 `"sources": "--sources"`；
  - `block_a.a2_build_tool_card`：`sources` 列表归一为逗号串（`str(list)` 会得到
    `"['A', 'B']"`，ct-literature 无法解析）；`None` 时不写键（默认全量行为不变）；
  - ct-literature `ct_literature.py` 新增 `--sources`（逗号分隔子集，**覆盖**各
    `--with-*` / `--cochrane` 默认；未知源名报错退出；`PubMed` 别名并入 EuropePMC；
    OpenAlex 为管线基座不可关闭，缺省时 stderr 提示）。
  - **诚实更正**：早先 `AVAILABLE_SOURCES` 里的 `PubMed` / `Cochrane` / `WebOfScience` /
    `Scopus` 是错的——PubMed 并入 EuropePMC、Cochrane 是 EuropePMC 的 journal-filter
    子模式、WoWS/Scopus 无授权 API，均非 ct-literature 独立可检索源。
  - 测试：`adapters/tests/test_block_a.py` 18 OK（新增 `test_sources_wired_to_cli`、
    `test_available_sources_are_real` 两条回归，锁住「arg_map 缺 sources」这类静默失效）。
  - 端到端实测（无网络，preview 模式）：`--sources "OpenAlex,EuropePMC"` →
    `sources=[OpenAlex + EuropePMC]`；`--sources "OpenAlex"` → `sources=[OpenAlex]`；
    无参 → 默认 `[OpenAlex + EuropePMC, bioRxiv, medRxiv]`（向后兼容）。

### Fixed

- **出站 coze 信封补齐 `skill_version` + `user_language`**（2026-09-11，对齐 ct-base
  `coze_io_contract.md §1.1/§1.2`）：此前 meta-analysis 的 `run_meta` / `build_stage_payload`
  只带 `contract_version` / `schema` / `query_origin` / `request_id`，**缺** ct-base 要求的
  `skill_version`（顶层）与 `params.user_language`（对照组：ct-literature 早已携带三者）。
  - `adapters/coze_client.py` 新增 `_skill_version()`（读 `SKILL.md` frontmatter `version:`，
    失败回退 `2.12.0`）、`_resolve_user_language(override)`（三级优先级，复用 `scripts/i18n._current_lang`）、
    `_with_user_language(params, override)`（单一承载位，已有有效值不覆盖）。
  - 注入点：`run_meta`（顶层 `skill_version` + `params.user_language`）、`build_stage_payload`
    （同）、`run_stage`（新增 `user_language` 透传，legacy 分支同样转发）。
  - 契约细节：`skill_version` **仅顶层**（不得嵌套 `params`）；`user_language` **仅 `params`**
    （顶层不双写）；均可选 + 向后兼容（缺失不改变旧格式）。`sanitize_payload` 只重写字符串值、
    不丢键，故两字段安全穿过出站脱敏。
  - 测试：`adapters/tests/test_pipeline_client.py` 新增 `TestCozeContractFields`（3 条：
    stage 信封字段位、legacy `run_meta` 字段位、`user_language` override）→ **10 OK**（原 7）。
    `test_fullflow.py` 9 OK、`test_block_b.py` 20 OK 无回归。

- **A1 修订（改检索范围 / 改 PICOS）之后回到 A1 等待批准**（2026-09-11，用户裁定）：
  此前 A1 的 `revised` 决策走通用 `_advance` 路径 → 重跑整块 Block A（含全库检索）并越过
  A1 批准闸直接跳到 A2，既触发无谓的全库检索、又让"改个检索范围"跳过了 A1 批准。
  - `adapters/fullflow.py` 的 `resume_fullflow` 对 `stage_id=A1.topic_selection` 的 `revised`
    决策新增特例：**只把修订补丁进 Block A 信封的 A1 `stage_result`**（`include_reviews` /
    `sources` / `report`，跳过值为 `None` 的占位键），随后**停回 A1**（`await` 仍为 A1
    软停，不重跑、不前进）。用户复核新检索范围后于 A1 批准，才按新范围触发真正的检索。
  - 修订仍经 `record_decision` 落盘（审计不丢）；`latest_revision("A1.topic_selection")`
    后续被 `_run_block` 读取，注入 `run_block_a(include_reviews=…, sources=…)`，批准即生效。
  - 信封缺失（异常）时回退通用重跑路径，行为降级安全。
  - 测试：`adapters/tests/test_fullflow.py` 新增 `TestA1ReviseStaysAtA1`（3 条：
    `test_revise_scope_returns_to_a1` 断言停回 A1 且 `a2_literature_search` 调用 0 次、
    信封 A1 `stage_result` 已补写、修订已落盘；`test_revise_report_also_returns_to_a1`；
    `test_approve_after_revise_triggers_search_and_advances` 断言批准后才触发检索且仅 1 次）
    → **12 OK**（原 9）。

## [2.12.0] — 2026-09-10 — A2/A3 合并为单节点「文献集」（D21）

> **一句话**：把 Block A 的 **A2 检索** 与 **A3 初筛** 合并为单节点「文献集」
> （`A2.literature_search`）——一次软停、一张合并表。A 阶段序列 `A1→A2→A3→A4`
> ⇒ **`A1→A2(文献集)→A4`**（停靠点 4→3）。并顺带修掉「批准即重跑检索」。

### Added

- **合并节点 `_a2_merged_nha()`**（`adapters/block_a.py`）：该节点 `next_human_action` 的唯一真源，
  键位刻意保留 `coverage`（原 A2）/ `summary` / `decisions`（原 A3），避免下游漂移。
- **两条入口**（用户明确要求）：
  1. **从 A1 过来**——A1 批准 → 系统自动检索 + 同节点内规则初筛 → 软停。
  2. **用户自己上传 Excel 转换过来**——A1 菜单 `[4] 上传裁决表并放行`，或 A2 节点内 `[4] 传回合并表`。
     识别到「裁决」列即按裁决表解析（`apply_screening_upload`，仅替换 `summary`/`decisions`，保留 `coverage`）；
     无「裁决」列视为文献清单整表替换。
- 合并表导出 `export_screening_xlsx()` 产出单张表：检索结果底表 + 「裁决 / 理由 / 文献类型确认」列。

### Changed

- `BLOCK_A_SEQUENCE` = `[A1, A2, A4]`；`fullflow.DEFAULT_PAUSE_AT` 删 `A3.screening`；
  `EDITABLE_KEYS["A2.literature_search"] = ["query", "screened"]`。
- `workbench/form_schema.py`：`STAGE_ORDER` 删 A3 行、A2 标题改「文献集（检索 + 初筛）」；
  `SCHEMA["A3.screening"]` 整段删除；`TITLE_EN` 同步。导航条 12 → **11 节点**。
- `scripts/flow_menu.py`：`A_STAGES` 去 A3；`_a2_summary` 合并检索覆盖 + 初筛漏斗；
  `_a2_options` = `[1]批准 [2]改检索式 [3]导出合并表 [4]传回合并表`；`_a1_options` 增 `[4]`；
  删 `_a3_summary`/`_a3_options`；A4 回退目标改 A2。L0 导航条与 A 阶段编号随之更新。
- 自动导出文件名 `A2_检索结果_<pid>.xlsx` → **`A2_文献集_<pid>.xlsx`**。

### Fixed

- **「批准即重跑检索」**：原 `_run_block` 仅在（旧）A3 已批准时复用缓存，批准 A2 会整块重算 →
  检索漂移 + 人工在 Excel 上的复核被作废。合并后判断点上移到 **A2 已批准**，续跑复用 A1/A2
  缓存、只跑 A4（`start_stage="A4"`）。
- `scripts/smoke_human_gates.py` stub `fake_a2` 的 `source` 用小写（`openalex`）而生产为 TitleCase
  （`OpenAlex`）→ `CORE_SOURCES` 判定漏配、`search_status` 误降级为 `partial`；已修正 stub 并补
  `skipped` 断言。
- `adapters/tests/test_fullflow.py` `sys.path` 只加了测试目录（未加 `adapters/`）→ `import block_a` 失败；
  补 parent 路径。
- `adapters/tests/test_block_a.py`（全仓扫描才发现的漏检项）：① `_fake_execute_tool_cards` 与
  `_fake_reg_exec` 缺 `on_line` 形参 → 生产侧 `a2_literature_search` 透传流式回调时 `TypeError`；
  ② `test_a2_ran_in_pipeline` 断言 `[A1,A2,A3,A4]` → `[A1,A2,A4]`；③ `test_gate_rejects_wrong_stage`
  的反例由 `ba.A3` 改 `"B1.merge"`（A3 已非停靠阶段，避免歧义）。修前 7 errors → 修后 16 tests OK。

### Verified

- `tests/test_flow_menu.py` **175 PASS / 0 FAIL**（原基线 179，见说明：删 A3 用例、并入 A2 断言）。
- `tests/test_a3_doc_type_confirm.py` **28 PASS / 0 FAIL**；`adapters/tests/test_fullflow.py` **9 tests OK**；
  `adapters/tests/test_block_a.py` **16 tests OK**；`adapters/tests/test_block_b.py` 20 OK；
  `adapters/tests/test_pipeline_client.py` 7 OK；
  `adapters/tests/test_phase2_rewind_revise.py` OK；`scripts/smoke_human_gates.py` **ALL PASS**。
- **两处既有失败与本轮合并无关**（供后续单独处理）：`tests/test_pdf_extractor.py` 缺 `reportlab` 依赖；
  `tests/test_block_c.py` 3 failures —— 该测试只 import `coze_client`/`block_c`（不 import `block_a`），
  失败源自更早会话对 `coze_client.py` 文案的改动，属既有技术债。

### Compatibility

- `block_a.A3 = "A3.screening"` 常量保留；旧会话的独立 A3 载荷（`screened`/`decisions`）仍可被
  `export_screening_xlsx` / `apply_screening_upload` / `_run_block` 续跑读回；**新会话不再产生 A3**。

---

## [2.11.1] — 2026-09-10 — CCM 实测记录：2 项契约缺口 + 1 类数据陷阱（**无代码改动**）

> **一句话**：用 `runs/` 真实会话把 CCM 跑起来做验收，渲染器本身正确，
> 但暴露了 **A4 下载配额**、**A4 菜单不暴露 `fetch_log`**、以及**旧会话数据被当新契约渲染**三类问题。
> 本轮**只改文档**：规范新增 §7.1 + §8 两行；交接文档 `references/HANDOFF_2026-09-10.md` 整篇重写。

### Added — 规范 `references/conversation_flow_menu.md`

- **§7.1 会话版本漂移**：`runs/` 存量会话可能早于当天契约，CCM 会**照实渲染旧语义**（看起来正常、实则误导）。
  给出**贴菜单前必验的 4 个字段**：`await.gate` 是否闸名字符串 / `per_doc[*].doc_type_confirmed` /
  A3 行有无 `doc_type_source` / `cursor.block` 与 `stage_id` 是否同块。附两例实测（`ff-9fc5c5469a4d`、`ff-65e2e0076337`）。
- **§8 新增 D18**：A4 下载配额 `max_attempts=12`（`block_a.py:1645`，值来自 `fullflow.py:232`）
  **与「100% 按列表下载」直接冲突** —— 实测 59 篇过 A3 门控仅 12 篇发起下载、**45 篇被静默 `quota_deferred`**；
  且 A4 菜单**无「继续下一批」入口**，这 45 篇在对话侧不可达。
- **§8 新增 D19**：A4 菜单未暴露 `fetch_log` 门控分布，`已下载全文 0` 甚至掩盖
  「盘上已有 1 份 PDF 但抽取失败（fitz 缺失）」这一事实。与 A2「沉默漏检」同类，应照搬其做法。

### Changed — 交接文档 `references/HANDOFF_2026-09-10.md`（整篇重写）

- 状态从「CCM 设计完成、**代码未写**」更正为「**两轮均已落地**（2.11.0）」。
- 新增 §1.2（CCM 7 项改动 + 实现期修的 4 个渲染层 bug）、§5（CCM 怎么调用：两个调用面 / CLI / 三层菜单 / 六条硬约束 / 全局指令）。
- 静默失效模式从 3 类扩为 **4 类**（新增「旧会话数据」）。
- §6.2 决策表补 **D18 / D19** 并附实测数据；§6.3 记录 `test_a4_b1_handoff.py` **现在会中途崩溃**
  （`tests/test_a4_b1_handoff.py:164` 未捕获 `TypeError`，一行守卫即可，**未改**）。
- §8 陷阱清单从 A–H 扩为 **A–L**（新增 I 会话版本漂移 / J `relevance_skip` 误读 / K A4 计数不同量纲 / L 渲染器不做版本校验）。
- §7 基线更正：`test_a4_b1_handoff.py` 为 **9 PASS / 4 FAIL + 尾部崩溃**（原文档记的 7 PASS/4 FAIL 已过时）。

### Docs — 澄清一处易误判点

- `a4_stream` 的 `gate="relevance_skip"` 触发条件是 `decision_of(sc) == DECISION_EXCLUDE`，
  即**消费 A3 裁决**，**不是**在 A4 重新判类型。会话数据里「review-guard 默认排除：命中综述特征…」
  是 A3 侧写下的 `reason` 被原样带出 —— 看到这句话不要误判为违反「人工确认后不再判类型」。

---

## [2.11.0] — 2026-09-10 — CCM 对话上下文菜单落地：菜单由代码产出，不再靠 LLM 即兴

> **一句话**：给工作台同一套 schema 加一层**对话投影**——全流程轨道每次停靠都渲染
> **代码生成、选项穷举、红线约束由状态机派生**的菜单，解决"同一节点两次渲染不一致"。
> **规范 → `references/conversation_flow_menu.md`** · **代码 `scripts/flow_menu.py`** · **回归 `tests/test_flow_menu.py`（153 PASS / 0 FAIL）**
> 设计归档 → `references/design/ccm/`（v0.1–v1.0，仅存设计过程）

### Added — `scripts/flow_menu.py`（CCM 渲染器，确定性）

- **三层菜单**：L0 导航条（12 节点压一行，✓/▶/○，每轮必贴）· L1 节点菜单（标题 + 摘要 + ⚠️ 预警 + 穷举编号选项）· L2 字段菜单（`EDITABLE_KEYS`）。
- **CLI**：`status` / `menu` / `nodes` / `decide` / `rewind`，支持 `--session` `--lang zh|en` `--json`。
  - `decide` / `rewind` **默认 dry-run**（只校验不落盘），加 `--apply` 才推进状态机。
  - 退出码 `0` 成功 / `2` 用法或校验错误 / `3` 会话缺失。
- **回显块**：固定前缀 `## 当前流程设定 / Current pipeline settings:`，与计算轨道 `## 当前分析设定:` 分离、互不覆盖。
- **A 阶段四节点菜单**：A1（PICOS + 探针一行 + 检索范围开关）、A2（覆盖 + 沉默漏检 + `/源` 上限标注）、
  A3（纯文件交接，**对话内零逐条编辑入口**）、A4（🔴 无跳过 + 待补传 PDF + 类型只读），加块间交接闸 2 选项。

### Changed — 防漂移：选项与可编辑键一律由代码派生

- **R3** 🔴 选项集由 `cc._REDLINE_GATES` 过滤 → A4 菜单**不可能**出现「跳过」；即使 LLM 误造，
  `fullflow._validate_decision` 也会拒（双保险，不靠提示词）。
- **R4** revise 选项 ⊆ `fullflow.EDITABLE_KEYS`；**未收录的键显式标注「暂不可用」，不静默丢弃** ——
  A2「改检索式」因 D16 未决而暴露为 `[2] 改检索式（暂不可用）`，把既有接缝摆在明面上。
- **R5** 当前节点与回退候选集从信封 stage 序列派生（与 `workbench/server.build_state` 同源），
  **不重写 `workbench.html` 的 JS 逻辑**。
- **R6** 纯算数请求（合并 / NMA / 敏感性分析）**零 CCM**，保住「描述即执行」卖点。

### Changed — A2「沉默漏检」判据改为保守版（避免天天误报）

- 不再拿「可调度的全部源」（`fetch_coze_unified._SOURCE_DISPLAY`，6 个）当期望——会话并未记录本次
  实际请求了哪些源，那样必然误报。改为：`search_status ≠ ok` / `by_source` 为空 / `total == 0` /
  **仅 1 个库返回** 四条硬判，外加调用方显式给 `--expected-sources a,b` 时才做缺库差集。

### Changed — `adapters/workbench/form_schema.py`（纯增量）

- 新增 `TITLE_EN`（12 节点英文标题）+ `title_for(stage_id, lang)`。原有 `title` / `SCHEMA` / `schema_for`
  行为**逐字节不变**，工作台零影响；自检通过。

### Added — `tests/test_flow_menu.py`（149 断言，0 失败）

覆盖：AC-A1（A4 无 skip + 状态机拒 skipped）· AC-A2（软停含 skip）· AC-A3（A3 无逐条入口）·
AC-A4（EDITABLE_KEYS 派生，D16 显式标注）· AC-A6（`/源` 标注）· AC-A7（沉默漏检且不误报）·
AC-A9（12 节点 × zh/en 无缺键）· R1 只读（字节级）· R2 确定性 · R3 选项派生 + 编号连续 ·
R5 回退候选集 · `expected_sources` 与 ct-literature 同步 · CLI 端到端 dry-run。

### 文档

- **新增** `references/conversation_flow_menu.md`（规范 v1.0：六条硬约束 / 状态真源映射 / 逐节点菜单 /
  CLI / 全局指令 / 验收证据 / 不适用边界 / 未决项）。
- `SKILL.md` §2.4 的 CCM 条目由「designed, NOT implemented」改为「implemented」并挂上命令与规范；
  新增触发词「上下文菜单 / 对话菜单 / 全流程菜单 / flow menu」；版本 2.10.0 → 2.11.0。
- `references/design/ccm/README.md` 状态改为「设计完成 · 已实现」，并记录 **3 处实现偏差**
  （未加 `form_schema.menu_for()`、`pending_actions` 闸态仍未加、漏检判据改保守版）。

### 未决 / 已知接受项

- **D16**（A2 改检索式语义）**D10**（A4 对话内收文件）**D11**（A2 前置下载）**D14**（A1 探针展示）仍待定，
  菜单已按建议实现但语义未闭合。
- R 路径硬编码 `C:/Tools/R-4.6.1`（`coze_client.py:1414`）→ `tests/test_a4_b1_handoff.py` 4 项 FAIL 为既有环境问题，非本轮回归。

---

## [2.10.0] — 2026-09-10 — A 阶段契约重构：类型降为人工确认字段，A3 纯文件交接，A4 按清单直下

> **一句话**：把「文献类型」从**判定门**降为**人工确认的一等字段**。判定权唯一归属 = A3 裁决表；A4 只读。
> 同时修掉三类**静默失效**（接口不报错、只是安静地少做事）：写死解释器路径、元组解包元数不对称、缺 PyMuPDF。
> **交接文档 → `references/HANDOFF_2026-09-10.md`**（含环境事实、待决策点、验证方式、陷阱清单）

### Changed — 文献类型：判定门 → 人工确认字段（规则闭环）

- **全链路不再做类型判断（用户裁定，2026-09-10）**：**人工确认文献类型后，任何一层都不再判类型；要改类型必须人工确认或人工发起。**
  - `pdf_extractor.extract()`：**删除规律 R1 短路返回**（原 review/guideline/protocol → 直接 `return excluded=True`）。`classify_pdf` 保留但仅作标注，且调用包进 `try/except`（探测失败降级 `unknown`，绝不阻断抽取）。
  - `extract()` 返回 `review_summary` 增 `excluded`（**恒 False**）/ `doc_type` / `signals` / **`type_notice`**（给闸位人读的提示文案）。
  - `block_a._a4_extract_pdf`：`doc_info["excluded"]` 恒 False，`type_notice` 透传。
  - 上传快速通道（`a4_seed_from_pdfs`）：删 `if doc_info.get("excluded")` 分支 → 一律 `extracted`。
  - `a4_stream` 缓存分支：删 `doc_info.excluded` 判断 + 删已成死分支的 `elif status == "excluded_review"`。
  - 结果：A4 **100% 按 A3 清单下载与抽取**，不存在 `excluded_review` 状态。

- **D17-A：文献类型成为 A3 裁决表的一等字段**
  - 类型词表 `original | review | guideline | protocol | unknown` 两个技能本就同源；预填**直接复用 `ct-literature doc_type_filter.classify_record()`**，**不在本技能内写第二套判定**。
  - 新增 `block_a.rule_doc_type()`（规则预填）与 `_read_doc_type()`（A4 只读唯一入口）。
  - 导出表新增「文献类型确认」列（规则已预填，下拉可选）；回传读取 + 校验 + 落审计字段：
    - 单元格非空 → 权威值，`doc_type_source="human"`；与预填不同 → 记 `doc_type_changed` + 留 `doc_type_rule` 对照（**「改判几篇」可审计**）
    - 留空 → 未确认，沿用规则预填，`doc_type_source="rule"`（不拦流程，计数可见）
    - 取值非法 → **报错不前进**，并指出具体哪一行
  - A4 侧：抽取层探测降为 `doc_type_detected`，**仅在与确认值不一致时**提示人工；`review_note` 由确认值驱动。工作台 A4 文案改为「类型只读 A3，要改请回 ③」。
  - **保留的两处类型判断均不越界**：A3 `is_likely_review()` review-guard（人工确认**之前**的预填建议，可改）；`review_note` / 工作台 `🔍 疑似综述` 徽标（**纯提示**，不做排除）。

### Changed — A3 = 纯文件交接

- A3 不再在对话/界面内逐条裁决：**导出裁决表 → 人工改 → 回传 → 校验 → 直接接 A4**。接线复用既有的 `export_screening_xlsx()` / `parse_screening_xlsx()`（`block_a.py`），**双端（工作台 + 对话）走同一套函数，漂移风险归零**。
- 回传校验失败一律不前进：列完整 / 行可对齐 / `decision` 合法 / `exclude` 必填 `reason` / 不允许新增行 / **零匹配拦截**。

### Fixed — 三类静默失效

- **A1/A2 解释器路径写死（P0，静默失效）**：`tool_mapping_meta.json` 两条 `cmd[0]` 写死 `C:/Anaconda3/python.exe`（本机不存在，实际为 `C:/Tools/Anaconda3/python.exe`）。`_load_tool_mapping()` 只展开 `skill_dir`、不碰 `cmd` → 每次 `FileNotFoundError` → 被 `except Exception` 吞掉 → `status:error` → 兜底读空目录 → **A2 静默返回 0 篇、A1 注册库探针静默无返回**（界面只显示「合并总数 0」或「探针无返回」，不报错）。
  修法：`cmd[0]` 改为占位符 `{python}`；新增 `coze_client.resolve_python_exe()` 运行时解算（环境变量 → Anaconda base 候选 → `sys.executable` → PATH，**只认实际存在的文件**）。这样 `cmd[0]` 从「硬编码环境事实」降级为「兜底默认值」，换机不再复现。

- **A4 下载路径元组解包元数不对称（静默失效）**：`_a4_extract_pdf` 自 v0.3 起返回 **6 元组**（末位新增 `doc_info`），三个调用点中**只有下载路径（`_a4_fetch_one`）仍按 5 元组解包** → 每次「下载成功 → 抽取」抛 `ValueError: too many values to unpack (expected 5, got 6)`，被 `a4_stream` 的 `except` 兜成 `gate=worker_error` / `status=needs_upload`。
  **症状极具迷惑性**：首轮全篇显示「待补传 PDF」，**重跑却正常**（PDF 已落盘 → 走缓存分支，那条是 6 元组）→ 易误判为 OA 覆盖不足。

- **缺失 PyMuPDF 致 A4 抽取不可用**：`fitz` / `pymupdf` 均缺失（仅 `pdfplumber` 在）→ `classify_pdf`（`:142`）与 `parse_pdf`（`:218`）硬依赖 `fitz`。已安装（见下方「环境」）。

- **G：裁决表 Works 表无 DOI 列**：`_WORKS_COLS` 11 列不含 DOI，而导出侧按 DOI 建键、回传侧只能给出标题键——当时能对上只因 `_match_keys` 生成多键且在含 DOI 的基线 decisions 上匹配，属**巧合容错**。一旦两端标题归一化口径分叉，匹配会**静默降为 0 且不报错**。修法：`_WORKS_COLS` **补 DOI 列**（回传匹配键显式化）+ 零匹配拦截。

### Added

- **`ct-literature/scripts/export_xlsx.py` 通用附加决策列能力 `decision_extra`**（e.g. meta 的「文献类型确认」列）：**不传该参数时行为与旧版逐字节一致**（实测无附加列表头仍以「理由」结尾）——不把 meta 的需求硬编码进 ct-literature。
- **`tests/test_a3_doc_type_confirm.py`**：A3 类型确认链路回归测试（临时冒烟固化为技能资产）。覆盖 4 类预填 → 导出预填 → 改判/留空 → 非法值拦截 → A4 只读 + 不一致提示 → 导出器向后兼容。
- **`references/HANDOFF_2026-09-10.md`**：交接文档（改动清单、环境事实、静默失效模式、待决策点、验证方式、陷阱清单）。
- **`references/design/ccm/`**：对话上下文菜单（CCM）设计归档（v0.1–v1.0 + README 索引）。**设计完成、代码未实现。**

### Environment

- **PyMuPDF 1.28.2 已装，但在 user site**：base 的 `site-packages` 对本机普通用户**只读**（`BUILTIN\Users: ReadAndExecute`）→ 必须 `pip install --user`，落点 `C:\Users\Wintone\AppData\Roaming\Python\Python314\site-packages`（**不在 PATH，换机部署需重新确认**）。wheel 文件名**不可重命名**（否则 `Invalid wheel filename (wrong number of parts)`）。
- **R 解释器路径为已知接受项（用户明确决定跳过，勿误判为回归）**：`coze_client.py:1414` 写死 `C:/Tools/R-4.6.1/bin/Rscript.exe`，本机不存在（实际 `C:/Program Files/R/R-4.2.2/bin/Rscript.exe`，且已在 PATH）→ B1 `k=0` / `TE=None`。`tests/test_a4_b1_handoff.py` 的 4 个 FAIL 均由此项所致。

### Verification

| 检查 | 结果 |
|---|---|
| `tests/test_a3_doc_type_confirm.py` | **28 PASS / 0 FAIL** |
| `tests/test_a4_b1_handoff.py` | 7 PASS / 4 FAIL（FAIL 全为 R 路径已知项，与改动前逐条一致） |
| A2 端到端（修复后） | `ct-literature --help` / `ct-registry --help` 双双 **rc=0**；`a2_build_tool_card` → `execute_tool_cards` `status=ok`，`_read_literature_dir` 取回 **20 篇真实文献** |
| A4 综述篇目 | 旧逻辑必拦 → 现 `gate=pass_downloaded`，PDF 落盘、`event=extracted` |
| `extract()` 类型短路（哨兵法） | 类型=review 仍走到 `parse_pdf`；`classify_pdf` 抛缺 `fitz` 异常不阻断 |
| 合成 PDF 真实抽取 | `doc_type=original` / `excluded=False` / `A4 rows=1` |
| `grep excluded_review\|type_screen_page\|_skip_page_screen`（`.py`） | **无代码级残留**（仅注释） |

### Notes — 陷阱与教训（详见 HANDOFF §7）

- **A2 `--max` 是每源上限，非合并上限**（`--max 5` × 4 源 = 20 篇）——菜单文案须写「5/源（合并 20）」。
- **`_read_literature_dir` 是主路径而非兜底**：stdout 只吐 NDJSON 日志，数据全在 `.merged.json`，`_extract_studies` **恒为 0**。注释曾写「回退读取」，是维护陷阱。
- **改了返回契约（元组加长、字段新增）后，必须 `grep` 全部调用点逐一核对解包元数**——`_a4_extract_pdf` 三处调用点改了两处，漏的那处恰在关键路径上。

---

## [2.9.19] — 2026-09-09 — 开发期结束，恢复生产态双站点路由

### Changed
- **开发期策略解除（2026-09-09 用户指令）**：`adapters/DEV_POLICY.json` 停用（改名归档），路由回切生产态——ct-meta 主站 / ct-meta2 回退；`publish_freeze` 解除，技能发布不再被冻结（SKILL.md §8.5 的 publish_guard 前置检查保留，退出码 0=放行）。SKILL.md §3 启动段与 §6 出站披露文案同步更新。ct-meta2 仍为旧引擎（缺 NMA 修复与 engine_version 指纹），待下次部署同步。

## [2.9.18] — Unreleased — NMA 空 plots 默认出图修复

### Added
- **引擎指纹 `engine_version`（run_task.R）**：响应 JSON 统一注入 `.MA_ENGINE_VERSION`（当前 2.9.18），ok/error 分支均覆盖。部署生效判定从"输出特征考古"变为一次字段比对：本地 HEAD 探针 vs 云端响应 `engine_version` 不一致 = 部署未生效。

### Fixed
- **`adapters/coze/src/r_engine/run_task.R` NMA 分支**：`figure.plots` 为空时 NMA 静默零图（stats 照常返回、status=ok），呈"分析成功但无图"的隐蔽体验。根因：NMA 分支仅认显式 plots 点名，而 nma_rank 已有空 plots 默认（sucra），设计不对称。修复：netgraph/netleague 渲染条件补 `|| (task == "nma" && length(plots) == 0)`；顺手将 netgraph 裸 `.render_fig` 收敛为 `.safe_fig`（渲染抛错不再中断整次分析）。
- **`adapters/rendering.py` 呈现层两处 NMA 缺口**：① `render_html_report` 从不消费 `stats.extra.league_table`（netleague 按设计是表格型输出非 SVG figure）→ R 端算了表格也静默丢弃；现补渲染为等宽 `<pre>` 保真卡片（标题复用 `fig_netleague` 中文名"网络证据表"）。② `_render_hero` 对 NMA 的多对比向量型 `pooled.estimate` 强行标量格式化 → TypeError，**此前 NMA 的 HTML 报告渲染即崩**；现向量型跳过 hero 卡（无单一合并效应量，各对比估计由 stats 分组区完整呈现）。
- **NMA `stats.pooled` 结构修正（R 端 + 呈现层配套）**：R 端原 `as.numeric(TE.random)` 把 n×n 反对称矩阵（含对角 0）摊成 n² 个无标签值（4 臂即 16 个数）；现按上三角展开为真实对比（4 臂 6 个），矩阵方向已实证（`TE.random[i,j]` = 行治疗 vs 列治疗），并新增 `pooled.comparisons` 标签字段。呈现层新增 `_render_pooled_card()`：向量型 pooled 渲染为「对比 | 效应量（unit）[95% CI]」结构化小表（旧镜像无 comparisons 时退化为索引行标），标量型走原通用渲染。
- **league_table 折行修复（R 端自建文本）**：旧实现 `capture.output(print(netleague(fit)))` 受 print.league 内置分块宽度（`nchar.trts`，默认 66 字符）约束——干预数多时每块仅容纳 2~3 列，第 4+ 个干预被整块折到表外、列头丢失，一个 league 表断成数截；`capture.output(width=)` 与 `nchar.trts=` 均无法从外部解除分块。现弃 print 路径，从 netleague 对象的 data.frame 矩阵（`lg$common`/`lg$random`：下三角 network 估计、上三角直接比较）自建等宽对齐文本（common + random 两块 + 标准方向尾注），单表完整永不折行；对角线渲染为 "."（干预名已在行首与列头，双重冗余）。注意：`formatC` 向量 width 在 R 4.6.1 抛 "condition has length > 1"，pad 已改逐元素实现。
- **`adapters/rendering.py` extra 卡去重**：`_render_stats_groups` 原把 `stats.extra`（含 league_table 多行文本）经 `_kv_rows` 平铺成无格式单行、且与"网络证据表"图卡重复；现 extra 卡剔除 `league_table` 键（已由图卡区等宽 `<pre>` 保真呈现），extra 其余字段（rank/pscore 等）照常。
- **league 表列对齐 + 合并效应卡数值右对齐（呈现细节，2.9.18 追加）**：① `.league_block` body 行宽度向量误传 `c(rw, cw)`（n+1 个宽对 n 个元素）→ 矩阵第 1 列错拿行名宽，对角 "." 不被 pad（首行偏短）；改传 `cw`，各数据行宽与列头行严格一致。② `_render_pooled_card` 效应量列改 `text-align:right` + 表级 `font-variant-numeric:tabular-nums`（等宽数字），数值列纵向对齐更易读。

### 验证
本地镜像三组回归：① nma 空 plots → netgraph SVG（10719 字符）+ `stats.extra.league_table` 有值；② nma 显式 plots → 行为不变；③ nma_rank 空 plots → 仅 sucra+rank，无回归。端到端渲染验证：含 league_table 的 NMA 结果经 `render_html_report` 产出 HTML，netgraph 图卡（1 个 SVG）与"网络证据表"卡片同卡正确。待人工打包部署后做端到端线上回归。

---

## [2.9.17] — Unreleased — 选题 Quick 卡融合"实时真实缺口证据"

> **目标**：修复 Quick 选题卡丢失"真实缺口"依据的回退——新版 Quick 卡仅给四维评分、缺了旧版"Cochrane N / PubMed N + 约宽泛方向 1/N → 真实缺口"的实时证据层。将两套输出融合进同一张卡，让"新颖性"评分始终有实时命中间据支撑（R7 落地）。

### Added
- **`scripts/generate_topic_report.py` 新增缺口渲染**：`GAP_ZH` 映射 + `_ratio_str()`（窄/宽命中数比 → `1/N` 或 `Nx`）+ `_gap_section()`，并并入 `build_quick_card()`。Quick 卡现在在结论行下渲染"## 真实缺口证据（实时探针）"块：Cochrane(CDSR) N / PubMed SR/MA(近5年) N / 对比宽泛父方向比 / 缺口判定（✅真实缺口 / 🔴已饱和 / ⚠️需谨慎）。
- **优雅降级**：`gap.verdict="unverified"` 或探针不可用时显示"⚠️ 探针不可用，缺口未验证；Full 评估将重跑"；`gap` 字段缺失时提示 Full 阶段补探针。**禁止用模板数字硬填**（沿用技能 `any_error→unverified` 模式）。
- **`adapters/build_gap_probe.py` 一键缺口探针**：封装 `literature_probe.py` 的窄方向(Cochrane+PubMed)+宽泛父方向(PubMed)双探针，按上述阈值判定 `real_gap`/`saturated`/`caution`/`unverified`，产出严格对齐报告 `gap` 字段；支持 `--out gap.json` 单独输出或 `--merge-into input.json` 一键合并进选题 input 直接喂给 `generate_topic_report.py`（已真实联网验证：PD-1 NSCLC 二线 vs NSCLC 免疫治疗 → Cochrane 36 / PubMed 6978 vs 15298 → ratio 0.46 → saturated）。

### Changed
- **`references/topic-selection.md`**：① Quick 双路径入口 Output 列补"live real-gap evidence"；② 新增"Quick 卡必须携带真实缺口证据"硬规则——Quick 路径须实时跑 `literature_probe.py` 两次（窄方向 + 宽泛父方向），取 `cochrane.hit_count`/`pubmed_meta.hit_count`，算 `ratio=窄.PubMed/宽.PubMed` 落到 `gap`；③ Output contract JSON 增 `gap` 字段（narrow/broad/ratio/verdict/label/summary）；④ 新增缺口判定阈值（ratio<0.3 且 Cochrane<10→real_gap；ratio≥0.5 或 Cochrane≥20→saturated；其间→caution），并与四维"新颖性"互校（新颖性 4–5 但缺口 saturated → 触发 R3 复核）。
- **`references/interactive_menu.md` 示例 6**：候选方向①补一行"真实缺口证据（实时探针）：Cochrane 1 / PubMed 38；约为宽泛方向 1/11 → ✅ 真实缺口"，演示融合卡实际长相。

### 验证
- 样例 `sample_quick_card.json` 经 `generate_topic_report.py` 渲染 md/html，四维评分 + 缺口块同卡正确输出；`_gap_section` 三分支（real_gap / saturated / unverified / missing）均通过。

---

## [2.9.16] — Unreleased — pdf_fetch 多通道回退上移 coze + workbench A4 批量匹配

- **workbench「数据提取核验（🔴 红线）」新增「📤 批量上传并匹配文献」**（实测反馈）：A4 面板 actions 首位新增按钮 + 折叠面板——上传 `.txt/.csv/.xlsx` 或粘贴 **DOI / PMID / 标题** 清单 → 新端点 `/api/a4_batch_match`（Europe PMC core 逐条解析；DOI/PMID 精确、标题先短语后 token-AND 近似并标 `fuzzy` 提示人工确认；去重 DOI 归一键；标注是否已在 A4 per_doc）→ 勾选后 `/api/a4_batch_add` 幂等追加为 `status=needs_upload` 待补篇（复用「补传 PDF → 抽取」通路）。纯元数据匹配，不下载正文。前端 `toggleA4Match / a4BatchMatch / a4BatchAdd`；实测 DOI/PMID/标题三类输入均命中。
- **架构（与 ct-literature v0.9.7 同规）**：`adapters/pdf_fetch.py` 的多通道/预印本回退算法一律上移 coze `publisher_pdf` 服务端（补充链 = Unpaywall → PPR bioRxiv/medRxiv → arXiv，作者级同篇校验，2026-09-06 起服务端实现）。本地 `fetch_pdf` 主路径改为：① 委托 coze（服务端含 A 路径 + 补充链）；② coze 不可用时仅本地直下降级（open_access_url / Unpaywall / PMC）；③ 本地 `_try_preprint_fallback`（PPR/arXiv）停用（保留为历史参考），不再本地实现预印本检索下载、不再为回退预取 title/authors（省 Crossref 反查）。CLI `--with-*` 开关兼容保留（自动由服务端生效）；docstring/usage 同步。

---

## [2.9.15] — 2026-09-06 — C3 真实 API 参考文献核验 + A1 选题报告可行性信号

> **目标**：C3 参考完整性核验从纯结构检查升级为真实 API 核验（CrossRef + PubMed E-utilities），防 AI 虚构/拼接参考文献（JAMA 2026-08 红线）；A1 选题报告补可行性信号（拥挤度 / 预期研究数 / 方向稀缺度）。

### Added
- **新 `adapters/ref_verify.py`**：CrossRef (`api.crossref.org/works/<DOI>`) + PubMed (`esummary.fcgi?id=<PMID>`) 双库真实核验。单条 `verify_reference()` 含双侧 DOI+PMID 交叉验证（PubMed 传回的 DOI 与传入 DOI 核对 → 防拼接幻觉）；批量 `verify_references()` 自动去重 + polite delay。撤稿文献（CrossRef type=retraction / PubMed pubtype 含 retraction）自动标 critical；作者不一致、DOI 不匹配均标 mismatch。零第三方依赖（纯 urllib + json），网络失败 status="error" 不阻塞。
- **增强 `c3_reference_verify`（block_c）**：接入 `verify_references`，每条参考真实查 CrossRef/PubMed；n_retracted / n_not_found / n_mismatch 计数 + 详细 issue 列表；撤稿/虚构/拼接任一标 critical → C3 reference_verification 红线闸阻断。

### Changed
- **增强 `a1_topic_selection`（block_a）**：报告新增 `feasibility` 结构（crowding / expected_studies / risk_alert）；拥挤度分 4 档（empty/low/moderate/high），来自 ct-registry 注册数推断；空/低方向自动给风险提示（meta 需 k≥2）；文本报告同步追加 📊 拥挤度行与 ⚠️ 风险行。

### 验证
- py_compile 全绿；合成 mock 测试 9 项全过（OK / not_found / retracted / mismatch / error / batch / c3 集成 / A1 拥挤 / A1 空方向）。

---

## [2.9.14] — 2026-09-05 — A4 逐篇剔除（不进合并）+ 抽取行治理

> **目标**：数据提取核验（A4 红线）界面允许把误纳入的文献剔除（如 review 漏网 / 抽取错源），被剔除篇的抽取行不进 Block B 合并；同时治理"综述正文被当原始研究抽取"。
> 退出标准：① per_doc 有 included 开关，剔除后卡片置灰可恢复；② approve 时剔除篇行不进 handoff.studies_for_b；③ 叙述性抽取行（他引转述）不再自动进 extracted_rows。✅ 全达成（E2E 双向实测）。

### Added
- **A4 逐篇剔除/恢复**：`per_doc[i]` 新增 `included=True`（block_a a4_stream）；`server.py` 新增 `POST /api/a4_set_doc_included`（就地更新 included + excluded_reason，重算 n_extracted/n_included_docs/n_excluded_docs）；前端每篇卡片操作区加「✕ 剔除本篇（不进合并）/ ↩ 恢复纳入」，剔除篇整卡置灰 + excl pill + 说明条（`.a4doc-excluded` 等样式）。
- **A4 approve 携带剔除态**：前端 `approveA4()` 在放行前把各 included 篇的抽取行汇总为 `revision.extracted_rows`（被剔除篇行排除）、剔除清单入 `revision.excluded` 再提交；`fullflow._extraction_input` 改用 `latest_revision`（不限 action，approved 携带 revision 亦被采用），使放行不重抽、剔除真正生效。

### Changed
- **抽取行治理（block_a a4_stream）**：`extracted_rows` 从"仅 2×2"扩为"2×2 + 来自表格模板的效应量行"（te/sete 齐全且 anchor 含 `table#`，转 TE/seTE 大写供 Block B）；叙述性行（anchor 含 `text:`，多为综述正文对他引结果的转述）**不再自动进 extracted_rows**——根治"综述抽出一堆错源效应量"。

### 诊断结论（10.3945/an.111.000893 = Adv Nutr 2012 REVIEW）
- 该 PDF 首页 RUNNING HEAD 即 "REVIEW"，Europe PMC pubType 含 `Review`/`review-article`（B1 硬信号应命中），但 ff-3770 会话中该记录来自 OpenAlex（type=article、无 abstract、pub_types 未透传）→ review-guard 三道全漏 → 进 A4。属 **ct-literature 合并归一化未透传 pub_types** — **已修复（ct-literature v0.9.6+ 见 CHANGELOG (6)）**：`fetch_europepmc._extract` 现保存 `pub_types`，`fetch_openalex._extract` 从 `type` 派生，`normalize.merge` 做 union-dedup 合并。
- 抽取 5 行全为 narrative 行（"HR (p3)"/"RR (p3)"/"farction" 等错 study 名）→ 现已被"叙述行不收"规则排除；用户在 A4 界面可进一步用「剔除」显式标出。

### 验证
- py_compile + node --check 通过；`/api/a4_set_doc_included` HTTP 实测 200（剔除持久化 + 计数 1/19）；函数级 E2E：剔除该篇 → handoff.studies_for_b=0，全保留 → =5。

---

## [2.9.13] — 2026-09-05 — 工作台 UI 视觉升级（对齐 ct-base workbench_ui 规范）

> **目标**：工作台"太简单不够美观"——按 ct-base `references/workbench_ui.md` 的视觉规范做纯 CSS 层升级，不动 JS 逻辑/类名/DOM 结构。
> 退出标准：① 深色品牌渐变顶栏 + 反色控件；② 卡片阴影层次 + 列表斑马纹 + 状态 pill 边框化；③ logo 换技能 icon 色系 SVG（禁 emoji 当图标）；④ JS 语法与 HTTP 渲染验证通过。✅ 达成。

### Changed
- **`workbench.html` 追加 ct-base 视觉层**：`--wb-*` 设计令牌（brand clinical-indigo 系）、深色渐变顶栏（`--wb-topbar-bg` + `--wb-on-topbar` 反色）、卡片圆角/阴影层次、表格斑马纹 + hover、按钮渐变主色 + hover 亮度、pill 边框化、JSON/代码块统一浅底、细窄滚动条。
- **header logo**：`🧬` emoji → 内联 SVG（技能 icon.svg 紫系同心圆 + 聚合菱形，34px），对齐 ct-base §5.2 logo 规范。
- **装饰性 emoji 清理**：logbar 标题 `🗂` 移除（ct-base §4.4 禁 emoji 当图标）。
- 业务文案内功能性指示符（✅ 状态徽标 / ⬇ 上传 / 🔗 DOI 等）保留——由 JS 模板生成，全量 SVG 化留作后续（避免大面积模板改动风险）。

### 验证
- `node --check` 抽取内联 JS 通过；HTTP GET / 返回 200 且含 `wb-brand`/`--wb-topbar-bg`/`--wb-row-alt` 等新标记；server 已重启载入。

---

## [2.9.17] — 2026-09-17 — 回退/提交报错可诊断化（前端错误透传 + 渲染容错）

> **目标**：用户反馈"回退按钮选了目标后报错"。经排查，当前源码下 rewind→decide 全链路 422/报错均不可复现：① `DecideReq.stage_id` 已于 2.9.12 改为 `Optional[str]`（handoff_confirm 的 null stage_id 不再 422）；② 前端 `decide()` 所有调用点均传字符串 action、`STATE.session.path` 恒由 `build_state` 注入，故 `decide_stream` 在源码层面不可能 422（已用 TestClient 端到端复现 rewind→decide 两次均 200 证实）；③ `schema_for()` 对任意未知 stage_id 回退通用 schema，不会返回 null。本版本不修"假想 422"，而是修复"报错无信息"——让真实错误（含字段级校验 detail）与渲染异常透传到界面，使残留问题可定位。
> 退出标准：① 任何非 200 响应（422/400/500）在前端显示 FastAPI `detail` 而非裸状态码；② `render()` 异常不再静默黑屏，显式提示 + 堆栈。

### Fixed
- **前端错误透传（关键）**：`workbench.html streamPost()` 原在非 200 时仅抛 `"422 Unprocessable Entity"`，丢弃 FastAPI 的 `detail`（含 pydantic 字段级校验错误）。新增 `_extractDetail()`：`!r.ok` 时读取响应体、提取 `detail`（字符串或 422 数组逐条展开），错误信息由"处理响应失败：422"升级为可读的字段级原因。同步收敛 `rejectAndRewind()` 与快速通道 `start_data` 的 `!r.ok` 处理到同一 `_extractDetail()`。
- **渲染容错**：`render()` 外包 try/catch（实现体移入 `_renderInner()`）。此前任一渲染异常会静默黑屏、表现为"页面报错且无信息"；现显式提示"渲染失败：<msg>"并附堆栈到后台输出，便于定位回退/提交后渲染问题。

### Verification
- `adapters/tests/test_phase2_rewind_revise.py` 9/9 PASS；新增 `adapters/tests/_repro_rewind_full.py`：从"已推进到 B"的会话回退到 A2 / A1，再 `POST /api/decide`，两次均 200、无 422。
- `node --check` 校验 workbench.html 两个 `<script>` 块语法通过。

---

## [2.9.12] — 2026-09-05 — 修复回退/交接闸 422 + A1 纳入综述开关 + PDF 入口分类模板

> **目标**：① 修复工作台「打回/回退」与块间交接（handoff_confirm）批准失效；② A1 选题页可直接决定"检索是否纳入综述"；③ 沉淀 PDF 下载入口分门别类模板。
> 退出标准：① handoff approve 不再 422、rewind 全链路 200；② A1 revision.include_reviews 覆盖 cfg 传入 A2（端到端实测 true 生效）；③ 模板覆盖 5 类框架且有代码/实测证据。

### Fixed
- **handoff_confirm 交接点 approve 422**：`server.py DecideReq.stage_id` 原为必填 `str`，而块间交接 await 的 `stage_id` 为 `null` → pydantic 422 → 交接点永远无法批准（表现为"回退后流程卡死/回退不起作用"）。改为 `Optional[str] = None`（后端 `_validate_decision` 对 handoff_confirm 本就不校验 stage_id）。
- **rewind 请求路径**：`workbench.html rejectAndRewind()` 用裸 `fetch("/api/rewind")`，未走 `apiUrl()` → file:// 打开工作台时必然失败。改用 `apiUrl("/api/rewind")`（与其余 API 调用一致）。

### Added
- **A1「是否纳入综述类文献（检索范围）」开关**：`form_schema.py` A1 新增 `kind=bool` 可编辑面板（revision_key=include_reviews）；`fullflow.py` `EDITABLE_KEYS["A1.topic_selection"]` 增 `include_reviews`、新增 `FullflowSession.latest_revision()`（读不限 action 的最新 revision）、`_run_block` A 分支用 A1 revision 的 include_reviews 覆盖 cfg；`block_a.run_block_a` 把 include_reviews 写入 A1 stage_result 作初值；前端 `renderPanel` 支持 `kind=bool`、`collectDraft` 支持独立 checkbox（整键存 true/false）。端到端实测：A1 approve + `revision.include_reviews=true` → A2 检索卡片收到 `"include_reviews": true`。
- **PDF 下载入口分类模板**：`references/pdf-download-portals.md` —— A 聚合 API（Unpaywall/Europe PMC core/OpenAlex）、B OA 仓储模板（PMC `/pdf/`、预印本 `.full.pdf`、MDPI `/pdf?version=`，后二者命中用户实例并有代码/检索数据佐证）、C 出版商文章页 DOM（pdf_cf_guard 规则）、D 签名直链（SD X-Amz 书签 + CDP 边界，2026-09-05 实测结论）、E 付费墙人工上传；附决策速查表。`SKILL.md` 边界段补引用。

### Changed
- 工作台 server 已重启载入修复（端口 8765）。

---

## [2.9.11] — 2026-09-05 — A4 下载文档列表不展示已排除篇目

> **目标**：A3 筛选裁决「排除」（review-guard / 相关性门控，status=skip）的文献不进 A4 下载文档列表，只保留需要下载/已下载/待上传的篇目，消除"已排除还显示在下载清单"的困惑。
> 退出标准：① 实时进度面板 skip 事件不上屏；② 逐篇文档展示过滤 status=skip；③ 过滤后 doc_index 仍按 per_doc 原始位置定位（后端不感知）。✅ 全部达成（JS 语法校验通过）。

### Changed
- **workbench.html `renderA4Documents()`**：`per_doc` 先过滤 `status !== "skip"`；展示编号与所有后端定位（doc_index / pdf_page / a4SaveDoc / a4ViewPage / 上传指派）改用 `d.index`（per_doc 原始位置），避免过滤后 map 位置与原始位置错位；空态区分"筛选后无需要下载" vs "尚无结果"。
- **workbench.html `renderA4Live()`（续跑实时进度）**：`skip` / `relevance_skip` 事件直接 return，不建行。
- **workbench.html `doA4Preview.addRow()`（A4 预览实时进度）**：同上，skip 事件不上屏。
- **deferred（配额延后）保留展示**：语义为"本轮配额未轮到、仍需下载"，与 skip（明确不下载）区分。

---

## [2.9.10] — 2026-09-05 — A2 源头排除综述：节省检索配额 + 避免 10.3390/ijms27114705 类困惑

> **目标**：默认从检索源头排除综述类文献（Review / Systematic Review / Meta-Analysis），节省检索配额，避免用户困惑（如 10.3390/ijms27114705 在 A3 被标记 review 但仍占用 A2 配额）。
> 退出标准：① Europe PMC / OpenAlex 双源头加 NOT review 过滤；② meta-analysis 默认 include_reviews=False；③ 前端加"包含综述"开关；④ 伞评/范围综述场景可显式开启。✅ 全部达成（代码级验证）。

### Added
- **Europe PMC 源头排除综述**：`fetch_europepmc.py` 新增 `include_reviews=True` 参数；`False` 时追加 `AND NOT (PUBLICATION_TYPE:"Review" OR PUBLICATION_TYPE:"Systematic Review" OR PUBLICATION_TYPE:"Meta-Analysis")` 过滤串；CLI 暴露 `--include-reviews/--no-include-reviews`（argparse.BooleanOptionalAction）。
- **OpenAlex 源头排除综述**：`fetch_openalex.py` 新增 `include_reviews=True` 参数；`False` 且无指定 `review_type` 时追加 `type:article` 过滤（拦截 `type:review` 条目）；CLI 同上。
- **编排层透传**：`ct_literature.run()` 新增 `include_reviews=True`，透传给两个 fetcher。
- **block_a A2 默认排除综述**：`a2_build_tool_card()` / `a2_literature_search()` / `run_block_a()` 新增 `include_reviews=False`（默认源头排除综述）；`tool_mapping_meta.json` 的 ct-literature arg_map 新增 `include_reviews` → `--include-reviews`。
- **coze_client 布尔参数透传**：`execute_tool_cards` 的 arg_map 循环识别 `include_*` / `exclude_*` 命名风格的 bool 参数，自动转为 `--no-*` 标志（BooleanOptionalAction 语义）。
- **前端开关**：`workbench.html` 启动表单新增"包含综述类文献"复选框（默认不勾选），`doStart()` 读取后写入 `opt.include_reviews`。
- **server / fullflow 透传**：`StartReq` 新增 `include_reviews: bool = False`；`api_start_stream._call` 透传给 `run_fullflow`；`run_fullflow` 写入 `cfg`；`fullflow._run_block` 透传给 `block_a.run_block_a`。

### Verified
- 编译验证：`py_compile` 全部 7 个修改文件通过。
- 语义验证：Europe PMC 过滤串语法对齐官方 search grammar（PUBLICATION_TYPE 为索引字段）；OpenAlex `type:article` 与既有 `_openalex_type_for()` 不冲突（仅在 `review_type="all"` 且 `include_reviews=False` 时生效）。

---

## [2.9.9] — 2026-09-03 — A4 续跑优化 + 逐篇下载实时进度 + 修复发起流程 TypeError（发布就绪）

> **目标**：① A3 批准后只跑 A4（不再整块重跑 A1→A4）；② A4 下载/抽取逐篇实时上屏；③ 修复 `api_start_stream` / `api_decide_stream` 因 `_call` 闭包未接收 `on_a4_event` 导致的 TypeError。
> 退出标准：A3 批准仅跑 A4（a1/a2/a3 调用计数 0）；A4 逐篇 `a4` 事件实时流出（生产实测 100s 内 31 条）；发起/决策流程零 TypeError。✅ 全部达成（生产环境端到端实测 + 单元验证）。

### Added
- **A4 续跑（A3 批准后只跑 A4）**：`fullflow._run_block` A3 已批准且无 A2/A3 修订时设 `start_stage='A4'` 并传 `cached_envelope`（含已算好的 A1/A2/A3）；`block_a.run_block_a` 新增 `start_stage`/`cached_envelope`，命中则 `a4_only=True`，复用缓存 `studies/screened`，跳过 A1/A2/A3 重算（实测调用计数 a1:a2:a3 = 0:0:0，原整块重跑约 7 分钟）。
- **A4 逐篇实时进度**：`block_a.a4_auto_fetch_and_extract` / `a4_data_extraction` 透传 `on_a4_event` 回调；`server._stream_blocking` 新增 `_make_on_a4()` 把逐篇事件推成 SSE `a4`；前端 `decide` SSE 处理新增 `a4` 分支 → `renderA4Live(ev.a4)` 逐篇进度面板（标题/状态徽章/原因即时刷新）+ `.a4live*` 样式。

### Fixed
- **发起/决策流程 TypeError（2026-09-03）**：`_stream_blocking` 向 `call(...)` 同时传 `on_line` 与 `on_a4_event`，但 `api_start_stream._call` / `api_decide_stream._call` 仅声明 `on_line=None`、不收 `on_a4_event` → 首次发起流程即抛 `TypeError: ..._call() got an unexpected keyword argument 'on_a4_event'`。两处 `_call` 增加 `on_a4_event=None` 形参并转发给 `run_fullflow` / `resume_fullflow`。`fullflow.py` 下游已全程透传，无需改动。
- **A4 面板渲染崩溃（Cannot read properties of undefined (reading 'split')）**：`renderPanel` 对无 `path` 字段的面板（a4documents/a4uploads）改 `data=ctx`；`resolve` 空/非字符串 dotted 返回 `ctx` 兜底；`form_schema.py` 自检改 `p.get('path')`。

### Verified
- 单元验证：monkeypatch `run_fullflow` / `resume_fullflow` 记录器，直接调真实 `api_start_stream` / `api_decide_stream` 端点 → 两处 `_call` 均收到 `on_a4_event`（callable）。
- 生产实测（会话 `fullflow_session_ff-753d2c8f347d`）：`start_stream` → A1 选题闸（零错误）→ approve A1 → A2 检索 75 篇 → A2 闸 → approve A2 → A3 初筛 75 篇 → A3 闸 → approve A3 → **A4-only 触发 + 100s 内 31 条逐篇 `a4` 事件实时流出，全程零 A1/A2/A3 重跑日志**。

### Notes
- 解除 2.9.8 的「开发期冻结」备注（DEV_POLICY.json 已不存在）；本次起恢复常规发布流程。
- 发布包排除：`.gitignore` / `.clawhubignore` 新增 A2/A4 运行产物（`adapters/*.json`、`lit_report.*`、`evidence_log.*`、`references.*`、`pdfs/`、`workbench/runs/` 等），测试内容不进发布包（§16）。

---

## [2.9.8] — 2026-09-01 — 数据抓取增强 port 进本体：连续型模板 + 无边框表重建 + 校验修正（开发期不发布）

> **目标**：把 seam_test 沙盒验证过的 `pdf_extractor_opt.py` 全量 port 进技能本体 `adapters/pdf_extractor.py`，并修复 port 过程暴露的保真缺陷与 opt 版固有 bug。
> 退出标准：4 篇人工 PDF（NEJM/JAMA/Nature/BMC）+ 8 篇自动 PDF 实测达标；`test_pdf_extractor.py`(16) + `test_block_b.py`(20) 离线全绿。✅ 全部达成。

### Added
- **多级降级抓取路径（用户 2026-09-01 明确）**：`parse_pdf` 逐页产出 `table_tiers`——T1 有框表（pdfplumber lines，通用）→ T2 无框表重建（PyMuPDF word 坐标，专用精细）；`extract` 逐页逐层跑模板、**命中即停**（`_review.tier`/`_review.method` 审计到行）。已评估不采用的中间层：pdfplumber text 对齐策略（把正文撕成伪表，实测 BMC 70×12 伪表）与 PyMuPDF find_tables（默认 lines 策略对无框表 0 检出）。
- **失败如实返回**：`review_summary.tier_report`（每页各层尝试与命中行数）+ `review_summary.unresolved`（scanned=无文本层需 OCR；all-tiers-no-template-hit=检出表格但模板全不命中，含 Table 标题者提示人工录入）。纯正文页不记失败（叙述通道仍扫其文本）。OCR 为预留扩展位。
- 连续型抓取模块 port：`t_cont_table`（T_CONT_BETA / T_CONT_CHANGE / T_CONT_CHANGE_CI / T_CONT_TWOARM 四形态）+ `narrative_continuous`（T_MD_CI 正文叙述）。
- 效应量模板 port：`EXTRACTION_TEMPLATES` 注册表（T_HR_CI / T_OR_CI / T_RR_CI / T_MD_CI / T_PVALUE）+ `t_effect_table`（森林表 2×2 计数列 + HR 列双源回填）。
- 无边框表重建 `_rebuild_borderless_table`：PyMuPDF word 坐标，「Table N 标题锚 + y 范围圈定 → y 相邻归并行聚类（标签词保留）→ x 中心 20pt 列聚类」；extract 主循环接入**行级 fallback**（页内全部表格模板未命中时重建后重跑一轮），重建行 `_meta.rebuild=True` 可审计。
- `_norm_path()`：Git Bash `/c/...` 路径 → Windows `C:/...`，`parse_pdf`/`_rebuild_borderless_table` 全部走规范化。

### Fixed
- **check_te_sete CI 尺度混乱（opt 版固有）**：HR/OR/RR 行 te 为 ln 值而 reported.ci 是原始尺度 → ci-asymmetric 全误判 failed。extract 调用点按 measure 对比值度量的 CI 先取 ln 再校验；MD 保持原值。JAMA failed 19→2（剩余 2 个为校验器正确拦截的可疑 interaction CI，交人工）。
- **sete 回填公式**：`0.5*(lnhi−lnlo)`（=1.96·se，错）→ `(lnhi−lnlo)/3.92`（Woolf se，与全模块约定一致）；且回填不再覆盖表格自带的报告 te/sete（`r.get(...) or` 语义）。
- **reported_summary 互证污染**：port 中误加的「正文 OR → reported_summary['*']」导致 NEJM 森林表 31 行全部 or-mismatch failed；移除（check_dichot 不再自动互证）。
- **ci-asymmetric 阈值**：1.10 → 1.25（报告值四舍五入致 ln 空间实测不对称 ≤1.12；真正取错数值实测 4.6）。
- **基线表/n(%) 表误抓**：t_continuous 加表级防御（`_BASELINE_KW` 表头且无结局词 → 跳过；表内 `n (%)` 声明 → 跳过；全表数值对 ≥80% 为整数对 → 跳过）+ 行级恰好 2 组 m±SD 才配两臂（>2 组为多臂基线表）。NEJM 基线表 14 行 + 合并用药 n(%) 4 行 + BMC 基线碎片 2 行误抓全部清除。
- **_PVAL 误抓**：`P\b`+IGNORECASE 命中 'group 30' 尾字母 p → 强制关系符 `[=<]` 必选 + pv>1 值域丢弃。
- **嵌套括号 OR/HR 句漏抓**：te→CI 锚间隔段 `[^()]{0,80}?` 禁括号，挡掉 BMC 系写法 '(odds ratio 1.71 (95% CI 0.93 to 3.16))' → 改 `.{0,80}?`（误越界由 lo≤te≤hi 校验兜底）。
- **CI 锚与 lo 间换行漏抓**：JAMA 原文 'HR, 0.83; 95% CI,\n0.76-0.92'——`[ ,:(]*` 不含 `\n` → 并列双 HR 段只抓到第二个（0.95/0.81），第一个（0.83/0.77）整行丢失 → 字符类加 `\n`。修复后 JAMA 并列双 HR 正确双抓（0.83 CI 0.76-0.92 + 0.95 CI 0.77-1.17 等均为原文真值），此前 2 个「拼接错行 failed」实为该 bug 症状，随修复消失（JAMA 终态 20 HR 全 needs_review，0 failed）。
- **无边框重建 block 选择**：正文 '(Table 1)' 引用被误当标题锚（start_bno 污染致正文全混入）→ 改「`Table N` 开头且词数 ≤15 的短 block」为锚，按 y 范围圈定表格区域。
- **tests/test_pdf_extractor.py**：`test_full_pipeline` 断言对齐现行 API（叙述 or_ci 直接成行 T_OR_CI、candidates 仅 P 值 kind='pvalue'、n_rows=3）。

### Verified（bench 12 篇：4 人工 + 8 自动）
- 效应量行：HR 73 / MD 9 / OR 2（vs port 前 opt 基准 HR 73 / MD 8 / OR 2；MD +1 来自 doc9 行级重建 fallback 增益）。
- verified 31（NEJM 森林表双源）保持不膨胀；垃圾行 142（vs 155）全为有效数据行。
- Nature 连续型 6 MD（Cystatin C/hs-CRP/PAB × Beta 列 + Changes 两来源一致）；BMC Table 1 无边框表完整重建（10 行 × 6 列，4 组 m±SD 对齐），基线表正确不产 meta 行。

### Notes
- 开发期冻结（DEV_POLICY.json）：仅本地改动，不推送 / 不发布。
- 测试 36/36 全绿（test_pdf_extractor 16 + test_block_b 20）；bench 12 篇终态 HR 73 / MD 9 / OR 2、verified 31 不膨胀。

---

## [2.9.7] — 2026-09-01 — B 阶段：Block B1 计算上云 + 删除本地双引擎（开发期不发布）

> **目标**：落实架构终态原则（coze 为唯一计算真相源，本地不保留计算引擎）。B1 pairwise 计算改走 coze R 引擎；删除本地 numpy 双引擎与 `_dev/local_engine.py` 残留。
> 退出标准：运行路径 B1 不再本地计算；`b1_pairwise_python` 降级为仅回归 oracle；`_dev/local_engine.py` 已删。`test_block_b.py`(20) + `test_pdf_extractor.py`(16) 离线全绿。

### Changed
- `adapters/block_b.py`：`b1_meta_analysis` 默认 `engine="coze"`，B1 经 `coze_client.run_stage` 发 ct-meta2 R 引擎；新增 `_build_b1_coze_env` / `_extract_coze_stats` / `_coze_stats_to_pairwise`（coze `stats` → 本地 pairwise 形状，对数尺度同构，B2/B3/B4 零行为变更）。`run_block_b` B1 显式 `engine="coze"`。
- `b1_pairwise_python` 标注为仅回归/调试 oracle（`engine="local"`），非运行路径；`engine="auto"` 移除。

### Fixed
- **单组率 `single_group_meta` 列名 bug（2026-09-01）**：coze 端 dispatcher（`adapters/coze/src/r_engine/run_task.R` `single_group_meta` 分支）硬编码读取 `df$event`（单数），而本地核心代码 `meta_analysis_core.R`、参考文档 `single_group_meta.md`、模板 `extract_assist.py` 与用户请求均使用 `events`（复数）。`.build_df()` 只 `tolower` 列名、不应用 colmap 重映射，导致 `events` 列落 else 分支调 `metamean(mean=NULL)` 报错。
  - `run_task.R`：改为经 `.col_name()` 解析 event/n 列并加 `events` 别名归一（colmap 对单组率生效，与二分类/连续分支一致）。
  - `meta_analysis_core.R`：`single_proportion`（`calculate_effect_size` + `ma_analyze`）同步兼容 `event`/`events` 两种列名。
  - 验证（Python 等价模拟）：`events`+colmap / `event`单数 / colmap `event→events` 三种输入均正确命中 `metaprop` 分支。
  - 注：measure 名 PLOGIT（coze/meta 包）vs PLO（本地 core/metafor）为两套 R 包各自合法 logit 写法，功能等价；已于同日后续修复中按别名归一统一（见下方 Fixed·measure 提示统一）。

### Fixed
- **coze 端同步核查 + `_STAGE_KEYS` 潜伏 bug 修复（2026-09-01 晚）**：用户拉取 coze 当前代码包（`project_code_4f377ea2.zip`，含 `state.py` 的 `schema→envelope_schema`+`alias="schema"`+`populate_by_name=True` 三处改名）核查死机问题。
  - 核查结论：`state.py` 改名规范干净（下游无消费 `.schema` 的代码、`contract_version` 字段兜底使 `is_legacy_request` 路由不受影响），**非死机原因**；单组率 `events` 案例在 R 核心计算实测不卡死不报错（`metaprop`+`rma.uni` 桥接正常）。**"长期死机不结束"实为 R 引擎冷启动 + 多张 SVG 出图（尤其 `influence` 多面板 7×9）在 coze 无头 Linux 环境耗时过长**（报告自承"R 引擎加载 + 出图耗时较长"），非代码死循环；建议用 `figure.plots=[]` 验证核心计算可秒级返回。
  - 潜伏 bug：`stage_envelope.py` 的 `_STAGE_KEYS` 仍含 `"schema"`，但 `state.py` 改名后 `model_dump()` 输出字段名变为 `envelope_schema`，导致"纯 per-stage 信封（只带 schema 不带 contract_version）"被 `is_legacy_request` 误判为 legacy。已修复：判定键集改为 `("contract_version","envelope_schema","schema","pipeline_id","pipeline","stage")`（同时保留 `schema` 兼容旧裸 dict）。已用 Python 等价模拟验证三场景（纯 schema / 含 contract_version / 纯 legacy）无回归。
  - 同步：`project_code_4f377ea2.zip` 与本地镜像 `adapters/coze/src/` 基本一致（仅 `meta_analysis_core.R` 不同——镜像含 2026-09-01 的 events 兼容修复、云端无，而云端不跑该文件故无影响），已将其余文件同步进镜像；`meta_analysis_core.R` 修复版保留（未被云端版覆盖）。
  - 交付：`coze_full_pkg_v2/meta_analysis_coze_full_2026-09-01_v2.zip`（含 state.py 改名 + events 修复 + `_STAGE_KEYS` 修复，33 文件，强校验通过）。

### Fixed
- **单组率 measure 提示统一（别名归一，2026-09-01 晚）**：消除 PLOGIT vs PLO 双口径文档混乱——统一为 **PLOGIT/PRAW 主口径，PLO/PR 等价别名**（logit/原始比例两包功能等价；PASF/PFT 两包实现不同，不做跨包映射）。
  - `meta_analysis_core.R` `calculate_effect_size`：`measure_up <- toupper(measure %||% "PLO")`，`PLO/PLOGIT → escalc(measure="PLO")`、`PR/PRAW → escalc(measure="PR")`，大小写不敏感，非法值显式报错。
  - `meta_analysis_core.R` `ma_analyze`：默认 measure 从 `PLO` 改为 `PLOGIT`（与 coze 端 `run_task.R` 默认口径一致），back-transform 判断改为 `toupper(measure) %in% c("PLO","PLOGIT")` 双兼容。
  - 文档统一：`references/single_group_meta.md` 加口径统一注记（PLOGIT/PRAW 主口径 + PLO/PR 等价别名 + PASF/PFT 不跨包映射）；`references/data_templates.md` 示例改 `measure="PLOGIT"`；`references/advanced_api.md` 注释改 `PLOGIT(PLO)`；`scripts/extract_assist.py` `measure_hint` 改 `PLOGIT / PRAW / PASF`。
  - 验证：纯 base R `parse()` 语法通过（19 expressions）；PLO/PLOGIT/plogit/PR/PRAW/praw 六种输入路由模拟全对、非法值正确拒绝。
  - 交付：`coze_full_pkg_v3/meta_analysis_coze_full_2026-09-01_v3.zip`（33 文件，五项强校验全过：core measure 别名统一 / core events 修复 / run_task.R events 修复 / stage_envelope envelope_schema / state.py 改名）。**注**：`run_task.R` source 本文件，measure 统一须随 v3 包部署 coze 后方在云端主路径生效。

### Fixed
- **influence 多面板图默认跳过保护（2026-09-01 晚，用户确认"确实是出图慢"）**：死机诊断为「R 引擎冷启动 + influence 7×9 多面板 SVG 出图在 coze 无头 Linux 耗时过长（k 大时分钟级）」后，给三处 influence 出图点加保护——**默认跳过 + warning 提示，确需出图须显式传 `figure.heavy_plots=true`**：
  - 主 pairwise 分支（`single_group_meta`/`pairwise_meta` 等）：`if ("influence" %in% plots) { if (isTRUE(figure$heavy_plots)) { .meta_to_rma 桥接 + .influence_plot } else { warns 追加跳过提示 } }`。
  - `rma` 桥接分支（`meta` 对象转 rma 后出图）与通用 meta 分支：同款 `heavy_plots` 保护。
  - `isTRUE()` 严格语义：仅逻辑 `TRUE` 触发，字符串/数值 `"false"`/`1` 均走跳过。
  - 验证：R `parse()` 语法通过（1416 行）；Python 复刻 `isTRUE` 语义 6 场景全过（默认跳过+warning / heavy_plots=true 出图 / 无 influence 不受影响 / 字符串/数值 heavy_plots 仍跳过 / 用户案例默认核心计算秒回）。
  - 交付：`coze_full_pkg_v4/meta_analysis_coze_full_2026-09-01_v4.zip`（33 文件；run_task.R 与镜像逐字节一致，其余 32 文件与 v3 包零差异，语义校验全过）。**注**：死机案例改用默认（不再传 `influence` 图或已由保护跳过）后核心计算应秒级返回；`figure.heavy_plots=true` 仅在确需 influence 图时显式开启。

### Fixed
- **v5 完整部署包补齐（2026-09-01 晚，用户平台提示"缺少 pyproject.toml/uv.lock/scripts/.coze/docker 等关键文件"）**：前 v1–v4 包仅打 `src/` 运行时代码，缺 coze 平台部署配套，无法直接运行/部署。重建**以 coze 项目根 `adapters/coze/` 为包根**的完整包：
  - **包含**（70 文件）：`.coze`（entrypoint `src/main.py`）、`pyproject.toml`、`uv.lock`、`docker/`（Dockerfile/build.sh/r_packages.txt/system_deps.txt/restore_r_env.sh 等 8 项）、`scripts/`（http_run.sh/setup.sh/setup_r_environment.sh/pre_deploy_check.py 等 8 项）、`src/`（33 文件，含本轮 events/measure/influence 修复）、`tests/`（14 项 R 回归）、`assets/`、`rendering.py`、`README.md`、`.gitignore`。
  - **排除**（依 ct-base 红线 + 噪音）：`coze_contract.md`（红线不打包）、`_deploy/`（嵌套旧包）、`AGENTS.md`/`DEV.md`/`REMOVED_PACKAGES.md`/`TEST_VS_PROD.md`（内部开发/过程文档）、`__pycache__`/`*.pyc`/`.venv`/`.pytest_cache`。
  - 校验：zip 完整性 OK；14 项部署关键文件全在；红线/噪音全排除（`_deploy` 命中实为 `scripts/pre_deploy_check.py` 的字符串误报，实际目录已排除）；6 项运行时修复（events/influence/measure×2/envelope_schema/state.py alias）全在。
  - 交付：`coze_full_pkg_v5/meta_analysis_coze_full_2026-09-01_v5.zip`（70 文件，完整部署形态）。

### Removed
- `adapters/_dev/local_engine.py`：本地 R 引擎残留，按原则删除（无代码 import，仅文档引用）。

### Notes
- NMA（`b1_nma_r` 本地 R）、B2 GRADE / B3 过度声明 / B4 质量门仍为本地启发式，待迁 coze（见 `contracts/migration/v0.1.0/SPEC.md` M3/M4）。
- A/C 大脑（a1/a3/a4/c1-c4）仍为本地启发式，待迁 coze（M1/M2）。
- 接入 coze 部署/发布须等「开发期结束」宣布（DEV_POLICY.json 冻结）。
- **M8 文档清扫（2026-09-01）**：`adapters/README.md` / `AGENTS.md` / `requirements.txt` 中「`local_engine.py` 保留 / 仅参考 / NOT invoked」等过期描述全部改为「已于 2026-09-01 删除，无本地回退」；迁移规格 M8 标记 ✅ DONE。
- **M7 SKILL.md 铁律更新（2026-09-01）**：§0 铁律 4 改为「Coze is the sole source of truth for computation」（唯一计算真相源 / 本地无计算引擎 / 无授权即无法计算=付费化）；§3 执行模型与 §6 失败兜底同步澄清「declined 仅文本说明未用云端分析、绝非本地计算替代」；README_zh-CN 经核查无矛盾表述；迁移规格 M7 标记 ✅ DONE。

---

## [2.5.0] — 2026-08-31 — Phase 1 Block A 本地优先管线驱动器（方向确定与文献/数据准备）

> **目标**：在不触碰 coze 部署的前提下，落地 Phase 1（Block A：A1 选题闸门 → A2 检索委派 → A3 筛选 → A4 提取核验闸）。
> 设计原则：A2 检索委派走本地 `ct-literature`（tool_card → `execute_tool_cards` 本地 subprocess），A4 🔴`extraction_review` 红线闸本地强执；
> A1/A3 的「AI 生成大脑」在 coze 侧（尚未部署），此处提供**本地启发式兜底 + 合规信封**，`use_coze` 占位待 coze 部署后无缝接管。
> 退出标准（路线图 §2 Phase 1）：选题报告/检索结果/筛选建议/提取草稿均可经 stage 信封流转 ✅；A4 闸本地强执 ✅。
> **未覆盖**：A1 双库（Cochrane/PubMed）探针评分与 PROSPERO 查重、A3 AI 筛选精度 —— 依赖 coze 或 ct-registry 部署，当前为离线启发式。

### Added
- **Block A 本地驱动器**（`adapters/block_a.py`，不调用 `run_stage`/`run_meta`，故不触发出站鉴权）：
  - `build_block_a_env(topic, ...)`：构造合规 stage 信封（`contract_version`/`schema`/`pipeline.block="A"`/`stage.id=A1`）。
  - `a1_topic_selection`：本地启发式选题闸门（PICOS 推断 + 范围预警），产出 `next_human_action(type=confirm, gate=none)`，标注 `coze_ready=False`。
  - `a2_literature_search` / `a2_build_tool_card`：构建 `ct-literature` tool_card → `execute_tool_cards` 本地执行 → `_extract_studies` 兼容多形态返回（list / `studies`/`papers`/`results`/`records`/`data.*`）。
  - `a3_screening`：本地启发式去重（by doi/title）+ 排除关键词（retracted/撤稿/abstract only/protocol/letter）标记纳入，产出 `next_human_action(type=review)`。
  - `a4_data_extraction`：解析提取表（list / JSON / 行文本退化）→ 产出 `next_human_action(type=approve, gate="extraction_review", required=True)`。
  - `run_block_a(topic, ...)`：编排 A1→A2→A3→A4，返回与 `run_pipeline` 同构的 dict（`done/await_human/gate/stages[]/tool_card_outputs[]`）；A4 闸未持 `human_decision` 批准 → `done=False/await_human=True/gate="extraction_review"`；`run_block_a(..., use_coze=...)` 预留 coze 接管 seam。
- **测试**（`adapters/tests/test_block_a.py`）：11 例全绿 —— 信封合规、A2 委派构造+解析（monkeypatch `execute_tool_cards` 模拟 ct-literature）、A3 去重/排除、A4 红线闸阻断（无决策）/放行（持 approved 决策）/错阶段拒绝、管线 stages 顺序 A1→A2→A3→A4。

### Notes
- **部署依赖**：`ct-literature` / `ct-registry` 须安装于 `~/.workbuddy/skills/<name>/scripts/ct_literature.py`（或 `ct_registry.py`，真实入口非 `run.py`；见 `tool_mapping_meta.json`）。A2 真实检索依赖本机技能就位；缺失时 `execute_tool_cards` 返回 `status=error`（草稿兜底），管线不崩。详见 [2.5.1]。
- **能力边界**：A1/A3 当前为离线启发式（精度有限，须人工确认）；A4 红线闸已强执，但提取草稿本身待 coze 部署后由 AI 生成并经本闸核验。coze 部署后即可移除 `coze_ready=False` 标记并启用 `use_coze=True`。

---

## [2.5.1] — 2026-08-31 — A2 真实检索打通（tool_mapping 修正 + 结果文件读取）

> **触发**：用户确认 ct-literature / ct-registry 本机安装就绪；实测发现 P0 写的 `tool_mapping_meta.json` 与真实 CLI 不一致，A2 实际无法检索（subprocess 找不到 `run.py`、缺 `--run`、stdout 仅日志）。

### Fixed
- **`tool_mapping_meta.json` 修正**（P0 未核真实 CLI 时臆写）：
  - 入口 `scripts/run.py` → 真实 `scripts/ct_literature.py` / `scripts/ct_registry.py`（`run.py` 不存在）。
  - `cmd` 裸 `python` → `C:/Tools/anaconda3/python.exe`（遵循 LRN-20260614-006）。
  - arg_map 错配修正：ct-literature `--query`/`--condition` → 真实 `--topic`（必填）；ct-registry `--condition`/`--country` → 真实 `--cond`/`--status`（无 `--country` 参数）。
  - 新增 `fixed_flags: ["--run"]`：ct-literature 必须带 `--run` 才发网络（否则 dry-run）；`execute_tool_cards` 现支持无条件追加开关参数。
  - 新增 `arg_map.out_dir → --out-dir`，检索结果落盘到指定目录。
- **`coze_client.execute_tool_cards` 健壮性**：
  - `skill_dir` 的 `~` 经 `os.path.expanduser` 展开（subprocess 不自动展开 ~）。
  - 新增 `_parse_tool_output`：整段 JSON 或逐行 NDJSON 均可解析（ct-literature 逐行 `print(json.dumps(rec))`），无可解析记录回退原始字符串。
- **`block_a.a2_literature_search`**：真实 ct-literature 把数据写入 `--out-dir` 文件（`.merged.json` 的 `works[]` 或各源 `openalex.json`/`europepmc.json`），stdout 仅日志；新增 `_read_literature_dir` 回退读取并归一化为 `{title,year,doi,source,pmid,is_retracted,url}` 去重。

### Added
- 真实端到端验证：`run_block_a('osimertinib NSCLC', ...)` 经本地 `ct-literature` 实拉 OpenAlex + EuropePMC 共 6 篇，A2 阶段 `n=6`，A4 🔴`extraction_review` 闸正确阻断（`done=False/await_human=True`）。

### Notes
- 本环境 `ct-literature`/`ct-registry` 已安装就绪，A2 真实检索已可用；ct-registry 的 `--cond/--status/--max/--drug` 亦已对齐（A1 查重待启用）。
- 回归：test_block_a(11)+test_pipeline_client(7)=18 passed；stage_envelope(8)；test_contract PASS。

---

## [2.5.2] — 2026-08-31 — A1 选题闸门接入真实 ct-registry 查重探针

> **触发**：用户确认 ct-literature/ct-registry 安装就绪后，按建议优先把 A1 选题闸门接到真实 ct-registry 查重（与已验证的 A2 同源、零新依赖）。

### Added
- **`block_a.a1_registry_check(topic, max_results, workdir)`**：真实调 ct-registry 做选题查重探针（CT.gov 来源，不走 WHO/CDE 共享端点配额）。返回 `{status, total, returned, sample[], note}`，`sample` 抽自 `report.xlsx`「试验总表」（登记号/标题/状态/国家/注册日期）。
- **`block_a._read_registry_xlsx(xlsx_path, limit)`**：解析 ct-registry 落盘的 `report.xlsx`（中文表头按子串匹配列；ct-registry 跑完会清理中间 json、仅保留 xlsx）。
- **`a1_topic_selection` 接入 `registry_probe`**：`total>=200` 自动追加「方向可能已较拥挤」、`total==0` 追加「空白/新兴方向」提示，写入 `scope_warning`。

### Fixed
- **`coze_client.execute_tool_cards` 新增 `cwd` 参数**：ct-registry 忽略 `--out-dir`、把结果写相对 `./out` 且仅保留 `report.xlsx`，故 A1 在临时 cwd 跑、再从 `<workdir>/out/report.xlsx` 读，避免污染工作区。
- **`tool_mapping_meta.json` ct-registry 新增 `fixed_flags: ["--run"]`**：ct-registry 与 ct-literature 同需 `--run` 才发网络（否则打 PREVIEW 不检索）——实测发现，补齐后查重才真实生效。
- `run_block_a` 调用 `a1_registry_check` 并 try/except 包裹，注册库异常/缺失时优雅降级（`coze_ready=False`、不阻断 A1）。

### Added (tests)
- `adapters/tests/test_block_a.py` 新增 5 例（共 16 passed）：A1 查重探针日志解析（total/returned/sample）、`run_block_a` 携带真实探针、`a1_topic_selection` 拥挤度/空白方向提示；`run_block_a` 系测试桩掉 `a1_registry_check` 保证离线确定性。

### Notes
- 实测 `run_block_a('osimertinib NSCLC')`：A1 经本地 ct-registry 实拉 **CT.gov total=277**、抽样 3 篇（NCT05583409 / NCT06068049 / NCT04148898），`scope_warning` 自动追加「方向可能已较拥挤」；A2 实拉 6 篇；A4 闸 `extraction_review` 正确阻断。
- 回归：test_block_a(16)+test_pipeline_client(7)=23 passed；stage_envelope(8)；test_contract PASS。

---

## [2.6.0] — 2026-08-31 — Phase 2 Block B 本地优先管线驱动器（分析结果产出：双范式 NMA + GRADE + 过度声明 + 质量门）

> **目标**：在不触碰 coze 部署的前提下，落地 Phase 2（Block B：B1 双范式 meta 分析 → B2 GRADE → B3 过度声明 → B4 质量门）。
> 设计原则：本模块完全本地运行（不调用 `run_stage`/`run_meta`，不触出站鉴权）。B1 pairwise 走纯 Python(numpy) 确定性主引擎；NMA 走**真实本地 R 引擎**（`C:/Tools/R-4.6.1/bin/Rscript.exe`，netmeta 3.6-1），R 缺失/异常优雅降级。B3 过度声明检测为单点实现，被 B4 与未来 Phase 3 C2 复用。B4 🔴`final_inclusion` 红线闸本地强执。
> 退出标准（路线图 §2 Phase 2）：B1 双范式（pairwise + NMA）可跑 ✅；B2 GRADE 降级 ✅；B3 12 模式过度声明 + 防误报 ✅；B4 质量门三重 + 红线闸阻断/放行 ✅。
> **未覆盖**：B1 贝叶斯 NMA（仅频率学派 random/common）、B2 GRADE 自动评级（κ=0.44 仅半自动，须人工确认各域）。

### Added
- **Block B 本地驱动器**（`adapters/block_b.py`，与 `run_pipeline` 同构返回 `{done,await_human,gate,final,stages[],attachments[],tool_card_outputs[]}`）：
  - `build_block_b_env(...)`：构造合规 stage 信封（`pipeline.block="B"`、`stage.id=B1`）。
  - `b1_pairwise_python(studies, effect_measure)`：逆方差加权 + DerSimonian-Laird 随机效应（固定+随机），纯 numpy 确定性；支持 2×2 表（Haldane 0.5 校正）或预计算 (TE,seTE)；输出 k/TE_fixed/se_fixed/ci_fixed/p_fixed/TE_random/se_random/ci_random/p_random/tau²/I²/Q/forest。
  - `b1_nma_r(network_studies, effect_measure, reference)`：**真实本地 R netmeta NMA**（见 Fixed 适配 netmeta 3.6-1），返回 `{status:ok, result:{model,n_treatments,treatments,tau,comparisons[]}}`；失败/缺 R/缺包 → `{status:error/skipped, reason}`（不抛）。
  - `b1_meta_analysis(...)`：编排 pairwise（python 主引擎）+ NMA（R，可选），nma=False 或缺失 network 时标记 skipped。
  - `b2_grade(pairwise, risk_of_bias, indirectness, publication_bias)`：起点 HIGH，按 5 域降级（不一致性 I²≥75→-2 / ≥50→-1 / ≥25→-0.5；不精确 k<3 或 CI 跨零→-1；偏倚风险 high→-1/moderate→-0.5；间接性/发表偏倚 serious→-1）→ High/Moderate/Low/VeryLow；标注 `coze_ready=False`（须人工确认）。
  - `_OVERCLAIM_PATTERNS`（12 模式）+ `detect_overclaims(claims_text, stats)`：单点实现，被 B4/C2 复用；辅助条件 `ci_cross`/`p_sig`/`ns`/`weak_meta`/`to_all` 防误报。
  - `b4_quality_gate(grade_report, overclaims)`：质量门三重（GRADE + 过度声明 + 人工闸），始终产出 🔴`final_inclusion` 人工闸（`required=True`）；存在 high 级过度声明或 GRADE=VeryLow → `critical=True` 阻断自动续跑。
  - `run_block_b(...)`：编排 B1→B2→B3→B4；B4 闸未持 `human_decision` 批准 → `done=False/await_human=True/gate="final_inclusion"`；持 `approved` 决策 → 放行。

### Fixed
- **`block_b._NMA_R_SCRIPT` 适配 netmeta 3.6-1（原 NMA 真实调用恒 `status=error`，Phase 2 收口阻断项）**：
  - 参数名 `Te`/`seTe` → 大写 `TE`/`seTE`（netmeta 3.6-1 不再识别小写别名）。
  - 参数 `reference` → `reference.group`（netmeta 3.6-1 已改名）。
  - NMA 结果字段由 `TE.nma`/`lower.nma` 等（旧版）改为 `.random`/`common` 两套（`TE.nma.random`/`seTE.nma.random`/`lower.nma.random`/`upper.nma.random`/`pval.nma.random`，优先 random 回退 common）。
  - `res$comparisons` 为 `"t1:t2"` 标签向量（非 data.frame），改为 `strsplit(...,":")` 拆出 t1/t2 构造比较表；`res$treatments` 在 3.6-1 为空，改为从拆分后的唯一臂标签推导。
  - 移除 `a$sm %||% "OR"`（`%||%` 来自 rlang，netmeta 命名空间未导入 → 解析报错），改为显式 `if (is.null(a$sm)) "OR" else a$sm`。
  - `reference.group` 为 NULL 时 netmeta 3.6-1 在 `== ""` 判定上崩（length zero）→ 改用 `do.call(netmeta, args)` 条件构造，仅当 `ref` 非 NULL 时加入 `reference.group`。

### Added (tests)
- `adapters/tests/test_block_b.py`：18 例（确定性、离线、monkeypatch `b1_nma_r` 验证优雅降级）+ 2 例真实 R 集成测试（`TestB1NMAReal`，R 缺失时 skip）。覆盖：信封合规、pairwise python 计算/2×2 折算/空、NMA skipped/error 降级、GRADE 高异质性降级/清洁→High、B3 12 模式命中（OC1/OC2/OC3/OC5）与防误报（OC2 CI 未跨零不误报）、B4 红线闸阻断（high 过度声明→critical）/放行/错阶段拒绝/stages 顺序 B1→B2→B3→B4。

### Notes
- 真实 R NMA 实测（`A/B/C` 三臂网络）：`status=ok`、`model=random`、`tau≈0.454`、3 条比较（A:B/A:C/B:C）均带 TE/CI/p；连续型 `MD` 在无 reference 时由 netmeta 自选参照亦通过。
- 端到端 `run_block_b(..., nma=True, network_studies=...)`：pairwise TE_random≈0.481、NMA 3 比较、GRADE=Moderate、B3 命中 OC5（亚组外推）、B4 闸人工批准后 `done=True`。
- 回归：test_block_a(16)+test_block_b(20)+test_pipeline_client(7)+stage_envelope(8)+test_contract = 全绿（共 51 passed）。

---

## [2.9.6] — 2026-08-31 — PDF 数据抓取 P1（文本型 PDF：表格模板 + 叙述正则 + 一致性校验，开发期不发布）

- 新增 `adapters/pdf_extractor.py`：fitz 页型检测 + pdfplumber（lines 策略，等效 lattice，零新依赖）。
  - 表格模板：`T_DICHOT`（2x2 n/N → ai/bi/ci/di 原始计数，臂列关键词/位置定位）、
    `T_CONTINUOUS`（行内 mean±sd 对 → te/sete，n 缺失回退行内整数）。
  - 正文通道：正则候选（dichot_counts / or_ci / md_ci，带页码锚点），零幻觉；不做臂方向推断。
  - 一致性校验：四格表重算 OR/95%CI（Woolf，1%/2% 容差）、零格/事件>总数拦截、te↔CI 对称性与
    宽度互推；CI 不匹配仍回填重算 te/sete（置信度单独降级 needs_review）。
  - 置信路由 verified / needs_review / failed；`to_a4_rows` 直通 fullflow A4 extraction_table。
- 契约 `contracts/pdf_extraction/v0.1.0/SPEC.md`（P1 范围/红线：无扫描件、无 LLM、连续来源强制人工）。
- 测试 `tests/test_pdf_extractor.py` 16 项全绿（校验数学/模板/叙述/合成 RCT PDF 端到端 → b1 冒烟）。
- P1 已知限制：无边框表、无扫描件、跨页表不合并、异形表头需人工列映射（P2）。

---

## [2.9.0] — 2026-08-31 — 本地 coze 镜像测试收口（Level 1 进程内冒烟 + 发布污染守护）

> **触发**：用户确认「可用本地 coze 镜像代码代替 coze 做测试」，并给出两条硬约束——
> (1) 测试数据真实写飞书可接受；(2) 镜像代码发布到 coze 端后必须能正常执行；
> (3)（前序红线仍生效）真实发布代码绝不受本地测试信息污染，且两者差异须白纸黑字标注。
> 目标：在不碰真实 coze 部署的前提下，用本地 `adapters/coze/` 镜像代码验证「图能跑通 + 产物可被 coze_client 解析」，且发布包字节一致。

### Added
- **本地 coze 镜像 Level 1 进程内测试驱动器**（`adapters/tests/coze_local_harness.py`，**唯一**容纳测试桩的文件，绝不写进 `src/`）：
  - 注入 `coze/src` + `adapters` 到 `sys.path`，设 `RSCRIPT_BIN=C:/Tools/R-4.6.1/bin/Rscript.exe`；`local_transport` 直接 `asyncio.run(graph.ainvoke(payload))`，零网络/零鉴权。
  - `run_stage_local` 复用 `coze_client.run_stage` 并在运行时 monkeypatch `_auth_gate = lambda *a,**k: True`（仅内存，不改盘、finally 还原），验证真实 per-stage 契约路径。
  - `smoke_test()` 跑 probe（短路）+ real（3 行 `pairwise_meta`，`sm=MD`）双路径，回传结构化报告（mode/stage_result/next_human_action）。
- **部署前污染校验**（`adapters/coze/scripts/pre_deploy_check.py`，gitignored）：
  - `_check_src_clean`：src/ 禁含 `coze_local_harness`/`local_transport`/`RSCRIPT_BIN = "C:/`/`_auth_gate = lambda`/`COZE_DEPLOY_ENV` 等测试态痕迹。
  - `_check_pyproject_faithful`：pyproject 须保留 coze 运行时依赖（pycairo/dbus-python/PyGObject，本地 `uv sync` 时曾临时移除、发布前须还原）。
  - `_check_harness_not_in_src`：harness 不得出现在 src/ 树。`main()` 退出码 0/1/2。
- **测试-生产差异标注**（`adapters/coze/TEST_VS_PROD.md`，gitignored）：6 维度差异表（运行方式/鉴权/R 路径/R 布局/飞书/S3/依赖）+ 本地 venv 构建须知 + pre_deploy_check 守住项 + 本轮抓到的真实 bug 与验证结论。
- **deploy_retest 新增 G7/G8 两道闸**：
  - G7 本地 coze 镜像冒烟（跑 `coze_local_harness.py`，probe+real 双绿且 real 须回 stage_result + next_human_action）。
  - G8 部署前污染校验（跑 `pre_deploy_check.py`，src 无测试态痕迹、pyproject 与 coze 一致）。

### Fixed
- **真实发布阻断 bug（本地镜像测试抓出）**：`meta_analysis` 节点经 `make_stage_response` 把 `stage` 序列化为 **JSON 字符串**回显，但 `FeishuSaveNodeInput.stage` 声明为 `Dict[str, Any]`，langgraph 同名字段传 str → `ValidationError` 崩溃；**该请求打到 coze 端也会崩**。修复 `adapters/coze/src/graphs/state.py`：`FeishuSaveNodeInput.stage` 放宽为 `Optional[Any]`（与「stage 字符串回显」设计一致）。复测 real 路径 `mode="stage"`、`has_stage_result=true`、EXIT=0。此为合法修复，非测试污染。

### Notes
- **R 引擎交叉验证一致**：镜像 R 引擎 `pairwise_meta` 算出 MD 合并 `0.4812 / CI[0.21,0.75] / I²=0`，与本地 `block_b` Python 引擎数值逐位吻合 —— 两套独立实现互证，镜像图在本地即可视为「coze 端等价」。
- 隔离策略：测试桩只活 `adapters/tests/coze_local_harness.py`；`adapters/coze/` 整体 gitignored；pyproject 已还原（含 pycairo/dbus-python/PyGObject）；发布代码字节一致。
- 未覆盖（仅 coze 运行时存在）：真实 workload-identity 鉴权、真实飞书/S3 写入、Linux `/tmp/r_env` R 布局。
- 回归：deploy_retest 8/8 GO（G1 66 passed / G2-G6 / G7 镜像冒烟 / G8 污染校验）。

---

## [2.9.5] — 2026-08-31 — fullflow HITL 编排器（A→B→C 可交互流水线，开发期不发布）

> **触发**：架构缺口 G1/G4 收口。设计原则（用户 2026-08-31 定）：人-AI 协作，非全自动——
> 低准确度环节随时可打断、改人工介入。spec：`contracts/fullflow/v0.1.0/SPEC.md`。

### Added
- `adapters/fullflow.py`：薄交互控制器 `run_fullflow` / `resume_fullflow` / `FullflowSession`。
  - 三档停靠：P1 块间交接确认（handoff_confirm）/ P2 红线闸（A4/B4/C3/C4，复用块层既有闸语义）/
    P3 任意阶段软停（`pause_at`）；默认停靠集 `DEFAULT_PAUSE_AT`（A1/A3/A4🔴/B4🔴/C1/C3🔴/C4🔴）。
  - 人工决策统一 schema（§6.1）：`approved / revised / skipped / rejected`；
    **红线闸拒 skipped**、rejected 停在原地重放视图、全部决策留痕会话 JSON（审计日志）。
  - revision 走输入参数降级映射（§6.3）：A4 rows → `extraction_table`（list）→ Block B studies；
    其余阶段为 stage_result 事后补丁（模块 docstring 标注限制）。
  - 会话原子落盘（tmp+rename）`fullflow_session_ff_*.json`，断点续跑 + 审计。
  - 进 B 前 `extraction_guard.check_verified` 双保险：未 `stamp --confirm` 的 CSV →
    `guard_blocked`（unverified_extraction 语义），核验后 approve 放行。
  - 红线：控制器**绝不**自动 approve；空/缺 decision 不推进；B 计算仍 coze 唯一路径。
- `block_a/b/c.py`：新增 `pause_at=None` 参数（P3 软停靠，默认 None = 现状行为逐字节兼容）
  与 `_any_approve` / `_soft_stop` 助手；红线闸凭据兼容单 dict / list 累积。
- `adapters/tests/test_fullflow.py`：9 项离线测试（向后兼容 / P3 停靠 / 红线闸+revision 接缝 /
  会话持久化+rejected / 守卫双保险 / skip 语义 ×3），全绿。

### Known limitations（v0.1）
- 续跑 = 重跑当前块（A1/A3/A4 幂等启发式；A2 检索会重复执行，成本可接受）。
- ct-literature tool_card 真实接线未验证（G5，后续单独做）；coze 端 A/C 图未部署（G3）。

---

## [2.9.4] — 2026-08-31 — 运行入口接入 per-stage 管线（run_analysis → run_stage）

> **触发**：重构核心收口——本地 Block A/B/C 驱动器与 coze 端图架构已就绪，但统一入口
> `adapters/run_analysis.py` 仍走 legacy `coze_client.run_meta`（单发式），未接入新架构。
> 本次把运行入口切到 per-stage `run_stage` 信封，使技能运行时与已部署的 ct-meta2 图、本地
> 驱动器对齐（R1 双模仍在客户端层成立：旧 per-task 信封经 run_stage 自动委派 run_meta）。

### Changed
- **`adapters/run_analysis.py`**：
  - 计算请求改构造 Block B「B1.meta_analysis」per-stage 信封（`_build_compute_stage_env`），
    经 `coze_client.run_stage` 发往 ct-meta2（开发期唯一站点，见 DEV_POLICY.json）。
  - 新增 `_normalize_stage(res)`：将 stage 信封规整为既有消费方（`scripts/run_meta.py` +
    `render_html_report`）期望的 `status/stats/figures` 形状；coze 仅回 `stage_result`（无顶层
    `result`）时从 `stage_result.result` 兜底抽取，避免下游渲染/CLI 缺字段崩溃。
  - `run_analysis(..., debug=False)` 新增 `debug` 透传（同 run_stage，隔离飞书测试流量）。
  - 旧 `run_meta` 单发路径移除；`run_stage` 是其超集，向后兼容。coze 失败/未授权仍返回
    结构化错误（`_source` = `coze_error` / `auth_blocked`），不回退本地。
  - **Fix**：`AuthRequiredError` 错误分支误用已移除的旧符号 `_coze_run.__module__`，改为
    `_coze_run_stage.__module__`（否则授权拦截分支会 `NameError` 崩溃而非返回友好提示）。

### Docs
- `AGENTS.md` / `SKILL.md`：运行路径 `run_meta` → `run_stage`（per-stage envelope）；端点默认改
  `ct-meta2.coze.site`（开发期 ct-meta 已禁用，见 DEV_POLICY.json）。

### Verified
- 真实调用 ct-meta2 端到端（debug=True 隔离飞书）：`run_analysis('pairwise_meta', rows[3], {sm:MD,model:REML}, {format:svg})`
  → `status=ok` / `mode=stage` / `source=coze` / `stats`+`figures`(森林图) 齐全 / HTML 报告生成
  / coze_elapsed≈4.3s；合并效应量与本地镜像 R 引擎一致。
- `deploy_retest` 8/9 GO（G1–G8 全绿；G9 发布冻结 NO-GO 为开发期预期）。

---

## [2.9.3] — 2026-08-31 — 真实调用 ct-meta2 端到端验证 + 修复 run_stage transport 解包 bug

> **触发**：coze 端 (ct-meta2) 已部署更新代码，用户要求真实测试。新增 `adapters/tests/coze_live_test.py`（直连 ct-meta2，debug=True 隔离飞书归因）。

### Fixed
- **`coze_client.run_stage` 真实调用崩溃**（被本地进程内测试掩盖的发布风险）：
  - 根因：`_post_run_with_fallback`（真实 HTTP transport）返回 **4 元组** `(raw, elapsed, used_fallback, final_url)`，
    而 `run_stage` 此前只 `raw, elapsed = transport(...)` 解包 2 个值 → `ValueError: too many values to unpack`。
  - 本地 `local_transport` 返回 2 元组，所以 Level-1 进程内冒烟测试从未暴露；真实出站必崩。
  - 修复：向后兼容两种形态 `raw, elapsed = _tr[0], _tr[1]`（`run_meta` 本就按 4 元组解包，无此问题）。

### Verified（真实出站到 ct-meta2）
- per-stage 信封正确往返：`mode=stage` + `stage_result` + `next_human_action`（coze 端 `schema→envelope_schema` alias 修复生效）。
- R 引擎真实执行 `pairwise_meta`：**MD 合并 = 0.4812 / 95%CI[0.2097, 0.7527] / I²=0**，与本地镜像 `block_b` Python 引擎**逐位吻合**（交叉验证）。
- coze 端 R = `4.6.1`、`meta 8.5.0 / metafor 5.0.1 / netmeta 3.6.1` 包齐全，森林图 SVG 已生成。
- `probe=True` 探测走 legacy 简化返回（status=ok、往返成功），真实分析走 stage 正常 —— 符合预期。
- **诚实标注**：`feishu_write_success` 在返回中为 `null`（coze 端未回该字段，可能 debug 模式跳过 / 凭据未配），真实飞书落库状态未能从响应确认。

---

## [2.9.2] — 2026-08-31 — 同步 coze 端 (ct-meta2) latest：Pydantic `schema` 字段冲突修复

> **触发**：用户上传 `meta_analysis_coze_latest.zip`（coze 端更新后的最新代码），要求比对差异并把需要的内容合并回本地镜像 `adapters/coze/`。

### Fixed
- **Pydantic `schema` 保留名冲突**（pyright 类型检查报错）：
  - `src/graphs/state.py` 3 处 `schema: Optional[str]` 字段重命名为 `envelope_schema`，改用 `Field(alias="schema")` 保持 JSON 序列化 / 反序列化兼容。
  - 3 个请求模型（`MetaRequest` / `GraphInput` / `MetaAnalysisNodeInput`）的 `model_config` 增加 `populate_by_name=True`，支持字段名与别名同时使用。
  - 验证：本地镜像冒烟 `real` 路径 `mode=stage` / `has_stage_result=true` / `has_next_action=true` / EXIT=0 —— 别名改动与现有信封契约向后兼容，**未破坏 per-stage 往返**。

### Added
- 合并 coze 端新增文件：`rendering.py`（SVG 内联渲染工具）、`assets/advanced_functions.R`（`run_task.R` 第 41 行 source 引用，真实在用）。

### Changed
- 同步 coze 端文档/锁文件：`AGENTS.md` / `DEV.md` / `REMOVED_PACKAGES.md` / `uv.lock` / `.gitignore`（与 coze 端 latest 逐字节一致）。

### 保留与清理
- **未丢失本地真实 bug 修复**：coze 端 `state.py` 已包含 `FeishuSaveNodeInput.stage: Optional[Any]`（修复 per-stage 请求打到 coze 的 `ValidationError` 崩溃），合并后本地镜像仍保留。
- 清理本地镜像 stray：`src/r_engine/Rplots.pdf`、`src/r_engine/_zh_extract.json`（R 跑出/孤儿，不在 coze 端）。
- 本地自有交付物保留：`TEST_VS_PROD.md` / `_deploy/` / `tests/test_stage_envelope.py` / `docker/r_packages_with_versions.csv`。

### 验证
- `pre_deploy_check.py` → EXIT=0；`deploy_retest` G7/G8 GO；全量 8/9 GO（G9 发布冻结 NO-GO 为开发期预期）。
- 最终 diff：coze 端 latest 与本地镜像 `modified: []`、`only_in_zip: []` —— 镜像现为 coze 端忠实快照。

---

## [2.9.1] — 2026-08-31 — 开发期策略：禁用 ct-meta + 冻结发布（DEV_POLICY 单源管控）

> **触发**：meta-analysis 进入架构大规模重构开发期，用户下达两条持续生效的硬约束——
> (1) 暂时禁用 ct-meta 调用，ct-meta2 为 coze 唯一调用站点；(2) 暂时禁止 meta-analysis 发布新版本。
> 两条约束持续生效，**直到用户明确告知开发期结束才取消**。故落地为「单源真相文件 + 代码读取 + 闸门拦截」三件套，便于开发结束时一键还原。

### Added
- **开发期策略单源真相**（`adapters/DEV_POLICY.json`，随技能发布包分发但仅开发期生效）：
  `{dev_period, ct_meta_disabled, publish_freeze, set_at, reason, unset_when, effects}`。
  无该文件 / `ct_meta_disabled=false` → 正常生产态（ct-meta 主 / ct-meta2 回退）。
- **`adapters/publish_guard.py`**（仅标准库）：`is_publish_frozen()` / `assert_publish_allowed(platform)` /
  `main()`（退出码 0=允许 / 2=冻结）。任何 meta-analysis 新版本发布（GitHub/SkillHub/ClawHub）前的权威拦截点。
- **deploy_retest 新增 G9「发布冻结状态（开发期）」闸**：读 `DEV_POLICY.json` 的 `publish_freeze`；
  冻结中 → **NO-GO**（明确提示删除该文件即解除）；否则 GO。本闸门只核对状态，不触碰发布动作。

### Changed
- **`adapters/coze_client.py` 端点选择改由 `DEV_POLICY.json` 动态决定**：
  新增 `_dev_ct_meta_disabled()`（读 `DEV_POLICY.json`）；开发期 → `DEFAULT_ENDPOINT=ct-meta2`、
  `FALLBACK_ENDPOINT=""`（**彻底禁用 ct-meta，无回退**）；正常态 → `ct-meta` 主 / `ct-meta2` 回退。
  原硬编码的 `DEFAULT/FALLBACK` 常量定义上移删除，统一在覆盖段按策略赋值。
  `_post_run_with_fallback` 增加 `FALLBACK_ENDPOINT` 空值守卫（`FALLBACK_ENDPOINT and ...`），
  确保开发期空回退端点绝不触发重试。
- token 无需改动：`coze_token.py` 已按 endpoint 分别内嵌 ct-meta2 / ct-meta JWT，切到 ct-meta2 自动用其专属 token。

### Notes
- **开发期还原步骤**（用户结束开发期时）：① 删除 `adapters/DEV_POLICY.json`；② 还原 `coze_client.py`
  覆盖段（`DEFAULT/FALLBACK` 回切 ct-meta/ct-meta2，删除 `_dev_ct_meta_disabled` 逻辑）——或直接
  `git checkout` 该文件；③ `config.json` 白名单可保留 ct-meta（不再被调用即无害）。还原后 G9 自动转 GO。
- **发布冻结优先级高于用户确认**：即使用户后续单独确认「发布」，开发期内仍须拒绝（G9 拦截 + 我不主动发布），
  必须待用户先明确结束开发期。这与前序「发布须用户确认」红线叠加，构成双重闸。
- **`config.json` 白名单保留 ct-meta**：仅影响 auth 授权列表，不影响调用路径（开发期 ct-meta 已无任何调用），最小化改动面。
- 验证：`coze_client.DEFAULT_ENDPOINT == ct-meta2` 且 `FALLBACK_ENDPOINT == ""`；`publish_guard.py` 退出码 2；
  `deploy_retest` 现 **8/9 GO（G9 冻结 NO-GO，符合预期）**。

---

## [2.8.0] — 2026-08-31 — Phase 4 收口：deploy_retest 全管线闸门 + §16/§20.11 红线核对

> **目标**：在 Phase 0–3 四阶段本地驱动器就绪后，落地发布前收口闸门，对齐 ct-base §16 发布前检查清单与 §20.11 coze 接口向后兼容硬约束；**不自动 push/publish**（发布属用户红线，须用户确认）。
> 设计原则：deploy_retest 离线、零网络、零出站；只做「只读核对 + 本地计算校验」，绝不发起出站请求、绝不自动改源、绝不触发 coze 部署/git push/平台 publish。

### Added
- **`adapters/deploy_retest.py`** — 部署前全管线闸门（6 道子闸门）：
  - G1 pytest 测试套件（block_a/block_b/block_c/pipeline_client/stage_envelope）→ 66 passed
  - G2 §20.11 契约向后兼容（`test_contract.py` 退出码 0 + `BACKWARD_COMPAT.md` + `coze_contract.md §9.5` R1–R5）
  - G3 信封契约：A/B/C 三驱动器返回与 `run_pipeline` 同构信封 + 阶段顺序 + 四道红线闸（extraction_review/final_inclusion/reference_verification/manuscript_approval）接线且未退化为自动放行
  - G4 §16.7 发布排除：`.gitignore`/`.clawhubignore` 均含 `adapters/coze/` 与三类 coze 接口文档
  - G5 §16.8 密钥泄漏扫描（ct-base `publish_secret_scan.py --warn-only`）：BLOCK 级才阻断
  - G6 §16.10 R 引擎公式审计：pairwise 逆方差/DL τ² 不变量 + NMA 真实本地 R(netmeta) 调用成功
  - 全 GO → 退出码 0；输出人类可读报告 + 可选 `--json` 报告（路径做 `/c/`→`C:/` 归一化）

### Fixed
- deploy_retest 末尾写 JSON 报告时 Git-Bash 风格 `/c/...` 路径在 Windows 下 `open()` 失败 → 加 `_norm_path` 归一化 + 父目录 `makedirs`；默认报告写入 `adapters/`（不在发布包外落盘）。

### 红线核对结果（逐项）
- §16.7 ✅：`adapters/coze/`、`**/coze_contract.md`、`**/coze_system_prompt_v*.md`、`**/ops.md` 双平台 ignore 齐备；`adapters/coze/` 经验证 `git ls-files` 未跟踪（不进发布包）。
- §20.11 ✅：`coze_contract.md §9.5`（R1–R5 向后兼容保证）与 `contracts/pipeline_stage/v1.0.0/BACKWARD_COMPAT.md` + `test_contract.py`（含 R1 双模 legacy 用例）齐备；`test_contract.py` 为独立脚本（`sys.exit(1)` + 打印 PASS/FAIL），按退出码判定（非 pytest 收集，故 pytest 显示 "no tests ran" 为误读）。
- §16.8 ✅ 密钥扫描：**无 BLOCK 级泄漏**；23 条 WARN 全为误报/策略允许——(a) coze JWT `aud`（受众声明，公开元数据，非签名密钥；用户已明确 coze 凭据允许发布）写入 `CHANGELOG.md` 历史记录；(b) 飞书多维表格 app_id/table_id 仅存于 `adapters/coze/coze_contract.md`（已 §16.7 排除）；(c) `covarian`/`frequent`/`build_V_` 等 R 源码变量名/文档词。跟踪文件中无任何真实私钥/云密钥形态（`sk-`/`AKIA`/`ghp_`/私钥头）。
- §16.10 ✅：pairwise 逆方差加权均值不变量（等 SE → 简单平均）+ CI=TE±1.96·SE + τ²≥0；NMA 真实本地 R `netmeta` 调用 `status=ok` 且 comparisons 非空。

### 边界 / 诚实标注
- deploy_retest 仅做离线核对；coze 端实际部署与 §12.4 实测（老请求仍含 `result`）仍待用户确认后执行。
- 发布（GitHub→SkillHub→ClawHub）属用户红线，**本版本未执行**：仅本地收口 + 闸门 GO，停在 push/publish 前。

---

## [2.7.0] — 2026-08-31 — Phase 3 Block C 本地优先管线驱动器（论文撰写与修改）

> **目标**：在不触碰 coze 部署的前提下，落地 Phase 3（Block C：C1 初稿 → C2 AI 评审 → C3 参考完整性核验 → C4 证据表+投稿前 QA）。
> 设计原则：本模块完全本地运行（不调用 `run_stage`/`run_meta`，不触出站鉴权）。C1 为本地结构化骨架生成器（数字自动填充 B1-B4）；C2 复用 `block_b.detect_overclaims`（B3 单点实现）；C3 参考完整性核验为 🔴`reference_verification` 红线（结构/PRISMA 层，真实 CrossRef/撤稿库核验待 coze 接管）；C4 含 🔴`manuscript_approval` 终闸。红线闸名严格复用 `coze_client._REDLINE_GATES`。
> 退出标准（路线图 §2 Phase 3）：初稿 + 参考核验通过 + GRADE 证据表 + QA 清单，C3/C4 双红线闸本地强执。
> **未覆盖**：C1 真实自然语言成稿（须 coze LLM 接管）、C3 真实 CrossRef/撤稿库核验（须 coze 端 + 外部 API）。

### Added
- **Block C 本地驱动器**（`adapters/block_c.py`，与 `run_pipeline` 同构返回 `{done,await_human,gate,final,stages[],attachments[],tool_card_outputs[]}`）：
  - `build_block_c_env(topic, ...)`：构造合规 stage 信封（`pipeline.block="C"`、`stage.id=C1`）。
  - `_extract_b_summary(b_env|analysis)`：从 `run_block_b` 输出信封或归一 dict 抽取 B1-B4 摘要（pairwise/nma/grade/overclaims/critical），供 C 阶段消费。
  - `c1_draft(topic, b_summary, studies, overclaim_hits)`：结构化 Markdown 初稿骨架（摘要/背景/方法/结果/讨论/结论/参考文献），B1-B4 统计量（k/合并效应/CI/p/I²/τ²/GRADE/NMA 模型）自动填充；B3 检出过度声明以「⚠️ 待核验」标注于讨论段，不擅自删改结论。
  - `c2_ai_review(manuscript, b_summary)`：复用 `block_b.detect_overclaims`（B3 单点实现），对初稿全文做过度声明评审；无 manuscript 时回退 B3 已有命中。
  - `c3_reference_verify(manuscript, sections, references)`：🔴 参考完整性核验（结构层）——必含章节（背景/方法/结果/讨论/结论）缺失→critical；提供参考时每条须有 doi/pmid、撤稿文献→critical；无参考→结构通过但 `coze_ready=False`（待 coze 接 CrossRef/撤稿库）。
  - `c4_evidence_qa(b_summary, c2_hits, c3_report)`：GRADE 证据表（来自 B2）+ 投稿前 QA 清单（统计量报告/异质性/证据表/过度声明处置/参考核验/high 过度声明已处置）；终闸 `manuscript_approval`（`required=True`），critical = C3 critical 或 C2 含 high 过度声明。
  - `run_block_c(topic, studies, b_env, analysis, references, human_decision)`：编排 C1→C2→C3→C4；红线闸解析按 C1→C4 顺序取首个未批准闸为阻断点；`human_decision` 支持单 dict 或 list[dict]（累积多闸批准，单轮即可放行 C3+C4）。

### Added (tests)
- `adapters/tests/test_block_c.py`：**15 passed**（确定性、离线、不触 coze/R）。覆盖：信封合规、C1 章节齐全+数字填充+过度声明标注、C2 复用 B3 命中 OC1/良性无命中、C3 缺章→critical/撤稿→critical/无参考→结构通过且 coze_ready=False、C4 证据表+QA 与 high 过度声明→critical、C3→C4 双红线闸阻断顺序与放行（含 list 累积批准 done=True）、错阶段决策无效、stages 顺序 C1→C2→C3→C4。

### Notes
- 端到端 A→B→C 链验证：`run_block_b(...)`（真实 R NMA，grade=Moderate）→ `run_block_c(analysis=b_env, references=None)`（双闸 list 批准）→ `done=True`、C1 初稿 872 字符/7 章节、C4 GRADE 证据表+6 项 QA。
- 回归：test_block_a(16)+test_block_b(20)+test_block_c(15)+test_pipeline_client(7)+stage_envelope(8) = **66 passed 无回归**；test_contract.py 无用例。
- 能力边界（诚实标注）：① C1 为结构化骨架生成器（本地启发式填数），真实自然语言成稿须 coze LLM 接管（`coze_ready=False`）；② C3 真实 CrossRef/撤稿库核验须 coze 端 + 外部 API，本地仅做结构/PRISMA 层；③ C2 复用 B3 规则匹配，AI 语义级润色评审待 coze。coze 部署后即可移除 `coze_ready=False` 标记并启用 `use_coze=True` seam（同 Block A/B 设计）。

---

## [2.4.0] — 2026-08-31 — Phase 0 per-stage Pipeline 客户端骨架（本地薄客户端 + coze 双模路由 R1）

> **目标**：把已确认的「本地薄客户端 + coze 编排引擎」架构（见 `meta_analysis_roadmap.md` Phase 0）
> 从规格层落到可运行骨架。契约（SPEC/双 schema/示例/`test_contract.py`）已于前序工作定稿，本版本实现两端代码。
> 退出标准（路线图 §2）：① 老 `run_meta` 请求仍返回 `result`（R1 实测通过）✅；② 新 `run_stage` 端到端
> 跑通 Block B（单阶段计算）✅；③ `test_contract.py` PASS ✅ + `test_pipeline_client.py`(7) + `test_stage_envelope.py`(8) 全绿 ✅。

### Added
- **本地 per-stage 客户端**（`adapters/coze_client.py`）：
  - `run_stage(env)`：发送 per-stage 信封；旧 per-task 信封（无管线字段）**委派 `run_meta`**（R1 双模在客户端层成立）。
  - `parse_stage_response(outer)`：解析 `stage_result`/`next_human_action`/`tool_cards`（coze 端以 JSON 字符串承载，与 `result` 同模式）+ 兼容旧 `result` 内层（R2）。
  - `execute_tool_cards(cards)`：复用 need_tool 范式——`request_upload` → 本地 `_upload_file` 经预签名 PUT 上传；`ct-*` → 查 `tool_mapping_meta.json` 构造 CLI 执行（草稿兜底）。绝不抛错中断管线。
  - `run_pipeline(initial_env)`：薄客户端编排（发→解析→执行 tool_card→回填 `stage_context`→续跑），**红线闸强执**（`gate≠none & required` 阻断自动续跑，交人工）。
  - `_upload_file` / `download_attachments`：文件双向传输（S3 预签名 PUT/GET，sha256 校验）。
  - `attach_billing(env, account_id, billing_token)` + `build_stage_payload`：`account_id`/`billing_token` 仅透传（预留接口，与 `query_origin` 独立）。
  - `_post_run_with_fallback`：抽取 run_meta / run_stage 共用的「主端点 → token 失败回退 FALLBACK_ENDPOINT」逻辑，消除重复。
- **coze 端 R1 双模路由**（`adapters/coze/`）：
  - `src/graphs/state.py`：所有 pydantic 模型加 `model_config = ConfigDict(extra="ignore")` 并新增可选字段
    `contract_version/schema/pipeline_id/pipeline/stage/stage_context/attachments/account_id/billing_token`（请求侧）
    + `GraphOutput`/`MetaAnalysisNodeOutput` 并列 `stage_result`/`next_human_action`/`tool_cards`/`stage`（str 模式，§9.1）。
  - `src/graphs/nodes/stage_envelope.py`（纯标准库，可单测）：`is_legacy_request`（R1 双模判定，兼容裸 dict 与 pydantic `model_dump`）、
    `make_stage_response`（把 R 引擎内层包成 stage 信封，R2：`result` 与 stage 字段并列）。
  - `src/graphs/nodes/meta_analysis.py`：`meta_analysis_node` 按双模路由——legacy → 仅填 `result`；stage → 填 `result` + stage 字段。**未重部署前本地侧已生效，coze 仍返旧结构（adapter 走兼容分支）。**
- **`adapters/tool_mapping_meta.json`**：Block A/C 需要的 `ct-*` 本地调用映射（`ct-literature`/`ct-registry`）；`request_upload` 为内建特殊类型不在表内。
- **测试**：`adapters/tests/test_pipeline_client.py`（7 例：R1 委派/解析/红线闸阻断/上传/下载/billing 透传）、
  `adapters/coze/tests/test_stage_envelope.py`（8 例：双模判定/字符串字段/R2/gate 映射）。

### Notes
- coze 端 `meta_analysis.py` 双模分支为**代码完成、待部署**状态（本地无 langgraph 运行环境，无法在此端到端跑；逻辑由 `stage_envelope` 单测覆盖）。部署前须按 coze_contract §12.4 用老 `run_meta` 风格请求 POST `/run` 断言仍含 `result` 且 `json.loads(result)` 含 `status`/`stats`/`figures`。
- P0 仅收口骨架；Block A/B/C 各阶段的具体逻辑（选题闸门、检索委派、GRADE、过度声明检测、初稿生成、参考核验）为 Phase 1–3 内容，经同一 `run_stage` 信封接入。

---

## [2.3.2] — 2026-08-30 — precomputed 轨 validate 字符串列误判修复

### Fixed
- **`scripts/extract_assist.py` `validate` 字符串列误判**：`precomputed` 类型的唯一 `str` 列 `effect_type`（取值如 `lnOR`/`SMD`）被旧逻辑当作数值列校验，调 `_to_num` 误报「非数值且非 NR」，导致所有 `precomputed` 轨道提取表无法通过 `validate`、卡死在计算轨入口。新增 `if kind == "str": continue` 透传分支（与协变量 `str` 透传逻辑一致），仅对 `int`/`float` 列做数值校验。`precomputed` 轨现在可正常 `validate` → `stamp --confirm` → `run_meta`。

---

## [2.3.1] — 2026-08-30 — 抽取链 P0 三修复（BCG 案例打脸：协变量/多臂/零事件）

> **触发**：用 BCG 疫苗预防结核病（Colditz 1994 经典 13 项 RCT）走完整「选题→检索→筛选→提取→合并」
> 全链路，实跑暴露出抽取链 3 个会被真实数据打脸的缺口，全部为 P0。已用真实 BCG 数据做端到端回归：
> 含协变量 + 单零单元的干净版（12 项 RCT）经 coze 复现 pooled RR=0.532 (95%CI 0.365–0.776)、I²=84.4%，
> 与教科书结论 RR≈0.58/I²≈87% 一致。

### Fixed
- **P0-1 协变量列缺失**（`scripts/extract_assist.py`）：原 binary 模板只有主结局列，纬度/分配方法等在
  提取阶段即被丢弃，亚组/元回归做不了。新增 `scaffold --covariates "latitude,allocation,vaccine_type"`
  动态追加协变量列，类型自动判定（数值型 float / 分类型 str），provenance 记录协变量 schema；
  `validate` 对协变量做类型/范围校验。
- **P0-1 协变量透传**（`scripts/build_request.py`）：CSV 中核心结局列之外的「额外列」（协变量 + arm 臂标识）
  自动透传进 coze payload；数值协变量 float 强转、分类/臂列字符串透传（`_classify_non_numeric_cols`）。
  同时修复 CSV 读取用 `utf-8-sig` 剥 BOM——否则首列 `study` 变 `\ufeffstudy`、study 值丢失（BCG v1 即已潜伏）。
- **P0-2 多臂独立性**（`scripts/extract_assist.py`）：binary/continuous schema 加可选 `arm` 臂标识列；
  `validate` 检测同一 study 多行（多臂/多对照）→ 提示独立性风险（直接全纳破坏独立性、低估 SE，建议 RVE 或按臂拆分）。
- **P0-3 零事件校验**（`scripts/extract_assist.py`）：`validate` 检测零事件单元——
  单零（一方 event=0）告警（引擎 +0.5 连续性校正可算）；**双零（两组皆 0）硬错误**（该研究 RR/OR 完全无信息，
  metafor::escalc 会抛 `invalid 'pos' value` 崩溃，实测确认）→ 须剔除或改用 `--measure RD`。
- **`references/data_templates.md`**：binary 表增补 `arm` 列、协变量列用法、零事件/多臂校验说明。
- **P0-4 抽取表 type 推断误把选填列当必填**（`scripts/extract_assist.py`）：`validate` 的 type 推断原用整张 schema 列集合（含 opt 列 `year`/`arm`）做 `issubset` 判定，导致用户按 `data_templates.md` 必填列（不含 `arm`）填表时被判「无法从列名推断 Type」。改为只匹配**非 opt 必填列**（binary 必填 = study/n_exp/event_exp/n_ctrl/event_ctrl），选填列存在与否不再影响推断；缺真正必填列仍正确拦截（rc=2）。回归 `[1b] validate ok` 由 FAIL→PASS，全回归 11/11。

---

## [2.3.0] — 2026-08-30 — 上游编排 + 数据提取助手（human-in-the-loop）

> **触发**：用户要求把 meta-analysis 从「只算合并效应量」升级为覆盖 Meta 全链路的编排器
> （方向判断 + 文献检索整理 + 文献清理 + 数据提取 → 直通计算轨）。经可行性核对，①方向判断
> 本技能已有雏形（topic-selection）、②检索去重归 ct-literature、③初筛已有
> prisma_bridge/agent 层；唯一缺且最难自动化的是「纳入研究 → Type 1/2/3 数据」这条抽取链，
> 故本次只新增「抽取助手 + 人工核验闸」，不把检索/清洗塞进本技能。
>
> **本版本已通过线上回归**：`tests/regression_live.py` 全绿（守卫拦未核验 / coze 真算出真实 RR / 本地闭环）。
> 实际发布到 GitHub / ClawHub / SkillHub **仍需用户确认后执行**（红线：推送/发布一律先停下等确认）。

### Added
- **`scripts/extract_assist.py`（数据提取助手）**：`scaffold` 按 Type 1/2/3/3b/3c/3d/3e 生成
  空白抽取表（仅含数据列，可直接喂 `run_meta.py --data`）+ 同伴 `<csv>.provenance.json`
  （`verified_by_human=NO`）；`validate` 按 `data_templates.md` schema 校验列名/数值合理性
  （event≤n、CI 方向、r∈[-1,1]、缺失标 NR）；`stamp --confirm` 在人工核验后把
  `verified_by_human` 置 YES；`types` 列出支持的 Type。纯 stdlib，对齐 scripts/ 约定。
- **`scripts/extraction_guard.py`（人工核验闸）**：`check_verified(data_path)` 检查同伴
  provenance 的 `verified_by_human`；未核验 → 拦截；无同伴文件 → 视为人工手搓 CSV 放行；
  非 CSV（内联 `--data-json`）→ 跳过。返回 `(ok, reason, status)`。
- **`run_meta.py` 接入守卫**：入口新增抽取核验闸，未核验提取 CSV 返回
  `META_STATUS=unverified_extraction` 并非零退出（exit 3）；新增 `--trust-data` 显式担责兜底
  （仅用于确认可信的存量/手搓 CSV）。
- **`references/upstream_orchestration.md`**：上游编排总文档——把方向判断(topic-selection) →
  检索去重(ct-literature) → 初筛+PRISMA(prisma_bridge) → 数据提取(extract_assist) → 计算轨
  (run_meta) 串成命令链，含接缝护栏与 `included_records≠included` 陷阱说明。
- **SKILL.md 升级定位**：summary/description 增补「上游编排」；triggers 加
  `系统综述全流程`/`从检索到meta分析`/`文献检索后做meta`/`检索→筛选→提取→合并`/`数据提取 meta`；
  新增 §2.3 Upstream orchestration；§6 增补数据提取红线（未核验禁止直灌）。
- **`references/systematic_review_fullflow.md`（全流程模式 playbook，@skill 入口）**：把
  meta-analysis 作为「编排器」的统一入口落为可执行 playbook——列出触发词、Stage 0 启动确认、
  5 阶段命令链（选题→ct-literature 检索→初筛+PRISMA→抽取助手→run_meta）、两道不可跳过的人工闸
  （Stage 3 最终 `included` 数 / Stage 4 `stamp --confirm`）、失败与边界处理。
- **SKILL.md 新增 §2.4 系统综述全流程模式**：把 full-flow 触发意图映射到
  `systematic_review_fullflow.md`，并再次声明两道人工闸与「不新增 classify 任务类」的定位。
- **triggers 扩充**：加 `系统综述全流程模式`/`系统综述流程`/`系统综述一站式`/`meta 全流程`/`全流程meta`/
  `从选题到meta分析`/`从选题到合并效应量`/`systematic review workflow`/`systematic review full pipeline`/
  `full meta pipeline`。
- **`extract_assist.py scaffold --studies-file`（纳入清单自动预填）**：新增 `--studies-file`，
  读取 Stage 3 人工确认的最终纳入清单（`.json` 数组 / `{"included":[...]}` / `{"studies":[...]}`，
  或 `.txt`/`.csv` 每行一个），自动预填 study 列；与 `--studies` 合并去重；来源记入同伴
  `.provenance.json` 的 `included_list_source` 以便溯源。缺失文件报错退出（exit 2）。
  全流程 playbook Stage 3 在人工闸确认后写 `included_studies.json`，Stage 4 用
  `--studies-file included_studies.json` 自动预填，免去手动重列研究名。
- **coze 入参 `user_language` 备用字段**：`build_request.build()` 现向 coze 入参 `params` 注入
  `user_language`（中文 `zh` / 英文 `en`），供 coze 端决定报告/图表文案语言，**属备用输入、不强制覆盖
  coze 自身判定**。支持「内容级」自动检测 + 显式覆盖：
  - **内容级判定（默认）**：未传 `--language` 时按【输入 query 文本】判定（含 CJK→zh，纯英文→en），
    解决「中文系统 + 英文输入」被 `i18n._current_lang()`（系统 locale）误判 zh 的盲区；query 为空时
    才回退系统 locale。`run_meta.py` / `build_request.py` 均新增 `--language zh|en|中文|english|...`
    入参，可显式覆盖（中英多写法归一化：中文语境→zh、英文→en、未知值原样小写透传），显式参数最高优先。
  - 不改 `i18n._current_lang()` 本身（那是全库 UI 文案按系统语言显示用的契约，跨技能共用）。
  - **2026-08-30 重构**：meta-analysis 侧不再自带 `_LANG_ALIASES` / `_normalize_language` / `detect_text_language` 三件套，改为经 `importlib` 以别名加载 ct-base 共享 `i18n`（`ctbase_i18n`），由 `ctbase_i18n.resolve_user_language(query, override)` 统一实现三级判定；单一事实来源上移 ct-base（详见 ct-base CHANGELOG 同日记）。

### Changed
- **AGENTS.md**：新增 §8 Upstream Orchestration & Extraction Guard；`scripts/` 目录结构补两条新脚本。

### Safety / 红线
- **数据提取不可无人值守直灌**：全文获取受限（付费墙）、效应量抽取精度属医学关键、系统综述要求
  双人独立抽取+仲裁。抽取环节强制 human-in-the-loop；任何 `extract_assist` 生成、未 `stamp --confirm`
  的 CSV 一律被 `run_meta` 拦截至 `META_STATUS=unverified_extraction`。

---

### A 档（并入 2.3.0）：综述流程类路由 + RoB/RoB Summary 修复 + PRISMA 投稿级

> **触发**：ct-update 对 meta-analysis 的 10 条 P1 建议中 C/D/F/G/H/I 共 5 项路由/代码
> 缺口，配合 R metagear 0.7 本地实测结论（仅取 plot_PRISMA 一个能力就够本）一次性收口。
>
> **本档随 2.3.0 一并发布**（与 B 档同属一次未发布累积）。部署/发布按 ct-base 发布规约走，
> 发布前已通过线上回归（HTTP 200 ≠ 任务成功，详见 ct-base LRN-20260817-002）。

### Added
- **classify 路由综述流程类 task（6 个）**：`scripts/classify.py` 新增 `prisma_flow` /
  `prisma_checklist` / `rob2` / `rob_summary` / `grade` / `ipd_meta` 路由。原实现
  只识别 6 个效应量 task，综述类一个不认——7 句相关请求 100% 误判为
  `pairwise_meta`。最危险的一例是「对这 12 项研究做偏倚风险评价」：句中含
  「研究」+ 数字，绕过了旧的 `has_data` 闸门，直接提交 coze 静默返回答非所问
  的合并效应量（不报错、给错答案，属最危险的一类误路由）。新路由对
  `REVIEW_TASKS` 走独立缺参判定：`prisma_flow` 缺数字 → 要 8 个筛选计数；
  `prisma_checklist` / `grade` → 纯 params 全默认跑；`rob2` / `rob_summary` 缺
  judgement 取值词 → 要 Study+D1..D5 判定表。
- **绕过「PRISMA 2020」版本号陷阱**：新增 `_has_prisma_counts` 剥离 `prisma 20xx`
  版本短语后再判数字，否则「画 PRISMA 2020 流程图」的「2020」会被当成筛选
  计数（带全 0 参数出空图）。
- **`run_task.R` 注册 `rob_summary` task**：`plot_rob_summary` 早已实现但**从未
  注册 task**，用户无从触发；现独立 task 出图，与 `rob2` 同数据契约。
- **`metagear` 0.7 重引入核心依赖**：仅取 `plot_PRISMA`（配色 `cinnamonMint`
  接近 PRISMA 2020 statement 官方推荐、纯 grid 矢量、零 GUI 依赖，coze Linux
  无头容器可直接跑）。净新增 0 个 R 包（metafor / Matrix / MASS / stringr
  均已在），安装走腾讯 CRAN 镜像 4.4 秒装完。
- **`plot_prisma_flow` 改用 metagear::plot_PRISMA 矢量直出**：返回 `draw`
  thunk，由 `.render_fig` 在 svgstring 设备开启时调用 → 纯矢量 SVG，零
  base64 栅格、零 png 包依赖。
- **结果文字模板 `references/rob2-narrative.md`**：配合 `rob2` / `rob_summary`
  产出的 traffic-light 与 summary bar，提供投稿可贴的整体/逐域/GRADE 联动
  /敏感性分析/读图说明英文段落模板。

### Changed
- **coze 本地镜像目录改名 `adapters/coze_project/` → `adapters/coze/`**：
  对齐 ct-base / ct-advisor / ct-registry / ct-samplesize 的统一约定（此前
  meta-analysis 是 ct 系列里唯一用 `coze_project` 的技能）。**纯本地镜像路径
  变更**，coze 远端目录结构不受影响，无需因本项重新部署。同步更新 9 个文件的
  路径引用：`.gitignore` / `.clawhubignore` / `AGENTS.md` / `adapters/README.md` /
  `adapters/coze/DEV.md` / `adapters/_dev/local_engine.py` / `learnings.md` /
  `references/r_packages.md` / `references/ADVANCED.md` / `ADVANCED_zh-CN.md`。
- **`plot_prisma_flow` design 参数白名单**：`design` 仅 7 个合法值
  （`classic` / `cinnamonMint` / `sunSplash` / `pomegranate` / `vintage` / `grey` /
  `greyMono`，取自 `metagear::designList`）。传非法值主动校验并回落
  `cinnamonMint`，不依赖 metagear 的 warning（它会静默回落到 `classic`）。
- **`plot_prisma_flow` 画板 7×9 英寸竖版**：匹配四阶段纵向布局（原 8×6 横版
  把图压扁）。支持 `fig_width` / `fig_height` 覆盖。
- **`plot_prisma_flow` 新增 2 个计数 + 3 个可选参数**：`other_sources` /
  `reports` 计数（与 `included` 不等时才出报告分支）、`design` / `colWidth` /
  `excludeDistance` 可选。**8 个原计数参数接口与 case40_prisma_flow.json 完全
  兼容**。
- **`grade` 分支兼容无 data**：原无条件 `df <- .build_df(data)`，空 data 时
  直接 stop；改为 `k_grade` 优先取行数，缺则回落 `params$k`。GRADE 是纯
  params 评分（5 降级 + 3 升级因素全走 params），研究数 k 仅用于 notes 文案。
- **`rob2` 分支删除 `check_pkg("robvis")` 守卫**：交通灯图自 2026-08-18 起
  已改 ggplot2 自绘，代码零调用 robvis；该守卫属**幽灵依赖**——只会在
  robvis 未装时把本可正常出图的任务拦死。`r_packages.txt` 同步把 robvis
  注释为「可不装」。

### Fixed
- **`plot_rob_traffic` / `plot_rob_summary` 列名大小写归一**：原只把 `nm`
  小写、`df` 的 names 不变，导致 `setdiff(names(df), study_col)` 对 "Study"
  列失效——Study 被当成域列混入，触发「replacement has 0 rows」。生产路径
  此前靠 `.build_df` 预先 tolower 才侥幸绕过，自身不自洽。
- **`.rob_domain_labels` 域标签映射长期失效（2026-08-20 声称修复实为假象）**：
  映射表 names 为大写 `D1..D5`，列名经归一后为小写 `d1..d5`，直接
  `labels[dom]` 全落空为 NA → 回退裸列名。改为 `labels[toupper(dom)]` 后
  三工具（ROB2 5 域 / ROB1 6 域 / ROBINS-I 7 域）的 traffic + summary 图
  全部正确显示「Randomization」等标准域标签。两张图 x 轴自此同源。
- **`plot_rob_summary` 改 robvis 风格百分比堆叠**：原 facet_wrap 分面计数
  柱图与 robvis::rob_summary 风格不同，改为 `position="fill"` +
  `coord_flip()` 的百分比堆叠横条，`scales::percent` 标 y 轴。Judgement 由
  字母序改为固定 `.ROB_LEVELS`（Low → Some concerns → High → Unclear →
  Critical），避免堆叠与图例按 High/Low/Some 乱序。
- **图标题中点 `·` (U+00B7) 在 svglite 下被注入占位字符「B7」**：traffic 与
  summary 标题改为 ` - `（更通用，字体回退无虞）。
- **`adapters/_dev/local_engine.py` 引擎路径恒不存在**：`_HERE` 指向
  `adapters/_dev/`，却直接 `join(_HERE, "coze_project", ...)` 拼出
  `adapters/_dev/coze_project/src/r_engine` —— 缺一级 `..`，本地引擎必然抛
  「缺失」。改为 `normpath(join(_HERE, "..", "coze", "src", "r_engine"))`。
  （该文件自 2026-08-26 起已不在运行路径，属潜伏 bug，非回归。）
- **「**1A 档执行**」补强：先实测后判断原则落实**：本次 4 笔早期判断
  （「metagear 不要装」「fig_* 可用」「PDF_download 可用」「impute_missingness
  可插补」）均被本地 R 4.6.1 + 腾讯镜像实测推翻——已写入
  `LRN-20260830-001/002/003`，ct-base §16 后续评估必须先做本地实测。
- **调用方约束：query_origin 发送层硬守卫（2026-08-30 实测 3 条空归因）**：
  飞书后台 08-30 仍出现 3 条 `query_origin` 为空记录（ID 3263/3270/3282，13:57/14:06/
  14:53），载荷为 `coze_contract.md` §2 示例（2 研究 A/B），判定为**裸 POST /run
  复制契约示例、body 缺 query_origin**——绕过了 2.2.28 客户端自动注入。修复（调用
  方约束，非 coze 端）：① `coze_client` 新增 `_assert_query_origin`，在 `run_meta`
  序列化出站前硬校验 `query_origin` 为 `[debug:]sha256:<64hex>`，缺失/空/非法直接
  `ValueError`（覆盖主端点与回退端点）；② `scripts/build_request.py` 的 build 产物
  `request.json` 自动注入有效 `query_origin`，即使被手 POST 也不产生空归因；③ 契约
  文档 §2 + 示例载荷（`req_test.json` / `meta_request*.json`）补 `query_origin` 占位
  并加「裸调必须带归因」显式条款。**根因在调用方、不在技能代码**——所有经
  `run_analysis` / `scripts/run_meta.py` 的路径本就带归因。

### Documentation
- **`references/review_workflow.md` 完全重写**：删 7 段**虚构 API**——
  `prisma_flow` / `export` / `screen_titles` / `retrieve_pdf` / `retrieve_pmid` /
  `extract_digit` / `impute_ml` 在 metagear 中**不存在**，是历史版本的幻觉
  文档。新结构：§0 能力边界（明确支持/不接入/转交）+ §1 PRISMA 真实可复现
  脚本 + §2 agent 行为层筛选 + §3 数据提取表模板 + §4 缺失值（如实说明
  `impute_missingness` 只返汇总表、不是插补）+ §5 引用。
- **`references/rob2-narrative.md` 新增**（见 Added 段）。
- **周边文档 metagear 条目统一修正**：`references/ADVANCED.md` /
  `ADVANCED_zh-CN.md` / `references/references.md` / `AGENTS.md` /
  `adapters/coze/AGENTS.md` / `setup_packages.R` —— 版本号统一为
  `≥0.7`、用途限定为 plot_PRISMA、移除「已移除」历史标注中的 metagear、
  补「2026-08-30 重引入」说明。

### Verified（本地，未线上回归）
- **prisma_flow 端到端 19/19 PASS**：case40_prisma_flow.json 原参数零改动
  兼容；矢量直出（零 base64 栅格）；7 个 design 全部出图；非法 design 回落
  正确；4 种边界（最简/全 0 / reports≠included / colWidth 自定义）均通过；
  缺包降级报错含包名。
- **rob2 / rob_summary 端到端 21/21 PASS**：3 工具 × 2 图共 6 张图全部出图、
  域标签全部命中、无裸 D 列名、summary y 轴含百分比。
- **路由回归 19/19 PASS**：综述流程类 12 例全正确（含「PRISMA 2020」剥离
  版本号陷阱），效应量类 7 例零回归。

### 部署注意
- **coze 端需重新部署**（`run_task.R` 的 `grade` / `rob2` / `rob_summary` /
  `prisma_flow` 分支与 `advanced_functions.R` 的多个函数均有改动）。
- **`r_packages.txt` 需补 metagear**（若镜像未预装，docker build 时会失败）。
- **部署后强制线上回归**：HTTP 200 ≠ 任务成功（见 LRN-20260817-002），
  必须实际触发各 task 并核对 SVG 字面与统计输出；建议按 `verify_meta_full.py`
  增加 `prisma_flow` / `rob2` / `grade` 三个新 case。

### Added (2026-08-30 PRISMA 检索前端桥接)
- **`scripts/prisma_bridge.py`（新）**：ct-literature `.merged.json` → meta-analysis
  `prisma_flow` 请求信封的**唯一 sanctioned 胶水**。自动填 4 字段
  （`records`=`identified_records`+`duplicates_removed` / `duplicates` / `screened` /
  `excluded_title`），其余 5 字段（`other_sources` / `assessed` / `excluded_elig` /
  `included` / `reports`）显式标 `[MANUAL]` 留空待人工补。强制打印
  「机器初筛，非人工终审」声明；`included` 绝不由机器初筛数映射（防方法学错误流程图）。
- **`references/review_workflow.md` §1.5 新增「计数来源与人工补齐」**：9 字段来源分级表
  （自动/人工/语义错位）+ 推荐工作流 + 强制声明，防 agent 过度承诺「全自动检索」。

---

## [2.2.30] — 2026-08-29 — coze 回传结构迁移 §20.8 模式 B（完整 JSON 单文件外置，删除 manifest 外置）

> 触发：ct-base §20.8 由「两种已批准模式（A manifest / B 完整 JSON 单文件）」收窄为**仅模式 B**（2026-08-29 用户拍板删除模式 A）。meta-analysis 原 coze 端实现模式 A（manifest 外置），现迁移到模式 B 以对齐单一标准；coze 端需重新部署。

### Changed（coze 端 `adapters/coze_project/src/graphs/nodes/meta_analysis.py`）
- **删除 `_externalize_to_manifest`**（含 `_collect_always` / `_collect_stats` / `_move` / `_discard_fallback` 及其 `_coze_manifest` 契约），整体替换为 §20.8 模式 B 三函数：
  - `_build_inline(out)`：内联轻量信封 = 删 `figures`/`repro`，其余字段（status/stats/warnings/notes/task）保留，恒内联 `_coze_version`。
  - `_trim_inline_to_limit(inline)`：内联超 4000 时从大到小丢 `stats` 子块直到 < 4000；**循环条件与 narrative 额度均把 `_coze_truncated` 标记自身大小计入预算**，末尾兜底逐条缩减标记，确保最终（含标记）恒 < 4000（沿用 ct-samplesize v5.3.14 的 ⑤ 修复）。meta-analysis 信封无顶层 narrative，故无 narrative 截断分支。
  - `_externalize_full(out, timeout=90)`：完整信封整体写单个 S3 文件（md5 摘要命名），内联挂 `_coze_full = {storage:"s3", url}`；S3 不可用/失败/超时降级无 `_coze_full` 的内联删减版。90s daemon 超时守护不变。
- `meta_analysis_node`：`_externalize_to_manifest` → `_externalize_full`，并在调用前注入 `out["_coze_version"]`（恒内联诊断透出，本地不再比对）。
- 常量：`_CORE_INLINE` 由 `{status,task,_coze_truncated,_coze_manifest}` 改为 `{status,task,_coze_truncated,_coze_full,_coze_version}`；新增 `_COZE_ENVELOPE_VERSION` / `_S3_URL_EXPIRE`；删除 `_EXTERNALIZE_MIN_BYTES`。

### Changed（本地 `adapters/coze_client.py`）
- 新增 `_fetch_full_json(parsed, timeout=30)`：优先经 `_coze_full` 下载完整 JSON 作分析源（含 figures/repro，零删减）；失败/无链接返回 None。
- `run_meta` 解析路径：`_fill_external_svgs(parsed)` → `full = _fetch_full_json(parsed); parsed = full if full is not None else _fill_external_svgs(parsed)`。内联删减版仅作飞书日志/老版本兼容。
- `_fill_external_svgs` 降级为**兜底**入口（仅当响应无 `_coze_full` 的旧 coze 响应才走 manifest 重组 / 旧 figures[].url·repro.url 回填），保留 `_reassemble_from_manifest` 向后兼容。
- `health()` 探测包**注入 Bearer token**：此前探测包无 token，被 coze 网关在鉴权层挡回 401、请求根本进不了 langgraph，probe 短路逻辑实际是"睡着"的（靠 401 兜底判定可达，但 probe 短路从未生效）。现经 `_resolve_token` 取 token 后挂 `Authorization` 头，probe 能越过鉴权真正进图、在 `meta_analysis` 节点短路（不调 R 引擎、不写飞书），既验证可达性又零算力零日志污染。token 解析失败 / 返回空时降级为无 token 探测（401 仍算可达，判定语义不变）。coze 端无需改动（probe 字段已于 2.2.28+ 引入）。

### Verified
- `verify_meta_full.py`（FakeS3 + file:// 全链路）**21/21 PASS**：① `_externalize_full` 内联 < 4000、无 figures/repro、含 `_coze_full`，S3 完整数据含 figures/repro 且 svg 全等；② 本地 `_fetch_full_json` 经 `_coze_full` 还原完整 JSON（figures/repro 全等、剔除 `_coze_full`）；③ 旧 `_coze_manifest` 内联 → `_fetch_full_json` 返回 None（降级旧契约）；④ S3 不可用 → 降级内联删减版（无 `_coze_full`）< 4000；⑤ 内联超 4000 → 丢 stats 子块、含标记后恒 < 4000。
- 两侧 `py_compile` 通过；coze 端已无 `_externalize_to_manifest` 残留（本地 `_reassemble_from_manifest` 仅旧响应兜底保留）。

### 部署注意
- **coze 端已改动，必须重新部署**（旧 `20260829a.zip` 不含本次模式 B 迁移）。升级包见 `meta-analysis_coze_2.2.30.zip`。

## [2.2.29] — 2026-08-29 — 契约漂移检测：移除版本号比对（对齐 ct-base §20.9 修订）

> 触发：ct-base §20.9 由「版本漂移 + 结构漂移」双信号修订为**仅数据内容/结构不一致触发**——版本号不同不再提醒。

### Changed
- **`_assess_contract` 移除版本漂移检测**：删除 `EXPECTED_COZE_ENVELOPE_VERSION` 常量与 `_coze_version` / `_contract_version` 的比对分支（原第 4 项）。版本由 coze 端随发布同步，本地不比对 —— 任何**仅版本号差异**（无数据内容/结构变化）一律不提示，避免无谓打扰。检测信号自此只剩一条：**coze 返回的数据内容/结构与本地消费接口是否一致**（字段别名自适应归一化）。
- **零噪音边界写入 docstring**：`_coze_version` 高于/低于本地、coze 未注入版本标记、结构一致且无别名映射 —— 三种情况均不提示。

### Unchanged（刻意保留，勿"顺手改回去"）
- 结构漂移自适应（`quality_gate` / `checks` / `pooled` / `figures` 别名映射）、`_needs_upgrade` / `_contract_drift` 机器标记、`rendering.py` 的 HTML 横幅唯一出口 —— 均按 ct-base §20.9 原样保留，横幅文案本就只描述"结构不一致"，无需改动。
- meta 的 coze 端本就**未注入** `_coze_version`（实测 `grep -r _coze_version adapters/coze_project/src` 无匹配），故本次是纯本地清理：**coze 端无需改动、无需重新部署**，已出的 `20260829a.zip` 不受影响。

### Verified
- `_assess_contract` 单测 9 例全通过：版本更高 / 更低 / 旧标记 / 缺标记 / 结构一致 → 全部 **零 drift**；`pooled` 别名 / `qgate` 别名 / `figures` dict→list → **触发 drift**；「版本更高 + 结构漂移」混合场景**只报结构**，断言文案不含"版本"字样。
- `py_compile` 通过；`deploy_retest --offline` / `--mock` 各 46/46 回归通过。

---

## [2.2.28] — 2026-08-29 — 归因不再为空 + 短窗幂等去重

> 触发：飞书后台发现 02:54 两条几乎同时、且 `query_origin` 均为空的 `pairwise_meta` 记录（数据完全相同，仅 `figure.plots` 差一个 `funnel`）。

### Fixed
- **空归因（主因）**：`query_origin` 此前只在 `run_analysis.py` 计算并作为参数传入；直接调 `coze_client.run_meta` 的路径（`__main__` 自测入口 / `coze_integration_test` / `deploy_retest --live` / 外部脚本）都不传 → coze 端 `state.query_origin or ""` 兜底成空串。后果不止"日志无法溯源"——**空值会绕过按 `query_origin` 计的限流**。现把计算下沉为 `coze_client._default_query_origin()`，`run_meta` 在入参为 `None` 时自动填充；`run_analysis.py` 改为复用同一函数（单一实现，消除两处逻辑漂移）。
- **调试/冒烟流量污染生产日志表**：`coze_integration_test.run_one` 与 `deploy_retest.call_one` 原为裸 POST（46 个 case 全空归因）。现统一经新增的 `with_trace()` 注入归因 + `request_id` + `_debug: true`，归因带 `debug:` 前缀——飞书归因列可直接筛出非生产流量。

### Added
- **短窗幂等去重**：对 `(task, data, params, figure)` 做 SHA-256 指纹（忽略 `request_id`/`_debug`/`query_origin` 等观测字段），`COZE_META_DEDUP_WINDOW`（默认 60s，≤0 关闭）内同指纹直接复用上次结果、不再打 coze。命中时结果附 `_dedup_hit: true` + `_dedup_original_request_id`。**仅缓存 ok/warn 结果**，失败不入缓存（避免偶发失败毒化窗口内的真实重试）；上限 32 条、按最旧淘汰；返回深拷贝，调用方互不影响。作用域为进程内（与 `_acquire_rate_limit` 同级；跨进程需文件锁，未实现）。
- **请求追踪 ID**：每次调用生成 UUID 写入 `request_id`，随结果以 `_request_id` 返回——相邻两条飞书记录可据此区分「两次独立调用」还是「一次调用的重放」。coze 端 `state.py` 未加该字段（pydantic `extra='ignore'` 静默忽略，实测不报错），故**暂不进飞书**；如需落表须改 `state.py` + `feishu_write_node` 并重新部署（发布动作，待授权）。

- **连通性探测标记 `probe`（coze 端消费 → 需重新上传部署包才生效）**：客户端 `health()` 每次启动都 POST 一次 `/run`（SKILL.md 要求启动探测），此前 coze 端照单全收 → 飞书日志表被空 `querystr` 记录污染，排查时无法与真实调用区分。现 `health()` 探测包带 `probe: true` + `debug:` 归因；coze 端 `meta_analysis` 节点识别后**直接返回探针结果、不调用 R 引擎**，`feishu_save` 节点**跳过飞书写入**。兜底：老客户端发 `{}`（无 `probe` 字段）时，靠 `data`/`params`/`figure` 三者全空的"空信封"特征识别。规则抽在 `src/graphs/nodes/_skip_rules.py`（**零第三方依赖，可本地单测**——节点模块依赖 langchain/langgraph，本地 import 不了）。
  - ⚠️ **未部署前不生效**：老 coze 端不认识 `probe` 字段（pydantic `extra='ignore'`），仍会写一条记录，但带 `debug:` 归因前缀可筛出，不再是空白归因 —— 平滑过渡，两侧独立发布互不影响。

### Removed
- **`coze_client.py` 的 `__main__` 自测入口**：删除原「硬编码 sample 调 `run_meta`」逻辑 —— 它就是飞书 08-29 两条空归因记录的来源（注释还停留在「需要本地已启动 coze 服务」的年代，端点早已换成公网，于是调试动作直接往生产日志表写记录），且与 `case1_pairwise_binary` 完全重复、无独立价值。CLI 保留 `--health` 子命令（仅探测可达性，不发起分析请求）；无参数时只打印用法、**零副作用**。冒烟改用 `python scripts/run_meta.py <request.json>`（走生产路径，自动带归因 + 去重）。

### Changed
- **调用方收敛（4 入口 → 3 入口，凭据/端点重复逻辑清零）**：`coze_integration_test` 与 `deploy_retest` 不再自建 `resolve_token` 与 `DEFAULT_ENDPOINT` 字面量，统一 `from coze_client import _resolve_token / _endpoint / DEFAULT_ENDPOINT`（保留 import 失败时的等价兜底实现）。端点从「模块导入时固化」改为**运行时**解析，与生产路径行为一致——旧写法在运行中途改 `COZE_META_ENDPOINT` 时生产生效、测试不生效。
- **`--endpoint` 默认留空**，由 `_endpoint()` 运行时读取；`deploy_retest` 报告记录**实际**端点（旧写法会把 `endpoint` 写成空字符串，事后看不出这一轮跑的是哪个端点）。
- **语义差异就地固化注释**：测试侧 `_post`（300s / 捕获 HTTPError 继续跑 / payload 原样发送）与生产侧 `_post_run`（600s / 抛异常触发端点回退 / 归一化+脱敏+强制 svg+指纹去重）的差异是**有意保留**的 —— 测试必须绕过客户端加工才能测到 coze 端真实行为（典型：`run_meta` 的 `byvar→subgroup` 归一会让「coze 只认 subgroup、byvar 静默失效」这个坑永远测不出来）。差异已写成对照表注释，避免后人误「统一」。
- 文档同步：`references/ADVANCED.md` / `ADVANCED_zh-CN.md` 的自测命令由 `python adapters/coze_client.py` 改为 `--health` + `scripts/run_meta.py`。

### Verified（mock + 真实 coze 链路）
- 归因：`sha256:<64hex>` 71 字符；`debug=True` → `debug:sha256:...`；`run_analysis` 与 `coze_client` 同源一致。
- 指纹：换 `request_id` 同指纹、换 `figure.plots` 不同指纹。
- 去重：第二次完全相同调用 **POST 次数保持 1**（`_dedup_hit=True`，复用自首次 `request_id`）；改 `figure` 后正常发起第二次；失败结果不入缓存；窗口置 0 可关闭。
- 真实链路：`python adapters/coze_client.py` 端到端 `status=ok`，统计值与飞书历史记录逐字一致（pooled logOR −0.626 / OR 0.5347，k=2，I²=0），coze 端对新增字段无 422/报错。
- 编译：`py_compile` 四个改动文件全通过。
- 收敛后回归：`python adapters/coze_client.py`（无参数）零副作用、不发请求；集成测试端点/token 解析走 `coze_client` 实现（端点 `https://ct-meta.coze.site/run`、token 739 字符）；`deploy_retest --offline` / `--mock` 各 46/46 通过；`COZE_META_ENDPOINT` 覆盖在报告中生效（`https://example.invalid/run`）；屏蔽 `coze_client` 导入后兜底分支功能完整（token 739 字符、归因与主路径同源 `sha256:b8cae3d46…`）。
- `probe` 跳过规则单测 9 例全通过：probe / 空信封 / 空信封+probe（probe 优先）/ 真实 rows 请求 / 仅 params / 仅 figure / csv_path / `{"rows":[]}` / 仅 colmap —— 前 3 例跳过，后 6 例**照常写入**（数据为空但结构完整的请求有排查价值）。
- `health()`：探测包实测 `{"probe": true, "query_origin": "debug:sha256:…"}`；端点不可达仍返回 `False`、4xx/5xx 仍视为可达 —— **判定语义未因包体变化而改变**。
- 部署包 `meta-analysis-coze_project-20260829a.zip`：70 文件 = 基准 69 + `_skip_rules.py`，内容变化 4 个（`state.py` / `meta_analysis.py` / `feishu_save_node.py` / `coze_contract.md`），无 `__pycache__`、无 `Rplots.pdf`，包内关键改动自校验通过，整包 MD5 `711446dbf3b2dd95de50482da3943cd9`。

### Fixed
- **部署包夹带 R 垃圾产物**：`src/r_engine/Rplots.pdf`（R 默认图形设备的落盘产物）此前会进部署包。打包时已排除，并同步排除 `__pycache__` / `*.pyc` / `.Rout` / `.RData` / `.Rhistory` / `.venv`。

---

## [2.2.27] — 2026-08-28 — coze 调用纪律 + 提示收敛 + 修复

### Added
- **coze 调用并发限流**：所有出站调用串行化，相邻两次间隔 ≥1s（`coze_client.py` 模块级 `threading.Lock` + 单调时钟；主端点 + 回退端点均约束；间隔可由 `COZE_META_MIN_INTERVAL` 覆写、≤0 关闭）。已写入 ct-base §20.10 全库通用标准。

### Fixed
- **classify 全角括号缺陷**：query 含全角括号（如 `region（Asia…）`）导致 subgroup 静默退化为 None；`_extract_subgroup` 前瞻断词补全 `（）`，亚组分析恢复（case5 实测 χ²=2.40, p=0.3008）。
- **质量评估版式**：`rendering.py` 质量卡由单列 `<ul>` 改为两列 `.kv`（左检查项带圆点、右着色状态词），所有案例两端对齐。

### Changed
- **coze 响应契约漂移 → 收敛到 HTML 唯一出口**：合并「版本漂移（`_coze_version`/旧 `_contract_version` 比对）」与「结构漂移（字段别名自适应）」为单入口 `_assess_contract`；检测到漂移时先自适应产出可用结果，**用户可见提示只在 HTML 报告顶部 `.banner` 出现一次**——删除 stderr 提示与 notes 污染；缺版本标记不误报。
- **端点回退提示同样收敛**：主端点 token 不一致回退备用端点时，提示仅写机器标记 `_coze_endpoint_notice` 并由 HTML 横幅渲染，不再写 stderr / 不污染 notes。
- **SKILL.md 正文翻译**：§5.1 残留中文说明按 ct-base 全英文规范译为英文（双语回显块 `当前分析设定 / Current analysis settings` 按要求保留）。

## [2.2.26] — 2026-08-28 — figures/repro 无条件外置（无论是否超 4000）

### Changed（coze 端 `meta_analysis.py::_externalize_to_manifest`）
- **figures/repro 恒外置**：不再「仅超限才外置」——**只要存在** svg 图元素 / repro.r，就**无条件**移出主返回体（原位替换为 `{storage:s3,type:block}` 引用），原值入 manifest。主返回体恒为「stats 数值 + manifest 链接」，更轻、更一致。
- **stats 子块按需外置**：figures/repro 移完后仍 > 4000，才依次把 stats 子元素从大到小移入同一 manifest，直到 < 4000。
- 契约不变：`_coze_manifest={storage:s3,url}` + manifest list `[{path,value}]`；本地 `_reassemble_from_manifest` **无需改动**。

### Verified（R 引擎 + mock HTTP server）
- 324 字符（未超限）+ 有 svg/repro → 两者**仍被无条件外置**，stats.pooled 内联，manifest 挂载；本地重组 **FULLY EQUAL=True**。
- 无 figures/repro + 未超限 → 原样、无 manifest、0 上传。
- 无 figures/repro + 超限 → stats 子块（big_str）外置为 block、k 保留、无丢弃。
- 本地/coze 衔接契约（path/占位/manifest 结构）与 2.2.25 完全一致，发布前已核验。

### 部署
- coze 端 `meta_analysis.py` → 重新上传 coze 包（`meta-analysis-coze_project-20260828e.zip`）。本地端无改动（契约未变）。

## [2.2.25] — 2026-08-28 — coze 截断收敛为「统一 manifest」方案（svg/r/stats 单文件外置）

### Changed（coze 端 `meta_analysis.py` + 本地 `coze_client.py`）
用户进一步提案的**统一 manifest 方案**取代 2.2.24 的「逐块外置 `_coze_externalized`」：

- **coze 端**：`_externalize_to_manifest()`（替代 `_externalize_figures`/`_externalize_repro`/`_trim_to_limit` 三套）。
  超 4000 时——先把 figures（含 svg）、repro（含 r 代码）移动为 `{storage:s3,type:block}` 引用，再依次把
  `stats` 下一级元素从**最大开始**移动，直到总量 < 4000；所有被移元素（含 path+原值）组成一个 list，
  **存为单个 S3 文件**，主返回体挂 `_coze_manifest={storage:s3,url}`。核心数值（pooled/heterogeneity/k/sm）始终内联。
- **本地端**：`_reassemble_from_manifest()`——GET manifest → 按 path 逐项写回 → **重组为原始 JSON**（含 svg/r/统计值），
  一次还原、零丢失。`_fill_external_svgs` 作为入口：优先走 manifest，无则回退旧契约（figures.url/repro.url/`_coze_externalized`）。
- **删旧代码**：`_externalize_figures`/`_externalize_repro`/`_trim_to_limit`/`_externalize_all_with_timeout` 及其
  `_coze_externalized` 逐块契约全部移除（用户约定：不留遗留实现）。

### Verified（单测 + mock HTTP server，含 svg/r 代码）
- 5652 字符超限体 → 外置 figures[0] 等块至 2861 字符（<4000），pooled/k 内联，manifest 挂载；
  本地重组后 **FULLY EQUAL = True**（figures[0].svg / figures[1].svg / repro.r / stats.subgroups 全部还原）。
- 未超限响应：原样返回、不产生 manifest、不上传 S3、svg/r 保持内联。
- 只移必要的块（够小就不动，如 repro 未触及）。

### 部署
- coze 端 `meta_analysis.py`（manifest 外置）→ 重新上传 coze 包（`meta-analysis-coze_project-20260828d.zip`）。
- 本地 `coze_client.py`（manifest 重组 + 兼容）→ 随技能本体发布。

## [2.2.24] — 2026-08-28 — coze 4000 截断改为「超限外置最大块」，零数据丢失

### Changed（coze 端 `meta_analysis.py` + 本地 `coze_client.py`）
用户提案的**泛化截断兜底**取代原「按优先级丢弃」：超 4000 时**不再丢数据**，而是迭代「找最大字符块 → 外置 S3 → 原位替换为 `{storage:s3,type:block,url}` 引用」，直到 < 4000，被外置路径记入 `out['_coze_externalized']=[{path,url}]`。

- **核心内联**：`status`/`task`/标记 + `stats` 容器（pooled/heterogeneity/k/sm/model…）整体永不外置，只下钻其子块（subgroups/quality_gate.checks/bias…）——关键数值始终内联可取。
- **兜底丢弃**：仅当 S3 不可用或所有可外置块已外置仍超限，才从大到小丢 stats 子字段并记 `_coze_truncated`（保 status 与最小数值核心）。
- **本地回填**：`coze_client.py` 新增 `_inflate_externalized()`（对称于 `_fill_external_svgs`），按 `_coze_externalized` 的 `{path,url}` 逐个 GET 回填还原；失败保留 url 并标 `_inflate_failed`，绝不中断分析。`run_meta` 在 `_fill_external_svgs` 末尾自动调用。

### Verified（单测 + R 4.6.1 真实数据）
- 单测：4169 字符超限体 → 外置 `stats.subgroups`、pooled/k 保持内联、回填后与原始完全相等（零丢失）。
- 真实 `_inflate_externalized` + mock HTTP server：从 url 正确还原 `stats.subgroups`，k/pooled 未动。
- R 引擎真实跑用户 7-RCT 亚组数据：figures/repro 外置后返回体 1783 字符 < 4000，`subgroups` 内联、Q_between=3.8522 完整。
- 用户案例截断根因（gate_json 冗余）已在 2.2.23 删除；本方案提供**任意胖字段**的通用兜底（不再依赖人工预判优先级）。

### 部署
- coze 端改 `meta_analysis.py`（外置逻辑）→ 需重新上传 coze 包（`meta-analysis-coze_project-20260828c.zip`）生效。
- 本地改 `coze_client.py`（回填）→ 随技能本体发布。

## [2.2.23] — 2026-08-28 — 修复亚组分析 coze 4000 截断裁掉 stats.subgroups

### Fixed（coze 端 R / Python，需重新上传 coze 部署包生效）
- **删除 `quality_gate.gate_json` 冗余**：`run_quality_gate` 不再生成 quality_gate 结构的字符串化 JSON 副本，`.quality_gate` 转发去掉 `gate_json`。该字段是 `checks/status/k/I2` 的重复，每次分析徒增 ~400 字符，是 `subgroup_analysis` 等 stats 较胖任务触发 coze 4000 字符截断、尾部裁掉 `stats.subgroups` 的主因。已 grep 确认本地渲染层无任何 `.py` 依赖 gate_json。
- **重排 `_trim_to_limit` 截断优先级**（`src/graphs/nodes/meta_analysis.py`）：亚组数值 `stats.subgroups / subgroup_test / bias` 列为高保真对象（亚组分析核心交付物），仅先丢 null 的 `notes/warnings/task` 与补充性 `stats.quality_gate`；超限时 subgroups 不再被优先丢弃。

### Verified（R 4.6.1 本地实测，非假设）
- 跑用户同款 7-RCT 按 PD-L1 分亚组案例：修复后 `stats` 序列化 979 字符、gate_json 消失，估算 coze 返回体 **~3459 < 4000**，`subgroups`（high/low 含 estimate/CI/k）完整返回。
- Python 单测：构造 4311 字符超限体，`_trim_to_limit` 丢弃顺序 `notes→warnings→task→quality_gate`，**subgroups 保留**、pooled/heterogeneity 完好。
- 注：本修复属 coze 端代码，未含在 SkillHub 2.2.22 发布包（coze_project 被 gitignore）；需重新打 coze 部署 zip 上传。

## [2.2.22] — 2026-08-28 — coze 部署复测全绿 + §8.5 门控两处修复

### Fixed（`tests/deploy_retest.py` 部署复测门控 §8.5）
- **图形 judge 只认内联 `svg` → 误杀所有图形案例**：coze 生产响应把 svg **外置为 S3 `url`**（不含内联 svg）。原规则「至少一个 figure 含有效 svg」会把图形任务全判空壳失败。改为**图形有效 = 内联 `svg` 或可达的外置 `url`**，新增 `_verify_fig_url()` GET 校验（HTTP 非 200 判死链失败，网络抖动不误杀）。
- **`_has_nan` 把 R 合法缺失标注 `"NA"` 当失败 → 误杀单组 meta / selmodel**：R 在 p 值缺省（单组无对照）、子模型 CI 缺失时输出字符串 `"NA"`，属预期缺失而非计算崩溃。改为**只拦 `NaN`/`Inf` 字面量 + 裸 NaN/Inf**，把 `"NA"` 移出失败判定。

### Verified（coze 主站点 `ct-meta` 部署后全量 `--live` 门控）
- **46/46 通过，0 失败**。确认本次 R 引擎修复已上云生效：
  - `diagnostic_meta` 现返回 sroc + **sens_forest + spec_forest**（escalc `PLO` 修复）；
  - `bayesian_pairwise` 森林图正常出图（`metafor::forest(x=)` 修复）；
  - netleague 中文映射、各方法默认图形扩充、函数化重构均随部署生效。
- 验证方法遵循 §20.2.5 / §20.6：开 `result` 字段真内容确认，不看 HTTP 200 假绿。

## [2.2.21] — 2026-08-28 — 端到端回归测试发现并修复 bayesian_pairwise 森林图 bug

### Fixed（`adapters/coze_project/src/r_engine/run_task.R`）
- **`bayesian_pairwise` 森林图不渲染（真实 bug）**：v2.2.20 新增的 bayes 森林图用
  `metafor::forest(yi = res$y, ...)`，但 **metafor 5.0.1 的 `forest()` 要求位置参数 `x`**（效应量），
  不认 `yi=` 具名参数（那是 `meta::forest` 的约定）→ 报 "argument 'x' is missing"，被 `.safe_fig`
  静默吞掉 → 返回 figures=0。改为 `metafor::forest(x = res$y, vi = res$sigma^2, ...)` 后正常出图。

### Verified（全量端到端回归，重构后引擎真实 R subprocess 跑 46 coze_cases + 4 增强 case）
- 全部 task 正确分发、`status ∈ {ok,warn}`；重构核心 task 逐项实测：
  - `metainc`（forest+funnel+radial+influence 4 图）、`survival_meta`（forest+funnel+radial 3 图 +
    **bias 正常填充** egger_p/begg_p）、`diagnostic_meta`（sroc+sens_forest+spec_forest 3 图）、
    `bayesian_pairwise`（修复后 forest 出图）。
  - 共享块 pairwise/单组/亚组/metareg/nma/留一/累积/剂量反应/TSA/power 等全部 status=ok。
- **说明**：测试框架报告的 case12/19 "NaN/NA" 与 case16 "netleague 缺失" 均为**误报**——stats 里的
  `"NA"` 是字符串（非数值 NaN，metamean 路径 p 值缺省，既有行为）；`netleague` 按设计进
  `stats.extra.league_table`（表格）而非 figure。`case38_rob2` 报 error 因本地缺 `robvis` 包
  （coze 服务端才有），非重构回归。
- 测试框架经验：`subprocess.run` 反复 spawn R 在本机触发资源耗尽崩溃、且共享 temp 文件会交叉污染；
  改为 bash 分批（每批 5 案例）+ 唯一 temp 文件后稳定。临时文件用后即清。

---

## [2.2.20] — 2026-08-28 — sens/spec 改 PLO 规范写法 + R 引擎函数化去重

### Changed（`adapters/coze_project/src/r_engine/run_task.R`）
- **`diagnostic_meta` sens/spec forest 修正 measure**：coze 直连实测 + 本地验证确认 `metafor::escalc`
  全 family（OR/SMD/PR/PLO 等）正常；`PLOD` 非合法 measure（metafor 报 Unknown measure），
  敏感度/特异度森林图改用标准的 **`escalc(measure="PLO")`**（logit 比例，xi=TP/ni=TP+FN 等），
  与 `meta_analysis_core.R` 既有 PLO 用法一致。
- **R 引擎函数化去重（纯机械提取，零行为改变）**：
  - 新增 `.safe_fig(figs, draw, type, w, h)`：收敛全库 13 处 `tryCatch(c(figs, list(.render_fig(...))))`
    出图安全包装 → 统一调用（sucra/contribution/nodesplit/egger/loo/cumulative/forest/sens/spec/influence 等）。
  - 新增 `.meta_to_rma(fit, model)`：收敛 meta 对象 → metafor::rma.uni 桥接（供 radial/influence 诊断），
    已传 rma 对象则原样返回；应用于 metainc 与共享块 influence 分支。
  - 新增 `.bias_test(fit, model, warns, plots, figs)`：收敛共享块与 survival_meta 两处 ~30 行几乎重复的
    Egger/Begg `regtest`/`ranktest` + egger_p<0.10 警告 + egger 图逻辑 → 一处定义两处调用。
  - 新增 `.quality_gate(fit, te_vec, se_vec, df, stats, bias_gate)`：收敛两处 `es_gate` 构造 +
    `run_quality_gate` 调用 + 结果回填 → 一处定义两处调用。
  - 新增 `.bayes_summary(res)`：收敛 bayesian_pairwise 分支 20+ 行 bayesmeta $summary 矩阵解析
    （兼容版本间行列方向差异）→ 一处定义一处调用。
  - 新增 `.col_name(colmap, role, default)`：列名解析（区别于 .col 的取值），dose_resp 手写 7 行
    `tolower(cm$x %||% ...)` 改用该 helper。

### Verified
- 本机 R 4.6.1 + metafor 5.0.1 实测：`escalc`（OR/SMD/PR/PLO）全部正常，**无段错误**——此前段错误
  为 Git Bash `-e` 多行引号破坏假象，非真实问题。PLO 版 sens/spec 森林图完整跑通（rma.uni 合并 + forest 绘制）。
- 冒烟测试通过：`.bias_test`（meta 对象 → rma 桥接 + bias + warns + egger 图）、`.bayes_summary`（NA 兜底）、
  `.col_name`（含 default 回退）、sens/spec PLO 森林图绘制。
- `run_task.R` Rscript `parse()` 通过；`.safe_fig` 14、`.meta_to_rma` 2、`.bias_test` 2、`.quality_gate` 2、
  `.bayes_summary` 1、`.col_name` 7 处调用确认。

### 说明
- 本次改动均为本地代码镜像 `adapters/coze_project`，**未部署到 coze 云端**（云端 `run_task.R` 仍是旧版，
  实测 `diagnostic_meta` 只返回 sroc，未含 sens_forest/spec_forest）。需在 coze 平台侧同步代码后生效。

---

## [2.2.19] — 2026-08-28 — 直接改 coze R 引擎，为单分支 task 增加默认伴侣图

### Changed（`adapters/coze_project/src/r_engine/run_task.R` + `scripts/build_request.py` + `adapters/rendering.py`）
上一版（2.2.18）核查发现 `survival_meta`/`diagnostic_meta`/`metainc`/`ipd_meta`/`bayesian_pairwise` 在 coze
R 引擎各自独立分支只渲染一种图。本次**直接改 coze 端 R 代码**（用户授权）为这些 task 补默认伴侣图：

- **`metareg`**：放宽 `run_task.R:577` 的 bubble gate（`task == "bubble_plot"` → `task %in% c("bubble_plot","metareg")`），
  让 metareg 也能渲染气泡图（meta 回归标志性图）。默认 `["forest","funnel"]` → `["forest","funnel","bubble"]`。
- **`survival_meta`**：R 分支补 `funnel` + `radial`（rma.uni 对象，引擎支持）。默认 → `["forest","funnel","radial"]`。
- **`diagnostic_meta`**：新增 `.diag_sens_forest` / `.diag_spec_forest` helper（手算 logit + 0.5 连续性校正，
  规避 escalc measure 兼容性，规避弃用依赖），补敏感度/特异度森林图。默认 → `["sroc","sens_forest","spec_forest"]`。
- **`bayesian_pairwise`**：该分支此前从未调用 `render_fig`，默认 `["forest"]` 实为空跑不出图。现用
  `res$y`/`res$sigma` 绘制个体研究森林图（metafor 已依赖），默认出图。
- **`metainc`**：补 `funnel`/`radial`/`influence`（meta 对象经 `rma.uni(fit$TE, fit$seTE)` 桥接）。默认 →
  `["forest","funnel","radial","influence"]`。
- **`ipd_meta`**：补 `funnel`/`influence`（rma.glmm 对象）。默认 → `["forest","funnel","influence"]`。

同步更新：`build_request.py` 的 `DEFAULT_PLOTS` 与 `VALID_PLOTS`（新增 `sens_forest`/`spec_forest`）、
`rendering.py` 的 `_I18N`/`type_names`（新增敏感度/特异度森林图中英文标题）。

### Verified
- `py_compile` 通过；`_default_plots_for` 输出确认（见下方表格）。
- `run_task.R` 经 Rscript `parse()` 通过；敏感度/特异度森林图 helper 在本地 R 4.6.1 + metafor 5.0.1 完整跑通
  （rma.uni 合并 + forest 绘制，敏感度 pooled=0.857 / 特异度=0.894 合理）。
- ⚠️ 说明：本机 metafor 5.0.1 经 `Rscript -e` 多行传参曾误报段错误，实为 Git Bash 引号破坏所致；
  改用临时 `.R` 文件执行全部正常，非代码问题。

---

## [2.2.18] — 2026-08-28 — 默认图形增强 + netleague 中文映射

### Added / Changed（`scripts/build_request.py` + `adapters/rendering.py`）
- **`netleague` 中文/英文标题映射补全**：`rendering.py::_I18N` 新增 `fig_netleague`（zh=网络证据表 /
  en=Network evidence table），`type_names` 取值 `netleague` → 该图在 HTML 模板中不再回退显示原始英文 type 名。
- **默认图形增强（仅动 coze 共用渲染大块内、引擎已支持的 task，不碰 R 端）**：
  - `single_group_meta`：`["forest"]` → `["forest","funnel","influence"]`（主森林图 + 漏斗图 + 影响诊断；
    baujat/radial 对 metaprop/metacor 对象不稳，不强行加）。
  - `subgroup_analysis`：`["forest"]` → `["forest","funnel","baujat","radial","trimfill","influence"]`
    （含 by-subgroup 分层森林图 + 异质性/发表偏倚/剪补/敏感性全套诊断，与 pairwise_meta 诊断集对齐）。
  - `metareg`：`["forest"]` → `["forest","funnel"]`（bubble 被锁死在 `bubble_plot` task，metareg 拿不到，
    见下方"需 R 端改动"项；此处加 funnel 作发表偏倚诊断）。
- **引擎能力核查结论**：`survival_meta`/`diagnostic_meta`/`metainc`/`ipd_meta`/`bayesian_pairwise` 在
  `run_task.R` 各自独立分支仅写了一种图的 `render_fig`（bayesian_pairwise 甚至无图），这些 task 想再加默认图
  需改 R 端，不在本次纯默认值调整范围内。

### Verified
- `py_compile` 通过；`_default_plots_for` 输出确认：single_group_meta=[forest,funnel,influence]、
  subgroup_analysis=[forest,funnel,baujat,radial,trimfill,influence]、metareg=[forest,funnel]、
  pairwise_meta(OR)=[forest,funnel,baujat,radial,labbe,trimfill]、nma=[netgraph,netleague]。
- `rendering._I18N['zh']['fig_netleague']` = 网络证据表；`['en']` = Network evidence table。

---

## [2.2.17] — 2026-08-28 — 图形默认出图与渲染健壮性修复

### Fixed（脚本 `scripts/build_request.py` + 呈现层 `adapters/rendering.py`）
- **`influence` 任务默认图不显示（核心 bug）**：旧 `DEFAULT_PLOTS["influence"] = []`，但 coze 端
  `run_task.R` 第 574 行 `if ("influence" %in% plots)` 才出影响力诊断面板——空 plots 仅返回 stats，
  面板永不显示，与注释"coze 自动渲染影响力诊断面板"不符。改为 `DEFAULT_PLOTS["influence"] = ["influence"]`，
  显式请求后 coze 正常出图；同步修正设计注释（influence 不再归入"空 plots 自渲染"组）。
- **`content_bbox` 健壮性加固（呈现层）**：原仅扫描 text/rect/line/circle/polyline。ggplot2 / 网络图
  主内容多为 `<path>`（曲线、edge），若漏扫会导致动态 viewBox 裁掉内容。新增：
  ① 解析 `<path d=...>` 绝对坐标对；② 将计算 bbox 与**原始 viewBox 取并集（union）**——既保留
  forest 负坐标溢出扩展，又保证 svglite 实际绘制区域（设备坐标恒在原 viewBox 内）不被裁。
  `build_figure_widget` 与 `svg_to_png` 两处调用均已传入原始 `vb`。

### Verified
- 审计脚本覆盖全部 23 个 coze 实际返回的 figure `type`（forest/funnel/labbe/baujat/radial/trimfill/
  influence/bubble/egger/netgraph/contribution/nodesplit/sucra/dose_resp/sroc/loo/cumulative/drapery/
  prisma_flow/gosh/tsa/power/rob2）：在 `render_html_report` 中**均以本地化标题正常显示**（无原始 type 兜底）。
- `content_bbox` 对森林图负坐标溢出（x∈[-140,644]）正确扩展；对纯 path 图形与原 viewBox 并集后不裁图。

---

## [2.2.16] — 2026-08-27 — 云端二次重建回归闭环确认（两项修复端到端生效）

### Verified（云端端到端，coze 节点用 coze_project_fixed_v2.zip 重建后）
- 用 6 研究 SMD+REML 亚组用例 POST `https://ct-meta.coze.site/run` 回归（cloud_regression_v2.json）：
  - `subgroup_test` = {Q_between=15.5055, df=1, p_between=0.0001, n_groups=2, model=random} —— 与本地 4.6.1 完全一致，**已生效**。
  - 亚组 short = -2.0473 [-2.395, -1.700]；long = -2.8913 [-3.127, -2.656]（长期降得更明显）。
  - pooled(REML) = -2.4631 [-2.875, -2.051]，p≈9.9e-32。
  - **森林图 SVG 头条闭环**：含 "Random effects model" ×3（short/long 亚组合并 + 总合并）、不含 "Common effect model"；头条数值 = -2.46（REML 合并量，非固定效应 -2.43）。问题二在云端彻底生效。
- 结论：coze_project_fixed_v2.zip 的两处修复（①森林图 `common=FALSE,random=TRUE` + 判断条件 `fit$random`；②`subgroup_test` 走 `Q.b.random` 原生槽位）在 coze 同款 R 4.6.1 + meta 8.5.0 环境下**端到端闭环**，不再需要 v1 或本地兜底。

---

## [2.2.15] — 2026-08-27 — 森林图头条二次修复：.forest_plot_theme 判断条件对齐 meta 8.5.0

### Fixed（coze 镜像 run_task.R）
- **根因（对 [2.2.14] 的纠正）**：[2.2.14] 修好了 `common/random` 形参与 `col.subgroup`，但 `.forest_plot_theme` 的分支判断条件
  `if (isTRUE(fit$comb.random))` **未同步修改**。meta 8.5.0 已弃用 `comb.random` 槽位（返回 NULL），
  故该判断恒为 FALSE → 永远走 `common=TRUE, random=FALSE` 分支，森林图头条仍画"Common effect model"（固定效应），
  与请求的 REML 随机效应口径不符、误导读图。
  ⚠️ [2.2.14] 第 19 行"头条=REML"为**误判**——当时本地验证未 grep SVG 模型名，仅依 subgroup_test 数值推断。
- **修复**：`.forest_plot_theme` 判断条件改为 `if (isTRUE(fit$random) || isTRUE(fit$comb.random))`，
  兼容 8.5.0 的 `random` 槽位（`fit$random=TRUE` 时即走 `common=FALSE, random=TRUE` 画随机效应头条）。

### Verified
- 本地 R 4.6.1 全流程跑 6 研究 SMD+REML 亚组用例：**SVG 含 "Random effects model"、不含 "Common effect model"**，证明头条修复生效。
- 云端回归（重建节点后）：`subgroup_test` 已在上一轮重建生效（Q_between=15.5055, p=0.0001, model=random）；
  森林图头条修复需**用本包（v2）再次重建 coze 节点**后方在云端生效（当前云端回归的森林图仍是 Common effect，因上一轮漏改判断条件）。

---

## [2.2.14] — 2026-08-27 — coze 镜像对齐 meta 8.5.0 破坏性变更（col.subgroup / Q.b.* 槽位）

### Fixed（coze 镜像 run_task.R + 本地验证环境升 R 4.6.1）
- **根因（部署环境 R 4.6.1 + meta 8.5.0 + metafor 5.0.1 的破坏性变更）**：历史镜像代码基于旧版 meta 假设，在 8.5.0 下行为失真：
  1. `meta::forest` 的 `col.by` 参数**已移除**（8.5.0 仅认 `col.subgroup`）→ 旧代码传 `col.by` 主题色静默失效（不报错但亚组分隔色丢失）。
  2. 亚组 `metacont/metabin` 结果对象的组间异质性槽位**更名为 `Q.b.random` / `Q.b.common`**（旧版为 `Q.between.random` 且旧版根本无该槽位）→ 历史 `subgroup_test` 主路径取 `fit$Q.between.random` 恒为 NULL，静默落兜底，与森林图 "Test for subgroup differences" 图例口径偶发不一致。
  3. （附带）`metacont(..., comb.random=)` 8.5.0 已弃用（改用 `random=`）；调用处写 `random = mm$comb.random`（值正确赋给新参数名），未触发弃用告警，无需改。
- **修复（run_task.R）**：
  - `.forest_plot_theme`：`col.by = th$by` → `col.subgroup = th$by`（3 处：comb.random / random 两分支 + tryCatch 兜底）。
  - `subgroup_analysis` 分支 `subgroup_test` 主路径：`fit$Q.between.random/.common` → `fit$Q.b.random/.common`（及 `pval.Q.b.*` / `df.Q.b.*`）；`rf` 判断改 `isTRUE(mm$random %||% mm$comb.random)` 兼容 8.5.0 的 `random` 槽位。
- **本地验证环境对齐**：旧版本地 R 4.5.1（meta 旧版）无法暴露这些槽位、也不吃 `common` 形参，验证无效；按用户要求本地验证环境升级到 R 4.6.1（与 coze 同款），实测：
  - subgroup_test 走 8.5.0 原生 `Q.b.random` 主路径 → `Q_between=15.5055, df=1, p=0.0001, model=random`，与云端此前 15.51 / <0.0001 完全对齐；
  - 森林图成功出图、无 `col.by` 告警、头条=REML（common=FALSE, random=TRUE）。

### Verified
- 本地 R 4.6.1 跑 6 研究 SMD+REML 亚组用例：subgroup_test 主路径生效、亚组 short=-2.0473 / long=-2.8913、pooled=-2.4631，全部正确；无 col.by / comb.random 告警。

---

## [2.2.13] — 2026-08-27 — 默认图形随分析方法自动适配（不再写死森林图）

### Fixed（build_request.py + coze_contract.md 文档同步；coze 镜像无需改动）
- **根因**：旧 `build_request.py` 永远发 `figure.plots=["forest"]`，且用户 plots 只能追加 `funnel`。coze 镜像 `run_task.R` dispatch **严格按 `figure.plots` 出图**，其各 task 默认图（nma→netgraph+netleague、diagnostic→sroc 等）仅在 `plots` 为空时触发——而 `plots` 永远非空 `["forest"]`，故兜底从不触发，所有 task 只落森林图。下游 HTML（`rendering.render_html_report`）只是内联 coze 返回的 `figures[]`，无硬编码，故"coze 与 HTML 都只给森林图"是同一根因的两层表现。
- **修复**：`build_request.py` 新增 `DEFAULT_PLOTS`（每 task 默认图，对齐 `coze_contract.md §3`）与 `VALID_PLOTS`（用户显式覆盖时的合法图名校验）。
  - 用户未指定 → 按 `spec.task` 取 `DEFAULT_PLOTS`（pairwise→forest+funnel、subgroup/metareg/bayesian/survival/single_group→forest、nma→netgraph+netleague、nma_rank→sucra、diagnostic→sroc、dose_resp→dose_resp、gosh→gosh 等）。
  - 用户显式 `params_extra.plots` → 采用（过滤 `VALID_PLOTS` 中的非法名；全非法则回退该 task 默认）。
- **文档同步**：`coze_contract.md §3` 三处与镜像矛盾修正——`metareg` 默认图 `bubble`→`forest`（`run_task.R:494` 的 bubble 图仅对 `task=="bubble_plot"` 生效、metareg 不发）；`nma_rank`/`dose_resp` 默认图由 `—` 补全为 `sucra`/`dose_resp`（`run_task.R` 对应分支空 plots 时即默认出此图，与代码一致）。
- **验证**：11 个分析方法默认图 + 用户覆盖（forest only / nma+contribution）+ 非法回退，共 14 用例冒烟全过（ALL_OK）。

---

## [2.2.12] — 2026-08-27 — build_request 不诚实字段清理：diagnostic_meta / survival_meta 跳过 params.sm

### Fixed（build_request.py + coze_contract.md 文档同步；coze 镜像无需改动）
- **`params.sm` 噪音字段清理**：经核对 coze 镜像 run_task.R 一手代码，`diagnostic_meta`（`mada::reitsma`，合成灵敏/特异度/SROC，不读 sm）与 `survival_meta`（`metafor::rma.uni(logHR)`，固定合 HR，不读 sm）**不消费 `params.sm`**。旧逻辑 `sm = measure_override or spec.measure or "OR"` 对所有 task 无差别写 `OR`，对这两 task 是镜像永不读的噪音字段，且 `coze_contract.md §3` 列 `sm` 为「所有 task 通用可选」会误导用户以为诊断/生存也能按 OR 换尺度。
  - 新增 `NON_SM_TASKS = {"diagnostic_meta", "survival_meta"}`；`build_request.py` 的 `params` 构造段对这两 task **跳过写 sm**，request 诚实。
  - ⚠️ **nma 仍消费 sm**（netmeta `sm` 参数，run_task.R:581 `sm <- params$sm %||% "OR"`），且连续型 nma 须显式 MD|SMD——**不剔除**，仅 diagnostic/survival 清理。
- `coze_contract.md` §3 同步：
  - `params.sm` 字段表加注「`diagnostic_meta`/`survival_meta` 不消费此字段」。
  - `nma` 行注明**消费** sm（二分类默认 OR / 连续型须显式 MD|SMD）。
  - `survival_meta` 行注明不消费 sm（HR 即效应尺度）。
  - `diagnostic_meta` 行注明不消费 sm（合成灵敏/特异度，非 OR 类）。

### Verified
- 实测 4 用例：`pairwise_meta`/`nma` → `params` 含 `sm=OR`（保留）；`diagnostic_meta`/`survival_meta` → `params` **不含 sm**（已剔除）。回归：classify + build_request import 无语法错误。

---

## [2.2.11] — 2026-08-27 — NMA 三格式自动探测：连续型/对比格式不再需 --colmap 回灌

### Fixed（build_request.py 本地修复；coze 镜像 run_task.R .nma_prep 已原生支持三种输入格式，无需改动）
- **NMA 列格式自动探测（消除 [2.2.10] Known limitation）**：`build_request.py` 对 `task=="nma"` 不再盲信 classify 固定的 arm-based 二分类列模板，改用新增 `_detect_nma_format()` 按数据实际列名自动选格式，对齐 run_task.R `.nma_prep` 与 coze_contract.md §3：
  - 对比二分类 `treat1/treat2 + event1/n1/event2/n2`
  - 对比连续 `treat1/treat2 + TE/seTE`（亦认 `te`/`sete`）
  - arm-based 二分类 `treatment + event + n`
  - arm-based 连续 `treatment + te + sete`
  - 同组（对比 / arm）内 binary 与 continuous 取「完整命中」者；均无完整命中则取命中列最多者交 LLM 兜底（exit 2，红线：有边界兜底、不破快路径）。
- 新增 `NMA_FORMATS` 列契约表 + 中/英别名（处理1/干预1/事件1/样本量1…），覆盖常见中文列名。
- `_coerce_rows` 增加 `non_numeric` 参数：对比格式的 `treat1`/`treat2` 臂标签列改为字符串透传（此前仅 `treatment`），避免 float 强转报错。
- 修正 nma 分支 `subgroup` 未初始化导致的 `UnboundLocalError`。

### Verified
- 实测 6 用例：T1 对比二分类 / T2 对比连续(TE/seTE) / T3 arm二分类(中文别名) / T4 arm连续 / T5 对比(中文别名) 全部正确探测+归一化为 coze 期望的小写规范列名；T6 无结构列正确走 `needs_llm_fallback`(exit 2)。四种格式现均无需 `--colmap` 即可直接装配 request.json。

---

## [2.2.10] — 2026-08-26 — 契约联调修复：task 名对齐 coze + build_request 列透传缺陷

### Fixed（与 coze 镜像 run_task.R / coze_contract.md §3 联调，修正一批会导致 unknown_task / 静默失效的真实 bug）
- **classify.py task 名契约断点（最致命）**：原 `network_meta` / `diagnostic` 与 coze 端点 task 白名单不符（coze 只认 `nma` / `diagnostic_meta`），NMA 与诊断 meta 会直接 `unknown_task` 失败。已改为 `nma` / `diagnostic_meta`（与 coze_contract.md §3、run_task.R dispatch 一致）。
- **classify.py 诊断 data_type 回归**：改 task 名时漏改 `if task == "diagnostic"` 守卫 → 诊断 query 错误回退 `data_type=binary`、列模板变成 `event_exp/n_exp…` 而非 `tp/fp/fn/tn`。已同步为 `if task == "diagnostic_meta"`；实测 `classify("做诊断试验meta分析")` 现返回 `task=diagnostic_meta / data_type=diagnostic / colmap=[tp,fp,fn,tn]`。
- **build_request.py 亚组变量列被丢弃（静默失效 bug）**：`_coerce_rows` 只输出 colmap 数值列，亚组变量列（如 `age`/`region`）不在 colmap 内被丢弃 → coze 收不到该列、`subgroup_analysis` 静默降级为主分析。已新增 `carry_cols` 原样透传亚组列；实测 `subgroup_analysis` 现正确携带 `params.subgroup` 对应列。
- **build_request.py 分类列被强制 float（nma 报错）**：`_coerce_rows` 对全部列 `float()` 强转，nma 的 `treatment` 臂标签列（字符串）直接报错。新增 `NON_NUMERIC_KEYS={"treatment"}` 透传字符串列；实测 arm-based 二分类 nma 数据现正常装配 `task=nma` + `treatment/event/n`。
- **classify.py nma 默认列模板错误**：nma 未单设 data_type，默认套用二分类 `event_exp/n_exp/event_ctrl/n_ctrl`（coze `.nma_prep` 不接受配对格式）。已加 `data_type="nma"` + `COLMAP["nma"]=["treatment","event","n"]`（arm-based 二分类默认；连续/对比格式走 `--colmap` 兜底）。
- **coze_client.py `byvar`→`subgroup` 兜底映射补回**：CHANGELOG `pending-2.2.1` 记录此修复但代码从未落地；`run_meta()` 现对 `params.byvar` 做 `subgroup` 归一化，兼容历史 spec，避免静默失效。

### Docs（与代码同步）
- SKILL.md §5.0 端点能力边界整段重写：以 coze_contract.md §3 + run_task.R 为准，`metareg` ✅已接线（需 `te`/`sete` + `params.cov`）、`nma`/`nma_rank`/`survival_meta`/`diagnostic_meta` ✅，删去原"metareg 未接线 / nma·diagnostic 未注册"过时错误。
- SKILL.md §5.1 + references/interactive_menu.md §6 回显块/范例：占位 task 名 `forest`→`pairwise_meta`、`subgroup`→`subgroup_analysis`；`byvar=`→`subgroup=`（§5.0 明令 byvar 静默失效）；补 `task=sensitivity` 实为未注册 task、应复用 `pairwise_meta` 做 leave-one-out 的说明。
- `pending-2.2.1` 标记已由本版落实，并更正其 `metareg 未接线` / `diagnostic 未注册` 两条与镜像实测矛盾的旧结论（`diagnostic_meta` 已注册）。

### Known limitation（本版未改，待后续）
- ~~nma 连续型 / 对比格式需 --colmap 回灌~~ → **已在 [2.2.11] 修复**：`build_request.py` `_detect_nma_format()` 按数据实际列名自动探测四种 NMA 输入格式（对比二分类/对比连续/arm二分类/arm连续），无需 `--colmap`。
- diagnostic_meta 默认 `params.sm=OR`（mada reitsma 通常忽略 sm，无害）。

### Verified
- 实测 6 用例：classify(诊断) / pairwise OR / diagnostic_meta / subgroup(age 透传) / nma(arm-based) 全部产出 task 名与列映射对齐 coze_contract.md §3 的 request.json；无 unknown_task 风险。

---

## [2.2.9] — 2026-08-27 — 长上下文保护：§0 规则 1 跨轮引用 carve-out（合法使用对话历史回填参数，不破速度纪律）

### Added（解决"严格纪律在长对话里误伤引用前文轮次"的缺口）
- **规则 1 carve-out**：「禁止深度思考」仅约束计算/呈现阶段；用户显式引用前文（"用之前的数据""和刚才一样"）时，LLM 允许回看对话历史提取既有数据/spec **用于回填 `--data-json`/参数**，但禁止据此重新推导数值或重路由。
- **延迟不变量补"跨轮回填例外"**：回看对话历史构造 `--data-json` 属构造入参、非额外工具调用，不计入火前 ≤1 次数；回填后仍是 1 次 `build_request.py`。仅放宽数据来源，不放宽计算/呈现禁令。
- **背景**：确认当前方案对长上下文交互无系统性负面影响（路由确定性 + 对话流零图形双保险），但"引用前文"轮次会被严格纪律误伤——本补丁收窄该缺口，速度内核不变。

---

## [2.2.8] — 2026-08-27 — 有边界 LLM 兜底：build_request.py 列名别名自动匹配 + needs_llm_fallback + --colmap/--measure/--model 回灌

### Added（错误触发、范围受限，不破默认快路径）
- **`COLUMN_ALIASES`**：中/英同义列名表（实验组事件数/处理组事件/trt_ev…），先自动模糊匹配，吃掉大部分"列名不符"。
- **`needs_llm_fallback`**：别名仍解析不出 → 发结构化 JSON（exit 2，含 `unresolved_columns`/`available_columns`/`partial_spec`/`hint`）。
- **回灌参数**：`--colmap`（列映射）/ `--measure` / `--model`，LLM 仅补缺映射或纠正参数后重跑；`_resolve_colmap` 优先采用 override。
- **错误分流**：列缺失走兜底路径；值非数值/缺值等用户数据错误为硬错误（exit 1），不兜底。
- **文档**：SKILL.md §0 规则 7（有边界 LLM 兜底）+ 延迟不变量补"兜底例外"；顶部红线注释同步。
- **实测**：中文列名别名匹配✅、陌生列名发 fallback✅、--colmap 回灌成功✅、非数值硬错误✅、原 4 项 OR 回归同构✅。

---

## [2.2.7] — 2026-08-27 — Phase 2 闭环：scripts/build_request.py（compute 轨 request.json 一键装配）

### Added（消灭"LLM 手写 request.json"，让延迟不变量真正可达）
- **新增 `scripts/build_request.py`**：计算轨归一化/装配脚本，**零 LLM 决策、零计算、零出网**。一次本地调用内完成：调 `classify.py` 出 spec → 校验数据列 → 装配 `run_analysis` 的 `request.json`。
  - 输入：`--query`（内部 classify）或 `--spec`；研究数据 `--data path.csv/.json` 或 `--data-json '[{...}]'`；输出 `--out request.json`。
  - 映射：`measure`→`params.sm`、`model` REM-L→REML(common:false,random:true) / MH→MH(common:true,random:false)、亚组变量→`params.subgroup`、funnel→`figure.plots`（forest 恒含）。
  - 红线：选题轨（`track==topic`）直接拒；缺列报错列名；`--data` 已给时覆盖 classify 仅凭 query 文本判的 `needs_clarify`（避免误报缺字段）。
- **§0 双轨门控 / 延迟不变量更新**：计算轨火前唯一动作显式写为一次 `build_request.py` 调用（内部含 classify），彻底取代"classify + LLM 手写 request.json = 2 次"的旧路径；§1 Triage 说明同步更新为"LLM 不再手写 request.json"。
- 实测（本地、零出网）：4 项 OR 随机效应 / 固定效应 RR / 亚组按年龄+漏斗图 / 选题轨拒 / 缺列报错——5 用例全过。
- 受影响文件：`scripts/build_request.py`（新增）、`SKILL.md`（§0 / §1）、`CHANGELOG.md`（本条）。

---

## [2.2.6] — 2026-08-26 — Phase 2 代码：scripts/classify.py 双轨路由脚本

### Added（把"火前路由犹豫"也压成代码，对齐 ct-advisor route.py）
- **新增 `scripts/classify.py`**：确定性 NL→spec 映射脚本，**零 LLM 决策、零计算、零出网**。输入用户 query，输出 `spec` JSON（`track` / `task` / `measure` / `model` / `data_type` / `params_extra` / `needs_clarify` / `missing_fields` / `colmap`）。
  - 关键词表覆盖：选题轨、数据类型（binary/continuous/diagnostic/survival/ipd）、效应量（OR/RR/RD/MD/SMD/HR）、模型（REM-L 默认 / MH）、task 覆盖（pairwise_meta/subgroup_analysis/metareg/network_meta/survival_meta/diagnostic）、plots（funnel/egger）、亚组变量抽取。
  - 判定顺序：track → task → data_type → measure → model → plots/subgroup → 数据迹象校验（`\d+/\d+` 或含数据词 + 数字；compute 轨无数据即 `needs_clarify=true`，仅回缺字段）。
  - `colmap` 给出默认列名建议（binary→`event_exp/n_exp/event_ctrl/n_ctrl` 等），agent 直接套用归一化。
- **§1 Triage 顶部加说明**：路由已由 `classify.py` 代码完成，LLM 不再决策；附表仅供理解。
- 延迟不变量兑现：计算轨 fire 前本地工具调用 ≤1 可由一次 `classify.py` 调用承担（取代此前翻 SKILL/references/adapter 的 10–20 轮火前拖拽）。
- 受影响文件：`scripts/classify.py`（新增）、`SKILL.md`（§1 说明）、`CHANGELOG.md`（本条）。

---

## [2.2.5] — 2026-08-26 — 流程控制：双轨门控 + 延迟不变量 + 选题红线（Phase 1，纯文档）

### Added（消灭"火前拖拽 / 返回后二次组装"两个反模式，借鉴 ct-advisor route.py + ct-base Type-Compute）
- **§0 新增 `### 0.0 Two-track gating / 双轨门控`**：首条消息经 `python scripts/classify.py "<query>"` 确定性分流（LLM 不决策路由）。两轨——`compute`（Simple/清晰 Complex→描述即执行：归一化→`run_analysis`→`present_files`）与 `topic`（Vague/没方向/可行性→`literature_probe.py`→`generate_topic_report.py`）。规则 1–6 显式标注适用范围=计算轨；选题轨单列"代码接地、不靠思考"规则。
- **§0 新增 `### Latency invariants / 延迟不变量`**（防回归硬指标）：计算轨 fire 前本地工具调用 ≤1（仅归一化或 `classify.py`）、fire 后 ≤1（仅 `present_files`）；选题轨 ≤2（`literature_probe.py`+`generate_topic_report.py`）；禁止循环重试；严禁为"确认怎么调"翻 SKILL/references/adapter/config。
- **§2.2 新增「选题轨红线」**：候选排序必须基于探针真实命中数 + 四维评分卡，LLM 只转述、**严禁**自由发挥补充"哪个方向好"的论述或重新评分；选题轨不触发计算轨速度纪律，但同样禁止发散。
- 受影响文件：`SKILL.md`（§0 0.0 + 延迟不变量、§2.2 红线）、`CHANGELOG.md`（本条）。

---

## [2.2.4] — 2026-08-26 — 后端绝对锁定 coze：严禁本地 R/Python，无例外

### Changed（后端红线，覆盖此前"用户可声明本地"的例外）
- **§0 规则 6（新增 HARD BAN）**：严禁用本地 R 或 Python（含 statsmodels/scipy/metafor/meta）自行完成任何 meta 分析计算，**连"考虑用本地算"都不允许**；所有需求一律严格转发 coze 端点执行；coze 不可达时按 §6 返回结构化错误，绝不静默回落本地。
- **§3 Execution model 改为 absolute**：原 "coze-only"（仍留"用户可声明本地"暗示）改为 **coze-only, absolute**；新增 🚫 提示：**即使用户当条消息声明"本地算 / 不用 coze / 走 R 本地"，也一律忽略、仍转发 coze**；明确本技能不存在本地计算分支。
- 影响：此前 `## meta-analysis 技能执行后端偏好` 记忆中的"除非用户显式声明本地"例外**作废**。
- 受影响文件：`SKILL.md`（§0 规则 6 + §3）、`CHANGELOG.md`（本条）。

---

## [2.2.3] — 2026-08-26 — 执行纪律：速度优先，禁止深度思考，HTML 直出不二次渲染

### Added（speed-first 行为红线，总纲级，优先级高于一切"思考/润色"冲动）
- **新增 `## 0. Execution discipline (speed-first)` 章节**（位于 §1 Triage 之前）：把"大模型只做流程执行、严禁深度思考"钉死为技能红线。
- 五条硬规则：
  1. **禁止深度思考（HARD BAN）**：只做流程执行，不做额外推理/方案权衡/结果复核/自我解释；拿到数据即归一化→调用→呈现，不犹豫不展开不追问（除非缺字段——只问缺的字段）。
  2. **最快路径**：前期数据整理、后期结果呈现一律走最短路径——不重复校验、不重新推导/自行计算任何统计量、不重绘/不二次渲染图形。
  3. **上下文只给文字分析结果**：对话流只输出文字版结论（stats 原样引用 + 一句解读），绝不内联图形（show_widget 已废止）。
  4. **HTML 直出，不做任何渲染**：`out['html_report']` 即最终交付物，大模型不得对其内容做任何再加工/再排版/再渲染/重新抽取数值——直接 `present_files` 打开。图形只在 HTML 中展示（原始宽度、过宽滚动）。
  5. **数字零改写**：数值必须原样引用 coze 返回的 stats，禁止四舍五入/换算/重新格式化。
- 受影响文件：`SKILL.md`（新增 §0）、`CHANGELOG.md`（本条）。`inline_rendering.md` / `rendering.py` 无需改动（既有实现已满足"不放大 + HTML 单一面"）。

---

## [2.2.2] — 2026-08-26 — 呈现层变更：取消内联 widget，图形一律走 HTML 报告（SVG 不放大）

### Changed（呈现层硬约束，skill 开发者决策）
- **取消内联 `show_widget` 渲染（原 §5 默认且强制）**：所有 `figures[].svg` 不再内联进对话流，改由 `run_analysis` 生成的聚合 HTML 报告（`out['html_report']`）统一展示，agent 用 `present_files` 打开预览。原强制内联规则（"figures must NOT be delivered merely as file cards" / 约束 #4 "Figures inline by default (mandatory)"）改为 "Figures in HTML report (mandatory)"。
- **SVG 宽度规则**：图保持自然内容宽度，**绝不放大到固定画幅**（如为 680px 容器而拉伸 504px 图）。嵌入按 `content_bbox` 算出的实际内容宽度，装不下即横向滚动。该行为由 `rendering.py` 的 `build_figure_widget` / `render_html_report` 已实现（SVG `width:{w}px`，`w = max_x - min_x`，无 680px 固定画布）；本次仅把规范对齐到既有实现，并废止此前为满足 show_widget 680px viewBox 而手动拉伸 SVG 的做法。
- 受影响文件：`SKILL.md` §5（Rendering + 约束 #4 + figure_mode 说明）、`references/inline_rendering.md`（标题与 §1/§3/§8 改为"HTML 报告唯一面 + 不放大"）。

### Verified
- 既有 `rendering.py` 无 680px 固定画布；`build_figure_widget` 输出 `width:{w}px`（w=自然内容宽）。本次仅改文案，渲染链零改动。

---

## [2.2.1] — 2026-08-26 — 契约对齐：亚组参数键 byvar→subgroup + 端点能力边界实测（已由 2.2.10 落实；metareg/diagnostic_meta 结论已更正）

### Fixed（本地契约 bug，实测发现）
- **亚组分析静默失效（契约 bug）**：SKILL.md §5.1 跨轮 spec 字段名写 `byvar`、task 名写 `subgroup`；但 coze 端点实际（2026-08-26 线上探测）只认 `subgroup_analysis` task + `subgroup` 参数键（`byvar`/`group`/`by`/`strata` 全部静默忽略，仅回主分析合并值）。修复方式双保险：
  1. `adapters/coze_client.py` `run_meta()` 在发请求前做 `byvar`→`subgroup` 兜底映射（兼容历史 spec 字段名，避免静默失效）；
  2. SKILL.md §5.1 的 spec 字段、回显块、task 切换示例全部对齐到实测契约（`byvar`→`subgroup`，`task:subgroup`→`task:subgroup_analysis`）。

### Documented（端点能力边界，实测标注，非本地可修）
- `pairwise_meta` ✅ 完整（异质性 I²/τ²、Egger/Begg、漏斗、质量门）；
- `subgroup_analysis` ✅ 正常（参数键 `subgroup`）；
- `metareg` ✅ **已接线**（2026-08-26 实测 + coze_contract.md §3 对齐）：需提供已算效应量列 `te`/`sete` + 协变量列，并以 `params.cov` 传协变量列名；仅给原始二分类/连续列会静默降级为 `pairwise_meta`。原 pending 记录"15 键均不返回 regression"系历史探测误判，已更正。
- `nma` ✅ 注册（需每研究 ≥2 臂）；
- `sensitivity` / `pub_bias` / `publication_bias` ❌ 未注册（`unknown_task`）；发表偏倚已内嵌进 `pairwise_meta` 自动算，无需单独 task。**更正**：`diagnostic` 未注册但 `diagnostic_meta` ✅ 已注册（原 pending 把两者混为一谈，已更正）；classify.py 现发 `diagnostic_meta`。

### Verified
- 线上实测：20 项 MDD RCT（OR），`subgroup_analysis`+`{"subgroup":"region"}`→ Asia/Europe/NorthAmerica 三亚组效应量正确分层；`metareg` 15 键均不返回 `regression`；`sensitivity`/`pub_bias` 返回 `unknown_task`。

---

## [2.2.0] — 2026-08-26 — 图形回归修复 + 扩充影响诊断 / 节点拆分 / 剪补法漏斗

### Fixed（coze 端图形回归，线上实测发现）
- **`.render_fig` 未打印 ggplot 对象**：原函数对 `function() .sucra_plot(rk)` / `.egger_plot()` / `.bubble_plot()` 这类「返回 ggplot」的工厂直接调用并丢弃返回值 → SVG 为空。线上实测 sucra/egger/bubble 三个图均返回 0 字节 SVG。改为捕获函数返回值、若为 ggplot 则 `print()`，基础绘图函数（forest/funnel/netgraph 等副作用绘制）不受影响。
- **NMA 贡献图静默失败**：`netmeta::netgraph(fit, contribution = TRUE, seq = TRUE)` 在 netmeta 3.6.1 不支持（`contribution` 被当图形参数忽略、`seq` 触发「argument is not interpretable as logical」），原 tryCatch 静默吞错 → `figures` 为空。改用 `.contribution_plot()`：优先原生 `netgraph(contribution=TRUE)`（新版本），否则走 `decomp.design()` 取各比较对不一致性的贡献（Q.inc.design）以 ggplot 条形图呈现，version-independent。

### Added（进一步扩充支持范围）
- **影响诊断图 `influence`**（pairwise_meta 等分支，`plots:["influence"]`）：`metafor::influence(rma_fit)` 多面板（Cook 距离 / 杠杆 / CovRatio / DFFITS / hat），7×9 SVG。
- **节点拆分图 `nodesplit`**（nma 分支，`plots:["nodesplit"]`）：`netsplit(fit)` → `forest()` 呈现局部不一致性（直接 vs 间接 vs 网络估计），netmeta 已依赖。
- **剪补法漏斗图 `trimfill`**（pairwise_meta 分支，`plots:["trimfill"]`）：`meta::trimfill(fit)` 后画漏斗，呈现发表偏倚校正后估计。
- 渲染层 `rendering.py` 双语图注补齐 `fig_influence` / `fig_nodesplit` / `fig_trimfill`，`type_names` 映射同步；现支持 **23 种** coze figure type 全图注。

### Verified
- R `parse()` 通过；本地 R 4.6.1 跑 `run_task.R` 真路径：sucra 5121 / egger 11439 / contribution 4903 / loo 8962 / cumulative 8963 / influence 43986 / nodesplit 12066 / trimfill 19967 / bubble 7017 字节 SVG 全部非空；`render_html_report` 23 种 type 双语自测 raw_hits=[] 且 missing=[]。

---

## [2.1.7] — 2026-08-26 — coze 端点重构：ct-meta2 主 / ct-meta 回退 + per-endpoint token

### Added
- **主工作流端点切换为 ct-meta2、回退 ct-meta**：`DEFAULT_ENDPOINT=https://ct-meta2.coze.site/run`（用户新 token，aud=`5v9HMQWtTSzxrEeZjI7kJJEzeMPrHXny`）；`FALLBACK_ENDPOINT=https://ct-meta.coze.site/run`（旧端点，保留旧 token，aud=`oxwSsfwdtRRfByYIM8Xg3U4RQH5OgEjO`）。
- **token 改为按端点分别解析**：`coze_token.get_token_for(endpoint)` 按 URL 映射不同工作流 JWT（ct-meta2 用新、ct-meta 用旧），不再全局共用；`_resolve_token(endpoint)` / `_headers(endpoint)` 接收端点参数，回退时用回退端点专属 token。优先级：`COZE_META_TOKEN`（全局覆盖）> 端点专属内嵌 blob > 历史默认 blob。
- **回退触发条件**：主端点因 token 不一致（401/403 + token/auth/invalid 关键字）失败时自动回退重试；回退成功结果附 `_coze_endpoint_notice` 并追加 notes「主分析工作流地址已切换，本次分析已自动回退到备用 coze 端点完成」。双端均 token 失败则抛错提示更新技能。
- `config.json` 白名单：移除 `wr65rdbc4w`，加入 `ct-meta2`（现三项：ct-meta2 / ct-meta / ct-bugreport）。

### Changed
- `coze_token.get_token` 重构为 `get_token_for(endpoint)` + `ENDPOINT_TOKEN_MAP`，支持 per-endpoint 凭据；`SKILL.md` / `README*` / `coze_integration_test.py` 同步更新旧默认端点引用。

### Verified
- 模块编译；`get_token_for("ct-meta2")`→aud=`5v9HMQWtTSzxrEeZjI7kJJEzeMPrHXny`、`get_token_for("ct-meta")`→aud=`oxwSsfwdtRRfByYIM8Xg3U4RQH5OgEjO`（二者不同）；线上探测两端点均 HTTP 200 + `unknown_task`（token 被接受）。

---

## [2.1.8] — 2026-08-26 — 聚合 HTML 报告（结果展示改进）

### Added
- **`rendering.render_html_report(out, out_dir="output")`**：把分析结果拼成单文件聚合 HTML 报告（内联 SVG 图形 + 统计结果明细表 + `<details>` 折叠可复现 R 代码），固化在**本地 agent 侧**。coze 返回体仅含 `stats`+S3 `url`，**不受 4000 截断与 S3 链接过期影响**；`_coze_truncated` 存在时报告顶部附截断告警 banner。
- 复用 `build_figure_widget`（含 content_bbox 扩展 viewBox、clip 移除、points 拆分与同名 CSS 变量），并自包含浅色主题 CSS（定义 `--color-text-primary` 等变量确保内联 SVG 区块在独立文件里正确着色）。
- `run_analysis.run_analysis` 成功分支自动调用，结果 `out['html_report']` 写入报告路径；生成失败不影响主结果（try/except 静默）。

### Changed
- `run_analysis` 顶部 import 增加 `render_html_report`。

### Verified
- 离线验证：真实森林图(8056B)+漏斗图(6321B) SVG 正确固化进单文件 HTML(17.5KB)，统计表 / 折叠 R 代码 / 截断 banner / CSS 变量解析 / `.format` 占位符清理均正确；`run_analysis` import 链编译无误。

### Fixed
- **PRISMA 流程图 `prisma_flow` 渲染崩溃（线上实测 status=error：`object 'label' not found`）**：`plot_prisma_flow`（`adapters/coze_project/src/r_engine/advanced_functions.R`）把 `label` 设在 `ggplot(df, aes(..., label = label))` 的**全局美学**里，被第 3 层 `geom_segment` 继承，而该层自己的 data.frame（x/y/xe/ye）无 `label` 列 → 渲染期报错。改为把 `label = label` 移入 `geom_text(aes(label = label))` 局部美学，`geom_segment` 不再继承 `label`。本地 R 4.6.1 复现并修复：ggsave 输出 5588 字节 SVG 正常。
- **SKILL.md `description` 与 `summary` 对齐**：`summary` 已含「等共 23 种分析图形」，`description` 中文段原缺失该表述 → 已补齐，英文段同步加「for a total of 23 analysis figures」，保留 ` / ` 双语分隔。

---

## [2.1.9] — 2026-08-26 — 新增四张图形（SUCRA / Egger / 贡献图 / 留一法·累积）并补齐 HTML 双语展示

### Added
- **SUCRA 排名图（`sucra`）**：NMA 排序图。在 `nma_rank` 分支接线 `if("sucra" %in% plots || (task=="nma_rank" && length(plots)==0))`；新增 `.sucra_plot(rk)`（ggplot 水平条形图，读 `rk$Pscore.random`/`Pscore`，零新增包）。
- **Egger 回归散点图（`egger`）**：在 `pairwise_meta`/`funnel_plot`/`trimfill`/`subgroup_analysis`/`metareg` 的偏倚块内接线 `if("egger" %in% plots)`，复用已算 `rma_fit`；新增 `.egger_plot(rma_fit)`（ggplot 散点 + `geom_smooth(lm)`，x=1/SE，y=yi/SE）。
- **NMA 贡献图（`contribution`）**：在 NMA 分支接线 `if("contribution" %in% plots)`，调用 `netmeta::netgraph(fit, contribution=TRUE, seq=TRUE)`。
- **留一法影响图（`loo`）/ 累积 Meta 图（`cumulative`）**：分别在 `leave_one_out` / `cumulative_meta` 分支接线（默认出图），用现有 `loo_df`/`cu_df` 经 `metafor::forest` 画 forest 变体。
- **HTML 双语展示补齐**：`rendering.py` 的 `_I18N`（zh/en）与 `type_names` 新增 `sucra`/`egger`/`contribution`/`loo`（`cumulative` 此前已在字典内，本次真正出图）。`locale="en"` 时对应英文 caption 生效。

### Changed
- 所有新增 `figs <- c(figs, list(.render_fig(...)))` 均用 `tryCatch(..., error=function(e) figs)` 包裹：单图出错仅静默降级、不影响其他图形与整体返回（`.render_fig` 自身无错误保护）。
- 后续发布不再带本地 R 引擎，图形一律由 coze 端 R 引擎（`adapters/coze_project/src/r_engine/`）生成，故改动落在 coze_project 代码而非本地 r_engine。

### Verified
- R 语法：`parse()` 通过 `meta_analysis_core.R` / `run_task.R` / `network_meta_analysis.R`。
- 渲染层：合成多 type figures 调 `render_html_report(locale=zh/en)`，12 项 caption 断言全 OK（含 `L'Abbe` / `Egger's` 撇号转义归一化），`type_names` 无回退到裸 type。
- **未做**：coze 容器端到端 SVG 生成（需重新部署到 ct-meta2 端点；按发布红线未自动部署）。

---

## [2.1.6] — 2026-08-26 — 图形默认内联 + 停止 SVG 精简

### Changed
- **图形默认内联（强制）**：`SKILL.md` §5 明确 `figures[].svg` **默认内联渲染进对话流**，agent 须用 `show_widget` 内联展示，不得退化为仅文件卡片/附件；S3 外置仅影响传输层，不改变内联默认行为（`coze_client._fill_external_svgs` 默认回填内联 SVG）。
- **停止 SVG 精简、原样输出**：`run_task.R` 的 `.render_fig` 移除 `minify` 形参与 `.minify_svg` 调用，直接透传 svglite 原始字符串（`.minify_svg` 保留为 DEPRECATED 死代码，不再被调用）。`coze_contract.md` §5 同步声明 `figures[].svg` 为 svglite 原始输出、不做任何 minify。
- 4000 截断防护改为完全依赖 S3 外置（传输层）+ 字段重排 + `_trim_to_limit` 兜底，不再依赖体积精简。

### Verified
- `run_task.R` 源码自洽：`.render_fig` 透传、`minify` 调用已删、`.minify_svg` 仅注释保留，无悬空引用。

---

## [2.1.5] — 2026-08-26 — README 去除内部框架注解

### Changed
- `README.md` / `README_zh-CN.md` 示例 1 段落移除面向用户的代码关联注解：
  - 删除反引号文件路径引用 `` `references/topic-selection.md` ``；
  - 删除英文代码标签 `(Topic Selection)`、`(upstream gate)`、`Stage 1 Gate 1`、`Rule R7`；
  - `Full Assessment` 代码阶段名改写为可读描述「完整选题评估 / full topic assessment」。
- 保留用户可点击的 `references/ADVANCED*.md` 导航链接（非注解，正常文档链接）。

---

## [2.1.4] — 2026-08-26 — README 示例1 校正（改为探针真实证据）

### Changed
- `README.md` / `README_zh-CN.md` **示例 1 答案重写**：原答案把「非糖尿病 CKD」列为首选（新颖性 5、总分 18，称其为真实缺口），
  与 in-skill 去重探针实测矛盾——探针显示非糖尿病 CKD（Cochrane 20 / PubMed 2402）与透析/晚期 CKD（22 / 1067）**均已高度饱和**。
  改为基于探针真实命中数的结论：首选 **IgA 肾病肾保护**（4 / 224）、次选 **净获益框架**（5 / 442）、
  条件型 **特定肾小球疾病**（FSGS 0 / 膜性 1 / ADPKD 2 / 狼疮 3）；并保留「先用 ct-literature 全量确证缺口」的提示。
- 示例 1 下方「说明」同步明确：候选方向基于**自含去重探针（Cochrane + PubMed 真实命中数）**核查（R7 规则）。
- 全文简化，未机械复制候选地图。

---

## [2.1.3] — 2026-08-26 — 探针 ↔ ct-literature 无缝对接 + 快速检索提示

### Added
- `adapters/literature_probe.py`：输出新增 `ct_handoff` 块（Cochrane / PubMed 两层的 ct-literature 复现命令
  + 原始 Europe PMC 查询串 + “快速检查 vs 全面检索”提示）；`probe()` 单层与 `dedup_probe()` 均携带该块。
- `references/dedup-search.md`：新增「快速检查 vs 全面检索（何时用 ct-literature）」段，明确本探针只是
  选题去重快速检查，全面检索先走 ct-literature，并给出可直接复制的命令。
- `SKILL.md` §2.2：选题去重 self-contained 说明补一句——“快速去重检查，非全面检索；全面检索先使用 ct-literature”。

### Changed
- 回写 **ct-literature（v0.10.1）**：新增 `--cochrane` 检索能力（Europe PMC 期刊过滤，过滤串与探针
  **完全一致**，Cochrane 计数跨技能一致），使「选题去重（meta-analysis）→ 全面检索（ct-literature）」
  形成无缝闭环。

### Verified
- meta-analysis 探针 live 测试：`ct_handoff` 命令串正确、Cochrane 查询与 ct-literature `--cochrane` 同源；
  ct-literature `--cochrane` 全链路 live 测试（NSCLC）合并 10 篇 → Cochrane 过滤后 5 篇，publication 全为
  Cochrane、`is_cochrane` 全 True；两技能 `py_compile` 通过。

## [2.1.2] — 2026-08-26 — 选题去重自包含（in-skill Europe PMC 探针）

### Added
- **`adapters/literature_probe.py`**：选题去重自包含探针（不依赖其他技能、不依赖 coze）。直接调
  Europe PMC 公开 REST（MEDLINE/PubMed，无需密钥），仅用标准库 `urllib/json/re/time/datetime`，
  字段映射与查询语法复用 ct-literature `adapters/fetch_europepmc.py`、重试/退避复刻其 `http_utils`
  （429 读 `Retry-After` + 指数退避），但**独立实现在本技能内、不 import ct-literature 包**。
  两层：`cochrane`（按 `JOURNAL:"The Cochrane database of systematic reviews"` 精准过滤，
  经验证避免短语匹配虚高）+ `pubmed`（`systematic review OR meta-analysis`，近 5 年）。
  返回真实 `hit_count` + top titles；`dedup_probe()` 一次性出 Cochrane+PubMed 双层去重信号。
- 选题（Stage 4 / R7）改为**默认真实联网、自包含**：不再默认只给模板、不再委派 ct-literature/ct-registry。
  PROSPERO 与中文库仍保留为「手动/模板」步骤（无干净公开 API，如实标注），符合「技能不假装包办一切」的边界。

### Changed
- `references/dedup-search.md`：网络说明从「从不自动检索、只给模板」翻转为「默认 in-skill 探针真实检索」；
  三层去重表重写（Layer1–2 = in-skill 实时，Layer3/中文 = 手动模板）；新增「Run the in-skill probe」段与真实输出示例。
- `references/topic-selection.md`：Stage 4 改写，明确去重自包含（Cochrane+PubMed 走探针），R7 的「真实去重筛查」落到探针。
- `SKILL.md` §2.2：选题去重标注 self-contained，移除「Dedup searches run ONLY on user opt-in; otherwise deliver query templates」。
- `adapters/README.md`：文件树补 `literature_probe.py` 并注明为选题去重自包含探针。

### Verified
- 真实联网端到端测试通过：选题「PD-1 inhibitors NSCLC second line」→ Cochrane `hit_count=36`
  （全部 `is_cochrane=True`）、PubMed SR/MA `hit_count=5358`；`py_compile` 通过。

## [2.1.1] — 2026-08-25 — 文档清理收尾 + 三平台统一发布

### Changed
- **版本号升 2.1.1**：SkillHub 已占用 2.1.0（早期发布），且 SkillHub 不允许同版本重发；为保持 GitHub / SkillHub / ClawHub 三平台版本一致，升到 2.1.1 统一发布。
- **对外文档清理收尾**（本轮发布前）：SKILL.md §5.1 跨轮连续性协议全文英文化并删除 `ct-base/references/*` 死链；`## Language` 段改为符合 ct-base skeleton 标准表述（双语指针单行 + 核心语义句 "answer language follows the user's question language"）；`references/interactive_menu.md` 与 `README_zh-CN.md` 清除同类死链。
- 版本号引用统一：SKILL frontmatter + metadata + README（中/英）+ interactive_menu/ADVANCED + bug-report 示例统一为 2.1.1。
- **文档与代码对齐（2026-08-26 收尾）**：默认计算路径统一描述为 coze（终端用户零本地依赖）；requirements.txt 改为「默认零依赖」清单（cairosvg 仅 PNG 可选，R 包降为 coze 端/开发者维护说明）；ADVANCED.md / ADVANCED_zh-CN.md / r_packages.md 的 coze 项目 R 引擎维护命令（`Rscript src/r_engine/*`）移至 `adapters/coze_project/DEV.md`（git/clawhub 忽略、不发布）；**取消本地 R 回退**——`run_analysis.py` 重写为 coze-only（coze 不可达/未授权直接返回结构化错误，不再兜底本地），原 `adapters/local_engine.py` 移至 `adapters/_dev/local_engine.py`（git/clawhub 双重忽略、不随发布包分发，仅开发调试参考，已不在运行路径）；同步更新 SKILL.md（network_note/data 改 coze-only 无回退）、AGENTS.md（Execution backend / 环境检测 / 代码执行 / 安全红线 / Outbound calls / 目录树 全部翻转）、adapters/README.md（路由图/文件清单/配置/用法清除回退）、data_templates.md（移除 `prefer="local"` 引导）；AGENTS.md / SKILL.md 版本号对齐 2.1.1。

## [2.1.0] — 2026-08-25 — 跨轮上下文交互能力完善 + 发布自包含修复（ct-base 模式 A / Type-Compute）

### Fixed / 发布自包含（P0-2）
- **`merge_spec.py` 注入发布包**：`ct-base/scripts/publish_inject.py` 的 `SHARED_ASSETS` 清单补 `scripts/merge_spec.py`，发布时注入 `meta-analysis/scripts/merge_spec.py`；SKILL.md §5.1 命令与描述改为相对路径 `scripts/merge_spec.py`（不再悬空引用 `ct-base/scripts/`，符合 AGENTS §5 发布后不假设 ct-base 存在）。
- **`ct-base/references/*` 悬空引用加注**（P1）：SKILL.md §5.1 声明"开发底座文档、发布包不含、关键规则已内联"，消除用户/审阅者困惑。
- **版本号统一**：SKILL frontmatter + metadata + README（中/英）+ interactive_menu/ADVANCED + bug-report 示例统一为 2.1.0。

### Added / 跨轮连续性协议（发布前完善，沿用 2.0.6 条目）
- **SKILL.md §5.1 升级为可操作协议**：定义跨轮 spec 字段集（task/data_path/measure/model/method/yi/sei/slab/byvar + params 透传）、回显块强制格式与位置、数据集指针继承、列映射显式继承（最高风险点：漏带 = 效应量错配 = 结论级静默不一致）、task 切换字段规则；`merge_spec.py` 从「可选」提为「推荐」并给调用范式。
- **interactive_menu.md 新增 §6 多轮连续性实战样板**：四轮 few-shot（forest→subgroup→sensitivity→metareg），每轮回显块演示「读最近块、只改变化字段、列映射零丢失」；含漏带 `yi=eff` 导致静默错配反例。
- **ct-base 回写（家族标准）**：`compute_menu.md` 补 §6.3（数据集指针继承）/ §6.4（列映射与 task 切换字段规则）；`continuity.md` §1.4 加交叉指针；`continuity_lint.py` 已验证 `meta-analysis` COMPLIANT。

### Added / 跨轮连续性协议（发布前完善）
- **SKILL.md §5.1 升级为可操作协议**：定义跨轮 spec 字段集（task/data_path/measure/model/method/yi/sei/slab/byvar + params 透传）、回显块强制格式与位置、数据集指针继承、列映射显式继承（最高风险点：漏带 = 效应量错配 = 结论级静默不一致）、task 切换字段规则；`merge_spec.py` 从「可选」提为「推荐」并给调用范式。
- **interactive_menu.md 新增 §6 多轮连续性实战样板**：四轮 few-shot（forest→subgroup→sensitivity→metareg），每轮回显块演示「读最近块、只改变化字段、列映射零丢失」；含漏带 `yi=eff` 导致静默错配反例。
- **ct-base 回写（家族标准）**：`compute_menu.md` 补 §6.3（数据集指针继承）/ §6.4（列映射与 task 切换字段规则）；`continuity.md` §1.4 加交叉指针；`continuity_lint.py` 已验证 `meta-analysis` COMPLIANT。

---

## [2.0.5] — 2026-08-24 — 发布前合规整改（ct-base §16 检查 + 文档对齐）

### Changed / 发布前整改（2026-08-24 逐项落实）
- **清理 i18n `install.*` 残留键组**：删除 `scripts/i18n.py` 中 6 个无引用的 `install.*` 键（`cmd_header` / `cran_warning` / `confirm_prompt` / `manual_alt` / `network_warning_en` / `code_header`）——它们引用已不存在的 `--run-install` 本地 R 安装参数（coze-only 形态已移除），且 `install.cran_warning` 文案"（即本技能唯一会联网的操作）"与当前默认走 coze 云端的架构严重矛盾。删除后语法校验通过（§16.8 legacy 死参数清理）。
- **版本 bump**：2.0.0 → **2.0.5**（SKILL.md frontmatter + metadata 同步），CHANGELOG 补本条目（此前正文已提"修复见 2.0.1"的 dose_resp 修复，本次统一为 2.0.5 发布）。
- **SKILL.md 文档重构（§13.3/§4 对齐）**：9 段式框架（Triage→引导→初始化→核心→输出→安全→上传→Bug→元信息）；`## Language` 精简为链接；`## Bug Reporting` 只留行为规则；正文英文化（保留运行时用户双语文案 + 触发词）。
- **README 结构重排（§13.3）**：对话示例前置、出站披露收敛为「数据与隐私」节；实测记录迁至 ADVANCED。
- **ct-base 注解清理**：对外文档（README/SKILL/AGENTS/interactive_menu）清除 `（ct-base §X）` 引用；内部技术文档（ADVANCED/units 等）保留溯源（§4 文档清理边界）。
- **安全审计披露矛盾修复（SkillSpector §16.0）**：修正 `data:` 字段"no external data transmission"、README"never touches raw datasets"、bug-report"本地保存+邮件作者"等声明与实际不符处。
- **执行模式变更（安全预览 → 自动执行，2026-08-24）**：技能从「默认展示 R 代码、需说『请直接计算』才执行」改为**自动执行**——用户描述需求后技能自动完成分析并返回结果，无需触发词。同步更新 README（中/英）顶部简介、示例注记、FAQ、原「安全预览」节（改为「执行机制」）、出站披露触发时机（改为自动发送 + 每会话首次出站前披露一次）；AGENTS.md 执行规范（AUTO-EXECUTE）；interactive_menu.md 对应节。出站授权红线不变（默认端点白名单自动执行、自定义端点首次弹确认）。
- **本地引擎改为内部备用（2026-08-24）**：本地 R 兜底引擎（`adapters/local_engine.py` + `adapters/coze_project/src/r_engine/` 镜像）**代码保留**，但**不再对外文档说明**——README（中/英）、SKILL.md、interactive_menu.md 移除全部"本地引擎 / 本地兜底 / `prefer="local"` / 数据不出域可走本地"的用户导向表述，统一呈现为纯 coze 云端执行；AGENTS.md 标注 "internal only, not advertised"。本地兜底仅作 coze 不可用时的内部备用（不向用户宣传）。

---

## [2.0.0] — 2026-08-22 — 升级为云端模式 + 补齐 bug report 接入

### Added / 云端模式全面测试（ct-update 模式 B，按功能点 2 案例扩展）
- **模式 B 联调（ct-meta.coze.site/run 线上端点）**：按"每个功能点覆盖、每 task 至少 1 标准 + 1 变体"原则，将 `adapters/coze_cases/` 从 10 例扩展至 **46 个案例**，覆盖 contract §3 全部 **24 个 task 类型**（pairwise_meta / single_group_meta / subgroup_analysis / metareg / forest_plot / funnel_plot / labbe_plot / baujat_plot / radial_plot / bubble_plot / influence / trimfill / nma / nma_rank / survival_meta / dose_resp / diagnostic_meta / bayesian_pairwise / gosh / tsa / power / rob2 / esc / prisma_flow / prisma_checklist / grade / metainc / nnt / leave_one_out / cumulative_meta / selmodel / rve_meta / multilevel_meta / multivariate_meta）+ 维度变体（locale 中英 / colmap 自定义 / 多图组合）。
- **结果**：**44/46 通过**（含 2 个预期 `warn`：Egger 检验偏倚提示，属 Quality Gate 正常非阻断输出）；**2 个失败 = dose_resp（case19 continuous / case45 binary），属 R 端 `run_dose_resp` dosresmeta NSE 集成缺陷，待修复 R 端代码**（见 Pending）。其余 44 例功能完整。

### Fixed / bug report 接入缺漏（ct-base §20.3.5）
- **问题**：`adapters/config.json` 的 `auto_approve_endpoints` 仅含 `https://ct-meta.coze.site/run`，**缺少**统一 bug-report 端点 `https://ct-bugreport.coze.site/run`，违反 §20.3.5（每个技能须将该端点列入自动批准白名单）。
- **修复**：`auto_approve_endpoints` 追加 `https://ct-bugreport.coze.site/run`。
- **已合规项确认**：`adapters/bug_report.py` 已含 §20.3.7 的 `confirm_thanks()` / `build_followup()` / `parse_history()`；SKILL.md §20.3 章节与 README §5/§20.3 出站披露均已就位。

### Pending / 待确认（非阻断，记入发布报告）
- **clawhub_security_audit MEDIUM**：SKILL.md 第 91 行 + `scripts/i18n.py` 读取 `~/.workbuddy/MEMORY.md` 用于 R config（用户已授权、仅取 R 相关键、不发送个人内容）。审计认为超出技能窄范围，建议移除或收窄。属预存在设计，改动可能影响 R 配置功能，标记待用户确认，未擅改。
- **dose_resp R 端缺陷（模式 B 抓出，2026-08-23，**已修复见 2.0.1**）**：`adapters/coze_project/src/r_engine/advanced_functions.R` 的 `run_dose_resp` 用 dosresmeta 公式法 `(cases/n) ~ dose`（LHS 表达式），触发 2.2.0 内部 bug（`unique() applies only to vectors` / `'x' must have positive length`；as.name/字符串列名均不行）。case19（continuous）与 case45（binary）失败。**非测试设计错误，是技能 R 端代码缺陷**，修复见 2.0.1（v4：预计算效应量列 + 裸列名 + 参考组 se=NA + type factor，R 4.6.1 实测通过）。

---

## [2.0.1] — 2026-08-23 — dose_resp 崩溃修复（v4：dosresmeta 官方写法，R 4.6.1 实测验证）

### Fixed / coze 端 dose_resp「死机」——R 进程 segfault（根因链完整闭环）
- **第一层根因（文件版本错位）**：`run_task.R` dose_resp 分支已改**字符串列名**，但 `advanced_functions.R` 的 `run_dose_resp` 内部仍用 **`as.name()`** 转符号 → dosresmeta 内部崩溃。本机实测 as.name 版 exit=139 Segfault（进程崩溃 → Python 侧等不到 result → coze 画布卡死）。
- **第二层根因（dosresmeta 2.2.0 正确用法，R 4.6.1 实测推翻 v2 字符串方案）**：字符串列名也会崩（`non-numeric argument to binary operator`，因 dosresmeta 对独立参数 `eval(mf.id, data)` 会把字符串当字面量）。**正确写法**：
  1. formula LHS 用**预计算效应量列**（binary: `logrr=log(cases/n)`；continuous: `yi`），不能用 `(cases/n) ~ dose` 表达式（触发 `unique() applies only to vectors` / `'x' must have positive length`）；
  2. 独立参数 id/cases/n/sd/se 传**裸列名**（写入 df 后传 `_id_f`/`_cases`/`_n`/`_se_use` 等短名列），不传字符串也不传 as.name；
  3. binary 参考剂量组（dose 最小）**se 置 NA**（Greenland-Longnecker 约定），type 转 factor；
  4. covariance: binary=`"gl"`（需 cases/n），continuous=`"md"`（需 sd/n）。
- **修复**：`run_dose_resp` 重写为 v4（预处理 df → 短名列 → 官方调用）；`run_task.R` dose_resp 分支 plot 条件对齐（plots 空也默认出图）。
- **验证（R 4.6.1 + 干净 PATH，完整复现 coze 环境）**：case45 binary `status=ok figures=1`（coef=-0.0191, p<0.0001, SVG 8535 字符）；case19 continuous `status=ok figures=1`（coef=0.0145, p<0.0001）；pairwise_meta 回归 k=5 I2=0% OR=1.221 无破坏。
- **case 数据修正**：case19/45 原"每剂量点一个研究"（S1-S5）是错误结构，dosresmeta 需**单研究×多剂量点**——已统一 id 为 S1。
- **交付**：`meta-analysis-coze-full-v4.zip`（完整工程 113 文件 + 修正 case19/45）。

---

## [1.12.2] — 2026-08-20

### Fixed / 部署环境候选列表过时（libicu76）

- **问题（2026-08-20 部署日志暴露）**：`scripts/setup.sh` 的 libicu 多候选列表为 `libicu74|libicu72|libicu71|libicu70`（注释误标"Debian13=libicu74"），但实际 **Debian 13 (trixie) 为 libicu76** → 4 次尝试全失败（`E: Unable to locate package libicu74/72/71/70`），依赖符号链接兜底（`.76 → .74`）才通过——能工作但属 ABI hack。
- **修复**：候选列表 `libicu76` 前置（trixie 直接命中，跳过无谓失败 + 免符号链接）；`libgsl28` 前置（trixie 为 28，避免先试 27 失败噪音）；注释同步修正。
- **验证**：`bash -n` 语法 OK；线上 v1.12.1 当前运行正常（兜底生效、回归 6/6），本修复随下次部署生效，无需重启线上。

### Added / README 对话示例实测（ct-base §16.6 实测闸门留痕）+ 新增「选择候选方向」示例

- **实测（2026-08-20，coze 端点 `https://ct-meta.coze.site/run`）**：按 §16.6 逐个实测两份 README 的对话示例，**7/7 通过**——计算类示例 1（OR 配对）/2（d→logOR=1.451）/3（SMD+亚组）/6（PRISMA 流程图，`prisma_flow` task 实测可用）均返回真实 `stats`+`figures`+`repro`；行为类示例 4（Complex 路由菜单）/5（Vague grill-me）与 SKILL.md Triage 一致。完整报告：`meta_readme_test/README_EXAMPLES_TEST_REPORT.md`。
- **新增示例 7（中英 README + interactive_menu.md）**：「选择候选 Meta 分析方向」——应用 `references/topic-selection.md` Stage 1 Gate 1 产出 1–3 候选方向 + 四维评分 + Meta 类型决策树，属分析前上游门控、不调用 R 计算。
- **修复（§5 / §16.6 文档-行为一致性）**：README「安全预览」§4 原「所有计算均在本地——不上传任何用户数据」为 coze-only 形态前的旧文案，与默认云端 R 引擎 + 数据出站矛盾——已改为「默认云端 coze R 引擎 + 按 §5 出站披露；本地/离线走 `prefer="local"`」；`interactive_menu.md` 开头与 §4 同步修正。
- **标记待确认（未擅改）**：README 尾部版本号 v1.9.7 滞后于 SKILL.md/CHANGELOG v1.12.2（§16.5 一致性），版本号统一属发布决策，等用户确认后统一。
- **契约枚举补充（2026-08-20）**：coze_contract.md §3 补 `prisma_flow`（四阶段流程图，params: records/duplicates/screened/excluded_title/assessed/excluded_elig/included/reports）与 `prisma_checklist`（27 项检查表，params: `done`=已完成项 id 列表）两行——实现早已存在，契约枚举滞后，现已同步。
- **更正（2026-08-20，用户确认）**：本机有 R 4.5.1（`C:/Tools/R-4.5.1/bin/Rscript.exe`，仅开发双轨使用、不在 PATH），**发布形态为 coze-only**（本地 R 只用于开发）——早前实测记录"无本地 R"为 PATH 探测误判，已更正。

### Changed / 发布前合规审计（ct-base §5 / §13 / §16，2026-08-21）

基于 `ct-base` 治理规范对 `meta-analysis` 作发布前检查与修正（coze-only 发布形态，归 ct 花名册 A 档）：

- **版本对齐（§16.5/§16.6）**：`AGENTS.md` / `README.md` / `README_zh-CN.md` / `SKILL.md` frontmatter（`metadata.version` + `version`）统一为 `1.12.2`；此前 README 尾部 v1.9.7 滞后已修正。
- **SAFE PREVIEW 双语义（§4 / Example 1 / FAQ）**：纠正 coze-only 形态前的旧表述"生成并展示 R 代码、不执行 / 说 `--yes` 才运行"——改为"生成并展示**分析请求信封**（task/data/params/figure），由自然语言触发发送（"请直接计算"）；**无 `--yes` 参数**（coze 为无状态远程引擎，发送动作由纯语言指令驱动）。两份 README 同步。
- **出站元数据披露（§5）**：两份 README 出站披露块补充 `query_origin`（主机名 SHA-256 哈希，仅服务端归因/限流，非明文主机名）+ `locale`（OS 语言，双语用）说明。
- **§13.1 保密声明块补回**：A/B 两档 CT 全系列保密声明 + 固定联系方式 `medstatstar@gmail.com` 加入两份 README 末尾（1.8.0 曾以"非 ct 技能"误删，现归 ct 花名册 A 档须含）。
- **§13.6 适用人群块**：两份 README 插入 `## Who This Is For`（药企临床试验从业者 / 医护 / 医学生）。
- **§13.10 保密数据 FAQ 块**：两份 README 插入"数据要保密怎么办"——只发汇总统计量；不出域走本地引擎 `prefer="local"`；可获可复现 R 代码。
- **§8.6 query_origin 客户端实现**：`adapters/run_analysis.py` 默认 coze 分支客户端计算 `sha256(hostname)`（71 字符 `"sha256:"`+64hex）随请求发送，coze 端不兜底生成（客户端唯一真相源）；`coze_client.run_meta(..., query_origin=...)` 签名已支持。
- **§16.1 SKILL.md 瘦身（≤200 行）**：24 行 Core Functions 表外迁 `references/advanced_api.md`（长参考外迁 remedy）+ Interactive Guide / 渲染计时冗余压缩 → **216 → 187 行**。
- **§16.8 干净包清理**：取消跟踪废弃 R 脚本（`scripts/r_*.py` + `scripts/check_integrity.sh`，为 `adapters/coze_project` 镜像的重复件）、`tests/*`（保留物理、gitignored）、`assets/icon.png`（SkillHub 窄白名单拒绝 .png、且非 live 图标）；物理删除调试产物 `Rplots.pdf`。`.gitignore` / `.clawhubignore` 补充发布排除项。
- **network 一致性（§16.6）**：frontmatter `network: optional` + 已修正 `network_note`（"有本地兜底（需本机 R）时才 optional；多数终端用户走 coze"）属可接受表述，与 README 出站披露一致。

### Changed / 发布前合规审计第二轮（bugreport 合规 + §16.9 收口 + §3 统一，2026-08-22）

因 bugreport 功能上线（ct-base §20.3），重新以 ct-base 治理规范复检并修正：

- **§20.3 bug_report.py 同步最新模板**：补齐 `confirm_thanks()` / `parse_history()` / `build_followup()` 历史回执三件套及对应 `_MSGS`（thank/done/pending 中英），`send_to_endpoint()` 现回传 `history`（与统一端点历史回执协议对齐）；保留叶子技能内嵌公共 token（`get_endpoint_token()`，§5 XOR+base64 混淆，用户授权发布）。
- **§20.3.1 触发词**：SKILL.md frontmatter `triggers` 补 `上报bug` / `report a bug` / `错误报告`；Bug Reporting 章节补「发送后历史回执」说明（`confirm_thanks()` + `build_followup(parse_history(resp["history"]))`）。
- **§5 / §13 出站披露补全**：两份 README 出站披露块新增「错误报告端点披露」——说明 bug 报告仅发 11 键脱敏信封至 `https://ct-bugreport.coze.site/run`、不含分析数据/PII、附 `query_origin`+`locale`、拒绝则不出站、无云端调用则本地保存。
- **§16.9 出站收口**：`scripts/pdf_fetch.py`（Unpaywall API 外站检索）迁出"纯本地"的 `scripts/` → 归入出站专用目录 `adapters/pdf_fetch.py`；同步更新 `SKILL.md:123` 与 `references/review_workflow.md:110` 路径引用（CHANGELOG 历史条目保留原路径）。
- **§3 frontmatter 统一**：`description` 中文部分补齐与 `summary` 一致的「中英双语自动切换（默认英文/中文环境切中文）」一句，英文部分同步补 `Auto-switches language (defaults to English, switches to Chinese in zh-* environments)`；双语文档一致性保持。
- **§16.1 SKILL.md ≤200 行**：新增触发词 +3 行 + 历史回执说明，复验仍 **≤200 行**（通过）。
- **§16.8 干净包复验**：`git archive HEAD` 重建包无 `.png/.R/.pdf/.pyc/.dat` 泄漏；`adapters/bug_report.py` / `adapters/coze_token.py` / `adapters/config.json` / `adapters/pdf_fetch.py` 均含于包内。
- **§20.3.5 端点设计文档补齐**：新增 `references/bug_report_endpoint.md`（统一报告端点协议——信封/11 键白名单/服务端分派流程/响应信封/治理与合规），示例 skill 改写 `meta-analysis`；SKILL.md Bug Reporting 章节加指针。此前审计标记缺失，本轮补建入包。

## [1.12.1] — 2026-08-20

### Fixed / UTF-8 环境防御（jsonlite toJSON 中文损坏）

- **问题（实测复现）**：Windows `LC_CTYPE=C` 时 `jsonlite::toJSON` 把 UTF-8 中文按 Latin-1 转码——"检验"→`f#`（字节 `66 23`）、产生 `\u0010e` 控制字符、NUL 截断；**R 内存中叙述正常、写出 JSON 乱码，会骗过本地验证**（coze Linux 服务器不受影响，故部署端正常而本地误判/漏判）。
- **修复（`run_task.R` 顶部）**：`try(Sys.setlocale("LC_CTYPE", "en_US.UTF-8"))` + `try(Sys.setlocale("LC_ALL", "en_US.UTF-8"))`（`en_US.UTF-8` 在 Windows R 4.2+ 自动映射为系统 UTF-8 locale，实测有效）；引擎文件 `source(..., encoding = "UTF-8")` 显式指定编码。
- **验证**：模拟 `LC_CTYPE=C` 启动 → 修复代码生效后 toJSON 中文完整（"成功合并 5 项研究（随机效应 OR）。"、"检验"无损）；真实引擎 locale=zh 输出中文 JSON 正常（无 NUL/损坏）；回归 12/12 通过。

## [1.12.0] — 2026-08-20

### Changed / 方案 C 落地：R 出双语模板 + LLM 润色 + SVG 恒英文 + 本地渲染中文

**最终方案（用户决策 2026-08-20）**：coze 端 R 引擎按请求 `locale` 参数直出双语模板（数值 + 标准 label 精确），本地 LLM 收到后只做两件事——组织通顺的用户语言 + 按需补充解释；SVG 一律英文；中文（如项目名/研究名）由本地渲染层替换字体。

| 改动 | 说明 |
|---|---|
| **locale 参数驱动双语**（`run_task.R` 入口） | `params$locale`（支持 zh/zh-CN/cn/en/en-US，缺省 en）→ `.MA_LANG` 全局切换；**不读环境变量**（coze 容器语言 ≠ 用户语言）。语言决策权在本地 LLM |
| **`.msg` 双语模板恢复** | 面向用户的叙述（notes/warns/stop/PRISMA 27 项/GRADE 理由/quality gate 检查）按 locale 出中/英双语；164 处中文硬编码叙述包入 `.msg("en","zh")` |
| **`.msg_plot`（SVG 恒英文）** | 图内文字（图标题/轴标签/图例/"Pooled"/Study 标签/PRISMA flow label 等 42 处）一律恒英文，不受 locale 影响——规避 cairosvg/字体回退的中文渲染依赖 |
| **统一语言机制** | 删除 4 个引擎文件中的 10 处 local `.MA_LANG`/`.msg` 定义（环境变量检测旧机制），统一走 global locale 驱动版 |
| **本地渲染中文**（`adapters/rendering.py`，v1.11.2 已落） | `_fix_cjk_fonts`：SVG→PNG 时把含中文的 `<text>` 字体族替换为中文字体族（Win: Microsoft YaHei / macOS: PingFang SC / Linux: Noto Sans CJK SC / `RENDERING_CJK_FONT` 可覆盖），英文图零变化 |

**验证**：locale=zh → 顶层 notes="成功合并 5 项研究（随机效应 OR）。"、quality gate msg="k=5 通过"/"建议补充剪补法（k>=5）"、SVG 无中文字符（恒英文）；locale=en → 全英文；最终回归 21/21 通过。

> ⚠️ 实现注记：本轮曾尝试"coze 端语言中性（zh2en 214 处转英文）"（方案 A 实验），因用户最终选定方案 C 且 zh2en 批量脚本存在实现缺陷（误替换 .msg 参数/引号转义），已从 v1.11.1 上传包解出干净基线重建——引擎现为"v1.11.1 全部修复 + 方案 C 双语"。

---

## [1.11.2] — 2026-08-20

### Changed / 语言与中文渲染（coze 端语言中性 + 本地渲染中文支持）

**原则（用户决策 2026-08-20）**：coze 端只负责计算、不做语言输出决策；语言转换与呈现由本地大模型完成；SVG 图内文字中文支持由本地渲染层处理。

| 改动 | 说明 |
|---|---|
| R 引擎语言中性 | `.MA_LANG` 恒 `"en"`（不再读 LANG/LC_ALL 环境变量），`.msg(en, zh)` 恒返回 en；zh 参数保留作注释参考。coze 输出稳定英文结构化结果，不受容器语言影响 |
| R 引擎 214 处中文→英文 | 引号内硬编码中文（notes/warns/stop/PRISMA 27 项/GRADE 条目/图标签/可复现脚本模板）全部替换为英文；仅行内代码注释保留中文（不影响输出）。回归 19/19 通过 |
| **本地渲染中文支持**（`adapters/rendering.py`） | 新增 `_fix_cjk_fonts()`：SVG→PNG 路径把**含中文的 `<text>`** 字体族替换为中文字体族（Windows: Microsoft YaHei / macOS: PingFang SC / Linux: Noto Sans CJK SC；可用 `RENDERING_CJK_FONT` 覆盖）；纯英文/数字 text 不动 → 英文图像素零变化 |
| 中文字体实测 | coze SVG（font-family 恒 DejaVu Sans）经 cairosvg 渲染中文 study 标签为空白；`_fix_cjk_fonts` 后中文正常（像素验证：study 区深色 0.03→0.05~0.07）；英文 SVG 经 `_fix_cjk_fonts` 返回原字符串（零变化） |

**实测证据（2026-08-20）**：coze 端 svglite 输出中文数据完整（`<text>` 含"研究一"~"研究五"），但 font-family 恒 `"DejaVu Sans"` 无中文字体回退 → cairosvg 渲染空白。替换字体族后同图中文立即正常。浏览器内联渲染依赖系统字体回退，通常正常；PNG 转换场景由 `_fix_cjk_fonts` 兜底。

---

## [1.11.1] — 2026-08-20

### Removed / 清理（ct-base §5 凭据规范对齐）

- **删除历史遗留 `config/coze.dat`**：该文件是早期「落盘混淆」方案残留。凭据已内嵌 `adapters/coze_token.py` 的 `EMBEDDED_SECRETS`（§5 第 63 行规范：公开凭据须内嵌 `.py`，任何平台不丢）；`.dat` 不在 SkillHub 窄白名单（仅 `.svg/.py/.md/.json/.yaml/.txt/.toml/.csv`），发布时被服务端**静默剥离** → 属「无法发布」的遗留文件，且代码不依赖（`coze_token.py` 内嵌链 `CLI > env > 文件 > 内嵌`，删除后自动回退内嵌）。
- **`.gitignore` / `.clawhubignore` 新增 `config/coze.dat` 兜底排除**：防止未来 `store_token()` 本地覆盖再生成后误打包；`config/` 目录现为空。
- 验证：删除后 `get_token()` 内嵌解析 OK（非空）、coze 端点 health=True，功能零影响。

---

## [1.11.0] — 2026-08-20

### Added / 实现（终审清单剩余 10 项全部清零；用户决策「全部修正实现」）

| 项 | 实现 | 验证 |
|---|---|---|
| **A1** F→d | `.esc_convert` 加 `f→d`（F=t² → d=√F·√((n1+n2)/(n1·n2))） | F=6.25/n=30 → d=0.6455 ✅ |
| **A2** NNT | 新 task `nnt`：二分类 → metabin RD 合并 → NNT=1/\|RD\| + 95%CI | NNT=14.1，CI [8.4, 43.7] ✅ |
| **A3** metacor | `single_group_meta` 加 `r/n` 形态 → meta::metacor（单组相关系数） | k=6，ZCOR=0.523 ✅ |
| **A4** quality filter | `leave_one_out` 接线 quality 列：numeric ≥阈值（默认 6）/ "low risk" 筛选重合并 → extra.high_quality | k=4，est=0.263 ✅ |
| **A5** subgroup power | `power` 加 `subgroup_effects/subgroup_k` → 各亚组功效近似 | effect 0.3/k5→0.918、0.5/k8→1.0 ✅ |
| **A6** HK 修正 | `.meta_method` 加 hakn（model ∈ hk/hakn/knha）→ metabin/metacont/metagen 传 hakn；metafor 路径加 `.rma_test`（knha） | model=HK 正常拟合 ✅ |
| **A7** 95% PI | `.extract_meta`（fit$lower/upper.predict）与 `.extract_rma`（predict() pi.lb/pi.ub）加 pooled_pi | PI [0.147, 0.423]（exp [1.158, 1.527]）✅ |
| **A9** JC prior | `run_bayes_pairwise` tau_prior 加 `jeffreys/jc`（Half-Cauchy 近似，bayesmeta 无内置槽位） | post_mean=0.2866 ✅ |
| **A10** 结构矩阵 | `multivariate_meta` 加 `structure` 参数（UN/CS/HCS/AR1/ID/DIAG → rma.mv struct） | UN 拟合 ✅ |
| **A11** 真多结局 | `multivariate_meta` 检测 outcome 列 → rma.mv(mods=~outcome−1, random=~outcome|study, struct) → by_outcome + rho | OS 0.333 / PFS 0.434，rho=0.843 ✅ |

### Regression / 回归

- 最终重跑 20 个代表用例（覆盖二分类/连续/预计算/别名/亚组/元回归/NMA/贝叶斯/TSA/功效/RoB/可视化）**20/20 通过**，零破坏。
- 引擎 task 达 **40 个**（38 + nnt + multivariate 语义升级）。

### Notes / 说明

- 终审清单（meta_doc_impl_audit.md）**全部清零**：A1–A11 已实现；B1/B2 已实现；A8 中 Digitize 按用户决策不做；B3 环境限制维持。
- 待部署（发布动作须确认）：`run_task.R`/`advanced_functions.R` 本地镜像全部改动。

## [1.10.3] — 2026-08-20

### Added / 实现（终审清单 B1/B2/A8；用户决策：Digitize 不做，IPD 走 coze）

**B1 · 效应量 + CI 输入形态（零依赖）**
- 引擎数据形态新增 `has_ci`：接受 `te + ci_low + ci_high` 列，`seTE=(ci_high−ci_low)/(2·Φ⁻¹(0.975))` 换算后走 metagen（与 te 同尺度，log 尺度给 log CI）。验证：te+CI → OR=1.405（与直接给 seTE 一致）。

**B2 · IPD Meta 真实实现（走 coze；用户原则：技能只实现功能+披露，安全决策归用户）**
- `ipd_meta` 由"安全边界提示"改为真实分析：个体行（`study/trt/event`）→ 按 study×arm 聚合 2×2 → `metafor::rma.glmm(measure="OR")` 一阶段 GLMM（核心包零新增依赖）。验证：4 研究 / 1560 个体 → OR=2.175 [1.758, 2.690] + 森林图。
- SKILL.md Security & Scope / §6.7.3 同步：删除"不传输 IPD"绝对化表述，改为「数据出域决策归用户；技能负责实现 + 透明披露；coze 可满足安全合规；用户要求不出域时提供本地路径」。

**A8 · PDF 批量下载 + Screening（Digitize 按用户决策不做）**
- 新增 `scripts/pdf_fetch.py`（stdlib-only，opt-in）：DOI → Unpaywall 开放获取全文、PMID → NCBI elink → PMC 全文；逐条独立容错、无 OA 如实报告、不绕过付费墙。验证：CLI/错误处理/假 DOI 容错通过。
- `references/review_workflow.md` 新增「AI 辅助文献筛选（Screening）」agent 行为层流程（纳入/排除判定表 + 一致性规则）。

**原则写入 ct-base（用户决策）**：`ct-base/docs/02-governance-redlines.md` §6.7.4「功能实现 vs 安全决策分离」（§5 级全库原则）——技能只实现功能 + 透明披露，不因数据敏感预设"不提供"红线；是否出域由用户决策；出站披露/确认/PII 脱敏照常；用户要求不出域时提供本地路径。

### Regression / 回归

- B1/B2 改动后重跑 18 个代表用例 **18/18 通过**（含别名 colmap、te+CI、IPD）。

### Notes / 说明

- 待部署（发布动作须确认）：`run_task.R`（has_ci + ipd_meta 真实现）+ `scripts/pdf_fetch.py` + 文档（SKILL.md/review_workflow.md/coze_contract）+ ct-base §6.7.4。
- 终审清单剩余未做：A3 metacor / A5 subgroup power / A6 HK / A7 95%PI / A9 JC prior / A10 rma.mv 结构 / A11 真多结局（另行评估）；A8 中 Digitize 明确不做；B3 环境限制维持。

## [1.10.2] — 2026-08-20

### Changed / 收紧（出图格式约定：coze 恒 SVG，PNG 本地转换）

**用户确认的设计**：图形处理时 coze 默认只发送 SVG；需要 PNG 时由本地处理。

**改动**：
- `adapters/coze_client.py` `run_meta`：payload 强制 `figure.format="svg"`（覆写任何 png 请求）——coze 端**恒返回 SVG，零 png 路径**（不再可能回 png_base64）。
- `adapters/local_engine.py` `run_meta`：同样强制 `figure.format="svg"`（一致性）。
- `SKILL.md` Output 新增「出图格式约定」说明；coze_contract.md §5 png 选项注明"适配层强制 svg"。

**验证**：
- 请求 `figure.format="png"` → coze 返回 `figures[].format=['svg','svg']`，无 png_base64 ✅
- 本地 PNG 链 `render_figures(mode="png_file")`（cairosvg 2.9.0）：forest.png 78KB / funnel.png 38KB，0.43s ✅
- 说明：PNG 转换依赖本地 cairosvg（`pip install cairosvg`）；未装时 `rendering.svg_to_png` 给出明确安装提示（原行为保留）。

### Notes / 说明

- 待部署（发布动作须确认）：改动在 `adapters/{coze_client,local_engine}.py` + 文档。

## [1.10.1] — 2026-08-20

### Fixed / 修复（W1：Quality Gate 引擎侧接线，走查发现）

**缺陷**：`run_quality_gate` 在 dispatch **零调用**——SKILL.md 声称"coze 侧 R 运行 run_quality_gate → gate JSON → 红灯阻断"，但分析响应不产出 gate JSON，红灯判定完全依赖 agent 呈现层手动执行（流程走查 W1，P3）。

**修复**（`run_task.R`）：
- 合并类分支（`pairwise_meta`/`funnel_plot`/`trimfill`/`subgroup_analysis`/`metareg` + `survival_meta`）在 stats 产出后调用 `run_quality_gate(es_data, fit, bias_gate)`，结果写入 `stats$quality_gate`（含 `gate_json` 字符串，可直接喂 `scripts/quality_gate.py [--yes]` 人工签字门）。
- 偏倚核查扩展：`metareg`（rma 对象兼容，`fit$yi/fit$se` 兜底）与 `survival_meta` 补 Egger/Begg（此前无 `stats$bias`，会让 Quality Gate 误判红灯"偏倚清单缺失"）。
- bias 映射：`stats$bias`（egger_p/begg_p）→ `bias_gate`（egger/begg 键，匹配 `run_quality_gate` 期望结构）；`trimfill` 任务附加 trimfill 键。
- `capture.output` 包裹调用以吞掉 `run_quality_gate` 的 `cat(gate_json)` 日志噪音。

**验证**（本地 R 4.5.1）：
- 三态正确：k=2 → **red**（pooled_presentable=false，k 检查红灯）；k=5（有偏倚核查）→ **yellow**（证据体较小）；k=6 survival → yellow（建议 trimfill）；fd09_a trimfill（含 trimfill 键）→ **green**。
- **闭环**：引擎产出 `gate_json` → `quality_gate.py`：red 无 `--yes` exit=2（阻断）、`--yes` exit=0（放行）。
- 回归：合并类 4 例带 gate 正常；非合并类（nma/bayesian/tsa/rob2/图）正确无 gate；状态均 ok/warn。

### Notes / 说明

- 待部署（发布动作须确认）：改动在本地镜像 `run_task.R`；部署后线上合并类响应将含 `stats.quality_gate`。
- 4 类非计算流程域走查完成：Triage / Topic Selection / 上传文件全绿，Quality Gate 本次修复后闭环。

## [1.10.0] — 2026-08-20

### Added / 新增（补齐 13 项文档-实现缺口，本地引擎验证通过）

> 背景：ct-update §18 测试盘点确认「文档声明但引擎无 task」13 项（此前均返回 `unknown_task`），本次全部补实现；用户决策「文档不降级，补齐实现」。

| 新 task | 实现 | 本地验证 |
|---|---|---|
| `leave_one_out` | metafor::leave1out（逐项剔除敏感性） | ok（k=8，含逐项 estimate/CI/I²） |
| `cumulative_meta` | metafor::cumul（累积 Meta） | ok（k=8） |
| `selmodel` | metafor::selmodel（选择模型，发表偏倚校正） | ok（estimate + LRT_p，多版本槽位 tryCatch） |
| `bootmeta` | 手写非参数 Bootstrap（B 次重采样，REML） | ok（boot_mean/sd/CI） |
| `drapery` | 复用 plot_drapery（α 稳健性图） | ok（drapery 图） |
| `rve_meta` | robumeta::robu + clubSandwich::vcovCR(CR2)（RVE 稳健方差） | ok（CI 经 reg_table 提取，含 dfs） |
| `multilevel_meta` / `multivariate_meta` | metafor::rma.mv（研究随机截距，UN 结构） | ok（k=8，n_study=4） |
| `metainc` | 双形态：两组 `meta::metainc`(IRR) / 单组 `meta::metarate`(IR) | ok（IR=0.118） |
| `grade` | 自实现简化 GRADE（5 降级 + 3 升级因素） | ok（RCT+偏倚+I²80%+事件200+偏倚可能 → Moderate） |
| `prisma_checklist` | PRISMA 2020 检查表（27 项，可传已完成项） | ok（27 项，done 可标记） |
| `prisma_flow` | PRISMA 2020 四阶段流程图（ggplot 自绘） | ok（prisma_flow 图） |
| `ipd_meta` | 安全模型边界提示（coze 形态不收 IPD，明确引导本地引擎/汇总效应量） | warn（预期，含出域提示） |

### Fixed / 修复（4 项 P2 偏差）

| P2 | 问题 | 修复 | 验证 |
|---|---|---|---|
| esc 扩展 | 仅 6 种转换；d→logOR/mean→d/t→d 返回空 | 补 `mean→d`（合并 SD）、`t→d`、`d↔logOR`（d·π/√3）、`r↔d` 公式 | d→logOR=1.451、mean→d=0.500、t→d=0.635 ✅ |
| nma_rank rank | `rk$rank` 恒 NULL（netmeta 3.6.1 无此槽位） | 改用 `ranking.random` + `Pscore.random` | rank/pscore 均返回（A/B/C P-score 0.098/0.652/0.750）✅ |
| rob2 tool | tool 参数未使用，三工具渲染相同 | 域标签按工具映射（ROB2 5 域/ROB1 6 域/ROBINS-I 7 域）+ 标题带工具名 | ROB2/ROB1/ROBINS-I 均 ok，标签差异化 ✅ |
| Forest 主题 | `figure$theme` 0 引用，5 主题纯文档承诺 | 新增 `.theme_map` + `.forest_plot_theme`（revman/default/lancet/nejm/classic 配色映射到 meta::forest col.*） | theme=lancet 正常出图 ✅ |

### Regression / 回归

- 修复后本地引擎重跑 **28 个代表性用例（含全部 P0/P1 修复项）28/28 通过**，零破坏。
- 13 新 task + 4 P2 修复全部本地 CLI 验证（R 4.5.1；robumeta 装临时库，coze 镜像已含）。

### Notes / 说明

- **待部署**：全部改动在本地镜像 `adapters/coze_project/src/r_engine/{run_task,advanced_functions}.R`；部署属发布动作，须显式确认（重打包 → 部署 → §18.6 线上回归）。
- 引擎 task 由 25 → **38 个**；文档-实现缺口 13 项清零；P2 偏差 4 项清零。
- 剩余未覆盖：Topic Selection / Quality Gate / 上传文件 / Triage 四类非计算流程域（另行走查）。

## [1.9.9] — 2026-08-20

### Fixed / 修复（ct-update §18 全功能 NL 测试发现，83 例；本地引擎验证通过，待部署）

| 缺陷 | 根因 | 修复 | 验证 |
|---|---|---|---|
| **P0-1** NMA 二分类 arm-based 全挂（`object 'TE' not found`） | `.nma_prep` arm-based 二分类分支返回 `event1/n1` 形式，dispatch 却用 netmeta `TE/seTE` 对比接口 | arm-based 二分类分支改 **Haldane 校正自算 logOR/SE**（与对比输入分支一致） | fd11_a/c 本地 ok（k=4/6，n_treat=3） |
| **P0-2** NMA 别名列名必挂（`Treatments must be different`） | `.nma_prep` 仅解析 `cm$treatment`，study/event/n 未按 colmap 解析（study 退化为单研究 → 跨研究同处理对） | study/event/n 均按 colmap 解析（`tolower(cm$study/event/n)` 兜底） | fd11_b 本地 ok（k=5，n_treat=4） |
| **P0-3** 贝叶斯配对后验提取错误（`post_mean=2, CI=[0.1,3.9]`，真后验 0.287 [0.151,0.422]） | `bayesmeta$mu` 槽位实为 `mu.prior` 参数向量 `c(mean,sd)`，`mean(res$mu)`/`quantile(res$mu)` 取到先验参数；且不同版本 `$summary` 行列方向不同 | 一律从 `$summary` 提取，兼容参数行×统计列 / 统计行×参数列两种方向 | fd14_a/b/c 本地 ok，后验 0.2866/0.2847/0.2844 ✅ |
| **P1-4** Egger/Begg 发表偏倚检验未实现（`stats.bias` 承诺缺失） | `funnel_plot`/`pairwise_meta` 等分支仅合并+画漏斗图，从未调用偏倚检验（`run_task.R` grep `regtest|ranktest` 零命中） | **补实现**：`funnel_plot`/`pairwise_meta`/`trimfill`/`subgroup_analysis` 拟合后调 `metafor::regtest()`/`ranktest()` 写入 `stats.bias`（metafor 为核心依赖，零新增安装；k≥3 才计算，tryCatch 兜底 NA；Egger p<0.10 加偏倚警告） | fd08 对称数据 p=0.547 不警告 / 不对称 p=0.029、0.0002 正确警告 ✅ |

**回归**：修复后本地引擎重跑 18 个代表性用例（二分类/连续/预计算/生存/单组率/亚组/元回归/剪补/敏感性/TSA/功效/RoB/可视化），18/18 通过，零破坏。

### Notes / 说明

- 由 `meta_test` NL 测试套件驱动（ct-update §18：60 首轮 + 23 补测 = 83 例）；用例/执行器/复现脚本待归档至 `tests/`。
- **待部署**：修复仅落地本地镜像 `adapters/coze_project/src/r_engine/run_task.R`（唯一源，无其它同步副本）；部署属发布动作，须显式确认后执行（三端同步已无 → 重打包 → 重部署 → §18.6 线上 83 例回归）。
- **未处理（另行评估）**：13 项文档声明但引擎无 task 的功能（multilevel/multivariate/IPD/cumulative/leave_one_out/selmodel/bootmeta/drapery/grade/prisma_checklist/prisma_flow/rve_meta/metainc → 均 `unknown_task`）；P2 偏差 4 项（Forest 5 主题 `figure$theme` 未消费、rob2 `tool` 参数未使用、esc 扩展转换返回空、nma_rank rank 提取 None）。

## [1.9.7] — 2026-08-19

### Added / 新增（上传文件处理对齐 ct-base §6.7）

- **SKILL.md 新增「上传文件处理 / User-Uploaded Files (ct-base §6.7)」章节**：区分两类上传——
  - **结构化数据文件（csv/xlsx/xls）**：走既有 Type 4 数据模板验证路径（`references/data_templates.md`），不适用文档→md 转换，但 §6.7.2 信息透明与 §6.7.3 保密边界生效；
  - **文档/模板类（docx/pptx/pdf/doc）**：先按 §6.7.1 分层转 md 再提取研究数据（`.docx/.pptx` → 共享转换器 `scripts/office_to_md.py`；`.pdf` → 环境 pdf 技能；`.doc` → 提示安装 word-reader/antiword；扫描件 → 提示提供文字版）；
  - **转换前必向用户展示 §6.7.2 提示**（PPT 转换丢非文本元素）；
  - **保密处理（§6.7.3）**：技能不主动拦截，coze 仅收汇总统计量（不含 IPD），用户明确要求数据不出域时引导本地引擎（`prefer="local"`）。
- **`references/data_templates.md` Type 4 补充文档上传指针**：非结构化文档不属 Type 4 范围，指引到 ct-base §6.7。
- **新增 `scripts/office_to_md.py`**（ct-base §6.7 共享件副本，stdlib-only，docx/pptx → md 单一解析器，与底座字节级一致）。
- **SKILL.md frontmatter 版本对齐**：1.8.3 → 1.9.7（消除长期漂移，与 CHANGELOG 一致）。

## [1.9.6] — 2026-08-19

### Changed / coze 端工作流调整（内部实现，细节不随发布）

- coze 端进行工作流调整（含运行日志记录机制与 skillname 更正 `meta`）。相关实现位于 `adapters/coze_project/`（Coze 远端镜像，§16.7 目录级排除、**不随技能发布**）；接口契约见镜像内 `coze_contract.md`（不发布）。本条目仅保留功能性概要，不披露内部实现细节。

## [1.9.7] — 2026-08-19

### Added / 新增（出图模式 + 渲染计时）

- **`figure_mode` 出图模式选项**（`adapters/run_analysis.py` 新增 `render_figures()`）：
  - `svg_inline`（默认）— `figures[].svg` 原样保留，agent 内联渲染
  - `png_file` — 本地 `cairosvg` 转 PNG 文件存 `out_dir/`，figures 替换为 `{type, format:"png", path}`；不占 LLM 上下文、界面渲染更快，但变位图
- **渲染计时（★ 本地渲染阶段，非 coze 计算）**：
  - `coze_client.run_meta` 仍测 coze 往返但**改名 `coze_elapsed_seconds`**（仅诊断参考）
  - `render_figures()` 新增 `render_elapsed_seconds` = 拿到 SVG → 处理 → widget/PNG 就绪的秒数（本地精确测）；界面浏览器渲染无法在 agent 侧计时，用 `render_svg_kb` 作代理
  - 阈值常量 `RENDER_SVG_THRESHOLD=30s` / `RENDER_SVG_KB_THRESHOLD=200KB`，超阈值自动生成 `render_hint`（中文），提示切 `png_file`
- **svglite 2.2.2 缺 `</g>` 修复**（`rendering.py` 新增 `_fix_xml()`）：用标签栈补齐缺失闭合（浏览器宽容但 cairosvg 严格解析失败；仅 PNG 路径使用）
- **SKILL.md Output 章节**更新：figure_mode 选项 + 渲染计时规则 + agent 必须在回复中体现 render_hint
- **inline_rendering.md §7** 新增：出图模式 + 渲染计时完整说明；坑列表补 svglite 缺闭合

### Notes / 说明

- coze 端**零改动**（png_file 是呈现层本地转换）；coze_elapsed_seconds / render_elapsed_seconds 语义分离，避免混淆"哪个时间"

## [1.9.8] — 2026-08-19

### Added / 新增（ct-base §5 coze 出站授权规范落地）

- **出站披露（§5 强制）**：SKILL.md 执行模型 + README/README_zh-CN 双份新增"数据将发送至 https://ct-meta.coze.site/run"披露声明（发送内容 = 分析数据，不含 PII）；杜绝"出站却声称零出域"
- **首次出站授权门控（§5 AUTH-BLOCK 范式）**：`coze_client.py` 新增 `_auth_gate()` / `approve_endpoint()` / `AuthRequiredError`——端点不在白名单 → stderr 输出 AUTH-BLOCK + 统一确认文案（目标服务器/发送内容/本地资料有限说明）；用户确认后写入 `adapters/config.json` `auto_approve_endpoints`（agent 绝不代写）；默认端点已**作者预置**（正常用户无感），自定义端点才弹确认
- **未授权不阻断（§5）**：`run_analysis.py` 捕获 AuthRequiredError → 优先本地兜底（notes 注明"本次未使用云端分析"）；本地不可用返回 `_source=auth_blocked` 明确提示（授权问题可解决，不抛 RuntimeError）
- **出站 payload 脱敏（§5）**：`sanitize_payload()` 发送前剥离 PII（身份证/手机号/邮箱，递归清理嵌套结构）
- **agent 行为规则（§5 出站全程确认）**：SKILL.md 新增——forward 前**恰好一条**流程通知；coze 失败**先问用户**是否允许诊断，拒绝则交付本地答案 + 显著警告

### Notes / 说明

- 凭据本就符合 §5（coze_token.py XOR+base64 混淆，README 声明非真加密）；config.json 仅含白名单（无凭据），随技能发布（作者预置设计）

---

## [1.9.5] — 2026-08-19

### Added / 新增（结果呈现规范）

- **内联渲染规范** `references/inline_rendering.md`：所有 `figures[].svg` 默认**内联渲染进对话流**（非附件），含：
  - **根因修复**：①svglite 内容超界（森林图实测 x∈[-140,644]，实际宽 785px 而 viewBox 仅声明 504px）→ `content_bbox()` 扫描内容极值动态扩展 viewBox；②**内部 clipPath 裁剪**（svglite 固定 0..504 clip 裁掉左右文字列，viewBox 扩展也无效）→ `_strip_clip()` 移除；③transform 旋转文本纳入 bbox（translate 锚点 + textLength 双向扩展）
  - **正式模块** `adapters/rendering.py`：`extract_svg` / `_strip_clip` / `content_bbox` / `build_figure_widget`（标准库零依赖，含 points 超长行拆分、px 后缀、transform 文本保守覆盖等实测处理）
  - **宽度策略**：SVG 固定实际内容宽度不缩放 + 外层 `overflow-x:auto` —— 容器装不下（含正常对话窗）即出横向滚动条；`margin:0 auto` 水平居中（窄容器自动回左对齐可滚动）；**y 方向 pad_y=24 上下留白（所有图统一）**；备选自适应模式仅在用户明确要求铺满时启用
  - 可选缩放控件（− / 适应 / ＋）
- SKILL.md `## Output` 更新：默认呈现 = 内联渲染（引用 inline_rendering.md），同时 output/ 落盘供下载/编辑
- **统一要求上收 `ct-base/BASE.md §19`**（docs/06-inline-rendering.md，全库强制）——本技能 `rendering.py` 为 §19.6 参考实现

### Notes / 说明

- 内联渲染由 agent 侧（LLM 呈现层）消费 `figures[].svg` 字符串完成，**coze 端无需改动**（返回已是标准 SVG）

---

## [1.9.4] — 2026-08-19

### Fixed / 修复（coze 端点默认值误报不可达）

**缺陷**：`adapters/coze_client.py` 的 `DEFAULT_ENDPOINT` 写死本地开发占位 `http://localhost:5000/run`；真实端点 `https://ct-meta.coze.site/run` 只记录在 `coze_integration_test.py` 注释。用户未配置 `COZE_META_ENDPOINT` 时，请求打到本机被拒 → `run_analysis` 误判 coze 不可达 → 错误回退本地（用户侧排查确认：401 仅缺 token，连接本身正常）。

**修复**：
1. `coze_client.py`：`DEFAULT_ENDPOINT` → `https://ct-meta.coze.site/run`（零配置即用）；docstring/错误提示同步。
2. `coze_client.py health()`：探测 `/health` 路由（自定义域名未必存在）→ 探测 `/run` 可达性（2xx/4xx/5xx 均视为可达，仅网络层错误判不可达）。
3. `SKILL.md` / `adapters/README.md`：默认端点描述同步。

**验证**：无环境变量下 `_endpoint()`=真实端点、`health()`=True、`run_meta` 跑通（status=ok + repro 返回）。

**补充修复（同日）**：`run_meta()` 的 URL 拼接 `_endpoint() + "/run"` 在 `COZE_META_ENDPOINT`/`DEFAULT_ENDPOINT` **已带 `/run` 后缀**时会拼成 `/run/run` → HTTP 404 `{"detail":"Not Found"}`，与 1.9.4 的默认值修复叠加后仍会误判 coze 不可达。修复：endpoint 以 `/run` 结尾时直接使用，否则自动拼接。验证：`health()`=True；真实分析（5 项 RCT pairwise_meta）经默认端点跑通，status=ok。

---

## [1.9.3] — 2026-08-19

### Changed / 变更（删除冗余 r_engine/，引擎统一到镜像）
- **技能根 `r_engine/` 删除（用户决策）**：本地引擎唯一来源 = `adapters/coze_project/src/r_engine/`（coze 远端双向同步唯一源）；本地测试/开发直接调用镜像内引擎，消除双份副本漂移风险。
- `adapters/local_engine.py` 默认 `META_LOCAL_ENGINE_DIR` 改为 `<skill>/adapters/coze_project/src/r_engine`（实测 fd01_a 通过：status=ok + repro 字段返回）。
- 文档同步：SKILL.md / AGENTS.md / adapters/README.md / coze_client.py 全部 r_engine 引用改为镜像路径；.gitignore 删除 `r_engine/*.R` 规则（目录已不存在，镜像整体已排除）。

---

## [1.9.2] — 2026-08-19

### Changed / 变更（coze 项目镜像统一到技能内）
- **镜像位置统一（用户决策）**：coze 项目本地镜像迁至 `adapters/coze_project/`（含 `coze_contract.md`、`src/r_engine/*.R`、`scripts/`、`docker/`），**作为与 coze 远端双向同步的唯一源**；不再使用工作区 `coze_meta_project/` 作为主镜像（保留为历史快照）。
- **发布排除（红线）**：`.gitignore` 重写（修正过时"Python 模板内嵌"注释）+ 新增 `.clawhubignore`——`adapters/coze_project/` 与 `r_engine/*.R` 均不随技能发布（`coze_contract.md` 属 ct-base §16.7 红线）。git archive 实测发布包 0 命中。
- **adapters/README.md**：路由策略更新为「发布 coze-only + 本地兜底仅开发者用」；新增「coze 项目镜像双向同步约定」章节（本地→coze 打包部署 / coze→本地导出覆盖 / diff 一致性基准）。
- 一致性验证：`adapters/coze_project/src/r_engine/` ≡ 技能 `r_engine/`（diff 为空）。

---

## [1.9.1] — 2026-08-19

### Changed / 变更（发布形态决策 + 复现性增强）
- **发布形态决策（用户拍板）**：对外发布 **coze-only（thin client）**——所有 R 计算经 coze 工作流，本地 LLM 仅做需求标准化/数据整理/结果呈现；**最终用户无需安装 R**。本地 `r_engine/` 保留为**开发/复现镜像**（与 coze 字节级同源，开发者经 `META_LOCAL_ENGINE_DIR` 启用）。SKILL.md Initialization 同步更新。
- **复现性（必须满足）**：每次分析输出新增 `repro` 字段 = ①可复现 R 脚本（`deparse(df)` 数据构造 + 按 task 的核心调用 + R/包版本报告，本地 R 直接 source 即可复现）②`r_version` ③`packages`（核心包版本号）。实现于 `run_task.R .repro_script()`，覆盖全部 16 个 task 分支（nma 用 `prep` 对比格式、dose_resp 用 `yi ~ dose` 公式等）。
- **coze 端版本报告**：`http_run.sh` 健康检查升级——打印 `R.version.string` + 核心 14/可选 2 包版本号（`[启动] R 版本 / 包 xxx ✅ vX.Y.Z`），下次部署日志即得基线版本。
- **coze_contract.md**：§4 出参 schema 增加 `repro` 字段说明；新增 **§8 coze 端环境版本**（R 4.6.1 实测基线 + 本地复现差异注意，以部署日志为准）。
- 96 例 dryrun 无回归（ok=87 err=0）；5 个代表案例 repro 脚本实测可执行。

---

## [1.9.0] — 2026-08-19

### Changed / 变更（coze 96 例联调闭环：依赖瘦身 + 15 处引擎修复 + 用例修正）
- **R 包清单瘦身**（单一可信源 `docker/r_packages.txt`）：核心 14（metafor/meta/netmeta/bayesmeta/dosresmeta/mada/robumeta/clubSandwich/ggplot2/svglite/forestploter/jsonlite/dplyr/scales）+ 可选 2（ggrepel/robvis）。移除：`esc`（effect_size_conversions.R 重写为 metafor::escalc + 标准公式，输出结构不变）、`metagear`/`gridExtra`（零引用）、`gemtc`/`rjags`/`multinma`（贝叶斯 NMA 后端移除，coze 容器无 root 无法装 JAGS——`bayesian_nma` 为已知环境限制，联调 MANIFEST 标记 `expected`）。
- **run_task.R 引擎修复**（96 例联调驱动，15 处）：colmap 统一小写（数据形态识别）；metaprop method 映射（meta≥8 仅 Inverse/GLMM）；metacont/metagen/metamean 移除已废弃 method 形参；method.tau 回退 "DL"；`.bubble_plot` ggplot 自实现（metafor::bubble 未导出）；influence 改 metafor::rma.uni 路径；`.nma_prep` 二分类 Haldane 校正自算 logOR（netmeta 统一对比路径）；netrank 用 `rk$rank` 提取；dose_resp 透传 cases/n/se/sd/type；bayesian_pairwise 后验稳健提取；tsa 传 data.frame；rob2 交通灯图 ggplot2 自绘（去 robvis 依赖）；esc 自实现 `.esc_convert`；`.engine_dir` 防御 `nzchar(NA)` 陷阱（source 调试场景）。
- **advanced_functions.R 修复**：run_diagnostic_meta 列名小写归一（tp/fp/fn/tn）；mada SROC 改 S3 泛型绘图；`.rob_colour` + ggplot2 自绘交通灯/汇总图。
- **用例生成器 `gen_meta_cases.py`**：dose_resp 用例修正（dosresmeta gl 法要求每 study 参考剂量组 se=0，否则 grl 崩溃——用例数据 bug）；MANIFEST.csv 新增 status 列（`expected` 豁免）。
- **`coze_contract.md`**：§6 包清单同步核心 14+可选 2；task 枚举表全量更新为实际实现。
- **`adapters/coze_integration_test.py`**：判分对齐 ct-base §18.4（ok/warn/None 通过）；新增 MANIFEST expected 豁免。
- **线上验证**：96 例联调全绿（90 ok + 3 warn[esc 近似] + 3 expected[bayesian_nma]），对比修复前 53 ok/43 error。相关标准已沉淀至 ct-base §18（BASE.md v1.1.41）。

---

## [1.8.3] — 2026-08-17

### Changed / 变更（执行后端双轨化：coze 默认优先 + 本地 R 兜底）
- **Reversed 1.8.2 "full coze transfer"**: 技能重新保留本地 R 分析能力，但默认一律优先调用 coze 工作流；
  本地分析仅作为 **coze 调用失败时的自动兜底**，或 **用户明确要求本地/离线分析** 时启用。
- 统一入口 `adapters/run_analysis.py`：`prefer="coze"`（默认）先调 coze，失败自动回退本地并标记 `_source="local_fallback"`；
  `prefer="local"` 仅本地、不触 coze。返回结果统一带 `_source` 字段（coze / local_fallback / local）。
- 新增 `adapters/local_engine.py`：subprocess 调用技能内置 `r_engine/run_task.R`（与 coze `src/r_engine/` 字节级同源，靠 `coze_contract.md` 同步）。
- 技能 `r_engine/` 重新放回（统一 dispatcher `run_task.R` + 各引擎 .R），作为本地兜底镜像（非权威副本）。
- `SKILL.md` / `AGENTS.md` / `adapters/README.md` 同步更新：双轨执行模型、环境检测、安全红线、目录结构。

---

## [1.8.0] — 2026-08-02

### Added / 新增
- **ct-base alignment**: comprehensive alignment with `ct-base` BASE.md specification.
  - Added `AGENTS.md` (English-only agent-facing rules: environment, execution, language, security, reuse, menu triage, traceability).
  - Added `CHANGELOG.md` (this file).
  - Added `references/units.md` (atomic task unit index for pipeline).
  - Added `scripts/i18n.py` (from ct-base — bilingual EN/ZH helper with auto locale detection).
  - Added `scripts/r_libs.py` (from ct-base — R invocation + validation + sanitization helper).
  - Added `references/language_policy.md` (from ct-base — detailed bilingual policy).
  - Added `references/report_template.md` (from ct-base — report skeleton reference).

### Changed / 变更
- **SKILL.md**: frontmatter enriched with `required_commands: [Rscript, python]`. Body remains English-only agent-facing.
- **README files**: renamed `README_ZH.md` → `README_zh-CN.md` per ct-base naming convention.
- **Language detection**: migrated to `i18n.py`'s unified `is_chinese_os()` (covers env vars + Windows API + Python locale fallback).
- **User menus & README (UI polish)**: SKILL.md Triage §5.2 now explicitly lists the "③ Can't decide? → explain the differences between these choices" routing-menu entry; README Complex popup-menu / Vague grill-me examples made more human-friendly so carbon-based users find it easier to use.

### Fixed / 修复
- Removed stale `README_ZH.md` references across SKILL.md, README.md, README_zh-CN.md.
- **English README untranslated Chinese**: translated all residual Chinese in `README.md` (Example 1 "You say", Scenario Index "Try saying" tables, §4 title) to English; synced version string to `1.8.0` in both READMEs.
- **Security-audit doc alignment** (SkillSpector 10 Medium/Low findings — all documentation-consistency, no malicious code):
  - Removed the `Confidentiality Notice` block from `README.md` — eliminates the "summary stats only" vs "supports IPD patient-level data" trust-boundary contradiction, and also complies with the earlier user instruction that non-`ct-` skills omit confidentiality statements (the zh-CN README never had it).
  - Added PDF-batch-download warnings (network access / local write / copyright) in both READMEs (§7).
  - Clarified the high-friction trigger rule in both READMEs' FAQ: code runs only when you explicitly say "execute"/"请直接计算"; casual mentions do not trigger execution.
  - Clarified the language-switch note: default follows OS locale and only affects display language, no extra authorization needed.
  - Tightened `SKILL.md` Memory-read scope note: "(R config keys only; no personal info is read or sent)".
- **ClawHub display-name fix**: republished with a clean top-level directory name `meta-analysis` so the ClawHub page title shows the correct skill name instead of the previous temp publish-folder name "Meta Analysis Strip V180".

---

## [1.8.1] — 2026-08-02

### Fixed / 修复
- **ClawHub display-name fix**: republished with a clean top-level directory name `meta-analysis`, correcting the ClawHub page title that wrongly showed "Meta Analysis Strip V180" (caused by the previous temp publish-folder name, which ClawHub used as the display name fallback).
- **Carries the v1.8.0 GitHub documentation-alignment to the marketplaces**: English README residual Chinese fully translated; `Confidentiality Notice` removed (resolves IPD-vs-summary-stats trust-boundary contradiction, complies with the non-`ct` no-confidentiality rule); added PDF-batch-download warnings, high-friction trigger clarification, and language-switch note in both READMEs; tightened `SKILL.md` Memory-read scope note.

---

## [Archived] — 2026-08-15 遗留条目（所列功能：r_engine/ 架构重组、Quality Gate、Topic Selection 模块——已验证全部实际落地并随后续 2.9–2.11 期间版本发布，此处仅存档，不再定版；2026-10-09 发布前检查时归档）

### Changed / 变更
- **Architecture restructure (ct-base §16.9 / future Coze workflow prep)**: all R-software-invoking code moved out of `scripts/` into a dedicated **`r_engine/`** folder (templates `r_*.py` + generated `*.R` + `r_libs.py` + `check_integrity.sh`). `scripts/` now holds only pure-local Python (`i18n.py`, `generate_topic_report.py`, example JSON). A reserved **`adapters/`** folder documents the future unified Coze workflow call layer (see `adapters/README.md`; `ct-samplesize`-style backend selection planned). All references updated: `SKILL.md`, `AGENTS.md`, `references/*.md` (`source("r_engine/*.R")`), `tests/*.R`, `.gitignore` (`r_engine/*.R`). `r_libs.py` gained a sys.path bootstrap to keep importing `scripts/i18n.py`. `check_integrity.sh` multi-line `_msg` quoting fixed (pre-existing latent bug, surfaced by bash strict mode).

### Added / 新增
- **Quality Gate (human sign-off + R red-light, ct-update upgrade A)**: numeric trustworthiness hardening inspired by O0000-code/meta-analysis-skill. New R function `run_quality_gate(es_data, model, bias_result)` (r_engine/meta_analysis_core.py) computes red/yellow/green flags **in R** (never LLM-read): k<3 red, I²>75% red → pooled estimate NOT presented, publication-bias checklist (Egger/Begg) missing → red; zero-dependency hand-written JSON output. New `scripts/quality_gate.py` consumes the gate JSON as the human sign-off gate: red → blocked (exit 2), `--yes` records human sign-off (exit 0), yellow → warn (exit 1), green → pass. SKILL.md Output section documents the gate; SKILL.md kept at 199 lines.
- **Topic Selection module（选题评估 · upstream gate）** — reference-designed from the public `meta-analysis-topic-selector` skill (ClawHub @wenhan9739), adapted to this skill's local-first architecture:
  - Dual path entry: **Quick** (≤30 min, 1-page decision card) / **Full** (5-stage workflow with decision gates).
  - Four-dimension scoring model (clinical value / methodological feasibility / data availability / novelty, 0–5 each, total 0–20, any ≤2 = veto).
  - Cross-check rules R1–R6 (automatically detected internal contradictions force re-review).
  - PICO/PECO operational decomposition (`references/pico-guide.md`).
  - Three-layer dedup search (PROSPERO → Cochrane → PubMed; non-English opt-in) + near-duplicate judgment matrix + increment statement (`references/dedup-search.md`).
  - PRISMA 2020 (11 key items) + AMSTAR-2 (7 critical domains) topic-stage pre-check (`references/compliance-precheck.md`).
  - Meta-type decision tree (pairwise / NMA / IPD / dose-response / DTA / single-group…).
  - 11-section topic report via `scripts/generate_topic_report.py` (JSON → Markdown/HTML, stdlib only) + manual template (`references/topic-report-template.md`) + PROSPERO field mapping (`references/prospero-mapping.md`).
  - New references: `topic-selection.md`, `pico-guide.md`, `dedup-search.md`, `compliance-precheck.md`, `topic-report-template.md`, `prospero-mapping.md`; example input `scripts/topic_report.example.json`.
  - `SKILL.md`: Level-1 menu gains `0️⃣ Topic Selection`, Triage Vague row routes "无选题/可行性评估" to the module, References table updated (SKILL.md kept at 200 lines).
- **ct-update competitor registration (2026-08-15)**: added `meta-analysis-topic-selector` (★★★★★) and `meta-analysis-journal-selector` (★★★★) (ClawHub @wenhan9739) to the meta-analysis competitor list with seed keywords.

### Changed / 变更
- `SKILL.md`: Language section compressed; Initialization integrity-check block inlined; Level-1/Level-2 menus reformatted to fit the new entry while keeping ≤200 lines.

---

## [1.8.3] — 2026-08-02

### Fixed / 修复
- **IPD trust-boundary contradiction (SkillSpector finding)**: rewrote `AGENTS.md` §4 security red-line — the old line stated "no patient-level data" while the skill advertises IPD meta. New wording clarifies that **all data you provide, including IPD, is processed locally from your own files and never uploaded or sent anywhere**; IPD is fully supported and handled the same local-only way. This closes the real source of the "summary stats vs IPD" divergence finding (the earlier `README.md` Confidentiality Notice removal addressed a duplicate copy of the same phrase).

---

## [1.7.0] — 2026-08-01

### Added / 新增
- Full bilingual auto-switch: default English, auto-switch to Chinese on `zh-*` locale (`.msg(en, zh)` pattern in R files + Python i18n).
- `permissions` block declaration in SKILL.md frontmatter.
- `references/svg_editing.md` — SVG editing tools & journal format conversion guide.
- `references/advanced_api.md` — reusable API reference for TSA / dose-response / survival / Bayesian NMA wrappers.

### Changed / 变更
- Effect size conversion module (`esc`) expanded: d ↔ g ↔ logOR ↔ r ↔ Fisher's z, batch mode + Hedges' g correction.

---

## [1.6.0] — 2026-07-25

### Added / 新增
- Bayesian NMA: `multinma` (Stan) + `gemtc` (JAGS) full workflows.
- TSA: self-implemented `run_tsa()` with O'Brien-Fleming boundaries.
- Survival meta: `survmeta` wrapper + KM pseudo-IPD reconstruction.
- Dose-response: `dosresmeta` wrapper.

---

## [1.5.0] — 2026-07-15

### Added / 新增
- Initial public release on GitHub / ClawHub / SkillHub.
- Full RevMan 5.x 1:1 code mapping.
- Stata `metareg` / `mvmeta` equivalents.
- Network meta: `netmeta` + `gemtc` + `multinma`.
- Single-group meta: `metaprop` / `metamean` / `metainc` / `metacor`.
- Diagnostic meta: `mada::reitsma` bivariate + SROC.

---

## [1.0.0] — 2026-06-01

### Added / 新增
- Initial version. Core pairwise meta-analysis with `metafor` / `meta`.
