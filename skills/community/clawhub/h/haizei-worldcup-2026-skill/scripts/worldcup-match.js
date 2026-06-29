#!/usr/bin/env node

/**
 * 2026年世界杯比赛详情获取工具
 * 从百度体育比赛详情页抓取多 tab 数据
 *
 * 6个tab:
 *   分析    - 情报、历史战绩、赛前预测、猜胜负
 *   阵容    - 双方首发/替补/阵型/场地/裁判
 *   聊天    - 聊天室
 *   赛况    - 比赛实况：进球/红黄牌/换人事件流，场地信息
 *   统计    - 控球/射门/角球等技术统计
 *   指数    - 多家博彩公司赔率
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

const DETAIL_URL = 'https://tiyu.baidu.com/al/live/detail';

const VALID_TABS = ['分析', '阵容', '聊天', '赛况', '统计', '指数'];

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
 * 提取页面中嵌入的 JSON 数据
 * 未开始/已结束: {"data":{"header":{...}, ...}, "data":{tabData}}
 * 进行中:      {"data":{"headLive":{...}, ...}, "data":{tabData}}
 * 第二个 "data":{ 是 tab 数据
 */
function extractDetailJson(html) {
  const matches = [...html.matchAll(/"data":\{/g)];
  if (matches.length < 2) {
    throw new Error('未找到比赛详情 JSON 数据');
  }

  // 第一个 data 是 header/headLive，第二个是 tab 数据
  const headerStart = matches[0].index + '"data":'.length;
  const tabStart = matches[1].index + '"data":'.length;

  const headerEnd = findMatchingBrace(html, headerStart);
  const tabEnd = findMatchingBrace(html, tabStart);

  const headerObj = JSON.parse(html.slice(headerStart, headerEnd));
  // 进行中的比赛用 headLive，已开始/未开始/已结束用 header
  return {
    header: headerObj.header || headerObj.headLive || headerObj,
    tabData: JSON.parse(html.slice(tabStart, tabEnd))
  };
}

function findMatchingBrace(str, start) {
  let depth = 0;
  let inString = false;
  let escape = false;
  for (let i = start; i < str.length; i++) {
    const c = str[i];
    if (escape) { escape = false; continue; }
    if (c === '\\') { escape = true; continue; }
    if (c === '"') { inString = !inString; continue; }
    if (inString) continue;
    if (c === '{') depth++;
    else if (c === '}') {
      depth--;
      if (depth === 0) return i + 1;
    }
  }
  return -1;
}

function extractTeamId(link) {
  if (!link) return '';
  const m = link.match(/id=([a-f0-9]+)/);
  return m ? m[1] : '';
}

/**
 * 解析 header：比赛基本信息
 */
function parseHeader(header) {
  return {
    game: header.game || '',
    matchDesc: header.matchDesc || '',
    matchStage: header.matchStage || '',
    date: header.date || '',
    dateFormat: header.dateFormat || '',
    weekday: header.weekday || '',
    time: header.time || '',
    timestamp: header.timestamp || 0,
    startTime: header.timestamp ? new Date(header.timestamp * 1000).toISOString() : '',
    status: header.status || '',
    matchStatus: header.matchStatus || '',
    matchStatusText: header.matchStatusText || '',
    vs: header.vs || '',
    winner: header.winner || '',
    hasLive: !!header.hasLive,
    hasFlash: !!header.hasFlash,
    hasVipLive: !!header.hasVipLive,
    hot: header.hot || 0,
    plainKey: header.plaintext_key || header.rawKey || '',
    homeTeam: {
      name: header.leftLogo ? header.leftLogo.name : '',
      score: header.leftLogo ? header.leftLogo.score : '',
      logo: header.leftLogo ? header.leftLogo.logo : '',
      rank: header.leftLogo && header.leftLogo.rankInfo1 ? header.leftLogo.rankInfo1.text : '',
      teamId: extractTeamId(header.leftLogo ? header.leftLogo.link : '')
    },
    awayTeam: {
      name: header.rightLogo ? header.rightLogo.name : '',
      score: header.rightLogo ? header.rightLogo.score : '',
      logo: header.rightLogo ? header.rightLogo.logo : '',
      rank: header.rightLogo && header.rightLogo.rankInfo1 ? header.rightLogo.rankInfo1.text : '',
      teamId: extractTeamId(header.rightLogo ? header.rightLogo.link : '')
    },
    liveList: (header.pcLiveList || []).map(l => ({
      name: l.name,
      category: l.category,
      link: l.link,
      isExternal: l.to === 'out'
    }))
  };
}

/**
 * 解析"分析"tab
 */
function parseAnalysis(data) {
  if (!data) return null;
  const result = {};

  if (Array.isArray(data.igence)) {
    result.intelligence = data.igence.map(item => ({
      title: item.intelligencetitle || '',
      homeTeam: item.intelligence ? item.intelligence.intelligenceTeamInfo : null,
      homeTeamPoints: item.intelligence ? (item.intelligence.intelligenceteam || []).map(p => p.content) : [],
      awayTeam: item.intelligence ? item.intelligence.intelligenceteamLeaterInfo : null,
      awayTeamPoints: item.intelligence ? (item.intelligence.intelligenceteamleater || []).map(p => p.content) : []
    }));
  }

  if (Array.isArray(data.homeRecord)) {
    result.records = data.homeRecord.map(rec => {
      const h = rec.history || {};
      return {
        title: h.title || '',
        subTitle: h.subTitle || '',
        result: h.result || '',
        resultArr: h.resultArr || null,
        probability: h.probability || [],
        matches: (h.list || []).map(m => ({
          date: m.date,
          match: m.match,
          home: { name: m.left.name, score: m.left.score, isWin: m.left.isWin },
          away: { name: m.right.name, score: m.right.score, isWin: m.right.isWin },
          score: m.vs,
          handicap: m.oddsHandicap,
          totalGoals: m.oddsTotalGoals
        }))
      };
    });
  }

  if (data.result) {
    result.prediction = {
      sampleSize: data.result.num,
      homeWinRate: data.result.team && data.result.team[0] ? data.result.team[0].winrate : '',
      awayWinRate: data.result.team && data.result.team[1] ? data.result.team[1].winrate : '',
      similarOddsHistory: {
        homeWin: data.result.percentage.victory,
        draw: data.result.percentage.draw,
        awayWin: data.result.percentage.lost
      },
      teams: data.result.team || []
    };
  }

  if (data.guess && data.guess.data) {
    result.guess = {
      title: data.guess.title,
      total: data.guess.total,
      deadline: data.guess.deadlineTime,
      options: data.guess.data.map(d => ({
        name: d.name,
        count: d.count,
        percentage: data.guess.total > 0 ? ((d.count / data.guess.total) * 100).toFixed(1) + '%' : '0%'
      }))
    };
  }

  return result;
}

/**
 * 解析"阵容"tab
 */
function parseLineup(data) {
  if (!data) return null;
  const parseTeam = (t) => {
    if (!t) return null;
    const parsePlayer = (p) => ({
      name: p.name,
      number: p.number,
      position: p.position,
      playerId: p.playerId,
      nation: p.nation ? p.nation.name : '',
      coordinate: p.coordinate || null,
      incidents: p.incidents || []
    });
    return {
      name: t.name,
      logo: t.logo,
      formation: t.formation,
      starter: (t.starter || []).map(parsePlayer),
      substitute: (t.substitute || []).map(parsePlayer),
      playerList: (t.playerList || []).map(parsePlayer)
    };
  };
  return {
    confirmed: data.confirmed,
    updateTime: data.update_time,
    court: data.court,
    referee: data.referee,
    home: parseTeam(data.home),
    away: parseTeam(data.away)
  };
}

/**
 * 解析"赛况"tab
 */
function parseLive(data) {
  if (!data) return null;
  return {
    venue: data.graphic_incidents ? data.graphic_incidents.venue : null,
    narrative: data.graphic_incidents ? (data.graphic_incidents.graphic || []).map(g => ({
      text: g.word,
      time: g.time,
      teamName: g.teamName,
      iconType: g.icon_type,
      position: g.position
    })) : [],
    incidents: data.graphic_incidents ? (data.graphic_incidents.incidents || []).map(i => ({
      type: i.type,
      text: i.text,
      goalType: i.goaltype,
      passedTime: i.passedTime,
      sortTime: i.sortTime,
      team: i.right ? i.right.teamName : (i.left ? i.left.teamName : ''),
      direction: i.right ? 'away' : (i.left ? 'home' : ''),
      detail: i.detail || null
    })) : [],
    events: data.events
  };
}

/**
 * 解析"统计"tab
 */
function parseStats(data) {
  if (!data) return null;
  const stats = data['line-statistics'];
  if (!stats) return null;
  return {
    title: stats.title,
    homeTeam: stats.team ? stats.team.left.name : '',
    awayTeam: stats.team ? stats.team.right.name : '',
    items: (stats.list || []).map(item => ({
      name: item.title,
      home: item.left,
      away: item.right
    }))
  };
}

/**
 * 解析"指数"tab
 */
function parseOdds(data) {
  if (!data) return null;
  return {
    asyncTime: data.asyncTime,
    bookmakers: (data.list || []).map(b => ({
      datas: (b.datas || []).map(d => ({
        initial: d.initial,
        now: d.now,
        history: d.history
      }))
    }))
  };
}

/**
 * 获取比赛详情
 */
async function fetchMatchDetail(matchId, tab = '分析') {
  const url = `${DETAIL_URL}?matchId=${encodeURIComponent(matchId)}&tab=${encodeURIComponent(tab)}`;
  const html = await httpGet(url);
  const { header, tabData } = extractDetailJson(html);

  const result = {
    matchId,
    tab,
    match: parseHeader(header),
    tabData: null
  };

  switch (tab) {
    case '分析': result.tabData = parseAnalysis(tabData); break;
    case '阵容': result.tabData = parseLineup(tabData); break;
    case '赛况': result.tabData = parseLive(tabData); break;
    case '统计': result.tabData = parseStats(tabData); break;
    case '指数': result.tabData = parseOdds(tabData); break;
    case '聊天': result.tabData = tabData; break;
    default: result.tabData = tabData;
  }

  return result;
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'detail':
      case 'get':
      case '-d': {
        const matchId = args[1];
        const tab = args[2] || '分析';
        if (!matchId) {
          console.error('Error: 请提供 matchId');
          process.exit(1);
        }
        const detail = await fetchMatchDetail(matchId, tab);
        console.log(JSON.stringify(detail, null, 2));
        break;
      }

      case 'info': {
        const matchId = args[1];
        if (!matchId) {
          console.error('Error: 请提供 matchId');
          process.exit(1);
        }
        const detail = await fetchMatchDetail(matchId, '分析');
        console.log(JSON.stringify(detail.match, null, 2));
        break;
      }

      case 'analysis':
      case 'lineup':
      case 'live':
      case 'stats':
      case 'odds': {
        const matchId = args[1];
        if (!matchId) {
          console.error('Error: 请提供 matchId');
          process.exit(1);
        }
        const tabMap = { analysis: '分析', lineup: '阵容', live: '赛况', stats: '统计', odds: '指数' };
        const tab = tabMap[command];
        const detail = await fetchMatchDetail(matchId, tab);
        console.log(JSON.stringify(detail.tabData, null, 2));
        break;
      }

      case 'help':
      default:
        console.log(`
2026年世界杯比赛详情获取工具

用法:
  node worldcup-match.js <command> <matchId> [tab]

命令:
  info <matchId>                    比赛基本信息
  analysis <matchId>                分析数据（情报/历史战绩/预测/猜胜负）
  lineup <matchId>                  阵容数据（首发/替补/阵型/裁判）
  live <matchId>                    赛况数据（事件流/场地信息）
  stats <matchId>                   统计数据（控球/射门/角球等）
  odds <matchId>                    指数数据（多家博彩公司赔率）
  detail <matchId> [tab]            完整详情（默认 分析）

可用tab:
  分析 (analysis)  - 情报、历史战绩、赛前预测、猜胜负
  阵容 (lineup)    - 首发、替补、阵型、场地、裁判
  赛况 (live)      - 比赛事件流（进球/红黄牌/换人）、场地信息
  统计 (stats)     - 控球率/射门/角球等技术统计（仅已结束比赛）
  指数 (odds)      - 多家博彩公司初盘/即时盘
  聊天 (chat)      - 聊天室信息

示例:
  node worldcup-match.js info 5LiW55WM...
  node worldcup-match.js analysis 5LiW55WM...
  node worldcup-match.js lineup 5LiW55WM...
  node worldcup-match.js live 5LiW55WM...
  node worldcup-match.js stats 5LiW55WM...
`);
        process.exit(0);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = {
  fetchMatchDetail,
  extractDetailJson,
  parseHeader,
  parseAnalysis,
  parseLineup,
  parseLive,
  parseStats,
  parseOdds,
  VALID_TABS
};

if (require.main === module) {
  main();
}