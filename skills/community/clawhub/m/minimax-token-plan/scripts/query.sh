#!/bin/bash
# MiniMax Token Plan 余额查询
# 认证：使用环境变量 MINIMAX_API_KEY
# 注意：从不通过命令行参数接收 Key，避免 ps aux 泄露

AUTH_VALUE="${MINIMAX_API_KEY:-}"

if [[ -z "$AUTH_VALUE" ]]; then
    echo "错误：未找到 API Key"
    echo ""
    echo "首次使用请先获取 API Key："
    echo ""
    echo "1. 登录 https://platform.minimaxi.com"
    echo "2. 进入 用户中心 → 接口密钥"
    echo "3. 创建 Token Plan Key"
    echo "4. 复制 Key 后直接粘贴给我"
    echo ""
    echo "获取后选择："
    echo "  - 单次查询：只查一次，不保存"
    echo "  - 保存到本地：保存 Key，以后直接查询"
    exit 1
fi

URL="https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"

RESULT=$(curl -s -X GET "$URL" \
    -H "Authorization: Bearer $AUTH_VALUE" \
    -H "Content-Type: application/json")

# 检查是否是错误响应
ERROR_CODE=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('base_resp',{}).get('status_code',0))" 2>/dev/null)

if [[ "$ERROR_CODE" != "0" ]]; then
    ERROR_MSG=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('base_resp',{}).get('status_msg','未知错误'))" 2>/dev/null)
    echo "查询失败：$ERROR_MSG"
    echo ""
    echo "可能原因："
    echo "  - API Key 无效或已过期"
    echo "  - Key 类型不是 Token Plan 类型"
    echo "  - 额度已用完"
    echo ""
    echo "请到 https://platform.minimaxi.com/user-center/basic-information/interface-key 检查 Key 是否正确"
    exit 1
fi

echo "$RESULT"
