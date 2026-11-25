# 阶段 5 规程 — Validate 校验

目标：机械化校验产物结构合规。**脚本是 pre-filter**：脚本通过 ≠ 任务完成，仍需人工/agent 抽查内容质量。

## 终稿锁定（前置门槛）

终态校验前 MUST 确认产物已终稿，二选一：

1. **agent 回报确认**：所有萃取/蒸馏 agent 均已回报完成，且回报中的产物规模指标（行数/条数）与磁盘实测一致（误差 ≤5%）；
2. **mtime 稳定性**：回报未达或迟到时，记录产物文件 mtime 快照，间隔 ≥5 分钟二次采样无变化，方可进入校验。

若 agent 回报在校验完成后才到达（第六轮实证：校验基于中间版全绿后 agent 又重写产物，「已验证态」被静默替换），MUST 对磁盘现状重跑全链路校验（validate → audit → spot_check → 回归），不允许沿用旧报告。

**行数口径统一**：一切行数以 `validate_skill.py` 的 `splitlines()` 口径（总行数，含空行）为准；禁用 PowerShell `Measure-Object -Line`（非空行口径）汇报或核对产物行数——两种口径差异可达 20%+，历史上多次造成同一文件三个「行数」数字打架。

## 首选：运行脚本

```
python <skill根>/scripts/validate_skill.py <产物目录> --keywords <description_keywords 逗号列表>
```

脚本检查项：frontmatter 可解析、name/description 合规且 name 与目录同名、description 关键词覆盖率、kb 文件非空/≤2000 行/含「来源索引」、UTF-8、总体积 ≤2MB、嵌套 SKILL.md。

退出码 0 = 全部通过；非 0 = 按报告逐项修复后重跑。**不要**为绕过校验去修改脚本阈值——阈值是质量红线，修产物不修红线。

## 编号审计（含编号法则体系的产物必跑）

```
python <skill根>/scripts/audit_refs_react.py <产物目录>    # react 域（LAW/MO/NE/NX/RA/RC/TQ/TE/VT）
python <skill根>/scripts/audit_refs.py <产物目录>          # ui-ux 域（LAW/G/AIM/P/VP/LC/CS/TY/SD/IM/UA/IND/TPL/WC/AP）
```

检查：各前缀编号 n=max 连续无缺口、断链（引用未定义编号）= 0、孤儿（定义零引用）= 0、corpus 路径存在性。退出码非 0 = 按报告修复后重跑。

## 降级：人工清单（Python 不可用时）

逐项核对（全部通过才算校验完成）：

### SKILL.md

- [ ] frontmatter `---` 包裹，`name` 与 `description` 均存在
- [ ] `name` 小写字母数字+连字符、≤64 字符、与目录名完全一致
- [ ] `description` 非空、第三人称、关键词前置、覆盖 ≥80% 配置 keywords

### kb 文件

- [ ] 配置的每个 subdomain + 扩展子领域（`spin_off_subdomains`）+ 横切文件都存在
- [ ] 每个文件非空、≤2000 行
- [ ] 每个文件含「来源索引」小节
- [ ] 单文件 UTF-8 无乱码

### 结构

- [ ] 产物总体积 ≤2MB
- [ ] 目录内有且仅有一个 SKILL.md（无嵌套）
- [ ] SKILL.md 索引表/决策树与 kb 实际文件一一对应

## 事实抽查（语义级，结构校验的盲区补充）

脚本只验结构不验事实。**每 2 个蒸馏轮次至少执行 1 次**：

1. **URL 抽查（脚本）**：`python <skill根>/scripts/spot_check.py <产物目录> [--sample N|--all]`——抽取 kb 来源索引 URL 探活，输出 OK/BLOCKED/EXEMPT/BROKEN 四态（EXEMPT=POST-only/需凭证端点豁免不探活；BLOCKED=反爬/限流/超时，可达不确定，不计失败）；BROKEN（404/4xx/5xx/DNS 失败）必须修复或登记，退出码非 0 即失败。
2. **硬事实抽查（agent 执行）**：随机抽 ≥10 条硬事实（版本号/API 签名/默认值/破坏性变更），重抓其来源 URL 比对：
   - 一致 → 无操作；
   - 不一致 → 修正条目，「冲突消解记录」登记（原依据 → 新文档事实）；
   - 来源已失效（404/改版）→ 按 URL 纪律重新发现来源，登记 URL 迁移。
3. 抽查结果记入被抽查 kb 尾「事实抽查记录」：`| 轮次 | 抽查条数 | 结果 | 日期 |`。
4. 「版本注意」小节的版本锚点按 npm registry / 官方发布日志复核，陈旧即更新。

### 内容抽查（agent 执行）

- [ ] 抽 3~5 条「版本注意」硬事实：有 `[官方文档]` 佐证或显式「未经文档验证」声明
- [ ] 抽 3~5 条 `[模型经验]`：附适用说明，且不属于版本号/API 签名类硬事实
- [ ] 抽查代码对照：错误代码真实典型、正确代码无语法错误
- [ ] 无凭空 URL：所有来源 URL 来自阶段 2 抓取记录
