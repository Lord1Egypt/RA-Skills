/**
 * LI_excel_handle - Excel 自动化处理技能
 * 支持读取、写入、清洗、转换、合并 Excel 文件
 */

const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');
const csvParser = require('csv-parser');
const { stringify } = require('csv-stringify/sync');

// ==================== 工具函数 ====================

/**
 * 确保目录存在
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * 生成输出文件路径
 */
function getOutputPath(inputPath, suffix = '_processed') {
  const dir = path.dirname(inputPath);
  const name = path.basename(inputPath, path.extname(inputPath));
  const ext = path.extname(inputPath);
  return path.join(dir, `${name}${suffix}${ext}`);
}

/**
 * 数据脱敏处理
 */
function maskSensitiveData(value, type = 'auto') {
  if (value === null || value === undefined) return value;
  
  const str = String(value);
  
  // 身份证号 (18 位)
  if (type === 'id' || /^\d{17}[\dXx]$/.test(str)) {
    return str.replace(/(\d{6})\d{8}(\d{4})/, '$1********$2');
  }
  
  // 手机号 (11 位)
  if (type === 'phone' || /^1[3-9]\d{9}$/.test(str)) {
    return str.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
  }
  
  // 邮箱
  if (type === 'email' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str)) {
    return str.replace(/([^\s@]{2})[^\s@]*(@)/, '$1***$2');
  }
  
  return value;
}

// ==================== 读取功能 ====================

/**
 * 读取 Excel 文件
 * @param {string} filePath - 文件路径
 * @param {object} options - 选项：sheetName, sheetIndex, range
 * @returns {object} { data: [], headers: [], sheetNames: [] }
 */
function readExcel(filePath, options = {}) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`文件不存在：${filePath}`);
  }
  
  const workbook = XLSX.readFile(filePath);
  const sheetNames = workbook.SheetNames;
  
  let sheetName = options.sheetName;
  if (!sheetName) {
    const index = options.sheetIndex !== undefined ? options.sheetIndex : 0;
    sheetName = sheetNames[index];
  }
  
  if (!sheetName || !workbook.Sheets[sheetName]) {
    throw new Error(`工作表不存在：${sheetName}`);
  }
  
  const sheet = workbook.Sheets[sheetName];
  const range = options.range ? XLSX.utils.decode_range(options.range) : null;
  
  const data = XLSX.utils.sheet_to_json(sheet, {
    range: range,
    header: 1, // 返回数组数组
    defval: ''
  });
  
  if (data.length === 0) {
    return { data: [], headers: [], sheetNames };
  }
  
  // 第一行作为表头
  const headers = data[0];
  const rows = data.slice(1).map(row => {
    const obj = {};
    headers.forEach((header, i) => {
      obj[header] = row[i] !== undefined ? row[i] : '';
    });
    return obj;
  });
  
  return {
    data: rows,
    headers: headers.filter(h => h !== undefined && h !== ''),
    sheetNames,
    totalRows: rows.length
  };
}

/**
 * 读取 CSV 文件
 * @param {string} filePath - 文件路径
 * @returns {Promise<object>} { data: [], headers: [] }
 */
function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(filePath)) {
      reject(new Error(`文件不存在：${filePath}`));
      return;
    }
    
    const results = [];
    let headers = [];
    
    fs.createReadStream(filePath)
      .pipe(csvParser())
      .on('headers', (hdrs) => {
        headers = hdrs;
      })
      .on('data', (data) => {
        results.push(data);
      })
      .on('end', () => {
        resolve({
          data: results,
          headers,
          totalRows: results.length
        });
      })
      .on('error', reject);
  });
}

// ==================== 写入功能 ====================

/**
 * 写入 Excel 文件
 * @param {array} data - 数据数组（对象数组）
 * @param {string} outputPath - 输出文件路径
 * @param {object} options - 选项：sheetName, headers
 */
