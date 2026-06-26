/**
 * LI_excel_handle 测试文件
 * 运行：node test.js
 */

const excel = require('./index.js');
const path = require('path');

// 创建测试数据（虚构数据，仅用于测试）
const testData = [
  { 姓名：'测试用户 A', 部门：'销售部', 手机号：'13800000001', 销售额：5000 },
  { 姓名：'测试用户 B', 部门：'技术部', 手机号：'13800000002', 销售额：3000 },
  { 姓名： '测试用户 C', 部门： '销售部', 手机号： '13800000001', 销售额： 4000 }, // 重复手机号（测试去重）
  { 姓名： '测试用户 D', 部门： '人事部', 手机号： '13800000003', 销售额： 2000 },
  { 姓名： '', 部门： '', 手机号： '', 销售额： 0 }, // 空行（测试删除空行）
  { 姓名：'测试用户 E', 部门： '技术部', 手机号： '13800000004', 销售额： 6000 },
];

console.log('🧪 LI_excel_handle 功能测试\n');
console.log('=' .repeat(50));

// 测试 1：写入 Excel
console.log('\n📝 测试 1: 写入 Excel');
const testFile = path.join(__dirname, 'test_data.xlsx');
excel.writeExcel(testData, testFile);
console.log(`✓ 测试文件已创建：${testFile}`);

// 测试 2：读取 Excel
console.log('\n📖 测试 2: 读取 Excel');
const { data, headers } = excel.readExcel(testFile);
console.log(`✓ 读取成功：${data.length}行，列：${headers.join(', ')}`);

// 测试 3：数据去重
console.log('\n🧹 测试 3: 数据去重');
const uniqueData = excel.removeDuplicates(data, '手机号');
console.log(`✓ 去重后：${uniqueData.length}行`);

// 测试 4：删除空行
console.log('\n🗑️  测试 4: 删除空行');
const cleanedData = excel.removeEmptyRows(uniqueData);
console.log(`✓ 清理后：${cleanedData.length}行`);

// 测试 5：文本清理
console.log('\n✨ 测试 5: 文本清理');
const normalizedData = excel.cleanText(cleanedData);
console.log('✓ 文本清理完成');

// 测试 6：格式标准化（脱敏）
console.log('\n🔒 测试 6: 格式标准化（脱敏）');
const formattedData = excel.formatData(normalizedData, {
  '手机号': 'phone'
});
console.log('脱敏后手机号示例:', formattedData[0]['手机号']);

// 测试 7：数据统计
console.log('\n📊 测试 7: 数据统计');
const stats = excel.getStatistics(formattedData, '销售额');
console.log('销售额统计:', stats);

// 测试 8：数据筛选
console.log('\n🔍 测试 8: 数据筛选');
const filtered = excel.filterData(formattedData, row => row['销售额'] > 3000);
console.log(`✓ 筛选结果：${filtered.length}行 (销售额>3000)`);

// 测试 9：数据排序
console.log('\n📈 测试 9: 数据排序');
const sorted = excel.sortData(formattedData, [{ column: '销售额', order: 'desc' }]);
console.log('✓ 按销售额降序排列');
console.log('前 3 名:', sorted.slice(0, 3).map(r => `${r.姓名}(${r.销售额})`).join(', '));

// 测试 10：分组聚合
console.log('\n📉 测试 10: 分组聚合');
const grouped = excel.groupBy(formattedData, '部门', {
  '销售额': 'sum',
  '销售额': 'avg'
});
console.log('✓ 按部门分组聚合:');
grouped.forEach(g => {
  console.log(`  ${g.部门}: 总额=${g.销售额_总和}, 平均=${g.销售额_平均}`);
});

// 测试 11：写入结果
console.log('\n💾 测试 11: 写入处理结果');
const outputFile = path.join(__dirname, 'test_result.xlsx');
excel.writeExcel(sorted, outputFile);
console.log(`✓ 结果已保存：${outputFile}`);

// 测试 12：CSV 转换
console.log('\n🔄 测试 12: CSV 转换');
const csvFile = path.join(__dirname, 'test_data.csv');
excel.writeCSV(formattedData, csvFile);
console.log(`✓ CSV 已保存：${csvFile}`);

console.log('\n' + '=' .repeat(50));
console.log('✅ 所有测试完成！\n');

// 清理测试文件（可选）
// fs.unlinkSync(testFile);
// fs.unlinkSync(outputFile);
// fs.unlinkSync(csvFile);
