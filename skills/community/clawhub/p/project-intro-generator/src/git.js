const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

function assertGitAvailable() {
  try {
    execSync('git --version', { stdio: 'ignore' });
  } catch (err) {
    throw new Error('未检测到 git，请安装 git 后再试。');
  }
}

async function createTempDir(prefix = 'project-intro-') {
  const base = await fs.promises.mkdtemp(path.join(os.tmpdir(), prefix));
  return base;
}

async function cloneRepo(gitUrl) {
  assertGitAvailable();
  const tempDir = await createTempDir();
  try {
    execSync(`git clone --depth 1 ${gitUrl} ${tempDir}`, { stdio: 'inherit' });
  } catch (err) {
    throw new Error(`克隆仓库失败：${err.message}`);
  }
  return tempDir;
}

module.exports = {
  cloneRepo,
  createTempDir
};
