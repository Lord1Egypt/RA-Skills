# Deploy Notes

## 这份补丁的适用方式

这份 `thread-continuity.patch` 面向：
- 有 OpenClaw 源码树
- 能自己执行构建
- 能自己部署到 live 或测试环境

## 构建顺序

必须：

```bash
cd <OPENCLAW_SOURCE_ROOT>
python3 <PACK_ROOT>/scripts/apply_runtime_patch.py --source-root <OPENCLAW_SOURCE_ROOT> --apply --rebuild
```

不要漏掉 `pnpm ui:build`。

如果你只想先确认 patch 能否干净落到当前源码树：

```bash
python3 <PACK_ROOT>/scripts/apply_runtime_patch.py --source-root <OPENCLAW_SOURCE_ROOT>
```

## 为什么必须整套同步 dist

不要只替换单个 runtime bundle。  
原因：
- OpenClaw 的 runtime 产物带 hash
- UI 资源和 runtime 资源需要匹配
- 单文件热替换容易造成 hash / asset 失配

推荐做法：
- 用新构建的整套 `dist/` 替换 live `dist/`
- 同时确认 `dist/control-ui/index.html` 存在

## 部署前备份

至少备份：
- `<OPENCLAW_INSTALL_ROOT>/dist/`
- `<OPENCLAW_INSTALL_ROOT>/dist/control-ui/`
- `<OPENCLAW_CONFIG_PATH>`
- `<OPENCLAW_WORKSPACE>/AGENTS.md`
- `<OPENCLAW_WORKSPACE>/SESSION_CONTINUITY.md`
- `<OPENCLAW_WORKSPACE>/plans/`
- `<OPENCLAW_WORKSPACE>/status/`
- `<OPENCLAW_WORKSPACE>/handoff/`
- `<OPENCLAW_WORKSPACE>/memory/`
- `<OPENCLAW_WORKSPACE>/temp/`

## 部署后先做的 3 项验证

1. `openclaw config validate --json`
2. `systemctl is-active <SERVICE_NAME>`
3. 打开 `<LIVE_GATEWAY_URL>`，确认根页面和 Control UI 正常加载

然后再做 [verify.md](./verify.md) 里的 disposable thread continuity 验收。
