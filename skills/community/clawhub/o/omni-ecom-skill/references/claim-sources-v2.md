# 数字索引的原文件复算（候选功能）

报告生成前读取本次数字索引 `claim-ledger.json` 所在目录内的授权来源副本。当前索引必须使用 `omni-ecom.claim-ledger@2.0`，并记录 `created_by_team_version`；报告生成器核对该版本与报告专家团版本一致。`build_report_package.py` 默认调用来源复算，`claim_guard.py` 默认也执行复算；不是只检查文件名和指纹格式。不要为满足规则自行制造或改写原始数据。

旧 `schema_version=1.0` 索引只能通过 `legacy_migration.py` 复制为只读历史记录：保留原字节和历史数字，但不取得 current_numeric_evidence，也不继承执行权限。不能只改 schema_version 或补几个身份字段后当作 2.0 当前证据；必须从本次授权来源重新生成、复算并核对范围。

数字索引必须放在本次报告目录内，可使用 inputs/claims.json 等子目录。报告 claim_ledger.file 保留相对路径；来源相对该索引目录解析。生成器不会自动复制目录外的文件，先按本次已授权范围准备只读副本，不扩大读取范围。

## 原表定位

`source_ref` 保留 source_id、source_file、field、source_sha256。source_file 相对索引目录，不得越界；实际字节必须符合指纹。

- CSV、XLSX、XLS：range 明确单列 A1 坐标，如 A2 或 A2:A3；field 必须与所选列真实表头一致且不重名。header_row 默认为 1，表头偏移时显式指定。Excel 必须指定实际 sheet；不把未缓存的公式或空白转为 0。CSV 默认 UTF-8，可明确 encoding。
- 多行必须明确 aggregation 为 sum 或 mean，不猜测用户要合计还是平均。单格默认 value。
- JSON：使用显式 pointer，如 /campaigns/0/spend；不读取负索引或猜测字段路径。
- 声明值必须与原值/聚合结果一致。单位转换、去重人数、跨期间对齐、客户与来源真实性仍需要相应业务口径和来源取得检查，不能靠此程序单独确认。

## 推导与缺数

### 原表范围核对

source_ref.contexts 可将期间、单位、平台、店铺、已声明币种和 dimensions 中的细分绑定到同一原表的实际内容。传了 contexts 就必须覆盖全部已声明项目，不能仅核对期间后声称其他范围也通过。新候选任务按 source_context_policy=required 准备索引，平台与店铺须明确；任一 verified 来源缺少 contexts 时阻断。旧索引默认 legacy_unbound，仅供兼容读取，凭证明确记录 source_context_unbound 和核验数量，不能作为完整范围验收。

- CSV/Excel 同行信息：例如 `"store":{"column":"D","field":"店铺"}`，逐行核对数值 range 涉及的全部行，检查实际表头且禁止同名歧义。
- CSV/Excel 页头信息：例如 `"period":{"cell":"B1","label_cell":"A1","field":"报告期"}`；值与标签必须来自表头之前的不同单元格，标签真实匹配。不能拿某个数据行冒充全表范围。
- JSON：例如 `"store":{"field":"store"}`，只读取数值 pointer 所在记录的同级字段，不允许另指定其他记录的路径。
- 期间默认 exact，必须是可解析的实际日期范围；“本期”之类标签不算证据。日记录归入周/月/自定义区间时须显式 period_mode=contained，并同时声明 period_coverage.frequency=daily、status=complete_no_missing_dates；程序要求报告范围内每个自然日恰好出现一次，少日、重复日、区间行冒充日记录或范围外日期均阻断。

核对前后都检查原文件指纹，单位不同不自动换算，平台/店铺名称不同不擅自映射。报告来源复核再将已核验的索引范围与报告范围对比，禁止原表核验一家店、报告却改标另一家；scope 内的细分也参与展示指标匹配，不能丢弃后借给全店指标。原表标签与实际取得权限/真实性是两层证据，不能混为一谈。

候选版 completion_gate 已在代码内强制原表范围核对，不接受报告版本号、单点模式或 legacy_unbound 开关降级。所有 verified 原始来源都须实际核对平台、店铺、期间、单位及已声明细分；仅有 unknown 的空核验不能发正式数字交付完成凭证。完全没有可分析输入时，必须使用 `scripts/intake_blocked.py` 生成不带报告的 `intake_blocked_no_input` 终态；存在文件但质量不足时，只能生成 `task_type=data_quality_audit` 的数据质量报告，并继续接受来源、范围、PDF、复核和完成闸门检查，不能冒充经营分析完成。

