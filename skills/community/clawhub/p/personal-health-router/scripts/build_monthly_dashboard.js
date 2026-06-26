#!/usr/bin/env node
const fs = require('fs');
const { spawnSync } = require('child_process');

function parseArgs(argv) {
  const args = { identity: 'user', themeStyle: 'summerBreeze' };
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--help' || token === '-h') {
      args.help = true;
      continue;
    }
    if (!args.config && !token.startsWith('--')) {
      args.config = token;
      continue;
    }
    if (token === '--identity') {
      args.identity = argv[++i];
      continue;
    }
    if (token === '--dashboard-name') {
      args.dashboardName = argv[++i];
      continue;
    }
    if (token === '--theme-style') {
      args.themeStyle = argv[++i];
      continue;
    }
    if (token === '--dry-run') {
      args.dryRun = true;
      continue;
    }
    if (token === '--json') {
      args.json = true;
      continue;
    }
    throw new Error(`Unknown arg: ${token}`);
  }
  if (!args.config && !args.help) {
    throw new Error('Usage: node build_monthly_dashboard.js <config.json> [--identity user|bot] [--dashboard-name NAME] [--theme-style STYLE] [--dry-run] [--json]');
  }
  return args;
}

function printHelp() {
  console.log('Usage: node build_monthly_dashboard.js <config.json> [--identity user|bot] [--dashboard-name NAME] [--theme-style STYLE] [--dry-run] [--json]');
}

