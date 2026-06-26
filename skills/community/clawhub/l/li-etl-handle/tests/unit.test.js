/**
 * LI_excel_handle 单元测试套件
 * 运行：npm test 或 node tests/unit.test.js
 */

const excel = require('../index.js');
const fs = require('fs');
const path = require('path');

// 测试工具
let passCount = 0;
let failCount = 0;
const failures = [];

function assert(condition, message) {
  if (condition) {
    console.log('  ✓ ' + message);
    passCount++;
  } else {
    console.log('  ✗ ' + message);
    failCount++;
    failures.push(message);
  }
}

function assertThrows(fn, message) {
  try {
    fn();
    console.log('  ✗ ' + message + ' (未抛出错误)');
    failCount++;
    failures.push(message);
  } catch (e) {
    console.log('  ✓ ' + message + ' (抛出：' + e.message + ')');
    passCount++;
  }
}

// 测试数据
const sampleData = [
  { name: 'zhangsan', dept: 'sales', phone: '13800138000', amount: 5000, date: '2024-01-01' },
  { name: 'lisi', dept: 'tech', phone: '13900139000', amount: 3000, date: '2024-01-02' },
  { name: 'wangwu', dept: 'sales', phone: '13800138000', amount: 4000, date: '2024-01-03' },
  { name: 'zhaoliu', dept: 'hr', phone: '13700137000', amount: 2000, date: '2024-01-04' },
  { name: '', dept: '', phone: '', amount: '', date: '' },
  { name: 'sunqi', dept: 'tech', phone: '13600136000', amount: 6000, date: '2024-01-05' },
];

const testDir = path.join(__dirname, 'temp');
if (!fs.existsSync(testDir)) {
  fs.mkdirSync(testDir, { recursive: true });
}

console.log('LI_excel_handle Unit Tests\n');
console.log('============================================================');

// ==================== Read Tests ====================
console.log('\n1. Read Excel - Basic');
try {
  const testFile = path.join(testDir, 'test_read.xlsx');
  excel.writeExcel(sampleData, testFile);
  const { data, headers, sheetNames, totalRows } = excel.readExcel(testFile);
  assert(headers.length === 5, 'Header count is 5');
  assert(data.length === 6, 'Data rows is 6');
  assert(totalRows === 6, 'totalRows correct');
  assert(sheetNames.includes('Sheet1'), 'Contains Sheet1');
  assert(data[0].name === 'zhangsan', 'First row name correct');
  assert(data[0].amount === 5000, 'First row amount correct');
} catch (e) {
  console.log('  ✗ Read failed: ' + e.message);
  failCount++;
}

console.log('\n2. Read Excel - File not exists');
assertThrows(
  () => excel.readExcel('/nonexistent/file.xlsx'),
  'Throws error for nonexistent file'
);

// ==================== Write Tests ====================
console.log('\n3. Write Excel - Basic');
try {
  const outputFile = path.join(testDir, 'test_write.xlsx');
  excel.writeExcel(sampleData, outputFile);
  assert(fs.existsSync(outputFile), 'File created');
  const { data } = excel.readExcel(outputFile);
  assert(data.length === 6, 'Written data rows correct');
} catch (e) {
  console.log('  ✗ Write failed: ' + e.message);
  failCount++;
}

console.log('\n4. Write Excel - Custom sheet name');
try {
  const outputFile = path.join(testDir, 'test_write_custom.xlsx');
  excel.writeExcel(sampleData, outputFile, { sheetName: 'CustomSheet' });
  const { sheetNames } = excel.readExcel(outputFile);
  assert(sheetNames.includes('CustomSheet'), 'Custom sheet name correct');
} catch (e) {
  failCount++;
}

console.log('\n5. Write Excel - Empty data');
try {
  const outputFile = path.join(testDir, 'test_write_empty.xlsx');
  excel.writeExcel([], outputFile);
  assert(fs.existsSync(outputFile), 'Empty data file created');
} catch (e) {
  failCount++;
}

// ==================== Cleaning Tests ====================
console.log('\n6. Remove Duplicates - Single column');
try {
  const unique = excel.removeDuplicates(sampleData, 'phone');
  assert(unique.length === 5, 'Dedup result is 5 rows (got ' + unique.length + ')');
} catch (e) {
  console.log('  ✗ Dedup failed: ' + e.message);
  failCount++;
}

