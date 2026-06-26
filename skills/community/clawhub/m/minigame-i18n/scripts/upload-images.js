#!/usr/bin/env node
/**
 * MCP 图片上传辅助脚本
 *
 * 将图片文件打包为 zip 并通过 MCP 分片上传接口上传到服务端。
 * 直接通过 HTTP 请求调用 MCP 接口，认证参数从多个 IDE 配置路径自动读取。
 * 支持 WorkBuddy/CodeBuddy、Cursor、Claude Code、Codex 等 IDE 的 mcp.json。
 *
 * 使用方法：
 *   node upload-images.js --project <projectRoot> --images <img1,img2,...> [options]
 *
 * 参数：
 *   --project       项目根目录路径
 *   --images        要上传的图片文件列表（逗号分隔的相对路径）
 *   --images-file   包含图片路径列表的文件（每行一个相对路径）
 *   --mcp-url       MCP 服务端地址（默认从 mcp.json 读取）
 *   --appid         小游戏 AppID（默认从 mcp.json 读取）
 *   --token         访问令牌（默认从 mcp.json 读取）
 *   --chunk-size    分片大小，单位字节，指 base64 编码前的原始字节（默认 2MB）
 *   --output        输出 file_id 到指定文件（JSON 格式）
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const { execSync } = require('child_process');

// ============================================================
// 参数解析
// ============================================================

const args = parseArgs(process.argv.slice(2));
const PROJECT_ROOT = path.resolve(args.project || process.cwd());
const CHUNK_SIZE = parseInt(args['chunk-size']) || 2 * 1024 * 1024; // 2MB 原始字节
const OUTPUT_FILE = args.output || null;

// 解析图片列表
let IMAGE_LIST = [];
if (args.images) {
  IMAGE_LIST = args.images.split(',').map(s => s.trim()).filter(Boolean);
} else if (args['images-file']) {
  const filePath = path.resolve(args['images-file']);
  const content = fs.readFileSync(filePath, 'utf8');
  IMAGE_LIST = content.split(/\r?\n/).map(s => s.trim()).filter(Boolean);
}

// ============================================================
// MCP 配置
// ============================================================

let MCP_URL, APPID, TOKEN;

function loadMcpConfig() {
  MCP_URL = args['mcp-url'];
  APPID = args.appid;
  TOKEN = args.token;

  if (!MCP_URL || !APPID || !TOKEN) {
    const homeDir = process.env.USERPROFILE || process.env.HOME || '';
    const mcpJsonPaths = [
      path.join(PROJECT_ROOT, 'mcp.json'),
      // 项目级配置（优先）
      path.join(PROJECT_ROOT, '.workbuddy', 'mcp.json'),
      path.join(PROJECT_ROOT, '.codebuddy', 'mcp.json'),
      path.join(PROJECT_ROOT, '.cursor', 'mcp.json'),
      path.join(PROJECT_ROOT, '.claude', 'mcp.json'),
      path.join(PROJECT_ROOT, '.codex', 'mcp.json'),
      // 各 IDE 用户级配置
      path.join(homeDir, '.workbuddy', 'mcp.json'),   // WorkBuddy
      path.join(homeDir, '.codebuddy', 'mcp.json'),    // CodeBuddy
      path.join(homeDir, '.cursor', 'mcp.json'),       // Cursor
      path.join(homeDir, '.claude', 'mcp.json'),       // Claude Code
      path.join(homeDir, '.codex', 'mcp.json'),        // Codex (OpenAI)
    ];

    for (const mcpPath of mcpJsonPaths) {
      if (fs.existsSync(mcpPath)) {
        try {
          const mcpConfig = JSON.parse(fs.readFileSync(mcpPath, 'utf8'));
          const l10nConfig = mcpConfig.mcpServers && mcpConfig.mcpServers['minigame-l10n'];
          if (l10nConfig) {
            MCP_URL = MCP_URL || l10nConfig.url;
            APPID = APPID || (l10nConfig.headers && l10nConfig.headers.APPID);
            TOKEN = TOKEN || (l10nConfig.headers && l10nConfig.headers.TOKEN);
            console.log(`✅ 从 ${mcpPath} 读取 MCP 配置`);
            break;
          }
        } catch (e) { /* ignore */ }
      }
    }
  }

  if (!MCP_URL || !APPID || !TOKEN) {
    console.error('❌ 缺少 MCP 配置。请提供 --mcp-url/--appid/--token 或确保以下任一路径有 minigame-l10n 配置：');
    console.error('   ~/.workbuddy/mcp.json (WorkBuddy)');
    console.error('   ~/.codebuddy/mcp.json (CodeBuddy)');
    console.error('   ~/.cursor/mcp.json (Cursor)');
    console.error('   ~/.claude/mcp.json (Claude Code)');
    console.error('   ~/.codex/mcp.json (Codex)');
    process.exit(1);
  }

  console.log(`   MCP URL: ${MCP_URL}`);
  console.log(`   AppID: ${APPID}`);
}

