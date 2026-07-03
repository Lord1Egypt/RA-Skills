<!-- wm:坤图_GIS:V5.0 -->

# PyQGIS 脚本模板

此目录存放QGIS桌面软件专用Python脚本。

## 标准模板

| 脚本 | 文件名 | 用途 |
|------|--------|------|
| Processing批量调用 | batch_processing.py | 批量运行QGIS算法 |
| 图层样式批量应用 | batch_style.py | QML样式批量加载 |
| 布局自动导出 | layout_export.py | 打印布局→PDF/PNG |
| 矢量瓦片生成 | vector_tiles.py | 矢量瓦片MBTiles生成 |
| COG发布 | cog_publish.py | 云优化GeoTIFF生成 |
| 数据源批量更新 | batch_update_datasource.py | 图层数据源修复 |

## 模板规范

所有脚本必须包含:
1. QgsApplication初始化
2. 项目文件加载 (QgsProject)
3. 图层遍历 (QgsProject.instance().mapLayers())
4. 异常捕获 + 日志记录
5. QGIS版本兼容性标注
