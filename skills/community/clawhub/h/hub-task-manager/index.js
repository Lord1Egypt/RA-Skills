/**
 * hub-task-manager — EvoMap Hub bounty task management
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const HUB_URL = process.env.A2A_HUB_URL || 'https://hub.evomap.ai';
const NODE_ID = 'node_f6046fad1274a2eb';

function getNodeSecret() {
  try {
    return fs.readFileSync(path.join(process.env.HOME, '.evomap', 'node_secret'), 'utf-8').trim();
  } catch {
    return null;
  }
}

function apiGet(endpoint) {
  const secret = getNodeSecret();
  const cmd = `curl -s "${HUB_URL}${endpoint}" -H "X-Node-Secret: ${secret}"`;
  return JSON.parse(execSync(cmd, { encoding: 'utf-8' }));
}

function apiPost(endpoint, data) {
  const secret = getNodeSecret();
  const body = JSON.stringify(data);
  const cmd = `curl -s -X POST "${HUB_URL}${endpoint}" -H "Content-Type: application/json" -H "X-Node-Secret: ${secret}" -d '${body}'`;
  return JSON.parse(execSync(cmd, { encoding: 'utf-8' }));
}

function listAvailable() {
  return apiGet('/a2a/task/list?reputation=0&limit=20');
}

function listMy() {
  return apiGet(`/a2a/task/my?node_id=${NODE_ID}`);
}

function claim(taskId) {
  return apiPost('/a2a/task/claim', { task_id: taskId, node_id: NODE_ID });
}

function submit(taskId, assetId) {
  return apiPost('/a2a/task/submit', { task_id: taskId, asset_id: assetId, node_id: NODE_ID });
}

function complete(taskId, assetId) {
  return apiPost('/a2a/task/complete', { task_id: taskId, asset_id: assetId, node_id: NODE_ID });
}

module.exports = { listAvailable, listMy, claim, submit, complete, getNodeSecret, NODE_ID, HUB_URL };
