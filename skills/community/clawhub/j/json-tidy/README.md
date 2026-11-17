# JSON 整形器 / JSON Tidy

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `json-tidy` v1.0.5 · LGD-Powered Utility Family · Zero-dependency

## English

The API returned JSON squashed onto one unreadable line, and the error just says "invalid" without telling you where — one command solves it. Format / minify / sort keys, with precise line-column error locating; pipe-friendly. rc=0 ok / rc=1 findings / rc=2 usage; `--json` for machines.

### Usage
```bash
python scripts/json_tidy.py --help
cat data.json | python scripts/json_tidy.py --format pretty
python scripts/json_tidy.py --input data.json --sort-keys
```

### Disclaimer
Efficiency aid only — back up important data before overwriting files.

## 中文

接口返回的 JSON 压成一行没法看，报错只说 invalid 不知道错在哪——一条命令搞定。格式化/压缩/键排序，解析错误精确定位行列，管道可用；成功 rc=0 / 发现问题 rc=1 / 用法错误 rc=2，`--json` 机器可读。

### 用法
```bash
python scripts/json_tidy.py --help
cat data.json | python scripts/json_tidy.py --format pretty
python scripts/json_tidy.py --input data.json --sort-keys
```

### 免责
效率辅助；覆盖写入前请备份重要数据。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

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
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
