#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');

const MIS_ENV = process.env.MIS_ENV_FILE || path.join(os.homedir(), '.openclaw', 'secrets', 'mis.env');
const LOGIN_URL = 'https://online.mis.pens.ac.id/index.php?Login=1&halAwal=1';
const WRAPPER_URL = 'https://online.mis.pens.ac.id/mEntry_Logbook_KP1.php';
const DEFAULT_START = '07:30';
const DEFAULT_END = '16:00';

function loadEnvFile(filePath) {
  const env = {};
  const raw = fs.readFileSync(filePath, 'utf8');
  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const match = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (!match) continue;
    let [, key, value] = match;
    value = value.trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    env[key] = value;
  }
  return env;
}

function requirePlaywright() {
  const candidates = [
    '/usr/lib/node_modules/@playwright/mcp/node_modules/playwright',
    '/usr/lib/node_modules/@executeautomation/playwright-mcp-server/node_modules/playwright',
    '/usr/lib/node_modules/openclaw/node_modules/playwright-core',
  ];
  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch (_) {
      // continue
    }
  }
  throw new Error('Playwright runtime not found in expected global locations');
}

function wibNow() {
  const now = new Date();
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Jakarta',
    day: '2-digit',
    month: 'short',
    year: '2-digit',
  }).formatToParts(now);
  const map = Object.fromEntries(parts.map((p) => [p.type, p.value]));
  return `${map.day}-${map.month.toUpperCase()}-${map.year}`;
}

function normalizeText(text) {
  return (text || '').replace(/\s+/g, ' ').trim();
}

function sanitizeActivity(text) {
  return normalizeText(text).replace(/&/g, 'dan');
}

async function loginIfNeeded(page, creds) {
  await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });

  if (/login\.pens\.ac\.id/.test(page.url())) {
    await page.locator('input[name="username"], input[type="text"]').first().fill(creds.MIS_NETID);
    await page.locator('input[name="password"], input[type="password"]').first().fill(creds.MIS_PASSWORD);
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }).catch(async () => {
        await page.waitForLoadState('networkidle');
      }),
      page.locator('input[name="submit"], input[type="submit"], button[type="submit"]').first().click({ force: true }),
    ]);
  }
}

async function openEntryPage(page) {
  await page.goto(WRAPPER_URL, { waitUntil: 'networkidle' });
}

async function readEntryState(page) {
  return page.evaluate(() => {
    const normalize = (text) => (text || '').replace(/\s+/g, ' ').trim();
    const valueOf = (selector) => document.querySelector(selector)?.value || '';
    const checkedOf = (selector) => Boolean(document.querySelector(selector)?.checked);
    const rowTexts = Array.from(document.querySelectorAll('#tdData table tr'))
      .map((row) => normalize(row.textContent))
      .filter(Boolean);
    const datedRows = rowTexts.filter((row) => /\b\d{2}-[A-Z]{3}-\d{2}\b/i.test(row));
    const saveButton = document.querySelector('#tdData input[type="button"][value="Simpan"]');
    const onclick = saveButton?.getAttribute('onclick') || '';
    const argsMatch = onclick.match(/simpan_data_logbook1\((.*)\)/);
    const rawArgs = argsMatch ? argsMatch[1].split(',').map((part) => part.trim()) : [];
    const bodyText = normalize(document.body.innerText);
    const nrpMatch = onclick.match(/simpan_data_logbook1\((\d+)/)
      || bodyText.match(/NRP\s*\.?\s*(\d{10})/i)
      || bodyText.match(/\((\d{10})\)/);

    return {
      url: location.href,
      title: document.title,
      bodyText,
      brokenOnclick: onclick,
      rows: datedRows,
      fields: {
        nrp: nrpMatch ? nrpMatch[1] : '',
        tahun: rawArgs[1] || valueOf('#tahun'),
        semester: rawArgs[2] || valueOf('#cbSemester'),
        minggu: rawArgs[3] || valueOf('#minggu') || '1',
        tanggal: valueOf('#tanggal'),
        jamMulai: valueOf('#jam_mulai'),
        jamSelesai: valueOf('#jam_selesai'),
        kegiatan: valueOf('#kegiatan'),
        sesuaiKuliahNo: valueOf('#sesuai_kuliah2') || '2',
        sesuaiKuliahYesChecked: checkedOf('#sesuai_kuliah1'),
        matakuliah: valueOf('#matakuliah'),
        setujuChecked: checkedOf('#Setuju'),
        kpDaftar: valueOf('#kp_daftar'),
        mahasiswa: valueOf('#mahasiswa'),
      },
    };
  });
}

async function submitEntry(page, payload) {
  return page.evaluate(async (formPayload) => {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(formPayload)) {
      if (value === undefined || value === null) continue;
      params.append(key, String(value));
    }

    const response = await fetch('entry_logbook_kp1.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      },
      credentials: 'same-origin',
      body: params.toString(),
    });

    const responseText = await response.text();
    const doc = new DOMParser().parseFromString(responseText, 'text/html');
    const normalize = (text) => (text || '').replace(/\s+/g, ' ').trim();
    const rows = Array.from(doc.querySelectorAll('table tr'))
      .map((row) => normalize(row.textContent))
      .filter(Boolean)
      .filter((row) => /\b\d{2}-[A-Z]{3}-\d{2}\b/i.test(row));

    return {
      httpStatus: response.status,
      ok: response.ok,
      responseText,
      bodyText: normalize(doc.body.textContent || ''),
      rows,
    };
  }, payload);
}

