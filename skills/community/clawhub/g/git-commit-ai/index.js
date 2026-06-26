/**
 * git-commit-ai skill
 * 根据 git diff 自动生成符合规范的 commit message
 */

import { execSync } from 'child_process';
import { existsSync, writeFileSync, chmodSync, mkdirSync, readFileSync, copyFileSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

// 从 package.json 动态读取版本号
const require = createRequire(import.meta.url);
const { version: VERSION } = require('./package.json');

const VALID_LANGUAGES = ['auto', 'zh', 'en'];

// 敏感信息检测模式
const SENSITIVE_PATTERNS = [
  { pattern: /(?:password|passwd|pwd)\s*[:=]\s*['"][^'"]+['"]/gi, name: '密码' },
  { pattern: /(?:api[_-]?key|apikey)\s*[:=]\s*['"][^'"]+['"]/gi, name: 'API 密钥' },
  { pattern: /(?:secret|token)\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]/gi, name: '密钥/令牌' },
  { pattern: /-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----/gi, name: '私钥' },
  { pattern: /mongodb(\+srv)?:\/\/[^:]+:[^@]+@/gi, name: 'MongoDB 连接字符串' },
  { pattern: /mysql:\/\/[^:]+:[^@]+@/gi, name: 'MySQL 连接字符串' },
  { pattern: /postgres(?:ql)?:\/\/[^:]+:[^@]+@/gi, name: 'PostgreSQL 连接字符串' },
  { pattern: /redis:\/\/[^:]*:[^@]+@/gi, name: 'Redis 连接字符串' },
  { pattern: /aws_access_key_id\s*=\s*[A-Z0-9]{20}/gi, name: 'AWS Access Key' },
  { pattern: /aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}/gi, name: 'AWS Secret Key' }
];

// Diff 大小警告阈值 (100KB)
const DIFF_SIZE_WARNING_THRESHOLD = 100 * 1024;

// 配置文件名称
const CONFIG_FILES = ['.gitcommitairc', '.gitcommitai.json'];

/**
 * 获取跨平台删除命令
 * @param {string} filePath - 文件路径
 * @returns {string}
 */
function getDeleteCommand(filePath) {
  return process.platform === 'win32' ? `del "${filePath}"` : `rm ${filePath}`;
}

/**
 * 获取 Git 仓库根目录
 * @returns {string}
 */
function getGitRoot() {
  try {
    return execSync('git rev-parse --show-toplevel', { encoding: 'utf-8' }).trim();
  } catch {
    return process.cwd();
  }
}

/**
 * * 获取 Git 目录的绝对路径
 * @returns {string}
 */
function getGitDir() {
  try {
    let gitDir = execSync('git rev-parse --git-dir', { encoding: 'utf-8' }).trim();
    // 转换为绝对路径
    if (!path.isAbsolute(gitDir)) {
      gitDir = path.resolve(process.cwd(), gitDir);
    }
    return gitDir;
  } catch {
    return '.git';
  }
}

/**
 * 加载配置文件（从 Git 根目录查找）
 * @returns {Object}
 */
function loadConfig() {
  const gitRoot = getGitRoot();

  for (const file of CONFIG_FILES) {
    const configPath = path.join(gitRoot, file);
    if (existsSync(configPath)) {
      try {
        const content = readFileSync(configPath, 'utf-8');
        const config = JSON.parse(content);
        return config;
      } catch (error) {
        console.warn(`警告: 无法解析配置文件 ${file}: ${error.message}`);
      }
    }
  }

  // 检查 package.json 中的 gitCommitAi 字段
  const packageJsonPath = path.join(gitRoot, 'package.json');
  if (existsSync(packageJsonPath)) {
    try {
      const content = readFileSync(packageJsonPath, 'utf-8');
      const packageJson = JSON.parse(content);
      if (packageJson.gitCommitAi) {
        return packageJson.gitCommitAi;
      }
    } catch {
      // 忽略 package.json 解析错误
    }
  }

  return {};
}

