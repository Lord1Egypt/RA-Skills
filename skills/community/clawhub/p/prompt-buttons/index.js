/**
 * prompt-buttons skill
 * Utility functions for building consistent short button menus.
 * Used by other skills/agents to send tappable prompts.
 */

const sendWithButtons = require('./lib/sendWithButtons');

/**
 * Build a buttons payload for the message tool.
 * @param {string} title - Short message body shown above buttons.
 * @param {Array<{text: string, callback_data: string}>} buttons - Button definitions.
 * @returns {{ message: string, buttons: Array }} Ready for `message(action=send)`.
 */
function buildPrompt(title, buttons) {
  return {
    message: title,
    buttons: [buttons]
  };
}

/**
 * Build a Yes/No prompt.
 * @param {string} yesDesc - One-line description for Yes.
 * @param {string} noDesc - One-line description for No.
 * @param {string} [yesCallback='yes'] - callback_data for Yes button.
 * @param {string} [noCallback='no'] - callback_data for No button.
 */
function yesNo(yesDesc, noDesc, yesCallback = 'yes', noCallback = 'no') {
  return buildPrompt(
    `Yes — ${yesDesc}\nNo — ${noDesc}`,
    [
      { text: 'Yes', callback_data: yesCallback },
      { text: 'No', callback_data: noCallback }
    ]
  );
}

/**
 * Build a numbered menu prompt (1–N).
 * @param {Array<{label: string, desc: string}>} options - Menu items.
 * @param {string} [prefix='opt'] - Prefix for callback_data (e.g. 'opt' → 'opt_1').
 */
function numberedMenu(options, prefix = 'opt') {
  const lines = options.map((o, i) => `${i + 1} — ${o.desc}`).join('\n');
  const buttons = options.map((o, i) => ({
    text: String(i + 1),
    callback_data: `${prefix}_${i + 1}`
  }));
  return buildPrompt(lines, buttons);
}

// Convenience: send a prompt using the validated sendWithButtons helper.
// messageTool should be the OpenClaw message tool object.
function sendPrompt(messageTool, promptPayload) {
  // promptPayload: { message, buttons }
  return sendWithButtons(messageTool, { channel: 'telegram', message: promptPayload.message, buttons: promptPayload.buttons });
}

module.exports = { buildPrompt, yesNo, numberedMenu, sendPrompt };
