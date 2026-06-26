# Bootstrap

## Goal

给第一次接入的人一个轻量起步方式。

它不是重安装器，不会试图自动改你的现有记忆数据层。

它只负责：

- 起一个 generic host 骨架
- 复制最小示例文件
- 帮你从“空白目录”进入“可理解、可修改”的状态

## Script

包内提供：

- `scripts/bootstrap-generic-host.sh`

## Usage

```sh
sh scripts/bootstrap-generic-host.sh /path/to/host-root
```

## What It Creates

脚本会在目标目录里补这些文件或目录。

如果文件已存在，会跳过，不覆盖。

- `HOST.md`
- `memory-governor-host.toml`
- `adapter-map.md`
- `memory/long-term.md`
- `memory/proactive-state.md`
- `memory/reusable-lessons.md`
- `memory/working-buffer.md`
- `docs/projects/README.md`
- `docs/tool-rules.md`
- `skills/example-writer/SKILL.md`
- `notes/daily/`
- `docs/`

## What It Does Not Do

它不会：

- 修改现有 `MEMORY.md`
- 迁移旧数据
- 自动重写你的其他 skill
- 自动判断你是否应该使用 OpenClaw profile
- 自动安装 optional adapters

## Recommended Flow

1. 运行 bootstrap 脚本
2. 打开 `HOST.md`
3. 修改 `memory-governor-host.toml`
4. 让 `adapter-map.md` 跟 manifest 保持一致
5. 删掉或替换 `skills/example-writer/`
6. 再按 `installation-integration.md` 接入你的真实宿主
7. Optional: run `scripts/check-memory-host.py` against the bootstrapped host root
8. Optional: run the validator against your structured fallback files

## Why It Is Kept Light

`memory-governor` 是治理内核，不是侵入式总线。

所以 bootstrap 也应该保持克制：

- 先给你可理解的骨架
- 不替你擅自改系统
- 把最终接线权保留给宿主
