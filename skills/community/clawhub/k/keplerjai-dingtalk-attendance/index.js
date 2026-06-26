/**
 * 钉钉考勤数据获取脚本
 * 
 * 功能：
 * - 获取 access_token
 * - 获取部门列表
 * - 获取用户列表
 * - 获取考勤报表（使用已确认可用的 API）
 * - 导出数据到本地 JSON
 * - 自动导出 Excel 文件
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const moment = require('moment');
const { exec } = require('child_process');
const dotenv = require('dotenv');

// 加载 .env（优先）
dotenv.config({ path: path.join(__dirname, '.env') });

function loadJsonConfig(configPath) {
  if (!fs.existsSync(configPath)) {
    return {};
  }

  try {
    return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  } catch (err) {
    console.error(`❌ 读取配置文件失败：${configPath}`);
    process.exit(1);
  }
}

const fileConfig = loadJsonConfig(path.join(__dirname, 'config.json'));

const config = {
  appKey: process.env.DINGTALK_APP_KEY || fileConfig.appKey,
  appSecret: process.env.DINGTALK_APP_SECRET || fileConfig.appSecret,
  agentId: process.env.DINGTALK_AGENT_ID || fileConfig.agentId,
  appId: process.env.DINGTALK_APP_ID || fileConfig.appId,
  outputDir: process.env.OUTPUT_DIR || fileConfig.outputDir || './data/attendance',
  outputFormat: process.env.OUTPUT_FORMAT || fileConfig.outputFormat || 'json',
  notifyChannel: process.env.NOTIFY_CHANNEL || fileConfig.notifyChannel || 'webchat',
  userFetchConcurrency: process.env.USER_FETCH_CONCURRENCY || fileConfig.userFetchConcurrency || 4,
  attendanceFetchConcurrency: process.env.ATTENDANCE_FETCH_CONCURRENCY || fileConfig.attendanceFetchConcurrency || 8
};

if (!config.appKey || !config.appSecret) {
  console.error('❌ 缺少配置：DINGTALK_APP_KEY / DINGTALK_APP_SECRET');
  console.error('请复制 .env.example 为 .env 并填写，或提供本地 config.json（均不要提交到仓库）。');
  process.exit(1);
}

// 钉钉 API 基础 URL
const DINGTALK_API_BASE = 'https://oapi.dingtalk.com';

// 读取性能相关配置（可在 .env 或 config.json 中覆盖）
const USER_FETCH_CONCURRENCY = Math.max(1, Number(config.userFetchConcurrency || 4));
const ATTENDANCE_FETCH_CONCURRENCY = Math.max(1, Number(config.attendanceFetchConcurrency || 8));

/**
 * 并发执行工具
 * @param {Array} items
 * @param {number} concurrency
 * @param {(item:any, index:number)=>Promise<any>} worker
 */
async function mapWithConcurrency(items, concurrency, worker) {
  const results = new Array(items.length);
  let currentIndex = 0;

  async function runWorker() {
    while (true) {
      const idx = currentIndex;
      currentIndex += 1;
      if (idx >= items.length) {
        break;
      }
      results[idx] = await worker(items[idx], idx);
    }
  }

  const workerCount = Math.min(concurrency, items.length);
  const tasks = [];
  for (let i = 0; i < workerCount; i++) {
    tasks.push(runWorker());
  }

  await Promise.all(tasks);
  return results;
}

/**
 * 获取 access_token
 */
async function getAccessToken() {
  try {
    const response = await axios.get(`${DINGTALK_API_BASE}/gettoken`, {
      params: {
        appkey: config.appKey,
        appsecret: config.appSecret
      }
    });
    
    if (response.data.errcode === 0) {
      console.log('✅ 获取 access_token 成功');
      return response.data.access_token;
    } else {
      throw new Error(`获取 token 失败：${response.data.errmsg}`);
    }
  } catch (error) {
    console.error('❌ 获取 access_token 失败:', error.message);
    throw error;
  }
}

