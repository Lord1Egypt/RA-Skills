#!/usr/bin/env node
/**
 * PowPow Robot Deployer
 * 通过 PowPow 账号体系，将 OpenClaw Agent 部署到全球地图
 * 流程：注册/登录 → 获取 token + userId → 创建/管理机器人
 *
 * 用法：
 *   node deploy-robot.js register --username "名字" --password "密码" [--nickname "昵称"]
 *   node deploy-robot.js login    --username "名字" --password "密码"
 *   node deploy-robot.js create   --username "名字" --password "密码" --name "机器人" --city 北京
 *   node deploy-robot.js list
 *   node deploy-robot.js move     --id <robotId> --city 上海  (需要登录)
 *   node deploy-robot.js delete   --id <robotId>  (需要登录)
 *   node deploy-robot.js delete   --all           (需要登录)
 *   node deploy-robot.js task     --id <robotId> --type patrol --city 广州
 */

const https = require('https');
const http  = require('http');
const fs    = require('fs');
const path  = require('path');
const os    = require('os');

// ─── 配置 ──────────────────────────────────────────────────────
const API_BASE   = 'https://global.powpow.online/api';
const MAP_URL    = 'https://global.powpow.online/map';
// 本地缓存 token（避免每次都要登录）
const TOKEN_FILE = path.join(os.homedir(), '.workbuddy', 'powpow-token.json');

// ─── 城市坐标预设 ──────────────────────────────────────────────
const CITIES = {
  '北京':  { lat: 39.9042, lng: 116.4074 },
  '上海':  { lat: 31.2304, lng: 121.4737 },
  '广州':  { lat: 23.1291, lng: 113.2644 },
  '深圳':  { lat: 22.5431, lng: 114.0579 },
  '成都':  { lat: 30.5728, lng: 104.0668 },
  '杭州':  { lat: 30.2741, lng: 120.1551 },
  '武汉':  { lat: 30.5928, lng: 114.3052 },
  '西安':  { lat: 34.3416, lng: 108.9398 },
  '南京':  { lat: 32.0603, lng: 118.7969 },
  '重庆':  { lat: 29.5630, lng: 106.5516 },
  '纽约':  { lat: 40.7128, lng: -74.0060 },
  '东京':  { lat: 35.6762, lng: 139.6503 },
  '伦敦':  { lat: 51.5074, lng: -0.1278 },
  '巴黎':  { lat: 48.8566, lng:   2.3522 },
  '悉尼':  { lat: -33.8688, lng: 151.2093 },
  '新加坡':{ lat:  1.3521, lng: 103.8198 },
  '首尔':  { lat: 37.5665, lng: 126.9780 },
};

// ─── Token 本地缓存 ────────────────────────────────────────────
function saveToken(data) {
  try {
    const dir = path.dirname(TOKEN_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(TOKEN_FILE, JSON.stringify(data, null, 2), 'utf8');
  } catch {}
}

function loadToken() {
  try {
    if (fs.existsSync(TOKEN_FILE)) {
      return JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
    }
  } catch {}
  return null;
}

// ─── HTTP 工具函数 ─────────────────────────────────────────────
function request(method, urlPath, body = null, token = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(API_BASE + urlPath);
    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https : http;
    const payload = body ? JSON.stringify(body) : null;

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'WorkBuddy-PowPow-Skill/1.0',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...(payload ? { 'Content-Length': Buffer.byteLength(payload) } : {}),
      },
    };

    const req = lib.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, body: data });
        }
      });
    });

    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

// ─── 解析命令行参数 ────────────────────────────────────────────
function parseArgs(argv) {
  const args = {};
  let i = 0;
  while (i < argv.length) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const val = (argv[i + 1] && !argv[i + 1].startsWith('--')) ? argv[i + 1] : true;
      args[key] = val;
      if (val !== true) i++;
    }
    i++;
  }
  return args;
}

// ─── 解析城市坐标 ──────────────────────────────────────────────
function resolveCoords(args) {
  let { lat, lng, city } = args;
  if (city && CITIES[city]) {
    lat = lat || CITIES[city].lat;
    lng = lng || CITIES[city].lng;
    console.log(`  📍 城市坐标 [${city}]: ${lat}, ${lng}`);
  }
  if (!lat || !lng) return null;
  return { lat: parseFloat(lat), lng: parseFloat(lng) };
}

