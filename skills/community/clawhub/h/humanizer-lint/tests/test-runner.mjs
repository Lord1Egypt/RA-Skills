import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';

const projectRoot = '..';
const projectModule = (...segments) => new URL([projectRoot, ...segments].join('/'), import.meta.url);
const { sanitizeMarkdown } = await import(projectModule('scripts', 'utils', 'sanitizer.mjs'));
const { isCJKText, normalizeLocale, tokenizeText, tokenizeWords } = await import(projectModule('scripts', 'utils', 'tokenizer.mjs'));
const {
  adjacentDelta,
  compressionRatio,
  coefficientOfVariation,
  mattr,
  mean,
  standardDeviation,
} = await import(projectModule('scripts', 'utils', 'metrics.mjs'));
const { analyzeText, runAnalyzeCli } = await import(projectModule('scripts', 'analyze.mjs'));
const { createBrowserAnalyzer } = await import(projectModule('demo', 'analyzer-browser.mjs'));
const { I18N } = await import(projectModule('demo', 'i18n.mjs'));
const { fingerprintSamples, runFingerprintCli } = await import(projectModule('scripts', 'fingerprint.mjs'));

let rootPath = decodeURIComponent(projectModule().pathname);
if (/^\/[A-Za-z]:/.test(rootPath)) rootPath = rootPath.slice(1);
const root = path.resolve(rootPath);
const fixture = async (name) => readFile(path.join(root, 'tests', 'fixtures', name), 'utf8');
const sourceFile = async (...segments) => (await readFile(path.join(root, ...segments), 'utf8')).replaceAll(String.fromCharCode(13), '');
async function sourceMjsFiles(directory = root) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (!['.git', '.pages-dist', '.wrangler', 'node_modules'].includes(entry.name)) files.push(...await sourceMjsFiles(path.join(directory, entry.name)));
    } else if (entry.name.endsWith('.mjs')) {
      files.push(path.join(directory, entry.name));
    }
  }
  return files;
}
const browserParityAvailable = (() => {
  try {
    return typeof CompressionStream === 'function' && Boolean(new CompressionStream('deflate-raw'));
  } catch {
    return false;
  }
})();

test('source modules avoid literal parent-path strings', async () => {
  const files = await sourceMjsFiles();
  assert.ok(files.length > 0);
  for (const file of files) assert.doesNotMatch(await readFile(file, 'utf8'), /\.\.\//, file);
});

test('sanitizer removes non-prose and preserves prose paragraphs', () => {
  const input = `---\ntitle: Sample\n---\n# Heading\n\nA real sentence has enough words to remain here.\n\n\`inline code\` and https://example.com/a?q=1 remain entities.\n\n\`\`\`js\nconst ignored = 'Tidak dapat dipungkiri';\n\`\`\`\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n- fragment only\n- This list item contains a complete sentence with enough words.\n`;
  const output = sanitizeMarkdown(input);
  assert.doesNotMatch(output, /title: Sample|Heading|ignored|\| A \|/);
  assert.match(output, /A real sentence/);
  assert.match(output, /TOKEN_ENTITY and TOKEN_ENTITY remain entities/);
  assert.doesNotMatch(output, /fragment only/);
  assert.match(output, /This list item contains a complete sentence/);
});

test('sanitizer preserves URL punctuation and complete wrapped list prose', () => {
  const output = sanitizeMarkdown('- This complete list item wraps onto\n  a second line and ends with punctuation.\n\nRead the [annual report](https://example.com/report). See https://example.com/docs. Then continue.\n\n| A | B |   ');
  assert.match(output, /This complete list item wraps onto a second line and ends with punctuation\./);
  assert.match(output, /Read the annual report\./);
  assert.doesNotMatch(output, /\[annual report\]|TOKEN_ENTITY\)/);
  assert.match(output, /See TOKEN_ENTITY\. Then continue\./);
  assert.doesNotMatch(output, /\| A \|/);
});

test('tokenizer protects abbreviations, casing, quotes, and brackets', () => {
  const result = tokenizeText('Dr. Rina berkata, "Saya setuju." Mereka pun pergi. Mr. Cole left (quickly.) Everyone noticed.', 'auto');
  assert.equal(result.sentences.length, 4);
  assert.match(result.sentences[0].text, /^Dr\./);
  assert.deepEqual(result.sentences.map((sentence) => sentence.paragraphIndex), [1, 1, 1, 1]);
});

test('tokenizer preserves reduplication and protects decimals and ellipses', () => {
  const result = tokenizeText('Anak-anak membaca undang-undang itu... Nilainya 3.5 persen. Biayanya Rp 10.000 sekarang.', 'id');
  assert.deepEqual(result.sentences[0].words.slice(0, 4), ['anak-anak', 'membaca', 'undang-undang', 'itu']);
  assert.equal(result.sentences.length, 2);
  assert.ok(result.sentences.some((sentence) => sentence.text.includes('3.5')));
  assert.ok(result.sentences.some((sentence) => sentence.text.includes('10.000')));
});