function loadConfig(configPath) {
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

function runJson(cmd, { allowEmpty = false } = {}) {
  const proc = spawnSync(cmd[0], cmd.slice(1), { encoding: 'utf8' });
  if (proc.status !== 0) {
    throw new Error((proc.stderr || proc.stdout || `Command failed: ${cmd.join(' ')}`).trim());
  }
  const stdout = (proc.stdout || '').trim();
  if (!stdout) {
    if (allowEmpty) return {};
    throw new Error(`Empty JSON output from command: ${cmd.join(' ')}`);
  }
  return JSON.parse(stdout);
}

function larkJson(args, extra = {}) {
  return runJson(['lark-cli', ...args], extra);
}

const MONTHLY_FIELDS = {
  date: ['Date'],
  range: ['Month Range'],
  overall: ['Overall Health Status'],
  nutritionStatus: ['Nutrition Status'],
  sleepScore: ['Sleep Score'],
  recovery: ['Recovery State'],
  workoutCount: ['Workout Count'],
  workoutMinutes: ['Workout Minutes'],
  calorieRatio: ['Calories Achievement (%)'],
  proteinRatio: ['Protein Achievement (%)'],
  workoutStatus: ['Workout Status'],
};

const MONTHLY_VALUES = {
  currentMonth: ['Current Month'],
  onTarget: ['On Target'],
};

const BLOCK_I18N = {
  en: {
    dashboardName: 'Monthly Health Calendar Overview',
    aboutName: 'About This Dashboard',
    aboutText: [
      '# Monthly Health Calendar Overview',
      '- Source: Monthly Health Calendar',
      '- Scope: current-month rows only',
      '- Use this dashboard to scan stability, recovery, and workout rhythm day by day.',
    ].join('\n'),
    recordedDays: 'Current-Month Recorded Days',
    nutritionOnTargetDays: 'Current-Month Nutrition On-Target Days',
    avgSleepScore: 'Current-Month Average Sleep Score',
    activeWorkoutDays: 'Current-Month Active Workout Days',
    overallDistribution: 'Current-Month Overall Health Status Distribution',
    sleepTrend: 'Current-Month Sleep Score Trend',
    workoutTrend: 'Current-Month Workout Minutes Trend',
    nutritionTrend: 'Current-Month Nutrition Achievement Trend',
    recoveryDistribution: 'Current-Month Recovery State Distribution',
    workoutDistribution: 'Current-Month Workout Status Distribution',
  },
};

const BLOCK_LABEL_KEYS = [
  'aboutName',
  'aboutText',
  'recordedDays',
  'nutritionOnTargetDays',
  'avgSleepScore',
  'activeWorkoutDays',
  'overallDistribution',
  'sleepTrend',
  'workoutTrend',
  'nutritionTrend',
  'recoveryDistribution',
  'workoutDistribution',
];

function mustGet(object, path, label) {
  const value = path.reduce((acc, key) => (acc == null ? undefined : acc[key]), object);
  if (value == null) {
    throw new Error(`Missing ${label}`);
  }
  return value;
}

function listTableSnapshot(baseToken, identity, tableRef) {
  const payload = larkJson([
    'base', '+record-list',
    '--as', identity,
    '--base-token', baseToken,
    '--table-id', tableRef,
    '--offset', '0',
    '--limit', '200',
  ]);
  const data = payload.data || {};
  const fieldNames = data.fields || [];
  const rows = (data.data || []).map((row) => {
    const mapped = {};
    fieldNames.forEach((field, index) => {
      mapped[field] = row[index];
    });
    return mapped;
  });
  return { fieldNames, rows };
}

function normalizeValue(value) {
  if (Array.isArray(value)) {
    if (value.length === 1 && typeof value[0] !== 'object') return value[0];
    if (value.length && value[0] && typeof value[0] === 'object' && 'text' in value[0]) {
      return value.map((item) => String(item.text || '')).join('');
    }
  }
  return value;
}

function resolveFields(fieldNames) {
  const resolved = {};
  for (const [key, aliases] of Object.entries(MONTHLY_FIELDS)) {
    resolved[key] = aliases.find((name) => fieldNames.includes(name)) || aliases[0];
  }
  return resolved;
}

function resolveValue(candidates, values, fallbackIndex = 0) {
  for (const candidate of candidates) {
    if (values.includes(candidate)) return candidate;
  }
  return candidates[fallbackIndex] || candidates[0];
}

function detectLocale() {
  return 'en';
}

function getDashboardConfig(config) {
  return config.dashboard || config.dashboards || {};
}

function resolveDashboardLabels(config, locale) {
  const dashboardConfig = getDashboardConfig(config);
  const localeConfig = dashboardConfig.locale_labels || dashboardConfig.localeLabels || {};
  const named = dashboardConfig.monthly_health_calendar || dashboardConfig.monthlyHealthCalendar || {};
  const namedLocale = (named.locale_labels || named.localeLabels || {});

  const base = { ...(BLOCK_I18N[locale] || BLOCK_I18N.en) };
  const merges = [localeConfig[locale], localeConfig.default, namedLocale[locale], namedLocale.default, named];
  for (const source of merges) {
    if (!source || typeof source !== 'object') continue;
    for (const key of ['dashboardName', ...BLOCK_LABEL_KEYS]) {
      if (source[key] != null) base[key] = source[key];
    }
  }
  return base;
}

function listDashboards(baseToken, identity) {
  const items = [];
  let pageToken;
  do {
    const cmd = ['base', '+dashboard-list', '--as', identity, '--base-token', baseToken];
    if (pageToken) cmd.push('--page-token', pageToken);
    const payload = larkJson(cmd);
    const data = payload.data || {};
    items.push(...(data.items || []));
    pageToken = data.has_more ? data.page_token : null;
  } while (pageToken);
  return items;
}

function listBlocks(baseToken, identity, dashboardId) {
  const items = [];
  let pageToken;
  do {
    const cmd = ['base', '+dashboard-block-list', '--as', identity, '--base-token', baseToken, '--dashboard-id', dashboardId];
    if (pageToken) cmd.push('--page-token', pageToken);
    const payload = larkJson(cmd);
    const data = payload.data || {};
    items.push(...(data.items || []));
    pageToken = data.has_more ? data.page_token : null;
  } while (pageToken);
  return items;
}

function findUnique(items, predicate, label) {
  const matches = items.filter(predicate);
  if (matches.length > 1) {
    throw new Error(`Ambiguous ${label}: ${matches.map((item) => item.block_id || item.dashboard_id || item.name).join(', ')}`);
  }
  return matches[0] || null;
}

function ensureDashboard(baseToken, identity, name, themeStyle, dryRun) {
  const dashboards = listDashboards(baseToken, identity);
  const existing = findUnique(dashboards, (item) => item.name === name, `dashboard name ${name}`);
  if (existing) {
    return { dashboardId: existing.dashboard_id, created: false };
  }
  if (dryRun) {
    return { dashboardId: null, created: true, dryRunPlanned: true };
  }
  const payload = larkJson([
    'base', '+dashboard-create',
    '--as', identity,
    '--base-token', baseToken,
    '--name', name,
    '--theme-style', themeStyle,
  ]);
  const dashboard = mustGet(payload, ['data', 'dashboard'], 'dashboard create response');
  return { dashboardId: dashboard.dashboard_id, created: true };
}

function dashboardBlocks(tableName, resolvedFields, resolvedValues, labels) {
  const currentMonthFilter = {
    conjunction: 'and',
    conditions: [
      { field_name: resolvedFields.range, operator: 'is', value: resolvedValues.currentMonth },
    ],
  };

  return [
    {
      name: labels.aboutName,
      type: 'text',
      dataConfig: {
        text: labels.aboutText,
      },
    },
    {
      name: labels.recordedDays,
      type: 'statistics',
      dataConfig: { table_name: tableName, count_all: true, filter: currentMonthFilter },
    },
    {
      name: labels.nutritionOnTargetDays,
      type: 'statistics',
      dataConfig: {
        table_name: tableName,
        count_all: true,
        filter: {
          conjunction: 'and',
          conditions: [
            { field_name: resolvedFields.range, operator: 'is', value: resolvedValues.currentMonth },
            { field_name: resolvedFields.nutritionStatus, operator: 'is', value: resolvedValues.onTarget },
          ],
        },
      },
    },
    {
      name: labels.avgSleepScore,
      type: 'statistics',
      dataConfig: {
        table_name: tableName,
        filter: currentMonthFilter,
        series: [{ field_name: resolvedFields.sleepScore, rollup: 'AVERAGE' }],
      },
    },
    {
      name: labels.activeWorkoutDays,
      type: 'statistics',
      dataConfig: {
        table_name: tableName,
        count_all: true,
        filter: {
          conjunction: 'and',
          conditions: [
            { field_name: resolvedFields.range, operator: 'is', value: resolvedValues.currentMonth },
            { field_name: resolvedFields.workoutCount, operator: 'isGreater', value: 0 },
          ],
        },
      },
    },
    {
      name: labels.overallDistribution,
      type: 'pie',
      dataConfig: {
        table_name: tableName,
        count_all: true,
        filter: currentMonthFilter,
        group_by: [{ field_name: resolvedFields.overall, mode: 'integrated', sort: { type: 'group', order: 'asc' } }],
      },
    },
    {
      name: labels.sleepTrend,
      type: 'line',
      dataConfig: {
        table_name: tableName,
        filter: currentMonthFilter,
        series: [{ field_name: resolvedFields.sleepScore, rollup: 'AVERAGE' }],
        group_by: [{ field_name: resolvedFields.date, mode: 'integrated', sort: { type: 'group', order: 'asc' } }],
      },
    },
    {
      name: labels.workoutTrend,
      type: 'column',
      dataConfig: {
        table_name: tableName,
        filter: currentMonthFilter,
        series: [{ field_name: resolvedFields.workoutMinutes, rollup: 'SUM' }],
        group_by: [{ field_name: resolvedFields.date, mode: 'integrated', sort: { type: 'group', order: 'asc' } }],
      },
    },
    {
      name: labels.nutritionTrend,
      type: 'combo',
      dataConfig: {
        table_name: tableName,
        filter: currentMonthFilter,
        series: [
          { field_name: resolvedFields.calorieRatio, rollup: 'AVERAGE' },
          { field_name: resolvedFields.proteinRatio, rollup: 'AVERAGE' },
        ],
        group_by: [{ field_name: resolvedFields.date, mode: 'integrated', sort: { type: 'group', order: 'asc' } }],
      },
    },
    {
      name: labels.recoveryDistribution,
      type: 'pie',
      dataConfig: {
        table_name: tableName,
        count_all: true,
        filter: currentMonthFilter,
        group_by: [{ field_name: resolvedFields.recovery, mode: 'integrated', sort: { type: 'group', order: 'asc' } }],
      },
    },
    {
      name: labels.workoutDistribution,
      type: 'pie',
      dataConfig: {
        table_name: tableName,
        count_all: true,
        filter: currentMonthFilter,
        group_by: [{ field_name: resolvedFields.workoutStatus, mode: 'integrated', sort: { type: 'group', order: 'asc' } }],
      },
    },
  ];
}

function ensureBlock(baseToken, identity, dashboardId, existingBlocks, spec, dryRun) {
  const exact = existingBlocks.filter((item) => item.name === spec.name);
  if (exact.length > 1) {
    throw new Error(`Ambiguous block name ${spec.name}: ${exact.map((item) => item.block_id).join(', ')}`);
  }
  const existing = exact[0];
  if (!existing) {
    if (dryRun) {
      return { action: 'create', name: spec.name, type: spec.type, block_id: null };
    }
    const payload = larkJson([
      'base', '+dashboard-block-create',
      '--as', identity,
      '--base-token', baseToken,
      '--dashboard-id', dashboardId,
      '--name', spec.name,
      '--type', spec.type,
      '--data-config', JSON.stringify(spec.dataConfig),
    ]);
    const block = mustGet(payload, ['data', 'block'], `created block ${spec.name}`);
    return { action: 'created', name: spec.name, type: spec.type, block_id: block.block_id };
  }

  if (existing.type !== spec.type) {
    throw new Error(`Block type mismatch for ${spec.name}: existing=${existing.type}, expected=${spec.type}`);
  }

  if (dryRun) {
    return { action: 'update', name: spec.name, type: spec.type, block_id: existing.block_id };
  }

  larkJson([
    'base', '+dashboard-block-update',
    '--as', identity,
    '--base-token', baseToken,
    '--dashboard-id', dashboardId,
    '--block-id', existing.block_id,
    '--name', spec.name,
    '--data-config', JSON.stringify(spec.dataConfig),
  ]);
  return { action: 'updated', name: spec.name, type: spec.type, block_id: existing.block_id };
}

function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    return;
  }
  const config = loadConfig(args.config);
  const baseToken = mustGet(config, ['feishu', 'active_base', 'token'], 'feishu.active_base.token');
  const monthly = mustGet(config, ['feishu', 'tables', 'monthly_health_calendar'], 'feishu.tables.monthly_health_calendar');
  const tableName = monthly.name;
  const tableRef = monthly.table_id || monthly.name;
  const snapshot = listTableSnapshot(baseToken, args.identity, tableRef);
  const resolvedFields = resolveFields(snapshot.fieldNames);
  const locale = detectLocale(resolvedFields);
  const labels = resolveDashboardLabels(config, locale);
  const dashboardName = args.dashboardName || labels.dashboardName;
  const monthRangeValues = snapshot.rows.map((row) => normalizeValue(row[resolvedFields.range])).filter((value) => value != null && value !== '');
  const nutritionStatusValues = snapshot.rows.map((row) => normalizeValue(row[resolvedFields.nutritionStatus])).filter((value) => value != null && value !== '');
  const resolvedValues = {
    currentMonth: resolveValue(MONTHLY_VALUES.currentMonth, monthRangeValues, 0),
    onTarget: resolveValue(MONTHLY_VALUES.onTarget, nutritionStatusValues, 0),
  };

  const dashboard = ensureDashboard(baseToken, args.identity, dashboardName, args.themeStyle, args.dryRun);
  const existingBlocks = dashboard.dashboardId ? listBlocks(baseToken, args.identity, dashboard.dashboardId) : [];
  const ops = [];
  for (const spec of dashboardBlocks(tableName, resolvedFields, resolvedValues, labels)) {
    ops.push(ensureBlock(baseToken, args.identity, dashboard.dashboardId, existingBlocks, spec, args.dryRun));
  }

  const result = {
    ok: true,
    dry_run: Boolean(args.dryRun),
    identity: args.identity,
    locale,
    dashboard_name: dashboardName,
    dashboard_id: dashboard.dashboardId,
    dashboard_created: dashboard.created,
    target_table: tableName,
    block_count: ops.length,
    blocks: ops,
  };

  console.log(JSON.stringify(result, null, 2));
}

main();
