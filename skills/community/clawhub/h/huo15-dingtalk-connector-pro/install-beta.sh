#!/bin/bash
set -e

# 清理函数：确保临时文件被清理
TEMP_FILES=()
cleanup() {
    for file in "${TEMP_FILES[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
        fi
    done
}
trap cleanup EXIT

# ============ 参数解析 ============
BRANCH="${1:-feat/migrate-to-openclaw-sdk}"  # 默认分支
VERSION=""  # 将从 package.json 动态获取

# 显示使用说明
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "使用方法: $0 [分支名]"
    echo ""
    echo "参数:"
    echo "  分支名    要安装的 Git 分支 (默认: feat/migrate-to-openclaw-sdk)"
    echo ""
    echo "示例:"
    echo "  $0                           # 安装默认分支"
    echo "  $0 main                      # 安装 main 分支"
    echo "  $0 feat/new-feature          # 安装指定功能分支"
    exit 0
fi

echo "🚀 开始安装钉钉连接器..."
echo "📌 分支: $BRANCH"

# 检查 OpenClaw 是否已安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ 错误：未检测到 OpenClaw，请先安装 OpenClaw"
    exit 1
fi

# 检查 jq 是否已安装（用于 JSON 处理）
if ! command -v jq &> /dev/null; then
    echo "⚠️  警告：未检测到 jq 工具，将跳过自动配置迁移"
    echo "💡 提示：安装 jq 可以自动迁移配置 (brew install jq 或 apt-get install jq)"
    HAS_JQ=false
else
    HAS_JQ=true
fi

CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# 检查并处理旧备份
echo "🔍 检查旧备份..."
BACKUP_DIR="$HOME/.openclaw"
OLD_BACKUPS=$(ls -t "$BACKUP_DIR"/openclaw.json.backup.* 2>/dev/null || true)

if [ -n "$OLD_BACKUPS" ]; then
    BACKUP_COUNT=$(echo "$OLD_BACKUPS" | wc -l | tr -d ' ')
    echo "📋 发现 $BACKUP_COUNT 个旧备份"
    
    # 找到最新的备份（用户当前正在使用的配置）
    LATEST_BACKUP=$(echo "$OLD_BACKUPS" | head -1)
    echo "📌 将从最新备份中提取配置：$(basename "$LATEST_BACKUP")"
    
    # 先复制最新的备份到临时位置（避免被删除）
    TEMP_SOURCE=$(mktemp)
    TEMP_FILES+=("$TEMP_SOURCE")
    if ! cp "$LATEST_BACKUP" "$TEMP_SOURCE"; then
        echo "❌ 错误：无法复制备份文件"
        exit 1
    fi
    SOURCE_CONFIG="$TEMP_SOURCE"
    
    # 保留最新的备份用于回滚，只删除旧的备份
    echo "🗑️  清理旧备份（保留最新备份用于回滚）..."
    FIRST=true
    while read -r backup; do
        if [ "$FIRST" = true ]; then
            FIRST=false
            echo "   - 保留：$(basename "$backup")"
        else
            rm -f "$backup"
            echo "   - 已删除：$(basename "$backup")"
        fi
    done <<< "$OLD_BACKUPS"
else
    echo "ℹ️  未发现旧备份，将使用当前配置"
    SOURCE_CONFIG="$CONFIG_FILE"
fi

# 创建新备份
echo "📦 创建新备份..."
BACKUP_FILE="$HOME/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)"

