#!/usr/bin/env node

/**
 * iHub 日报填写自动化脚本
 * 使用 OpenClaw Browser 工具实现
 */

const BASE_URL = 'https://ihub.testfarm.cn:8020/admin/login';
const DEFAULT_USERNAME = '';  // 请在参数中传入账号
const DEFAULT_PASSWORD = '';  // 请在参数中传入密码

/**
 * 获取目标日期（昨天）
 */
function getTargetDate(dateStr) {
  if (dateStr === 'today') {
    return new Date();
  } else if (dateStr === 'yesterday' || !dateStr) {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    return yesterday;
  } else if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
    return new Date(dateStr + 'T00:00:00+08:00');
  } else if (dateStr.match(/^\d{8}$/)) {
    return new Date(
      parseInt(dateStr.substring(0, 4)),
      parseInt(dateStr.substring(4, 6)) - 1,
      parseInt(dateStr.substring(6, 8))
    );
  }
  return new Date(dateStr);
}

/**
 * 计算给定日期对应的周文件夹名称
 * 格式：第四周(3.23-3.29)(202603230329)
 */
function getWeekFolderName(date) {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  // 计算是第几周
  const firstDay = new Date(year, month - 1, 1);
  const firstDayWeekDay = firstDay.getDay(); // 0 = 周日
  const dayOfMonth = day;
  
  // 计算周的序号（从1开始）
  const weekNum = Math.ceil((dayOfMonth + firstDayWeekDay - 1) / 7);
  
  // 计算周的起始和结束日期
  const weekStart = day - (date.getDay() === 0 ? 6 : date.getDay() - 1);
  const weekEnd = weekStart + 6;
  
  const monthStr = month.toString().padStart(2, '0');
  const weekStartStr = `${monthStr}.${weekStart.toString().padStart(2, '0')}`;
  const weekEndStr = `${monthStr}.${weekEnd.toString().padStart(2, '0')}`;
  
  // 生成周ID
  const weekId = `${year}${monthStr}${weekStart.toString().padStart(2, '0')}${weekEnd.toString().padStart(2, '0')}`;
  
  const weekFolderName = `第${toChineseNumber(weekNum)}周(${weekStartStr}-${weekEndStr})(${weekId})`;
  
  return {
    yearMonth: `${year}年${month}月`,
    folderName: weekFolderName,
    weekNum: weekNum
  };
}

function toChineseNumber(num) {
  const cn = ['', '一', '二', '三', '四', '五', '六'];
  return cn[num] || num;
}

/**
 * 获取星期几（1=周一，7=周日）
 */
function getDayOfWeek(date) {
  const day = date.getDay();
  return day === 0 ? 7 : day;
}

/**
 * 获取星期名称
 */
function getDayName(date) {
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  return days[date.getDay()];
}

/**
 * 主执行函数
 */
async function executeDailyReport(args) {
  const username = args.username || DEFAULT_USERNAME;
  const password = args.password || DEFAULT_PASSWORD;
  const content = args.content || '';
  const name = args.name || '';
  const dateStr = args.date || 'yesterday';
  
  // 解析日期
  const targetDate = getTargetDate(dateStr);
  const weekInfo = getWeekFolderName(targetDate);
  const dayOfWeek = getDayOfWeek(targetDate);
  const dayName = getDayName(targetDate);
  
  console.log('=== iHub 日报填写任务 ===');
  console.log(`姓名: ${name}`);
  console.log(`目标日期: ${targetDate.toLocaleDateString('zh-CN')} (${dayName})`);
  console.log(`周文件夹: ${weekInfo.yearMonth}/${weekInfo.folderName}`);
  console.log(`内容长度: ${content.length} 字符`);
  console.log('==============================');
  
  // 返回执行信息供后续使用
  return {
    username,
    password,
    content,
    name,
    targetDate,
    weekInfo,
    dayOfWeek,
    dayName,
    steps: [
      { action: 'open', url: BASE_URL },
      { action: 'wait', ms: 2000 }
    ]
  };
}

// 导出为可执行脚本
if (require.main === module) {
  const args = process.argv.slice(2);
  const params = {};
  
  // 解析参数
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--content' || args[i] === '-c') {
      params.content = args[i + 1];
      i++;
    } else if (args[i] === '--username' || args[i] === '-u') {
      params.username = args[i + 1];
      i++;
    } else if (args[i] === '--password' || args[i] === '-p') {
      params.password = args[i + 1];
      i++;
    } else if (args[i] === '--date' || args[i] === '-d') {
      params.date = args[i + 1];
      i++;
    } else if (args[i] === '--name' || args[i] === '-n') {
      params.name = args[i + 1];
      i++;
    }
  }
  
  executeDailyReport(params).then(result => {
    console.log(JSON.stringify(result, null, 2));
  }).catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}

module.exports = { 
  executeDailyReport, 
  getWeekFolderName, 
  getTargetDate,
  getDayOfWeek,
  getDayName 
};