function writeExcel(data, outputPath, options = {}) {
  ensureDir(path.dirname(outputPath));
  
  const headers = options.headers || (data.length > 0 ? Object.keys(data[0]) : []);
  
  // 转换为二维数组
  const wsData = [headers];
  data.forEach(row => {
    wsData.push(headers.map(h => row[h] !== undefined ? row[h] : ''));
  });
  
  const ws = XLSX.utils.aoa_to_sheet(wsData);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, options.sheetName || 'Sheet1');
  
  XLSX.writeFile(wb, outputPath);
  console.log(`✓ 文件已保存：${outputPath}`);
  return outputPath;
}

/**
 * 写入 CSV 文件
 * @param {array} data - 数据数组
 * @param {string} outputPath - 输出文件路径
 */
function writeCSV(data, outputPath) {
  ensureDir(path.dirname(outputPath));
  
  if (data.length === 0) {
    fs.writeFileSync(outputPath, '');
    return outputPath;
  }
  
  const headers = Object.keys(data[0]);
  const output = stringify(data, {
    header: true,
    columns: headers
  });
  
  fs.writeFileSync(outputPath, output);
  console.log(`✓ 文件已保存：${outputPath}`);
  return outputPath;
}

// ==================== 数据清洗 ====================

/**
 * 数据去重
 * @param {array} data - 数据数组
 * @param {array|string} keys - 去重键（单列或数组）
 * @returns {array} 去重后的数据
 */
function removeDuplicates(data, keys) {
  if (!Array.isArray(keys)) {
    keys = [keys];
  }
  
  const seen = new Set();
  const result = [];
  
  for (const row of data) {
    const key = keys.map(k => row[k]).join('|');
    if (!seen.has(key)) {
      seen.add(key);
      result.push(row);
    }
  }
  
  console.log(`✓ 去重完成：${data.length} → ${result.length} 行 (移除${data.length - result.length}行重复)`);
  return result;
}

/**
 * 删除空行
 * @param {array} data - 数据数组
 * @param {object} options - 选项：checkAllColumns (检查所有列还是特定列)
 * @returns {array} 清理后的数据
 */
function removeEmptyRows(data, options = {}) {
  const result = data.filter(row => {
    if (options.columns) {
      // 检查指定列 - 任一指定列非空就保留
      return options.columns.some(col => row[col] !== '' && row[col] !== null && row[col] !== undefined);
    } else {
      // 检查所有列 - 任一列非空就保留
      return Object.values(row).some(val => val !== '' && val !== null && val !== undefined);
    }
  });
  
  console.log(`✓ 删除空行完成：${data.length} → ${result.length} 行`);
  return result;
}

/**
 * 文本清理
 * @param {array} data - 数据数组
 * @param {array} columns - 要清理的列（不传则清理所有文本列）
 * @returns {array} 清理后的数据
 */
function cleanText(data, columns = null) {
  const colsToClean = columns || Object.keys(data[0]);
  const result = data.map(row => {
    const newRow = { ...row };
    
    colsToClean.forEach(col => {
      if (typeof newRow[col] === 'string') {
        // 去除首尾空格
        newRow[col] = newRow[col].trim();
        // 去除多余空格
        newRow[col] = newRow[col].replace(/\s+/g, ' ');
      }
    });
    
    return newRow;
  });
  
  console.log(`✓ 文本清理完成：处理${colsToClean.length}列`);
  return result;
}

/**
 * 格式标准化
 * @param {array} data - 数据数组
 * @param {object} rules - 格式化规则 { columnName: 'phone'|'email'|'date'|'number' }
 * @returns {array} 格式化后的数据
 */
function formatData(data, rules) {
  const result = data.map(row => {
    const newRow = { ...row };
    
    for (const [col, format] of Object.entries(rules)) {
      let value = newRow[col];
      if (value === '' || value === null || value === undefined) continue;
      
      switch (format) {
        case 'phone':
          newRow[col] = maskSensitiveData(value, 'phone');
          break;
        case 'email':
          newRow[col] = maskSensitiveData(value, 'email');
          break;
        case 'id':
          newRow[col] = maskSensitiveData(value, 'id');
          break;
        case 'upper':
          newRow[col] = String(value).toUpperCase();
          break;
        case 'lower':
          newRow[col] = String(value).toLowerCase();
          break;
        case 'number':
          newRow[col] = Number(value) || 0;
          break;
        default:
          break;
      }
    }
    
    return newRow;
  });
  
  console.log(`✓ 格式标准化完成：应用${Object.keys(rules).length}个格式规则`);
  return result;
}

