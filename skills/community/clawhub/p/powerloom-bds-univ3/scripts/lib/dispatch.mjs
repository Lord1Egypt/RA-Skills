import {
  telegramBotToken,
  telegramChatId,
  discordWebhookUrl,
} from "./powerloom-env.mjs";

/**
 * Dispatch alert lines to Telegram, Discord webhook, or stdout.
 */

export async function dispatchLines(lines, channel) {
  const text = lines.filter(Boolean).join("\n");
  if (!text) return;

  if (channel === "telegram") {
    const token = telegramBotToken();
    const chat = telegramChatId();
    if (!token || !chat) {
      console.log(text);
      return;
    }
    const u = `https://api.telegram.org/bot${token}/sendMessage`;
    const r = await fetch(u, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chat, text, disable_web_page_preview: true }),
    });
    if (!r.ok) {
      const errText = await r.text();
      console.error("Telegram dispatch failed:", r.status, errText.slice(0, 400));
      console.log(text);
    }
    return;
  }

  if (channel === "discord") {
    const url = discordWebhookUrl();
    if (!url) {
      console.log(text);
      return;
    }
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: text.slice(0, 1900) }),
    });
    if (!r.ok) {
      console.error("Discord dispatch failed:", r.status, await r.text());
      console.log(text);
    }
    return;
  }

  console.log(text);
}