if [ -f "$CONFIG_FILE" ]; then
    if ! cp "$CONFIG_FILE" "$BACKUP_FILE"; then
        echo "❌ 错误：备份配置文件失败"
        exit 1
    fi
    echo "✅ 配置已备份到: $BACKUP_FILE"
    
    # 自动迁移配置（如果有 jq）
    if [ "$HAS_JQ" = true ]; then
        # 先检查当前配置中是否已有 dingtalk-connector 配置
        EXISTING_CONNECTOR_ID=$(jq -r '.channels."dingtalk-connector".clientId // empty' "$CONFIG_FILE")
        EXISTING_CONNECTOR_SECRET=$(jq -r '.channels."dingtalk-connector".clientSecret // empty' "$CONFIG_FILE")
        EXISTING_CONNECTOR_ACCOUNTS=$(jq -r '.channels."dingtalk-connector".accounts // empty' "$CONFIG_FILE")
        
        # 如果已经有 dingtalk-connector 配置，跳过迁移
        if [ -n "$EXISTING_CONNECTOR_ID" ] || [ -n "$EXISTING_CONNECTOR_SECRET" ] || { [ "$EXISTING_CONNECTOR_ACCOUNTS" != "null" ] && [ -n "$EXISTING_CONNECTOR_ACCOUNTS" ]; }; then
            echo "✅ 检测到已有 dingtalk-connector 配置，跳过迁移"
            echo "   - 配置文件保持不变"
        else
            echo "🔄 从原始配置中提取并迁移..."
            
            # 从源配置中提取旧的 dingtalk 配置
            OLD_CLIENT_ID=$(jq -r '.channels.dingtalk.clientId // empty' "$SOURCE_CONFIG")
            
            # 检查 clientSecret 的类型（字符串或对象）
            SECRET_TYPE=$(jq -r '.channels.dingtalk.clientSecret | type' "$SOURCE_CONFIG")
            
            if [ "$SECRET_TYPE" = "string" ]; then
                # 如果是字符串，直接提取
                OLD_CLIENT_SECRET=$(jq -r '.channels.dingtalk.clientSecret // empty' "$SOURCE_CONFIG")
            elif [ "$SECRET_TYPE" = "object" ]; then
                # 如果是对象（SecretInput 引用），保持原样
                OLD_CLIENT_SECRET=$(jq -c '.channels.dingtalk.clientSecret' "$SOURCE_CONFIG")
            else
                OLD_CLIENT_SECRET=""
            fi
            
            # 如果原始配置中有旧配置，则迁移
            if [ -n "$OLD_CLIENT_ID" ] && [ -n "$OLD_CLIENT_SECRET" ]; then
            echo "📋 正在迁移配置到 dingtalk-connector..."
            
            # 创建临时文件
            TEMP_FILE=$(mktemp)
            TEMP_FILES+=("$TEMP_FILE")
            
            # 迁移配置（根据 clientSecret 类型选择不同的处理方式）
            if [ "$SECRET_TYPE" = "string" ]; then
                # 字符串类型：使用 --arg 传递
                if ! jq --arg clientId "$OLD_CLIENT_ID" \
                       --arg clientSecret "$OLD_CLIENT_SECRET" \
                       '.channels."dingtalk-connector" = (.channels."dingtalk-connector" // {}) | 
                        .channels."dingtalk-connector".enabled = true |
                        .channels."dingtalk-connector".clientId = $clientId |
                        .channels."dingtalk-connector".clientSecret = $clientSecret |
                        .channels.dingtalk.enabled = false' \
                       "$CONFIG_FILE" > "$TEMP_FILE"; then
                    echo "❌ 错误：配置迁移失败"
                    rm -f "$TEMP_FILE"
                    exit 1
                fi
            elif [ "$SECRET_TYPE" = "object" ]; then
                # 对象类型：使用 --argjson 传递 JSON 对象
                if ! jq --arg clientId "$OLD_CLIENT_ID" \
                       --argjson clientSecret "$OLD_CLIENT_SECRET" \
                       '.channels."dingtalk-connector" = (.channels."dingtalk-connector" // {}) | 
                        .channels."dingtalk-connector".enabled = true |
                        .channels."dingtalk-connector".clientId = $clientId |
                        .channels."dingtalk-connector".clientSecret = $clientSecret |
                        .channels.dingtalk.enabled = false' \
                       "$CONFIG_FILE" > "$TEMP_FILE"; then
                    echo "❌ 错误：配置迁移失败"
                    rm -f "$TEMP_FILE"
                    exit 1
                fi
            fi
            
            # 替换原配置文件
            if ! mv "$TEMP_FILE" "$CONFIG_FILE"; then
                echo "❌ 错误：无法更新配置文件"
                exit 1
            fi
            
                echo "✅ 配置迁移完成："
                echo "   - clientId: ${OLD_CLIENT_ID:0:12}..."
                echo "   - clientSecret: [已迁移]"
                echo "   - 旧 dingtalk 插件已禁用"
            else
                echo "ℹ️  未发现旧的 dingtalk 配置"
                echo ""
                echo "📝 检测到您是首次配置钉钉连接器，安装完成后请运行以下命令进行配置："
                echo "   openclaw wizard"
                echo ""
                echo "或者手动编辑配置文件："
                echo "   vim ~/.openclaw/openclaw.json"
                echo ""
                echo "配置示例："
                echo '   {'
                echo '     "channels": {'
                echo '       "dingtalk-connector": {'
                echo '         "enabled": true,'
                echo '         "clientId": "your-client-id",'
                echo '         "clientSecret": "your-client-secret"'
                echo '       }'
                echo '     }'
                echo '   }'
            fi
        fi
    fi
else
    echo "⚠️  配置文件不存在，将在安装后创建"
    echo ""
    echo "📝 安装完成后请运行以下命令进行配置："
    echo "   openclaw wizard"
    echo ""
    echo "或者手动编辑配置文件："
    echo "   vim ~/.openclaw/openclaw.json"
fi

# 克隆升级分支
echo "📥 克隆分支: $BRANCH..."
cd /tmp
rm -rf dingtalk-openclaw-connector-beta

