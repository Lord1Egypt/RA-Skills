<!-- © 2026 MoldYang（老杨）保留所有权利。本作品采用 CC BY-NC-SA 4.0 许可：禁止商业使用，转载/改编须署名并依相同协议发布。联系方式：502898119@qq.com -->
# CHANGELOG
## [v1.1.13] - 2026-07-15
- fix(具名策略更新): 据用户最新口径，具名保留名单收紧为 **Perlos / Nokia / NST** 三者；其余企业名（Philips、精英制模/Ace Mold、LiteOn 等）一律去除。
  - 恢复 NST 具名：mold-design-standards.md 第一组重命名回「NST 模具设计指南（NOKIA/NRT）」、来源标注 NST Confidential、钢种体系改回 NST；SKILL.md 触发词与目录表补回 NST；GAPS 状态表；对外 guide-05/index 文首横幅、十三章标题与小节、免责声明；guide-05 版本号对齐 v1.1.13。
  - 去除 LiteOn：advanced-processes.md 首段、CHANGELOG 历史条目。
  - Perlos / Nokia 维持原技术来源署名不变。

## [v1.1.12] - 2026-07-15
- fix(去具名合规): 技能库全文件去除具体客户/企业具名，统一改为「企业通用设计规范（第一/二/三组）」「企业专有标准（多套企业标准）」等中性表述；mold-design-standards.md 三个企业命名小节重命名、来源标注中性化，SKILL.md 触发词与目录表去具名，CHANGELOG/GAPS 同步；对外发布件 guide-05/index 已先于本轮完成相同去具名。

## [v1.1.11] - 2026-07-15
- feat(输出规范): 文首出处声明补充联系方式 QQ 502898119 / Email 502898119@qq.com（SKILL.md「输出规范」模板第6条 + 样板横幅）；刷新 outputs/output-style-sample.html。

## [v1.1.10] - 2026-07-15
- fix(P1 实际漏落节补齐): v1.1.9 仅材料三节进库，本轮补齐 advanced-processes §15 气辅 GAIM 正文（四阶段原理/气道设计/GAIM vs WIT 对比，含 TOC 第15条）与 缺陷库 §28 MuCell 微发泡专项缺陷、§29 LSR 液态硅胶专项缺陷（总计 29 条）——与 CHANGELOG/GAPS 文案对齐，P1 五项物理落库完成。
- feat(输出规范): SKILL.md 新增「输出规范（出处声明）」——所有对外文件（HTML/MD/PDF/图片/知识库·IMA 发布件）文首强制注明知识来源：MoldYang（老杨）注塑专业知识库；含 5 条规则。新增 outputs/output-style-sample.html 文首出处声明样板。

## [v1.1.9] - 2026-07-15
- feat(P1 业务延展补库): 材料库新增 §30 高温尼龙家族(PA46 Stanyl/PA6T/PA9T Genestar/PA10T，四主力对比表+干燥/嵌件预热/SMT/选型)、§31 TPE 家族(TPE-S/TPV Santoprene/TPEE Hytrel，加工窗口+硬软包覆配对)、§32 碳纤维增强(CF/PA·PPS·PEEK，各向异性/翘曲/导电/模钢H13/浇口防断纤/干燥料温表)；advanced-processes 新增 §15 气辅成型 GAIM(四阶段原理/三方式/气道设计/参数/GAIM vs WIT 对比，补审计所指"仅顺带提及"缺口)；缺陷库新增 §28 MuCell 微发泡缺陷、§29 LSR 液态硅胶缺陷(总计29条)+快速排查表4行。来源：多源权威(Envalior/Kuraray/杜邦/索尔维/Celanese TDS、Fictiv/zetarmold/rapid-protos、cpcic/carbonele、cadit Moldflow)交叉，硬值均标注以供应商 TDS/试模为准。审计 P1 五项(高温尼龙/弹性体/气辅GAIM/碳纤维/微发泡·LSR专项缺陷)清零。

