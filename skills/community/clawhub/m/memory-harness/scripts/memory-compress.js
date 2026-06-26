#!/usr/bin/env node

function main() {
  const input = process.argv.slice(2).join(" ").trim();

  let parsed = {};
  try {
    parsed = input ? JSON.parse(input) : {};
  } catch {
    parsed = { items: [{ text: input }] };
  }

  const items = Array.isArray(parsed.items) ? parsed.items : [];
  const seen = new Set();
  const compressed = [];

  for (const item of items) {
    const text = String(item?.text || "").trim();
    if (!text) continue;
    if (seen.has(text)) continue;
    seen.add(text);
    compressed.push({
      text: text.length > 160 ? text.slice(0, 160) + "..." : text
    });
    if (compressed.length >= 5) break;
  }

  const out = {
    totalCount: items.length,
    compressedCount: compressed.length,
    items: compressed
  };

  process.stdout.write(JSON.stringify(out, null, 2) + "\n");
}

main();
