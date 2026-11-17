# PRD 原型与需求说明 / PRD + Interactive Prototype

> Turn a one-line idea into a clickable, demo-ready **PRD** (text + single-file HTML). Clear interactions anyone gets; preview locally or publish to share online.
> 把一句话需求变成「能点、能演示」的 PRD 原型。交互清晰、业务一看就懂；本地预览或一键发布分享给同事在线看。

- **Version 版本:** 1.4.0
- **Author 作者:** QQ 965621229（反馈 / 合作请加 QQ）
- **License 许可:** MIT
- **Tags 标签:** prd, prototype, product-management, html, interactive, documentation
- **Language 语言:** 中英双语 / bilingual（不限制语言，可按你的语言回复）

---

## 它是什么 / What it does（一句话概览）

你只要给一个**模糊想法或一句话需求**，它就能用标准产品方法论（用户故事地图 / JTBD / 用户旅程 / KANO / 状态机）帮你补全成一份完整的 PRD，并顺手生成**可点击演示的单文件 HTML 原型**。

- **低门槛默认本地预览**：生成 HTML 后用 `present_files` 直接打开，能点能演示，不需要任何部署。
- **有方法**：缺口自动用产品方法论补全，不必等"信息齐全"才开工。
- **带"交互说明"**：给元素加 `data-ix`，右下角"交互"面板自动汇总；PRD 内也有独立"交互说明"章节，评审方一眼看懂"怎么动"。
- **发布可选**：只有你要对外分享链接时才发布，默认推荐静态托管，并给国内替代；覆盖远端前会先确认。
- **数据联动自洽**：前序页选择驱动后序页（如选商品 → 金额/优惠实时算）。

### 适合谁 / Who it's for
- **产品经理**：日常写 PRD、做方案评审、对齐研发与设计。
- **创业者 / 业务方**：只有一个想法，需要快速成型。
- **任何需要"把方案讲清楚、演出来"的人**：汇报、拉齐、售前都适用。

---

## 能力对照 / Capability coverage（评测维度覆盖）

| 维度 | 覆盖方式 |
|---|---|
| 安全合规 | 单文件自包含、无可执行脚本，可过安全扫描；发布前强制确认；描述中英双语。 |
| 可靠性 | 先采集再补全，缺口用方法论兜底，不卡流程。 |
| 信任度 | 本地预览零门槛；发布提供国内静态托管替代，不绑单一平台。 |
| 适用性 | 附完整可运行示例 `references/example-full.html` + 最小章节示例。 |
| 规范性 | 集中 FAQ + 标准 12 章结构 + 交互说明规范。 |
| 有效性 | 状态对象 + `render()` 数据联动；自定义效果可内联第三方库，仍单文件自包含。 |

---

## 安装 / Install

本技能为标准 Agent Skills 格式（纯提示词 + references + assets，无可执行脚本，可自动通过安全扫描）。将 `prd-html-prototype/` 文件夹复制到对应客户端的 skills 目录即可使用：

- **WorkBuddy**：`cp -r prd-html-prototype ~/.workbuddy/skills/` 后重启会话。
- **其他支持 Agent Skills 的客户端**（如 Claude Code / Cline 等）：导入 `prd-html-prototype/` 文件夹到对应 skills 目录。
- **市场 / 平台**：直接上传本包（zip 或文件夹），平台会自动解析 `SKILL.md` 与 `_meta.json`。

---

## 目录结构 / Structure

```
prd-html-prototype/
├── SKILL.md                      # 主文档（元数据 + 工作流 + FAQ + 能力对照）
├── _meta.json                   # 注册元数据（name/version/author/description/tags）
├── LICENSE.txt                  # MIT（作者：QQ 965621229）
├── references/
│   ├── ONBOARDING.md            # 首次使用环境配置（可选依赖）
│   ├── prd-structure.md         # PRD 12 章结构 + 交互说明 + 诊断
│   ├── product-methodology.md   # 产品方法论速查与映射
│   ├── deploy-github-pages.md   # 发布与缓存失效、国内替代、发布前确认
│   └── example-full.html        # 完整可运行示例（团队订餐拼单）
└── assets/
    └── prd-template.html        # 可运行单文件骨架（含交互说明面板 + 可用 demo）
```

---

## 快速开始 / Quick start

1. 说："帮我写个 PRD：门店要对接万代 CRM 做会员核销。"
2. 技能会用方法论补全缺口，生成本地可点预览。
3. 看右下角"交互"面板，确认关键交互已标注。
4. 要分享时再让它发布（默认静态托管，会先确认）。

---

© 2026 · MIT License · 作者 QQ 965621229
