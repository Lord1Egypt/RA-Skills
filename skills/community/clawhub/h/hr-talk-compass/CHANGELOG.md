# Changelog

## v1.1.0 (2026-07-31)

### 新增
- **`prompts/follow-up.md`**：双周跟进回访 + 风险重评 prompt，补齐"两周跟进是灵魂"的闭环（此前只有约定、没有工具落地）
- **SKILL.md「数据脱敏与升级边界」**：新增一组所有版本必须执行的规则——数据卫生（用代号、不录敏感信息）、场合限制（群聊/共享文档禁传真实员工信息）、升级边界（心理危机→EAP、骚扰/歧视→合规法务、劳动纠纷→法务、超授权承诺→边界话术）
- **review-insights 结构化记录**：单场复盘末尾新增固定 YAML 块（employee_code / trigger_signal / main_issue_tags / 风险等级 / eap_flag / legal_flag / actions…），让季度汇总真正可聚合、可算闭环率
- **`LICENSE`（MIT）** 与 `CHANGELOG.md`

### 修正 / 统一口径
- 仪表盘四维最终定稿为 **健康 / 工作 / 娱乐 / 爱**——忠于卡兹克原文口径（健康含身体/情绪/心理三层，娱乐=纯粹为了快乐而做的事，爱=双向关系）。注：优化过程中曾短暂改为 HR 适配版"健康/工作/生活平衡/关系"，用户拍板改回原文口径
- 新增**方法论来源标注**：SKILL.md / README.md 显式注明方法论源自卡兹克《我把斯坦福最火的一门课，做成了Prompt来帮我设计人生》一文公开的「人生设计师」Prompt（附原文链接），并说明本 skill 的场景化改造范围
- quick-brief = **4-6 核心问题**、deep-dialogue = **6-9 个核心问题**（此前 quick-brief 表格标 6-9，正文写 4-6，前后矛盾）
- `SKILL.md` / `README.md` 场景选择表新增 follow-up 行，目录结构同步

### 工程化
- `exports/` 补齐为 5 个纯 prompt（原只有 quick/deep 两个），README 内附一键重新生成脚本，避免 prompts 与 exports 漂移
- 全部 prompt 增加数据卫生与升级红线引用

### 未做（待你确认）
- 未 push 到 GitHub —— 本地已改好，需你确认 diff 后再决定是否推送
