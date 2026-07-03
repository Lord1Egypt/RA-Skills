# Industry Solution Quick Reference

> This document provides core IT consulting focus areas for 6 major industries, enabling quick identification of industry-specific issues and solution directions.

---

## 1. Financial Services (Banking / Insurance / Securities)

### Core Industry Challenges
- Legacy core systems: Mainframe/Cobol, high maintenance costs, talent gap
- Regulatory compliance pressure: Basel IV/DORA/China CBIRC & PBOC & CAC
- Open finance: API economy, embedded finance, ecosystem competition
- Extremely high security requirements: Zero tolerance, real-time risk control

### IT Consulting Focus Areas
| Area | Typical Problem | Solution Direction |
|------|---------|-------------|
| Core Banking Modernization | Mainframe→Cloud-native, how to migrate without data loss | Strangler Fig pattern, gradual replacement |
| Real-Time Risk Control | Millisecond-level anti-fraud/anti-money laundering | Stream computing + AI + Graph database |
| Intelligent Customer Service | High customer service volume, high standardization | NLP+RAG+Agent, automation rate 70-90% |
| Open Banking | API standardization / security / governance | API Gateway + OAuth2.0 + Developer Portal |
| RegTech | Manual regulatory reporting, high error rate | Automated data collection + AI audit + real-time compliance monitoring |

### Key Metrics
- Core system availability > 99.99%
- Transaction processing latency < 50ms (P99)
- Real-time risk control false positive rate < 5%
- Regulatory report automation rate > 90%

---

## 2. Manufacturing / Industry 4.0

### Core Industry Challenges
- OT/IT Convergence: Data silos between industrial control systems and IT systems
- Poor production visibility: Don't know when machines will stop
- Supply chain resilience: Global supply chain volatility
- Product homogenization: Transition from selling products → selling services

### IT Consulting Focus Areas
| Area | Typical Problem | Solution Direction |
|------|---------|-------------|
| Industrial Internet | Equipment data collection / diverse protocols | IIoT Platform + Edge Computing + Data Standardization |
| Predictive Maintenance | High scheduled maintenance costs / unexpected downtime | IoT Sensors + ML Time-Series Prediction |
| Digital Twin | Design-Production-Operations data disconnected | Unified Data Platform + 3D Modeling + Simulation |
| Smart Manufacturing | MES/WMS/SCADA each separate, data disconnected | Unified Manufacturing Data Platform + API Integration Layer |
| Supply Chain Digital Twin | Don't know where supply chain breaks / how large the impact | Supply Chain Visualization + AI Prediction + What-If Simulation |

### Key Metrics
- OEE improvement > 15%
- Unplanned downtime reduction > 30%
- Quality defect rate reduction > 25%

---

## 3. Retail & Consumer Goods

### IT Consulting Focus Areas
| Area | Typical Problem | Solution Direction |
|------|---------|-------------|
| Omnichannel Middle Platform | Online/offline/distribution data fragmented | OMS+CRM+CDP+Loyalty Middle Platform |
| AI Precision Marketing | Marketing ROI unclear | CDP+AI Recommendation+Dynamic Pricing |
| Intelligent Supply Chain | High inventory but also high stockout rate | Demand Forecasting AI + Intelligent Replenishment + Warehouse Automation |
| Store Digitalization | No data on store traffic / conversion | IoT+CV+Smart Shopping Assistant |
| Private Domain Operations | Expensive public domain traffic, poor private domain conversion | WeCom + Mini Program + SCRM |

### Key Metrics
- Online conversion rate improvement > 20%
- Inventory turnover days reduction > 15%
- Marketing ROI improvement > 30%

---

## 4. Healthcare

### IT Consulting Focus Areas
| Area | Typical Problem | Solution Direction |
|------|---------|-------------|
| Hospital Informatization | HIS/CIS/LIS/PACS each separate, not interconnected | ESB Integration Bus + HL7/FHIR Standards |
| Internet Hospital | Online consultation / prescription / payment integration | Microservice Architecture + Security Compliance |
| AI-Assisted Diagnosis | Heavy imaging/pathology doctor workload | AI Medical Imaging + CDSS |
| Data Compliance | Health data is sensitive personal information | Classification + De-identification + Audit Trail |
| Interoperability | Medical records not shared across hospitals | Interoperability Maturity Assessment (V4/V5) + Platform Construction |

---

## 5. Government & Public Services

### Policy Background: Digital China 2025
- "Data Element ×" Three-Year Action Plan: Data assets recognized on balance sheets
- Xinchuang Substitution: 2027 full-stack replacement of core systems for Party & government + central SOEs
- National Integrated Government Big Data System: Initially established by 2025
- Three Major Projects: One-stop government services / Unified urban governance / Integrated government collaboration

### IT Consulting Focus Areas
| Area | Typical Problem | Solution Direction |
|------|---------|-------------|
| Digital Government | Departments build systems independently | Government Cloud / Big Data Platform / Unified Identity Authentication |
| One-Stop Government Services | Citizens need to visit multiple offices | Business Process Reengineering + Data Sharing + Electronic Certificates |
| Smart City | Siloed construction, data disconnected | City Brain + IOC + Data Middle Platform |
| Xinchuang Substitution | Foreign products have security risks | Full-stack localization of CPU/OS/DB/Middleware/Applications |
| Government AI | Low approval efficiency | Intelligent Approval / Policy Simulation / Urban Governance AI |
| Xinchuang Substitution | Foreign product security risks + compliance risks | Full-stack localization + Zone-based batch rollout + Dual-track operation |
| Data Asset Recognition | Data value cannot be reflected | Rights confirmation → Valuation → Balance sheet recognition → Trading |

---

## 6. Energy & Utilities

### IT Consulting Focus Areas
| Area | Typical Problem | Solution Direction |
|------|---------|-------------|
| Smart Grid | Distributed energy grid integration management | Energy IoT Platform + AI Dispatch |
| Carbon Management | ESG compliance / carbon trading needs | Carbon Emission Data Collection + MRV + Trading Platform |
| New Energy O&M | Wind/solar scattered, low O&M efficiency | Digital Twin + Predictive Maintenance + Drone Inspection |
| OT Security | Weak industrial control system security protection | OT/IT Security Integration (Classified Protection + Industry Standards) |
| Integrated Energy Services | Energy sales → Integrated service transformation | Digital Service Platform + AI Energy Efficiency Optimization |


---
## 7. Digital Native / Internet Enterprises

### IT Consulting Focus Areas
| Area | Typical Problem | Solution |
|------|---------|---------|
| Technology Stack Modernization | Multiple generations of tech stacks coexist | Standardization + Incremental Refactoring + API-fication |
| AI Infrastructure | Low GPU utilization | Model Routing + GPU Pooling + Inference Optimization |
| Data Compliance | Personal information protection + Cross-border data transfer | Classification + Cross-border Compliance + Privacy Computing |
| Engineering Efficiency | R&D efficiency bottleneck | DORA + Platform Engineering + AI-Assisted Development |

---
## 8. Central SOEs Digital Transformation

### IT Consulting Focus Areas
| Area | Typical Problem | Solution |
|------|---------|---------|
| Top-Level Design | Lack of systematic planning | Five-Force Diagnosis + Eight-Step Advancement + Benchmarking against world-class |
| Xinchuang Adaptation | Full-stack replacement of business systems | Zone-based batch rollout + Dual-track operation + Adaptation verification |
| Data Assetization | Abundant resources but not monetized | Rights confirmation + Valuation + Balance sheet recognition + Trading |
| Control Efficiency | Group control vs subsidiary flexibility | Strategic / Financial / Operational control models