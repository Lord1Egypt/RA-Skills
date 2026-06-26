const { HorseRacingAPI } = require('hkjc-api');

// Simple in-memory cache (TTL 15 minutes)
const cache = new Map();
// Rate limiting: timestamp of last API call (not cache read)
let lastApiCall = 0;
const RATE_LIMIT_MS = 60 * 1000; // 1 minute

function makeCacheKey({date, classFilter, excludeHorseNos, excludeBarriers, raceNo, advancedScoring, newsBoost, lightWeightBonus, formAnalysis}) {
  const cf = JSON.stringify((classFilter || []).sort());
  const ehn = JSON.stringify((excludeHorseNos || []).sort());
  const eb = JSON.stringify((excludeBarriers || []).sort());
  const rn = raceNo != null ? String(raceNo) : 'all';
  const adv = advancedScoring ? '1' : '0';
  const news = newsBoost ? '1' : '0';
  const lwb = lightWeightBonus != null ? String(lightWeightBonus) : '0.05';
  const fa = formAnalysis ? '1' : '0';
  return `${date}|${cf}|${ehn}|${eb}|${rn}|${adv}|${news}|${lwb}|${fa}`;
}

function getTodayHKT() {
  const now = new Date();
  const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
  const hktTime = new Date(utc + (8 * 3600000));
  return hktTime.toISOString().split('T')[0];
}

function padNumber(num, size = 2) {
  return String(num).padStart(size, '0');
}

// Reason phrases: fixed English
const PHRASES = {
  winOdds: 'Win odds',
  recentForm: 'recent form avg',
  barrier: 'barrier',
  weight: 'weight',
  gear: 'gear',
  tjBonus: 'trainer/jockey bonus',
  barrierBonus: 'barrier effectiveness'
};

// Top jockeys and trainers (names as they appear in HKJC API)
const TOP_JOCKEYS = new Set([
  'Z Purton', 'J Purton', 'Y L Chung', 'B Avdulla', 'A Badel', 'K Teetan', 'M L Yeung', 'C Y Ho'
]);
const TOP_TRAINERS = new Set([
  'K W Lui', 'D J Whyte', 'D A Hayes', 'W Y So', 'C Fownes', 'P F Yiu', 'K H Ting', 'C W Chang', 'Y S Tsui', 'A S Cruz'
]);

// Barrier effectiveness by distance class (empirical approximation)
// Effectiveness score added to candidate score (0-1 scale) multiplied by barrierBonusWeight
function barrierEffectiveness(barrier, distance) {
  if (!barrier) return 0;
  // Short: <1000m, Middle: 1000-1800m, Long: >1800m
  const distClass = distance < 1000 ? 'short' : distance <= 1800 ? 'middle' : 'long';
  // Simplified model: inner barriers (1-4) generally better for short, outer better for long; middle varies.
  const effectiveness = {
    short: [0.10, 0.08, 0.05, 0.02, 0, -0.02, -0.04, -0.06, -0.08, -0.10, -0.12, -0.14, -0.16],
    middle: [0.15, 0.04, 0.02, 0.01, 0, -0.01, -0.02, -0.03, -0.04, -0.05, -0.06, -0.07, -0.08],
    long: [-0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16]
  };
  const idx = barrier - 1;
  if (idx >= 0 && idx < 13) {
    return effectiveness[distClass][idx];
  }
  return 0;
}

// Optional: fetch news sentiment for a horse name via Brave search
// Returns a small boost (0-0.05) if recent positive mentions found; otherwise 0.
// This is a stub; actual implementation would require a search API call and NLP. Since we have Brave search, we could do it, but for now it's a placeholder.
async function fetchNewsBoost(horseName) {
  // Placeholder: return 0. Could be extended to use web_search skill if available.
  return 0;
}

// ── Enhanced form analysis helpers ──