## [v1.1.8] - 2026-07-15
- feat(P0 前沿补库): 材料库新增 §28 LCP 液晶聚合物、§29 功能塑料(导电/导热/EMI屏蔽)；advanced-processes 新增 §12 MuCell 微发泡、§13 随形冷却(3D打印异形水路)、§14 LSR 液态硅胶；mold-structure §2 加随形冷却 cross-ref。来源：多源权威资料(Trexel/PTonline/SMARTMolding、DMLS案例tstar/SSPrecision/ChanHonTech、TE/CoolPoly/Ziitek、cncprotolabs/jzsilicone、Celanese/Polyplastics/Toray/Solvay LCP TDS) + 通用工程原则。知识库无 LCP/MuCell/LSR 独立专文，已标注以供应商 TDS 为准。

## [v1.1.7] - 2026-07-15
- feat(advanced-processes): 新增 §11 2K-MID 双射三维电路（双射+电镀）。来源：知识库 Perlos《2K-MID Antenna Design Guideline V02》(2010) 全文 7 条设计准则 + TE Connectivity/Hahn-Schickard/NISSHA/Cicor 多源验证。含工艺链、Perlos 实测材料配对(PC+ABS/Pd-ABS)、结合/收缩准则、镍禁令、与 LDS/IME 选型矩阵；新增 outputs/2k-mid-detailed-guide.html。MID 三大路线(LDS/2K-MID/IME) 现已在库内完整闭环。

## [v1.1.6] - 2026-07-15
- feat(advanced-processes): §2 Overmolding 补齐「典型失效速查表」+「风险提示」（对齐早期 outputs/overmolding-design-guidelines.md 草稿 §五/§六）。全 6 主题(Overmolding/ICM/IMD家族含IME/LDS/Babyplast)均已入库，本轮为收尾对齐。

## [v1.1.5] - 2026-07-15
- feat(advanced-processes): 6 LDS 扩为完整详细节（四步工艺链/材料体系/DFM/失效模式/与IME·2K-MID选型），新增 outputs/lds-detailed-guide.html。来源：知识库 LDS 专文(DSM/MEP)+ LPKF/KYOCERA AVX/金发/日写NISSHA/IDTechEx 多源验证。


## [v1.1.4] - 2026-07-15
### 微型注塑与 Babyplast 设备要点：新增 §10
- **新增节** `advanced-processes.md` §10 微型注塑与 Babyplast：定义与难点、Babyplast（西班牙 Cronoplast，模块化三形态）、核心设备特征（柱塞式注射+预塑化 / 机模板即模架 / 立式专长嵌件 / UAI 嫁接变 2K / LSR·洁净室版）、两主力系列参数表（6/10P 锁模 62.5kN·注射压力 815–2650bar；10/12 锁模 10t·注射量 4.7–36cm³·占地<0.6m²·能耗 0.2kWh/kg）、微型件 DFM 注意（微浇口高剪切·模温±1°C·真空排气·计量重复性·嵌件准则衔接）、适用场景
- **TOC** 加第 10 项
- **路由升级** `SKILL.md`：`read_when` 补触发词 微型注塑 / micro-molding / micro injection / Babyplast / 柱塞式注射 / 微量注塑
- **来源**：官网 babyplast.com / babyplast.co.uk + 610P 经销商技术页（参数已交叉核对）
- **主交付物**：`outputs/babyplast-intro.html`（完整版，含参数表/技术原理/微型件 DFM/与 IME·嵌件·2K 衔接/试制建议）

## [v1.1.3] - 2026-07-13
### IME 模内电子详细指南：§8.4 从一句话扩为完整节
- **内容扩充** `advanced-processes.md` §8.4 IME：由原单句扩为完整指南——定义与定位、四步工艺链（Print→Thermoform→Assemble→Inject，附 IME 与 IML 的本质分水岭=热成型导电油墨抗拉伸）、材料体系（PC 基膜 / 银浆·碳浆·铜浆·可拉伸银浆 / 介电层 / 导电胶，附 NAMICS·Dycotec 牌号）、设计准则（拉伸率≤10–15% / 线宽间距≥150µm / 器件避浇口 / 热成型窗口）、失效模式表（断线·银迁移·剥离·器件损·触控失灵）、可靠性标准（TCT -40/+85°C Grade3 / HTOL / Damp-Heat / 百格5B / GMW16717 / QUV1500h）、应用与趋势（汽车智能表面 + IDTechEx 2033 ~$2B 口径更新）、并标注与 LDS 激光直接成型的对标选型
- **来源**：企业知识库（Perlos IMD Design Guidelines / Nokia IML）+ 多源权威公开（IDTechEx / NAMICS / Dycotec / CIDETEC / ASME InterPACK 2025 / NextFlex-DTIC / cncprotolabs / hal.science）
- **主交付物**：`outputs/ime-detailed-guide.html`（完整版，含工艺链图示、油墨参数表、可靠性验证清单、IME vs LDS 选型矩阵）

