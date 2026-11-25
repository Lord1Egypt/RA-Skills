# 目录结构（本仓库特例）

> 组织标准（目录）：`~/.user-agents/standards/hekouwang-skill-structure.md`  
> 付费化口径：`~/.user-agents/standards/hekouwang-skill-monetize.md`  
> 迁移执行手册：`~/.user-agents/standards/hekouwang-skill-monetize-playbook.md`  
> 本文件只写本仓特例与成熟度档位。渠道 × 版本见 [`RELEASE.md`](RELEASE.md)。  
> 公开面策略：**A. Lite 引流**。版本同号：根 `VERSION` ↔ `edition/VERSION` ↔ `SKILL.md` / `_meta.json` / `edition/meta.paid.json`（`bump_version.py --check`）。  
> 更新：2026-11-20（对齐 terminal/writer；废止 `plans/`；链接真源 = lite）

---

## 成熟度

| 档 | 本仓状态 |
|---|---|
| **现况** | **L3** + 付费化：**SkillPay 商品已过审上架**；主仓 = Lite；Pro ∈ `edition/`；白名单 Pro 包；Lite ClawHub/SkillHub；bump；`dist/<version>/`；日常 `git push origin`；Pages = `docs/` |
| **商品深链** | `scripts/links.sh` → `HKW_URL_SKILLPAY`（P0806000213890180） |
| **E1 留证** | 商品门已过；订单/安装留证可按需补 `roadmap/evidence/e1-order-*.md`（playbook 实单模板） |

---

## 命名

| 版本 | 命名 | 交付 |
|---|---|---|
| 专业版 | `hekouwang-typora-theme-skill` | `dist/<version>/…-paid.zip` / SkillPay |
| 免费版 | `hekouwang-typora-theme-lite-skill` | GitHub + Pages + ClawHub + SkillHub 社区 |

根 `SKILL.md` = Lite（MIT）；`edition/SKILL.paid-section.md` = Pro 增补（`pack.sh` 拼接）。

---

## 目录树

```text
hekouwang-typora-theme-skill/   # 本机开发家；origin = 公开 Lite
├── SKILL.md · _meta.json       Lite（name: *-lite-skill）
├── scripts/ · references/ · theme/ · demo/
├── docs/                       GitHub Pages（含付费档预览图，引流用，非 Pro 源码）
├── listing-skillpay.md         货架文案（入库）
├── materials/                  本地运营物料（不入库，见 .gitignore）
├── RELEASE.md · STRUCTURE.md · .clawhubignore
├── VERSION                     = edition/VERSION
├── edition/                    本地仓：Pro 增量（无公开远程）
├── roadmap/                    本地仓：升级与作战地图（含 evidence/ 发版回执）
├── services/README.md          本期无按次服务（C1）
└── dist/<version>/             不版控；仅 zip（Lite + Pro）
```

```text
专业版 zip  =  主仓（Lite）  ∪  edition/
免费版/公开 =  主仓本身（git push origin → *-lite-skill；Pages = docs/）
```

**不再使用 `public/` worktree。**  
**不另开本机旁路目录 `hekouwang-typora-theme-lite-skill/`。**  
**禁止再建 `plans/`（已更名为 `roadmap/`）。**

---

## 推送

| Remote | 用途 |
|---|---|
| `origin` | 公开 Lite：`hekouwang-typora-theme-lite-skill`；**日常 `git push origin`** |
| `paid` | 可选；专业版仓 `hekouwang-typora-theme-skill`（private / 备份），**不要**把 Pro 源推进 `origin` |

禁止给 `edition/`、`roadmap/` 加公开远程。

---

## 导出与打包

| 命令 | 作用 |
|---|---|
| `python3 scripts/bump_version.py --check` | 双产物同号门 |
| `python3 scripts/build.py --tier free\|paid` | 构建 CSS |
| `./scripts/pack.sh` | Pro → `dist/<version>/…-skill-…-paid.zip` |
| `./scripts/pack-skill-zip.sh` | Lite → `dist/<version>/…-lite-skill-….zip`（含免费 V2 CSS；剔 SkillHub 拒收项） |
| `./scripts/unlock.sh <zip>` | 装付费包；开发树可同步回 `edition/` |

对外 URL 真源：`scripts/links.sh`（必须指向 `*-lite-skill` Pages）。

---

## 禁止

- 免费版与专业版同名  
- 给 `edition/`、`roadmap/` 加公开远程  
- 把「必选 `public/`」或「旁路 lite 工作树」或根目录 `plans/` 写回本仓流程  
- `materials/` / listing 进 Skill/ClawHub 包  
- `materials/` 提交进主仓 git（本机挂载，见 `.gitignore`）  
- 把 Pro 源 / 付费 CSS 提交进 `origin`（公开 Lite）  
- Lite 包内出现无扩展名 `LICENSE`/`VERSION`、`docs/fonts/` 字体二进制（SkillHub 400）  
