#!/usr/bin/env node

/**
 * 2026年世界杯球员数据获取工具
 * 从百度体育球员页抓取资料/动态/数据/赛程
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

const PLAYER_URL = 'https://tiyu.baidu.com/al/player';

const VALID_TABS = ['赛程', '评分', '动态', '资料', '数据'];

const TAB_TO_INDEX = {
  '赛程': 0,
  '评分': 1,
  '动态': 2,
  '资料': 3,
  '数据': 4
};

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
    if (c === '[') depth++;
    else if (c === ']') {
      depth--;
      if (depth === 0) return i + 1;
    }
  }
  return -1;
}

function extractTabsList(html) {
  const idx = html.indexOf('tabsList');
  if (idx === -1) throw new Error('未找到 tabsList 标记');
  const arrStart = html.indexOf('[', idx);
  const end = findMatchingBrace(html, arrStart);
  if (end === -1) throw new Error('tabsList 数组未闭合');
  return JSON.parse(html.slice(arrStart, end));
}

/**
 * 解析赛程 tab（item 0）
 */
function parseSchedule(item) {
  if (!item || !item.subTabList) return null;
  const result = { subTabs: item.subTabs || [], teams: {} };
  for (const sub of item.subTabList) {
    result.teams[sub.id] = {
      title: sub.title,
      teamId: sub.id,
      matches: []
    };
    for (const dayBlock of sub.data || []) {
      for (const m of dayBlock.list || []) {
        result.teams[sub.id].matches.push({
          matchId: m.matchId,
          oriKey: m.oriKey,
          date: m.startTime ? m.startTime.split(' ')[0] : '',
          time: m.time,
          weekday: m.weekday,
          stage: m.matchStage,
          homeTeam: m.leftLogo ? m.leftLogo.name : '',
          awayTeam: m.rightLogo ? m.rightLogo.name : '',
          homeScore: m.scoreInfo ? m.scoreInfo.leftRegularScore : '',
          awayScore: m.scoreInfo ? m.scoreInfo.rightRegularScore : '',
          scoreLine: m.vsLine,
          status: m.matchStatusText,
          competition: m.game
        });
      }
    }
  }
  return result;
}

/**
 * 解析评分 tab（item 1）
 */
function parseRatings(item) {
  return item && Object.keys(item).length > 1 ? item : null;
}

/**
 * 解析动态 tab（item 2）
 */
function parseNews(item) {
  if (!item) return null;
  return {
    total: item.pn || (item.newsList || []).length,
    newsList: (item.newsList || []).map(n => ({
      title: n.title,
      link: n.link,
      linkType: n.linkType,
      endTime: n.endTime,
      factorTime: n.factorTime,
      source: n.source,
      nid: n.nid,
      img: n.img,
      single: n.single
    }))
  };
}

/**
 * 解析资料 tab（item 3）
 * data: {ability, honor, honorRecords, market, transfer, wiki}
 */
function parseInfo(item) {
  if (!item || !item.data) return null;
  const data = item.data;

  const wiki = data.wiki || {};
  const detail = wiki.detail || {};

  return {
    wiki: {
      num: wiki.num,
      img: wiki.img,
      nickName: wiki.nickName,
      height: wiki.height,
      weight: wiki.weight,
      detail: {
        position: detail.position,
        heavyFoot: detail.heavyFoot,
        age: detail.age,
        national: detail.national,
        expiryDate: detail.expiryDate,
        socialStatus: detail.socialStatus,
        socialStatusUnit: detail.socialStatusUnit
      },
      list: wiki.list || []
    },
    ability: data.ability ? {
      overall: data.ability.overall,
      overallColor: data.ability.overallColor,
      radarDims: (data.ability.radarDims || []).map(d => ({
        name: d.name,
        value: d.value,
        level: d.level,
        color: d.color
      })),
      categories: data.ability.categories || []
    } : null,
    honor: (data.honor || []).map(h => ({
      match: h.match,
      logo: h.logo,
      seasons: (h.list || []).map(l => ({ date: l.date, logo: l.logo }))
    })),
    honorRecords: (data.honorRecords || []).map(r => ({
      honorName: r.honorName,
      totalWins: r.totalWins,
      seasons: r.seasons || []
    })),
    transfer: data.transfer ? {
      unit: data.transfer.unit,
      list: (data.transfer.list || []).map(t => ({
        date: t.date,
        description: t.description,
        price: t.price,
        team: t.team,
        teamLogo: t.teamLogo,
        outTeam: t.outTeam,
        outTeamLogo: t.outTeamLogo
      }))
    } : null,
    market: data.market || null
  };
}

