#!/bin/bash
# openclaw-plugin-upgrade/scripts/upgrade-plugin.sh
#
# 通用 OpenClaw 插件升级脚本
#
# 功能：
#   - 自动检测 openclaw CLI (openclaw / clawdbot / moltbot)
#   - 已安装 → plugins update；未安装 / 指定版本 → rm + plugins install
#   - 安装后验证 package.json 中版本号可读
#   - 重启 gateway 使新版生效
#
# 用法：
#   upgrade-plugin.sh <npm-pkg-name> <plugin-id> [--version <ver>] [--no-restart] [--verify-files <file1,file2,...>]
#
# 参数：
#   <npm-pkg-name>           npm 包名，如 @tencent-connect/openclaw-qqbot
#   <plugin-id>              插件目录名，如 openclaw-qqbot
#   --version <ver>          指定版本（跳过 update，走 reinstall）
#   --no-restart             不重启 gateway（热更新场景）
#   --verify-files <files>   逗号分隔的文件相对路径，验证是否存在（可选）
#   --legacy-dirs <dirs>     逗号分隔的历史遗留目录名，安装前删除（可选）
#
# 退出码：
#   0 - 成功
#   1 - 失败（详见 stderr）

set -eo pipefail

PKG_NAME="${1:-}"
PLUGIN_ID="${2:-}"

if [ -z "$PKG_NAME" ] || [ -z "$PLUGIN_ID" ]; then
    echo "用法: $0 <npm-pkg-name> <plugin-id> [--version <ver>] [--no-restart] [--verify-files file1,file2] [--legacy-dirs dir1,dir2]"
    exit 1
fi

shift 2

TARGET_VERSION=""
NO_RESTART=false
VERIFY_FILES=""
LEGACY_DIRS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --version)
            [ -z "$2" ] && echo "❌ --version 需要参数" && exit 1
            TARGET_VERSION="${2#v}"
            shift 2
            ;;
        --no-restart)
            NO_RESTART=true
            shift
            ;;
        --verify-files)
            [ -z "$2" ] && echo "❌ --verify-files 需要参数" && exit 1
            VERIFY_FILES="$2"
            shift 2
            ;;
        --legacy-dirs)
            [ -z "$2" ] && echo "❌ --legacy-dirs 需要参数" && exit 1
            LEGACY_DIRS="$2"
            shift 2
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

INSTALL_SRC="${PKG_NAME}@${TARGET_VERSION:-latest}"

# 检测 CLI
CMD=""
for name in openclaw clawdbot moltbot; do
    command -v "$name" &>/dev/null && CMD="$name" && break
done
[ -z "$CMD" ] && echo "❌ 未找到 openclaw / clawdbot / moltbot CLI" && exit 1

OPENCLAW_VERSION="$($CMD --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || true)"

# 动态获取 global extensions 目录（兼容非标准数据目录，如 /projects/.openclaw）
EXTENSIONS_DIR="$($CMD plugins list 2>/dev/null | grep -oE 'global: [^ ]+' | head -1 | sed 's/global: //' || true)"
if [ -z "$EXTENSIONS_DIR" ]; then
    EXTENSIONS_DIR="$HOME/.$CMD/extensions"
fi

echo "==========================================="
echo "  插件升级: $INSTALL_SRC"
echo "  CLI: $CMD  版本: ${OPENCLAW_VERSION:-unknown}"
echo "==========================================="
echo ""

# 记录旧版本
OLD_PKG="$EXTENSIONS_DIR/$PLUGIN_ID/package.json"
OLD_VERSION=""
[ -f "$OLD_PKG" ] && OLD_VERSION="$(node -e "try{const v=JSON.parse(require('fs').readFileSync('$OLD_PKG','utf8')).version;if(v)process.stdout.write(String(v));}catch{}" 2>/dev/null || true)"
[ -n "$OLD_VERSION" ] && echo "  当前版本: $OLD_VERSION"

# [1/4] 安装/升级
echo ""
echo "[1/4] 安装/升级插件..."

# 动态定位配置文件（兼容非标准数据目录，如 /projects/.openclaw/openclaw.json）
DATA_DIR="$(dirname "$EXTENSIONS_DIR")"
CONFIG_FILE=""
for _name in "$CMD.json" "openclaw.json"; do
    _f="$DATA_DIR/$_name"
    if [ -f "$_f" ]; then CONFIG_FILE="$_f"; break; fi
done
[ -z "$CONFIG_FILE" ] && CONFIG_FILE="$HOME/.$CMD/$CMD.json"

