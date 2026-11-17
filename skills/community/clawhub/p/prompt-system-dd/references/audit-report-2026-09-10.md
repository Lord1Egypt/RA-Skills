# 全链路审计报告(2026-09-10)

> 审计对象:advanced-prompt-engineering-template v5.5.0(SKILL.md + references/ 全部协议与原子 + scripts/ 四个脚本 + benchmark/ 基线)
> 审计方法:① 运行自带门禁 `validate_skill.py --strict`(结果:0 error / 0 warning,67 文件 checked);② 运行门禁自测 `test_validate_skill.py`(6/6 passed);③ 在门禁绿灯前提下,对文档间引用、脚本间常量、规则→实现→示例→基线四层链路做逐条人工比对。
> 结论前提:**门禁全绿 ≠ 链路无断裂**。门禁只做字符串/结构级存在性校验,以下问题全部位于门禁盲区。每条问题均给出证据(文件:行号+关键原文)、影响与修复建议,无跳步。

---

## 一、P0 级(执行链路真实断裂,照文档走会做错)

### P0-1 核心原子位序存在第三处硬编码,且完全不受门禁保护

- **主张**:注册制承诺"新增原子无需修改脚本"是假的——位序实际硬编码在三处,门禁只校验前两处。
- **证据链**:
  1. `validate_skill.py:33-36` 硬编码 `CORE_ATOM_KEYS`;`fingerprint.py:29-32` 第二处硬编码;`score_prompt.py:294-297` 第三处硬编码(`--atoms` 缺省时直接内联九项列表)。
  2. `score_prompt.py:291` 的 argparse help 写着 **"默认读门禁常量"**,但代码没有任何读取门禁常量的逻辑,是纯注释谎言。
  3. 门禁 FP003(`validate_skill.py:696`)只比对 validate_skill ↔ fingerprint.py 两处;`score_prompt.py` 的第三处不在任何校验里。
- **影响**:未来按 depth-adaptation.md"新增原子"扩展指南插入一个核心原子时,改完 `CORE_ATOM_KEYS` 两处后门禁照样全绿,但 `score_prompt.py` 继续按旧九位解析 `--depth` 参数——`base_level()` 众数与逐位阈值全部错位,七维评分静默失真。这是"看起来通过、实际坏掉"的最典型脱节。
- **修复建议**:`score_prompt.py` 改为 `import validate_skill`(或用与 FP003 相同的 ast 解析)读取 `CORE_ATOM_KEYS`;或在门禁新增一项 SC 校验,对 score_prompt.py 的 `keys` 默认列表做 ast 比对。同步修正 help 文案。

### P0-2 覆盖调档规则缺失"目标原子已在 D4 顶档"分支,示例被迫规范外即兴处理

- **主张**:"迭代反馈→对应位调档"是全链路宣传的核心机制(SKILL.md 示例3、depth-adaptation 覆盖表第 3 行、iterate D4 段三处引用),但规则集没有定义升档目标已为 D4 时的合法动作,属于"从需求直接跳到结果"的关键环节缺失。
- **证据链**:
  1. `depth-adaptation.md:134-138` 覆盖触发表只写"迭代反馈'XX再严格些'→指纹对应位调档→仅重生成对应模块",无顶档分支。
  2. `complete-examples.md:75-76`(示例3)实际操作:"constraints 已是 D4,确认无升档空间 → **改为对 self-check 施加影响:constraints D4 的合规审查条目扩充**"——既不调指纹位(指纹未变),也不是"重生成对应模块",与三处宣传的机制定义都对不上;该处理路径在任何规范文档中不存在。
  3. 更深一层:指纹未变但内容变了,直接击穿的正是 R07 的设计承诺——`depth-adaptation.md:90` "同哈希的两次组装应产出结构一致的提示词"。同一指纹 `96d5bcd2f545`([3,3,3,3,3,3,3,3,3] 裸串实测哈希)对应了"条目扩充后"与"扩充前"两种产出,哈希失去复现语义。
- **影响**:模型按示例模仿时,遇到"再严格些"反馈会产出一套规范外行为,且优化日志无据可依(日志字段格式在 iterate D4 只定义了"指纹变化+修改点",此场景指纹无变化)。
- **修复建议**:在 depth-adaptation.md 覆盖触发表补一行"目标原子已处档位上限 → 可选:①声明已达上限并给出同档内的加强维度(如条目扩充/阈值收紧),在优化日志记录'位不变-内容增强';②改调关联原子上浮并说明理由",并在 iterate.md D4 段同步该日志格式。

---

