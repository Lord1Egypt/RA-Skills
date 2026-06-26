---
name: Obstetrics-and-Gynecology-PMPH-10edition
version: 1.0.0
description: 基于人民卫生出版社《妇产科学》第10版 — 187 项妇产科临床技能注册表
author: PMPH
categories: 15
skills: 187
categories:
  - 妊娠与产科管理(41) | 高危妊娠与并发症(19) | 分娩与产后管理(9)
  - 妇科肿瘤(22) | 生殖内分泌与不孕不育(17) | 子宫内膜异位症与子宫肌瘤(5)
  - 妇科感染与炎症(9) | 外阴与阴道疾病(7) | 盆底与泌尿妇科(4)
  - 青春期、围绝经期与老年妇科(5) | 遗传、产前筛查与诊断(11) | 女性性健康与心理(4)
  - 解剖、生理与基础医学(8) | 手术与操作技术(3) | 教学、资源与质控(23)
---

# SKILL 核心配置

本文件为所有技能的注册表，每个技能条目包含：
- **name**: 技能标识符（对应同名文件夹）
- **display**: 中文显示名称
- **category**: 所属分类
- **trigger**: 触发条件/使用时机
- **ref**: 详细文档路径

---

## 🤰 妊娠与产科管理 (41)

- name: post-term-pregnancy-diagnosis-and-management
  display: 过期妊娠诊断与管理
  trigger: 妊娠≥41周且孕周经可靠方法确认时
  ref: post-term-pregnancy-diagnosis-and-management/SKILL.md

- name: prenatal-visit-scheduling
  display: 产前检查计划制定
  trigger: 需为孕妇制定或验证产检时间安排时
  ref: prenatal-visit-scheduling/SKILL.md

- name: estimated-due-date-calculation
  display: 预产期计算
  trigger: 首次产检需确定或验证预产期时
  ref: estimated-due-date-calculation/SKILL.md

- name: pregnancy-weight-gain-recommendation
  display: 孕期体重增长指导
  trigger: 首次产检已知孕前体重和身高时
  ref: pregnancy-weight-gain-recommendation/SKILL.md

- name: shoulder-dystocia-emergency-management
  display: 肩难产应急处理
  trigger: 胎头娩出后出现乌龟征、胎肩无法娩出时
  ref: shoulder-dystocia-emergency-management/SKILL.md

- name: shoulder-presentation-diagnosis-and-delivery
  display: 肩先露诊断与分娩处理
  trigger: 腹部检查显示子宫横椭圆形、阴道检查触及肩胛骨时
  ref: shoulder-presentation-diagnosis-and-delivery/SKILL.md

- name: second-stage-labor-abnormalities
  display: 第二产程异常分类与处理
  trigger: 第二产程持续时间超阈值、胎头下降停滞时
  ref: second-stage-labor-abnormalities/SKILL.md

- name: persistent-occiput-posterior-transverse-position-management
  display: 持续性枕后位/枕横位处理
  trigger: 第二产程进展缓慢且胎方位为枕后位或枕横位时
  ref: persistent-occiput-posterior-transverse-position-management/SKILL.md

- name: diagnosis-and-management-of-occiput-anterior-posterior-vertical-position
  display: 高直前位/高直后位诊治
  trigger: 阴道检查发现胎头矢状缝位于骨盆入口前后径时
  ref: diagnosis-and-management-of-occiput-anterior-posterior-vertical-position/SKILL.md

- name: buttocks-presentation-vaginal-delivery-management
  display: 臀先露阴道分娩管理
  trigger: 宫缩时阴道外口见胎足且宫口未开全时
  ref: buttocks-presentation-vaginal-delivery-management/SKILL.md

- name: macrosomic-fetus-delivery-mode-selection
  display: 巨大儿分娩方式选择
  trigger: 估计胎儿体重≥4000g时
  ref: macrosomic-fetus-delivery-mode-selection/SKILL.md

- name: narrow-pelvis-classification-and-delivery-decision
  display: 狭窄骨盆分类与分娩决策
  trigger: 骨盆测量显示任一平面径线低于正常阈值时
  ref: narrow-pelvis-classification-and-delivery-decision/SKILL.md

- name: uterine-hypercontractility-classification
  display: 子宫收缩过强分类与风险预警
  trigger: 产妇出现宫缩频率异常增高或持续性腹痛时
  ref: uterine-hypercontractility-classification/SKILL.md

- name: uterine-hypercontractility-narrow-pelvis-emergency
  display: 子宫收缩过强及狭窄骨盆紧急处理
  trigger: 确诊不协调性宫缩过强伴胎心异常时
  ref: uterine-hypercontractility-narrow-pelvis-emergency/SKILL.md

- name: oxytocin-iv-infusion-for-hypotonic-uterine-contraction
  display: 缩宫素静脉滴注催产
  trigger: 协调性宫缩乏力、无头盆不称、胎心良好时
  ref: oxytocin-iv-infusion-for-hypotonic-uterine-contraction/SKILL.md

- name: preterm-labor-tocolytic-selection
  display: 早产宫缩抑制药物选择与使用
  trigger: 孕周<37周、规律宫缩伴宫颈缩短且无立即终止妊娠指征时
  ref: preterm-labor-tocolytic-selection/SKILL.md

- name: hyperemesis-gravidarum-diagnosis-and-treatment
  display: 妊娠剧吐诊断与综合治疗
  trigger: 妊娠6-10周持续呕吐、体重下降>5%、尿酮体阳性时
  ref: hyperemesis-gravidarum-diagnosis-and-treatment/SKILL.md

- name: spontaneous-abortion-classification
  display: 自然流产临床分型与处理
  trigger: 妊娠≤28周阴道流血/腹痛时
  ref: spontaneous-abortion-classification/SKILL.md

- name: pprom-expectant-management
  display: 未足月胎膜早破期待治疗
  trigger: 妊娠28–33周诊断为PPROM且无感染禁忌证时
  ref: pprom-expectant-management/SKILL.md

- name: qian-zhi-tai-pan-qi-dai-liao-fa
  display: 前置胎盘期待治疗
  trigger: 妊娠＜36周、阴道流血量少、母儿状况稳定时
  ref: qian-zhi-tai-pan-qi-dai-liao-fa/SKILL.md

