// Task Receiver — disabled (local-only build).
async function fetchTasks() { return { tasks: [] }; }
function selectBestTask() { return null; }
function estimateCapabilityMatch() { return 0; }
function scoreTask() { return { composite: 0, factors: {} }; }
async function claimTask() { return false; }
async function completeTask() { return false; }
function taskToSignals() { return []; }
module.exports = { fetchTasks, selectBestTask, estimateCapabilityMatch, scoreTask, claimTask, completeTask, taskToSignals };