test('Intl tokenizer normalizes locales and segments CJK text without splitting sanitizer placeholders', () => {
  assert.equal(normalizeLocale('universal'), 'und');
  assert.equal(normalizeLocale('auto'), 'und');
  assert.equal(normalizeLocale('tr'), 'tr');
  assert.equal(isCJKText('日本語와 한국어'), true);
  assert.equal(isCJKText('Bahasa Melayu'), false);

  const result = tokenizeText('这是第一句话。第二句话更长，而且包含更多不同的词汇！TOKEN_ENTITY 保持完整。', 'zh');
  assert.equal(result.sentences.length, 3);
  assert.ok(result.words.length >= 12);
  assert.ok(tokenizeWords('TOKEN_ENTITY 中文', 'zh').includes('token_entity'));
});

test('built-in rule packs detect Spanish, Malay, and Mandarin while universal fallback remains available', () => {
  const spanish = analyzeText('En el vertiginoso mundo actual, cada equipo usa el mismo proceso. En el vertiginoso mundo actual, cada grupo sigue el mismo proceso. En el vertiginoso mundo actual, cada área repite el mismo proceso.', { language: 'es' });
  assert.equal(spanish.language, 'es');
  assert.equal(spanish.rulePack, 'es');
  assert.equal(spanish.status, 'FAIL');
  assert.ok(spanish.violations.some((violation) => violation.type === 'SLOP_PHRASE'));

  const malay = analyzeText('Dalam era digital kini, pasukan ini boleh mengurus kerja dengan cepat. Kerana itu, mereka boleh menyemak rekod bagi setiap pelanggan. Beliau kemudian menghantar laporan daripada pejabat kepada ketua.', { language: 'auto' });
  assert.equal(malay.language, 'ms');
  assert.equal(malay.rulePack, 'ms');
  assert.ok(malay.violations.some((violation) => violation.type === 'SLOP_PHRASE'));

  const mandarin = analyzeText('在当今快节奏的世界中，团队使用同一种流程。值得注意的是，成员每天重复相同的步骤。综上所述，结果总是按照同样的模板出现。', { language: 'zh' });
  assert.equal(mandarin.language, 'zh');
  assert.equal(mandarin.rulePack, 'zh');
  assert.ok(Number.isFinite(mandarin.metrics.burstinessCV));
  assert.ok(Number.isFinite(mandarin.metrics.mattr));
  assert.ok(mandarin.violations.some((violation) => violation.type === 'SLOP_PHRASE'));

  const japanese = analyzeText('これは短い文です。次の文は少し長く、異なる語彙を含んでいます。最後の文で要点を確認します。', { language: 'auto' });
  assert.equal(japanese.language, 'ja');
  assert.equal(japanese.rulePack, 'universal');

  const arabic = analyzeText('هذه جملة قصيرة. تحتوي الجملة التالية على كلمات مختلفة وتفاصيل إضافية. وتؤكد الجملة الأخيرة النتيجة بوضوح.', { language: 'auto' });
  assert.equal(arabic.language, 'ar');
  assert.equal(arabic.rulePack, 'universal');

  const monotoneTurkish = analyzeText('Ekip sabah raporu dikkatle inceledi. Grup öğleden sonra kayıtları dikkatle doğruladı. Kurul akşam aynı notları dikkatle karşılaştırdı. Yönetici gece sonuçları dikkatle arşivledi.', { language: 'tr' });
  assert.equal(monotoneTurkish.language, 'tr');
  assert.equal(monotoneTurkish.rulePack, 'universal');
  assert.equal(monotoneTurkish.status, 'FAIL');
  assert.ok(monotoneTurkish.violations.some((violation) => violation.type === 'MONOTONOUS_RHYTHM'));

  const variedTurkish = analyzeText('Dur. Ekip, depodaki eski kayıtları tek tek karşılaştırdı ve iki yanlış tarihi düzeltti. Sonraki denetim için hukuk, satış, destek ve finans ekiplerinin kullandığı farklı kaynaklardan gelen belgeleri bir araya getirerek ayrıntılı bir kontrol listesi hazırladılar.', { language: 'universal' });
  assert.equal(variedTurkish.rulePack, 'universal');
  assert.equal(variedTurkish.status, 'PASS');
});

test('automatic language detection favors Indonesian function words over technical loanwords', () => {
  const result = analyzeText('Framework cloud ini berjalan di server dan digunakan untuk deployment yang aman dengan konfigurasi dari tim. Operator memeriksa log setelah proses selesai. Catatan terakhir menjelaskan perubahan yang dibuat.', { language: 'auto' });
  assert.equal(result.language, 'id');
});

