---
name: ortho-deal-match
display_name: 骨科供需撮合台
version: 1.1.0
description: 骨科供需撮合台。买方发布需求、卖方发布能力，自动按分类/工艺/材料/资质/市场五维打分撮合，双方都确认意向后才交换联系方式。内置实名登记、反骚扰承诺、配额限速、拒访名单、角色权限分派与哈希链审计；可从骨科展会名录（L1 公开级）导入线索做获客。当用户提到骨科撮合、找代工、发布需求、供需对接、获客、搭接买卖双方时使用。
description_en: Two-sided orthopedic deal matching. Buyers post demands, sellers post capabilities; a five-dimension scorer (category / process / material / certification / market) pairs them, and contact details are exchanged only after BOTH sides confirm. Includes real-name registration, anti-harassment pledge, quotas, do-not-contact list, role-based access with deal assignment, and a hash-chained audit log.
author: 注册老炮
license: MIT
category: business
platforms: [windows, linux, macos]
tags: ["骨科", "撮合", "供需对接", "医疗器械", "代工", "获客", "orthopedic", "matching", "sourcing"]
---

# 骨科供需撮合台

双向的：买方发需求，卖方发能力，系统打分撮合，**双方都点头才交换联系方式**。

不是名录查询工具——名录是「我去找人」，撮合是「双方都愿意才见面」。后者才不会骚扰人。

## 核心规则：双向同意

```
发布需求/能力 → 五维打分撮合 → 买方确认 → 卖方确认 → 才交换联系方式
                                    ↓ 任一方拒绝
                              永不交换，可永久列入拒访名单
```

单边同意看不到对方任何联系方式。撮合结果里，非我方主体一律打码。

## 快速上手（三步跑通）

```bash
cd ~/.workbuddy/skills/ortho-deal-match
PY="python"      # Windows 用 Python 环境里 python.exe 的完整路径

# 0. 一键看效果（会清空现有数据）
$PY scripts/demo.py --yes

# 1. 实名登记 + 签署撮合守则（第一个登记的人自动成为 owner）
$PY scripts/core.py register --name 姓名 --company 公司 --title 职务 \
                             --contact 你的邮箱 --purpose 用途
$PY scripts/core.py pledge --user U001        # 不加 --yes 可看条款全文
$PY scripts/core.py pledge --user U001 --yes

# 2. 登记主体（我方加 --self，联系方式必填）
$PY scripts/publish.py party --name "示例医疗科技" --side both \
                             --country 中国 --person 张三 --email 你的邮箱 --user U001 --self

# 3. 发需求（买方）/ 发能力（卖方）
$PY scripts/publish.py demand --party P001 --title "找PEEK脊柱融合器代工" \
    --desc "PEEK颈椎融合器与椎弓根螺钉，8000套/年，需ISO13485与CE MDR，销往德国" \
    --qty "8000套/年" --deadline 2027-06-30 --user U001

$PY scripts/publish.py capability --party P002 --title "脊柱植入物PEEK加工" \
    --desc "CNC machining of PEEK spinal cages, ISO13485, CE MDR, exporting to EU" \
    --capacity "1.5万件/月" --moq "300件" --lead-time "40天" --user U001

# 4. 撮合
$PY scripts/match.py run --all --user U001 --min-score 40 --verbose

# 5. 双向同意 → 交换联系方式
$PY scripts/intro.py request --match M001 --side buyer  --user U001 --note "想了解MOQ"
$PY scripts/intro.py accept  --match M001 --side seller --user U002
$PY scripts/intro.py reveal  --match M001 --user U001

# 6. 回写结果
$PY scripts/intro.py feedback --match M001 --user U001 --result "已寄样，报价中"
```

## 撮合打分（满分 100）

| 维度 | 分值 | 说明 |
|---|---|---|
| 产品分类 | 40 | 完全契合才给满分，不符则 0 并列为缺口 |
| 工艺能力 | 15 | 每个交集 +5 |
| 材料 | 15 | 每个交集 +6 |
| 资质认证 | 15 | 每个交集 +6，需求有而供应无的列为缺口 |
| 目标市场 | 10 | 每个交集 +5，含区域蕴含（德国→欧盟） |
| 加分 | 5 | 卖方经展会名录核验 +3；我方主体参与 +2 |

**缺口比分数更有用**：需求要 CE MDR 而对方只有 ISO13485，会明确写出来，而不是默默扣分。

需求/能力没写市场时，用主体国别兜底。

## 获客：从展会名录捞线索

```bash
# 从 L1 展会公开名录导入线索（不含个人联系方式）
$PY scripts/import_expo.py --country 德国 --kw spine --limit 50 --user U001 --dry-run
$PY scripts/import_expo.py --country 德国 --kw spine --limit 50 --user U001

# 按需求从线索池找人
$PY scripts/match.py leads --demand D001 --user U001

# 看中某家 → 激活（补录经确认的联系方式）→ 发能力 → 进撮合池
$PY scripts/publish.py activate --lead P009 --person "Michael Braun" \
                                --email 你的邮箱 --user U001
```

**线索只有公司信息，没有个人联系方式——这是刻意的。**
展方公开的是公司名录，个人邮箱不在授权范围内。要撮合必须先 activate，
而 activate 要求你已经确认对方愿意被接触。

