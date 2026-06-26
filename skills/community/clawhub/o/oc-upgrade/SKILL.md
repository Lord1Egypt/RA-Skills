---
name: openclaw-upgrade
description: OpenClaw 版本升级标准流程。适用于各类 OpenClaw 部署（WSL2/Linux VM）。自动探测代理、lossless-claw、systemd override 等可选组件，缺失组件自动跳过。每次说"升级openclaw"、"openclaw升级"、"更新openclaw"时必须执行此技能。
---

# OpenClaw 升级技能

每次升级 OpenClaw 都必须严格按此流程执行，不能省步骤。
- 上次（4.14版本）因为没检查 lossless-claw 兼容性踩过坑
- 上次升级后忘记发完成通知，爸比等了7小时不知道结果

两个教训都已写入流程。

---

## 第零步：环境探测

在任何操作之前，先自动探测并汇报当前环境：

```bash
# === 环境探测 ===
echo "=== OpenClaw 环境 ==="
echo "用户: $(whoami)"
echo "Home: $HOME"

# npm global 路径
NPM_PREFIX=$(npm prefix -g 2>/dev/null || echo "unknown")
echo "npm global: $NPM_PREFIX"

# 代理检测
if curl -s --connect-timeout 3 -x "http://127.0.0.1:7890" https://registry.npmjs.org/ > /dev/null 2>&1; then
  PROXY_OPT="--proxy http://127.0.0.1:7890"
  echo "代理: 127.0.0.1:7890 ✅"
elif curl -s --connect-timeout 3 https://registry.npmjs.org/ > /dev/null 2>&1; then
  PROXY_OPT=""
  echo "代理: 直连 ✅"
else
  echo "⚠️ npm 网络不通，请检查代理"
fi

# 可选组件检测
HAS_LOSSLESS=false
[ -d "$HOME/.openclaw/extensions/lossless-claw" ] && HAS_LOSSLESS=true
echo "lossless-claw: $HAS_LOSSLESS"

HAS_OVERRIDE=false
OVERRIDE="$HOME/.config/systemd/user/openclaw-gateway.service.d/override.conf"
[ -f "$OVERRIDE" ] && HAS_OVERRIDE=true
echo "override.conf: $HAS_OVERRIDE"

echo "服务管理: systemd --user"

# 多用户 /tmp/jiti 权限检查（防止 codex EACCES 问题）
if [ -d "/tmp/jiti" ]; then
  JITI_PERM=$(stat -c "%a" /tmp/jiti)
  if [ "$JITI_PERM" != "1777" ]; then
    echo "⚠️ /tmp/jiti 权限为 $JITI_PERM，多用户环境可能导致 codex EACCES 错误"
    echo "建议执行: sudo chmod 1777 /tmp/jiti"
  else
    echo "/tmp/jiti: 1777 ✅"
  fi
else
  echo "/tmp/jiti: 不存在 ✅"
fi
```

向爸比汇报环境探测结果，确认后继续。

---

## 第一步：确认目标版本

```bash
# 查当前版本和 npm 最新版
openclaw --version
npm view openclaw version

# 查目标版本 release notes
GITHUB_TOKEN=$(grep GITHUB_TOKEN ~/.openclaw/.env | cut -d= -f2)
TARGET_VER=<目标版本，如 2026.5.12>
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/openclaw/openclaw/releases/tags/v${TARGET_VER}" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('body','')[:3000])"
```

向爸比汇报：当前版本、目标版本、release highlights 摘要，等爸比确认目标版本。

---

## 第二步：检查插件兼容性

```bash
# 列出当前启用的插件
openclaw plugins list 2>/dev/null | grep "enabled"
```

针对**每个 enabled 插件**，在 release notes 里搜索对应关键词：

```bash
GITHUB_TOKEN=$(grep GITHUB_TOKEN ~/.openclaw/.env | cut -d= -f2)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/openclaw/openclaw/releases/tags/v${TARGET_VER}" | \
  python3 -c "
import json,sys
d=json.load(sys.stdin)
body = d.get('body','')
keywords = ['feishu', 'lossless', 'minimax', 'anthropic', 'deepseek', 'openai', 'memory-core']
for kw in keywords:
    lines = [l.strip() for l in body.split('\n') if kw.lower() in l.lower() and l.strip()]
    if lines:
        print(f'=== {kw} ===')
        for l in lines[:5]: print(' ', l)
"
```

