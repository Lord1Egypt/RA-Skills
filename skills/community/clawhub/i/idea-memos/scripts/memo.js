#!/usr/bin/env node
/**
 * 硅虾备忘录 CLI - 给硅虾用的命令行工具
 * 用法: node memo.js <command> [args]
 * 
 * 命令:
 *   list                  列出所有备忘录
 *   list --tag <tag>      按标签筛选
 *   list --search <关键词>  搜索
 *   show <id>             查看单条
 *   add <标题>            快速新增（会从 stdin 读内容）
 *   add -t <标题> -c <内容>  -g <标签1,标签2>
 *   edit <id> -t <标题> -c <内容> -g <标签1,标签2>
 *   pin <id>              置顶/取消置顶
 *   rm <id>               删除
 */

const BASE = 'http://localhost:3377';

async function api(method, path, body) {
  const opts = { method, headers: {} };
  if (body) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(`${BASE}${path}`, opts);
  return res.json();
}

function formatMemo(m, verbose) {
  const tags = (m.tags || []).map(t => `#${t}`).join(' ');
  const pin = m.pinned ? '📌 ' : '';
  const title = m.title || '(无标题)';
  if (!verbose) {
    return `  ${pin}[${m.id}] ${title} ${tags ? '('+tags+')' : ''}`;
  }
  return `
┌─ ${pin}${title} ${tags ? '— ' + tags : ''}
│ ${m.created_at}${m.pinned ? ' · 置顶' : ''}
│
${(m.content || '').split('\n').map(l => '│ ' + l).join('\n')}
└─
`;
}

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === 'list' || cmd === 'ls') {
    const search = args.find(a => a.startsWith('--search='))?.split('=')[1] || 
                   args[args.indexOf('--search') + 1];
    const tag = args.find(a => a.startsWith('--tag='))?.split('=')[1] ||
                args[args.indexOf('--tag') + 1];
    const params = {};
    if (search) params.search = search;
    if (tag) params.tag = tag;
    const data = await api('GET', '/api/memos?' + new URLSearchParams(params));
    if (data.memos.length === 0) {
      console.log('🫙  空空如也');
      return;
    }
    console.log(`📝 共 ${data.total} 条:\n`);
    data.memos.forEach(m => console.log(formatMemo(m)));
    return;
  }

  if (cmd === 'show' || cmd === 'get') {
    const id = parseInt(args[1]);
    if (!id) { console.log('⚠️  需要 ID'); return; }
    const data = await api('GET', `/api/memos/${id}`);
    if (!data.ok) { console.log('❌', data.error); return; }
    console.log(formatMemo(data.memo, true));
    return;
  }

  if (cmd === 'add' || cmd === 'create') {
    const ti = args.find(a => a.startsWith('-t='))?.slice(3) ||
               args[args.indexOf('-t') + 1];
    let content = args.find(a => a.startsWith('-c='))?.slice(3) ||
                  args[args.indexOf('-c') + 1];
    const tags = args.find(a => a.startsWith('-g='))?.slice(3)?.split(/[,，]/) ||
                 (args.includes('-g') ? args[args.indexOf('-g') + 1]?.split(/[,，]/) : []);

    // If no -c, read from pipe/stdin
    if (!content && !process.stdin.isTTY) {
      const chunks = [];
      for await (const chunk of process.stdin) chunks.push(chunk);
      content = Buffer.concat(chunks).toString().trim();
    }

    if (!ti && !content) { console.log('⚠️  需要标题(-t)或内容(-c)'); return; }

    const data = await api('POST', '/api/memos', {
      title: ti || '',
      content: content || '',
      tags: tags || []
    });
    console.log(`✅ 已创建 [#${data.memo.id}]`);
    console.log(formatMemo(data.memo, true));
    return;
  }

  if (cmd === 'edit' || cmd === 'update') {
    const id = parseInt(args[1]);
    if (!id) { console.log('⚠️  需要 ID'); return; }
    const ti = args.find(a => a.startsWith('-t='))?.slice(3) || undefined;
    let content = args.find(a => a.startsWith('-c='))?.slice(3) || undefined;
    const tags = args.find(a => a.startsWith('-g='))?.slice(3)?.split(/[,，]/) || undefined;

    const body = {};
    if (ti !== undefined) body.title = ti;
    if (content !== undefined) body.content = content;
    if (tags !== undefined) body.tags = tags;

    const data = await api('PUT', `/api/memos/${id}`, body);
    if (!data.ok) { console.log('❌', data.error); return; }
    console.log('✅ 已更新');
    console.log(formatMemo(data.memo, true));
    return;
  }

  if (cmd === 'pin') {
    const id = parseInt(args[1]);
    if (!id) { console.log('⚠️  需要 ID'); return; }
    // Toggle: first get current state
    const cur = await api('GET', `/api/memos/${id}`);
    if (!cur.ok) { console.log('❌', cur.error); return; }
    const data = await api('PUT', `/api/memos/${id}`, { pinned: !cur.memo.pinned });
    console.log(`📌 ${data.memo.pinned ? '已置顶' : '已取消置顶'}`);
    return;
  }

  if (cmd === 'rm' || cmd === 'delete') {
    const id = parseInt(args[1]);
    if (!id) { console.log('⚠️  需要 ID'); return; }
    const data = await api('DELETE', `/api/memos/${id}`);
    if (!data.ok) { console.log('❌', data.error); return; }
    console.log('🗑️  已删除');
    return;
  }

  console.log(`
🦐 硅虾备忘录 CLI

用法:
  node memo.js list [--tag <tag>] [--search <关键词>]
  node memo.js show <id>
  node memo.js add -t <标题> -c <内容> -g <标签1,标签2>
  node memo.js edit <id> [-t <标题>] [-c <内容>] [-g <标签1,标签2>]
  node memo.js pin <id>
  node memo.js rm <id>
`);
}

main().catch(e => console.error('💥', e.message));