// ─── 格式化输出机器人 ──────────────────────────────────────────
function printRobot(robot) {
  const name = (robot.name || '未命名').padEnd(33);
  console.log('\n  ┌───────────────────────────────────────┐');
  console.log(`  │  🤖  ${name}│`);
  console.log('  ├───────────────────────────────────────┤');
  console.log(`  │  ID     : ${String(robot.id || '-').substring(0, 28).padEnd(28)}│`);
  console.log(`  │  位置   : ${String(robot.lat).padEnd(12)} / ${String(robot.lng).padEnd(13)}│`);
  console.log(`  │  状态   : ${String(robot.status || 'idle').padEnd(28)}│`);
  if (robot.description) {
    const d = String(robot.description).substring(0, 28);
    console.log(`  │  描述   : ${d.padEnd(28)}│`);
  }
  console.log('  └───────────────────────────────────────┘');
}

// ─── 获取有效 token（优先缓存，其次登录，其次注册） ────────────
async function getAuthToken(args) {
  const { username, password, nickname } = args;

  // 1. 有参数 → 直接登录（或注册后登录）
  if (username && password) {
    // 先尝试登录
    const loginRes = await request('POST', '/auth/login', { username, password });
    if (loginRes.status === 200 && loginRes.body.token) {
      saveToken({ token: loginRes.body.token, userId: loginRes.body.user.id, username });
      return { token: loginRes.body.token, userId: loginRes.body.user.id, user: loginRes.body.user, isNew: false };
    }

    // 登录失败 → 尝试注册
    if (loginRes.body?.error === '用户名或密码错误' || loginRes.status === 401) {
      console.log(`  ℹ️  账号不存在，正在自动注册 "${username}"...`);
      const regRes = await request('POST', '/auth/register', {
        username,
        password,
        nickname: nickname || username,
      });
      if (regRes.status === 200 && regRes.body.token) {
        saveToken({ token: regRes.body.token, userId: regRes.body.user.id, username });
        return { token: regRes.body.token, userId: regRes.body.user.id, user: regRes.body.user, isNew: true };
      }
      throw new Error(`注册失败: ${regRes.body?.error || JSON.stringify(regRes.body)}`);
    }

    throw new Error(`登录失败: ${loginRes.body?.error || JSON.stringify(loginRes.body)}`);
  }

  // 2. 无参数 → 读本地缓存 token
  const cached = loadToken();
  if (cached?.token) {
    return { token: cached.token, userId: cached.userId, fromCache: true };
  }

  return null;
}

// ═══════════════════════════════════════════════════════════════
//  命令实现
// ═══════════════════════════════════════════════════════════════

// 注册
async function cmdRegister(args) {
  const { username, password, nickname, email } = args;
  if (!username || !password) {
    console.error('❌ 请提供 --username 和 --password'); process.exit(1);
  }
  console.log(`\n📝 注册账号 "${username}"...`);
  const res = await request('POST', '/auth/register', {
    username, password,
    nickname: nickname || username,
    ...(email ? { email } : {}),
  });
  if (res.status === 200 && res.body.token) {
    saveToken({ token: res.body.token, userId: res.body.user.id, username });
    const u = res.body.user;
    console.log(`\n✅ 注册成功！`);
    console.log(`  用户名: ${u.username}`);
    console.log(`  用户ID: ${u.id}`);
    console.log(`  Token 已缓存，后续操作无需重复登录`);
  } else {
    console.error(`\n❌ 注册失败: ${res.body?.error || JSON.stringify(res.body)}`);
    process.exit(1);
  }
}

// 登录
async function cmdLogin(args) {
  const { username, password } = args;
  if (!username || !password) {
    console.error('❌ 请提供 --username 和 --password'); process.exit(1);
  }
  console.log(`\n🔑 登录账号 "${username}"...`);
  const res = await request('POST', '/auth/login', { username, password });
  if (res.status === 200 && res.body.token) {
    saveToken({ token: res.body.token, userId: res.body.user.id, username });
    const u = res.body.user;
    console.log(`\n✅ 登录成功！`);
    console.log(`  用户名: ${u.username}  昵称: ${u.nickname || '-'}`);
    console.log(`  用户ID: ${u.id}`);
    console.log(`  Token 已缓存，30天内无需重复登录`);
  } else {
    console.error(`\n❌ 登录失败: ${res.body?.error || JSON.stringify(res.body)}`);
    process.exit(1);
  }
}

