# GDPR Compliance v1.1.0

**欧盟通用数据保护条例（GDPR）合规检查、风险评估和文档生成工具**

🎉 **v1.1.0 重要更新**：全新统一化CLI接口，与PIPL、CCPA工具体验一致；支持JSON/Markdown/HTML/CSV多格式报告输出；跨法域联合检查功能。

## 🌟 核心价值

**为欧盟市场提供全面的GDPR合规解决方案**，帮助企业和组织在欧盟境内处理个人数据时确保合规。

### 解决的关键问题
1. **合规检查复杂** - GDPR要求繁多，全面评估难度大
2. **DPIA高频需求** - 数据保护影响评估是法定要求
3. **跨境传输风险** - 第三国数据传输需严格合规审查
4. **数据主体权利** - 多类权利响应机制需落实

## 📁 文件结构

```
gdpr-compliance-1.0.4/
├── SKILL.md                      # 主技能文档
├── README.md                     # 本文件
├── package.json                  # 元数据 (v1.1.0)
├── CHANGELOG.md                  # 更新日志
├── requirements.txt              # 依赖列表
├── scripts/                      # 核心脚本
│   ├── gdpr-check.py             # GDPR合规检查（统一CLI接口）
│   ├── data-subject-rights.py    # 数据主体权利检查
│   ├── dpia-generator.py         # DPIA生成器
│   ├── cross-border-transfer.py  # 跨境传输检查
│   ├── security_check_gdpr.py    # 安全检查脚本
│   └── utils/                    # 工具函数库
│       ├── gdpr_validator.py     # GDPR验证工具
│       ├── gdpr_templates.py     # 模板引擎
│       └── gdpr_report_formatter.py # 报告格式化
├── references/                   # 参考文档
│   └── gdpr-regulation.md        # GDPR法规摘要
└── assets/                       # 资源文件
    └── templates/                # 文档模板
```

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行GDPR合规检查
```bash
# 场景模式
python scripts/gdpr-check.py --scenario "用户数据分析"

# 交互模式
python scripts/gdpr-check.py --interactive

# 指定报告格式（JSON / Markdown / HTML / CSV）
python scripts/gdpr-check.py --scenario "用户数据分析" --format json
```

### 其他专项检查
```bash
# 数据主体权利检查
python scripts/data-subject-rights.py --right access

# 跨境传输检查
python scripts/cross-border-transfer.py --country "US"

# DPIA生成
python scripts/dpia-generator.py
```

### 跨法域联合检查（新）
```bash
# 一键运行PIPL + GDPR + CCPA三合一检查
python ../compliance_core/global_check.py
```

## ✨ 主要功能

### 1. GDPR合规检查（统一CLI接口）
- 合法性基础验证（Article 6）
- 数据保护原则检查
- 数据主体权利保障检查
- DPO要求检查
- DPIA要求检查

### 2. 数据保护影响评估（DPIA）
- 识别高风险数据处理活动
- 生成标准化DPIA报告
- 提供风险缓解措施建议

### 3. 数据主体权利管理
- 访问权、更正权、删除权、数据可携权、反对权

### 4. 跨境数据传输合规
- 充分性决定国家检查
- 标准合同条款（SCCs）验证
- 约束性公司规则（BCRs）检查

## 📊 版本信息

- **版本**: 1.0.4
- **发布日期**: 2026-07-05
- **许可证**: MIT
- **作者**: Wei Wu (wwumit)

## 🛡️ 安全特性

- ✅ **纯本地运行** - 无网络调用，不收集用户数据
- ✅ **透明依赖** - 仅依赖pandas和jinja2（可选）
- ✅ **代码开源可审计**

## ⚠️ 重要法律声明

### 免责条款

1. **非法律建议**：本技能提供的信息仅供参考，不构成法律建议
2. **专业性咨询**：重大GDPR合规决策必须咨询专业律师或DPO
3. **责任限制**：用户对使用本技能的所有决策和后果负全责
4. **适用性限制**：专为欧盟GDPR设计

完整法律声明详见 `SKILL.md`。

---

**GPDR Compliance v1.1.0 - Wei Wu (wwumit)**
