/**
 * 产品分组配置向导
 * 功能：首次运行时让用户为每个产品分组指定产品类型，保存到配置文件
 *
 * 用法：
 *   const mapping = await configureProductMapping(groups);
 *   // mapping: { "Stainless Steel Kitchen Cabinet": "厨房橱柜", ... }
 */

const fs = require('fs');
const readline = require('readline');

const MAPPING_FILE = './product-mapping.json';

// 常见产品类型列表（用于自动补全和展示建议）
const COMMON_PRODUCT_TYPES = [
  '厨房橱柜',
  '箱体户外厨房',
  '定制户外厨房',
  '标品户外厨房',
  '户外厨房',
  '工具柜',
  '枪柜',
  '餐边柜',
  '浴室柜',
  '衣柜',
  '电视柜',
  '酒柜',
  '入户柜',
  '书柜',
  '抽屉柜',
  'Kamado Grill',
  '电烤箱',
  '凉亭',
  '阳台柜',
  '其他',
];

// ========== 映射文件管理 ==========

/**
 * 加载已有的映射配置
 */
function loadMapping() {
  try {
    if (fs.existsSync(MAPPING_FILE)) {
      const data = fs.readFileSync(MAPPING_FILE, 'utf8');
      const mapping = JSON.parse(data);
      console.log(`  [配置] 已加载 ${Object.keys(mapping).length} 个分组映射`);
      return mapping;
    }
  } catch (e) {
    console.log(`  [配置] 加载失败: ${e.message}`);
  }
  return {};
}

/**
 * 保存映射配置
 */
function saveMapping(mapping) {
  try {
    const data = {
      version: '1.0',
      updatedAt: new Date().toISOString(),
      mapping: mapping,
    };
    fs.writeFileSync(MAPPING_FILE, JSON.stringify(data, null, 2), 'utf8');
    console.log(`  [配置] 已保存 ${Object.keys(mapping).length} 个分组映射到 ${MAPPING_FILE}`);
  } catch (e) {
    console.log(`  [配置] 保存失败: ${e.message}`);
  }
}

// ========== 类型推导 ==========

/**
 * 从分组名推导产品类型（用于建议）
 */
function suggestProductType(groupName) {
  if (!groupName) return '其他';

  const lower = groupName.toLowerCase();

  // 厨房橱柜
  if (/kitchen.*cabinet|stainless.*steel.*kitchen/i.test(lower)) {
    return '厨房橱柜';
  }
  if (/kitchen/i.test(lower)) {
    return '厨房橱柜';
  }

  // 户外厨房
  if (/outdoor.*kitchen.*shed|outdoor.*shed/i.test(lower)) {
    return '箱体户外厨房';
  }
  if (/custom.*outdoor.*kitchen/i.test(lower)) {
    return '定制户外厨房';
  }
  if (/modular.*|standard.*|标品/i.test(lower) && /outdoor.*kitchen/i.test(lower)) {
    return '标品户外厨房';
  }
  if (/outdoor.*kitchen/i.test(lower)) {
    return '户外厨房';
  }

  // Kamado Grill
  if (/kamado.*grill|kamado/i.test(lower)) {
    return 'Kamado Grill';
  }

  // 工具柜
  if (/tool.*cabinet|tool.*storage|工具/i.test(lower)) {
    return '工具柜';
  }

  // 枪柜
  if (/gun.*cabinet|gun.*storage|枪/i.test(lower)) {
    return '枪柜';
  }

  // 餐边柜
  if (/sideboard|餐边/i.test(lower)) {
    return '餐边柜';
  }

  // 浴室柜
  if (/bathroom.*cabinet|bathroom.*vanity|浴室/i.test(lower)) {
    return '浴室柜';
  }

  // 衣柜
  if (/wardrobe|closet|衣柜/i.test(lower)) {
    return '衣柜';
  }

  // 电视柜
  if (/tv.*cabinet|tv.*stand|电视/i.test(lower)) {
    return '电视柜';
  }

  // 酒柜
  if (/wine.*cabinet|wine.*storage|酒/i.test(lower)) {
    return '酒柜';
  }

  // 鞋柜/入户柜
  if (/shoe.*cabinet|shoe.*rack|entryway|鞋柜|入户/i.test(lower)) {
    return '入户柜';
  }

  // 书柜
  if (/bookcase|bookshelf|书柜/i.test(lower)) {
    return '书柜';
  }

  // 阳台柜
  if (/balcony.*storage|阳台/i.test(lower)) {
    return '阳台柜';
  }

  // 抽屉柜
  if (/chest.*drawer|dresser|抽屉/i.test(lower)) {
    return '抽屉柜';
  }

  // 凉亭
  if (/pergola|gazebo|pavilion|凉亭/i.test(lower)) {
    return '凉亭';
  }

  // 电烤箱
  if (/built-in.*oven|electric.*oven|oven/i.test(lower)) {
    return '电烤箱';
  }

  // 未知分组，返回分组名本身让用户自定义
  return '其他';
}

