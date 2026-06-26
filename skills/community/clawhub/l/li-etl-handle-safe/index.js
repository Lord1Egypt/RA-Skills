/**
 * li-etl-handle-safe - 安全版 Excel/CSV ETL 处理
 * 
 * 功能：读取、写入、清洗、转换、合并 Excel/CSV 文件
 * 安全特性：无 executeScript，使用 exceljs 替代 xlsx
 */

const XLSX = require('exceljs');
const csvParser = require('csv-parser');
const { stringify } = require('csv-stringify/sync');
const fs = require('fs');
const path = require('path');

/**
 * 读取 Excel 文件
 * @param {string} filePath - 文件路径
 * @param {object} options - 选项 { sheet: 0, header: true }
 * @returns {Promise<Array>} 数据数组
 */
async function readExcel(filePath, options = {}) {
  const { sheet = 0, header = true } = options;
  
  if (!fs.existsSync(filePath)) {
    throw new Error(`文件不存在：${filePath}`);
  }
  
  const workbook = new XLSX.Workbook();
  await workbook.xlsx.readFile(filePath);
  
  const worksheet = workbook.getWorksheet(sheet + 1) || workbook.worksheets[sheet];
  if (!worksheet) {
    throw new Error(`工作表不存在：${sheet}`);
  }
  
  const data = [];
  worksheet.eachRow((row, rowNumber) => {
    if (header && rowNumber === 1) return; // 跳过表头（如果需要）
    const rowData = {};
    row.eachCell((cell, colNumber) => {
      const headerName = header ? worksheet.getRow(1).getCell(colNumber).value : `col${colNumber}`;
      rowData[headerName] = cell.value;
    });
    data.push(rowData);
  });
  
  return data;
}

/**
 * 读取 CSV 文件
 * @param {string} filePath - 文件路径
 * @param {object} options - 选项 { encoding: 'utf8', separator: ',' }
 * @returns {Promise<Array>} 数据数组
 */
async function readCSV(filePath, options = {}) {
  const { encoding = 'utf8', separator = ',' } = options;
  
  if (!fs.existsSync(filePath)) {
    throw new Error(`文件不存在：${filePath}`);
  }
  
  const content = fs.readFileSync(filePath, encoding);
  const lines = content.trim().split('\n');
  
  if (lines.length === 0) return [];
  
  const headers = lines[0].split(separator).map(h => h.trim());
  const data = [];
  
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(separator).map(v => v.trim());
    const row = {};
    headers.forEach((header, idx) => {
      row[header] = values[idx] || '';
    });
    data.push(row);
  }
  
  return data;
}

/**
 * 写入 Excel 文件
 * @param {string} filePath - 文件路径
 * @param {Array} data - 数据数组
 * @param {object} options - 选项 { sheetName: 'Sheet1', header: true }
 */
async function writeExcel(filePath, data, options = {}) {
  const { sheetName = 'Sheet1', header = true } = options;
  
  const workbook = new XLSX.Workbook();
  const worksheet = workbook.addWorksheet(sheetName);
  
  if (data.length === 0) {
    await workbook.xlsx.writeFile(filePath);
    return;
  }
  
  // 写入表头
  if (header) {
    const headers = Object.keys(data[0]);
    worksheet.addRow(headers);
  }
  
  // 写入数据
  const headers = Object.keys(data[0]);
  data.forEach(row => {
    const rowData = header ? headers.map(h => row[h]) : Object.values(row);
    worksheet.addRow(rowData);
  });
  
  // 确保目录存在
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  await workbook.xlsx.writeFile(filePath);
}

/**
 * 写入 CSV 文件
 * @param {string} filePath - 文件路径
 * @param {Array} data - 数据数组
 * @param {object} options - 选项 { header: true, encoding: 'utf8' }
 */
function writeCSV(filePath, data, options = {}) {
  const { header = true, encoding = 'utf8' } = options;
  
  if (data.length === 0) {
    fs.writeFileSync(filePath, '', encoding);
    return;
  }
  
  const headers = Object.keys(data[0]);
  const output = stringify(data, {
    header,
    columns: header ? headers : undefined,
    encoding
  });
  
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(filePath, output, encoding);
}

/**
 * 清洗数据
 * @param {Array} data - 数据数组
 * @param {object} rules - 清洗规则 { trim: true, removeEmpty: true, removeNull: true }
 * @returns {Array} 清洗后的数据
 */
function cleanData(data, rules = {}) {
  const { trim = false, removeEmpty = false, removeNull = false } = rules;
  
  return data.filter(row => {
    // 移除空行
    if (removeEmpty && Object.values(row).every(v => v === '' || v === null || v === undefined)) {
      return false;
    }
    
    // 处理每个字段
    const cleanedRow = {};
    for (const [key, value] of Object.entries(row)) {
      let newValue = value;
      
      // 移除 null
      if (removeNull && (value === null || value === undefined)) {
        continue;
      }
      
      // 修剪字符串
      if (trim && typeof value === 'string') {
        newValue = value.trim();
      }
      
      cleanedRow[key] = newValue;
    }
    
    return true;
  });
}

