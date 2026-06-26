/**
 * LI_excel_handle 真实场景测试套件
 * 模拟实际办公场景，验证功能完整性
 * 运行：node tests/scenario.test.js
 */

const excel = require('../index.js');
const fs = require('fs');
const path = require('path');

const testDir = path.join(__dirname, 'scenarios');
if (!fs.existsSync(testDir)) {
  fs.mkdirSync(testDir, { recursive: true });
}

console.log('LI_excel_handle Scenario Tests\n');
console.log('============================================================');

let passCount = 0;
let failCount = 0;

function runScenario(name, fn) {
  console.log('\nScenario ' + (passCount + failCount + 1) + ': ' + name);
  console.log('------------------------------------------------------------');
  try {
    fn();
    console.log('PASS: Scenario completed');
    passCount++;
  } catch (e) {
    console.log('FAIL: ' + e.message);
    console.log(e.stack);
    failCount++;
  }
}

// ==================== Scenario 1: Customer Data Cleaning ====================
runScenario('Customer Data Cleaning and Masking', () => {
  console.log('Background: Sales dept provided customer data with duplicates and sensitive info');
  
  const rawData = [
    { name: 'Zhang San', phone: '13800138000', email: 'zhangsan@example.com', id: '110101199001011234', city: 'Beijing' },
    { name: 'Li Si', phone: '13900139000', email: 'lisi@example.com', id: '310101199502022345', city: 'Shanghai' },
    { name: 'Zhang San', phone: '13800138000', email: 'zhangsan@example.com', id: '110101199001011234', city: 'Beijing' }, // Duplicate
    { name: 'Wang Wu', phone: '13700137000', email: 'wangwu@example.com', id: '440101198803033456', city: 'Guangzhou' },
    { name: '', phone: '', email: '', id: '', city: '' }, // Empty row
    { name: 'Zhao Liu', phone: '13600136000', email: 'zhaoliu@example.com', id: '510101199204044567', city: 'Chengdu' },
  ];
  
  console.log('Raw data: ' + rawData.length + ' rows');
  
  // Step 1: Remove empty rows
  const step1 = excel.removeEmptyRows(rawData);
  console.log('After removing empty: ' + step1.length + ' rows');
  
  // Step 2: Dedup by phone
  const step2 = excel.removeDuplicates(step1, 'phone');
  console.log('After dedup: ' + step2.length + ' rows');
  
  // Step 3: Mask sensitive info
  const step3 = excel.formatData(step2, {
    'phone': 'phone',
    'email': 'email',
    'id': 'id'
  });
  console.log('Sensitive info masked');
  
  // Step 4: Save result
  const outputFile = path.join(testDir, 'scenario1_customers_clean.xlsx');
  excel.writeExcel(step3, outputFile);
  
  // Verify
  const { data } = excel.readExcel(outputFile);
  if (data.length !== 4) throw new Error('Expected 4 rows, got ' + data.length);
  if (!data[0].phone.includes('****')) throw new Error('Phone not masked');
  if (!data[0].id.includes('********')) throw new Error('ID not masked');
  
  console.log('Output: ' + outputFile);
  console.log('Masked phone example: ' + data[0].phone);
});

