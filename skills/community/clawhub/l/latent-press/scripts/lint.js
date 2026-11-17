#!/usr/bin/env node
// Usage: node lint.js chapter-3.md [--strict]
//
// Flags the prose patterns readers use to spot machine-written fiction. Warns, never
// rewrites. Exit 1 only with --strict and at least one flag. English-only for the
// phrase checks; structural checks run on any language.

const fs = require('fs');

const STOCK_PHRASES = [
  'took a deep breath', 'taking a deep breath', 'let out a breath', "didn't know he was holding",
  "didn't know she was holding", 'voice barely above a whisper', 'barely a whisper', 'barely audible',
  "couldn't help but", "couldn't shake the feeling", 'could not shake the feeling', 'casting long shadows',
  'sun dipped below the horizon', 'sun hung low', 'hung low in the sky', 'felt a chill', 'shiver down',
  'shiver run', 'chill run', 'air was thick with', 'air thick with', 'air hung thick', 'hung heavy in the air',
  'hung in the air', 'words hung', 'felt like an eternity', 'heart pounding', 'heart pounded', 'heart hammered',
  'heart raced', 'heart racing', 'heart skipped a beat', 'room fell silent', 'silence stretched',
  'something else entirely', 'brow furrowed', 'furrowed brow', 'smile playing on', 'smile tugging',
  'days turned into weeks', 'growing sense of', 'renewed sense of purpose', 'newfound sense of',
  'sense of purpose', 'sense of unease', 'sense of dread', 'spread like wildfire', 'dust motes',
  'emerged from the shadows', 'blood ran cold', 'piercing blue eyes', 'eyes widened', 'eyes narrowed',
  'eyes darting', 'eyes scanning', 'eyes locked', 'swallowed hard', 'steeling himself', 'steeling herself',
  'for the first time in a long time', 'knew one thing', 'one thing was certain', 'mind racing', 'mind raced',
  'in that moment', 'little did', 'the world around', 'found herself', 'found himself', 'it was as if',
  'as if on cue', 'a testament to', 'tapestry', 'delve', 'in the heart of', 'nestled', 'stark contrast',
  'almost imperceptible', 'constant reminder', 'glimmer of hope', 'flicker of something', 'a mixture of',
  'the weight of it', 'the weight of the', 'unspoken', 'palpable', 'visceral', 'unbidden', 'tendrils',
  'thrumming', 'thrummed', 'the hum of', 'ozone', 'liminal', 'susurrus', 'ministrations', 'a beat passed',
  'let that sink in', 'whatever came next', 'would never be the same', 'only the beginning',
  'the beginning of something', 'a problem for tomorrow', 'somewhere in the distance', 'somewhere, a',
  'the silence was deafening', 'deafening silence', 'time seemed to slow', 'time stood still',
  'a wave of', 'a surge of', 'a pang of', 'a jolt of', 'washed over', 'coursed through', 'crashed over',
  'breath caught', 'caught in her throat', 'caught in his throat', 'fingers flying across', 'raised a hand, silencing',
  'seen anything like', 'unlike anything', 'never seen anything', 'intricately carved', 'weathered face',
  'said, his voice', 'said, her voice', 'asked, his voice', 'asked, her voice', 'whispered, her voice',
  'whispered, his voice', 'voice low', 'voice steady', 'voice trembling', 'voice laced', 'voice tinged',
  'voice dripping', 'voice filled', 'voice a low', 'voice cracked', 'a low rumble',
];

const EMOTION_NAMING = /\b(?:felt|feel|feeling|filled with|overcome with|overwhelmed by|consumed by)\s+(?:a\s+|an\s+|the\s+)?(?:deep|sudden|overwhelming|profound|strange|growing|quiet|familiar|cold|hot|sharp|dull)?\s*(?:sense of\s+)?(?:sadness|sorrow|fear|dread|terror|relief|joy|anger|rage|fury|guilt|shame|hope|hopelessness|unease|panic|grief|longing|warmth|calm|peace|excitement|anxiety|nervousness|frustration|disappointment|confusion|determination|resolve|pride|loneliness|happiness|despair|regret|envy|jealousy|gratitude|tenderness|helplessness|emptiness|numbness)\b/gi;

const CONTRAST_PATTERNS = [
  /\b(?:not|isn't|wasn't|weren't|aren't|never|no longer)\b[^.!?;\n]{2,60}?,?\s+but\b/gi,
  /\bnot (?:just|only|merely|simply|because)\b[^.!?\n]{2,60}/gi,
  /\b(?:it|this|that|she|he|they|there)\s+(?:wasn't|isn't|weren't|aren't|was not|is not|were not)\b[^.!?\n]{2,60}[.;]\s+(?:it|this|that|she|he|they|there)\s+(?:was|is|were|are)\b/gi,
  /\b(?:less|more)\s+(?:a|an)\s+\w+\s+than\s+(?:a|an)\b/gi,
];

