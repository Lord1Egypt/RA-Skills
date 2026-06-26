const { getProviderSecret } = require("./secrets");

async function listMiniMaxVoices(languageFilter) {
  const secret = getProviderSecret("minimax");
  if (!secret || !secret.apiKey) {
    throw new Error("MiniMax API key is not configured. Store it first with `node scripts/set_provider_secret.js minimax <api-key>` or set MINIMAX_API_KEY.");
  }

  const response = await fetch("https://api.minimaxi.com/v1/get_voice", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${secret.apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      voice_type: "all"
    })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`MiniMax voice query failed (${response.status}): ${text}`);
  }

  const payload = await response.json();
  if (!payload || !payload.base_resp || payload.base_resp.status_code !== 0) {
    throw new Error(`MiniMax voice query returned an error: ${JSON.stringify(payload)}`);
  }

  const voices = [
    ...((payload.system_voice || []).map((item) => ({ ...item, group: "system" }))),
    ...((payload.cloned_voice || []).map((item) => ({ ...item, group: "cloned" })))
  ];

  const filtered = languageFilter
    ? voices.filter((voice) => {
        const content = `${voice.voice_id || ""} ${(voice.voice_name || "")} ${Array.isArray(voice.description) ? voice.description.join(" ") : ""}`;
        return content.toLowerCase().includes(languageFilter.toLowerCase());
      })
    : voices;

  if (filtered.length === 0) {
    console.log("No voices matched the filter.");
    return;
  }

  filtered.slice(0, 60).forEach((voice) => {
    const description = Array.isArray(voice.description) ? voice.description.join(" / ") : "";
    console.log(`- ${voice.voice_id} | ${voice.voice_name || "Unnamed"} | ${voice.group}${description ? ` | ${description}` : ""}`);
  });

  if (filtered.length > 60) {
    console.log(`... ${filtered.length - 60} more voices not shown`);
  }
}

if (require.main === module) {
  const providerId = process.argv[2];
  const languageFilter = process.argv[3] || "";

  if (!providerId) {
    console.error("Usage: node scripts/list_tts_voices.js <provider-id> [filter]");
    process.exit(1);
  }

  if (providerId !== "minimax") {
    console.error(`Voice listing is currently implemented for minimax only. Received: ${providerId}`);
    process.exit(1);
  }

  listMiniMaxVoices(languageFilter).catch((error) => {
    console.error(error.message || String(error));
    process.exit(1);
  });
}
