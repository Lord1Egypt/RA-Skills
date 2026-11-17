# 注塑模具专业助手 (injection-molding-pro) · 发布包

> **版本**：v1.1.13 ｜ **作者**：MoldYang（老杨） ｜ **许可**：CC BY-NC-SA 4.0
> **发布日期**：2026-07-23 ｜ **联系方式**：502898119@qq.com ｜ 微信：502898119

---

## 一、知识产权与授权声明（请先读）

本作品（"注塑模具专业助手"技能）由 **MoldYang（老杨）** 独立编写，保留所有权利。

- **许可协议**：[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](./LICENSE)
- **你可以**：免费下载、使用、学习、基于本技能二次创作（**仅限非商业用途**）。
- **你必须**：使用时**署名 MoldYang**；若转载或发布修改版，**须沿 CC BY-NC-SA 4.0 相同协议发布**并保留本声明。
- **你不可以**：将本技能用于**任何商业目的**（含收费咨询、培训、集成进商业产品/服务）；不得擅自去除、篡改作者署名与版权标识；不得以"去署名"方式再分发。
- **商标与来源**：本技能引用的 Perlos / Nokia / NST 等企业技术规范为其各自权利人的资产，本技能仅作技术要点归纳，相关权利归原权利人所有。
- **免责**：材料物性取公开文献典型值，工艺参数基于通用经验，成本估算为参考性质。使用者须自行验证并承担一切风险。

本发布包内**每一份文件头部均嵌入 © 版权水印**，复制传播时一并保留。

## 二、文件清单

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能入口与触发词、10 大功能模块、对外输出出处声明规范 |
| `README.md` | 功能介绍、安装方法、许可说明 |
| `NOTICE.md` | 作者与原创性声明、免责 |
| `LICENSE` | CC BY-NC-SA 4.0 完整文本 |
| `CHANGELOG.md` | 版本演进记录（v1.1.13） |
| `references/materials-database.md` | 26+ 种注塑材料物性（含 Cross-WLF + Tait PVT） |
| `references/process-optimization.md` | 工艺参数推荐与调机指南 |
| `references/defect-diagnostics.md` | 29 种缺陷诊断与对策 |
| `references/dfm-design-rules.md` | 可制造性设计规则清单 |
| `references/mold-structure-design.md` | 浇口/流道/冷却/顶出设计 |
| `references/simulation-guide.md` | Moldflow / Moldex3D 仿真规范 |
| `references/mold-design-standards.md` | 企业设计规范（NST 等）与 SPI 等级 |
| `references/advanced-processes.md` | 特殊成型工艺（ICM/E-Mold/RHCM/LDS/IML-IMD/2K/包覆/水辅/气辅/MuCell/LSR 等） |
| `references/cost-estimation.md` | 模具与单件成本估算 |

> 注：内部开发文档（EVOLUTION.md / GAPS.md）及 `.git` 版本库不在发布包内。

## 三、安装方法（WorkBuddy）

1. 解压本包，得到 `injection-molding-pro/` 文件夹。
2. 整体复制到 WorkBuddy 技能目录：
   - 用户级：`~/.workbuddy/skills/injection-molding-pro/`
   - 或项目级：`<工作区>/.workbuddy/skills/injection-molding-pro/`
3. 在对话中通过 `@skill:injection-molding-pro` 调用。
4. 本技能产生的任何对外文件（HTML/MD/PDF/图片）将自动在文首标注来源：MoldYang（老杨）注塑专业知识库。

## 四、上传到 IMA 知识库（供他人下载）

- IMA 知识库接受 `.zip`（归入 media_type=14 Xmind 类型，接口明确支持 `application/zip`），单文件上限 10MB，本包约 300KB 远低于限制。
- 在 IMA 网页端或**桌面端**上传本 zip 后，将以文件形式存在于知识库，关注你"知识号"的人可通过下载按钮获取。
- 若网页端对 zip 有限制，请用 **IMA 桌面端**上传（桌面端支持更多文件类型）。
- 下载链接获取：通过 `get_media_info` 返回的 URL 追加 `response-content-type=application/octet-stream&response-content-disposition=attachment` 即以原文件名下载。

---
*技术咨询、企业培训、工艺诊断：502898119@qq.com ｜ 微信 502898119*
