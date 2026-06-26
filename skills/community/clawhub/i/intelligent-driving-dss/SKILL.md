---
name: intelligent-driving-dss
description: 智能驾驶决策支持系统 - 基于 L2 到 L5 级别的自动化和主动风险预测模型，提供实时路况下的情景压力测试、多传感器融合分析及高精度风险预警。集成中国道路交通安全法核心规则与新能源车型数据库。使用场景：自动驾驶算法设计、交通工程模拟、高级辅助驾驶功能评估、极端天气工况决策等。
author: mikewongonline
metadata:
  openclaw:
    emoji: 🤖
    requires:
      bins: []
---

# 智能驾驶决策支持系统 (Intelligent Driving DSS)

## 🎯 Core Objectives
Evolve from a simple Q&A tool into a complete, iterative **task execution agent**, whose outputs must include: **[Identify Target] → [Analyze Risk] → [Propose Optimal Decision] → [Warning & Self-Check Report]**.

**Legal Basis:** This system is built on the "Road Traffic Safety Law of the People's Republic of China" (3rd Revision, 2021) decision logic to ensure all traffic behaviors comply with Chinese laws and regulations.

## 📊 **当前任务状态一览（2026-05-15）**

| Agent Name | Current Status/Progress | ✅ Milestone Achieved | 🚧 Next Action |
|-----------|--------------|-----------------------------------|----------------------------------|
| **🚦法规合规专家** | ✅ **已完成** | 1. 资料汇编与骨架搭建完毕<br>2. 关键违章行为标准定义已建立<br>3. 具备"法规检查"初级校验能力<br>4. **新增：** 修法草案对比分析框架（对接 2026 年度立法计划） | 📌 待定：将最新的修法草案与现有规则进行比对，找出冲突点和新增要求（待公安部正式发布修订草案全文后自动触发） |
| **⚡新能源动力系统工程师** | ✅✅✅ **已完成并升级** | 1. BMS 核心概念已定义<br>2. **能耗模型动态化升级完成**（已将坡度、载重、环境温度作为输入变量）<br>3. 电量 ↔ 行驶距离约束关系建立 | 🎯 无新增待办任务（能耗计算模块已完善） |
| **🚗市场分析与对比师** | ✅✅✅ **已完成并升级** | 1. 数据采集初步完成<br>2. 定义了"配置标准化"、"价格区间"和"性价比评分体系"<br>3. 构建了结构化的数据表单模板<br>4. **新增：** 行业通用趋势提炼（动力总成格局/价格分层规律/用户偏好迁移） | 🎯 无新增待办任务（已实现从离散数据库到通用规律的升华） |

---

## 📚 **知识库模块 (The Knowledge Base)**
### **1. Chinese Traffic Law Core Library (`core-traffic-rules`)**
**法律依据：** 《中华人民共和国道路交通安全法》及其实施条例

#### **✅ Completed Files List (Total 10 files):**
- `README.md` - 模块总览与使用指南
- `general-principles.md` - Chapter 1: Legislative Purpose, Scope of Application, Management Responsibilities
- `vehicle-and-driver.md` - Chapter 2: Vehicle Registration Inspection, Driver's License System (including drink-driving penalties)
- `road-passage-conditions.md` - Chapter 3: Traffic Signals, Signs, Markings, Safety Facilities
- `road-passage-regulations.md` - **Chapter 4 Focus**: Motor Vehicle/Non-motor Vehicle/Pedestrian Traffic Rules (Core Application)
- `traffic-accident-handling.md` - Chapter 5: Accident Reporting, Liability Determination, Compensation Principles
- `law-enforcement-supervision.md` - Chapter 6: Traffic Police Team Building, Penalty Collection Separation System
- `legal-responsibility.md` - **Chapter 7 Focus**: Penalties for Various Violations (drink-driving/running red lights/fleeing after accident, etc.)
- `supplementary-provisions.md` - Chapter 8: Legal Term Definitions, Revision History
- `revision-draft-comparison.md` - **⚠️ NEW**: Framework for comparing and analyzing the revision draft of the Legislative Plan for 2026

#### **🔬 法规检查能力：**
- ✅ 超速认定标准（高速公路≥130km/h、城市道路≥50km/h）
- ✅ 闯红灯/不礼让行人责任划分（机动车负全责或主要责任）
- ✅ 酒驾分级处罚（饮酒→吊销→终生禁驾的阶梯机制）
- ⏳ **修法比对能力：** 待 2026 年修订草案发布后自动激活

---

### **2. NEV System Module (`nev-system-module`)**
**适用对象：** BEV（纯电）、PHEV（插电混动）、HEV（普通混动）、FCEV（燃料电池）

