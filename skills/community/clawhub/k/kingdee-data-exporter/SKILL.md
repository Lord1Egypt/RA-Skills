---
name: kingdee-data-exporter
description: 金蝶 K3Cloud 经营数据（多表单据+报表）导出 Skill。用于指导用户安装后填写 `config.py` 的 `KINGDEE_CONFIG`（base_url/acctid/username/password），然后运行 `data_exporter.py` 批量导出 `bill_configs` + `report_configs` 中已配置的所有表单/报表。支持先 `--list-orgs` 导出全部组织列表，再用 `--org` 指定组织（或 `--org all` 全组织）导出，并可用 `--only` 只导出某个单据/报表；也提供对导出 Excel 做二次筛选（按组织/单据类型）的脚本用法示例。
---

## 你需要做什么（最少步骤）

1) 安装依赖（在本 Skill 目录执行）：

```bash
python -m pip install -r requirements.txt
```

2) 准备配置（避免把真实账号提交到 GitHub）：

- 复制 `config.example.py` 为 `config.py`
- 在 `config.py` 里填写 `KINGDEE_CONFIG`
- `WECHAT_CONFIG.webhook` 可留空（或运行时加 `--no-wechat`）

3) 运行导出：

```bash
python data_exporter.py
```

说明：默认会导出 `data_exporter.py` 里 `bill_configs` + `report_configs` 的全部配置项，生成一个多 Sheet 的 Excel。

## 常用命令

### 查看当前脚本支持导出的“单据/报表清单”

```bash
python data_exporter.py --show-config
```

你会看到两类条目：

- `[BILL] form_id | bill_name`
- `[RPT ] form_id | report_name`

后续 `--only` 参数就填这些 `form_id` 或者中文名称（支持逗号分隔）。

### 先导出全部组织列表（降低配置难度）

```bash
python data_exporter.py --list-orgs --no-wechat
```

会生成 `组织列表_YYYYmmdd_HHMMSS.xlsx`，里面至少包含：

- `number`: 组织编码（后续 `--org` 要用）
- `name`: 组织名称

### 某期间 + 某组织 + 全部单据/报表

例如导出 2026-02-01 到 2026-02-28，组织编码 101 的所有配置项：

```bash
python data_exporter.py --start 2026-02-01 --end 2026-02-28 --org 101 --no-wechat
```

组织也可以填多个（逗号分隔）：

```bash
python data_exporter.py --start 2026-02-01 --end 2026-02-28 --org 101,102,104 --no-wechat
```

### 某期间 + 某组织 + 某单据类型明细（只导出 1 个表单/报表）

1) 先用 `--show-config` 找到你要的 `form_id`，比如“销售出库单”对应 `SAL_OUTSTOCK`

2) 再用 `--only` 只导出它：

```bash
python data_exporter.py --start 2026-02-01 --end 2026-02-28 --org 101 --only SAL_OUTSTOCK --no-wechat
```

也可以用中文名：

```bash
python data_exporter.py --start 2026-02-01 --end 2026-02-28 --org 101 --only 销售出库单 --no-wechat
```

### 全组织导出（先“全量”再二次筛选）

如果你想先导出全组织，再在 Excel 中二次筛选：

```bash
python data_exporter.py --start 2026-02-01 --end 2026-02-28 --org all --no-wechat
```

注意：全组织数据量可能很大，建议优先使用 `--only` 缩小范围。

## 二次筛选：从导出 Excel 里筛某组织/某单据类型

当你已经用 `--org all` 导出了一份总表（或导出多个组织），可以用下面脚本把各 Sheet 按组织/单据类型再筛一遍，输出一个“过滤后的新 Excel”。

脚本位置：`skills/kingdee-data-exporter/scripts/filter_export_excel.py`

示例（按组织编码 101 过滤，并且只保留“单据类型=手工标准应收单”的明细行；会自动对每个 Sheet 尝试匹配常见组织列/单据类型列）：

```bash
python scripts/filter_export_excel.py --input "金蝶经营数据_2026年02月_20260401_120000.xlsx" --org 101 --bill-type "手工标准应收单"
```

如果你只想处理某一个 Sheet：

```bash
python scripts/filter_export_excel.py --input "金蝶经营数据_2026年02月_20260401_120000.xlsx" --sheet "应付单" --org 101
```

输出文件默认会生成在同目录，文件名会带 `_filtered` 后缀；也可指定 `--output`。

## 打包发布（可选）

如果你要把该 Skill 打包成 `.skill` 文件发布，有两种方式：

```bash
python ../skill-creator/scripts/package_skill.py .
```

如果你的仓库里没有 `skill-creator`，也可以直接把本目录打成 zip 并改后缀为 `.skill`（本质是 zip）。