/**
 * 获取帮助信息
 * @returns {string}
 */
function getHelpText() {
  return `
git-commit-ai - 根据 git diff 自动生成符合规范的 commit message

用法:
  /git-commit-ai [选项]

选项:
  --language <zh|en|auto>  指定 commit message 语言 (默认: auto)
  --install                安装 Git prepare-commit-msg hook
  --force                  强制覆盖现有的 hook（与 --install 配合使用）
  --help, -h               显示帮助信息
  --version, -v            显示版本号

示例:
  /git-commit-ai
  /git-commit-ai --language zh
  /git-commit-ai --language en
  /git-commit-ai --install

语言说明:
  - auto: 自动检测（根据代码注释语言）
  - zh:   强制使用中文
  - en:   强制使用英文
`;
}

/**
 * 获取精简版系统提示词
 * @param {string} language - 语言设置
 * @returns {string}
 */
function getSystemPrompt(language = 'auto') {
  const langInstruction = language === 'zh'
    ? '使用中文生成 commit message'
    : language === 'en'
    ? 'Use English for commit message'
    : '根据代码注释语言自动选择 commit message 语言（中文注释用中文，英文注释用英文，无注释默认中文）';

  return `你是 Git commit message 生成助手。

语言规则: ${langInstruction}

格式: <type>(<scope>): <description>

类型: feat(新功能) | fix(修复) | docs(文档) | style(格式) | refactor(重构) | perf(性能) | test(测试) | chore(构建)

规则:
1. description 必须具体（包含组件/函数/模块名称）
2. 从 diff 提取: 函数名、注释、文件路径、API 端点
3. scope 可选（如: auth, api, utils）
4. 长度 <= 50 字
5. 只输出 message，不要解释

示例:
- feat(auth): 添加用户登录验证，支持邮箱格式校验
- fix(api): 修复 getUser 接口空指针异常
- refactor(utils): 提取邮箱验证逻辑到独立函数`;
}

/**
 * 检查是否在 Git 仓库中
 * @returns {boolean}
 */