- name: qian-zhi-tai-pan-zhong-zhi-ren-shen
  display: 前置胎盘终止妊娠
  trigger: 确诊前置胎盘并出现大出血、休克或胎儿窘迫时
  ref: qian-zhi-tai-pan-zhong-zhi-ren-shen/SKILL.md

- name: placenta-previa-classification
  display: 前置胎盘分类
  trigger: 孕周≥28周阴道超声确认胎盘位置异常时
  ref: placenta-previa-classification/SKILL.md

- name: placenta-accreta-diagnosis-and-management
  display: 胎盘植入诊断与处理
  trigger: 胎儿娩出后胎盘滞留、剥离困难或术中发现异常粘连时
  ref: placenta-accreta-diagnosis-and-management/SKILL.md

- name: velamentous-cord-insertion-with-vasa-previa-management
  display: 脐带帆状附着合并前置血管管理
  trigger: 超声确诊脐带帆状附着且血管跨过宫颈内口时
  ref: velamentous-cord-insertion-with-vasa-previa-management/SKILL.md

- name: umbilical-cord-entanglement-diagnosis-and-management
  display: 脐带缠绕诊断与管理
  trigger: 超声显示胎儿颈部/躯干压迹或多普勒检出环绕血流时
  ref: umbilical-cord-entanglement-diagnosis-and-management/SKILL.md

- name: umbilical-cord-prolapse-diagnosis-and-management
  display: 脐带脱垂诊断与处理
  trigger: 临产孕妇胎膜已破且出现胎心率异常时
  ref: umbilical-cord-prolapse-diagnosis-and-management/SKILL.md

- name: acute-fetal-distress-emergency-management
  display: 急性胎儿窘迫紧急处理
  trigger: 分娩期出现Ⅲ类EFM图形或其他急性胎儿窘迫征象时
  ref: acute-fetal-distress-emergency-management/SKILL.md

- name: late-pregnancy-fetal-movement-monitoring
  display: 晚孕期胎动监测
  trigger: 妊娠≥28周需进行胎儿宫内安危初步筛查时
  ref: late-pregnancy-fetal-movement-monitoring/SKILL.md

- name: amniotic-fluid-volume-assessment
  display: 羊水量评估
  trigger: 需判断羊水过多或过少以辅助诊断时
  ref: amniotic-fluid-volume-assessment/SKILL.md

- name: amniotic-fluid-volume-abnormality-ultrasound
  display: 羊水量异常超声诊断
  trigger: DVP≥8cm/AFI≥25cm或DVP≤2cm/AFI≤5cm时
  ref: amniotic-fluid-volume-abnormality-ultrasound/SKILL.md

- name: efm-three-tier-interpretation
  display: EFM三级分类判读
  trigger: 产程中实施≥20分钟连续EFM时
  ref: efm-three-tier-interpretation/SKILL.md

- name: fetal-in-utero-intervention-principles
  display: 胎儿宫内干预原则
  trigger: 胎儿确诊为CPAM/TTTS/严重心律失常等可干预疾病时
  ref: fetal-in-utero-intervention-principles/SKILL.md

- name: ttts-diagnosis-and-staging
  display: TTTS诊断与Quintero分期
  trigger: 单绒毛膜双胎超声显示羊水量显著差异时
  ref: ttts-diagnosis-and-staging/SKILL.md

- name: ttts-fetoscopic-laser-surgery-indications
  display: TTTS胎儿镜激光手术指征
  trigger: 确诊TTTS且处于Quintero分期Ⅰ–Ⅳ期、孕周16–26周时
  ref: ttts-fetoscopic-laser-surgery-indications/SKILL.md

- name: fetal-laser-occlusion-of-placental-anastomoses
  display: 胎盘血管吻合支激光凝固
  trigger: 胎儿镜已置入受血胎儿羊膜腔并直视胎盘表面血管时
  ref: fetal-laser-occlusion-of-placental-anastomoses/SKILL.md

- name: fgr-diagnosis-and-monitoring
  display: FGR诊断与监护
  trigger: 超声估测体重或腹围低于第10百分位数时
  ref: fgr-diagnosis-and-monitoring/SKILL.md

---

## ⚠️ 高危妊娠与并发症 (19)

- name: preeclampsia-pathophysiology-analysis
  display: 子痫前期病理生理机制分析
  trigger: 妊娠20周后高血压伴/不伴蛋白尿出现多系统器官功能障碍时
  ref: preeclampsia-pathophysiology-analysis/SKILL.md

- name: preeclampsia-diagnosis-severe-features
  display: 子痫前期诊断与重度特征判定
  trigger: 妊娠≥20周新发高血压≥140/90mmHg且合并蛋白尿或终末器官损害时
  ref: preeclampsia-diagnosis-severe-features/SKILL.md

- name: preeclampsia-delivery-timing-decision
  display: 子痫前期终止妊娠时机决策
  trigger: 子痫前期/HELLP综合征经24–48小时治疗后病情无改善或进展时
  ref: preeclampsia-delivery-timing-decision/SKILL.md

- name: magnesium-sulfate-therapy-for-preeclampsia-eclampsia
  display: 硫酸镁解痉治疗
  trigger: 重度子痫前期、子痫发作或高危孕妇需解痉治疗时
  ref: magnesium-sulfate-therapy-for-preeclampsia-eclampsia/SKILL.md

- name: peripartum-cardiomyopathy-diagnosis-and-management
  display: 围产期心肌病诊治
  trigger: 妊娠晚期至产后6个月内出现心衰症状且LVEF<45%时
  ref: peripartum-cardiomyopathy-diagnosis-and-management/SKILL.md

- name: pregnancy-appendicitis-and-pancreatitis-surgical-decision
  display: 妊娠期阑尾炎/胰腺炎手术决策
  trigger: 孕妇确诊妊娠期急性阑尾炎或急性胰腺炎时
  ref: pregnancy-appendicitis-and-pancreatitis-surgical-decision/SKILL.md

- name: cardiac-disease-high-risk-period-monitoring
  display: 心脏病高风险期监护
  trigger: 孕妇患有心脏病且处于妊娠32周后、分娩期或产后3日内时
  ref: cardiac-disease-high-risk-period-monitoring/SKILL.md

- name: pregnancy-hypercoagulability-assessment
  display: 妊娠期高凝状态评估
  trigger: 围产期对无病理性凝血障碍孕妇进行常规血栓风险筛查时
  ref: pregnancy-hypercoagulability-assessment/SKILL.md

