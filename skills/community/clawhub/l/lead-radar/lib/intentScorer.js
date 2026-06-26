const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

const KEYWORD_EXTRACTION_PROMPT = `Extract 3-5 search keywords from this product description. Return a JSON array of strings.

Example: "I sell a CRM tool for freelance designers"
Output: ["CRM for freelancers", "freelance client tracking", "invoice management freelance", "freelance designer tools", "freelance CRM software"]`;

const INTENT_SCORING_PROMPT = `You are a sales intent classifier. Given a social media post and a product offer, determine if the post author is a warm lead.

OFFER: {OFFER_DESCRIPTION}

POST:
Title: {title}
Body: {body}
Source: {source}

Return ONLY this JSON object, nothing else:
{"score": 0, "reason": "", "intent_type": "none", "draft_reply": ""}

Rules:
- score: integer 0-10
- reason: one sentence
- intent_type: one of "asking_for_tool", "expressing_pain", "comparing_options", "none"
- draft_reply: helpful non-spammy reply under 100 words if score >= 5, empty string otherwise`;

function extractJSON(text) {
  if (!text || !text.trim()) return null;

  // Try direct parse first
  try {
    return JSON.parse(text);
  } catch {}

  // Try to find JSON object in the text
  const objMatch = text.match(/\{[\s\S]*\}/);
  if (objMatch) {
    try {
      return JSON.parse(objMatch[0]);
    } catch {}
  }

  // Try to find JSON array in the text
  const arrMatch = text.match(/\[[\s\S]*\]/);
  if (arrMatch) {
    try {
      return JSON.parse(arrMatch[0]);
    } catch {}
  }

  // Handle truncated JSON — extract score and fields manually
  const scoreMatch = text.match(/"score"\s*:\s*(\d+)/);
  if (scoreMatch) {
    const score = parseInt(scoreMatch[1], 10);
    const reasonMatch = text.match(/"reason"\s*:\s*"([^"]*)/);
    const intentMatch = text.match(/"intent_type"\s*:\s*"([^"]*)/);
    const replyMatch = text.match(/"draft_reply"\s*:\s*"([^"]*)/);
    return {
      score,
      reason: reasonMatch ? reasonMatch[1] : '',
      intent_type: intentMatch ? intentMatch[1] : 'none',
      draft_reply: replyMatch ? replyMatch[1] : '',
    };
  }

  return null;
}

async function callGemini(prompt, maxTokens = 300, retries = 2) {
  const apiKey = process.env.GEMINI_API_KEY;

  for (let attempt = 0; attempt <= retries; attempt++) {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: {
            maxOutputTokens: maxTokens,
            temperature: 0.2,
            responseMimeType: 'application/json',
          },
        }),
      }
    );

    if (!res.ok) {
      const err = await res.text();
      if (attempt < retries) {
        await new Promise((r) => setTimeout(r, 1000 * (attempt + 1)));
        continue;
      }
      throw new Error(`Gemini API error: ${res.status} — ${err}`);
    }

    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!text) {
      if (attempt < retries) {
        await new Promise((r) => setTimeout(r, 1000 * (attempt + 1)));
        continue;
      }
      throw new Error('Gemini returned empty response');
    }

    return text;
  }
}

function smartFallbackKeywords(offerDescription) {
  // Extract meaningful 2-3 word phrases from the offer description
  const stopWords = new Set(['i', 'a', 'an', 'the', 'for', 'to', 'and', 'or', 'who', 'that', 'is', 'are', 'my', 'sell', 'offer', 'provide', 'help', 'with', 'of', 'in', 'on', 'it', 'do', 'this', 'their', 'they', 'we', 'our']);
  const words = offerDescription
    .toLowerCase()
    .replace(/[^\w\s]/g, '')
    .split(/\s+/)
    .filter((w) => w.length > 2 && !stopWords.has(w));

  const keywords = [];
  // Create 2-word pairs from meaningful words
  for (let i = 0; i < words.length - 1 && keywords.length < 5; i++) {
    keywords.push(`${words[i]} ${words[i + 1]}`);
  }
  // If we didn't get enough, add individual important words
  if (keywords.length < 3) {
    for (const w of words) {
      if (keywords.length >= 5) break;
      if (w.length > 4) keywords.push(w);
    }
  }
  console.log('[Keywords] Fallback keywords:', keywords.join(', '));
  return keywords.slice(0, 5);
}