console.log('\n7. Remove Duplicates - Multiple columns');
try {
  const unique = excel.removeDuplicates(sampleData, ['dept', 'phone']);
  // zhangsan and wangwu have same dept+phone, so should be 5 rows
  assert(unique.length === 5, 'Multi-column dedup correct (got ' + unique.length + ')');
} catch (e) {
  failCount++;
}

console.log('\n8. Remove Empty Rows');
try {
  const cleaned = excel.removeEmptyRows(sampleData);
  assert(cleaned.length === 5, 'Empty rows removed (got ' + cleaned.length + ')');
} catch (e) {
  failCount++;
}

console.log('\n9. Clean Text');
try {
  const dataWithSpaces = [
    { name: '  zhangsan  ', addr: 'Beijing  Chaoyang' },
    { name: 'lisi', addr: 'Shanghai' }
  ];
  const cleaned = excel.cleanText(dataWithSpaces);
  assert(cleaned[0].name === 'zhangsan', 'Trim spaces correct');
  assert(cleaned[0].addr === 'Beijing Chaoyang', 'Remove extra spaces correct');
} catch (e) {
  failCount++;
}

console.log('\n10. Format Data - Phone mask');
try {
  const data = [{ phone: '13800138000' }];
  const formatted = excel.formatData(data, { phone: 'phone' });
  assert(formatted[0].phone === '138****8000', 'Phone mask correct (got ' + formatted[0].phone + ')');
} catch (e) {
  failCount++;
}

console.log('\n11. Format Data - Email mask');
try {
  const data = [{ email: 'test@example.com' }];
  const formatted = excel.formatData(data, { email: 'email' });
  assert(formatted[0].email.includes('***'), 'Email mask correct');
} catch (e) {
  failCount++;
}

console.log('\n12. Format Data - ID mask');
try {
  const data = [{ id: '110101199001011234' }];
  const formatted = excel.formatData(data, { id: 'id' });
  assert(formatted[0].id.includes('********'), 'ID mask correct');
} catch (e) {
  failCount++;
}

console.log('\n13. Format Data - Case conversion');
try {
  const data = [{ name: 'zhang san', status: 'ACTIVE' }];
  const formatted = excel.formatData(data, { name: 'upper', status: 'lower' });
  assert(formatted[0].name === 'ZHANG SAN', 'Uppercase correct');
  assert(formatted[0].status === 'active', 'Lowercase correct');
} catch (e) {
  failCount++;
}

// ==================== Transform Tests ====================
console.log('\n14. Transpose');
try {
  const data = [
    { name: 'zhangsan', age: 25 },
    { name: 'lisi', age: 30 }
  ];
  const transposed = excel.transpose(data);
  assert(transposed.length === 2, 'Transpose row count correct');
  assert(transposed[0].列名 === 'name', 'First row key correct (got ' + transposed[0].列名 + ')');
  assert(transposed[1].列名 === 'age', 'Second row key correct (got ' + transposed[1].列名 + ')');
} catch (e) {
  failCount++;
}

console.log('\n15. Excel to CSV');
try {
  const inputFile = path.join(testDir, 'test_convert.xlsx');
  const outputFile = path.join(testDir, 'test_convert.csv');
  excel.writeExcel(sampleData, inputFile);
  excel.excelToCSV(inputFile, outputFile);
  assert(fs.existsSync(outputFile), 'CSV file created');
  const csvContent = fs.readFileSync(outputFile, 'utf-8');
  assert(csvContent.includes('name'), 'CSV contains header');
  assert(csvContent.includes('zhangsan'), 'CSV contains data');
} catch (e) {
  failCount++;
}

// ==================== Analysis Tests ====================
console.log('\n16. Statistics');
try {
  const stats = excel.getStatistics(sampleData, 'amount');
  assert(stats.count === 6, 'Count correct (got ' + stats.count + ')');
  assert(stats.sum === 20000, 'Sum correct (got ' + stats.sum + ')');
  assert(stats.avg === 3333.33, 'Avg correct (got ' + stats.avg + ')');
  assert(stats.min === 0, 'Min correct');
  assert(stats.max === 6000, 'Max correct');
} catch (e) {
  failCount++;
}

console.log('\n17. Filter Data');
try {
  const filtered = excel.filterData(sampleData, row => row['amount'] > 3000);
  assert(filtered.length === 3, 'Filter result is 3 rows (got ' + filtered.length + ')');
} catch (e) {
  failCount++;
}

console.log('\n18. Filter Data - Multiple conditions');
try {
  const filtered = excel.filterData(sampleData, row => 
    row['dept'] === 'sales' && row['amount'] > 4000
  );
  assert(filtered.length === 1, 'Multi-condition filter correct');
} catch (e) {
  failCount++;
}

