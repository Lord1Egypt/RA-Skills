#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const IMAGE_EXTS = new Set(['.jpg', '.jpeg', '.png', '.webp', '.heic']);

function usage() {
  console.error(`Usage:
  marktplaats-ad-preflight --ad-json ./ad.json [options]

Options:
  --description PATH             Override description file
  --photo-dir PATH               Override processed photo directory
  --min-photos N                 Minimum photo count, default 1
  --require-bidding-allowed      Fail unless ad.biddingAllowed is true
  --allow-stale-copy-quality     Warn instead of fail when copy-QA hash is missing
  --json                         Emit JSON only
  --self-test                    Run deterministic smoke test
  -h, --help                     Show this help
`);
}

function parseArgs(argv) {
  const out = {
    adJson: null,
    description: null,
    photoDir: null,
    minPhotos: 1,
    requireBiddingAllowed: false,
    allowStaleCopyQuality: false,
    json: false,
    selfTest: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new Error(`Missing value for ${arg}`);
      i += 1;
      return argv[i];
    };

    if (arg === '-h' || arg === '--help') {
      usage();
      process.exit(0);
    } else if (arg === '--ad-json') out.adJson = next();
    else if (arg === '--description') out.description = next();
    else if (arg === '--photo-dir') out.photoDir = next();
    else if (arg === '--min-photos') out.minPhotos = Number(next());
    else if (arg === '--require-bidding-allowed') out.requireBiddingAllowed = true;
    else if (arg === '--allow-stale-copy-quality') out.allowStaleCopyQuality = true;
    else if (arg === '--json') out.json = true;
    else if (arg === '--self-test') out.selfTest = true;
    else throw new Error(`Unknown option: ${arg}`);
  }

  if (!out.selfTest && !out.adJson) {
    usage();
    process.exit(2);
  }
  return out;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function sha256(text) {
  return crypto.createHash('sha256').update(text.replace(/\r\n/g, '\n'), 'utf8').digest('hex');
}

function countChars(text) {
  return [...text.replace(/\r\n/g, '\n')].length;
}

function getLastSentence(text) {
  return text.trim().replace(/\r\n/g, '\n').match(/[^.!?\n][^.!?]*(?:[.!?])?\s*$/)?.[0]?.trim() || '';
}

function resolveMaybeRelative(baseDir, value) {
  if (!value) return null;
  return path.isAbsolute(value) ? value : path.resolve(baseDir, value);
}

function findDescriptionPath(ad, adJsonPath, override) {
  const baseDir = path.dirname(adJsonPath);
  return resolveMaybeRelative(baseDir, override || ad.descriptionFile || 'description.md');
}

function listImageFiles(dir) {
  if (!dir || !fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .map((name) => path.join(dir, name))
    .filter((file) => {
      try {
        return fs.statSync(file).isFile() && IMAGE_EXTS.has(path.extname(file).toLowerCase());
      } catch {
        return false;
      }
    })
    .sort();
}

function findPhotoFiles(ad, adJsonPath, override) {
  const baseDir = path.dirname(adJsonPath);
  const dirs = [
    override,
    ad.imageDir,
    path.join(baseDir, 'photos', 'processed'),
    path.join(baseDir, 'photos'),
  ]
    .filter(Boolean)
    .map((value) => resolveMaybeRelative(baseDir, value));

  const files = [];
  for (const dir of dirs) {
    for (const file of listImageFiles(dir)) {
      if (!files.includes(file)) files.push(file);
    }
  }

  if (Array.isArray(ad.photoSources) && ad.imageDir) {
    const imageDir = resolveMaybeRelative(baseDir, ad.imageDir);
    for (const source of ad.photoSources) {
      if (!source?.file) continue;
      const file = path.join(imageDir, source.file);
      if (fs.existsSync(file) && !files.includes(file)) files.push(file);
    }
  }

  return files.sort();
}

function hasKeywordDump(text) {
  const normalized = text.replace(/\r\n/g, '\n');
  if (/^\s*(zoektermen|keywords?|seo)\s*:/gim.test(normalized)) return true;
  return normalized.split('\n').some((line) => {
    const trimmed = line.trim();
    return trimmed.length >= 120 && (trimmed.match(/,/g) || []).length >= 8;
  });
}

function evaluate(ad, adJsonPath, options) {
  const failures = [];
  const warnings = [];
  const descriptionPath = findDescriptionPath(ad, adJsonPath, options.description);
  const photoFiles = findPhotoFiles(ad, adJsonPath, options.photoDir);

  const requiredFields = ['title', 'price', 'condition', 'delivery', 'category'];
  for (const field of requiredFields) {
    if (ad[field] == null || String(ad[field]).trim() === '') failures.push(`missing ad.${field}`);
  }

  if (!ad.categoryIds || (!ad.categoryIds.l1 && !ad.categoryIds.l2)) {
    failures.push('missing ad.categoryIds.l1/l2');
  }

  if (typeof ad.biddingAllowed !== 'boolean') {
    failures.push('missing boolean ad.biddingAllowed');
  } else if (options.requireBiddingAllowed && ad.biddingAllowed !== true) {
    failures.push('ad.biddingAllowed is not true');
  }

  if (!descriptionPath || !fs.existsSync(descriptionPath)) {
    failures.push(`description file not found: ${descriptionPath || '(missing)'}`);
  }

  let description = '';
  let descriptionSha256 = null;
  let lastSentence = '';
  let chars = 0;
  if (descriptionPath && fs.existsSync(descriptionPath)) {
    description = fs.readFileSync(descriptionPath, 'utf8').replace(/\r\n/g, '\n');
    descriptionSha256 = sha256(description);
    lastSentence = getLastSentence(description);
    chars = countChars(description);
    if (hasKeywordDump(description)) failures.push('description contains keyword dump');
  }

  if (photoFiles.length < options.minPhotos) {
    failures.push(`not enough photos: ${photoFiles.length} < ${options.minPhotos}`);
  }

  const copyQuality = ad.copyQuality || null;
  if (!copyQuality) {
    failures.push('missing ad.copyQuality; run marktplaats-copy-qa first');
  } else {
    if (copyQuality.passed !== true) failures.push('ad.copyQuality.passed is not true');
    if (copyQuality.hasKeywordDump === true) failures.push('ad.copyQuality.hasKeywordDump is true');
    if (Array.isArray(copyQuality.requiredMissing) && copyQuality.requiredMissing.length) {
      failures.push(`copyQuality required terms missing: ${copyQuality.requiredMissing.join(', ')}`);
    }
    if (copyQuality.hasIntentionalVariant !== true) failures.push('copyQuality has no intentional search variant');
    if (description && copyQuality.chars !== chars) {
      failures.push(`description chars changed after copy-QA: ${chars} != ${copyQuality.chars}`);
    }
    if (description && copyQuality.lastSentence && copyQuality.lastSentence !== lastSentence) {
      failures.push('description last sentence changed after copy-QA');
    }
    if (description && copyQuality.descriptionSha256) {
      if (copyQuality.descriptionSha256 !== descriptionSha256) failures.push('description sha256 changed after copy-QA');
    } else if (!options.allowStaleCopyQuality) {
      failures.push('copyQuality.descriptionSha256 missing; rerun marktplaats-copy-qa');
    } else {
      warnings.push('copyQuality.descriptionSha256 missing; accepted because --allow-stale-copy-quality was set');
    }
  }

  return {
    checkedAt: new Date().toISOString(),
    passed: failures.length === 0,
    adJson: adJsonPath,
    descriptionPath,
    descriptionSha256,
    chars,
    lastSentence,
    photoCount: photoFiles.length,
    photoFiles,
    requireBiddingAllowed: options.requireBiddingAllowed,
    failures,
    warnings,
  };
}

function printResult(result, json) {
  if (json) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }
  console.log(`Ad preflight: ${result.passed ? 'PASS' : 'FAIL'}`);
  console.log(`chars=${result.chars} photos=${result.photoCount} biddingRequired=${result.requireBiddingAllowed}`);
  if (result.warnings.length) console.log(`warnings:\n- ${result.warnings.join('\n- ')}`);
  if (result.failures.length) console.log(`failures:\n- ${result.failures.join('\n- ')}`);
}