async function extractKeywords(offerDescription) {
  const prompt = `${KEYWORD_EXTRACTION_PROMPT}\n\nInput: "${offerDescription}"`;

  try {
    const raw = await callGemini(prompt, 512);
    console.log('[Keywords] Raw Gemini response:', raw.slice(0, 300));
    const parsed = extractJSON(raw);
    console.log('[Keywords] Parsed:', JSON.stringify(parsed));

    if (Array.isArray(parsed)) return parsed;
    if (parsed && parsed.keywords && Array.isArray(parsed.keywords)) return parsed.keywords;
    // Handle { "keywords": [...] } or any object with an array value
    if (parsed && typeof parsed === 'object') {
      const values = Object.values(parsed);
      for (const v of values) {
        if (Array.isArray(v)) return v;
      }
    }

    console.error('Unexpected keyword format, using fallback');
    return smartFallbackKeywords(offerDescription);
  } catch (err) {
    console.error('Keyword extraction failed:', err.message);
    return smartFallbackKeywords(offerDescription);
  }
}

/**
 * Pre-filter posts by keyword relevance before sending to AI.
 * Posts whose title+body contain at least one keyword token get through.
 * This avoids wasting API calls on completely irrelevant posts.
 */
function preFilter(posts, offerDescription) {
  // Build a set of meaningful tokens from the offer description
  const stopWords = new Set(['i', 'a', 'an', 'the', 'for', 'to', 'and', 'or', 'who', 'that', 'is', 'are', 'my', 'sell', 'offer', 'provide', 'help', 'with', 'of', 'in', 'on', 'it', 'do', 'this', 'their', 'they', 'we', 'our', 'can', 'how', 'what', 'need', 'want']);
  const tokens = offerDescription
    .toLowerCase()
    .replace(/[^\w\s]/g, '')
    .split(/\s+/)
    .filter((w) => w.length > 2 && !stopWords.has(w));

  const filtered = posts.filter((post) => {
    const text = `${post.title || ''} ${post.body || ''}`.toLowerCase();
    return tokens.some((token) => text.includes(token));
  });

  console.log(`[Lead Radar] Pre-filter: ${filtered.length}/${posts.length} posts match offer keywords (${tokens.join(', ')})`);
  return filtered;
}

async function scoreIntent(posts, offerDescription) {
  // Pre-filter to only score posts with keyword relevance
  const relevant = preFilter(posts, offerDescription);

  if (relevant.length === 0) {
    console.log('[Lead Radar] No posts passed pre-filter, skipping AI scoring');
    return [];
  }

  const scored = [];

  // Process in batches of 5 for speed (Gemini has generous rate limits)
  const batchSize = 5;
  for (let i = 0; i < relevant.length; i += batchSize) {
    const batch = relevant.slice(i, i + batchSize);

    const results = await Promise.all(
      batch.map(async (post) => {
        try {
          const prompt = INTENT_SCORING_PROMPT
            .replace('{OFFER_DESCRIPTION}', offerDescription)
            .replace('{title}', (post.title || '').slice(0, 200))
            .replace('{body}', (post.body || '').slice(0, 500))
            .replace('{source}', post.source);

          const raw = await callGemini(prompt, 1024);
          const result = extractJSON(raw);

          if (!result || typeof result.score !== 'number') {
            console.error(`Invalid score response for ${post.id}. Raw:`, raw.slice(0, 500));
            return null;
          }

          if (result.score >= 5) {
            return {
              ...post,
              intentScore: result.score,
              intentReason: result.reason || '',
              intentType: result.intent_type || 'none',
              draftReply: result.draft_reply || '',
            };
          }
          return null;
        } catch (err) {
          console.error(`Scoring failed for ${post.id}:`, err.message);
          return null;
        }
      })
    );

    scored.push(...results.filter(Boolean));

    // Short delay between batches to respect rate limits
    if (i + batchSize < relevant.length) {
      await new Promise((r) => setTimeout(r, 500));
    }
  }

  // Sort by intent score descending, take top 10
  scored.sort((a, b) => b.intentScore - a.intentScore);
  return scored.slice(0, 10);
}

module.exports = { extractKeywords, scoreIntent };
