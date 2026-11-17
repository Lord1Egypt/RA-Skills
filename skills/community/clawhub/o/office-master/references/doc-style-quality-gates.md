# 文档样式质量门禁方法论（office-master 增量方法论）

> [scripts/check_doc_style.py](../scripts/check_doc_style.py) / `check_ppt_brief.py` 是机械执行层。本文档讲**为什么**要这些门禁、
> 哪些规则该卡、哪些不该卡、怎么把门禁嵌进写作流而不是事后补救。这是脚本装不下的判断方法论。

## 1. 决策树：这份文档要不要过样式门禁？

```
文档用途
├─ 要转成 Word/PPT/PDF（md-to-office）？ → 必过（层级错=分页错）
├─ 要进 Git / 多人协作？ → 必过（diff 友好、结构清晰）
├─ 要当演示 brief（presentation-designer）？ → 必过（H2=页，结构错=页数错）
└─ 纯个人草稿？ → 可选，但养成习惯省后期
```

**铁律**：凡是会被「机器读取结构」的文档（转换、分页、检索），层级规范不是美观问题，是功能正确性。

## 2. 为什么标题层级这么重要

| 错误 | 后果 |
|------|------|
| 多个 H1 | Pandoc 分页错乱、目录生成异常 |
| 跳级（H1→H3） | 大纲断档，读者丢失上下文层级 |
| 超深（>4 级） | 信息过细，PPT 分页碎成十几页 |
| 重复 slug | 锚点链接指向歧义，交叉引用错 |
| 缺 frontmatter | 元数据（标题/作者）丢失，交付件无属性 |

> 这些不是「最好有」，是「机器解析的前提」。门禁把人易忽略的结构错误量化出来。

## 3. 规则卡控矩阵（卡 / 不卡）

| 规则 | 卡？ | 理由 |
|------|------|------|
| 单一 H1 | 卡 | 分页与目录正确性的前提 |
| 不跳级 | 卡 | 大纲层级完整 |
| 最大深度 ≤3-4 | 卡 | 防止过度细分 |
| 重复 slug | 卡 | 锚点唯一 |
| frontmatter title | 卡 | 交付件元数据 |
| 残留 token（`TODO`） | 卡 | 不应进交付物 |
| 具体用词/语气 | 不卡 | 属表达，人审 |
| 内容对错 | 不卡 | 超出静态检查范围 |
| 围栏代码块内的 `#` 注释 / 示例 token | **不卡** | 那是代码，不是标题也不是残留 |
| 行内代码里的 `TODO` | **不卡** | 那是「在讲这个 token」，不是没写完 |

> 边界：门禁只管「结构正确」，不管「写得好不好」。把内容质量留给人和 presentation-designer。

**作用域边界（易踩）**：`required_frontmatter_keys: ["title"]` 是**交付稿件**规范。
技能仓库的 `SKILL.md` 用 `name`/`description`/`metadata`，天然没有 `title` 键——
别对含 `SKILL.md` 的仓库根递归跑门禁，那会刷出一堆与稿件质量无关的误报。
正确做法：只对稿件目录跑（`docs/`、`briefs/`），或显式列出稿件文件。

## 4. 门禁嵌入写作流（而非事后）

```
写 MD 时：编辑器实时标层级 → 提交前跑 check_doc_style → CI 再跑一次
         ↓ 不过则本地修
转 Office / 生成 PPT 前：已合规，零结构错误
```

比「写完转完发现分页乱、再回 MD 改、再转」省力十倍。门禁前移是核心收益。

```bash
# 提交前本地门禁
python3 scripts/check_doc_style.py docs/ product.md
# CI 同款命令，防回归
```

## 5. 与规则文件的关系（单一事实来源）

所有阈值都在 [assets/doc-style-rules.json](../assets/doc-style-rules.json)：

```json
{
  "single_h1": true,
  "no_skipped_levels": true,
  "max_heading_depth": 3,
  "required_frontmatter_keys": ["title"],
  "missing_tokens": ["TODO", "FIXME", "XXX", "TBD"],
  "ppt_min_slides": 3,
  "ppt_max_slides": 20,
  "ppt_max_title_len": 60,
  "ppt_max_body_chars": 400
}
```

> 团队调整「最大深度」「允许 token」只改这一个文件，脚本与 CI 同步生效。注释键以 `_` 开头，脚本读取时跳过，不会被当规则。

## 6. 典型坑与规避

