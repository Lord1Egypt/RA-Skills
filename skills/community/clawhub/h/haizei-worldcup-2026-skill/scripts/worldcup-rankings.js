#!/usr/bin/env node

/**
 * 2026年世界杯排名数据获取工具
 * 从百度体育赛事页抓取 排名/球队榜/球员榜/FIFA排名 数据
 *
 * 4个tab:
 *   排名      - 小组赛积分榜（12组） + 淘汰赛对阵图
 *   球队榜    - 按数据维度（进球/控球/射门等）的球队排名
 *   球员榜    - 按数据维度（射手/助攻等）的球员排名
 *   FIFA排名  - 国际足联官方排名
 */

const https = require('https');
const { getRandomUserAgent } = require('./lib/user-agents');

const HEADERS = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Encoding': 'identity',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Referer': 'https://tiyu.baidu.com/',
  'Origin': 'https://tiyu.baidu.com'
};

const API_BASE = 'https://tiyu.baidu.com/go/api/header';
const PAGE_BASE = 'https://tiyu.baidu.com/al/match';

// 球员榜分类
const PLAYER_TAB_IDS = {
  '进球': 10, '助攻': 11, '射门': 12, '射正': 13,
  '过人': 23, '过人成功': 24, '任意球': 28, '击中门框': 30,
  '快攻': 31, '快攻射门': 32, '丢失球权': 27, '解围': 18,
  '有效阻挡': 34, '拦截': 22, '抢断': 17, '1对1拼抢': 35,
  '1对1拼抢成功': 36, '拳击球': 37, '守门员出击': 38, '守门员出击成功': 39,
  '高空出击': 40, '传球': 15, '传球成功': 16, '关键传球': 41,
  '传中球': 42, '传中球成功': 43, '长传': 25, '成功长传': 26,
  '传球被断': 44, '红牌': 21, '黄牌': 20, '犯规': 19,
  '被侵犯': 45, '越位': 46
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
        const text = Buffer.concat(chunks).toString('utf-8');
        try {
          resolve(JSON.parse(text));
        } catch (e) {
          reject(new Error(`JSON 解析失败: ${e.message}`));
        }
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

function httpGetHtml(url) {
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
  return JSON.parse(html.slice(arrStart, end));
}

/**
 * 解析小组赛积分榜（Stage.data）
 * record 结构: [teamInfo, played, W/D/L, goals, points]
 */
function parseStageRankings(stage) {
  return {
    title: stage.title,
    type: stage.type,
    rulerDesc: stage.rulerDesc,
    refreshTime: stage.refreshTime,
    updateTime: stage.updateTime,
    columns: stage.cols || [],
    groups: (stage.data || []).map(g => ({
      list: (g.list || []).map(team => {
        const r = team.record || [];
        const teamInfo = r[0] || {};
        return {
          teamId: team.teamId || extractTeamId(team.link || ''),
          teamName: teamInfo.name,
          teamLogo: teamInfo.logo,
          teamRank: teamInfo.rank,
          status: team.fillsName,
          bgColor: team.bgColor,
          isQualified: team.bgColor === '#456de6',
          isRelegated: team.bgColor === '#ff5050',
          played: r[1] || '',
          winDrawLoss: r[2] || '',
          goals: r[3] || '',
          points: r[4] || '',
          link: team.link,
          naTabInfo: team.naTabInfo
        };
      })
    }))
  };
}

function extractTeamId(link) {
  if (!link) return '';
  const m = link.match(/id=([a-f0-9]+)/);
  return m ? m[1] : '';
}

function extractPlayerId(link) {
  if (!link) return '';
  const m = link.match(/id=([a-f0-9]+)/);
  return m ? m[1] : '';
}

/**
 * 获取小组赛排名（积分榜）
 */
async function fetchGroupStandings() {
  const url = `${API_BASE}?match=%E4%B8%96%E7%95%8C%E6%9D%AF&tab=%E6%8E%92%E5%90%8D&async=1&tab_type=single&page=match&rankChildTab=teamRank`;
  const data = await httpGet(url);
  const item = data.data.tabsList[0];
  return parseStageRankings(item);
}

/**
 * 解析 FIFA 排名
 */
function parseFifaRankings(data) {
  return {
    highlightTeamId: data.highlightTeamId,
    text: data.text,
    rankings: (data.ranking || []).map(r => ({
      rank: r.ranking,
      teamId: r.team.id,
      teamName: r.team.name_zh,
      logo: r.team.logo,
      points: r.points,
      positionChanged: r.position_changed,
      highlight: r.highlight
    }))
  };
}

/**
 * 获取 FIFA 排名
 */
async function fetchFifaRankings() {
  const url = `${API_BASE}?match=%E4%B8%96%E7%95%8C%E6%9D%AF&tab=FIFA%E6%8E%92%E5%90%8D&async=1&tab_type=single&page=match&rankChildTab=fifaRank`;
  const data = await httpGet(url);
  const item = data.data.tabsList[0];
  return parseFifaRankings(item.data);
}

/**
 * 获取球员榜
 * 注意：当前 API 对所有 tabId 返回相同数据（赛事初期的射手榜）
 * 随着比赛进行，其它分类的数据会逐渐丰富
 */
async function fetchPlayerRankings(tabName = '进球', limit = 50) {
  const tabId = PLAYER_TAB_IDS[tabName];
  if (tabId === undefined) {
    throw new Error(`未知的球员榜分类: ${tabName}。可用: ${Object.keys(PLAYER_TAB_IDS).join(', ')}`);
  }
  const url = `${API_BASE}?match=%E4%B8%96%E7%95%8C%E6%9D%AF&tab=%E7%90%83%E5%91%98%E6%A6%9C&async=1&tab_type=single&page=match&rankChildTab=playerRank&tabId=${tabId}`;
  const data = await httpGet(url);
  const item = data.data.tabsList[0];
  const wrapper = item.data && item.data[0];
  if (!wrapper) return { tabName, tabId, players: [] };
  return {
    tabName,
    tabId,
    statsName: wrapper.data && wrapper.data[0] ? wrapper.data[0].statsName : null,
    availableTabs: wrapper.tabs,
    note: 'API 当前仅返回射手榜数据，其它分类待赛事进行后丰富',
    players: (wrapper.data || []).slice(0, limit).map(p => ({
      rank: p.shooterRank,
      playerId: p.playerId,
      playerName: p.playerName,
      team: p.teamName,
      position: p.position,
      score: p.score,
      penaltyValue: p.penaltyValue,
      logo: p.logo,
      link: p.link
    }))
  };
}

/**
 * 获取球队榜（基于赛事统计）
 * 通过 group stage API 获取的 teams[] 数据
 */
async function fetchTeamRankings() {
  // 球队榜 = 排名 tab 中的球队排行
  // 使用 group standings 数据
  return await fetchGroupStandings();
}

/**
 * 获取淘汰赛对阵图（从 HTML 页面解析）
 */
async function fetchKnockoutBracket() {
  const url = `${PAGE_BASE}?match=%E4%B8%96%E7%95%8C%E6%9D%AF&tab=%E6%8E%92%E5%90%8D`;
  const html = await httpGetHtml(url);
  const tabsList = extractTabsList(html);
  // 排名 tab 是 item 1
  const rankingItem = tabsList[1];
  if (!rankingItem) return null;
  return {
    currentTab: rankingItem.currentTab,
    subCurrentTab: rankingItem.subCurrentTab,
    refreshTime: rankingItem.refreshTime,
    tabList: rankingItem.tabList,
    fifawc: rankingItem.fifawc,
    asyncUrl: rankingItem.asyncUrl,
    raw: rankingItem
  };
}

/**
 * 获取可用的球员榜分类
 */
function getPlayerTabNames() {
  return Object.keys(PLAYER_TAB_IDS);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'standings':
      case 'groups':
      case '积分榜': {
        const data = await fetchGroupStandings();
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case 'fifa':
      case 'FIFA排名': {
        const limit = parseInt(args[1]) || 50;
        const data = await fetchFifaRankings();
        if (limit && limit < data.rankings.length) {
          data.rankings = data.rankings.slice(0, limit);
        }
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case 'players':
      case '球员榜': {
        const tabName = args[1] || '进球';
        const limit = parseInt(args[2]) || 50;
        const data = await fetchPlayerRankings(tabName, limit);
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case 'team-rank':
      case '球队榜': {
        const data = await fetchTeamRankings();
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case 'knockout':
      case '淘汰赛': {
        const data = await fetchKnockoutBracket();
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case 'categories':
      case 'cats': {
        console.log(JSON.stringify(getPlayerTabNames(), null, 2));
        break;
      }

      case 'help':
      default:
        console.log(`
2026年世界杯排名数据获取工具

用法:
  node worldcup-rankings.js <command> [args]

命令:
  standings / groups        小组赛积分榜（12组）
  fifa / FIFA排名 [N]        FIFA 官方排名（前N名，默认50）
  players / 球员榜 [分类] [N]  球员榜（按数据维度）
  team-rank / 球队榜         球队榜
  knockout / 淘汰赛          淘汰赛对阵图
  categories / cats         列出球员榜可用分类

球员榜分类示例:
  进球 / 助攻 / 射门 / 射正 / 过人 / 关键传球 / 抢断 / 红牌 / 黄牌

示例:
  node worldcup-rankings.js standings
  node worldcup-rankings.js fifa 20
  node worldcup-rankings.js players 进球
  node worldcup-rankings.js players 助攻 30
  node worldcup-rankings.js categories
`);
        process.exit(0);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = {
  fetchGroupStandings,
  fetchFifaRankings,
  fetchPlayerRankings,
  fetchTeamRankings,
  fetchKnockoutBracket,
  parseStageRankings,
  parseFifaRankings,
  getPlayerTabNames,
  PLAYER_TAB_IDS
};

if (require.main === module) {
  main();
}