// ==================== Scenario 2: Multi-Region Sales Report Merge ====================
runScenario('Multi-Region Sales Report Merge', () => {
  console.log('Background: Regional sales reports need to be merged and analyzed');
  
  const regions = {
    'North': [
      { date: '2024-01', sales: 'Zhang San', product: 'Product A', amount: 5000, profit: 1500 },
      { date: '2024-01', sales: 'Li Si', product: 'Product B', amount: 3000, profit: 900 },
      { date: '2024-02', sales: 'Zhang San', product: 'Product A', amount: 6000, profit: 1800 },
    ],
    'East': [
      { date: '2024-01', sales: 'Wang Wu', product: 'Product A', amount: 4000, profit: 1200 },
      { date: '2024-01', sales: 'Zhao Liu', product: 'Product C', amount: 7000, profit: 2100 },
      { date: '2024-02', sales: 'Wang Wu', product: 'Product B', amount: 5000, profit: 1500 },
    ],
    'South': [
      { date: '2024-01', sales: 'Sun Qi', product: 'Product B', amount: 8000, profit: 2400 },
      { date: '2024-02', sales: 'Sun Qi', product: 'Product A', amount: 9000, profit: 2700 },
    ]
  };
  
  // Create regional files
  const files = [];
  for (const [region, data] of Object.entries(regions)) {
    const file = path.join(testDir, 'scenario2_' + region + '.xlsx');
    excel.writeExcel(data, file);
    files.push(file);
    console.log('Created: ' + region + ' (' + data.length + ' rows)');
  }
  
  // Merge all regions
  const mergedFile = path.join(testDir, 'scenario2_all_regions.xlsx');
  excel.mergeExcelFiles(files, mergedFile);
  
  const { data: merged } = excel.readExcel(mergedFile);
  console.log('Merged total: ' + merged.length + ' rows');
  
  // Statistics
  const stats = excel.getStatistics(merged, 'amount');
  console.log('Total amount: ' + stats.sum + ', Avg: ' + stats.avg);
  
  // Group by sales person
  const bySalesman = excel.groupBy(merged, 'sales', {
    'amount': 'sum',
    'profit': 'sum'
  });
  console.log('Sales ranking:');
  bySalesman.sort((a, b) => b.amount_sum - a.amount_sum).forEach(s => {
    console.log('  ' + s.sales + ': ' + s.amount_sum + ' (profit ' + s.profit_sum + ')');
  });
  
  if (merged.length !== 8) throw new Error('Expected 8 rows, got ' + merged.length);
  
  console.log('Output: ' + mergedFile);
});

// ==================== Scenario 3: Attendance Data Filter ====================
runScenario('Attendance Data Filter and Sort', () => {
  console.log('Background: HR needs to filter late employees and sort by dept');
  
  const attendanceData = [
    { name: 'Zhang San', dept: 'Sales', date: '2024-01-15', time: '09:05', status: 'Late' },
    { name: 'Li Si', dept: 'Tech', date: '2024-01-15', time: '08:55', status: 'Normal' },
    { name: 'Wang Wu', dept: 'Sales', date: '2024-01-15', time: '09:15', status: 'Late' },
    { name: 'Zhao Liu', dept: 'HR', date: '2024-01-15', time: '08:50', status: 'Normal' },
    { name: 'Sun Qi', dept: 'Tech', date: '2024-01-15', time: '09:30', status: 'Late' },
    { name: 'Zhou Ba', dept: 'Finance', date: '2024-01-15', time: '08:45', status: 'Normal' },
  ];
  
  // Filter late employees
  const lateEmployees = excel.filterData(attendanceData, row => row['status'] === 'Late');
  console.log('Late employees: ' + lateEmployees.length);
  
  // Sort by dept
  const sorted = excel.sortData(lateEmployees, [
    { column: 'dept', order: 'asc' },
    { column: 'time', order: 'desc' }
  ]);
  
  console.log('Late report (sorted by dept):');
  sorted.forEach(e => {
    console.log('  ' + e.dept + ' - ' + e.name + ': ' + e.time);
  });
  
  // Group by dept
  const byDept = excel.groupBy(lateEmployees, 'dept', {
    'name': 'count'
  });
  console.log('Late count by dept:');
  byDept.forEach(d => {
    console.log('  ' + d.dept + ': ' + d.name_count);
  });
  
  const outputFile = path.join(testDir, 'scenario3_late_report.xlsx');
  excel.writeExcel(sorted, outputFile);
  
  if (lateEmployees.length !== 3) throw new Error('Expected 3 late, got ' + lateEmployees.length);
  
  console.log('Output: ' + outputFile);
});

