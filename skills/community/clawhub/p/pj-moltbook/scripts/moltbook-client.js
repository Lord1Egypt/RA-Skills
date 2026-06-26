/**
 * Moltbook API Client for AI Agents — v16
 *
 * Key algorithm improvement (v16):
 * - Trie-based token matching with 1-letter tolerance
 * - Exhaustive search as fallback (catches merged forms like "twentythree")
 * - Dedupe-based matching: "ThReE" → dedupe → "three" → match
 * - Greedy overlap resolution with strategy priority
 * - Subtraction: merge adjacent tokens (e.g. "twenty three" → 23)
 *
 * Usage: Include in browser evaluate, then use createMoltbookClient(apiKey)
 */

function createMoltbookClient(apiKey) {
  if (!apiKey) throw new Error("MOLTBOOK_API_KEY is required");

  const BASE = "https://www.moltbook.com/api/v1";

  // ─────────────────────────────────────────────
  //  Number word dictionary (sorted by length desc)
  // ─────────────────────────────────────────────
  const NUMBER_WORDS_SORTED = [
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

  // Dedupe map: key = dedupe(word), value = number
  const _NUM_DEDUP = {};
  for (const [w, n] of NUMBER_WORDS_SORTED) {
    _NUM_DEDUP[dedupeLetters(w)] = n;
  }

  // ─────────────────────────────────────────────
  //  Dedupe: collapse consecutive duplicate letters
  //  "ThReE" → "thre", "twentythre" → "twenty"
  //  This is the core insight of v16
  // ─────────────────────────────────────────────
  function dedupeLetters(text) {
    let result = '';
    for (let i = 0; i < text.length; i++) {
      if (i === 0 || text[i] !== text[i - 1]) result += text[i];
    }
    return result;
  }

  // ─────────────────────────────────────────────
  //  Trie for fast prefix matching
  // ─────────────────────────────────────────────
  class TrieNode {
    constructor() { this.children = {}; this.num = null; this.isEnd = false; }
  }

  class Trie {
    constructor() {
      this.root = new TrieNode();
      for (const [word, num] of NUMBER_WORDS_SORTED) {
        let node = this.root;
        for (const ch of word) {
          if (!node.children[ch]) node.children[ch] = new TrieNode();
          node = node.children[ch];
        }
        node.isEnd = true;
        node.num = num;
      }
    }

    /** Match at position s[start:], returns {num, len} or null */
    matchAt(s, start) {
      const results = [];

      // Strategy 1: exact path
      let node = this.root, pos = start;
      while (pos < s.length && s[pos] in node.children) {
        node = node.children[s[pos++]];
        if (node.isEnd) results.push({ num: node.num, len: pos - start, strategy: 'trie' });
      }

      // Strategy 2: allow 1 skipped char (1 interference letter)
      node = this.root; pos = start; let skipped = 0;
      while (pos < s.length && skipped <= 1) {
        if (s[pos] in node.children) {
          node = node.children[s[pos++]];
          skipped = 0;
          if (node.isEnd) results.push({ num: node.num, len: pos - start, strategy: 'trie' });
        } else {
          skipped++; pos++;
        }
      }

      // Strategy 3: dedupe-based matching (handles "ThReE"→"thre")
      for (const [word, num] of NUMBER_WORDS_SORTED) {
        const cand = s.slice(start, start + word.length);
        if (cand.length < word.length) continue;

        // Exact dedupe match
        if (dedupeLetters(cand) === word) {
          results.push({ num, len: word.length, strategy: 'dedupe' });
          continue;
        }

        // Dedupe after skipping 1 letter (handles "Thre"→"thre" dedupe→"three")
        for (let skip = 0; skip < cand.length; skip++) {
          const skipCand = cand.slice(0, skip) + cand.slice(skip + 1);
          if (dedupeLetters(skipCand) === word) {
            results.push({ num, len: word.length, strategy: 'dedupe' });
            break;
          }
        }

        // Restore trailing letter: dedupe(cand) == word[:-1] && last char matches
        const dedupedCand = dedupeLetters(cand);
        if (dedupedCand.length === word.length - 1 && dedupedCand === word.slice(0, -1)) {
          if (dedupeLetters(dedupedCand + cand[cand.length - 1]) === word) {
            results.push({ num, len: word.length, strategy: 'dedupe' });
          }
        }
      }

      if (results.length === 0) return null;
      // Prefer dedupe > trie; longest match wins
      results.sort((a, b) => {
        if (b.strategy !== a.strategy) return a.strategy === 'dedupe' ? -1 : 1;
        return b.len - a.len;
      });
      return results[0];
    }
  }

  // ─────────────────────────────────────────────
  //  Tokenise original text preserving word boundaries
  //  Returns: [{text, offset}]  (cleaned lower, word boundaries from original)
  // ─────────────────────────────────────────────
  function splitByWords(text) {
    const tokens = [];
    let inWord = false, wordStart = 0, wordChars = [], cleanPos = 0;
    for (let i = 0; i < text.length; i++) {
      const ch = text[i];
      if (/[a-zA-Z]/.test(ch)) {
        if (!inWord) { inWord = true; wordStart = cleanPos; wordChars = []; }
        wordChars.push(ch.toLowerCase());
        cleanPos++;
      } else {
        if (inWord) { tokens.push({ text: wordChars.join(''), offset: wordStart }); inWord = false; }
      }
    }
    if (inWord) tokens.push({ text: wordChars.join(''), offset: wordStart });
    return tokens;
  }

  // ─────────────────────────────────────────────
  //  Exhaustive search across full cleaned string
  //  Catches merged forms like "twentythree" (no space)
  // ─────────────────────────────────────────────
  function findAllNumbers(cleaned) {
    const results = [];
    for (let i = 0; i < cleaned.length; i++) {
      for (const [word, num] of NUMBER_WORDS_SORTED) {
        const end = i + word.length;
        if (end > cleaned.length) continue;
        const slice = cleaned.slice(i, end);
        if (dedupeLetters(slice) === word) {
          results.push({ num, idx: i, end, strategy: 'exhaustive', len: word.length });
          break;
        }
        // Allow 1 extra char read at the end
        if (end < cleaned.length) {
          const cand = cleaned.slice(i, end + 1);
          for (let skip = 0; skip < cand.length; skip++) {
            if (dedupeLetters(cand.slice(0, skip) + cand.slice(skip + 1)) === word) {
              results.push({ num, idx: i, end: end + 1, strategy: 'exhaustive', len: word.length });
              break;
            }
          }
        }
      }
    }
    return results;
  }

  // ─────────────────────────────────────────────
  //  Token-level search: Trie match + dedupe
  // ─────────────────────────────────────────────
  function tokenSearch(tokens) {
    const found = [];
    const trie = new Trie();
    for (const { text, offset } of tokens) {
      const result = trie.matchAt(text, 0);
      if (result) found.push({ num: result.num, idx: offset, end: offset + result.len, strategy: result.strategy, len: result.len });
    }
    // Token-level dedupe
    for (const { text, offset } of tokens) {
      const deduped = dedupeLetters(text);
      if (deduped in _NUM_DEDUP) {
        const num = _NUM_DEDUP[deduped];
        const end = offset + text.length;
        if (!found.some(f => f.idx < end && f.end > offset)) {
          found.push({ num, idx: offset, end, strategy: 'dedupe', len: text.length });
        }
      }
    }
    // Token merge dedupe (adjacent tokens, e.g. "twenty"+"three" → 23)
    for (let i = 0; i < tokens.length - 1; i++) {
      const merged = dedupeLetters(tokens[i].text + tokens[i + 1].text);
      if (merged in _NUM_DEDUP) {
        const num = _NUM_DEDUP[merged];
        const end = tokens[i + 1].offset + tokens[i + 1].text.length;
        if (!found.some(f => f.idx < end && f.end > tokens[i].offset)) {
          found.push({ num, idx: tokens[i].offset, end, strategy: 'merge', len: merged.length });
        }
      }
    }
    return found;
  }

  // ─────────────────────────────────────────────
  //  Main solve function
  // ─────────────────────────────────────────────
  function solveChallenge(challengeText) {
    const cleaned = challengeText.toLowerCase().replace(/[^a-z]/g, '');
    const tokens = splitByWords(challengeText);
    const preferMerge = detectOperation(challengeText) === 'subtract';

    // Step 1: Token-level search
    let allFound = tokenSearch(tokens);

    // Step 2: Exhaustive fallback if < 2 numbers found
    if (allFound.length < 2) {
      const exhaustive = findAllNumbers(cleaned);
      for (const ex of exhaustive) {
        if (!allFound.some(f => f.idx === ex.idx)) allFound.push(ex);
      }
    }

    // Step 3: Greedy deduplication by strategy priority
    const priority = preferMerge
      ? { merge: 0, dedupe: 1, exhaustive: 2, trie: 3 }
      : { trie: 0, dedupe: 1, exhaustive: 2, merge: 3 };
    allFound.sort((a, b) => {
      if (a.idx !== b.idx) return a.idx - b.idx;
      return (priority[a.strategy] ?? 9) - (priority[b.strategy] ?? 9);
    });

    const selected = [];
    let lastEnd = -1;
    for (const f of allFound) {
      if (f.idx >= lastEnd) {
        selected.push(f);
        lastEnd = f.end;
      }
    }

    if (selected.length < 2) {
      return {
        success: false,
        error: `Found ${selected.length} number(s). Challenge: "${challengeText.slice(0, 80)}"`,
        numbers: selected,
        cleaned
      };
    }

    const a = selected[0].num, b = selected[1].num;
    const op = detectOperation(challengeText);
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
  //  Detect operation keyword
  // ─────────────────────────────────────────────
  function detectOperation(text) {
    const lower = text.toLowerCase();
    if (/\b(slows|slow|decelerat|brake|reduc|less|lost|subtract|minus|decreas|drop)\b/.test(lower)) return 'subtract';
    if (/\b(product|multiplied|times)\b/.test(lower)) return 'multiply';
    if (/\bdivid/.test(lower)) return 'divide';
    return 'add';
  }

  // ─────────────────────────────────────────────
  //  HTTP helpers
  // ─────────────────────────────────────────────
  async function request(method, endpoint, body = null) {
    const opts = { method, headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" } };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${BASE}${endpoint}`, opts);
    return res.json();
  }

  async function verify(verificationCode, answer) {
    return request("POST", "/verify", { verification_code: verificationCode, answer });
  }

  async function autoVerify(verification) {
    if (!verification) return null;
    const result = solveChallenge(verification.challenge_text);
    if (!result.success) return { autoSolved: false, verification, parseResult: result };
    const vResult = await verify(verification.verification_code, result.answerStr || result.answer.toFixed(2));
    return { autoSolved: true, answer: result.answer, detail: result, verifyResult: vResult };
  }

  // ─────────────────────────────────────────────
  //  Public API
  // ─────────────────────────────────────────────
  async function publishPost(submolt, title, content) {
    const data = await request("POST", "/posts", { submolt_name: submolt, title, content });
    if (data.post?.verification) {
      const vResult = await autoVerify(data.post.verification);
      return { post: data.post, verification: vResult };
    }
    return { post: data.post };
  }

  async function commentOnPost(postId, content) {
    const data = await request("POST", `/posts/${postId}/comments`, { content });
    if (data.comment?.verification) {
      const vResult = await autoVerify(data.comment.verification);
      return { comment: data.comment, verification: vResult };
    }
    return { comment: data.comment };
  }

  async function upvotePost(postId) { return request("POST", `/posts/${postId}/upvote`); }

  async function batchUpvote(postIds) {
    const results = [];
    for (const id of postIds) {
      try { results.push(await upvotePost(id)); } catch (e) { results.push({ error: e.message, postId: id }); }
    }
    return results;
  }

  async function getFeed() { const d = await request("GET", "/feed"); return d.posts || []; }
  async function getPost(postId) { return request("GET", `/posts/${postId}`); }
  async function getAgentInfo() { return request("GET", "/agents/me"); }

  return {
    publishPost, commentOnPost, upvotePost, batchUpvote,
    getFeed, getPost, getAgentInfo,
    solveChallenge, autoVerify
  };
}