<!-- wm:坤图_GIS:V5.0 -->
# scripts/ —— GIS_SKILL V5.0 自动化脚本仓库

> 版本：V5.0 | 分类：配套工具库
> 覆盖引擎：Python | ArcPy | PyQGIS | FME | GDAL | Shell

---

## 目录结构

```
scripts/
├── python/           # 通用Python脚本(geopandas/gdal/shapely)
│   ├── batch_project.py           # 批量坐标转换
│   ├── topology_check.py          # 拓扑检查
│   ├── format_convert.py          # 格式互转
│   ├── metadata_generate.py       # 元数据自动生成
│   └── quality_report.py          # 质检报告生成
│
├── arcpy/            # ArcPy专用脚本(需ArcGIS授权)
│   ├── gdb_build.py               # GDB建库
│   ├── topology_repair.py         # 拓扑修复
│   ├── dwg_export.py              # DWG导出
│   └── batch_processing.py        # 批量处理
│
├── pyqgis/           # PyQGIS脚本(无需授权)
│   ├── processing_pipeline.py    # Processing管道
│   └── map_export.py              # 地图导出
│
├── fme/              # FME脚本
│   └── workspace_templates/       # FME工作空间模板
│
└── shell/            # 跨平台Shell脚本
    ├── gdal_batch.sh              # GDAL批量处理
    ├── ogr2ogr_convert.sh         # ogr2ogr转换
    └── deploy_pmtiles.sh          # PMTiles部署
```

---

## 脚本模板

### Python: 批量坐标转换

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/python/batch_project.py
GIS_SKILL V5.0 - 批量坐标转换脚本
引擎: geopandas + pyproj
"""
import os
import sys
import logging
import argparse
from pathlib import Path
import geopandas as gpd
from pyproj import CRS

# [日志配置]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('batch_project.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def batch_project(input_dir, target_epsg, output_dir=None, pattern="*.shp"):
    """
    批量坐标转换
    Args:
        input_dir: 输入目录
        target_epsg: 目标EPSG代码(如4490=CGCS2000)
        output_dir: 输出目录(默认 input_dir/output_YYYYMMDD)
        pattern: 文件匹配模式
    """
    from datetime import datetime
    
    if output_dir is None:
        output_dir = os.path.join(input_dir, f"output_{datetime.now().strftime('%Y%m%d')}")
    os.makedirs(output_dir, exist_ok=True)
    
    files = list(Path(input_dir).glob(pattern))
    logger.info(f"发现 {len(files)} 个文件待转换")
    
    success = 0
    failed = []
    
    for f in files:
        try:
            gdf = gpd.read_file(f)
            src_crs = gdf.crs
            
            if src_crs is None:
                logger.warning(f"{f.name}: 无坐标系，跳过")
                failed.append({'file': str(f), 'reason': 'no_crs'})
                continue
            
            if src_crs.to_epsg() == target_epsg:
                logger.info(f"{f.name}: 已是目标坐标系，跳过")
                continue
            
            gdf = gdf.to_crs(CRS.from_epsg(target_epsg))
            out_path = os.path.join(output_dir, f.name)
            gdf.to_file(out_path)
            logger.info(f"{f.name}: {src_crs.to_epsg()} → {target_epsg} ✓")
            success += 1
            
        except Exception as e:
            logger.error(f"{f.name}: 转换失败 - {e}")
            failed.append({'file': str(f), 'reason': str(e)})
    
    logger.info(f"完成: 成功{success}, 失败{len(failed)}")
    return success, failed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GIS_SKILL V5.0 批量坐标转换')
    parser.add_argument('input_dir', help='输入目录')
    parser.add_argument('target_epsg', type=int, help='目标EPSG代码')
    parser.add_argument('--output', '-o', help='输出目录')
    parser.add_argument('--pattern', '-p', default='*.shp', help='文件匹配模式')
    
    args = parser.parse_args()
    batch_project(args.input_dir, args.target_epsg, args.output, args.pattern)
```

### ArcPy: GDB建库脚本

```python
# scripts/arcpy/gdb_build.py
# GIS_SKILL V5.0 - ArcPy GDB建库脚本
# 依赖: ArcGIS Pro 3.6+

import arcpy
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def build_feature_dataset(gdb_path, dataset_name, spatial_ref=4549):
    """
    创建要素数据集
    Args:
        gdb_path: GDB路径
        dataset_name: 要素数据集名称(如DLG_Basic)
        spatial_ref: 坐标系WKID(默认4549=CGCS2000 3 Degree GK CM 120E)
    """
    sr = arcpy.SpatialReference(spatial_ref)
    
    ds_path = os.path.join(gdb_path, dataset_name)
    if not arcpy.Exists(ds_path):
        arcpy.management.CreateFeatureDataset(gdb_path, dataset_name, sr)
        logger.info(f"创建要素数据集: {dataset_name} (WKID: {spatial_ref})")
    
    return ds_path

def build_dlg_database(gdb_path, spatial_ref_wkid):
    """
    DLG标准建库
    自动创建GB/T 13923-2022定义的9大类图层
    """
    ds = build_feature_dataset(gdb_path, "DLG_Base", spatial_ref_wkid)
    
    layers = {
        "CTL_Point": "测量控制点(11000000)",
        "HYD_Polygon": "水系面(21000000)",
        "RES_Polygon": "居民地面(31000000)",
        "TRA_Line": "交通线(41000000)",
        "PIP_Line": "管线(51000000)",
        "BOU_Polygon": "境界面(61000000)",
        "TER_Polygon": "地貌面(71000000)",
        "VEG_Polygon": "植被面(81000000)",
        "ANO_Point": "地名点(91000000)",
    }
    
    for name, alias in layers.items():
        fc_path = os.path.join(ds, name)
        if not arcpy.Exists(fc_path):
            arcpy.management.CreateFeatureclass(ds, name, "POLYGON" if "Polygon" in name else "LINE" if "Line" in name else "POINT")
            logger.info(f"创建图层: {name} ({alias})")
    
    return ds
```
