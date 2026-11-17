# GitHub 美学前端仓库 · 外部基准库（包内内联版）

> **用途**：作为 nexl-builder 案例召回（Case Recall）的**外部美学对标源**。当包内模板库不足以覆盖某行业/风格时，引导用户到此库取灵感。
> **性质**：本库**不直接进** `templates/catalog`（不符合 nexl 暗黑极简 + 单文件零依赖工艺）。若采用某仓库风格，须由 nexl 按 aurora 工艺重写进 catalog 后才进橱窗。
> **收录铁律**：仅收许可证经核实为 MIT / Apache-2.0 / CC0 / Unlicense 的仓库。

---

## 商用许可证红绿灯

| 许可证 | 商用克隆 | 注意 |
|---|---|---|
| 🟢 MIT | OK | 保留 `LICENSE` 与原版权声明即可 |
| 🟢 CC0-1.0 | OK（最自由） | 作者完全放弃权利，无需署名 |
| 🟢 Apache-2.0 | OK（更稳） | 改了需声明；自带专利授权 |
| 🟢 Unlicense | OK | 等价公有领域 |
| 🔴 无 license | **禁止** | 默认 All rights reserved，再美也不能 clone 商用 |

---

## 精选清单（按 nexl 5 类目对齐）

### 作品集 / 个人 IP
| 仓库 | ⭐ | 许可证 | 美学特点 | 适配 |
|---|---|---|---|---|
| `codewithsadee/vcard-personal-portfolio` | 7.9k | MIT | 经典响应式个人作品集，结构干净 | 作品集 |
| `Renovamen/playground-macos` | 3.5k | MIT | 拟物 macOS GUI 作品集，记忆点极强 | 个人 IP |
| `CommunityPro/portfolio-html` | 671 | MIT | 纯 HTML/CSS/JS 零依赖（最贴 nexl 单文件哲学）| 作品集 |
| `manuelernestog/astrofy` | 1.4k | MIT | Astro+Tailwind 全能站（博客/CV/商店）| 个人 IP |

### 产品 / SaaS 落地页
| 仓库 | ⭐ | 许可证 | 美学特点 | 适配 |
|---|---|---|---|---|
| `karthikmudunuri/saas-landing-page-template` | 255 | MIT | Next+Tailwind+Framer 暗黑 SaaS | 产品落地页 |
| `AayushBharti/ai-saas-landing-starter` | 127 | MIT | AI SaaS 视差 + bento 布局，现代感强 | 产品落地页 |

### 品牌官网 / 活动（MIT 缺口区）
| 仓库 | ⭐ | 许可证 | 美学特点 | 适配 |
|---|---|---|---|---|
| `michelegera/tailwindcss-open-template` | 152 | MIT | "Open" 经典落地页（Tailwind）| 品牌官网 |
| `adrienjoly/landing-page-boilerplate` | 154 | MIT | 可 fork 的纯客户端落地页 | 活动 |

### 导航 / 灵感清单（本身自由用）
| 仓库 | ⭐ | 许可证 | 用途 |
|---|---|---|---|
| `Evavic44/portfolio-ideas` | 6.2k | MIT | 作品集灵感库 |
| `mratanusarkar/awesome-web-designs` | 1 | CC0-1.0 | 精美 UI/UX 网站集合（最自由）|
| `nicolesaidy/awesome-web-design` | 2.7k | 无（清单）| 设计师资源导航，条目需逐条核实 |

---

## 与 nexl 的衔接规则（agent 必须遵守）
1. **外部库 ≠ 种子**：清单内仓库不可直接写进 `templates/catalog`。
2. **对标流程**：用户要某类目美学参考 → 引导查看本库 → 若采用某仓库风格，由 nexl 按 `aurora-minimal` 工艺（暗黑极简 + 字符级 stagger + 磁吸光标 + 滚动揭示 + 单文件零依赖）**重写进 catalog** 后才进橱窗。
3. **案例召回触发**：当包内模板库（见 `references/template-catalog.md`）内部模板不足以覆盖用户行业/风格时，在 Case Recall 步补充：「外部美学基准见 `references/aesthetic-repos.md`」。

_收录日期：2026-07-21 · 维护者：nexl_
