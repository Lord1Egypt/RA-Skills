/**
 * IELTS Reading Review Skill — 匿名使用统计 Worker
 * 
 * 部署到 Cloudflare Workers，绑定一个 KV namespace（STATS）
 * 
 * 功能：
 *   POST /ping  — 记录一次使用事件（匿名，仅 event + version + timestamp）
 *   GET  /stats — 返回统计摘要（总次数、按版本、按日期）
 *   GET  /       — 健康检查
 * 
 * 隐私：不收集 IP、用户名、文件内容等任何个人信息
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Health check
    if (url.pathname === '/' && request.method === 'GET') {
      return new Response(JSON.stringify({ status: 'ok', service: 'ielts-skill-stats' }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Record a usage event
    if (url.pathname === '/ping' && request.method === 'POST') {
      try {
        let body = {};
        try {
          body = await request.json();
        } catch {
          // empty body is fine
        }

        const event = String(body.event || 'unknown').slice(0, 50);
        const version = String(body.version || 'unknown').slice(0, 20);
        const now = new Date();
        const dateKey = now.toISOString().slice(0, 10); // YYYY-MM-DD

        // Increment total counter
        const totalKey = 'total';
        const total = parseInt(await env.STATS.get(totalKey) || '0', 10);
        await env.STATS.put(totalKey, String(total + 1));

        // Increment daily counter
        const dailyKey = `daily:${dateKey}`;
        const daily = parseInt(await env.STATS.get(dailyKey) || '0', 10);
        await env.STATS.put(dailyKey, String(daily + 1));

        // Increment per-event counter
        const eventKey = `event:${event}`;
        const eventCount = parseInt(await env.STATS.get(eventKey) || '0', 10);
        await env.STATS.put(eventKey, String(eventCount + 1));

        // Increment per-version counter
        const versionKey = `version:${version}`;
        const versionCount = parseInt(await env.STATS.get(versionKey) || '0', 10);
        await env.STATS.put(versionKey, String(versionCount + 1));

        // Append to daily event log (max 500 entries per day to avoid bloat)
        const logKey = `log:${dateKey}`;
        const existingLog = await env.STATS.get(logKey) || '[]';
        const logArray = JSON.parse(existingLog);
        if (logArray.length < 500) {
          logArray.push({
            event,
            version,
            ts: now.toISOString(),
          });
          await env.STATS.put(logKey, JSON.stringify(logArray));
        }

        return new Response(JSON.stringify({ ok: true, total: total + 1 }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      } catch (err) {
        return new Response(JSON.stringify({ ok: false, error: err.message }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
    }

    // Get stats summary
    if (url.pathname === '/stats' && request.method === 'GET') {
      try {
        const total = parseInt(await env.STATS.get('total') || '0', 10);

        // Collect last 30 days of daily stats
        const dailyStats = {};
        const now = new Date();
        for (let i = 0; i < 30; i++) {
          const d = new Date(now);
          d.setDate(d.getDate() - i);
          const dateKey = d.toISOString().slice(0, 10);
          const count = parseInt(await env.STATS.get(`daily:${dateKey}`) || '0', 10);
          if (count > 0) {
            dailyStats[dateKey] = count;
          }
        }

        // Collect version stats (list known versions)
        const versionStats = {};
        const knownVersions = ['1.0.0', '1.1.0', '1.2.0', '2.0.0'];
        for (const v of knownVersions) {
          const count = parseInt(await env.STATS.get(`version:${v}`) || '0', 10);
          if (count > 0) {
            versionStats[v] = count;
          }
        }

        // Collect event stats
        const eventStats = {};
        const knownEvents = ['pdf_generated', 'skill_loaded', 'review_completed'];
        for (const e of knownEvents) {
          const count = parseInt(await env.STATS.get(`event:${e}`) || '0', 10);
          if (count > 0) {
            eventStats[e] = count;
          }
        }

        return new Response(JSON.stringify({
          total,
          daily: dailyStats,
          versions: versionStats,
          events: eventStats,
          generated_at: now.toISOString(),
        }, null, 2), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
  },
};