- name: gestational-thrombocytopenia-management
  display: 妊娠期血小板减少管理
  trigger: 妊娠晚期出现轻度血小板减少且无出血症状时
  ref: gestational-thrombocytopenia-management/SKILL.md

- name: pregnancy-anemia-diagnosis-and-treatment
  display: 妊娠期贫血诊治
  trigger: 孕妇血红蛋白<110g/L且血细胞比容<0.33时
  ref: pregnancy-anemia-diagnosis-and-treatment/SKILL.md

- name: physiological-glycosuria-vs-gdm-differentiation
  display: 生理性糖尿与GDM鉴别
  trigger: 孕妇尿糖阳性但无典型糖尿病症状时
  ref: physiological-glycosuria-vs-gdm-differentiation/SKILL.md

- name: pregnancy-thyroid-hypofunction-management
  display: 妊娠期甲状腺功能减退管理
  trigger: 孕妇确诊临床甲减或亚临床甲减伴TPOAb阳性时
  ref: pregnancy-thyroid-hypofunction-management/SKILL.md

- name: viral-hepatitis-diagnosis-in-pregnancy
  display: 妊娠期病毒性肝炎诊断
  trigger: 妊娠期女性出现消化道症状、黄疸且有肝炎接触史时
  ref: viral-hepatitis-diagnosis-in-pregnancy/SKILL.md

- name: thalassemia-screening-and-diagnosis
  display: 地中海贫血筛查与诊断
  trigger: MCV<82fl且MCH<27pg并已排除缺铁性贫血时
  ref: thalassemia-screening-and-diagnosis/SKILL.md

- name: rh-negative-pregnancy-rh-incompatibility-prevention
  display: Rh阴性妊娠同种免疫预防
  trigger: Rh阴性未致敏孕妇需规范注射抗D免疫球蛋白时
  ref: rh-negative-pregnancy-rh-incompatibility-prevention/SKILL.md

- name: congenital-heart-disease-pregnancy-suitability-assessment
  display: 先心病妊娠适宜性评估
  trigger: 孕前咨询或早孕期≤12周评估先心病患者时
  ref: congenital-heart-disease-pregnancy-suitability-assessment/SKILL.md

- name: neonatal-hepatitis-b-mother-to-child-transmission-prevention
  display: 新生儿乙肝母婴阻断
  trigger: 母亲HBsAg阳性、状态不明或有乙肝家族史时
  ref: neonatal-hepatitis-b-mother-to-child-transmission-prevention/SKILL.md

- name: maternal-fetal-medicine-subspecialty-triage
  display: 母体胎儿医学亚专科分诊
  trigger: 妊娠患者需分配至普通产科、母体医学或胎儿医学亚专科时
  ref: maternal-fetal-medicine-subspecialty-triage/SKILL.md

- name: common-pregnancy-symptom-management
  display: 常见妊娠症状管理
  trigger: 孕妇出现恶心、贫血、水肿、便秘等常见妊娠症状时
  ref: common-pregnancy-symptom-management/SKILL.md

- name: tubal-pregnancy-diagnosis-protocol
  display: 输卵管妊娠诊断方案
  trigger: 育龄女性停经伴腹痛或阴道流血、hCG阳性但超声未见宫内孕囊时
  ref: tubal-pregnancy-diagnosis-protocol/SKILL.md

- name: tubal-pregnancy-etiology-analysis
  display: 输卵管妊娠病因分析
  trigger: 有早孕症状且需排除异位妊娠时
  ref: tubal-pregnancy-etiology-analysis/SKILL.md

- name: tubal-pregnancy-pathological-outcomes
  display: 输卵管妊娠病理结局判断
  trigger: 输卵管妊娠病史且出现腹痛、出血或hCG异常时
  ref: tubal-pregnancy-pathological-outcomes/SKILL.md

- name: hbv-vertical-transmission-blocking
  display: HBV母婴垂直传播阻断
  trigger: 孕妇HBsAg阳性时
  ref: hbv-vertical-transmission-blocking/SKILL.md

- name: icp-diagnosis-and-severity-classification
  display: 妊娠期肝内胆汁淤积症诊断与分度
  trigger: 妊娠中晚期孕妇出现无皮损瘙痒且需判断ICP诊断时
  ref: icp-diagnosis-and-severity-classification/SKILL.md

---

## 🛏️ 分娩与产后管理 (9)

- name: uterine-atony-postpartum-hemorrhage-management
  display: 子宫收缩乏力性产后出血处理
  trigger: 产后子宫轮廓不清、质地软、阴道持续出血时
  ref: uterine-atony-postpartum-hemorrhage-management/SKILL.md

- name: postpartum-hemorrhage-diagnosis-and-quantification
  display: 产后出血诊断与量化
  trigger: 胎儿娩出后阴道分娩出血≥500ml或剖宫产出血≥1000ml时
  ref: postpartum-hemorrhage-diagnosis-and-quantification/SKILL.md

- name: late-postpartum-hemorrhage-management
  display: 晚期产后出血处理
  trigger: 产后24小时至产褥期末出现阴道流血时
  ref: late-postpartum-hemorrhage-management/SKILL.md

- name: postpartum-2-hour-complication-monitoring
  display: 产后2小时并发症监测
  trigger: 产妇处于产后0-2小时观察期时
  ref: postpartum-2-hour-complication-monitoring/SKILL.md

- name: postpartum-depression-diagnosis-intervention
  display: 产后抑郁症诊断与干预
  trigger: 产妇抑郁症状持续≥2周且影响社会功能时
  ref: postpartum-depression-diagnosis-intervention/SKILL.md

- name: lochia-staging-and-abnormal-warning
  display: 恶露分期识别与异常预警
  trigger: 产后6周内观察到阴道排出物时
  ref: lochia-staging-and-abnormal-warning/SKILL.md

- name: breastfeeding-maintenance-and-insufficiency-intervention
  display: 母乳分泌维持与不足干预
  trigger: 产妇主诉乳汁不足或婴儿摄入疑似不足时
  ref: breastfeeding-maintenance-and-insufficiency-intervention/SKILL.md

- name: puerperal-infection-clinical-classification
  display: 产褥感染临床分型
  trigger: 产褥期女性（产后6周内）出现发热、疼痛或异常恶露时
  ref: puerperal-infection-clinical-classification/SKILL.md