test('metrics implement the specified formulas', () => {
  const values = [2, 10, 4, 20];
  assert.equal(mean(values), 9);
  assert.equal(standardDeviation(values), 7);
  assert.equal(coefficientOfVariation(values), 7 / 9);
  assert.equal(adjacentDelta(values), 10);
  assert.ok(Math.abs(mattr(['a', 'b', 'a', 'c'], 3) - (2.5 / 3)) < 1e-12);
  assert.equal(compressionRatio(''), 0);
});

test('short prose skips statistical scoring without NaN values', () => {
  const result = analyzeText('Kalimat pendek. Selesai.', { language: 'id' });
  assert.equal(result.status, 'SKIP');
  assert.match(result.warning, /too short/i);
  for (const value of Object.values(result.metrics)) {
    if (typeof value === 'number') assert.ok(Number.isFinite(value));
  }
});

test('Markdown code and Indonesian whitelist words do not create false positives', () => {
  const text = `Perusahaan menjaga kesehatan anak-anak melalui diskusi distribusi dan digitalisasi rutin.\n\n\`\`\`txt\nTidak dapat dipungkiri bahwa pengimplementasian dilakukan.\n\`\`\`\n\nDiskriminasi dibahas tanpa distorsi oleh tim setelah pertemuan selesai. Undang-undang itu memberi dasar yang jauh lebih rinci untuk evaluasi berikutnya.`;
  const result = analyzeText(text, { language: 'id' });
  assert.equal(result.violations.some((v) => v.type === 'SLOP_PHRASE'), false);
  assert.equal(result.violations.some((v) => v.type === 'EXCESSIVE_NOMINALIZATION'), false);
  assert.equal(result.violations.some((v) => v.type === 'PASSIVE_BLOATING'), false);
});

test('custom voice profile creates a capped profile penalty when mean sentence length drifts', () => {
  const text = 'Rina membuka laporan pagi. Tim membaca catatan baru dengan teliti. Setelah data selesai diperiksa, mereka menyusun daftar perubahan yang cukup panjang untuk rapat siang dan membagikan tugas kepada setiap pemilik layanan.';
  const baseline = analyzeText(text, { language: 'id' });
  const result = analyzeText(text, {
    language: 'id',
    profile: { targets: { meanSentenceLength: 40 } },
  });
  assert.ok(result.violations.some((violation) => violation.type === 'VOICE_PROFILE_DEVIATION'));
  assert.equal(baseline.score - result.score, 5);
});

test('translationese openings trigger only when consecutive within one paragraph', () => {
  const sameParagraph = analyzeText('Dengan menggunakan data baru, tim memperbaiki jadwal kerja. Guna memastikan hasilnya stabil, operator memeriksa setiap catatan sebelum rapat dimulai. Mereka lalu mengirim laporan yang jauh lebih panjang kepada pemilik layanan.', { language: 'id' });
  assert.ok(sameParagraph.violations.some((violation) => violation.type === 'PASSIVE_BLOATING' && /consecutive sentences/i.test(violation.match)));

  const separateParagraphs = analyzeText('Dengan menggunakan data baru, tim memperbaiki jadwal kerja.\n\nGuna memastikan hasilnya stabil, operator memeriksa setiap catatan sebelum rapat dimulai. Kalimat terakhir dibuat jauh lebih panjang agar pemeriksaan statistik tetap berjalan tanpa mengubah tujuan pengujian ini.', { language: 'id' });
  assert.equal(separateParagraphs.violations.some((violation) => violation.type === 'PASSIVE_BLOATING' && /consecutive sentences/i.test(violation.match)), false);
});

test('statistical gate failures always include actionable diagnostics', () => {
  const text = [
    'Anna checked the morning report before the meeting started.',
    'Bram reviewed the latest figures before the meeting started.',
    'Clara opened the shared notes before the meeting started.',
    'Dimas tested the backup process before the meeting started.',
    'Elena verified the release checklist before the meeting started.',
    'Farid inspected the server logs before the meeting started.',
    'Grace compared the final totals before the meeting started.',
    'Hana updated the project board before the meeting started.',
  ].join(' ');
  const result = analyzeText(text, { language: 'en' });
  assert.equal(result.status, 'FAIL');
  const types = new Set(result.violations.map((violation) => violation.type));
  assert.ok(types.has('LOW_BURSTINESS'));
  assert.ok(types.has('MISSING_SENTENCE_RANGE'));
  assert.ok(types.has('LOW_ADJACENT_DELTA'));
  assert.ok(result.violations.every((violation) => violation.location && violation.fixInstruction));
});

