<!-- wm:坤图_GIS:V5.0 -->

# ArcPy 脚本模板

此目录存放ArcGIS Pro/ArcMap专用Python脚本。

## 标准模板

| 脚本 | 文件名 | 用途 |
|------|--------|------|
| 坐标批量转换 | batch_project.py | 批量Project工具 |
| 拓扑检查 | topology_check.py | GDB拓扑规则验证 |
| 字段批量处理 | batch_fields.py | 添加/删除/计算字段 |
| 要素类导出 | export_features.py | 按属性/空间选择导出 |
| 要素转CAD | features_to_cad.py | GIS要素→DWG |
| 批量质检 | batch_qc.py | 几何+属性完整性检查 |

## 模板规范

所有脚本必须包含:
1. arcpy环境设置 (workspace + overwriteOutput)
2. 参数变量化（不硬编码路径）
3. 异常捕获 + 日志记录
4. 进度输出 (arcpy.GetMessages)