// ========== 交互式配置 ==========

/**
 * 创建 readline 接口
 */
function createReadline() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

/**
 * 询问用户输入
 */
function ask(rl, question, defaultValue = '') {
  return new Promise((resolve) => {
    const prompt = defaultValue
      ? `${question} [默认: ${defaultValue}]: `
      : `${question}: `;
    rl.question(prompt, (answer) => {
      resolve(answer.trim() || defaultValue);
    });
  });
}

/**
 * 确认问题
 */
function confirm(rl, question) {
  return new Promise((resolve) => {
    rl.question(`${question} [y/N]: `, (answer) => {
      resolve(answer.trim().toLowerCase() === 'y');
    });
  });
}

/**
 * 配置产品分组映射（交互式）
 */
async function configureProductMapping(groups) {
  const rl = createReadline();
  const mapping = {};
  let index = 1;

  console.log('\n========== 产品分组配置向导 ==========');
  console.log(`共找到 ${groups.length} 个产品分组`);
  console.log('请为每个分组指定对应的产品类型\n');

  // 显示可用类型列表
  console.log('可用产品类型：');
  console.log(COMMON_PRODUCT_TYPES.map((t, i) => `  ${i + 1}. ${t}`).join('\n'));
  console.log('');

  for (const group of groups) {
    console.log(`\n[${index}/${groups.length}] 分组: ${group}`);

    // 建议类型
    const suggested = suggestProductType(group);
    console.log(`  建议类型: ${suggested}`);

    // 让用户输入
    const answer = await ask(
      rl,
      '请输入产品类型（输入数字选择建议，或直接输入自定义类型）',
      suggested
    );

    // 处理数字输入
    let productType = answer;
    const numMatch = answer.match(/^\d+$/);
    if (numMatch) {
      const num = parseInt(numMatch[0]);
      if (num >= 1 && num <= COMMON_PRODUCT_TYPES.length) {
        productType = COMMON_PRODUCT_TYPES[num - 1];
        console.log(`  已选择: ${productType}`);
      } else {
        console.log(`  数字无效，使用输入值: ${answer}`);
      }
    }

    mapping[group] = productType;
    index++;
  }

  // 确认保存
  console.log('\n========== 配置确认 ==========');
  console.log('分组映射预览：');
  for (const [group, type] of Object.entries(mapping)) {
    console.log(`  ${group} → ${type}`);
  }

  const shouldSave = await confirm(rl, '\n是否保存此配置？');
  rl.close();

  if (shouldSave) {
    saveMapping(mapping);
    return mapping;
  } else {
    console.log('配置已取消');
    return null;
  }
}

// ========== 自动配置 ==========

/**
 * 自动配置（使用建议类型，无需交互）
 */
function autoConfigureProductMapping(groups) {
  console.log(`\n[自动配置] 为 ${groups.length} 个分组自动分配产品类型`);

  const mapping = {};
  for (const group of groups) {
    const suggested = suggestProductType(group);
    mapping[group] = suggested;
    console.log(`  ${group} → ${suggested}`);
  }

  saveMapping(mapping);
  return mapping;
}

// ========== 导出 ==========

module.exports = {
  loadMapping,
  saveMapping,
  suggestProductType,
  configureProductMapping,
  autoConfigureProductMapping,
  COMMON_PRODUCT_TYPES,
  MAPPING_FILE,
};
