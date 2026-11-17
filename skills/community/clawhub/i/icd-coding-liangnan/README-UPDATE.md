# ICD-Coding Skill v2.3.0 更新包

## 更新内容

将 v2.2.0 → v2.3.0，新增 **CHS-DRG 3.0 分组知识**（医保发〔2026〕22号 附件 1）。

## 新增文件清单

### 文档 (3 个)
- `SKILL.md` — 更新版本号到 v2.3.0，新增 DRG 3.0 章节
- `docs/DRG3.0_Knowledge.md` — CHS-DRG 3.0 知识手册（11KB）
- `docs/DRG3.0_Changes.md` — 2.0 → 3.0 关键变更对照（12KB）
- `docs/drg3.0_lookup_tool.py` — Python 查询工具（13KB）

### 数据 (15 个 JSON)
| 文件 | 大小 | 行数 | 说明 |
|------|------|------|------|
| `data/drg3.0_mdc.json` | 3KB | 26 | MDC 目录 |
| `data/drg3.0_mdc_summary.json` | 1KB | 26 | MDC 概览（ADRG/DRG 数） |
| `data/drg3.0_adrg.json` | 60KB | 492 | ADRG 目录 |
| `data/drg3.0_drg.json` | 152KB | 825 | DRG 目录 |
| `data/drg3.0_basal.json` | 5KB | 31 | 基层病组 |
| `data/drg3.0_adrg_compare.json` | 114KB | 493 | 2.0↔3.0 对比 |
| `data/drg3.0_mdc_dx.json` | 3.9MB | 29,174 | MDC 主诊表 |
| `data/drg3.0_adrg_to_icd.json` | 4.5MB | 67,329 | ADRG→ICD 入组规则 |
| `data/drg3.0_icd_to_adrg.json` | 1.8MB | 38,427 | ICD→ADRG 反向索引 |
| `data/drg3.0_ops.json` | 0.9MB | 9,629 | 手术操作目录 |
| `data/drg3.0_mcc.json` | 153KB | 1,581 | MCC 严重合并症 |
| `data/drg3.0_cc.json` | 607KB | 6,337 | CC 合并症 |
| `data/drg3.0_excl_dx.json` | 204KB | 1,859 | 疾病排除列表 |
| `data/drg3.0_high_risk_preg.json` | 80KB | 811 | 高危妊娠 |
| `data/drg3.0_robot_ops.json` | 1KB | 5 | 机器人辅助手术 |

**总数据量约 12.5 MB**。

## 应用步骤

### 方法 1：直接替换（推荐）

如果你已下载 v2.2.0 源码：

1. 解压本更新包
2. 把 `docs/` 和 `data/` 里 `drg3.0_*` 开头的文件复制到你的 skill 目录
3. 用本更新包里的 `SKILL.md` 替换原 `SKILL.md`
4. 重新上传到 ClawHub：https://clawhub.ai/skills/publish

### 方法 2：整包上传

1. 在 ClawHub 上传整个目录作为新版本
2. 版本号设为 v2.3.0
3. 更新日志引用本 README

## 数据来源

- **原始文件**：国家医保局《按病组（DRG）付费 3.0 版分组方案》PDF（2026-09-02 印发，1829 页）
- **结构化**：基于 PDF 双栏版面解析，逐章节结构化提取
- **生成时间**：2026-08-27
- **文号**：医保发〔2026〕22号

## 注意事项

1. **过渡期**：2026-09 ~ 2027-03，建议 skill 同时支持 2.0 和 3.0 查询命令
2. **执行时点**：DRG 3.0 自 2027-01-01 起正式执行
3. **与 DIP 3.0 关系**：DIP 3.0（附件 2，311 页）首批 127 个基层病种与 DRG 3.0 首批 31 个基层病组共同构成"同病同付"政策体系；DIP 3.0 数据未在本更新包中，如需请另作处理
4. **原 2.0 数据保留**：未删除任何 2.0 数据，与 3.0 并行

## 工具测试

```bash
cd icd-coding/
python3 docs/drg3.0_lookup_tool.py --help
python3 docs/drg3.0_lookup_tool.py mdc I63.401
python3 docs/drg3.0_lookup_tool.py adrg 33.5000
python3 docs/drg3.0_lookup_tool.py drg BB21
python3 docs/drg3.0_lookup_tool.py basal 高血压
python3 docs/drg3.0_lookup_tool.py compare AE1
python3 docs/drg3.0_lookup_tool.py list MDCB
python3 docs/drg3.0_lookup_tool.py search 脑梗死
```

## 验证清单

更新后请确认：

- [ ] SKILL.md 顶部版本号 = v2.3.0
- [ ] 核心能力列表中 CHS-DRG 3.0 项可见
- [ ] docs/DRG3.0_Knowledge.md 和 DRG3.0_Changes.md 存在
- [ ] docs/drg3.0_lookup_tool.py 可执行
- [ ] data/ 下有 15 个 drg3.0_*.json
- [ ] 查询命令 `DRG3.0查MDC I63.401` 返回 `MDCB 神经系统疾病及功能障碍`
- [ ] `DRG3.0查ADRG 33.5000` 返回 `AA2 肺移植`（MDCA）
- [ ] `DRG3.0查DRG BB21` 返回伴出血诊断的颅脑手术伴严重合并症
- [ ] `DRG3.0基层病组 高血压` 返回 `FV29`
- [ ] `DRG3.0对比2.0 AE1` 返回 `AE1 肾移植 → AC2 肾移植`

---

最后更新：2026-09-08 by Mavis Agent
