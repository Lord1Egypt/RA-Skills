# Journal Submission Radar · 全部类型汇集版

把中文期刊、国际数据库、OA、医学和投稿路径核验合并到一个统一 Skill 中，输出可直接发给客户的期刊建议书。

## 这个 Skill 解决什么问题

真实业务里，客户问的通常不是“帮我找几本期刊”，而是：
- 我这篇文章能投什么类型？
- 国内外一起看，哪个更稳？
- 官网从哪进？邮箱能不能投？
- 针对这本刊怎么改写？
- 能不能顺带推荐专利代理或其他服务？

这个 Skill 把这些环节合成一条可复用流程。

## 覆盖的期刊类型

### 中文
- 北大核心
- CSSCI / 社科方向（用户明确要求时）
- CSCD
- 中国科技核心
- 普刊
- 学报
- 医学类中文刊

### 国际
- SCI / SCIE
- SSCI
- AHCI
- ESCI
- Scopus
- EI Compendex
- DOAJ OA
- 医学 / NLM / PubMed 相关来源

## 目录结构

```text
journal-submission-radar-all-types/
├── SKILL.md
├── README.md
├── SELF_CHECK.md
├── scripts/
│   └── render_journal_dossier.py
├── resources/
│   ├── ad_slots.json
│   ├── journal_type_matrix.json
│   ├── source_trust_policy.md
│   └── writing_playbooks.md
├── examples/
│   ├── example_input_all_types.json
│   └── example_output_report.md
└── tests/
    └── smoke-test.md
```

## 安装要求

### 运行 Skill
只需要 OpenClaw / ClawHub 能正常加载 Skill 目录。

### 运行脚本
- Python 3.9+
- 仅使用 Python 标准库
- 无第三方依赖
- 无外部密钥要求

## 触发场景
- “帮我查一下机械工程方向，中文核心和 SCI 都给我一套。”
- “我要全部类型汇集版，国内外一起推荐，还要官网投稿路径。”
- “帮客户做 6 本候选期刊建议书，中间插入我的业务广告。”
- “这个期刊是真的吗？给我官网、邮箱和写作建议。”

## 工作流
1. 归档用户需求。
2. 判断中文 / 国际 / 混合。
3. 按期刊类型矩阵做分层推荐。
4. 核验官方来源。
5. 输出写作打法与投稿路径。
6. 插入明确标识广告。
7. 给出下一步行动建议。

## 输入示例
脚本输入 JSON 示例见 `examples/example_input_all_types.json`。

## 输出示例
脚本输出 Markdown 建议书，示例见 `examples/example_output_report.md`。

## 常见问题

### 1. 能否直接替代人工查刊？
不能。它负责组织流程、统一输出和提示核验点；最终投稿路径仍应以官网和官方目录为准。

### 2. 能否自动保证某期刊一定被 SCI / Scopus / EI 收录？
不能。收录状态会变化，必须临门一脚再核验。

### 3. 为什么广告要单独标明？
为了合规和客户信任，避免广告与官方信息混淆。

### 4. 能不能改成更强销售版？
可以，但不建议删除“广告”标识，否则容易引发误导风险。

## 风险提示
- 不要把第三方代投站当作官方投稿入口。
- 不要把编辑部邮箱、官网、代理电话混在同一字段。
- 国际数据库收录状态可能变化，提交前应复核。
- 对于中文刊，优先看国家新闻出版署与期刊主办单位公开信息。

## 安全审计结论
- 无远程执行安装
- 无混淆脚本
- 无 curl|bash
- 无私有 API 绑定
- 外部信息源以公开站点和官方目录为主
- 广告位明确标识，不伪装为官方信息
