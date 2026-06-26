/**
 * Moltbook API Client — v16 (v16: Trie + dedupe + exhaustive + greedy)
 *
 * 算法核心（v16 改进）：
 * 1. Trie 前缀匹配（允许每个字母后跳过1个干扰字符）
 * 2. Dedupe 匹配："ThReE" → dedupe("three") → "thre" → 匹配
 * 3. 全字符串穷举兜底：捕获无空格的合并形式如 "twentythree"
 * 4. 贪心去重叠 + 策略优先级（减法优先 merge，加法优先 trie）
 * 5. Token 合并 dedupe：相邻 token 可拼接后再 dedupe 匹配
 *
 * Usage: Include this file in browser evaluate, then call createClient().METHOD(...)
 * Requires: MOLTBOOK_API_KEY in scope (hardcoded below or from closure)
 */

const MOLTBOOK_API_KEY = "moltbook_sk_oOyURnwFc5RbKKpraIUW9h0BAgM_vNI0";
const BASE = "https://www.moltbook.com/api/v1";

// ─────────────────────────────────────────────
//  核心：数字词字典（按长度降序）
// ─────────────────────────────────────────────
const NW = [
  ["thirtynine",39],["thirtyeight",38],["thirtyseven",37],["thirtysix",36],
  ["thirtyfive",35],["thirtyfour",34],["thirtythree",33],["thirtytwo",32],["thirtyone",31],
  ["twentynine",29],["twentyeight",28],["twentyseven",27],["twentysix",26],
  ["twentyfive",25],["twentyfour",24],["twentythree",23],["twentytwo",22],["twentyone",21],
  ["fortynine",49],["fortyeight",48],["fortyseven",47],["fortysix",46],
  ["fortyfive",45],["fortyfour",44],["fortythree",43],["fortytwo",42],["fortyone",41],
  ["ninety",90],["eighty",80],["seventy",70],["sixty",60],["fifty",50],
  ["forty",40],["thirty",30],["twenty",20],
  ["nineteen",19],["eighteen",18],["seventeen",17],["sixteen",16],
  ["fifteen",15],["fourteen",14],["thirteen",13],["twelve",12],["eleven",11],
  ["ten",10],["nine",9],["eight",8],["seven",7],["six",6],
  ["five",5],["four",4],["three",3],["two",2],["one",1],["zero",0],
];

// Dedupe 映射
const NUM_DEDUP = {};
for (const [w, n] of NW) { NUM_DEDUP[dedupe(w)] = n; }

// ─────────────────────────────────────────────
//  工具函数
// ─────────────────────────────────────────────

/** 去除连续重复字母（核心算法）："ThReE" → "thre" */
function dedupe(text) {
  let r = '';
  for (let i = 0; i < text.length; i++) {
    if (i === 0 || text[i] !== text[i - 1]) r += text[i];
  }
  return r;
}

/** 按词切分，返回 [{text, offset}] */
function splitByWords(text) {
  const tokens = [], lower = text.toLowerCase();
  let inW = false, wStart = 0, chars = [], cleanPos = 0;
  for (let i = 0; i < lower.length; i++) {
    const ch = lower[i];
    if (ch >= 'a' && ch <= 'z') {
      if (!inW) { inW = true; wStart = cleanPos; chars = []; }
      chars.push(ch); cleanPos++;
    } else {
      if (inW) { tokens.push({ text: chars.join(''), offset: wStart }); inW = false; }
    }
  }
  if (inW) tokens.push({ text: chars.join(''), offset: wStart });
  return tokens;
}

/** 检测运算类型 */
function detectOp(text) {
  const t = text.toLowerCase();
  if (/\b(slows|slow|decelerat|brake|reduc|less|lost|subtract|minus|decreas|drop)\b/.test(t)) return 'subtract';
  if (/\b(product|multiplied|times)\b/.test(t)) return 'multiply';
  if (/\bdivid/.test(t)) return 'divide';
  return 'add';
}

// ─────────────────────────────────────────────
//  Trie 实现
// ─────────────────────────────────────────────
class TrieNode { constructor() { this.children = {}; this.num = null; this.isEnd = false; } }

class NumberTrie {
  constructor() {
    this.root = new TrieNode();
    for (const [word, num] of NW) {
      let node = this.root;
      for (const ch of word) {
        if (!node.children[ch]) node.children[ch] = new TrieNode();
        node = node.children[ch];
      }
      node.isEnd = true; node.num = num;
    }
  }

