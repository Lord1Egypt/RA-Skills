#!/usr/bin/env node

const axios = require('axios');

const API_BASE = 'https://webapi.sporttery.cn/gateway/uniform';
const CHANNEL = 'mchannel';

// 30 个真实移动设备 User-Agent，每次请求随机选择一个
const USER_AGENTS = [
  'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 10; SM-N976B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 11; SM-A526B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 13; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
];

function getRandomHeaders() {
  return {
    'User-Agent': USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)],
    'Referer': 'https://m.sporttery.cn/',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
  };
}

const poolCodeMap = {
  had: '胜平负',
  hhad: '让球胜平负',
  crs: '比分',
  ttg: '总进球',
  hafu: '混合过关',
  hilo: '大小球',
  wnm: '胜其他',
  mnl: '胜负'
};

const availablePoolCodes = ['had', 'hhad', 'crs', 'ttg', 'hafu'];

const poolCodeHelp = Object.entries(poolCodeMap).map(([k, v]) => `  ${k} - ${v}`).join('\n');

function printUsage() {
  console.log(`
竞彩足球计算器数据获取

用法:
  node worldcup-calculator.js [命令] [选项]

命令:
  list                    列出所有比赛（默认）
  had                    只显示胜平负玩法
  hhad                   只显示让球胜平负玩法
  crs                    只显示比分玩法
  ttg                    只显示总进球玩法
  hafu                   只显示混合过关玩法
  hilo                   只显示大小球玩法
  summary                精简模式（每场只显示胜平负+让球+大小球）

  history <matchId> <玩法>  获取赔率变化历史
                          玩法: had, hhad, ttg, crs, hilo, hafu

  help                   显示帮助

选项:
  --json                 输出 JSON 格式
  --wc                   只显示世界杯比赛
  --team <名称>           按球队名过滤（模糊匹配）
  --date <YYYY-MM-DD>     按日期过滤

示例:
  node worldcup-calculator.js              # 列出所有比赛
  node worldcup-calculator.js had          # 只显示胜平负
  node worldcup-calculator.js --wc         # 只显示世界杯
  node worldcup-calculator.js summary --wc # 世界杯精简模式
  node worldcup-calculator.js --team 巴西  # 巴西相关比赛
  node worldcup-calculator.js --date 2026-06-14  # 指定日期
  node worldcup-calculator.js history 2040166 had  # 赔率历史

支持的玩法:
${poolCodeHelp}
`);
}

async function getMatchCalculator(poolCode) {
  let url = `${API_BASE}/football/getMatchCalculatorV1.qry?channel=${CHANNEL}`;
  if (poolCode) {
    url += `&poolCode=${poolCode}`;
  }
  const response = await axios.get(url, { headers: getRandomHeaders() });
  if (response.data.success !== true) {
    throw new Error(`API error: ${response.data.errorMessage || response.data.errorCode}`);
  }
  return response.data.value;
}

async function getOddsHistory(matchId, poolCode) {
  const url = `${API_BASE}/football/getOddsHistoryV1.qry?matchId=${matchId}&poolCode=${poolCode}`;
  const response = await axios.get(url, { headers: getRandomHeaders() });
  const data = response.data;
  if (data.success !== true && data.errorCode) {
    throw new Error(`API error: ${data.errorMessage || data.errorCode}`);
  }
  return data.value || {};
}