// Compute recency-weighted form: recent finishes count more
// pastRuns is ordered oldest-first, last6run string is "rN/.../r2/r1" -> most recent last
function recencyWeightedAvg(pastRuns) {
  if (!pastRuns || pastRuns.length === 0) return null;
  let weightedSum = 0, weightTotal = 0;
  for (let i = 0; i < pastRuns.length; i++) {
    const weight = i + 1; // most recent gets highest weight
    weightedSum += pastRuns[i] * weight;
    weightTotal += weight;
  }
  return weightedSum / weightTotal;
}

// Trend: negative = improving (positions getting lower), positive = declining
function formTrend(pastRuns) {
  if (!pastRuns || pastRuns.length < 2) return 0;
  // Simple linear regression slope on finish positions
  const n = pastRuns.length;
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
  for (let i = 0; i < n; i++) {
    sumX += i;
    sumY += pastRuns[i];
    sumXY += i * pastRuns[i];
    sumX2 += i * i;
  }
  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  return slope; // negative = improving
}

// Consistency: coefficient of variation (lower = more consistent)
function formConsistency(pastRuns) {
  if (!pastRuns || pastRuns.length < 2) return null;
  const mean = pastRuns.reduce((a, b) => a + b, 0) / pastRuns.length;
  if (mean === 0) return null;
  const variance = pastRuns.reduce((sum, p) => sum + (p - mean) ** 2, 0) / pastRuns.length;
  const stdDev = Math.sqrt(variance);
  return stdDev / mean; // CV: lower = more consistent
}

// Last run finish (most recent)
function lastRunPos(pastRuns) {
  if (!pastRuns || pastRuns.length === 0) return null;
  return pastRuns[pastRuns.length - 1];
}

// Best finish in last 6
function bestFinish(pastRuns) {
  if (!pastRuns || pastRuns.length === 0) return null;
  return Math.min(...pastRuns);
}

// Win rate in last 6 (finishing 1st)
function winRate(pastRuns) {
  if (!pastRuns || pastRuns.length === 0) return 0;
  return pastRuns.filter(p => p === 1).length / pastRuns.length;
}

// Place rate (top 3) — for Quinella/Place pool context
function placeRate(pastRuns) {
  if (!pastRuns || pastRuns.length === 0) return 0;
  return pastRuns.filter(p => p <= 3).length / pastRuns.length;
}