## 二、P1 级(跨文档链路脱节,升级残留导致口径互相矛盾)

### P1-1 组装流程步数:同一文件自相矛盾,且四处引用两个版本

- **主张**:组装流程到底是 7 步还是 8 步,全链路没有统一。
- **证据链**:v5.2 变更记录(`changelog.md:39`)明确"7 步 → **8 步**(新增第 7 步模型适配)"。现状:
  - `composition-manifest.md:5`(目录)写"组装流程(8 步)",同文件 `:17`(正文标题)却仍是"## 组装流程(7 步)",而正文实际列出 8 项(:19-29);
  - `SKILL.md:33` 说"八步流程";`routing-protocol.md:88` 说"按组装流程 7 步执行";`usage-guide.md:14` 说"七步组装"。
- **影响**:门禁无 MF 项校验步骤数与标题一致(只查"组装流程"字样存在,MF002),故长期无人发现。执行方读不同文档得到不同流程契约。
- **修复**:manifest 正文标题改 8 步;routing-protocol、usage-guide、SKILL.md 三处统一。

### P1-2 SKILL.md 七维表引用"manifest 第 7 步",实际指向错误步骤

- **证据链**:`SKILL.md:40` "原子映射见 manifest 第 7 步"。`composition-manifest.md:28` 第 7 步 = 模型适配(与七维核对无关);`manifest:29` 第 8 步才是"门禁自检:…对照 SKILL.md 七维表'对应原子'列确认每维均有原子支撑"。此错位正是 P1-1 的 7→8 步升级的连带伤害:`changelog.md:68`(v5.0.1 T13)登记时第 7 步确是自检,v5.2 插入模型适配后自检顺延为第 8 步,SKILL.md 引用未随动。
- **影响**:按引用跳转的读者会读到错误章节;双向引用环断裂。
- **修复**:改"第 8 步";并在 P1-1 修复后约定引用一律用步骤名而非序号,防再次漂移。

### P1-3 usage-guide 整体停留在 v5.3 之前:五步判定、9 类校验、目录树缺一半

- **证据链**(`usage-guide.md`,自称"README 等价物"):
  - `:9-15` "五步路由速查",无第零步/能力边界预判/路由 D/C1-C5——v5.4 已改六步(`changelog.md:16`),且 `:13` 基调映射漏写 B1 的"产出短小"路由分流条件;
  - `:26` "契约门禁(9 类校验)"——脚本头注释(`validate_skill.py:6-11`)已列 13+ 类(另有 IR/PK/RG/MA/TB/BN/FP/QL 等);
  - `:24-37` 目录树缺 `benchmark/`、`registry/`、`model-adapters/`、`quality-metrics.md`、`prompt-ir.md`、`prompt-package.md`,与 SKILL.md 资源索引(:68-88)严重不一致。
- **影响**:SKILL.md 资源索引(:76)明确引导"首次接入本 Skill"读 usage-guide,新接入者拿到的是过期三代的地图。
- **修复**:重写 usage-guide 为当前版本;门禁可增一项检查 usage-guide 目录树条目与磁盘实际文件的差集(可选)。

### P1-4 SKILL.md 示例3 指向的"完整过程"在 complete-examples.md 中不存在

- **证据链**:`SKILL.md:66` 示例3="对示例2产出反馈'约束再严格些'→…完整过程见 complete-examples.md"。但 `complete-examples.md` 示例3(:53-78)的任务是**秒杀系统设计(B4)**,与示例2(市场调研,B3)无关;市场调研报告的调档迭代过程在整个仓库中没有任何文档展示。
- **影响**:入口文档承诺的回链落空;且见 P0-2,即便想参照示例3学习"约束再严格些"的调档,其操作本身就是规范外路径。
- **修复**:或改 SKILL.md 示例3 的任务主体与 complete-examples 示例3 对齐(秒杀+已是 D4 的场景,顺势演示 P0-2 补的顶档规则),或在 complete-examples 增补"示例2 调档"真过程。

### P1-5 R10 第零步与主示例/基线脱节:需实时数据的需求全部绕过边界预判直接组装

