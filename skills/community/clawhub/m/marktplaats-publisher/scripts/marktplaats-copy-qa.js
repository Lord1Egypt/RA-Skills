#!/usr/bin/env node
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import path from 'node:path';

const DEFAULTS = {
  min: 3200,
  max: 3500,
  absoluteMin: 2800,
  absoluteMax: 3600,
  minParagraphs: 7,
  minRequiredTerms: 2,
  minVariants: 1,
};

function usage() {
  console.error(`Usage: marktplaats-copy-qa <description.md> [options]

Options:
  --min <n>                 Target minimum characters, default 3200
  --max <n>                 Target maximum characters, default 3500
  --absolute-min <n>        Hard lower stop limit, default 2800
  --absolute-max <n>        Hard upper stop limit, default 3600
  --min-paragraphs <n>      Minimum substantial paragraphs/sections, default 7
  --require <term>          Required product/SEO term; repeat at least twice
  --variant <term>          Natural typo/search variant; repeat if useful
  --ad-json <path>          Write copyQuality evidence into an ad.json file
  --allow-no-variant        Allow no typo/search variant; use only with explicit exception
  --allow-no-required       Allow no required product terms; use only for diagnostics
  --json                    Output JSON only
  --self-test               Run built-in pass/fail smoke tests
`);
}

function parseArgs(argv) {
  const options = {
    ...DEFAULTS,
    required: [],
    variants: [],
    adJson: null,
    allowNoVariant: false,
    allowNoRequired: false,
    json: false,
    selfTest: false,
  };
  const files = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new Error(`Missing value for ${arg}`);
      i += 1;
      return argv[i];
    };

    if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else if (arg === '--min') options.min = Number(next());
    else if (arg === '--max') options.max = Number(next());
    else if (arg === '--absolute-min') options.absoluteMin = Number(next());
    else if (arg === '--absolute-max') options.absoluteMax = Number(next());
    else if (arg === '--min-paragraphs') options.minParagraphs = Number(next());
    else if (arg === '--require') options.required.push(next());
    else if (arg === '--variant') options.variants.push(next());
    else if (arg === '--ad-json') options.adJson = next();
    else if (arg === '--allow-no-variant') options.allowNoVariant = true;
    else if (arg === '--allow-no-required') options.allowNoRequired = true;
    else if (arg === '--json') options.json = true;
    else if (arg === '--self-test') options.selfTest = true;
    else if (arg.startsWith('-')) throw new Error(`Unknown option: ${arg}`);
    else files.push(arg);
  }

  if (!options.selfTest && files.length !== 1) {
    usage();
    process.exit(2);
  }

  return { file: files[0], options };
}

function normalize(text) {
  return text.replace(/\r\n/g, '\n');
}

function countChars(text) {
  return [...text].length;
}

function sha256(text) {
  return crypto.createHash('sha256').update(text, 'utf8').digest('hex');
}

function getLastSentence(text) {
  return text.trim().match(/[^.!?\n][^.!?]*(?:[.!?])?\s*$/)?.[0]?.trim() || '';
}

