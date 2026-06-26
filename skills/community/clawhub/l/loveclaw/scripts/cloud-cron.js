/**
 * LoveClaw - 云端版定时任务（精简版）
 * 匹配和报告生成均在 FC 服务端完成，skill 端只负责触发 + 通知路由。
 */

const path = require('path');
const fs = require('fs');
const os = require('os');
process.chdir(path.join(process.env.HOME || '/root', '.openclaw', 'workspace'));

require('./load-workspace-env').applyFromWorkspaceDotenv();

const cloudData = require('./cloud-data');

// ==================== 通知路由辅助 ====================

function loadSessionIdMap() {
  try {
    const p = path.join(os.homedir(), '.openclaw', 'workspace', 'skills', 'loveclaw', 'sessions.json');
    const raw = fs.readFileSync(p, 'utf8');
    const parsed = JSON.parse(raw);
    return parsed && parsed._idMap && typeof parsed._idMap === 'object' ? parsed._idMap : {};
  } catch {
    return {};
  }
}

function loadGatewaySessionRoutes() {
  try {
    const p = path.join(os.homedir(), '.openclaw', 'agents', 'main', 'sessions', 'sessions.json');
    const raw = fs.readFileSync(p, 'utf8');
    const parsed = JSON.parse(raw);
    const routes = [];
    for (const [k, v] of Object.entries(parsed || {})) {
      if (!k.startsWith('agent:main:')) continue;
      const parts = k.split(':');
      if (parts.length < 5) continue;
      const channel = String(parts[2] || '').trim().toLowerCase();
      const to = String(
        (v && (v.lastTo || (v.state && v.state.to) || (v.route && v.route.to) || (v.meta && v.meta.to))) || ''
      ).trim();
      if (!channel || !to) continue;
      routes.push({ channel, to, sessionKey: k });
    }
    return routes;
  } catch {
    return [];
  }
}

function looksPhone(v) {
  return /^1\d{10}$/.test(String(v || ''));
}

function normChannel(input) {
  const ch = String(input || '').trim().toLowerCase();
  if (!ch) return 'feishu';
  if (ch === 'wx' || ch === 'weixin') return 'wechat';
  return ch;
}

function normalizeTargetByChannel(channelInput, rawTarget, idMap) {
  const channel = normChannel(channelInput);
  let t = String(rawTarget || '').trim();
  if (!t) return '';

  if (channel === 'feishu') {
    if (/^(user|chat):/i.test(t)) return t;
    if (t.startsWith('ou_')) return `user:${t}`;
    if (t.startsWith('oc_')) return `chat:${t}`;
    if (looksPhone(t) && idMap && idMap[t]) {
      const mapped = String(idMap[t]).trim();
      if (mapped.startsWith('ou_')) return `user:${mapped}`;
      if (mapped.startsWith('oc_')) return `chat:${mapped}`;
      return mapped;
    }
    return t;
  }

  if (channel === 'whatsapp') {
    if (t.startsWith('+')) return t;
    if (looksPhone(t)) return `+86${t}`;
    return t;
  }

  return t;
}

function findRouteTarget(channelInput, candidates, idMap, routes) {
  const channel = normChannel(channelInput);
  const routeList = (routes || []).filter(r => r.channel === channel);
  if (routeList.length === 0) return '';

  const byTo = new Set(routeList.map(r => String(r.to || '').trim()).filter(Boolean));

  const feishuForms = (v) => {
    const t = String(v || '').trim();
    if (!t) return [];
    const forms = new Set([t]);
    if (t.startsWith('user:') || t.startsWith('chat:')) forms.add(t.replace(/^(user|chat):/i, ''));
    if (t.startsWith('ou_')) { forms.add(`user:${t}`); forms.add(`chat:${t}`); }
    if (t.startsWith('oc_')) { forms.add(`chat:${t}`); }
    return [...forms];
  };

  for (const c of candidates) {
    const raw = String(c || '').trim();
    if (!raw) continue;
    if (channel === 'feishu') {
      for (const f of feishuForms(raw)) { if (byTo.has(f)) return f; }
      if (looksPhone(raw) && idMap && idMap[raw]) {
        for (const f of feishuForms(String(idMap[raw]).trim())) { if (byTo.has(f)) return f; }
      }
    } else {
      if (byTo.has(raw)) return raw;
      const lowered = raw.toLowerCase();
      const hit = routeList.find(r => String(r.to || '').trim().toLowerCase() === lowered);
      if (hit) return String(hit.to || '').trim();
    }
  }
  return '';
}

function resolveNotificationTarget(channel, userId, delivery, idMap, routes) {
  const candidates = [
    delivery.notificationTarget,
    delivery.openId,
    userId,
  ];
  const routeTarget = findRouteTarget(channel, candidates, idMap, routes);
  if (routeTarget) return routeTarget;
  for (const c of candidates) {
    const normalized = normalizeTargetByChannel(channel, c, idMap);
    if (normalized) return normalized;
  }
  return '';
}

function isNotifyEnabled(v) {
  if (v === true || v === 1 || v === '1') return true;
  if (typeof v === 'string') {
    const s = v.trim().toLowerCase();
    return s === 'true' || s === '1';
  }
  return false;
}

// ==================== 每日匹配 ====================