旧索引先按 [旧版迁移说明](legacy-migration-v2.md) 只读归档，再用 `legacy_claim_revalidation.py` 选择真实原导出和逐 Claim 范围位置，生成新的候选索引。程序核对旧 SHA、重新读取数值及原表范围标签，并明确外部范围确认不等于平台真实性认证。随后对新索引运行 `python scripts/claim_guard.py --claims <索引路径> --require-context --output <新检查凭证路径>`；不要将输出路径指向输入。原表没有平台店铺等标签时请用户重新导出，不往原表补造标签。索引变化后重新生成报告和 PDF、冻结并独立复核，旧批准不能沿用。

### 正文与行动数字绑定

事实、判断、假设和行动的经营数字也不能绕过数字索引。含金额、比例、倍数、人数、订单、件数或普通经营数值的字段，按出现次序填写 number_bindings：field 是字段名（列表项写成 counter_conditions[0]），token 保留正文中的原字符串，occurrence 是该字段内同一检查序列的第几次出现。

- 已发生事实或当前/历史数值使用 kind=claim 和 claim_id；系统核对编号存在、状态已核验/已推导、数值和单位一致。`1万元` 可与 `10000元` 对应，百分号和倍数不隐式互换。
- 目标、阈值、试验预算或样本量可用 kind=proposal，但只能出现在假设、行动或判断的反证条件中；同时提供 label、非空 basis_claim_ids 和 rationale。事实、行动 baseline 不能用“建议值”伪装已有事实。
- 行动中的金额、比例或倍数目标必须 approval_required=true，且不能写成 not_required。它只是“待验证/待审批建议”，不是平台已执行或结果承诺。

生成的 Markdown/PDF 明示“数字依据”或“待验证目标”。报告质量检查重新扫描结构化正文；漏绑定、错编号、错值、错单位、重复/多余绑定均阻断。日期、版本、报告编号、T+2 和“观察 7 天”这类时间安排不当作经营数据。当前扫描覆盖结构化报告字段；任意新自由文本章节和图片内文字尚需在完整报告流水线验收中继续核对。

根 period 仍是本次报告期。确需同时引用历史或报告内分期时，在索引根部明确 additional_periods 列表，各条目仍填写自己的实际期间；不能把历史值改标成本期。普通 derived 输入须与该推导条目同期间，跨期变化由明确期间的分组比较和裁决机制处理，不能把不同期间的花费和成交拼成一个投产比。

derived 的 inputs 引用真实 claim_id，允许前向引用；默认按输入指标名绑定公式变量。重名时必须明确 formula.bindings，不能循环依赖、漏用输入、把 unknown 当 0。常见比率实际表达式必须为声明的分子除以分母，不能用常数与零乘法拼出虚假投产比。

计算采用十进制，不默认放宽误差。确需显示舍入时，在条目写 decimal_places（0 至 12），按四舍五入复核。unknown 保持 null 并标记未复算。

数字检查和指标裁决共用 metric_semantics 的标准比率定义：转化率为 buyers/visitors，客单价为 gmv/buyers，访客价值为 gmv/visitors，金额退款率为 refund_amount/gmv，ROAS 为 attributed_gmv/ad_spend，利润 ROI 为 profit/total_cost。orders/visitors 只能明确命名为 orders_per_visitor（单/人），不能叫买家转化率。后台原字段即便叫 ROI，也须保留原字段名并按真实定义归类，不能直接把销售投产比叫利润回报。

上述标准比率必须由两个对应的已知输入复算，单位须匹配；原始后台比率可留作对账，但不能用 verified 状态冒充已按标准口径复算的比率。公式变量须实际绑定对应输入，分母必须大于零；除利润 ROI 和明确的广告前贡献 ROAS 可为负外，分子不能为负；买家数不得大于同口径访客数。% 单位须在公式明确写 `(分子 / 分母) * 100`（或 100 乘该比率），ratio 不隐式乘百。任一条目声明 currency 时，推导及两个输入必须声明同一币种；不自动换汇。