1. **门禁当摆设**：本地不跑、全靠 CI 报错 → 改一轮推一轮，慢；本地先跑。
2. **阈值过严**：max_depth=2 逼人全平铺 → 按真实需求设 3-4。
3. **把内容问题塞进门禁**：让脚本判「用词不当」→ 超范围，误报多，回归人审。
4. **忽略 `_` 注释键**：把注释当规则 → 脚本应跳过，规则文件设计已保障。
5. **只查不修**：门禁报了但手动改 Word 绕过 → 回 MD 源改，保持单向。
6. **PPT brief 不过 check_ppt_brief**：页数/标题乱 → 分页与一致性崩。
7. **围栏正则写成 `^```{3,}`**（本仓库真实踩坑，2026-09-01 修）：`{3,}` 只作用于紧邻的
   **第 3 个**反引号，整体等价于「要求 ≥5 个反引号」，普通三反引号围栏一个都匹配不上 →
   代码块剥离**静默失效**。后果：一份完全合规的技术文档，只因含 3 个 `bash` 代码块（注释以
   `#` 开头）就被误报「H1 数量 4 + 跳级」，门禁被误报淹没，团队直接弃用。
   正确写法 `^ {0,3}(` + 三反引号 + `{3,}|~{3,})`，且闭合围栏须同字符、长度不短于开启（防嵌套示例提前闭合）。
   **教训**：量词只管前一个字符——涉及重复字符的正则必须写单元测试逐串验证，别靠肉眼读。
8. **残留 token 检测不剥离代码块与行内代码**（同批修）：讲规则时写的 `TODO`、反例代码块里的
   `TODO: 补结论` 全被当成「没写完」→ 越是认真写门禁文档的仓库误报越多。
   剥离规则：围栏内一律不算；行内代码 `` `TODO` `` 视为「在讲这个 token」不算；只有裸散文里的才算。
9. **只查稿件正文、漏查分页口径**：`check_ppt_brief` 若同样不剥离围栏，代码块里的 `## step`
   会被数成幻灯片页——3 页 brief 数成 5 页，**且仍落在 min/max 区间内静默通过**，
   下游按 H2 分页的转换随之产出错误页数。页数类校验必须先确认「页」的识别口径本身没被污染。

## 7. 实战：一份坏文档被门禁逐条拦下

把下面这段存成 `bad.md`（**注意：样稿里不要用 `#` 当行尾注释**——Markdown 没有行内注释，
`## 重复   # 重复 slug` 的标题文本会变成「重复 # 重复 slug」，和另一个「重复」不同 slug，
重复检测反而不触发；这个坑本文档自己踩过，见第 6 节第 7 条）：

```markdown
---
author: alice
---
# 第一章
# 第二章
### 子节
#### 过深层
## 重复
## 重复
TODO: 补结论
```

```bash
python3 scripts/check_doc_style.py bad.md   # 退出码 1
```

实跑输出（6 类缺陷一一对应，不是凑数字）：

```text
[样式] bad.md: frontmatter 缺少必需键 'title'
[样式] bad.md: H1 数量应为 1，实际 2
[样式] bad.md:6 标题层级从 1 跳到 3（禁止跳级）
[样式] bad.md:7 标题层级 4 超过最大深度 3
[样式] bad.md:9 重复标题（slug='重复'，首次在 8 行）
[残留] bad.md:10 -> TODO
[FAIL] 发现 6 处样式问题
```

作者按报告逐条回 MD 修正，重跑通过，再转 Office——分页与目录从此正确。

> 这个「注入 6 缺陷、检出 6 类」正是门禁可信的底线：静默漏报比报错更危险。
> **验证纪律**：断言「注入 N 检出 N」时，必须核对**逐条类型**，不能只核总数——
> 本节旧版曾声称检出「重复 slug」，实际它没触发，而是被另一条多报的跳级把总数凑回 6，
> 总数对、类型错，等于藏了一处静默漏报。写自证示例必须真跑一次并贴原始输出。

## 8. CI 集成（防回归）

```yaml
# .github/workflows/doc-style.yml
name: doc-style
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/check_doc_style.py docs/ README.md
      - run: python3 scripts/check_ppt_brief.py assets/presentation-brief-template.md
```

> 门禁进 CI 后，「结构错」永远卡在合并前，不会流进转换流水线污染交付件。

## 9. 门禁演进：从哪儿加规则

加规则遵循三问：
1. 这是「结构正确」还是「内容好坏」？→ 后者不加。
2. 误报率高吗？→ 高则放宽或移除。
3. 团队真需要吗？→ 没人触发就别加（YAGNI）。

例：曾想加「标题含动词」规则，发现误报多且属表达 → 否决。保留「单一 H1 / 不跳级 / 深度 / 重复 / frontmatter / token」这组最小集。

## 10. 典型坑与规避（续）

7. **门禁通过=文档写好**：结构对不等于内容对 → 门禁后仍需人审表达。
8. **不同仓库阈值打架**：A 仓 max_depth=3、B 仓=4 → 各仓库自有 rules 文件，别全局强一。
9. **脚本当法官**：用门禁结果替人拍板内容 → 越界，脚本只报结构。
10. **忘了 brief 门禁**：只查长文档不查 brief → PPT 分页乱；brief 必过 check_ppt_brief。

## 11. 可勾选清单

