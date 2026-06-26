#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

function usage() {
  console.error(`Usage:
  marktplaats-register-update --ad-json ./ad.json --central-json ./advertenties.json [options]

Options:
  --note TEXT       Append a note to the ad and central register
  --add-missing     Add ad to central register if no matching adId/localId exists
  --json            Emit JSON only
  --self-test       Run deterministic smoke test
  -h, --help        Show this help
`);
}

function parseArgs(argv) {
  const out = {
    adJson: null,
    centralJson: null,
    note: null,
    addMissing: false,
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
    else if (arg === '--central-json') out.centralJson = next();
    else if (arg === '--note') out.note = next();
    else if (arg === '--add-missing') out.addMissing = true;
    else if (arg === '--json') out.json = true;
    else if (arg === '--self-test') out.selfTest = true;
    else throw new Error(`Unknown option: ${arg}`);
  }

  if (!out.selfTest && (!out.adJson || !out.centralJson)) {
    usage();
    process.exit(2);
  }

  return out;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function acquireLock(targetPath) {
  const lockPath = `${targetPath}.lock`;
  let fd = null;
  try {
    fd = fs.openSync(lockPath, 'wx');
    fs.writeFileSync(fd, `${process.pid}\n${new Date().toISOString()}\n`, 'utf8');
    return {
      lockPath,
      release() {
        try {
          fs.closeSync(fd);
        } catch {
          // best effort
        }
        try {
          fs.unlinkSync(lockPath);
        } catch {
          // best effort
        }
      },
    };
  } catch (error) {
    if (fd != null) {
      try {
        fs.closeSync(fd);
      } catch {
        // best effort
      }
    }
    throw new Error(`central register is locked: ${lockPath}. Do not run register updates in parallel.`);
  }
}

function appendNote(existing, note) {
  if (!note) return existing || '';
  const current = existing || '';
  if (current.includes(note)) return current;
  return `${current}${current ? ' ' : ''}${note}`.trim();
}

function normalizeCentral(value) {
  if (Array.isArray(value)) {
    return { schema: 'marktplaats-register-v1', updatedAt: null, ads: value };
  }
  if (value && Array.isArray(value.ads)) return value;
  throw new Error('central register must be an array or object with ads[]');
}

function matchesAd(candidate, ad) {
  if (ad.adId && candidate.adId === ad.adId) return true;
  if (ad.localId && candidate.localId === ad.localId) return true;
  return false;
}

function updateRegister({ ad, central, note, addMissing }) {
  const timestamp = new Date().toISOString();
  const normalized = normalizeCentral(central);
  const index = normalized.ads.findIndex((candidate) => matchesAd(candidate, ad));
  const nextAd = {
    ...ad,
    lastCheckedAt: ad.lastCheckedAt || timestamp,
    notes: appendNote(ad.notes, note),
  };

  if (index === -1) {
    if (!addMissing) {
      return {
        passed: false,
        updatedAt: timestamp,
        action: 'not-found',
        failures: ['ad not found in central register; pass --add-missing to append'],
        register: normalized,
      };
    }
    normalized.ads.push(nextAd);
    normalized.updatedAt = timestamp;
    return {
      passed: true,
      updatedAt: timestamp,
      action: 'added',
      index: normalized.ads.length - 1,
      failures: [],
      register: normalized,
    };
  }

  normalized.ads[index] = {
    ...normalized.ads[index],
    ...nextAd,
    notes: appendNote(normalized.ads[index].notes, note || nextAd.notes),
  };
  normalized.updatedAt = timestamp;
  return {
    passed: true,
    updatedAt: timestamp,
    action: 'updated',
    index,
    failures: [],
    register: normalized,
  };
}

function printResult(result, json) {
  const publicResult = {
    passed: result.passed,
    action: result.action,
    index: result.index ?? null,
    updatedAt: result.updatedAt,
    failures: result.failures,
  };
  if (json) {
    process.stdout.write(`${JSON.stringify(publicResult, null, 2)}\n`);
    return;
  }
  console.log(`Register update: ${result.passed ? 'PASS' : 'FAIL'}`);
  console.log(`action=${result.action}${result.index == null ? '' : ` index=${result.index}`}`);
  if (result.failures.length) console.log(`failures:\n- ${result.failures.join('\n- ')}`);
}

function runSelfTest() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'marktplaats-register-update-'));
  const adJson = path.join(dir, 'ad.json');
  const centralJson = path.join(dir, 'advertenties.json');
  const ad = {
    localId: 'test-1',
    adId: 'm123',
    title: 'Test advertentie',
    lastCheckedAt: '2026-01-01T00:00:00.000Z',
    copyQuality: { passed: true, lastSentenceVerified: true },
    notes: 'Basisnotitie.',
  };
  fs.writeFileSync(adJson, `${JSON.stringify(ad, null, 2)}\n`);
  fs.writeFileSync(centralJson, `${JSON.stringify({ schema: 'marktplaats-register-v1', updatedAt: null, ads: [{ localId: 'test-1', adId: 'm123', title: 'Oud' }] }, null, 2)}\n`);

  const result = updateRegister({
    ad: readJson(adJson),
    central: readJson(centralJson),
    note: 'Live gecontroleerd.',
    addMissing: false,
  });
  if (!result.passed || result.action !== 'updated') throw new Error('self-test expected update PASS');
  if (!result.register.ads[0].notes.includes('Live gecontroleerd.')) throw new Error('self-test expected note append');
  console.log('marktplaats-register-update self-test: PASS');
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.selfTest) {
    runSelfTest();
    return;
  }
  const adJsonPath = path.resolve(options.adJson);
  const centralJsonPath = path.resolve(options.centralJson);
  const lock = acquireLock(centralJsonPath);
  try {
    const ad = readJson(adJsonPath);
    if (options.note) {
      ad.notes = appendNote(ad.notes, options.note);
      fs.writeFileSync(adJsonPath, `${JSON.stringify(ad, null, 2)}\n`, 'utf8');
    }
    const central = readJson(centralJsonPath);
    const result = updateRegister({ ad, central, note: options.note, addMissing: options.addMissing });
    if (result.passed) {
      fs.writeFileSync(centralJsonPath, `${JSON.stringify(result.register, null, 2)}\n`, 'utf8');
    }
    printResult(result, options.json);
    if (!result.passed) process.exitCode = 1;
  } finally {
    lock.release();
  }
}

main();
