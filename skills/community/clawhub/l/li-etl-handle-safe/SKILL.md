# li-etl-handle-safe - 安全版 Excel/CSV ETL 处理技能

## 功能描述

安全的 Excel/CSV 文件处理技能，支持读取、写入、清洗、转换和合并表格数据。**本版本已移除任意代码执行功能，使用安全的 exceljs 库替代有漏洞的 xlsx 库。**

## 版本

**v1.0.2** - 修复 CSV 解析和 Excel 写入问题，完善功能测试

## 支持格式

- `.xlsx` - Excel 2007+
- `.xls` - Excel 97-2003（通过转换）
- `.csv` - CSV 文本文件

## 功能列表

### 读取表格
- `readExcel(filePath, options)` - 读取 Excel 文件
- `readCSV(filePath, options)` - 读取 CSV 文件

### 写入表格
- `writeExcel(filePath, data, options)` - 写入 Excel 文件
- `writeCSV(filePath, data, options)` - 写入 CSV 文件

### 数据清洗
- `cleanData(data, rules)` - 根据规则清洗数据
- `removeEmptyRows(data)` - 删除空行
- `removeDuplicates(data, columns)` - 删除重复行

### 数据转换
- `transformColumns(data, transforms)` - 转换列数据（支持类型转换、格式化等预设操作）
- `filterRows(data, conditions)` - 按条件过滤行
- `sortData(data, sortColumns)` - 排序数据

### 数据合并
- `mergeFiles(filePaths, options)` - 合并多个文件
- `appendRows(targetData, sourceData)` - 追加行数据

## 安全特性

✅ **无任意代码执行** - 移除了 executeScript 功能
✅ **安全依赖** - 使用 exceljs 替代有漏洞的 xlsx 库
✅ **官方源** - 所有依赖来自官方 HTTPS npm registry
✅ **禁止自主调用** - disable-model-invocation: true

## 使用示例

```javascript
// 读取 Excel
const data = await readExcel('/path/to/file.xlsx', { sheet: 0 });

// 清洗数据
const cleaned = await cleanData(data, { trim: true, removeEmpty: true });

// 转换列类型
const transformed = await transformColumns(cleaned, {
  columns: { price: 'number', date: 'datetime' }
});

// 写入 CSV
await writeCSV('/path/to/output.csv', transformed);
```

## 注意事项

- 所有文件操作均在本地进行
- 不支持执行自定义 JavaScript 代码（安全考虑）
- 大文件建议分批处理
