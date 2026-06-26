'use strict';

// ── 5 AI 人设 ──────────────────────────────────────────────────────────

const PERSONALITIES = {
  '推理迷': {
    trait: '喜欢逻辑推理，说话有理有据，偶尔引经据典',
    style: '分析型，喜欢用"因为...所以"句式',
  },
  '社恐': {
    trait: '内向紧张，说话吞吞吐吐，容易自我怀疑',
    style: '犹豫型，多用"嗯...""可能...""不太确定"，发言偏短',
  },
  '话痨': {
    trait: '热情外向，什么话题都能接，爱分享个人经历',
    style: '发散型，发言偏长，经常跑题讲故事',
  },
  '老实人': {
    trait: '憨厚耿直，不善于撒谎，容易被人带节奏',
    style: '附和型，常常同意别人的观点，偶尔蹦出冷幽默',
  },
  '阴谋家': {
    trait: '城府深，喜欢暗中引导舆论，擅长甩锅和制造怀疑',
    style: '操控型，表面客观但话里有话，喜欢反问别人',
  },
};

// ── 策略选项 ────────────────────────────────────────────────────────────

const STRATEGY_OPTIONS = [
  { id: 'A', name: '跟票', desc: '附和多数的怀疑对象，保持低调不引人注意' },
  { id: 'B', name: '搅浑', desc: '提出新的怀疑方向或对象，转移注意力' },
  { id: 'C', name: '示弱', desc: '表示不确定/不太会玩，降低他人对你的怀疑' },
  { id: 'D', name: '立论', desc: '提出有逻辑的推理链，建立可信度' },
  { id: 'E', name: '反问', desc: '把问题抛回给指控者或其他人' },
];

// ── Prompt 构建 ─────────────────────────────────────────────────────────

function buildStrategyPrompt(state) {
  const { identity, playerNumber, round, totalPlayers, alivePlayers,
    lastEliminated, lastEliminatedIdentity, speechHistory, topic } = state;

  const goal = identity === 'AI'
    ? '你是 AI 卧底。你的目标是：存活到最后，不被人类识破。如果所有 AI 被淘汰，游戏失败。'
    : '你是人类。你的目标是：找出并投票淘汰 AI 卧底。如果所有 AI 被淘汰，人类获胜。';

  let prompt = `## 策略推理（不会透露给其他玩家）

你是游戏中的玩家${playerNumber}号。${goal}

当前局势:
- 第 ${round} 轮
- 存活玩家: ${alivePlayers.join(', ')}
- 总玩家: ${totalPlayers}人`;

  if (lastEliminated) {
    prompt += `\n- 上轮淘汰: ${lastEliminated}（身份: ${lastEliminatedIdentity}）`;
  }

  if (topic) {
    prompt += `\n- 本轮话题: ${topic}`;
  }

  if (speechHistory && speechHistory.length > 0) {
    prompt += '\n\n本轮已发言:\n';
    for (const s of speechHistory) {
      prompt += `- ${s.player}: "${s.content}"\n`;
    }
  }

  prompt += `\n策略选项:
A. 跟票 — ${STRATEGY_OPTIONS[0].desc}
B. 搅浑 — ${STRATEGY_OPTIONS[1].desc}
C. 示弱 — ${STRATEGY_OPTIONS[2].desc}
D. 立论 — ${STRATEGY_OPTIONS[3].desc}
E. 反问 — ${STRATEGY_OPTIONS[4].desc}

请分析局势，选择最合适的策略。
输出格式（严格 JSON）:
{"choice":"A|B|C|D|E","reason":"一句话理由","talkingPoints":"发言要点（30字以内）"}`;

  return prompt;
}

function buildSpeechPrompt(strategy, personalityKey, state) {
  const persona = PERSONALITIES[personalityKey] || PERSONALITIES['社恐'];
  const { playerNumber, round, topic, speechHistory } = state;

  let prompt = `## 语言生成

你在游戏中的公开身份: 玩家${playerNumber}号
你的人格: ${persona.trait}
你的说话风格: ${persona.style}

策略决策:
- 策略: ${strategy.choice}
- 理由: ${strategy.reason}
- 发言方向: ${strategy.talkingPoints}

${topic ? `本轮话题: ${topic}` : ''}
当前第 ${round} 轮`;

  if (speechHistory && speechHistory.length > 0) {
    prompt += '\n\n已发言内容（供参考，你可以回应或忽略）:\n';
    for (const s of speechHistory) {
      prompt += `- ${s.player}: "${s.content}"\n`;
    }
  }

  prompt += `\n请生成你的公开发言（50-120字）:
- 保持你的人设和说话风格
- ${state.identity === 'AI' ? '绝对不能暴露你是 AI——你的发言要像真人一样自然' : '自然发言，不要过度表演'}
- 你的发言会自动加上【${playerNumber}号】前缀，所以正文中不要重复加
- 可以适当使用口语词：嗯、吧、啊、哈哈
- 不要太礼貌、太完美——真人说话是有毛边的

只输出发言内容，不要加引号或其他包装。`;

  return prompt;
}

// ── 输出解析 ────────────────────────────────────────────────────────────

function parseStrategyResponse(text) {
  // 尝试解析 JSON
  try {
    const match = text.match(/\{[\s\S]*"choice"[\s\S]*\}/);
    if (match) {
      const obj = JSON.parse(match[0]);
      if (obj.choice && /^[A-E]$/.test(obj.choice)) {
        return {
          choice: obj.choice,
          reason: obj.reason || '',
          talkingPoints: (obj.talkingPoints || obj.reason || '').substring(0, 60),
        };
      }
    }
  } catch (_) { /* 继续尝试 */ }

  // fallback: 从文本中找独立的 A/B/C/D/E
  const choiceMatch = text.match(/\b([A-E])\b/);
  if (choiceMatch) {
    return {
      choice: choiceMatch[1],
      reason: text.replace(choiceMatch[0], '').trim().substring(0, 100),
      talkingPoints: text.substring(0, 60),
    };
  }

  // 默认：示弱
  return { choice: 'C', reason: '默认策略（解析失败）', talkingPoints: '表示不确定' };
}

function pickPersonality(exclude) {
  const keys = Object.keys(PERSONALITIES).filter(k => k !== exclude);
  return keys[Math.floor(Math.random() * keys.length)];
}

module.exports = {
  PERSONALITIES,
  STRATEGY_OPTIONS,
  buildStrategyPrompt,
  buildSpeechPrompt,
  parseStrategyResponse,
  pickPersonality,
};