- **证据链**:`routing-protocol.md:19-29` 规定第零步**在任何计分之前**执行,C1 判定信号含"今天/当前/最新…要求引用模型训练截止后的事实"(`:140`),执行约束明确"禁止对 C1 直接产出'看似满足需求'的内容"(`:178`)。而三个标志性输入:"**2026**年国内新能源汽车市场调研"(`SKILL.md:65` 示例2、`complete-examples.md:33` 示例2、`cases.yaml:73` case-07)必然要求训练截止后的市场数据,判定过程(`complete-examples.md:35-39`)却直接从复杂度计分开始,无第零步痕迹;case-03 的"**Python入门课**简介"等则不受影响。5 组 model-samples 同样基于 case-07 语义载荷。
- **影响**:框架门面示例违反自己最新加入的门面规则,读者会学到"2026 调研报告 → 直接组装 B3"这一被 R10 明令禁止的路径;回归基线的 12 条用例头部也没有"第零步:未命中 C1-C5"的判定记录(`cases.yaml` 字段集中无此字段)。
- **修复**:三种之一——①示例/基线输入去掉未来年份;②在判定过程中显式补一行"第零步:命中 C1 → 选 A 降级(产出数据获取清单+分析框架,实时数据由用户填入)→ 重新走第零步未命中 → 计分 B3",把降级路径走全;③cases.yaml 增加 `boundary_precheck: none|C1→A` 字段并由门禁 RB 校验。推荐②+③,还能顺带成为路由 D 唯一的端到端示例。

### P1-6 @lang 后缀:语法已定义、解析已支持,全链路零消费者,并与主文档约束冲突

- **证据链**:`depth-adaptation.md:72` 定义 `@lang=zh/en/bilingual`,省略时默认 zh;`fingerprint.py:35-39` 解析并校验该键。但检索全库,`@lang` 除"定义/解析/提论"外没有任何**执行环节**:`composition-manifest.md` 八步流程无语言处理步骤,5 个 model-adapters 的"结构偏好/注入模块"全部只有中文形态、无 en/bilingual 映射(`prompt-ir.md:37` 把它归入 `meta.suffixes` 可选字段,同样无渲染规则);而 `SKILL.md:95` 注意事项规定"产出提示词内部标点统一使用中文标点,禁止中英混排"——与 `@lang=en` 的输出诉求直接冲突,无任何冲突消解条款。
- **影响**:用户写 `@lang=en` 会被 parse 接受、进哈希、门禁全绿,但没有任何文档告诉执行者该做什么——产出语言实际仍由基座原子(全中文)决定。三键后缀有一键是空接口。
- **修复**:要么补一节"@lang 处理规则"(含与中文标点条款的优先级),要么把 `@lang` 从语法中移除并保留 parse 兼容告警;门禁可加一项 LP 校验:`@lang` 若存在,必须能找到含"语言/标点"的处理章节。

### P1-7 迭代调档必经的 diff 工具没有挂进调档真相源(iterate 原子)

- **证据链**:`SKILL.md:37` 路由第 6 步"迭代调档时先用 `scripts/fingerprint.py diff` 评估影响面"。但调档行为的原子级唯一真相源 `references/atoms/core/iterate.md` 全文(48 行,已核)没有任何 diff/fingerprint.py 字样;D4 段(:33-37)只说"输出 DEPTH 指纹与档位说明…仅重生成对应模块"。依赖链:组装产物注入的是 iterate 原子内容,终端模型执行迭代时只会看到 iterate 段文字,不会看到 SKILL.md 的路由速查——diff 这一步在进入实际提示词后丢失。
- **影响**:框架核心卖点"先 diff 再重生成、不全量重出"在产出层没有承载体;只有读 SKILL.md 路由的人(即组装时)知道 diff,使用产出的模型不知道。
- **修复**:iterate.md D3/D4 段补一行"调档前先按 depth-adaptation.md'指纹 diff'节评估影响面";或在路由协议第六步说明该信息须随产出注入。

### P1-8 assets/ 目录整体游离于治理之外:无关方案文档 + 内部记忆 + 真实生成脚本被埋

