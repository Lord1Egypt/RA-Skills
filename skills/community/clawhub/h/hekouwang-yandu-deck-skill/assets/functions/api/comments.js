// 首页留言板 · Cloudflare Pages Functions + D1
// GET  /api/comments        → 拉最新已通过的留言（最多 200 条）
// POST /api/comments        → 发一条留言（校验 + 限频），body: { nickname, content, website(蜜罐) }
// 评论存在你自己的 Cloudflare D1（binding=DB）里，不经任何第三方。

const MAX_NICK = 24;      // 昵称最长
const MAX_BODY = 500;     // 正文最长
const MIN_BODY = 1;       // 正文最短（去空白后）
const LIST_LIMIT = 200;   // 一次最多返回
const RATE_WINDOW = 20;   // 同一 IP 两条留言最短间隔（秒）
// IP 只存加盐哈希、不存明文。盐取 Pages 环境变量 IP_SALT（wrangler pages secret put IP_SALT），
// 未配置时退回公开默认值，只够做限频，不算匿名化。
const DEFAULT_IP_SALT = "yandu-deck-default-salt";
const PAGE_RE = /^[a-z0-9][a-z0-9/_-]{0,60}$/; // 页 key 白名单：home / suanli/ep04 …

// 规范化页 key；非法一律归到 home，避免任意写入
function pageKey(v) {
  const s = String(v == null ? "" : v).trim().toLowerCase();
  return PAGE_RE.test(s) ? s : "home";
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

// 建表（幂等）——即使忘了跑 schema.sql 也能自愈
async function ensureSchema(db) {
  await db.exec(
    "CREATE TABLE IF NOT EXISTS comments (" +
      "id INTEGER PRIMARY KEY AUTOINCREMENT," +
      "page TEXT NOT NULL DEFAULT 'home'," +
      "nickname TEXT NOT NULL," +
      "content TEXT NOT NULL," +
      "created_at INTEGER NOT NULL," +
      "ip_hash TEXT," +
      "approved INTEGER NOT NULL DEFAULT 1" +
    ")"
  );
}

async function hashIP(ip, salt) {
  const buf = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode((salt || DEFAULT_IP_SALT) + "|" + (ip || "unknown"))
  );
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, 32);
}

// 折叠连续空白 + 去首尾；不接受纯空白
function clean(s, max) {
  return String(s == null ? "" : s).replace(/\s+/g, (m) => (m.includes("\n") ? "\n" : " ")).trim().slice(0, max);
}

export async function onRequestGet({ request, env }) {
  if (!env.DB) return json({ error: "未配置数据库" }, 500);
  try {
    await ensureSchema(env.DB);
    const page = pageKey(new URL(request.url).searchParams.get("page"));
    const { results } = await env.DB.prepare(
      "SELECT id, nickname, content, created_at FROM comments WHERE approved = 1 AND page = ? ORDER BY id DESC LIMIT ?"
    ).bind(page, LIST_LIMIT).all();
    return json({ comments: results || [] });
  } catch (e) {
    return json({ error: "读取失败", detail: String(e && e.message || e) }, 500);
  }
}

export async function onRequestPost({ request, env }) {
  if (!env.DB) return json({ error: "未配置数据库" }, 500);

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "请求格式不对" }, 400);
  }

  // 蜜罐：正常用户看不到 website 字段，机器人会填 → 静默丢弃（假装成功）
  if (body && String(body.website || "").trim() !== "") {
    return json({ ok: true });
  }

  const page = pageKey(body && body.page);
  const nickname = clean(body && body.nickname, MAX_NICK) || "匿名读者";
  const content = clean(body && body.content, MAX_BODY);

  if (content.length < MIN_BODY) return json({ error: "留言不能为空" }, 400);
  if (String(body && body.content || "").length > MAX_BODY + 200) {
    return json({ error: "留言太长了" }, 400);
  }

  try {
    await ensureSchema(env.DB);
    const ip = request.headers.get("CF-Connecting-IP") || "";
    const ipHash = await hashIP(ip, env.IP_SALT);
    const now = Math.floor(Date.now() / 1000);

    // 限频：同 IP 在 RATE_WINDOW 秒内已发过 → 429
    const recent = await env.DB.prepare(
      "SELECT created_at FROM comments WHERE ip_hash = ? ORDER BY id DESC LIMIT 1"
    ).bind(ipHash).first();
    if (recent && now - recent.created_at < RATE_WINDOW) {
      return json({ error: "发得太快啦，歇口气再来" }, 429);
    }

    const res = await env.DB.prepare(
      "INSERT INTO comments (page, nickname, content, created_at, ip_hash, approved) VALUES (?, ?, ?, ?, ?, 1)"
    ).bind(page, nickname, content, now, ipHash).run();

    return json({
      ok: true,
      comment: { id: res.meta.last_row_id, nickname, content, created_at: now },
    });
  } catch (e) {
    return json({ error: "写入失败", detail: String(e && e.message || e) }, 500);
  }
}
