# 医学量表检索技能 (medical-scale-research)

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-green)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/kevinget-svg/medical-scale-research?style=social)](https://github.com/kevinget-svg/medical-scale-research)

> 🤖 自动检索医学量表信息，生成标准化研究报告的 AI 助手

---

## 📖 简介

**医学量表检索技能**是一个专为临床研究人员、生物统计师和医药行业从业者设计的 OpenClaw 技能。它能够自动检索医学量表的完整信息（背景、版权、CDISC 映射、统计方法等），下载量表官方 PDF 或截图，并生成标准化的飞书云文档报告。

### 🎯 适用人群
- 🏥 临床研究人员
- 📊 生物统计师
- 💊 医药企业研发人员
- 🎓 医学研究生
- 📚 系统评价/Meta 分析研究者

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🔍 **7 维度并行检索** | 背景信息、版本历史、版权信息、中文版、CDISC 映射、统计方法、量表全文 |
| 📄 **量表全文获取** | 自动下载官方 PDF 或屏幕截图，强制要求，确保完整性 |
| 🎯 **CDISC 自动推荐** | 基于规则引擎自动推荐 SDTM/ADaM Domain（High 置信度） |
| 📊 **标准化报告** | 生成 5 章结构报告（量表简介/版权/CDISC/统计/参考文献） |
| 💾 **飞书集成** | 自动创建飞书云文档，支持知识库归档 |
| 📝 **代码示例** | 含完整 SAS/R 代码（缺失处理、MMRM、应答率分析等） |

---

## 🚀 快速开始

### 前置要求

- ✅ OpenClaw 运行环境
- ✅ 飞书 API 权限（用于文档生成）
- ✅ 浏览器自动化权限（用于信息检索）

### 安装方式

#### 方式 1：通过 ClawHub 安装（推荐）
```bash
openclaw skill install medical-scale-research
```

#### 方式 2：手动安装
```bash
# 1. 克隆或下载本仓库
git clone https://github.com/kevinget-svg/medical-scale-research.git

# 2. 复制到 OpenClaw 技能目录
cp -r medical-scale-research ~/.openclaw/workspace/skills/

# 3. 验证安装
openclaw skill list | grep medical-scale
```

### 使用示例

在 OpenClaw 对话中输入以下指令：

```
# 基础检索
"检索 SGRQ 量表的信息"
"整理 TNSS 量表的完整报告"

# 查询特定信息
"查询 PASI量表的 CDISC domain"
"PASI量表的统计分析方法是什么"

# 更新已有报告
"更新 EASI量表的版本信息"
```

### 输出示例

**技能会生成如下报告**：

```
✅ 已完成 SGRQ 量表信息检索

📄 文档链接：https://xxx.feishu.cn/docx/xxxxx
📚 已归档至：医学量表库 > 呼吸系统 > SGRQ

检索维度：
✓ 背景信息（5 篇文献）
✓ 官方量表（✅ 已下载 PDF - 7.0KB）
✓ 版本历史（v2.1 最新版，2023 更新）
✓ 版权信息（Mapi Research Trust）
✓ 中文版（3 篇验证文献）
✓ CDISC 映射（QS/ADQS 推荐）
✓ 统计方法（4 种模型）

📎 量表全文：
- PDF 路径：/Users/wangyafei/Downloads/scales/SGRQ_official.pdf
- 下载链接：[SGRQ Official PDF](https://xxx.xxx.ac.uk/xxx.pdf)
```

---

## 📋 报告结构

生成的标准化报告包含以下章节：

```
一、量表简介
  ├─ 1.1 背景及发展历程
  ├─ 1.2 版本历史
  ├─ 1.3 应用领域
  ├─ 1.4 量表内容
  └─ 1.5 官方量表全文 ⚠️（PDF 链接或截图）

二、版权与授权信息
  ├─ 2.1 版权方信息
  └─ 2.2 中文版信息

三、CDISC 编程
  ├─ 3.1 标准 aCRF 与受控术语
  ├─ 3.2 SDTM 实现
  └─ 3.3 ADaM 实现

四、统计分析
  ├─ 4.1 数据类型与分布特征
  ├─ 4.2 缺失值处理（含 SAS/R 代码）
  ├─ 4.3 常规分析模型
  ├─ 4.4 探索性分析
  └─ 4.5 结果呈现（Table/Figure 模板）

五、参考文献

附录
  ├─ A. 检索策略记录
  └─ B. 量表全文获取记录
```

---

## 📦 发布指南

### 发布到 ClawHub（手动）

目前 ClawHub 不支持 CLI 直接发布，需要手动操作：

1. **访问 ClawHub 官网**
   - 打开 https://clawhub.ai
   - 登录你的 GitHub 账号

2. **创建技能包**
   ```bash
   # 打包技能目录
   cd ~/.openclaw/workspace/skills/
   tar -czf medical-scale-research.tar.gz medical-scale-research/
   ```

3. **上传技能**
   - 进入 "Submit Skill" 页面
   - 填写技能信息：
     - 名称：医学量表检索技能
     - 描述：自动检索医学量表信息，生成标准化研究报告
     - 分类：Healthcare / Research Tools
     - 标签：medical, scale, CDISC, feishu, clinical-trials
   - 上传 `medical-scale-research.tar.gz`
   - 提交审核

4. **等待审核**
   - ClawHub 团队会在 1-3 个工作日内审核
   - 审核通过后会出现在技能市场

---

## 🔧 配置说明

### 文件保存路径

量表 PDF 文件默认保存到：
```
/Users/wangyafei/Downloads/scales/[量表名]_official.pdf
```

可在 `SKILL.md` 中修改保存路径。

### 飞书权限配置

1. 打开飞书开发者后台
2. 创建应用 → 添加权限：
   - 云文档读写权限
   - 知识库管理权限
3. 将应用添加到工作群

### CDISC 规则配置

CDISC Domain 推荐规则位于：
```
rules/cdisc-mapping.json
```

可根据需要添加新的映射规则。

---

## 📚 已支持量表示例

| 量表名称 | 英文全称 | 疾病领域 | 状态 |
|---------|---------|---------|------|
| SGRQ | St George's Respiratory Questionnaire | 呼吸系统 | ✅ 已测试 |
| TNSS | Total Nasal Symptom Score | 耳鼻喉科 | ✅ 已测试 |
| PASI | Psoriasis Area and Severity Index | 皮肤科 | ✅ 已测试 |
| EASI | Eczema Area and Severity Index | 皮肤科 | ✅ 已测试 |
| EORTC QLQ-C30 | European Organisation for Research and Treatment of Cancer Quality of Life Questionnaire | 肿瘤科 | 🔄 待测试 |
| PHQ-9 | Patient Health Questionnaire-9 | 精神科 | 🔄 待测试 |

---

## 🛠️ 技能文件结构

```
medical-scale-research/
├── SKILL.md                      # 技能说明和执行指令
├── templates/
│   └── scale-report.md           # 文档模板（含 1.5 官方量表全文）
├── rules/
│   └── cdisc-mapping.json        # CDISC 推荐规则（12 条映射）
├── examples/
│   └── SGRQ-example.md           # SGRQ 量表示例输出
├── README.md                     # 本文件
└── LICENSE                       # MIT 许可证
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 如何贡献

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 报告问题

如遇到以下问题，请提交 Issue：
- 🐛 技能执行错误
- 📝 文档内容错误
- 💡 功能改进建议
- 🔍 新量表检索请求

---

## 📝 更新日志

### v1.0.0 (2026-04-19)
- ✨ 初始版本发布
- 🔍 7 维度并行检索
- 📄 强制量表全文获取（PDF/截图）
- 🎯 CDISC Domain 自动推荐
- 📊 标准化报告生成
- 💾 飞书文档集成
- 📝 SAS/R 代码示例

---

## 📄 许可证

本项目采用 **MIT 许可证**。详见 [LICENSE](LICENSE) 文件。

---

## 📧 联系方式

- 📮 Issue: [GitHub Issues](https://github.com/kevinget-svg/medical-scale-research/issues)
- 💬 讨论：OpenClaw 社区
- 📧 邮件：justingwang0726@gmail.com

---

## 🙏 致谢

感谢以下项目提供的数据源：
- [CDISC](https://www.cdisc.org/) - 临床数据交换标准
- [Mapi Research Trust](https://eprovide.mapi-trust.org/) - 量表版权信息
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) - 医学文献数据库
- [OpenClaw](https://openclaw.ai) - AI 自动化框架

---

## ⭐ 支持项目

如果觉得这个技能有用，欢迎：
1. 给仓库点个 ⭐ Star
2. 分享给需要的同事/朋友
3. 提交 Issue 或 Pull Request

---

*最后更新：2026-04-19*
*维护者：王亚飞 (Kevin Wang)*
