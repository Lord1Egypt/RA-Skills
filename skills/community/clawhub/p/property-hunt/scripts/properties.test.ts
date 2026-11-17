import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { resolveDataDir } from './properties.ts';
import { coerceScraped, readStore, upsertScraped, writeStore } from './store.ts';

const CLI = fileURLToPath(new URL('./properties.ts', import.meta.url));

function tmpdir(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'property-hunt-cli-'));
}

/**
 * Seed a property. scrape.ts owns adding in production (it scrapes and writes
 * in one step), so there is no CLI verb to seed through — tests use the same
 * store functions scrape.ts calls.
 */
function seed(dir: string, over: Record<string, unknown> = {}): void {
  writeStore(dir, upsertScraped(readStore(dir), coerceScraped({ ...LISTING, ...over })));
}

/** Run the CLI the way the agent will: as a subprocess against a real folder. */
function run(dir: string, ...args: string[]): string {
  return execFileSync(process.execPath, [CLI, ...args], {
    env: { ...process.env, PROPERTY_HUNT_DIR: dir },
    encoding: 'utf8',
  });
}

const LISTING = {
  address: '424 28th Street',
  city: 'San Francisco',
  state: 'CA',
  zip: '94131',
  lat: 37.7451548,
  lng: -122.4320644,
  price: 3250000,
  beds: 3,
  baths: 3,
  sqft: 2315,
  property_type: 'SingleFamilyResidence',
  listing_status: 'active',
  listing_url: 'https://www.compass.com/homedetails/424-28th-St-San-Francisco-CA-94131/1QUY9H_pid/',
};

test('the data folder honours an explicit override', () => {
  assert.equal(resolveDataDir({ PROPERTY_HUNT_DIR: '/tmp/somewhere' } as NodeJS.ProcessEnv), '/tmp/somewhere');
});

test('a Mac with no agent mount falls back to the Plow folder', () => {
  const resolved = resolveDataDir({} as NodeJS.ProcessEnv);
  assert.ok(
    resolved === path.join(os.homedir(), 'Plow', 'properties') || resolved === '/workspace/host/properties',
    `unexpected default ${resolved}`,
  );
});

test('init scaffolds a folder the frontend can actually load', () => {
  const dir = tmpdir();
  run(dir, 'init');
  for (const expected of ['data.js', 'index.html', 'photos', 'vendor']) {
    assert.ok(fs.existsSync(path.join(dir, expected)), `init must produce ${expected}`);
  }
  assert.match(fs.readFileSync(path.join(dir, 'data.js'), 'utf8'), /^window\.PROPERTIES =/);
});

test('init never destroys properties already collected', () => {
  const dir = tmpdir();
  run(dir, 'init');
  seed(dir);
  run(dir, 'set', '424-28th-st-94131-ca', 'notes', 'keep me');

  run(dir, 'init'); // e.g. after a skill upgrade

  const after = JSON.parse(run(dir, 'list', '--json'));
  assert.equal(after.length, 1);
  assert.equal(after[0].mine.notes, 'keep me');
});

test('the add-then-annotate-then-refresh flow a user actually does', () => {
  const dir = tmpdir();
  run(dir, 'init');

  seed(dir);

  const id = '424-28th-st-94131-ca';
  run(dir, 'set', id, 'rating', '4');
  run(dir, 'set', id, 'notes', 'sweeping views, needs a new roof');
  run(dir, 'set', id, 'status', 'toured');

  // Price cut — the agent re-scrapes.
  seed(dir, { price: 2950000 });

  const [row] = JSON.parse(run(dir, 'list', '--json'));
  assert.equal(row.scraped.price, 2950000);
  assert.equal(row.mine.rating, 4);
  assert.equal(row.mine.notes, 'sweeping views, needs a new roof');
  assert.equal(row.mine.status, 'toured');

  assert.match(run(dir, 'list'), /\n1 property\n/, 'one house is not "1 properties"');
});

test('multi-word notes survive the shell without quoting gymnastics', () => {
  const dir = tmpdir();
  run(dir, 'init');
  seed(dir);
  run(dir, 'set', '424-28th-st-94131-ca', 'notes', 'needs', 'a', 'new', 'roof');
  const [row] = JSON.parse(run(dir, 'list', '--json'));
  assert.equal(row.mine.notes, 'needs a new roof');
});

test('operating on a store that does not exist yet says what to do', () => {
  const dir = tmpdir();
  assert.throws(() => run(dir, 'list'), /init/);
});

test('rm deletes the property and its photo', () => {
  const dir = tmpdir();
  run(dir, 'init');
  seed(dir, { photo: 'photos/x.jpg' });
  fs.writeFileSync(path.join(dir, 'photos', 'x.jpg'), 'jpegbytes');

  run(dir, 'rm', '424-28th-st-94131-ca');

  assert.deepEqual(JSON.parse(run(dir, 'list', '--json')), []);
  assert.equal(fs.existsSync(path.join(dir, 'photos', 'x.jpg')), false, 'the photo is orphaned otherwise');
});

test('an unknown id lists the ids that do exist', () => {
  const dir = tmpdir();
  run(dir, 'init');
  seed(dir);
  assert.throws(() => run(dir, 'get', 'wrong-house'), /424-28th-st-94131-ca/);
});