if ! git clone --single-branch --branch "$BRANCH" \
    https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector.git \
    dingtalk-openclaw-connector-beta; then
    echo "❌ 错误：克隆分支 '$BRANCH' 失败"
    echo "💡 提示：请检查分支名是否正确"
    exit 1
fi

cd dingtalk-openclaw-connector-beta

# 从 package.json 获取版本号
if command -v jq &> /dev/null; then
    VERSION=$(jq -r '.version' package.json 2>/dev/null || echo "unknown")
else
    # 如果没有 jq，使用 grep 和 sed 提取版本号
    VERSION=$(grep '"version"' package.json | sed 's/.*"version": "\(.*\)".*/\1/' || echo "unknown")
fi

echo "📦 版本: $VERSION"
echo ""

npm install

# 卸载旧版本
echo "🗑️  卸载旧版本..."

# 检查插件是否已安装
INSTALLED_PLUGINS=$(openclaw plugins list 2>/dev/null || echo "")
if echo "$INSTALLED_PLUGINS" | grep -q "dingtalk-connector"; then
    echo "📦 检测到已安装的 dingtalk-connector，正在卸载..."
    # 使用 -f 强制卸载，避免交互式确认
    # 捕获卸载错误，即使失败也继续执行（可能是插件文件已被手动删除）
    UNINSTALL_FAILED=false
    if command -v yes &> /dev/null; then
        yes | openclaw plugins uninstall dingtalk-connector 2>&1 || {
            echo "⚠️  卸载过程出现错误（可能插件文件已被手动删除）"
            UNINSTALL_FAILED=true
        }
    else
        echo "y" | openclaw plugins uninstall dingtalk-connector 2>&1 || {
            echo "⚠️  卸载过程出现错误（可能插件文件已被手动删除）"
            UNINSTALL_FAILED=true
        }
    fi
    
    # 如果卸载失败，手动清理配置文件中的残留配置
    if [ "$UNINSTALL_FAILED" = true ] && [ "$HAS_JQ" = true ]; then
        echo "🧹 清理配置文件中的残留配置..."
        if [ -f "$CONFIG_FILE" ]; then
            # 先保存 dingtalk-connector 配置，用于后续恢复
            SAVED_CONNECTOR_CONFIG=$(mktemp)
            TEMP_FILES+=("$SAVED_CONNECTOR_CONFIG")
            jq '.channels."dingtalk-connector" // {}' "$CONFIG_FILE" > "$SAVED_CONNECTOR_CONFIG"
            
            TEMP_CLEANUP=$(mktemp)
            TEMP_FILES+=("$TEMP_CLEANUP")
            
            # 删除 channels.dingtalk-connector 和 plugins 相关配置
            if jq 'del(.channels."dingtalk-connector") | 
                  del(.plugins.entries."dingtalk-connector") |
                  .plugins.allow = (.plugins.allow // [] | map(select(. != "dingtalk-connector"))) |
                  .plugins.load.paths = (.plugins.load.paths // [] | map(select(. | contains("dingtalk-openclaw-connector") | not)))' \
                  "$CONFIG_FILE" > "$TEMP_CLEANUP"; then
                mv "$TEMP_CLEANUP" "$CONFIG_FILE"
                echo "✅ 配置文件已清理（channels + plugins + load paths）"
                echo "💾 已保存 dingtalk-connector 配置，将在安装后恢复"
            else
                echo "⚠️  无法清理配置文件，请手动检查"
                rm -f "$TEMP_CLEANUP"
            fi
        fi
    fi
    
    echo "✅ 旧版本处理完成"
else
    echo "ℹ️  未检测到已安装的 dingtalk-connector，跳过卸载"
fi

# 安装新版本
echo "✨ 安装新版本..."
openclaw plugins install -l .

# 如果之前保存了配置，现在恢复
if [ "$UNINSTALL_FAILED" = true ] && [ "$HAS_JQ" = true ] && [ -f "$SAVED_CONNECTOR_CONFIG" ]; then
    echo "🔄 恢复 dingtalk-connector 配置..."
    
    # 检查保存的配置是否为空对象
    SAVED_CONFIG_CONTENT=$(cat "$SAVED_CONNECTOR_CONFIG")
    if [ "$SAVED_CONFIG_CONTENT" != "{}" ] && [ "$SAVED_CONFIG_CONTENT" != "null" ]; then
        TEMP_RESTORE=$(mktemp)
        TEMP_FILES+=("$TEMP_RESTORE")
        
        # 将保存的配置合并回去
        if jq --slurpfile saved "$SAVED_CONNECTOR_CONFIG" \
              '.channels."dingtalk-connector" = $saved[0]' \
              "$CONFIG_FILE" > "$TEMP_RESTORE"; then
            mv "$TEMP_RESTORE" "$CONFIG_FILE"
            echo "✅ 配置已恢复"
            
            # 显示恢复的配置信息
            RESTORED_CLIENT_ID=$(jq -r '.channels."dingtalk-connector".clientId // empty' "$CONFIG_FILE")
            if [ -n "$RESTORED_CLIENT_ID" ]; then
                echo "   - clientId: ${RESTORED_CLIENT_ID:0:12}..."
                echo "   - clientSecret: [已恢复]"
            fi
        else
            echo "⚠️  配置恢复失败，请手动检查"
            rm -f "$TEMP_RESTORE"
        fi
    else
        echo "ℹ️  未发现需要恢复的配置"
    fi
fi

# 重启 Gateway
echo "🔄 重启 Gateway..."
if ! openclaw gateway restart; then
    echo "⚠️  警告：Gateway 重启失败，请手动重启"
    echo "   命令：openclaw gateway restart"
fi

echo ""
echo "============================================"
echo "✅ 安装完成！"
echo "============================================"
echo ""

# ============ 验证结果 ============
echo "🔍 验证安装结果..."
echo ""

# 1. 检查插件是否已安装
PLUGIN_INSTALLED=false
if openclaw plugins list 2>/dev/null | grep -q "dingtalk-connector"; then
    PLUGIN_INSTALLED=true
    echo "✅ 插件已安装"
else
    echo "❌ 插件未安装"
fi

# 2. 检查配置文件
CONFIG_VALID=false
if [ -f "$CONFIG_FILE" ]; then
    if [ "$HAS_JQ" = true ]; then
        CONNECTOR_ENABLED=$(jq -r '.channels."dingtalk-connector".enabled // false' "$CONFIG_FILE")
        CONNECTOR_CLIENT_ID=$(jq -r '.channels."dingtalk-connector".clientId // empty' "$CONFIG_FILE")
        
        if [ "$CONNECTOR_ENABLED" = "true" ] && [ -n "$CONNECTOR_CLIENT_ID" ]; then
            CONFIG_VALID=true
            echo "✅ 配置文件有效"
            echo "   - 插件已启用"
            echo "   - clientId: ${CONNECTOR_CLIENT_ID:0:12}..."
        else
            echo "⚠️  配置文件需要完善"
            if [ "$CONNECTOR_ENABLED" != "true" ]; then
                echo "   - 插件未启用"
            fi
            if [ -z "$CONNECTOR_CLIENT_ID" ]; then
                echo "   - 缺少 clientId"
            fi
        fi
    else
        echo "⚠️  无法验证配置（需要 jq 工具）"
    fi
else
    echo "❌ 配置文件不存在"
fi

# 3. 检查 Gateway 状态
GATEWAY_RUNNING=false
if openclaw gateway status 2>/dev/null | grep -q "running"; then
    GATEWAY_RUNNING=true
    echo "✅ Gateway 运行中"
else
    echo "⚠️  Gateway 未运行"
fi

echo ""
echo "============================================"
echo "📊 安装总结"
echo "============================================"
echo "版本: $VERSION"
echo "分支: $BRANCH"
echo "插件安装: $([ "$PLUGIN_INSTALLED" = true ] && echo "✅" || echo "❌")"
echo "配置有效: $([ "$CONFIG_VALID" = true ] && echo "✅" || echo "⚠️")"
echo "Gateway: $([ "$GATEWAY_RUNNING" = true ] && echo "✅" || echo "⚠️")"
echo "============================================"
echo ""

# 根据验证结果给出建议
if [ "$PLUGIN_INSTALLED" = true ] && [ "$CONFIG_VALID" = true ] && [ "$GATEWAY_RUNNING" = true ]; then
    echo "🎉 一切就绪！钉钉连接器已成功安装并配置完成"
else
    echo "⚠️  需要进一步操作："
    
    if [ "$PLUGIN_INSTALLED" = false ]; then
        echo "   1. 插件未安装，请检查安装日志"
    fi
    
    if [ "$CONFIG_VALID" = false ]; then
        echo "   2. 配置未完成，请运行："
        echo "      openclaw wizard"
        echo "      或手动编辑：vim ~/.openclaw/openclaw.json"
    fi
    
    if [ "$GATEWAY_RUNNING" = false ]; then
        echo "   3. Gateway 未运行，请运行："
        echo "      openclaw gateway restart"
    fi
fi

echo ""
echo "📖 更多信息："
echo "   - 新功能说明：README_UPGRADE.md"
echo "   - 问题反馈：https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues"
echo ""
echo "💡 如需回滚："
echo "   1. 恢复配置：cp $BACKUP_FILE ~/.openclaw/openclaw.json"
echo "   2. 安装旧版本：openclaw plugins install @dingtalk-real-ai/dingtalk-connector@latest"
echo ""
