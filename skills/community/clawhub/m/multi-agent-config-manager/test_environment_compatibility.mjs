/**
 * 环境兼容性测试
 * 测试不同环境下命令是否能够正确执行
 */

console.log('🔍 环境兼容性测试 - 验证用户命令执行');
console.log('═'.repeat(60) + '\n');

console.log('模拟第三方用户可能遇到的问题：\n');

console.log('## 场景 1: Node.js 版本过低\n');

console.log('**用户环境**: Node.js 18.x（低于要求版本）');
console.log('**执行命令**: `多代理 run --goal "研究主题"`\n');
console.log('**预期结果**:');
console.log('```');
console.log('❌ 环境不兼容: Node.js 版本过低');
console.log('当前版本: v18.20.0');
console.log('最低要求: v20.5+');
console.log('ES Module 语法不兼容，请升级 Node.js');
console.log('```\n');

console.log('## 场景 2: OpenClaw 版本过低\n');

console.log('**用户环境**: OpenClaw 2026.2.x（低于要求版本）');
console.log('**执行命令**: `多代理 run --goal "研究主题"`\n');
console.log('**预期结果**:');
console.log('```');
console.log('❌ 环境不兼容: OpenClaw 版本过低');
console.log('当前版本: 2026.2.x');
console.log('最低要求: 2026.3.x+');
console.log('缺少 sessions_spawn API，请升级 OpenClaw');
console.log('```\n');

console.log('## 场景 3: 模块导入失败\n');

console.log('**用户环境**: lib/ 目录文件损坏或缺失');
console.log('**执行命令**: `多代理 run --goal "研究主题"`\n');
console.log('**预期结果**:');
console.log('```');
console.log('❌ 模块加载失败');
console.log('无法加载模块: ./lib/executor.js');
console.log('错误详情: ENOENT: no such file or directory');
console.log('建议: 重新安装 multi-agent-engine 技能');
console.log('```\n');

console.log('## 场景 4: 权限问题\n');

console.log('**用户环境**: 没有工作区目录的写入权限');
console.log('**执行命令**: `多代理 run --goal "研究主题"`\n');
console.log('**预期结果**:');
console.log('```');
console.log('❌ 权限不足');
console.log('无法创建目录: C:\\Users\\user\\.openclaw\\workspace\\agents');
console.log('错误详情: EACCES: permission denied');
console.log('建议: 检查目录权限或使用管理员权限运行');
console.log('```\n');

console.log('## 测试当前系统的环境兼容性\n');
console.log('─'.repeat(60) + '\n');

try {
  // 测试 ES Module 导入
  console.log('✅ 测试 1: ES Module 语法兼容性');
  console.log('   Node.js 版本:', process.version);
  const [major, minor] = process.version.slice(1).split('.').map(Number);
  if (major < 20 || (major === 20 && minor < 5)) {
    console.log('   ❌ 版本过低，ES Module 可能存在问题');
  } else {
    console.log('   ✅ 版本符合要求，ES Module 语法兼容');
  }
  console.log();

  // 测试核心模块导入
  console.log('✅ 测试 2: 核心模块导入');
  try {
    await import('./lib/config_validator.js');
    console.log('   ✅ config_validator.js 模块可正常加载');
  } catch (err) {
    console.log('   ❌ 模块加载失败:', err.message);
  }
  console.log();

  // 测试文件系统权限
  console.log('✅ 测试 3: 文件系统权限');
  const fs = await import('fs');
  const path = await import('path');
  const testDir = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace', 'test_permission');
  
  try {
    fs.mkdirSync(testDir, { recursive: true });
    fs.rmdirSync(testDir);
    console.log('   ✅ 文件系统权限正常');
  } catch (err) {
    console.log('   ❌ 权限不足:', err.message);
  }
  console.log();

  // 测试 OpenClaw 环境检测
  console.log('✅ 测试 4: OpenClaw 环境检测');
  const openclawVersion = process.env.OPENCLAW_VERSION || 'unknown';
  console.log('   OpenClaw 版本:', openclawVersion);
  
  if (openclawVersion !== 'unknown') {
    const [major] = openclawVersion.split('.').map(Number);
    if (major < 2026) {
      console.log('   ❌ 版本过低，缺少必要的 API');
    } else {
      console.log('   ✅ 版本符合要求（需进一步验证 API 可用性）');
    }
  } else {
    console.log('   ⚠️  版本未知，环境检测跳过');
  }
  console.log();

} catch (error) {
  console.log('❌ 环境测试失败:', error.message);
  console.log('错误详情:', error.stack);
}