// 创建机器人（核心流程：注册/登录 → 创建）
async function cmdCreate(args) {
  const { name, desc, description, avatar } = args;

  // 解析坐标
  const coords = resolveCoords(args);
  if (!coords) {
    console.error('❌ 请提供位置：--city <城市名> 或 --lat <纬度> --lng <经度>');
    console.error(`   可用城市: ${Object.keys(CITIES).join(', ')}`);
    process.exit(1);
  }

  // 获取认证
  console.log('\n🤖 准备部署机器人...');
  const auth = await getAuthToken(args);
  if (!auth) {
    console.error('❌ 未登录。请提供 --username 和 --password，或先运行 login 命令');
    process.exit(1);
  }

  if (auth.isNew) {
    console.log(`  ✅ 新账号 "${args.username}" 注册成功，用户ID: ${auth.userId}`);
  } else if (auth.fromCache) {
    console.log(`  ✅ 使用已登录账号 (userId: ${auth.userId})`);
  } else {
    console.log(`  ✅ 登录成功，用户ID: ${auth.userId}`);
  }

  // 创建机器人
  const payload = {
    name: name || 'OpenClaw Agent',
    description: desc || description || '由 WorkBuddy 部署的 OpenClaw 智能机器人',
    avatarUrl: avatar || 'https://www.powpow.online/robot-avatar.png',
    lat: coords.lat,
    lng: coords.lng,
    creatorId: auth.userId,
  };

  console.log(`\n🚀 正在将 "${payload.name}" 部署到 (${coords.lat}, ${coords.lng})...`);
  const res = await request('POST', '/openclaw/robots', payload, auth.token);

  if ((res.status === 200 || res.status === 201) && res.body.success) {
    const robot = res.body.robot || res.body.data;
    console.log('\n✅ 机器人部署成功！');
    printRobot(robot);
    console.log(`\n  🗺️  立即查看地图: ${MAP_URL}`);
    console.log(`  📌 机器人ID: ${robot.id}  (移动/删除时使用)`);
  } else {
    console.error(`\n❌ 部署失败: ${res.body?.error || JSON.stringify(res.body)}`);
    process.exit(1);
  }
}

// 列出所有机器人
async function cmdList() {
  console.log('\n📋 正在获取地图上的机器人...');
  const res = await request('GET', '/openclaw/robots');
  if (res.status === 200 && res.body.success) {
    const robots = res.body.robots || res.body.data || [];
    if (robots.length === 0) {
      console.log('\n  🌍 地图上暂无机器人。使用 create 命令部署第一个！');
    } else {
      console.log(`\n  🌍 当前地图上共有 ${robots.length} 个机器人：`);
      robots.forEach((r, i) => {
        console.log(`\n  [${i + 1}/${robots.length}]`);
        printRobot(r);
      });
      console.log(`\n  🗺️  查看地图: ${MAP_URL}`);
    }
  } else {
    console.error(`\n❌ 获取失败: ${res.body?.error || JSON.stringify(res.body)}`);
    process.exit(1);
  }
}

// 移动机器人
async function cmdMove(args) {
  const { id } = args;
  if (!id) { console.error('❌ 请提供 --id <机器人ID>'); process.exit(1); }

  const coords = resolveCoords(args);
  if (!coords) {
    console.error('❌ 请提供目标位置：--city <城市> 或 --lat/--lng'); process.exit(1);
  }

  const auth = await getAuthToken(args);
  const token = auth?.token || null;

  // 获取当前机器人数据
  const getRes = await request('GET', `/openclaw/robots/${id}`, null, token);
  if (getRes.status !== 200 || !getRes.body.success) {
    console.error(`❌ 机器人 ${id} 不存在`); process.exit(1);
  }

  const current = getRes.body.robot;
  const payload = { ...current, lat: coords.lat, lng: coords.lng, status: 'moving' };

  console.log(`\n📍 移动 "${current.name}" → (${coords.lat}, ${coords.lng})...`);
  const res = await request('PUT', `/openclaw/robots/${id}`, payload, token);

  if (res.status === 200 && res.body.success) {
    console.log('\n✅ 移动成功！');
    printRobot(res.body.robot || res.body.data);
    console.log(`\n  🗺️  查看地图: ${MAP_URL}`);
  } else {
    console.error(`\n❌ 移动失败: ${res.body?.error || JSON.stringify(res.body)}`);
    process.exit(1);
  }
}

// 删除机器人
async function cmdDelete(args) {
  const { id, all } = args;
  const auth = await getAuthToken(args);
  const token = auth?.token || null;

  if (all) {
    console.log('\n🗑️  获取所有机器人...');
    const listRes = await request('GET', '/openclaw/robots', null, token);
    if (listRes.status !== 200) { console.error('❌ 获取列表失败'); process.exit(1); }
    const robots = listRes.body.robots || listRes.body.data || [];
    if (robots.length === 0) { console.log('✅ 地图上没有机器人。'); return; }
    console.log(`  即将删除 ${robots.length} 个机器人...`);
    let ok = 0;
    for (const r of robots) {
      const res = await request('DELETE', `/openclaw/robots/${r.id}`, null, token);
      if (res.status === 200 && res.body.success) { console.log(`  ✓ ${r.name} (${r.id})`); ok++; }
      else { console.log(`  ✗ 失败: ${r.name}`); }
    }
    console.log(`\n✅ 完成，删除 ${ok}/${robots.length} 个`);
  } else {
    if (!id) { console.error('❌ 请提供 --id <机器人ID> 或 --all'); process.exit(1); }
    console.log(`\n🗑️  删除机器人 ${id}...`);
    const res = await request('DELETE', `/openclaw/robots/${id}`, null, token);
    if (res.status === 200 && res.body.success) {
      console.log('✅ 删除成功！');
    } else {
      console.error(`❌ 删除失败: ${res.body?.error || '机器人不存在'}`);
      process.exit(1);
    }
  }
}

