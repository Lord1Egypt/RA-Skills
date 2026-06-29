/**
 * OpenClaw Super Memory (Hermes Mind Evolution) - Installer
 * 
 * Run: node install.js
 * Restore: node install.js --restore
 */
const fs = require('fs');
const path = require('path');

function findOpenclawJson() {
  // 1. Try env variables
  const envHome = process.env.OPENCLAW_HOME || process.env.OPENCLAW_STATE_DIR;
  if (envHome) {
    const candidatePaths = [
      path.join(envHome, 'openclaw.json'),
      path.join(envHome, '.openclaw', 'openclaw.json')
    ];
    for (const p of candidatePaths) {
      if (fs.existsSync(p)) return path.resolve(p);
    }
  }

  // 2. Try relative paths walking up from current script file (__dirname)
  let current = __dirname;
  while (true) {
    const candidatePaths = [
      path.join(current, 'openclaw.json'),
      path.join(current, '.openclaw', 'openclaw.json')
    ];
    for (const p of candidatePaths) {
      if (fs.existsSync(p)) return path.resolve(p);
    }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }

  // 3. Try relative paths walking up from process working dir
  current = process.cwd();
  while (true) {
    const candidatePaths = [
      path.join(current, 'openclaw.json'),
      path.join(current, '.openclaw', 'openclaw.json')
    ];
    for (const p of candidatePaths) {
      if (fs.existsSync(p)) return path.resolve(p);
    }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }

  // 4. Try well-known locations (user home directory)
  const userHome = process.env.HOME || process.env.USERPROFILE || process.env.HOMEPATH;
  if (userHome) {
    const p = path.join(userHome, '.openclaw', 'openclaw.json');
    if (fs.existsSync(p)) return path.resolve(p);
  }

  // 5. Hardcoded docker fallbacks
  const fallbackPaths = [
    '/home/node/project/.openclaw/openclaw.json',
    '/root/project/.openclaw/openclaw.json'
  ];
  for (const p of fallbackPaths) {
    if (fs.existsSync(p)) return path.resolve(p);
  }

  return null;
}

const openclawJsonPath = findOpenclawJson();

if (!openclawJsonPath) {
  console.error('❌ Error: Could not locate openclaw.json in standard search directories.');
  process.exit(1);
}

console.log(`🔍 Located openclaw.json at: ${openclawJsonPath}`);

// Helper to resolve actual workspace path on host/container
function resolveWorkspacePath(jsonPath, workspaceStr) {
  const openclawDir = path.dirname(jsonPath);
  
  // If the path exists as-is on the current OS, return it
  if (fs.existsSync(workspaceStr)) {
    return path.resolve(workspaceStr);
  }
  
  // Otherwise, extract the last folder segment and resolve relative to .openclaw directory
  const baseName = path.basename(workspaceStr.replace(/\\/g, '/'));
  const resolved = path.resolve(openclawDir, baseName);
  if (fs.existsSync(resolved)) {
    return resolved;
  }
  
  // Fallback to resolving relative to the parent of .openclaw
  return path.resolve(path.dirname(openclawDir), baseName);
}

// Read openclaw.json
let config;
try {
  config = JSON.parse(fs.readFileSync(openclawJsonPath, 'utf8'));
} catch (err) {
  console.error('❌ Error parsing openclaw.json:', err.message);
  process.exit(1);
}

const agents = config.agents && config.agents.list ? config.agents.list : [];
if (agents.length === 0) {
  console.warn('⚠️ No agents found in openclaw.json.');
  process.exit(0);
}

const isRestore = process.argv.includes('--restore');

