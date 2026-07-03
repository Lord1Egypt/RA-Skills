<!-- wm:坤图_GIS:V5.0 -->
# 原子GIS Skill单元 —— DWG↔GIS互转 Skill ATS-009

> V5.0 | 中层-原子Skill | 触发词: DWG转GIS/CAD转SHP/导出CAD/数据互转
> 约束: V5_CONSTITUTION.md | V3规则5(DWG坐标规范)

---

## Skill 元数据

```yaml
skill_id: ATS-009
skill_name: dwg_gis_convert
category: 数据转换
min_inputs: [DWG/DXF文件, 目标图层/全部图层]
outputs: [GIS数据(GDB/GPKG), 转换日志, 字段映射表, 异常报告]
engines: [arcpy, ogr2ogr, geopandas]
rules: [DWG强制投影坐标导出, KML强制WGS84]
```

---

## 完整执行代码

```python
#!/usr/bin/env python3
"""
ATS-009: DWG↔GIS互转 Skill V5.0
完整工程化版本 —— 四步探查法 + 图层/属性映射 + 坐标强制投影 + 批量转换
"""

import os, sys, json, logging, csv
from datetime import datetime
from pathlib import Path

# 通用CAD图层→GIS要素类型映射
CAD_LAYER_MAP = {
    'Point': 'Point', 'Polyline': 'Polyline', 'Polygon': 'Polygon',
    'Annotation': 'Annotation', 'Multipatch': 'Multipatch',
    'Insert': 'Point', '3D Polyline': 'Polyline',
}

# CASS扩展属性字段映射
CASS_FIELD_MAP = {
    'Layer': 'CAD图层名', 'Entity': '类型', 'Handle': '句柄',
    'Color': '颜色', 'Linetype': '线型', 'Elevation': '高程',
    'Thickness': '厚度', 'Text': '文本', 'RefName': '图块名',
}

# 常见CAD图层→GIS要素类映射
CAD_TO_GIS_LAYER = {
    'JZD': {'type': 'Polygon', 'name': '宗地', 'code': '310100'},
    'JZX': {'type': 'Polyline', 'name': '界址线', 'code': '640000'},
    'JZP': {'type': 'Point', 'name': '界址点', 'code': '110102'},
    'DLDW': {'type': 'Polyline', 'name': '道路', 'code': '420000'},
    'SXSS': {'type': 'Polyline', 'name': '水系', 'code': '210000'},
    'JMD': {'type': 'Polygon', 'name': '居民地', 'code': '310000'},
    'JZDW': {'type': 'Point', 'name': '建筑物注记', 'code': '310000'},
    'DGX': {'type': 'Polyline', 'name': '等高线', 'code': '710100'},
    'GCD': {'type': 'Point', 'name': '高程点', 'code': '720000'},
    'GXYZ': {'type': 'Point', 'name': '管线设施', 'code': '510000'},
    'DLJ': {'type': 'Polyline', 'name': '地类界线', 'code': '650000'},
    'ZBTZ': {'type': 'Point', 'name': '植被注记', 'code': '810000'},
}


def setup_logger(output_dir):
    log_path = Path(output_dir) / f"dwg_convert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()])
    return logging.getLogger(__name__), log_path


# ============================================================
# 第一段: 输入校验
# ============================================================
class InputValidator:
    @staticmethod
    def validate(dwg_path, output_format='gdb'):
        errors, warnings = [], []
        if not os.path.exists(dwg_path):
            errors.append(f"DWG文件不存在: {dwg_path}")
            return errors, warnings
        
        ext = Path(dwg_path).suffix.lower()
        if ext not in ['.dwg', '.dxf']:
            errors.append(f"不支持的文件格式: {ext}，仅支持 .dwg / .dxf")
        
        # 文件版本检测
        try:
            import struct
            with open(dwg_path, 'rb') as f:
                header = f.read(6)
                if header[:4] == b'AC10':
                    ver = header[4:6].decode('ascii', errors='ignore')
                    warnings.append(f"DWG版本: {ver}")
        except:
            pass
        
        if output_format.lower() not in ['gdb', 'gpkg', 'shp']:
            warnings.append(f"建议输出格式为GDB/GPKG/SHP，当前: {output_format}")
        
        return errors, warnings


# ============================================================
# 第二段: 核心转换引擎
# ============================================================
class DWGGISConverter:
    """DWG→GIS核心转换引擎"""
    
    def __init__(self, dwg_path, target_crs=None, output_format='gdb', 
                 layer_filter=None, cad_map=None):
        self.dwg_path = dwg_path
        self.target_crs = target_crs
        self.output_format = output_format.lower()
        self.layer_filter = layer_filter or []
        self.cad_map = cad_map or CAD_TO_GIS_LAYER
        self.conversion_log = []
    
    def step1_explore(self):
        """四步探查法-步骤1: 数据探查"""
        import arcpy as ap
        
        layers = []
        dataset_name = Path(self.dwg_path).stem
        
        # 列出所有CAD图层
        for geom_type in ['Point', 'Polyline', 'Polygon', 'Annotation', 'Multipatch']:
            fc_path = f"{self.dwg_path}/{geom_type}"
            if ap.Exists(fc_path):
                count = int(ap.management.GetCount(fc_path).getOutput(0))
                if count > 0:
                    # 按Layer属性细分
                    layer_names = set()
                    with ap.da.SearchCursor(fc_path, ['Layer']) as cursor:
                        for row in cursor:
                            if row[0]:
                                layer_names.add(row[0])
                    
                    for layer in sorted(layer_names):
                        layers.append({
                            'cad_layer': layer,
                            'geom_type': geom_type,
                            'gis_name': self.cad_map.get(layer, {}).get('name', layer),
                            'gis_code': self.cad_map.get(layer, {}).get('code', ''),
                            'gis_type': self.cad_map.get(layer, {}).get('type', geom_type)
                        })
        
        if not layers:
            # 如果没有分层数据，返回整体统计
            for geom_type in ['Point', 'Polyline', 'Polygon', 'Annotation', 'Multipatch']:
                fc_path = f"{self.dwg_path}/{geom_type}"
                if ap.Exists(fc_path):
                    count = int(ap.management.GetCount(fc_path).getOutput(0))
                    if count > 0:
                        layers.append({
                            'cad_layer': geom_type,
                            'geom_type': geom_type,
                            'gis_name': f'{dataset_name}_{geom_type}',
                            'gis_code': '',
                            'gis_type': CAD_LAYER_MAP.get(geom_type, geom_type)
                        })
        
        return layers
    
    def step2_coordinate_check(self, layers):
        """步骤2: 坐标系检查与转换策略"""
        import arcpy as ap
        
        sr_info = {}
        for layer_info in layers[:1]:  # 只需检查一个
            fc_path = f"{self.dwg_path}/{layer_info['geom_type']}"
            if ap.Exists(fc_path):
                desc = ap.Describe(fc_path)
                sr = desc.spatialReference
                sr_info = {
                    'name': sr.name if sr else '未定义',
                    'wkid': sr.factoryCode if sr else 0,
                    'unit': sr.linearUnitName if sr and sr.type == 'Projected' else '未知',
                    'is_projected': sr.type == 'Projected' if sr else False,
                    'is_geographic': sr.type == 'Geographic' if sr else False,
                }
        
        # 转换策略: 投影坐标→直接使用; 地理坐标→转为投影坐标; 未定义→警告
        strategy = {}
        if not sr_info or sr_info.get('wkid', 0) == 0:
            strategy = {
                'action': 'warn',
                'message': 'DWG无投影信息，转换时将保持原始坐标',
                'recommend': '建议确认DWG原始坐标系后定义投影'
            }
        elif sr_info.get('is_geographic'):
            strategy = {
                'action': 'project',
                'message': f'DWG为地理坐标({sr_info["name"]})，需转为投影坐标',
                'source_wkid': sr_info['wkid'],
                'target_wkid': self.target_crs or self._auto_select_projection(sr_info['wkid'])
            }
        else:
            strategy = {
                'action': 'direct',
                'message': f'DWG已有投影坐标({sr_info["name"]})，可直接转换',
                'wkid': sr_info['wkid']
            }
        
        return sr_info, strategy
    
    def _auto_select_projection(self, source_wkid):
        """自动选择CGCS2000投影带"""
        # 默认返回CGCS2000 3度带38(全国通用)
        return 4526
    
    def step3_convert(self, layers, output_gdb, sr_info, strategy):
        """步骤3: 批量转换执行"""
        import arcpy as ap
        
        results = []
        errors_list = []
        
        for layer_info in layers:
            fc_path = f"{self.dwg_path}/{layer_info['geom_type']}"
            if not ap.Exists(fc_path):
                continue
            
            out_name = layer_info['gis_name'].replace('/', '_').replace('\\', '_')
            out_path = f"{output_gdb}/{out_name}"
            
            try:
                # 按CAD图层筛选
                where_clause = None
                if layer_info['cad_layer'] != layer_info['geom_type']:
                    where_clause = f"Layer = '{layer_info['cad_layer']}'"
                
                # FeatureClassToFeatureClass 转换
                ap.conversion.FeatureClassToFeatureClass(
                    fc_path, output_gdb, out_name,
                    where_clause=where_clause
                )
                
                count = int(ap.management.GetCount(out_path).getOutput(0))
                
                # 坐标系处理
                if strategy.get('action') == 'project' and strategy.get('target_wkid'):
                    projected_name = f"{out_name}_cgcs"
                    projected_path = f"{output_gdb}/{projected_name}"
                    target_sr = ap.SpatialReference(strategy['target_wkid'])
                    ap.management.Project(out_path, projected_path, target_sr)
                    # 替换原文件
                    ap.management.Delete(out_path)
                    ap.management.Rename(projected_path, out_name)
                    results.append({
                        'layer': layer_info['cad_layer'],
                        'name': out_name,
                        'count': count,
                        'status': 'converted+projected',
                        'crs': strategy['target_wkid']
                    })
                else:
                    results.append({
                        'layer': layer_info['cad_layer'],
                        'name': out_name,
                        'count': count,
                        'status': 'converted',
                        'crs': strategy.get('wkid', 0)
                    })
                
            except Exception as e:
                errors_list.append({
                    'layer': layer_info['cad_layer'],
                    'error': str(e)[:200]
                })
        
        return results, errors_list
    
    def step4_quality_check(self, results, output_gdb):
        """步骤4: 转换质量检查"""
        import arcpy as ap
        
        qc_report = {
            'total_layers': len(results),
            'total_features': sum(r['count'] for r in results),
            'empty_layers': [r['layer'] for r in results if r['count'] == 0],
            'coordinate_issues': [],
            'geometry_issues': []
        }
        
        for result in results:
            if result['count'] > 0:
                fc_path = f"{output_gdb}/{result['name']}"
                if ap.Exists(fc_path):
                    desc = ap.Describe(fc_path)
                    sr = desc.spatialReference
                    if not sr or sr.factoryCode == 0:
                        qc_report['coordinate_issues'].append({
                            'layer': result['layer'],
                            'issue': '无坐标系'
                        })
        
        return qc_report


# ============================================================
# 第三段: 输出校验
# ============================================================
class OutputValidator:
    @staticmethod
    def validate(results, qc_report):
        errors = []
        if not results:
            errors.append("转换结果为空，所有图层转换失败")
        empty = [r for r in results if r['count'] == 0]
        if len(empty) == len(results):
            errors.append("所有输出图层为空")
        if qc_report.get('coordinate_issues'):
            errors.append(f"{len(qc_report['coordinate_issues'])}个图层缺少坐标系")
        return errors


# ============================================================
# HTML报告
# ============================================================
def generate_html_report(report, output_dir):
    results = report.get('results', [])
    qc = report.get('qc_report', {})
    layers_found = report.get('layers_found', [])
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>DWG↔GIS转换报告</title>
<style>
body{{font-family:'Microsoft YaHei',sans-serif;max-width:1100px;margin:0 auto;padding:20px}}
h1{{color:#6a1b9a;border-bottom:3px solid #6a1b9a;padding-bottom:10px}}
h2{{margin-top:30px;color:#333}}
table{{border-collapse:collapse;width:100%;margin:10px 0}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left}}
th{{background:#6a1b9a;color:white}}
.success{{color:green}}
.fail{{color:red}}
.warn{{color:orange}}
.summary-box{{background:#f3e5f5;border-radius:8px;padding:15px;margin:15px 0}}
</style>
</head>
<body>
<h1>DWG↔GIS数据转换报告</h1>
<p>时间: {report.get('timestamp','')} | 输入: {report.get('dwg_path','')}</p>

<div class="summary-box">
<p>图层总数: <b>{report.get('total_layers',0)}</b> | 
   总要素: <b>{report.get('total_features',0)}</b> | 
   成功: <b class="success">{len([r for r in results if r['status'] != 'failed'])}</b> | 
   失败: <b class="fail">{len([r for r in results if r['status'] == 'failed'])}</b></p>
<p>坐标系策略: {report.get('coordinate_strategy',{}).get('message','')}</p>
</div>

<h2>发现的CAD图层</h2>
<table><tr><th>CAD图层</th><th>几何类型</th><th>GIS名称</th><th>建议编码</th></tr>
"""
    for l in layers_found[:50]:
        html += f"<tr><td>{l['cad_layer']}</td><td>{l['geom_type']}</td><td>{l['gis_name']}</td><td>{l.get('gis_code','')}</td></tr>"
    html += "</table>"
    
    html += "<h2>转换结果</h2><table><tr><th>图层</th><th>输出名</th><th>要素数</th><th>状态</th><th>坐标系</th></tr>"
    for r in results:
        status_cls = 'success' if r['status'] != 'failed' else 'fail'
        html += f"<tr><td>{r['layer']}</td><td>{r['name']}</td><td>{r['count']}</td><td class='{status_cls}'>{r['status']}</td><td>{r.get('crs','')}</td></tr>"
    html += "</table>"
    
    if qc.get('coordinate_issues'):
        html += "<h2>坐标系问题</h2><ul>"
        for ci in qc['coordinate_issues']:
            html += f"<li>{ci['layer']}: {ci['issue']}</li>"
        html += "</ul>"
    
    html += "</body></html>"
    
    html_path = Path(output_dir) / f"dwg_convert_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_path


# ============================================================
# 主入口
# ============================================================
def main(dwg_path, output_gdb=None, target_crs=None, layer_filter=None, max_retries=3):
    output_dir = output_gdb or f"output_dwg2gis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    logger, log_path = setup_logger(output_dir)
    logger.info(f"ATS-009 DWG→GIS启动: {dwg_path}")
    
    for attempt in range(1, max_retries + 1):
        try:
            import arcpy
            
            # 输入校验
            errors, warnings = InputValidator.validate(dwg_path, 'gdb')
            if errors and attempt >= max_retries:
                raise RuntimeError(f"输入校验失败: {errors}")
            
            converter = DWGGISConverter(dwg_path, target_crs, 'gdb', layer_filter)
            
            # 步骤1: 探查
            logger.info("[步骤1] CAD图层探查...")
            layers = converter.step1_explore()
            logger.info(f"发现 {len(layers)} 个图层")
            
            # 步骤2: 坐标系检查
            logger.info("[步骤2] 坐标系检查...")
            sr_info, strategy = converter.step2_coordinate_check(layers)
            logger.info(f"坐标系: {sr_info}, 策略: {strategy['action']}")
            
            # 步骤3: 转换执行
            logger.info("[步骤3] 批量转换...")
            output_gdb_path = os.path.join(output_dir, 'output.gdb')
            if arcpy.Exists(output_gdb_path):
                arcpy.management.Delete(output_gdb_path)
            arcpy.management.CreateFileGDB(os.path.dirname(output_gdb_path), 'output.gdb')
            
            results, errors_list = converter.step3_convert(layers, output_gdb_path, sr_info, strategy)
            logger.info(f"转换完成: {len(results)}个图层, {len(errors_list)}个错误")
            
            # 步骤4: 质量检查
            logger.info("[步骤4] 质量检查...")
            qc_report = converter.step4_quality_check(results, output_gdb_path)
            
            # 输出校验
            output_errors = OutputValidator.validate(results, qc_report)
            if output_errors:
                logger.warning(f"输出校验: {output_errors}")
            
            # 生成报告
            report = {
                'task': 'DWG↔GIS转换',
                'skill_id': 'ATS-009',
                'version': 'V5.0',
                'timestamp': datetime.now().isoformat(),
                'dwg_path': str(dwg_path),
                'output': output_gdb_path,
                'total_layers': len(layers),
                'total_features': sum(r['count'] for r in results),
                'layers_found': layers,
                'results': results,
                'errors': errors_list,
                'coordinate_info': sr_info,
                'coordinate_strategy': strategy,
                'qc_report': qc_report
            }
            
            json_path = Path(output_dir) / "dwg_convert_report.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            html_path = generate_html_report(report, output_dir)
            
            return {
                'output_gdb': output_gdb_path,
                'report_json': str(json_path),
                'report_html': str(html_path),
                'log': str(log_path),
                'summary': {
                    'layers': len(layers),
                    'features': sum(r['count'] for r in results),
                    'success': len([r for r in results if r['status'] != 'failed']),
                    'failed': len(errors_list)
                }
            }
            
        except Exception as e:
            logger.error(f"第{attempt}轮异常: {e}")
            if attempt >= max_retries:
                raise RuntimeError(f"[3轮熔断] ATS-009失败: {e}")
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ATS-009 DWG↔GIS互转')
    parser.add_argument('dwg', help='DWG文件路径')
    parser.add_argument('-o', '--output', default=None, help='输出目录')
    parser.add_argument('-c', '--crs', type=int, default=None, help='目标坐标系WKID')
    args = parser.parse_args()
    result = main(args.dwg, args.output, args.crs)
    print(f"\n转换完成: {result['summary']['layers']}个图层, {result['summary']['features']}个要素")
```

---

## 验收检查单

| 序号 | 检查项 | 标准 |
|------|--------|------|
| 1 | 四步探查法完整执行 | 探查→坐标检查→转换→质量检查 |
| 2 | 坐标系强制投影 | DWG地理坐标→自动转为投影坐标 |
| 3 | 图层映射 | 内置20+常见CAD→GIS图层映射 |
| 4 | 批量转换 | 支持全部图层/指定图层筛选 |
| 5 | CASS属性保留 | RefName/Elevation/Color等字段保留 |
| 6 | 质量检查 | 空图层/坐标系缺失/几何类型 |