#### **✅ Completed Files List (Total 9 files):**
- `README.md` - Module overview and API examples
- `concept-definition.md` - Core Terminology: BEV/PHEV/FCEV/HEV, BMS/OBC/DC-DC/VCU
- `data-structure.json` - Standard data models (VehicleNEV/BatteryStatus/ChargingStation/MarketComparison) + API specifications
- `market-comparison-module.md` - Model Selection, Market Positioning Analysis, Competitive Advantage Matrix
- `energy-management.md` - Power Distribution Strategy, Energy Recovery Optimization, Thermal Management
- `charging-management.md` - Smart Charging Planning, Charging Station Type Adaptation, Cost Optimization Algorithms
- `safety-monitoring.md` - Battery Health Management, Thermal Runaway Warning, High Voltage System Protection
- `energy-consumption-calculation.md` - **⚠️ NEW**: Dynamic model with external factors (gradient/load/temp), supports accurate range prediction
- `industry-trends.md` - **Industry Trend Analysis**: Powertrain popularity trends, price segmentation, value scoring system, market landscape by tier

#### **📈 行业趋势提炼：**
- ✅ 动力总成组合受欢迎度趋势（BEV 主导 → PHEV 下滑 → HEV/FCEV 边缘化）
- ✅ 价格区间分布规律（经济型→入门级→中端级→高端旗舰的 4 层结构）
- ✅ 配置标准化与性价比评分体系（安全>智能>舒适的三级优先级）
- ✅ 热门车型市场格局（经济型 SUV/B 级轿车/MPV 细分赛道分析）

#### **🚀 核心升级点：**
1. **能耗模型动态化**：将坡度、载重、环境温度作为输入变量，使计算结果更贴近真实场景。
2. **行业规律提炼**：从离散数据中发现市场通用规律（如 BEV 占比超 85%、用户偏好向智能化迁移）。

---

## ⚙️ **核心功能模块 (The DSS Engine)**

### **1. 法规合规专家模式**
*   **输入：** "分析酒驾处罚标准"或"闯红灯的法律责任是什么？"
*   **输出：** 基于现行法律条文+修法草案跟踪（待发布）的权威回答。

### **2. 新能源查询接口（NEV Query Interface）**
*   **功能：** 提供车辆类型识别、市场对比、能耗预测等增值服务。
*   **数据结构：** 遵循 GB/T 32960 协议，支持 VIN、功率、能耗等多维度查询。
*   **动态计算能力：** 坡度/载重/温度修正模型已集成至能耗算法。

### **3. 情景压力测试模块（Scenario Stress Test）**
*   **流程：** 用户输入"极难"的场景描述 → 输出决策树（检测→预测→决策）
*   **应用场景：** "暴雨天气，前方施工工人突然横穿马路，AI 系统如何决策？"

### **4. 主动风险指数警报系统**
*   **输出格式：** `[风险等级] → [原因分析] → [建议修正值]`
*   **示例：** "⚠️【预警指数：橙色（中等偏高）】- *【根因】* 视觉信息受限（雨雾），路面湿滑系数升高，当前车速超出安全冗余范围。✅ **建议修正值**：立即将减速度提高 15%，并保持与前车的最小跟车距离。"

### **5. 系统自检报告**
*   每次决策后输出"数据源确认 + 不确定性提示"，保持决策透明度。

### **6. 合规审查专家模式 (新增)**
*   **输入：** "检查该车型是否符合 GB 38031-2020 安全规范"
*   **输出：** 基于《电动汽车用动力蓄电池安全规范》逐项核查（碰撞后防护时间、电池包防水等级、热失控预警机制）。
*   **法规依据：** GB 38031-2020《电动汽车用动力蓄电池安全规范》+ GB/T 32960-2016《电动汽车远程服务与管理系统技术规范》

---

## 💡 **使用指南与最佳实践**

### **场景 1：交通法规咨询**
- **用户输入：** "酒驾 200mg/100ml 的处罚是什么？"
- **系统响应：** 引用《道路交通安全法》第 91 条 + 刑法修正案（十一）危险驾驶罪条款，给出完整法律解读。

### **场景 2：新能源车型对比**
- **用户输入：** "帮我对比一下极氪 001 和小米 SU7"
- **系统响应：** 调用市场对比模块，输出优劣势分析矩阵（性能/智能/价格等维度）。

### **场景 3：能耗精准预测**
- **用户输入：** "从北京到天津，满载 5 人，爬山路段平均坡度 2%，环境温度 -5°C，预测续航多少？"
- **系统响应：** 调用能耗计算模型，输出动态修正后的实际续航数据（而非 WLTP 基准值）。