// ==================== Scenario 4: CSV Conversion ====================
runScenario('CSV Data Conversion and Standardization', () => {
  console.log('Background: System exported CSV data needs Excel conversion and formatting');
  
  const csvData = [
    { name: '  zhang san  ', email: 'ZHANG@EXAMPLE.COM', phone: '13800138000', amount: ' 5000 ' },
    { name: '   li si', email: '  LISI@example.com  ', phone: '13900139000', amount: '3000' },
    { name: 'wang wu ', email: 'wangwu@example.com', phone: '13700137000', amount: '4000 ' },
  ];
  
  // Save as CSV
  const csvFile = path.join(testDir, 'scenario4_raw.csv');
  excel.writeCSV(csvData, csvFile);
  console.log('Raw CSV saved');
  
  // Read CSV file back (simulate real workflow)
  const csvContent = fs.readFileSync(csvFile, 'utf-8');
  console.log('CSV content preview: ' + csvContent.substring(0, 100) + '...');
  
  // Clean text
  const cleaned = excel.cleanText(csvData, ['name', 'email', 'amount']);
  
  // Format
  const formatted = excel.formatData(cleaned, {
    'name': 'upper',
    'email': 'email',
    'phone': 'phone',
    'amount': 'number'
  });
  
  // Convert to Excel
  const xlsxFile = path.join(testDir, 'scenario4_standardized.xlsx');
  excel.writeExcel(formatted, xlsxFile);
  
  console.log('Standardized:');
  console.log('  Name uppercase: ' + formatted[0].name);
  console.log('  Email masked: ' + formatted[0].email);
  console.log('  Phone masked: ' + formatted[0].phone);
  console.log('  Amount type: ' + typeof formatted[0].amount);
  
  if (formatted[0].name !== 'ZHANG SAN') throw new Error('Uppercase failed');
  if (!formatted[0].email.includes('***')) throw new Error('Email mask failed');
  if (typeof formatted[0].amount !== 'number') throw new Error('Number conversion failed');
  
  console.log('Output: ' + xlsxFile);
});

// ==================== Scenario 5: Inventory Analysis ====================
runScenario('Product Inventory Statistical Analysis', () => {
  console.log('Background: Warehouse needs inventory stats and valuation');
  
  const inventoryData = [
    { id: 'P001', name: 'Laptop', category: 'Electronics', stock: 50, price: 5000, warehouse: 'Beijing' },
    { id: 'P002', name: 'Mouse', category: 'Electronics', stock: 200, price: 100, warehouse: 'Beijing' },
    { id: 'P003', name: 'Desk', category: 'Furniture', stock: 30, price: 1500, warehouse: 'Shanghai' },
    { id: 'P004', name: 'Chair', category: 'Furniture', stock: 100, price: 500, warehouse: 'Shanghai' },
    { id: 'P005', name: 'Printer', category: 'Electronics', stock: 25, price: 2000, warehouse: 'Guangzhou' },
    { id: 'P006', name: 'Cabinet', category: 'Furniture', stock: 40, price: 800, warehouse: 'Beijing' },
  ];
  
  // Calculate inventory value
  const withValue = inventoryData.map(item => ({
    ...item,
    value: item.stock * item.price
  }));
  
  // Group by category
  const byCategory = excel.groupBy(withValue, 'category', {
    'stock': 'sum',
    'value': 'sum'
  });
  
  console.log('Category stats:');
  byCategory.forEach(c => {
    console.log('  ' + c.category + ': ' + c.stock_sum + ' items, value ' + c.value_sum);
  });
  
  // Group by warehouse
  const byWarehouse = excel.groupBy(withValue, 'warehouse', {
    'value': 'sum'
  });
  
  console.log('Warehouse value:');
  byWarehouse.sort((a, b) => b.value_sum - a.value_sum).forEach(w => {
    console.log('  ' + w.warehouse + ': ' + w.value_sum);
  });
  
  // Filter low stock (<50)
  const lowStock = excel.filterData(withValue, item => item.stock < 50);
  console.log('Low stock warning: ' + lowStock.length + ' products');
  lowStock.forEach(p => {
    console.log('  ' + p.name + ': ' + p.stock);
  });
  
  const outputFile = path.join(testDir, 'scenario5_inventory.xlsx');
  excel.writeExcel(withValue, outputFile);
  
  const totalValue = withValue.reduce((sum, item) => sum + item.value, 0);
  console.log('Total value: ' + totalValue);
  
  console.log('Output: ' + outputFile);
});

