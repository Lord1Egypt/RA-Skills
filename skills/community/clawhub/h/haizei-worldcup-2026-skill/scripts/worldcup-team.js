#!/usr/bin/env node

/**
 * 2026年世界杯球队数据获取工具
 * 从百度体育球队页抓取赛程/阵容/资料/历史成绩/数据
 */

const https = require('https');
const path = require('path');
const fs = require('fs');
const { getRandomUserAgent } = require('./lib/user-agents');
const { loadTeams, findTeamByName, lookupTeam, resolveTeamId, isTeamId } = require('./lib/teams');

const HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding': 'identity',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Referer': 'https://tiyu.baidu.com/',
  'Origin': 'https://tiyu.baidu.com'
};

const TEAM_URL = 'https://tiyu.baidu.com/al/team';

const VALID_TABS = ['赛程', '阵容', '资料', '历史成绩', '球迷圈', '数据'];

const TAB_TO_INDEX = {
  '赛程': 0,
  '阵容': 1,
  '资料': 2,
  '历史成绩': 3,
  '球迷圈': 4,
  '数据': 5
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

/**
 * 提取页面中的 tabsList 数据
 */
function extractTabsList(html) {
  const idx = html.indexOf('tabsList');
  if (idx === -1) throw new Error('未找到 tabsList 标记');
  const arrStart = html.indexOf('[', idx);
  if (arrStart === -1) throw new Error('未找到 tabsList 数组');
  const end = findMatchingBrace(html, arrStart);
  if (end === -1) throw new Error('tabsList 数组未闭合');
  return JSON.parse(html.slice(arrStart, end));
}

/**
 * 获取球队基础信息（页头）
 */
function extractTeamHeader(html) {
  // 查找 "name": "加拿大" 之类
  const m = html.match(/"name":"([^"]+)","nameEn":"([^"]*)"[^}]*"logo":"([^"]+)"/);
  if (!m) {
    // 尝试另一种格式
    const m2 = html.match(/"name":"([^"]+)"[^}]*"logo":"(https:\/\/[^"]+)"/);
    if (m2) return { name: m2[1], logo: m2[2] };
    return null;
  }
  return { name: m[1], nameEn: m[2], logo: m[3] };
}

/**
 * 解析赛程 tab（item 0）
 */
function parseSchedule(item) {
  if (!item || !item.subTabList) return null;
  const result = { subTabs: item.subTabs || [], competitions: {} };
  for (const sub of item.subTabList) {
    result.competitions[sub.id] = {
      title: sub.title,
      index: sub.index,
      matches: []
    };
    for (const dayBlock of sub.data || []) {
      for (const m of dayBlock.list || []) {
        result.competitions[sub.id].matches.push(normalizeTeamMatch(m));
      }
    }
  }
  return result;
}

function normalizeTeamMatch(m) {
  return {
    matchId: m.matchId,
    oriKey: m.oriKey,
    date: m.startTime ? m.startTime.split(' ')[0] : '',
    time: m.time,
    weekday: m.weekday,
    stage: m.matchStage,
    matchName: m.matchName,
    homeTeam: m.leftLogo ? m.leftLogo.name : '',
    awayTeam: m.rightLogo ? m.rightLogo.name : '',
    homeScore: m.scoreInfo ? m.scoreInfo.leftRegularScore : '',
    awayScore: m.scoreInfo ? m.scoreInfo.rightRegularScore : '',
    scoreLine: m.vsLine,
    status: m.matchStatusText,
    statusId: m.matchStatus,
    isHome: m.leftLogo && m.leftLogo.name === (m.leftLogo ? m.leftLogo.name : '') ? null : null,
    competition: m.game
  };
}

/**
 * 解析阵容 tab（item 1）
 */
