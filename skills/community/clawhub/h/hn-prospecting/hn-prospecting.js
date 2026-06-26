/**
 * Skill: Hacker News Lead Prospecting
 * Publisher: @modelfitai
 *
 * Find high-intent leads on Hacker News via the free Algolia HN Search API.
 * No API key required — fully public endpoint.
 *
 * Commands:
 *   search <keyword>                        — Find high-intent HN posts
 *   ask <keyword>                           — Find Ask HN threads only
 *   front                                   — Get current front page stories
 *   score --title "..." --points 45 --comments 32  — Score a post for lead quality
 *
 * Example:
 *   node hn-prospecting.js search "looking for AI agent tool"
 *   node hn-prospecting.js ask "outreach automation"
 *   node hn-prospecting.js front
 *
 * No API key required.
 */

import https from 'https';

// =============================================
// INTENT ANALYSIS
// =============================================

/**
 * Analyze an HN post for lead generation opportunity
 */
export function analyzeHnPost({ title, text = '', points = 0, numComments = 0, tags = [] }) {
  if (!title) return { success: false, error: 'Title is required' };

  const fullText = `${title} ${text}`.toLowerCase();

  const highIntent = [
    'what do you use', 'what are you using', 'looking for',
    'any recommendations', 'alternative to', 'switching from',
    'ask hn:', 'what tool', 'which tool', 'best way to',
    'how do you', 'anyone built', 'worth paying for',
    'replacing', 'frustrated with', 'tired of',
  ];

  const mediumIntent = [
    'thinking about', 'considering', 'opinions on',
    'workflow for', 'experience with', 'used by anyone',
    'show hn:', 'launch hn:',
  ];

  let intentLevel = 'low';
  let matchedPhrase = null;

  for (const phrase of highIntent) {
    if (fullText.includes(phrase)) {
      intentLevel = 'high';
      matchedPhrase = phrase;
      break;
    }
  }
  if (intentLevel === 'low') {
    for (const phrase of mediumIntent) {
      if (fullText.includes(phrase)) {
        intentLevel = 'medium';
        matchedPhrase = phrase;
        break;
      }
    }
  }

  // HN-specific signals
  const isAskHn = title.toLowerCase().startsWith('ask hn:');
  const isShowHn = title.toLowerCase().startsWith('show hn:');
  const isTrending = points >= 100;
  const isActive = numComments >= 20;

  // Ask HN threads are always high-intent for tool discovery
  if (isAskHn && intentLevel === 'low') {
    intentLevel = 'medium';
    matchedPhrase = 'Ask HN thread';
  }

  let responseUrgency;
  if (intentLevel === 'high' && points < 20) {
    responseUrgency = '🔴 Comment now — high-intent, still gaining traction';
  } else if (intentLevel === 'high') {
    responseUrgency = '🟡 Comment within 2 hours — high-intent, competitive';
  } else if (intentLevel === 'medium') {
    responseUrgency = '🟢 Comment within 6 hours';
  } else {
    responseUrgency = '⚪ Monitor — add value only if genuinely relevant';
  }

  return {
    success: true,
    data: {
      intentLevel,
      matchedPhrase,
      isAskHn,
      isShowHn,
      isTrending,
      isActive,
      responseUrgency,
      suggestedApproach: isAskHn
        ? 'Ask HN threads welcome direct recommendations — lead with your honest take, mention alternatives, disclose if you built it'
        : intentLevel === 'high'
          ? 'Reply with 2-3 paragraphs of genuine help → mention your tool naturally with disclosure'
          : 'Add technical value → build credibility → no hard sell',
    },
    summary: `📊 HN: ${intentLevel.toUpperCase()} intent — "${matchedPhrase || 'no keyword match'}" | ${points}pts ${numComments} comments`,
  };
}

/**
 * Score an HN post as a lead generation opportunity (0-200)
 */
