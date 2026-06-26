#!/usr/bin/env node
/**
 * Preview and confirm plan before pushing
 * Usage: node preview_plan.cjs <plans.json>
 * 
 * Features:
 * - Display plan in human-readable format
 * - Show weekly summary
 * - Ask for confirmation
 * - Optional: edit before push
 */

const fs = require('fs');
const readline = require('readline');

function formatDate(dateStr) {
  const date = new Date(dateStr);
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  return `${dateStr} ${weekdays[date.getDay()]}`;
}

function parseNameField(name) {
  // Simple parsing for display
  if (name === '休息' || name === 'rest') {
    return '休息日';
  }
  
  // Replace common patterns with readable text
  let readable = name
    .replace(/@\(HRR\+([\d.]+)~([\d.]+)\)/g, '(心率区间 $1-$2)')
    .replace(/@\(VDOT\+([\d.]+)~([\d.]+)\)/g, '(VDOT $1-$2)')
    .replace(/@\(PACE\+([\d']+)~([\d']+)\)/g, '(配速 $1-$2)')
    .replace(/@\(t\/([\d.]+)~([\d.]+)\)/g, '(阈值 $1-$2)')
    .replace(/@\(rest\)/g, '(休息)')
    .replace(/@\(EFFORT\+([\d.]+)~([\d.]+)\)/g, '(尽力程度 $1-$2)')
    .replace(/min@/g, '分钟')
    .replace(/km@/g, '公里')
    .replace(/m@/g, '米')
    .replace(/s@/g, '秒');
  
  // Replace interval notation
  readable = readable.replace(/\{([^}]+)\}x(\d+)/g, '【$1】×$2组');
  
  return readable;
}

function getIntensityLabel(weight) {
  const labels = {
    'q1': '🔴 高强度',
    'q2': '🟠 中强度',
    'q3': '🟢 低强度',
    'xuanxiu': '🔵 恢复/选修'
  };
  return labels[weight] || weight;
}

function getTypeLabel(type) {
  const labels = {
    'qingsong': '轻松跑',
    'xiuxi': '休息日',
    'e': '有氧训练',
    'lsd': '长距离慢跑',
    'm': '马拉松配速',
    't': '阈值训练',
    'i': '间歇训练',
    'r': '速度训练',
    'ft': '法特莱克',
    'com': '组合训练',
    'ch': '变速训练',
    'jili': '肌力训练',
    'max': '最大心率测试',
    'drift': '有氧稳定测试',
    'other': '其他'
  };
  return labels[type] || type;
}

function displayPlan(plansData) {
  const plans = plansData.plans || [];
  
  console.log('\n' + '='.repeat(60));
  console.log('📋 训练计划预览');
  console.log('='.repeat(60) + '\n');
  
  // Group by week
  const byWeek = {};
  plans.forEach(plan => {
    const date = new Date(plan.start);
    const week = Math.floor((date - new Date(plans[0].start)) / (7 * 24 * 60 * 60 * 1000)) + 1;
    if (!byWeek[week]) byWeek[week] = [];
    byWeek[week].push(plan);
  });
  
  // Display each week
  Object.keys(byWeek).sort().forEach(week => {
    console.log(`\n📅 第 ${week} 周`);
    console.log('-'.repeat(60));
    
    byWeek[week].forEach((plan, idx) => {
      console.log(`\n${idx + 1}. ${formatDate(plan.start)}`);
      console.log(`   📌 ${plan.title}`);
      console.log(`   📝 ${parseNameField(plan.name)}`);
      console.log(`   🏃 类型: ${getTypeLabel(plan.type)}`);
      console.log(`   ⚡ 强度: ${getIntensityLabel(plan.weight)}`);
      if (plan.description) {
        console.log(`   💭 ${plan.description}`);
      }
    });
  });
  
  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 计划摘要');
  console.log('='.repeat(60));
  console.log(`总训练日: ${plans.length} 天`);
  
  const byType = {};
  const byWeight = {};
  plans.forEach(p => {
    byType[p.type] = (byType[p.type] || 0) + 1;
    byWeight[p.weight] = (byWeight[p.weight] || 0) + 1;
  });
  
  console.log('\n按类型:');
  Object.entries(byType).forEach(([type, count]) => {
    console.log(`  ${getTypeLabel(type)}: ${count} 次`);
  });
  
  console.log('\n按强度:');
  Object.entries(byWeight).forEach(([weight, count]) => {
    console.log(`  ${getIntensityLabel(weight)}: ${count} 次`);
  });
  
  console.log('\n' + '='.repeat(60) + '\n');
}

function prompt(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim().toLowerCase());
    });
  });
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage: node preview_plan.cjs <plans.json>');
    process.exit(1);
  }
  
  const planFile = args[0];
  
  if (!fs.existsSync(planFile)) {
    console.error(`Error: File not found: ${planFile}`);
    process.exit(1);
  }
  
  let plansData;
  try {
    plansData = JSON.parse(fs.readFileSync(planFile, 'utf8'));
  } catch (e) {
    console.error(`Error: Invalid JSON: ${e.message}`);
    process.exit(1);
  }
  
  // Display plan
  displayPlan(plansData);
  
  // Interactive confirmation
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  console.log('请选择操作:');
  console.log('  [Y] 确认并推送');
  console.log('  [N] 取消');
  console.log('  [E] 编辑计划 (需要手动修改文件)');
  console.log('');
  
  const answer = await prompt(rl, '你的选择 (Y/N/E): ');
  
  rl.close();
  
  if (answer === 'y' || answer === 'yes') {
    console.log('\n✅ 已确认，准备推送...\n');
    process.exit(0); // Success - continue to push
  } else if (answer === 'e' || answer === 'edit') {
    console.log('\n📝 请手动编辑计划文件:');
    console.log(`   ${planFile}`);
    console.log('\n编辑完成后，重新运行预览命令。\n');
    process.exit(2); // Edit needed
  } else {
    console.log('\n❌ 已取消推送\n');
    process.exit(1); // Cancelled
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