// ==================== 数据转换 ====================

/**
 * CSV 转 Excel
 * @param {string} inputPath - CSV 文件路径
 * @param {string} outputPath - 输出 Excel 路径
 */
async function csvToExcel(inputPath, outputPath) {
  const { data } = await readCSV(inputPath);
  writeExcel(data, outputPath || getOutputPath(inputPath, '.xlsx').replace('.csv', ''));
  return outputPath;
}

/**
 * Excel 转 CSV
 * @param {string} inputPath - Excel 文件路径
 * @param {string} outputPath - 输出 CSV 路径
 * @param {object} options - 选项：sheetName, sheetIndex
 */
function excelToCSV(inputPath, outputPath, options = {}) {
  const { data } = readExcel(inputPath, options);
  writeCSV(data, outputPath || getOutputPath(inputPath, '.csv').replace('.xlsx', '').replace('.xls', ''));
  return outputPath;
}

/**
 * 行列转置
 * @param {array} data - 数据数组
 * @returns {array} 转置后的数据
 */
function transpose(data) {
  if (data.length === 0) return [];
  
  const headers = Object.keys(data[0]);
  const result = [];
  
  headers.forEach(header => {
    const newRow = { 列名: header };
    data.forEach((row, i) => {
      newRow[`第${i + 1}行`] = row[header];
    });
    result.push(newRow);
  });
  
  console.log(`✓ 行列转置完成：${headers.length}列 × ${data.length}行 → ${result.length}列 × ${headers.length}行`);
  return result;
}

// ==================== 数据合并 ====================

/**
 * 合并多个 Excel 文件（纵向）
 * @param {array} filePaths - 文件路径数组
 * @param {string} outputPath - 输出文件路径
 * @param {object} options - 选项：sheetName
 */
function mergeExcelFiles(filePaths, outputPath, options = {}) {
  const allData = [];
  let headers = null;
  
  filePaths.forEach(filePath => {
    console.log(`正在读取：${filePath}`);
    const { data, headers: fileHeaders } = readExcel(filePath, options);
    
    if (!headers) {
      headers = fileHeaders;
    }
    
    // 确保列一致
    data.forEach(row => {
      const normalizedRow = {};
      headers.forEach(h => {
        normalizedRow[h] = row[h] !== undefined ? row[h] : '';
      });
      allData.push(normalizedRow);
    });
  });
  
  writeExcel(allData, outputPath);
  console.log(`✓ 合并完成：${filePaths.length}个文件 → ${allData.length}行`);
  return outputPath;
}

/**
 * 批量合并文件夹中的 Excel 文件
 * @param {string} folderPath - 文件夹路径
 * @param {string} outputPath - 输出文件路径
 * @param {object} options - 选项：pattern, sheetName
 */
function mergeFolderExcel(folderPath, outputPath, options = {}) {
  const pattern = options.pattern || /\.xlsx?$/i;
  const files = fs.readdirSync(folderPath)
    .filter(f => pattern.test(f))
    .map(f => path.join(folderPath, f));
  
  if (files.length === 0) {
    throw new Error(`文件夹中没有找到 Excel 文件：${folderPath}`);
  }
  
  return mergeExcelFiles(files, outputPath, options);
}

// ==================== 数据分析 ====================

/**
 * 基础统计
 * @param {array} data - 数据数组
 * @param {string} column - 统计列
 * @returns {object} 统计结果
 */
function getStatistics(data, column) {
  const values = data
    .map(row => Number(row[column]))
    .filter(v => !isNaN(v));
  
  if (values.length === 0) {
    return { count: 0, sum: 0, avg: 0, min: 0, max: 0 };
  }
  
  const sum = values.reduce((a, b) => a + b, 0);
  const avg = sum / values.length;
  const min = Math.min(...values);
  const max = Math.max(...values);
  
  return {
    count: values.length,
    sum,
    avg: Number(avg.toFixed(2)),
    min,
    max
  };
}

