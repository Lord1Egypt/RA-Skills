#!/bin/bash
# scripts/check_format.sh
# 国自然申请书格式审查交互式检查

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        国自然申请书格式审查（形式审查）检查工具              ║"
echo "║        格式审查不合格将直接淘汰，无法进入专家评审            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

PASS=0
WARN=0
FAIL=0

check_pass() { echo "   ✅ $1"; ((PASS++)); }
check_warn() { echo "   ⚠️  $1"; ((WARN++)); }
check_fail() { echo "   ❌ $1"; ((FAIL++)); }

# ============ 4.1 基本信息检查 ============
echo "【一、基本信息检查】"
echo ""

read -p "1. 项目名称是否在100字/符以内？(y/n) " ans
[ "$ans" == "y" ] && check_pass "字数符合要求" || check_fail "项目名称超限"

read -p "2. 学科代码是否与研究内容匹配？(y/n) " ans
[ "$ans" == "y" ] && check_pass "学科代码匹配" || check_warn "请核实学科代码"

read -p "3. 是否已选择研究方向（如有系统提示）？(y/n) " ans
[ "$ans" == "y" ] && check_pass "研究方向已选择" || check_warn "请确认研究方向"

read -p "4. 关键词是否准确且与学科代码对应？(y/n) " ans
[ "$ans" == "y" ] && check_pass "关键词准确" || check_warn "请优化关键词"

read -p "5. 研究属性是否已选择（自由探索类/目标导向类）？(y/n) " ans
[ "$ans" == "y" ] && check_pass "研究属性已选择" || check_fail "必须选择研究属性"

echo ""

# ============ 4.2 人员信息检查 ============
echo "【二、人员信息检查】"
echo ""

read -p "6. 职称信息是否真实有效？(y/n) " ans
[ "$ans" == "y" ] && check_pass "职称信息有效" || check_fail "职称信息需核实"

read -p "7. 年龄是否符合项目要求？(y/n) " ans
[ "$ans" == "y" ] && check_pass "年龄符合要求" || check_fail "年龄超限，无法申请"

read -p "8. 是否确认未超项申请限项？(y/n) " ans
[ "$ans" == "y" ] && check_pass "限项检查通过" || check_fail "存在限项问题"

echo ""
echo "   注：青年项目无参与人，面上项目需检查："
read -p "9. 参与人是否已邀请并点击'邮件通知参与人'？(y/n/跳过) " ans
if [ "$ans" == "y" ]; then
    check_pass "参与人已通知"
elif [ "$ans" == "跳过" ]; then
    echo "   ⏭️  青年项目跳过此项"
else
    check_warn "请通知参与人填写简历"
fi

read -p "10. 是否有学生列为参与人？(y/n) " ans
[ "$ans" == "n" ] && check_pass "符合2024新规" || check_fail "学生不能再列为参与人"

echo ""

# ============ 4.3 个人简历检查 ============
echo "【三、个人简历（代表作）检查】"
echo ""

read -p "11. 作者署名是否按原文真实列出？(y/n) " ans
[ "$ans" == "y" ] && check_pass "作者署名真实" || check_fail "不得篡改作者顺序"

read -p "12. 第一作者/通讯作者是否如实标注？(y/n) " ans
[ "$ans" == "y" ] && check_pass "标注真实" || check_fail "不得虚假标注"

read -p "13. 是否已上传代表性论文全文PDF？(y/n) " ans
[ "$ans" == "y" ] && check_pass "论文已上传" || check_fail "需上传论文全文"

read -p "14. 是否有预警期刊论文作为代表作？(y/n) " ans
[ "$ans" == "n" ] && check_pass "无预警期刊" || check_warn "预警期刊论文最好不放"

echo ""

# ============ 4.4 预算与正文检查 ============
echo "【四、预算与正文检查】"
echo ""

read -p "15. 是否使用信息系统最新版模板？(y/n) " ans
[ "$ans" == "y" ] && check_pass "模板正确" || check_fail "请下载最新模板"

read -p "16. 正文篇幅是否≤30页？(y/n) " ans
[ "$ans" == "y" ] && check_pass "篇幅符合要求" || check_fail "正文超限，必须精简"

read -p "17. 立项依据:研究内容:研究基础是否约1:2:1？(y/n) " ans
[ "$ans" == "y" ] && check_pass "篇幅比例合理" || check_warn "建议调整篇幅比例"

read -p "18. 是否涉及科技伦理敏感领域？(y/n) " ans
if [ "$ans" == "y" ]; then
    read -p "    是否已通过伦理审查？(y/n) " ans2
    [ "$ans2" == "y" ] && check_pass "伦理审查已完成" || check_fail "需补充伦理审查"
else
    check_pass "无伦理敏感问题"
fi

echo ""

# ============ 4.5 附件材料检查 ============
echo "【五、附件材料检查】"
echo ""

read -p "19. 所有附件是否为JPG或PDF格式？(y/n) " ans
[ "$ans" == "y" ] && check_pass "格式正确" || check_fail "仅支持JPG/PDF格式"

read -p "20. 所有附件单个文件是否<1M？(y/n) " ans
[ "$ans" == "y" ] && check_pass "文件大小符合" || check_warn "部分文件过大，请压缩"

read -p "21. 代表性论文首页是否清晰可读？(y/n) " ans
[ "$ans" == "y" ] && check_pass "首页清晰" || check_warn "请确保首页清晰"

echo ""

# ============ 4.6 科研诚信检查 ============
echo "【六、科研诚信检查】"
echo ""

read -p "22. 申请书是否出现涉密信息？(y/n) " ans
[ "$ans" == "n" ] && check_pass "无涉密信息" || check_fail "不得出现涉密信息"

read -p "23. 是否使用AI直接生成的申请书内容？(y/n) " ans
if [ "$ans" == "y" ]; then
    read -p "    是否已如实声明并标识？(y/n) " ans2
    [ "$ans2" == "y" ] && check_pass "AI使用已声明" || check_fail "AI内容必须声明标识"
else
    check_pass "无AI直接生成内容"
fi

read -p "24. 申请书相似度是否在合理范围？(y/n) " ans
[ "$ans" == "y" ] && check_pass "相似度正常" || check_warn "相似度过高，请修改"

echo ""

# ============ 4.7 提交前核对 ============
echo "【七、提交前最终核对】"
echo ""

read -p "25. 依托单位是否已上传《项目申请承诺书》？(y/n) " ans
[ "$ans" == "y" ] && check_pass "承诺书已上传" || check_fail "需上传承诺书"

read -p "26. 申请书是否已征得参与者和合作单位同意？(y/n) " ans
[ "$ans" == "y" ] && check_pass "已征得同意" || check_warn "请确认各方同意"

read -p "27. 电子邮箱是否畅通有效？(y/n) " ans
[ "$ans" == "y" ] && check_pass "邮箱有效" || check_warn "请确保邮箱畅通"

read -p "28. 是否在单位截止时间前提交？(y/n) " ans
[ "$ans" == "y" ] && check_pass "时间充足" || check_fail "请尽快提交！"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "                    格式审查结果汇总"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "   ✅ 通过：$PASS 项"
echo "   ⚠️  警告：$WARN 项"
echo "   ❌ 不合格：$FAIL 项"
echo ""

if [ $FAIL -eq 0 ]; then
    if [ $WARN -eq 0 ]; then
        echo "   🎉 格式审查全部通过！可以提交申请。"
    else
        echo "   ✅ 基本合格，但有 $WARN 项警告，建议优化后再提交。"
    fi
else
    echo "   🚫 存在 $FAIL 项不合格，必须修改后才能提交！"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"