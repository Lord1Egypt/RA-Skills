#!/usr/bin/env node

/**
 * 2026年世界杯赛程获取工具
 * 从百度体育网页内嵌的 JSON 数据中解析赛程
 */

const https = require('https');
const { getRandomUserAgent } = require('./lib/user-agents');

const HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding': 'identity',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Referer': 'https://tiyu.baidu.com/',
  'Origin': 'https://tiyu.baidu.com'
};

const SCHEDULE_URL = 'https://tiyu.baidu.com/al/match?match=%E4%B8%96%E7%95%8C%E6%9D%AF&tab=%E8%B5%9B%E7%A8%8B';

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: { ...HEADERS, 'User-Agent': getRandomUserAgent() }
    };

    const req = https.request(options, (res) => {
      const chunks = [];
      res.on('data', (chunk) => { chunks.push(chunk); });
      res.on('end', () => {
        resolve(Buffer.concat(chunks).toString('utf-8'));
      });
    });

    req.on('error', reject);
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.end();
  });
}

/**
 * 从HTML中提取内嵌的JSON赛程数据
 * 结构: {"all":{"data":[{"time":"2026-06-12","dateText":"06-12/今天","list":"[{...},...]"}, ...]}}
 * 每个 data[i].list 是一个字符串化的 JSON 数组
 */
function extractScheduleJson(html) {
  // 寻找赛程数据数组标记: "data":[{"time":"...
  // 避免依赖"今天/昨天/明天"等动态字符串
  const dataMarkerIdx = html.indexOf('"data":[{"time":"');
  if (dataMarkerIdx === -1) {
    throw new Error('未找到赛程 JSON 数据标记');
  }

  // 从 data 数组的 [ 开始，向后匹配对应的 ]
  let depth = 0;
  let end = -1;
  let inString = false;
  let escape = false;
  for (let i = dataMarkerIdx + '"data":'.length; i < html.length; i++) {
    const c = html[i];
    if (escape) { escape = false; continue; }
    if (c === '\\') { escape = true; continue; }
    if (c === '"') { inString = !inString; continue; }
    if (inString) continue;
    if (c === '[') depth++;
    else if (c === ']') {
      depth--;
      if (depth === 0) { end = i + 1; break; }
    }
  }

  if (end === -1) throw new Error('未匹配到 data 数组结束');

  const dataArrJson = html.slice(dataMarkerIdx + '"data":'.length, end);
  const dataArr = JSON.parse(dataArrJson);

  // 解析每个 block 的 list 字符串
  for (const block of dataArr) {
    if (typeof block.list === 'string') {
      block.list = JSON.parse(block.list);
    }
  }

  return dataArr;
}

/**
 * 把所有日期块的 list 合并为统一比赛数组
 */
function flattenSchedule(blocks) {
  const all = [];
  for (const block of blocks) {
    if (Array.isArray(block.list)) {
      for (const item of block.list) {
        all.push(item);
      }
    }
  }
  return all;
}

/**
 * 将 list 中的原始 JSON 转换为结构化的比赛对象
 */
function normalizeMatch(raw) {
  // 解码 oriKey: 世界杯#2026-06-12#墨西哥vs南非
  const oriKey = raw.oriKey || '';
  const idParts = parseOriKey(oriKey);

  // matchStage: 小组赛A组第1轮
  const stageMatch = (raw.matchStage || '').match(/小组赛([A-L])组第(\d)轮/);
  const group = stageMatch ? stageMatch[1] : '';
  const round = stageMatch ? parseInt(stageMatch[2]) : 0;

  // vsLine: "2-0" 或 "0-0"
  const vsLine = raw.vsLine || '';

  const statusMap = {
    '0': '未开赛',
    '1': '进行中',
    '2': '已结束',
    '3': '已结束'
  };

  // 优先使用 startTime 中的日期（最权威），否则回退到 oriKey
  const startTime = raw.startTime || '';
  const dateFromStart = startTime.match(/^(\d{4}-\d{2}-\d{2})/) ? RegExp.$1 : idParts.date;

  return {
    matchId: raw.matchId,
    oriKey,
    tournament: idParts.tournament,
    date: dateFromStart,
    startTime,
    time: raw.time,
    weekday: raw.date,
    stage: raw.matchStage,
    group,
    round,
    homeTeam: raw.leftLogo ? raw.leftLogo.name : (idParts.homeTeam || ''),
    awayTeam: raw.rightLogo ? raw.rightLogo.name : (idParts.awayTeam || ''),
    homeScore: raw.scoreInfo ? (raw.scoreInfo.leftRegularScore || null) : null,
    awayScore: raw.scoreInfo ? (raw.scoreInfo.rightRegularScore || null) : null,
    scoreLine: vsLine,
    status: statusMap[raw.matchStatus] || raw.matchStatusText || '',
    statusId: raw.matchStatus,
    statusText: raw.matchStatusText || '',
    dataSourceText: raw.dataSourceText || '',
    resultDesc: raw.resultDesc ? raw.resultDesc.text : '',
    winner: raw.winner || '',
    hasLive: !!raw.hasLive,
    hasLiveOrFlash: !!raw.hasLiveOrFlash,
    hot: raw.hot || 0,
    startTimeStamp: raw.startTimeStamp,
    detailUrl: `https://tiyu.baidu.com${raw.link}`
  };
}

