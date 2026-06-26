/**
 * 保险费率二维表生成脚本
 * 
 * 输入：产品参数（产品名称、保障计划、交费期间、交费方式、领取时间、年龄范围）
 * 输出：符合格式标准的 Excel 文件
 * 
 * 使用方法：
 *   node generate-rate-table.js "产品名称" [选项]
 * 
 * 选项：
 *   --plans=计划一,计划二
 *   --payment-years=趸交,10年,20年
 *   --payment-methods=一次交清,月交,年交
 *   --receive-ages=自55周岁,自60周岁
 *   --age-range=0-70
 * 
 * 示例：
 *   node generate-rate-table.js "星海赢家朱雀版" --plans="计划一,计划二" --payment-years="趸交,10年,20年" --payment-methods="一次交清,月交,年交,半年交,季交,不定期交" --receive-ages="自55周岁,自60周岁"
 */

const XLSX = require('xlsx');
const path = require('path');

// 默认参数
const DEFAULT_PARAMS = {
  plans: ['计划一', '计划二'],
  paymentYears: ['趸交', '10年', '20年'],
  paymentMethods: ['一次交清', '月交', '年交', '半年交', '季交', '不定期交'],
  receiveAges: ['自55周岁', '自60周岁'],
  genders: ['女', '男'],
  ageRange: { min: 0, max: 70 }
};

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const productName = args[0] || '费率表';
  const params = { ...DEFAULT_PARAMS };
  
  args.slice(1).forEach(arg => {
    if (arg.startsWith('--plans=')) {
      params.plans = arg.replace('--plans=', '').split(',');
    } else if (arg.startsWith('--payment-years=')) {
      params.paymentYears = arg.replace('--payment-years=', '').split(',');
    } else if (arg.startsWith('--payment-methods=')) {
      params.paymentMethods = arg.replace('--payment-methods=', '').split(',');
    } else if (arg.startsWith('--receive-ages=')) {
      params.receiveAges = arg.replace('--receive-ages=', '').split(',');
    } else if (arg.startsWith('--age-range=')) {
      const range = arg.replace('--age-range=', '').split('-');
      params.ageRange = { min: parseInt(range[0]), max: parseInt(range[1]) };
    }
  });
  
  return { productName, params };
}

// 生成有效的列组合
function generateCols(params) {
  const cols = [];
  
  params.plans.forEach(plan => {
    params.paymentYears.forEach(py => {
      params.paymentMethods.forEach(pm => {
        // 约束规则：一次交清只能配趸交，其他交费方式不能配趸交
        if (pm === '一次交清' && py !== '趸交') return;
        if (pm !== '一次交清' && py === '趸交') return;
        
        params.receiveAges.forEach(ra => {
          params.genders.forEach(gender => {
            cols.push({ plan, py, pm, ra, gender });
          });
        });
      });
    });
  });
  
  return cols;
}

// 生成年龄数组
function generateAges(params) {
  const ages = [];
  for (let i = params.ageRange.min; i <= params.ageRange.max; i++) {
    ages.push(i);
  }
  return ages;
}

// 生成费率数据（示例，实际需要从外部数据源获取）
function generateRate(age, colIndex) {
  // 示例费率，实际应从数据库或配置文件读取
  return 34000 + age + colIndex;
}

// 主函数
function main() {
  const { productName, params } = parseArgs();
  const cols = generateCols(params);
  const ages = generateAges(params);
  
  // 生成表头和数据
  const data = [];
  data.push(['保障计划', ...cols.map(c => c.plan)]);
  data.push(['交费期间', ...cols.map(c => c.py)]);
  data.push(['交费方式', ...cols.map(c => c.pm)]);
  data.push(['领取时间', ...cols.map(c => c.ra)]);
  data.push(['被保人年龄/被保人性别', ...cols.map(c => c.gender)]);
  
  // 生成数据行
  ages.forEach(age => {
    const row = [age];
    cols.forEach((c, i) => {
      row.push(generateRate(age, i));
    });
    data.push(row);
  });
  
  // 创建工作簿
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(data);
  
  // 设置列宽
  const colWidths = [{ wch: 18 }, ...cols.map(() => ({ wch: 10 }))];
  ws['!cols'] = colWidths;
  
  // 添加工作表并保存
  XLSX.utils.book_append_sheet(wb, ws, '费率表');
  const fileName = `${productName}费率表.xlsx`;
  const filePath = path.join(process.cwd(), fileName);
  XLSX.writeFile(wb, filePath);
  
  console.log('✓ 文件生成成功:', fileName);
  console.log('  - 方案组合:', cols.length, '列');
  console.log('  - 年龄范围:', params.ageRange.min, '-', params.ageRange.max, '岁');
  console.log('  - 数据行:', ages.length, '行');
}

main();
