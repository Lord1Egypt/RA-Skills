---
name: openrouter-model-picker
description: 从 OpenRouter 拉取所有 AI 模型，在交互式 Canvas UI 中让用户选择启用模型并一键热更新 OpenClaw 配置。当用户说"模型选择器"、"换模型"、"更新模型列表"、"选择 OpenRouter 模型"、"管理模型"、"模型管理"、"切换模型"、"换个模型"时使用。支持按厂商分组、按能力筛选（视觉/推理/免费）、搜索过滤、主模型选择，apply 后 3s 自动刷新页面，配置热更新无需重启 Gateway。
---

# OpenRouter Model Picker

交互式 Canvas 模型选择器：拉取 OpenRouter 全部模型 → UI 选择 → 一键 apply → 配置热更新。

## 架构

```
fetch_models.py ──→ picker.html (Canvas embed) ──→ config_server.py ──→ openclaw config patch
     ↑ 拉数据              ↑ 交互 UI                ↑ POST /apply          ↑ 热更新
```

- **fetch_models.py**: 从 OpenRouter API 拉取模型列表，归一化 ID，注入 picker.html
- **config_server.py**: 监听 `127.0.0.1:18790`，接受 POST /apply → `openclaw config patch --stdin`
  - apply 成功后立即退出
  - idle 超过 `--idle` 秒自动退出（默认 600s）；设 `--idle 0` 禁自动退出
- **picker.html**: 前端 UI，部署到 Canvas，内联模型 JSON + 时间戳

## 路径约定

所有路径相对于 skill 根目录。将 skill 目录路径存为变量：

```bash
SKILL_DIR="$(dirname $(find ${HOME}/.openclaw/workspace/skills -name SKILL.md -path '*/openrouter-model-picker/*' 2>/dev/null | head -1 | xargs dirname))"
# 如果上面找不到，直接用 workspace 相对路径：
# SKILL_DIR="${HOME}/.openclaw/workspace/skills/openrouter-model-picker"
OPENCLAW_CANVAS="${HOME}/.openclaw/canvas"
```

## 完整工作流程

每一步必须按顺序执行，不可跳过。

### 1. 检查 config_server 状态

```bash
curl -s --connect-timeout 2 http://127.0.0.1:18790/health 2>/dev/null && echo "RUNNING" || echo "DEAD"
```

如果 RUNNING，跳到步骤 3。如果 DEAD，执行步骤 2。

### 2. 拉取模型数据 + 启动 config_server

```bash
# 拉取数据（验证 API 可达）
python3 ${SKILL_DIR}/scripts/fetch_models.py > /dev/null || { echo "Failed to fetch models"; exit 1; }

# 后台启动 config_server
python3 ${SKILL_DIR}/scripts/config_server.py --port 18790 --idle 600 &
sleep 1
curl -s http://127.0.0.1:18790/health
```

### 3. 部署到 Canvas

```bash
DOC_ID="model-picker-$(date +%Y%m%d-%H%M%S)"
CANVAS_DIR="${OPENCLAW_CANVAS}/documents/${DOC_ID}"
mkdir -p "$CANVAS_DIR"
cp ${SKILL_DIR}/assets/picker.html "$CANVAS_DIR/index.html"

DATA=$(python3 ${SKILL_DIR}/scripts/fetch_models.py 2>/dev/null)

python3 -c "
import json, sys, os
data = sys.stdin.read()
ts = '${DOC_ID}'
html_path = '${CANVAS_DIR}/index.html'
with open(html_path) as f:
    html = f.read()
inject = '<script>var MY_PICKER_TS = \"' + ts + '\";\nwindow.__PICKER_DATA__ = ' + data + ';\ninitWithData(window.__PICKER_DATA__);\n</script>'
html = html.replace('</body>', inject + '</body>')
# 让旧的固定-ref picker 显示过期提示
stale_dir = '${OPENCLAW_CANVAS}/documents/model-picker'
if os.path.exists(stale_dir):
    with open(os.path.join(stale_dir, 'index.html'), 'w') as f:
        f.write('<html><body style=\"background:#0f0f10;color:#666;display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif\"><p>选择器已过期，请重新触发「选择模型」</p></body></html>')
with open(html_path, 'w') as f:
    f.write(html)
print('OK')
" <<< "$DATA"
```

### 4. 渲染 embed

```
[embed ref="<DOC_ID>" title="OpenRouter 模型选择器" height="600" /]
```

### 5. 用户操作完成后

用户点击「应用选择」→ 无需额外操作。config_server 自动执行 apply → 退出。

## Picker 前端行为

- **初始化时**：立即检查 server 健康（`GET /health`），每 10s 轮询。如果 server 不在 → 显示 ⏳ "选择器已超时" 遮罩
- **应用中**：POST /apply → 成功后显示 ✅ 遮罩 → 3s 后自动刷新父页面
- **刷新后**：页面重载 → server 已退出 → health check 失败 → 显示 ⏳ 超时遮罩
- **沙盒兼容**：localStorage 访问包在 try/catch 中，sandboxed iframe 下优雅降级

## 备用方案：命令行直接修改配置

不走 UI 时用：

```bash
python3 ${SKILL_DIR}/scripts/update_config.py \
  --primary "auto" \
  --enabled "auto,anthropic/claude-sonnet-4.6,deepseek/deepseek-v3.2" \
  --fallbacks "deepseek/deepseek-v3.2,free"
```

## 参考

- **config_server 完整参数和生命周期**：见 `references/config-server.md`
- **ID 归一化规范**：Picker 内部所有 ID 去掉 `openrouter/` 前缀，config_server 写回时自动加回
- **热更新范围**：`agents.*` 和 `models.*` 全部热更新，无需重启 Gateway
- **代理**：`fetch_models.py` 需要访问 `openrouter.ai`，走 `https_proxy` 环境变量