## 防骚扰三道闸

| 闸 | 规则 |
|---|---|
| 实名登记 | 姓名/公司/职务/本人联系方式/用途缺一不可。对方要能找到你、回绝你、投诉你 |
| 撮合守则 | 七条守则逐条确认，90 天重签。含「不绕过流程私下找上门」「先签 NDA 再交换图纸」 |
| 配额限速 | 撮合 40 条/日、交换联系方式 8 次/日、发布 20 条/日。查不到不扣费，按实际命中计 |

外加三条：

- **拒访名单**：`intro.py decline --block` 或 `core.py block`，此后该主体从所有撮合结果中消失，任何人都碰不到。对方意愿优先于你的需求。
- **哈希链审计**：每个动作进 SHA-256 链，改一条后面的全断。`core.py audit --verify` 可验。
- **角色权限**：`owner`（首位登记者，全库视野）与 `member`（只能看自己参与的单）。owner 用 `intro.py assign` 把撮合分派给同事跟进；member 看不到、也碰不到别人的单，越权访问会被拦截并留痕。

## 角色与分派（多账号协作）

```bash
# 第一个登记的人自动是 owner；之后登记的都是 member
$PY scripts/core.py whoami --user U002          # 查看角色

# owner 把撮合分派给同事（此后该同事可查看与跟进这条单）
$PY scripts/intro.py assign --match M001 --to U002 --by U001
$PY scripts/intro.py assign --match M001 --clear --by U001   # 撤销分派

# owner 调整成员角色
$PY scripts/core.py role --user U002 --set owner --by U001
```

member 的可见域 = 自己发布的任一侧 + 分派给自己的 + 自己在留痕里操作过的。
其余撮合连存在都看不到；强行访问会被拒绝并写进审计链。

## 命令参考

| 脚本 | 子命令 | 用途 |
|---|---|---|
| `core.py` | register / pledge / whoami / role / block / unblock / blocklist / audit | 准入、角色与留痕 |
| `publish.py` | party / demand / capability / activate / list / close | 发布端 |
| `match.py` | run / leads / list / show | 撮合与线索匹配 |
| `intro.py` | request / accept / decline / reveal / feedback / assign | 对接、交换与分派 |
| `import_expo.py` | — | 从展会名录导入线索 |
| `init_db.py` | --reset / --stats | 建库与体检 |
| `demo.py` | --yes | 一键铺演示数据 |

## 数据落点

```
data/match.db        SQLite：parties / demands / capabilities / matches / intros
registry/users.jsonl    登记用户
registry/blocklist.jsonl 拒访名单
audit/audit.log      哈希链审计
```

主体状态：`lead`（线索，不参与撮合）→ `active`（可撮合）。
需求/能力可见性：`public`（进撮合池）/ `private`（仅自己可见）。

## 与 ortho-expo-contacts 的关系

| | ortho-expo-contacts | 本技能 |
|---|---|---|
| 干什么 | 查展会名录联系方式 | 撮合供需双方 |
| 方向 | 单向（我去找人） | 双向（双方都同意） |
| 门禁 | 登记+承诺+配额 | 登记+承诺+配额+**双向同意** |
| 数据 | 只读展会源，不落业务数据 | 落自己的需求与撮合记录 |

本技能**只读** ortho-expo-contacts 的库做背景核验与线索导入，不修改它。
展会库不存在时，核验与导入功能自动跳过，撮合不受影响。

## 领域词典

`scripts/taxonomy.py`：10 类产品 / 14 类工艺 / 13 类材料 / 10 类资质 / 24 个市场，
共 545 个中英别名。买房写 `locking plate`、卖方写「锁定接骨板」能撮合到一起。

匹配要点：
- 长别名优先且**命中即挖空**——`commercially pure titanium` 归纯钛，不会再被 `titanium` 抢成钛合金
- 词边界保护——`cn` 不会命中 `cnc`，`in` 不会命中 `implants`
- 代词语境清洗——`contact us` 不算美国，`export to US` 才算
- 市场蕴含——销往德国的，能供欧盟的也算匹配

## 已知边界

- 单机本地工具（SQLite + 文件），没有网络服务与多端并发；多人协作靠角色权限约束，`--side` 仍靠自觉声明
- 撮合方（owner，中间人）能看到所有 connected 的联系方式，这是设计内的；member 只能看自己参与的单
- 线索导入只取 L1 展会公开级，L2 个人参会者不导入
- 展会库路径默认取兄弟技能目录，可用环境变量 `ORTHO_EXPO_DB` 覆盖；不存在时核验与导线索自动跳过

## 版权与许可

Copyright (c) 2026 注册老炮。保留所有权利。

**知识版权声明**：本技能的设计方法论（五维打分撮合、双向同意交换、
骨科领域中英词典、角色可见域、哈希链审计）为作者原创知识资产，
禁止复制、转售，或用于训练任何模型。

**免责声明**：本技能按"原样"（AS IS）提供，不含任何明示或默示担保。
撮合结果由算法自动生成，仅供参考，不构成任何商业承诺或背书；
使用者对自身的发布、撮合与联络行为负全责，因违反上述守则造成的
纠纷与损失由使用者自行承担。

**许可**：MIT License（详见随包 `LICENSE.md`）。
