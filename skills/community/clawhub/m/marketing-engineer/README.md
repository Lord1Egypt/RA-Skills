# Marketing Engineer · 营销工程 Skill

把营销当工程项目做：**知识层 → 业务条线 → 工单管线 → 人工签发 → 数据回流**，再加一层随时可查的**驾驶舱**。
不靠灵感堆内容，靠可复用的结构让每一篇产出都建立在已核实的事实与固定口径之上。

方法论源自 Shann Holmberg（[@shannholmberg](https://x.com/shannholmberg)）的 Marketing Engineer 体系（X 长推文 "this is my AI marketing engine" 与文章 *How to Become a Marketing Engineer* 的四个构建块：Context / Loops / Graphs / Harness）。本项目是在该理论之上的工程实践与产品化。

---

## 它解决什么

AI 已经能写、能设计。真正会翻车的是另外三件事：

| 问题 | 这套东西怎么治 |
|---|---|
| 上下文漂移：今天定的口径，三天后就跑了 | 唯一可引用的 `shared-knowledge/` 五件套 + 「没有来源不许写」的硬规矩 |
| 标准不落盘：每次审稿靠当场想，等于没有标准 | 规程写进文件（术语表、域名口径、发布前自查），机器巡检、人工只判判断力 |
| 状态看不见：几十个文件，不知道哪篇到哪一步 | 单文件驾驶舱：左目录树 / 右文件列表，日期 + 状态 + 可点开看全文 |

## 30 秒上手

装好之后**不用敲命令**，你说话，它跑：

```
「给 XX 产品建一个营销工作区，带上驾驶舱」
「看下整体情况」
「内容更新了，刷新一下驾驶舱」
「这篇发在公众号了，链接是 xxx」
```

Agent 侧收到的动作（正常由它自动执行，命令留给你挂定时任务或排查用）：

| 你的意图 | 它执行的脚本 |
|---|---|
| 建工作区 | `scripts/init_workspace.py <目录> --product "<产品名>" --with-dashboard` |
| 看整体 | `scripts/serve_dashboard.py <工作区> 8799` → <http://127.0.0.1:8799/dashboard.html> |
| 刷新快照 | `scripts/build_dashboard.py <工作区>` |
| 只重扫 | `scripts/scan_workspace.py <工作区>` |

完整用法见 [`references/usage-manual.md`](references/usage-manual.md)（使用手册）。

## 安装

```bash
# 方式一：克隆后放进 skills 目录
git clone https://github.com/iguoguo/marketing-engineer.git
cp -r marketing-engineer ~/.workbuddy/skills/

# 方式二：下 zip（不想碰 git 用这个）
# https://github.com/iguoguo/marketing-engineer/releases/download/v1.1.0/marketing-engineer-skill.zip
```

依赖只有 Python 3（标准库），无第三方包。

## 建完之后的工作区

```
<工作区>/
├── README.md                  # 工作区宪法（八条铁律）
├── shared-knowledge/          # 唯一可引用来源（先填这里）
│   ├── product-and-offer.md   # 产品事实：定位、模块、官方话术、Offer、内部数据
│   ├── positioning.md         # 定位与差异化（含待验证假设）
│   ├── brand-voice.md         # 术语表 / 视觉规范 / 域名口径 / 发布前自查
│   ├── audience.md            # 受众画像
│   └── channels.md            # 渠道清单与分组打法
├── content/ geo-seo/ outbound/ competitor-intel/ launch-campaigns/ raw/
├── scripts/                   # 驾驶舱三件套
├── workspace-folders.json     # 可选：定制目录说明
└── dashboard.html             # 单文件驾驶舱，双击即看
```

## 驾驶舱

- **左目录树 / 右文件列表**：目录说明只在左边出现一次；每个文件都能点开看（Markdown 渲染、表格、代码块一键复制、图片预览）
- **状态不是猜的**：人工注册表 → 发布台账命中 → 文件头 `> 状态：待审核` → 目录规则兜底，四级判定
- **两种更新**：实时（本地服务，每次打开重扫）/ 手动（重建静态快照，断网也能看）
- **明亮 / 暗夜双主题**；任何 `<section id="tab-xxx">` 自动成为一个 Tab

## 文档索引

| 文件 | 内容 |
|---|---|
| [`SKILL.md`](SKILL.md) | Skill 主入口：交互原则、快速开始、工作流、八条铁律、工具箱 |
| [`references/usage-manual.md`](references/usage-manual.md) | 使用手册：三种入口、五步启动法、日常指令卡、驾驶舱用法、排错表 |
| [`references/workspace-structure.md`](references/workspace-structure.md) | 目录模板、文件骨架、目录语义册、状态口径、渠道矩阵 |
| [`references/workflow-content-production.md`](references/workflow-content-production.md) | 工单制内容生产管线 |
| [`references/geo-playbook.md`](references/geo-playbook.md) | GEO / SEO：关键词调研、AI 引擎诊断、探针、KPI |
| [`references/dashboard-playbook.md`](references/dashboard-playbook.md) | 驾驶舱设计 + 驾驶舱引擎（脚本 / 状态 / 主题 / 踩坑） |
| [`references/brand-consistency-audit.md`](references/brand-consistency-audit.md) | 品牌口径巡检六项清单 |

## 八条铁律（任何环节不可违反）

1. **先读后写**：产出前必须查 `shared-knowledge/`，不得虚构渠道、数据、功能
2. **证据留痕**：事实带来源 + 日期；未核实标 `[未验证]`，不流入成品
3. **发布必须人工审批**：台账以线上实际发布版本为准
4. **口径一致性**：术语 / 域名 / 免费表述全渠道唯一，变更必须跑巡检（内部看板也要扫）
5. **密钥只进 `.env`**，不进任何素材或文档
6. **产出归位**：草稿 / 成品 / 台账按目录约定存放
7. **敏感边界**：不点名竞品贬损；定价未定稿不出现具体价格
8. **看板是视图不是源**：从台账 / 工单 / 渠道表派生，不反过来当真相源

## 已知边界

- 只发一篇稿、不打算持续生产的，别装——成本在启动，收益在复利
- 知识层空着，产出立刻退回通用 AI 水平
- 驾驶舱是视图不是源；文件量到几千级需重设快照预算

## English

完整英文版见 [`README_EN.md`](README_EN.md)（用于发布到海外平台）。

## License

MIT © 2026 iguoguo. See [LICENSE](LICENSE).

方法论归属：Shann Holmberg（[@shannholmberg](https://x.com/shannholmberg)）。

由 2Ryun 团队打磨 · 2ryun.wiki