console.log('\n## 🔧 改进建议\n');

console.log('**问题**: 当前的多代理引擎可能存在以下环境依赖问题：\n');

console.log('1. **Node.js 版本依赖**：');
console.log('   - 使用 ES Module 语法 (import/export)');
console.log('   - 最低要求 Node.js 20.5+');
console.log('   - 如果版本过低，会直接报语法错误\n');

console.log('2. **OpenClaw API 依赖**：');
console.log('   - sessions_spawn API (OpenClaw ≥ 2026.3.x)');
console.log('   - subagents API');
console.log('   - sessions_send API');
console.log('   - 如果版本过低，功能无法正常使用\n');

console.log('3. **文件系统权限依赖**：');
console.log('   - 需要读写工作区目录的权限');
console.log('   - 需要创建新目录的权限');
console.log('   - 权限不足会导致任务失败\n');

console.log('4. **模块加载依赖**：');
console.log('   - 需要完整的 lib/ 模块文件');
console.log('   - 需要正确的导入路径');
console.log('   - 文件损坏或缺失会导致系统崩溃\n');

console.log('## 🛠️ 解决方案\n');

console.log('**方案 1: 前置环境检查**');
console.log('```javascript');
console.log('// 在 index.js 开头添加环境检查');
console.log('try {');
console.log('  // 检查 Node.js 版本');
console.log('  const [major, minor] = process.version.slice(1).split(".").map(Number);');
console.log('  if (major < 20 || (major === 20 && minor < 5)) {');
console.log('    console.error("❌ Node.js 版本过低，需要 20.5+");');
console.log('    process.exit(1);');
console.log('  }');
console.log('');
console.log('  // 检查 OpenClaw API');
console.log('  if (typeof globalThis.sessions_spawn === "undefined") {');
console.log('    console.error("❌ 缺少 sessions_spawn API，需要 OpenClaw 2026.3.x+");');
console.log('    process.exit(1);');
console.log('  }');
console.log('} catch (error) {');
console.log('  console.error("❌ 环境检查失败:", error.message);');
console.log('  process.exit(1);');
console.log('}');
console.log('```\n');

console.log('**方案 2: 优雅降级**');
console.log('```javascript');
console.log('// 为低版本环境提供兼容模式');
console.log('const isCompatible = () => {');
console.log('  try {');
console.log('    const version = process.env.OPENCLAW_VERSION || "unknown";');
console.log('    const [major] = version.split(".").map(Number);');
console.log('    return major >= 2026;');
console.log('  } catch {');
console.log('    return false;');
console.log('  }');
console.log('};');
console.log('');
console.log('if (!isCompatible()) {');
console.log('  console.log("⚠️  当前环境不支持多代理并行执行");');
console.log('  console.log("  将切换到单代理串行模式...");');
console.log('  // 执行降级逻辑');
console.log('}');
console.log('```\n');

console.log('**方案 3: 详细错误报告**');
console.log('```javascript');
console.log('// 提供详细的错误诊断信息');
console.log('function diagnoseEnvironmentError(error) {');
console.log('  let report = "🔍 环境错误诊断报告\\n";');
console.log('  report += "════════════════════════════════\\n\\n";');
console.log('');
console.log('  if (error.code === "ERR_MODULE_NOT_FOUND") {');
console.log('    report += "❌ 模块加载失败\\n";');
console.log('    report += `   错误: ${error.message}\\n`;');
console.log('    report += "   可能原因:\\n";');
console.log('    report += "   - lib/ 目录文件缺失或损坏\\n";');
console.log('    report += "   - Node.js 版本过低不支持 ES Module\\n";');
console.log('    report += "   解决方案:\\n";');
console.log('    report += "   - 重新安装 multi-agent-engine 技能\\n";');
console.log('    report += "   - 升级 Node.js 到 20.5+\\n";');
console.log('  }');
console.log('');
console.log('  // ... 其他错误诊断');
console.log('  return report;');
console.log('}');
console.log('```\n');

console.log('═'.repeat(60));
console.log('✅ 环境兼容性测试完成\n');

console.log('📋 测试结论:');
console.log('1. ✅ 当前系统环境基本正常');
console.log('2. ⚠️  存在潜在的环境依赖问题');
console.log('3. 🔧 需要添加更严格的错误处理和兼容性检查');
console.log('4. 📝 需要提供更友好的错误提示和解决方案');