### **场景 4：法规合规检查**
- **用户输入：** "这辆车是否符合最新的电动车安全标准？"
- **系统响应：** 基于 GB 38031-2020《电动汽车用动力蓄电池安全规范》逐项核查（碰撞后防护时间、电池包防水等级、热失控预警机制）。

---

## 📋 **查询使用指南**

#### **场景 A：法规合规性审查**
```
✅ 适用案例："帮我检查这辆车是否符合最新的电动车安全标准"
    → 调用 GB 38031-2020 逐项核查
    → 输出：碰撞后防护时间 + 防水等级 + 热失控预警机制
```

#### **场景 B：能耗计算与续航预测**
```
✅ 适用案例："从珠海到广州，高速路段平均车速 100km/h，环境温度 28°C，预估能耗多少？"
    → 调用动态修正模型（坡度/载重/温度因素）
    → 输出：预计总能耗 + WLTP 基准对比
```

#### **场景 C：车型市场对比分析**
```
✅ 适用案例："帮我对比一下极氪 001 和小米 SU7"
    → 调用市场对比模块（性能/智能/价格等维度）
    → 输出：优劣势分析矩阵
```

#### **场景 D：法规条文查询**
```
✅ 适用案例："酒驾 200mg/100ml 的处罚是什么？"
    → 引用《道路交通安全法》第 91 条 + 刑法修正案（十一）危险驾驶罪条款
    → 输出：完整法律解读
```

---

## 📈 **技能升级里程碑（截至 2026-05-17）**

| 维度 | 完成度 | 说明 |
|------|--------|------|
| **法规合规能力** | ✅✅✅ 95% | 现行法律框架完善，修法草案比对待正式发布后自动激活，新增合规审查流程 |
| **新能源系统分析** | ✅✅✅ 100% | 概念定义→能耗模型→市场对比全部完成，外部因素动态化已实现 |
| **场景测试能力** | ✅✅✅ 95% | L2-L3 级自动驾驶规则覆盖完整，L4-L5 级需等待法规更新 |
| **数据分析深度** | ✅✅✅ 85% | 已从"数据汇总"升级到"趋势提炼 + 规律抽象" |

---

*本技能致力于将交通规则从静态的"法律知识"，升级为动态的"生存决策模型"，同时集成新能源车型数据库支持智能驾驶决策优化。*

## ⚖️ **合规审查与免责声明（新增）**

### **1. 法规审查范围**

| 法规标准 | 版本状态 | 审查维度 |
|----------|---------|----------|
| GB 38031-2020 | ✅ 现行有效 | 碰撞后防护时间、电池包防水等级、热失控预警机制 |
| GB/T 32960-2016 | ✅ 现行有效 | 远程服务与管理系统技术规范、车载通信协议 |
| 《道路交通安全法》 | ✅ 2021 年第三次修正版 | 酒驾/超速/闯红灯等核心规则 |
| **《道路交通运输管理条例（修法草案）** | ⏳ 待正式发布 | **冲突点分析 + 新增要求对比**（需公安部正式公布后自动触发） |

### **2. 合规审查流程（新增）**

```
步骤 1：用户输入车型/场景 → 系统识别需求
     ↓
步骤 2：调用知识库模块检索相关法规条款
     ↓
步骤 3：逐项核对 GB 38031-2020 安全规范（碰撞防护/防水等级/热失控预警）
     ↓
步骤 4：生成合规性报告 + 不确定性提示
     ↓
步骤 5：输出数据源确认（法规版本 + 数据截止时间）
```

### **3. 使用免责声明（重要）**

> ⚠️ **声明：** 本技能的所有分析结果、决策建议仅基于公开法律法规及数据库信息进行整理，不构成任何具有法律效力的意见或承诺。以下事项需特别注意：
>
> - **非法律效力文件**：所有法规解读仅供参考，最终解释权归国家主管部门所有
> - **数据时效性风险**：法规更新可能滞后于实际执行情况，建议以官方最新发布为准
> - **个性化场景差异**：系统输出结果基于通用模型推导，具体案件需结合实际情况评估
> - **专业咨询必要性**：涉及重大决策（如车辆购置、事故处理等），建议咨询专业人士或律师
>
> 本系统严格遵循以下安全边界：
> - ✅ 读取/搜索类操作直接执行（不涉及敏感信息）
> - ❌ 禁止自动执行任何外部付费服务或金融交易
> - ⚠️ Private Data Access 需用户明确授权
> - ⚠️ External Actions (Email/Social) 需获得批准