  /** 从 s[start] 位置匹配，返回 [{num, len, strategy}] */
  matchAt(s, start) {
    const results = [];

    // 策略1：精确路径
    let node = this.root, pos = start;
    while (pos < s.length && s[pos] in node.children) {
      node = node.children[s[pos++]];
      if (node.isEnd) results.push({ num: node.num, len: pos - start, strategy: 'trie' });
    }

    // 策略2：允许每个字母后跳过1个干扰字符
    node = this.root; pos = start; let skipped = 0;
    while (pos < s.length && skipped <= 1) {
      if (s[pos] in node.children) {
        node = node.children[s[pos++]]; skipped = 0;
        if (node.isEnd) results.push({ num: node.num, len: pos - start, strategy: 'trie' });
      } else { skipped++; pos++; }
    }

    // 策略3：Dedupe 匹配（处理 "ThReE" → "thre"）
    for (const [word, num] of NW) {
      const cand = s.slice(start, start + word.length);
      if (cand.length < word.length) continue;
      if (dedupe(cand) === word) {
        results.push({ num, len: word.length, strategy: 'dedupe' });
        continue;
      }
      // 跳过任意1个字母后 dedupe
      for (let skip = 0; skip < cand.length; skip++) {
        if (dedupe(cand.slice(0, skip) + cand.slice(skip + 1)) === word) {
          results.push({ num, len: word.length, strategy: 'dedupe' }); break;
        }
      }
      // 末尾字母缺失恢复
      const dc = dedupe(cand);
      if (dc.length === word.length - 1 && dc === word.slice(0, -1)) {
        if (dedupe(dc + cand[cand.length - 1]) === word) {
          results.push({ num, len: word.length, strategy: 'dedupe' });
        }
      }
    }

    if (!results.length) return null;
    results.sort((a, b) => {
      if (a.strategy !== b.strategy) return a.strategy === 'dedupe' ? -1 : 1;
      return b.len - a.len;
    });
    return results[0];
  }
}

// ─────────────────────────────────────────────
//  全字符串穷举搜索（兜底无空格的合并形式）
// ─────────────────────────────────────────────
function findAllNumbers(cleaned) {
  const results = [];
  for (let i = 0; i < cleaned.length; i++) {
    for (const [word, num] of NW) {
      const end = i + word.length;
      if (end > cleaned.length) continue;
      const slice = cleaned.slice(i, end);
      if (dedupe(slice) === word) {
        results.push({ num, idx: i, end, strategy: 'exhaustive', len: word.length }); break;
      }
      // 末尾多读1个字符
      if (end < cleaned.length) {
        const cand = cleaned.slice(i, end + 1);
        for (let skip = 0; skip < cand.length; skip++) {
          if (dedupe(cand.slice(0, skip) + cand.slice(skip + 1)) === word) {
            results.push({ num, idx: i, end: end + 1, strategy: 'exhaustive', len: word.length }); break;
          }
        }
      }
    }
  }
  return results;
}

// ─────────────────────────────────────────────
//  Token 级搜索
// ─────────────────────────────────────────────
function tokenSearch(tokens) {
  const found = [];
  const trie = new NumberTrie();
  for (const { text, offset } of tokens) {
    const r = trie.matchAt(text, 0);
    if (r) found.push({ num: r.num, idx: offset, end: offset + r.len, strategy: r.strategy, len: r.len });
  }
  // Token dedupe
  for (const { text, offset } of tokens) {
    const d = dedupe(text);
    if (d in NUM_DEDUP) {
      const num = NUM_DEDUP[d];
      const end = offset + text.length;
      if (!found.some(f => f.idx < end && f.end > offset)) {
        found.push({ num, idx: offset, end, strategy: 'dedupe', len: text.length });
      }
    }
  }
  // 相邻 token 合并 dedupe（"twenty"+"three" → 23）
  for (let i = 0; i < tokens.length - 1; i++) {
    const merged = dedupe(tokens[i].text + tokens[i + 1].text);
    if (merged in NUM_DEDUP) {
      const num = NUM_DEDUP[merged];
      const end = tokens[i + 1].offset + tokens[i + 1].text.length;
      if (!found.some(f => f.idx < end && f.end > tokens[i].offset)) {
        found.push({ num, idx: tokens[i].offset, end, strategy: 'merge', len: merged.length });
      }
    }
  }
  return found;
}

