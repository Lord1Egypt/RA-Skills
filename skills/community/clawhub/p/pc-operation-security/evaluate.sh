#!/bin/bash
# PC-OCS v1.0 操作风险评估脚本
# 用法: ./evaluate.sh "操作描述"

OPERATION="${1:-}"

if [ -z "$OPERATION" ]; then
    echo "用法: $0 \"操作描述\""
    echo "示例: $0 \"删除文件\""
    exit 1
fi

# 转换为小写便于匹配
OP_LOWER=$(echo "$OPERATION" | tr '[:upper:]' '[:lower:]')

# L4 灾难级关键词
L4_KEYWORDS="密码|私钥|证书|双因素|2fa|勒索|暗网|非法|借贷|赌博"

# L3 高危级关键词
L3_KEYWORDS="删除|银行|转账|支付|银行卡|身份证|远程|ssh|rdp|防火墙|杀毒|未知|钓鱼|wifi|安装"

# L2 中危级关键词
L2_KEYWORDS="上传|下载|登录|邮箱|文档|编辑|配置|注册表|位置|行程|联系人|浏览器|插件"

# L1 低危级关键词（默认）

# 评估逻辑
if echo "$OP_LOWER" | grep -qE "$L4_KEYWORDS"; then
    LEVEL="L4"
    NAME="灾难级"
    COLOR="\033[31m"  # 红色
    ADVICE="⚠️ 禁止或严格限制！需要多重确认或隔离环境。"
elif echo "$OP_LOWER" | grep -qE "$L3_KEYWORDS"; then
    LEVEL="L3"
    NAME="高危级"
    COLOR="\033[33m"  # 黄色
    ADVICE="⚡ 需要二次确认、2FA验证或沙箱运行。"
elif echo "$OP_LOWER" | grep -qE "$L2_KEYWORDS"; then
    LEVEL="L2"
    NAME="中危级"
    COLOR="\033[34m"  # 蓝色
    ADVICE="📋 保持警惕，建议监控和记录。"
else
    LEVEL="L1"
    NAME="低危级"
    COLOR="\033[32m"  # 绿色
    ADVICE="✅ 常规处理即可。"
fi

# 输出结果
echo ""
echo "═════════════════════════════════════════════════"
echo "         PC-OCS v1.0 操作风险评估结果"
echo "═════════════════════════════════════════════════"
echo ""
echo "📋 操作描述: $OPERATION"
echo ""
echo -e "🔒 风险等级: ${COLOR}${LEVEL} (${NAME})\033[0m"
echo ""
echo "💡 建议措施: $ADVICE"
echo ""
echo "═════════════════════════════════════════════════"