// ==================== Scenario 6: Financial Report Transpose ====================
runScenario('Financial Report Transpose', () => {
  console.log('Background: Finance provided horizontal report, need vertical format');
  
  const horizontalData = [
    { item: 'Revenue', 'Jan': 100000, 'Feb': 120000, 'Mar': 110000 },
    { item: 'Cost', 'Jan': 60000, 'Feb': 70000, 'Mar': 65000 },
    { item: 'Profit', 'Jan': 40000, 'Feb': 50000, 'Mar': 45000 },
  ];
  
  // Transpose
  const transposed = excel.transpose(horizontalData);
  
  console.log('Transposed data:');
  transposed.forEach(row => {
    console.log('  ' + row.item + ': ' + JSON.stringify(row));
  });
  
  const outputFile = path.join(testDir, 'scenario6_transposed.xlsx');
  excel.writeExcel(transposed, outputFile);
  
  // Transpose converts 3 rows x 4 cols to 4 rows x 3 cols (one row per original column)
  if (transposed.length !== 4) throw new Error('Expected 4 rows, got ' + transposed.length);
  
  console.log('Output: ' + outputFile);
});

// ==================== Scenario 7: Large Data Performance ====================
runScenario('Large Data Performance Test', () => {
  console.log('Background: Test performance with large dataset');
  
  const departments = ['Sales', 'Tech', 'HR', 'Finance', 'Marketing'];
  const largeData = [];
  
  console.log('Generating 5000 rows...');
  for (let i = 0; i < 5000; i++) {
    largeData.push({
      id: i + 1,
      name: 'Employee' + (i + 1),
      dept: departments[i % 5],
      joinDate: '2024-' + String((i % 12) + 1).padStart(2, '0') + '-01',
      salary: 5000 + Math.floor(Math.random() * 15000),
      performance: Math.floor(Math.random() * 100)
    });
  }
  
  // Write performance
  const writeStart = Date.now();
  const largeFile = path.join(testDir, 'scenario7_large.xlsx');
  excel.writeExcel(largeData, largeFile);
  const writeTime = Date.now() - writeStart;
  console.log('Write time: ' + writeTime + 'ms');
  
  // Read performance
  const readStart = Date.now();
  const { data } = excel.readExcel(largeFile);
  const readTime = Date.now() - readStart;
  console.log('Read time: ' + readTime + 'ms');
  
  // Dedup performance
  const dupStart = Date.now();
  const unique = excel.removeDuplicates(data, 'name');
  const dupTime = Date.now() - dupStart;
  console.log('Dedup time: ' + dupTime + 'ms');
  
  // Group performance
  const groupStart = Date.now();
  const byDept = excel.groupBy(data, 'dept', {
    'salary': 'sum',
    'performance': 'avg'
  });
  const groupTime = Date.now() - groupStart;
  console.log('Group time: ' + groupTime + 'ms');
  
  console.log('Dept salary totals:');
  byDept.forEach(d => {
    console.log('  ' + d.dept + ': ' + d.salary_sum + ' (avg perf: ' + d.performance_avg + ')');
  });
  
  if (writeTime > 10000) throw new Error('Write too slow: ' + writeTime + 'ms');
  if (readTime > 5000) throw new Error('Read too slow: ' + readTime + 'ms');
  
  console.log('Performance test passed');
});

// ==================== Summary ====================
console.log('\n============================================================');
console.log('Scenario Test Summary');
console.log('============================================================');
console.log('Pass: ' + passCount);
console.log('Fail: ' + failCount);
console.log('Rate: ' + ((passCount / (passCount + failCount)) * 100).toFixed(1) + '%');

if (failCount > 0) {
  console.log('\nFailed scenarios need review');
}

console.log('\n');

process.exit(failCount > 0 ? 1 : 0);