function evaluate(text, options, file = null) {
  const normalized = normalize(text);
  const chars = countChars(normalized);
  const words = normalized.trim() ? normalized.trim().split(/\s+/).length : 0;
  const lines = normalized.split('\n');
  const paragraphs = normalized
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim())
    .filter((paragraph) => paragraph.length >= 80).length;
  const bulletLines = lines.filter((line) => /^\s*[-*]\s+\S/.test(line)).length;
  const lower = normalized.toLocaleLowerCase('nl-NL');
  const includes = (term) => lower.includes(String(term).toLocaleLowerCase('nl-NL'));
  const keywordHeading = /^\s*(zoektermen|keywords?|seo)\s*:/gim.test(normalized);
  const commaDump = lines.some((line) => {
    const trimmed = line.trim();
    return trimmed.length >= 120 && (trimmed.match(/,/g) || []).length >= 8;
  });
  const requiredMissing = options.required.filter((term) => !includes(term));
  const variantMatches = options.variants.filter((term) => includes(term));
  const lastSentence = getLastSentence(normalized);

  const failures = [];
  const warnings = [];

  if (chars < options.absoluteMin) {
    failures.push(`description is below absolute minimum: ${chars} < ${options.absoluteMin}`);
  } else if (chars < options.min) {
    failures.push(`description is below target minimum: ${chars} < ${options.min}`);
  }

  if (chars > options.absoluteMax) {
    failures.push(`description is above absolute maximum: ${chars} > ${options.absoluteMax}`);
  } else if (chars > options.max) {
    warnings.push(`description is above target maximum: ${chars} > ${options.max}`);
  }

  if (paragraphs < options.minParagraphs) {
    failures.push(`not enough substantial paragraphs/sections: ${paragraphs} < ${options.minParagraphs}`);
  }

  if (bulletLines < 3) {
    warnings.push(`few concrete feature bullets: ${bulletLines} < 3`);
  }

  if (keywordHeading) {
    failures.push('contains forbidden keyword/SEO heading such as Zoektermen:, Keywords:, or SEO:');
  }

  if (commaDump) {
    failures.push('contains a likely comma-separated keyword dump');
  }

  if (!options.allowNoRequired && options.required.length < options.minRequiredTerms) {
    failures.push(`provide at least ${options.minRequiredTerms} --require product/SEO terms`);
  }

  if (requiredMissing.length) {
    failures.push(`missing required product/SEO terms: ${requiredMissing.join(', ')}`);
  }

  if (!options.allowNoVariant && options.variants.length < options.minVariants) {
    failures.push(`provide at least ${options.minVariants} --variant typo/search variant`);
  }

  if (!options.allowNoVariant && options.variants.length && !variantMatches.length) {
    failures.push(`missing natural typo/search variant; expected one of: ${options.variants.join(', ')}`);
  }

  if (lastSentence.length < 20) {
    warnings.push('last sentence is very short; live last-sentence verification may be weak');
  }

  const passed = failures.length === 0;

  return {
    file,
    checkedAt: new Date().toISOString(),
    passed,
    chars,
    words,
    descriptionSha256: sha256(normalized),
    paragraphs,
    bulletLines,
    minChars: options.min,
    maxChars: options.max,
    absoluteMinChars: options.absoluteMin,
    absoluteMaxChars: options.absoluteMax,
    hasNaturalSeo: options.required.length >= options.minRequiredTerms && requiredMissing.length === 0 && !keywordHeading && !commaDump,
    hasIntentionalVariant: options.allowNoVariant || variantMatches.length > 0,
    hasKeywordDump: keywordHeading || commaDump,
    requiredTerms: options.required,
    requiredMissing,
    variantTerms: options.variants,
    variantMatches,
    lastSentence,
    lastSentenceVerified: false,
    failures,
    warnings,
  };
}

function writeAdJson(adJsonPath, result) {
  const ad = JSON.parse(fs.readFileSync(adJsonPath, 'utf8'));
  ad.copyQuality = {
    checkedAt: result.checkedAt,
    chars: result.chars,
    words: result.words,
    descriptionSha256: result.descriptionSha256,
    paragraphs: result.paragraphs,
    minChars: result.minChars,
    maxChars: result.maxChars,
    passed: result.passed,
    hasNaturalSeo: result.hasNaturalSeo,
    hasIntentionalVariant: result.hasIntentionalVariant,
    hasKeywordDump: result.hasKeywordDump,
    requiredTerms: result.requiredTerms,
    requiredMissing: result.requiredMissing,
    variantTerms: result.variantTerms,
    variantMatches: result.variantMatches,
    lastSentence: result.lastSentence,
    lastSentenceVerified: result.lastSentenceVerified,
    failures: result.failures,
    warnings: result.warnings,
  };
  fs.writeFileSync(adJsonPath, `${JSON.stringify(ad, null, 2)}\n`, 'utf8');
}

function printResult(result, json) {
  if (json) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }

  console.log(`Copy QA: ${result.passed ? 'PASS' : 'FAIL'}`);
  console.log(`chars=${result.chars} words=${result.words} paragraphs=${result.paragraphs} bullets=${result.bulletLines}`);
  if (result.requiredTerms.length) console.log(`requiredTerms=${result.requiredTerms.join(', ')}`);
  if (result.variantTerms.length) console.log(`variantTerms=${result.variantTerms.join(', ')}`);
  if (result.variantMatches.length) console.log(`variantMatches=${result.variantMatches.join(', ')}`);
  if (result.warnings.length) console.log(`warnings:\n- ${result.warnings.join('\n- ')}`);
  if (result.failures.length) console.log(`failures:\n- ${result.failures.join('\n- ')}`);
  console.log(`lastSentence=${result.lastSentence}`);
}

