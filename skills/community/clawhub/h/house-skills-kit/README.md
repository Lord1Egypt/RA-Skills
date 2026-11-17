# house-skills-kit 🏠

**房产 AI 技能仓库 —— 按身份分 Skill，按需取用。**

为房地产行业的七类角色提供开箱即用的 AI 技能（Skill）：房开企业、经纪公司、渠道分销公司、购房者/业主、二手经纪人、一手销售人员、房产自媒体博主。每个身份场景对应一个独立 Skill，`skills/` 目录下各技能均含完整提示词与配套工具，可单独安装、单独发布。

> 🇨🇳 模板通用、零外部依赖（纯 Python 标准库）：不绑定任何平台与数据商，装进 Claude / 其他 Agent 均可。

## 已发布技能

### 🧮 calc-toolkit · 公共计算工具包（全身份通用）

一套覆盖房产交易核心测算场景的命令行工具，**全部身份共用**。

| 编号 | 工具 | 命令 | 说明 |
|---|---|---|---|
| ⑦-1 | 房贷月供 | `mortgage.py` | 商贷/公积金/组合贷 × 等额本息/本金，按城市利率档自动取数 |
| ⑦-2 | 二手房全成本 | `tax.py` | 契税/增值税/个税 + 中介/评估/担保等 6 项费用，买卖双方分账 |
| ⑦-3 | 提前还款 | `prepay.py` | 缩期 vs 减月供双方案对比，违约金/最低额提示，省息一目了然 |
| ⑦-5 | 购房能力 | `capacity.py` | 收入负债 → 可贷上限 → 可买总价，银行双线口径（月供收入比 × 首付成数），瓶颈诊断 |
| ⑦-6 | 一手房成本 | `newhome.py` | 契税/维修基金（按城市×物业类型）/首年物业/登记工本费，按功能分类出单 |
| ⑥ | 首套二套认定 | `status.py` | 商贷/公积金/契税三口径分判（认房不认贷），卖一买一，联动下游工具参数 |
| ⑦-15 | 楼层差价折扣 | `floor.py` | 楼层修正 × 营销折上折，防"先涨后折"真伪校验 |
| ⑦-16 | 公积金额度 | `fund.py` | 四限取最低：上限/房价成数/还贷能力/余额倍数×缴存时间系数，多子女/绿建/人才上浮，组合贷缺口提示 |
| ⑦-17 | 佣金提成试算 | `commission.py` | 二手中介费买卖分账+折扣；渠道阶梯双算法对账（全额跳档vs分段累进）；返佣+团队分佣 |
| ⑦-18 | 得房率换算 | `efficiency.py` | 建面↔套内↔公摊↔使用面积链，单价双向换算，双盘套内口径比价（防"建面便宜"幻觉） |
| ⑦-19 | 租金回报率 | `rent.py` | 租售比/毛净回报率/回收年限+五档坐标（存款/50城均值/回本线/价值线/以租养贷），目标反推 |

**35 城规则库**（北上广深 + 强二线 + 昆明等省会全覆盖）+ **四层规则引擎**：

```
全国默认档 → 城市档（如昆明高层维修基金90元/㎡）→ 区县档 → 我的模板档（使用者自建）
```

- 每个数字可追溯：输出带「参数来源」，规则档标注文号/口径（如"2024年契税16号公告：140㎡线"）
- 政策数据与代码分离：政策变了改 `rules/cities.yaml`，工具不用动
- 万能覆盖：任何参数均可 `--set 键=值` 即时改（如 `--set dti=0.55`）

**快速上手**（零安装，Python 3.8+ 直接跑）：

```bash
git clone https://github.com/danfeistar/house-skills-kit.git
cd house-skills-kit

python3 skills/calc-toolkit/mortgage.py --price 1500000 --downpay 30 --years 30 --city 昆明
python3 skills/calc-toolkit/capacity.py --income 8000,6000 --cash 400000 --debts 2000 --city 昆明
python3 skills/calc-toolkit/tax.py --price 1500000 --area 89 --city 昆明 --first 1 --held 6 --unique 1
python3 skills/calc-toolkit/prepay.py --loan 1000000 --rate 3.1 --years 30 --paid 24 --prepay 200000
```

## 🏢 案场销售线技能（一手销售/案场团队）

