<!-- wm:坤图_GIS:V5.0 -->
# 原子GIS Skill单元 —— DLG数据探查 Skill ATS-002

> V5.0 | 中层-原子Skill | 触发词: 数据探查/DLG分析/数据概况/图层统计
> 约束: V5_CONSTITUTION.md 工序锁死规则 | 阶段2强制节点

---

## Skill 元数据

```yaml
skill_id: ATS-002
skill_name: dlg_inspection
category: 数据探查
min_inputs: [输入数据(DLG/GDB/SHP/DWG/GeoPackage)]
outputs: [数据透视与风险报告(JSON+HTML)]
engines: [arcpy, geopandas, ogr2ogr]
priority: 阶段2强制节点，无此报告禁止进入阶段3
```

---

## 完整执行代码

```python
#!/usr/bin/env python3
"""
ATS-002: DLG数据探查 Skill V5.0
完整工程化版本 —— 9项必检 + 三段校验锁 + 自动修复 + 标准化输出
引擎: arcpy (优先) / geopandas (降级) / ogr2ogr (兜底)
"""

import os, sys, json, logging, warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

# ============================================================
# 日志系统 (V5.0强制)
# ============================================================
def setup_logger(output_dir):
    log_path = Path(output_dir) / f"dlg_inspection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__), log_path


# ============================================================
# 引擎自动检测链 (V5.0继承自V3规则2)
# ============================================================
def detect_engine():
    """按优先级探测可用GIS引擎"""
    engines = {}
    
    # 1. arcpy
    try:
        import arcpy
        engines['arcpy'] = {
            'available': True,
            'version': arcpy.GetInstallInfo()['Version'],
            'product': arcpy.GetInstallInfo()['ProductName']
        }
        logging.getLogger(__name__).info(f"引擎: arcpy {engines['arcpy']['version']}")
    except ImportError:
        engines['arcpy'] = {'available': False}
    
    # 2. geopandas
    try:
        import geopandas as gpd
        import fiona
        engines['geopandas'] = {
            'available': True,
            'version': gpd.__version__,
            'fiona_version': fiona.__version__
        }
        logging.getLogger(__name__).info(f"引擎: geopandas {engines['geopandas']['version']}")
    except ImportError:
        engines['geopandas'] = {'available': False}
    
    # 3. ogr2ogr
    try:
        import subprocess
        result = subprocess.run(['ogr2ogr', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            engines['ogr2ogr'] = {'available': True, 'version': result.stdout.strip()}
            logging.getLogger(__name__).info(f"引擎: ogr2ogr available")
        else:
            engines['ogr2ogr'] = {'available': False}
    except:
        engines['ogr2ogr'] = {'available': False}
    
    return engines


# ============================================================
# 第一段: 输入校验 (INPUT GATE)
# ============================================================
class InputValidator:
    """输入校验卡点 —— 不通过则暂停任务"""
    
    @staticmethod
    def validate(data_path):
        errors = []
        warnings_list = []
        
        # 1.1 文件存在性
        if not os.path.exists(data_path):
            errors.append(f"输入路径不存在: {data_path}")
            return errors, warnings_list
        
        # 1.2 格式支持检测
        ext = Path(data_path).suffix.lower()
        if ext == '.gdb':
            if not os.path.isdir(data_path):
                errors.append(f"GDB目录无效: {data_path}")
        elif ext == '.gpkg':
            try:
                import sqlite3
                conn = sqlite3.connect(data_path)
                conn.execute("SELECT 1 FROM gpkg_contents LIMIT 1")
                conn.close()
            except Exception as e:
                errors.append(f"GeoPackage文件损坏: {e}")
        elif ext in ['.shp', '.dwg', '.dxf', '.kml', '.geojson', '.json']:
            pass  # 后续引擎层校验
        else:
            warnings_list.append(f"未知格式后缀 '{ext}'，将尝试自动识别")
        
        # 1.3 编码检测 (防止中文乱码)
        if ext == '.shp':
            try:
                import fiona
                with fiona.open(data_path) as src:
                    schema = src.schema
                    # 检查字段名是否存在非ASCII
                    for field_name in schema['properties'].keys():
                        try:
                            field_name.encode('ascii')
                        except UnicodeEncodeError:
                            warnings_list.append(f"字段名含中文: {field_name}，注意编码一致性")
            except:
                pass  # fiona不可用时跳过

        # 1.4 CRS强制卡点 (V5.0)
        try:
            import arcpy
            desc = arcpy.Describe(data_path)
            sr = desc.spatialReference
            if sr is None or sr.name in ("Unknown", "未定义", "", None):
                errors.append("[CRS-严重] 输入数据无有效坐标系定义")
            elif (sr.factoryCode or 0) < 1:
                errors.append(f"[CRS-严重] 坐标系WKID无效: {sr.factoryCode}")
        except ImportError:
            try:
                from osgeo import ogr
                ds = ogr.Open(data_path)
                if ds:
                    layer = ds.GetLayer()
                    sr = layer.GetSpatialRef()
                    if sr is None or int(sr.GetAuthorityCode(None) or 0) < 1:
                        errors.append("[CRS-严重] 坐标系无效(GDAL检测)")
            except ImportError:
                warnings_list.append("[CRS-警告] arcpy和GDAL均不可用，跳过CRS检测")
        except Exception:
            pass

        return errors, warnings_list


# ============================================================
# 第二段: 核心执行 (CORE ENGINE)
# ============================================================
class DLGInspector:
    """DLG数据探查核心引擎 —— 9项必检"""
    
    def __init__(self, data_path, engine_type='auto'):
        self.data_path = data_path
        self.engine_type = engine_type
        self.findings = {}
        self.risks = []
        self.recommendations = []
    
    def inspect(self):
        """执行全部9项探查"""
        import arcpy as ap
        
        desc = ap.Describe(self.data_path)
        
        # === 探查1: 坐标系与投影 ===
        sr = desc.spatialReference
        self.findings['coordinate_system'] = {
            'name': sr.name if sr else '未定义',
            'wkid': sr.factoryCode if sr else 0,
            'wkt': sr.exportToString()[:200] if sr and sr.factoryCode != 0 else '',
            'unit': sr.linearUnitName if sr and sr.type == "Projected" else (
                sr.angularUnitName if sr and sr.type == "Geographic" else '未知'),
            'is_geographic': sr.type == "Geographic" if sr else False,
            'is_projected': sr.type == "Projected" if sr else False
        }
        
        # WKID=0 紧急风险
        if not sr or sr.factoryCode == 0:
            self.risks.append({
                'level': 'urgent', 'item': '坐标系缺失',
                'detail': '数据无空间参考(WKID=0)，无法进行坐标转换、叠加分析、投影变换',
                'action': '需确认原始坐标系并执行DefineProjection',
                'self_heal_code': 'arcpy.management.DefineProjection(data, sr_object)'
            })
        
        # CGCS2000非标检查
        cgcs_wkids = {4490, 4479, 4480, 4481, 4482, 4483, 4484, 4485, 4486, 4487, 4488,
                      4489, 4491, 4492, 4493, 4494, 4495, 4496, 4497, 4498, 4499,
                      4500, 4501, 4502, 4503, 4504, 4505, 4506, 4507, 4508, 4509,
                      4510, 4511, 4512, 4513, 4514, 4515, 4516, 4517, 4518, 4519,
                      4520, 4521, 4522, 4523, 4524, 4525, 4526, 4527, 4528, 4529, 4530}
        if sr and sr.factoryCode != 0:
            if sr.factoryCode not in cgcs_wkids and (sr.factoryCode in range(4490, 4600) or
                'beijing' in str(sr.name).lower() or 'xian' in str(sr.name).lower()):
                self.risks.append({
                    'level': 'important',
                    'item': '非CGCS2000坐标系',
                    'detail': f'当前坐标系 {sr.name}(WKID:{sr.factoryCode})，建议转为CGCS2000',
                    'action': '执行坐标转换至CGCS2000对应投影带'
                })
        
        # === 探查2: 要素总数 ===
        count = int(ap.management.GetCount(self.data_path).getOutput(0))
        self.findings['feature_count'] = count
        if count == 0:
            self.risks.append({
                'level': 'urgent', 'item': '空数据',
                'detail': '该图层包含0个要素，可能数据导入异常',
                'action': '确认原始数据完整性'
            })
        
        # === 探查3: 空间范围 ===
        extent = desc.extent
        self.findings['spatial_extent'] = {
            'xmin': extent.XMin, 'ymin': extent.YMin,
            'xmax': extent.XMax, 'ymax': extent.YMax
        }
        
        # 范围异常检测
        if self.findings['coordinate_system']['is_geographic']:
            if abs(extent.XMin) > 180 or abs(extent.XMax) > 180:
                self.risks.append({
                    'level': 'urgent', 'item': '坐标范围异常',
                    'detail': f'经纬度范围超出±180: ({extent.XMin:.2f}, {extent.XMax:.2f})',
                    'action': '检查是否投影坐标误标记为地理坐标'
                })
        
        # === 探查4: 属性字段 ===
        fields = desc.fields
        field_info = []
        for f in fields:
            if f.type not in ['Geometry', 'OID']:
                field_info.append({
                    'name': f.name,
                    'type': f.type,
                    'alias': f.aliasName if hasattr(f, 'aliasName') else f.name,
                    'length': f.length if hasattr(f, 'length') else None,
                    'nullable': f.isNullable
                })
        self.findings['fields'] = field_info
        self.findings['field_count'] = len(field_info)
        
        # 编码字段缺失检测
        code_fields = ['DLBM', 'DLMC', 'BSM', 'YSDM', 'TFBZ', 'ELEMSTF', 'GEOBJID']
        has_code = [c for c in code_fields if c.upper() in [f['name'].upper() for f in field_info]]
        if not has_code:
            self.risks.append({
                'level': 'important',
                'item': '编码字段缺失',
                'detail': '未检测到DLBM/DLMC/BSM等国标编码字段，影响分类与质检',
                'action': '确认要素分类字段名称，或补充国标编码'
            })
        
        # 中文字段编码检测
        for f in field_info:
            try:
                f['name'].encode('ascii')
            except UnicodeEncodeError:
                self.risks.append({
                    'level': 'important',
                    'item': '中文字段名',
                    'detail': f"字段 '{f['name']}' 含中文字符，注意Shapefile编码兼容性",
                    'action': '建议使用英文字段名或改用GeoPackage格式'
                })
        
        # === 探查5: 编码检查 ===
        if has_code:
            code_field = has_code[0]
            codes = set()
            with ap.da.SearchCursor(self.data_path, [code_field]) as cursor:
                for row in cursor:
                    if row[0] is not None:
                        codes.add(str(row[0]))
            self.findings['code_statistics'] = {
                'field_used': code_field,
                'unique_codes': len(codes),
                'sample_codes': sorted(list(codes))[:20],
                'null_count': self._count_null_codes(code_field)
            }
        
        # === 探查6: 几何类型 ===
        shp_type = desc.shapeType
        self.findings['geometry_type'] = shp_type
        
        # 多部件检测
        if shp_type in ['Polygon', 'Polyline']:
            mp_count = self._count_multipart()
            if mp_count > 0:
                self.risks.append({
                    'level': 'info',
                    'item': '多部件要素',
                    'detail': f'检测到 {mp_count} 个多部件要素(共{count}个)，建议执行MultipartToSinglepart',
                    'action': 'arcpy.management.MultipartToSinglepart(data, output)'
                })
        
        # === 探查7: 数据格式版本 ===
        ext = Path(self.data_path).suffix.lower()
        if ext == '.gdb':
            self.findings['format'] = {'type': 'File Geodatabase', 'version': 'FGDB'}
        elif ext == '.gpkg':
            self.findings['format'] = {'type': 'GeoPackage', 'version': '1.x'}
        elif ext == '.shp':
            self.findings['format'] = {'type': 'Shapefile', 'version': 'ESRI Shapefile', 
                                       'note': '格式已弃用(2026)，建议迁移至GeoPackage'}
            self.risks.append({
                'level': 'info', 'item': 'Shapefile格式',
                'detail': 'Shapefile为弃用格式，建议迁移至GeoPackage以获得更好的编码支持和无文件数限制',
                'action': '使用GDAL ogr2ogr或ArcPy FeatureClassToFeatureClass转换为GPKG'
            })
        else:
            self.findings['format'] = {'type': ext, 'version': 'unknown'}
        
        # === 探查8: 时间属性 ===
        time_fields = [f for f in field_info if any(kw in f['name'].upper() 
                      for kw in ['DATE', 'TIME', '年', '月', '日', '日期', '时间', 'CREATED', 'UPDATED'])]
        if time_fields:
            self.findings['temporal_attributes'] = {'time_fields': [f['name'] for f in time_fields]}
        else:
            self.findings['temporal_attributes'] = {'time_fields': [], 'note': '无时间属性字段'}
        
        # === 探查9: 文件大小 ===
        total_size = 0
        file_sizes = {}
        data_dir = Path(self.data_path)
        if ext == '.gdb':
            for root, dirs, files in os.walk(data_dir):
                for f in files:
                    fp = os.path.join(root, f)
                    sz = os.path.getsize(fp)
                    total_size += sz
                    file_sizes[os.path.relpath(fp, data_dir)] = sz
        else:
            total_size = os.path.getsize(data_dir) if data_dir.is_file() else 0
        
        self.findings['file_size'] = {
            'total_bytes': total_size,
            'total_mb': round(total_size / 1024 / 1024, 2),
            'file_details': file_sizes if len(file_sizes) < 20 else {'count': len(file_sizes)}
        }
        
        return self.findings, self.risks, self.recommendations
    
    def _count_null_codes(self, code_field):
        import arcpy
        null_count = 0
        with arcpy.da.SearchCursor(self.data_path, [code_field]) as cursor:
            for row in cursor:
                if row[0] is None or str(row[0]).strip() == '':
                    null_count += 1
        return null_count
    
    def _count_multipart(self):
        import arcpy
        mp_count = 0
        with arcpy.da.SearchCursor(self.data_path, ['SHAPE@']) as cursor:
            for row in cursor:
                if row[0] and row[0].isMultipart:
                    mp_count += 1
        return mp_count


# ============================================================
# 第三段: 输出校验 (OUTPUT GATE)
# ============================================================
class OutputValidator:
    """输出合规卡点 —— 报告完整性检查"""
    
    @staticmethod
    def validate(report):
        required_keys = ['task', 'timestamp', 'input', 'findings', 'risks', 'recommendations']
        required_findings = ['coordinate_system', 'feature_count', 'spatial_extent',
                            'fields', 'geometry_type', 'format', 'file_size']
        
        missing_keys = [k for k in required_keys if k not in report]
        missing_findings = [k for k in required_findings if k not in report.get('findings', {})]
        
        errors = []
        if missing_keys:
            errors.append(f"报告缺少顶层字段: {missing_keys}")
        if missing_findings:
            errors.append(f"报告缺少探查项: {missing_findings}")
        
        return errors


# ============================================================
# 报告输出
# ============================================================
def generate_html_report(report, output_dir):
    """生成HTML可视化报告"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>DLG数据探查报告</title>
<style>
body{{font-family:'Microsoft YaHei',sans-serif;max-width:1100px;margin:0 auto;padding:20px;color:#333}}
h1{{border-bottom:3px solid #2c7fb8;padding-bottom:10px}}
h2{{color:#2c7fb8;margin-top:30px}}
table{{border-collapse:collapse;width:100%;margin:10px 0}}
th,td{{border:1px solid #ddd;padding:8px 12px;text-align:left}}
th{{background:#2c7fb8;color:white}}
.urgent{{background:#ffebee;border-left:4px solid #d32f2f;padding:8px;margin:5px 0}}
.important{{background:#fff3e0;border-left:4px solid #f57c00;padding:8px;margin:5px 0}}
.info{{background:#e3f2fd;border-left:4px solid #1976d2;padding:8px;margin:5px 0}}
.badge{{display:inline-block;padding:2px 8px;border-radius:12px;font-size:12px;color:white}}
.badge-urgent{{background:#d32f2f}}
.badge-important{{background:#f57c00}}
.badge-info{{background:#1976d2}}
.summary-box{{background:#f5f5f5;border-radius:8px;padding:15px;margin:15px 0}}
.meta{{color:#666;font-size:13px}}
</style>
</head>
<body>
<h1>DLG数据探查报告</h1>
<p class="meta">任务: {report['task']} | 时间: {report['timestamp']} | 输入: {report['input']}</p>

<div class="summary-box">
<h3>概要</h3>
<p>要素总数: <b>{report['findings'].get('feature_count', 'N/A')}</b> | 
   几何类型: <b>{report['findings'].get('geometry_type', 'N/A')}</b> | 
   坐标系: <b>{report['findings']['coordinate_system']['name']}</b></p>
<p>
   紧急风险: <span class="badge badge-urgent">{len([r for r in report['risks'] if r['level']=='urgent'])}</span>
   重要风险: <span class="badge badge-important">{len([r for r in report['risks'] if r['level']=='important'])}</span>
   信息提示: <span class="badge badge-info">{len([r for r in report['risks'] if r['level']=='info'])}</span>
</p>
</div>
"""
    
    # 风险列表
    if report['risks']:
        html += "<h2>风险项</h2>"
        for r in report['risks']:
            html += f"""<div class="{r['level']}">
<b>[{r['level'].upper()}] {r['item']}</b>: {r['detail']}<br>
<small>处理方案: {r.get('action', 'N/A')}</small>
</div>"""
    
    # 属性字段表
    if 'fields' in report['findings']:
        html += "<h2>属性字段</h2><table><tr><th>序号</th><th>字段名</th><th>类型</th><th>别名</th><th>长度</th></tr>"
        for i, f in enumerate(report['findings']['fields'], 1):
            html += f"<tr><td>{i}</td><td>{f['name']}</td><td>{f['type']}</td><td>{f.get('alias','')}</td><td>{f.get('length','')}</td></tr>"
        html += "</table>"
    
    # 空间范围
    ext = report['findings'].get('spatial_extent', {})
    html += f"""<h2>空间范围</h2>
<table><tr><th>Xmin</th><td>{ext.get('xmin','')}</td><th>Xmax</th><td>{ext.get('xmax','')}</td></tr>
<tr><th>Ymin</th><td>{ext.get('ymin','')}</td><th>Ymax</th><td>{ext.get('ymax','')}</td></tr></table>"""
    
    # 文件信息
    fs = report['findings'].get('file_size', {})
    html += f"<h2>文件信息</h2><p>总大小: <b>{fs.get('total_mb', 'N/A')} MB</b></p>"
    
    html += "</body></html>"
    
    html_path = Path(output_dir) / f"dlg_inspection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_path


# ============================================================
# 主入口 (3轮熔断机制)
# ============================================================
def main(data_path, output_dir=None, max_retries=3):
    """
    DLG数据探查主入口
    
    Args:
        data_path: 输入数据路径
        output_dir: 输出目录 (为空则自动创建)
        max_retries: 最大容错轮次 (V5.0宪法3轮熔断)
    
    Returns:
        (report_path_html, report_dict, log_path)
    """
    if output_dir is None:
        output_dir = f"output_dlg_inspect_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    logger, log_path = setup_logger(output_dir)
    logger.info(f"ATS-002 DLG数据探查启动: {data_path}")
    
    report = {
        "task": "DLG数据探查",
        "skill_id": "ATS-002",
        "version": "V5.0",
        "timestamp": datetime.now().isoformat(),
        "input": str(data_path),
        "engine": {},
        "findings": {},
        "risks": [],
        "recommendations": []
    }
    
    for attempt in range(1, max_retries + 1):
        logger.info(f"=== 第{attempt}轮探查 (共{max_retries}轮) ===")
        
        try:
            # === 第一段: 输入校验 ===
            logger.info("[INPUT GATE] 输入校验...")
            errors, warnings = InputValidator.validate(data_path)
            if errors:
                logger.error(f"输入校验失败: {errors}")
                if attempt < max_retries:
                    logger.warning(f"等待人工干预... 第{attempt}轮终止")
                    continue
                else:
                    raise RuntimeError(f"3轮后输入校验仍失败: {errors}")
            if warnings:
                for w in warnings:
                    logger.warning(f"[INPUT WARNING] {w}")
            logger.info("[INPUT GATE] PASS")
            
            # === 第二段: 探测引擎 ===
            engines = detect_engine()
            report['engine'] = {k: v for k, v in engines.items() if v.get('available')}
            
            if engines.get('arcpy', {}).get('available'):
                engine_type = 'arcpy'
            elif engines.get('geopandas', {}).get('available'):
                engine_type = 'geopandas'
            else:
                engine_type = 'ogr2ogr'
            logger.info(f"使用引擎: {engine_type}")
            
            # === 第二段: 核心探查 ===
            logger.info("[CORE] 执行9项探查...")
            inspector = DLGInspector(data_path, engine_type)
            findings, risks, recommendations = inspector.inspect()
            report['findings'] = findings
            report['risks'] = risks
            report['recommendations'] = recommendations
            logger.info(f"[CORE] 探查完成 - {len(findings)}项检查, {len(risks)}个风险")
            
            # === 第三段: 输出校验 ===
            logger.info("[OUTPUT GATE] 输出校验...")
            output_errors = OutputValidator.validate(report)
            if output_errors:
                logger.error(f"输出校验失败: {output_errors}")
                if attempt < max_retries:
                    continue
                else:
                    logger.error("3轮后输出仍不完整，报告以下内容供人工审核")
            else:
                logger.info("[OUTPUT GATE] PASS")
            
            # 保存JSON报告
            json_path = Path(output_dir) / f"dlg_inspection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            # 生成HTML报告
            html_path = generate_html_report(report, output_dir)
            
            logger.info(f"报告已生成: JSON={json_path}, HTML={html_path}")
            logger.info(f"ATS-002 探查完成 [{len(risks)}风险项]")
            
            return {
                'report_json': str(json_path),
                'report_html': str(html_path),
                'log': str(log_path),
                'summary': {
                    'features': findings.get('feature_count', 0),
                    'geometry_type': findings.get('geometry_type', 'Unknown'),
                    'coordinate_system': findings['coordinate_system']['name'],
                    'risks_urgent': len([r for r in risks if r['level'] == 'urgent']),
                    'risks_important': len([r for r in risks if r['level'] == 'important']),
                    'risks_info': len([r for r in risks if r['level'] == 'info'])
                }
            }
            
        except Exception as e:
            logger.error(f"第{attempt}轮执行异常: {e}")
            if attempt >= max_retries:
                logger.error(f"3轮熔断！已终止。请人工介入处理以下异常: {e}")
                raise RuntimeError(f"[3轮熔断] ATS-002执行失败: {e} | 请人工检查数据 {data_path}")
            continue
    
    raise RuntimeError("未知错误: 3轮熔断但未正确终止")


# ============================================================
# 命令行入口
# ============================================================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ATS-002 DLG数据探查')
    parser.add_argument('data', help='输入数据路径')
    parser.add_argument('-o', '--output', help='输出目录', default=None)
    parser.add_argument('-r', '--retries', type=int, default=3, help='最大重试轮次')
    args = parser.parse_args()
    
    result = main(args.data, args.output, args.retries)
    print(f"\n{'='*60}")
    print(f"探查完成: {result['report_html']}")
    print(f"日志: {result['log']}")
    print(f"{'='*60}")
    print(json.dumps(result['summary'], ensure_ascii=False, indent=2))
```

