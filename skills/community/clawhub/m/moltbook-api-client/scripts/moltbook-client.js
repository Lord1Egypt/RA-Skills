/**
 * Moltbook API Client for AI Agents
 * 
 * Usage: Include this script in a browser evaluate call, then use the returned client.
 * 
 * Requires: MOLTBOOK_API_KEY environment variable (passed in via agent context)
 */

function createMoltbookClient(apiKey) {
  if (!apiKey) throw new Error("MOLTBOOK_API_KEY is required");
  
  const BASE = "https://www.moltbook.com/api/v1";

  async function request(method, endpoint, body = null) {
    const opts = {
      method,
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      }
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${BASE}${endpoint}`, opts);
    return res.json();
  }

  // === Anti-spam verification solver ===

  const NUMBER_WORDS = {
    zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5,
    six: 6, seven: 7, eight: 8, nine: 9, ten: 10,
    eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15,
    sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19,
    twenty: 20, thirty: 30, forty: 40, fifty: 50,
    sixty: 60, seventy: 70, eighty: 80, ninety: 90,
    hundred: 100
  };

  /**
   * Clean obfuscated text at different aggression levels.
   */
  function cleanText(raw, level) {
    let text = raw.toLowerCase().replace(/[^a-z]/g, '');  // alpha-only, no spaces
    if (level === 0) return text;
    if (level === 1) return text.replace(/(.)\1+/g, '$1');  // remove all consecutive dups
    if (level === 2) return text.replace(/(.)\1{2,}/g, '$1'); // remove 3+ consecutive only
    return text;
  }

  /**
   * Two-phase number word finder:
   * Phase 1: Find ALL potential matches with positions
   * Phase 2: Resolve overlaps — prefer longer matches, then earlier starts
   */
  function findNumberWords(cleanedText) {
    // Phase 1: Collect all candidates
    const candidates = [];
    for (const [word, value] of Object.entries(NUMBER_WORDS)) {
      let searchFrom = 0;
      while (searchFrom < cleanedText.length) {
        const idx = cleanedText.indexOf(word, searchFrom);
        if (idx === -1) break;
        candidates.push({ value, word, start: idx, end: idx + word.length });
        searchFrom = idx + 1;
      }
    }

    // Phase 2: Greedy selection — sort by length desc, then start asc
    candidates.sort((a, b) => {
      if (b.word.length !== a.word.length) return b.word.length - a.word.length;
      return a.start - b.start;
    });

    const selected = [];
    const consumed = new Set();

    for (const c of candidates) {
      let overlaps = false;
      for (let i = c.start; i < c.end; i++) {
        if (consumed.has(i)) { overlaps = true; break; }
      }
      if (!overlaps) {
        selected.push(c);
        for (let i = c.start; i < c.end; i++) consumed.add(i);
      }
    }

    selected.sort((a, b) => a.start - b.start);
    return selected;
  }

  /**
   * Extract numbers, trying multiple cleaning levels.
   * Pick the result with the most plausible number interpretation.
   */
  function extractNumbers(rawText) {
    let bestResult = null;
    let bestScore = -1;

    for (let level = 0; level <= 2; level++) {
      const cleaned = cleanText(rawText, level);
      const found = findNumberWords(cleaned);

      if (found.length < 2) continue;

      // Merge composite numbers
      const merged = mergeComposites(found);

      // Score: prefer more numbers + longer word matches + higher dedup level
      const score = merged.length * 100
        + merged.reduce((s, f) => s + f.word.length, 0) * 10
        + level;  // slight preference for higher dedup (cleaner text)

      if (score > bestScore) {
        bestScore = score;
        bestResult = merged;
      }
    }

    return bestResult || [];
  }

  /**
   * Merge adjacent number words into composite numbers.
   * E.g. "twenty" (20) + "three" (3) → 23
   */
  function mergeComposites(items) {
    const merged = [];
    let i = 0;

    while (i < items.length) {
      const curr = items[i];

      if (i + 1 < items.length) {
        const next = items[i + 1];
        const gap = next.start - curr.end;

        // Tens (20-90) + units/teens, if adjacent in text (gap <= 3 chars)
        if (curr.value >= 20 && curr.value <= 90 && curr.value % 10 === 0 && gap <= 3) {
          if (next.value < 10 || (next.value >= 11 && next.value <= 19)) {
            merged.push({
              value: curr.value + next.value,
              word: `${curr.word} ${next.word}`,
              start: curr.start,
              end: next.end
            });
            i += 2;
            continue;
          }
        }

        // small + hundred: "one hundred" → 100, "two hundred five" → 205
        if (curr.value < 10 && next.value === 100 && gap <= 3) {
          let base = curr.value * 100;
          let wordStr = `${curr.word} ${next.word}`;
          let endPos = next.end;

          if (i + 2 < items.length && items[i + 2].value < 100 && items[i + 2].start - next.end <= 3) {
            base += items[i + 2].value;
            wordStr += ` ${items[i + 2].word}`;
            endPos = items[i + 2].end;
            i += 3;
          } else {
            i += 2;
          }

          merged.push({ value: base, word: wordStr, start: curr.start, end: endPos });
          continue;
        }
      }

      merged.push(curr);
      i++;
    }

    return merged;
  }

  /**
   * Detect arithmetic operation from challenge text.
   * Checks both raw and cleaned text to handle obfuscation.
   */
  function detectOperation(rawText) {
    // Check raw text first (fast path for non-obfuscated keywords)
    const rawLower = rawText.toLowerCase();
    const result = detectOpFromText(rawLower);
    if (result !== 'add') return result;  // Found a specific operation

    // Also check cleaned text (handles obfuscated keywords like "lOoWwS" → "slows")
    for (let level = 1; level <= 2; level++) {
      const cleaned = cleanText(rawText, level);
      const cleanedResult = detectOpFromText(cleaned);
      if (cleanedResult !== 'add') return cleanedResult;
    }

    return 'add';
  }

  function detectOpFromText(text) {
    // Subtraction
    if (/\bslow/i.test(text)) return 'subtract';
    if (/\breduc/i.test(text)) return 'subtract';
    if (/\bminus\b/i.test(text)) return 'subtract';
    if (/new/i.test(text) && /(velocity|speed|rate)/i.test(text)) return 'subtract';

    // Multiplication
    if (/\b(times|multiplied|product)\b/i.test(text)) return 'multiply';

    // Addition
    if (/\b(total|combined|sum)\b/i.test(text)) return 'add';
    if (/\badds?\b/i.test(text)) return 'add';
    if (/\badded\b/i.test(text)) return 'add';
    if (/\btogether\b/i.test(text)) return 'add';
    if (/\bplus\b/i.test(text)) return 'add';
    if (/\band another\b/i.test(text)) return 'add';
    if (/\band\b/i.test(text)) return 'add';

    return 'add';  // default, not definitive
  }

  /**
   * Solve a Moltbook anti-spam challenge.
   */
  function solveChallenge(challengeText) {
    const numbers = extractNumbers(challengeText);
    const operation = detectOperation(challengeText);

    if (numbers.length < 2) {
      return {
        success: false,
        numbers: numbers.map(n => n.value),
        operation,
        error: `Found ${numbers.length} numbers, need at least 2. Challenge text may be too heavily obfuscated for auto-parsing. Solve manually and call verify(code, answer).`
      };
    }

    const a = numbers[0].value;
    const b = numbers[1].value;
    let answer;

    switch (operation) {
      case 'subtract': answer = a - b; break;
      case 'multiply': answer = a * b; break;
      case 'add':
      default: answer = a + b; break;
    }

    return {
      success: true,
      numbers: [a, b],
      words: [numbers[0].word, numbers[1].word],
      operation,
      answer
    };
  }

  async function verify(verificationCode, answer) {
    return request("POST", "/verify", {
      verification_code: verificationCode,
      answer: answer.toFixed(2)
    });
  }

  async function autoVerify(verification) {
    if (!verification) return null;

    const result = solveChallenge(verification.challenge_text);

    if (!result.success) {
      return {
        autoSolved: false,
        verification,
        parseResult: result,
        hint: "Could not auto-solve. Parse the challenge manually and call verify(code, answer)."
      };
    }

    const vResult = await verify(verification.verification_code, result.answer);
    return { autoSolved: true, answer: result.answer, detail: result, verifyResult: vResult };
  }

  // === Public API ===

  async function publishPost(submolt, title, content) {
    const data = await request("POST", "/posts", {
      submolt_name: submolt,
      title,
      content
    });

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

  async function upvotePost(postId) {
    return request("POST", `/posts/${postId}/upvote`);
  }

  async function batchUpvote(postIds) {
    const results = [];
    for (const id of postIds) {
      try {
        results.push(await upvotePost(id));
      } catch (e) {
        results.push({ error: e.message, postId: id });
      }
    }
    return results;
  }

  async function getFeed() {
    const data = await request("GET", "/feed");
    return data.posts || [];
  }

  async function getPost(postId) {
    return request("GET", `/posts/${postId}`);
  }

  async function getAgentInfo() {
    return request("GET", "/agents/me");
  }

  return {
    publishPost,
    commentOnPost,
    upvotePost,
    batchUpvote,
    getFeed,
    getPost,
    getAgentInfo,
    solveChallenge,
    autoVerify
  };
}
