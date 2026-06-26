# 组织学与胚胎学 Histology-Embryology-PMPH-10edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《组织学与胚胎学》第10版的技能手册 — 124 项核心形态学与胚胎学技能
<br>
<br>
<img src="/assets/Histology-Embyology.png" width="260px">
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages / Другие языки:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合组织学、胚胎学及先天畸形等核心领域，涵盖 **124 项关键技能**，分为组织学基础、上皮与屏障、结缔组织、肌与神经、循环淋巴、血液免疫、内分泌、生殖、泌尿、消化、呼吸、感觉器官、胚胎发育、先天畸形、特殊主题等分类。

**适用人群**：医学生、组织学教师、研究人员、临床医师

**参考教材**：人民卫生出版社《组织学与胚胎学》第 10 版

**⚠️风险⚠️**：该技能涵盖组织学结构识别、胚胎发育机制、先天畸形分类及临床病理关联，这些内容可能被误用为独立的医疗建议。

缓解措施：仅将输出作为教育或临床医师审核的参考资料使用，并根据当前官方指南、本地方案和合格专家核实建议。

## 项目结构

```
Histology-Embryology-PMPH-10edition/
├── SKILL.md              # 核心配置 — 124 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（使用时机、执行步骤、参考文档）
├── scripts/              # 可执行工具脚本
├── config/               # 配置文件
├── tests/                # 验证与测试
└── assets/               # 项目资源文件
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🔬 组织学基础与技术方法 | 11 | 显微镜技术、染色方法、教材评估等 |
| 🧱 上皮组织与屏障功能 | 13 | 紧密连接、滤过屏障、血-脑/胸腺屏障等 |
| 🧶 结缔组织与细胞外基质 | 5 | ECM整合、成纤维细胞、分子筛等 |
| 💪 肌肉与神经组织 | 13 | 肌纤维类型、突触传导、轴突运输等 |
| 💓 循环与淋巴系统 | 7 | 毛细血管分类、微循环、淋巴管等 |
| 🩸 血液与免疫 | 16 | 血细胞发育、IHC、ISH、PD-1/PD-L1等 |
| ⚡ 内分泌系统 | 8 | 垂体、胰岛、DNES、神经内分泌轴等 |
| ⚧️ 生殖系统 | 9 | 卵泡发育、黄体、受精、双胎等 |
| 🫘 泌尿系统 | 4 | 肾小体、近端小管、球旁复合体等 |
| 🫃 消化系统 | 6 | 中肠旋转、肝胆发生、卵黄蒂残留等 |
| 🫁 呼吸系统 | 1 | 呼吸道黏膜防御 |
| 👁️ 感觉器官 | 7 | 视网膜、螺旋器、前庭感知、房水循环等 |
| 🧬 胚胎发育 | 17 | 三胚层、神经管、心脏分隔、唇腭裂等 |
| 🧫 先天畸形与预防 | 7 | 致畸敏感期、产前筛查、三级预防等 |
| 🧪 特殊主题 | 6 | BCG机制、结核分枝杆菌、黑色素等 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install histology-and-embryology-pmph-10edition
```

### 使用方式

每个技能包含四部分内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示
4. **参考文档** — 详细补充资料

### 提问策略

#### 1. **概念理解**

**Question:**
```bash
血-脑屏障的结构与功能
```
**Answer:**
```bash
## 血-脑屏障结构与功能

血-脑屏障（BBB）位于脑毛细血管与脑组织之间，由以下结构组成：

### 三层结构
1. **连续性毛细血管内皮** — 无窗孔，细胞间以紧密连接封闭
2. **基膜** — 完整连续的基膜
3. **星形胶质细胞足突** — 覆盖毛细血管外表面

### 功能意义
- **选择性通透**：允许O₂、CO₂、葡萄糖、氨基酸等通过，阻止大分子、毒素、药物进入
- **维持微环境稳定**：保证神经元正常活动所需的离子浓度
- **免疫豁免**：限制免疫细胞进入中枢神经系统

### 临床相关
- 台盼蓝无法进入脑组织（经典示教实验）
- 某些药物需设计为脂溶性或通过载体转运才能入脑
- 多发性硬化、脑膜炎等可破坏BBB完整性
```

#### 2. **发育机制分析**

**Question:**
```bash
法洛四联症的胚胎学成因
```
**Answer:**
```bash
## 法洛四联症胚胎发生机制

### 关键发育事件
法洛四联症源于胚胎第4-8周心脏分隔发育异常，具体机制如下：

### 四大畸形的胚胎学基础
| 畸形 | 胚胎学机制 |
|------|-----------|
| 肺动脉狭窄 | 动脉干分隔不均，肺动脉较主动脉窄 |
| 室间隔缺损 | 漏斗部间隔未与室间隔肌部融合 |
| 主动脉骑跨 | 动脉干间隔偏位，主动脉跨越室间隔缺损 |
| 右心室肥厚 | 继发于肺动脉狭窄的代偿改变 |

### 胚胎关键期
- **第4周**：心管开始环化
- **第5-6周**：动脉干与心球分隔
- **第8周**：心脏四腔形成基本完成
```

#### 3. **临床案例分析**

**Question:**
```bash
男孩，外观为女性，腹股沟可触及包块，染色体核型为46,XY，应考虑什么诊断？
```
**Answer:**
```bash
## 病例分析

### 诊断线索
- 男性假两性畸形
- 46,XY核型但女性外生殖器
- 腹股沟可触及性腺（可能为睾丸）

### 最可能的诊断
**雄激素不敏感综合征（Androgen Insensitivity Syndrome, AIS）**

### 诊断依据
1. 雄激素受体缺陷 → 靶细胞对雄激素不反应
2. 睾丸正常分泌苗勒管抑制因子 → 无子宫/输卵管
3. 雄激素作用障碍 → 外生殖器女性化
4. 青春期可有乳房发育 → 雌激素来自雄激素外周转化

### 进一步检查
- 血清睾酮水平（正常或升高）
- 雄激素受体基因突变检测
- 腹股沟区超声/活检确认睾丸
```

## 关于作者

**小绿绿 xllgreen** — 九江学院临床医学院学生 · 科技极客

## 技术支持

PDF2App项目：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
DeepSeek API：https://platform.deepseek.com/
<br>
<br>
Xiaomi Mimo API：https://platform.xiaomimimo.com/

## 许可证

本项目内容基于人民卫生出版社《组织学与胚胎学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/#xllgreen/Histology-Embryology-PMPH-10edition&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xllgreen/Histology-Embryology-PMPH-10edition&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xllgreen/Histology-Embryology-PMPH-10edition&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xllgreen/Histology-Embryology-PMPH-10edition&type=Date" />
 </picture>
</a>
