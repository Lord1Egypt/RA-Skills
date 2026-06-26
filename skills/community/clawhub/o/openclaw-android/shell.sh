#!/bin/bash

# 日志文件路径
LOG_FILE="/sdcard/Download/openclaw_$(date +%Y%m%d_%H%M%S).log"

# 写入日志函数
log() {
    echo "[$(date +%Y-%m-%d %H:%M:%S)] $1" >> "$LOG_FILE"
    echo "$1"
}

# 初始化日志
log "===== OpenClaw Android 命令执行开始 ====="
log "执行命令: $0 $@"

# 切换到root权限
log "切换到root权限"
su

# 根据参数执行不同命令
case "$1" in
    "start")
        # 启动应用
        if [ -n "$2" ]; then
            log "启动应用: $2"
            am start -n "$2"
            log "应用启动完成"
        else
            log "错误: 缺少应用包名和Activity"
        fi
        ;;
    "stop")
        # 停止应用
        if [ -n "$2" ]; then
            log "停止应用: $2"
            am force-stop "$2"
            log "应用停止完成"
        else
            log "错误: 缺少应用包名"
        fi
        ;;
    "clear")
        # 清除应用数据
        if [ -n "$2" ]; then
            log "清除应用数据: $2"
            pm clear "$2"
            log "应用数据清除完成"
        else
            log "错误: 缺少应用包名"
        fi
        ;;
    "install")
        # 安装应用
        if [ -n "$2" ]; then
            log "安装应用: $2"
            pm install -r "$2"
            log "应用安装完成"
        else
            log "错误: 缺少APK路径"
        fi
        ;;
    "uninstall")
        # 卸载应用
        if [ -n "$2" ]; then
            log "卸载应用: $2"
            pm uninstall "$2"
            log "应用卸载完成"
        else
            log "错误: 缺少应用包名"
        fi
        ;;
    "list-packages")
        # 列出已安装应用
        log "列出所有已安装应用"
        pm list packages
        log "应用列表获取完成"
        ;;
    "list-system")
        # 列出系统应用
        log "列出系统应用"
        pm list packages -s
        log "系统应用列表获取完成"
        ;;
    "list-third-party")
        # 列出第三方应用
        log "列出第三方应用"
        pm list packages -3
        log "第三方应用列表获取完成"
        ;;
    "tap")
        # 点击屏幕
        if [ -n "$2" ] && [ -n "$3" ]; then
            log "点击屏幕坐标: $2, $3"
            input tap "$2" "$3"
            log "点击操作完成"
        else
            log "错误: 缺少坐标参数"
        fi
        ;;
    "swipe")
        # 滑动屏幕
        if [ -n "$2" ] && [ -n "$3" ] && [ -n "$4" ] && [ -n "$5" ]; then
            if [ -n "$6" ]; then
                log "滑动屏幕: $2,$3 -> $4,$5, 延迟: $6ms"
                input swipe "$2" "$3" "$4" "$5" "$6"
            else
                log "滑动屏幕: $2,$3 -> $4,$5"
                input swipe "$2" "$3" "$4" "$5"
            fi
            log "滑动操作完成"
        else
            log "错误: 缺少坐标参数"
        fi
        ;;
    "text")
        # 输入文本
        if [ -n "$2" ]; then
            log "输入文本: $2"
            input text "$2"
            log "文本输入完成"
        else
            log "错误: 缺少文本参数"
        fi
        ;;
    "keyevent")
        # 按键操作
        if [ -n "$2" ]; then
            log "按键操作: $2"
            input keyevent "$2"
            log "按键操作完成"
        else
            log "错误: 缺少按键代码"
        fi
        ;;
    "screenshot")
        # 截取屏幕
        if [ -n "$2" ]; then
            log "截取屏幕到: $2"
            screencap -p "$2"
            log "屏幕截图完成"
        else
            log "截取屏幕到默认路径"
            screencap -p /sdcard/screenshot.png
            log "屏幕截图完成"
        fi
        ;;
    "ls")
        # 查看文件列表
        if [ -n "$2" ]; then
            log "查看目录: $2"
            ls -la "$2"
            log "文件列表获取完成"
        else
            log "查看当前目录"
            ls -la
            log "文件列表获取完成"
        fi
        ;;
    *)
        log "错误: 未知命令 '$1'"
        log "可用命令: start, stop, clear, install, uninstall, list-packages, list-system, list-third-party, tap, swipe, text, keyevent, screenshot, ls"
        ;;
esac

log "===== OpenClaw Android 命令执行结束 ====="