- **证据链**:
  1. 门禁盲区原理:`validate_skill.py:862-871` DH005 只对**顶层文件**查白名单,`assets` 是目录 → 整目录内容不校验;`TMP_PATTERNS`(`:50`)无隐藏目录穿透,`assets\.workbuddy\`(8 个文件,实测存在)不受影响——上一轮审计自己也把报告写在了这里。
  2. `assets/api-docs-auto-generation.md`(10KB)+ `generate-api-docs.py`(9.6KB)是"API 文档自动生成"技术方案,与提示词工程主题无关,零引用(`SKILL.md` 与全部 references/scripts 检索 "assets" 无命中)。
  3. `references/registry/atom-registry.yaml:1` 头部注释称"由 **scripts 下**生成脚本从 atoms/ 目录实证生成",实测 `scripts/` 目录只有 4 个 py(已核),**registry 声称的生成器 scripts/gen_registry.py 不存在**;真实文件躺在 `assets/.workbuddy/gen_registry.py`(已核)。注册中心声称的再生成链路断裂,跨 Skill 复用场景(atom-registry 的存在意义)无法按声称方式重建。
- **影响**:交付包里混有内部工作记忆(`assets\.workbuddy\memory\*.md`)与两套无关文档;"注册中心=脚本实证生成"的声明不成立。
- **修复**:①把 gen_registry.py 移入 `scripts/`(修正 registry 头部声明的链路);②api-docs 两件移出本 Skill 仓库或明确归档目录;③`.workbuddy` 记忆/审计中间产物移出交付目录;④门禁 DH 类补"顶层目录白名单"校验(目录也要进 WHITELIST_TOP,白名单里的 `TODO.md` 实际不在顶层,属死条目,顺带清理)。

---

## 三、P2 级(声明-实现轻微不一致、伪校验、注释错误)

### P2-1 裸指纹与 @lang=zh 的哈希等价性:文档承诺与实现相反

- **证据链**:`depth-adaptation.md:80` "省略全部后缀的裸指纹…与 `... @lang=zh` **等价(默认值不产生新哈希)**"。实测(本机复跑):`hash "DEPTH: [3×9]"` → `96d5bcd2f545`,规范串 `[3,3,3,3,3,3,3,3,3]`;`hash "... @lang=zh"` → `723b2294e54c`,规范串 `[3,...]|lang=zh`。`fingerprint.py:125-132` `canonical()` 只对 `tokens` 做排除,未对默认值归一——两哈希不同,文档声明失效。
- **影响**:缓存命中判定会因写不写 `@lang=zh` 分裂为两个键,与"默认值不产生新哈希"承诺相反。
- **修复**:`canonical()` 对 `lang==zh` 视同缺省排除(或文档改口);补一条正反单测。

### P2-2 FP-HASH 规范无产出落点,承诺字段成死链

- **证据链**:`depth-adaptation.md:87` 规定哈希"写作 `FP-HASH: <12 位>`"、`:90` "哈希写入产出的优化日志,用于追溯"。全库检索 `FP-HASH`(`:8` 命中)仅存在于规范/变更记录/门禁存在性检查(`validate_skill.py:714` 只查 depth-adaptation.md 文档里有这个名词);12 份快照与 5 份 model-samples 头部只有 `DEPTH:` 行,无一携带 FP-HASH。
- **修复**:快照/示例头部补 FP-HASH 行,或规范将 FP-HASH 降级为"可选追溯字段";门禁若要求产出级哈希,应校验 snapshots 而不只是校验协议文档。

### P2-3 ATOM 契约块 `deps` 字段是无人消费的死接口

- **证据链**:28 个原子头部均声明 `deps: none`(实测枚举);全库无任何文档解释 deps 语义、无任何校验读取它;原子间真实耦合知识只活在 depth-adaptation.md 的 R1-R5。若未来新增原子的 deps 与其参与规则不符,没有任何机制会发现。
- **修复**:定义 deps 语义(建议:声明该原子参与哪些 R 规则,如 `deps: R1,R2`)并让门禁与 DEPENDENCY_RULES 反查一致;或从契约块中删除该字段,减少假接口。

### P2-4 changelog 登记的 MF014 在门禁中不存在

- **证据链**:`changelog.md:58`(v5.0.1 T03)"新增 MF010-MF014(…信号词弱比对)"。实测 `validate_skill.py` 全文无 "MF014"(检索 False),MF 系列实际为 MF001-003、MF010-013、MF015。"信号词判定表与原子内'适用判定信号'弱比对"这一层校验从未存在——当前 manifest 域表信号与 legal.md:30 等原子内声明的信号是**两份独立维护的文本**,可以漂移(门禁 MF010-013 只查原子名双向存在,不查信号内容)。
- **修复**:要么补实现 MF014 弱比对,要么 changelog 加勘误;至少在 manifest 加一句"信号词以判定表为准,原子内'适用判定信号'节为辅助描述"。

### P2-5 门禁条目号跨文档互相指错(引用漂移)

- **证据链**:`fingerprint.py:19` 注释"位序…由门禁 **FP005** 校验"→实际位序校验是 FP003(`validate_skill.py:696`),FP005 是后缀键校验(`:712`);`depth-adaptation.md:78` "合法后缀键…(门禁 **FP003** / 脚本 parse)"→实际键合法性由 FP004/FP005/FP007 族负责。同类:`quality-metrics.md:5` 说门禁校验为"QL001-QL007",脚本实有 QL008(`:543`);`quality-metrics.md:64` 说"门禁对 QL 系列只报 warning",实际 QL001/002/004-007 为 error。`depth-adaptation.md:31-32` 说"门禁 TB001 只校验表结构完整性,不校验数值",实际 TB004(`:567`)对数值做一致性比对(虽为 warning)。
- **影响**:维护者按引用找错校验点;上一轮 changelog(`:21`)已自省"第三次踩存在性检查过宽的坑",本次发现的是另一种坑——引用编号坑。
- **修复**:全文档统一以脚本为准订正编号;建议门禁 findings 输出时附带条目号定义行号,方便对账。

### P2-6 门禁自测 test_confirmed_without_snapshot_blocked 是伪反例

- **证据链**:`test_validate_skill.py` 该用例先 `replace("confirmed: false", "confirmed: true", 1)`——但 cases.yaml 现状 12 条全部 `confirmed: true`(实测),replace 命中 0 处、空操作;用例实际只验证了"删除全部快照→RB007"路径,RB003("未确认但有快照")分支从未被反例覆盖。
- **修复**:改为构造 `confirmed: true` + 删单条快照、并另加"`confirmed: false` + 有快照 → RB003"用例,替换语义写明断言目标。

### P2-7 depth-adaptation 目录与概览未覆盖后期新增章节

- **证据链**:`depth-adaptation.md:3-9` 目录列 5 项,正文实际含"档位 Token 基线(R04)""指纹后缀与哈希(R02/R07)""LITE 骨架豁免声明"等 v5.1+ 新章节;`:13` 概览仍写"三要素",与新增内容不符。轻,但同属"改文不改目"的升级残留模式。
- **修复**:补目录、概览改为"多要素"并列举当前协议覆盖。

---

## 四、验证过、确认无问题的链路(排除误报)

- 位序三方一致:`CORE_ATOM_KEYS`(validate_skill:33)= fingerprint.py:29 = depth-adaptation.md:53-54 位序表 = manifest 第 6 步组装顺序,门禁 DP007/FP003 双向锁死。
- 依赖规则五方一致:depth-adaptation R1-R5 表 = fingerprint.py `DEPENDENCY_RULES` = complete-examples 示例3 求值文字 = 12 份快照全为 [n×9] 全档位(恒满足 R1-R5,已逐条求值) = 5 份 model-samples 同。
- cases.yaml 12 条指纹与 snapshots/model-samples 头部逐条比对一致;`fingerprint_slots: 9` 与原子数一致;confirmed↔快照双向自洽(RB007 语义)。
- QL001-QL008 阈值表与 score_prompt.py METRICS 常量逐格一致(文档 "-" ↔ 脚本缺档位键的 skip 语义一致)。
- 七维表权重合计 100%,每维"对应原子"列在 CORE_ATOM_KEYS 内。
- atom-registry 28 条与 atoms/ 目录 28 文件双向一致、type 归属正确(RG 语义复跑通过)。
- 域/输出判定表信号词与原子内"适用判定信号"抽查(legal/consulting/hr/education)当前语义一致——但注意 P2-4:这是巧合性一致,无机制保障。
- manifest 域表"歧义处理:命中多个域原子时全部注入(不超过 2 个)"与 `prompt-ir.md:47` "≤2 个"一致。
- FM 版本三处(5.5.0 / 标题 v5.5 / 派生输出)一致;LITE-2/3/4 死锚已清(LT005 通过)。

## 五、汇总

| 级别 | 数量 | 编号 |
|------|------|------|
| P0 | 2 | P0-1 位序第三处硬编码脱保 / P0-2 顶档调档分支缺失致示例规范外 |
| P1 | 8 | P1-1~P1-8(步数、交叉引用、usage-guide 过期、示例回链落空、第零步与示例脱节、@lang 空接口、diff 未挂原子、assets 治理盲区) |
| P2 | 7 | P2-1~P2-7(哈希等价性失效、FP-HASH 死链、deps 死接口、MF014 幻影、条目号漂移、伪反例、目录滞后) |

**共性根因**:本项目的错误都是"升级时新增一层、旧层引用不随动"的单向棘轮——v5.2 加步骤不修引用、v5.4 加第零步不修示例、v5.1 加哈希不修产出、v5.3 加后缀键不修消费者。建议建立一条通则:**任何"数量性/编号性/引用性"表述(第 N 步、X 维、N 类、编号 XXnnn)只允许出现在一个真相源文档,其余位置用语义名引用**;并把本报告 P0/P1 各项转化为门禁新校验(FP 族扩到 score_prompt、新增目录级 DH、RB 增 boundary_precheck 字段)后,再进入 v5.6 迭代。
