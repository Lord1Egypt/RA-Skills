---
name: openclaw-plugin-upgrade
description: OpenClaw 插件升级助手。当用户说「升级 qqbot 插件」「更新 openclaw-qqbot」「qqbot 更新」「帮我升级插件」「升级 openclaw 插件」等相关语句时激活。支持通用 openclaw 插件（任意 npm 包）升级，以及 QQ 机器人插件（@tencent-connect/openclaw-qqbot）的专项升级（含完整文件验证、兼容 3.23+ 配置校验绕过、自动回滚）。
---

# OpenClaw 插件升级

通过 `scripts/upgrade-plugin.sh` 在 agent 内直接完成插件升级，无需用户在终端手动操作。

## 核心脚本

`scripts/upgrade-plugin.sh` — 通用插件升级脚本。

```
用法: upgrade-plugin.sh <npm-pkg-name> <plugin-id> [选项]

必填：
  <npm-pkg-name>           npm 包名，如 @tencent-connect/openclaw-qqbot
  <plugin-id>              插件目录名，如 openclaw-qqbot

选项：
  --version <ver>          指定版本（跳过 update，走 reinstall）
  --no-restart             不重启 gateway（热更新场景）
  --verify-files <files>   逗号分隔的相对路径，验证这些文件存在
  --legacy-dirs <dirs>     逗号分隔的旧目录名，安装前清理
```

## 升级流程

1. **检测策略**：有安装记录 + 有目录 + 未指定版本 → `plugins update`；否则 → backup + `plugins install --pin`
2. **兼容 3.23+**：若配置含 plugin 的 channel key，自动创建临时配置副本绕过校验（不触发 gateway watcher）
3. **验证**：读取 `package.json` 版本号，并检查 `--verify-files` 指定的文件
4. **postinstall**：若存在 `scripts/postinstall-link-sdk.js` 自动执行
5. **重启**：执行 `gateway restart`（`--no-restart` 跳过）

## QQ 机器人插件（openclaw-qqbot）专项升级

**标准升级（升到 latest）：**
```bash
bash <skill_dir>/scripts/upgrade-plugin.sh \
  "@tencent-connect/openclaw-qqbot" \
  "openclaw-qqbot" \
  --verify-files "dist/index.js,dist/src/gateway.js,dist/src/api.js,dist/src/admin-resolver.js" \
  --legacy-dirs "qqbot,openclaw-qq"
```

**升级到指定版本：**
```bash
bash <skill_dir>/scripts/upgrade-plugin.sh \
  "@tencent-connect/openclaw-qqbot" \
  "openclaw-qqbot" \
  --version "1.2.3" \
  --verify-files "dist/index.js,dist/src/gateway.js,dist/src/api.js,dist/src/admin-resolver.js" \
  --legacy-dirs "qqbot,openclaw-qq"
```

**不重启（热更新）：**
加 `--no-restart`，然后单独调用 `gateway` tool 重启。

> `<skill_dir>` = 本 skill 文件所在目录，即 `SKILL.md` 的 dirname。
> 执行前需用 `exec` 运行脚本，并将输出展示给用户。

## 执行后处理

脚本输出包含结构化行，解析示例：
- `PLUGIN_NEW_VERSION=1.2.3` → 新版本号
- `PLUGIN_REPORT=✅ ...` → 结果摘要（直接转发给用户）

若脚本退出码非 0，告知用户升级失败并粘贴输出，建议检查网络和 npm registry。

## 通用插件示例（非 qqbot）

```bash
bash <skill_dir>/scripts/upgrade-plugin.sh \
  "my-org/my-openclaw-plugin" \
  "my-plugin-id"
```

无需 `--verify-files` 时脚本仍会验证 `package.json` 版本可读。
