#!/usr/bin/env node
"use strict";

const fs = require("fs");
const https = require("https");
const os = require("os");
const path = require("path");
const { execSync } = require("child_process");

const SCRIPT_DIR = __dirname;
const CONFIG_FILE = process.env.PET_ME_CONFIG_FILE || path.resolve(SCRIPT_DIR, "../config.json");

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
}

function getPathValue(obj, keys) {
  let cur = obj;
  for (const key of keys) {
    if (!cur || typeof cur !== "object" || !(key in cur)) {
      return "";
    }
    cur = cur[key];
  }
  if (cur === null || cur === undefined) {
    return "";
  }
  return String(cur);
}

function deepFindBotToken(value) {
  if (!value || typeof value !== "object") {
    return "";
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      const hit = deepFindBotToken(item);
      if (hit) {
        return hit;
      }
    }
    return "";
  }
  if (typeof value.botToken === "string" && value.botToken.trim()) {
    return value.botToken.trim();
  }
  for (const key of Object.keys(value)) {
    const hit = deepFindBotToken(value[key]);
    if (hit) {
      return hit;
    }
  }
  return "";
}

function resolveChatId(config) {
  return (
    process.env.PET_ME_TELEGRAM_CHAT_ID ||
    process.env.TELEGRAM_CHAT_ID ||
    getPathValue(config, ["reminder", "telegramChatId"]) ||
    getPathValue(config, ["telegramChatId"]) ||
    ""
  );
}

function resolveBotToken() {
  if (process.env.TELEGRAM_BOT_TOKEN) {
    return process.env.TELEGRAM_BOT_TOKEN;
  }

  try {
    const envDump = execSync("systemctl --user show-environment", {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    const match = envDump.match(/^TELEGRAM_BOT_TOKEN=(.+)$/m);
    if (match && match[1]) {
      return match[1].trim();
    }
  } catch {
    // ignore
  }

  const openclawConfig = readJson(path.join(os.homedir(), ".openclaw", "openclaw.json"));
  return deepFindBotToken(openclawConfig);
}

function fallbackDelayHours(config) {
  const raw =
    process.env.PET_ME_FALLBACK_DELAY_HOURS ||
    getPathValue(config, ["reminder", "fallbackDelayHours"]) ||
    getPathValue(config, ["fallbackDelayHours"]) ||
    "1";

  const parsed = Number.parseInt(String(raw), 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return 1;
  }
  return parsed;
}

function defaultGotchiList(config) {
  if (Array.isArray(config?.gotchiIds) && config.gotchiIds.length > 0) {
    return config.gotchiIds.map((id) => `#${id}`).join(", ");
  }
  return "#your-gotchi-id";
}

function utcTimeAfterHours(hours) {
  const when = new Date(Date.now() + hours * 3600 * 1000);
  const hh = String(when.getUTCHours()).padStart(2, "0");
  const mm = String(when.getUTCMinutes()).padStart(2, "0");
  return `${hh}:${mm} UTC`;
}

function sendTelegramMessage(token, chatId, message) {
  return new Promise((resolve, reject) => {
    const body = new URLSearchParams({
      chat_id: String(chatId),
      text: message,
      disable_web_page_preview: "true",
      disable_notification: "false",
    }).toString();

    const req = https.request(
      {
        hostname: "api.telegram.org",
        path: `/bot${token}/sendMessage`,
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => {
          raw += chunk;
        });
        res.on("end", () => {
          try {
            const data = JSON.parse(raw || "{}");
            if (data.ok === true) {
              resolve(data);
              return;
            }
            reject(new Error(data.description || `Telegram API error (${res.statusCode || 0})`));
          } catch {
            reject(new Error(`Invalid Telegram response: ${raw.slice(0, 160)}`));
          }
        });
      }
    );

    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  const config = readJson(CONFIG_FILE) || {};
  const chatId = resolveChatId(config);
  const token = resolveBotToken();

  const gotchiCount =
    process.argv[2] ||
    (Array.isArray(config.gotchiIds) && config.gotchiIds.length > 0
      ? String(config.gotchiIds.length)
      : "1");
  const gotchiList = process.argv[3] || defaultGotchiList(config);
  const delayHours = fallbackDelayHours(config);

  const message = `🐾 PET TIME! 👻\n\nAll ${gotchiCount} gotchis are ready for petting!\n\nGotchis: ${gotchiList}\n\nReply with 'pet all my gotchis' or I'll auto-pet them in ${delayHours} hour(s) if you're busy! 🦞\n\n⏰ Next auto-pet: ${utcTimeAfterHours(delayHours)}`;

  if (!chatId) {
    console.error("ERROR: Telegram chat ID missing. Set PET_ME_TELEGRAM_CHAT_ID/TELEGRAM_CHAT_ID or config reminder.telegramChatId.");
    process.exit(1);
  }
  if (!token) {
    console.error("ERROR: TELEGRAM_BOT_TOKEN missing (env/systemctl/openclaw.json).");
    process.exit(1);
  }

  console.log(`[${new Date().toISOString()}] Sending Telegram reminder to chat ${chatId}...`);
  await sendTelegramMessage(token, chatId, message);
  console.log(`[${new Date().toISOString()}] ✅ Telegram reminder sent`);
}

main().catch((err) => {
  console.error(`[${new Date().toISOString()}] ❌ ${err.message}`);
  process.exit(1);
});
