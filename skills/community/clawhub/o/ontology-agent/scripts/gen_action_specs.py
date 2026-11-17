# -*- coding: utf-8 -*-
"""
gen_action_specs.py — 本体论智能体 · 逻辑层动作加厚生成器
把 department_actions.yaml 的 141 个动作从"一行名"扩成完整 action spec：
  desc / inputs / outputs / preconditions / effects / uses_entities / skill_ref / method
策略：OPB 92 个技能真实方法论描述优先覆盖（模糊匹配），其余 source + 未匹配项用 FALLBACK 兜底字典。
本文件为 references/ 内部构建脚本，生成 references/action_specs.yaml（不随产品交付用户，仅开发期/实例化引用）。
"""
import os, re, glob, yaml, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "references")
SRC = "C:/Users/li_sh/WorkBuddy/2026-08-12-22-13-55/开源参考/B_skills"

# ───────────────────────── 兜底字典（全 141，对照源库方法论要点，中文） ─────────────────────────
# 字段：n=显示名 s=来源 d=描述 i=输入 o=输出 u=引用实体 r=源路径 m=方法论要点
FALLBACK = {
 # 1 负责人/综合决策
 "strategic-startup-mentor":{"n":"创业指导师","s":"OPB","d":"以教练式对话帮助创始人厘清战略、识别盲点、制定阶段性行动。","i":["创业现状","困惑点","资源清单"],"o":["战略建议","行动清单","风险提示"],"u":["Organization","Goal"],"r":"OPB/skills/strategy-startup-mentor","m":"GROW 教练模型：目标-现状-选项-意愿"},
 "strategic-startup-simulator":{"n":"创业模拟器","s":"OPB","d":"用场景推演模拟经营决策结果，预测现金流与风险。","i":["经营假设","市场参数"],"o":["情景推演","敏感性分析"],"u":["Organization","Project"],"r":"OPB/skills/strategy-startup-simulator","m":"蒙特卡洛/情景树推演"},
 "personal-review":{"n":"周期性复盘","s":"OPB","d":"按周/月/季结构化复盘目标达成与偏差。","i":["周期目标","实际结果"],"o":["复盘报告","改进项"],"u":["Goal","Task"],"r":"OPB/skills/personal-review","m":"KPT(Keep-Problem-Try)复盘法"},
 "personal-planning":{"n":"规划助手","s":"OPB","d":"把模糊目标拆成可执行计划与里程碑。","i":["目标描述"],"o":["计划","里程碑"],"u":["Goal","Task"],"r":"OPB/skills/personal-planning","m":"OKR 拆解"},
 "personal-talent-discovery":{"n":"天赋发现顾问","s":"OPB","d":"通过测评与访谈发现个人天赋与适配角色。","i":["兴趣","过往经历"],"o":["天赋画像","角色建议"],"u":["Person"],"r":"OPB/skills/personal-talent-discovery","m":"优势识别(CliftonStrengths 思路)"},
 "personal-goal-manager":{"n":"目标管理","s":"OPB","d":"设定、追踪、对齐个人与组织目标。","i":["目标"],"o":["目标树","进度"],"u":["Goal"],"r":"OPB/skills/personal-goal-manager","m":"SMART+OKR"},
 "personal-habit-builder":{"n":"习惯养成","s":"OPB","d":"设计习惯回路与执行意图。","i":["想养成的习惯"],"o":["习惯方案","提示卡"],"u":["Person"],"r":"OPB/skills/personal-habit-builder","m":"习惯回路(提示-渴求-回应-奖赏)"},
 "personal-career-planner":{"n":"职业规划","s":"OPB","d":"结合市场与个人禀赋做职业路径规划。","i":["当前职业","志向"],"o":["路径图","能力缺口"],"u":["Person","Goal"],"r":"OPB/skills/personal-career-planner","m":"职业锚+能力地图"},
 "personal-time-manager":{"n":"时间管理","s":"OPB","d":"排程、优先级与时间块管理。","i":["任务清单","时间预算"],"o":["日程","优先级"],"u":["Task"],"r":"OPB/skills/personal-time-manager","m":"时间块+ Eisenhower 矩阵"},
 "personal-health-manager":{"n":"健康管理","s":"OPB","d":"结合可穿戴数据给作息与运动建议。","i":["健康数据"],"o":["健康计划"],"u":["Person"],"r":"OPB/skills/personal-health-manager","m":"行为医学基础"},
 "personal-human3":{"n":"HUMAN3.0评估","s":"OPB","d":"评估个人在 AI 时代的人机协作能力层级。","i":["能力自述"],"o":["HUMAN3.0 报告"],"u":["Person"],"r":"OPB/skills/personal-human3-evaluation","m":"HUMAN 3.0 框架"},
 "learning-planner":{"n":"学习规划","s":"OPB","d":"按目标设计学习路径与资源。","i":["学习目标"],"o":["学习路径"],"u":["Goal"],"r":"OPB/skills/learning-planner","m":"微学习路径"},
 "knowledge-manager":{"n":"知识管理","s":"OPB","d":"构建第二大脑、知识分类与检索体系。","i":["资料流"],"o":["知识库结构"],"u":["Document"],"r":"OPB/skills/knowledge-manager","m":"PARA/Zettelkasten"},
 "company-values":{"n":"公司价值观","s":"slav","d":"从创始人信念提炼公司价值观与行为准则。","i":["创始人信念"],"o":["价值观声明"],"u":["Organization"],"r":"slavingia/skills/company-values","m":"价值观工作坊"},
 # 2 行政/运营
 "user-operations":{"n":"用户运营","s":"OPB","d":"用户分层、生命周期运营与活跃提升。","i":["用户数据"],"o":["运营策略","分层"],"u":["Customer"],"r":"OPB/skills/user-operations","m":"AARRR 用户生命周期"},
 "event-planner":{"n":"活动策划","s":"OPB","d":"从目标到落地的活动全流程策划。","i":["活动目标","预算"],"o":["活动方案","执行表"],"u":["Event","Project"],"r":"OPB/skills/event-planner","m":"活动管理五步法"},
 # 3 人力
 "hr-recruiter":{"n":"招聘助手","s":"OPB","d":"JD 撰写、简历筛选与面试评估。","i":["岗位需求"],"o":["JD","候选人评估"],"u":["Person","Department"],"r":"OPB/skills/hr-recruiter","m":"结构化面试"},
 "hr-performance":{"n":"绩效管理","s":"OPB","d":"设计绩效指标与考核周期。","i":["岗位职责"],"o":["绩效方案"],"u":["Department","Person"],"r":"OPB/skills/hr-performance","m":"KPI/KPI+OKR"},
 "hr-compensation":{"n":"薪酬设计","s":"OPB","d":"薪酬结构与激励方案设计。","i":["岗位价值","预算"],"o":["薪酬带宽","激励方案"],"u":["Department"],"r":"OPB/skills/hr-compensation","m":"3P 薪酬模型"},
 # 4 财务
 "finance-planner":{"n":"财务规划","s":"OPB","d":"编制预算、现金流预测、财务指标分析，输出月度/年度财务规划。","i":["历史收支","业务计划","税务状态"],"o":["预算表","现金流预测","财务指标"],"u":["Organization","Account","Task"],"r":"OPB/skills/finance-financial-planner","m":"预算编制流程+现金流模型+分析指标体系"},
 "finance-cost-analyst":{"n":"成本分析","s":"OPB","d":"归集成本、测算单位成本与盈亏平衡点。","i":["成本数据","产量"],"o":["成本结构","盈亏平衡"],"u":["Account","Project"],"r":"OPB/skills/finance-cost-analyst","m":"本量利分析(CVP)"},
 "finance-investment-analyst":{"n":"投资分析","s":"OPB","d":"评估投资项目回报与风险。","i":["投资方案","现金流"],"o":["NPV/IRR","风险评级"],"u":["Project","Account"],"r":"OPB/skills/finance-investment-analyst","m":"DCF+IRR+情景分析"},
 # 5 法务/合规
 "legal-contract-reviewer":{"n":"合同审查","s":"OPB","d":"识别合同条款风险、缺失与不利约定。","i":["合同文本"],"o":["风险清单","修改建议"],"u":["Document","Organization"],"r":"OPB/skills/legal-contract-reviewer","m":"Clause 风险矩阵"},
 "legal-compliance-checker":{"n":"合规检查","s":"OPB","d":"按行业法规做合规体检。","i":["业务描述"],"o":["合规差距","整改清单"],"u":["Organization","Policy"],"r":"OPB/skills/legal-compliance-checker","m":"合规清单法"},
 "legal-ip-manager":{"n":"知识产权管理","s":"OPB","d":"专利/商标/著作权布局与维护。","i":["创新成果"],"o":["IP 布局","申请清单"],"u":["Document","Organization"],"r":"OPB/skills/legal-ip-manager","m":"IP 组合管理"},
 "legal-overview":{"n":"法律总览","s":"Frog","d":"一人公司法律结构与风险总览。","i":["公司形态"],"o":["法律结构图","风险点"],"u":["Organization"],"r":"Frog1205/skills/legal","m":"主体结构梳理"},
 "legal-agreement":{"n":"协议起草","s":"Frog","d":"起草合作/服务/股权等协议。","i":["合作要点"],"o":["协议草案"],"u":["Document","Person"],"r":"Frog1205/skills/legal","m":"协议模板化"},
 "legal-compare":{"n":"条款比对","s":"Frog","d":"对比多版合同差异。","i":["多版合同"],"o":["差异表"],"u":["Document"],"r":"Frog1205/skills/legal","m":"差异高亮"},
 "legal-freelancer":{"n":"自由职业法务","s":"Frog","d":"面向自由职业者的轻量法务支持。","i":["业务场景"],"o":["法务要点"],"u":["Person"],"r":"Frog1205/skills/legal","m":"场景化法务"},
 "legal-missing":{"n":"缺失条款","s":"Frog","d":"检查合同缺失的关键条款。","i":["合同文本"],"o":["缺失清单"],"u":["Document"],"r":"Frog1205/skills/legal","m":"必备条款清单"},
 "legal-nda":{"n":"保密协议","s":"Frog","d":"起草保密/竞业协议。","i":["保密范围"],"o":["NDA 草案"],"u":["Document","Person"],"r":"Frog1205/skills/legal","m":"NDA 模板"},
 "legal-negotiate":{"n":"法务谈判","s":"Frog","d":"谈判策略与条款博弈。","i":["谈判议题"],"o":["谈判脚本"],"u":["Person"],"r":"Frog1205/skills/legal","m":"利益型谈判"},
 "legal-plain":{"n":"白话法律","s":"Frog","d":"把法律语言转成大白话。","i":["法律文本"],"o":["白话解释"],"u":["Document"],"r":"Frog1205/skills/legal","m":"法律翻译"},
 "legal-privacy":{"n":"隐私合规","s":"Frog","d":"个人信息处理合规设计。","i":["数据处理流"],"o":["合规方案"],"u":["Policy","Person"],"r":"Frog1205/skills/legal","m":"GDPR/个保法映射"},
 "legal-report-pdf":{"n":"法律报告","s":"Frog","d":"生成结构化法律报告 PDF。","i":["分析结论"],"o":["PDF 报告"],"u":["Document"],"r":"Frog1205/skills/legal","m":"报告生成"},
 "legal-review":{"n":"法律审查","s":"Frog","d":"综合法律审查与意见。","i":["待审材料"],"o":["法律意见"],"u":["Document","Organization"],"r":"Frog1205/skills/legal","m":"尽调式审查"},
 "legal-risks":{"n":"法律风险","s":"Frog","d":"识别与评级法律风险。","i":["业务模式"],"o":["风险图谱"],"u":["Organization"],"r":"Frog1205/skills/legal","m":"风险评级"},
 "legal-terms":{"n":"条款生成","s":"Frog","d":"按场景生成标准条款。","i":["条款类型"],"o":["条款文本"],"u":["Document"],"r":"Frog1205/skills/legal","m":"条款库"},
 "opc-compliance-diagnosis":{"n":"OPC合规诊断","s":"sober","d":"一对一公司主体选型、新公司法合规、财税规划诊断。","i":["主体信息","业务模式"],"o":["合规诊断报告","整改项"],"u":["Organization","Policy"],"r":"sober568/docs/skill-reference","m":"五阶段-实体期合规落地"},
 # 6 研发/产品/技术/设计/QA/DevOps
 "product-industry-analyst":{"n":"行业分析","s":"OPB","d":"行业规模、格局与趋势分析。","i":["行业"],"o":["行业报告"],"u":["Project"],"r":"OPB/skills/product-industry-analyst","m":"PESTEL+波特五力"},
 "product-researcher":{"n":"产品调研","s":"OPB","d":"用户与需求调研。","i":["调研目标"],"o":["调研报告"],"u":["Customer","Goal"],"r":"OPB/skills/product-researcher","m":"用户访谈+问卷"},
 "product-market-researcher":{"n":"市场调研","s":"OPB","d":"市场规模与竞品调研。","i":["品类"],"o":["市场地图"],"u":["Project"],"r":"OPB/skills/product-market-researcher","m":"TAM/SAM/SOM"},
 "product-ideation-pm":{"n":"产品创意PM","s":"OPB","d":"创意发散与优先级排序。","i":["问题域"],"o":["创意清单","PRD"],"u":["Project"],"r":"OPB/skills/product-ideation-pm","m":"头脑风暴+ RICE"},
 "product-ai-remake":{"n":"AI产品重做","s":"OPB","d":"用 AI 重做/增强现有产品。","i":["现有产品"],"o":["AI 改造方案"],"u":["Project"],"r":"OPB/skills/product-ai-remake","m":"AI 原生重构"},
 "rnd-frontend-review":{"n":"前端审查","s":"OPB","d":"前端代码与体验审查。","i":["代码/页面"],"o":["审查意见"],"u":["Project"],"r":"OPB/skills/rnd-frontend-review","m":"Code Review"},
 "rnd-code-simplify":{"n":"代码简化","s":"OPB","d":"重构与去除复杂度。","i":["代码"],"o":["简化方案"],"u":["Project"],"r":"OPB/skills/rnd-code-simplify","m":"重构七宗罪"},
 "rnd-requirements-writer":{"n":"需求编写","s":"OPB","d":"写可测试的需求文档。","i":["需求要点"],"o":["需求文档"],"u":["Task","Project"],"r":"OPB/skills/rnd-requirements-writer","m":"INVEST"},
 "rnd-fullstack-architect":{"n":"全栈架构","s":"OPB","d":"设计全栈技术方案。","i":["业务需求"],"o":["架构方案"],"u":["Project"],"r":"OPB/skills/rnd-fullstack-architect","m":"分层架构"},
 "rnd-api-design":{"n":"API设计","s":"OPB","d":"REST/GraphQL 接口设计。","i":["领域模型"],"o":["API 规范"],"u":["Project"],"r":"OPB/skills/rnd-api-design","m":"API First"},
 "rnd-db-table-design":{"n":"数据库表设计","s":"OPB","d":"表结构与索引设计。","i":["实体关系"],"o":["DDL"],"u":["Project"],"r":"OPB/skills/rnd-db-table-design","m":"范式+反范式"},
 "rnd-technical-writer":{"n":"技术写作","s":"OPB","d":"技术文档撰写。","i":["技术内容"],"o":["技术文档"],"u":["Document"],"r":"OPB/skills/rnd-technical-writer","m":"Docs-as-code"},
 "rnd-blog-planner":{"n":"博客系列规划","s":"OPB","d":"技术博客内容矩阵规划。","i":["主题"],"o":["选题矩阵"],"u":["Document"],"r":"OPB/skills/rnd-blog-planner","m":"内容漏斗"},
 "rnd-arch-diagrammer":{"n":"架构图绘制","s":"OPB","d":"用图表达系统架构。","i":["架构描述"],"o":["架构图"],"u":["Project"],"r":"OPB/skills/rnd-arch-diagrammer","m":"C4 模型"},
 "rnd-frontend-design":{"n":"前端设计","s":"OPB","d":"前端视觉与交互设计。","i":["需求"],"o":["设计稿"],"u":["Project"],"r":"OPB/skills/rnd-frontend-design","m":"设计系统"},
 "rnd-cockpit-architect":{"n":"座舱架构","s":"OPB","d":"智能座舱系统架构（行业专项）。","i":["车机需求"],"o":["座舱架构"],"u":["Project"],"r":"OPB/skills/rnd-cockpit-architect","m":"座舱域架构","industry_specific":True},
 "rnd-android-architect":{"n":"Android架构","s":"OPB","d":"Android 端架构（行业专项）。","i":["端侧需求"],"o":["Android 架构"],"u":["Project"],"r":"OPB/skills/rnd-android-architect","m":"MVVM/MVI","industry_specific":True},
 "rnd-android-perf":{"n":"Android性能","s":"OPB","d":"Android 性能优化（行业专项）。","i":["性能基线"],"o":["优化方案"],"u":["Project"],"r":"OPB/skills/rnd-android-perf","m":"性能剖析","industry_specific":True},
 "rnd-anr-analyzer":{"n":"ANR分析","s":"OPB","d":"ANR 卡顿根因分析（行业专项）。","i":["trace"],"o":["根因"],"u":["Project"],"r":"OPB/skills/rnd-anr-analyzer","m":"主线程阻塞分析","industry_specific":True},
 "rnd-auto-issue":{"n":"座舱问题分析","s":"OPB","d":"座舱问题自动归因（行业专项）。","i":["日志"],"o":["归因报告"],"u":["Project"],"r":"OPB/skills/rnd-auto-issue-analyzer","m":"日志聚类","industry_specific":True},
 "rnd-aspice-sys2swe":{"n":"ASPICE需求拆解","s":"OPB","d":"ASPICE 系统需求到软件需求拆解（行业专项）。","i":["系统需求"],"o":["软件需求"],"u":["Project"],"r":"OPB/skills/rnd-aspice-sys2swe","m":"ASPICE","industry_specific":True},
 "rnd-aspice-reviewer":{"n":"ASPICE需求评审","s":"OPB","d":"ASPICE 需求评审（行业专项）。","i":["需求"],"o":["评审结论"],"u":["Project"],"r":"OPB/skills/rnd-aspice-reviewer","m":"ASPICE","industry_specific":True},
 "design-ui-ux":{"n":"UI/UX设计","s":"OPB","d":"界面与体验设计。","i":["需求"],"o":["UI/UX 方案"],"u":["Project"],"r":"OPB/skills/design-ui-ux","m":"用户中心设计"},
 "design-visual":{"n":"视觉设计","s":"OPB","d":"视觉风格与素材设计。","i":["品牌"],"o":["视觉稿"],"u":["Project"],"r":"OPB/skills/design-visual","m":"视觉规范"},
 "design-remotion":{"n":"视频生成","s":"OPB","d":"用代码生成视频/动效。","i":["脚本"],"o":["视频"],"u":["Document"],"r":"OPB/skills/design-remotion","m":"Remotion 程序化视频"},
 "test-case-writer":{"n":"测试用例","s":"OPB","d":"编写覆盖用例。","i":["需求"],"o":["用例集"],"u":["Task"],"r":"OPB/skills/test-case-writer","m":"等价类+边界值"},
 "test-automation":{"n":"自动化测试","s":"OPB","d":"搭建自动化测试。","i":["待测系统"],"o":["测试脚本"],"u":["Project"],"r":"OPB/skills/test-automation","m":"测试金字塔"},
 "test-performance":{"n":"性能测试","s":"OPB","d":"压测与性能评估。","i":["系统","目标"],"o":["性能报告"],"u":["Project"],"r":"OPB/skills/test-performance","m":"负载模型"},
 "test-security":{"n":"安全测试","s":"OPB","d":"漏洞扫描与渗透。","i":["目标"],"o":["漏洞报告"],"u":["Project"],"r":"OPB/skills/test-security","m":"OWASP"},
 "test-manager":{"n":"测试管理","s":"OPB","d":"测试计划与质量门禁。","i":["发布计划"],"o":["测试计划"],"u":["Project"],"r":"OPB/skills/test-manager","m":"质量门禁"},
 "quality-system-builder":{"n":"质量体系建设","s":"OPB","d":"搭建质量管理体系。","i":["组织现状"],"o":["质量体系"],"u":["Organization"],"r":"OPB/skills/quality-system-builder","m":"ISO9001"},
 "quality-monitor":{"n":"质量监控","s":"OPB","d":"质量指标监控。","i":["指标"],"o":["监控看板"],"u":["Project"],"r":"OPB/skills/quality-monitor","m":"质量度量"},
 "quality-auditor":{"n":"质量审计","s":"OPB","d":"过程与产品审计。","i":["审计范围"],"o":["审计报告"],"u":["Project"],"r":"OPB/skills/quality-auditor","m":"过程审计"},
 "quality-improvement":{"n":"质量改进","s":"OPB","d":"问题根因与改进。","i":["质量问题"],"o":["改进方案"],"u":["Project"],"r":"OPB/skills/quality-improvement","m":"PDCA+8D"},
 "quality-risk-manager":{"n":"质量风险","s":"OPB","d":"质量风险识别与缓解。","i":["流程"],"o":["风险登记"],"u":["Project"],"r":"OPB/skills/quality-risk-manager","m":"FMEA"},
 "devops-system-ops":{"n":"系统运维","s":"OPB","d":"系统运行保障。","i":["系统"],"o":["运维方案"],"u":["Project"],"r":"OPB/skills/devops-system-ops","m":"SRE"},
 "devops-engineer":{"n":"DevOps","s":"OPB","d":"CI/CD 与交付流水线。","i":["代码库"],"o":["流水线"],"u":["Project"],"r":"OPB/skills/devops-engineer","m":"CI/CD"},
 "devops-cloud-arch":{"n":"云架构","s":"OPB","d":"云上架构设计。","i":["业务"],"o":["云架构"],"u":["Project"],"r":"OPB/skills/devops-cloud-arch","m":"Well-Architected"},
 "sec-strategist":{"n":"安全策略","s":"OPB","d":"安全战略与治理。","i":["资产"],"o":["安全战略"],"u":["Organization"],"r":"OPB/skills/sec-strategist","m":"安全治理"},
 "sec-data-security":{"n":"数据安全","s":"OPB","d":"数据分类分级与保护。","i":["数据流"],"o":["防护方案"],"u":["Policy","Document"],"r":"OPB/skills/sec-data-security","m":"数据分级"},
 "sec-incident-response":{"n":"安全响应","s":"OPB","d":"安全事件响应。","i":["事件"],"o":["处置报告"],"u":["Project"],"r":"OPB/skills/sec-incident-response","m":"IR 流程"},
 "meta-skill-creator":{"n":"技能创建器","s":"OPB","d":"按规范创建新技能。","i":["技能需求"],"o":["SKILL.md"],"u":["Project"],"r":"OPB/skills/meta-skill-creator","m":"Skill 规范"},
 "opc-template-engine":{"n":"OPC模板引擎","s":"ReS","d":"生成 OPC 标准化技能模板。","i":["技能定义"],"o":["模板"],"u":["Project"],"r":"ReScienceLab/skills","m":"模板引擎"},
 "opc-add-skill-engine":{"n":"新增OPC技能","s":"ReS","d":"向 OPC 体系新增技能。","i":["新技能需求"],"o":["技能文件"],"u":["Project"],"r":"ReScienceLab/skills","m":"插件化"},
 # 7 内容营销/品牌/视觉
 "content-app-namer":{"n":"应用起名","s":"OPB","d":"为产品起名与 slogan。","i":["定位"],"o":["名称候选"],"u":["Project"],"r":"OPB/skills/content-app-namer","m":"命名法"},
 "content-creator":{"n":"内容创作","s":"OPB","d":"多形态内容生成。","i":["主题"],"o":["内容"],"u":["Document"],"r":"OPB/skills/content-creator","m":"内容工厂"},
 "content-audio":{"n":"音频生成","s":"OPB","d":"播客/音频内容生成。","i":["脚本"],"o":["音频"],"u":["Document"],"r":"OPB/skills/content-audio","m":"TTS"},
 "content-video-script":{"n":"视频脚本","s":"OPB","d":"短视频脚本撰写。","i":["选题"],"o":["脚本"],"u":["Document"],"r":"OPB/skills/content-video-script","m":"脚本结构"},
 "content-altay":{"n":"散文写作","s":"OPB","d":"品牌故事/散文创作。","i":["主题"],"o":["文章"],"u":["Document"],"r":"OPB/skills/content-altay","m":"叙事写作"},
 "content-oss-article":{"n":"开源文章","s":"OPB","d":"技术/开源向文章。","i":["主题"],"o":["文章"],"u":["Document"],"r":"OPB/skills/content-oss-article","m":"技术写作"},
 "content-notebooklm":{"n":"研究助手","s":"OPB","d":"资料研读与综述。","i":["文献"],"o":["综述"],"u":["Document"],"r":"OPB/skills/content-notebooklm","m":"文献综述"},
 "mkt-ad-copywriter":{"n":"广告文案","s":"OPB","d":"转化导向广告文案。","i":["产品","受众"],"o":["文案"],"u":["Document"],"r":"OPB/skills/mkt-ad-copywriter","m":"AIDA"},
 "brand-manager":{"n":"品牌管理","s":"OPB","d":"品牌定位与资产管理。","i":["品牌现状"],"o":["品牌策略"],"u":["Organization"],"r":"OPB/skills/brand-manager","m":"品牌资产模型"},
 "brand-pr-strategist":{"n":"公关策略","s":"OPB","d":"公关传播策划。","i":["传播目标"],"o":["公关方案"],"u":["Event"],"r":"OPB/skills/brand-pr-strategist","m":"议题管理"},
 "brand-reputation":{"n":"舆情监控","s":"OPB","d":"舆情监测与应对。","i":["品牌"],"o":["舆情报告"],"u":["Organization"],"r":"OPB/skills/brand-reputation","m":"舆情监测"},
 "design-banner":{"n":"横幅创作","s":"ReS","d":"营销横幅设计。","i":["主题"],"o":["横幅"],"u":["Document"],"r":"ReScienceLab/skills/banner-creator","m":"视觉模板"},
 "design-logo":{"n":"Logo创作","s":"ReS","d":"Logo 设计。","i":["品牌"],"o":["Logo"],"u":["Document"],"r":"ReScienceLab/skills/logo-creator","m":"标识设计"},
 "design-image-ai":{"n":"AI图像","s":"ReS","d":"AI 生成营销图像。","i":["描述"],"o":["图像"],"u":["Document"],"r":"ReScienceLab/skills/image-ai","m":"文生图"},
 # 8 分销/渠道/商务拓展
 "bd-partnership":{"n":"合作伙伴管理","s":"OPB","d":"伙伴筛选与关系管理。","i":["伙伴需求"],"o":["合作方案"],"u":["Customer"],"r":"OPB/skills/business-development-partnership","m":"伙伴生命周期"},
 "bd-negotiator":{"n":"商务谈判","s":"OPB","d":"商务条款谈判。","i":["谈判议题"],"o":["谈判结果"],"u":["Person"],"r":"OPB/skills/business-development-negotiator","m":"双赢谈判"},
 "bd-channel-dev":{"n":"渠道拓展","s":"OPB","d":"渠道招募与管理。","i":["渠道策略"],"o":["渠道计划"],"u":["Customer"],"r":"OPB/skills/business-development-channel-developer","m":"渠道分级"},
 "dist-reddit":{"n":"Reddit分发","s":"ReS","d":"在 Reddit 做内容分发获客。","i":["内容"],"o":["分发计划"],"u":["Document"],"r":"ReScienceLab/skills/reddit-distributor","m":"社区分发"},
 "dist-twitter":{"n":"Twitter分发","s":"ReS","d":"Twitter/X 内容分发。","i":["内容"],"o":["分发计划"],"u":["Document"],"r":"ReScienceLab/skills/twitter-distributor","m":"社媒分发"},
 "dist-producthunt":{"n":"ProductHunt","s":"ReS","d":"ProductHunt 发布策划。","i":["产品"],"o":["发布方案"],"u":["Project"],"r":"ReScienceLab/skills/producthunt-launcher","m":"发布节奏"},
 "dist-requesthunt":{"n":"需求猎手","s":"ReS","d":"挖掘与提交产品需求。","i":["需求线索"],"o":["需求报告"],"u":["Project"],"r":"ReScienceLab/skills/requesthunt","m":"需求挖掘"},
 # 9 SEO/增长/社媒获客
 "seo-optimizer":{"n":"SEO优化","s":"OPB","d":"站内/站外 SEO 优化。","i":["站点"],"o":["SEO 方案"],"u":["Document"],"r":"OPB/skills/seo-optimizer","m":"SEO 技术"},
 "seo-geo":{"n":"地理SEO","s":"ReS","d":"本地地理 SEO 优化。","i":["区域"],"o":["本地方案"],"u":["Document"],"r":"ReScienceLab/skills/geo-seo","m":"本地搜索"},
 "seo-domain-hunter":{"n":"域名猎手","s":"ReS","d":"域名挖掘与评估。","i":["关键词"],"o":["域名候选"],"u":["Project"],"r":"ReScienceLab/skills/domain-hunter","m":"域名策略"},
 "growth-user-ops":{"n":"用户增长","s":"OPB","d":"增长漏斗与实验。","i":["增长目标"],"o":["增长方案"],"u":["Customer"],"r":"OPB/skills/growth-user-ops","m":"增长飞轮"},
 "growth-sustainably":{"n":"可持续增长","s":"slav","d":"低成本可持续增长策略。","i":["业务"],"o":["增长路径"],"u":["Organization"],"r":"slavingia/skills/grow-sustainably","m":"可持续增长"},
 "growth-first-customers":{"n":"首批客户","s":"slav","d":"获取首批付费客户。","i":["产品"],"o":["获客方案"],"u":["Customer"],"r":"slavingia/skills/first-customers","m":"早期获客"},
 "growth-pricing":{"n":"定价策略","s":"slav","d":"定价模型设计。","i":["成本","价值"],"o":["定价方案"],"u":["Product"],"r":"slavingia/skills/pricing","m":"价值定价"},
 # 10 销售/客户
 "sales-strategist":{"n":"销售策略","s":"OPB","d":"销售体系与打法设计。","i":["产品","市场"],"o":["销售策略"],"u":["Customer"],"r":"OPB/skills/sales-strategist","m":"销售方法论"},
 "sales-crm":{"n":"CRM管理","s":"OPB","d":"客户全生命周期管理。","i":["客户数据"],"o":["CRM 方案"],"u":["Customer"],"r":"OPB/skills/sales-crm","m":"CRM 漏斗"},
 "sales-forecaster":{"n":"销售预测","s":"OPB","d":"销售目标与预测。","i":["历史","目标"],"o":["预测"],"u":["Customer"],"r":"OPB/skills/sales-forecaster","m":" Pipeline 预测"},
 "support-customer-service":{"n":"客服助手","s":"OPB","d":"售前售后客服应答。","i":["客户问题"],"o":["应答"],"u":["Customer"],"r":"OPB/skills/support-customer-service","m":"服务剧本"},
 "support-technical":{"n":"技术支持","s":"OPB","d":"技术问题的排查与支持。","i":["故障"],"o":["解决方案"],"u":["Project"],"r":"OPB/skills/support-technical","m":"分级支持"},
 # 11 数据/分析/BI
 "data-analyst":{"n":"数据分析","s":"OPB","d":"数据清洗、分析与洞察。","i":["数据集"],"o":["分析报告"],"u":["Document"],"r":"OPB/skills/data-analyst","m":"EDA"},
 "data-user-behavior":{"n":"用户行为分析","s":"OPB","d":"行为漏斗与留存分析。","i":["行为数据"],"o":["行为洞察"],"u":["Customer"],"r":"OPB/skills/data-user-behavior","m":"漏斗/留存"},
 "data-bi":{"n":"商业智能","s":"OPB","d":"指标体系统与看板。","i":["业务指标"],"o":["BI 看板"],"u":["Organization"],"r":"OPB/skills/data-bi","m":"指标中台"},
 # 12 战略/商业模式/创业诊断
 "strategy-validate-idea":{"n":"创意验证","s":"slav","d":"用最小成本验证创意真伪。","i":["创意"],"o":["验证结论"],"u":["Goal"],"r":"slavingia/skills/validate-idea","m":"问题-方案拟合"},
 "strategy-mvp":{"n":"MVP设计","s":"slav","d":"设计最小可行产品。","i":["核心假设"],"o":["MVP 方案"],"u":["Project"],"r":"slavingia/skills/mvp","m":"MVP 裁剪"},
 "strategy-marketing-plan":{"n":"营销计划","s":"slav","d":"营销组合与节奏。","i":["产品","受众"],"o":["营销计划"],"u":["Project"],"r":"slavingia/skills/marketing-plan","m":"4P/7P"},
 "strategy-find-community":{"n":"社群发现","s":"slav","d":"找到目标社群与种子用户。","i":["画像"],"o":["社群列表"],"u":["Customer"],"r":"slavingia/skills/find-community","m":"社群地图"},
 "strategy-processize":{"n":"流程化","s":"slav","d":"把重复工作 SOP 化。","i":["流程描述"],"o":["SOP"],"u":["Task"],"r":"slavingia/skills/processize","m":"SOP 化"},
 "strategy-minimalist-review":{"n":"极简复盘","s":"slav","d":"一页纸极简复盘。","i":["周期"],"o":["复盘页"],"u":["Goal"],"r":"slavingia/skills/minimalist-review","m":"极简复盘"},
 "diagnosis-idea-feasibility":{"n":"创意可行性","s":"sober","d":"需求真伪校验、个人匹配度测评、竞品分析、可行性等级。","i":["projectInfo","demandDescription","personalSkills","budget","availableTime"],"o":["demandValidation","personalMatch","feasibilityLevel","nextStep"],"u":["Goal","Project"],"r":"sober568/docs/skill-reference","m":"五阶段-构思期"},
 "diagnosis-mvp-design":{"n":"诊断MVP设计","s":"sober","d":"MVP 裁剪、三层产品体系、交付成本测算。","i":["产品构想"],"o":["MVP 方案","成本测算"],"u":["Project"],"r":"sober568/docs/skill-reference","m":"五阶段-原型期"},
 "diagnosis-seed-coldstart":{"n":"种子冷启动","s":"sober","d":"低成本获客、招募策略、商业闭环验证。","i":["产品","受众"],"o":["冷启动方案"],"u":["Customer"],"r":"sober568/docs/skill-reference","m":"五阶段-验证期"},
 "diagnosis-scale-growth":{"n":"规模增长","s":"sober","d":"业务自动化、产品升级、渠道规模化。","i":["业务现状"],"o":["增长方案"],"u":["Organization"],"r":"sober568/docs/skill-reference","m":"五阶段-规模化期"},
 "diagnosis-feasibility-score":{"n":"可行性打分","s":"sober","d":"对可行性等级量化打分。","i":["诊断结论"],"o":["评分"],"u":["Goal"],"r":"sober568/docs/skill-reference","m":"评分卡"},
 "diagnosis-report-export":{"n":"诊断报告导出","s":"sober","d":"导出结构化诊断报告。","i":["诊断数据"],"o":["报告"],"u":["Document"],"r":"sober568/docs/skill-reference","m":"报告生成"},
 "diagnosis-user-feedback":{"n":"用户反馈","s":"sober","d":"采集并分析用户反馈。","i":["反馈"],"o":["反馈洞察"],"u":["Customer"],"r":"sober568/docs/skill-reference","m":"反馈分析"},
 "wf-opc-orchestrator":{"n":"OPC编排器","s":"easy","d":"一人公司阶段编排器：跨阶段状态机与交接。","i":["公司状态"],"o":["阶段计划","交接单"],"u":["Organization","Project","Task"],"r":"easychen/skills/opc-orchestrator","m":"六阶段状态机(自有表达)","derived":True},
 "wf-conversion-loop":{"n":"转化循环","s":"easy","d":"获客-转化-留存-复购的闭环工作流。","i":["流量"],"o":["转化漏斗"],"u":["Customer","Goal"],"r":"easychen/skills/opc-conversion-loop","m":"转化循环(自有表达)","derived":True},
 "wf-asset-ops":{"n":"资产运营","s":"easy","d":"数字资产运营与增殖工作流。","i":["资产清单"],"o":["运营计划"],"u":["Document","Account"],"r":"easychen/skills/opc-asset-ops","m":"资产运营(自有表达)","derived":True},
 "wf-business-model":{"n":"商业模式设计","s":"easy","d":"商业模式画布设计与验证。","i":["价值假设"],"o":["商业模式画布"],"u":["Organization","Goal"],"r":"easychen/skills/opc-business-model","m":"画布(自有表达)","derived":True},
 "wf-value-proposition":{"n":"价值主张","s":"easy","d":"价值主张设计与验证。","i":["客户痛点"],"o":["价值主张"],"u":["Customer","Goal"],"r":"easychen/skills/opc-value-proposition","m":"价值主张(自有表达)","derived":True},
 "wf-niche-positioning":{"n":"细分定位","s":"easy","d":"细分市场定位。","i":["市场"],"o":["定位"],"u":["Goal"],"r":"easychen/skills/opc-niche-positioning","m":"细分定位(自有表达)","derived":True},
 "wf-dashboard-review":{"n":"仪表盘复盘","s":"easy","d":"经营仪表盘定期复盘。","i":["经营数据"],"o":["复盘"],"u":["Organization"],"r":"easychen/skills/opc-dashboard-review","m":"仪表盘(自有表达)","derived":True},
 "wf-resource-audit":{"n":"资源审计","s":"easy","d":"资源盘点与配置审计。","i":["资源"],"o":["审计报告"],"u":["Organization"],"r":"easychen/skills/opc-resource-audit","m":"资源审计(自有表达)","derived":True},
 "wf-mvp-designer":{"n":"MVP设计器","s":"easy","d":"MVP 范围设计与验证计划。","i":["核心假设"],"o":["MVP 范围"],"u":["Project"],"r":"easychen/skills/opc-mvp-designer","m":"MVP(自有表达)","derived":True},
}

