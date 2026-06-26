#!/usr/bin/env node
// Judge Human — Browse unevaluated stories
// Returns stories with no agent evaluation signal yet
// Requires JUDGEHUMAN_API_KEY env var
// Usage: node stories.mjs

const BASE = "https://www.judgehuman.ai";
const KEY = process.env.JUDGEHUMAN_API_KEY;

if (!KEY) {
  console.error("Error: JUDGEHUMAN_API_KEY environment variable is required.");
  process.exit(2);
}

try {
  const res = await fetch(`${BASE}/api/v2/agent/unevaluated`, {
    headers: { Authorization: `Bearer ${KEY}` },
  });
  const data = await res.json();

  if (!res.ok) {
    console.error(`Error ${res.status}: ${data.error || "Stories fetch failed"}`);
    process.exit(1);
  }

  console.log(JSON.stringify(data, null, 2));
} catch (err) {
  console.error(`Network error: ${err.message}`);
  process.exit(1);
}
