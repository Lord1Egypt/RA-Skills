---
name: local-file-organizer
description: |
  本地文件整理虾 — 自动分类、重命名并归档本地文件。

  当以下情况时使用此 Skill：
  (1) 需要自动整理本地目录（下载文件夹、桌面、项目归档等）
  (2) 需要按文件类型分类（文档/图片/视频/音频/压缩包/代码）
  (3) 需要检测并清理重复文件
  (4) 需要批量重命名文件，统一命名格式
  (5) 用户提到"整理文件"、"文件分类"、"自动归档"、"重命名文件"、"清理重复"、"文件管理"、"桌面整理"、"照片分类"、"文档归档"、"文件夹整理"
---

# 本地文件整理虾

核心脚本：`scripts/organize_files.py`

## 快速使用

```bash
# 预览整理效果（不实际移动）
python3 scripts/organize_files.py ~/Downloads --dry-run

# 执行整理（移动到同目录下的分类子文件夹）
python3 scripts/organize_files.py ~/Downloads

# 整理到指定目标目录
python3 scripts/organize_files.py ~/Downloads ~/Organized

# 整理 + 检测重复文件
python3 scripts/organize_files.py ~/Downloads --find-dups

# 使用自定义规则
python3 scripts/organize_files.py ~/Downloads --rules my-rules.json
```

## 工作流程

1. **理解需求** — 确认源目录、目标目录、整理模式（移动/复制/重命名）
2. **预览** — 先用 `--dry-run` 展示整理计划，让用户确认
3. **执行** — 用户确认后执行实际整理
4. **汇报** — 展示整理统计（移动了多少文件、发现多少重复）

## 分类规则

默认按扩展名分类到：Documents / Pictures / Videos / Audio / Archives / Code / Others

自定义规则 JSON 格式：
```json
{
  "设计稿": ["psd", "ai", "sketch", "fig"],
  "文档": ["pdf", "docx", "md"]
}
```

详细规则参考：`references/classification-rules.md`

## 重复文件检测

`--find-dups` 标志启用 MD5 哈希比对，输出重复文件列表。
用户确认后可手动删除，或使用 `trash` 命令移到回收站（推荐）。

保留策略详见：`references/duplicate-detection.md`

## 命名规范

批量重命名时参考：`references/naming-conventions.md`

支持变量：`{date}` `{name}` `{ext}` `{index}` `{parent}`

## 安全原则

- **默认不删除文件**，只移动/复制
- 删除操作前必须用户二次确认
- 优先使用 `trash` 而非 `rm`（可恢复）
- 文件名冲突时自动添加序号（`file_1.pdf`）

## 已知限制

- 无法处理正在被占用的文件
- 大文件（>10GB）哈希计算较慢，可先用 `--quick` 模式
- 不支持网络驱动器（NAS/SMB）的实时监控
