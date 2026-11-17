# insight-challenge

对代码评审、静态分析或安全扫描产出的"发现"进行**对抗性验证**的技能：以怀疑立场独立查证每条发现是否真实成立，产出 overturned（推翻）/ weakened（削弱）/ confirmed（确认）三态结论，避免修复无中生有的问题。

## 目录结构

```
insight-challenge/
├── SKILL.md                       # 中文主文档（技能入口：输入格式、四阶段流程、输出模板、错误码）
├── SKILL.en.md                    # English 主文档
├── README.md                      # 本文件：导航与运行说明
├── README.en.md                   # English navigation & usage
├── specs/
│   ├── challenge-protocol.md      # 挑战协议：五种挑战策略与决策树
│   ├── challenge-protocol.en.md
│   ├── verdict-schema.md          # 结论 schema：字段定义与取值约束
│   └── verdict-schema.en.md
├── scripts/
│   └── validate-verdict.mjs       # 零依赖结论校验器（fail-closed）
└── tests/fixtures/
    ├── verdict-good.json          # 合规样本（校验应 PASSED）
    └── verdict-bad.json           # 违规样本（校验应以错误码拒绝）
```

注：源仓库中还包含 `LICENSE`（发布打包时被剔除，仅存于仓库）。

## 依赖

仅需 Node.js ≥ 18；校验器零第三方依赖，无需安装任何包。

## 运行校验器

三种输入方式：

```bash
# 1. 校验 JSON 文件（单条结论、批量 verdicts 对象或顶层数组）
node scripts/validate-verdict.mjs verdict.json

# 2. 从 stdin 管道输入
cat verdict.json | node scripts/validate-verdict.mjs -

# 3. 直接校验 markdown 报告（自动提取内嵌的 ```json 结论块）
node scripts/validate-verdict.mjs report.md
```

校验失败时按错误码（IC-V00~V13）定位问题；证据期望未满足时输出 IC-W01~W03 警告（不影响 exit 码）；exit 0 表示通过。

## 运行测试

```bash
node scripts/validate-verdict.mjs tests/fixtures/verdict-good.json   # 期望：PASSED
node scripts/validate-verdict.mjs tests/fixtures/verdict-bad.json     # 期望：校验失败 exit 1，错误码覆盖 IC-V01~V06、V09、V11~V13
```

仓库根的 `.github/workflows/ci.yml`（不属于本技能分发包）在每次推送时运行这两组断言及 stdin/markdown 模式门。

## 文档导读

| 想了解 | 看这里 |
|--------|--------|
| 技能如何调用、输入输出 | SKILL.md |
| 五种挑战策略与决策树 | specs/challenge-protocol.md |
| 结论字段与校验规则 | specs/verdict-schema.md |
| 校验器用法 | 本文件 + `node scripts/validate-verdict.mjs`（无参数显示 Usage） |
