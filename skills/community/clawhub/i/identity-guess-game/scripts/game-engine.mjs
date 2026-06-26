#!/usr/bin/env node

/**
 * game-engine.mjs
 * 身份猜猜猜 - 游戏引擎脚本
 *
 * 功能：管理游戏状态、身份分配、线索记录、猜测、得分计算、积分排行榜持久化
 * 数据存储在 scripts/data/ 目录下（JSON 文件）
 *
 * 命令：
 *   create   - 创建新游戏
 *   status   - 查看游戏状态
 *   clue     - 提交线索
 *   guess    - 提交猜测
 *   settle   - 结算游戏
 *   ranking  - 查看排行榜
 *   help     - 显示帮助
 *
 * 使用方式：
 *   node game-engine.mjs <command> [options]
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================================================
// 数据目录
// ============================================================================

const DATA_DIR = path.join(__dirname, 'data');
const GAMES_DIR = path.join(DATA_DIR, 'games');
const RANKINGS_DIR = path.join(DATA_DIR, 'rankings');

function ensureDirs() {
  for (const dir of [DATA_DIR, GAMES_DIR, RANKINGS_DIR]) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

// ============================================================================
// 身份库
// ============================================================================

const IDENTITY_POOL = [
  // 职业类
  '宇航员', '考古学家', '消防员', '魔术师', '潜水员',
  '指挥家', '气象学家', '雕塑家', '驯兽师', '灯塔守护者',
  // 动物类
  '火烈鸟', '变色龙', '猫头鹰', '海豚', '企鹅',
  '蜂鸟', '树懒', '章鱼', '孔雀', '北极熊',
  // 虚构/特殊类
  '时间旅行者', '海盗船长', '炼金术士', '星际探险家', '深海探险家',
  '云朵牧羊人', '彩虹画师', '风的信使', '月光收集者', '梦境建筑师',
];

// ============================================================================
// 工具函数
// ============================================================================

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function loadJSON(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch {
    return null;
  }
}

function saveJSON(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
}

function gamePath(groupId) {
  return path.join(GAMES_DIR, `${groupId}.json`);
}

function rankingPath(groupId) {
  return path.join(RANKINGS_DIR, `${groupId}.json`);
}

function output(data) {
  console.log(JSON.stringify(data, null, 2));
}

function fail(message) {
  output({ success: false, error: message });
  process.exit(1);
}

// ============================================================================
// 参数解析
// ============================================================================

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { command: null, options: {} };

  if (args.length === 0) {
    result.command = 'help';
    return result;
  }

  // 第一个非 -- 参数是命令
  let i = 0;
  if (!args[0].startsWith('--')) {
    result.command = args[0];
    i = 1;
  }

  // 解析后续 key-value 参数
  for (; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const val = args[i + 1];
      if (val && !val.startsWith('--')) {
        result.options[key] = val;
        i++;
      } else {
        result.options[key] = true;
      }
    }
  }

  return result;
}

// ============================================================================
// 命令: create — 创建新游戏
// ============================================================================

function cmdCreate(options) {
  const { group, players } = options;
  if (!group) fail('缺少 --group 参数');
  if (!players) fail('缺少 --players 参数（JSON 数组: [{id, name}, ...]）');

  let playerList;
  try {
    playerList = JSON.parse(players);
  } catch {
    fail('--players 参数不是有效的 JSON');
  }

  if (!Array.isArray(playerList) || playerList.length < 2) {
    fail('至少需要 2 名玩家');
  }

  // 检查是否已有进行中的游戏
  const existingGame = loadJSON(gamePath(group));
  if (existingGame && existingGame.phase !== 'finished') {
    fail(`群 ${group} 已有进行中的游戏，请先结束当前游戏`);
  }

  // 随机分配身份
  const identities = shuffle(IDENTITY_POOL).slice(0, playerList.length);

  const playersMap = {};
  playerList.forEach((p, idx) => {
    playersMap[p.id] = {
      id: p.id,
      name: p.name,
      identity: identities[idx],
      clues: [],         // 每轮提交的线索
      guesses: {},       // 猜测结果 { targetName: guessedIdentity }
      score: 0,
    };
  });

  const game = {
    groupId: group,
    phase: 'clue',           // clue → guessing → finished
    currentRound: 1,
    totalRounds: 3,
    players: playersMap,
    playerOrder: playerList.map(p => p.id),
    roundClues: {},          // { round: { playerId: clueText } }
    createdAt: new Date().toISOString(),
  };

  ensureDirs();
  saveJSON(gamePath(group), game);

  // Return player list WITHOUT identity — identity must be fetched one-by-one via get_identity
  const playerListOut = playerList.map(p => ({
    id: p.id,
    name: p.name,
  }));

  output({
    success: true,
    message: '游戏创建成功！身份已分配。请使用 get_identity 命令逐一获取每位玩家的身份并通过私聊(DM)发送，严禁在群聊中展示身份信息。',
    gameId: group,
    phase: 'clue',
    currentRound: 1,
    totalRounds: 3,
    playerCount: playerList.length,
    players: playerListOut,
  });
}

// ============================================================================
// 命令: get_identity — 获取单个玩家的身份（用于私聊发送）
// ============================================================================

function cmdGetIdentity(options) {
  const { group, player } = options;
  if (!group) fail('缺少 --group 参数');
  if (!player) fail('缺少 --player 参数');

  const game = loadJSON(gamePath(group));
  if (!game) fail(`群 ${group} 没有进行中的游戏`);

  const p = game.players[player];
  if (!p) fail(`玩家 ${player} 不在游戏中`);

  output({
    success: true,
    id: p.id,
    name: p.name,
    identity: p.identity,
    instruction: `请通过私聊(DM)将身份 "${p.identity}" 发送给 ${p.name}(${p.id})，严禁在群聊中展示此信息。`,
  });
}

// ============================================================================
// 命令: status — 查看游戏状态
// ============================================================================

function cmdStatus(options) {
  const { group } = options;
  if (!group) fail('缺少 --group 参数');

  const game = loadJSON(gamePath(group));
  if (!game) fail(`群 ${group} 没有进行中的游戏`);

  const playerSummary = game.playerOrder.map(pid => {
    const p = game.players[pid];
    return {
      id: p.id,
      name: p.name,
      cluesSubmitted: p.clues.length,
      hasGuessed: Object.keys(p.guesses).length > 0,
    };
  });

  output({
    success: true,
    groupId: game.groupId,
    phase: game.phase,
    currentRound: game.currentRound,
    totalRounds: game.totalRounds,
    players: playerSummary,
  });
}

// ============================================================================
// 命令: clue — 提交线索
// ============================================================================

function cmdClue(options) {
  const { group, player, text } = options;
  if (!group) fail('缺少 --group 参数');
  if (!player) fail('缺少 --player 参数');
  if (!text) fail('缺少 --text 参数');

  const game = loadJSON(gamePath(group));
  if (!game) fail(`群 ${group} 没有进行中的游戏`);
  if (game.phase !== 'clue') fail('当前不是线索阶段');

  const p = game.players[player];
  if (!p) fail(`玩家 ${player} 不在游戏中`);

  const round = game.currentRound;

  // 检查是否已提交本轮线索
  if (!game.roundClues[round]) {
    game.roundClues[round] = {};
  }
  if (game.roundClues[round][player]) {
    fail(`玩家 ${p.name} 已提交第 ${round} 轮线索`);
  }

  // 作弊检测：线索中不能直接包含自己的身份名
  if (text.includes(p.identity)) {
    fail(`线索中不能直接包含你的身份名"${p.identity}"！请用暗示的方式描述。`);
  }

  // 记录线索
  game.roundClues[round][player] = text;
  p.clues.push({ round, text });

  // 检查本轮是否所有人都提交了
  const allSubmitted = game.playerOrder.every(pid => game.roundClues[round][pid]);

  let roundComplete = false;
  let allRoundsComplete = false;
  let nextPhase = game.phase;

  if (allSubmitted) {
    roundComplete = true;
    if (round >= game.totalRounds) {
      // 所有轮次完成，进入猜测阶段
      game.phase = 'guessing';
      nextPhase = 'guessing';
      allRoundsComplete = true;
    } else {
      game.currentRound = round + 1;
    }
  }

  saveJSON(gamePath(group), game);

  // 构建本轮线索汇总
  const roundCluesSummary = Object.entries(game.roundClues[round]).map(([pid, clueText]) => ({
    name: game.players[pid].name,
    clue: clueText,
  }));

  output({
    success: true,
    player: p.name,
    round,
    clue: text,
    roundComplete,
    allRoundsComplete,
    nextPhase,
    currentRoundClues: roundCluesSummary,
    submittedCount: Object.keys(game.roundClues[round]).length,
    totalPlayers: game.playerOrder.length,
  });
}

// ============================================================================
// 命令: guess — 提交猜测
// ============================================================================

function cmdGuess(options) {
  const { group, player, guesses: guessesJson } = options;
  if (!group) fail('缺少 --group 参数');
  if (!player) fail('缺少 --player 参数');
  if (!guessesJson) fail('缺少 --guesses 参数（JSON: {targetName: guessedIdentity, ...}）');

  const game = loadJSON(gamePath(group));
  if (!game) fail(`群 ${group} 没有进行中的游戏`);
  if (game.phase !== 'guessing') fail('当前不是猜测阶段');

  const p = game.players[player];
  if (!p) fail(`玩家 ${player} 不在游戏中`);

  if (Object.keys(p.guesses).length > 0) {
    fail(`玩家 ${p.name} 已提交猜测`);
  }

  let guesses;
  try {
    guesses = JSON.parse(guessesJson);
  } catch {
    fail('--guesses 参数不是有效的 JSON');
  }

  p.guesses = guesses;
  saveJSON(gamePath(group), game);

  // 检查是否所有人都猜完
  const allGuessed = game.playerOrder.every(pid => Object.keys(game.players[pid].guesses).length > 0);

  output({
    success: true,
    player: p.name,
    guessesSubmitted: guesses,
    allGuessed,
    guessedCount: game.playerOrder.filter(pid => Object.keys(game.players[pid].guesses).length > 0).length,
    totalPlayers: game.playerOrder.length,
  });
}

// ============================================================================
// 命令: settle — 结算游戏
// ============================================================================

function cmdSettle(options) {
  const { group } = options;
  if (!group) fail('缺少 --group 参数');

  const game = loadJSON(gamePath(group));
  if (!game) fail(`群 ${group} 没有进行中的游戏`);
  if (game.phase !== 'guessing') fail('游戏还未到猜测阶段，无法结算');

  // 检查是否所有人都已猜测
  const allGuessed = game.playerOrder.every(pid => Object.keys(game.players[pid].guesses).length > 0);
  if (!allGuessed) fail('还有玩家未提交猜测，无法结算');

  // 构建 name → identity 映射
  const nameToIdentity = {};
  const nameToId = {};
  for (const pid of game.playerOrder) {
    const pl = game.players[pid];
    nameToIdentity[pl.name] = pl.identity;
    nameToId[pl.name] = pl.id;
  }

  // 计算得分
  const results = [];
  for (const pid of game.playerOrder) {
    const pl = game.players[pid];
    let correctCount = 0;
    const guessDetails = [];

    for (const [targetName, guessedIdentity] of Object.entries(pl.guesses)) {
      const actualIdentity = nameToIdentity[targetName];
      const isCorrect = actualIdentity && guessedIdentity === actualIdentity;
      if (isCorrect) correctCount++;
      guessDetails.push({
        target: targetName,
        guessed: guessedIdentity,
        actual: actualIdentity || '未知',
        correct: !!isCorrect,
      });
    }

    // 得分：每猜对一个得 10 分
    const guessScore = correctCount * 10;

    // 隐藏分：被猜错的次数越多得分越高（说明伪装好）
    let disguiseScore = 0;
    for (const otherPid of game.playerOrder) {
      if (otherPid === pid) continue;
      const otherGuesses = game.players[otherPid].guesses;
      for (const [tName, gIdentity] of Object.entries(otherGuesses)) {
        if (tName === pl.name && gIdentity !== pl.identity) {
          disguiseScore += 5;
        }
      }
    }

    pl.score = guessScore + disguiseScore;

    results.push({
      id: pl.id,
      name: pl.name,
      identity: pl.identity,
      guessScore,
      disguiseScore,
      totalScore: pl.score,
      guessDetails,
    });
  }

  // 排名
  results.sort((a, b) => b.totalScore - a.totalScore);
  results.forEach((r, idx) => { r.rank = idx + 1; });

  // 更新排行榜
  ensureDirs();
  let ranking = loadJSON(rankingPath(group)) || { groupId: group, players: {}, gamesPlayed: 0 };
  ranking.gamesPlayed++;
  for (const r of results) {
    if (!ranking.players[r.id]) {
      ranking.players[r.id] = { id: r.id, name: r.name, totalScore: 0, gamesPlayed: 0, wins: 0 };
    }
    const rp = ranking.players[r.id];
    rp.name = r.name; // 更新名字
    rp.totalScore += r.totalScore;
    rp.gamesPlayed++;
    if (r.rank === 1) rp.wins++;
  }
  saveJSON(rankingPath(group), ranking);

  // 标记游戏结束
  game.phase = 'finished';
  game.results = results;
  game.finishedAt = new Date().toISOString();
  saveJSON(gamePath(group), game);

  output({
    success: true,
    message: '游戏结算完成！',
    results,
    allClues: game.roundClues,
  });
}

// ============================================================================
// 命令: ranking — 查看排行榜
// ============================================================================

function cmdRanking(options) {
  const { group } = options;
  if (!group) fail('缺少 --group 参数');

  const ranking = loadJSON(rankingPath(group));
  if (!ranking) {
    output({ success: true, message: '暂无排行榜数据', groupId: group, gamesPlayed: 0, leaderboard: [] });
    return;
  }

  const leaderboard = Object.values(ranking.players)
    .sort((a, b) => b.totalScore - a.totalScore)
    .map((p, idx) => ({ rank: idx + 1, ...p }));

  output({
    success: true,
    groupId: ranking.groupId,
    gamesPlayed: ranking.gamesPlayed,
    leaderboard,
  });
}

// ============================================================================
// 命令: help
// ============================================================================

function cmdHelp() {
  console.log(`
身份猜猜猜 - 游戏引擎

命令：
  create        创建新游戏
              --group <groupId>  群组ID
              --players <json>   玩家列表 [{id, name}, ...]

  get_identity  获取单个玩家的秘密身份（用于私聊发送）
              --group <groupId>
              --player <playerId>

  status   查看游戏状态
           --group <groupId>

  clue     提交线索
           --group <groupId>
           --player <playerId>
           --text <clueText>

  guess    提交猜测
           --group <groupId>
           --player <playerId>
           --guesses <json>   猜测 {targetName: guessedIdentity, ...}

  settle   结算游戏
           --group <groupId>

  ranking  查看排行榜
           --group <groupId>

  help     显示此帮助

示例：
  node game-engine.mjs create --group g1 --players '[{"id":"u1","name":"Alice"},{"id":"u2","name":"Bob"}]'
  node game-engine.mjs clue --group g1 --player u1 --text "我喜欢在天上飞"
  node game-engine.mjs guess --group g1 --player u1 --guesses '{"Bob":"宇航员"}'
  node game-engine.mjs settle --group g1
  node game-engine.mjs ranking --group g1
`);
}

// ============================================================================
// 主入口
// ============================================================================

const { command, options: opts } = parseArgs();

const commands = {
  create: cmdCreate,
  get_identity: cmdGetIdentity,
  status: cmdStatus,
  clue: cmdClue,
  guess: cmdGuess,
  settle: cmdSettle,
  ranking: cmdRanking,
  help: cmdHelp,
  '--help': cmdHelp,
};

if (!commands[command]) {
  fail(`未知命令: ${command}。使用 help 查看可用命令。`);
}

commands[command](opts);
