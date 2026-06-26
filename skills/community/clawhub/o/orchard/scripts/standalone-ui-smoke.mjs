#!/usr/bin/env node

const DEFAULT_BASE_URL = 'http://127.0.0.1:18790';

function fail(message, extra) {
  console.error(`FAIL: ${message}`);
  if (extra) console.error(extra);
  process.exitCode = 1;
}

function ok(message, extra = '') {
  console.log(`OK: ${message}${extra ? ` — ${extra}` : ''}`);
}

function parseArgs(argv) {
  const args = { baseUrl: DEFAULT_BASE_URL, token: '' };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--base-url') args.baseUrl = argv[++i];
    else if (arg === '--token') args.token = argv[++i];
  }
  return args;
}

async function request(url, { token = '', ...opts } = {}) {
  const headers = {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(opts.headers || {}),
  };
  const res = await fetch(url, { ...opts, headers });
  const text = await res.text();
  let body = text;
  try { body = text ? JSON.parse(text) : null; } catch {}
  return { res, body, text };
}

function assert(cond, message, extra = '') {
  if (cond) ok(message, extra);
  else fail(message, extra);
}

function taskCounts(tasks) {
  const counts = { total: tasks.length, ready: 0, running: 0, done: 0 };
  for (const task of tasks) {
    if (task?.status === 'ready') counts.ready++;
    if (task?.status === 'running') counts.running++;
    if (task?.status === 'done') counts.done++;
  }
  return counts;
}

function progressFromTasks(tasks) {
  const counts = taskCounts(tasks);
  const pct = counts.total ? Math.round((counts.done / counts.total) * 100) : 0;
  return { counts, pct };
}

const args = parseArgs(process.argv.slice(2));
const token = args.token;
const baseUrl = args.baseUrl.replace(/\/$/, '');
const regressions = [];

function check(cond, message, extra = '') {
  if (cond) ok(message, extra);
  else {
    regressions.push(`${message}${extra ? ` (${extra})` : ''}`);
    fail(message, extra);
  }
}

console.log(`Smoke testing Orchard standalone UI at ${baseUrl}`);

if (!token) {
  console.error('FAIL: No gateway token available. Pass --token <gateway-token>.');
  process.exit(2);
}

const root = await request(`${baseUrl}/`);
check(root.res.status === 200, 'Standalone UI root responds', `status=${root.res.status}`);
check(typeof root.text === 'string' && root.text.includes('<title>OrchardOS</title>'), 'Standalone UI HTML shell served');
check(root.text.includes("const AUTH_INJECTED = '';"), 'Standalone HTML does not embed a gateway token');
check(root.text.includes('Enter your OpenClaw gateway token to continue'), 'Token entry flow is present in standalone HTML');
check(root.text.includes("localStorage.getItem('orchard-token')"), 'Standalone HTML reads auth token from localStorage');
check(root.text.includes('refreshDashboardDataSilently') && root.text.includes('setInterval(() => {') && root.text.includes('30000'), 'Silent refresh loop is present');
check(root.text.includes('updateLastUpdated()'), 'Last-updated timestamp hook is present');
check(root.text.includes("id=\"sidebar-projects\""), 'Sidebar project list container exists');
check(root.text.includes('session-pill'), 'Sessions pill markup exists');
check(root.text.includes('kanban-columns'), 'Board columns markup exists');
check(root.text.includes('progress-fill'), 'Progress bar markup exists');

const unauthProjects = await request(`${baseUrl}/orchard/projects`);
check(unauthProjects.res.status === 401, 'Projects API rejects unauthenticated access', `status=${unauthProjects.res.status}`);

const projectsResp = await request(`${baseUrl}/orchard/projects`, { token });
check(projectsResp.res.status === 200, 'Projects API accepts authenticated access', `status=${projectsResp.res.status}`);
const projects = Array.isArray(projectsResp.body) ? projectsResp.body : [];
check(projects.length > 0, 'Projects API returns live project data', `count=${projects.length}`);

const targetProject = projects.find((p) => p?.id === 'orchard-hardening') || projects[0];
check(!!targetProject?.id, 'Selected a project for downstream smoke checks', targetProject?.id || 'none');

const projectResp = await request(`${baseUrl}/orchard/projects/${encodeURIComponent(targetProject.id)}`, { token });
check(projectResp.res.status === 200, 'Project detail endpoint works via standalone proxy', `status=${projectResp.res.status}`);
check(projectResp.body?.id === targetProject.id, 'Project detail matches requested project', projectResp.body?.id || 'missing');

const tasksResp = await request(`${baseUrl}/orchard/projects/${encodeURIComponent(targetProject.id)}/tasks`, { token });
check(tasksResp.res.status === 200, 'Project tasks endpoint works via standalone proxy', `status=${tasksResp.res.status}`);
const tasks = Array.isArray(tasksResp.body) ? tasksResp.body : [];
check(tasks.length > 0, 'Project tasks endpoint returns live task data', `count=${tasks.length}`);

const sampleTask = tasks[0];
if (sampleTask?.id) {
  const taskDetailResp = await request(`${baseUrl}/orchard/tasks/${sampleTask.id}`, { token });
  check(taskDetailResp.res.status === 200, 'Task detail endpoint works', `task=${sampleTask.id}`);
  const runsResp = await request(`${baseUrl}/orchard/tasks/${sampleTask.id}/runs`, { token });
  check(runsResp.res.status === 200, 'Task runs endpoint works', `task=${sampleTask.id}`);
}

const activityResp = await request(`${baseUrl}/orchard/activity`, { token });
check(activityResp.res.status === 200, 'Activity endpoint works via standalone proxy', `status=${activityResp.res.status}`);
check(activityResp.body && typeof activityResp.body === 'object', 'Activity endpoint returns JSON');
check(Number.isInteger(activityResp.body?.counts?.running ?? NaN), 'Sessions pill source count is numeric', `running=${activityResp.body?.counts?.running}`);
check(Array.isArray(activityResp.body?.running), 'Live running sessions array is present', `count=${activityResp.body?.running?.length ?? 'n/a'}`);
check(Array.isArray(activityResp.body?.recent), 'Recent activity array is present', `count=${activityResp.body?.recent?.length ?? 'n/a'}`);

const settingsResp = await request(`${baseUrl}/orchard/settings`, { token });
check(settingsResp.res.status === 200, 'Settings endpoint works', `status=${settingsResp.res.status}`);

const progress = progressFromTasks(tasks);
check(progress.pct >= 0 && progress.pct <= 100, 'Progress percentage derived from live tasks is valid', `${progress.pct}% done (${progress.counts.done}/${progress.counts.total})`);
check(Object.values(tasks.reduce((acc, task) => {
  const status = task?.status || 'unknown';
  acc[status] = (acc[status] || 0) + 1;
  return acc;
}, {})).length > 0, 'Board columns have live task groupings', JSON.stringify(tasks.reduce((acc, task) => {
  const status = task?.status || 'unknown';
  acc[status] = (acc[status] || 0) + 1;
  return acc;
}, {})));
check(projects.some((p) => p?.id && p?.name), 'Sidebar project list has live project records', `${projects.filter((p) => p?.id && p?.name).length} named projects`);

console.log('');
if (regressions.length) {
  console.error('REGRESSIONS DETECTED:');
  for (const item of regressions) console.error(`- ${item}`);
  process.exit(1);
} else {
  console.log('Standalone OrchardOS UI smoke check passed.');
}