const CLOSING_STATEMENTS = [
  /\b(?:for the first time|would never be the same|only the beginning|the beginning of|whatever came next|whatever (?:tomorrow|the future) (?:held|brought))\b/i,
  /\b(?:she|he|they|i) (?:knew|understood|realized|realised) (?:then|now|that|what|it)\b/i,
  /\b(?:and )?(?:somewhere|somehow|for now|tomorrow|tonight),?\s/i,
  /\b(?:a problem for|that was enough|it was enough|that would have to be enough|had to be enough)\b/i,
  /\b(?:the (?:story|night|journey|work|fight) (?:was|is) (?:far from|not) over)\b/i,
  /\bin that moment\b/i,
];

const EM_DASH_LIMIT = 2;
const CONTRAST_LIMIT = 1;

function words(text) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function latinShare(text) {
  const letters = text.match(/\p{L}/gu) || [];
  if (!letters.length) return 0;
  const latin = text.match(/\p{Script=Latin}/gu) || [];
  return latin.length / letters.length;
}

function lineOf(text, index) {
  return text.slice(0, index).split('\n').length;
}

function findAll(text, re) {
  const hits = [];
  const flags = re.flags.includes('g') ? re.flags : re.flags + 'g';
  const global = new RegExp(re.source, flags);
  let m;
  while ((m = global.exec(text)) !== null) {
    hits.push({ line: lineOf(text, m.index), index: m.index, match: m[0].replace(/\s+/g, ' ').trim() });
    if (m.index === global.lastIndex) global.lastIndex++;
  }
  return hits;
}

function context(text, at, length) {
  return text.slice(Math.max(0, at - 30), at + length + 30).replace(/\s+/g, ' ').trim();
}

function lastParagraph(text) {
  const paragraphs = text.trim().split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
  return paragraphs[paragraphs.length - 1] || '';
}

function lint(text) {
  const findings = [];
  const wordCount = words(text);
  const english = latinShare(text) > 0.6;

  const dashes = findAll(text, /——|—|–|\s--\s/g).map((h) => ({ ...h, match: context(text, h.index, h.match.length) }));
  if (dashes.length > EM_DASH_LIMIT) {
    findings.push({
      rule: 'em-dashes',
      message: `${dashes.length} dashes, limit ${EM_DASH_LIMIT} per chapter. Use a comma or a full stop.`,
      hits: dashes.slice(0, 5),
    });
  }

  const contrasts = CONTRAST_PATTERNS.flatMap((re) => findAll(text, re));
  if (contrasts.length > CONTRAST_LIMIT) {
    findings.push({
      rule: 'not-x-but-y',
      message: `${contrasts.length} "not X, but Y" constructions. Say the thing that is true and stop.`,
      hits: contrasts.slice(0, 8),
    });
  }

  if (english) {
    const emotions = findAll(text, EMOTION_NAMING);
    if (emotions.length) {
      findings.push({
        rule: 'named-emotion',
        message: `${emotions.length} named emotions. Show what the body or the room does instead.`,
        hits: emotions.slice(0, 8),
      });
    }

    const lower = text.toLowerCase();
    const stock = STOCK_PHRASES.flatMap((phrase) => {
      const hits = [];
      let from = 0;
      while (true) {
        const at = lower.indexOf(phrase, from);
        if (at < 0) break;
        hits.push({ line: lineOf(text, at), match: phrase });
        from = at + phrase.length;
      }
      return hits;
    });
    if (stock.length) {
      findings.push({
        rule: 'stock-phrase',
        message: `${stock.length} stock phrases that machine prose over-uses. Replace each with something only this scene could produce.`,
        hits: stock.slice(0, 12),
      });
    }

    const closing = lastParagraph(text);
    const closer = CLOSING_STATEMENTS.find((re) => re.test(closing));
    if (closer) {
      findings.push({
        rule: 'closing-statement',
        message: 'The last paragraph reads as a summary or a moral. End on an open question, a reversal or an image, and cut the wrap-up.',
        hits: [{ line: lineOf(text, text.lastIndexOf(closing.slice(0, 40))), match: closing.slice(0, 120) }],
      });
    }
  }

  return { wordCount, english, findings };
}

function format({ wordCount, english, findings }) {
  const lines = [];
  lines.push(`[lint] ${wordCount} words${english ? '' : ' (non-Latin text: phrase checks skipped)'}`);
  if (!findings.length) {
    lines.push('[lint] clean');
    return lines.join('\n');
  }
  for (const f of findings) {
    lines.push(`[lint] ${f.rule}: ${f.message}`);
    for (const h of f.hits) lines.push(`         line ${h.line}: ${h.match}`);
  }
  const total = findings.reduce((n, f) => n + f.hits.length, 0);
  lines.push(`[lint] ${total} flags in ${findings.length} rules. Fix them before you upload.`);
  return lines.join('\n');
}

module.exports = { lint, format };

if (require.main === module) {
  const args = process.argv.slice(2);
  const strict = args.includes('--strict');
  const file = args.find((a) => !a.startsWith('--'));
  if (!file || args.includes('--help')) {
    console.log('Usage: node lint.js chapter-3.md [--strict]');
    process.exit(file ? 0 : 1);
  }
  if (!fs.existsSync(file)) {
    console.error(`No such file: ${file}`);
    process.exit(1);
  }
  const result = lint(fs.readFileSync(file, 'utf8'));
  console.log(format(result));
  if (strict && result.findings.length) process.exit(1);
}