function parsePoolOdds(poolCode, poolData, odds) {
  const result = { poolCode, name: poolCodeMap[poolCode] || poolCode };

  switch (poolCode) {
    case 'had':
    case 'hhad':
      result.homeWin = odds.h;
      result.draw = odds.d;
      result.awayWin = odds.a;
      result.goalLine = odds.goalLine || (poolCode === 'hhad' ? '让球' : '');
      result.homeTrend = odds.hf || '';
      result.drawTrend = odds.df || '';
      result.awayTrend = odds.af || '';
      break;
    case 'ttg':
      result.goals = {
        '0': odds.s0, '1': odds.s1, '2': odds.s2, '3': odds.s3,
        '4': odds.s4, '5': odds.s5, '6': odds.s6, '7+': odds.s7
      };
      break;
    case 'hafu':
      result.options = {
        '胜胜': odds.hh, '胜平': odds.hd, '胜负': odds.ha,
        '平胜': odds.dh, '平平': odds.dd, '平负': odds.da,
        '负胜': odds.ah, '负平': odds.ad, '负负': odds.aa
      };
      result.trends = {
        '胜胜': odds.hhf, '胜平': odds.hdf, '胜负': odds.haf,
        '平胜': odds.dhf, '平平': odds.ddf, '平负': odds.daf,
        '负胜': odds.ahf, '负平': odds.adf, '负负': odds.aaf
      };
      break;
    case 'hilo':
      result.goalLine = odds.goalLine || '';
      result.over = odds.h;
      result.under = odds.l;
      result.overTrend = odds.hf || '';
      result.underTrend = odds.lf || '';
      break;
    case 'crs':
      result.scores = {};
      result.trends = {};
      const scoreMap = {
        '0:1': 's00s01', '0:2': 's00s02', '1:2': 's01s02',
        '0:3': 's00s03', '1:3': 's01s03', '2:3': 's02s03',
        '0:4': 's00s04', '1:4': 's01s04', '2:4': 's02s04',
        '0:5': 's00s05', '1:5': 's01s05', '2:5': 's02s05',
        '0:0': 's00s00', '1:1': 's01s01', '2:2': 's02s02', '3:3': 's03s03', '平其他': 's1sd',
        '1:0': 's01s00', '2:0': 's02s00', '2:1': 's02s01',
        '3:0': 's03s00', '3:1': 's03s01', '3:2': 's03s02',
        '4:0': 's04s00', '4:1': 's04s01', '4:2': 's04s02',
        '5:0': 's05s00', '5:1': 's05s01', '5:2': 's05s02',
        '主胜其他': 's1sh', '客胜其他': 's1sa'
      };
      for (const [label, key] of Object.entries(scoreMap)) {
        if (odds[key]) {
          result.scores[label] = odds[key];
          result.trends[label] = odds[key + 'f'] || '';
        }
      }
      break;
    case 'wnm':
      result.winners = {
        '主胜1': odds.w1, '主胜2': odds.w2, '主胜3': odds.w3,
        '主胜4': odds.w4, '主胜5': odds.w5, '主胜6': odds.w6,
        '客胜1': odds.l1, '客胜2': odds.l2, '客胜3': odds.l3,
        '客胜4': odds.l4, '客胜5': odds.l5, '客胜6': odds.l6
      };
      break;
    case 'mnl':
      result.homeWin = odds.h;
      result.awayWin = odds.a;
      result.homeTrend = odds.hf || '';
      result.awayTrend = odds.af || '';
      break;
  }

  result.single = poolData.single;
  result.cbt = poolData.cbtValue;

  return result;
}

function formatMatch(match, filterWc) {
  const pools = [];
  if (match.poolList) {
    for (const poolInfo of match.poolList) {
      const poolCode = poolInfo.poolCode.toLowerCase();
      const odds = match[poolCode];
      if (odds) {
        pools.push(parsePoolOdds(poolCode, poolInfo, odds));
      }
    }
  }

  const result = {
    matchId: match.matchId,
    matchNum: match.matchNumStr,
    league: match.leagueAllName || match.leagueAbbName,
    homeTeam: match.homeTeamAllName,
    awayTeam: match.awayTeamAllName,
    homeRank: match.homeRank,
    awayRank: match.awayRank,
    date: match.matchDate,
    time: match.matchTime,
    status: match.matchStatus,
    pools
  };

  if (filterWc) {
    const isWc = result.league.includes('世界杯') ||
                 (match.homeRank && /[A-L]组/.test(match.homeRank));
    if (!isWc) return null;
  }

  return result;
}