- name: amniotic-fluid-embolism-diagnosis-and-rescue
  display: 羊水栓塞诊断与抢救
  trigger: 分娩/剖宫产/产后短时间内突发低氧血症、低血压和凝血功能障碍三联征时
  ref: amniotic-fluid-embolism-diagnosis-and-rescue/SKILL.md

---

## 🧬 妇科肿瘤 (22)

- name: cervical-cancer-chemoradiation-protocol
  display: 子宫颈癌同步放化疗方案
  trigger: 局部晚期≥IB3期或术后高危因素阳性时
  ref: cervical-cancer-chemoradiation-protocol/SKILL.md

- name: cervical-cancer-staging-based-personalized-treatment
  display: 子宫颈癌分期个体化治疗
  trigger: 子宫颈癌确诊且需制定治疗方案时
  ref: cervical-cancer-staging-based-personalized-treatment/SKILL.md

- name: cervical-cancer-three-tier-prevention-strategy
  display: 子宫颈癌三级预防策略
  trigger: 涉及宫颈癌防控体系构建或个体化筛查建议时
  ref: cervical-cancer-three-tier-prevention-strategy/SKILL.md

- name: vulvar-squamous-cell-carcinoma-diagnosis-and-staging
  display: 外阴鳞状细胞癌诊断与分期
  trigger: 外阴可疑病灶（赘生物、溃疡）需系统性诊断时
  ref: vulvar-squamous-cell-carcinoma-diagnosis-and-staging/SKILL.md

- name: vulvar-squamous-cell-carcinoma-surgical-management
  display: 外阴鳞状细胞癌手术管理
  trigger: 病理确诊和分期后需确定手术方式时
  ref: vulvar-squamous-cell-carcinoma-surgical-management/SKILL.md

- name: endometrial-cancer-molecular-subtyping
  display: 子宫内膜癌分子分型
  trigger: 具备完整分子检测结果需进行四类分子分型时
  ref: endometrial-cancer-molecular-subtyping/SKILL.md

- name: endometrial-cancer-molecular-subtyping-for-treatment
  display: 子宫内膜癌分子分型指导治疗
  trigger: 已确诊子宫内膜癌且具备组织样本需确定治疗强度时
  ref: endometrial-cancer-molecular-subtyping-for-treatment/SKILL.md

- name: endometrial-cancer-postop-risk-stratification
  display: 子宫内膜癌术后风险分层
  trigger: 提供完整术后病理报告并询问后续治疗建议时
  ref: endometrial-cancer-postop-risk-stratification/SKILL.md

- name: endometrial-cancer-fertility-preserving-treatment
  display: 子宫内膜癌保留生育功能治疗
  trigger: 年龄≤40-45岁、有生育意愿、低级别子宫内膜样癌时
  ref: endometrial-cancer-fertility-preserving-treatment/SKILL.md

- name: endometrial-cancer-screening-indications
  display: 子宫内膜癌筛查指征
  trigger: 绝经后/绝经过渡期或异常子宫出血需筛查时
  ref: endometrial-cancer-screening-indications/SKILL.md

- name: endometrial-polyp-histopathological-diagnosis
  display: 子宫内膜息肉病理诊断
  trigger: 已获取子宫内膜息肉切除标本需确诊时
  ref: endometrial-polyp-histopathological-diagnosis/SKILL.md

- name: uterine-leiomyosarcoma-histological-diagnosis
  display: 子宫平滑肌肉瘤组织学诊断
  trigger: 子宫肌层来源肿瘤HE染色切片需判断时
  ref: uterine-leiomyosarcoma-histological-diagnosis/SKILL.md

- name: ovarian-epithelial-tumor-surgical-management
  display: 卵巢上皮性肿瘤手术管理
  trigger: 确诊卵巢上皮性肿瘤后需制定手术方案时
  ref: ovarian-epithelial-tumor-surgical-management/SKILL.md

- name: ovarian-germ-cell-tumor-fertility-sparing-treatment
  display: 卵巢生殖细胞肿瘤保留生育功能治疗
  trigger: 年轻患者需保留生育功能且为生殖细胞肿瘤时
  ref: ovarian-germ-cell-tumor-fertility-sparing-treatment/SKILL.md

- name: epithelioid-trophoblastic-tumor-surgical-management
  display: 上皮样滋养细胞肿瘤手术管理
  trigger: 病理确诊ETT且病变局限可耐受手术时
  ref: epithelioid-trophoblastic-tumor-surgical-management/SKILL.md

- name: ett-chemotherapy-immunotherapy-combination
  display: ETT化疗联合免疫治疗
  trigger: 复发/转移性ETT对常规化疗反应不佳时
  ref: ett-chemotherapy-immunotherapy-combination/SKILL.md

- name: gynecological-solid-pelvic-mass-malignancy-screening
  display: 妇科实性盆腔包块恶性筛查
  trigger: 下腹部实性包块已排除良性病变时
  ref: gynecological-solid-pelvic-mass-malignancy-screening/SKILL.md

- name: fallopian-tube-cancer-triad
  display: 输卵管癌三联征识别与诊断
  trigger: 同时出现阴道排液、下腹胀痛及盆腔包块时
  ref: fallopian-tube-cancer-triad/SKILL.md

- name: high-grade-serous-carcinoma-origin-assessment
  display: 高级别浆液性癌起源评估
  trigger: 卵巢或腹膜病变不典型但输卵管存在上皮内癌时
  ref: high-grade-serous-carcinoma-origin-assessment/SKILL.md

- name: cervical-pregnancy-diagnosis-and-management
  display: 宫颈妊娠诊断与处理
  trigger: 妇科检查发现宫颈桶状膨大、宫腔空虚时
  ref: cervical-pregnancy-diagnosis-and-management/SKILL.md

- name: gynecologic-cancer-immunotherapy-selection
  display: 妇科肿瘤免疫治疗选择
  trigger: 晚期/复发性妇科肿瘤患者需根据生物标志物选择ICI或肿瘤疫苗时
  ref: gynecologic-cancer-immunotherapy-selection/SKILL.md

- name: ovarian-cancer-chemotherapy-regimen-selection
  display: 卵巢癌化疗方案选择
  trigger: 卵巢上皮性癌患者需制定个体化化疗计划时
  ref: ovarian-cancer-chemotherapy-regimen-selection/SKILL.md

---

## 💊 生殖内分泌与不孕不育 (17)