function parseOriKey(oriKey) {
  const m = oriKey.match(/^(.+?)#(\d{4}-\d{2}-\d{2})#(.+?)vs(.+)$/);
  if (!m) return { tournament: '', date: '', homeTeam: '', awayTeam: '' };
  return {
    tournament: m[1],
    date: m[2],
    homeTeam: m[3],
    awayTeam: m[4]
  };
}

/**
 * 获取赛程并转换为标准格式
 */
async function fetchAllSchedule() {
  const html = await httpGet(SCHEDULE_URL);
  const blocks = extractScheduleJson(html);
  const raw = flattenSchedule(blocks);
  return raw.map(normalizeMatch);
}

function filterByDate(matches, date) {
  return matches.filter(m => m.date === date);
}

function filterByGroup(matches, group) {
  const g = group.toUpperCase();
  return matches.filter(m => m.group === g);
}

function filterByTeam(matches, teamName) {
  return matches.filter(m => m.homeTeam === teamName || m.awayTeam === teamName);
}

function filterByStage(matches, stage) {
  return matches.filter(m => m.stage.includes(stage));
}

function filterByDateKeyword(matches, keyword, currentDate = new Date()) {
  const today = formatDate(currentDate);
  const tomorrow = formatDate(new Date(currentDate.getTime() + 86400000));
  if (keyword === '今天' || keyword === 'today') return matches.filter(m => m.date === today);
  if (keyword === '明天' || keyword === 'tomorrow') return matches.filter(m => m.date === tomorrow);
  if (/^\d{4}-\d{2}-\d{2}$/.test(keyword)) return matches.filter(m => m.date === keyword);
  if (/^\d{2}-\d{2}$/.test(keyword)) return matches.filter(m => m.date.endsWith('-' + keyword));
  return [];
}

function formatDate(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function getAvailableDates(matches) {
  return Array.from(new Set(matches.map(m => m.date))).sort();
}

function getStats(matches) {
  return {
    total: matches.length,
    finished: matches.filter(m => m.statusId === '2').length,
    pending: matches.filter(m => m.statusId === '0').length,
    live: matches.filter(m => m.statusId === '1').length,
    dateRange: {
      from: matches.length ? matches.reduce((a, b) => a.date < b.date ? a : b).date : '',
      to: matches.length ? matches.reduce((a, b) => a.date > b.date ? a : b).date : ''
    }
  };
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'all':
      case '--all':
      case '-a': {
        const dateKeyword = args[1];
        const matches = await fetchAllSchedule();
        const result = dateKeyword ? filterByDateKeyword(matches, dateKeyword) : matches;
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case 'today': {
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(filterByDateKeyword(matches, '今天'), null, 2));
        break;
      }

      case 'tomorrow': {
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(filterByDateKeyword(matches, '明天'), null, 2));
        break;
      }

      case 'date': {
        const date = args[1];
        if (!date) {
          console.error('Error: 请提供日期，例如 2026-06-12 或 06-12');
          process.exit(1);
        }
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(filterByDateKeyword(matches, date), null, 2));
        break;
      }

      case 'group':
      case '-g': {
        const group = args[1];
        if (!group) {
          console.error('Error: 请提供小组标识，例如 A、B');
          process.exit(1);
        }
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(filterByGroup(matches, group), null, 2));
        break;
      }

      case 'team':
      case '-t': {
        const teamName = args[1];
        if (!teamName) {
          console.error('Error: 请提供球队名称');
          process.exit(1);
        }
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(filterByTeam(matches, teamName), null, 2));
        break;
      }

      case 'stage': {
        const stage = args[1];
        if (!stage) {
          console.error('Error: 请提供阶段关键字，例如 小组赛、淘汰赛');
          process.exit(1);
        }
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(filterByStage(matches, stage), null, 2));
        break;
      }

      case 'dates': {
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(getAvailableDates(matches), null, 2));
        break;
      }

      case 'stats': {
        const matches = await fetchAllSchedule();
        console.log(JSON.stringify(getStats(matches), null, 2));
        break;
      }

      default:
        console.log(`
2026年世界杯赛程获取工具

用法:
  node worldcup-schedule.js <command> [options]

命令:
  all, -a [日期]      获取全部赛程，可选日期过滤 (今天/明天/2026-06-12/06-12)
  today                获取今天的赛程
  tomorrow             获取明天的赛程
  date <日期>          获取指定日期的赛程
  group, -g <A-L>      获取指定小组的赛程
  team, -t <球队名>    获取指定球队的赛程
  stage <阶段>         按阶段筛选（小组赛/淘汰赛）
  dates                获取可用的日期列表
  stats                获取赛程统计信息

示例:
  node worldcup-schedule.js all
  node worldcup-schedule.js all today
  node worldcup-schedule.js date 2026-06-14
  node worldcup-schedule.js group A
  node worldcup-schedule.js team 巴西
  node worldcup-schedule.js stage 小组赛
  node worldcup-schedule.js dates
  node worldcup-schedule.js stats
`);
        process.exit(0);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = {
  fetchAllSchedule,
  extractScheduleJson,
  flattenSchedule,
  normalizeMatch,
  parseOriKey,
  filterByDate,
  filterByGroup,
  filterByTeam,
  filterByStage,
  filterByDateKeyword,
  getAvailableDates,
  getStats
};

if (require.main === module) {
  main();
}