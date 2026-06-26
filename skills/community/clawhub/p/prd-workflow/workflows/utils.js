/**
 * 工具函数 v2.8.2
 *
 * 提供跨平台路径检测等通用功能
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * 动态检测技能安装路径
 *
 * 搜索顺序：
 * 1. 环境变量 OPENCLAW_SKILLS_DIR
 * 2. ~/.openclaw/skills/
 * 3. workspace/skills/（开发模式）
 * 4. 当前模块的上级目录
 *
 * @param {string} skillName - 技能名称
 * @returns {string|null} 技能路径，不存在返回 null
 */
function findSkillPath(skillName) {
  const searchPaths = [];

  // 1. 环境变量
  if (process.env.OPENCLAW_SKILLS_DIR) {
    searchPaths.push(process.env.OPENCLAW_SKILLS_DIR);
  }

  // 2. 用户主目录
  searchPaths.push(path.join(os.homedir(), '.openclaw', 'skills'));

  // 3. workspace 目录（开发模式）
  // __dirname 可能是 workflows/modules 或 workflows
  let currentDir = __dirname;
  for (let i = 0; i < 5; i++) {
    const workspaceSkills = path.join(currentDir, 'skills');
    if (fs.existsSync(path.join(workspaceSkills, skillName))) {
      return path.join(workspaceSkills, skillName);
    }
    currentDir = path.dirname(currentDir);
  }

  // 4. 检查已知路径
  const knownPaths = [
    // 从 workflows/modules 向上查找
    path.resolve(__dirname, '../../skills'),
    // 从 workflows 向上查找
    path.resolve(__dirname, '../skills'),
    // 用户主目录
    path.join(os.homedir(), '.openclaw', 'skills'),
    // 标准安装路径
    '/usr/local/lib/openclaw/skills',
    '/opt/openclaw/skills'
  ];

  for (const basePath of knownPaths) {
    const skillPath = path.join(basePath, skillName);
    if (fs.existsSync(skillPath)) {
      return skillPath;
    }
  }

  // 5. 遍历 searchPaths
  for (const basePath of searchPaths) {
    const skillPath = path.join(basePath, skillName);
    if (fs.existsSync(skillPath)) {
      return skillPath;
    }
  }

  return null;
}

/**
 * 检查技能是否可用
 *
 * @param {string} skillName - 技能名称
 * @returns {object} { available: boolean, path: string|null, message: string }
 */
function checkSkillAvailable(skillName) {
  const skillPath = findSkillPath(skillName);

  if (!skillPath) {
    return {
      available: false,
      path: null,
      message: `${skillName} 未安装`
    };
  }

  // 检查 SKILL.md 是否存在
  const skillMdPath = path.join(skillPath, 'SKILL.md');
  if (!fs.existsSync(skillMdPath)) {
    return {
      available: false,
      path: skillPath,
      message: `${skillName} 目录存在但缺少 SKILL.md`
    };
  }

  return {
    available: true,
    path: skillPath,
    message: `${skillName} 可用`
  };
}

/**
 * 查找可执行文件
 *
 * @param {string} cmd - 命令名
 * @returns {string|null} 可执行文件路径
 */
function findExecutable(cmd) {
  const { execSync } = require('child_process');

  try {
    // 尝试 which/where
    const whichCmd = process.platform === 'win32' ? 'where' : 'which';
    const result = execSync(`${whichCmd} ${cmd}`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    }).trim();

    if (result) {
      return result.split('\n')[0].trim();
    }
  } catch (e) {
    // 忽略错误
  }

  // 检查常见路径
  const commonPaths = process.platform === 'win32'
    ? [`C:\\Program Files\\${cmd}`, `C:\\Program Files (x86)\\${cmd}`]
    : [`/usr/local/bin/${cmd}`, `/usr/bin/${cmd}`, `/opt/homebrew/bin/${cmd}`];

  for (const p of commonPaths) {
    if (fs.existsSync(p)) {
      return p;
    }
  }

  return null;
}

/**
 * 获取 OpenClaw 工作区根目录
 *
 * @returns {string} 工作区根目录
 */
function getWorkspaceRoot() {
  // 1. 环境变量
  if (process.env.OPENCLAW_WORKSPACE) {
    return process.env.OPENCLAW_WORKSPACE;
  }

  // 2. 从当前目录向上查找
  let currentDir = __dirname;
  for (let i = 0; i < 10; i++) {
    // 检查是否是 workspace 目录（包含 skills/ 目录）
    if (fs.existsSync(path.join(currentDir, 'skills'))) {
      return currentDir;
    }
    currentDir = path.dirname(currentDir);
  }

  // 3. 默认返回标准路径
  return path.join(os.homedir(), '.openclaw', 'workspace');
}

/**
 * 获取输出目录
 *
 * @param {string} userId - 用户 ID
 * @param {string} projectName - 项目名称
 * @returns {string} 输出目录
 */
function getOutputDir(userId, projectName) {
  const workspaceRoot = getWorkspaceRoot();
  return path.join(workspaceRoot, 'output', userId, projectName);
}

module.exports = {
  findSkillPath,
  checkSkillAvailable,
  findExecutable,
  getWorkspaceRoot,
  getOutputDir
};