// ─────────────────────────────────────────────
//  验证码解题主函数（v16 核心）
// ─────────────────────────────────────────────
function solveChallenge(challengeText) {
  const cleaned = challengeText.toLowerCase().replace(/[^a-z]/g, '');
  const tokens = splitByWords(challengeText);
  const preferMerge = detectOp(challengeText) === 'subtract';

  // Step 1: Token 级搜索
  let all = tokenSearch(tokens);

  // Step 2: 穷举兜底（< 2 个数字时触发）
  if (all.length < 2) {
    const ex = findAllNumbers(cleaned);
    for (const x of ex) { if (!all.some(f => f.idx === x.idx)) all.push(x); }
  }

  // Step 3: 贪心去重叠
  const prio = preferMerge
    ? { merge: 0, dedupe: 1, exhaustive: 2, trie: 3 }
    : { trie: 0, dedupe: 1, exhaustive: 2, merge: 3 };
  all.sort((a, b) => {
    if (a.idx !== b.idx) return a.idx - b.idx;
    return (prio[a.strategy] ?? 9) - (prio[b.strategy] ?? 9);
  });
  const selected = []; let lastEnd = -1;
  for (const f of all) { if (f.idx >= lastEnd) { selected.push(f); lastEnd = f.end; } }

  if (selected.length < 2) {
    return { success: false, error: `Found ${selected.length} number(s). Challenge: "${challengeText.slice(0, 80)}"`, numbers: selected, cleaned };
  }

  const a = selected[0].num, b = selected[1].num;
  const op = detectOp(challengeText);
  let answer;
  if (op === 'subtract') answer = a - b;
  else if (op === 'multiply') answer = a * b;
  else if (op === 'divide') answer = b ? a / b : 0;
  else answer = a + b;

  return {
    success: true, answer, answerStr: answer.toFixed(2),
    numbers: selected.slice(0, 4).map(n => ({ word: String(n.num), num: n.num, strategy: n.strategy })),
    operation: op, cleaned, challenge: challengeText.slice(0, 100)
  };
}

// ─────────────────────────────────────────────
//  HTTP 基础请求
// ─────────────────────────────────────────────
async function mbReq(method, endpoint, body) {
  const opts = { method, headers: { Authorization: `Bearer ${MOLTBOOK_API_KEY}`, "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${endpoint}`, opts);
  return res.json();
}

async function verifyAnswer(code, answer) {
  return mbReq("POST", "/verify", { verification_code: code, answer });
}

async function autoVerify(verification) {
  if (!verification) return null;
  const result = solveChallenge(verification.challenge_text);
  if (!result.success) return { autoSolved: false, verification, parseResult: result };
  const vResult = await verifyAnswer(verification.verification_code, result.answerStr);
  return { autoSolved: true, answer: result.answer, detail: result, verifyResult: vResult };
}

// ─────────────────────────────────────────────
//  公开 API
// ─────────────────────────────────────────────
async function publishPost(submolt, title, content) {
  const data = await mbReq("POST", "/posts", { submolt_name: submolt, title, content });
  if (data.post?.verification) {
    const v = await autoVerify(data.post.verification);
    return { post: data.post, verification: v };
  }
  return { post: data.post };
}

async function commentOnPost(postId, content) {
  const data = await mbReq("POST", `/posts/${postId}/comments`, { content });
  if (data.comment?.verification) {
    const v = await autoVerify(data.comment.verification);
    return { comment: data.comment, verification: v };
  }
  return { comment: data.comment };
}

async function upvotePost(postId) { return mbReq("POST", `/posts/${postId}/upvote`); }

async function batchUpvote(postIds) {
  const results = [];
  for (const id of postIds) {
    try { results.push(await upvotePost(id)); } catch (e) { results.push({ error: e.message, postId: id }); }
  }
  return results;
}

async function getFeed() { const d = await mbReq("GET", "/feed"); return d.posts || []; }
async function getPost(postId) { return mbReq("GET", `/posts/${postId}`); }
async function getHome() { return mbReq("GET", "/home"); }
async function getAgentInfo() { return mbReq("GET", "/agents/me"); }
async function editPost(postId, content) { return mbReq("PATCH", `/posts/${postId}`, { content }); }

/** 创建客户端实例（兼容旧写法） */
function createMoltbookClient() {
  return { publishPost, commentOnPost, upvotePost, batchUpvote, getFeed, getPost, getHome, getAgentInfo, editPost, solveChallenge, autoVerify };
}