function isGitRepository() {
  try {
    execSync('git rev-parse --git-dir', { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

/**
 * 获取暂存区的 diff（带敏感信息检测和大小警告）
 * @returns {{ diff: string, warnings: string[] }}
 */
function getStagedDiff() {
  try {
    const diff = execSync('git diff --cached', {
      encoding: 'utf-8',
      maxBuffer: 10 * 1024 * 1024  // 支持 10MB 的 diff
    });

    const warnings = [];

    // 检查 diff 大小
    const diffSize = Buffer.byteLength(diff, 'utf-8');
    if (diffSize > DIFF_SIZE_WARNING_THRESHOLD) {
      warnings.push(`Diff 内容较大 (${(diffSize / 1024).toFixed(2)}KB)，建议拆分为多个提交以获得更准确的 commit message`);
    }

    // 检测敏感信息（每次创建新的正则实例避免 lastIndex 问题）
    for (const { pattern, name } of SENSITIVE_PATTERNS) {
      const regex = new RegExp(pattern.source, pattern.flags);
      if (regex.test(diff)) {
        warnings.push(`检测到可能包含${name}，请检查是否应该提交`);
        break;
      }
    }

    return { diff, warnings };
  } catch (error) {
    // 安全处理 stderr
    const stderr = error.stderr
      ? (Buffer.isBuffer(error.stderr) ? error.stderr.toString() : error.stderr)
      : '';

    // 根据不同的 exit code 提供更详细的错误信息
    switch (error.status) {
      case 128:
        throw new Error('Git 仓库状态异常，请检查:\n' +
          '  1. 当前目录是否在 Git 仓库中\n' +
          '  2. .git 目录是否完整\n' +
          '  3. 是否有读取权限');
      case 127:
        throw new Error('Git 命令未找到，请确保已安装 Git 并添加到 PATH');
      case 1:
        throw new Error('没有暂存的改动，请先使用 git add 暂存文件');
      default:
        throw new Error(`获取 git diff 失败 (exit code: ${error.status})\n` +
          `详细信息: ${stderr || error.message}\n` +
          `建议: 检查 Git 仓库状态或提交 Issue 反馈`);
    }
  }
}

/**
 * 检查是否有暂存的改动
 * @returns {boolean}
 */
function hasStagedChanges() {
  try {
    const output = execSync('git diff --cached --name-only', { encoding: 'utf-8' });
    return output.trim().length > 0;
  } catch {
    return false;
  }
}

/**
 * 安装 Git prepare-commit-msg hook
 * @param {boolean} force - 是否强制覆盖现有 hook
 * @returns {string}
 */
function installGitHook(force = false) {
  if (!isGitRepository()) {
    return '错误: 当前目录不是 Git 仓库\n\n请在 Git 仓库目录中运行此命令。';
  }

  // 获取 Git 目录的绝对路径
  const gitDir = getGitDir();
  const hooksDir = path.join(gitDir, 'hooks');

  // 确保 hooks 目录存在
  if (!existsSync(hooksDir)) {
    mkdirSync(hooksDir, { recursive: true });
  }

  const hookPath = path.join(hooksDir, 'prepare-commit-msg');
  const hookContent = '#!/bin/sh\n' +
    '# git-commit-ai auto-generated hook\n' +
    '# 此 hook 会提醒你使用 /git-commit-ai 生成 commit message\n' +
    '\n' +
    '# 只在有 staged changes 时提醒\n' +
    'if ! git diff --cached --quiet; then\n' +
    '    echo ""\n' +
    '    echo "提示: 请运行 /git-commit-ai 生成符合规范的 commit message"\n' +
    '    echo "      或直接编辑此文件输入你的 commit message"\n' +
    '    echo ""\n' +
    'fi\n';

  const deleteCmd = getDeleteCommand(hookPath);

  // 检查是否已存在 hook
  if (existsSync(hookPath)) {
    const existingContent = readFileSync(hookPath, 'utf-8');

    // 检查是否是 git-commit-ai 的 hook
    if (existingContent.includes('git-commit-ai auto-generated hook')) {
      try {
        writeFileSync(hookPath, hookContent, 'utf-8');

        // Unix 系统设置可执行权限
        if (process.platform !== 'win32') {
          chmodSync(hookPath, 0o755);
        }

        return `成功更新 Git prepare-commit-msg hook!

位置: ${hookPath}

现在每次执行 git commit 时，都会提醒你使用 /git-commit-ai 生成 commit message。

如需卸载 hook，删除该文件即可:
  ${deleteCmd}`;
      } catch (error) {
        return `更新 Git hook 失败: ${error.message}

你可以手动创建 hook 文件:
  ${hookPath}`;
      }
    }

    // 存在其他 hook，检查是否强制覆盖
    if (!force) {
      // 备份现有 hook
      const backupPath = `${hookPath}.backup.${Date.now()}`;
      copyFileSync(hookPath, backupPath);

      return `警告: 已存在 prepare-commit-msg hook

已创建备份: ${backupPath}

如需保留原 hook，请恢复备份:
  ${process.platform === 'win32' ? `move "${backupPath}" "${hookPath}"` : `mv ${backupPath} ${hookPath}`}

如需使用 git-commit-ai hook，请使用 --force 选项:
  /git-commit-ai --install --force`;
    }
  }

  try {
    writeFileSync(hookPath, hookContent, 'utf-8');

    // Unix 系统设置可执行权限
    if (process.platform !== 'win32') {
      chmodSync(hookPath, 0o755);
    }

    return `成功安装 Git prepare-commit-msg hook!

位置: ${hookPath}

现在每次执行 git commit 时，都会提醒你使用 /git-commit-ai 生成 commit message。

如需卸载 hook，删除该文件即可:
  ${deleteCmd}`;
  } catch (error) {
    return `安装 Git hook 失败: ${error.message}

你可以手动创建 hook 文件:
  ${hookPath}`;
  }
}

/**
 * Skill 主函数
 * @param {string[]} args - 命令行参数
 * @returns {Promise<string>}
 */
export async function execute(args = []) {
  // 检查帮助命令
  if (args.includes('--help') || args.includes('-h')) {
    return getHelpText();
  }

  // 检查版本命令
  if (args.includes('--version') || args.includes('-v')) {
    return `git-commit-ai v${VERSION}`;
  }

  // 检查安装 hook 命令
  if (args.includes('--install')) {
    const force = args.includes('--force');
    return installGitHook(force);
  }

  // 解析参数
  // 加载配置文件（命令行参数优先级更高）
  const config = loadConfig();
  let language = config.language || 'auto';
  let languageCount = 0;
  const unknownArgs = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--language') {
      languageCount++;

      // 检测重复参数
      if (languageCount > 1) {
        return '警告: --language 参数重复指定，将使用最后一个值\n\n' +
               '建议: 只指定一次 --language 参数\n\n' +
               '用法: /git-commit-ai --language <zh|en|auto>';
      }

      const langValue = args[i + 1]?.trim();  // 添加 trim() 处理

      if (!langValue) {
        return '错误: --language 参数需要一个值\n\n用法: /git-commit-ai --language <zh|en|auto>';
      }

      if (!VALID_LANGUAGES.includes(langValue)) {
        return `错误: 无效的语言值 "${langValue}"\n\n支持的语言: ${VALID_LANGUAGES.join(', ')}`;
      }

      language = langValue;
      i++;
    } else if (args[i].startsWith('--') && !['--install', '--force', '--help', '-h', '--version', '-v'].includes(args[i])) {
      unknownArgs.push(args[i]);
    }
  }

  // 警告未知参数
  if (unknownArgs.length > 0) {
    return `警告: 未知参数 ${unknownArgs.join(', ')}\n\n${getHelpText()}`;
  }

  // 检查 Git 仓库
  if (!isGitRepository()) {
    return '错误: 当前目录不是 Git 仓库\n\n请在 Git 仓库目录中运行此命令。';
  }

  // 检查暂存的改动
  if (!hasStagedChanges()) {
    return `错误: 没有暂存的改动

请先使用 git add 暂存改动:
  git add .
  git add <file>

然后再运行 /git-commit-ai`;
  }

  // 获取 diff（带警告检测）
  let diffResult;
  try {
    diffResult = getStagedDiff();
  } catch (error) {
    return `错误: ${error.message}`;
  }

  const { diff, warnings } = diffResult;

  if (!diff || diff.trim().length === 0) {
    return '错误: 无法获取 git diff 内容';
  }

  // 返回分析请求
  const systemPrompt = getSystemPrompt(language);

  // 构建输出，包含警告信息
  let output = '';

  if (warnings.length > 0) {
    output = `⚠️ 警告:\n${warnings.map(w => `  - ${w}`).join('\n')}\n\n---\n\n`;
  }

  output += `请根据以下 Git diff 生成 commit message:

---

## Git Diff 内容:

\`\`\`diff
${diff}
\`\`\`

---

## 分析要求:

${systemPrompt}

---

请生成符合规范的 commit message，只输出 message 本身，不要其他解释。`;

  return output;
}

// 导出 skill 信息
export const info = {
  name: 'git-commit-ai',
  description: '根据 git diff 自动生成符合规范的 commit message',
  usage: '/git-commit-ai [--language <zh|en|auto>] [--install] [--help] [--version]',
  examples: [
    '/git-commit-ai',
    '/git-commit-ai --language zh',
    '/git-commit-ai --language en',
    '/git-commit-ai --install',
    '/git-commit-ai --help'
  ]
};
