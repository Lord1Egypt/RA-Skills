# hgrac-route-checker · 人类遗传资源事项路径判定器

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

## English

### What it does
Routes human-genetic-resource matters (collect / store / use / transfer / cooperate) to approval (审批) or filing (备案) per the **Human Genetic Resources Regulation (State Council Order 717) + implementing rules (effective 2023-07-01), articles 8–22** (clause numbers pending manual verification; official texts prevail).

- **Insufficient input → strict presumption**: `collect` without `foreign_involved` / `scale` returns the **most obligation-heavy route** (approval), states the possible range in `warnings`, and sets `rc=1`. It never silently returns filing.
- **No silent invalid input**: non-yes/no `foreign_involved`, non-big/normal `scale`, unknown `action` → gate error (`rc=2`).
- **Out of scope**: material checklists, ethics-review detail, processing timelines.

### Install & run (zero-dependency, Python 3.8+)
```bash
python hgrac-route-checker.py --demo   # 3 built-in smoke cases
# rc=1 (strict presumption, incomplete args)
python hgrac-route-checker.py --action collect
# rc=0 (complete args → filing)
python hgrac-route-checker.py --action collect --foreign_involved no --scale normal
# rc=2 (invalid input)
python hgrac-route-checker.py --action collect --scale huge
```

### Parameters
| Parameter | Required | Meaning |
|---|---|---|
| `action` | yes | Matter: collect / store / use / transfer / coop |
| `foreign_involved` | no | Foreign party involved: yes / no |
| `scale` | no | Important species / cumulative person-count: big / normal |

### Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `route`, `obligations`, `warnings`, and `aigc_mark` (GB45438-2025 metadata).

Real output (`--action collect`, values verbatim):

```json
{
  "input": {"action": "collect", "foreign_involved": null, "scale": null},
  "result": {
    "route": "Approval (MoST)",
    "evidence": ["Regulation articles 8–11"],
    "warnings": [
      "Incomplete input: no foreign_involved / scale given; official rules split collect into approval vs filing by species/scale and foreign involvement; review after completing.",
      "Route uncertain (possible range filing ~ approval): strict presumption took approval (heaviest obligations); actual route may be lighter; review after completing parameters."
    ]
  },
  "rc": 1
}
```

### Clause review checklist (pending manual verification)
| Clause | Used for | Status |
|---|---|---|
| Regulation art. 8–11 | Approval vs filing split for collect/store | pending manual check |
| Regulation art. 12–13 | Deposit approval route | pending manual check |
| Regulation art. 14–16 | Utilization (filing / approval) route | pending manual check |
| Regulation art. 17–22 | Outbound provision / international cooperation approval | pending manual check |

### Theory hook
The source of life must be registered — genetic-resource approval/filing is fiduciary registration of a common human heritage. Domain slot: TH-BIO-001.

## 中文

### 它做什么
依据**《人类遗传资源管理条例》（国务院令717号）+ 实施细则（2023-07-01 施行）第 8–22 条**（条款号待人工核对；以官方文本为准），把人类遗传资源事项（采集/保藏/利用/对外提供/国际合作）路由到**审批**或**备案**。

- **输入不足 → 从严推定**：`collect` 缺 `foreign_involved`/`scale` 时返回**义务最重的路径**（审批），在 `warnings` 中说明可能区间，置 `rc=1`，绝不静默返回备案。
- **无效输入不静默**：`foreign_involved` 非 yes/no、`scale` 非 big/normal、`action` 未知 → 门禁错误（`rc=2`）。
- **不做什么**：材料清单、伦理审查细节、办理时限。

### 安装与运行（零依赖，Python 3.8+）
```bash
python hgrac-route-checker.py --demo   # 3 个内置冒烟用例
python hgrac-route-checker.py --action collect                       # rc=1（从严推定，参数不全）
python hgrac-route-checker.py --action collect --foreign_involved no --scale normal   # rc=0（参数齐 → 备案）
python hgrac-route-checker.py --action collect --scale huge           # rc=2（非法输入）
```

### 参数
| 参数 | 必填 | 含义 |
|---|---|---|
| `action` | 是 | 事项：collect/store/use/transfer/coop |
| `foreign_involved` | 否 | 是否涉外：yes/no |
| `scale` | 否 | 重要种类/累计人份：big/normal |

### 输出
确定性 JSON IR，含 `rc`（**0**=ok / **1**=完成有告警 / **2**=输入不全或非法）、`route`、`obligations`、`warnings` 与 `aigc_mark`（GB45438-2025 元数据）。

### 条款待人工核对清单
| 条款 | 用途 | 状态 |
|---|---|---|
| 条例 第8-11条 | 采集/保藏的审批与备案区分 | 待人工核对 |
| 条例 第12-13条 | 保藏审批路径 | 待人工核对 |
| 条例 第14-16条 | 利用（备案/审批）路径 | 待人工核对 |
| 条例 第17-22条 | 对外提供/国际合作审批路径 | 待人工核对 |

### 理论钩子
生命之源须有籍——遗传资源审批/备案即对人类共同遗产的受托登记。域站位件：TH-BIO-001。

---

## License & attribution
**分层许可——代码许可不覆盖文档与理论文本。**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `hgrac-route-checker.py` | **MIT** |
| 文档与理论文本 | 本 `README.md`、`SKILL.md`、「理论依据」部分及一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利 |

> 代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**。）

## 家族合集
| 域 | 工具 | 大使 |
|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 |
| AUT 驾驶 | aut-grade-checker | 诺卫 |
| DAT 数据 | data-grade-checker | 诺源 |
| BIO 生物 | hgrac-route-checker | 诺康 |
| FIN 金融 | fin-ai-classifier | 诺丰 |
| LAW 法律 | evid-four-check | 诺律 |
