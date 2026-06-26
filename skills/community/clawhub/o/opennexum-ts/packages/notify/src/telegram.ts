const TELEGRAM_API_BASE = "https://api.telegram.org";

export async function sendMessage(
  chatId: string,
  text: string,
  botToken: string
): Promise<void> {
  try {
    const url = `${TELEGRAM_API_BASE}/bot${botToken}/sendMessage`;
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: "HTML" }),
    });
    if (!response.ok) {
      const body = await response.text();
      console.error(`[notify] Telegram sendMessage failed: ${response.status} ${body}`);
    }
  } catch (err) {
    console.error("[notify] Telegram sendMessage error:", err);
  }
}

export function getChatId(): string | undefined {
  return process.env["TELEGRAM_CHAT_ID"];
}

export function getBotToken(): string | undefined {
  return process.env["TELEGRAM_BOT_TOKEN"];
}
