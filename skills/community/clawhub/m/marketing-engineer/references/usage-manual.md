# 使用手册 · Marketing Engineer Skill

> 目标：**一句话启动一个完整的营销工作区**——目录、口径、管线、驾驶舱一次到位，之后你只需要说「今天写什么 / 发什么 / 调研谁」，剩下的按本 skill 的规矩跑。

---

## 一、它是什么 / 什么时候用

把营销当工程项目做：**知识层 → 垂直域 → 工单管线 → 人审闭环 → 数据回流**，外加一个随时可查的**驾驶舱**。

出现下列任一诉求时用它：

- 「搭个营销工作区 / 参考某某方法论做营销体系」
- 「我要随时看到整体情况、排期、任务、文件状态」
- 写内容（公众号 / 知乎 / X / Medium / 小红书…）、做上线推广 campaign
- SEO / GEO（生成式引擎优化）、AI 引擎可见度诊断、关键词调研
- 竞品情报、渠道矩阵、多平台分发

---

## 二、三种入口（你说一句话就行）

**脚本由 agent 在背后执行，不需要用户敲命令。** 左列是你说的话，右列是 agent 会做的事（只有排查问题、挂定时任务、在没有 agent 的环境里，才需要自己跑命令，见第七节 recipes）。

| 你的情况 | 你说什么 | agent 做什么 |
|---|---|---|
| **全新项目** | 「给 <产品名> 建个营销工作区，带驾驶舱」 | 跑 `init_workspace.py … --with-dashboard`：建目录 + 口径骨架 + dashboard.html |
| **已有目录，想接上体系** | 「这个目录接上营销体系，再给我一个驾驶舱」 | 按 `workspace-structure.md` 补齐目录与 shared-knowledge 五件套，再跑 `build_dashboard.py` |
| **只要一个全景看板** | 「给我一个工作区全景看板」 | 复制三件套到 `scripts/`，跑 `build_dashboard.py`（不需要先有内容） |

skill 路径通常是 `~/.workbuddy/skills/marketing-engineer/`。

**生成后你会得到：**

```
<工作区>/
├── README.md                  # 工作区宪法（铁律清单）
├── shared-knowledge/          # 唯一可引用来源（先填这里）
├── content/ geo-seo/ outbound/ competitor-intel/ launch-campaigns/ raw/
├── scripts/                   # scan_workspace.py / build_dashboard.py / serve_dashboard.py
├── workspace-folders.json     # 可选：定制目录说明
└── dashboard.html             # 单文件驾驶舱（双击即看）
```

---

## 三、五步启动法（第一次用必做）

**Step 0 · 建骨架**：跟 agent 说「建个工作区，带驾驶舱」，它会跑 `init_workspace.py --with-dashboard`，把驾驶舱三件套一起装好并生成 `dashboard.html`。

**Step 1 · 填 shared-knowledge 五件套**（最重要，别跳过）

| 文件 | 填什么 |
|---|---|
| `product-and-offer.md` | 一句话定位、价值要素、模块表、官方原话术、Offer、内部数据（标检索日期） |
| `positioning.md` | 定位与差异化，含「待验证假设 `[未验证]`」区 |
| `brand-voice.md` | 术语表（统一说法 vs 禁用说法）、视觉规范、域名口径、发布前自查清单 |
| `audience.md` | 受众画像 |
| `channels.md` | 渠道清单 + 分组打法 |

> 规则：这里之外的事实不得直接对外引用；新事实必须带**来源 + 日期**。

**Step 2 · 定渠道与排期**：按 `workspace-structure.md` 的分组原则（按受众分组，不按平台罗列）写 `channels.md`，产出第一版排期。

**Step 3 · 开第一批工单**：`launch-campaigns/<campaign>/tickets/` 一任务一单，走 `workflow-content-production.md`（brief → 草稿 → 人审 → 排版/封面 → 发布 → 台账回填 → 数据回流）。

**Step 4 · 建驾驶舱视图**：默认已有「工作区全景」。需要排期月历 / 倒计时 / 工单看板 / 台账等区块时，按 `dashboard-playbook.md` 加 `<section id="tab-xxx">`——**任何 `tab-` 开头的 section 会自动变成一个 Tab**。