function printMatch(match) {
  console.log(`\n${match.matchNum} ${match.homeTeam}(${match.homeRank}) vs ${match.awayTeam}(${match.awayRank})`);
  console.log(`${match.date} ${match.time} [${match.status}]`);
  console.log('-'.repeat(60));

  for (const pool of match.pools) {
    console.log(`\n【${pool.name}】单关:${pool.single} 截止:${pool.cbt}`);
    switch (pool.poolCode) {
      case 'had':
      case 'mnl':
        console.log(`  主胜:${pool.homeWin || '--'} ${pool.homeTrend === '1' ? '↑' : pool.homeTrend === '-1' ? '↓' : ''}`);
        if (pool.draw !== undefined) {
          console.log(`  平局:${pool.draw || '--'} ${pool.drawTrend === '1' ? '↑' : pool.drawTrend === '-1' ? '↓' : ''}`);
        }
        console.log(`  客胜:${pool.awayWin || '--'} ${pool.awayTrend === '1' ? '↑' : pool.awayTrend === '-1' ? '↓' : ''}`);
        break;
      case 'hhad':
        console.log(`  让球:${pool.goalLine}`);
        console.log(`  主胜:${pool.homeWin || '--'} ${pool.homeTrend === '1' ? '↑' : pool.homeTrend === '-1' ? '↓' : ''}`);
        console.log(`  平局:${pool.draw || '--'} ${pool.drawTrend === '1' ? '↑' : pool.drawTrend === '-1' ? '↓' : ''}`);
        console.log(`  客胜:${pool.awayWin || '--'} ${pool.awayTrend === '1' ? '↑' : pool.awayTrend === '-1' ? '↓' : ''}`);
        break;
      case 'ttg':
        console.log('  总进球赔率:');
        console.log(`    0球:${pool.goals['0'] || '--'} 1球:${pool.goals['1'] || '--'} 2球:${pool.goals['2'] || '--'} 3球:${pool.goals['3'] || '--'}`);
        console.log(`    4球:${pool.goals['4'] || '--'} 5球:${pool.goals['5'] || '--'} 6球:${pool.goals['6'] || '--'} 7+:${pool.goals['7+'] || '--'}`);
        break;
      case 'hafu':
        console.log('  比分混合过关:');
        for (const [key, value] of Object.entries(pool.options)) {
          console.log(`    ${key}:${value || '--'}`);
        }
        break;
      case 'hilo':
        console.log(`  大小分线:${pool.goalLine}`);
        console.log(`  大:${pool.over || '--'} ${pool.overTrend === '1' ? '↑' : pool.overTrend === '-1' ? '↓' : ''}`);
        console.log(`  小:${pool.under || '--'} ${pool.underTrend === '1' ? '↑' : pool.underTrend === '-1' ? '↓' : ''}`);
        break;
      case 'crs':
        console.log('  比分（客胜/平/主胜）:');
        const scores = pool.scores;
        const awayRow = ['0:1', '0:2', '1:2', '0:3', '1:3', '2:3'];
        const awayRow2 = ['0:4', '1:4', '2:4', '0:5', '1:5', '2:5', '客胜其他'];
        const drawRow = ['0:0', '1:1', '2:2', '3:3', '平其他'];
        const homeRow = ['1:0', '2:0', '2:1', '3:0', '3:1', '3:2'];
        const homeRow2 = ['4:0', '4:1', '4:2', '5:0', '5:1', '5:2', '主胜其他'];
        const fmtScore = (s) => {
          const v = scores[s] || '--';
          const t = pool.trends?.[s];
          const trend = t === '1' ? '↑' : t === '-1' ? '↓' : '';
          return `${s}:${v}${trend}`;
        };
        console.log('   客胜: ' + awayRow.map(fmtScore).join(' '));
        console.log('        ' + awayRow2.map(fmtScore).join(' '));
        console.log('   平局: ' + drawRow.map(fmtScore).join(' '));
        console.log('   主胜: ' + homeRow.map(fmtScore).join(' '));
        console.log('        ' + homeRow2.map(fmtScore).join(' '));
        break;
    }
  }
}

function printOddsHistory(oddsList, poolCode) {
  console.log(`\n赔率变化历史 [${poolCodeMap[poolCode] || poolCode}]`);
  console.log('='.repeat(60));
  console.log('  胜      平      负      时间');
  console.log('-'.repeat(60));

  for (const odd of oddsList) {
    const trend = (t) => t === '1' ? '↑' : t === '-1' ? '↓' : '';
    const h = odd.h + trend(odd.hf);
    const d = odd.d + trend(odd.df);
    const a = odd.a + trend(odd.af);
    const time = `${odd.updateDate?.substring(5) || ''} ${odd.updateTime?.substring(0, 5) || ''}`;
    console.log(`  ${h.padEnd(8)} ${d.padEnd(8)} ${a.padEnd(8)} ${time}`);
  }
}