- name: pcos-diagnosis-china-2011
  display: PCOS诊断（中国2011标准）
  trigger: 女性出现月经异常需排除PCOS时
  ref: pcos-diagnosis-china-2011/SKILL.md

- name: pcos-drug-treatment-selection
  display: PCOS药物治疗选择
  trigger: 已确诊PCOS需制定个体化药物治疗方案时
  ref: pcos-drug-treatment-selection/SKILL.md

- name: luteal-phase-deficiency-diagnosis-and-treatment
  display: 黄体功能不足诊治
  trigger: 月经周期缩短、经前期出血或不孕且高温相<11日时
  ref: luteal-phase-deficiency-diagnosis-and-treatment/SKILL.md

- name: luteinized-unruptured-follicle-syndrome-diagnosis
  display: 未破卵泡黄素化综合征诊断
  trigger: 规律月经、双相基础体温但长期不孕时
  ref: luteinized-unruptured-follicle-syndrome-diagnosis/SKILL.md

- name: amenorrhea-progestogen-estrogen-test
  display: 闭经孕激素与雌孕激素序贯试验
  trigger: 闭经女性需进行内分泌功能评估时
  ref: amenorrhea-progestogen-estrogen-test/SKILL.md

- name: amenorrhea-etiology-classification
  display: 闭经病因分类与诊断路径
  trigger: 女性出现病理性闭经已排除妊娠及生理性无月经时
  ref: amenorrhea-etiology-classification/SKILL.md

- name: poi-diagnosis-and-evaluation
  display: 早发性卵巢功能不全诊断
  trigger: 年龄<40岁、闭经/月经异常≥4个月时
  ref: poi-diagnosis-and-evaluation/SKILL.md

- name: female-infertility-cause-classification
  display: 女性不孕症病因分类
  trigger: 生殖科医生完成基础病史采集和初步检查后
  ref: female-infertility-cause-classification/SKILL.md

- name: infertility-definition-classification
  display: 不孕症定义与分类
  trigger: 规律无避孕性生活满12个月未妊娠时
  ref: infertility-definition-classification/SKILL.md

- name: ovulation-induction-drug-protocol-and-monitoring
  display: 诱导排卵药物方案与监测
  trigger: 确诊排卵障碍且下丘脑-垂体-卵巢轴功能基本健全时
  ref: ovulation-induction-drug-protocol-and-monitoring/SKILL.md

- name: controlled-ovarian-hyperstimulation-protocol
  display: 控制性超促排卵方案
  trigger: 患者进入IVF/ICSI周期且满足卵巢储备评估标准时
  ref: controlled-ovarian-hyperstimulation-protocol/SKILL.md

- name: embryo-implantation-receptivity-assessment
  display: 胚胎着床容受性评估
  trigger: 不孕症或反复流产患者排查着床失败原因时
  ref: embryo-implantation-receptivity-assessment/SKILL.md

- name: preimplantation-genetic-testing-classification-and-indications
  display: 植入前遗传学检测分类与指征
  trigger: 夫妇存在单基因病/染色体异常/高龄/反复流产时
  ref: preimplantation-genetic-testing-classification-and-indications/SKILL.md

- name: assisted-reproductive-technology-selection
  display: 辅助生殖技术选择
  trigger: 确诊不孕症且常规治疗无效时
  ref: assisted-reproductive-technology-selection/SKILL.md

- name: bu-yun-zheng-ding-yi-fen-lei
  display: 不孕症定义与分类
  trigger: 规律无避孕性生活满12个月（≥35岁则6个月）未妊娠时
  ref: bu-yun-zheng-ding-yi-fen-lei/SKILL.md

- name: premenstrual-syndrome-etiology-analysis
  display: 经前期综合征病因分析
  trigger: 育龄期女性黄体期出现周期性躯体、精神或行为症状时
  ref: premenstrual-syndrome-etiology-analysis/SKILL.md

- name: cah-female-virilization-diagnosis-and-treatment
  display: 先天性肾上腺皮质增生症女性男性化诊治
  trigger: 46,XX女性新生儿或胎儿出现阴蒂肥大、阴唇融合等男性化表现时
  ref: cah-female-virilization-diagnosis-and-treatment/SKILL.md

---

## 🔴 子宫内膜异位症与子宫肌瘤 (5)

- name: endometriosis-and-adenomyosis-differentiation
  display: 子宫内膜异位症与腺肌病鉴别
  trigger: 生育期女性出现继发性进行性痛经、月经过多或不孕时
  ref: endometriosis-and-adenomyosis-differentiation/SKILL.md

- name: endometriosis-diagnostic-pathway
  display: 子宫内膜异位症诊断路径
  trigger: 疑似子宫内膜异位症的生育期女性需系统性诊断时
  ref: endometriosis-diagnostic-pathway/SKILL.md

- name: endometriosis-treatment-strategy
  display: 子宫内膜异位症治疗策略
  trigger: 确诊或高度临床怀疑子宫内膜异位症时
  ref: endometriosis-treatment-strategy/SKILL.md

- name: endometriosis-prevention-strategies
  display: 子宫内膜异位症预防策略
  trigger: 育龄期存在经血逆流风险、高发家族史或即将接受宫腔手术时
  ref: endometriosis-prevention-strategies/SKILL.md

- name: uterine-fibroid-classification-and-management
  display: 子宫肌瘤分类与管理
  trigger: 超声或MRI确诊子宫肌瘤后需制定管理策略时
  ref: uterine-fibroid-classification-and-management/SKILL.md

---

## 🦠 妇科感染与炎症 (9)

- name: acute-cervicitis-pathogen-directed-treatment
  display: 急性宫颈炎病原体导向治疗
  trigger: 性活跃育龄女性出现黏液脓性宫颈分泌物时
  ref: acute-cervicitis-pathogen-directed-treatment/SKILL.md

- name: pelvic-inflammatory-disease-diagnosis-cdc-2021
  display: 盆腔炎性疾病诊断（CDC 2021）
  trigger: 下腹痛且妇科检查发现宫颈举痛或附件压痛时
  ref: pelvic-inflammatory-disease-diagnosis-cdc-2021/SKILL.md

- name: pelvic-inflammatory-disease-infection-pathways
  display: 盆腔炎性疾病感染途径
  trigger: 疑似PID需明确感染来源时
  ref: pelvic-inflammatory-disease-infection-pathways/SKILL.md

