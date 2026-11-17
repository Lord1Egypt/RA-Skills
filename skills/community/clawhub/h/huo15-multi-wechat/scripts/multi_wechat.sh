#!/bin/bash
# 微信多开脚本 — 复制完整微信应用并修改 Bundle ID + 重命名可执行文件 + 重新签名
# 用法: bash multi_wechat.sh [数量]  (默认 2)
set -e

ORIGINAL_APP="/Applications/WeChat.app"
COUNT="${1:-2}"

# 检查原版微信是否存在
if [ ! -d "$ORIGINAL_APP" ]; then
    echo "ERROR: $ORIGINAL_APP not found"
    echo "Please install WeChat first."
    exit 1
fi

# 获取原版 Bundle ID 和可执行文件名
ORIGINAL_BUNDLE_ID=$(/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "$ORIGINAL_APP/Contents/Info.plist")
ORIGINAL_EXEC=$(/usr/libexec/PlistBuddy -c "Print :CFBundleExecutable" "$ORIGINAL_APP/Contents/Info.plist")
echo "Original WeChat: bundle ID=$ORIGINAL_BUNDLE_ID, executable=$ORIGINAL_EXEC"

# 清理旧的副本（可能需要管理员权限）
NEED_SUDO=""
for i in $(seq 2 $((COUNT + 1))); do
    APP_PATH="/Applications/WeChat${i}.app"
    if [ -d "$APP_PATH" ]; then
        OWNER=$(stat -f '%Su' "$APP_PATH" 2>/dev/null || echo "unknown")
        if [ "$OWNER" = "root" ]; then
            NEED_SUDO="$NEED_SUDO $APP_PATH"
        else
            rm -rf "$APP_PATH"
        fi
    fi
done

# 如果有 root 拥有的旧副本，用 osascript 获取管理员权限删除
if [ -n "$NEED_SUDO" ]; then
    echo "Removing root-owned old copies (requires admin password)..."
    osascript -e "do shell script \"rm -rf $NEED_SUDO\" with administrator privileges"
fi

# 创建副本
for i in $(seq 2 $((COUNT + 1))); do
    APP_PATH="/Applications/WeChat${i}.app"
    NEW_BUNDLE_ID="${ORIGINAL_BUNDLE_ID}${i}"
    NEW_EXEC="WeChat${i}"

    echo ""
    echo "=== Creating WeChat${i}.app ==="

    # 1. 复制完整应用
    echo "Copying..."
    cp -R "$ORIGINAL_APP" "$APP_PATH"

    # 2. 修改 Bundle ID（绕过微信单实例锁）
    echo "Modifying CFBundleIdentifier -> $NEW_BUNDLE_ID"
    /usr/libexec/PlistBuddy -c "Set :CFBundleIdentifier $NEW_BUNDLE_ID" "$APP_PATH/Contents/Info.plist"

    # 3. 重命名可执行文件（绕过 Launch Services 缓存，让 open 命令也能多开）
    echo "Renaming executable: $ORIGINAL_EXEC -> $NEW_EXEC"
    cp "$APP_PATH/Contents/MacOS/$ORIGINAL_EXEC" "$APP_PATH/Contents/MacOS/$NEW_EXEC"
    chmod +x "$APP_PATH/Contents/MacOS/$NEW_EXEC"
    /usr/libexec/PlistBuddy -c "Set :CFBundleExecutable $NEW_EXEC" "$APP_PATH/Contents/Info.plist"

    # 4. 修改显示名
    /usr/libexec/PlistBuddy -c "Set :CFBundleName WeChat${i}" "$APP_PATH/Contents/Info.plist"

    # 5. 重新签名（ad-hoc）
    echo "Re-signing..."
    codesign --force --deep --sign - "$APP_PATH"

    # 6. 验证
    ACTUAL_ID=$(/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "$APP_PATH/Contents/Info.plist")
    ACTUAL_EXEC=$(/usr/libexec/PlistBuddy -c "Print :CFBundleExecutable" "$APP_PATH/Contents/Info.plist")
    echo "Verify: CFBundleIdentifier=$ACTUAL_ID, CFBundleExecutable=$ACTUAL_EXEC"
    codesign -v "$APP_PATH" 2>&1 && echo "Signature: OK" || echo "Signature: FAILED"

    echo "✅ WeChat${i}.app created"
done

# 7. 重新注册到 Launch Services + 刷新 Dock
echo ""
echo "Refreshing Launch Services..."
LSREGISTER="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"
for i in $(seq 2 $((COUNT + 1))); do
    "$LSREGISTER" -f "/Applications/WeChat${i}.app"
done
killall Dock 2>/dev/null

echo ""
echo "=== All done! ==="
echo "Original: WeChat.app ($ORIGINAL_BUNDLE_ID, executable=$ORIGINAL_EXEC)"
for i in $(seq 2 $((COUNT + 1))); do
    echo "Copy $((i-1)):  WeChat${i}.app ($ORIGINAL_BUNDLE_ID${i}, executable=WeChat${i})"
done
echo ""
echo "Now you can launch with:"
echo "  open /Applications/WeChat.app   # original"
for i in $(seq 2 $((COUNT + 1))); do
    echo "  open /Applications/WeChat${i}.app"
done
echo ""
echo "Note: First launch may be blocked by Gatekeeper — go to"
echo "      System Settings > Privacy & Security > 'Open Anyway'"