- [ ] 凡被机器读结构的文档都过样式门禁
- [ ] 门禁只卡结构、不卡内容表达
- [ ] 阈值设在 doc-style-rules.json 单一事实来源
- [ ] 本地提交前先跑，CI 再跑防回归
- [ ] 规则文件 `_` 注释键被正确跳过
- [ ] brief 额外过 check_ppt_brief（页数/标题/正文/重复）
- [ ] 门禁不过时回源（MD）修正，不绕到 Office 手改
- [ ] 阈值随团队实际调整，不过严也不过松
- [ ] 新规则经「结构/误报/必要」三问才加
- [ ] 门禁通过后仍有人审内容表达
- [ ] 门禁只对稿件目录跑，未误扫 `SKILL.md` 等非稿件文件
- [ ] 改过检查逻辑后，用「合规样稿必须 rc=0」+「坏样稿必须逐条报出」两侧各跑一次
- [ ] 自证示例的断言核对到**逐条类型**，不只核总数（防总数对、类型错的静默漏报）

## 12. 门禁与转换工具的分工

| 环节 | 谁负责 | 产出 |
|------|--------|------|
| 结构规范 | check_doc_style / check_ppt_brief | 结构正确 |
| 格式转换 | markitdown / Pandoc / python-pptx | 格式正确 |
| 品牌设计 | presentation-designer | 视觉正确 |
| 内容表达 | 人 | 说清楚 |

四者各管一段，门禁守第一道闸。任何一段越界（如让脚本判内容）都会制造误报与维护负担。

## 13. 一句话总结

门禁的价值不是「拦住你」，而是把「结构正确性」这件机械、易漏、难肉眼发现的事，变成
一条确定性、可复现、进 CI 的命令。你因此能把精力放在只有人能做好的事——把话写清楚。

## 14. 阈值调优记录（示例）

| 时间 | 调整 | 原因 |
|------|------|------|
| 初版 | max_depth=2 | 过严，技术文档需 H3 |
| v2 | max_depth=3 | 放宽到真实上限 |
| v2 | ppt_max_title_len=60 | 实测超 60 字页标题在 16:9 易折行 |
| v3 | 加 missing_tokens `TBD` | 发现 `TBD` 漏进交付件 |

> 阈值不是拍脑袋，是从真实文档问题反推。每次调整都回写 `doc-style-rules.json` 并跑一遍 `--check-rules` 自检。

## 15. 给新人的最小心法

写任何要被转换或分页的 Markdown，记住三条：① 只有一个最高级标题；② 标题一级一级往下，不跳；
③ 写之前就把 `title` 放进 frontmatter。做到这三条，`check_doc_style` 几乎永远一次过，
后面的转换与分页自然稳。门禁不是负担，是让你少返工的习惯。

## 16. 相关子技能与层次边界（L2→L3）

本篇是 **L2 决策层**：只解决「要不要过门禁 / 卡哪些规则 / 阈值怎么调 / 怎么进 CI」。
门禁通过之后的转换与设计动作由 L3 子技能承担，不在本篇复制：

| 你要做的事 | 去 L3 子技能 | 本篇只负责 |
|-----------|-------------|-----------|
| 门禁过了之后转 Word/PPT/PDF | [skills/md-to-office/SKILL.md](../skills/md-to-office/SKILL.md) | 只保证源结构合法 |
| 把 Office 转成 MD 后再过门禁 | [skills/office-to-md/SKILL.md](../skills/office-to-md/SKILL.md) | 只定义合法标准 |
| 演示大纲通过后的设计执行 | [skills/presentation-designer/SKILL.md](../skills/presentation-designer/SKILL.md) | 只卡结构不管美观 |
| 用 python-pptx 批改幻灯片 | [skills/ppt-automation/SKILL.md](../skills/ppt-automation/SKILL.md) | 不涉及 pptx 编程 |
| 门禁规则里的品牌 / 模板项来源 | [skills/office-context/SKILL.md](../skills/office-context/SKILL.md) | 不存储品牌状态 |

同层 references（平级 L2，互不复制）：

- 门禁在转换流水线中的位置 → [references/office-md-roundtrip.md](office-md-roundtrip.md)（其第 3、9 节调用本篇命令）
- 演示侧的 brief 门禁与设计规则 → [references/presentation-design-system.md](presentation-design-system.md)（其第 9 节调用本篇命令）
- 品牌 / 模板上下文与规则文件的关系 → [references/office-context-playbook.md](office-context-playbook.md)

配套确定性工具：[scripts/check_doc_style.py](../scripts/check_doc_style.py) + [scripts/check_ppt_brief.py](../scripts/check_ppt_brief.py)，规则单一事实来源为 [assets/doc-style-rules.json](../assets/doc-style-rules.json)。

边界一句话：**本篇决定「卡什么、卡多严」，脚本负责机械执行，L3 负责门禁之后的产出动作。**