test('required rule edge cases are detected', () => {
  const english = analyzeText('The change reduced delays, ensuring that the team could ship today. The first path--although old--still worked for several users. Another sentence is deliberately much longer because the analyzer needs enough prose to run its statistical and structural checks without using the short-text fallback.', { language: 'en' });
  assert.ok(english.violations.some((violation) => violation.type === 'STRUCTURAL_CLICHE' && /ensuring that/i.test(violation.match)));
  assert.ok(english.violations.some((violation) => violation.type === 'STRUCTURAL_CLICHE' && /--/.test(violation.match)));

  const indonesian = analyzeText('Pengembangan perangkat lunak terintegrasi adalah sebuah sistem yang menghubungkan pekerjaan lintas tim secara langsung. Tim menguji alurnya. Setelah pemeriksaan selesai, operator mencatat hasil yang jauh lebih rinci untuk bahan evaluasi berikutnya.', { language: 'id' });
  assert.ok(indonesian.violations.some((violation) => violation.type === 'DEFINITIONAL_OPENING'));
});

test('AI fixtures fail below 70 with actionable violations', async () => {
  for (const [name, language] of [['ai-sample-id.txt', 'id'], ['ai-sample-en.txt', 'en']]) {
    const result = analyzeText(await fixture(name), { language });
    assert.equal(result.status, 'FAIL', name);
    assert.ok(result.score < 70, `${name}: ${result.score}`);
    assert.ok(result.violations.length > 0, name);
    assert.ok(result.violations.every((v) => v.location && v.fixInstruction), name);
  }
});

test('human fixtures pass at 85 or above', async () => {
  for (const [name, language] of [['human-sample-id.txt', 'id'], ['human-sample-en.txt', 'en']]) {
    const result = analyzeText(await fixture(name), { language });
    assert.equal(result.status, 'PASS', `${name}: ${JSON.stringify(result, null, 2)}`);
    assert.ok(result.score >= 85, `${name}: ${result.score}`);
  }
});

test('browser analyzer matches CLI results', { skip: !browserParityAvailable }, async () => {
  const [idRules, enRules, defaultProfile] = await Promise.all([
    readFile(path.join(root, 'rules', 'id-slop.json'), 'utf8').then(JSON.parse),
    readFile(path.join(root, 'rules', 'en-slop.json'), 'utf8').then(JSON.parse),
    readFile(path.join(root, 'profiles', 'default-human.json'), 'utf8').then(JSON.parse),
  ]);
  const browser = createBrowserAnalyzer({ rules: { id: idRules, en: enRules }, defaultProfile });
  for (const [name, language] of [['ai-sample-id.txt', 'id'], ['ai-sample-en.txt', 'en'], ['human-sample-id.txt', 'id'], ['human-sample-en.txt', 'en']]) {
    const text = await fixture(name);
    assert.deepEqual(await browser.analyzeTextAsync(text, { language }), analyzeText(text, { language }));
  }
});

test('demo chrome has complete eight-language copy and official domain metadata', async () => {
  const index = await readFile(path.join(root, 'demo', 'index.html'), 'utf8');
  const app = await readFile(path.join(root, 'demo', 'app.mjs'), 'utf8');
  const languageCodes = ['en', 'id', 'es', 'ms', 'fr', 'de', 'pt', 'zh'];
  const requiredKeys = Object.keys(I18N.en);
  for (const language of languageCodes) {
    assert.ok(I18N[language], language);
    for (const key of requiredKeys) assert.ok(I18N[language][key], `${language}.${key}`);
    assert.ok(I18N[language].pageTitle);
    assert.ok(I18N[language].description);
    assert.ok(I18N[language].analyze);
    assert.ok(I18N[language].themeToDark);
    assert.doesNotMatch(I18N[language].pageTitle, /\p{Extended_Pictographic}/u);
    assert.match(index, new RegExp(`<option value="${language}" data-language="${language}">`));
    assert.match(index, new RegExp(`hreflang="${language}"`));
  }
  assert.match(index, /<html lang="en">/);
  assert.match(index, /https:\/\/humanizer\.aiclub\.ai\.id/);
  assert.match(app, /UI_LANGUAGE_CODES/);
  assert.match(app, /humanizer-lint\.language/);
  assert.match(app, /humanizer-lint\.theme/);
  assert.match(index, /id="interface-language"/);
  assert.doesNotMatch(index, /class="language-button"/);
  assert.match(index, /href="https:\/\/aiclub\.ai\.id" target="_blank" rel="noopener noreferrer">Website/);
  assert.match(index, /href="https:\/\/t\.me\/aiclub_id" target="_blank" rel="noopener noreferrer">Telegram/);
});