/**
 * 获取部门列表
 */
async function getDepartments(accessToken) {
  try {
    const response = await axios.get(`${DINGTALK_API_BASE}/department/list`, {
      params: { access_token: accessToken }
    });
    
    if (response.data.errcode === 0) {
      const departments = response.data.department || [];
      console.log(`✅ 获取部门列表成功，共 ${departments.length} 个部门`);
      return departments;
    } else {
      console.error('❌ 获取部门列表失败:', response.data.errmsg);
      return [];
    }
  } catch (error) {
    console.error('❌ 获取部门列表失败:', error.message);
    return [];
  }
}

/**
 * 获取部门用户列表
 */
async function getUsersInDepartment(accessToken, departmentId) {
  try {
    const response = await axios.get(`${DINGTALK_API_BASE}/user/simplelist`, {
      params: { 
        access_token: accessToken,
        department_id: departmentId
      }
    });
    
    if (response.data.errcode === 0) {
      const users = response.data.userlist || [];
      return users.map(u => ({
        userId: u.userid,
        name: u.name
      }));
    } else {
      console.warn(`⚠️ 获取部门 ${departmentId} 用户失败:`, response.data.errmsg);
      return [];
    }
  } catch (error) {
    console.error(`❌ 获取部门 ${departmentId} 用户失败:`, error.message);
    return [];
  }
}

/**
 * 获取所有用户（遍历所有部门）
 */
async function getAllUsers(accessToken, departments) {
  const allUsers = [];
  const seenUserIds = new Set();

  const usersByDepartment = await mapWithConcurrency(
    departments,
    USER_FETCH_CONCURRENCY,
    async (dept) => {
      const deptId = dept.id;
      console.log(`  获取部门 "${dept.name}" 的用户...`);
      const users = await getUsersInDepartment(accessToken, deptId);
      return { dept, users };
    }
  );

  for (const item of usersByDepartment) {
    const users = item.users || [];

    for (const user of users) {
      if (!seenUserIds.has(user.userId)) {
        seenUserIds.add(user.userId);
        allUsers.push(user);
      }
    }
  }
  
  console.log(`✅ 共获取 ${allUsers.length} 个用户`);
  return allUsers;
}

/**
 * 获取考勤报表（单个用户）
 */
async function getAttendanceReport(accessToken, userId, workDate) {
  try {
    const response = await axios.post(
      `${DINGTALK_API_BASE}/topapi/attendance/getupdatedata`,
      {
        userid: userId,
        work_date: workDate
      },
      {
        params: { access_token: accessToken }
      }
    );
    
    if (response.data.errcode === 0) {
      const result = response.data.result || {};
      return {
        userId: userId,
        attendanceList: result.attendance_result_list || [],
        approveList: result.approve_list || []
      };
    } else {
      return { userId, attendanceList: [], approveList: [], error: response.data.errmsg };
    }
  } catch (error) {
    console.error(`❌ 获取用户 ${userId} 考勤报表失败:`, error.message);
    return { userId, attendanceList: [], approveList: [], error: error.message };
  }
}

/**
 * 获取所有用户的考勤报表
 */
async function getAllAttendanceReports(accessToken, users, workDate) {
  const reports = [];
  let successCount = 0;
  let completedCount = 0;
  
  console.log(`  获取 ${users.length} 个用户的考勤报表...`);

  const resultList = await mapWithConcurrency(
    users,
    ATTENDANCE_FETCH_CONCURRENCY,
    async (user) => {
      const report = await getAttendanceReport(accessToken, user.userId, workDate);

      completedCount++;
      if (completedCount % 10 === 0 || completedCount === users.length) {
        console.log(`    进度：${completedCount}/${users.length}`);
      }

      return {
        userId: user.userId,
        name: user.name,
        ...report
      };
    }
  );

  for (const item of resultList) {
    if (item.attendanceList.length > 0) {
      successCount++;
    }
    reports.push(item);
  }
  
  console.log(`✅ 共获取 ${successCount} 个用户的有效考勤记录`);
  return reports;
}