async function main() {
  const input = fs.readFileSync(0, 'utf8');
  const activity = sanitizeActivity(input);
  if (!activity) {
    throw new Error('No activity text was provided on stdin');
  }

  if (!fs.existsSync(MIS_ENV)) {
    throw new Error(`Missing MIS env file: ${MIS_ENV}`);
  }

  const creds = loadEnvFile(MIS_ENV);
  if (!creds.MIS_NETID || !creds.MIS_PASSWORD) {
    throw new Error('MIS env file must define MIS_NETID and MIS_PASSWORD');
  }

  const { chromium } = requirePlaywright();
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const page = await browser.newPage();
  page.setDefaultTimeout(30000);
  page.on('dialog', (dialog) => dialog.dismiss().catch(() => {}));

  const todayShort = wibNow();

  try {
    await loginIfNeeded(page, creds);
    await openEntryPage(page);

    const initialState = await readEntryState(page);
    if (!initialState.fields.nrp || !initialState.fields.tanggal) {
      throw new Error('MIS entry page did not expose the expected logbook fields');
    }

    if (initialState.rows.some((row) => row.includes(todayShort))) {
      const existingRow = initialState.rows.find((row) => row.includes(todayShort)) || '';
      console.log(JSON.stringify({
        status: 'duplicate',
        todayShort,
        url: initialState.url,
        title: initialState.title,
        row: existingRow,
      }));
      return;
    }

    const payload = {
      valnrpMahasiswa: initialState.fields.nrp,
      valTahun: initialState.fields.tahun,
      valSemester: initialState.fields.semester,
      Simpan: '1',
      valMinggu: initialState.fields.minggu || '1',
      tanggal: initialState.fields.tanggal,
      jam_mulai: DEFAULT_START,
      jam_selesai: DEFAULT_END,
      kegiatan: activity,
      sesuai_kuliah: initialState.fields.sesuaiKuliahNo || '2',
      matakuliah: '',
      kp_daftar: initialState.fields.kpDaftar,
      mahasiswa: initialState.fields.mahasiswa,
      Setuju: '1',
      sid: Math.random().toString(),
    };

    const submitResult = await submitEntry(page, payload);
    if (!submitResult.ok) {
      throw new Error(`MIS save request failed with HTTP ${submitResult.httpStatus}`);
    }

    await openEntryPage(page);
    const finalState = await readEntryState(page);
    const matchingRow = finalState.rows.find((row) => row.includes(todayShort)) || '';
    const saveMessage = /Simpan Data Berhasil/i.test(submitResult.responseText) ? 'Simpan Data Berhasil' : '';
    const deleteNoise = /Hapus Data Gagal/i.test(submitResult.responseText) || /Hapus Data Gagal/i.test(finalState.bodyText);
    const success = Boolean(saveMessage || matchingRow);

    if (!success) {
      throw new Error('MIS save did not show a success marker or a new row for today');
    }

    console.log(JSON.stringify({
      status: 'success',
      todayShort,
      url: finalState.url,
      title: finalState.title,
      row: matchingRow,
      saveMessage,
      deleteNoise,
      brokenOnclick: initialState.brokenOnclick,
    }));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
