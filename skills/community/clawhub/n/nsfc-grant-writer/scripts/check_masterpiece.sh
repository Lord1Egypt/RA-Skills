#!/bin/bash
# scripts/check_masterpiece.sh
# 国自然申请书代表作选择策略交互式检查

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           国自然申请书代表作选择策略检查工具                 ║"
echo "║           2026新模板：代表作份量更重，需与正文打配合          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 先确认项目类型
echo "请选择项目类型："
echo "  1) 青年科学基金项目（C类）"
echo "  2) 面上项目"
echo ""
read -p "请输入选项 (1/2): " project_type

if [ "$project_type" == "1" ]; then
    PROJECT="青年项目"
    CORE_AUTHOR="第一作者"
    CORE_LOGIC="秀'动手能力'，证明你独立干过"
elif [ "$project_type" == "2" ]; then
    PROJECT="面上项目"
    CORE_AUTHOR="通讯作者"
    CORE_LOGIC="秀'体系能力'，证明你能带队攻关"
else
    echo "无效选项，退出。"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  项目类型：$PROJECT"
echo "  核心逻辑：$CORE_LOGIC"
echo "  关键署名：$CORE_AUTHOR"
echo "═══════════════════════════════════════════════════════════"
echo ""

PASS=0
WARN=0
FAIL=0

check_pass() { echo "   ✅ $1"; ((PASS++)); }
check_warn() { echo "   ⚠️  $1"; ((WARN++)); }
check_fail() { echo "   ❌ $1"; ((FAIL++)); }

# ============ 代表作基本信息 ============
echo "【一、代表作基本信息】"
echo ""

read -p "1. 代表作数量是否为5篇？(y/n) " ans
[ "$ans" == "y" ] && check_pass "数量正确" || check_fail "必须提供5篇代表作"

read -p "2. 所有代表作是否都有正式DOI？(y/n) " ans
[ "$ans" == "y" ] && check_pass "DOI齐全" || check_fail "代表作必须有正式DOI"

read -p "3. 是否有未正式在线发表的论文？(y/n) " ans
[ "$ans" == "n" ] && check_pass "均已正式发表" || check_fail "仅接受已正式发表成果"

read -p "4. 是否有专利、会议摘要作为代表作？(y/n) " ans
[ "$ans" == "n" ] && check_pass "成果类型正确" || check_fail "专利/摘要不能当代表作"

echo ""

# ============ 代表作排序检查 ============
echo "【二、代表作排序检查】"
echo ""

echo "请依次输入5篇代表作的关键信息："
echo ""

for i in 1 2 3 4 5; do
    echo "--- 第${i}篇代表作 ---"
    read -p "  期刊/会议名称: " journal
    read -p "  期刊分区（一区/二区/三区/四区/未分区）: " zone
    read -p "  你在论文中的身份（第一作者/通讯作者/共同一作/其他）: " author_role
    read -p "  与本项目的相关性（直接相关/间接相关/弱相关）: " relevance
    
    echo "  汇总：$journal | $zone | $author_role | $relevance"
    echo ""
done

echo ""

# ============ 署名策略检查 ============
echo "【三、署名策略检查】"
echo ""

if [ "$project_type" == "1" ]; then
    # 青年项目检查
    echo "【青年项目核心要求：前三篇必须是第一作者】"
    echo ""
    
    read -p "5. 第1篇是否为第一作者？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "第1篇一作" || check_fail "第1篇应为一作"
    
    read -p "6. 第2篇是否为第一作者？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "第2篇一作" || check_fail "第2篇应为一作"
    
    read -p "7. 第3篇是否为第一作者？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "第3篇一作" || check_fail "第3篇应为一作"
    
    read -p "8. 第1篇是否为顶刊/一区？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "首篇高影响力" || check_warn "首篇建议选顶刊"
    
    read -p "9. 是否有综述放在第1篇？(y/n) " ans
    [ "$ans" == "n" ] && check_pass "排序正确" || check_fail "综述不能放首位"
    
else
    # 面上项目检查
    echo "【面上项目核心要求：体现通讯作者+研究脉络】"
    echo ""
    
    read -p "5. 第1篇是否为通讯作者？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "第1篇通讯作者" || check_warn "建议首篇为通讯"
    
    read -p "6. 第1篇是否为前序项目核心成果？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "体现前序产出" || check_warn "建议展示前序成果"
    
    read -p "7. 是否有预研论文（与本项目直接相关）？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "有预研支撑" || check_warn "建议展示预研成果"
    
    read -p "8. 通讯作者论文数量是否≥3篇？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "通讯作者充足" || check_warn "通讯作者偏少"
    
