#!/usr/bin/env node
/**
 * IELTS Tuyaya Upload Tool
 *
 * 把本地雅思复盘 JSON 上传到 liuxue.online 服务器
 *
 * 用法：
 *   node upload.js --register              # 注册新账号
 *   node upload.js --login                 # 登录并保存 token 到本地
 *   node upload.js --logout                # 清除本地 token
 *   node upload.js --whoami                # 查看当前登录的账号
 *   node upload.js --status                # 查看服务器上已有的记录
 *   node upload.js --diff <dir>            # 对比本地和服务器差量
 *   node upload.js --batch <dir>           # 批量上传目录下所有复盘 JSON
 *   node upload.js <file.json>             # 上传单个 JSON
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

const API_BASE = 'https://www.liuxue.online/api/ielts';
const TOKEN_FILE = path.join(os.homedir(), '.ielts-tuyaya-token');

// ============ Token 持久化 ============
function saveToken(token, username) {
  const payload = { token, username, savedAt: new Date().toISOString() };
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(payload, null, 2), { mode: 0o600 });
}

function loadToken() {
  if (!fs.existsSync(TOKEN_FILE)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
    return data;
  } catch (e) {
    return null;
  }
}

function clearToken() {
  if (fs.existsSync(TOKEN_FILE)) fs.unlinkSync(TOKEN_FILE);
}

function requireToken() {
  const data = loadToken();
  if (!data || !data.token) {
    console.error('❌ 还没登录，先运行：node upload.js --login');
    console.error('   没账号？运行：node upload.js --register');
    process.exit(1);
  }
  return data.token;
}

// ============ 交互式输入 ============
function prompt(question, { hidden = false } = {}) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    if (hidden) {
      // 隐藏密码输入
      const stdin = process.stdin;
      process.stdout.write(question);
      stdin.resume();
      stdin.setRawMode && stdin.setRawMode(true);
      let pwd = '';
      const onData = (ch) => {
        const s = ch.toString('utf8');
        if (s === '\n' || s === '\r' || s === '\u0004') {
          stdin.setRawMode && stdin.setRawMode(false);
          stdin.pause();
          stdin.removeListener('data', onData);
          process.stdout.write('\n');
          rl.close();
          resolve(pwd);
        } else if (s === '\u0003') {
          // Ctrl+C
          process.exit(1);
        } else if (s === '\u007f' || s === '\b') {
          if (pwd.length > 0) {
            pwd = pwd.slice(0, -1);
            process.stdout.write('\b \b');
          }
        } else {
          pwd += s;
          process.stdout.write('*');
        }
      };
      stdin.on('data', onData);
    } else {
      rl.question(question, (answer) => {
        rl.close();
        resolve(answer.trim());
      });
    }
  });
}

// ============ API 请求 ============
async function apiRequest(action, data = {}) {
  const body = { action, ...data };
  const resp = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    throw new Error(`HTTP ${resp.status}: ${await resp.text()}`);
  }
  return await resp.json();
}

// ============ 账号相关 ============
async function doRegister() {
  console.log('📝 注册 liuxue.online 账号\n');
  const username = await prompt('用户名（2-20 字符，字母数字下划线）: ');
  if (!/^[a-zA-Z0-9_]{2,20}$/.test(username)) {
    console.error('❌ 用户名格式不正确');
    process.exit(1);
  }
  const password = await prompt('密码（至少 6 位）: ', { hidden: true });
  if (password.length < 6) {
    console.error('❌ 密码太短');
    process.exit(1);
  }
  const confirm = await prompt('再输一次密码: ', { hidden: true });
  if (password !== confirm) {
    console.error('❌ 两次密码不一致');
    process.exit(1);
  }
  const nickname = await prompt('昵称（可选，回车跳过）: ');

  const result = await apiRequest('register', {
    username,
    password,
    nickname: nickname || username,
  });

  if (result.code === 0) {
    console.log(`✅ 注册成功！欢迎 ${nickname || username}`);
    // 自动登录
    const login = await apiRequest('login', { username, password });
    if (login.code === 0) {
      saveToken(login.data.token, username);
      console.log(`🔑 已自动登录，token 已保存到 ${TOKEN_FILE}`);
      console.log('\n👉 下一步：node upload.js --batch <你的 JSON 目录>');
    }
  } else {
    console.error(`❌ 注册失败：${result.message}`);
    process.exit(1);
  }
}

async function doLogin() {
  console.log('🔐 登录 liuxue.online\n');
  const username = await prompt('用户名: ');
  const password = await prompt('密码: ', { hidden: true });

  const result = await apiRequest('login', { username, password });

  if (result.code === 0) {
    saveToken(result.data.token, username);
    console.log(`✅ 登录成功！token 已保存到 ${TOKEN_FILE}`);
    console.log(`👤 欢迎回来，${result.data.nickname || username}`);
  } else {
    console.error(`❌ 登录失败：${result.message}`);
    process.exit(1);
  }
}

function doLogout() {
  const data = loadToken();
  if (!data) {
    console.log('📭 当前没有保存的登录信息');
    return;
  }
  clearToken();
  console.log(`👋 已退出账号 ${data.username}`);
}

async function doWhoami() {
  const data = loadToken();
  if (!data) {
    console.log('📭 未登录');
    return;
  }
  console.log(`👤 当前账号：${data.username}`);
  console.log(`🔑 Token 文件：${TOKEN_FILE}`);
  console.log(`📅 保存时间：${data.savedAt}`);

  // 顺便验证 token 是否还有效
  try {
    const info = await apiRequest('getUserInfo', { token: data.token });
    if (info.code === 0) {
      console.log(`✅ Token 有效，服务器昵称：${info.data.nickname || info.data.username}`);
    } else {
      console.log(`⚠️  Token 可能已过期：${info.message}`);
      console.log('   重新登录：node upload.js --login');
    }
  } catch (e) {
    console.log(`⚠️  无法验证 token：${e.message}`);
  }
}

// ============ JSON → API 数据转换 ============
function jsonToReviewData(json) {
  const data = typeof json === 'string' ? JSON.parse(json) : json;

  // v3.0 / v4.0 格式（结构化复盘 JSON）
  if (data.version && (data.version.startsWith('3.') || data.version.startsWith('4.'))) {
    return {
      book: data.source.book,
      test: data.source.test,
      passage: data.source.passage,
      score: data.score.correct,
      total: data.score.total,
      duration: data.timing && data.timing.minutes != null ? Math.round(data.timing.minutes * 60) : 0, // 分钟→秒
      date: data.date || new Date().toISOString().slice(0, 10),
      answers: JSON.stringify({
        wrongQuestions: data.wrongQuestions || [],
        synonyms: data.synonyms || [],
        vocabulary: data.vocabulary || [],
        problems: data.problems || [],
      }),
    };
  }

  // 兼容旧格式
  return {
    book: data.book,
    test: data.test,
    passage: data.passage,
    score: data.score || data.correct || 0,
    total: data.total || 13,
    duration: data.duration || data.minutes || 0,
    date: data.date || new Date().toISOString().slice(0, 10),
    answers: JSON.stringify(data.answers || {}),
  };
}

// ============ 上传单个文件 ============
async function uploadSingle(filePath, token) {
  const absPath = path.resolve(filePath);
  if (!fs.existsSync(absPath)) {
    console.error(`❌ 文件不存在：${absPath}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(absPath, 'utf8');
  const json = JSON.parse(raw);
  const reviewData = jsonToReviewData(json);

  const label = `剑${reviewData.book}-T${reviewData.test}-P${reviewData.passage}`;
  console.log(`📤 上传 ${label}（${reviewData.score}/${reviewData.total}）...`);

  const result = await apiRequest('saveReview', { token, ...reviewData });

  if (result.code === 0) {
    console.log(`✅ ${label} 上传成功`);
  } else {
    console.error(`❌ ${label} 上传失败：${result.message}`);
  }
  return result;
}

// ============ 批量上传 ============
async function uploadBatch(dirPath, token) {
  const absDir = path.resolve(dirPath);
  if (!fs.existsSync(absDir)) {
    console.error(`❌ 目录不存在：${absDir}`);
    process.exit(1);
  }

  // 找出所有 JSON 文件（不强制要求文件名含"复盘"）
  const files = fs
    .readdirSync(absDir)
    .filter((f) => f.endsWith('.json'))
    .map((f) => path.join(absDir, f));

  if (files.length === 0) {
    console.log('📂 没有找到 JSON 文件');
    return;
  }

  console.log(`📂 找到 ${files.length} 个 JSON 文件`);

  // 查询已有记录
  console.log('🔍 查询服务器已有记录...');
  const existing = await apiRequest('getReviews', { token });
  const existingSet = new Set();
  if (existing.code === 0 && existing.data) {
    existing.data.forEach((r) => existingSet.add(`${r.book}-${r.test}-${r.passage}`));
    console.log(`   服务器已有 ${existingSet.size} 条记录`);
  }

  // 解析并过滤
  const reviews = [];
  const skipped = [];
  const parseFailed = [];

  for (const file of files) {
    try {
      const raw = fs.readFileSync(file, 'utf8');
      const json = JSON.parse(raw);
      // 必须是复盘 JSON（有 source 或 book 字段）
      if (!json.source && !json.book) {
        continue;
      }
      const data = jsonToReviewData(json);
      const key = `${data.book}-${data.test}-${data.passage}`;

      if (existingSet.has(key)) {
        skipped.push({ file: path.basename(file), key, reason: '已存在' });
      } else {
        reviews.push(data);
      }
    } catch (e) {
      parseFailed.push({ file: path.basename(file), reason: e.message });
    }
  }

  if (parseFailed.length > 0) {
    console.log(`⚠️  ${parseFailed.length} 个文件解析失败：`);
    parseFailed.forEach((s) => console.log(`   - ${s.file}（${s.reason}）`));
  }

  if (skipped.length > 0) {
    console.log(`⏭️  跳过 ${skipped.length} 个已存在的：`);
    skipped.slice(0, 10).forEach((s) => console.log(`   - ${s.file}（${s.key}）`));
    if (skipped.length > 10) console.log(`   ...（还有 ${skipped.length - 10} 个）`);
  }

  if (reviews.length === 0) {
    console.log('✅ 所有记录已是最新，无需上传');
    return;
  }

  console.log(`📤 准备上传 ${reviews.length} 条新记录...`);

  const result = await apiRequest('batchImport', { token, reviews });

  if (result.code === 0) {
    console.log(`✅ 批量导入完成：${result.data.imported} 条成功，${result.data.skipped} 条跳过`);
  } else {
    console.error(`❌ 批量导入失败：${result.message}`);
  }
}

// ============ 查看服务器状态 ============
async function showStatus(token) {
  console.log('🔍 查询服务器数据...\n');

  const userInfo = await apiRequest('getUserInfo', { token });
  if (userInfo.code === 0) {
    const d = userInfo.data;
    console.log(`👤 用户: ${d.nickname || d.username}`);
    console.log(
      `📊 统计: ${d.stats.total_reviews} 篇复盘，${d.stats.total_tests} 套完整测试，平均 Band ${d.stats.avg_band}`,
    );
    if (d.scores && d.scores.length > 0) {
      console.log(`📈 成绩:`);
      d.scores.forEach((s) => {
        console.log(
          `   ${s.label}: ${s.raw}/${s.total} → Band ${s.band}${s.duration ? ` (${Math.round(s.duration / 60)}min)` : ''}`,
        );
      });
    }
    console.log(`📝 掌握词汇: ${(d.mastered_words || []).length} 个`);
    console.log(`🔄 掌握同义替换: ${(d.mastered_synonyms || []).length} 组`);
  } else {
    console.error(`❌ 获取用户信息失败：${userInfo.message}`);
    if (userInfo.message && userInfo.message.includes('token')) {
      console.log('👉 请重新登录：node upload.js --login');
    }
  }

  console.log('\n--- 做题记录 ---');
  const reviews = await apiRequest('getReviews', { token });
  if (reviews.code === 0) {
    const data = reviews.data || [];
    console.log(`共 ${data.length} 条记录：`);
    data.forEach((r) => {
      console.log(
        `   剑${r.book}-T${r.test}-P${r.passage}: ${r.score}/${r.total}${r.duration ? ` (${Math.round(r.duration / 60)}min)` : ''} [${r.date}]`,
      );
    });
  }
}

// ============ 差量对比 ============
async function showDiff(dirPath, token) {
  const absDir = path.resolve(dirPath);

  const files = fs.readdirSync(absDir).filter((f) => f.endsWith('.json'));

  const localMap = {};
  for (const file of files) {
    try {
      const raw = fs.readFileSync(path.join(absDir, file), 'utf8');
      const json = JSON.parse(raw);
      if (!json.source && !json.book) continue;
      const data = jsonToReviewData(json);
      const key = `${data.book}-${data.test}-${data.passage}`;
      localMap[key] = { ...data, file };
    } catch (e) {}
  }

  const reviews = await apiRequest('getReviews', { token });
  const serverMap = {};
  if (reviews.code === 0) {
    (reviews.data || []).forEach((r) => {
      serverMap[`${r.book}-${r.test}-${r.passage}`] = r;
    });
  }

  console.log('📊 本地 vs 服务器对比：\n');

  const allKeys = new Set([...Object.keys(localMap), ...Object.keys(serverMap)]);
  const sorted = [...allKeys].sort();

  let newCount = 0,
    matchCount = 0,
    serverOnlyCount = 0,
    diffCount = 0;

  for (const key of sorted) {
    const local = localMap[key];
    const server = serverMap[key];
    const [b, t, p] = key.split('-');
    const label = `剑${b}-T${t}-P${p}`;

    if (local && !server) {
      console.log(`  🆕 ${label}: 仅本地（${local.score}/${local.total}）→ 需上传`);
      newCount++;
    } else if (!local && server) {
      console.log(`  ☁️  ${label}: 仅服务器（${server.score}/${server.total}）`);
      serverOnlyCount++;
    } else if (local && server) {
      if (local.score === server.score && local.total === server.total) {
        matchCount++;
      } else {
        console.log(
          `  ⚠️  ${label}: 不一致 — 本地 ${local.score}/${local.total} vs 服务器 ${server.score}/${server.total}`,
        );
        diffCount++;
      }
    }
  }

  console.log(
    `\n📋 汇总：${matchCount} 条一致，${newCount} 条待上传，${serverOnlyCount} 条仅服务器，${diffCount} 条不一致`,
  );
}

// ============ 主逻辑 ============
function printHelp() {
  console.log(`
IELTS Tuyaya Upload Tool

📘 账号管理
  node upload.js --register           注册新账号
  node upload.js --login              登录并保存 token
  node upload.js --logout             退出账号（清除本地 token）
  node upload.js --whoami             查看当前登录的账号

📤 数据同步
  node upload.js <file.json>          上传单个 JSON
  node upload.js --batch <dir>        批量上传目录下所有 JSON
  node upload.js --status             查看服务器上已有的记录
  node upload.js --diff <dir>         对比本地和服务器差量

💡 首次使用
  1. node upload.js --register        （没账号的话）
  2. node upload.js --batch ./batch-output/
  3. 打开 https://www.liuxue.online/ielts/ 查看成绩

🔑 Token 保存位置：${TOKEN_FILE}
`);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    return;
  }

  // 账号管理类命令（不需要 token）
  if (args[0] === '--register') return doRegister();
  if (args[0] === '--login') return doLogin();
  if (args[0] === '--logout') return doLogout();
  if (args[0] === '--whoami') return doWhoami();

  // 数据类命令（需要 token）
  const token = requireToken();

  if (args[0] === '--status') {
    await showStatus(token);
  } else if (args[0] === '--batch') {
    const dir = args[1] || '.';
    await uploadBatch(dir, token);
  } else if (args[0] === '--diff') {
    const dir = args[1] || '.';
    await showDiff(dir, token);
  } else if (args[0].startsWith('--')) {
    console.error(`❌ 未知命令：${args[0]}`);
    printHelp();
    process.exit(1);
  } else {
    await uploadSingle(args[0], token);
  }
}

main().catch((err) => {
  console.error('❌ 错误：', err.message);
  process.exit(1);
});
