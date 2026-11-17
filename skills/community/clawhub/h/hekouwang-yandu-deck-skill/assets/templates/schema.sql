-- 留言板表结构（D1）· 按 page 隔离（首页=home，每期=slug 如 suanli/ep04）
-- 本地：wrangler d1 execute hekouwang-comments --local  --file=schema.sql
-- 远程：wrangler d1 execute hekouwang-comments --remote --file=schema.sql
CREATE TABLE IF NOT EXISTS comments (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  page       TEXT    NOT NULL DEFAULT 'home', -- 归属页：home / suanli/ep04 / toushi/ep01 …
  nickname   TEXT    NOT NULL,
  content    TEXT    NOT NULL,
  created_at INTEGER NOT NULL,                -- Unix 秒
  ip_hash    TEXT,                            -- SHA256(salt|IP) 前 32 位，只用于限频，不存明文
  approved   INTEGER NOT NULL DEFAULT 1       -- 1=显示 0=隐藏（留后手做审核）
);
CREATE INDEX IF NOT EXISTS idx_comments_page    ON comments (page, id DESC);
CREATE INDEX IF NOT EXISTS idx_comments_iphash  ON comments (ip_hash);
