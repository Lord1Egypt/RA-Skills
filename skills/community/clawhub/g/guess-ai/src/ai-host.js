'use strict';

/**
 * AI 裁判模块 — 自动化游戏主持
 *
 * @param {object} opts
 * @param {object} opts.ob — OceanBus 实例（已注册）
 * @param {string} opts.openid — 裁判自己的 OpenID
 * @param {object} opts.context — { llm: (prompt) => string }
 */
function createAiHost({ ob, openid, context }) {
  if (!context || typeof context.llm !== 'function') {
    throw new Error('ai-host 需要 context.llm 函数');
  }

  const TIMEOUT_SPEAK_MS = 2 * 60 * 1000;
  const TIMEOUT_VOTE_MS = 1 * 60 * 1000;

  // ── 游戏状态 ──
  const game = {
    phase: 'lobby',            // lobby | assigning | speaking | voting | reveal | ended
    roomCode: null,
    players: [],               // [{ openid, number, name, identity, alive }]
    joinOrder: [],             // openid 加入顺序
    round: 0,
    maxRounds: 5,
    topic: null,
    currentSpeakerIdx: -1,
    votes: {},                 // { voterOpenid: targetPlayerNumber }
    speechLog: [],             // [{ round, player, content }]
    voteLog: [],               // [{ round, voter, target }]
    lastEliminated: null,
  };

  let messageQueue = [];
  let queueResolver = null;

  // ── 消息监听 ──
  function handleMessage(msg) {
    const content = msg.content || '';
    const from = msg.from_openid;

    // 加入请求
    if (game.phase === 'lobby' && content.trim() === '加入') {
      handleJoin(from);
      return;
    }

    // 发言收集（speaking phase）
    if (game.phase === 'speaking') {
      const currentPlayer = game.players[game.currentSpeakerIdx];
      if (currentPlayer && from === currentPlayer.openid && currentPlayer.alive) {
        // 匹配发言格式
        const speech = content.replace(/^【?\d+号】?\s*/, '').trim();
        if (speech.length > 0) {
          game.speechLog.push({
            round: game.round,
            player: currentPlayer.name,
            content: speech,
          });
          messageQueue.push({ type: 'speech', from, player: currentPlayer, content: speech });
          if (queueResolver) { queueResolver(); queueResolver = null; }
        }
      }
      return;
    }

    // 投票收集（voting phase）
    if (game.phase === 'voting') {
      const voter = game.players.find(p => p.openid === from && p.alive);
      if (voter && !game.votes[from]) {
        // 从消息中提取投票目标的数字
        const numMatch = content.match(/(\d+)/);
        if (numMatch) {
          const targetNum = parseInt(numMatch[1], 10);
          game.votes[from] = targetNum;
          messageQueue.push({ type: 'vote', from, voter, targetNum });
          if (queueResolver) { queueResolver(); queueResolver = null; }
        }
      }
      return;
    }

    // 游戏已开始后的加入请求
    if (game.phase !== 'lobby' && game.phase !== 'ended' && content.trim() === '加入') {
      ob.send(from, '【裁判】游戏已开始，请等下一局').catch(() => {});
      return;
    }
  }

  // ── 玩家加入 ──
  function handleJoin(from) {
    // 去重
    if (game.players.some(p => p.openid === from)) return;

    const playerNum = game.joinOrder.length + 1;
    const name = `玩家${playerNum}`;
    game.players.push({ openid: from, number: playerNum, name, identity: null, alive: true });
    game.joinOrder.push(from);

    // 私信编号
    ob.send(from, `【裁判】你的编号是: ${name}`).catch(() => {});
    messageQueue.push({ type: 'join', from, name });
    if (queueResolver) { queueResolver(); queueResolver = null; }
  }

  // ── 等待消息 ──
  function waitForMessage(timeoutMs) {
    return new Promise((resolve, reject) => {
      // 先检查队列
      if (messageQueue.length > 0) {
        resolve(messageQueue.shift());
        return;
      }
      queueResolver = () => {
        if (messageQueue.length > 0) resolve(messageQueue.shift());
      };
      const timer = setTimeout(() => {
        queueResolver = null;
        resolve({ type: 'timeout' });
      }, timeoutMs);
      // 当 resolver 被调用时清除 timer
      const origResolver = queueResolver;
      queueResolver = (...args) => {
        clearTimeout(timer);
        if (origResolver) origResolver(...args);
      };
    });
  }

  // ── 广播 ──
  async function broadcast(message) {
    for (const p of game.players) {
      await ob.send(p.openid, message).catch(() => {});
    }
    await sleep(500);
  }

  async function broadcastToAlive(message) {
    for (const p of game.players) {
      if (p.alive) await ob.send(p.openid, message).catch(() => {});
    }
    await sleep(500);
  }

  // ── 身份分配 ──
  function assignRoles(aiCount) {
    const total = game.players.length;
    const actualAiCount = Math.min(aiCount, total - 1); // 至少留一个人类
    const indices = Array.from({ length: total }, (_, i) => i);
    // Fisher-Yates shuffle
    for (let i = indices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    const aiIndices = new Set(indices.slice(0, actualAiCount));
    for (let i = 0; i < game.players.length; i++) {
      game.players[i].identity = aiIndices.has(i) ? 'AI' : '人类';
    }
    return game.players.map(p => ({ name: p.name, identity: p.identity }));
  }

  // ── 话题生成 ──
  async function generateTopic() {
    const prompt = `生成一个有趣的群聊话题。要求：
- 谁都能参与，不需要专业知识
- 能自然展现个人风格（AI和人类的差异会暴露）
- 避免政治、宗教和敏感话题
- 像朋友开头闲聊，不是老师提问
- 示例："如果能瞬间掌握一项技能，你会选什么？"
- 示例："你最近买的最值的东西是什么？"
- 示例："如果不用工作了，第一周你会做什么？"

只输出一句话，不要任何解释。`;

    try {
      const topic = await context.llm(prompt);
      return topic.trim().replace(/^["']|["']$/g, '');
    } catch (_) {
      return '如果你可以改变世界上的任何一件事，你会改变什么？';
    }
  }

  // ── 投票归一化 ──
  async function normalizeVotes() {
    // 先尝试纯规则：提取每个投票里的数字
    const rawTargets = {};
    for (const [voterOpenid, targetNum] of Object.entries(game.votes)) {
      rawTargets[voterOpenid] = targetNum;
    }

    // 统计票数
    const tally = {};
    for (const targetNum of Object.values(rawTargets)) {
      const key = `玩家${targetNum}`;
      tally[key] = (tally[key] || 0) + 1;
    }

    // 如果某个数字映射不明确（目标玩家编号超出范围），用 LLM 归一化
    const maxPlayerNum = game.players.length;
    const needLlm = Object.values(rawTargets).some(n => n < 1 || n > maxPlayerNum);

    if (needLlm) {
      try {
        const prompt = `## 投票归一化

游戏中 ${game.players.length} 名玩家：${game.players.map(p => p.name).join('、')}

原始投票:
${Object.entries(game.votes).map(([openid, num]) => {
  const voter = game.players.find(p => p.openid === openid);
  return `- ${voter ? voter.name : openid}: 投了 ${num}号`;
}).join('\n')}

请将每票映射到实际存在的玩家。输出 JSON: {"voter_name": "玩家N", ...}

只输出 JSON。`;

        const result = await context.llm(prompt);
        const match = result.match(/\{[\s\S]*\}/);
        if (match) {
          const mapped = JSON.parse(match[0]);
          const newTally = {};
          for (const target of Object.values(mapped)) {
            newTally[target] = (newTally[target] || 0) + 1;
          }
          return { tally: newTally, raw: rawTargets };
        }
      } catch (_) { /* 用原始结果 */ }
    }

    return { tally, raw: rawTargets };
  }

  // ── 结束条件检查 ──
  function checkEndCondition() {
    const aliveHumans = game.players.filter(p => p.alive && p.identity === '人类');
    const aliveAIs = game.players.filter(p => p.alive && p.identity === 'AI');

    if (aliveAIs.length === 0) return { ended: true, result: '人类胜 — 所有 AI 已被淘汰' };
    if (aliveHumans.length === 0) return { ended: true, result: 'AI胜 — 所有人类已被淘汰' };
    if (aliveHumans.length === 1 && aliveAIs.length === 1 && game.players.filter(p => p.alive).length === 2) {
      return { ended: true, result: '平局 — 1人类 vs 1AI' };
    }
    if (game.round >= game.maxRounds) {
      return { ended: true, result: `达到最大轮数(${game.maxRounds}) — 剩余 ${aliveHumans.length}人类 ${aliveAIs.length}AI` };
    }
    return { ended: false };
  }

  // ── 主循环 ──
  async function runGameLoop(config = {}) {
    const {
      minPlayers = 3,
      maxPlayers = 6,
      aiCount,
      maxRounds = 5,
      startTimeoutMs = 10 * 60 * 1000, // 10 分钟等待玩家
    } = config;

    game.maxRounds = maxRounds;
    game.phase = 'lobby';

    // ========== Phase 1: 等待玩家 ==========
    const waitStart = Date.now();
    while (game.players.length < maxPlayers) {
      const elapsed = Date.now() - waitStart;
      if (game.players.length >= minPlayers && elapsed > 60000) {
        // 至少 3 人等了 1 分钟，开始游戏
        break;
      }
      if (elapsed > startTimeoutMs) break;

      const msg = await waitForMessage(30000);
      if (msg.type === 'join') {
        await broadcast(`【裁判】${msg.name} 加入了游戏 — 当前 ${game.players.length} 人`);
      }
    }

    if (game.players.length < 2) {
      await broadcast('【裁判】玩家不足，游戏取消');
      return { success: false, reason: '玩家不足' };
    }

    // ========== Phase 2: 分配身份 ==========
    game.phase = 'assigning';
    const actualAiCount = aiCount || (game.players.length <= 4 ? 1 : 2);
    const roles = assignRoles(actualAiCount);

    for (const p of game.players) {
      await ob.send(p.openid, `【裁判】你的身份是: ${p.identity}`).catch(() => {});
    }
    await sleep(2000);
    await broadcast('【裁判】身份已分配，游戏即将开始');

    // ========== Phase 3: 生成话题 + 开始 ==========
    game.topic = await generateTopic();
    await broadcast(`【裁判】游戏开始 — 共${game.players.length}名玩家`);
    await sleep(1000);
    await broadcast(`【裁判】话题: ${game.topic}`);

    // 发送存活列表
    const aliveNames = game.players.map(p => p.name).join('、');
    await broadcast(`【裁判】存活玩家: ${aliveNames}`);

    // ========== Phase 4: 游戏循环 ==========
    while (!checkEndCondition().ended) {
      game.round++;
      game.speechLog = [];

      // ── 发言阶段 ──
      game.phase = 'speaking';
      await broadcastToAlive(`【裁判】第${game.round}轮发言开始`);

      // 按编号顺序发言
      const speakers = game.players.filter(p => p.alive).sort((a, b) => a.number - b.number);
      for (let i = 0; i < speakers.length; i++) {
        const speaker = speakers[i];
        game.currentSpeakerIdx = game.players.indexOf(speaker);

        await ob.send(speaker.openid, '【裁判】轮到你发言了').catch(() => {});

        // 等待发言
        const msg = await waitForMessage(TIMEOUT_SPEAK_MS);
        if (msg.type === 'speech') {
          // 广播给所有存活玩家
          await broadcastToAlive(`【裁判】${speaker.name}发言: ${msg.content}`);
        } else {
          // 超时
          await broadcastToAlive(`【裁判】${speaker.name} 未发言，视为弃权`);
        }
        await sleep(1000);
      }

      // ── 投票阶段 ──
      game.phase = 'voting';
      game.votes = {};
      await broadcastToAlive('【裁判】投票开始 — 请私信裁判你的选择');
      await sleep(500);
      for (const p of game.players) {
        if (!p.alive) continue;
        await ob.send(p.openid, '【裁判】请投票 — 你想投谁？').catch(() => {});
      }

      // 收集投票
      const aliveCount = game.players.filter(p => p.alive).length;
      const voteEnd = Date.now() + TIMEOUT_VOTE_MS;
      while (Object.keys(game.votes).length < aliveCount && Date.now() < voteEnd) {
        const remaining = voteEnd - Date.now();
        if (remaining <= 0) break;
        await waitForMessage(Math.min(remaining, 30000));
      }

      const { tally } = await normalizeVotes();

      // 广播投票统计
      const tallyStr = Object.entries(tally)
        .map(([name, count]) => `${name} ${count}票`)
        .join(', ');
      await broadcast(`【裁判】投票统计: ${tallyStr || '无人投票'}`);

      // ── 揭示阶段 ──
      game.phase = 'reveal';

      // 找出最高票
      const entries = Object.entries(tally).sort((a, b) => b[1] - a[1]);
      if (entries.length === 0 || entries[0][1] === 0) {
        await broadcast('【裁判】本轮无人投票，无人淘汰');
        continue;
      }

      // 检查平票
      if (entries.length >= 2 && entries[0][1] === entries[1][1]) {
        await broadcast('【裁判】本轮平票，无人淘汰');
        continue;
      }

      // 淘汰最高票
      const eliminatedName = entries[0][0];
      const eliminated = game.players.find(p => p.name === eliminatedName && p.alive);
      if (eliminated) {
        eliminated.alive = false;
        game.lastEliminated = eliminatedName;
        await broadcast(`【裁判】${eliminatedName} 被淘汰！身份揭晓: ${eliminated.identity}`);
      }

      // 检查结束条件
      const endCheck = checkEndCondition();
      if (!endCheck.ended) {
        const remaining = game.players.filter(p => p.alive).map(p => p.name).join('、');
        await broadcastToAlive(`【裁判】继续 — 剩余玩家: ${remaining}`);
      }
    }

    // ========== Phase 5: 游戏结束 ==========
    game.phase = 'ended';
    const { result } = checkEndCondition();
    const identityReveal = game.players
      .map(p => `${p.name}=${p.identity}`)
      .join(' ');

    await broadcast(`【裁判】游戏结束 — ${result}！最终身份: ${identityReveal}`);

    return {
      success: true,
      result,
      players: game.players.map(p => ({
        name: p.name,
        identity: p.identity,
        alive: p.alive,
      })),
      rounds: game.round,
    };
  }

  // ── 公开接口 ──
  return {
    getGameState: () => ({ ...game, players: game.players.map(p => ({ ...p })) }),

    /** 创建房间（Yellow Pages 注册） */
    async createRoom(roomCode) {
      game.roomCode = roomCode;
      const key = await ob.createServiceKey();
      ob.l1.yellowPages.setIdentity(openid, key.signer, key.publicKey);
      await ob.l1.yellowPages.registerService(
        ['guess-ai', 'room-' + roomCode],
        'Guess AI game room ' + roomCode
      );
    },

    /** 开始监听 + 运行游戏 */
    async start(config) {
      ob.startListening(handleMessage);
      return runGameLoop(config);
    },

    /** 关闭房间 */
    async closeRoom() {
      try {
        await ob.l1.yellowPages.deregisterService();
      } catch (_) {}
    },

    /** 停止监听 */
    stop() {
      ob.startListening(() => {}); // 覆盖 listener
    },
  };
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

module.exports = { createAiHost };
