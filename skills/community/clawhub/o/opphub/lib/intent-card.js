//
//   "原始内容归原始内容, 你得 写一个 飞书 card 的渲染层 当然未来也有其他通道需要特定的渲染"
//   "只到 skill 开放完, 没开发完, 不会会话"
// = skill 层发 IntentMessage (channel-agnostic), 不拼飞书 card JSON
// = OpenClaw runtime 8 renderer (FeishuCard / WeixinText / SlackBlock /
//   DiscordEmbed / TelegramInline / CliInquirer / WebForm / FallbackText)
//   负责转译 IntentMessage 到 channel 原生渲染
//
// 本文件提供:
//   1. IntentMessage schema (从 v3.1-architecture.md §13)
//   2. buildInteractive / buildFreeText / buildSend 三个 helper
//   3. output(intent) 输出到 stdout (bot 解析 JSON)
//   4. fallbackToCli (无 runtime 时走 inquirer)

// === IntentMessage schema (channel-agnostic) ===

/**
 * @typedef {Object} IntentOption
 * @property {string} id        - 选中时回传 (feishu:pm)
 * @property {string} label     - 显示 ("feishu:pm ⭐")
 * @property {string} [hint]    - 副文案 ("pm bot")
 * @property {boolean} [isDefault]
 *
 * @typedef {Object} IntentAction
 * @property {string} id          - 唯一 action id
 * @property {string} label       - 按钮文字 ("确认" / "🚀 一键装 plugin")
 * @property {'primary'|'default'|'danger'} [style]
 * @property {Object} [payload]   - action 回调带的元数据
 *
 * @typedef {Object} IntentLink
 * @property {string} text
 * @property {string} url
 *
 * @typedef {Object} IntentMessage
 * @property {string} [prompt]
 * @property {string} [markdown]
 * @property {IntentOption[]} [options]
 * @property {IntentAction[]} [actions]
 * @property {string} [inputHint]
 * @property {IntentLink[]} [links]
 * @property {{title: string, color?: 'blue'|'orange'|'red'|'green'}} [header]
 * @property {Object} [metadata]
 */

/**
 * 拼一个 askInteractive IntentMessage (pickOne + actions)
 * @param {Object} params
 * @param {string} params.header
 * @param {string} params.prompt
 * @param {IntentOption[]} [params.options]
 * @param {IntentAction[]} [params.actions]
 * @param {string} [params.markdown]
 * @returns {IntentMessage}
 */
function buildInteractive({ header, prompt, options = [], actions = [], markdown }) {
  return {
    header: typeof header === 'string'
      ? { title: header, color: 'blue' }
      : header,
    prompt,
    markdown,
    options,
    actions,
  };
}

/**
 * 拼一个 askFreeText IntentMessage (自由文本输入 + actions)
 */
function buildFreeText({ header, prompt, inputHint, actions = [], markdown }) {
  return {
    header: typeof header === 'string'
      ? { title: header, color: 'blue' }
      : header,
    prompt,
    markdown,
    inputHint,
    actions,
  };
}

/**
 * 拼一个 send IntentMessage (单向通知, 无操作)
 */
function buildSend({ header, prompt, markdown, actions = [], links = [] }) {
  return {
    header: typeof header === 'string'
      ? { title: header, color: 'green' }
      : header,
    prompt,
    markdown,
    actions,
    links,
  };
}

/**
 * 把 IntentMessage 输出到 stdout, bot 解析 JSON
 * @param {IntentMessage} intent
 */
function output(intent) {
  // bot 期望 {"ok": true, "intent": {...}, "next_steps": {...}}
  console.log(JSON.stringify({ ok: true, intent }, null, 2));
}

/**
 * 错误输出
 */
function errorOut(code, message, extra = {}) {
  console.log(JSON.stringify({ ok: false, error: code, message, ...extra }, null, 2));
  process.exit(1);
}

// === Fallback: 无 OpenClaw runtime 时走 CLI inquirer ===
// (用于本地调试 / SSH / 没有 bot.skillApi 上下文时)
//
//   - fallback 跟 plugin CLI 的 inquirer 姿势对齐 (Skill ↔ Plugin 同姿势)
//   - 但运行时这是 fallback, 主路径是 bot.skillApi

async function isBotSkillApiAvailable() {
  // 检测是否在 OpenClaw bot 上下文 (有 skillApi)
  return typeof process.env.OPENCLAW_BOT_CONTEXT !== 'undefined';
}

async function fallbackToCli(intent) {
  // 简化版: 用 readline 实现 (跟 plugin CLI 姿势同)
  // 不强依赖 inquirer (避免 requires.bins 引入 inquirer)
  const readline = await import('node:readline');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  // 打印 header + prompt
  if (intent.header?.title) {
    console.error(`\n=== ${intent.header.title} ===`);
  }
  if (intent.prompt) console.error(intent.prompt);
  if (intent.markdown) console.error(intent.markdown);

  // pickOne
  if (intent.options?.length) {
    console.error('\n选项:');
    intent.options.forEach((opt, i) => {
      const star = opt.isDefault ? ' ⭐' : '';
      const hint = opt.hint ? ` (${opt.hint})` : '';
      console.error(`  [${i + 1}] ${opt.label}${star}${hint}`);
    });
    const ans = await new Promise(res => rl.question('\n选 (回车=默认): ', res));
    rl.close();
    const idx = ans.trim() === '' ? intent.options.findIndex(o => o.isDefault) : parseInt(ans, 10) - 1;
    const picked = intent.options[idx] || intent.options[0];
    return { ok: true, picked: picked.id, fallback: 'cli' };
  }

  // freeText
  if (intent.inputHint) {
    console.error(`\n提示: ${intent.inputHint}`);
    const text = await new Promise(res => rl.question('> ', res));
    rl.close();
    return { ok: true, text: text.trim(), fallback: 'cli' };
  }

  // actions
  if (intent.actions?.length) {
    console.error('\n操作:');
    intent.actions.forEach((a, i) => {
      console.error(`  [${i + 1}] ${a.label}`);
    });
    const ans = await new Promise(res => rl.question('\n选: ', res));
    rl.close();
    const idx = parseInt(ans, 10) - 1;
    const picked = intent.actions[idx] || intent.actions[0];
    return { ok: true, action: picked.id, fallback: 'cli' };
  }

  rl.close();
  return { ok: true, fallback: 'cli' };
}

// === 主导出: processIntent ===
// bot 上下文: output(intent), bot 调 runtime skillApi 渲染
// CLI 上下文: fallbackToCli(intent), readline 选
async function processIntent(intent) {
  if (await isBotSkillApiAvailable()) {
    output(intent);
  } else {
    const result = await fallbackToCli(intent);
    console.log(JSON.stringify(result, null, 2));
  }
}

export {
  buildInteractive,
  buildFreeText,
  buildSend,
  output,
  errorOut,
  processIntent,
  isBotSkillApiAvailable,
  fallbackToCli,
};

// CommonJS 兼容 (skill 现有 bin 用 require())
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    buildInteractive,
    buildFreeText,
    buildSend,
    output,
    errorOut,
    processIntent,
    isBotSkillApiAvailable,
    fallbackToCli,
  };
}
