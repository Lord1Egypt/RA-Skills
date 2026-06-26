#!/usr/bin/env python3
"""Memory Tree 最小可用实现（MVP）— 约 200 行，可直接复制到任何项目。"""
import sqlite3, hashlib, json, re, time
from pathlib import Path

class MemoryTreeMVP:
    """Memory Tree 最小实现：热路径摄入 + 全文检索。"""

    def __init__(self, db_path='memory.db'):
        self.db_path = Path(db_path)
        self._conn = sqlite3.connect(str(self.db_path))
        self._init_schema()

    def _init_schema(self):
        c = self._conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS memory_chunks (
            id TEXT PRIMARY KEY, session_id TEXT, content TEXT,
            content_hash TEXT, token_count INTEGER, source TEXT,
            role TEXT, timestamp REAL, score REAL, is_admitted INTEGER,
            score_reasons TEXT
        )''')
        c.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS memory_chunks_fts
            USING FTS5(content='memory_chunks', content_rowid='rowid')''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_chunks_session
            ON memory_chunks(session_id)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_chunks_score
            ON memory_chunks(score DESC)''')
        self._conn.commit()

    @staticmethod
    def _content_hash(text):
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    @staticmethod
    def _token_count(text):
        cn = len(re.findall(r'[\u4e00-\u9fff]', text))
        en = len(re.findall(r'[a-zA-Z]+', text))
        return int(cn * 1.5 + en * 1.3 + len(text) * 0.5)

    @staticmethod
    def _fast_score(text):
        """14 条规则快速打分，无 LLM。"""
        score, reasons = 0.0, []
        rules = [
            (r'记住|记忆|保存', 0.25, '用户要求记忆'),
            (r'偏好|喜欢|讨厌', 0.25, '用户偏好'),
            (r'\d+[万块元千]', 0.20, '金额信息'),
            (r'重要|必须|一定', 0.20, '重要标记'),
            (r'需要|想要|希望', 0.15, '情感需求'),
            (r'bug|错误|异常|报错', 0.15, '错误异常'),
            (r'v?\d+\.\d+', 0.10, '版本信息'),
            (r'project|项目|repo|仓库', 0.10, '项目相关'),
            (r'config|配置|setting', 0.10, '配置信息'),
            (r'成功|完成|搞定', 0.10, '成功完成'),
            (r'api.?key|token|secret|密码', 0.05, '凭证相关'),
            (r'\d{4}-\d{2}-\d{2}', 0.05, '时间信息'),
        ]
        for pattern, pts, reason in rules:
            if re.search(pattern, text, re.I):
                score += pts
                reasons.append(reason)
        if len(text.strip()) < 20:
            score *= 0.5
            reasons.append('短文本惩罚')
        return round(score, 3), reasons

    def ingest(self, session_id, messages, source='chat'):
        """摄入消息，返回生成的 chunk IDs。"""
        c = self._conn.cursor()
        chunks = []
        for i, msg in enumerate(messages):
            content = msg.get('content', '')
            cid = f"{session_id[:12]}-{msg.get('role','u')[:3]}-{i:03d}-{self._content_hash(content)}"
            score, reasons = self._fast_score(content)
            token_count = self._token_count(content)
            c.execute('''INSERT OR IGNORE INTO memory_chunks
                (id, session_id, content, content_hash, token_count, source, role, timestamp, score, is_admitted, score_reasons)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)''',
                (cid, session_id, content, self._content_hash(content), token_count,
                 source, msg.get('role','user'), msg.get('timestamp', time.time()), score,
                 json.dumps(reasons, ensure_ascii=False)))
            chunks.append({'id': cid, 'score': score, 'reasons': reasons})
        self._conn.commit()
        return chunks

    def search(self, query, limit=10, min_score=0.1):
        """搜索记忆（中文 LIKE / 英文 FTS5 MATCH）。"""
        c = self._conn.cursor()
        has_cjk = bool(re.search(r'[\u4e00-\u9fff]', query))
        if has_cjk:
            sql = '''SELECT id, session_id, content, score, is_admitted, score_reasons
                FROM memory_chunks WHERE content LIKE ? AND is_admitted >= 1 AND score >= ?
                ORDER BY score DESC LIMIT ?'''
            params = [f'%{query}%', min_score, limit]
        else:
            sql = '''SELECT c.id, c.session_id, c.content, c.score, c.is_admitted, c.score_reasons
                FROM memory_chunks c JOIN memory_chunks_fts f ON c.rowid = f.rowid
                WHERE f MATCH ? AND c.is_admitted >= 1 AND c.score >= ?
                ORDER BY c.score DESC LIMIT ?'''
            params = [query, min_score, limit]
        c.execute(sql, params)
        results = []
        for row in c.fetchall():
            results.append({
                'id': row[0], 'session_id': row[1], 'content': row[2],
                'score': row[3], 'is_admitted': row[4],
                'reasons': json.loads(row[5]) if row[5] else []
            })
        return results

    def stats(self):
        """全局统计。"""
        c = self._conn.cursor()
        c.execute('SELECT COUNT(*) FROM memory_chunks WHERE is_admitted >= 1')
        total = c.fetchone()[0]
        c.execute('SELECT COUNT(DISTINCT session_id) FROM memory_chunks')
        sessions = c.fetchone()[0]
        c.execute('SELECT AVG(score) FROM memory_chunks WHERE is_admitted >= 1')
        avg_score = c.fetchone()[0] or 0
        return {'total_chunks': total, 'sessions': sessions, 'avg_score': round(avg_score, 3)}

    def close(self):
        self._conn.close()


# ── 快速测试 ──
if __name__ == '__main__':
    mt = MemoryTreeMVP(':memory:')
    msgs = [
        {'role': 'user', 'content': '记住：项目预算 5 万，9 月 15 日前完成。', 'timestamp': time.time()},
        {'role': 'assistant', 'content': '已记住。项目预算 5 万，截止 9 月 15 日。', 'timestamp': time.time()},
        {'role': 'user', 'content': 'github.com/worm128/AI-YinMei 是项目仓库。', 'timestamp': time.time()},
        {'role': 'user', 'content': '偏好：使用免费方案，讨厌云 API 费用。', 'timestamp': time.time()},
    ]
    chunks = mt.ingest('test-session', msgs, source='qqbot')
    print(f'✅ 摄入 {len(chunks)} 个 chunk')
    for r in mt.search('预算', limit=3):
        print(f'  [{r["score"]:.2f}] {r["content"][:80]}')
    for r in mt.search('免费', limit=3):
        print(f'  [{r["score"]:.2f}] {r["content"][:80]}')
    print(f'📊 {mt.stats()}')
    mt.close()