console.log('\n19. Sort Data - Ascending');
try {
  const sorted = excel.sortData(sampleData, [{ column: 'amount', order: 'asc' }]);
  // Empty string sorts before numbers, so first might be empty
  // Check that 2000 (the min non-empty) is before 6000 (the max)
  const amounts = sorted.map(r => r.amount);
  const nonEmptyIdx = amounts.findIndex(a => a !== '');
  assert(nonEmptyIdx >= 0, 'Has non-empty values');
  assert(amounts[nonEmptyIdx] === 2000, 'Min non-empty value first (got ' + amounts[nonEmptyIdx] + ')');
  assert(sorted[sorted.length - 1].amount === 6000, 'Max value last');
} catch (e) {
  failCount++;
}

console.log('\n20. Sort Data - Descending');
try {
  const sorted = excel.sortData(sampleData, [{ column: 'amount', order: 'desc' }]);
  assert(sorted[0].amount === 6000, 'Max value first');
} catch (e) {
  failCount++;
}

console.log('\n21. Group By - Sum');
try {
  const grouped = excel.groupBy(sampleData, 'dept', {
    'amount': 'sum'
  });
  // sales, tech, hr, and empty string = 4 groups
  assert(grouped.length === 4, 'Grouped into 4 depts (got ' + grouped.length + ')');
  const salesDept = grouped.find(g => g.dept === 'sales');
  assert(salesDept && salesDept.amount_sum === 9000, 'Sales dept sum correct (got ' + (salesDept ? salesDept.amount_sum : 'undefined') + ')');
} catch (e) {
  failCount++;
}

console.log('\n22. Group By - Multiple aggregations (separate calls)');
try {
  // Note: JS objects don't support duplicate keys, so test separately
  const groupedSum = excel.groupBy(sampleData, 'dept', { 'amount': 'sum' });
  const groupedCount = excel.groupBy(sampleData, 'dept', { 'amount': 'count' });
  const salesSum = groupedSum.find(g => g.dept === 'sales');
  const salesCount = groupedCount.find(g => g.dept === 'sales');
  assert(salesSum && salesSum.amount_sum === 9000, 'Sales dept sum correct');
  assert(salesCount && salesCount.amount_count === 2, 'Sales dept count correct');
} catch (e) {
  failCount++;
}

// ==================== Merge Tests ====================
console.log('\n23. Merge Excel Files');
try {
  const file1 = path.join(testDir, 'merge1.xlsx');
  const file2 = path.join(testDir, 'merge2.xlsx');
  const outputFile = path.join(testDir, 'merged.xlsx');
  
  excel.writeExcel(
    [{ name: 'zhangsan', dept: 'sales' }, { name: 'lisi', dept: 'tech' }],
    file1
  );
  excel.writeExcel(
    [{ name: 'wangwu', dept: 'hr' }, { name: 'zhaoliu', dept: 'finance' }],
    file2
  );
  
  excel.mergeExcelFiles([file1, file2], outputFile);
  
  const { data } = excel.readExcel(outputFile);
  assert(data.length === 4, 'Merged rows correct (got ' + data.length + ')');
} catch (e) {
  console.log('  ✗ Merge failed: ' + e.message);
  failCount++;
}

console.log('\n24. Merge Folder Excel');
try {
  const mergeDir = path.join(testDir, 'merge_folder');
  if (!fs.existsSync(mergeDir)) {
    fs.mkdirSync(mergeDir, { recursive: true });
  }
  
  for (let i = 1; i <= 3; i++) {
    const file = path.join(mergeDir, 'data' + i + '.xlsx');
    excel.writeExcel(
      [{ name: 'user' + i, value: i * 100 }],
      file
    );
  }
  
  const outputFile = path.join(testDir, 'folder_merged.xlsx');
  excel.mergeFolderExcel(mergeDir, outputFile);
  
  const { data } = excel.readExcel(outputFile);
  assert(data.length === 3, 'Folder merge correct (got ' + data.length + ')');
} catch (e) {
  console.log('  ✗ Folder merge failed: ' + e.message);
  failCount++;
}

// ==================== Edge Cases ====================
console.log('\n25. Empty Array');
try {
  const result = excel.removeDuplicates([], 'id');
  assert(result.length === 0, 'Empty array dedup returns empty');
} catch (e) {
  failCount++;
}

console.log('\n26. Single Row');
try {
  const singleData = [{ name: 'zhangsan', age: 25 }];
  const unique = excel.removeDuplicates(singleData, 'name');
  assert(unique.length === 1, 'Single row dedup correct');
} catch (e) {
  failCount++;
}