function computeRecommendations(horses, options = {}) {
  const {
    advancedScoring = false,
    tjBonusWeight = 0.1,
    barrierBonusWeight = 0.12,
    raceDistance = null,
    newsBoost = false,
    lightWeightBonus = 0.05,
    formAnalysis = true  // NEW: enable enhanced form analysis
 } = options;

  // Split candidates: those with form data vs those without (debutants / no past runs)
  const withForm = horses.filter(h => h.winOdds != null && h.pastRuns && h.pastRuns.length > 0);
  const withoutForm = horses.filter(h => h.winOdds != null && (!h.pastRuns || h.pastRuns.length === 0));
  const candidates = [...withForm, ...withoutForm];
  if (candidates.length < 2) return [];

  // Compute implied probability from win odds (1/odds) and normalize to sum=1
  const implied = {};
  let sumImplied = 0;
  for (const h of candidates) {
    implied[h.horseName] = 1 / h.winOdds;
    sumImplied += implied[h.horseName];
  }
  for (const h of candidates) {
    implied[h.horseName] /= sumImplied;
  }

  // ── Enhanced form metrics ──
  const formAvg = {};
  const formWeightedAvg = {};
  const formTrendScore = {};
  const formConsistencyScore = {};
  const lastRun = {};
  const bestRun = {};
  const formWinRate = {};
  const formPlaceRate = {};

  // Populate for horses with form data
  for (const h of withForm) {
    formAvg[h.horseName] = h.pastRuns.reduce((a, b) => a + b, 0) / h.pastRuns.length;
    formWeightedAvg[h.horseName] = recencyWeightedAvg(h.pastRuns);
    formTrendScore[h.horseName] = formTrend(h.pastRuns);
    formConsistencyScore[h.horseName] = formConsistency(h.pastRuns);
    lastRun[h.horseName] = lastRunPos(h.pastRuns);
    bestRun[h.horseName] = bestFinish(h.pastRuns);
    formWinRate[h.horseName] = winRate(h.pastRuns);
    formPlaceRate[h.horseName] = placeRate(h.pastRuns);
  }

  // Normalize simple form avg to 0-1 (better form = higher score)
  const formScore = {};
  const allAvgs = withForm.map(h => formAvg[h.horseName]);
  const minAvg = allAvgs.length > 0 ? Math.min(...allAvgs) : 0;
  const maxAvg = allAvgs.length > 0 ? Math.max(...allAvgs) : 0;
  for (const h of withForm) {
    formScore[h.horseName] = (maxAvg === minAvg) ? 0.5 : 1 - (formAvg[h.horseName] - minAvg) / (maxAvg - minAvg);
  }

  // Normalize recency-weighted form
  const wtdFormScore = {};
  const allWtd = withForm.map(h => formWeightedAvg[h.horseName]);
  const minWtd = allWtd.length > 0 ? Math.min(...allWtd) : 0;
  const maxWtd = allWtd.length > 0 ? Math.max(...allWtd) : 0;
  for (const h of withForm) {
    wtdFormScore[h.horseName] = (maxWtd === minWtd) ? 0.5 : 1 - (formWeightedAvg[h.horseName] - minWtd) / (maxWtd - minWtd);
  }

  // Normalize trend (negative slope = improving = good)
  const trendScore = {};
  const allTrends = withForm.map(h => formTrendScore[h.horseName]);
  const minTrend = allTrends.length > 0 ? Math.min(...allTrends) : 0;
  const maxTrend = allTrends.length > 0 ? Math.max(...allTrends) : 0;
  for (const h of withForm) {
    // Invert: more negative trend (improving) -> higher score
    trendScore[h.horseName] = (maxTrend === minTrend) ? 0.5 : 1 - (formTrendScore[h.horseName] - minTrend) / (maxTrend - minTrend);
  }

  // Normalize consistency (lower CV = more consistent = better)
  const consistencyScore = {};
  const allCV = withForm.map(h => formConsistencyScore[h.horseName]).filter(v => v != null);
  const minCV = allCV.length > 0 ? Math.min(...allCV) : 0;
  const maxCV = allCV.length > 0 ? Math.max(...allCV) : 0;
  for (const h of withForm) {
    const cv = formConsistencyScore[h.horseName];
    if (cv == null) { consistencyScore[h.horseName] = 0.5; continue; }
    // Invert: lower CV -> higher score
    consistencyScore[h.horseName] = (maxCV === minCV) ? 0.5 : 1 - (cv - minCV) / (maxCV - minCV);
  }

  // ── Build combined form score ──
  // With form analysis: use weighted blend of recency, trend, consistency + base form
  // Without: use simple average (original behavior)
  const combinedFormScore = {};
  for (const h of withForm) {
    if (formAnalysis) {
      combinedFormScore[h.horseName] =
        0.35 * wtdFormScore[h.horseName] +   // recency-weighted form
        0.25 * formScore[h.horseName] +       // simple average form
        0.20 * trendScore[h.horseName] +      // improving or declining
        0.20 * consistencyScore[h.horseName]; // consistency
    } else {
      combinedFormScore[h.horseName] = formScore[h.horseName];
    }
  }

  // For horses without form (debutants), assign a neutral score
  for (const h of withoutForm) {
    combinedFormScore[h.horseName] = 0.3; // slightly below average — unknown quantity
  }

  // Base combined score: 0.6 implied, 0.4 form
  const scores = {};
  for (const h of candidates) {
    let score = 0.6 * implied[h.horseName] + 0.4 * combinedFormScore[h.horseName];
    scores[h.horseName] = { score, reasons: {} };
  }

  // ── Advanced scoring ──
  if (advancedScoring) {
    // 1) Trainer/Jockey bonus: both top-tier
    for (const h of candidates) {
      const isTopJockey = h.jockey && TOP_JOCKEYS.has(h.jockey);
      const isTopTrainer = h.trainer && TOP_TRAINERS.has(h.trainer);
      if (isTopJockey && isTopTrainer) {
        scores[h.horseName].score += tjBonusWeight;
        scores[h.horseName].reasons.tj = true;
      }
    }
    // 1b) Jockey penalty: below-average jockeys
    const BAD_JOCKEYS = new Set(['A. Basel']);
    for (const h of candidates) {
      if (h.jockey && BAD_JOCKEYS.has(h.jockey)) {
        scores[h.horseName].score -= 0.018;
        scores[h.horseName].reasons.badJockey = true;
      }
    }
    // 2) Barrier effectiveness by distance
    if (raceDistance != null) {
      for (const h of candidates) {
        const bEff = barrierEffectiveness(h.barrier, raceDistance);
        const bonus = bEff * barrierBonusWeight;
        if (Math.abs(bonus) > 0.001) {
          scores[h.horseName].score += bonus;
          scores[h.horseName].reasons.barrier = bonus;
        }
      }
    }
    // 3) Weight penalty: above‑average weight costs a little
    const weights = candidates.map(h => h.weight).filter(w => w != null);
    if (weights.length > 0) {
      const avgWeight = weights.reduce((a, b) => a + b, 0) / weights.length;
      for (const h of candidates) {
        if (h.weight && h.weight > avgWeight + 2) {
          const penalty = (h.weight - avgWeight) * 0.005; // 0.5% per lb above avg+2
          scores[h.horseName].score -= penalty;
          scores[h.horseName].reasons.weight = -(penalty);
        }
      }
    }
    // 4) Light weight bonus: reward horses under 120lb
    for (const h of candidates) {
      if (h.weight && h.weight < 120) {
        scores[h.horseName].score += lightWeightBonus;
        scores[h.horseName].reasons.lightWeight = true;
      }
    }
  }

  // ── Helper functions for form analysis ──

  // Count consecutive placed runs (top 3) from most recent
  // pastRuns is oldest-first, so we traverse from the end
  function consecutivePlacedRuns(pastRuns) {
    if (!pastRuns || pastRuns.length === 0) return 0;
    let count = 0;
    for (let i = pastRuns.length - 1; i >= 0; i--) {
      if (pastRuns[i] <= 3) count++;
      else break;
    }
    return count;
  }

  // Check if horse finished 4th-5th last after peak form (bounce-back candidate)
  function isBounceBack(pastRuns) {
    if (!pastRuns || pastRuns.length < 3) return false;
    const last = pastRuns[pastRuns.length - 1];
    const prev = pastRuns[pastRuns.length - 2];
    const prev2 = pastRuns[pastRuns.length - 3];
    return (last === 4 || last === 5) && prev <= 3 && prev2 <= 3;
  }

  // ── Peak penalty: last-start winner without sustained form ──
  // A horse that won last start after 6+ runs is often peaking, not sustaining
  for (const h of withForm) {
    const lr = lastRun[h.horseName];
    if (lr === 1 && h.pastRuns.length >= 6) {
      const consec = consecutivePlacedRuns(h.pastRuns);
      if (consec < 3) {
        scores[h.horseName].score -= 0.04;
        scores[h.horseName].reasons.peakPenalty = true;
      }
    }
  }

  // ── Form analysis bonus/penalty (separate from advancedScoring) ──
  if (formAnalysis) {
    for (const h of withForm) {
      const trend = formTrendScore[h.horseName];
      // Bounce-back bonus: 4th-5th last after peak form
      if (isBounceBack(h.pastRuns)) {
        scores[h.horseName].score += 0.03;
        scores[h.horseName].reasons.bounceBack = true;
      }
      // Improving form bonus: trend slope < -0.3 (positions dropping meaningfully)
      if (trend < -0.3) {
        scores[h.horseName].score += 0.03;
        scores[h.horseName].reasons.formTrend = 'improving';
      }
      // Declining form penalty: trend slope > 0.5
      if (trend > 0.5) {
        scores[h.horseName].score -= 0.02;
        scores[h.horseName].reasons.formTrend = 'declining';
      }
      // Consistency bonus: very consistent (CV < 0.4)
      const cv = formConsistencyScore[h.horseName];
      if (cv != null && cv < 0.4) {
        scores[h.horseName].score += 0.02;
        scores[h.horseName].reasons.consistent = true;
      }
    }
  }

  // Normalize final scores to sum to 1
  let sumScores = 0;
  for (const name of Object.keys(scores)) {
    sumScores += scores[name].score;
  }
  const estimatedProb = {};
  for (const name of Object.keys(scores)) {
    estimatedProb[name] = scores[name].score / sumScores;
  }

  // Rank and take top 4
  const ranked = candidates
    .map(h => ({ horse: h, prob: estimatedProb[h.horseName], reasons: scores[h.horseName].reasons }))
    .sort((a, b) => b.prob - a.prob)
    .slice(0, 4);

  // ── QP ranking: prioritize place rate + consistency over win prob ──
  // Only consider horses with at least 3 past runs (need enough data to trust place rate)
  const qpWithForm = withForm.filter(h => h.pastRuns.length >= 3);
  const qpRanked = (qpWithForm.length >= 2 ? qpWithForm : withForm)
    .map(h => {
      let qpScore = 0;
      // 35% place rate (top 3 finishes) — most important for QP
      const pr = formPlaceRate[h.horseName] || 0;
      qpScore += 0.35 * pr;
      // 25% consistency (inverted CV — lower is more reliable)
      const cv = formConsistencyScore[h.horseName];
      qpScore += 0.25 * (cv != null ? (1 - Math.min(cv, 1)) : 0.3);
      // 20% recency-weighted form
      qpScore += 0.20 * (wtdFormScore[h.horseName] || 0.5);
      // 10% odds value (modest — don't chase crazy longshots)
      const placeOdds = h.placeOdds || h.winOdds;
      const valueRatio = placeOdds ? Math.min(placeOdds / 30, 0.7) : 0.3;
      qpScore += 0.10 * valueRatio;
      // 10% form trend (improving = better)
      qpScore += 0.10 * (trendScore[h.horseName] || 0.5);
      return { horse: h, qpScore, placeRate: pr };
    })
    .sort((a, b) => {
      // Primary: QP score. Tiebreak: higher place rate, then shorter odds (more reliable)
      if (Math.abs(b.qpScore - a.qpScore) > 0.01) return b.qpScore - a.qpScore;
      if (Math.abs(b.placeRate - a.placeRate) > 0.05) return b.placeRate - a.placeRate;
      return a.winOdds - b.winOdds;
    })
    .slice(0, 4);

  const qpPair = qpRanked.length >= 2
    ? [qpRanked[0].horse, qpRanked[1].horse]
    : ranked.slice(0, 2).map(r => r.horse);

  // Build win recommendations (original behavior)
  const recommendations = ranked.map(r => {
    const h = r.horse;
    const probPercent = (r.prob * 100).toFixed(1);
    let reason = `${PHRASES.winOdds} ${h.winOdds}`;
    if (h.barrier) reason += `; ${PHRASES.barrier} ${h.barrier}`;
    if (h.weight) reason += `; ${PHRASES.weight} ${h.weight}`;

    // Form detail
    if (formAvg[h.horseName] != null) {
      const avgPos = formAvg[h.horseName].toFixed(1);
      reason += `; avg ${avgPos} over ${h.pastRuns.length} runs`;
      // Add trend arrow
      if (r.reasons.formTrend === 'improving') reason += ' ↑ trending up';
      else if (r.reasons.formTrend === 'declining') reason += ' ↓ fading';
      // Add last run
      if (lastRun[h.horseName] != null) reason += `; last: ${lastRun[h.horseName]}`;
      // Add place rate
      const pr = formPlaceRate[h.horseName];
      if (pr != null) reason += `; place rate ${(pr*100).toFixed(0)}%`;
    } else {
      reason += `; debut — no past form`;
    }

    if (h.gear && h.gear.length > 0) {
      reason += `; ${PHRASES.gear}: ${h.gear.join('/')}`;
    }

    // Advanced/form analysis tags
    if (r.reasons) {
      if (r.reasons.tj) {
        reason += `; TJ bonus +${(tjBonusWeight*100).toFixed(1)}%`;
      }
      if (r.reasons.barrier) {
        const b = r.reasons.barrier;
        reason += `; Barrier ${b >= 0 ? '+' : ''}${(b*100).toFixed(1)}%`;
      }
      if (r.reasons.weight) {
        const w = r.reasons.weight;
        reason += `; Weight${w >= 0 ? '+' : ''}${(w*100).toFixed(1)}%`;
      }
      if (r.reasons.lightWeight) {
        reason += `; Light weight +${(lightWeightBonus*100).toFixed(1)}%`;
      }
      if (r.reasons.lastWin) {
        reason += `; WON last start`;
      }
      if (r.reasons.consistent) {
        reason += `; consistent form`;
      }
    }

    return {
      horseName: h.horseName,
      reason,
      winProbability: parseFloat(probPercent)
    };
  });

  return {
    recommendations,
    qpPair: qpPair.map(h => ({ horseNo: h.horseNo, horseName: h.horseName, winOdds: h.winOdds, placeOdds: h.placeOdds }))
  };
}

