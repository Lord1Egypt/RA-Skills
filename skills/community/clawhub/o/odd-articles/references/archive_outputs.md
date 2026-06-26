# 存档工具

> 将环境变量 `OUTPUT_DIR` 目录下的历史文档文件（*.md, *.html, *.png, manifest.json）移动到环境变量 `ARCHIVE_DIR` 目录下，按月份和标题归档

---

## 环境变量

在 `local/.env` 中配置环境变量：`OUTPUT_DIR`, `ARCHIVE_DIR`

---

## 使用方式

### 基本用法

```bash
python3 "${SKILL_DIR}/scripts/archive_outputs.py"
```

### Windows 示例

```bash
# 使用默认配置
python "scripts/archive_outputs.py"

# 预览模式（不实际移动）
python "scripts/archive_outputs.py" --dry-run

# 指定目录
python "scripts/archive_outputs.py" --output-dir OUTPUT_DIR --archive-dir ARCHIVE_DIR
```

---

## 参数说明

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--output-dir` | `-o` | 否 | 指定输出目录（默认从环境变量 `OUTPUT_DIR` 读取） |
| `--archive-dir` | `-a` | 否 | 指定存档目录（默认从环境变量 `ARCHIVE_DIR` 读取） |
| `--dry-run` | `-n` | 否 | 预览模式，不实际移动文件 |

---

## 归档规则

1. **文件目录**：若 `output-dir` 未指定，则默认从环境变量`OUTPUT_DIR`读取。若上述目录不存在，结束存档，并提示未发现需要归档的文件
2. **归档目录**：若 `archive-dir` 未指定，则默认从环境变量`ARCHIVE_DIR`读取，若环境变量`ARCHIVE_DIR`未指定，则默认使用 `archives` 目录; 上述目录若不存在，则创建
3. **文件类型**：自动查找 `output-dir` 下的 `.md`、`.html`、`.png` 文件，以及 `manifest.json` 文件
4. **归档目录结构**：在 `archive-dir` 下创建以当前月份命名的子目录（格式：YYYY-MM，如 2026-03），并根据文章标题创建子目录
5. **文件移动**：将找到的文件移动到步骤2创建的子目录中
6. **冲突处理**：如果目标文件已存在，则跳过移动

### 归档目录结构示例

```
[存档目录]/
├── 2026-03                  # 2026年3月份的归档
│   ├── Fish-Audio-S2-Tutorial-v2/    # 文章标题目录
│   │   ├── Fish-Audio-S2-Tutorial-v2.md
│   │   ├── Fish-Audio-S2-Tutorial-v2_preview.html
│   │   ├── Fish-Audio-S2-Tutorial-v2_cover.html
│   │   └── manifest.json
│   └── OpenClaw-Memory-Deep-Article/  # 另一篇文章
│       ├── OpenClaw-Memory-Deep-Article.md
│       ├── OpenClaw-Memory-Deep-Article_preview.html
│       └── manifest.json
├── 2026-04                  # 2026年3月份的归档
│   └── ...
└── 2026-05    └── ...
```bash
python archive_outputs.py
```

**输出**：
```
[INFO] 输出目录: g:/AAA/odd-outputs
[INFO] 存档目录: g:/AAA/odd-archives
[INFO] 模式: 执行
--------------------------------------------------
[INFO] 创建归档目录: g:/AAA/odd-archives/2026-03
[OK] 已移动: Fish-Audio-S2-Tutorial-v2.md
[OK] 已移动: Fish-Audio-S2-Tutorial-v2_preview.html
[OK] 已移动: Fish-Audio-S2-Tutorial-v2_cover.html
[OK] 已移动: manifest.json

[OK] 归档完成！共移动 4 个文件到: g:/AAA/odd-archives/2026-03
```


### 示例 2：预览模式

```bash
python archive_outputs.py --dry-run
```

**输出**：
```
[INFO] 输出目录: g:/AAA/odd-outputs
[INFO] 存档目录: g:/AAA/odd-archives
[INFO] 模式: 预览（不实际移动）
--------------------------------------------------
[DRY RUN] 将创建目录: g:/AAA/odd-archives/2026-03
[DRY RUN] 将移动: g:/AAA/odd-outputs/Fish-Audio-S2-Tutorial-v2.md -> g:/AAA/odd-archives/2026-03/Fish-Audio-S2-Tutorial-v2.md
[DRY RUN] 将移动: g:/AAA/odd-outputs/Fish-Audio-S2-Tutorial-v2_preview.html -> g:/AAA/odd-archives/2026-03/Fish-Audio-S2-Tutorial-v2_preview.html
[DRY RUN] 将移动: g:/AAA/odd-outputs/Fish-Audio-S2-Tutorial-v2_cover.html -> g:/AAA/odd-archives/2026-03/Fish-Audio-S2-Tutorial-v2_cover.html
[DRY RUN] 将移动: g:/AAA/odd-outputs/manifest.json -> g:/AAA/odd-archives/2026-03/Fish-Audio-S2-Tutorial-v2_manifest.json

[DRY RUN] 总计将移动 4 个文件
```


### 示例 3：指定目录

```bash
python archive_outputs.py --output-dir /tmp/outputs --archive-dir /tmp/archives
```

---

## 常见问题

### "未指定输出目录"

**原因**：`OUTPUT_DIR` 环境变量未设置

**解决方案**：
1. 在 `local/.env` 中设置 `OUTPUT_DIR`
2. 或使用 `--output-dir` 参数指定

### "未指定存档目录"

**原因**：`ARCHIVE_DIR` 环境变量未设置

**解决方案**：
1. 在 `local/.env` 中设置 `ARCHIVE_DIR`
2. 或使用 `--archive-dir` 参数指定

### "没有找到需要归档的文件"

**原因**：`OUTPUT_DIR` 下没有 `.md`、`.html`、`.png`、`manifest.json` 文件

**解决方案**：
1. 检查 `OUTPUT_DIR` 路径是否正确
2. 确认目录下是否有需要归档的文件
3. 使用 `--dry-run` 预览模式查看会找到哪些文件

### "目标文件已存在，跳过"

**原因**：`ARCHIVE_DIR` 下已存在同名文件

**解决方案**：
1. 手动检查并删除或重命名已存在的文件
2. 或修改源文件名后再归档

---

## 相关文件

- 脚本位置：`scripts/archive_outputs.py`
- 配置文件：`local/.env`
- 环境变量：`OUTPUT_DIR`、`ARCHIVE_DIR`

---

## 触发词

在对话中使用以下触发词可调用存档功能：

| 触发词 | 说明 |
|-------|------|
| `/archive` | 将 `OUTPUT_DIR` 下的历史文档归档到 `ARCHIVE_DIR` |
| "存档" | 同上 |
| "归档" | 同上 |