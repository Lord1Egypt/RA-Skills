const { readCSV, readExcel, writeExcel, writeCSV, cleanData, transformColumns, filterRows, sortData, removeDuplicates } = require('./index.js');
const path = require('path');

async function runTests() {
  const testDir = __dirname;
  const testFile = path.join(testDir, 'test-data.csv');
  
  console.log('🧪 开始测试 li-etl-handle-safe 技能...\n');
  
  try {
    // 测试 1: 读取 CSV
    console.log('✅ 测试 1: 读取 CSV');
    const data = await readCSV(testFile);
    console.log(`   读取成功，共 ${data.length} 行`);
    console.log(`   第一行：${JSON.stringify(data[0])}\n`);
    
    // 测试 2: 写入 Excel
    console.log('✅ 测试 2: 写入 Excel');
    const excelFile = path.join(testDir, 'test-output.xlsx');
    await writeExcel(excelFile, data);
    console.log(`   写入成功：${excelFile}\n`);
    
    // 测试 3: 读取 Excel
    console.log('✅ 测试 3: 读取 Excel');
    const excelData = await readExcel(excelFile);
    console.log(`   读取成功，共 ${excelData.length} 行\n`);
    
    // 测试 4: 数据清洗
    console.log('✅ 测试 4: 数据清洗');
    const cleaned = cleanData(data, { trim: true, removeEmpty: true });
    console.log(`   清洗完成，剩余 ${cleaned.length} 行\n`);
    
    // 测试 5: 类型转换
    console.log('✅ 测试 5: 类型转换');
    const transformed = transformColumns(cleaned, {
      columns: { age: 'number', salary: 'number' }
    });
    console.log(`   转换完成，age 类型：${typeof transformed[0].age}, salary 类型：${typeof transformed[0].salary}\n`);
    
    // 测试 6: 过滤数据
    console.log('✅ 测试 6: 过滤数据（salary > 15000）');
    const filtered = filterRows(transformed, { column: 'salary', operator: 'gt', value: 15000 });
    console.log(`   过滤后剩余 ${filtered.length} 行：${filtered.map(r => r.name).join(', ')}\n`);
    
    // 测试 7: 排序
    console.log('✅ 测试 7: 排序（salary 降序）');
    const sorted = sortData(transformed, [{ column: 'salary', order: 'desc' }]);
    console.log(`   排序后：${sorted.map(r => `${r.name}(${r.salary})`).join(', ')}\n`);
    
    // 测试 8: 写入 CSV
    console.log('✅ 测试 8: 写入 CSV');
    const csvOut = path.join(testDir, 'test-output.csv');
    writeCSV(csvOut, sorted);
    console.log(`   写入成功：${csvOut}\n`);
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 所有测试通过！技能功能正常！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

runTests();
