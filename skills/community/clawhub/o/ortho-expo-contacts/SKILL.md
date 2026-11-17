---
name: ortho-expo-contacts
display_name: 骨科展会名录合规查询
version: 1.1.0
description: 骨科展会名录合规查询工具。覆盖 AAOS 2026、OMTEC 2025、DKOU 2026、AAHKS 2025、AOSSM 2025、SOFCOT 2025 共 2600+ 条参展商与参会者记录，内置实名登记、反骚扰承诺、配额限速、撞车提醒、拒访名单与哈希链审计四道闸门。当用户要查骨科展会联系方式、找某国参展商、找某类产品供应商、查 OMTEC 参会人、整理展会名录时使用。
description_en: Compliance-first orthopedic expo contact lookup. 2600+ exhibitor/attendee records from AAOS, OMTEC, DKOU, AAHKS, AOSSM and SOFCOT, gated by real-name registration, anti-harassment pledge, daily quotas, collision alerts, a do-not-contact list and a hash-chained audit log.
author: 注册老炮
license: MIT
category: business
platforms:
  - win32
  - darwin
  - linux
tags: ["骨科", "展会", "名录", "医疗器械", "合规", "获客", "orthopedic", "expo", "contacts"]
---

# 骨科展会名录合规查询

把分散在 8 个展会文件夹里的参展商与参会者名录，收敛成一个**可查询、可追溯、防滥用**的本地库。

数据来自展会官方公开发布的参展商/参会者名录，本身即为展会方授权公开、供商务联络之用的信息。
但这不代表可以随意批量抓取和群发——所以本工具在"能不能查"这件事上设了闸。

## 设计原则

**查得到，但赖不掉。** 每一次查询都绑定到一个留下真实联系方式的人，写进防篡改的审计链。
对方若投诉被骚扰，能立刻查到是谁、什么时候、查了哪几条。

## 数据分级

| 级别 | 内容 | 条数 | 谁能查 |
|------|------|------|--------|
| **L1 公开级** | 展会官方参展商名录：公司、国家、产品、官网、展位 | 907 | 登记 + 签承诺 |
| **L2 受限级** | OMTEC 2025 个人参会者：姓名、职务、工作邮箱 | 1716 | 登记 + 签承诺 + 更严配额 |
| **L3 私密级** | 自有客户表、供应商台账（手机 / WhatsApp） | 47 | **默认不入库**，仅本人 |

L3 是跑展会攒下的人脉资产，不进查询库。确需自用：`python scripts/build_index.py --include-l3`。

## 四道闸门

### 闸一 · 实名登记
必须留下姓名、公司、职务、**本人联系方式**、查询用途。缺一不可——
对方要能找到你、回绝你、投诉你。

### 闸二 · 反骚扰承诺（六条，90 天重签）
1. 不群发、不批量拨号、不轰炸式联系
2. 只用于骨科医疗器械相关的正当商务沟通
3. 不转售、不外传、不导入营销群发系统
4. 表明真实身份与来意，不伪造身份
5. 对方拒绝后立即停止，且不换渠道继续
6. 每次沟通留下自己的真实联系方式

### 闸三 · 配额限速
L1 每日 30 条 · L2 每日 10 条 · 单次最多返回 20 条 · 展开明文按 3 倍计价。
**不提供批量导出**，这是刻意的。

### 闸四 · 审计留痕
每条查询写入 SHA-256 哈希链（前一条哈希嵌进后一条）。删一条、改一条都会断链。

## 快速上手（三步跑通）

```bash
cd ~/.workbuddy/skills/ortho-expo-contacts
PY="python"      # Windows 用 ~/.workbuddy/binaries/python/envs/default/Scripts/python.exe

# 1. 登记（必须留真实联系方式）
$PY scripts/gate.py register --name 张三 --company 某某医疗 --title 国际业务 \
                             --contact 本人邮箱 --purpose 寻找欧洲OEM代工伙伴

# 2. 签反骚扰承诺（逐条确认六条）
$PY scripts/gate.py pledge --user U001

# 3. 查询（默认掩码）
$PY scripts/query.py --user U001 --country 德国 --kw spine
```

## 命令参考

### 查询 `scripts/query.py`

| 参数 | 说明 |
|------|------|
| `--user` | 必填，用户编号 |
| `--kw` | 关键词，匹配公司/人名/职务/产品/地区/展位，中英自动互译 |
| `--country` | 国家过滤，中英互通（"德国" 与 "Germany" 等价） |
| `--source` | 按展会过滤：`AAOS 2026` / `OMTEC 2025` / `DKOU 2026` / `AAHKS 2025` / `AOSSM 2025` / `SOFCOT 2025` |
| `--tier` | `L1`（默认，公司）或 `L2`（个人参会者） |
| `--has-email` / `--has-phone` | 只看有邮箱 / 有电话的 |
| `--limit` | 本次最多返回，上限 20 |
| `--reveal` | 展开完整联系方式（3 倍配额计价并重点留痕） |

```bash
# 找德国做脊柱的参展商
$PY scripts/query.py --user U001 --country 德国 --kw spine

# 找有邮箱的美国 OEM 供应商，展开明文
$PY scripts/query.py --user U001 --country 美国 --kw oem --has-email --reveal

# 在 OMTEC 参会人里找 sourcing 相关的人
$PY scripts/query.py --user U001 --tier L2 --kw sourcing
```