利润 ROI 必须另外提供 accounting，不能只写 cost_complete=true。当前明确支持 method=net_operating_profit_over_operating_cost，即本期间净经营利润除以经营成本，不把它当成所有投资回报定义。scope_note 说明本次收入确认、退回和成本范围；revenue_claim 引用 recognized_revenue（本期已确认、扣本次退回前收入），refund_claim 引用 revenue_refund（与该收入对应的退回），不能不加判断地拿 GMV 或跨期售后退款替代。

accounting.costs 分别引用 product_cost、ad_spend、platform_fee、fulfillment_cost、inventory_loss、tax_cost、other_operating_cost 七类金额的 claim_id。每类须有实际来源，明确为零也要读取原表；一类包含多项可用已复算的 derived 汇总。accounting.perimeter 还要给出范围编号、权责发生/现金/平台结算基础、已关账状态、来源系统、导出记录号和导出时间，并明确标为“来源已绑定但未经独立真实性认证”；程序不得把本地文件哈希冒充财务真实性审计。七类成本逐项声明 direct_source、explicit_zero 或 allocated，不能省略处理方式。

共享费用使用 allocated 时，必须绑定共享成本池、本范围实际基数、全部范围总基数和分摊表合计；当前成本只能用 `shared_pool * scope_base / total_base` 复算，分摊表合计必须等于成本池。成本池、当前基数和总基数不能引用同一来源单元格，任一缺失或总基数为零即阻断。该检查能防止随手填比例，却仍不独立认证分摊基数的业务合理性；报告须展示分摊依据名称并保留财务复核边界。

利润 ROI 如进入专家分歧裁决，裁决记录只引用本报告数字索引中已复算的 ROI claim_id。系统重读报告索引、原表范围及 accounting 结果，然后用同一 profit/total_cost 表达式复算；不再接受裁决文件自行填写两个数或仅凭 profit_scope/total_cost_scope 文字通过。裁决期间、平台、店铺、细分和币种必须与基线范围一致；总范围声明的细分与币种会被所有财务组件继承，不能由某条组件改写。

复算要求成本之和=total_cost，收入−对应退回−成本=profit；所有分项与利润比率的客户、期间、平台店铺、细分和币种须一致。来源明细随数字复算凭证记录，并进入原有来源冻结/复核流程。缺数、错位、重算不符时不能出利润 ROI；net_roi 仍未定义，应先确认具体利润模型，不能只改名称绕过。

扣退款 ROAS 使用两步复算：先产生 derived 的 attributed_net_sales = attributed_gmv − attributed_refund，再算 net_roas = attributed_net_sales / ad_spend。中间净销售额不能直接标 verified 跳过扣减，退款不能拿全店 refund_amount 顶替。公式的 numerator/denominator 对减法分别表示被减数与减数；必须实际执行对应减法，不能用常数拼值。金额单位为元，输出为倍或 ratio；退款须为非负且不超过对应销售额，花费须大于零，缺退款与真实零退款分开处理。

上述五个条目（销售、对应退款、净销售、花费、扣退款 ROAS）的 attribution 必须同时具有一致的 source_id、window、level、refund_basis；refund_basis 明确为 matched_attributed_sales，source_ref.source_id 也须一致。它们可以来自同一归因口径下不同文件，但不能拼接不同店铺/期间/细分/币种。归因声明仍须由真实平台/订单证据支持，程序核对声明一致和本地复算，不独立认证订单匹配。PDF 标注“扣退款 ROAS（非利润）”，凭证记录 profit_checked=false；不能凭其高低直接宣称盈利或批准预算。

所有 ROAS、扣退款 ROAS 和广告前贡献 ROAS 还必须在 attribution 中绑定 acquisition_mode=manual_platform_export、可定位的 export_reference、exported_at、client_scope、platform 和 metric_semantics_version=2.0；authenticity_status 只能是 source_bound_export_not_platform_authenticated。客户或平台错位、导出元数据缺失、指标含义版本缺失，或把手工导出写成“平台已认证”都会阻断。真实连接器回读将在平台验收链另行证明，不能用这些元数据替代。

需要进一步观察投放贡献时，可用 attributed_contribution_before_ad = attributed_net_sales − attributed_discount − attributed_product_cost − attributed_platform_fee − attributed_fulfillment_cost，再计算 contribution_roas = attributed_contribution_before_ad / ad_spend。优惠和四类变动成本都必须有匹配归因来源，全部条目共用 reconciliation_id、window、level、refund_basis=matched_attributed_sales 和 cost_basis=matched_attributed_sales；缺任一项保持未知，不能补零。PDF 显示为“扣匹配变动成本 ROAS（非净利润）”，允许为负，仍不包含库存损失、税费、其他经营成本或未列共享费用，不能替代利润 ROI。