- name: female-genital-tuberculosis-management
  display: 女性生殖器结核管理
  trigger: 表现为不孕、闭经、盆腔包块或疑似结核性病变时
  ref: female-genital-tuberculosis-management/SKILL.md

- name: genital-tuberculosis-transmission-assessment
  display: 生殖器结核传播途径评估
  trigger: 不孕、月经异常伴低热盗汗且有结核病史时
  ref: genital-tuberculosis-transmission-assessment/SKILL.md

- name: infant-vulvovaginitis-management
  display: 婴幼儿外阴阴道炎处理
  trigger: 5岁以下女童出现脓性阴道分泌物或外阴瘙痒时
  ref: infant-vulvovaginitis-management/SKILL.md

- name: condyloma-acuminatum-pregnancy-delivery-decision
  display: 尖锐湿疣妊娠分娩决策
  trigger: 孕妇确诊外阴尖锐湿疣且临近分娩时
  ref: condyloma-acuminatum-pregnancy-delivery-decision/SKILL.md

- name: chlamydia-trachomatis-pregnancy-neonatal-management
  display: 沙眼衣原体妊娠与新生儿管理
  trigger: 孕妇确诊沙眼衣原体感染或新生儿出现结膜炎/肺炎时
  ref: chlamydia-trachomatis-pregnancy-neonatal-management/SKILL.md

- name: hiv-pregnant-art-regimen-selection
  display: HIV孕妇ART方案选择
  trigger: 确诊HIV感染的围产期孕妇时
  ref: hiv-pregnant-art-regimen-selection/SKILL.md

---

## 🔵 外阴与阴道疾病 (7)

- name: vulvar-lichen-sclerosus-biopsy-indication
  display: 外阴硬化性苔藓活检指征
  trigger: 疑似VLS伴持续溃疡/糜烂或长期治疗无效时
  ref: vulvar-lichen-sclerosus-biopsy-indication/SKILL.md

- name: vulvar-lichen-sclerosus-corticosteroid-staged-treatment
  display: 外阴硬化性苔藓糖皮质激素分阶段治疗
  trigger: 确诊VLS且存在瘙痒、疼痛或皮肤角化症状时
  ref: vulvar-lichen-sclerosus-corticosteroid-staged-treatment/SKILL.md

- name: vulvar-lichen-sclerosus-vs-simplex-differentiation
  display: 外阴硬化性苔藓与慢性单纯性苔藓鉴别
  trigger: 外阴白色病变（瘙痒、皮肤颜色或质地改变）时
  ref: vulvar-lichen-sclerosus-vs-simplex-differentiation/SKILL.md

- name: vulvar-vaginal-sil-management
  display: 外阴/阴道鳞状上皮内病变管理
  trigger: 经活检确诊为VIN/VaIN时
  ref: vulvar-vaginal-sil-management/SKILL.md

- name: atrophic-vaginitis-diagnosis
  display: 萎缩性阴道炎诊断
  trigger: 绝经后/产后闭经女性阴道黏膜萎缩伴出血点时
  ref: atrophic-vaginitis-diagnosis/SKILL.md

- name: pathological-leucorrhea-type-identification
  display: 病理性白带类型识别
  trigger: 白带量、色、质或味异常已排除生理性变化时
  ref: pathological-leucorrhea-type-identification/SKILL.md

- name: yin-dao-liu-xue-lin-chuang-jian-bie
  display: 阴道出血临床鉴别
  trigger: 患者出现非月经期阴道流血时
  ref: yin-dao-liu-xue-lin-chuang-jian-bie/SKILL.md

---

## 🩺 盆底与泌尿妇科 (4)

- name: stress-urinary-incontinence-diagnosis
  display: 压力性尿失禁诊断流程
  trigger: 咳嗽/打喷嚏/运动时出现不自主漏尿时
  ref: stress-urinary-incontinence-diagnosis/SKILL.md

- name: pop-q-pelvic-organ-prolapse-staging
  display: POP-Q盆腔器官脱垂分度
  trigger: 下坠感、阴道肿物脱出且能配合Valsalva动作时
  ref: pop-q-pelvic-organ-prolapse-staging/SKILL.md

- name: urinary-fistula-diagnosis-and-differentiation
  display: 尿瘘诊断与鉴别
  trigger: 阴道无痛性持续流液且证实为尿液时
  ref: urinary-fistula-diagnosis-and-differentiation/SKILL.md

- name: shu-ruan-guan-tong-ye-shu-caozuo-yu-panduan
  display: 输卵管通液术操作与判断
  trigger: 男方精液正常且临床怀疑输卵管阻塞时
  ref: shu-ruan-guan-tong-ye-shu-caozuo-yu-panduan/SKILL.md

---

## 🌸 青春期、围绝经期与老年妇科 (5)

- name: pubertal-development-assessment
  display: 评估青春期发育阶段与进程
  trigger: 8～10岁女孩出现乳房发育、阴毛生长等线索时
  ref: pubertal-development-assessment/SKILL.md

- name: female-lifecycle-healthcare
  display: 女性全生命周期保健
  trigger: 需为不同年龄段女性提供预防性健康指导时
  ref: female-lifecycle-healthcare/SKILL.md

- name: perimenopausal-abnormal-uterine-bleeding-management
  display: 围绝经期异常子宫出血管理
  trigger: 绝经过渡期女性已排除妊娠和恶性病变时
  ref: perimenopausal-abnormal-uterine-bleeding-management/SKILL.md

- name: menopausal-hormone-therapy-indications-and-personalized-management
  display: 绝经激素治疗指征与个体化管理
  trigger: 年龄<60岁、绝经10年内、存在血管舒缩症状时
  ref: menopausal-hormone-therapy-indications-and-personalized-management/SKILL.md

- name: turner-syndrome-clinical-assessment-and-management
  display: Turner综合征评估与管理
  trigger: 身材矮小、蹼颈、原发性闭经及第二性征不发育时
  ref: turner-syndrome-clinical-assessment-and-management/SKILL.md

---

## 🧪 遗传、产前筛查与诊断 (11)

- name: prenatal-screening-for-aneuploidy
  display: 非整倍体产前筛查
  trigger: 妊娠11～24周需评估胎儿染色体异常风险时
  ref: prenatal-screening-for-aneuploidy/SKILL.md

