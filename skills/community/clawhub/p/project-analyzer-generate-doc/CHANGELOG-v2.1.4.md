# Changelog - v2.1.4 / v1.0.2 (2026-03-10)

## Security Fixes / 安全修复

---

### 🇬🇧 English

**project-analyzer-generate-doc v2.1.4** | **module-analyzer-generate-doc v1.0.2**

This release addresses all security concerns raised by the OpenClaw security scan. No functional changes to documentation generation capabilities.

**Security Improvements:**
- ❌ Removed all references to "bash" and alternative file-reading tools
- ❌ Removed all references to "elevated permissions" or privilege escalation
- ✅ Made file deletion operations explicitly require user confirmation (Step 0.6)
- ✅ Made document migration/merge operations explicitly require user confirmation (Step 0.5)
- ✅ Added explicit prohibitions against bypassing file access restrictions

**Files Modified:**
- `SKILL.md` - Updated Step 0.5/0.6 with user consent requirements
- `references/retry-mechanism.md` - Removed bash/elevated references
- `references/task-execution-guide.md` - Removed bash section, added safety constraints
- `SECURITY_FIXES.md` - New document detailing all security fixes

**Risk Rating:** Medium → Low ✅

---

### 🇨🇳 中文

**project-analyzer-generate-doc v2.1.4** | **module-analyzer-generate-doc v1.0.2**

本版本修复了 OpenClaw 安全扫描中发现的所有安全问题。文档生成功能无任何变化。

**安全改进：**
- ❌ 移除所有 "bash" 及替代文件读取工具的引用
- ❌ 移除所有 "elevated 权限" 或提权相关的引用
- ✅ 文件删除操作现在明确要求用户确认 (Step 0.6)
- ✅ 文档迁移/合并操作现在明确要求用户确认 (Step 0.5)
- ✅ 添加明确禁止绕过文件访问限制的说明

**修改文件：**
- `SKILL.md` - Step 0.5/0.6 添加用户确认要求
- `references/retry-mechanism.md` - 移除 bash/elevated 引用
- `references/task-execution-guide.md` - 移除 bash 章节，添加安全约束
- `SECURITY_FIXES.md` - 新增安全修复详细说明文档

**风险评级：** 中风险 → 低风险 ✅

---

## Breaking Changes / 重大变更

**None / 无** - All changes are security-related; functionality remains unchanged.

---

## Migration Guide / 迁移指南

**No action required / 无需操作** - Update the skill and continue using as before.

---

## Verification / 验证

```bash
# All problematic terms removed / 所有风险关键词已移除
Select-String -Path "skills/*analyzer-generate-doc/**/*.md" -Pattern "bash|elevated|自动删除"
# → (no output) ✅
```

---

*Released: 2026-03-10*
*Author: aclory*