console.log('\n27. Special Characters');
try {
  const specialData = [
    { name: 'zhang@#$', note: 'has"quote"and,comma' },
    { name: 'lisi\nnewline', note: 'has\ttab' }
  ];
  const outputFile = path.join(testDir, 'special_chars.xlsx');
  excel.writeExcel(specialData, outputFile);
  const { data } = excel.readExcel(outputFile);
  assert(data.length === 2, 'Special chars handled');
} catch (e) {
  failCount++;
}

console.log('\n28. Big Numbers');
try {
  const bigNumberData = [
    { id: 123456789012345, amount: 999999999999 }
  ];
  const outputFile = path.join(testDir, 'big_numbers.xlsx');
  excel.writeExcel(bigNumberData, outputFile);
  const { data } = excel.readExcel(outputFile);
  assert(data.length === 1, 'Big numbers handled');
} catch (e) {
  failCount++;
}

// ==================== Performance Tests ====================
console.log('\n29. Performance - Write 1000 rows');
try {
  const largeData = [];
  for (let i = 0; i < 1000; i++) {
    largeData.push({
      id: i,
      name: 'user' + i,
      dept: ['sales', 'tech', 'hr'][i % 3],
      amount: Math.floor(Math.random() * 10000)
    });
  }
  
  const startTime = Date.now();
  const outputFile = path.join(testDir, 'large_data.xlsx');
  excel.writeExcel(largeData, outputFile);
  const writeTime = Date.now() - startTime;
  
  assert(writeTime < 5000, 'Write time ' + writeTime + 'ms < 5000ms');
  console.log('    Write time: ' + writeTime + 'ms');
} catch (e) {
  failCount++;
}

console.log('\n30. Performance - Read 1000 rows');
try {
  const inputFile = path.join(testDir, 'large_data.xlsx');
  const startTime = Date.now();
  const { data } = excel.readExcel(inputFile);
  const readTime = Date.now() - startTime;
  
  assert(data.length === 1000, 'Read rows correct (got ' + data.length + ')');
  assert(readTime < 2000, 'Read time ' + readTime + 'ms < 2000ms');
  console.log('    Read time: ' + readTime + 'ms');
} catch (e) {
  failCount++;
}

console.log('\n31. Performance - Dedup 1000 rows');
try {
  const largeData = [];
  for (let i = 0; i < 1000; i++) {
    largeData.push({
      id: i,
      phone: '138' + String(i).padStart(8, '0')
    });
  }
  
  const startTime = Date.now();
  const unique = excel.removeDuplicates(largeData, 'phone');
  const time = Date.now() - startTime;
  
  assert(unique.length === 1000, 'Dedup count correct');
  assert(time < 1000, 'Dedup time ' + time + 'ms < 1000ms');
  console.log('    Dedup time: ' + time + 'ms');
} catch (e) {
  failCount++;
}

// ==================== New Features Tests ====================
console.log('\n32. Concat Fields');
try {
  const concatData = [
    { firstName: 'John', lastName: 'Doe' },
    { firstName: 'Jane', lastName: 'Smith' }
  ];
  const concatenated = excel.concatFields(concatData, ['firstName', 'lastName'], 'fullName', ' ');
  assert(concatenated[0].fullName === 'John Doe', 'Concat result correct (got ' + concatenated[0].fullName + ')');
  assert(concatenated[1].fullName === 'Jane Smith', 'Concat result 2 correct');
} catch (e) {
  failCount++;
}

console.log('\n33. Value Mapping');
try {
  const mapData = [
    { gender: 'M' },
    { gender: 'F' },
    { gender: 'M' }
  ];
  const mapped = excel.valueMapping(mapData, 'gender', { 'M': 'Male', 'F': 'Female' });
  assert(mapped[0].gender === 'Male', 'Mapping correct (got ' + mapped[0].gender + ')');
  assert(mapped[1].gender === 'Female', 'Mapping 2 correct');
} catch (e) {
  failCount++;
}

console.log('\n34. Split Field');
try {
  const splitData = [
    { fullName: 'John Doe' },
    { fullName: 'Jane Smith' }
  ];
  const splitted = excel.splitField(splitData, 'fullName', ' ', ['firstName', 'lastName']);
  assert(splitted[0].firstName === 'John', 'Split firstName correct');
  assert(splitted[0].lastName === 'Doe', 'Split lastName correct');
  assert(splitted[0].fullName === undefined, 'Original field removed');
} catch (e) {
  failCount++;
}