- name: prenatal-diagnosis-disease-classification
  display: 产前诊断疾病分类
  trigger: 妊娠期有指征进行产前诊断时
  ref: prenatal-diagnosis-disease-classification/SKILL.md

- name: prenatal-serum-biochemical-screening
  display: 产前血清生化筛查
  trigger: 孕11~13⁺⁶周或15~20周需进行风险评估时
  ref: prenatal-serum-biochemical-screening/SKILL.md

- name: amniocentesis-standard-procedure
  display: 羊膜腔穿刺标准操作
  trigger: 妊娠≥15周有明确遗传学检查指征时
  ref: amniocentesis-standard-procedure/SKILL.md

- name: transabdominal-amniocentesis-procedure
  display: 经腹壁羊膜腔穿刺
  trigger: 孕周≥15周需进行产前诊断或宫内治疗时
  ref: transabdominal-amniocentesis-procedure/SKILL.md

- name: serum-hcg-reference-ranges
  display: 血清hCG参考范围
  trigger: 需确认妊娠、排查异位妊娠或监测hCG异常时
  ref: serum-hcg-reference-ranges/SKILL.md

- name: complete-vs-partial-molar-pregnancy-differentiation
  display: 完全性与部分性葡萄胎鉴别
  trigger: 妊娠组织呈水泡状且血清hCG异常升高时
  ref: complete-vs-partial-molar-pregnancy-differentiation/SKILL.md

- name: post-molar-evacuation-follow-up
  display: 葡萄胎清宫术后随访
  trigger: 葡萄胎清宫术后需hCG监测和随访时
  ref: post-molar-evacuation-follow-up/SKILL.md

- name: pregnancy-trophoblastic-tumor-diagnosis
  display: 妊娠滋养细胞肿瘤诊断
  trigger: 葡萄胎/流产后异常阴道流血且hCG异常升高时
  ref: pregnancy-trophoblastic-tumor-diagnosis/SKILL.md

- name: gestational-trophoblastic-neoplasia-stratified-therapy
  display: 妊娠滋养细胞肿瘤分层治疗
  trigger: 提供预后评分、分期及耐受性信息时
  ref: gestational-trophoblastic-neoplasia-stratified-therapy/SKILL.md

- name: genetic-counseling-ethical-principles
  display: 遗传咨询伦理原则
  trigger: 涉及遗传风险评估、遗传检测决策或家庭遗传病咨询时
  ref: genetic-counseling-ethical-principles/SKILL.md

---

## 💕 女性性健康与心理 (4)

- name: female-sexual-dysfunction-diagnosis
  display: 女性性功能障碍诊断
  trigger: 20-70岁性活跃女性报告性相关困扰且持续≥6个月时
  ref: female-sexual-dysfunction-diagnosis/SKILL.md

- name: female-sexual-dysfunction-comprehensive-treatment
  display: 女性性功能障碍综合治疗
  trigger: 已确诊FSD且症状产生心理痛苦或影响人际关系时
  ref: female-sexual-dysfunction-comprehensive-treatment/SKILL.md

- name: female-sexual-response-cycle-assessment
  display: 女性性反应周期评估
  trigger: 需识别性功能障碍具体阶段或开展性健康指导时
  ref: female-sexual-response-cycle-assessment/SKILL.md

- name: age-specific-sexual-health-education-framework
  display: 年龄分层性健康教育框架
  trigger: 需为特定年龄群体设计或评估性健康教育内容时
  ref: age-specific-sexual-health-education-framework/SKILL.md

---

## 🫀 解剖、生理与基础医学 (8)

- name: female-pelvic-anatomy-clinical-implications
  display: 女性盆腔解剖临床应用
  trigger: 处理盆腔疼痛、感染、肿块或计划盆腔手术时
  ref: female-pelvic-anatomy-clinical-implications/SKILL.md

- name: female-reproductive-organ-embryonic-development-pathway
  display: 女性生殖器官胚胎发育
  trigger: 需理解正常解剖结构形成或评估先天畸形时
  ref: female-reproductive-organ-embryonic-development-pathway/SKILL.md

- name: female-genital-lymphatic-drainage-pathways
  display: 女性生殖器淋巴引流途径
  trigger: 需指导手术清扫范围或影像学评估时
  ref: female-genital-lymphatic-drainage-pathways/SKILL.md

- name: placental-structure-and-fetoplacental-circulation
  display: 胎盘结构与胎儿-胎盘循环
  trigger: 涉及胎盘生理、妊娠并发症机制时
  ref: placental-structure-and-fetoplacental-circulation/SKILL.md

- name: placental-substance-transfer-mechanisms
  display: 胎盘物质转运机制
  trigger: 围产期用药评估、胎儿感染风险判断时
  ref: placental-substance-transfer-mechanisms/SKILL.md

- name: placental-hormone-function-assessment
  display: 胎盘激素功能评估与临床解读
  trigger: 评估胎盘内分泌功能或解释产前筛查指标异常时
  ref: placental-hormone-function-assessment/SKILL.md

- name: estrogen-hypothalamic-pituitary-feedback-regulation
  display: 雌激素下丘脑-垂体反馈调节
  trigger: 需解释排卵调控机制或预测排卵时机时
  ref: estrogen-hypothalamic-pituitary-feedback-regulation/SKILL.md

- name: gnrh-pulse-frequency-regulation-of-lh-fsh-ratio
  display: GnRH脉冲频率调节LH/FSH比值
  trigger: 提及GnRH脉冲模式或LH/FSH比值异常时
  ref: gnrh-pulse-frequency-regulation-of-lh-fsh-ratio/SKILL.md

---

## 🔪 手术与操作技术 (3)

- name: laparoscopic-tubal-sterilization
  display: 腹腔镜输卵管绝育术操作与并发症管理
  trigger: 咨询永久避孕手术方案或术式选择时
  ref: laparoscopic-tubal-sterilization/SKILL.md

- name: vacuum-aspiration-procedure
  display: 负压吸引术操作与并发症管理
  trigger: 宫内妊娠≤10周需终止妊娠时
  ref: vacuum-aspiration-procedure/SKILL.md

- name: hysteroscopic-distension-fluid-selection-and-tahss-prevention
  display: 宫腔镜膨宫液选择与TAHSS预防
  trigger: 使用电能量设备进行宫腔镜手术时
  ref: hysteroscopic-distension-fluid-selection-and-tahss-prevention/SKILL.md