for (const agent of agents) {
  if (!agent.workspace) continue;
  const workspacePath = resolveWorkspacePath(openclawJsonPath, agent.workspace);
  const agentsMdPath = path.join(workspacePath, 'AGENTS.md');
  const memoryMdPath = path.join(workspacePath, 'MEMORY.md');
  const toolsMdPath = path.join(workspacePath, 'TOOLS.md');

  if (!fs.existsSync(agentsMdPath)) {
    console.warn(`⚠️ AGENTS.md not found in workspace: ${workspacePath}. Skipping.`);
    continue;
  }

  console.log(`Processing Agent "${agent.name}" (${agent.id}) at workspace: ${workspacePath}`);

  let content = fs.readFileSync(agentsMdPath, 'utf8');

  // Markers
  const startMarker = '\n<!-- openclaw:skill:super-memory:start -->';
  const endMarker = '<!-- openclaw:skill:super-memory:end -->\n';

  // Remove existing patch if present
  const startIndex = content.indexOf(startMarker);
  const endIndex = content.indexOf(endMarker);

  if (startIndex !== -1 && endIndex !== -1) {
    console.log(`  - Found existing super-memory patch in AGENTS.md. Removing it.`);
    content = content.substring(0, startIndex) + content.substring(endIndex + endMarker.length);
  }

  if (isRestore) {
    fs.writeFileSync(agentsMdPath, content, 'utf8');
    console.log(`  ✓ Successfully restored AGENTS.md for ${agent.name}!`);
    continue;
  }

  // Format file paths using the file:/// scheme and forward slashes for cross-platform links
  const formatFileUrl = (filePath) => {
    const normalized = filePath.replace(/\\/g, '/');
    return normalized.startsWith('/') ? `file://${normalized}` : `file:///${normalized}`;
  };
  const formattedMemoryUrl = formatFileUrl(memoryMdPath);
  const formattedToolsUrl = formatFileUrl(toolsMdPath);

  // Patch Content
  const patchContent = `${startMarker}
---

## 🧠 Quy tắc Tự tiến hóa & Tối ưu hóa Bộ não (Autonomous Mode)

Để nâng cấp trí thông minh, khả năng ghi nhớ dài hạn và tự động tiến hóa kỹ năng của bạn lên mức tối ưu và tự chủ cao nhất, bạn **BẮT BUỘC** phải tuân thủ nghiêm ngặt các hướng dẫn vận hành cốt lõi dưới đây:

### 1. Chủ động ghi nhớ dài hạn (Durable Memory Auto-Synthesis)
- **Tự động cập nhật**: Ngay khi hoàn thành một phiên làm việc, nếu phát hiện bất kỳ bài học kinh nghiệm nào (cú pháp code sửa lỗi, lỗi cài đặt API, cấu hình server, thói quen hoặc yêu cầu cụ thể của UserKent) → Bạn **bắt buộc** phải tự động cập nhật trực tiếp các thông tin này vào mục \`## Ghi chú\` của file [MEMORY.md](${formattedMemoryUrl}).
- **Tính tức thì**: Tuyệt đối không lưu ghi chú tạm thời ở log hay đợi cơ chế Dreaming ban đêm tổng hợp một cách thụ động. Hãy lưu trữ dạng gạch đầu dòng ngắn gọn, súc tích (1-2 câu chứa từ khóa chính và cách giải quyết) ngay trong phiên làm việc hiện tại để các phiên sau có thể đọc được ngay.

### 2. Tự động đóng gói Kỹ năng mới (Autonomous Skill Creation & Evolution)
- **Phát hiện quy trình lặp**: Khi thực hiện thành công các thao tác phức tạp (ví dụ: tạo tệp excel báo cáo đặc thù, cào dữ liệu Zalo/Facebook qua API tùy chỉnh, viết mã tự động cấu hình server...) → Hãy tự động tạo một file script Javascript helper tương ứng lưu vào thư mục \`skills/\` hoặc \`plugin-skills/\` của workspace (ví dụ: \`skills/custom-task.js\`).
- **Nâng cấp TOOLS.md**: Tự động cập nhật mô tả lệnh chạy của kỹ năng đó vào file [TOOLS.md](${formattedToolsUrl}) để các phiên làm việc sau bạn có thể tự gọi lại script thông qua lệnh hệ thống, tránh việc phải code lại từ đầu.

### 3. Vòng lặp phản tư cuối phiên (Self-Reflection Loop)
- Ở cuối mỗi phiên làm việc lớn hoặc trước khi gửi phản hồi cuối cùng cho UserKent, hãy dành 1 lượt suy nghĩ để phản tư (self-reflect):
  1. *Hôm nay mình có học được gì mới về hệ thống hoặc sở thích của Kent không?* → Cập nhật \`MEMORY.md\`.
  2. *Quy trình xử lý phức tạp vừa rồi có nên đóng gói thành script không?* → Tạo file Skill.
  3. *Có thông tin cũ nào trong MEMORY.md cần được dọn dẹp hoặc tối ưu lại không?* → Sửa đổi \`MEMORY.md\`.
  4. *Đã thực hiện xong các bước trên chưa?* → Báo cáo ngắn gọn kết quả tự học/tự cập nhật cho Kent.

${endMarker}`;

  // Find position to insert. We will append it at the end of the file.
  content = content.trim() + '\n' + patchContent;

  fs.writeFileSync(agentsMdPath, content, 'utf8');
  console.log(`  ✓ Successfully patched AGENTS.md for ${agent.name}!`);
}

console.log('🎉 Super Memory installation workflow completed successfully!');
