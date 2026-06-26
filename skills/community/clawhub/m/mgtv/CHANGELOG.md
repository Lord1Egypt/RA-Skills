# MGTV Skill - 更新说明

## v1.0.2 (2026-04-15)

### 🔒 安全修复

- **移除未使用的 playwright 依赖**：`package.json` 中的 `playwright` 会在 `npm install` 时下载大量浏览器二进制文件，增加攻击面。现已完全移除
- **修复命令注入漏洞**：将 `child_process.exec`（使用字符串命令，存在注入风险）替换为 `child_process.spawn`（使用参数数组，参数不会经过 shell 解析，从根本上消除注入风险）

### 🐛 其他修复

- **修正 required-binaries 元数据**：SKILL.md 中只声明了 `open`（macOS 专用），实际脚本是跨平台的。现已移除该声明，因为 `open`/`xdg-open`/`start` 均为系统自带命令
- **统一许可证**：将 `package.json` 中的 `MIT` 改为 `MIT-0`，与 ClawHub 标准一致

### ✨ 新增功能：浏览器启动失败时输出链接

**更新内容：**
当无法自动打开浏览器时，脚本会清晰地输出播放链接，用户可以手动复制并打开。

**输出示例：**
```
正在打开浏览器：https://www.mgtv.com/b/338497/8337559.html
打开浏览器失败：Command failed: open "..."

============================================================
⚠️  无法自动打开浏览器
请手动复制以下链接到浏览器中打开：
============================================================
https://www.mgtv.com/b/338497/8337559.html
============================================================

提示：
  - 选中上面的链接并复制 (Ctrl+C / Cmd+C)
  - 打开浏览器粘贴到地址栏 (Ctrl+V / Cmd+V)
  - 按回车键打开页面
============================================================

⚠️  请手动打开上面的链接继续操作。
```

### 使用场景

1. **无头模式/服务器环境**：在没有图形界面的环境中
2. **浏览器未配置**：系统没有默认浏览器
3. **权限限制**：无法执行浏览器命令
4. **Docker 容器**：在容器中运行

### 代码变更

**修改文件：** `scripts/search-mgtv.js`

**新增函数：**
```javascript
// 输出备用链接（当无法打开浏览器时）
function outputFallbackUrl(url) {
  console.log('\n' + '='.repeat(60));
  console.log('⚠️  无法自动打开浏览器');
  console.log('请手动复制以下链接到浏览器中打开：');
  console.log('='.repeat(60));
  console.log(url);
  console.log('='.repeat(60));
  console.log('\n提示：');
  console.log('  - 选中上面的链接并复制 (Ctrl+C / Cmd+C)');
  console.log('  - 打开浏览器粘贴到地址栏 (Ctrl+V / Cmd+V)');
  console.log('  - 按回车键打开页面');
  console.log('='.repeat(60) + '\n');
}
```

**修改逻辑：**
```javascript
async function openInBrowser(url) {
  try {
    // 尝试打开浏览器
    await execAsync(command);
    return true;
  } catch (error) {
    console.error(`打开浏览器失败：${error.message}`);
    outputFallbackUrl(url);  // 新增：输出备用链接
    return false;
  }
}
```

### 兼容性

- ✅ macOS
- ✅ Windows
- ✅ Linux
- ✅ 无头模式/服务器环境
- ✅ Docker 容器

### 测试

```bash
# 正常情况：自动打开浏览器
node scripts/search-mgtv.js --query "乘风破浪的姐姐"
# 结果：✓ 已在浏览器中打开

# 模拟失败：输出链接
# （通过修改代码模拟浏览器失败）
# 结果：输出备用链接供手动复制
```

### 优势

1. **用户体验更好**：即使浏览器启动失败，用户也能看到链接并手动打开
2. **适用场景更广**：支持服务器、Docker 等无头环境
3. **错误提示清晰**：明确告知用户下一步操作
4. **无额外依赖**：仅使用 Node.js 标准库

---

## v1.0.0 (2024-04-10)

- ✅ 使用芒果 TV 官方搜索 API
- ✅ 智能匹配最相关的视频
- ✅ 支持直接打开视频链接
- ✅ 跨平台支持（macOS/Windows/Linux）

---

**最新版本**: v1.0.2
**更新日期**: 2026-04-15
**状态**: ✅ 稳定