/**
 * 导出数据到文件
 */
function exportData(data, filename) {
  const outputDir = path.resolve(__dirname, config.outputDir || './data/attendance');
  
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const filepath = path.join(outputDir, filename);
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
  
  console.log(`📁 数据已保存到：${filepath}`);
  return filepath;
}

function getExportNameBase(startDate, endDate) {
  const start = moment(startDate, 'YYYY-MM-DD', true);
  const end = moment(endDate, 'YYYY-MM-DD', true);

  if (!start.isValid() || !end.isValid()) {
    return `考勤_${moment().format('YYYY-MM-DD')}`;
  }

  if (start.isSame(end, 'day')) {
    return `${start.format('YYYY-MM-DD')}考勤`;
  }

  const isWholeMonth =
    start.isSame(end, 'month') &&
    start.date() === 1 &&
    end.date() === end.daysInMonth();

  if (isWholeMonth) {
    return `${start.year()}.${start.month() + 1}月考勤`;
  }

  return `${start.format('YYYY-MM-DD')}至${end.format('YYYY-MM-DD')}考勤`;
}

/**
 * 延时函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 导出 Excel 文件
 * @param {string} jsonFile - JSON 文件路径（可选）
 */
function exportToExcel(jsonFile) {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(__dirname, 'export_excel.py');
    const pythonCmd = jsonFile 
      ? `python "${pythonScript}" "${jsonFile}"`
      : `python "${pythonScript}"`;
    
    console.log('  执行：', pythonCmd);
    
    exec(pythonCmd, { cwd: __dirname }, (error, stdout, stderr) => {
      if (error) {
        console.error('  ❌ Excel 导出失败:', error.message);
        reject(error);
        return;
      }
      
      // 输出 Python 脚本的日志
      const lines = stdout.split('\n').filter(line => line.trim());
      lines.forEach(line => {
        if (line.includes('✅') || line.includes('📁')) {
          console.log('  ' + line.trim());
        }
      });
      
      resolve();
    });
  });
}

/**
 * 主函数
 * @param {string} mode - 运行模式：'daily' (单日) 或 'weekly' (周)
 */
