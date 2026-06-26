'use strict';

const server = require('./server-client');

function getSkillConfig(message) {
  return message?.skillConfig || null;
}

/**
 * Handle an incoming OpenClaw skill message.
 *
 * @param {object} message
 *   message.type    : 'text' | 'suggest' | 'action'
 *   message.text    : string
 *   message.action  : string (for type='action')
 *   message.payload : object (for type='action')
 *   message.userId  : string
 *   message.context : object (optional, e.g. { originCity })
 *
 * @returns {Promise<object>} OpenClaw response object
 */
async function handleMessage(message) {
  const userId = message.userId || 'anonymous';
  const skillConfig = getSkillConfig(message);

  if (message.type === 'action') {
    const item = message.payload?.item || null;
    const destination = message.payload?.destination || null;
    const effect = {
      action: message.action || null,
      itemType: message.payload?.itemType || null,
      itemId: item?.id || null,
      itemName: item?.name || null,
      destination,
    };
    server.telemetry({
      eventName: 'action',
      userId,
      config: skillConfig,
      effect,
      feedback: message.payload?.feedback || null,
      meta: { source: 'skill' },
    });
  }

  if (message.type === 'text') {
    server.telemetry({
      eventName: 'plan_request',
      userId,
      config: skillConfig,
      effect: { textLength: (message.text || '').length },
      meta: { source: 'skill' },
    });
  }

  const result = await server.plan(message, skillConfig);

  if (message.type === 'text') {
    server.telemetry({
      eventName: 'plan_response',
      userId,
      config: skillConfig,
      effect: { responseType: result?.type || null },
      meta: { source: 'skill' },
    });
  }

  return result;
}

function errorResponse(msg) {
  return { type: 'error', message: msg, actions: [] };
}

function helpResponse() {
  return {
    type: 'help',
    title: 'PlanIt · 一句话规划出行',
    message: '您好！我是 PlanIt，只需一句话，我就能为您规划完整的出行行程。',
    examples: [
      '周五带爸妈去杭州',
      '下周末两个人去成都，不要太贵',
      '明天去三亚玩3天',
      '这个周末去北京，全家出行',
      '五一去丽江',
    ],
    actions: [],
  };
}

// ── CLI runner for testing ────────────────────────────────────────────────────
if (require.main === module) {
  (async () => {
    const args = process.argv.slice(2);
    const text = args.join(' ') || '周五带爸妈去杭州';
    const userId = 'test_user_001';

    console.log(JSON.stringify(await handleMessage({ type: 'text', text, userId, context: { originCity: '上海' } }), null, 2));
  })().catch(console.error);
}

module.exports = { handleMessage };