---

## 📚 教学、资源与质控 (23)

- name: obstetrics-gynecology-textbook-10th-edition-structure
  display: 妇产科学第10版编撰团队结构
  trigger: 需引用教材、确认版权归属或学术溯源时
  ref: obstetrics-gynecology-textbook-10th-edition-structure/SKILL.md

- name: clinical-medicine-textbook-revision-principles
  display: 临床医学教材修订原则
  trigger: 医学教材编者需遵循第十轮修订核心原则时
  ref: clinical-medicine-textbook-revision-principles/SKILL.md

- name: evaluate-obstetrics-gynecology-textbook-editor-authority
  display: 妇产科学教材主编权威性评估
  trigger: 需判断该教材主编是否具备国家级学术权威性时
  ref: evaluate-obstetrics-gynecology-textbook-editor-authority/SKILL.md

- name: access-digital-resources-for-medical-textbooks
  display: 医学教材数字资源获取
  trigger: 持有带激活码的纸质教材需访问数字内容时
  ref: access-digital-resources-for-medical-textbooks/SKILL.md

- name: maternal-death-and-near-miss-review-system
  display: 孕产妇死亡/危重症评审体系
  trigger: 孕产妇死亡或出现WHO定义的危重症指标时
  ref: maternal-death-and-near-miss-review-system/SKILL.md

- name: maternal-and-child-health-statistical-indicators
  display: 妇幼保健统计指标
  trigger: 需计算标准化妇幼保健核心绩效指标时
  ref: maternal-and-child-health-statistical-indicators/SKILL.md

- name: ru-fang-nong-zhong-fang-she-zhuang-qie-kou-yuan-ze
  display: 乳房脓肿放射状切口原则
  trigger: 确诊哺乳期女性乳房脓肿需手术引流时
  ref: ru-fang-nong-zhong-fang-she-zhuang-qie-kou-yuan-ze/SKILL.md

- name: zi-gong-ren-dai-jie-gou-yu-gong-neng
  display: 子宫韧带结构与功能
  trigger: 涉及盆底支持结构或广泛子宫切除术术前规划时
  ref: zi-gong-ren-dai-jie-gou-yu-gong-neng/SKILL.md

- name: geng-zu-xing-sheng-zhi-dao-ji-xing-chu-li
  display: 梗阻性生殖道畸形处理
  trigger: 原发性闭经伴周期性下腹痛且影像学证实生殖道积血时
  ref: geng-zu-xing-sheng-zhi-dao-ji-xing-chu-li/SKILL.md

- name: wu-pai-luan-xing-aub-ji-su-zhi-xue-ce-lve
  display: 无排卵性AUB激素止血策略
  trigger: 无排卵性异常子宫出血需药物干预止血时
  ref: wu-pai-luan-xing-aub-ji-su-zhi-xue-ce-lve/SKILL.md

- name: wu-pai-luan-xing-aub-chu-xue-ji-zhi-fen-xi
  display: 无排卵性AUB出血机制分析
  trigger: 临床表现提示无排卵性AUB且已排除器质性病变时
  ref: wu-pai-luan-xing-aub-chu-xue-ji-zhi-fen-xi/SKILL.md

- name: ca125-ovarian-cancer-clinical-application
  display: CA125卵巢癌临床应用
  trigger: 面对绝经后女性或卵巢上皮性肿瘤患者需评估时
  ref: ca125-ovarian-cancer-clinical-application/SKILL.md

- name: barrier-contraception-usage-and-effectiveness
  display: 屏障避孕方法使用与效果
  trigger: 需同时实现避孕和预防性传播疾病时
  ref: barrier-contraception-usage-and-effectiveness/SKILL.md

- name: cervical-sample-collection-and-satisfaction-evaluation
  display: 宫颈标本采集与满意度评价
  trigger: 需进行子宫颈癌筛查且无禁忌证时
  ref: cervical-sample-collection-and-satisfaction-evaluation/SKILL.md

- name: cervical-sil-classification-with-p16
  display: 宫颈SIL分类与P16判读
  trigger: CIN2形态学难以明确区分LSIL或HSIL时
  ref: cervical-sil-classification-with-p16/SKILL.md

- name: cervical-intraepithelial-neoplasia-risk-stratification
  display: 宫颈上皮内病变风险分层
  trigger: 未治疗的宫颈上皮内病变需制定随访或治疗策略时
  ref: cervical-intraepithelial-neoplasia-risk-stratification/SKILL.md

- name: ogtt-insulin-release-test-interpretation
  display: OGTT联合胰岛素释放试验判读
  trigger: 需评估糖尿病/PCOS患者胰岛β细胞功能时
  ref: ogtt-insulin-release-test-interpretation/SKILL.md

- name: benign-ovarian-tumor-surgical-timing
  display: 良性卵巢肿瘤手术时机
  trigger: 妊娠期诊断为良性卵巢肿瘤且无并发症时
  ref: benign-ovarian-tumor-surgical-timing/SKILL.md

- name: ovarian-cyst-vs-ascites-differentiation
  display: 卵巢囊肿与腹水鉴别
  trigger: 腹部膨隆需鉴别巨大卵巢囊肿与腹腔积液时
  ref: ovarian-cyst-vs-ascites-differentiation/SKILL.md

- name: adoptive-cell-therapy-in-gynecologic-cancers
  display: 妇科肿瘤过继性细胞治疗
  trigger: 复发/难治性妇科肿瘤患者表达特定靶抗原时
  ref: adoptive-cell-therapy-in-gynecologic-cancers/SKILL.md

- name: gynecological-exam-preparation-and-contraindications
  display: 妇科检查准备与禁忌证
  trigger: 需执行或指导妇科检查时
  ref: gynecological-exam-preparation-and-contraindications/SKILL.md

- name: neonatal-asphyxia-diagnostic-criteria
  display: 新生儿窒息联合诊断标准
  trigger: 新生儿Apgar评分≤7且脐动脉血气pH<7.15时
  ref: neonatal-asphyxia-diagnostic-criteria/SKILL.md

- name: qian-bu-jun-qing-wei-shi-bie-yu-chu-li
  display: 前不均倾位识别与处理
  trigger: 阴道检查发现胎头矢状缝后移、前顶骨嵌顿时
  ref: qian-bu-jun-qing-wei-shi-bie-yu-chu-li/SKILL.md