export function scoreHnPost({ title, points = 0, numComments = 0, isAskHn = false, matchedKeyword = false }) {
  let score = 0;
  const reasons = [];

  if (isAskHn) {
    score += 40;
    reasons.push('Ask HN thread — community expects recommendations');
  }

  if (matchedKeyword) {
    score += 30;
    reasons.push('Matched your target keyword');
  }

  // Engagement signals
  if (points >= 100) { score += 25; reasons.push('Trending (100+ points)'); }
  else if (points >= 30) { score += 15; reasons.push('Gaining traction (30+ points)'); }
  else if (points < 10) { score += 20; reasons.push('Early — first-mover advantage in comments'); }

  if (numComments >= 30) { score += 20; reasons.push('Active discussion (30+ comments)'); }
  else if (numComments >= 10) { score += 10; reasons.push('Some discussion (10+ comments)'); }
  else if (numComments < 5) { score += 15; reasons.push('Low competition in comments'); }

  // Title signals
  const titleLower = (title || '').toLowerCase();
  if (['alternative', 'replacement', 'switching'].some(w => titleLower.includes(w))) {
    score += 25; reasons.push('Actively seeking alternative (high buying intent)');
  }
  if (['looking for', 'need', 'want'].some(w => titleLower.includes(w))) {
    score += 20; reasons.push('Active need expressed');
  }

  let tier;
  if (score >= 80) tier = '🔥 HOT';
  else if (score >= 50) tier = '🟡 WARM';
  else tier = '🔵 COLD';

  return {
    score,
    maxScore: 200,
    tier,
    reasons,
    nextAction:
      score >= 80
        ? 'Comment immediately with genuine value + natural product mention (with disclosure)'
        : score >= 50
          ? 'Comment helpfully, track thread for follow-up opportunities'
          : 'Bookmark for content inspiration, comment only if genuinely helpful',
    summary: `${tier} HN Lead: Score ${score}/200`,
  };
}

// =============================================
// HN ALGOLIA API
// =============================================

/**
 * Fetch from HN Algolia API
 */
function hnRequest(path) {
  return new Promise((resolve) => {
    const options = {
      hostname: 'hn.algolia.com',
      path,
      headers: { 'Accept': 'application/json' },
    };

    const req = https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ success: true, data: JSON.parse(data) });
        } catch (e) {
          resolve({ success: false, error: `Parse error: ${e.message}` });
        }
      });
    });

    req.on('error', e => resolve({ success: false, error: e.message }));
    req.end();
  });
}

/**
 * Search HN for buying-intent posts matching a keyword
 */
export async function searchHn(keyword, { askOnly = false, count = 15 } = {}) {
  if (!keyword) return { success: false, error: 'Keyword is required' };

  const tags = askOnly ? 'story,ask_hn' : 'story';
  const query = encodeURIComponent(keyword);
  const path = `/api/v1/search?query=${query}&tags=${tags}&hitsPerPage=${count}&numericFilters=points>0`;

  const res = await hnRequest(path);
  if (!res.success) return res;

  const hits = res.data.hits || [];
  const results = hits.map(hit => {
    const isAskHn = (hit.title || '').toLowerCase().startsWith('ask hn:');
    const analysis = analyzeHnPost({
      title: hit.title,
      text: hit.story_text || '',
      points: hit.points || 0,
      numComments: hit.num_comments || 0,
    });
    const scored = scoreHnPost({
      title: hit.title,
      points: hit.points || 0,
      numComments: hit.num_comments || 0,
      isAskHn,
      matchedKeyword: true,
    });

    return {
      title: hit.title,
      url: `https://news.ycombinator.com/item?id=${hit.objectID}`,
      externalUrl: hit.url || null,
      author: hit.author,
      points: hit.points || 0,
      comments: hit.num_comments || 0,
      isAskHn,
      intentLevel: analysis.data?.intentLevel || 'low',
      score: scored.score,
      tier: scored.tier,
      responseUrgency: analysis.data?.responseUrgency,
    };
  }).sort((a, b) => b.score - a.score);

  const hot = results.filter(r => r.tier === '🔥 HOT').length;
  const warm = results.filter(r => r.tier === '🟡 WARM').length;

  return {
    success: true,
    keyword,
    count: results.length,
    results,
    summary: `🟠 Found ${results.length} HN posts for "${keyword}" — ${hot} HOT, ${warm} WARM`,
  };
}

