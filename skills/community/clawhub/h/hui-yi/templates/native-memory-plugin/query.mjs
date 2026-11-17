const NOISE = new Set([
  "什么", "这个", "那个", "我们", "你们", "请问", "一下", "告诉", "现在",
  "之前", "可以", "需要", "帮我", "记得", "回忆", "我的", "请你", "怎么",
  "the", "and", "please", "what", "this", "that", "with", "from",
]);
const MARKER = "\n[Recall search terms only; not additional user facts]\n";
const HAN_NOISE = new RegExp([...NOISE].filter(word => /^\p{Script=Han}+$/u.test(word)).join("|"), "u");

// Match the latest-message noise removal in audited OpenClaw 2026.9.5
// query-BoM0vDJB.mjs. Do not copy its empty-result fallback to raw text: stripped
// content must never acquire new searchable words outside its original block.
export function cleanExpansionSource(text) {
  return text
    .replace(/<<<EXTERNAL_UNTRUSTED_CONTENT\b[^>]*>>>[\s\S]*?<<<END_EXTERNAL_UNTRUSTED_CONTENT\b[^>]*>>>/g, " ")
    .replace(/```(?:json)?\s*[\s\S]*?```/gi, " ")
    .replace(/<active_memory_plugin>[\s\S]*?<\/active_memory_plugin>/gi, " ")
    .split("\n").map(line => line.trim()).filter(line => {
      if (!line || line === "Context:") return false;
      if (/^(conversation info|sender|untrusted context)\b/i.test(line)) return false;
      if (/^(source: external|---|untrusted discord message body)$/i.test(line)) return false;
      if (/^⚠️?\s*Agent couldn't generate a response/i.test(line)) return false;
      if (/^Please try again\.?$/i.test(line)) return false;
      return true;
    }).join(" ").replace(/\s+/g, " ").trim();
}

// Return data only. Matchers must not tokenize the human-readable marker used
// by expandRecallQuery, which contains words absent from the user's request.
export function recallQueryTerms(original) {
  if (typeof original !== "string" || !original.trim()) return [];
  // Bound work as well as output when the host supplies a large fallback prompt.
  // Preserve the complete original text; only expansion examines this prefix.
  // Strip before slicing so a cut inside a closed block cannot expose its tail.
  const normalized = cleanExpansionSource(original).slice(0, 4096).normalize("NFKC");
  const buckets = Array.from({ length: 8 }, () => new Set());
  const add = (bucket, token) => {
    const key = token.toLowerCase();
    if (bucket.size < 256 && !NOISE.has(key) && key.length >= 2) bucket.add(key);
  };
  const runs = [...normalized.matchAll(/\p{Script=Han}+/gu)]
    .flatMap(match => match[0].split(HAN_NOISE)).filter(Boolean).map(run => [...run]);
  // Split at query noise without joining unrelated words across it. Balance
  // span lengths so long spans cannot exhaust all space before exact short tags.
  for (let size = 8; size >= 2; size--) {
    for (const run of runs) {
      for (let start = 0; start + size <= run.length; start++) add(buckets[8 - size], run.slice(start, start + size).join(""));
    }
  }
  for (const match of normalized.matchAll(/[A-Za-z0-9][A-Za-z0-9._-]*/g)) add(buckets[7], match[0]);
  const queues = buckets.map(bucket => [...bucket]);
  const terms = new Set();
  for (let index = 0; index < 256; index++) {
    for (const queue of queues) if (queue[index] !== undefined) terms.add(queue[index]);
  }
  const selected = [];
  let length = MARKER.length;
  for (const term of terms) {
    if (selected.length >= 256 || length + term.length + 1 > 2000) break;
    selected.push(term);
    length += term.length + 1;
  }
  return selected;
}

export function expandRecallQuery(original) {
  const terms = recallQueryTerms(original);
  return terms.length ? original + MARKER + terms.join(" ") : original;
}
