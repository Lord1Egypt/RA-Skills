# Li_ETL_handle - ETL 自动化处理技能

## 🌍 多语言说明 / Multilingual Description

### 🇨🇳 中文
**Excel 自动化处理技能** - 一站式 Excel 数据处理解决方案，支持读取、写入、清洗、转换、合并 Excel 文件。基于 Node.js，无需安装 Excel 即可处理 .xlsx、.xls、.csv 文件。

**核心功能**：
- 📖 数据读取 - 支持 xlsx/xls/csv 多种格式
- ✍️ 数据写入 - 创建、追加、格式化输出
- 🧹 数据清洗 - 去重、删除空行、文本清理
- 🔄 数据转换 - 格式互转、行列转置、字段处理
- 🔗 数据合并 - 多文件批量合并
- 📈 数据分析 - 统计、筛选、排序、分组聚合
- 🔗 多表连接 - 内连接、左连接、右连接、全外连接
- 🔄 流程控制 - Switch/Case、If-Else
- 📝 脚本支持 - JavaScript 自定义处理

**作者**: 北京老李  
**版本**: 1.0.1  
**许可**: MIT

---

### 🇺🇸 English
**Excel Automation Skill** - All-in-one Excel data processing solution, supporting read, write, clean, transform, and merge Excel files. Based on Node.js, handles .xlsx, .xls, .csv files without Excel installation.

**Core Features**:
- 📖 Data Reading - Support xlsx/xls/csv formats
- ✍️ Data Writing - Create, append, format output
- 🧹 Data Cleaning - Deduplication, remove empty rows, text cleanup
- 🔄 Data Transformation - Format conversion, transpose, field processing
- 🔗 Data Merging - Batch merge multiple files
- 📈 Data Analysis - Statistics, filtering, sorting, grouping
- 🔗 Table Joins - Inner, Left, Right, Full Outer joins
- 🔄 Flow Control - Switch/Case, If-Else
- 📝 Script Support - JavaScript custom processing

**Author**: Beijing Lao Li  
**Version**: 1.0.1  
**License**: MIT

---

### 🇫🇷 Français
**Compétence d'Automatisation Excel** - Solution tout-en-un de traitement de données Excel, prenant en charge la lecture, l'écriture, le nettoyage, la transformation et la fusion de fichiers Excel. Basé sur Node.js, gère les fichiers .xlsx, .xls, .csv sans installation d'Excel.

**Fonctionnalités Principales**:
- 📖 Lecture de Données - Support des formats xlsx/xls/csv
- ✍️ Écriture de Données - Création, ajout, formatage de sortie
- 🧹 Nettoyage de Données - Déduplication, suppression des lignes vides
- 🔄 Transformation de Données - Conversion, transposition, traitement des champs
- 🔗 Fusion de Données - Fusion par lots de plusieurs fichiers
- 📈 Analyse de Données - Statistiques, filtrage, tri, regroupement
- 🔗 Jointures de Tables - Inner, Left, Right, Full Outer
- 🔄 Contrôle de Flux - Switch/Case, If-Else
- 📝 Support de Script - Traitement personnalisé JavaScript

**Auteur**: Pékin Lao Li  
**Version**: 1.0.1  
**Licence**: MIT

---

### 🇩🇪 Deutsch
**Excel-Automatisierungsfähigkeit** - All-in-One-Excel-Datenverarbeitungslösung, unterstützt Lesen, Schreiben, Bereinigen, Transformieren und Zusammenführen von Excel-Dateien. Basierend auf Node.js, verarbeitet .xlsx, .xls, .csv Dateien ohne Excel-Installation.

**Hauptfunktionen**:
- 📖 Datenlesen - Unterstützung für xlsx/xls/csv Formate
- ✍️ Datenschreiben - Erstellen, Anhängen, Ausgabe formatieren
- 🧹 Datenbereinigung - Deduplizierung, leere Zeilen entfernen
- 🔄 Datentransformation - Formatkonvertierung, Transponierung
- 🔗 Datenzusammenführung - Stapelzusammenführung mehrerer Dateien
- 📈 Datenanalyse - Statistik, Filterung, Sortierung, Gruppierung
- 🔗 Tabellenverknüpfungen - Inner, Left, Right, Full Outer Joins
- 🔄 Flusssteuerung - Switch/Case, If-Else
- 📝 Skriptunterstützung - Benutzerdefinierte JavaScript-Verarbeitung

**Autor**: Peking Lao Li  
**Version**: 1.0.1  
**Lizenz**: MIT

---

### 🇯🇵 日本語
**Excel 自動化スキル** - Excel ファイルの読み取り、書き込み、クリーニング、変換、マージをサポートするオールインワンの Excel データ処理ソリューション。Node.js に基づき、Excel のインストールなしで.xlsx、.xls、.csv ファイルを処理できます。