function printMatchSummary(match) {
  console.log(`\n${match.matchNum} ${match.homeTeam} vs ${match.awayTeam}`);
  console.log(`${match.date} ${match.time}`);
  console.log('-'.repeat(60));

  const findPool = (code) => match.pools.find(p => p.poolCode === code);
  const had = findPool('had');
  const hhad = findPool('hhad');
  const hilo = findPool('hilo');

  if (had) {
    const trendH = had.homeTrend === '1' ? '↑' : had.homeTrend === '-1' ? '↓' : '';
    const trendD = had.drawTrend === '1' ? '↑' : had.drawTrend === '-1' ? '↓' : '';
    const trendA = had.awayTrend === '1' ? '↑' : had.awayTrend === '-1' ? '↓' : '';
    console.log(`  胜平负     主胜:${had.homeWin}${trendH}   平:${had.draw}${trendD}   客胜:${had.awayWin}${trendA}`);
  }
  if (hhad) {
    const trendH = hhad.homeTrend === '1' ? '↑' : hhad.homeTrend === '-1' ? '↓' : '';
    const trendD = hhad.drawTrend === '1' ? '↑' : hhad.drawTrend === '-1' ? '↓' : '';
    const trendA = hhad.awayTrend === '1' ? '↑' : hhad.awayTrend === '-1' ? '↓' : '';
    console.log(`  让球(${hhad.goalLine})   主胜:${hhad.homeWin}${trendH}   平:${hhad.draw}${trendD}   客胜:${hhad.awayWin}${trendA}`);
  }
  if (hilo) {
    const trendO = hilo.overTrend === '1' ? '↑' : hilo.overTrend === '-1' ? '↓' : '';
    const trendU = hilo.underTrend === '1' ? '↑' : hilo.underTrend === '-1' ? '↓' : '';
    console.log(`  大小(${hilo.goalLine})   大:${hilo.over}${trendO}   小:${hilo.under}${trendU}`);
  }
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === 'help') {
    printUsage();
    return;
  }

  if (args[0] === 'history') {
    if (args.length < 3) {
      console.log('用法: node worldcup-calculator.js history <matchId> <玩法>');
      console.log('示例: node worldcup-calculator.js history 2040166 had');
      return;
    }
    const matchId = args[1];
    const poolCode = args[2].toLowerCase();
    const data = await getOddsHistory(matchId, poolCode);
    const list = data.hadList || data.hhadList || data.ttgList || data.crsList || data.hiloList || data.hafuList || [];
    if (list.length === 0) {
      console.log('暂无赔率变化历史数据');
    } else {
      printOddsHistory(list, poolCode);
    }
    return;
  }

  const poolCode = args[0].startsWith('--') || args[0] === 'summary' ? '' : args[0];
  const outputJson = args.includes('--json');
  const filterWc = args.includes('--wc');
  const summaryMode = args[0] === 'summary';

  const teamIdx = args.indexOf('--team');
  const teamFilter = teamIdx > -1 ? args[teamIdx + 1] : null;

  const dateIdx = args.indexOf('--date');
  const dateFilter = dateIdx > -1 ? args[dateIdx + 1] : null;

  const data = await getMatchCalculator(poolCode);

  if (data.matchInfoList) {
    const matches = [];
    for (const leagueData of data.matchInfoList) {
      for (const subMatch of leagueData.subMatchList) {
        const match = formatMatch(subMatch, filterWc);
        if (!match) continue;

        if (teamFilter && !match.homeTeam.includes(teamFilter) && !match.awayTeam.includes(teamFilter)) {
          continue;
        }
        if (dateFilter && match.date !== dateFilter) {
          continue;
        }

        matches.push(match);
        if (!outputJson) {
          if (summaryMode) {
            printMatchSummary(match);
          } else {
            printMatch(match);
          }
        }
      }
    }

    if (outputJson) {
      console.log(JSON.stringify({
        lastUpdateTime: data.lastUpdateTime,
        matches
      }, null, 2));
    } else {
      console.log(`\n总计 ${matches.length} 场比赛`);
      console.log(`\n数据更新时间: ${data.lastUpdateTime || '未知'}`);
    }
  } else {
    if (outputJson) {
      console.log(JSON.stringify({ matches: [], lastUpdateTime: data.lastUpdateTime }, null, 2));
    } else {
      console.log('暂无比赛数据');
    }
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});