async function main(mode = 'daily', customStartDate = null, customEndDate = null) {
  console.log('🚀 开始获取钉钉考勤数据...\n');
  
  let startDate, endDate, dateLabel;
  
  if (mode === 'range') {
    if (!customStartDate || !customEndDate) {
      throw new Error('range 模式需要提供开始和结束日期，例如：node index.js range 2026-03-01 2026-03-31');
    }
    startDate = customStartDate;
    endDate = customEndDate;
    dateLabel = `${startDate} to ${endDate}`;
    console.log(`📅 获取自定义日期范围：${startDate} 至 ${endDate}\n`);
  } else if (mode === 'weekly') {
    // 获取上一周的数据（上周一到上周日）
    endDate = moment().subtract(1, 'weeks').endOf('week').format('YYYY-MM-DD');
    startDate = moment().subtract(1, 'weeks').startOf('week').format('YYYY-MM-DD');
    dateLabel = moment().subtract(1, 'weeks').format('YYYY-WW');
    console.log(`📅 获取周期：第 ${dateLabel} 周`);
    console.log(`📅 日期范围：${startDate} 至 ${endDate}\n`);
  } else {
    // 默认获取昨天的数据
    endDate = moment().subtract(1, 'days').format('YYYY-MM-DD');
    startDate = endDate;
    dateLabel = endDate.replace('-', '');
    console.log(`📅 获取日期：${startDate}\n`);
  }
  
  try {
    // 1. 获取 access_token
    const accessToken = await getAccessToken();
    
    // 2. 获取部门列表
    console.log('\n🏢 获取部门列表...');
    const departments = await getDepartments(accessToken);
    
    if (departments.length === 0) {
      console.log('⚠️ 没有部门数据，退出');
      return;
    }
    
    // 3. 获取所有用户
    console.log('\n👥 获取用户列表...');
    const users = await getAllUsers(accessToken, departments);
    
    if (users.length === 0) {
      console.log('⚠️ 没有用户数据，退出');
      return;
    }
    
    // 4. 获取考勤报表（遍历日期范围）
    console.log('\n📋 获取考勤报表...');
    const allReports = {}; // 按用户 ID 存储所有日期的报表
    
    const dateRange = [];
    let currentDate = moment(startDate);
    while (currentDate.isSameOrBefore(endDate)) {
      dateRange.push(currentDate.format('YYYY-MM-DD'));
      currentDate.add(1, 'days');
    }
    
    console.log(`  需要获取 ${dateRange.length} 天的数据`);
    
    for (const workDate of dateRange) {
      console.log(`\n  获取 ${workDate} 的考勤数据...`);
      const dayReports = await getAllAttendanceReports(accessToken, users, workDate);
      
      // 合并同一用户的多日数据
      for (const report of dayReports) {
        const userId = report.userId;
        if (!allReports[userId]) {
          allReports[userId] = {
            userId: report.userId,
            name: report.name,
            attendanceList: [],
            approveList: []
          };
        }
        allReports[userId].attendanceList.push(...report.attendanceList);
        allReports[userId].approveList.push(...report.approveList);
      }
    }
    
    const reports = Object.values(allReports);
    
    // 5. 统计数据
    const totalRecords = reports.reduce((sum, r) => sum + r.attendanceList.length, 0);
    const usersWithAttendance = reports.filter(r => r.attendanceList.length > 0).length;
    
    console.log(`\n📊 统计:`);
    console.log(`  总用户数：${users.length}`);
    console.log(`  有考勤记录的用户：${usersWithAttendance}`);
    console.log(`  总考勤记录数：${totalRecords}`);
    
    // 6. 导出数据
    console.log('\n💾 导出数据...');
    const exportNameBase = getExportNameBase(startDate, endDate);
    const outputData = {
      mode: mode,
      startDate: startDate,
      endDate: endDate,
      exportTime: moment().format('YYYY-MM-DD HH:mm:ss'),
      summary: {
        totalDepartments: departments.length,
        totalUsers: users.length,
        usersWithAttendance: usersWithAttendance,
        totalRecords: totalRecords,
        totalDays: dateRange.length
      },
      users: users,
      attendanceReports: reports
    };
    
    const jsonFile = exportData(outputData, `${exportNameBase}.json`);
    
    // 7. 自动导出 Excel（传入刚生成的 JSON 文件路径）
    console.log('\n📊 生成 Excel 文件...');
    await exportToExcel(jsonFile);
    
    console.log('\n✅ 考勤数据获取完成！\n');
    
  } catch (error) {
    console.error('\n❌ 执行失败:', error.message);
    process.exit(1);
  }
}

// 运行（支持命令行参数）
const mode = process.argv[2] || 'daily';
if (mode === 'weekly' || mode === 'daily') {
  main(mode);
} else if (mode === 'range') {
  const start = process.argv[3];
  const end = process.argv[4];
  if (!start || !end || !moment(start, 'YYYY-MM-DD', true).isValid() || !moment(end, 'YYYY-MM-DD', true).isValid()) {
    console.log('range 模式参数错误，示例：node index.js range 2026-03-01 2026-03-31');
    process.exit(1);
  }
  if (moment(start).isAfter(moment(end))) {
    console.log('range 模式参数错误：开始日期不能晚于结束日期');
    process.exit(1);
  }
  main(mode, start, end);
} else {
  console.log('用法：node index.js [daily|weekly|range]');
  console.log('  daily  - 获取昨天的考勤数据（默认）');
  console.log('  weekly - 获取上一周的考勤数据（上周一到上周日）');
  console.log('  range  - 获取自定义日期范围，例如：node index.js range 2026-03-01 2026-03-31');
  process.exit(1);
}
