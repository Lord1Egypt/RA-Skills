# EUDAMED 欧盟医疗器械数据库实务

> 原创整理，依据公开官方法规：Regulation (EU) 2017/745 (MDR)、2017/746 (IVDR)、Regulation (EU) 2024/1860（渐进式上线）、Commission Decision (EU) 2025/2371（OJEU 2025-11-27）。**强制日期与模块状态以欧盟委员会官方当前发布为准。**

## 0. 官方原文直达
- EUDAMED 官方入口（数据库本体）：https://webgate.ec.europa.eu/eudamed
- 欧盟委员会 EUDAMED 专题页（模块状态/强制日期）：https://health.ec.europa.eu/medical-devices-eudamed_en
- MDR 法规原文（Regulation (EU) 2017/745）：https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0745
- IVDR 法规原文（Regulation (EU) 2017/746）：https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0746
- 渐进式上线法规（Regulation (EU) 2024/1860）：https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1860

## 1. 是什么
EUDAMED 是欧盟委员会建立的基于网络的集中式医疗器械数据库，整合多个电子系统，向监管机构、公告机构、经济经营者及（公开部分）公众/医疗专业人员提供器械与主体的结构化信息。目标是提升欧盟市场器械的透明度、可追溯性与监管协同。

## 2. 六个模块（渐进式上线）
1. 参与方注册（Actor registration）
2. UDI / 器械注册（UDI/Device registration）
3. 公告机构与证书（Notified bodies & certificates）
4. 市场监督（Market surveillance）
5. 临床调查与性能研究（CIPS，待实施）
6. 警戒与上市后监督（VGL，待实施）

根据 Reg (EU) 2024/1860，各模块可在"宣布具备功能"时单独强制，无需等全部六个就绪。

## 3. 强制启用时间线
- 委员会决定 (EU) 2025/2371 于 2025-11-26 作出、2025-11-27 刊于 OJEU。
- 依 Reg (EU) 2024/1860 过渡条款，公布触发 6 个月过渡期。
- **自 2026-05-28 起，前 4 个模块（参与方、UDI/器械、公告机构与证书、市场监督）强制使用。**
- 后两个模块（VGL、CIPS）仍在开发，上线时间以委员会官方功能公告为准（业界预期 2027，但须以官方 notice 为准，不臆测）。

## 4. 注册义务与 SRN
- 所有经济主体（分销商除外：制造商、授权代表、进口商、系统/程序包生产者、临床调查申办者）须先完成参与方注册并取得 **SRN（Single Registration Number，单一注册号）**。
- SRN 是后续所有 EUDAMED 操作（器械注册、证书关联等）的前置条件，须出现在符合性声明、CE 申请、现场安全通知等关键文件上。
- 器械注册依赖主体身份：公司须先注册 + 取得 SRN，才能注册产品。UDI/器械模块自 2021-10 起已开放自愿使用。
- 注意：**EUDAMED 注册 ≠ 取得 CE 标志**。CE 通过合格评定授予；EUDAMED 注册是独立合规要求，须在器械欧盟上市前完成。

## 5. 数据提交方式
- 用户界面手动录入
- 门户网站 XML 上传（半自动）
- M2M 机器对机器自动交换
方式选择取决于产品组合规模与 IT 能力。

## 6. 实操检查清单
- [ ] 确认主体角色并完成参与方注册、取得 SRN
- [ ] 梳理在售/拟上市器械清单，按模块要求归集 UDI-DI、基础 UDI-DI、证书关联
- [ ] Legacy 器械（MDD 下证书）也需注册，确认过渡期适用
- [ ] 定制器械、旧器械（MDCG 2021-25 等）有例外，仅在 MIR/FSCA 时提交有限数据集
- [ ] 关注后两模块公告，提前准备警戒/PMS 数据接入

官方入口：health.ec.europa.eu（EUDAMED 概览与 Q&A）
