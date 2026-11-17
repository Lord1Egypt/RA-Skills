const fs = require("fs");
const path = require("path");

function printBanner() {
  process.stderr.write("╔════════════════════════════════════════════╗\n");
  process.stderr.write("║                                            ║\n");
  process.stderr.write("║          🎬 视频文案智能提取助手            ║\n");
  process.stderr.write("║                                            ║\n");
  process.stderr.write("╚════════════════════════════════════════════╝\n");
  process.stderr.write("\n");
}

function printLog(level, message) {
  message = String(message ?? "");
  const colorMap = {
    INFO: "\x1b[34m",
    SUCCESS: "\x1b[32m",
    WARN: "\x1b[33m",
    ERROR: "\x1b[31m",
  };
  console.error(
    `${colorMap[level] || ""}[${new Date().toLocaleString()}] [${level}] ${message}\x1b[0m`,
  );
}

/**
 * 定义技能下载/临时目录路径
 */
function downloadPath() {
  return path.join(path.dirname(__filename), "..", "..", "tmp");
}

/**
 * 记录最近一次成功的视频分析任务ID，供 --id last 复用
 */
function lastTaskPath() {
  return path.join(downloadPath(), ".last_task_id");
}

function saveLastTask(id) {
  try {
    fs.mkdirSync(downloadPath(), { recursive: true });
    fs.writeFileSync(lastTaskPath(), String(id), "utf-8");
  } catch (_) {
    /* 非关键路径，忽略失败 */
  }
}

function loadLastTask() {
  try {
    if (fs.existsSync(lastTaskPath())) {
      return fs.readFileSync(lastTaskPath(), "utf-8").trim();
    }
  } catch (_) {
    /* 忽略读取失败 */
  }
  return "";
}

module.exports = {
  printBanner,
  printInfo: (msg) => printLog("INFO", msg),
  printSuccess: (msg) => printLog("SUCCESS", msg),
  printError: (msg) => printLog("ERROR", msg),
  printWarn: (msg) => printLog("WARN", msg),
  downloadPath,
  saveLastTask,
  loadLastTask,
};
