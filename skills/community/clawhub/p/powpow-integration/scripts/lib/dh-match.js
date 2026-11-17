/**
 * Shared digital-human matching: health filtering + topic relevance ranking.
 * Used by BOTH match-digital-human.js (top-N suggestions) and compose.js
 * (--dh auto) - the two must never drift apart, which is why this lives in
 * lib/ instead of being duplicated per script.
 */

const TEST_NAME_PATTERN = /(测试|test)/i;
const PLACEHOLDER_AVATAR_PATTERN = /default-avatar\.(png|jpg)/i;

// Common 学-suffix discipline terms. A topic keyword that is the SUFFIX of a
// longer discipline term would otherwise match ACROSS the morpheme boundary:
// keyword 文学 (literature) matching 天文学家 (astronomer) inside every
// astronomer's description, drowning the real writers in a ranking that is
// then re-shuffled on every call. Before matching, discipline terms that END
// with the keyword are masked out of the text. Prefix hits stay valid:
// keyword 天文 still finds 天文学家, keyword 天文学 still matches in full.
const DISCIPLINE_TERMS = [
  '天文学', '水文学', '地理学', '地质学', '物理学', '化学', '生物学', '生态学',
  '气象学', '海洋学', '考古学', '历史学', '人类学', '社会学', '语言学', '心理学',
  '经济学', '政治学', '统计学', '数学', '医学', '药学', '法学', '哲学', '文学',
  '美学', '伦理学', '逻辑学', '宗教学', '民族学', '教育学', '军事学', '工程学',
  '建筑学', '艺术学', '音乐学', '农学', '林学', '光学', '力学',
];

function isHealthy(dh) {
  if (!dh.isActive) return false;
  if (!dh.name || TEST_NAME_PATTERN.test(dh.name) || dh.name.includes('\uFFFD')) return false;
  if (!dh.avatarUrl || PLACEHOLDER_AVATAR_PATTERN.test(dh.avatarUrl)) return false;
  return true;
}

function maskCrossBoundary(text, keyword) {
  let masked = text;
  for (const t of DISCIPLINE_TERMS) {
    if (t !== keyword && t.endsWith(keyword)) {
      masked = masked.split(t).join('\u0000');
    }
  }
  return masked;
}

/**
 * Topic relevance, 0 = unrelated. Weights:
 * - keyword hit in the NAME: +3 (searching a person's name must always rank
 *   that person first, ahead of any description text match)
 * - keyword hit in description / location: +1 (weak evidence - descriptions
 *   are often template text)
 * A keyword counts at most once per digital human.
 */
function relevance(dh, topic) {
  const words = topic.toLowerCase().split(/[^a-z\u4e00-\u9fff]+/).filter(w => w.length > 1);
  const name = (dh.name || '').toLowerCase();
  const descLoc = `${dh.description || ''} ${dh.locationName || ''}`.toLowerCase();
  let score = 0;
  for (const w of words) {
    if (name.includes(w)) { score += 3; continue; }
    if (maskCrossBoundary(descLoc, w).includes(w)) score += 1;
  }
  return score;
}

/**
 * Deterministic ranking: score desc, ties broken by name so equal-score
 * candidates keep a stable order across calls (the old comparison sort let
 * API return order decide, which read as random shuffling to the user).
 */
function rankByTopic(digitalHumans, topic) {
  return digitalHumans
    .filter(isHealthy)
    .map(dh => ({ dh, score: relevance(dh, topic) }))
    .sort((a, b) => b.score - a.score || a.dh.name.localeCompare(b.dh.name, 'zh'));
}

module.exports = { isHealthy, relevance, rankByTopic, DISCIPLINE_TERMS };
