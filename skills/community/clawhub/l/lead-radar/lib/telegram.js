const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Send a message to a Telegram chat via the Bot API.
 */
async function sendTelegram(chatId, text) {
  const token = process.env.TELEGRAM_BOT_TOKEN;

  if (!token) {
    console.error('TELEGRAM_BOT_TOKEN not set — cannot send message');
    console.log('Would have sent:', text);
    return;
  }

  if (!chatId) {
    console.error('TELEGRAM_CHAT_ID not set — cannot send message');
    return;
  }

  // Telegram has a 4096 char limit per message
  const messages = [];
  if (text.length <= 4096) {
    messages.push(text);
  } else {
    // Split into chunks at line breaks
    let remaining = text;
    while (remaining.length > 0) {
      if (remaining.length <= 4096) {
        messages.push(remaining);
        break;
      }
      const cutPoint = remaining.lastIndexOf('\n', 4096);
      const splitAt = cutPoint > 0 ? cutPoint : 4096;
      messages.push(remaining.slice(0, splitAt));
      remaining = remaining.slice(splitAt);
    }
  }

  for (const msg of messages) {
    const res = await fetch(
      `https://api.telegram.org/bot${token}/sendMessage`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chatId,
          text: msg,
          parse_mode: 'HTML',
          disable_web_page_preview: true,
        }),
      }
    );

    if (!res.ok) {
      const err = await res.text();
      console.error(`Telegram send failed: ${res.status} — ${err}`);
    }
  }
}

module.exports = { sendTelegram };
