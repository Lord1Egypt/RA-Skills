const fs = require('fs');
const path = require('path');
const { collectProjectInfo } = require('./analyzer');
const { resolveTheme, THEMES } = require('./themes');
const { renderHtml } = require('./template');
const { exportLongImage } = require('./image');
const { pathExists } = require('./utils');
const { cloneRepo } = require('./git');

async function ensureDir(dirPath) {
  await fs.promises.mkdir(dirPath, { recursive: true });
}

async function resolveProjectPath(options = {}) {
  if (options.gitUrl) {
    const cloned = await cloneRepo(options.gitUrl);
    return { projectPath: cloned, temp: true };
  }
  const projectPath = options.projectPath ? path.resolve(options.projectPath) : process.cwd();
  return { projectPath, temp: false };
}

async function generateIntro(options = {}) {
  const { projectPath, temp } = await resolveProjectPath(options);
  const outputPath = options.outputPath ? path.resolve(options.outputPath) : path.join(projectPath, '介绍.html');
  const theme = resolveTheme(options.theme || 'aurora', options.accent);

  const info = await collectProjectInfo(projectPath, { gitUrl: options.gitUrl });
  const html = renderHtml({
    ...info,
    themeName: theme.name,
    imagePath: options.imageOut ? path.resolve(options.imageOut) : null,
    htmlPath: outputPath,
    projectPath,
    cliPath: path.resolve(__dirname, '../bin/cli.js')
  }, theme);

  await ensureDir(path.dirname(outputPath));
  await fs.promises.writeFile(outputPath, html, 'utf8');

  return { htmlPath: outputPath, theme: theme.name, info, html, tempProjectPath: temp ? projectPath : null };
}

async function generateLongImage(htmlPath, imagePath, options = {}) {
  const resolvedHtml = path.resolve(htmlPath);
  if (!(await pathExists(resolvedHtml))) {
    throw new Error(`HTML 文件不存在: ${resolvedHtml}`);
  }
  const resolvedImg = path.resolve(imagePath);
  await ensureDir(path.dirname(resolvedImg));
  await exportLongImage(resolvedHtml, resolvedImg, options);
  return { imagePath: resolvedImg };
}

module.exports = {
  generateIntro,
  generateLongImage,
  THEMES
};
