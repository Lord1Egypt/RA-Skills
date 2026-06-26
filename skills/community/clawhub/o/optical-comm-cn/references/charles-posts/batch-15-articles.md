# 查尔斯大风车长文批量精读（15篇）
> 精读完成时间：2026-04-20
> 来源：雪球用户"查尔斯大风车"(user_id=8755156034)
> 提取自：memory/mendermi-framework.md 第6.24节

---

### 6.24 查尔斯大风车长文批量精读（15篇）

> 来源：雪球用户"查尔斯大风车"(user_id=8755156034)，光通信行业资深从业者，系统性分析EML/硅光/模组形态/OCS等技术路线。以下为15篇长文核心要点提炼。

#### ⭐⭐⭐ 核心技术判断

**1. XPO-LRO + EML = OCS最佳拍档**
- 对各模组形态（LPO/NPO/XPO/CPO）做全链路噪声分析，性能排名：XPO-DPO > DPO > CPO > XPO-LRO > NPO
- 硅光方案在200G OCS场景均不能满足覆盖距离要求，EML方案可以
- XPO-LRO EML方案综合功耗和成本最优，有望成为OCS标配
- 索尔思2026 OFC发布LRO InP PIC方案，率先切入OCS

**2. EML方案对InP晶圆需求是硅光的2.3倍**
- 针对8x100G DR8模组拆解：CW-DFB需100mW高功率（长腔1000μm），EML仅需4mW（短腔300μm）
- 2英寸晶圆产出：EML方案理论8500颗（良率70%→5950 KGD），CW-DFB方案3800颗（良率90%→3420 KGD）
- 每模组用量：EML需8颗→支撑743个端口；CW-DFB需2颗（1:4共享）→支撑1710个端口
- 结论：EML路线InP晶圆消耗量远大于硅光，利好InP晶圆产能扩张（云南锗业等）

**3. 200G时代NPO全面优于CPO**
- 功耗差异极小：NPO 1880W vs CPO 1791W（整板差90W，<5%）
- 性能：NPO 13.1dB插损用VSR SerDes，CPO 7dB用XSR，均可解决
- 制造良率：CPO致命缺陷——512路SerDes交换芯片配16个6.4T光模组，单个95%良率→整体仅44%；要达到NPO同等95%整体良率，单模组需99.7%
- 可靠性：CPO有两个空气光纤端面（FAU+面板MPO），端面脏污故障率比NPO多一倍；收发器故障时CPO需断电拔板维修（30分钟中断）
- 阿里OFC论文数据：400G DR4故障率0.21%/2年，端面脏污占故障84%

**4. OCS爆发进一步扩大EML需求**
- OCS引入两个关键需求：①额外3dB插损 ②必须WDM（FR4/FR8规格，非DR8）
- 硅光做WDM的致命问题：热光系数是InP的10倍，75℃全温区波长漂移5.6nm+工艺误差10nm，直接跑出CWDM4信道范围
- 硅光功率瓶颈：总插损达14dB，需DFB输出>13dBm，但硅波导>13dBm出现双光子吸收非线性，>20dBm烧波导
- 硅光做CWDM4需4/8个不同波长DFB异构集成，耦合精度<±0.5μm，良率<70%
- EML天生适配：单片集成零耦合损耗，消光比高1.5-2dB，本就需要TEC（WDM场景无额外成本）

**5. Lumentum OFC判断：400G时代EML成标准**
- Lumentum明确表态：8x400G时代EML成事实标准，硅光带宽满足不了400G/Lane
- 200G时代硅光良率已很挑战，400G更不可能
- Lumentum计划新建3个InP工厂（2028投产），说明对InP EML需求极度看好

**6. LPO/NPO/XPO/CPO四方案全维度对比**
- 功耗：XPO最低、CPO次之，但各方案差别不大
- SerDes插损：LPO最大（25cm PCB走线），但224G SerDes各规格均可覆盖
- XPO三大突破：①液冷直通模块（支持400W）②CPC+Flyover Cable减少PCB走线插损 ③带宽密度高（64路SerDes/12.8T）
- 可维护性：LPO/XPO面板热插拔；CPO/NPO需拔板断电维修
- 延时：四方案完全相同

