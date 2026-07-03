<!-- wm:坤图_GIS:V5.0 -->
# GIS_SKILL V5.0 避坑库标准化索引

> 版本：V5.0 | 条目数：目标800+ (当前160+ → 升级中)
> 格式：统一 WRONG / CAUSE / SOLUTION / CODE 四字段
> 分类：8大类 + 报错码速查索引

---

## 分类架构

```
pitfalls/
├── 01_coordinate_system/    # 坐标系陷阱 (80+条)
├── 02_software/             # 软件操作陷阱 (120+条)
├── 03_data_conversion/      # 数据转换陷阱 (100+条)
├── 04_3d_pointcloud/        # 三维与点云陷阱 (80+条)
├── 05_ai_remote_sensing/    # AI与遥感陷阱 (60+条)
├── 06_database_web/         # 数据库与Web陷阱 (100+条)
├── 07_batch_automation/     # 批量处理陷阱 (80+条)
└── 08_error_codes/          # 报错码速查 (180+条)
```

---

## 标准化条目模板

```yaml
pitfall_id: PIT-CRS-001
category: coordinate_system
severity: critical  # critical | high | medium | low
software: [ArcGIS Pro, QGIS]
version: all

wrong: |
  将CGCS2000地理坐标系数据直接以经纬度导出DWG，
  导致CAD中坐标显示为0.XXXX而非实际米值。

cause: |
  DWG/DXF仅支持投影坐标系(米制单位)，
  地理坐标系以度为单位无法正确表达。

solution: |
  1. 使用 Project 工具将数据从地理CS(CGCS2000)转换到投影CS(如CGCS2000 GK Zone)
  2. 再执行 Export to CAD
  3. 确认目标投影带号与数据所在区域匹配

code: |
  # ArcPy解决方案
  arcpy.management.Project("input_gcs", "temp_projected", 
      arcpy.SpatialReference(4547))  # CGCS2000 3 Degree GK CM 114E
  arcpy.conversion.ExportCAD("temp_projected", "CADRG", "output.dwg")

tags: [DWG, 坐标偏移, 经纬度, 投影, CGCS2000]
related_errors: [ERROR 000732, ERROR 000210]
```

---

## 报错码速查索引

### ArcGIS 报错码

| 错误码 | 含义 | 避坑ID | 快速方案 |
|--------|------|--------|---------|
| ERROR 000210 | 无法创建输出 | PIT-SW-001 | 检查路径/权限/GDB名称不含空格 |
| ERROR 000229 | 无法打开数据 | PIT-SW-002 | 检查数据源路径/锁文件 |
| ERROR 000732 | 输入不存在 | PIT-SW-003 | 检查文件路径/工作空间设置 |
| ERROR 000735 | 坐标系不匹配 | PIT-CRS-002 | Project工具统一坐标系 |
| ERROR 999999 | 未知错误 | PIT-SW-004 | 重启ArcGIS/检查数据完整性/64位 |
| ERROR 001156 | 字段冲突 | PIT-SW-005 | 检查字段名长度/重复/非法字符 |

### GDAL 错误码

| 错误码 | 含义 | 避坑ID | 快速方案 |
|--------|------|--------|---------|
| GDAL_ERROR 1 | 文件打开失败 | PIT-SW-020 | 检查路径编码/文件权限 |
| GDAL_ERROR 4 | 不支持的操作 | PIT-SW-021 | 格式不支持/投影不支持 |
| GDAL_ERROR 6 | 坐标转换失败 | PIT-CRS-010 | 检查PROJ数据路径 |

### FME 转换异常

| 异常 | 含义 | 避坑ID | 快速方案 |
|------|------|--------|---------|
| INVALID_GEOMETRY | 无效几何 | PIT-SW-040 | GeometryValidator转换器 |
| COORDINATE_SYS_CONFLICT | 坐标系冲突 | PIT-CRS-020 | CoordinateSystemSetter统一 |
| MEMORY_LIMIT | 内存溢出 | PIT-BAT-030 | 分块处理/Features Per Bulk |

### QGIS 算法崩溃

| 崩溃场景 | 原因 | 避坑ID | 快速方案 |
|----------|------|--------|---------|
| Processing崩溃 | 内存不足 | PIT-SW-060 | 分层处理/关闭其他程序 |
| 大文件保存失败 | 临时目录满 | PIT-SW-061 | 清理临时文件/更换输出目录 |
| 坐标偏移 | CRS选择错误 | PIT-CRS-030 | 检查on-the-fly投影设置 |

---

## 更新规则

- 新条目优先归类到现有8大类
- 每条必须包含可运行修复代码
- 关联报错码同时更新速查索引
- 季度评估避坑库覆盖完整度
- 用户反馈的新坑24h内入库