async function fetchRaceCard(params = {}) {
  const { date, classFilter = [], excludeHorseNos = [], excludeBarriers = [], raceNo, advancedScoring = false, tjBonusWeight = 0.15, barrierBonusWeight = 0.12, newsBoost = false, lightWeightBonus = 0.05,    formAnalysis = true } = params;
  const targetDate = date || getTodayHKT();

  const cacheKey = makeCacheKey({ date: targetDate, classFilter, excludeHorseNos, excludeBarriers, raceNo, advancedScoring, newsBoost, lightWeightBonus });
  const cached = cache.get(cacheKey);
  if (cached && (Date.now() - cached.timestamp < 15 * 60 * 1000)) {
    return cached.data;
  }

  // Enforce rate limit on fresh fetches
  const now = Date.now();
  if (now - lastApiCall < RATE_LIMIT_MS) {
    const waitMs = RATE_LIMIT_MS - (now - lastApiCall);
    await new Promise(resolve => setTimeout(resolve, waitMs));
  }
  lastApiCall = Date.now();

  const horseAPI = new HorseRacingAPI();

  try {
    const allMeetings = await horseAPI.getAllRaces();

    // Filter meetings by date (API returns string date)
    const filteredMeetings = allMeetings.filter(m => m.date === targetDate);

    const result = {
      meeting: null,
      races: [],
      source: 'hkjc-api',
      timestamp: new Date().toISOString()
    };

    if (filteredMeetings.length === 0) {
      cache.set(cacheKey, { data: result, timestamp: Date.now() });
      return result;
    }

    // Use the first meeting for overall meeting info (venue, date)
    const firstMeeting = filteredMeetings[0];
    const venueCode = firstMeeting.venueCode || (firstMeeting.races?.[0]?.raceCourse) || 'Unknown';
    result.meeting = {
      venue: venueCode,
      date: targetDate,
      weather: null,
      trackCondition: null
    };

    // Collect all races from all meetings on this date
    const allRaces = [];
    for (const m of filteredMeetings) {
      allRaces.push(...(m.races || []));
    }

    for (const race of allRaces) {
      // Apply class filter if any
      if (classFilter.length > 0) {
        const raceClass = (race.raceClass_en || '').toLowerCase();
        const matches = classFilter.some(cls => raceClass.includes(cls.toLowerCase()));
        if (!matches) continue;
      }

      // Fetch odds for this race
      let oddsMap = {}; // { '01': {WIN: '14', PLA: '5.8'}, ... }
      try {
        const raceNumber = race.no ? parseInt(race.no, 10) : 1;
        const oddsResult = await horseAPI.getRaceOdds(raceNumber, ['WIN', 'PLA']);
        for (const oddsNode of oddsResult) {
          const type = oddsNode.oddsType; // 'WIN' or 'PLA'
          for (const node of oddsNode.oddsNodes) {
            const key = node.combString; // padded horse number string
            if (!oddsMap[key]) oddsMap[key] = {};
            oddsMap[key][type] = node.oddsValue;
          }
        }
      } catch (err) {
        console.warn(`Failed to fetch odds for race ${race.no}:`, err.message);
      }

      // Map runners to horse objects (English only)
      let horses = (race.runners || []).map(runner => {
        const barrier = runner.barrierDrawNumber ? parseInt(runner.barrierDrawNumber, 10) : null;
        const horseNo = runner.no ? parseInt(runner.no, 10) : null;
        const horseName = runner.name_en || '(no English name)';
        const horseId = runner.horse?.id || runner.id || null;
        const handicapWeight = runner.handicapWeight ? parseInt(runner.handicapWeight, 10) : null;

        let jockeyName = null;
        if (runner.jockey) {
          jockeyName = runner.jockey.name_en || '(no English name)';
        }

        let trainerName = null;
        if (runner.trainer) {
          trainerName = runner.trainer.name_en || '(no English name)';
        }

        const allowanceRaw = runner.allowance;
        let jockeyAllowance = null;
        if (allowanceRaw && allowanceRaw.trim() !== '') {
          jockeyAllowance = parseInt(allowanceRaw.trim(), 10);
          if (isNaN(jockeyAllowance)) jockeyAllowance = null;
        }

        // Past runs: last6run string like '4/1/1/2/6/6' — NEWEST first, oldest last
        // Reverse so pastRuns[0] = oldest, pastRuns[last] = most recent
        let pastRuns = [];
        if (runner.last6run) {
          pastRuns = runner.last6run.split('/').map(p => parseInt(p, 10)).filter(n => !isNaN(n)).reverse();
        }

        // Gear: gearInfo string like 'B/TT'
        let gear = [];
        if (runner.gearInfo) {
          gear = runner.gearInfo.split('/').map(s => s.trim()).filter(Boolean);
        }

        // Odds lookup
        const oddsKey = horseNo ? padNumber(horseNo) : null;
        const oddsEntry = oddsKey && oddsMap[oddsKey] ? oddsMap[oddsKey] : {};
        const winOdds = oddsEntry.WIN ? parseFloat(oddsEntry.WIN) : null;
        const placeOdds = oddsEntry.PLA ? parseFloat(oddsEntry.PLA) : null;

        return {
          barrier,
          horseNo,
          horseName,
          horseId,
          weight: handicapWeight,
          jockey: jockeyName,
          jockeyAllowance,
          trainer: trainerName,
          pastRuns,
          gear,
          winOdds,
          placeOdds
        };
      });

      // Apply exclusions
      if (excludeHorseNos.length > 0) {
        horses = horses.filter(h => !excludeHorseNos.includes(h.horseNo));
      }
      if (excludeBarriers.length > 0) {
        horses = horses.filter(h => !excludeBarriers.includes(h.barrier));
      }

      // Filter out SB horses (missing critical data)
      horses = horses.filter(h => h.horseNo != null && h.barrier != null);

      const recs = computeRecommendations(horses, {
        advancedScoring,
        tjBonusWeight,
        barrierBonusWeight,
        raceDistance: race.distance || null,
        newsBoost,
        lightWeightBonus,
        formAnalysis
      });

      // Class and going (English only)
      const raceClass = race.raceClass_en || null;
      const going = race.go_en || null;
      if (!result.meeting.trackCondition && going) {
        result.meeting.trackCondition = going;
      }

      result.races.push({
        raceNo: race.no ? parseInt(race.no, 10) : null,
        distance: race.distance || null,
        class: raceClass,
        going: going,
        horses,
        ...recs
      });
    }

    cache.set(cacheKey, { data: result, timestamp: Date.now() });
    return result;
  } catch (error) {
    console.error('HKJC fetchRaceCard error:', error);
    throw error;
  }
}

module.exports = {
  tools: {
    fetchRaceCard
  }
};