async function runDailyMatching() {
  console.log('[匹配任务] 触发 FC 端匹配...');
  try {
    const result = await cloudData.triggerMatch();
    console.log(`[匹配任务] 完成：${result.pairsMatched} 对匹配, ${result.elapsedMs}ms`);
    if (result.stats) {
      const s = result.stats;
      console.log(
        `[匹配任务][指标] total=${s.totalProfiles}, eligible=${s.eligibleProfiles}, ` +
        `alreadyMatched=${s.alreadyMatchedToday}, invalid=${s.invalidProfiles}, ` +
        `edges=${s.keptEdges}, saved=${s.saveSuccessPairs}, failed=${s.saveFailedPairs}`
      );
    }
    return result;
  } catch (e) {
    console.error('[匹配任务] 触发失败:', e.message);
    return { pairsMatched: 0, error: e.message };
  }
}

// ==================== 本地用户列表 ====================

function loadLocalUserIds() {
  const sessions = loadSessionIdMap();
  const phones = new Set();
  for (const [phone] of Object.entries(sessions)) {
    if (looksPhone(phone)) phones.add(phone);
  }
  try {
    const p = path.join(os.homedir(), '.openclaw', 'workspace', 'skills', 'loveclaw', 'sessions.json');
    const raw = fs.readFileSync(p, 'utf8');
    const parsed = JSON.parse(raw);
    for (const [key, val] of Object.entries(parsed || {})) {
      if (key === '_idMap') continue;
      if (val && val.data && val.data.phone && looksPhone(val.data.phone)) {
        phones.add(val.data.phone);
      }
    }
  } catch {}
  return [...phones];
}

// ==================== 晚间报告 ====================

async function runEveningReports() {
  console.log('[报告任务] 逐用户获取报告...');

  try {
    const localUsers = loadLocalUserIds();
    console.log(`[报告任务] 本机用户数: ${localUsers.length} (${localUsers.join(', ')})`);

    if (localUsers.length === 0) {
      console.log('[报告任务] 本机无已注册用户，跳过');
      const payload = { version: 2, deliveries: [], matched: [], noMatch: [] };
      console.log(`[报告任务] 匹配报告数据：【REPORTS_JSON】${JSON.stringify(payload)}【REPORTS_JSON_END】`);
      return { matched: [], noMatch: [], deliveries: [] };
    }

    const sessionIdMap = loadSessionIdMap();
    const gatewayRoutes = loadGatewaySessionRoutes();
    const deliveries = [];

    for (const phone of localUsers) {
      try {
        const report = await cloudData.getMyReport(phone);
        if (!report || !report.success) {
          console.log(`[报告任务] ${phone}: 无数据或请求失败`);
          continue;
        }

        const profile = report.profile || {};
        const channel = normChannel(profile.channel) || 'feishu';
        const notifyEnabled = isNotifyEnabled(profile.notifyEnabled);

        if (!notifyEnabled) {
          console.log(`[报告任务] ${phone}: 推送未开启，跳过`);
          continue;
        }

        const kind = report.status === 'matched' ? 'match' : 'no_match';
        const target = resolveNotificationTarget(
          channel, phone,
          { notificationTarget: profile.notificationTarget, openId: profile.openId },
          sessionIdMap, gatewayRoutes
        );

        deliveries.push({
          kind,
          userId: phone,
          channel,
          target,
          openId: target,
          imageUrl: report.imageUrl || '',
          message: report.message || '',
        });
        console.log(`[报告任务] ${phone}: ${kind}, target=${target}`);
      } catch (e) {
        console.error(`[报告任务] ${phone} 失败:`, e.message);
      }
    }

    const matchCount = deliveries.filter(d => d.kind === 'match').length;
    const noMatchCount = deliveries.filter(d => d.kind === 'no_match').length;

    const payload = {
      version: 2,
      deliveries,
      matched: deliveries.filter(d => d.kind === 'match'),
      noMatch: deliveries.filter(d => d.kind === 'no_match'),
    };
    console.log(`[报告任务] 匹配报告数据：【REPORTS_JSON】${JSON.stringify(payload)}【REPORTS_JSON_END】`);

    if (deliveries.length === 0) {
      console.log('[报告任务] 今日无推送数据');
    } else {
      console.log(`[报告任务] 共 ${deliveries.length} 条推送（成功 ${matchCount}，未匹配 ${noMatchCount}）`);
    }
    return { matched: payload.matched, noMatch: payload.noMatch, deliveries };
  } catch (e) {
    console.error('[报告任务] 失败:', e.message);
    return { matched: [], noMatch: [], deliveries: [] };
  }
}

module.exports = { runDailyMatching, runEveningReports };

// ========================
// CLI 入口
// ========================
if (require.main === module) {
  const [, , command] = process.argv;

  if (command === 'match') {
    runDailyMatching().then(() => process.exit(0)).catch(e => {
      console.error('[匹配任务异常]', e);
      process.exit(1);
    });
  } else if (command === 'report') {
    runEveningReports().then(() => process.exit(0)).catch(e => {
      console.error('[报告任务异常]', e);
      process.exit(1);
    });
  } else {
    console.log('用法: node cloud-cron.js [match|report]');
    process.exit(1);
  }
}