function assertSelfTest(condition, message) {
  if (!condition) throw new Error(`self-test failed: ${message}`);
}

function runSelfTest() {
  const bad = `Te koop: korte advertentie.\n\nZoektermen: marktplaats, test, kort, spam, lijst, los, zoekwoord, fout, advertentie.`;
  const sections = [
    'Te koop: Testmerk Model X buitenantenne voor betere ontvangst. Deze tekst is bewust lang genoeg om de Marktplaats copy gate te testen en bevat productinformatie in gewone taal.',
    'De set is bedoeld voor kopers die gericht zoeken naar een nette gebruikte antenne voor een router, modem of vergelijkbare toepassing. De beschrijving blijft feitelijk en vermijdt garanties.',
    'De staat wordt als gebruikt beschreven. Eventuele lichte gebruikssporen horen bij normaal gebruik en een koper moet altijd de foto controleren voordat hij reageert.',
    'Kenmerken zijn een paneelvormige behuizing, montageoptie en kabels zoals zichtbaar op foto. Dit is geen claim dat accessoires compleet zijn buiten wat zichtbaar of bevestigd is.',
    'Voor gebruik is het belangrijk om de aansluiting, kabellengte, montageplek en eigen router of modem te vergelijken. Niet elke buitenantenne past op elke situatie.',
    'In normale zinnen staan zoekvarianten zoals buitenantenne, LTE antenne, router antenne en buiten antenne. Die laatste schrijfwijze is een natuurlijke variant die sommige kopers gebruiken.',
    'Ophalen of verzenden kan afhankelijk van de afspraak met de verkoper. Bieden mag als dat zo in de advertentie is ingesteld en de vraagprijs blijft duidelijk.',
    'Stuur gerust een bericht als je wilt controleren of dit item past bij jouw toepassing voordat je een bod doet.',
  ];
  const extra =
    'Deze extra alinea vult de voorbeeldtekst aan tot de normale lengte die voor een echte advertentie nodig is. De inhoud blijft concreet: vergelijk altijd de aansluiting, de montageplek en de foto met je eigen situatie. Daardoor test de gate niet alleen lengte, maar ook of de tekst als gewone advertentietaal blijft klinken. Een koper krijgt zo genoeg context om gericht te reageren zonder dat de tekst verandert in een lijst met losse zoekwoorden of onnatuurlijke herhaling.';
  const good = `${sections.join('\n\n')}\n\n- Testmerk Model X\n- Buitenantenne\n- Router antenne\n\n${sections.join('\n\n')}\n\n${extra}`;
  const options = {
    ...DEFAULTS,
    required: ['Testmerk', 'buitenantenne'],
    variants: ['buiten antenne'],
    allowNoVariant: false,
    allowNoRequired: false,
  };

  assertSelfTest(!evaluate(bad, options).passed, 'bad sample should fail');
  assertSelfTest(evaluate(good, options).passed, 'good sample should pass');

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'marktplaats-copy-qa-'));
  const adJson = path.join(tmpDir, 'ad.json');
  fs.writeFileSync(adJson, '{}\n', 'utf8');
  const result = evaluate(good, options, 'self-test.md');
  writeAdJson(adJson, result);
  const saved = JSON.parse(fs.readFileSync(adJson, 'utf8'));
  assertSelfTest(saved.copyQuality?.passed === true, 'copyQuality should be written');
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log('marktplaats-copy-qa self-test: PASS');
}

try {
  const { file, options } = parseArgs(process.argv.slice(2));
  if (options.selfTest) {
    runSelfTest();
    process.exit(0);
  }

  const text = fs.readFileSync(file, 'utf8');
  const result = evaluate(text, options, file);
  if (options.adJson) writeAdJson(options.adJson, result);
  printResult(result, options.json);
  process.exit(result.passed ? 0 : 1);
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(2);
}
