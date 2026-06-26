#!/usr/bin/env node
/**
 * KreadoAI — 数字人视频、文字转语音、形象克隆、字幕去除
 * 用法：node kreado.mjs <account|avatar|video|clone|tts|subtitle> [选项]
 * Node.js 18+，零外部依赖
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

function getVersionFromSkillMd() {
  try {
    const raw = readFileSync(join(__dirname, '..', 'SKILL.md'), 'utf-8');
    const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!m) return null;
    const v = m[1].match(/^version:\s*["']?([^"'\s\n]+)["']?/m);
    return v ? v[1].trim() : null;
  } catch {
    return null;
  }
}

let argvRest = process.argv.slice(2);
const vidx = argvRest.indexOf('--skill-version');
if (vidx === -1 || argvRest[vidx + 1] == null || String(argvRest[vidx + 1]).startsWith('--')) {
  argvRest = [argvRest[0], '--skill-version', getVersionFromSkillMd() || '1.1.0', ...argvRest.slice(1)];
}
process.argv = [process.argv[0], process.argv[1], ...argvRest];

const SUBCOMMANDS = new Set(['account', 'avatar', 'video', 'clone', 'tts', 'subtitle']);

function printHelp() {
  console.log(`KreadoAI

用法：
  node kreado.mjs <子命令> [选项]

子命令：
  account    账号信息（余额、VIP 到期时间），配置凭证
  avatar     数字人形象管理（列表、上传照片、查询）
  video      数字人视频生成（提交、查询、列表、详情）
  clone      即时形象克隆（上传视频、查询）
  tts        文字转语音（语言、声音、合成）
  subtitle   视频字幕和水印去除

示例：
  node kreado.mjs account
  node kreado.mjs account --configure
  node kreado.mjs avatar --list
  node kreado.mjs video --submit-system --task_name "test" --video_ratio 2 --digital_human_id 9 --audio_url "https://..."
  node kreado.mjs tts --languages
  node kreado.mjs clone --upload --video_url "https://..."
  node kreado.mjs subtitle --submit --task_name "test" --src_file_url "https://..."

  node kreado.mjs <子命令> --help

环境变量：
  KREADO_API_TOKEN        API Token（在 kreadoai.com 账号 -> API 设置中获取）
  KREADO_STORAGE_ROOT     可选，凭证存储根目录`);
}

const sub = argvRest[0];
if (!sub || sub === '--help' || sub === '-h') {
  printHelp();
  process.exit(sub === '--help' || sub === '-h' ? 0 : 1);
}

if (!SUBCOMMANDS.has(sub)) {
  console.error(`错误：未知子命令 "${sub}"。可用：account | avatar | video | clone | tts | subtitle`);
  process.exit(1);
}

async function run() {
  const mod = await import(`./${sub}.mjs`);
  await mod.main();
}

run().catch((err) => {
  console.error(`错误：${err?.message || err}`);
  process.exit(1);
});