该检查证明的是“声明的经营范围内金额相互勾稽”，不证明收入确认正确、未漏财务项目、原表真实、分摊依据合理或人数已去重。其他利润模型和实际业务的完整成本覆盖仍需进一步验收；不能仅凭程序通过作确定性利润或投放承诺。

`--structure-only` 仅用于老格式检查，生成 claim_structure_passed，不能作为正式数字来源通过凭证。实际通过的 source_checks 标明哪些条目来自原表、哪些来自计算、哪些仍未知。

## 展示指标对应来源

实际构建、PDF 与质量检查调用 report_metric_guard.validate_delivery_metrics，不只检查已裁决数字。metrics 每行中的 metrics/inputs、标准顶层指标，以及无这些容器时展示的顶层数值，都须对应同指标、同期间、同范围/细分的数字索引。唯一匹配可自动对应；多来源时显式写 metric_bindings，例如 `{"gmv":"C-sales"}`。来源状态须为 verified/derived，不能用 unknown 支撑真实 0。自定义指标还须在 metric_units 明确单位，与索引一致。

标准图表金额仍用元、比率用小数比例；索引的 % 值可明确换算后比对，但不允许把原始 20 直接放入小数比率图再绘成 2000%。缺值保留 null，不画成零。底层 validate 仅用于已有裁决的一致性比较，不是正式数值覆盖入口；unmapped_not_checked 不代表正式来源验收通过。

多平台/店铺范围须来自本次授权范围，在 scope.members 声明完整的 platform/store 配对，不能将两个列表任意交叉组合。指标行和索引可以明确平台、店铺及 dimensions（如渠道），未说明的字段继承报告范围；不允许渠道借用全店总数。新字段不构成扩大客户资料读取或平台操作权限。

PDF 按平台、店铺、细分分别生成指标表和业务图，真实日期按先后排序，不改输入原值。支持明确年月日、ISO 周、季度及起止日期；同组重复/重叠期间或无法判定先后的标签不能默认为本期/上期。来源索引同时显示平台、店铺及细分，方便对应各组图表。

## 验收边界

质量检查默认重读报告指定索引，核对 run_id、client_scope、period、原始文件指纹、报告内索引投影、条目数及来源检查结果；综合与单点报告均不能省略。索引和所有被实际读取的来源自动进入质量输入及复核冻结清单。只列一个未读取的来源名称不算通过。

最终完成关再次读取与复算，不信任传入凭证的成功文字；凭证身份、索引指纹、各类数量及 source_checks 必须与实际结果一致，并与本轮质量检查相同。完成写入前复查文件指纹，完成凭证保留来源指纹供恢复时核对。复核后即使改成数值相同的新文件，并同步改写索引与报告，也必须重新冻结和复核；不能沿用旧批准。完成后源文件改变则旧交付不可继续显示为有效完成。

独立 `generate_pdf_report.py` 同样要求同目录 report.md 与数字索引，生成前直接复算，不允许省略来源。PDF 正文逐项显示全部数字编号、值/单位、实际原表定位或推导公式/输入编号、缺数状态及期间，不截断到前几项。页尾明确是待冻结和独立复核候选稿，不能在生成时声称已经冻结。

生成在临时目录中排版与检查，原表或报告在渲染期间改变时不发布新 PDF；排版失败不替换已有 PDF 和凭证。输出文件与图表/页面目录不得覆盖输入。成功凭证含报告、Markdown、索引和实际来源的指纹及复算结果。冻结与完成关要求这些字段匹配当前文件，不能拿旧 PDF 的渲染凭证批准新报告。多文件发布不等于文件系统事务；任何复制/写入错误仍需按失败处理，不能据此宣告交付。

这些检查验证已展示的结构化指标与索引对应、本地来源复算、标准比率定义、PDF 来源快照与冻结绑定，不认证来源取得方式，也不证明所有应有业务分析已经覆盖。自由叙述、行动中的数字、原表维度/期间/单位列、财务完整性及去重人数仍需进一步检查。CSV/XLSX/JSON 已有真实本地合成文件测试；XLS 分支尚缺独立格式测试。全部合成验证都不代替真实平台和双宿主验收。