// ============================================================
// MCP HTTP 调用
// ============================================================

let requestId = 1;

function mcpCall(toolName, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0',
      id: requestId++,
      method: 'tools/call',
      params: { name: toolName, arguments: params }
    });

    const url = new URL(MCP_URL);
    const isHttps = url.protocol === 'https:';
    const transport = isHttps ? https : http;

    const reqOptions = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + (url.search || ''),
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'APPID': APPID,
        'TOKEN': TOKEN,
        'Content-Length': Buffer.byteLength(body)
      }
    };

    const req = transport.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          // 修复服务端可能返回空 id: "id":, → "id":null,
          const fixedData = data.replace(/"id"\s*:(\s*),/g, '"id":null,');
          const json = JSON.parse(fixedData);

          if (json.error) {
            reject(new Error(`[${toolName}] code=${json.error.code}, message=${json.error.message}`));
            return;
          }

          // 从 MCP content 格式中提取数据
          const result = json.result;
          if (result && result.content) {
            for (const item of result.content) {
              if (item.type === 'text' && item.text) {
                try {
                  resolve(JSON.parse(item.text));
                } catch (e) {
                  resolve(item.text);
                }
                return;
              }
            }
          }
          resolve(result);
        } catch (e) {
          reject(new Error(`[${toolName}] JSON parse error: ${e.message}\nResponse: ${data.substring(0, 500)}`));
        }
      });
    });

    req.on('error', (e) => reject(new Error(`[${toolName}] HTTP error: ${e.message}`)));
    req.setTimeout(120000, () => {
      req.destroy();
      reject(new Error(`[${toolName}] Timeout 120s`));
    });

    req.write(body);
    req.end();
  });
}

// ============================================================
// ZIP 打包
// ============================================================

function createImageZip(imageRelPaths) {
  const tempDir = path.join(PROJECT_ROOT, 'i18n', '.upload_temp_' + Date.now());
  const zipPath = path.join(PROJECT_ROOT, 'i18n', '.upload_' + Date.now() + '.zip');

  try {
    fs.mkdirSync(tempDir, { recursive: true });
    fs.writeFileSync(path.join(tempDir, 'data.json'), '[]', 'utf8');

    const filesDir = path.join(tempDir, 'files');
    let copiedCount = 0;

    for (const relPath of imageRelPaths) {
      const srcPath = path.join(PROJECT_ROOT, relPath);
      if (!fs.existsSync(srcPath)) {
        console.warn(`  ⚠️ 图片不存在，跳过: ${relPath}`);
        continue;
      }
      const destPath = path.join(filesDir, relPath);
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      fs.copyFileSync(srcPath, destPath);
      copiedCount++;
    }

    if (copiedCount === 0) {
      throw new Error('没有有效的图片文件可以打包');
    }

    console.log(`📦 打包 ${copiedCount} 张图片...`);

    if (process.platform === 'win32') {
      execSync(
        `powershell -Command "Compress-Archive -Path '${tempDir}${path.sep}*' -DestinationPath '${zipPath}' -Force"`,
        { stdio: 'pipe' }
      );
    } else {
      execSync(`cd "${tempDir}" && zip -r "${zipPath}" .`, { stdio: 'pipe' });
    }

    const stat = fs.statSync(zipPath);
    console.log(`✅ ZIP 已创建: ${(stat.size / 1024).toFixed(1)} KB`);
    return zipPath;
  } finally {
    try { fs.rmSync(tempDir, { recursive: true, force: true }); } catch (e) { /* ignore */ }
  }
}

// ============================================================
// 分片上传核心逻辑
// ============================================================

