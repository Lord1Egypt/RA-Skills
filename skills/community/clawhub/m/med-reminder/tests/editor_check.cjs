/*
 * editor_check.cjs — drive editor.html's real <script> under a stub DOM.
 *
 * Scenarios (exit 0 = pass):
 *   save-fresh   open → save → the write happens and the mtime baseline re-syncs
 *   save-stale   open → the file changes on disk → save is REFUSED (M4, issue #1 §2)
 *   passthrough  edit a med → optional fields the form doesn't know survive
 *   multi-day    weekly day list → canonical sorted array written; an empty
 *                day selection is refused before anything changes
 *   calculator   syringe-unit math matches reconstitution.py; the syringe
 *                field saves/clears and validates (PR 8a, #10)
 *
 * The script source is eval'd together with the scenario driver so the
 * driver sees the eval scope (let/const declarations stay inside it).
 */
const fs = require('fs');
const path = require('path');

const scenario = process.argv[2];
const html = fs.readFileSync(path.join(__dirname, '..', 'editor.html'), 'utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) { console.error('no <script> block found in editor.html'); process.exit(2); }

// ── stub DOM ────────────────────────────────────────────────────────────────
const els = new Map();
function el(id) {
  if (!els.has(id)) {
    els.set(id, {
      value: '', checked: false, innerHTML: '', textContent: '',
      className: '', disabled: false, style: {},
      classList: { add() {}, remove() {}, contains() { return false; } },
      appendChild() {}, addEventListener() {}, scrollIntoView() {},
      options: [], selectedOptions: [],   // the multi-select day picker (PR 7)
    });
  }
  return els.get(id);
}
// querySelectorAll results a driver can inject (e.g. the weekly form's
// time-row inputs); anything unregistered matches nothing, as before.
const queried = {};
globalThis.document = {
  getElementById: el,
  createElement: () => el('created-' + els.size),
  querySelectorAll: (sel) => queried[sel] || [],
  addEventListener() {},
};
globalThis.window = globalThis;
globalThis.confirm = () => true;

// ── scenario state ──────────────────────────────────────────────────────────
const result = { writes: 0, failed: false };
let lastMod = 1000;
const STATE = JSON.stringify({
  version: '1',
  global: {
    timezone: 'America/Los_Angeles',
    quiet_hours: { start: '22:00', end: '07:00' },
    paused: false, digest_time: '08:00', delivery_channel: 'whatsapp',
    log_redact: true,
  },
  tick: { watermark_utc: '2026-04-21T15:00:00+00:00' },
  meds: [{
    id: 'med-001', name: 'Metformin', type: 'pill', dose: '500', unit: 'mg',
    paused: false,
    min_gap_hours: 6,
    active_since_utc: '2026-04-21T13:00:00+00:00',
    start_date: '2026-04-22', end_date: '2026-04-29',
    schedule: { frequency: 'interval', interval_hours: 8, day_of_week: null,
                with_food: false, notes: '', quiet_policy: 'shift' },
    escalation: { late_threshold_minutes: 30, missed_threshold_minutes: 90,
                  late_message: 'Late: {name}', missed_message: 'Missed: {name}' },
    state: { status: 'pending', last_taken: null, last_reminded: null,
             next_due: '2026-04-21T20:00:00+00:00', confirmed_dose: null,
             missed_count: 0, history: [] },
  }],
});
const file = {
  name: 'meds-state.json',
  get lastModified() { return lastMod; },
  async text() { return STATE; },
};
const writable = {
  async write() { result.writes++; },
  async close() {},
};
const handle = {
  async getFile() { return file; },
  async createWritable() { return writable; },
};
globalThis.showOpenFilePicker = async () => [handle];
globalThis.showSaveFilePicker = async () => handle;

function assert(cond, msg) {
  if (!cond) { console.error('ASSERT FAILED: ' + msg); result.failed = true; }
}

// ── scenarios (source-injected into the eval scope) ─────────────────────────
async function drvSaveFresh() {
  await openFile();
  assert(currentState !== null, 'state loaded');
  assert(openedLastModified === lastMod, 'baseline recorded at open');
  await saveFile();
  assert(result.writes === 1, 'save wrote the file (writes=' + result.writes + ')');
  assert(openedLastModified === lastMod, 'baseline re-synced after own write');
}

async function drvSaveStale() {
  await openFile();
  lastMod = 2000;   // the tick / reply.py replaced the file while it was open
  await saveFile();
  assert(result.writes === 0, 'stale save refused (writes=' + result.writes + ')');
  const status = el('status').textContent;
  assert(/changed on disk/i.test(status), 'refusal explains the problem: ' + status);
  assert(el('status').className === 'err', 'refusal is an error status');
}

async function drvPassthrough() {
  await openFile();
  openEditMed('med-001');
  el('f-name').value = 'Metformin XR';
  saveMed();
  const med = currentState.meds[0];
  assert(med.name === 'Metformin XR', 'name edited');
  assert(med.schedule.quiet_policy === 'shift', 'unknown schedule field preserved');
  assert(med.schedule.interval_hours === 8, 'known schedule field intact');
  assert(med.min_gap_hours === 6, 'unknown med-level field preserved');
  assert(med.active_since_utc === '2026-04-21T13:00:00+00:00', 'active_since preserved');
  assert(med.start_date === '2026-04-22' && med.end_date === '2026-04-29',
         'date-range bounds preserved (PR 6)');
  assert(med.state.status === 'pending', 'runtime state block preserved');
  assert(currentState.tick.watermark_utc === '2026-04-21T15:00:00+00:00',
         'top-level tick block preserved');
  assert(currentState.global.log_redact === true, 'unknown global field preserved');
}

async function drvMultiDay() {
  await openFile();
  // hand-edit the disk state to a multi-day weekly schedule in non-canonical
  // order — the way a text editor would leave it
  currentState.meds[0].schedule = { frequency: 'weekly', times: ['09:00'],
                                    interval_hours: null, day_of_week: ['sat','tue'],
                                    with_food: false, notes: '', quiet_policy: 'shift' };
  let errs = validate(currentState);
  assert(errs.some(e => /sorted mon\.\.sun/.test(e)),
         'non-canonical day list flagged: ' + errs.join(' | '));

  // the modal's time rows live in the DOM — inject one 09:00 input
  queried['#f-times-list input[type=time]'] = [{ value: '09:00' }];
  openEditMed('med-001');
  el('f-day').selectedOptions = [{ value: 'tue' }, { value: 'sat' }];
  saveMed();
  const med = currentState.meds[0];
  assert(Array.isArray(med.schedule.day_of_week)
         && med.schedule.day_of_week.join() === 'tue,sat',
         'saved as canonical sorted array: ' + JSON.stringify(med.schedule.day_of_week));
  assert(med.schedule.quiet_policy === 'shift', 'unknown schedule field still preserved');
  errs = validate(currentState);
  assert(errs.length === 0, 'state with day array validates: ' + errs.join(' | '));

  // an empty day selection is refused before anything is written
  openEditMed('med-001');
  el('f-day').selectedOptions = [];
  saveMed();
  assert(/Pick at least one day/.test(el('f-form-errors').textContent),
         'empty day selection refused: ' + el('f-form-errors').textContent);
  assert(currentState.meds[0].schedule.day_of_week.join() === 'tue,sat',
         'refused save left the schedule untouched');
}

async function drvCalculator() {
  let d = computeDraw(250, 5, 2, 'U-100');
  assert(d.units === 10 && d.warnings.length === 0, 'U-100 worked example: ' + JSON.stringify(d));
  assert(computeDraw(250, 5, 2, 'U-50').units === 5, 'U-50 is half the units');
  d = computeDraw(320, 10, 2, 'U-100');
  assert(d.units === 6 && /off the exact 6\.4/.test(d.warnings[0] || ''), 'rounding warning: ' + d.warnings);
  assert(computeDraw(250, 10, 3, 'U-100').units === 8, 'half unit rounds up');
  assert(doseMcg('0.25', 'mg') === 250 && doseMcg('15', 'units') === null, 'dose units');

  await openFile();
  openEditMed('med-001');
  el('f-dose').value = '250'; el('f-unit').value = 'mcg';
  el('calc-vial').value = '5'; el('calc-dil').value = '2';
  calcUnits();
  assert(/250mcg = 10 units on a U-100/.test(el('calc-out').textContent),
         'scratch calculator output: ' + el('calc-out').textContent);
  el('f-syringe').value = 'U-50';
  calcUnits();
  assert(/= 5 units on a U-50/.test(el('calc-out').textContent), 'calculator follows syringe');
  saveMed();
  assert(currentState.meds[0].syringe === 'U-50', 'syringe saved');
  assert(validate(currentState).length === 0, 'state with syringe validates');
  assert(!('calc_vial' in currentState.meds[0]) && !('vial_mg' in currentState.meds[0]),
         'calculator persists nothing');

  openEditMed('med-001');
  assert(el('f-syringe').value === 'U-50', 'syringe loaded into the form');
  el('f-syringe').value = '';
  saveMed();
  assert(!('syringe' in currentState.meds[0]), 'default clears the field');

  currentState.meds[0].syringe = 'U-40';
  assert(validate(currentState).some(e => /syringe/.test(e)), 'bad syringe flagged');
}

async function drvSupplies() {
  await openFile();
  openEditMed('med-001');
  el('f-inv-unit').value = 'tablet'; el('f-reorder').value = '14'; el('f-dpu').value = '';
  saveMed();
  let med = currentState.meds[0];
  assert(med.inventory_unit === 'tablet' && med.reorder_when_below_days === 14,
         'supplies saved: ' + JSON.stringify(med));
  assert(!('doses_per_unit' in med), 'empty doses-per-unit not written');
  assert(validate(currentState).length === 0, 'state with supplies validates');

  openEditMed('med-001');
  assert(el('f-inv-unit').value === 'tablet', 'inventory unit loaded into the form');
  el('f-reorder').value = '2.5';
  saveMed();
  assert(/whole number of days/.test(el('f-form-errors').textContent), 'fractional reorder refused');
  assert(currentState.meds[0].reorder_when_below_days === 14, 'refused save changed nothing');

  openEditMed('med-001');
  el('f-inv-unit').value = ''; el('f-reorder').value = '';
  saveMed();
  med = currentState.meds[0];
  assert(!('inventory_unit' in med) && !('reorder_when_below_days' in med), 'clearing removes the fields');

  currentState.meds[0].doses_per_unit = 0;
  assert(validate(currentState).some(e => /doses_per_unit/.test(e)), 'bad doses_per_unit flagged');
}

const DRIVERS = {
  'save-fresh': drvSaveFresh,
  'save-stale': drvSaveStale,
  'passthrough': drvPassthrough,
  'multi-day': drvMultiDay,
  'calculator': drvCalculator,
  'supplies': drvSupplies,
};
const driver = DRIVERS[scenario];
if (!driver) { console.error('unknown scenario: ' + scenario); process.exit(2); }

// The editor script references `el`, `result` etc. through the eval's scope
// chain, so the driver body is appended to the eval'd source.
eval(
  m[1] +
  '\n;(async () => { await (' + driver.toString() + ')(); })()' +
  '.then(() => { process.exit(result.failed ? 1 : 0); },' +
  '        (e) => { console.error(e && e.stack || e); process.exit(2); });'
);