test('Pages build prevents the full technical SEO, security, and accessibility audit set from regressing', async () => {
  const dist = path.join(root, '.pages-dist');
  const index = await readFile(path.join(dist, 'index.html'), 'utf8');
  const headers = await readFile(path.join(dist, '_headers'), 'utf8');
  const robots = (await readFile(path.join(dist, 'robots.txt'), 'utf8')).replaceAll(String.fromCharCode(13), '');
  const missing = await readFile(path.join(dist, '404.html'), 'utf8');
  const favicon = await readFile(path.join(dist, 'favicon.ico'));
  for (const asset of ['404.html', '_headers', 'favicon.ico', 'favicon.svg', 'robots.txt', 'sitemap.xml']) {
    await readFile(path.join(dist, asset));
  }
  await assert.rejects(readFile(path.join(dist, '_redirects')));

  assert.match(missing, /<meta name="robots" content="noindex">/);
  assert.match(missing, /404 — Page Not Found/);
  assert.match(missing, /https:\/\/humanizer\.aiclub\.ai\.id\//);
  assert.deepEqual([...favicon.subarray(0, 6)], [0, 0, 1, 0, 1, 0]);
  assert.match(index, /<link rel="icon" href="\/favicon\.ico" sizes="any">/);
  assert.match(index, /<link rel="icon" href="\/favicon\.svg" type="image\/svg\+xml">/);
  assert.match(index, /<link rel="apple-touch-icon" href="\/favicon\.svg">/);
  assert.match(index, /max-image-preview:large/);

  const schemaMatch = index.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  assert.ok(schemaMatch);
  const schema = JSON.parse(schemaMatch[1]);
  const graph = new Map(schema['@graph'].map((node) => [node['@type'], node]));
  assert.equal(graph.get('WebSite').publisher['@id'], 'https://humanizer.aiclub.ai.id/#organization');
  assert.equal(graph.get('Organization').name, 'AI Club Indonesia (aiclub.ai.id)');
  assert.ok(graph.has('SoftwareApplication'));
  assert.ok(graph.has('FAQPage'));

  for (const header of [
    'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload',
    "Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'",
    'X-Frame-Options: DENY',
    'X-Content-Type-Options: nosniff',
    'Referrer-Policy: strict-origin-when-cross-origin',
    'Permissions-Policy: accelerometer=()',
    'Last-Modified: Sat, 31 Oct 2026 00:00:00 GMT',
    'ETag: W/"humanizer-lint-1.3.0-seo-audit"',
    'Cache-Control: public, max-age=0, must-revalidate',
  ]) assert.match(headers, new RegExp(header.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  for (const crawler of ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-Web', 'anthropic-ai', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Googlebot', 'Bingbot', 'Applebot', 'Applebot-Extended', 'Amazonbot', 'YouBot', 'DuckAssistBot', 'Bytespider', 'CCBot']) {
    assert.ok(robots.includes(`User-agent: ${crawler}\nAllow: /`), crawler);
  }
  assert.match(robots, /^Sitemap: https:\/\/humanizer\.aiclub\.ai\.id\/sitemap\.xml$/m);

  for (const [, tag, attributes, body] of index.matchAll(/<(button|a)\b([^>]*)>([\s\S]*?)<\/\1>/g)) {
    assert.ok(/\baria-label=/.test(attributes) || body.replace(/<[^>]+>/g, '').trim(), `${tag} is missing an accessible name`);
  }
  assert.match(index, /<select id="interface-language" aria-label="Interface language"/);
  assert.match(index, /<select id="analysis-language" aria-label="Analysis language">/);
  assert.match(index, /<label for="text"/);
  assert.match(await sourceFile('demo', 'app.mjs'), /button\.textContent = sampleLabel\(id\)/);
  assert.match(await sourceFile('demo', 'app.mjs'), /button\.append\(type, location, instruction\)/);
});

test('demo samples preserve verified multilingual outcomes and shareable state', async () => {
  const { DEMO_SAMPLES } = await import(projectModule('demo', 'samples.mjs'));
  const { buildAutoFixPrompt, diagnosticExcerpt, languageLabel, parseDemoQuery } = await import(projectModule('demo', 'presentation.mjs'));
  const expected = Object.fromEntries(['en', 'id', 'es', 'ms', 'fr', 'de', 'pt', 'zh'].flatMap((language) => [
    [`ai-${language}`, { language, status: 'FAIL', maxScore: 67 }],
    [`human-${language}`, { language, status: 'PASS', minScore: 85 }],
  ]));

  for (const [id, expectation] of Object.entries(expected)) {
    const sample = DEMO_SAMPLES[id];
    assert.equal(sample.language, expectation.language, id);
    const report = analyzeText(sample.text, { language: expectation.language });
    assert.equal(report.status, expectation.status, id);
    if (expectation.maxScore != null) assert.ok(report.score < 68, `${id}: ${report.score}`);
    if (expectation.minScore != null) assert.ok(report.score >= expectation.minScore, `${id}: ${report.score}`);
    if (id.startsWith('ai-')) {
      const types = new Set(report.violations.map((violation) => violation.type));
      assert.ok(types.has('SLOP_PHRASE'), id);
      assert.ok(types.has('MONOTONOUS_RHYTHM'), id);
      assert.ok(types.has('LOW_BURSTINESS'), id);
    } else {
      assert.equal(report.violations.length, 0, id);
    }
  }

  assert.deepEqual(parseDemoQuery('?sample=ai-es&lang=en&targetLang=es'), { sample: 'ai-es', language: 'en', targetLang: 'es' });
  assert.deepEqual(parseDemoQuery('?sample=unknown&lang=fr&targetLang=bad'), { sample: null, language: 'fr', targetLang: null });
  assert.equal(languageLabel('zh'), '中文 / Mandarin (Tier 1 Pack)');
  assert.equal(languageLabel('universal'), 'Universal Stylometry (Tier 2)');

  const source = DEMO_SAMPLES['ai-id'].text;
  const report = analyzeText(source, { language: 'id' });
  const first = report.violations[0];
  assert.match(diagnosticExcerpt(source, first), /Di era digital/);
  const prompt = buildAutoFixPrompt({ text: source, report });
  assert.match(prompt, /Bahasa Indonesia \(Tier 1 Pack\)/);
  assert.match(prompt, /LOW_BURSTINESS/);
  assert.match(prompt, /burstinessCV/);
  assert.match(prompt, /Di era digital/);
});

test('CLI runners cover PASS, SKIP, FAIL, stdin, and invalid arguments', async () => {
  const failedOutput = [];
  const failCode = await runAnalyzeCli(
    ['--file', path.join(root, 'tests', 'fixtures', 'ai-sample-en.txt'), '--lang', 'en', '--json'],
    { stdout: (value) => failedOutput.push(value), stderr: (value) => failedOutput.push(value), stdin: async () => '' },
  );
  assert.equal(failCode, 1);
  assert.equal(JSON.parse(failedOutput.join('')).status, 'FAIL');

  const passedOutput = [];
  const passCode = await runAnalyzeCli(
    ['--stdin', '--lang', 'en', '--json'],
    { stdout: (value) => passedOutput.push(value), stderr: (value) => passedOutput.push(value), stdin: async () => fixture('human-sample-en.txt') },
  );
  assert.equal(passCode, 0);
  assert.equal(JSON.parse(passedOutput.join('')).status, 'PASS');

  const skippedOutput = [];
  const skipCode = await runAnalyzeCli(
    ['--stdin', '--lang', 'id', '--json'],
    { stdout: (value) => skippedOutput.push(value), stderr: (value) => skippedOutput.push(value), stdin: async () => 'Pendek. Selesai.' },
  );
  assert.equal(skipCode, 0);
  assert.equal(JSON.parse(skippedOutput.join('')).status, 'SKIP');

  const humanOutput = [];
  assert.equal(await runAnalyzeCli(
    ['--stdin', '--lang', 'id'],
    { stdout: (value) => humanOutput.push(value), stderr: (value) => humanOutput.push(value), stdin: async () => 'Pendek. Selesai.' },
  ), 0);
  assert.match(humanOutput.join(''), /Status:\s+SKIP[\s\S]*Metrics:/);

  const errors = [];
  assert.equal(await runAnalyzeCli([], { stdout: () => {}, stderr: (value) => errors.push(value), stdin: async () => '' }), 2);
  assert.match(errors.join(''), /exactly one input/i);
});

test('fingerprint aggregates one to five samples and writes a loadable profile', async () => {
  const dir = await mkdtemp(path.join(tmpdir(), 'humanizer-lint-'));
  try {
    const first = path.join(dir, 'one.txt');
    const second = path.join(dir, 'two.txt');
    const output = path.join(dir, 'profile.json');
    await writeFile(first, await fixture('human-sample-id.txt'));
    await writeFile(second, await fixture('human-sample-en.txt'));
    const profile = await fingerprintSamples([first, second], { output });
    assert.equal(profile.sampleCount, 2);
    assert.ok(profile.metrics.burstinessCV > 0);
    assert.ok(profile.metrics.punctuationRates.comma >= 0);
    assert.deepEqual(JSON.parse(await readFile(output, 'utf8')), profile);

    const cliOutput = path.join(dir, 'cli-profile.json');
    const cliMessages = [];
    const cliCode = await runFingerprintCli(
      ['--input', first, '--output', cliOutput, '--name', 'cli-test', '--lang', 'id'],
      { stdout: (value) => cliMessages.push(value), stderr: (value) => cliMessages.push(value) },
    );
    assert.equal(cliCode, 0);
    assert.equal(JSON.parse(cliMessages.join('')).sampleCount, 1);
    assert.equal(JSON.parse(await readFile(cliOutput, 'utf8')).name, 'cli-test');

    const singleProfile = await fingerprintSamples([first]);
    const selfAnalysis = analyzeText(await readFile(first, 'utf8'), { language: 'id', profile: singleProfile });
    assert.equal(selfAnalysis.metrics.voiceProfileDeviation, 0);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});

test('package, skill, README, static demo, and skills.sh config match the v1.3.0 discovery contract', async () => {
  const packageSource = await readFile(path.join(root, 'package.json'), 'utf8');
  const packageJson = JSON.parse(packageSource);
  const skillsConfig = JSON.parse(await sourceFile('skills.sh.json'));
  const languageCodes = ['id', 'en', 'es', 'ms', 'fr', 'de', 'pt', 'zh'];
  const rulePacks = await Promise.all(languageCodes.map(async (code) => JSON.parse(await readFile(path.join(root, 'rules', `${code}-slop.json`), 'utf8'))));
  const gitignore = await sourceFile('.gitignore');
  const skill = await sourceFile('SKILL.md');
  const readme = await sourceFile('README.md');
  const workflow = await sourceFile('.github', 'workflows', 'ci.yml');
  const index = await sourceFile('demo', 'index.html');
  const build = await sourceFile('demo', 'build.mjs');
  const app = await sourceFile('demo', 'app.mjs');
  const llms = await sourceFile('demo', 'public', 'llms.txt');
  const fullReference = await sourceFile('demo', 'public', 'llms-full.md');
  const samples = await import(projectModule('demo', 'samples.mjs'));
  const sitemap = await sourceFile('demo', 'public', 'sitemap.xml');
  const ogImage = await sourceFile('demo', 'public', 'og-image.svg');
  const license = await sourceFile('LICENSE');

  assert.equal(packageJson.type, 'module');
  assert.equal(packageJson.engines.node, '>=18.3.0');
  assert.equal(packageJson.name, 'humanizer-lint');
  assert.equal(packageJson.version, '1.3.0');
  assert.equal(skillsConfig.$schema, 'https://skills.sh/schemas/skills.sh.schema.json');
  assert.equal(skillsConfig.notGrouped, 'bottom');
  assert.deepEqual(skillsConfig.groupings, [{
    title: 'Multilingual Prose Linting & AI Humanizer',
    description: 'Deterministic closed-loop stylometric linter, burstiness (CV) & MATTR analyzer, and anti-slop humanizer for 8 languages (EN, ID, ES, MS, FR, DE, PT, ZH) + 100+ universal languages.',
    skills: ['humanizer-lint']
  }]);
  assert.match(packageJson.description, /^Deterministic multilingual AI text humanizer, anti-slop prose linter/);
  assert.match(packageJson.description, /100\+ universal languages\. Local zero-dependency Node\.js CLI, no network\./);
  assert.equal(packageJson.homepage, 'https://humanizer.aiclub.ai.id');
  assert.deepEqual(packageJson.files, ['SKILL.md', 'README.md', 'LICENSE', 'scripts/', 'rules/', 'profiles/']);
  assert.deepEqual(packageJson.keywords, ['skills-sh', 'agent-skill', 'ai-humanizer', 'humanizer', 'anti-slop', 'prose-linter', 'stylometry', 'burstiness', 'mattr', 'multilingual-nlp', 'indonesian-nlp', 'copywriting', 'markdown-linter', 'claude-code', 'cursor-skill', 'windsurf', 'codex', 'gemini-cli']);
  assert.equal(packageJson.dependencies, undefined);
  assert.deepEqual(packageJson.bin, { 'humanizer-lint': 'scripts/analyze.mjs', 'humanizer-fingerprint': 'scripts/fingerprint.mjs' });
  assert.deepEqual(packageJson.repository, { type: 'git', url: 'git+https://github.com/yanstd888/humanizer-lint.git' });
  assert.equal((packageSource.match(/"files"\s*:/g) ?? []).length, 1);
  for (const ignored of ['node_modules/', '.wrangler/', '.pages-dist/', 'tasks/', '*.tmp.md', '.stylometric-draft.tmp.md', '.DS_Store']) assert.match(gitignore, new RegExp(`^${ignored.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`, 'm'));
  for (const [index, pack] of rulePacks.entries()) {
    assert.equal(pack.language, languageCodes[index]);
    assert.equal(pack.stopwords.length, 20);
    assert.ok(pack.patterns.length >= 25);
  }

  assert.match(skill, /^---\nname: humanizer-lint\n/);
  assert.match(skill, /description: Deterministic multilingual AI text humanizer, anti-slop prose linter/);
  assert.match(skill, /version: 1\.3\.0/);
  assert.match(skill, /summary: Deterministic closed-loop AI text humanizer/);
  assert.match(skill, /topic: agent-workflows/);
  assert.match(skill, /  - marketing/);
  assert.match(skill, /\*\*Audit, lint, and humanize AI-generated prose across 100\+ languages/);
  assert.match(skill, /`node <skill_dir>\/scripts\/analyze\.mjs --stdin --json`/);
  assert.match(skill, /8 deep anti-slop lexical & morphological rule packs/);
  assert.match(skill, /## Supported Languages \(Two-Tier Multilingual Architecture\)/);
  assert.match(skill, /## Agent-SEO Trigger Intents & Search Keywords/);
  assert.match(skill, /metadata:\n  version: "1\.3\.0"\n  author: "yanstd888"/);

  assert.match(readme, /### Humanize AI-generated text with a deterministic local AI humanizer and anti-slop prose linter/);
  assert.match(readme, /\[!\[skills\.sh\]\(https:\/\/skills\.sh\/b\/yanstd888\/humanizer-lint\)\]\(https:\/\/www\.skills\.sh\/yanstd888\/humanizer-lint\/humanizer-lint\)/);
  assert.match(readme, /\*\*Summary\*\*/);
  assert.match(readme, /Eliminates robotic LLM writing patterns/);
  assert.match(readme, /## Language support/);
  assert.match(readme, /Tier 1 — rule packs/);
  assert.match(readme, /Tier 2 — universal/);
  assert.match(readme, /--lang auto/);
  assert.match(readme, /--lang universal/);
  assert.doesNotMatch(readme, /\p{Extended_Pictographic}/u);

  assert.match(workflow, /node: \["18", "20", "22"\]/);
  assert.match(workflow, /npm test/);
  assert.match(workflow, /npm pack --dry-run/);

  assert.match(index, /application\/ld\+json/);
  assert.match(index, /{{pageTitle}}/);
  assert.match(index, /humanizer bahasa indonesia/);
  assert.match(index, /Eight anti-slop packs, plus universal stylometry/);
  assert.match(index, /hreflang="x-default"/);
  assert.match(index, /id="analysis-language"/);
  for (const code of ['auto', ...languageCodes, 'universal']) assert.match(index, new RegExp(`value="${code}"`));
  for (const code of languageCodes) for (const kind of ['ai', 'human']) assert.ok(samples.DEMO_SAMPLES[`${kind}-${code}`], `${kind}-${code}`);
  assert.match(app, /targetLang/);
  assert.match(app, /Object\.fromEntries\(ruleEntries\)/);
  assert.doesNotMatch(app, /fetch\(['"]https?:\/\//);
  for (const asset of ['robots.txt', 'sitemap.xml', 'llms.txt', 'favicon.svg', 'og-image.svg', 'llms-full.md']) await readFile(path.join(root, 'demo', 'public', asset), 'utf8');
  assert.match(build, /ruleCodes = \['id', 'en', 'es', 'ms', 'fr', 'de', 'pt', 'zh'\]/);
  assert.match(build, /'llms-full\.txt'/);
  assert.match(llms, /Version 1\.3\.0/);
  assert.match(llms, /## Executive summary/);
  assert.match(llms, /Eliminates robotic LLM writing patterns/);
  assert.match(fullReference, /Version 1\.3\.0/);
  assert.match(fullReference, /## Executive summary/);
  assert.match(fullReference, /Eliminates robotic LLM writing patterns/);
  assert.match(llms, /Intl\.Segmenter/);
  assert.match(fullReference, /\{\{ruleCatalog\}\}/);
  assert.match(license, /MIT License/);

  const rootMarkdown = (await readdir(root)).filter((name) => name.toLowerCase().endsWith('.md')).sort();
  assert.deepEqual(rootMarkdown, ['README.md', 'SKILL.md']);
});

test('production scripts use only approved built-ins and forbidden APIs are absent', async () => {
  const scriptsRoot = path.join(root, 'scripts');
  const files = [];
  const visit = async (dir) => {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) await visit(file);
      else if (entry.name.endsWith('.mjs')) files.push(file);
    }
  };
  await visit(scriptsRoot);
  const allowed = new Set(['node:fs', 'node:path', 'node:os', 'node:zlib', 'node:util']);
  for (const file of files) {
    const source = await readFile(file, 'utf8');
    assert.doesNotMatch(source, /child_process|\beval\s*\(|\bFunction\s*\(|\bfetch\s*\(/, file);
    for (const match of source.matchAll(/from\s+['"](node:[^'"]+)['"]/g)) {
      assert.ok(allowed.has(match[1]), `${file} imports ${match[1]}`);
    }
  }
});