async function uploadZip(zipPath) {
  const zipBuf = fs.readFileSync(zipPath);
  const totalBytes = zipBuf.length;
  // 分片大小是指 base64 编码前的原始字节数
  const totalChunks = Math.ceil(totalBytes / CHUNK_SIZE);

  console.log(`\n📤 分片上传 (${(totalBytes / 1024).toFixed(1)} KB, ${totalChunks} 片, 每片原始字节 ≤ ${(CHUNK_SIZE / 1024 / 1024).toFixed(1)} MB)`);

  // Step 1: Init
  console.log('\n[1/3] 初始化上传...');
  const initResult = await mcpCall('UploadScanFilesInitMcp', { file_type: 1 });
  const fileId = initResult.file_id;
  if (fileId === undefined || fileId === null) {
    throw new Error(`Init 未返回 file_id: ${JSON.stringify(initResult)}`);
  }
  console.log(`  ✅ file_id: ${fileId}`);

  // Step 2: Upload parts
  // 关键：先按 CHUNK_SIZE 切分原始字节，再对每片单独做 base64 编码
  console.log(`\n[2/3] 上传分片...`);
  const partList = [];

  for (let i = 0; i < totalChunks; i++) {
    const start = i * CHUNK_SIZE;
    const end = Math.min(start + CHUNK_SIZE, totalBytes);
    const chunkBuf = zipBuf.slice(start, end);
    const chunkB64 = chunkBuf.toString('base64');
    const partNum = i + 1;

    process.stdout.write(`  分片 ${partNum}/${totalChunks}: ${chunkBuf.length} 字节 → ${chunkB64.length} chars base64 ... `);

    const partResult = await mcpCall('UploadScanFilesPartMcp', {
      file_id: fileId,
      part_number: partNum,
      content_base64: chunkB64
    });

    const etag = typeof partResult === 'string' ? partResult : (partResult && partResult.etag);
    if (!etag) {
      throw new Error(`Part ${partNum} 未返回 etag: ${JSON.stringify(partResult)}`);
    }

    partList.push({ part_number: partNum, etag: String(etag) });
    console.log(`✅ etag: ${String(etag).substring(0, 16)}...`);
  }

  // Step 3: Complete
  console.log(`\n[3/3] 完成上传...`);
  await mcpCall('UploadScanFilesCompleteMcp', {
    file_id: fileId,
    part_list: partList
  });
  console.log(`  ✅ 合并完成`);

  return fileId;
}

// ============================================================
// 主流程
// ============================================================

async function main() {
  console.log('🖼️  MCP 图片上传工具');
  console.log(`   项目路径: ${PROJECT_ROOT}`);
  console.log(`   图片数量: ${IMAGE_LIST.length}`);
  console.log(`   分片大小: ${(CHUNK_SIZE / 1024 / 1024).toFixed(1)} MB（base64 编码前）`);
  console.log('');

  if (IMAGE_LIST.length === 0) {
    console.error('❌ 未指定图片文件。使用 --images 或 --images-file');
    process.exit(1);
  }

  loadMcpConfig();

  const zipPath = createImageZip(IMAGE_LIST);

  let fileId;
  try {
    fileId = await uploadZip(zipPath);
  } finally {
    try { fs.unlinkSync(zipPath); } catch (e) { /* ignore */ }
  }

  // 输出结果
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`✅ 上传成功！`);
  console.log(`   file_id: ${fileId}`);
  console.log(`   图片数: ${IMAGE_LIST.length}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  const outputData = {
    fileId,
    timestamp: new Date().toISOString(),
    imageCount: IMAGE_LIST.length,
    images: IMAGE_LIST
  };

  const outPath = OUTPUT_FILE || path.join(PROJECT_ROOT, 'i18n', 'upload_result.json');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(outputData, null, 2), 'utf8');
  console.log(`📄 结果: ${outPath}`);

  // 供 AI 捕获
  console.log(`\n__FILE_ID__=${fileId}`);
}

// ============================================================
// 工具函数
// ============================================================

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].substring(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        result[key] = next;
        i++;
      } else {
        result[key] = true;
      }
    }
  }
  return result;
}

main().catch(err => {
  console.error(`\n❌ 上传失败: ${err.message}`);
  process.exit(1);
});