# 兼容 openclaw 3.23+ 配置校验：创建不含本插件 channel 的临时配置
TEMP_CONFIG_FILE=""
PLUGIN_CHANNEL_KEY="${PLUGIN_ID/openclaw-/}"  # openclaw-qqbot → qqbot

if [ -f "$CONFIG_FILE" ]; then
    HAS_PLUGIN_CHANNEL="$(node -e "
      try {
        const cfg = JSON.parse(require('fs').readFileSync('$CONFIG_FILE','utf8'));
        if (cfg.channels && (cfg.channels['$PLUGIN_ID'] || cfg.channels['$PLUGIN_CHANNEL_KEY']))
          process.stdout.write('true');
      } catch {}
    " 2>/dev/null || true)"

    if [ "$HAS_PLUGIN_CHANNEL" = "true" ]; then
        TEMP_CONFIG_FILE="$(mktemp)"
        node -e "
          const fs=require('fs');
          const cfg=JSON.parse(fs.readFileSync('$CONFIG_FILE','utf8'));
          if(cfg.channels){delete cfg.channels['$PLUGIN_ID']; delete cfg.channels['$PLUGIN_CHANNEL_KEY'];}
          if(cfg.channels && Object.keys(cfg.channels).length===0) delete cfg.channels;
          fs.writeFileSync('$TEMP_CONFIG_FILE',JSON.stringify(cfg,null,4)+'\n');
        " 2>/dev/null && {
            export OPENCLAW_CONFIG_PATH="$TEMP_CONFIG_FILE"
            echo "  [兼容] 使用临时配置副本绕过 3.23+ 校验"
        } || { TEMP_CONFIG_FILE=""; }
    fi
fi

# 临时配置 install 记录同步 + 清理（幂等：执行后清空 TEMP_CONFIG_FILE 防止重入）
restore_temp_config() {
    if [ -n "$TEMP_CONFIG_FILE" ] && [ -f "$TEMP_CONFIG_FILE" ]; then
        local _tmp="$TEMP_CONFIG_FILE"
        TEMP_CONFIG_FILE=""          # 立即清空，防止 trap EXIT 重复执行
        unset OPENCLAW_CONFIG_PATH
        node -e "
          try {
            const fs=require('fs');
            const tmp=JSON.parse(fs.readFileSync('$_tmp','utf8'));
            const real=JSON.parse(fs.readFileSync('$CONFIG_FILE','utf8'));
            if(tmp.plugins&&tmp.plugins.installs){
              if(!real.plugins)real.plugins={};
              real.plugins.installs={...(real.plugins.installs||{}),...tmp.plugins.installs};
              fs.writeFileSync('$CONFIG_FILE',JSON.stringify(real,null,4)+'\n');
            }
          } catch {}
        " 2>/dev/null || true
        rm -f "$_tmp"
        echo "  [兼容] 已同步 install 记录并清理临时配置"
    fi
}
trap restore_temp_config EXIT

# 决策：有配置记录 + 有目录 + 未指定版本 → update，否则 → reinstall
HAS_INSTALL_RECORD="$(node -e "
  try {
    const cfg=JSON.parse(require('fs').readFileSync('$CONFIG_FILE','utf8'));
    const inst=cfg.plugins&&cfg.plugins.installs&&cfg.plugins.installs['$PLUGIN_ID'];
    if(inst) process.stdout.write('yes');
  } catch {}
" 2>/dev/null || true)"
HAS_PLUGIN_DIR=false
[ -d "$EXTENSIONS_DIR/$PLUGIN_ID" ] && [ -f "$EXTENSIONS_DIR/$PLUGIN_ID/package.json" ] && HAS_PLUGIN_DIR=true

UPGRADE_OK=false

if [ "$HAS_INSTALL_RECORD" = "yes" ] && [ "$HAS_PLUGIN_DIR" = "true" ] && [ -z "$TARGET_VERSION" ]; then
    echo "  [策略] 已安装 + 未指定版本 → plugins update"
    if $CMD plugins update "$PLUGIN_ID" 2>&1; then
        POST_VER="$(node -e "try{const v=JSON.parse(require('fs').readFileSync('$OLD_PKG','utf8')).version;if(v)process.stdout.write(String(v));}catch{}" 2>/dev/null || true)"
        if [ -z "$OLD_VERSION" ] || [ "$POST_VER" != "$OLD_VERSION" ]; then
            UPGRADE_OK=true
            echo "  ✅ update 成功${OLD_VERSION:+ ($OLD_VERSION → $POST_VER)}"
        else
            echo "  ⚠️  版本未变 ($POST_VER)，回退到 reinstall..."
        fi
    else
        echo "  ⚠️  update 失败，回退到 reinstall..."
    fi
fi

