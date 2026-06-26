/**
 * IMA 通用上传脚本 — 将 Markdown/文本文件上传到指定知识库
 * 
 * 用法: node scripts/ima-upload.cjs <文件路径> <知识库KB_ID> [标题]
 * 
 * 示例:
 *   node scripts/ima-upload.cjs memory/报告.md fh6uPoAPAxgoak... "我的报告"
 * 
 * 依赖: 环境变量 IMA_OPENAPI_CLIENTID + IMA_OPENAPI_APIKEY
 * 流程: import_doc(创建笔记) → add_knowledge(关联到知识库)
 * 
 * 退出码: 0=成功, 1=失败
 * 输出JSON(成功): {"ok":true,"note_id":"...","media_id":"...","kb_id":"..."}
 * 输出JSON(失败): {"ok":false,"error":"..."}
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

// ── 参数解析 ──
const args = process.argv.slice(2);
if (args.length < 2) {
  console.error(JSON.stringify({ ok: false, error: '用法: node scripts/ima-upload.cjs <文件路径> <KB_ID> [标题]' }));
  process.exit(1);
}

const filePath = path.resolve(args[0]);
const kbId = args[1];
const title = args[2] || path.basename(filePath, path.extname(filePath));

// ── 凭证 ──
const clientId = process.env.IMA_OPENAPI_CLIENTID;
const apiKey = process.env.IMA_OPENAPI_APIKEY;
if (!clientId || !apiKey) {
  console.error(JSON.stringify({ ok: false, error: '缺少 IMA 凭证（IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY）' }));
  process.exit(1);
}

// ── 文件读取 ──
if (!fs.existsSync(filePath)) {
  console.error(JSON.stringify({ ok: false, error: `文件不存在: ${filePath}` }));
  process.exit(1);
}

const content = fs.readFileSync(filePath, 'utf8');
const fileName = path.basename(filePath);

// ── API 调用封装 ──
const SKILL_DIR = path.resolve(process.env.USERPROFILE, '.openclaw/skills/ima-skill');
const apiScript = path.join(SKILL_DIR, 'ima_api.cjs');

function callApi(method, payloadObj) {
  const opts = JSON.stringify({ clientId, apiKey });
  const payload = JSON.stringify(payloadObj);
  const proc = spawnSync(process.execPath, [apiScript, method, payload, opts], {
    encoding: 'utf8', maxBuffer: 100 * 1024 * 1024, windowsHide: true
  });
  if (proc.error) throw new Error(proc.error.message);
  if (proc.status !== 0) throw new Error(proc.stderr || `Exit code ${proc.status}`);
  return proc.stdout.trim();
}

// ── 主流程 ──
function main() {
  // Step 1: import_doc — 创建笔记
  const ext = path.extname(filePath).toLowerCase();
  const isMd = ext === '.md' || ext === '.markdown';
  const isTxt = ext === '.txt';

  if (!isMd && !isTxt) {
    console.error(JSON.stringify({ ok: false, error: `不支持的文件类型 ${ext}，仅支持 .md / .txt / .markdown` }));
    process.exit(1);
  }

  const r1 = callApi('openapi/note/v1/import_doc', {
    title,
    content,
    content_format: 1  // 1=markdown
  });

  let noteId;
  try {
    const d = JSON.parse(r1);
    if (d.code !== 0) throw new Error(d.msg || 'import_doc 失败');
    noteId = d.data?.note_id || d.data?.id;
  } catch (e) {
    console.error(JSON.stringify({ ok: false, error: `import_doc 失败: ${e.message}` }));
    process.exit(1);
  }

  if (!noteId) {
    console.error(JSON.stringify({ ok: false, error: 'import_doc 返回中未找到 note_id' }));
    process.exit(1);
  }

  // Step 2: add_knowledge — 关联到知识库
  const r2 = callApi('openapi/wiki/v1/add_knowledge', {
    media_type: 11,
    note_info: { content_id: noteId },
    knowledge_base_id: kbId
  });

  let mediaId;
  try {
    const d2 = JSON.parse(r2);
    if (d2.code !== 0) throw new Error(d2.msg || 'add_knowledge 失败');
    mediaId = d2.data?.media_id || '';
  } catch (e) {
    console.error(JSON.stringify({ ok: false, error: `add_knowledge 失败: ${e.message}`, note_id: noteId }));
    process.exit(1);
  }

  console.log(JSON.stringify({
    ok: true,
    note_id: noteId,
    media_id: mediaId,
    kb_id: kbId,
    title,
    file: fileName,
    size: Buffer.byteLength(content, 'utf8')
  }));
}

main();