/**
 * 数据筛选
 * @param {array} data - 数据数组
 * @param {function} condition - 筛选条件函数
 * @returns {array} 筛选后的数据
 */
function filterData(data, condition) {
  const result = data.filter(condition);
  console.log(`✓ 筛选完成：${data.length} → ${result.length} 行`);
  return result;
}

/**
 * 数据排序
 * @param {array} data - 数据数组
 * @param {array} sortRules - 排序规则 [{ column: 'name', order: 'asc' }]
 * @returns {array} 排序后的数据
 */
function sortData(data, sortRules) {
  const result = [...data].sort((a, b) => {
    for (const { column, order = 'asc' } of sortRules) {
      const aVal = a[column];
      const bVal = b[column];
      
      let comparison = 0;
      if (typeof aVal === 'number' && typeof bVal === 'number') {
        comparison = aVal - bVal;
      } else {
        comparison = String(aVal).localeCompare(String(bVal));
      }
      
      if (comparison !== 0) {
        return order === 'desc' ? -comparison : comparison;
      }
    }
    return 0;
  });
  
  console.log(`✓ 排序完成：按${sortRules.map(r => r.column).join(', ')}排序`);
  return result;
}

/**
 * 分组聚合
 * @param {array} data - 数据数组
 * @param {string} groupBy - 分组列
 * @param {object} aggregations - 聚合规则 { column: 'sum'|'count'|'avg' }
 * @returns {array} 聚合结果
 */
function groupBy(data, groupBy, aggregations) {
  const groups = {};
  
  data.forEach(row => {
    const key = row[groupBy];
    if (!groups[key]) {
      groups[key] = [];
    }
    groups[key].push(row);
  });
  
  const result = Object.entries(groups).map(([groupValue, rows]) => {
    const resultRow = { [groupBy]: groupValue };
    
    for (const [col, aggFunc] of Object.entries(aggregations)) {
      const values = rows.map(r => Number(r[col])).filter(v => !isNaN(v));
      
      switch (aggFunc) {
        case 'sum':
          resultRow[`${col}_sum`] = values.reduce((a, b) => a + b, 0);
          break;
        case 'count':
          resultRow[`${col}_count`] = values.length;
          break;
        case 'avg':
          resultRow[`${col}_avg`] = values.length > 0 ? (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2) : 0;
          break;
        case 'min':
          resultRow[`${col}_min`] = values.length > 0 ? Math.min(...values) : 0;
          break;
        case 'max':
          resultRow[`${col}_max`] = values.length > 0 ? Math.max(...values) : 0;
          break;
      }
    }
    
    return resultRow;
  });
  
  console.log(`✓ 分组聚合完成：按"${groupBy}"分为${result.length}组`);
  return result;
}

// ==================== 字段拼接 ====================

/**
 * 字段拼接（Concat fields）
 * 将多个字段连接成一个新字段
 * @param {array} data - 数据数组
 * @param {array} fields - 要拼接的字段列表
 * @param {string} newField - 新字段名
 * @param {string} separator - 分隔符（默认空字符串）
 * @param {boolean} removeOld - 是否删除原字段（默认 false）
 * @returns {array} 处理后的数据
 */
function concatFields(data, fields, newField, separator = '', removeOld = false) {
  const result = data.map(row => {
    const newRow = { ...row };
    const values = fields.map(f => row[f] !== undefined ? row[f] : '');
    newRow[newField] = values.join(separator);
    
    if (removeOld) {
      fields.forEach(f => delete newRow[f]);
    }
    
    return newRow;
  });
  
  console.log(`✓ 字段拼接完成：${fields.join(separator)} → ${newField}`);
  return result;
}

// ==================== 值映射 ====================

/**
 * 值映射（Value Mapping）
 * 将字段的值映射成其他值
 * @param {array} data - 数据数组
 * @param {string} field - 要映射的字段
 * @param {object} mapping - 映射规则 { '原值': '新值' }
 * @param {string} newField - 新字段名（不传则覆盖原字段）
 * @param {any} defaultValue - 默认值（不在映射中的值使用此值）
 * @returns {array} 处理后的数据
 */