重点关注：
- **lossless-claw**：手动装的 global 插件，历史上踩过坑，必须关注
- **@openclaw/feishu**：openclaw 自管 npm，升级可能改版本
- 其余 stock 插件随主包升级，通常无需额外处理

向爸比汇报兼容性评估，有⚠️风险说清楚。

---

## 第三步：记录插件快照

```bash
openclaw plugins list 2>/dev/null > /tmp/plugins-before-${TARGET_VER}.txt
echo "✅ 插件快照已保存 → /tmp/plugins-before-${TARGET_VER}.txt"
```

---

## 第四步：备份

```bash
CURRENT_VER=$(openclaw --version 2>/dev/null | grep -oP '[\d.]+' | head -1)
OVERRIDE="$HOME/.config/systemd/user/openclaw-gateway.service.d/override.conf"
FEISHU_DIR="$HOME/.openclaw/npm/node_modules/@openclaw/feishu"
LOSSLESS_DIR="$HOME/.openclaw/extensions/lossless-claw"

# 1. 主配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-${CURRENT_VER}
echo "1/5 openclaw.json ✅"

# 2. systemd override（含 Token + 代理）—— 可选，如存在才备份
if [ -f "$OVERRIDE" ]; then
  cp "$OVERRIDE" "${OVERRIDE}.bak-${CURRENT_VER}"
  echo "2/5 override.conf ✅"
else
  echo "2/5 override.conf 不存在，跳过 ✅"
fi

# 3. 环境变量（含 API Keys）
cp ~/.openclaw/.env ~/.openclaw/.env.bak-${CURRENT_VER}
echo "3/5 .env ✅"

# 4. lossless-claw —— 可选，如存在才备份；自适应大小
#    node_modules >500MB → 只备份 dist + package.json（避免 SIGKILL）
#    node_modules ≤500MB → 完整备份
if [ -d "$LOSSLESS_DIR" ]; then
  LOSSLESS_VER=$(cat "$LOSSLESS_DIR/package.json" | \
    python3 -c "import json,sys;print(json.load(sys.stdin)['version'])")
  LOSSLESS_NM_SIZE=$(du -sm "$LOSSLESS_DIR/node_modules/" 2>/dev/null | cut -f1)
  LOSSLESS_BAK="$HOME/.openclaw/extensions/lossless-claw.bak-${LOSSLESS_VER}"
  mkdir -p "$LOSSLESS_BAK"
  if [ "${LOSSLESS_NM_SIZE:-0}" -gt 500 ]; then
    cp "$LOSSLESS_DIR/package.json" "$LOSSLESS_BAK/"
    cp "$LOSSLESS_DIR/openclaw.plugin.json" "$LOSSLESS_BAK/"
    cp -r "$LOSSLESS_DIR/dist" "$LOSSLESS_BAK/"
    echo "4/5 lossless-claw (dist only, node_modules=${LOSSLESS_NM_SIZE}MB 过大跳过) ✅"
  else
    cp -r "$LOSSLESS_DIR/." "$LOSSLESS_BAK/"
    echo "4/5 lossless-claw (完整备份) ✅"
  fi
else
  echo "4/5 lossless-claw 不存在，跳过 ✅"
fi

# 5. feishu 插件（只备份 package.json 作版本存档，dist 随 openclaw 安装重建）
if [ -d "$FEISHU_DIR" ]; then
  mkdir -p "${FEISHU_DIR}.bak-${CURRENT_VER}"
  cp "$FEISHU_DIR/package.json" "${FEISHU_DIR}.bak-${CURRENT_VER}/"
  echo "5/5 feishu ✅"
else
  echo "5/5 feishu 插件目录不存在，跳过 ✅"
fi

echo ""
echo "=== 备份清单 ==="
ls ~/.openclaw/openclaw.json.bak-${CURRENT_VER} 2>/dev/null && echo "✅ openclaw.json"
ls ~/.openclaw/.env.bak-${CURRENT_VER} 2>/dev/null && echo "✅ .env"
[ -f "${OVERRIDE}.bak-${CURRENT_VER}" ] && echo "✅ override.conf" || echo "⏭ override.conf (不存在)"
ls -d "$HOME/.openclaw/extensions/lossless-claw.bak-"* 2>/dev/null | tail -1 | xargs -I{} echo "✅ {}" || echo "⏭ lossless-claw (不存在)"
ls -d "${FEISHU_DIR}.bak-${CURRENT_VER}" 2>/dev/null && echo "✅ feishu" || echo "⏭ feishu (不存在)"
```