| 技能 | 内容 | 适合谁 |
|---|---|---|
| [sales-talk-library 案场话术库](skills/sales-talk-library/) | 地段/配套/户型/竞品/品牌五域 24 个话术块：标准说辞 + 分客群变通 + 翻车警示，合规红线内嵌 | 置业顾问、销售经理、案场培训 |
| [sales-objection-handling 客户异议处理](skills/sales-objection-handling/) | "太贵了/再看看/怕烂尾/会不会降价"四大高频异议：顾虑分支拆解→应对话术→禁语清单，附 6 条二级异议 | 置业顾问、销售经理 |
| [sales-closing-sop 算价与逼定 SOP](skills/sales-closing-sop/) | 算价五要素→让步梯度→购买信号判读→五级逼定→成交收口，含红白脸与审批链团队配合 | 置业顾问、销售主管/经理 |
| [sales-reception-sop 接待与需求挖掘 SOP](skills/sales-reception-sop/) | 首访动线（品牌→区域→项目→户型）+ 七维需求提问树 + 客户画像复述 + 带看匹配与交接 | 置业顾问、销售主管、案场负责人 |
| [sales-lead-grading 判客与跟进 SOP](skills/sales-lead-grading/) | ABC判客分级四维标准 + 分级跟进节奏 + 掉客三层挽回 + 复判升级与归属仲裁 | 置业顾问、销售主管、案场负责人 |
| [sales-mortgage-sop 按揭问题应对 SOP](skills/sales-mortgage-sop/) | 贷款口径统一 + 资质预判分流 + 六类高频问题（流水/征信/首付缺口/首付来源/收入形态/公积金）路径与话术 + 批贷进度跟进 + 合规红线汇总 | 置业顾问、按揭专员、销售主管 |
| [sales-opening-sop 开盘执行 SOP](skills/sales-opening-sop/) | 盘前客户梳理与预登记 + 认筹转认购 + 开盘日七环节选房动线 + 选房规则口径表 + 五类应急预案 + 盘后转化与复盘 | 置业顾问、案场负责人、开盘执行团队 |
| [presale-marketing-sop 蓄客期营销动作清单](skills/presale-marketing-sop/) | 节点倒排四阶段节奏 + 暖场/拓客/圈层/认筹预热动作库 + 自媒体蓄客专节（项目号定位/内容日历/线索承接闭环）+ 四级漏斗与费效复盘 + 合规红线 | 策划、营销负责人、自媒体运营、拓客团队 |
| [competitive-intel-sop 竞品踩盘与市场监控](skills/competitive-intel-sop/) | 竞品A/B/C分级与踩盘频次 + 现场六模块采集清单（价值主张/展示面/销售力/价格/销控/服务）+ 百分制打分表与竞品预判 + 供应成交去化价格四指标周监控（三源交叉）+ 月度竞品报告模板 + 反踩盘纪律与合规红线 | 策划、营销负责人、市调岗、置业顾问 |

> 数字类话术（月供/得房率/楼间距等）与 [calc-toolkit](skills/calc-toolkit/) 联动计算，不口算。

## 技能路线图（按身份扩容）

| 身份 | Skill | 状态 |
|---|---|---|
| 全身份通用 | `calc-toolkit` 公共计算工具包 | ✅ 已发布（19 件工具收官） |
| 一手销售/案场 | `sales-talk-library` / `sales-objection-handling` / `sales-closing-sop` / `sales-reception-sop` / `sales-lead-grading` 案场销售线五技能 | ✅ 已发布（L1 主干 7/7 完成） |
| 购房客户 | C端购房顾问（资格/选筹/谈判） | 排期 |
| 房开案场 | 案场销售顾问 | 排期 |
| 一手销售 | 置业顾问跟客助手（含判客/话术） | 排期 |
| 二手经纪人 | 经纪人作业助手 | 排期 |
| 渠道分销 | 渠道管理助手 | 排期 |
| 房产自媒体 | 内容创作助手 | 排期 |

## 两条生产线

1. **`skills/` 直发技能**：每个子目录独立 SKILL.md，发布到 ClawHub 各自成技能，可独立安装。
2. **`template/` 品牌生成骨架**：4 类角色原型（购房者/房开销售/经纪经纪人/渠道分销）× 29 业务模块，一份品牌配置即可生成专属顾问技能：

```bash
python3 render.py --config examples/kunming/kunming.buy.yaml --out output/my-brand/
```

## 分发渠道

| 平台 | 链接 |
|---|---|
| GitHub 主库 | [github.com/danfeistar/house-skills-kit](https://github.com/danfeistar/house-skills-kit) |
| Gitee 镜像 | [gitee.com/danfeistar/house-skills-kit](https://gitee.com/danfeistar/house-skills-kit) |
| AtomGit 镜像 | [atomgit.com/danfeistar/house-skills-kit](https://atomgit.com/danfeistar/house-skills-kit) |
| ClawHub 技能市场 | [clawhub.ai/skills/house-skills-kit](https://clawhub.ai/skills/house-skills-kit) |

## 👤 作者

**老何** — 地产行业从业 17 年，历任多家房企云南营销负责人，长期深耕云南及昆明市场，早期 AI 使用者与运用者。现全力建设「房产 AI 平台」（房企端 + 经纪公司端 + 销售人员端 + 买房客户端）。

**为什么做这个仓库**：作者在国内外公开渠道（GitHub / ClawHub / 各大 AI 应用市场）均未找到专注中国房地产的 AI Skill 工具库——市面上的 Skill 生态几乎空白于这个年交易额十万亿级的行业。既然没有，就来做**最早、最专业的中文房产 AI Skill 与工具库**：把一线地产人的业务知识，做成 AI 真正能用的技能。

**本仓库的差异化**：这里的业务模块（判客规则 / 佣金政策 / 案场话术 / 验房清单 / 城市税费档…）全部来自一线业务实践和企业规范化工作场景，不是工程师想象出来的 prompt。AI 懂技术，我们懂房产——两者结合才是行业真正能用的 AI 工作流。

> 💡 **免费开源，长期维护**。如果它对你的工作有帮助，欢迎 Star / Issue / 转发——每一次使用和反馈都是对"房产 AI 开源"路线的支持。
>
> 🤝 **业务合作**：需要为你的房企 / 经纪公司 / 销售团队定制 AI 工具与 AI 工作流？欢迎通过 [GitHub 主页](https://github.com/danfeistar) 联系作者——一线地产 17 年 × AI 工程化落地，帮你把 AI 真正用进业务。

## License

Apache-2.0