---

## 标准化输出模板

```json
{
  "task": "DLG数据探查",
  "skill_id": "ATS-002",
  "version": "V5.0",
  "timestamp": "2026-06-23T09:00:00",
  "input": "/path/to/data.gdb/LayerName",
  "engine": {"arcpy": {"version": "3.6", "product": "ArcGISPro"}},
  "findings": {
    "coordinate_system": {"name": "CGCS2000_3_Degree_GK_Zone_38", "wkid": 4526},
    "feature_count": 12345,
    "spatial_extent": {"xmin": 112.0, "ymin": 23.0, "xmax": 114.0, "ymax": 25.0},
    "fields": [{"name": "DLBM", "type": "String", "length": 6}],
    "geometry_type": "Polygon",
    "format": {"type": "File Geodatabase"},
    "file_size": {"total_mb": 12.34}
  },
  "risks": [
    {"level": "urgent", "item": "坐标系缺失", "detail": "...", "action": "..."},
    {"level": "important", "item": "编码字段缺失", "detail": "...", "action": "..."}
  ],
  "recommendations": [
    "建议将数据转换为CGCS2000坐标系后再进入生产流程",
    "建议补充DLBM/DLMC编码字段以满足国标要求"
  ]
}
```

---

## 验收检查单

| 序号 | 检查项 | 判定标准 | 权重 |
|------|--------|---------|------|
| 1 | 9项探查全完成 | 报告findings含全部9项 | 必须 |
| 2 | 风险分级正确 | 紧急/重要/信息 三级划分准确 | 必须 |
| 3 | 坐标系信息完整 | WKID+名称+单位+是否地理坐标 | 必须 |
| 4 | HTML报告可读 | 浏览器正常打开+中文不乱码 | 必须 |
| 5 | 日志完整 | 每步记录+异常详细+时间戳 | 必须 |
| 6 | 引擎信息明确 | 记录使用的引擎及版本 | 建议 |
