# Li_ETL_handle - ETL 自动化处理技能

> 🌍 多语言支持 / Multilingual Support  
> 👤 作者 / Author: **北京老李 (Beijing Lao Li)**  
> 📦 版本 / Version: 1.0.1  
> 📄 许可 / License: MIT

---

## 🌐 语言选择 / Language Selection

- [🇨🇳 中文](#中文)
- [🇺🇸 English](#english)
- [🇫🇷 Français](#français)
- [🇩🇪 Deutsch](#deutsch)
- [🇯🇵 日本語](#日本語)

---

## 中文

### 📋 简介

**Li_ETL_handle** 是一个功能完整的 ETL 自动化处理技能，支持读取、写入、清洗、转换、合并 Excel 文件。无需安装 Microsoft Excel，基于 Node.js 实现跨平台支持。

### ✨ 核心功能

| 类别 | 功能 | API 数量 |
|------|------|---------|
| 📥 数据读取 | Excel/CSV 读取 | 2 |
| 📤 数据写入 | Excel/CSV 写入 | 2 |
| 🧹 数据清洗 | 去重、删除空行、文本清理 | 5 |
| 🔄 数据转换 | 转置、拼接、拆分、映射 | 7 |
| 🔗 数据合并 | 多文件合并、文件夹批量 | 2 |
| 📈 数据分析 | 统计、筛选、排序、分组 | 4 |
| 🔗 多表连接 | 内/左/右/全外/交叉连接 | 5 |
| 🔄 流程控制 | Switch/Case、If-Else | 2 |
| 📝 脚本支持 | JavaScript 脚本、日志 | 2 |
| **总计** | **32 个核心功能** | **32** |

### 🚀 快速开始

```bash
# 安装依赖
npm install

# 运行测试
npm test

# 使用技能
const excel = require('./index.js');
const { data } = excel.readExcel('./input.xlsx');
const cleaned = excel.removeDuplicates(data, 'phone');
excel.writeExcel(cleaned, './output.xlsx');
```

### 📚 使用示例

#### 1. 数据清洗
```javascript
const excel = require('./index.js');

// 读取数据
const { data } = excel.readExcel('./customers.xlsx');

// 删除空行
const step1 = excel.removeEmptyRows(data);

// 去重
const step2 = excel.removeDuplicates(step1, '手机号');

// 文本清理
const step3 = excel.cleanText(step2, ['姓名', '地址']);

// 格式标准化（脱敏）
const step4 = excel.formatData(step3, {
  '手机号': 'phone',
  '邮箱': 'email'
});

// 保存结果
excel.writeExcel(step4, './customers_clean.xlsx');
```

#### 2. 多表连接
```javascript
// 左连接
const result = excel.leftJoin(employees, departments, 'dept_id', 'id');

// 内连接
const matched = excel.innerJoin(orders, customers, 'customer_id', 'id');
```

#### 3. 流程控制
```javascript
// Switch/Case 分类
const classified = excel.switchCase(data, 'dept', {
  '销售部': 'A 类',
  '技术部': 'B 类',
  '人事部': 'C 类'
}, '其他类');

// If-Else 条件处理
const leveled = excel.ifElse(
  data,
  row => row.score >= 85,
  row => ({ ...row, level: '优秀' }),
  row => ({ ...row, level: '良好' })
);
```

#### 4. 脚本执行
```javascript
// 自定义计算
const result = excel.executeScript(data, (row, index) => ({
  ...row,
  年薪：row.月薪 * 12,
  奖金：row.月薪 * 0.1
}));
```

### 📊 性能表现

| 操作 | 数据量 | 耗时 | 目标 |
|------|--------|------|------|
| 写入 | 1000 行 | <50ms | <5000ms ✅ |
| 读取 | 1000 行 | <60ms | <2000ms ✅ |
| 去重 | 1000 行 | <5ms | <1000ms ✅ |
| 分组 | 5000 行 | <10ms | <1000ms ✅ |

### 📁 文件结构

```
Li_exec_handle/
├── index.js           # 核心功能代码
├── package.json       # 依赖配置
├── SKILL.md          # 技能说明（多语言）
├── README.md         # 使用文档（多语言）
├── TEST_REPORT.md    # 测试报告
├── SECURITY_AUDIT.md # 安全审计报告
└── tests/            # 测试文件
    ├── unit.test.js      # 单元测试
    ├── scenario.test.js  # 场景测试
    └── temp/             # 测试临时文件
```

### ⚠️ 安全提示

- **executeScript 函数**允许执行自定义 JavaScript 代码，请确保传入的函数安全
- **处理未知来源的 Excel 文件**时请注意潜在风险
- **依赖包**：xlsx 存在已知漏洞，建议只处理可信来源文件

### 📞 联系作者

- **作者**: 北京老李
- **邮箱**: beijing.laoli@example.com
- **GitHub**: https://github.com/beijing-laoli
- **ClawHub**: https://clawhub.com/skills/li-excel-handle

---

## English

### 📋 Introduction

**Li_ETL_handle** is a full-featured ETL automation skill supporting read, write, clean, transform, and merge Excel files. No Microsoft Excel installation required, cross-platform support based on Node.js.

### ✨ Core Features

| Category | Features | API Count |
|----------|----------|-----------|
| 📥 Data Reading | Excel/CSV Reading | 2 |
| 📤 Data Writing | Excel/CSV Writing | 2 |
| 🧹 Data Cleaning | Dedup, Empty Rows, Text Cleanup | 5 |
| 🔄 Data Transform | Transpose, Concat, Split, Map | 7 |
| 🔗 Data Merging | Multi-file, Folder Batch | 2 |
| 📈 Data Analysis | Stats, Filter, Sort, Group | 4 |
| 🔗 Table Joins | Inner/Left/Right/Full/Cross | 5 |
| 🔄 Flow Control | Switch/Case, If-Else | 2 |
| 📝 Script Support | JavaScript, Logging | 2 |
| **Total** | **32 Core Functions** | **32** |

### 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run tests
npm test

# Use the skill
const excel = require('./index.js');
const { data } = excel.readExcel('./input.xlsx');
const cleaned = excel.removeDuplicates(data, 'phone');
excel.writeExcel(cleaned, './output.xlsx');
```

### 📞 Contact

- **Author**: Beijing Lao Li
- **GitHub**: https://github.com/beijing-laoli
- **ClawHub**: https://clawhub.com/skills/li-excel-handle

---

## Français

### 📋 Introduction

**LI_excel_handle** est une compétence d'automatisation Excel complète prenant en charge la lecture, l'écriture, le nettoyage, la transformation et la fusion de fichiers Excel. Aucune installation de Microsoft Excel requise.

### ✨ Fonctionnalités Principales

32 fonctions principales pour le traitement de données Excel.

### 🚀 Démarrage Rapide

```bash
npm install
npm test
```

### 📞 Contact

- **Auteur**: Pékin Lao Li
- **GitHub**: https://github.com/beijing-laoli

---

## Deutsch

### 📋 Einführung

**LI_excel_handle** ist eine vollständige Excel-Automatisierungsfähigkeit mit Unterstützung für Lesen, Schreiben, Bereinigen, Transformieren und Zusammenführen von Excel-Dateien.

### ✨ Hauptfunktionen

32 Kernfunktionen für die Excel-Datenverarbeitung.

### 🚀 Schnellstart

```bash
npm install
npm test
```

### 📞 Kontakt

- **Autor**: Peking Lao Li
- **GitHub**: https://github.com/beijing-laoli

---

## 日本語

### 📋 概要

**LI_excel_handle** は、Excel ファイルの読み取り、書き込み、クリーニング、変換、マージをサポートする包括的な Excel 自動化スキルです。

### ✨ 主な機能

Excel データ処理のための 32 のコア機能。

### 🚀 クイックスタート

```bash
npm install
npm test
```

### 📞 お問い合わせ

- **著者**: 北京老李
- **GitHub**: https://github.com/beijing-laoli

---

## 📄 License / 许可

MIT License - © 2026 北京老李 (Beijing Lao Li)
