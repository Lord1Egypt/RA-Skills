import assert from 'node:assert/strict';
import { execFile, spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const skillRoot = path.resolve(new URL('..', import.meta.url).pathname);

function runWithClosedInput(command, args, options) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, options);
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('error', reject);
    child.on('close', code => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(new Error(`子进程退出码 ${code}：${stderr}`));
    });
    child.stdin.end();
  });
}

test('环境准备脚本复用符合版本要求的 Node.js', async t => {
  const runtimeDir = await fs.mkdtemp(path.join(os.tmpdir(), 'lvpin-runtime-test-'));
  t.after(() => fs.rm(runtimeDir, { recursive: true, force: true }));
  const { stdout } = await execFileAsync('sh', ['scripts/bootstrap.sh', '--ensure'], {
    cwd: skillRoot,
    env: { ...process.env, HAOLVSHI_NODE_BIN: process.execPath, HAOLVSHI_RUNTIME_DIR: runtimeDir }
  });
  const result = JSON.parse(stdout);
  assert.equal(result.ok, true);
  assert.equal(result.installed, false);
  assert.equal(result.nodePath, process.execPath);
});

test('统一运行入口会先检查环境再执行技能命令', async t => {
  const runtimeDir = await fs.mkdtemp(path.join(os.tmpdir(), 'lvpin-runner-test-'));
  const stateDir = await fs.mkdtemp(path.join(os.tmpdir(), 'lvpin-state-test-'));
  t.after(() => Promise.all([
    fs.rm(runtimeDir, { recursive: true, force: true }),
    fs.rm(stateDir, { recursive: true, force: true })
  ]));
  const { stdout } = await runWithClosedInput('sh', ['scripts/run.sh', 'cleanup'], {
    cwd: skillRoot,
    env: {
      ...process.env,
      HAOLVSHI_NODE_BIN: process.execPath,
      HAOLVSHI_RUNTIME_DIR: runtimeDir,
      HAOLVSHI_STATE_DIR: stateDir
    }
  });
  const result = JSON.parse(stdout);
  assert.equal(result.ok, true);
  assert.equal(result.stage, 'cleaned');
});

async function copySkillScripts(prefix) {
  const workDir = await fs.mkdtemp(path.join(os.tmpdir(), prefix));
  await fs.cp(path.join(skillRoot, 'scripts'), path.join(workDir, 'scripts'), { recursive: true });
  // 报告模板等资源也要带上，否则命令会因缺资源失败，掩盖真正要验的权限问题。
  await fs.cp(path.join(skillRoot, 'assets'), path.join(workDir, 'assets'), { recursive: true });
  for (const name of await fs.readdir(path.join(workDir, 'scripts'))) {
    await fs.chmod(path.join(workDir, 'scripts', name), 0o644);
  }
  return workDir;
}

test('运行环境准备会补齐脚本执行位并建好状态目录', async t => {
  // 有些宿主解压技能包时不保留文件权限。等流程中途报 Permission denied
  // 再让模型去补，会白白多出一轮排查和决策，必须在准备阶段一次性做完。
  const workDir = await copySkillScripts('haolvshi-perm-');
  const runtimeDir = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-perm-rt-'));
  const stateDir = path.join(workDir, 'state');
  t.after(() => Promise.all([
    fs.rm(workDir, { recursive: true, force: true }),
    fs.rm(runtimeDir, { recursive: true, force: true })
  ]));

  const { stdout } = await execFileAsync('sh', [path.join(workDir, 'scripts', 'bootstrap.sh'), '--ensure'], {
    env: {
      ...process.env,
      HAOLVSHI_NODE_BIN: process.execPath,
      HAOLVSHI_RUNTIME_DIR: runtimeDir,
      HAOLVSHI_STATE_DIR: stateDir
    }
  });
  const result = JSON.parse(stdout);
  assert.equal(result.ok, true);
  assert.equal(result.executableFixed, true);

  for (const entry of ['run.sh', 'bootstrap.sh', 'legal-skill.mjs']) {
    const mode = (await fs.stat(path.join(workDir, 'scripts', entry))).mode & 0o111;
    assert.notEqual(mode, 0, `${entry} 应被补回执行位`);
  }
  // 被 import 的模块不需要执行位，不该跟着一起改，否则每次准备环境
  // 都会在仓库里留下一堆无谓的权限变更。
  const moduleMode = (await fs.stat(path.join(workDir, 'scripts', 'state-store.mjs'))).mode & 0o111;
  assert.equal(moduleMode, 0, '非入口模块不应被加上执行位');
  assert.ok((await fs.stat(stateDir)).isDirectory(), '状态目录应提前建好');
});

test('执行位全部丢失时技能仍能正常运行', async t => {
  // run.sh 不能直接执行 bootstrap.sh：权限一丢整条流程就会中断。
  const workDir = await copySkillScripts('haolvshi-noexec-');
  const runtimeDir = await fs.mkdtemp(path.join(os.tmpdir(), 'haolvshi-noexec-rt-'));
  t.after(() => Promise.all([
    fs.rm(workDir, { recursive: true, force: true }),
    fs.rm(runtimeDir, { recursive: true, force: true })
  ]));

  const { stdout } = await runWithClosedInput('sh', [path.join(workDir, 'scripts', 'run.sh'), 'cleanup'], {
    env: {
      ...process.env,
      HAOLVSHI_NODE_BIN: process.execPath,
      HAOLVSHI_RUNTIME_DIR: runtimeDir,
      HAOLVSHI_STATE_DIR: path.join(workDir, 'state')
    }
  });
  assert.equal(JSON.parse(stdout).ok, true);
});