---

## 四、日常怎么用（对话里直接说就行）

| 你想做的事 | 直接说 | agent 会做什么 |
|---|---|---|
| 写内容 | 「按 X 渠道人设写一篇关于…的稿子」 | 先读 shared-knowledge → 出 brief → 工单 → 草稿 → 标「待审核」等你点头 |
| 看整体 | 「看下整体情况」 | 打开驾驶舱（实时模式会先刷新）再汇报 |
| 做调研 | 「调研一下 XX 竞品 / 这个话题最近在讨论什么」 | 一手源取证 → 落 `competitor-intel/research/` 或 `geo-seo/`，带来源+日期 |
| 改口径 | 「以后统一叫…，不要叫…」 | 改 shared-knowledge → **跑品牌口径巡检**（含内部看板）→ 留档 |
| 排期 | 「接下来两周每天发什么」 | 出逐日排期 → 进驾驶舱 → 关键节点可同步系统日历 |
| 发布后 | 「这篇发在 XX 了，链接是…」 | 回填台账 `results/channel-posts.md`（**以线上实际标题为准**）→ 重建驾驶舱 |
| 文件找不着 | 「那个 XX 文件在哪」 | 驾驶舱左栏搜目录、右栏搜文件名 |

---

## 五、驾驶舱怎么用

### 布局语义（记住这一句就够）

> **左边选目录，右边看文件。目录的说明只在左边出现一次，右边不重复。**

- **左栏**：目录树 —— 目录名 + 文件数（含子目录）+ 一句话说明；点箭头展开、点名字切换；顶上有「展开 / 收起 / 搜目录」
- **右栏**：面包屑（点任一段跳回上级）+ 搜索框 + 状态筛选 + 文件表（文件名 / 说明 / 日期 / 状态 / 渠道·发布时间 / **最右侧操作列**）
- **每个文件都能点开看**：Markdown 渲染（标题、表格、代码块带一键复制、元信息卡）、图片直接预览 + 新窗口开原图、二进制文件给路径提示
- **右上角 ☾/☀︎ 按钮**：切换暗夜 / 明亮，选择会被记住

### 状态怎么看

顶部彩色 chip 一点即筛（再点取消）：

| 状态 | 含义 |
|---|---|
| 已发布 | 台账里有 URL 与发布时间 |
| 待审核 | 已成稿，等你人工审核 |
| 全文已备 | 全文写完，排在后续日期 |
| 需出稿 | 排期已定，稿子还没写 |
| 草稿 | 待完善后送审 |
| 定稿口径 / 方案 / 情报 / 源稿 / 内部 | 内部文档（分别对应 shared-knowledge / strategy / competitor-intel / outputs / 过程文档） |
| 构建物 / 素材 / 记忆 | 脚本、图片、AI 记忆 |

**状态不是猜的**，判定优先级：① 人工注册表 `workspace-registry.json` → ② 发布台账命中 → ③ 文件头 `> 状态：xxx` → ④ 目录规则兜底。想在文件头标注，写一行 `> 状态：待审核` 即可被识别。

### 更新机制（两种方式都支持，都由 agent 执行）

1. **实时**（默认）：说「看下整体情况」，agent 起 `serve_dashboard.py <工作区> 8799` → 打开 `http://127.0.0.1:8799/dashboard.html`，**每次打开重新扫描**，页头显示「● 实时扫描」
2. **手动**：说「刷新一下驾驶舱」，agent 跑 `build_dashboard.py <工作区>`（重写 `dashboard.html`，旧的自动备份到 `.cache/`）

新增 / 改名 / 删除文件**不需要登记**，扫描器自动归类。

### 定制

- **目录说明**：改工作区根目录 `workspace-folders.json`（`{"目录路径": ["中文名","角色","一句话说明"]}`），重建即生效
- **状态人工指定**：建 `workspace-registry.json`（`{"文件相对路径": {"status":"待审核","date":"09-22","channels":["公众号"],"url":""}}`），优先级最高
- **加自己的区块**：在 `dashboard.html` 里写
  ```html
  <!-- CUSTOM:START -->
  <section id="tab-kpi"><h2>本月 KPI</h2>…</section>
  <!-- CUSTOM:END -->
  ```
  用 `CUSTOM` 注释包起来，重建时会被自动迁移；`id="tab-…"` 让它自动成为 Tab