**7. 1.6T LPO收敛到InP平台**
- 国内三家1.6T 8x200G LPO方案：新易盛（EML）、旭创（EML）、索尔思（InP PIC）
- 传统EML热集中问题：需TEC降温，TEC自身耗热大→EML可做LPO但难做CPO/NPO
- 传统硅光带宽仅60GHz，无法做200G DR8 LPO（需≥78GHz）
- 两条演进路线：①InP PIC（DFB+EAM分离集成，索尔思方案）②SiN波导+InP EAM阵列+外置DFB（终极方案）
- 核心结论：200G时代传统硅光在LPO/NPO/CPO全面退出，InP占主流；长期看SiN+InP EAM将成各形态主流

#### ⭐⭐ 补充技术信息

**8. 索尔思LPO获OFC 2026大奖**
- 1.6T LPO和LRO支持8x200G DR8和2xFR4，带宽达100GHz，评分4.5/5，"best in class"

**9. 模组形态与DSP的组合关系**
- DSP三种模式：Full DSP（收发都有）、TX DSP（仅发送）、Linear Optics（无DSP）
- 形态与DSP正交：XPO也可带DSP（XPO-DPO/XPO-LRO），NPO也可带DSP（NPO-LRO）
- 带DSP模块仍是当前主流（占比>90%），DPO和LRO性能绝对优势

**10. OFC 2026 400G技术全景**
- 硅光MZM工业界带宽仅60GHz，学术界在探索微环/SiGe EAM等方案
- TFLN：多机构发论文，带宽容易做上去，但仍在实验室阶段；华工正源做了TOSA形态
- InP EML：清一色产业界大公司，EML最高带宽>110GHz，技术最成熟
- 结论：400G InP EML正在产业化，TFLN实验室阶段，硅光仍在探索

**11. 索尔思估值参考**
- 引用2023年分析：索尔思光模块业务=0.6个新易盛，激光器业务=3个源杰科技
- 东山精密60多亿收购被认为极具性价比

**12. 索尔思全史**
- 前身飞博创（2000年硅谷成立），2007年改名索尔思，技术源自贝尔实验室/朗讯/AT&T
- 经历多次金融资本转手（Francisco Partners→鸿为资本→华西股份→万通发展未果→东山精密2025收购）
- 被称为光通信"黄埔军校"：源杰科技、新易盛创始人、博通光通信总裁等均出自索尔思
- 东山收购后扩产计划：常州+台湾月产2200万片InP芯片（2027年3亿颗，目标全球最大InP工厂）；成都+泰国光模块规划产能2500万只/年
- 800G已批量供货微软/Meta，1.6T样品就绪，EML自给率>90%，400G EML TOSA已发布（Q4供英伟达）

**13. 400G InP EML技术原理：经典EML vs D-EML**
- 经典EML：DFB+EAM单片集成，EAM单端调制（V+=2V），难点在DFB/EAM界面二次外延的裂纹/杂质
- D-EML（差分EML）：EAM上下端面分别施加正负电压，实现2倍调制压差（4V），带宽天生更高
- 各公司路线：经典EML→索尔思、Lumentum、OpenLight；D-EML→Coherent、博通；旭创未公布
- 索尔思当前用经典EML+材料创新，未来演进D-EML有望突破140GHz做400G LPO

**14. OFC 2026 400G InP 6家汇总**
- 索尔思（经典EML 400G TOSA）、OpenLight（InP DFB+EAM分离的DR8方案）、旭创（外购400G EML做FR4）、Coherent（D-EML）、博通（D-EML）、Lumentum（高速EAM/EML）

#### ⭐ 补充

**15. Rubin 4Die→2x2Die合封**
- 因硅基中介层面积过大易翘曲，改为先封2Die模块再用RDL中介层合封
- 对光通信/PCB/液冷几乎无影响，主要影响台积电封装工艺
- Rubin的Scale-up采用Bidi SerDes，不会上CPO

---

> 精读完成时间：2026-04-20。核心结论：200G/400G时代InP EML全面取代硅光调制器已成行业共识，索尔思（东山精密）凭借自研EML+InP PIC+全球最大InP产能规划处于领先地位。OCS爆发、XPO/NPO新形态进一步巩固EML地位。