## [v1.1.2] - 2026-07-13
### 实战澄清 + 权威补强：IML/IMD/ICM 关联性
- **概念修正** `advanced-processes.md` §3 ICM：删去"型腔开 0.1–0.2mm"通用定值，改为"初始间隙按制件设定（sub-mm 至数 mm）"；补 Moldex3D 应力 48→12 MPa 定量佐证、ICM 4 种变体（全压缩/局部/Coining/微压缩）、8 项核心收益与应用边界
- **结构重构** `advanced-processes.md` §8：由"IML 模内贴标"重构为「IMD 家族总览」，明确 IMD=模内装饰总称(umbrella)、下辖 IML/IMR/INS/IME，判别主轴=膜片留否件上；补 IMR/INS·IMF/IME 三支定义、IML 留膜三层结构、膜功能分层（"五层"降级为泛指，以供应商 TDS 为准）、IMD vs IML 选型判据（拉伸深度/分型线可达性）、装饰×成型组合矩阵
- **TOC / 选型速查**：第8节更名、ICM 行与 IML 行同步更新
- **路由升级** `SKILL.md`：`read_when` 补触发词 IMR / INS / IMF / IME / 模内电子 / 智能表面
- **来源**：网络权威多源交叉验证（学术期刊、行业技术站、Plastics Decorating、Moldex3D、IDTechEx、OE Journal、IEEE）

## [v1.1.1] - 2026-07-13
### 实战澄清：Overmolding 定义与 Insert Moulding 区分
- **深化** `advanced-processes.md` 第2节 Overmolding：新增「料带连续进给补充要点(reel-to-reel/卷对卷)」+「与 Insert Moulding(intermod) 区别对比表」（8 维度），明确 Perlos 定义 overmolding = 金属料带连续包覆、与离散嵌件的核心分界=连续料带进给 vs 单件放入
- **路由升级** `SKILL.md`：`read_when` 补触发词 intermod / overmolding / 料带连续 / 卷对卷 / reel-to-reel / 端子连续包塑 / 金属带包覆
- **来源**：IMA 知识库 Perlos《Overmolding_instruction.ppt》《2K tooling guideline》原文核实

## [v1.1.0] - 2026-07-10
### 知识库扩充（4 项提案：来源 IMA「注塑模具技术资料库」通用原则）
- **新增** `advanced-processes.md`：特殊成型工艺 9 项（水辅 WIT / 包覆 Overmolding / ICM 注塑压缩 / E-Mold 电加热 / RHCM 急冷急热 / LDS 激光直接成型 / 嵌件 Insert / IML 模内贴标 / 双色 2K），含选型速查表
- **新增** `mold-design-standards.md`：企业设计规范通用原则（多套企业标准）+ 设计评审检查表（跨标准对照）
- **深化** `simulation-guide.md`：新增第九 / 十 / 十一章（Moldflow 结果解读要点 / 翘曲专项与对策 / 网格质量与 CAD Doctor）
- **补充** `materials-database.md`：新增 §27 商业牌号工艺窗口（Perlos 常用料，覆盖 ABS / PC-ABS / PC / PMMA / PA12 / POM / PA 增强 / PPS / TPE 全族）
- **路由升级** `SKILL.md`：模块数 8 → 10，新增「特殊成型工艺」「模具设计规范」路由与 `read_when` 触发词
- **版权合规**：企业专有标准（含多套企业标准）仅提炼通用工程原则并注明来源，不复制完整专有文本

## [v1.0.0] - 2026-07-05
### 初始发布
- 材料数据库：26种工程塑料
- 缺陷诊断库：27条缺陷（13核心 + 14扩展）
- DFM设计规则：8大类通用规则
- 模具结构设计：浇注、冷却、顶出、排气、热流道
- 工艺参数优化：温度、压力、速度、保压、背压
- 模流仿真规范：8章完整指南
- 成本估算：模具报价 + 单件成本
- 许可证：CC BY-NC-SA 4.0
- 作者：MoldYang（东莞）
