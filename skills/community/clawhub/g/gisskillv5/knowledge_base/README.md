<!-- wm:坤图_GIS:V5.0 -->
# knowledge_base/ —— GIS_SKILL V5.0 底层知识库

> 版本：V5.0 | 原V1.0 45文件参考文档 | 新增V5.0三级分层架构

---

## V5.0 目录总览

```
knowledge_base/
├── group_01_foundation/      # 群组一：基础底座 (原01-04)
├── group_02_standards/       # 群组二：标准与规范 (原05-10)
├── group_03_software/        # 群组三：软件工具 (原12-20,36,38)
├── group_04_development/     # 群组四：开发与自动化 (原21-27,35,39)
├── group_05_practice/        # 群组五：实战与避坑 (原28-33)
├── group_06_modern/          # 群组六：现代GIS技术栈 (原39-45)
├── group_07_evolution/       # 群组七：自进化机制 (原37)
└── appendix/                 # 独立附录 (原31)
```

---

## 文件映射表 (原references/ → 新knowledge_base/)

| 原文件 | 新位置 |
|--------|--------|
| references/01~04号 | knowledge_base/group_01_foundation/ |
| references/05~10号 | knowledge_base/group_02_standards/ |
| references/12~20,36,38号 | knowledge_base/group_03_software/ |
| references/21~27,35,39号 | knowledge_base/group_04_development/ |
| references/28~33号 | knowledge_base/group_05_practice/ |
| references/39~45号 | knowledge_base/group_06_modern/ |
| references/37号 | knowledge_base/group_07_evolution/ |
| references/31号 | knowledge_base/appendix/ |

---

## YAML元数据头规范

每个md文件必须包含以下yaml frontmatter:

```yaml
---
knowledge_id: GK-01-CRS-001       # 全局唯一知识ID
title: "坐标系统与投影"
version: "5.0"
category: coordinate_system
group: 01_foundation
standards: ["GB/T 14911-2008", "CH/T 1006-2000"]
software_versions: ["ArcGIS Pro 3.6+", "QGIS 3.40+"]
keywords: ["坐标系", "投影", "CGCS2000", "椭球", "WKID"]
related_modules: ["04", "32", "05"]
risk_level: low
last_updated: 2026-06-22
update_cycle: quarterly
---
```

---

## 现有文件自动归组脚本

```bash
# 将references/下文件按群组归组到knowledge_base/
# 执行前备份references/

for f in references/0[1-4]_*; do cp "$f" knowledge_base/group_01_foundation/; done
for f in references/0[5-9]_* references/10_*; do cp "$f" knowledge_base/group_02_standards/; done
for f in references/1[2-9]_* references/20_* references/36_* references/38_*; do cp "$f" knowledge_base/group_03_software/; done
for f in references/2[1-7]_* references/35_* references/39_*; do cp "$f" knowledge_base/group_04_development/; done
for f in references/2[8-9]_* references/3[0-3]_*; do cp "$f" knowledge_base/group_05_practice/; done
for f in references/39_* references/4[0-5]_*; do cp "$f" knowledge_base/group_06_modern/; done
for f in references/37_*; do cp "$f" knowledge_base/group_07_evolution/; done
for f in references/31_*; do cp "$f" knowledge_base/appendix/; done
```
