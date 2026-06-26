#!/usr/bin/env node
/**
 * Hook Runner - 工具钩子系统
 * 支持 PreToolUse 和 PostToolUse 钩子
 */

import { spawn } from 'child_process';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============ 类型定义 ============

/**
 * @typedef {Object} HookResult
 * @property {boolean} allowed - 是否允许执行
 * @property {boolean} denied - 是否被拒绝
 * @property {string[]} messages - 钩子输出消息
 */

/**
 * @typedef {Object} HookConfig
 * @property {string[]} [preToolUse] - 执行前钩子列表
 * @property {string[]} [postToolUse] - 执行后钩子列表
 */

// ============ 工具函数 ============

/**
 * 解析工具输入为美化格式
 */
function parseToolInput(inputStr) {
  try {
    const parsed = JSON.parse(inputStr);
    return JSON.stringify(parsed, null, 2);
  } catch {
    return inputStr;
  }
}

/**
 * 运行单个钩子命令
 * @param {string} command
 * @param {Object} env
 * @returns {Promise<{exitCode: number, stdout: string, stderr: string}>}
 */
function runHookCommand(command, env) {
  return new Promise((resolve) => {
    const isWindows = process.platform === 'win32';
    const shell = isWindows ? 'cmd' : '/bin/sh';
    const shellArgs = isWindows ? ['/C', command] : ['-c', command];

    const child = spawn(shell, shellArgs, {
      env: { ...process.env, ...env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => { stdout += data.toString(); });
    child.stderr.on('data', (data) => { stderr += data.toString(); });

    child.on('close', (code) => {
      resolve({
        exitCode: code ?? 0,
        stdout: stdout.trim(),
        stderr: stderr.trim()
      });
    });

    child.on('error', (err) => {
      resolve({
        exitCode: 3,
        stdout: '',
        stderr: err.message
      });
    });
  });
}

// ============ HookRunner 类 ============

class HookRunner {
  /**
   * @param {HookConfig} config
   */
  constructor(config = {}) {
    this.preHooks = config.preToolUse || [];
    this.postHooks = config.postToolUse || [];
  }

  /**
   * 构建钩子环境变量
   * @param {string} event
   * @param {string} toolName
   * @param {string} toolInput
   * @param {string} [toolOutput]
   * @param {boolean} [isError]
   */
  _buildEnv(event, toolName, toolInput, toolOutput = '', isError = false) {
    return {
      HOOK_EVENT: event,
      HOOK_TOOL_NAME: toolName,
      HOOK_TOOL_INPUT: toolInput,
      HOOK_TOOL_INPUT_PARSED: parseToolInput(toolInput),
      HOOK_TOOL_OUTPUT: toolOutput,
      HOOK_TOOL_IS_ERROR: isError ? '1' : '0'
    };
  }

  /**
   * 解析钩子结果
   * @param {number} exitCode
   * @param {string} stdout
   * @returns {{allowed: boolean, denied: boolean, isWarning: boolean}}
   */
  _parseResult(exitCode, stdout) {
    // Exit code 0 = Allow
    // Exit code 2 = Deny (only for PreToolUse)
    // Other = Warning (allow but show warning)
    if (exitCode === 0) {
      return { allowed: true, denied: false, isWarning: false };
    } else if (exitCode === 2) {
      return { allowed: false, denied: true, isWarning: false };
    } else {
      return { allowed: true, denied: false, isWarning: true };
    }
  }

  /**
   * 运行钩子列表
   * @param {string[]} hooks
   * @param {Object} env
   * @returns {Promise<HookResult>}
   */
  async _runHooks(hooks, env) {
    const messages = [];
    let denied = false;

    for (const hook of hooks) {
      const result = await runHookCommand(hook, env);
      const parsed = this._parseResult(result.exitCode, result.stdout);

      if (result.stdout) {
        messages.push(result.stdout);
      }

      if (result.stderr) {
        messages.push(`[stderr] ${result.stderr}`);
      }

      if (parsed.denied) {
        denied = true;
        messages.push(`Hook denied: ${hook}`);
        break;
      }

      if (parsed.isWarning) {
        messages.push(`Hook warning: ${hook} (exit ${result.exitCode})`);
      }
    }

    return {
      allowed: !denied,
      denied,
      messages
    };
  }

  /**
   * 执行 PreToolUse 钩子
   * @param {string} toolName
   * @param {string} toolInput
   * @returns {Promise<HookResult>}
   */
  async runPreToolUse(toolName, toolInput) {
    if (this.preHooks.length === 0) {
      return { allowed: true, denied: false, messages: [] };
    }

    const env = this._buildEnv('PreToolUse', toolName, toolInput);
    return this._runHooks(this.preHooks, env);
  }

  /**
   * 执行 PostToolUse 钩子
   * @param {string} toolName
   * @param {string} toolInput
   * @param {string} toolOutput
   * @param {boolean} isError
   * @returns {Promise<HookResult>}
   */
  async runPostToolUse(toolName, toolInput, toolOutput, isError = false) {
    if (this.postHooks.length === 0) {
      return { allowed: true, denied: false, messages: [] };
    }

    const env = this._buildEnv('PostToolUse', toolName, toolInput, toolOutput, isError);
    const result = await this._runHooks(this.postHooks, env);

    // PostToolUse 钩子不能阻止执行，但可以修改输出
    result.allowed = true;
    result.denied = false;

    return result;
  }

  /**
   * 合并钩子输出到工具结果
   * @param {string[]} hookMessages
   * @param {string} toolOutput
   * @param {boolean} isError
   * @returns {string}
   */
  static mergeOutput(hookMessages, toolOutput, isError = false) {
    if (hookMessages.length === 0) {
      return toolOutput;
    }

    const sections = [];
    if (toolOutput && toolOutput.trim()) {
      sections.push(toolOutput);
    }

    const label = isError ? 'Hook feedback (denied)' : 'Hook feedback';
    sections.push(`${label}:\n${hookMessages.join('\n')}`);

    return sections.join('\n\n');
  }
}

// ============ CLI 界面 ============

function printHelp() {
  console.log(`
Hook System - 工具钩子框架
===========================

用法:
  node hook-runner.mjs <command> [options]

命令:
  pre <tool> <input>     运行 PreToolUse 钩子
  post <tool> <input> [output] [error]  运行 PostToolUse 钩子
  test                   测试钩子配置

示例:
  node hook-runner.mjs pre read_file '{"path":"README.md"}'
  node hook-runner.mjs post bash '{"command":"ls"}' 'file listing...' 0

配置:
  通过 HOOK_PRE 和 HOOK_POST 环境变量指定钩子命令，多个用逗号分隔

  HOOK_PRE="echo PreHook" node hook-runner.mjs pre read_file '{}'
  HOOK_POST="node filter.mjs" node hook-runner.mjs post read_file '{}' 'output' 0
`);
}

async function main(args) {
  const runner = new HookRunner({
    preToolUse: process.env.HOOK_PRE?.split(',').filter(Boolean) || [],
    postToolUse: process.env.HOOK_POST?.split(',').filter(Boolean) || []
  });

  if (args[0] === 'pre' && args.length >= 3) {
    const toolName = args[1];
    const toolInput = args[2];
    console.log(`🔍 Running PreToolUse hooks for: ${toolName}`);
    const result = await runner.runPreToolUse(toolName, toolInput);
    console.log(`\nResult: ${result.allowed ? '✅ Allowed' : '❌ Denied'}`);
    if (result.messages.length > 0) {
      console.log('Messages:');
      result.messages.forEach(m => console.log(`  ${m}`));
    }
    return result.allowed ? 0 : 1;
  }

  if (args[0] === 'post' && args.length >= 3) {
    const toolName = args[1];
    const toolInput = args[2];
    const toolOutput = args[3] || '';
    const isError = args[4] === '1' || args[4] === 'true';
    console.log(`🔍 Running PostToolUse hooks for: ${toolName}`);
    const result = await runner.runPostToolUse(toolName, toolInput, toolOutput, isError);
    console.log(`\nOutput merged: ${result.messages.length} hook message(s)`);
    if (result.messages.length > 0) {
      console.log('Hook messages:');
      result.messages.forEach(m => console.log(`  ${m}`));
    }
    return 0;
  }

  if (args[0] === 'test') {
    console.log('🧪 Testing hook configuration...\n');
    const testRunner = new HookRunner({
      preToolUse: ['echo "Pre hook test"'],
      postToolUse: ['echo "Post hook test"']
    });
    const preResult = await testRunner.runPreToolUse('test_tool', '{"test":true}');
    console.log('PreToolUse:', preResult);
    const postResult = await testRunner.runPostToolUse('test_tool', '{"test":true}', 'test output', false);
    console.log('PostToolUse:', postResult);
    return 0;
  }

  printHelp();
  return 0;
}

// ============ 导出 ============

export { HookRunner };

// CLI 入口（仅在直接运行时执行）
const isMain = import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  const args = process.argv.slice(2);
  if (args[0] === '--help' || args[0] === '-h') {
    printHelp();
  } else {
    main(args).then(code => process.exit(code));
  }
}
