# 文件哈希校验 / File Hash Check

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `hash-check` v1.0.1 · LGD-Powered Utility Family · Zero-dependency

## English

Not sure whether the downloaded file is intact, and unsure whether the copy you sent to a colleague was changed on the way back — one command solves it. Generate / verify a SHA-256 manifest: download integrity, before/after transfer comparison, tamper-evident records. rc=0 ok / rc=1 findings / rc=2 usage; `--json` for machines.

### Usage
```bash
python scripts/hash_check.py --help
python scripts/hash_check.py --input <dir> --action generate
python scripts/hash_check.py --input <dir> --action check
```

### Disclaimer
Integrity aid only — back up important data before any cleanup you act on from the results.

## 中文

下载的文件不知道完不完整，传给同事再传回来不确定有没有被改——一条命令搞定。生成/校验目录 SHA-256 清单：下载验 integrity、传输前后比对、防篡改留证；成功 rc=0 / 发现问题 rc=1 / 用法错误 rc=2，`--json` 机器可读。

### 用法
```bash
python scripts/hash_check.py --help
python scripts/hash_check.py --input <目录> --action generate
python scripts/hash_check.py --input <目录> --action check
```

### 免责
完整性校验辅助；依据结果清理前请备份重要数据。

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
