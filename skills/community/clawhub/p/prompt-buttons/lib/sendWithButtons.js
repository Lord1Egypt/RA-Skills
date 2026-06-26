// sendWithButtons helper for prompt-buttons skill
// Validates compact buttons, ensures message body present, sends buttons and a short confirmation.
module.exports = function sendWithButtons(messageTool, params) {
  if (!params || !messageTool) throw new Error('messageTool and params required');
  if (!params.message || params.message.length === 0) {
    throw new Error('message body required');
  }
  const buttons = params.buttons || [];
  if (!Array.isArray(buttons) || buttons.length === 0) {
    throw new Error('buttons array required');
  }
  for (const row of buttons) {
    for (const b of row) {
      if (!b.text || b.text.length > 3) {
        throw new Error('button label too long; use 1-3 chars');
      }
      if (!b.callback_data) {
        throw new Error('callback_data required');
      }
    }
  }

  let attempts = 0;
  while (attempts < 3) {
    attempts += 1;
    try {
      const res = messageTool.send({ action: 'send', channel: params.channel || 'telegram', message: params.message, buttons: params.buttons });
      try {
        messageTool.send({ action: 'send', channel: params.channel || 'telegram', message: '已发送按钮，请点数字选择。' });
      } catch (e) {
        // ignore confirmation failure
      }
      return res;
    } catch (err) {
      if (attempts >= 3) throw new Error('failed to send buttons after retries: ' + err.message);
      // otherwise retry
    }
  }
};