---

## 六、铁律速查（任何环节不可违反）

1. **先读后写**：产出前必须查 shared-knowledge；不得虚构渠道、数据、功能
2. **证据留痕**：事实带来源+日期；未核实标 `[未验证]`，不流入成品
3. **发布必须人工审批**：草稿送审，你确认后才排版/发布；台账以**线上实际发布版本**为准
4. **口径一致性**：术语/域名/免费表述全渠道唯一；口径变更必须跑巡检，**内部看板也要扫**
5. **密钥只进 `.env`**，不进任何素材或文档
6. **产出归位**：草稿/成品/台账按目录约定存放
7. **敏感边界**：不点名竞品贬损；定价未定稿不出现具体价格
8. **看板是视图不是源**：源永远是台账 / 工单 / 渠道表 / 周报，看板从它们派生

---

## 七、常见场景 recipes

> 正常情况下这些命令由 agent 自动执行；下面列出是为了手动执行、挂定时任务或排查问题。

```bash
# 1）新项目全套启动
python3 ~/.workbuddy/skills/marketing-engineer/scripts/init_workspace.py ~/my-ws --product "我的产品" --with-dashboard

# 2）内容更新后刷新驾驶舱（静态）
python3 scripts/build_dashboard.py .

# 3）起实时服务（推荐开会/日常看）
python3 scripts/serve_dashboard.py . 8799

# 4）只重新扫描（不重建页面，写 CI/自动化用）
python3 scripts/scan_workspace.py .

# 5）FAQ 定稿 → JSON-LD（同源生成，保证与可见文字一致）
python3 scripts/md-faq-to-schema.py faq.md > faq.jsonld

# 6）把 skill 打成 zip 分发给别人（排除 __pycache__）
cd ~/.workbuddy/skills && zip -rq /path/to/marketing-engineer-skill.zip marketing-engineer -x "*/__pycache__/*" "*.DS_Store"
```

**自动化建议**：让 agent 每次「发布 / 关单 / 新调研 / 口径变更」后自动跑一次 `build_dashboard.py`；也可挂定时任务每天重跑，保证离线快照不过期。

---

## 八、排错与坑

| 现象 | 原因 / 处理 |
|---|---|
| 页头显示「静态快照」 | 没起服务，或用的是 `file://` 打开。起服务走 http 即自动实时 |
| 改了扫描脚本但服务数据没变 | 服务常驻会用旧模块，**必须重启** `serve_dashboard.py` |
| `build_dashboard.py` 提示已存在 | 加 `--force`（会自动备份旧文件到 `.cache/`） |
| 找不到 `dashboard-skeleton.html` | 重跑 `init_workspace.py --with-dashboard`，它会把骨架放进 `.cache/` |
| 暗夜模式下某些行 hover 变白 | 有硬编码的 hover 底色没进变量体系：统一改用 `var(--hover)` |
| 后台服务进程随命令结束消失 | 用后台任务方式启动，不要 `&` 后立刻返回 |
| 台账里明明发了，驾驶舱却不是「已发布」 | 台账 URL 需出现在 **`outputs/` 目录下**的文件里；且台账自身/README 不算 |

---

## 九、文件索引

| 想了解什么 | 看哪个文件 |
|---|---|
| 目录结构、各文件骨架、渠道矩阵 | `references/workspace-structure.md` |
| 内容生产管线（brief→发布→回流） | `references/workflow-content-production.md` |
| GEO / SEO 打法、关键词、探针、KPI | `references/geo-playbook.md` |
| 驾驶舱设计 + 引擎（脚本/状态/更新/主题/踩坑） | `references/dashboard-playbook.md` |
| 品牌口径巡检清单 | `references/brand-consistency-audit.md` |
| 本手册 | `references/usage-manual.md` |
