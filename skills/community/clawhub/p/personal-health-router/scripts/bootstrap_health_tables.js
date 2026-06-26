#!/usr/bin/env node
const fs = require('fs');
const { spawnSync } = require('child_process');

const DEFAULT_TABLE_SPECS = {
  nutrition_meal: {
    defaultName: 'Nutrition Meals',
    fields: [
      { name: 'Logged At', type: 'datetime', style: { format: 'yyyy-MM-dd HH:mm' } },
      { name: 'Food Description', type: 'text' },
      { name: 'Food Image', type: 'attachment' },
      { name: 'Calories (kcal)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Protein (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Sodium (mg)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Carbs (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Fat (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Fiber (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Estimated Weight (g)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Portion Note', type: 'text' },
      { name: 'Nutrition Summary', type: 'text' },
      { name: 'Confidence', type: 'number', style: { type: 'plain', precision: 2 } },
      { name: 'Note', type: 'text' },
      { name: 'Potassium (mg)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Calcium (mg)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Iron (mg)', type: 'number', style: { type: 'plain', precision: 2 } },
      { name: 'Magnesium (mg)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Vitamin A (μg RAE)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Vitamin C (mg)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Vitamin B1 (mg)', type: 'number', style: { type: 'plain', precision: 3 } },
      { name: 'Vitamin B2 (mg)', type: 'number', style: { type: 'plain', precision: 3 } },
      { name: 'Vitamin B3 (mg)', type: 'number', style: { type: 'plain', precision: 3 } },
      { name: 'Vitamin B6 (mg)', type: 'number', style: { type: 'plain', precision: 3 } },
      { name: 'Folate B9 (μg)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Vitamin B12 (μg)', type: 'number', style: { type: 'plain', precision: 3 } },
    ],
  },
  nutrition_daily_history: {
    defaultName: 'Nutrition Daily History',
    fields: [
      { name: 'Date', type: 'datetime', style: { format: 'yyyy-MM-dd' } },
      { name: 'Daily Conclusion', type: 'text' },
      { name: 'Total Calories (kcal)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Total Protein (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Total Sodium (mg)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Total Carbs (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Total Fat (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Total Fiber (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Metric Assessment', type: 'text' },
      { name: 'Risk Alert', type: 'text' },
      { name: 'Action Advice', type: 'text' },
      { name: 'Meal Summary', type: 'text' },
      { name: 'Analysis Note', type: 'text' },
      { name: 'Reference Calories (kcal)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Reference Sodium (mg)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Reference Fiber (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Reference Carbs (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Reference Protein (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Reference Fat (g)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Reference Vitamin C (mg)', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Reference Iron (mg)', type: 'number', style: { type: 'plain', precision: 2 } },
      { name: 'Reference Vitamin B12 (μg)', type: 'number', style: { type: 'plain', precision: 3 } },
      { name: 'Reference Vitamin B6 (mg)', type: 'number', style: { type: 'plain', precision: 3 } },
    ],
  },
  sleep_recovery: {
    defaultName: 'Sleep Recovery',
    fields: [
      { name: 'Date', type: 'datetime', style: { format: 'yyyy-MM-dd' } },
      {
        name: 'Source App',
        type: 'select',
        multiple: false,
        options: [{ name: 'Apple Health' }, { name: 'Android' }, { name: 'Other', hue: 'Gray', lightness: 'Lighter' }],
      },
      { name: 'Total Sleep', type: 'text' },
      { name: 'Sleep Score', type: 'number', style: { type: 'plain', precision: 0 } },
      {
        name: 'Recovery State',
        type: 'select',
        multiple: false,
        options: [{ name: 'Poor', hue: 'Red', lightness: 'Dark' }, { name: 'Weak', hue: 'Orange', lightness: 'Light' }, { name: 'Average', hue: 'Yellow', lightness: 'Lighter' }, { name: 'Above Average', hue: 'Wathet', lightness: 'Lighter' }, { name: 'Good', hue: 'Green', lightness: 'Lighter' }],
      },
      {
        name: 'Fatigue Risk',
        type: 'select',
        multiple: false,
        options: [{ name: 'Low', hue: 'Green', lightness: 'Light' }, { name: 'Low to Medium', hue: 'Blue', lightness: 'Lighter' }, { name: 'Medium to High', hue: 'Orange', lightness: 'Light' }, { name: 'High', hue: 'Red', lightness: 'Dark' }],
      },
      { name: 'Confidence', type: 'select', multiple: false, options: [{ name: 'Low', hue: 'Gray', lightness: 'Lighter' }, { name: 'Medium', hue: 'Blue', lightness: 'Lighter' }, { name: 'High', hue: 'Green', lightness: 'Lighter' }] },
      { name: 'One-Line Summary', type: 'text' },
      { name: 'Deep Sleep', type: 'text' },
      { name: 'REM Sleep', type: 'text' },
      { name: 'Awake Time', type: 'text' },
      { name: 'Core Sleep', type: 'text' },
      { name: 'Light Sleep', type: 'text' },
      { name: 'Total Sleep Minutes', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Deep Sleep Minutes', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'REM Minutes', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Core/Light Minutes', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'HRV', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Body Signals', type: 'text' },
      { name: 'Advice', type: 'text' },
      { name: 'Reason', type: 'text' },
      { name: 'Missing Fields', type: 'text' },
    ],
  },
  exercise_workout: {
    defaultName: 'Exercise Workouts',
    fields: [
      { name: 'Logged At', type: 'datetime', style: { format: 'yyyy-MM-dd HH:mm' } },
      {
        name: 'Source App',
        type: 'select',
        multiple: false,
        options: [{ name: 'Apple Health' }, { name: 'Strava' }, { name: 'Garmin' }, { name: 'Keep' }, { name: 'Android' }, { name: 'Other', hue: 'Gray', lightness: 'Lighter' }],
      },
      {
        name: 'Workout Type',
        type: 'select',
        multiple: false,
        options: [{ name: 'Running' }, { name: 'Walking' }, { name: 'Cycling' }, { name: 'Strength' }, { name: 'HIIT' }, { name: 'Swimming' }, { name: 'Boxing' }, { name: 'Other', hue: 'Gray', lightness: 'Lighter' }],
      },
      { name: 'Duration', type: 'text' },
      { name: 'Duration Minutes', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Calories (kcal)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Load', type: 'select', multiple: false, options: [{ name: 'Light', hue: 'Wathet', lightness: 'Lighter' }, { name: 'Medium', hue: 'Orange', lightness: 'Lighter' }, { name: 'High', hue: 'Red', lightness: 'Dark' }] },
      { name: 'One-Line Summary', type: 'text' },
      { name: 'Confidence', type: 'select', multiple: false, options: [{ name: 'Low', hue: 'Gray', lightness: 'Lighter' }, { name: 'Medium', hue: 'Blue', lightness: 'Lighter' }, { name: 'High', hue: 'Green', lightness: 'Lighter' }] },
      { name: 'Average HR', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Max HR', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Pace / Speed', type: 'text' },
      { name: 'Distance', type: 'text' },
      { name: 'Distance (km)', type: 'number', style: { type: 'plain', precision: 2 } },
      { name: 'Load Assessment', type: 'text' },
      { name: 'Advice', type: 'text' },
      { name: 'Reason', type: 'text' },
      { name: 'Missing Fields', type: 'text' },
    ],
  },
  monthly_health_calendar: {
    defaultName: 'Monthly Health Calendar',
    views: [{ name: 'Calendar', type: 'calendar' }],
    fields: [
      { name: 'Date', type: 'datetime', style: { format: 'yyyy-MM-dd' } },
      { name: 'Month Key', type: 'text' },
      { name: 'Month Range', type: 'select', multiple: false, options: [{ name: 'Current Month', hue: 'Blue', lightness: 'Lighter' }, { name: 'History', hue: 'Gray', lightness: 'Lighter' }] },
      { name: 'Overall Health Status', type: 'select', multiple: false, options: [{ name: 'Stable', hue: 'Green', lightness: 'Lighter' }, { name: 'Attention', hue: 'Orange', lightness: 'Lighter' }, { name: 'Alert', hue: 'Red', lightness: 'Dark' }] },
      { name: 'Nutrition Status', type: 'select', multiple: false, options: [{ name: 'On Target', hue: 'Green', lightness: 'Lighter' }, { name: 'Low', hue: 'Orange', lightness: 'Lighter' }, { name: 'High', hue: 'Red', lightness: 'Dark' }, { name: 'Missing', hue: 'Gray', lightness: 'Lighter' }] },
      { name: 'Calories Achievement (%)', type: 'number', style: { type: 'plain', precision: 1, percentage: false } },
      { name: 'Protein Achievement (%)', type: 'number', style: { type: 'plain', precision: 1, percentage: false } },
      { name: 'Sodium vs Reference (%)', type: 'number', style: { type: 'plain', precision: 1, percentage: false } },
      { name: 'Nutrition Summary', type: 'text' },
      { name: 'Sleep Score', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Recovery State', type: 'select', multiple: false, options: [{ name: 'Poor', hue: 'Red', lightness: 'Dark' }, { name: 'Weak', hue: 'Orange', lightness: 'Light' }, { name: 'Average', hue: 'Yellow', lightness: 'Lighter' }, { name: 'Above Average', hue: 'Wathet', lightness: 'Lighter' }, { name: 'Good', hue: 'Green', lightness: 'Lighter' }] },
      { name: 'Fatigue Risk', type: 'select', multiple: false, options: [{ name: 'Low', hue: 'Green', lightness: 'Light' }, { name: 'Low to Medium', hue: 'Blue', lightness: 'Lighter' }, { name: 'Medium to High', hue: 'Orange', lightness: 'Light' }, { name: 'High', hue: 'Red', lightness: 'Dark' }] },
      { name: 'Sleep Summary', type: 'text' },
      { name: 'Workout Count', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Workout Minutes', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Workout Calories (kcal)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Workout Status', type: 'select', multiple: false, options: [{ name: 'Rest', hue: 'Gray', lightness: 'Lighter' }, { name: 'Light', hue: 'Wathet', lightness: 'Lighter' }, { name: 'Medium', hue: 'Orange', lightness: 'Lighter' }, { name: 'High Load', hue: 'Red', lightness: 'Dark' }] },
      { name: 'Workout Summary', type: 'text' },
      { name: 'Daily Overview', type: 'text' },
    ],
  },
  weekly_health_assessment: {
    defaultName: 'Weekly Health Assessment',
    fields: [
      { name: 'Week Start', type: 'datetime', style: { format: 'yyyy-MM-dd' } },
      { name: 'Week End', type: 'datetime', style: { format: 'yyyy-MM-dd' } },
      { name: 'Week Key', type: 'text' },
      { name: 'Weekly Health Status', type: 'select', multiple: false, options: [{ name: 'Stable', hue: 'Green', lightness: 'Lighter' }, { name: 'Attention', hue: 'Orange', lightness: 'Lighter' }, { name: 'Alert', hue: 'Red', lightness: 'Dark' }] },
      { name: 'Recorded Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Nutrition Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Sleep Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Workout Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Nutrition On-Target Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Nutrition Low Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Nutrition High Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Attention Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Alert Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Average Sleep Score', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Low Recovery Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'High Fatigue Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Short Sleep Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Severe Short Sleep Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Low Protein Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'High Sodium Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'HRV Recorded Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Active Workout Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'High Load Training Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Total Workout Minutes', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Total Workout Calories (kcal)', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Activity Equivalent Minutes', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Underfueled Training Days', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Poor Recovery After Training Count', type: 'number', style: { type: 'plain', precision: 0 } },
      { name: 'Composite Risk Score', type: 'number', style: { type: 'plain', precision: 1 } },
      { name: 'Nutrition Weekly Review', type: 'text' },
      { name: 'Sleep Weekly Review', type: 'text' },
      { name: 'Workout Weekly Review', type: 'text' },
      { name: 'Cross-Domain Reassessment', type: 'text' },
      { name: 'Risk Focus', type: 'text' },
      { name: 'Next-Week Actions', type: 'text' },
      { name: 'Chat Brief', type: 'text' },
    ],
  },
};

const DEFAULT_RETRY_COUNT = 2;
const DEFAULT_RETRY_DELAY_MS = 800;
const DEFAULT_WRITE_DELAY_MS = 250;

function loadConfig(configPath) {
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

function parseArgs(argv) {
  const args = {
    identity: 'user',
    dryRun: false,
    retryCount: DEFAULT_RETRY_COUNT,
    retryDelayMs: DEFAULT_RETRY_DELAY_MS,
    writeDelayMs: DEFAULT_WRITE_DELAY_MS,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!args.configPath && !token.startsWith('--')) {
      args.configPath = token;
      continue;
    }
    if (token === '--dry-run') {
      args.dryRun = true;
      continue;
    }
    if (token === '--identity') {
      args.identity = argv[i + 1] || 'user';
      i += 1;
      continue;
    }
    if (token === '--retry-count') {
      args.retryCount = Number(argv[i + 1] || DEFAULT_RETRY_COUNT);
      i += 1;
      continue;
    }
    if (token === '--retry-delay-ms') {
      args.retryDelayMs = Number(argv[i + 1] || DEFAULT_RETRY_DELAY_MS);
      i += 1;
      continue;
    }
    if (token === '--write-delay-ms') {
      args.writeDelayMs = Number(argv[i + 1] || DEFAULT_WRITE_DELAY_MS);
      i += 1;
    }
  }
  return args;
}

function normalizeTableName(table) {
  return table?.name || table?.table_name || null;
}

function normalizeTableId(table) {
  return table?.table_id || table?.id || null;
}

function normalizeFieldName(field) {
  return field?.field_name || field?.name || null;
}

function sleepMs(ms) {
  if (!Number.isFinite(ms) || ms <= 0) return;
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

function shouldRetryBaseError(message) {
  if (!message) return false;
  return [
    'FXDB_ERR_TRANSACTION_COMMIT_FAILED',
    'ER_KV_INTERNAL_ERROR',
    '800100001',
    'internal_error',
    'status code: 800004709',
    'timeout',
    'temporarily unavailable',
  ].some((token) => message.includes(token));
}

function runBase(args, identity, options = {}) {
  const fullArgs = ['base', ...args, '--as', identity];
  const retryCount = Number.isFinite(options.retryCount) ? options.retryCount : DEFAULT_RETRY_COUNT;
  const retryDelayMs = Number.isFinite(options.retryDelayMs) ? options.retryDelayMs : DEFAULT_RETRY_DELAY_MS;
  const writeDelayMs = Number.isFinite(options.writeDelayMs) ? options.writeDelayMs : 0;

  for (let attempt = 0; attempt <= retryCount; attempt += 1) {
    const result = spawnSync('lark-cli', fullArgs, { encoding: 'utf8' });
    if (result.status === 0) {
      if (writeDelayMs > 0) {
        sleepMs(writeDelayMs);
      }
      return JSON.parse(result.stdout);
    }

    const message = result.stderr || result.stdout || `lark-cli ${fullArgs.join(' ')} failed`;
    if (attempt < retryCount && shouldRetryBaseError(message)) {
      sleepMs(retryDelayMs * (attempt + 1));
      continue;
    }
    throw new Error(message);
  }
}

function listTables(baseToken, identity, options) {
  return runBase(['+table-list', '--base-token', baseToken], identity, options);
}

function listFields(baseToken, tableId, identity, options) {
  return runBase(['+field-list', '--base-token', baseToken, '--table-id', tableId], identity, options);
}

function createTable(baseToken, name, identity, options) {
  return runBase(['+table-create', '--base-token', baseToken, '--name', name], identity, options);
}

function createField(baseToken, tableId, fieldSpec, identity, options) {
  return runBase([
    '+field-create',
    '--base-token',
    baseToken,
    '--table-id',
    tableId,
    '--json',
    JSON.stringify(fieldSpec),
  ], identity, options);
}

function createViews(baseToken, tableId, views, identity, options) {
  return runBase([
    '+view-create',
    '--base-token',
    baseToken,
    '--table-id',
    tableId,
    '--json',
    JSON.stringify(views),
  ], identity, options);
}

function resolveTableId(createResult) {
  return createResult?.data?.table?.table_id || createResult?.data?.table?.id || createResult?.data?.table_id || createResult?.table?.table_id || null;
}

function getTableSpec(key, tableConfig, config) {
  const fallback = DEFAULT_TABLE_SPECS[key];
  const override = config?.schemas?.[key] || {};
  if (!fallback && !override.fields) {
    throw new Error(`No schema found for table key: ${key}`);
  }
  return {
    key,
    name: tableConfig?.name || override.name || fallback?.defaultName || key,
    fields: override.fields || fallback.fields || [],
    views: override.views || fallback?.views || [],
    existingTableId: tableConfig?.table_id || null,
  };
}

function findTablesByName(existingTables, targetName) {
  const normalizedTarget = String(targetName || '').trim();
  if (!normalizedTarget) return [];
  return existingTables.filter((item) => {
    const name = String(normalizeTableName(item) || '').trim();
    return name === normalizedTarget || name.startsWith(`${normalizedTarget}_conflict_`);
  });
}

function planBootstrap(config) {
  const baseToken = config?.feishu?.active_base?.token;
  const tables = config?.feishu?.tables || {};
  if (!baseToken) {
    throw new Error('config.feishu.active_base.token is required');
  }
  const specs = Object.entries(tables).map(([key, tableConfig]) => getTableSpec(key, tableConfig, config));
  return { baseToken, specs };
}

function executeBootstrap(config, identity, dryRun, runtimeOptions = {}) {
  const { baseToken, specs } = planBootstrap(config);
  const baseOptions = {
    retryCount: runtimeOptions.retryCount,
    retryDelayMs: runtimeOptions.retryDelayMs,
    writeDelayMs: 0,
  };
  const writeOptions = {
    retryCount: runtimeOptions.retryCount,
    retryDelayMs: runtimeOptions.retryDelayMs,
    writeDelayMs: runtimeOptions.writeDelayMs,
  };

  if (dryRun) {
    return {
      ok: true,
      dry_run: true,
      identity,
      base_token_present: Boolean(baseToken),
      tables: specs.map((spec) => ({
        key: spec.key,
        name: spec.name,
        existing_table_id: spec.existingTableId,
        field_count: spec.fields.length,
        views: spec.views,
      })),
    };
  }

  const tablesResp = listTables(baseToken, identity, baseOptions);
  const existingTables = tablesResp?.data?.tables || tablesResp?.data?.items || [];
  const resultTables = [];

  for (const spec of specs) {
    let table = null;
    if (spec.existingTableId) {
      table = existingTables.find((item) => normalizeTableId(item) === spec.existingTableId) || { table_id: spec.existingTableId, table_name: spec.name };
    } else {
      const matchingTables = findTablesByName(existingTables, spec.name);
      const exactMatches = matchingTables.filter((item) => normalizeTableName(item) === spec.name);
      if (matchingTables.length > 1) {
        const candidateIds = matchingTables.map((item) => normalizeTableId(item)).filter(Boolean).join(', ');
        throw new Error(`Ambiguous table name for ${spec.name}. Matching table ids: ${candidateIds}. Pin config.feishu.tables.${spec.key}.table_id before rerunning.`);
      }
      table = exactMatches[0] || matchingTables[0] || null;
    }

    let created = false;
    if (!table) {
      const createResp = createTable(baseToken, spec.name, identity, writeOptions);
      const tableId = resolveTableId(createResp);
      if (!tableId) {
        throw new Error(`Unable to resolve table id for ${spec.name}`);
      }
      table = { table_id: tableId, table_name: spec.name };
      created = true;
      if (spec.views.length > 0) {
        createViews(baseToken, tableId, spec.views, identity, writeOptions);
      }
    }

    const tableId = normalizeTableId(table);
    const fieldResp = listFields(baseToken, tableId, identity, baseOptions);
    const existingFieldNames = new Set((fieldResp?.data?.fields || fieldResp?.data?.items || []).map(normalizeFieldName).filter(Boolean));
    const createdFields = [];

    for (const field of spec.fields) {
      if (existingFieldNames.has(field.name)) {
        continue;
      }
      createField(baseToken, tableId, field, identity, writeOptions);
      createdFields.push(field.name);
    }

    resultTables.push({
      key: spec.key,
      name: spec.name,
      table_id: tableId,
      created,
      created_fields: createdFields,
    });
  }

  return {
    ok: true,
    dry_run: false,
    identity,
    tables: resultTables,
  };
}

function main() {
  const { configPath, identity, dryRun, retryCount, retryDelayMs, writeDelayMs } = parseArgs(process.argv.slice(2));
  if (!configPath) {
    console.error('Usage: node bootstrap_health_tables.js <config.json> [--identity user|bot] [--dry-run] [--retry-count N] [--retry-delay-ms MS] [--write-delay-ms MS]');
    process.exit(1);
  }
  const config = loadConfig(configPath);
  const result = executeBootstrap(config, identity, dryRun, { retryCount, retryDelayMs, writeDelayMs });
  console.log(JSON.stringify(result, null, 2));
}

main();
