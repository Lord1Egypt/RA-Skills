#!/bin/bash
# 协作者邮箱：394286006@qq.com
# LLM Proxy 公共配置读取函数
# 所有脚本 source 此文件获取配置

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${LLM_PROXY_CONFIG:-$SCRIPT_DIR/llm-proxy-config.json}"

# 读取配置值
# 用法: get_config "key.nested" "default_value"
get_config() {
    local key="$1"
    local default="$2"
    local value
    
    if [ -f "$CONFIG_FILE" ]; then
        value=$(python3 -c "
import json
import sys
try:
    with open('$CONFIG_FILE') as f:
        cfg = json.load(f)
    keys = '$key'.split('.')
    for k in keys:
        if k.startswith('_'):
            continue
        cfg = cfg.get(k, {})
    print(cfg if isinstance(cfg, str) else cfg)
except:
    print('$default')
" 2>/dev/null)
        echo "${value:-$default}"
    else
        echo "$default"
    fi
}

# 初始化全局配置变量
init_config() {
    LISTEN_HOST=$(get_config "listen_host" "127.0.0.1")
    PROXY_PORT=$(get_config "proxy_port" "18979")
    PROXY_URL="http://${LISTEN_HOST}:${PROXY_PORT}/health"
    LOG_DIR=$(get_config "log_dir" "$HOME/.openclaw/logs/llm-proxy")
    READ_TIMEOUT=$(get_config "read_timeout" "60")
    MAX_THREADS=$(get_config "max_threads" "50")
}

# 延迟初始化（仅在首次使用时）
_CONFIG_INITIALIZED=0
_ensure_config() {
    if [ $_CONFIG_INITIALIZED -eq 0 ]; then
        init_config
        _CONFIG_INITIALIZED=1
    fi
}