**主な機能**:
- 📖 データ読み取り - xlsx/xls/csv 形式をサポート
- ✍️ データ書き込み - 作成、追加、フォーマット出力
- 🧹 データクリーニング - 重複削除、空行削除
- 🔄 データ変換 - 形式変換、転置、フィールド処理
- 🔗 データマージ - 複数ファイルのバッチマージ
- 📈 データ分析 - 統計、フィルタリング、並べ替え、グループ化
- 🔗 テーブル結合 - 内部結合、左結合、右結合、完全外部結合
- 🔄 フロー制御 - Switch/Case、If-Else
- 📝 スクリプトサポート - JavaScript カスタム処理

**著者**: 北京老李  
**バージョン**: 1.0.1  
**ライセンス**: MIT

---

## 📚 详细功能 / Detailed Features

### 1️⃣ 数据读取 (Extract)
- `readExcel()` - 读取 Excel 文件
- `readCSV()` - 读取 CSV 文件

### 2️⃣ 数据写入 (Load)
- `writeExcel()` - 写入 Excel 文件
- `writeCSV()` - 写入 CSV 文件

### 3️⃣ 数据清洗 (Clean)
- `removeDuplicates()` - 去重
- `removeEmptyRows()` - 删除空行
- `cleanText()` - 文本清理
- `formatData()` - 格式标准化
- `replaceNull()` - NULL 值替换

### 4️⃣ 数据转换 (Transform)
- `csvToExcel()` - CSV 转 Excel
- `excelToCSV()` - Excel 转 CSV
- `transpose()` - 行列转置
- `concatFields()` - 字段拼接
- `valueMapping()` - 值映射
- `splitField()` - 字段拆分
- `columnsToRows()` - 列转行
- `rowsToColumns()` - 行转列

### 5️⃣ 数据合并 (Merge)
- `mergeExcelFiles()` - 多文件合并
- `mergeFolderExcel()` - 文件夹批量合并

### 6️⃣ 数据分析 (Analyze)
- `getStatistics()` - 基础统计
- `filterData()` - 数据筛选
- `sortData()` - 数据排序
- `groupBy()` - 分组聚合

### 7️⃣ 多表连接 (Join)
- `innerJoin()` - 内连接
- `leftJoin()` - 左连接
- `rightJoin()` - 右连接
- `fullOuterJoin()` - 全外连接
- `crossJoin()` - 交叉连接

### 8️⃣ 流程控制 (Flow Control)
- `switchCase()` - Switch/Case 数据分类
- `ifElse()` - If-Else 条件处理

### 9️⃣ 脚本支持 (Script)
- `executeScript()` - JavaScript 脚本执行
- `writeLog()` - 写日志调试

### 🔟 工具函数 (Utils)
- `maskSensitiveData()` - 敏感数据脱敏
- `getOutputPath()` - 输出路径生成

---

## 🚀 使用示例 / Usage Examples

### 基本使用 / Basic Usage
```javascript
const excel = require('./index.js');

// 读取 Excel
const { data } = excel.readExcel('./data.xlsx');

// 数据清洗
const cleaned = excel.removeDuplicates(data, 'phone');

// 写入结果
excel.writeExcel(cleaned, './output.xlsx');
```

### 多表连接 / Table Join
```javascript
// 左连接
const result = excel.leftJoin(employees, departments, 'dept', 'dept_name');
```

### 流程控制 / Flow Control
```javascript
// Switch/Case
const classified = excel.switchCase(data, 'dept', {
  'Sales': 'A',
  'Tech': 'B'
}, 'Other');

// If-Else
const leveled = excel.ifElse(
  data,
  row => row.score >= 85,
  row => ({ ...row, level: 'High' }),
  row => ({ ...row, level: 'Low' })
);
```

---

## ⚠️ 安全提示 / Security Notice

- **executeScript 函数**允许执行自定义 JavaScript 代码，请确保传入的函数安全可靠
- **处理未知来源的 Excel 文件**时请注意潜在风险，建议在沙箱环境中测试
- **依赖包安全**：xlsx 包存在已知漏洞，建议只处理可信来源的文件

---

## 📦 依赖 / Dependencies

- xlsx@^0.18.5 - Excel 文件处理
- csv-parser@^3.0.0 - CSV 文件解析
- csv-stringify@^6.4.0 - CSV 文件生成

---

## 📄 许可 / License

MIT License - © 2026 北京老李 (Beijing Lao Li)

---

## 📞 联系 / Contact

- **作者**: 北京老李
- **GitHub**: https://github.com/beijing-laoli
- **ClawHub**: https://clawhub.com/skills/li-excel-handle