function makeGoodDescription() {
  const sections = [
    'Te koop: Testmerk Model X buitenantenne voor een router of modem. Deze advertentie is bedoeld als realistische preflight-test met voldoende gewone tekst.',
    'De staat is gebruikt maar netjes beschreven. Er worden geen garanties gegeven buiten wat zichtbaar en controleerbaar is.',
    'De kenmerken zijn concreet beschreven zodat kopers weten waar ze op moeten letten. Denk aan aansluiting, montage, kabel en toepassing.',
    'Voor compatibiliteit moet de koper altijd de foto en eigen situatie vergelijken. Niet elk accessoire past op elk apparaat.',
    'De advertentie verwerkt zoekwoorden in normale zinnen, zoals buitenantenne, LTE antenne, router antenne en buiten antenne.',
    'Ophalen of verzenden kan in overleg. Bieden mag als dat in de advertentie is ingesteld.',
    'Stuur gerust een bericht als je wilt controleren of dit item past bij jouw toepassing voordat je biedt.',
  ];
  const body = `${sections.join('\n\n')}\n\n- Testmerk Model X\n- Buitenantenne\n- Router antenne\n\n`;
  return `${body}${body}${body}${sections[6]}`;
}

function runSelfTest() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'marktplaats-preflight-'));
  const descriptionFile = path.join(dir, 'description.md');
  const imageDir = path.join(dir, 'photos', 'processed');
  fs.mkdirSync(imageDir, { recursive: true });
  fs.writeFileSync(path.join(imageDir, '01.jpg'), 'fake image bytes');
  const description = makeGoodDescription();
  const descriptionSha256 = sha256(description);
  fs.writeFileSync(descriptionFile, description);
  const adJson = path.join(dir, 'ad.json');
  const ad = {
    title: 'Testmerk Model X buitenantenne',
    price: '25,00',
    condition: 'Gebruikt',
    delivery: 'Ophalen of Verzenden',
    category: 'Computeronderdelen',
    categoryIds: { l1: '1', l2: '2' },
    biddingAllowed: true,
    descriptionFile,
    imageDir,
    copyQuality: {
      passed: true,
      hasKeywordDump: false,
      hasIntentionalVariant: true,
      requiredMissing: [],
      chars: countChars(description),
      descriptionSha256,
      lastSentence: getLastSentence(description),
    },
  };
  fs.writeFileSync(adJson, `${JSON.stringify(ad, null, 2)}\n`);
  const ok = evaluate(ad, adJson, { minPhotos: 1, requireBiddingAllowed: true });
  if (!ok.passed) throw new Error(`self-test expected PASS: ${ok.failures.join('; ')}`);
  ad.biddingAllowed = false;
  const bad = evaluate(ad, adJson, { minPhotos: 1, requireBiddingAllowed: true });
  if (bad.passed) throw new Error('self-test expected FAIL for biddingAllowed=false');
  console.log('marktplaats-ad-preflight self-test: PASS');
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.selfTest) {
    runSelfTest();
    return;
  }
  const adJsonPath = path.resolve(options.adJson);
  const ad = readJson(adJsonPath);
  const result = evaluate(ad, adJsonPath, options);
  printResult(result, options.json);
  if (!result.passed) process.exitCode = 1;
}

main();