function parseLineup(item) {
  if (!item) return null;
  return {
    coaching: (item.coach || []).map(c => ({
      name: c.name,
      subTitle: c.subTitle,
      avatar: c.avatar,
      url: c.url
    })),
    players: (item.data || []).map(group => ({
      position: group.position,
      columnTitles: (group.title || []).map(t => ({ field: t.field, name: t.name, type: t.type })),
      players: (group.data || []).map(p => ({
        name: p.name,
        number: p.number,
        age: p.age,
        playerId: p.playerId,
        club: p.teamName,
        avatar: p.avatar,
        link: p.link,
        goals: p.goals,
        court: p.court,
        assists: p.assists,
        value: p.value,
        saves: p.saves,
        runsOut: p.runs_out_combined
      }))
    }))
  };
}

/**
 * 解析资料 tab（item 2）
 */
function parseInfo(item) {
  if (!item || !item.data) return null;
  const data = item.data;
  return {
    baseInfo: data.baseInfo ? {
      title: data.baseInfo.title,
      items: (data.baseInfo.info || []).map(i => ({
        name: i.name,
        content: i.content,
        link: i.link,
        naTabInfo: i.naTabInfo
      }))
    } : null,
    honor: data.honor ? {
      title: data.honor.title,
      awards: (data.honor.honor || []).map(h => ({
        title: h.match,
        years: h.list
      }))
    } : null
  };
}

/**
 * 解析历史成绩 tab（item 3）
 */
function parseHistory(item) {
  if (!item || !item.data) return null;
  return {
    records: (Array.isArray(item.data) ? item.data : []).map(r => ({
      season: r.season,
      description: r.mark_desc,
      groupMatches: r.group_mark || [],
      url: r.jump_info ? r.jump_info.url : ''
    }))
  };
}

/**
 * 解析数据 tab（item 5）
 * 结构: {data: {honor, seasonStats: [{match, season, scope, rank, stats: [{group, groupField, list}]}], wiki}}
 */
function parseStats(item) {
  if (!item || !item.data) return null;
  const data = item.data;
  return {
    honor: data.honor ? data.honor.list : null,
    seasonStats: (data.seasonStats || []).map(ss => ({
      competition: ss.match,
      season: ss.season,
      scope: ss.scope,
      rank: ss.rank || null,
      statGroups: (ss.stats || []).map(g => ({
        group: g.group,
        field: g.groupField,
        items: (g.list || []).map(s => ({
          name: s.name,
          field: s.field,
          value: s.value,
          average: s.average,
          rank: s.rank,
          ranking: s.ranking,
          rankingText: s.rankingTxt
        }))
      }))
    })),
    wiki: data.wiki
  };
}

/**
 * 获取球队数据
 */
async function fetchTeamData(teamId, tab = '资料', options = {}) {
  const params = new URLSearchParams({ id: teamId, tab });
  if (options.season) params.set('season', options.season);
  if (options.scope) params.set('scope', options.scope);
  if (options.subTab) params.set('subTab', options.subTab);

  const url = `${TEAM_URL}?${params.toString()}`;
  const html = await httpGet(url);

  const tabsList = extractTabsList(html);
  const header = extractTeamHeader(html);
  const tabIndex = TAB_TO_INDEX[tab];
  const item = tabsList[tabIndex];

  const result = {
    teamId,
    tab,
    header,
    options,
    tabData: null
  };

  switch (tab) {
    case '赛程': result.tabData = parseSchedule(item); break;
    case '阵容': result.tabData = parseLineup(item); break;
    case '资料': result.tabData = parseInfo(item); break;
    case '历史成绩': result.tabData = parseHistory(item); break;
    case '数据': result.tabData = parseStats(item); break;
    case '球迷圈': result.tabData = item; break;
    default: result.tabData = item;
  }

  return result;
}