确认核心备份（openclaw.json + .env）存在后再继续。

---

## 第五步：设好重启后通知 cron（先于重启执行）

gateway 重启会中断当前 session，重启后欢欢是全新上下文，不会记得升级完成这件事。
**必须在重启前设好一次性 systemEvent cron，重启后自动触发通知爸比。**

用 `cron` 工具创建：
- `schedule`: `at`，时间 = 当前时间 + 3 分钟（180 秒，实践中90秒有时 gateway 还未完全恢复）
- `payload.kind`: `systemEvent`
- `payload.text`: 升级完成通知（含版本号、插件状态、耗时）
- `sessionTarget`: `main`
- `deleteAfterRun`: `true`

示例通知文本：
```
🎉 OpenClaw 升级完成！v<旧版本> → v<新版本>，插件全部正常（lossless-claw ✅ feishu ✅），耗时约X分钟。
```

> ⚠️ **3分钟是经过实践的安全值**，90秒有时会在 gateway 恢复前触发导致通知失败。

cron 创建成功后，再执行下一步。

---

## 第六步：执行升级

**等爸比说「执行」才动手。**

```bash
# 自动检测代理并安装
if curl -s --connect-timeout 3 -x "http://127.0.0.1:7890" https://registry.npmjs.org/ > /dev/null 2>&1; then
  export HTTP_PROXY=http://127.0.0.1:7890
  export HTTPS_PROXY=http://127.0.0.1:7890
  echo "使用代理: 127.0.0.1:7890"
else
  echo "直连安装"
fi
npm install -g openclaw@${TARGET_VER}
```

---

## 第七步：验证

```bash
# 版本确认
openclaw --version   # 应为目标版本

# 自动修复配置问题（如外部化插件导致的 Invalid Config）
openclaw doctor --fix 2>&1 | tail -5

# 插件健康检查
openclaw doctor      # Errors = 0

# 检查是否有插件加载失败
FAILED=$(openclaw plugins list 2>/dev/null | grep -i "fail\|error" | grep -v "grep")
if [ -n "$FAILED" ]; then
  echo "⚠️ 检测到插件加载失败："
  echo "$FAILED"
  echo "尝试自动修复..."
  
  # feishu 失败 → 强制重装（feishu是最关键通道）
  if echo "$FAILED" | grep -qi "feishu"; then
    echo "🔧 feishu 插件失败，强制重装..."
    openclaw plugins install --force @openclaw/feishu 2>&1
    echo "⚠️ 重装后需要重启 gateway"
  fi
else
  echo "✅ 所有插件加载正常"
fi

# 插件对比
diff /tmp/plugins-before-${TARGET_VER}.txt <(openclaw plugins list 2>/dev/null)
```

验收标准（全部通过才继续）：
- ✅ 版本 = 目标版本
- ✅ lossless-claw（若存在）仍在 enabled 列表
- ✅ feishu（若存在）仍在 enabled 列表
- ✅ doctor Errors = 0
- ✅ 无插件加载失败（`FAILED` 为空）

有任何一项不通过 → 立即执行回滚，不继续。

---

## 第八步：重启 gateway

```bash
systemctl --user restart openclaw-gateway.service
```

第五步设好的 cron 会在重启后 90 秒内自动触发，通知爸比升级完成。

---

## ⏪ 回滚方案