### 闸门管理 `scripts/gate.py`

| 命令 | 说明 |
|------|------|
| `register` | 实名登记，返回用户编号 |
| `pledge --user U001` | 签署/重签反骚扰承诺 |
| `whoami --user U001` | 查看登记信息 |
| `quota --user U001` | 查看今日剩余配额 |
| `block --company "X" --reason "..."` | 加入拒访名单 |
| `unblock --company "X"` | 移出拒访名单 |
| `blocklist` | 查看拒访名单 |
| `audit --verify` | 校验审计链完整性 |
| `audit --tail 20` | 查看最近审计记录 |

### 索引维护 `scripts/build_index.py`

```bash
$PY scripts/build_index.py                        # 重建索引（默认不含 L3）
$PY scripts/build_index.py --stats                # 只看统计
$PY scripts/build_index.py --include-l3           # 含 L3 私密数据（仅自用）
$PY scripts/build_index.py --src <展会Excel目录>   # 指定源目录
```

**源目录定位**：`--src` 参数 > 环境变量 `ORTHO_EXPO_SRC` > `<技能目录>/sources/`。
把展会 Excel 按子文件夹（01-AAOS / 03-SOFCOT / 04-AOSSM / 05-OMTEC / 06-AAHKS / 08-DKOU）
放进源目录即可；没有的展会自动跳过。

**源文件只读，绝不改动。** 源目录新增或更新展会表格后重建索引即可。

**依赖披露**：仅构建器 `build_index.py` 需要 `openpyxl`（解析展会 Excel）——
当前环境没有时它会打印安装指引。日常查询 `query.py` 与闸门 `gate.py` 零依赖（纯标准库）。

## 两个防骚扰的实用机制

**撞车提醒** — 同一家公司 30 天内被别人查过，会提示"该主体近期已被 U002(日期) 查询过，请先内部确认"。避免同事前后脚联系同一家，把人家烦到拉黑。

**拒访名单** — 某家明确表示拒绝后加入名单，此后任何人查询都只显示"已屏蔽 + 原因"，不再展示联系方式。对方的意愿优先于你的需求。

```bash
$PY scripts/gate.py block --company "Acme Corp" --reason "电话中明确拒绝，勿再联系"
```

## 数据源与已知坑

详见 `references/DATA_SOURCES.md`。两个已踩过的坑：

- **AOSSM**：Sheet1 的 Company 列大量公式无缓存值（`data_only` 读出来是 None），136 行里只有 8 行有公司名。完整名录在 Sheet2（105 家）。解析器已改用以 Sheet2 为底、Sheet1 补明细。
- **AAOS / DKOU**："联系方式"列是混合列，479 行里 7 个真邮箱 + 65 个电话 + 407 空。只按 `@` 提取会丢掉全部 65 个电话。

构建器带空值率自检，覆盖率异常会告警；源目录缺失或为空时不崩溃，自动降级为三条引导提示（也可用 `--src` 临时指定源目录）。

## 红线

- 索引库 `data/contacts.db` 含个人联系方式，**不得进入任何发布包、云盘、群聊或外部服务**
- 不提供批量导出功能，也不要用脚本绕过配额
- L3 私密数据默认不入库；若自行启用，严禁对外共享
- 若本技能要对外发布，必须先把 `data/`、`registry/`、`audit/` 整个排除

## 常见问题

**查不到东西？** 先 `--stats` 确认索引在；国家字段中英混排，用中文（"德国"）或英文（"Germany"）都能查；产品关键词支持中英互译（spine ↔ 脊柱）。

**配额不够用？** 配额是刻意的限制。真有批量需求，说明你要做的事可能不适合用这个工具——商务联络从来不是靠量。

**数据要更新？** 把新的展会表格放进源目录，跑一次 `build_index.py`。

## 配套技能：ortho-deal-match（骨科供需撮合台）

本技能是**单向查名录**——我去找人。如果要**双向撮合**——买卖双方都把需求/能力发出来、
系统打分配对、双方都确认后才交换联系方式——用 `ortho-deal-match`：

```bash
cd ~/.workbuddy/skills/ortho-deal-match
python scripts/import_expo.py --country 德国 --kw spine --limit 50 --user U001
python scripts/match.py leads --demand D001 --user U001
```

它只读本技能的 `data/contacts.db`：L1 记录用于背景核验与线索导入（**不导入个人邮箱电话**），
L2 个人参会者不导入。删掉本技能不影响撮合台运行，只是核验与导线索功能会跳过。

## 版权与许可

Copyright (c) 2026 注册老炮。保留所有权利。

**知识版权声明**：本技能的设计方法论（数据分级、四道闸门、哈希链审计、
中英双向别名归一化）为作者原创知识资产，禁止复制、转售，或用于训练任何模型。

**免责声明**：本技能按"原样"（AS IS）提供，不含任何明示或默示担保。
使用者对自身的查询与商务行为负全责；因违反上述反骚扰条款造成的纠纷、
投诉与损失，由使用者自行承担。查询结果仅供参考，不构成任何商业承诺；
数据覆盖以实测统计为准，不夸大解析成功率。

**许可**：MIT License（详见随包 `LICENSE.md`）。数据源版权归各展会主办方所有，
本工具仅处理已获授权公开的信息，不重新分发任何名录数据。