function resolveArg(input) {
  if (!input || isTeamId(input)) return input;
  const data = loadTeams();
  const team = lookupTeam(input, data);
  if (!team) return input;
  return team.teamId;
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'info': {
        const teamId = resolveArg(args[1]);
        if (!teamId) {
          console.error('Error: 请提供 teamId 或球队名称');
          process.exit(1);
        }
        const data = await fetchTeamData(teamId, '资料');
        console.log(JSON.stringify(data.tabData, null, 2));
        break;
      }

      case 'schedule': {
        const teamId = resolveArg(args[1]);
        const competition = args[2];
        if (!teamId) {
          console.error('Error: 请提供 teamId 或球队名称');
          process.exit(1);
        }
        const data = await fetchTeamData(teamId, '赛程');
        if (competition && data.tabData.competitions[competition]) {
          console.log(JSON.stringify(data.tabData.competitions[competition], null, 2));
        } else {
          console.log(JSON.stringify(data.tabData, null, 2));
        }
        break;
      }

      case 'lineup': {
        const teamId = resolveArg(args[1]);
        if (!teamId) {
          console.error('Error: 请提供 teamId 或球队名称');
          process.exit(1);
        }
        const data = await fetchTeamData(teamId, '阵容');
        console.log(JSON.stringify(data.tabData, null, 2));
        break;
      }

      case 'history': {
        const teamId = resolveArg(args[1]);
        if (!teamId) {
          console.error('Error: 请提供 teamId 或球队名称');
          process.exit(1);
        }
        const data = await fetchTeamData(teamId, '历史成绩');
        console.log(JSON.stringify(data.tabData, null, 2));
        break;
      }

      case 'stats': {
        const teamId = resolveArg(args[1]);
        const season = args[2] || '2026';
        const scope = args[3] || '小组赛';
        if (!teamId) {
          console.error('Error: 请提供 teamId 或球队名称');
          process.exit(1);
        }
        const data = await fetchTeamData(teamId, '数据', { season, scope });
        // 过滤seasonStats
        if (Array.isArray(data.tabData.seasonStats)) {
          const filtered = data.tabData.seasonStats.filter(s => s.season === season);
          if (filtered.length === 0) {
            console.error(`未找到 ${season} 年数据，可用赛季: ${data.tabData.seasonStats.map(s => s.season).join(', ')}`);
            process.exit(1);
          }
          console.log(JSON.stringify({ ...data.tabData, seasonStats: filtered }, null, 2));
        } else {
          console.log(JSON.stringify(data.tabData, null, 2));
        }
        break;
      }

      case 'tabs': {
        console.log(JSON.stringify(VALID_TABS, null, 2));
        break;
      }

      case 'lookup': {
        const name = args[1];
        if (!name) {
          console.error('Error: 请提供球队名称');
          process.exit(1);
        }
        const data = loadTeams();
        const team = findTeamByName(data, name);
        if (!team) {
          console.error(`未找到球队: ${name}`);
          process.exit(1);
        }
        console.log(JSON.stringify(team, null, 2));
        break;
      }

      case 'help':
      default:
        console.log(`
2026年世界杯球队数据获取工具

用法:
  node worldcup-team.js <command> [args]

命令:
  lookup <球队名>          通过球队名查找 teamId（从 teams.json）
  info <teamId|球队名>     球队资料（自动识别名称或ID）
  schedule <teamId|球队名> [赛事] 球队赛程（赛事可选: all/世界杯/国际友谊赛）
  lineup <teamId|球队名>   球队阵容（教练组 + 球员按位置分组）
  history <teamId|球队名>  历史成绩（世界杯参赛记录）
  stats <teamId|球队名> [赛事] [scope] 球队数据统计（scope: 小组赛/全部）
  tabs                     列出可用tab

示例:
  node worldcup-team.js lookup 加拿大
  node worldcup-team.js info 35779c25e9dec553f154e9d6286925e6
  node worldcup-team.js info 巴西
  node worldcup-team.js schedule 巴西 世界杯
  node worldcup-team.js lineup 法国
  node worldcup-team.js history 35779c25e9dec553f154e9d6286925e6
  node worldcup-team.js stats 巴西 2026 小组赛
`);
        process.exit(0);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = {
  fetchTeamData,
  extractTabsList,
  parseSchedule,
  parseLineup,
  parseInfo,
  parseHistory,
  parseStats,
  VALID_TABS,
  TAB_TO_INDEX
};

if (require.main === module) {
  main();
}