/**
 * 删除空行
 * @param {Array} data - 数据数组
 * @returns {Array} 过滤后的数据
 */
function removeEmptyRows(data) {
  return data.filter(row => 
    !Object.values(row).every(v => v === '' || v === null || v === undefined)
  );
}

/**
 * 删除重复行
 * @param {Array} data - 数据数组
 * @param {Array} columns - 用于判断重复的列名
 * @returns {Array} 去重后的数据
 */
function removeDuplicates(data, columns) {
  const seen = new Set();
  return data.filter(row => {
    const key = columns.map(col => row[col]).join('|');
    if (seen.has(key)) {
      return false;
    }
    seen.add(key);
    return true;
  });
}

/**
 * 转换列数据
 * @param {Array} data - 数据数组
 * @param {object} transforms - 转换配置 { columns: { colName: 'type' } }
 * 支持类型：'string', 'number', 'integer', 'float', 'boolean', 'datetime', 'uppercase', 'lowercase'
 * @returns {Array} 转换后的数据
 */
function transformColumns(data, transforms) {
  const { columns = {} } = transforms;
  
  return data.map(row => {
    const newRow = { ...row };
    
    for (const [colName, transformType] of Object.entries(columns)) {
      const value = newRow[colName];
      if (value === null || value === undefined) continue;
      
      switch (transformType) {
        case 'string':
          newRow[colName] = String(value);
          break;
        case 'number':
          newRow[colName] = Number(value);
          break;
        case 'integer':
          newRow[colName] = parseInt(value, 10);
          break;
        case 'float':
          newRow[colName] = parseFloat(value);
          break;
        case 'boolean':
          newRow[colName] = value === true || value === 'true' || value === 1;
          break;
        case 'datetime':
          newRow[colName] = new Date(value).toISOString();
          break;
        case 'uppercase':
          newRow[colName] = String(value).toUpperCase();
          break;
        case 'lowercase':
          newRow[colName] = String(value).toLowerCase();
          break;
        default:
          // 未知转换类型，保持原值
          break;
      }
    }
    
    return newRow;
  });
}

/**
 * 过滤行
 * @param {Array} data - 数据数组
 * @param {object} conditions - 过滤条件 { column: 'name', operator: 'eq', value: 'test' }
 * 支持运算符：'eq', 'ne', 'gt', 'gte', 'lt', 'lte', 'contains', 'startsWith', 'endsWith'
 * @returns {Array} 过滤后的数据
 */
function filterRows(data, conditions) {
  const { column, operator, value } = conditions;
  
  return data.filter(row => {
    const rowValue = row[column];
    
    switch (operator) {
      case 'eq': return rowValue == value;
      case 'ne': return rowValue != value;
      case 'gt': return rowValue > value;
      case 'gte': return rowValue >= value;
      case 'lt': return rowValue < value;
      case 'lte': return rowValue <= value;
      case 'contains': return String(rowValue).includes(String(value));
      case 'startsWith': return String(rowValue).startsWith(String(value));
      case 'endsWith': return String(rowValue).endsWith(String(value));
      default: return true;
    }
  });
}

/**
 * 排序数据
 * @param {Array} data - 数据数组
 * @param {Array} sortColumns - 排序配置 [{ column: 'name', order: 'asc' }]
 * @returns {Array} 排序后的数据
 */
function sortData(data, sortColumns) {
  return [...data].sort((a, b) => {
    for (const { column, order = 'asc' } of sortColumns) {
      const aVal = a[column];
      const bVal = b[column];
      
      let comparison = 0;
      if (aVal < bVal) comparison = -1;
      else if (aVal > bVal) comparison = 1;
      
      if (comparison !== 0) {
        return order === 'desc' ? -comparison : comparison;
      }
    }
    return 0;
  });
}

/**
 * 合并多个文件
 * @param {Array} filePaths - 文件路径数组
 * @param {object} options - 选项 { output: 'merged.xlsx', format: 'xlsx' }
 * @returns {Promise<Array>} 合并后的数据
 */
async function mergeFiles(filePaths, options = {}) {
  const { output, format = 'xlsx' } = options;
  const allData = [];
  
  for (const filePath of filePaths) {
    let data;
    if (filePath.endsWith('.csv')) {
      data = await readCSV(filePath);
    } else {
      data = await readExcel(filePath);
    }
    allData.push(...data);
  }
  
  if (output) {
    if (output.endsWith('.csv')) {
      writeCSV(output, allData);
    } else {
      await writeExcel(output, allData);
    }
  }
  
  return allData;
}

/**
 * 追加行数据
 * @param {Array} targetData - 目标数据
 * @param {Array} sourceData - 源数据
 * @returns {Array} 合并后的数据
 */
function appendRows(targetData, sourceData) {
  return [...targetData, ...sourceData];
}

// 导出所有函数
module.exports = {
  readExcel,
  readCSV,
  writeExcel,
  writeCSV,
  cleanData,
  removeEmptyRows,
  removeDuplicates,
  transformColumns,
  filterRows,
  sortData,
  mergeFiles,
  appendRows
};