if [ "$UPGRADE_OK" != "true" ]; then
    echo "  [策略] 使用 reinstall: $INSTALL_SRC"

    # 备份旧目录
    BACKUP_DIR=""
    if [ -d "$EXTENSIONS_DIR/$PLUGIN_ID" ]; then
        BACKUP_DIR="$EXTENSIONS_DIR/.$PLUGIN_ID-backup-$$"
        mv "$EXTENSIONS_DIR/$PLUGIN_ID" "$BACKUP_DIR"
        echo "  已备份: $BACKUP_DIR"
    fi

    # 清理历史遗留目录
    if [ -n "$LEGACY_DIRS" ]; then
        IFS=',' read -ra LDIRS <<< "$LEGACY_DIRS"
        for d in "${LDIRS[@]}"; do
            [ -d "$EXTENSIONS_DIR/$d" ] && rm -rf "$EXTENSIONS_DIR/$d" && echo "  已清理历史目录: $d"
        done
    fi

    if $CMD plugins install "$INSTALL_SRC" --pin 2>&1; then
        UPGRADE_OK=true
        echo "  ✅ install 成功"
        [ -n "$BACKUP_DIR" ] && [ -d "$BACKUP_DIR" ] && rm -rf "$BACKUP_DIR" && echo "  已清理旧版备份"
    else
        echo "  ❌ install 失败"
        [ -n "$BACKUP_DIR" ] && [ -d "$BACKUP_DIR" ] && mv "$BACKUP_DIR" "$EXTENSIONS_DIR/$PLUGIN_ID" && echo "  ↩️  已回滚"
        restore_temp_config
        exit 1
    fi
fi

restore_temp_config

# [2/4] 验证安装
echo ""
echo "[2/4] 验证安装..."

TARGET_DIR="$EXTENSIONS_DIR/$PLUGIN_ID"
PKG_JSON="$TARGET_DIR/package.json"
NEW_VERSION=""
VERIFY_OK=true

if [ -f "$PKG_JSON" ]; then
    NEW_VERSION="$(node -e "process.stdout.write(JSON.parse(require('fs').readFileSync(process.argv[1],'utf8')).version||'')" "$PKG_JSON" 2>/dev/null || true)"
fi

if [ -z "$NEW_VERSION" ]; then
    echo "  ❌ 无法读取版本号"
    VERIFY_OK=false
else
    echo "  ✅ 版本号: $NEW_VERSION"
fi

# 验证自定义文件列表
if [ -n "$VERIFY_FILES" ]; then
    IFS=',' read -ra FILES <<< "$VERIFY_FILES"
    for f in "${FILES[@]}"; do
        if [ -f "$TARGET_DIR/$f" ]; then
            echo "  ✅ $f"
        else
            echo "  ❌ 缺少文件: $f"
            VERIFY_OK=false
        fi
    done
fi

# 执行 postinstall 脚本（如有）
POSTINSTALL="$TARGET_DIR/scripts/postinstall-link-sdk.js"
if [ -f "$POSTINSTALL" ]; then
    echo "  执行 postinstall-link-sdk..."
    node "$POSTINSTALL" 2>&1 && echo "  ✅ plugin-sdk 链接就绪" || echo "  ⚠️  postinstall 失败，插件可能无法加载"
fi

if [ "$VERIFY_OK" != "true" ]; then
    echo ""
    echo "❌ 验证未通过"
    exit 1
fi
echo "  ✅ 验证通过"

# [3/4] 输出结构化信息
echo ""
echo "[3/4] 升级结果..."
echo "PLUGIN_NEW_VERSION=${NEW_VERSION:-unknown}"
echo "PLUGIN_ID=$PLUGIN_ID"
if [ -n "$NEW_VERSION" ]; then
    echo "PLUGIN_REPORT=✅ $PLUGIN_ID 升级完成: v${NEW_VERSION}"
else
    echo "PLUGIN_REPORT=⚠️ 升级完成但无法确认新版本"
fi

echo ""
echo "==========================================="
echo "  ✅ 安装完成"
echo "==========================================="

# [4/4] 重启 gateway
if [ "$NO_RESTART" = "true" ]; then
    echo ""
    echo "[跳过重启] --no-restart 已指定"
    exit 0
fi

echo ""
echo "[4/4] 重启 gateway..."
if $CMD gateway restart 2>&1; then
    echo "  ✅ gateway 已重启"
    [ -n "$NEW_VERSION" ] && echo "" && echo "🎉 $PLUGIN_ID 已更新至 v${NEW_VERSION}"
else
    echo "  ⚠️  gateway 重启失败，请手动执行: $CMD gateway restart"
fi