# ───────────────────────── OPB 真实方法论抽取 ─────────────────────────
def load_opb_descriptions():
    """遍历 OPB 92 个 SKILL.md，优先抽 frontmatter 的 description(真实方法论简介)，返回 {dirkey: (title, desc)}"""
    out = {}
    base = os.path.join(SRC, "chendongqi-OPB-Skills", "skills")
    if not os.path.isdir(base):
        return out
    for d in glob.glob(os.path.join(base, "*")):
        if not os.path.isdir(d):
            continue
        md = os.path.join(d, "SKILL.md")
        if not os.path.isfile(md):
            continue
        key = os.path.basename(d).lower()
        try:
            txt = open(md, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        title, desc = "", ""
        # 解析 frontmatter（--- ... ---）
        if txt.lstrip().startswith("---"):
            end = txt.find("---", 3)
            if end != -1:
                fm = txt[3:end]
                body = txt[end+3:]
                try:
                    fm_yaml = yaml.safe_load(fm)
                    if isinstance(fm_yaml, dict):
                        title = fm_yaml.get("name", "") or ""
                        desc = fm_yaml.get("description", "") or ""
                except Exception:
                    body = txt
            else:
                body = txt
        else:
            body = txt
        # description 缺失时，取正文第一个足够长的非空非标题段
        if not desc:
            for l in body.splitlines():
                s = l.strip()
                if s and not s.startswith("#") and not s.startswith(">") and len(s) > 25:
                    desc = s
                    break
        if not title:
            for l in body.splitlines():
                if l.strip().startswith("#"):
                    title = l.strip().lstrip("#").strip()
                    break
        # 过滤掉形如 frontmatter 键的伪描述（裸 name:/description:/--- 开头）
        if desc.startswith(("name:", "description:", "---")):
            desc = ""
        out[key] = (title, desc[:500])
    return out

def match_opb(slug, opb):
    """模糊匹配：slug tokens 与 OPB 目录 tokens 重叠最多者"""
    st = set(re.split(r"[-\s]+", slug.lower()))
    best, best_score = None, 0
    for k, (title, desc) in opb.items():
        kt = set(re.split(r"[-\s]+", k))
        score = len(st & kt)
        if score > best_score:
            best, best_score = (k, title, desc), score
    return best if best_score >= 2 else None

def main():
    da = yaml.safe_load(open(os.path.join(REF, "department_actions.yaml"), encoding="utf-8"))
    opb = load_opb_descriptions()
    specs = {}
    used_opb = 0
    for dept, body in da["departments"].items():
        for a in body["actions"]:
            slug = a["slug"]; src = a["source"]
            fb = FALLBACK.get(slug, {})
            spec = {
                "name": fb.get("n", a["name"]),
                "source": src,
                "desc": fb.get("d", a["name"]),
                "inputs": fb.get("i", []),
                "outputs": fb.get("o", []),
                "uses_entities": fb.get("u", []),
                "skill_ref": fb.get("r", ""),
            }
            if a.get("industry_specific"):
                spec["industry_specific"] = True
            if a.get("derived"):
                spec["derived"] = True
            # OPB 真实描述覆盖（优先）
            if src == "OPB":
                m = match_opb(slug, opb)
                if m:
                    _, title, desc = m
                    if desc:
                        spec["desc"] = desc
                        spec["skill_ref"] = "OPB/skills/" + m[0]
                        used_opb += 1
            specs[slug] = spec
    # 写文件
    out = {"meta": {"generated_by": "gen_action_specs.py", "total": len(specs), "opb_real_covered": used_opb}, "actions": specs}
    with open(os.path.join(REF, "action_specs.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False)
    print(f"action_specs.yaml 生成完成：共 {len(specs)} 个动作，其中 OPB 真实描述覆盖 {used_opb} 个")
    missing = [s for s in specs if not FALLBACK.get(s)]
    print("未命中兜底(应有 0):", missing)

if __name__ == "__main__":
    main()