任一步骤出问题立即执行：

```bash
PREV_VER=<回退版本，如 2026.5.6>
OVERRIDE="$HOME/.config/systemd/user/openclaw-gateway.service.d/override.conf"
FEISHU_DIR="$HOME/.openclaw/npm/node_modules/@openclaw/feishu"
LOSSLESS_BAK=$(ls -d "$HOME/.openclaw/extensions/lossless-claw.bak-"* 2>/dev/null | sort | tail -1)

# 1. 回退 openclaw（自动检测代理）
if curl -s --connect-timeout 3 -x "http://127.0.0.1:7890" https://registry.npmjs.org/ > /dev/null 2>&1; then
  export HTTP_PROXY=http://127.0.0.1:7890
  export HTTPS_PROXY=http://127.0.0.1:7890
fi
npm install -g openclaw@${PREV_VER}

# 2. 还原配置
cp ~/.openclaw/openclaw.json.bak-${PREV_VER} ~/.openclaw/openclaw.json
cp ~/.openclaw/.env.bak-${PREV_VER} ~/.openclaw/.env

# 3. 还原 override.conf（可选，如备份存在才还原）
if [ -f "${OVERRIDE}.bak-${PREV_VER}" ]; then
  cp "${OVERRIDE}.bak-${PREV_VER}" "$OVERRIDE"
  echo "override.conf 已还原 ✅"
else
  echo "override.conf 备份不存在，跳过 ✅"
fi

# 4. 还原 lossless-claw（可选，如备份存在才还原）
if [ -n "$LOSSLESS_BAK" ] && [ -d "$LOSSLESS_BAK" ]; then
  rm -rf "$HOME/.openclaw/extensions/lossless-claw"
  cp -r "$LOSSLESS_BAK" "$HOME/.openclaw/extensions/lossless-claw"
  echo "lossless-claw 已还原 ✅"
else
  echo "lossless-claw 备份不存在，跳过 ✅"
fi

# 5. 还原 feishu（package.json 存档，dist 由 openclaw 重建，通常无需手动还原）

# 6. 重启
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

等飞书收到「欢欢重启完毕，在线了 🐾」，告知爸比回滚完成及原因。

---

## 注意事项

- **不要用 `gateway update.run` 升级**，npm 手动指定版本更可控
- **feishu 插件路径**：`~/.openclaw/npm/node_modules/@openclaw/feishu`（openclaw 自管，非 npm global）
- **lossless-claw 路径**：`~/.openclaw/extensions/lossless-claw`（openclaw 自管）
- **systemd service 不读 .bashrc**，代理若需在 service 中生效，需配置 override.conf 或 EnvironmentFile
- **lossless-claw 踩坑**：2026-04-14 升级 4.14 不兼容，回退 4.11 解决，每次升级必须检查
- **MiniMax 不调用 message 工具**，涉及发消息的 cron 不要用 MiniMax
- **brave 插件外部化（2026.5.12 起）**：升级后如果遇到 "web_search provider is not available: brave"，执行 `openclaw plugins install --force @openclaw/brave-plugin` 后重启
- **feishu 插件不兼容**：升级后 feishu 注册失败时，执行 `openclaw plugins install --force @openclaw/feishu` 后重启
- **codex EACCES 错误**：多用户同机时，`/tmp/jiti/` 目录需要 sticky bit（`sudo chmod 1777 /tmp/jiti`），否则不同用户的 codex 会互相冲突
- **升级完成通知 cron**：设置 3 分钟而非更短，防止 gateway 还未完全恢复时触发

---

## 开源版说明

- 技能适配 OpenClaw 所有标准部署（WSL2/Linux VM/原生 Linux）
- 如果使用代理，自动检测 127.0.0.1:7890，也可在执行前手动 `export HTTP_PROXY=http://your-proxy:port`
- lossless-claw / override.conf 均为可选组件，不存在时自动跳过，不会报错中断
- 服务管理默认 `systemd --user`，如使用其他方式（如 pm2、docker）请修改第八步的重启命令
- 首次使用前建议先执行第零步（环境探测），确认环境配置正确