function valueMapping(data, field, mapping, newField = null, defaultValue = null) {
  const targetField = newField || field;
  
  const result = data.map(row => {
    const newRow = { ...row };
    const value = row[field];
    
    if (mapping.hasOwnProperty(value)) {
      newRow[targetField] = mapping[value];
    } else {
      newRow[targetField] = defaultValue !== null ? defaultValue : value;
    }
    
    return newRow;
  });
  
  const mapDesc = Object.entries(mapping).map(([k, v]) => `${k}→${v}`).join(', ');
  console.log(`✓ 值映射完成：${field} (${mapDesc})`);
  return result;
}

// ==================== 字段拆分 ====================

/**
 * 字段拆分（Split Field）
 * 按分隔符拆分字段成多个字段
 * @param {array} data - 数据数组
 * @param {string} field - 要拆分的字段
 * @param {string} separator - 分隔符
 * @param {array} newFields - 新字段名列表
 * @param {boolean} removeOld - 是否删除原字段（默认 true）
 * @returns {array} 处理后的数据
 */
function splitField(data, field, separator, newFields, removeOld = true) {
  const result = data.map(row => {
    const newRow = { ...row };
    const value = row[field] !== undefined ? row[field] : '';
    const parts = String(value).split(separator);
    
    newFields.forEach((newField, i) => {
      newRow[newField] = parts[i] !== undefined ? parts[i] : '';
    });
    
    if (removeOld) {
      delete newRow[field];
    }
    
    return newRow;
  });
  
  console.log(`✓ 字段拆分完成：${field} → ${newFields.join(', ')}`);
  return result;
}

// ==================== 列转行 ====================

/**
 * 列转行（Columns to Rows）
 * 将多列转换为多行
 * @param {array} data - 数据数组
 * @param {array} keyFields - 保持不变的字段（分组字段）
 * @param {array} valueFields - 要转换的字段
 * @param {string} keyName - 新列名字段名（默认 'variable'）
 * @param {string} valueName - 新值字段名（默认 'value'）
 * @returns {array} 处理后的数据
 */
function columnsToRows(data, keyFields, valueFields, keyName = 'variable', valueName = 'value') {
  const result = [];
  
  data.forEach(row => {
    valueFields.forEach(field => {
      const newRow = {};
      keyFields.forEach(kf => {
        newRow[kf] = row[kf];
      });
      newRow[keyName] = field;
      newRow[valueName] = row[field] !== undefined ? row[field] : '';
      result.push(newRow);
    });
  });
  
  console.log(`✓ 列转行完成：${valueFields.length}列 × ${data.length}行 → ${result.length}行`);
  return result;
}

// ==================== 行转列 ====================

/**
 * 行转列（Rows to Columns）
 * 将多行转换为多列（需要指定分组字段和透视字段）
 * @param {array} data - 数据数组
 * @param {string} groupField - 分组字段
 * @param {string} keyField - 列名字段（该字段的值会变成新列名）
 * @param {string} valueField - 值字段（该字段的值会变成新列的值）
 * @returns {array} 处理后的数据
 */
function rowsToColumns(data, groupField, keyField, valueField) {
  const groups = {};
  const allKeys = new Set();
  
  // 分组并收集所有键
  data.forEach(row => {
    const groupKey = row[groupField];
    const colKey = row[keyField];
    
    if (!groups[groupKey]) {
      groups[groupKey] = {};
    }
    groups[groupKey][colKey] = row[valueField];
    allKeys.add(colKey);
  });
  
  // 转换为结果
  const sortedKeys = Array.from(allKeys).sort();
  const result = Object.entries(groups).map(([groupKey, values]) => {
    const row = { [groupField]: groupKey };
    sortedKeys.forEach(key => {
      row[key] = values[key] !== undefined ? values[key] : '';
    });
    return row;
  });
  
  console.log(`✓ 行转列完成：${Object.keys(groups).length}组 × ${sortedKeys.length}列`);
  return result;
}

// ==================== NULL 替换 ====================

/**
 * 替换 NULL 值
 * 将空值替换成指定值
 * @param {array} data - 数据数组
 * @param {object} replacements - 替换规则 { '字段名': 替换值 }
 * @returns {array} 处理后的数据
 */
