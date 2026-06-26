---
name: 文件快速扫描 (Project Anatomy)
description: 文件快速扫描，减少token消耗。AI 不读文件就能知道内容，避免重复读取浪费 token。
triggers:
  - 扫描项目
  - 文件快扫
  - 项目透视
  - project anatomy
  - file index
  - reduce file reads
  - project map
---

# 文件快速扫描 (Project Anatomy)

受 OpenWolf 启发。扫描项目生成精简文件索引，让 AI 不打开文件就能判断是否需要读取，大幅减少 token 消耗。

## 命令

### 全量扫描
```bash
python3 <skill-dir>/scripts/anatomy_scan.py <项目路径> [选项]
```

选项：
- `--format compact|table|summary` — 输出格式（默认 compact 最省 token）
- `--incremental` / `-i` — 增量模式，未变文件复用缓存
- `--max-depth N` — 目录深度限制
- `--exclude pattern [...]` — 额外排除规则
- `--output path` — 自定义输出路径（默认 `<项目>/.anatomy.md`）

### 自动注入（会话启动用）
```bash
python3 <skill-dir>/scripts/anatomy_inject.py <项目路径> [--max-age-hours 24] [--quiet]
```
检查索引新鲜度，超过 24h 自动重新扫描，输出索引内容。

## 输出格式

**compact**（默认，最省 token）：
```
- `src/index.ts` (~180t) — 入口文件
- `src/server.ts` (~520t) — HTTP 服务
```

**summary**（按目录分组）：
```
## src/ (5 文件, ~2,400t)
- `index.ts` (~180t) — 入口文件
- `server.ts` (~520t) — HTTP 服务
```

**table**（最详细，含日期）：
```
| 文件 | Token | 描述 | 修改日 |
|------|-------|------|--------|
| `src/index.ts` | ~180 | 入口文件 | 2026-05-12 |
```

## 配置

项目根目录可选 `.anatomy.yaml`：
```yaml
exclude:           # 排除目录/文件
  - my_custom_dir
  - "*.generated.ts"
max_depth: 5        # 最大扫描深度
max_file_size_kb: 500    # 跳过超大文件
description_max_chars: 120  # 文件描述最大字符数
```

## Startup Integration (OpenClaw AGENTS.md)

已在 AGENTS.md Session Startup 中集成：

1. 启动时读 `.anatomy.md`（文件快扫索引），已知内容不再重复 `read`
2. 超过 24h 自动触发重新扫描：
   ```bash
   python3 skills/project-anatomy-0.1.0/scripts/anatomy_inject.py .
   ```
3. 扫描输出写入 `.anatomy.md`，后续会话直接复用

**效果**：AI 看索引就能判断是否需要打开文件，避免逐文件 `read` 浪费 token。

## How to Use

1. 首次扫描项目：`python3 .../anatomy_scan.py /path/to/project`
2. 读文件前先检查 `.anatomy.md` 索引
3. 只在单行描述不够时再 `read` 打开文件
4. 定期用 `--incremental` 增量更新

## Token Savings

实测数据：
- 47 文件目录：索引 ~1,058t vs 全量 ~29,533t → **节省 96%**
- 对同一个反复访问的项目效果最显著