console.log('\n35. Columns to Rows');
try {
  const colData = [
    { name: 'Alice', math: 90, english: 85 },
    { name: 'Bob', math: 88, english: 92 }
  ];
  const rowified = excel.columnsToRows(colData, ['name'], ['math', 'english'], 'subject', 'score');
  assert(rowified.length === 4, 'Rows count correct (got ' + rowified.length + ')');
  assert(rowified[0].subject === 'math', 'First subject correct');
  assert(rowified[0].score === 90, 'First score correct');
} catch (e) {
  failCount++;
}

console.log('\n36. Rows to Columns');
try {
  const rowData = [
    { name: 'Alice', subject: 'math', score: 90 },
    { name: 'Alice', subject: 'english', score: 85 },
    { name: 'Bob', subject: 'math', score: 88 },
    { name: 'Bob', subject: 'english', score: 92 }
  ];
  const colified = excel.rowsToColumns(rowData, 'name', 'subject', 'score');
  assert(colified.length === 2, 'Groups count correct');
  assert(colified[0].math === 90, 'Alice math score correct');
  assert(colified[0].english === 85, 'Alice english score correct');
} catch (e) {
  failCount++;
}

console.log('\n37. Replace NULL');
try {
  const nullData = [
    { name: 'Alice', age: '' },
    { name: 'Bob', age: 25 },
    { name: 'Charlie', age: null }
  ];
  const replaced = excel.replaceNull(nullData, { age: 0 });
  assert(replaced[0].age === 0, 'Empty string replaced');
  assert(replaced[1].age === 25, 'Existing value kept');
  assert(replaced[2].age === 0, 'Null replaced');
} catch (e) {
  failCount++;
}

// ==================== Join Tests ====================
console.log('\n38. Inner Join');
try {
  const left = [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }];
  const right = [{ id: 1, dept: 'Sales' }, { id: 3, dept: 'Tech' }];
  const joined = excel.innerJoin(left, right, 'id', 'id');
  assert(joined.length === 1, 'Inner join result count');
  assert(joined[0].name === 'Alice' && joined[0].dept === 'Sales', 'Inner join data correct');
} catch (e) {
  failCount++;
}

console.log('\n39. Left Join');
try {
  const left = [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }];
  const right = [{ id: 1, dept: 'Sales' }];
  const joined = excel.leftJoin(left, right, 'id', 'id');
  assert(joined.length === 2, 'Left join result count');
  assert(joined[1].name === 'Bob' && joined[1].dept === '', 'Left join unmatched correct');
} catch (e) {
  failCount++;
}

console.log('\n40. Switch/Case');
try {
  const data = [{ dept: 'Sales' }, { dept: 'Tech' }, { dept: 'HR' }];
  const result = excel.switchCase(data, 'dept', { 'Sales': 'A', 'Tech': 'B' }, 'Other');
  assert(result[0].case_result === 'A', 'Switch case A correct');
  assert(result[1].case_result === 'B', 'Switch case B correct');
  assert(result[2].case_result === 'Other', 'Switch case default correct');
} catch (e) {
  failCount++;
}

console.log('\n41. If-Else');
try {
  const data = [{ score: 90 }, { score: 80 }, { score: 70 }];
  const result = excel.ifElse(
    data,
    row => row.score >= 85,
    row => ({ ...row, level: 'High' }),
    row => ({ ...row, level: 'Low' })
  );
  assert(result[0].level === 'High', 'If condition met');
  assert(result[1].level === 'Low', 'Else condition met');
} catch (e) {
  failCount++;
}

console.log('\n42. Execute Script');
try {
  const data = [{ price: 100 }, { price: 200 }];
  const result = excel.executeScript(data, (row) => ({ ...row, doubled: row.price * 2 }));
  assert(result[0].doubled === 200, 'Script execution correct');
  assert(result[1].doubled === 400, 'Script execution 2 correct');
} catch (e) {
  failCount++;
}

// ==================== Summary ====================
console.log('\n============================================================');
console.log('Test Summary');
console.log('============================================================');
console.log('Pass: ' + passCount);
console.log('Fail: ' + failCount);
console.log('Rate: ' + ((passCount / (passCount + failCount)) * 100).toFixed(1) + '%');

if (failures.length > 0) {
  console.log('\nFailed tests:');
  failures.forEach((f, i) => {
    console.log('  ' + (i + 1) + '. ' + f);
  });
}

console.log('\n');

process.exit(failCount > 0 ? 1 : 0);
