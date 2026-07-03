<!-- wm:坤图_GIS:V5.0 -->
# assets/ —— GIS_SKILL V5.0 样例资源库

> 版本：V5.0 | 用途：可直接复用的测试数据/模板/示意图

---

## 目录结构

```
assets/
├── samples/              # 样例数据
│   ├── vector/           # 矢量样例(SHP/GeoPackage/GDB)
│   ├── raster/           # 栅格样例(TIF/COG)
│   ├── pointcloud/       # 点云样例(LAS/LAZ)
│   ├── threed/           # 三维样例(3DTiles/OBJ)
│   └── dwg/              # CAD样例(DWG/DXF/CASS)
│
├── templates/            # 可复用模板
│   ├── reports/          # 报告模板
│   │   ├── data_inspection_report.md
│   │   ├── quality_check_report.md
│   │   ├── project_archive_report.md
│   │   └── metadata_template.xml
│   ├── code/             # 代码模板
│   │   ├── arcpy_skeleton.py
│   │   ├── pyqgis_skeleton.py
│   │   └── gdal_skeleton.py
│   └── workflows/        # 流程Mermaid模板
│       ├── dlg_production.mmd
│       ├── dem_production.mmd
│       └── data_conversion.mmd
│
└── diagrams/             # 示意图/流程图
    ├── architecture/     # 架构图
    └── workflows/        # 工序流程图
```

---

## 报告模板示例

### 数据探查报告模板 (data_inspection_report.md)

```markdown
# 数据探查报告

## 基本信息
- 项目名称: {project_name}
- 数据来源: {data_source}
- 探查时间: {timestamp}
- 探查工具: {engine}

## 坐标系信息
| 项目 | 值 |
|------|-----|
| 坐标系名称 | {crs_name} |
| EPSG/WKID | {wkid} |
| 投影类型 | {projection_type} |
| 单位 | {unit} |

## 数据概况
| 图层 | 要素类型 | 记录数 | 空间范围 |
|------|---------|--------|---------|
| {layer_name} | {geom_type} | {count} | {extent} |

## 属性字段
| 字段名 | 类型 | 别名 | 长度 | 非空率 |
|--------|------|------|------|--------|
| {field} | {type} | {alias} | {len} | {fill_rate}% |

## 风险清单
| 等级 | 问题 | 影响 | 建议 |
|------|------|------|------|
| {level} | {issue} | {impact} | {suggestion} |

## 探查结论
{conclusion}
```
```
