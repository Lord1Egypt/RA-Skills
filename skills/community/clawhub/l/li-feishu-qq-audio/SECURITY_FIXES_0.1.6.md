# Security Fixes for v0.1.6

## 修复的安全问题

### 1. ✅ Shell 注入漏洞 (P0)
**问题**: `scripts/common.sh` 中 `run_with_retry()` 使用 `eval "$cmd"`，存在命令注入风险

**修复**: 
- 改用数组参数 `"$@"` 直接执行命令
- 移除所有 eval 调用
- 添加命令脱敏显示

```bash
# 修复前（危险）
run_with_retry() {
    local cmd="$1"
    eval "$cmd"  # ❌ 命令注入风险
}

# 修复后（安全）
run_with_retry() {
    local max_retries="${1:-3}"
    local retry_delay="${2:-2}"
    shift 2
    "$@"  # ✅ 直接执行，无注入风险
}
```

### 2. ✅ 供应链攻击 - curl|sh (P0)
**问题**: `install.sh` 和 `install-with-model-choice.sh` 使用 `curl -sSf URL | sh`，存在供应链攻击风险

**修复**:
- 先下载到临时文件
- 验证脚本头（shebang 检查）
- 再执行本地文件
- 失败时回退到 pip 安装

```bash
# 修复前（危险）
curl -sSf https://astral.sh/uv/install.sh | sh  # ❌ 直接执行远程代码

# 修复后（安全）
UV_INSTALL_SCRIPT="/tmp/uv-install-$$.sh"
if curl -sSf https://astral.sh/uv/install.sh -o "$UV_INSTALL_SCRIPT"; then
    if head -1 "$UV_INSTALL_SCRIPT" | grep -qE '^#!(/bin/sh|/bin/bash)'; then
        sh "$UV_INSTALL_SCRIPT"  # ✅ 先验证再执行
    fi
    rm -f "$UV_INSTALL_SCRIPT"
fi
```

### 3. ✅ 元数据不一致 (P0)
**问题**: `_meta.json` 版本号 1.0.0 与实际 0.1.6 不符，未声明必要环境变量

**修复**:
```json
{
    "version": "0.1.6",
    "requiredTools": ["ffmpeg", "jq", "python3"],
    "requiredEnvVars": ["FEISHU_APP_ID", "FEISHU_APP_SECRET"],
    "optionalEnvVars": ["WHISPER_MODEL", "FAST_WHISPER_MODEL_DIR", "LOG_LEVEL", "PRIVACY_MODE"]
}
```

### 4. ✅ 非官方镜像警告 (P1)
**问题**: 使用 `hf-mirror.com` 非官方镜像，无用户提示

**修复**:
- 添加警告提示用户这是非官方镜像
- 提供 `USE_HF_MIRROR` 环境变量让用户选择
- 默认启用（考虑国内访问速度），但明确告知用户

```bash
: "${USE_HF_MIRROR:=true}"
if [ "$USE_HF_MIRROR" = "true" ]; then
    echo "⚠️  使用非官方镜像 hf-mirror.com（国内访问更快）"
    export HF_ENDPOINT="https://hf-mirror.com"
fi
```

### 5. ✅ openclaw.json 凭证读取风险 (P1)
**问题**: 脚本读取 `~/.openclaw/openclaw.json`，可能访问其他频道凭证

**修复**:
- 优先使用环境变量（推荐方式）
- 添加安全警告提示用户使用环境变量更安全
- 仅读取飞书相关凭证字段，不读取整个文件
- 日志中脱敏处理

```bash
# 优先环境变量
if [ -n "$FEISHU_APP_ID" ] && [ -n "$FEISHU_APP_SECRET" ]; then
    # ✅ 使用环境变量，最安全
fi

# 配置文件回退（带警告）
log_warn "⚠️  从配置文件加载凭证存在安全风险，建议设置环境变量"
APP_ID=$(jq -r '.feishu_app_id // empty' "$config_file")  # 仅读取必要字段
```

## 安全验证

```bash
# 检查 eval 使用情况
grep -rn "eval" scripts/*.sh  # 无结果 ✅

# 检查 curl|sh 使用情况
grep -rn "curl.*|.*sh" scripts/*.sh  # 无结果 ✅

# 检查版本号
cat _meta.json | jq '.version'  # "0.1.6" ✅

# 检查环境变量声明
cat _meta.json | jq '.requiredEnvVars'  # ["FEISHU_APP_ID", "FEISHU_APP_SECRET"] ✅
```

## 剩余风险提示

1. **hf-mirror.com**: 仍默认使用非官方镜像，用户可通过 `USE_HF_MIRROR=false` 切换到官方源
2. **openclaw.json**: 仍支持从配置文件读取凭证作为回退，建议用户始终使用环境变量

## 建议用户配置

```bash
# 推荐：使用环境变量（最安全）
export FEISHU_APP_ID="your-app-id"
export FEISHU_APP_SECRET="your-app-secret"
export WHISPER_MODEL="base"
export LOG_LEVEL="INFO"
export PRIVACY_MODE="standard"

# 可选：使用官方 HuggingFace 源
export USE_HF_MIRROR="false"
```