// 分配任务
async function cmdTask(args) {
  let { id, type } = args;
  if (!id) { console.error('❌ 请提供 --id <机器人ID>'); process.exit(1); }
  type = type || 'patrol';
  const validTypes = ['patrol', 'greet', 'deliver', 'explore'];
  if (!validTypes.includes(type)) {
    console.error(`❌ 任务类型无效，可选：${validTypes.join(', ')}`); process.exit(1);
  }

  const coords = resolveCoords(args);
  const auth = await getAuthToken(args);
  const token = auth?.token || null;

  const getRes = await request('GET', `/openclaw/robots/${id}`, null, token);
  if (getRes.status !== 200 || !getRes.body.success) {
    console.error(`❌ 机器人 ${id} 不存在`); process.exit(1);
  }
  const current = getRes.body.robot;
  const task = {
    type, progress: 0,
    ...(coords ? { targetLocation: coords } : {}),
    ...(args.user ? { targetUser: args.user } : {}),
  };
  const payload = { ...current, status: 'tasking', task };

  console.log(`\n🎯 给 "${current.name}" 分配 [${type}] 任务...`);
  const res = await request('PUT', `/openclaw/robots/${id}`, payload, token);
  if (res.status === 200 && res.body.success) {
    console.log(`\n✅ 任务分配成功！`);
    printRobot(res.body.robot || res.body.data);
    console.log(`\n  🗺️  查看地图: ${MAP_URL}`);
  } else {
    console.error(`\n❌ 失败: ${res.body?.error || JSON.stringify(res.body)}`);
    process.exit(1);
  }
}

// ─── 帮助 ──────────────────────────────────────────────────────
function printHelp() {
  console.log(`
╔═══════════════════════════════════════════════════════╗
║     PowPow Robot Deployer  — WorkBuddy Skill          ║
║     部署 OpenClaw Agent 到 PowPow 全球地图             ║
╚═══════════════════════════════════════════════════════╝

用法:  node deploy-robot.js <命令> [选项]

命令:
  register  注册新账号
            --username "名字" --password "密码" [--nickname "昵称"]

  login     登录（token 缓存30天，后续无需重复登录）
            --username "名字" --password "密码"

  create    🚀 一键注册+部署机器人（最常用！）
            --username "名字" --password "密码"
            --name "机器人名" --city 北京
            [--desc "描述"] [--avatar "头像URL"]
            ※ 若账号不存在会自动注册

  list      📋 列出地图上所有机器人

  move      📍 移动机器人
            --id <robotId> --city <城市>  或  --lat/--lng

  delete    🗑️  删除机器人
            --id <robotId>  或  --all（删除全部）

  task      🎯 给机器人分配任务
            --id <robotId> --type patrol|greet|deliver|explore
            [--city <城市>] 或 [--lat/--lng]

城市预设（--city 参数）:
  ${Object.keys(CITIES).join('  ')}

示例:
  # 一句话部署（自动注册+登录+创建）
  node deploy-robot.js create --username mybot --password abc123 --name "探索者" --city 北京

  # 登录后（token缓存），直接创建
  node deploy-robot.js create --name "上海守卫" --city 上海

  # 查看地图
  node deploy-robot.js list

  # 移动机器人
  node deploy-robot.js move --id abc-123 --city 深圳

  # 删除全部
  node deploy-robot.js delete --all

地图: ${MAP_URL}
`);
}

// ─── 主入口 ────────────────────────────────────────────────────
async function main() {
  const [,, command, ...rest] = process.argv;
  const args = parseArgs(rest);

  const commands = {
    register: cmdRegister,
    login:    cmdLogin,
    create:   cmdCreate,
    list:     cmdList,
    move:     cmdMove,
    delete:   cmdDelete,
    task:     cmdTask,
  };

  if (!command || command === 'help' || command === '--help') {
    printHelp(); return;
  }

  const fn = commands[command];
  if (!fn) {
    console.error(`❌ 未知命令: "${command}"。运行 help 查看用法。`);
    process.exit(1);
  }

  try {
    await fn(args);
  } catch (err) {
    console.error(`\n❌ 执行出错: ${err.message}`);
    if (err.code === 'ENOTFOUND' || err.code === 'ECONNREFUSED') {
      console.error('   请检查网络，或确认 https://global.powpow.online 是否可访问');
    }
    process.exit(1);
  }
}

main();
