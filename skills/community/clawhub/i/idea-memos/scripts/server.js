const express = require('express');
const path = require('path');
const { listMemos, getMemo, createMemo, updateMemo, deleteMemo } = require('./db');

const app = express();
const PORT = 3377;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// CORS for local dev
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

// ---------- API ----------

// 列出备忘录
app.get('/api/memos', (req, res) => {
  const { page, pageSize, search, tag } = req.query;
  const result = listMemos({
    page: parseInt(page) || 1,
    pageSize: Math.min(parseInt(pageSize) || 20, 100),
    search,
    tag
  });
  res.json({ ok: true, ...result });
});

// 获取单条
app.get('/api/memos/:id', (req, res) => {
  const memo = getMemo(parseInt(req.params.id));
  if (!memo) return res.status(404).json({ ok: false, error: '没找到这条备忘录' });
  res.json({ ok: true, memo });
});

// 创建
app.post('/api/memos', (req, res) => {
  const { title, content, tags } = req.body;
  if (!content && !title) {
    return res.status(400).json({ ok: false, error: '标题或内容至少要有一个' });
  }
  const memo = createMemo({ title, content, tags });
  res.status(201).json({ ok: true, memo });
});

// 更新
app.put('/api/memos/:id', (req, res) => {
  const { title, content, tags, pinned } = req.body;
  const memo = updateMemo(parseInt(req.params.id), { title, content, tags, pinned });
  if (!memo) return res.status(404).json({ ok: false, error: '没找到这条备忘录' });
  res.json({ ok: true, memo });
});

// 删除
app.delete('/api/memos/:id', (req, res) => {
  const ok = deleteMemo(parseInt(req.params.id));
  if (!ok) return res.status(404).json({ ok: false, error: '没找到这条备忘录' });
  res.json({ ok: true });
});

// SPA fallback: serve index.html for all non-API routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🦐 硅虾备忘录已启动 → http://localhost:${PORT}`);
  console.log(`📝 API: http://localhost:${PORT}/api/memos`);
});
