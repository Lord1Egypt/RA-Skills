# 马德里技能：参考资料体积与定位索引

> **用途**：参考资料清单的**体积基准**与**大文件章节→行号定位**，供按需分段读取。

> **权威范围**：本文件是**参考资料体积与行号定位**的唯一权威源；条款级索引见 SKILL.md §3.7 与 @references/madrid-faq.md §四。

> **维护**：第 0 节与第 I 节由 `scripts/selftest.py` 校验（体积表漂移、行号有效性）；文件增删或大文件改版后重跑 `py scripts/selftest.py --fix-index` 自动重生成两节。**本文件自身不计入体积表**（否则自指、永不一致）。

> **编码**：CRLF、UTF-8 无 BOM。

---

## 0. 实测体积表（脚本生成，勿手改）

<!-- SIZE_TABLE_START -->
| 文件 | 字节 | 行数 |
| --- | --- | --- |
| `madrid-admin-instructions-en.md` | 11598 | 279 |
| `madrid-admin-instructions.md` | 16302 | 370 |
| `madrid-agreement-en.md` | 46715 | 383 |
| `madrid-agreement.md` | 51712 | 796 |
| `madrid-cnipa-bridge.md` | 4590 | 63 |
| `madrid-declarations.md` | 28819 | 373 |
| `madrid-faq.md` | 13561 | 125 |
| `madrid-fast-track-examination-cnipa.md` | 5502 | 111 |
| `madrid-fees.md` | 17210 | 235 |
| `madrid-goods-services-classification.md` | 26236 | 291 |
| `madrid-protocol-en.md` | 55233 | 478 |
| `madrid-protocol.md` | 55500 | 855 |
| `madrid-regulations-en.md` | 158986 | 1309 |
| `madrid-regulations.md` | 156614 | 2133 |
| `madrid-scripts.md` | 5109 | 45 |
| `madrid-sources.md` | 8233 | 57 |
| `madrid-workflows.md` | 7757 | 61 |
<!-- SIZE_TABLE_END -->

> 说明：两份官方 PDF 原件（Madrid e-Filing 申请人操作指南、商品和服务分类审查指南第五版）已于 v3.7.0 依维护决定自本技能移除，故不在本表内。

---

## I. 大文件章节 → 行号定位

> 覆盖 4 份中文法律全文文件。定位用途：区分**条文正文逐字全文**段与技能整理的**附录（要点与勘误／文档元信息／目录结构／各条要点详解）**段，避免把整理内容当官方原文引用。

<!-- LINE_INDEX_START -->
### madrid-agreement.md（796 行）
| 行号 | 章节 |
| --- | --- |
| 559 | 附录：要点与勘误（本技能整理，非官方文本；条文正文以上文逐字全文为准） |
| 561 | 文档元信息 |
| 574 | 目录结构 |
| 606 | 各条要点详解 |
| 759 | 协定要点与议定书对比 |
| 785 | 实务要点 |

### madrid-protocol.md（855 行）
| 行号 | 章节 |
| --- | --- |
| 642 | 附录：要点与勘误（本技能整理，非官方文本；条文正文以上文逐字全文为准） |
| 644 | 文档元信息 |
| 656 | 目录结构 |
| 687 | 各条要点详解 |
| 832 | 议定书对协定的关键改进 |
| 844 | 实务要点 |

### madrid-regulations.md（2133 行）
| 行号 | 章节 |
| --- | --- |
| 1684 | 附录：要点与勘误（本技能整理，非官方文本；条文正文以上文逐字全文为准） |
| 1686 | 文档元信息 |
| 1699 | 目录结构 |
| 1714 | 各章要点详解 |
| 2013 | 费用表（Fee Schedule）要点 |
| 2032 | 实务操作要点 |
| 2042 | 英文条款标题对照（术语锚定，依据 WIPO Lex text/596531） |

### madrid-admin-instructions.md（370 行）
| 行号 | 章节 |
| --- | --- |
| 227 | 附录：要点与勘误（本技能整理，非官方文本；条文正文以上文逐字全文为准） |
| 229 | 文档元信息 |
| 241 | 目录结构 |
| 253 | 各条要点详解 |
| 341 | 实务操作要点总结 |

<!-- LINE_INDEX_END -->