function replaceNull(data, replacements) {
  const result = data.map(row => {
    const newRow = { ...row };
    
    for (const [field, replaceValue] of Object.entries(replacements)) {
      if (newRow[field] === '' || newRow[field] === null || newRow[field] === undefined) {
        newRow[field] = replaceValue;
      }
    }
    
    return newRow;
  });
  
  const fields = Object.keys(replacements).join(', ');
  console.log(`✓ NULL 替换完成：字段 ${fields}`);
  return result;
}

// ==================== 多表连接 ====================

/**
 * 内连接（Inner Join）
 * 只返回两个表中匹配的字段
 */
function innerJoin(leftData, rightData, leftKey, rightKey) {
  const result = [];
  const rightMap = new Map();
  
  rightData.forEach(row => {
    const key = row[rightKey];
    if (!rightMap.has(key)) rightMap.set(key, []);
    rightMap.get(key).push(row);
  });
  
  leftData.forEach(leftRow => {
    const key = leftRow[leftKey];
    const rightRows = rightMap.get(key) || [];
    rightRows.forEach(rightRow => {
      result.push({ ...leftRow, ...rightRow });
    });
  });
  
  console.log(`✓ 内连接完成：${leftData.length} × ${rightData.length} → ${result.length} 行`);
  return result;
}

/**
 * 左连接（Left Join）
 * 返回左表所有记录，右表匹配不到的为空
 */
function leftJoin(leftData, rightData, leftKey, rightKey) {
  const result = [];
  const rightMap = new Map();
  const rightFields = rightData.length > 0 ? Object.keys(rightData[0]) : [];
  
  rightData.forEach(row => {
    const key = row[rightKey];
    if (!rightMap.has(key)) rightMap.set(key, []);
    rightMap.get(key).push(row);
  });
  
  leftData.forEach(leftRow => {
    const key = leftRow[leftKey];
    const rightRows = rightMap.get(key) || [];
    
    if (rightRows.length === 0) {
      const merged = { ...leftRow };
      rightFields.forEach(f => merged[f] = '');
      result.push(merged);
    } else {
      rightRows.forEach(rightRow => result.push({ ...leftRow, ...rightRow }));
    }
  });
  
  console.log(`✓ 左连接完成：${leftData.length} × ${rightData.length} → ${result.length} 行`);
  return result;
}

/**
 * 右连接（Right Join）
 * 返回右表所有记录，左表匹配不到的为空
 */
function rightJoin(leftData, rightData, leftKey, rightKey) {
  const result = [];
  const leftMap = new Map();
  const leftFields = leftData.length > 0 ? Object.keys(leftData[0]) : [];
  
  leftData.forEach(row => {
    const key = row[leftKey];
    if (!leftMap.has(key)) leftMap.set(key, []);
    leftMap.get(key).push(row);
  });
  
  rightData.forEach(rightRow => {
    const key = rightRow[rightKey];
    const leftRows = leftMap.get(key) || [];
    
    if (leftRows.length === 0) {
      const merged = { ...rightRow };
      leftFields.forEach(f => merged[f] = '');
      result.push(merged);
    } else {
      leftRows.forEach(leftRow => result.push({ ...leftRow, ...rightRow }));
    }
  });
  
  console.log(`✓ 右连接完成：${leftData.length} × ${rightData.length} → ${result.length} 行`);
  return result;
}

/**
 * 全外连接（Full Outer Join）
 * 返回两个表的所有记录
 */
