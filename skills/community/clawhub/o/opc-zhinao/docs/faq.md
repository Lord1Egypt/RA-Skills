<!-- @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-11 -->

# OPC智脑 - 常见问题解答（FAQ）

## IDE路径速查

| IDE | Skills路径 | 配置文件 |
|-----|----------|---------|
| 码道IDE | `.codeartsdoer/skills/` | `.codeartsdoer/agents/opc-zhinao.json` |
| CodeBuddy | `.codebuddy/skills/` | `.codebuddy/skills-registry.json` |
| Cursor | `skills/` | `.cursorrules` |
| VSCode | `skills/` | `.github/copilot-instructions.md` |
| 其他 | `skills/` | `AGENTS.md` |

---

## 安装问题

**Q1：安装后IDE没识别到？**

检查3项：① `AGENTS.md` 存在 ② Skills目录存在（路径见上表） ③ 配置文件正确（路径见上表）。仍不行则重启IDE。

**Q2：如何验证安装成功？**

```bash
# Skills数量应为8
ls -d .codeartsdoer/skills/*/ | wc -l   # 码道IDE
ls -d .codebuddy/skills/*/ | wc -l       # CodeBuddy
ls -d skills/*/ | wc -l                  # 其他IDE

# 或使用验证脚本
bash verify-install.sh
```

**Q3：可以在已有项目中安装吗？**

可以。OPC智脑只添加文件，不覆盖现有内容。如遇同名文件会提示是否覆盖。

**Q4：如何卸载？**

```bash
# 码道IDE
rm AGENTS.md .codeartsdoer/agents/opc-zhinao.json && rm -rf .codeartsdoer/skills/
# CodeBuddy
rm AGENTS.md .codebuddy/skills-registry.json && rm -rf .codebuddy/skills/
# 其他
rm -rf AGENTS.md skills/ opc-zhinao-prompt.md
```

**Q5：权限不足/路径不存在？**

```bash
# 权限不足
sudo bash install-prompt.sh /path/to/project
# 路径不存在
mkdir -p /path/to/project && bash install-prompt.sh /path/to/project
```

---

## 使用问题

**Q6：Skills无法触发？**

1. 确认安装成功（见Q2） 2. 使用正确触发关键词 3. 重启IDE

| Skill | 触发关键词 |
|-------|----------|
| Skill1-Idea可行性研判 | 创业Idea、想法、点子、可行性、需求验证 |
| Skill2-MVP精益设计 | MVP、产品设计、功能裁剪、交付成本、首单 |
| Skill3-OPC合规落地 | 注册公司、个体户、合规、财税、经营范围 |
| Skill4-种子用户冷启动 | 获客、种子用户、冷启动、定价、付费验证 |
| Skill5-规模化增长 | 规模化、增长引擎、自动化、品牌、复购 |

**Q7：输出格式异常？**

重新安装：`bash install-prompt.sh .`

**Q8：阶段判定错误？**

提供完整的6项核心信息（行业赛道、是否有Idea、是否有产品、是否注册公司、是否有付费用户、个人背景），使用量化数据，避免模糊表述。

**Q9：可以跳阶段吗？**

不建议。坚持跳阶段会输出风险警告，标注需补课事项。

---

## 配置问题

**Q10：如何自定义Skill？**

在对应IDE的Skills路径下创建目录并编写SKILL.md：

```bash
# 码道IDE示例
mkdir -p .codeartsdoer/skills/my-custom-skill
cat > .codeartsdoer/skills/my-custom-skill/SKILL.md << 'EOF'
---
name: my-custom-skill
description: 自定义Skill
---
# Skill内容
EOF
```

**Q11：如何修改触发关键词？**

编辑 `AGENTS.md` 的"九、Skills 触发规则"表格，修改后重启IDE。

---

## 兼容性问题

**Q12：支持哪些IDE/平台？**

国内：码道IDE、通义灵码、百度Comate、腾讯云AI、豆包MarsCode、CodeGeeX、讯飞iFlyCode
国际：Cursor、VSCode+Copilot、Windsurf、CodeBuddy
平台：OpenAI API、Claude API、Coze、Dify、LangChain

**Q13：如何更新？**

```bash
cd opc-skills && git pull origin main
bash install-prompt.sh /path/to/your-project
```

---

## 错误用法警告（⚠️ 不要这样做）

**Q16：把AI诊断结论当成确定事实**

❌ 错误：AI说"高度可行"就直接投入全部资源开发
✅ 正确：AI诊断是参考意见，必须经过你自己的验证。AI判定"高度可行"→你再用Landing Page测试转化率→确认后才投入。

**Q17：跳过需求验证直接开发产品**

❌ 错误：有Idea就立刻写代码，跳过Skill1直接进Skill2
✅ 正确：必须先验证需求真伪。未验证的需求=赌博，开发3个月发现没人要=浪费3个月。

**Q18：把OPC智脑当法律/财税/技术顾问**

❌ 错误：让OPC智脑起草合同条款、做税务申报、写代码
✅ 正确：OPC智脑给出方向和建议，具体执行找律师（合同）、会计师（财税）、代码助手（开发）。

**Q19：一次跳多个阶段**

❌ 错误：从构思期直接跳到注册公司，跳过MVP设计和验证
✅ 正确：五阶段必须按序推进。每阶段有毕业条件，未毕业就跳=基础不牢，后续大概率返工。

**Q20：忽略AI输出的自检警告**

❌ 错误：看到校验警告（如"核心功能超过3个"）直接忽略继续
✅ 正确：校验警告是AI输出纠偏机制，每个warning都必须处理或明确标注"已知悉，有意为之"。

**Q21：用模糊表述代替量化数据**

❌ 错误：回答"预算还行"、"时间够用"、"有一些技能"
✅ 正确：必须量化——"预算5000元"、"每周可投入20小时"、"会Python和产品设计"。模糊输入=模糊输出=诊断无价值。

**Q22：把AI当搜索引擎问非创业问题**

❌ 错误：问"今天天气怎么样"、"帮我写一首诗"、"XX明星八卦"
✅ 正确：OPC智脑只服务创业诊断，非创业问题会被拒绝。专注才能给出有价值的建议。

**Q23：诊断一次就当定论，不复盘不迭代**

❌ 错误：做完一次诊断就照着执行3个月，中间不复盘
✅ 正确：创业是动态过程，每完成一个关键动作都应该回来重新诊断。建议每2-4周复盘一次。

---

## 其他

**Q14：OPC智脑能/不能做什么？**

✅ 能：创业Idea诊断、MVP设计、合规落地、冷启动策略、规模化增长、阶段判定
❌ 不能：写代码（用Cursor等）、法律合同（找律师）、财税操作（找会计师）、爬虫（违法）

**Q15：如何获取帮助？**

- 仓库：https://gitee.com/zx_allen_li/opc_skills.git
- 作者：李屹镒（公众号：科技新潮。视频号：小李君与AI）
- Issue：https://gitee.com/zx_allen_li/opc_skills/issues

---

**最后更新**：2026-06-13
