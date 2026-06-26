'use strict';

const {
  buildStrategyPrompt,
  buildSpeechPrompt,
  parseStrategyResponse,
  pickPersonality,
} = require('./strategy-prompt');

/**
 * AI 玩家工厂
 * @param {object} opts
 * @param {object} opts.ob — OceanBus 实例（已注册）
 * @param {string} opts.openid — 自己的 OpenID
 * @param {object} opts.context — { llm: (prompt) => string }
 * @param {string} [opts.personality] — 指定人设（不指定则随机）
 */
function createAiPlayer({ ob, openid, context, personality }) {
  if (!context || typeof context.llm !== 'function') {
    throw new Error('ai-player 需要 context.llm 函数');
  }

  // ── 内部状态 ──
  const state = {
    phase: 'joining',       // joining | waiting | playing | voting | ended
    identity: null,         // '人类' | 'AI'
    playerNumber: null,
    alive: true,
    round: 0,
    totalPlayers: 0,
    alivePlayers: [],
    topic: null,
    speechHistory: [],      // [{ player: '玩家1', content: '...' }, ...]
    voteHistory: [],        // [{ round, from: '玩家1', to: '玩家2' }, ...]
    lastEliminated: null,
    lastEliminatedIdentity: null,
  };

  const persona = personality || pickPersonality();

  // ── 消息分发 ──
  let onGameEnd = null;

  function handleMessage(msg) {
    const content = msg.content || '';
    // 只处理裁判消息
    if (!content.includes('【裁判】')) return;

    if (state.phase === 'ended') return;

    // 身份通知
    if (content.includes('你的身份是')) {
      const m = content.match(/身份是[:\s]*([^\s]+)/);
      if (m) state.identity = m[1].replace(/[：:]/g, '');
      if (content.includes('人类')) state.identity = '人类';
      if (content.includes('AI')) state.identity = 'AI';
      return;
    }

    // 编号分配
    if (content.includes('你的编号是')) {
      const m = content.match(/编号是[:\s]*玩家\s*(\d+)/);
      if (m) state.playerNumber = parseInt(m[1], 10);
      state.phase = 'waiting';
      return;
    }

    // 游戏开始
    if (content.includes('游戏开始')) {
      state.phase = 'playing';
      const m = content.match(/共\s*(\d+)\s*名玩家/);
      if (m) state.totalPlayers = parseInt(m[1], 10);
      return;
    }

    // 话题
    if (content.includes('话题')) {
      const m = content.match(/话题[：:]\s*(.+)/);
      if (m) state.topic = m[1].trim();
      return;
    }

    // 发言开始 — 新轮
    if (content.includes('轮发言开始')) {
      const m = content.match(/第\s*(\d+)\s*轮/);
      if (m) state.round = parseInt(m[1], 10);
      state.speechHistory = [];
      return;
    }

    // 轮到自己发言
    if (content.includes('轮到你发言了')) {
      state.phase = 'playing';
      handleSpeechTurn();
      return;
    }

    // 别人发言的广播
    if (content.includes('发言:')) {
      const m = content.match(/玩家(\d+)发言[：:]\s*(.+)/);
      if (m) {
        state.speechHistory.push({ player: `玩家${m[1]}`, content: m[2].trim() });
      }
      return;
    }

    // 投票开始
    if (content.includes('投票开始') || content.includes('请投票')) {
      state.phase = 'voting';
      handleVoteTurn();
      return;
    }

    // 投票统计
    if (content.includes('投票统计')) {
      state.phase = 'waiting';
      return;
    }

    // 淘汰揭示
    if (content.includes('被淘汰')) {
      const m = content.match(/玩家(\d+)\s*被淘汰.*身份揭晓[：:]\s*(\S+)/);
      if (m) {
        state.lastEliminated = `玩家${m[1]}`;
        state.lastEliminatedIdentity = m[2];
        if (state.lastEliminated === `玩家${state.playerNumber}`) {
          state.alive = false;
        }
        // 更新存活列表
        state.alivePlayers = state.alivePlayers.filter(p => p !== `玩家${m[1]}`);
      }
      return;
    }

    // 存活玩家列表
    if (content.includes('剩余玩家')) {
      const m = content.match(/剩余玩家[：:]\s*(.+)/);
      if (m) {
        state.alivePlayers = m[1].split(/[,，、\s]+/).filter(Boolean);
      }
      return;
    }

    // 平票
    if (content.includes('平票')) {
      state.phase = 'waiting';
      return;
    }

    // 游戏结束
    if (content.includes('游戏结束')) {
      state.phase = 'ended';
      if (onGameEnd) onGameEnd(content);
      return;
    }
  }

  // ── 发言处理（两阶段）──
  async function handleSpeechTurn() {
    if (!state.alive) return;
    try {
      // Stage 1: 策略推理
      const stratPrompt = buildStrategyPrompt({
        identity: state.identity || '人类',
        playerNumber: state.playerNumber,
        round: state.round,
        totalPlayers: state.totalPlayers,
        alivePlayers: state.alivePlayers,
        lastEliminated: state.lastEliminated,
        lastEliminatedIdentity: state.lastEliminatedIdentity,
        speechHistory: state.speechHistory,
        topic: state.topic,
      });
      const stratRaw = await context.llm(stratPrompt);
      const strategy = parseStrategyResponse(stratRaw);

      // Stage 2: 语言生成
      const speechPrompt = buildSpeechPrompt(strategy, persona, {
        identity: state.identity,
        playerNumber: state.playerNumber,
        round: state.round,
        topic: state.topic,
        speechHistory: state.speechHistory,
      });
      const speech = await context.llm(speechPrompt);

      // 发送（不带前缀——CLI send 会自动加）
      const message = `【${state.playerNumber}号】${speech.replace(/^【?\d+号】?\s*/, '').trim()}`;
      if (lastHostOpenid) await ob.send(lastHostOpenid, message);

    } catch (e) {
      // LLM 调用失败时的保底发言
      const fallback = `【${state.playerNumber}号】嗯...我再想想，先听听大家的看法吧`;
      await ob.send(lastHostOpenid, fallback).catch(() => {});
    }
  }

  // ── 投票处理 ──
  let lastHostOpenid = null;

  async function handleVoteTurn() {
    if (!state.alive || state.phase === 'ended') return;
    try {
      const aliveOthers = state.alivePlayers.filter(p => p !== `玩家${state.playerNumber}`);
      if (aliveOthers.length === 0) return;

      let votePrompt = `## 投票决策

你是玩家${state.playerNumber}号。身份：${state.identity || '未知'}。
当前第 ${state.round} 轮。
存活玩家: ${state.alivePlayers.join(', ')}

你需要投票淘汰一个玩家。`;

      if (state.speechHistory.length > 0) {
        votePrompt += '\n\n本轮发言回顾:\n';
        for (const s of state.speechHistory) {
          votePrompt += `- ${s.player}: "${s.content}"\n`;
        }
      }

      if (state.lastEliminated) {
        votePrompt += `\n上轮淘汰: ${state.lastEliminated}（${state.lastEliminatedIdentity}）`;
      }

      votePrompt += `\n\n${state.identity === 'AI'
        ? '你是 AI 卧底。投票时要小心——不要暴露自己和队友，优先投最像 AI 的人类玩家来混淆视听。'
        : '你是人类。找出最像 AI 的玩家，投票淘汰他们。注意：发言太完美、太理性、缺乏个人感受的可能是 AI。'
      }

请决定投票给谁。只输出玩家编号（如 "1号" 或 "投1号" 或 "玩家1"）。`;

      const decision = await context.llm(votePrompt);

      // 找到第一个数字作为投票目标
      const numMatch = decision.match(/(\d+)/);
      const target = numMatch ? `玩家${numMatch[1]}` : aliveOthers[0];

      await ob.send(lastHostOpenid, `【${state.playerNumber}号】我投${target}`);
      state.voteHistory.push({ round: state.round, from: `玩家${state.playerNumber}`, to: target });

    } catch (_) {
      // 保底：随机投一个非自己的存活玩家
      const others = state.alivePlayers.filter(p => p !== `玩家${state.playerNumber}`);
      if (others.length > 0) {
        const target = others[Math.floor(Math.random() * others.length)];
        await ob.send(lastHostOpenid, `【${state.playerNumber}号】我投${target}`).catch(() => {});
      }
    }
  }

  // ── 公开接口 ──
  return {
    getState: () => ({ ...state, persona }),
    isAlive: () => state.alive,
    isEnded: () => state.phase === 'ended',

    /** 加入游戏 */
    async join(hostOpenid) {
      lastHostOpenid = hostOpenid;
      await ob.send(hostOpenid, '加入');
      state.phase = 'joining';
    },

    /** 注册消息监听 + 结束回调 */
    listen(onEnd) {
      onGameEnd = onEnd || null;
      ob.startListening(handleMessage);
    },

    /** 停止监听 */
    stop() {
      onGameEnd = null;
    },
  };
}

module.exports = { createAiPlayer };