function fullOuterJoin(leftData, rightData, leftKey, rightKey) {
  const result = [];
  const leftMap = new Map();
  const rightMap = new Map();
  const leftFields = leftData.length > 0 ? Object.keys(leftData[0]) : [];
  const rightFields = rightData.length > 0 ? Object.keys(rightData[0]) : [];
  
  leftData.forEach(row => {
    const key = row[leftKey];
    if (!leftMap.has(key)) leftMap.set(key, []);
    leftMap.get(key).push(row);
  });
  
  rightData.forEach(row => {
    const key = row[rightKey];
    if (!rightMap.has(key)) rightMap.set(key, []);
    rightMap.get(key).push(row);
  });
  
  leftData.forEach(leftRow => {
    const key = leftRow[leftKey];
    const rightRows = rightMap.get(key) || [];
    
    if (rightRows.length === 0) {
      const merged = { ...leftRow };
      rightFields.forEach(f => merged[f] = '');
      result.push(merged);
    } else {
      rightRows.forEach(rightRow => result.push({ ...leftRow, ...rightRow }));
    }
  });
  
  rightData.forEach(rightRow => {
    const key = rightRow[rightKey];
    if (!leftMap.has(key)) {
      const merged = { ...rightRow };
      leftFields.forEach(f => merged[f] = '');
      result.push(merged);
    }
  });
  
  console.log(`✓ 全外连接完成：${leftData.length} × ${rightData.length} → ${result.length} 行`);
  return result;
}

/**
 * 交叉连接（Cross Join）
 * 返回两个表的笛卡尔积
 */
function crossJoin(leftData, rightData) {
  const result = [];
  leftData.forEach(leftRow => {
    rightData.forEach(rightRow => {
      result.push({ ...leftRow, ...rightRow });
    });
  });
  console.log(`✓ 交叉连接完成：${leftData.length} × ${rightData.length} → ${result.length} 行`);
  return result;
}

// ==================== 流程控制 ====================

/**
 * Switch/Case 数据分类
 */
function switchCase(data, field, cases, defaultCase = 'default', outputField = 'case_result') {
  const result = data.map(row => {
    const newRow = { ...row };
    const value = row[field];
    newRow[outputField] = cases.hasOwnProperty(value) ? cases[value] : defaultCase;
    return newRow;
  });
  console.log(`✓ Switch/Case 完成：${Object.keys(cases).length} 个分支`);
  return result;
}

/**
 * 条件执行（If-Else）
 */
function ifElse(data, condition, ifFn, elseFn = null) {
  const result = data.map(row => {
    if (condition(row)) {
      return ifFn(row);
    } else if (elseFn) {
      return elseFn(row);
    }
    return row;
  });
  const ifCount = data.filter(row => condition(row)).length;
  console.log(`✓ If-Else 完成：${ifCount}/${data.length} 满足条件`);
  return result;
}

// ==================== 脚本支持 ====================

/**
 * 执行 JavaScript 脚本处理数据
 */
function executeScript(data, scriptFn) {
  const result = data.map((row, index) => {
    try {
      return scriptFn(row, index, data);
    } catch (e) {
      console.log(`⚠️ 脚本执行错误 (行${index}): ${e.message}`);
      return row;
    }
  });
  console.log(`✓ 脚本执行完成：处理${data.length}行`);
  return result;
}

/**
 * 写日志（调试用）
 */
function writeLog(data, message = '', limit = 10) {
  console.log(`\n📝 ${message || '数据日志'} (${data.length}行):`);
  data.slice(0, limit).forEach((row, i) => {
    console.log(`  [${i}] ${JSON.stringify(row)}`);
  });
  if (data.length > limit) console.log(`  ... 还有 ${data.length - limit} 行`);
  console.log('');
  return data;
}

// ==================== 导出接口 ====================

module.exports = {
  // 读取
  readExcel,
  readCSV,
  
  // 写入
  writeExcel,
  writeCSV,
  
  // 清洗
  removeDuplicates,
  removeEmptyRows,
  cleanText,
  formatData,
  replaceNull,
  
  // 转换
  csvToExcel,
  excelToCSV,
  transpose,
  concatFields,
  valueMapping,
  splitField,
  columnsToRows,
  rowsToColumns,
  
  // 合并
  mergeExcelFiles,
  mergeFolderExcel,
  
  // 分析
  getStatistics,
  filterData,
  sortData,
  groupBy,
  
  // 连接
  innerJoin,
  leftJoin,
  rightJoin,
  fullOuterJoin,
  crossJoin,
  
  // 流程
  switchCase,
  ifElse,
  
  // 脚本
  executeScript,
  writeLog,
  
  // 工具
  maskSensitiveData,
  getOutputPath
};
