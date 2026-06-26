# Host Checker

## Goal

给宿主一个轻量健康检查：

- 当前 reference profile 是什么
- 关键 target class 有没有落点
- 结构化 fallback 文件是否通过 schema 校验

它解决的是 `Validated` 这一步，而不是 `Installed` 或 `Integrated` 本身。

## Script

- `scripts/check-memory-host.py`

## Supported Profiles

当前支持两种入口：

- manifest-driven host
- reference profiles

manifest 优先。只有没有 manifest 时，才回退到 reference profile。

它做的是：

- 对 reference profiles 给出稳定检查
- 对 richer external adapters 做 presence check
- 对结构化 fallback 文件做 schema validation
- 对 manifest 中声明的 `fallback_paths` 做降级可用性检查

## Usage

### Auto detect

```sh
python3 scripts/check-memory-host.py /path/to/host-root
```

### Force profile

```sh
python3 scripts/check-memory-host.py /path/to/host-root --profile manifest
python3 scripts/check-memory-host.py /path/to/host-root --profile openclaw
python3 scripts/check-memory-host.py /path/to/host-root --profile generic
```

## Output

脚本会输出：

- `PROFILE`
- `STATUS`
- `CHECKS`

状态含义：

- `PASS` -> 没有错误，也没有告警
- `WARN` -> 没有错误，但有缺省项或可选项缺失
- `FAIL` -> 至少一个 required check 失败

推荐理解：

- 已安装 skill，但没跑 checker：最多只能说 `Installed` 或 `Integrated`
- checker `PASS` / 可接受 `WARN`：可以说 `Validated`

## What It Validates

### Manifest

- `memory-governor-host.toml`
- target-specific `mode`
- target-specific `paths`
- target-specific `fallback_paths`
- structured targets 的 schema validity
- `learning_candidates` 这类已标准化新 target 的 recognition
- 可选的 host entry / writer contract integration checks
- integration checks now require host entry acknowledgement and real Memory Contract markers, not just file existence
- split adapter 是否至少有一个 canonical slice

manifest 格式见：

- `adapter-manifest.md`

### OpenClaw

- `AGENTS.md`
- `memory/` directory
- `learning_candidates` 落点
- `reusable_lessons` 落点
- `proactive_state` 落点
- `working_buffer` 落点
- `TOOLS.md` presence as optional signal

### Generic

- `HOST.md`
- `memory/proactive-state.md`
- `memory/reusable-lessons.md`
- `memory/working-buffer.md`
- `skills/` directory as optional signal

## Limitations

- split external adapters are still validated lightly unless one slice is schema-valid
- manifest 允许宿主把 legacy external adapter 标成 `structured = false`
- `daily_memory` 这类 pattern target 目前只做声明检查，不扫全量 daily files
- this is a health check, not an automatic fixer