/**
 * 解析数据 tab（item 4）
 * data: {seasonStats: [{match, season, rank, stats: [{group, list}]}]}
 */
function parseStats(item) {
  if (!item || !item.data) return null;
  const data = item.data;
  return {
    seasonStats: (data.seasonStats || []).map(ss => ({
      competition: ss.match,
      season: ss.season,
      rank: ss.rank || null,
      statGroups: (ss.stats || []).map(g => ({
        group: g.group,
        field: g.groupField,
        items: (g.list || []).map(s => ({
          name: s.name,
          value: s.value,
          average: s.average,
          rank: s.rank,
          ranking: s.ranking,
          rankingText: s.rankingTxt
        }))
      }))
    }))
  };
}

/**
 * 获取球员数据
 */
async function fetchPlayerData(playerId, tab = '资料') {
  const url = `${PLAYER_URL}?id=${encodeURIComponent(playerId)}&tab=${encodeURIComponent(tab)}`;
  const html = await httpGet(url);
  const tabsList = extractTabsList(html);
  const tabIndex = TAB_TO_INDEX[tab];
  const item = tabsList[tabIndex];

  const result = { playerId, tab, tabData: null };

  switch (tab) {
    case '赛程': result.tabData = parseSchedule(item); break;
    case '评分': result.tabData = parseRatings(item); break;
    case '动态': result.tabData = parseNews(item); break;
    case '资料': result.tabData = parseInfo(item); break;
    case '数据': result.tabData = parseStats(item); break;
    default: result.tabData = item;
  }

  return result;
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'info': {
        const playerId = args[1];
        if (!playerId) {
          console.error('Error: 请提供 playerId');
          process.exit(1);
        }
        const data = await fetchPlayerData(playerId, '资料');
        console.log(JSON.stringify(data.tabData, null, 2));
        break;
      }

      case 'news':
      case '动态': {
        const playerId = args[1];
        if (!playerId) {
          console.error('Error: 请提供 playerId');
          process.exit(1);
        }
        const data = await fetchPlayerData(playerId, '动态');
        console.log(JSON.stringify(data.tabData, null, 2));
        break;
      }

      case 'stats':
      case '数据': {
        const playerId = args[1];
        const season = args[2];
        const competition = args[3];
        if (!playerId) {
          console.error('Error: 请提供 playerId');
          process.exit(1);
        }
        const data = await fetchPlayerData(playerId, '数据');
        let stats = data.tabData.seasonStats;
        if (season) stats = stats.filter(s => s.season === season);
        if (competition) stats = stats.filter(s => s.competition === competition);
        console.log(JSON.stringify({ seasonStats: stats }, null, 2));
        break;
      }

      case 'schedule': {
        const playerId = args[1];
        if (!playerId) {
          console.error('Error: 请提供 playerId');
          process.exit(1);
        }
        const data = await fetchPlayerData(playerId, '赛程');
        console.log(JSON.stringify(data.tabData, null, 2));
        break;
      }

      case 'detail': {
        const playerId = args[1];
        const tab = args[2] || '资料';
        if (!playerId) {
          console.error('Error: 请提供 playerId');
          process.exit(1);
        }
        const data = await fetchPlayerData(playerId, tab);
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case 'help':
      default:
        console.log(`
2026年世界杯球员数据获取工具

用法:
  node worldcup-player.js <command> <playerId> [args]

命令:
  info <playerId>                    球员资料（基本资料+能力雷达+荣誉+转会）
  news <playerId>                    球员动态（新闻列表）
  stats <playerId> [赛季] [赛事]     球员数据统计
  schedule <playerId>                球员赛程（按俱乐部/国家队）
  detail <playerId> [tab]            完整详情（默认资料）

可用tab:
  资料 (info)    - 基本资料/能力雷达/荣誉/转会历史
  动态 (news)    - 球员相关新闻
  数据 (stats)   - 球员多维数据统计（按赛事+赛季）
  赛程 (schedule)- 球员出场记录
  评分 (ratings) - 球员评分

示例:
  node worldcup-player.js info 4262f62d5769aaf16ecc96d12bdf6b57
  node worldcup-player.js news 4262f62d5769aaf16ecc96d12bdf6b57
  node worldcup-player.js stats 7bf18ff5b176d56a734dd90598461b2b 2026 世界杯
  node worldcup-player.js schedule 4262f62d5769aaf16ecc96d12bdf6b57
`);
        process.exit(0);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = {
  fetchPlayerData,
  parseSchedule,
  parseRatings,
  parseNews,
  parseInfo,
  parseStats,
  VALID_TABS,
  TAB_TO_INDEX
};

if (require.main === module) {
  main();
}