/**
 * Get current front page stories
 */
export async function getHnFrontPage(count = 20) {
  const path = `/api/v1/search?tags=front_page&hitsPerPage=${count}`;
  const res = await hnRequest(path);
  if (!res.success) return res;

  const hits = res.data.hits || [];
  const results = hits.map(hit => ({
    title: hit.title,
    url: `https://news.ycombinator.com/item?id=${hit.objectID}`,
    author: hit.author,
    points: hit.points || 0,
    comments: hit.num_comments || 0,
    isAskHn: (hit.title || '').toLowerCase().startsWith('ask hn:'),
  }));

  return {
    success: true,
    count: results.length,
    results,
    summary: `🟠 HN Front Page: ${results.length} stories | Top: "${results[0]?.title}"`,
  };
}

// =============================================
// CLI ENTRY POINT
// =============================================
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
if (path.resolve(process.argv[1]) === path.resolve(__filename)) {
  const [,, cmd, ...rest] = process.argv;

  const parseArgs = (args) => {
    const result = { _: [] };
    for (let i = 0; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        const key = args[i].slice(2);
        result[key] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      } else {
        result._.push(args[i]);
      }
    }
    return result;
  };

  (async () => {
    switch (cmd) {
      case 'search': {
        const args = parseArgs(rest);
        const keyword = args._.join(' ') || args.keyword;
        if (!keyword) { console.error('Usage: search <keyword>'); process.exit(1); }
        const result = await searchHn(keyword);
        if (!result.success) { console.error(result.error); process.exit(1); }
        console.log(`\n${result.summary}\n`);
        result.results.forEach((r, i) => {
          console.log(`${r.tier} ${i + 1}. ${r.title}`);
          console.log(`   👤 ${r.author} | ▲ ${r.points} pts | 💬 ${r.comments} comments`);
          console.log(`   ${r.responseUrgency || ''}`);
          console.log(`   ${r.url}\n`);
        });
        break;
      }
      case 'ask': {
        const args = parseArgs(rest);
        const keyword = args._.join(' ') || args.keyword || '';
        const result = await searchHn(keyword, { askOnly: true });
        if (!result.success) { console.error(result.error); process.exit(1); }
        console.log(`\n${result.summary}\n`);
        result.results.forEach((r, i) => {
          console.log(`${r.tier} ${i + 1}. ${r.title}`);
          console.log(`   ▲ ${r.points} pts | 💬 ${r.comments} comments | ${r.url}\n`);
        });
        break;
      }
      case 'front': {
        const result = await getHnFrontPage();
        if (!result.success) { console.error(result.error); process.exit(1); }
        console.log(`\n${result.summary}\n`);
        result.results.forEach((r, i) => {
          const tag = r.isAskHn ? '[Ask HN]' : '';
          console.log(`${i + 1}. ${tag} ${r.title}`);
          console.log(`   ▲ ${r.points} pts | 💬 ${r.comments} | ${r.url}\n`);
        });
        break;
      }
      case 'score': {
        const args = parseArgs(rest);
        if (!args.title) { console.error('Usage: score --title "..." --points 45 --comments 32'); process.exit(1); }
        const result = scoreHnPost({
          title: args.title,
          points: parseInt(args.points || '0'),
          numComments: parseInt(args.comments || '0'),
          isAskHn: args.title.toLowerCase().startsWith('ask hn:'),
          matchedKeyword: !!args.keyword,
        });
        console.log(result.summary);
        console.log('Reasons:', result.reasons.join(', ') || 'none');
        console.log('Next action:', result.nextAction);
        break;
      }
      default:
        console.log('Commands:');
        console.log('  search <keyword>          Find high-intent HN posts');
        console.log('  ask [keyword]             Find Ask HN threads');
        console.log('  front                     Get current front page');
        console.log('  score --title "..." --points 45 --comments 32');
    }
  })();
}
