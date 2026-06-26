'use strict';

const CATEGORY_GROUPS = {
  visual: [
    'image_generation','illustration','art','drawing','design',
    'graphic','graphic_design','photo','photography','animation',
    'video','render','rendering','concept_art','sketch','painting',
    'anime','digital_art','character','character_design','webtoon',
    'manhwa','manga','portrait','thumbnail','banner','logo',
    'icon','sprite','texture','storyboard','realistic','photorealistic'
  ],
  writing: [
    'copywriting','writing','content','blog','article',
    'editing','proofreading','storytelling','script','scriptwriting',
    'social_media','marketing_copy','ux_writing','caption','tagline',
    'newsletter','press_release','resume','cover_letter'
  ],
  translation: [
    'translation','translate','localization','l10n','i18n',
    'subtitling','subtitle','dubbing'
  ],
  code: [
    'code','coding','programming','development','software',
    'web','app','backend','frontend','fullstack','api',
    'automation','script','bot','plugin','debugging','refactor'
  ],
  data: [
    'data_analysis','data','analysis','research','statistics',
    'excel','spreadsheet','reporting','visualization','dashboard',
    'scraping','crawling','survey'
  ]
};

function getGroup(token) {
  const n = token.toLowerCase().replace(/[-\s]/g, '_');
  for (const [group, aliases] of Object.entries(CATEGORY_GROUPS)) {
    if (aliases.includes(n)) return group;
    if (aliases.some(a => a.includes(n) || n.includes(a))) return group;
  }
  return null;
}

function tokenize(cat) {
  return cat.toLowerCase().replace(/[-\s]/g, '_').split('_').filter(t => t.length > 2);
}

function calcMatch(jobCategory, capabilities) {
  const groups    = Object.keys(capabilities).filter(k => k !== 'default');
  const jobNorm   = jobCategory.toLowerCase().replace(/[-\s]/g, '_');
  const jobTokens = tokenize(jobCategory);
  const allAliases = groups.flatMap(g => CATEGORY_GROUPS[g] || []);

  if (allAliases.includes(jobNorm)) {
    return { score: 100, label: 'Exact match', group: getGroup(jobNorm) };
  }

  const jobGroup = getGroup(jobNorm);
  if (jobGroup && groups.includes(jobGroup)) {
    return { score: 80, label: `Same domain (${jobGroup})`, group: jobGroup };
  }

  for (const token of jobTokens) {
    const tokenGroup = getGroup(token);
    if (tokenGroup && groups.includes(tokenGroup)) {
      return { score: 50, label: `Partial match — "${token}" in ${tokenGroup}`, group: tokenGroup };
    }
  }

  if (capabilities.default) {
    return { score: 30, label: 'No direct match — using default executor', group: 'default' };
  }

  return { score: 0, label: 'No overlap', group: null };
}

function outlook(score) {
  if (score === 100) return '✅ Exact specialty';
  if (score >= 80)   return '🟡 Same domain';
  if (score >= 50)   return '🟠 Partial match';
  if (score >= 30)   return '⚪ Default executor';
  return '❌ Outside skill set';
}

module.exports = { CATEGORY_GROUPS, getGroup, tokenize, calcMatch, outlook };