fi

echo ""

# ============ 相关性检查 ============
echo "【四、相关性检查】"
echo ""

read -p "10. 5篇代表作中，直接相关的有多少篇？(输入数字) " direct_count

if [ "$project_type" == "1" ]; then
    if [ "$direct_count" -ge 3 ]; then
        check_pass "直接相关论文≥3篇"
    else
        check_warn "青年项目建议至少3篇直接相关"
    fi
else
    if [ "$direct_count" -ge 2 ]; then
        check_pass "直接相关论文充足"
    else
        check_warn "面上项目建议至少2篇直接相关"
    fi
fi

read -p "11. 是否有高影响力但弱相关的论文？(y/n) " ans
[ "$ans" == "n" ] && check_pass "无无关顶刊充数" || check_warn "宁要二区强相关，不要顶刊弱相关"

echo ""

# ============ 贡献栏检查 ============
echo "【五、贡献栏写法检查】"
echo ""

read -p "12. 贡献栏是否写清楚了'我具体干了什么'？(y/n) " ans
[ "$ans" == "y" ] && check_pass "贡献描述具体" || check_warn "贡献描述需更具体"

read -p "13. 是否有'在导师指导下完成'之类表述？(y/n) " ans
[ "$ans" == "n" ] && check_pass "无导师背书表述" || check_fail "禁止'导师指导下'表述"

if [ "$project_type" == "1" ]; then
    read -p "14. 是否体现了'独立设计/独立完成'？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "体现独立能力" || check_warn "建议强调独立完成"
else
    read -p "14. 是否体现了'延续性'（关联前序项目）？(y/n) " ans
    [ "$ans" == "y" ] && check_pass "体现延续性" || check_warn "建议关联前序项目"
fi

read -p "15. 是否有共同一作/共同通讯？(y/n) " ans
if [ "$ans" == "y" ]; then
    read -p "    是否写明了贡献比例？(y/n) " ans2
    [ "$ans2" == "y" ] && check_pass "贡献比例明确" || check_fail "共同作者需写明贡献比例"
else
    check_pass "无共同署名问题"
fi

echo ""

# ============ 与正文配合检查 ============
echo "【六、与正文配合检查】"
echo ""

read -p "16. 正文立项依据中的关键现象，是否在代表作贡献栏点明？(y/n) " ans
[ "$ans" == "y" ] && check_pass "与立项依据配合" || check_warn "建议在贡献栏呼应立项依据"

read -p "17. 正文研究内容中的关键技术，是否在代表作贡献栏写明？(y/n) " ans
[ "$ans" == "y" ] && check_pass "与研究内容配合" || check_warn "建议在贡献栏呼应研究内容"

echo ""

# ============ 雷区检查 ============
echo "【七、雷区检查】"
echo ""

read -p "18. 是否有预警期刊论文？(y/n) " ans
[ "$ans" == "n" ] && check_pass "无预警期刊" || check_fail "预警期刊论文最好不放"

read -p "19. 贡献栏是否使用了模糊表述（如'做出重要贡献'）？(y/n) " ans
[ "$ans" == "n" ] && check_pass "贡献描述具体" || check_fail "避免模糊贡献描述"

read -p "20. 作者排序是否与原文一致？(y/n) " ans
[ "$ans" == "y" ] && check_pass "排序一致" || check_fail "不得改变作者排序"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "                 代表作策略检查结果汇总"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "   ✅ 通过：$PASS 项"
echo "   ⚠️  警告：$WARN 项"
echo "   ❌ 不合格：$FAIL 项"
echo ""

if [ $FAIL -eq 0 ]; then
    if [ $WARN -eq 0 ]; then
        echo "   🎉 代表作选择策略完全正确！"
    else
        echo "   ✅ 基本合格，但有 $WARN 项警告，建议优化。"
    fi
else
    echo "   🚫 存在 $FAIL 项问题，必须调整代表作选择！"
fi

echo ""
echo "【核心要点回顾】"
if [ "$project_type" == "1" ]; then
    echo "  青年项目："
    echo "  • 前三篇必须是第一作者"
    echo "  • 选篇：3篇直接相关 + 1篇拓展 + 1篇高影响力"
    echo "  • 贡献栏：写具体干了什么，体现独立能力"
    echo "  • 避免：综述放首位、导师背书表述"
else
    echo "  面上项目："
    echo "  • 核心是通讯作者，体现带队能力"
    echo "  • 选篇：前序产出 + 预研成果 + 方法学 + 团队合作"
    echo "  • 贡献栏：体现延续性，关联前序项目"
    echo "  • 避免：青年未产出就申面上"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"