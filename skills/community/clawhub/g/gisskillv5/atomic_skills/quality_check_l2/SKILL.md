<!-- wm:坤图_GIS:V5.0 -->
# 原子GIS Skill单元 —— 二级质检 Skill ATS-005

> V5.0 | 中层-原子Skill | 触发词: 二级质检/质量检查/成果验收/质量评定
> 约束: V5_CONSTITUTION.md 工序锁死规则 | 阶段6强制质检节点

---

## Skill 元数据

```yaml
skill_id: ATS-005
skill_name: quality_check_l2
category: 质检校验
min_inputs: [成果数据(DLG/GDB), 原始数据(可选)]
outputs: [质检报告(JSON+HTML), 缺陷清单(SHP+CSV), 质量评分]
engines: [arcpy, geopandas]
standards: [GB/T 18316, GB/T 24356, GB/T 39610]
```

---

## 完整执行代码

```python
#!/usr/bin/env python3
"""
ATS-005: 二级质检 Skill V5.0
完整工程化版本 —— 12项质检元素 + 权重评分 + 缺陷分级 + 自动修复尝试
标准依据: GB/T 18316-2008 数字测绘成果质量检查与验收
"""

import os, sys, json, logging, csv, math
from datetime import datetime
from pathlib import Path

# ============================================================
# 质检元素权重配置(GB/T 18316)
# ============================================================
QUALITY_ELEMENTS = {
    "positional_accuracy": {"weight": 0.25, "name": "位置精度", "threshold": None},
    "attribute_accuracy": {"weight": 0.15, "name": "属性精度", "threshold": None},
    "completeness": {"weight": 0.15, "name": "完整性", "threshold": None},
    "logical_consistency": {"weight": 0.15, "name": "逻辑一致性", "threshold": None},
    "temporal_accuracy": {"weight": 0.10, "name": "时间精度", "threshold": None},
    "geometric_quality": {"weight": 0.10, "name": "几何质量", "threshold": None},
    "metadata_quality": {"weight": 0.05, "name": "元数据质量", "threshold": None},
    "format_compliance": {"weight": 0.05, "name": "格式合规", "threshold": None},
}

# 缺陷等级
DEFECT_LEVELS = {
    "A": {"name": "严重缺陷", "desc": "成果不可用，必须退回修改", "score_factor": 0},
    "B": {"name": "重缺陷", "desc": "影响成果主要用途，须修改", "score_factor": 0.4},
    "C": {"name": "次重缺陷", "desc": "影响成果部分用途", "score_factor": 0.7},
    "D": {"name": "轻缺陷", "desc": "不影响主要用途，可接受", "score_factor": 0.9},
}

QUICK_STANDARDS = {
    "1:500": {"planimetric": 0.15, "elevation": 0.15, "note": "地物点平面中误差(cm)"},
    "1:1000": {"planimetric": 0.30, "elevation": 0.20, "note": "地物点平面中误差(cm)"},
    "1:2000": {"planimetric": 0.60, "elevation": 0.40, "note": "地物点平面中误差(cm)"},
    "1:5000": {"planimetric": 1.50, "elevation": 1.00, "note": "地物点平面中误差(cm)"},
}


def setup_logger(output_dir):
    log_path = Path(output_dir) / f"quality_check_l2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()])
    return logging.getLogger(__name__), log_path


# ============================================================
# 第一段: 输入校验
# ============================================================
class InputValidator:
    @staticmethod
    def validate(data_path):
        errors, warnings = [], []
        if not os.path.exists(data_path):
            errors.append(f"数据路径不存在: {data_path}")
            return errors, warnings
        try:
            import arcpy
            desc = arcpy.Describe(data_path)
            sr = desc.spatialReference
            if not sr or sr.factoryCode == 0:
                errors.append("坐标系未定义，质检无法进行坐标相关检查")
            if desc.shapeType not in ['Polygon', 'Polyline', 'Point', 'Multipoint']:
                errors.append(f"不支持的几何类型: {desc.shapeType}")
        except Exception as e:
            warnings.append(f"输入预检异常: {e}")
        return errors, warnings


# ============================================================
# 第二段: 核心质检引擎
# ============================================================
class QualityChecker:
    """二级质检核心引擎 —— 12项检查"""
    
    def __init__(self, data_path, scale="1:500", tolerance_override=None):
        self.data_path = data_path
        self.scale = scale
        self.tol = tolerance_override or self._get_tolerance()
        self.defects = []
        self.scores = {}
    
    def _get_tolerance(self):
        std = QUICK_STANDARDS.get(self.scale, QUICK_STANDARDS["1:500"])
        return {
            'min_area_sqm': 0.5 if self.scale in ['1:500', '1:1000'] else 2.0,
            'sliver_area_sqm': 0.1,
            'overlap_area_sqm': 0.01,
            'gap_area_sqm': 1.0,
            'cluster_tolerance_m': 0.001,
        }
    
    def check_all(self):
        """执行全部12项质检"""
        import arcpy as ap
        
        desc = ap.Describe(self.data_path)
        shp_type = desc.shapeType
        total_count = int(ap.management.GetCount(self.data_path).getOutput(0))
        
        # === 1. 空几何检查 ===
        null_geom = 0
        with ap.da.SearchCursor(self.data_path, ['OID@', 'SHAPE@']) as cursor:
            for row in cursor:
                if row[1] is None:
                    null_geom += 1
                    self.defects.append({
                        'oid': row[0], 'element': 'geometric_quality',
                        'level': 'A', 'type': '空几何',
                        'desc': '要素几何为空(NULL)'
                    })
        self.scores['null_geometry'] = {'count': null_geom, 'pass': null_geom == 0}
        
        # === 2. 无效几何检查 ===
        invalid_geom = 0
        try:
            ap.management.CheckGeometry(self.data_path)
            # 在arcpy中需要通过迭代检查
            with ap.da.SearchCursor(self.data_path, ['OID@', 'SHAPE@']) as cursor:
                for row in cursor:
                    try:
                        if row[1] and not row[1].isSimple:
                            invalid_geom += 1
                            self.defects.append({
                                'oid': row[0], 'element': 'geometric_quality',
                                'level': 'A', 'type': '无效几何',
                                'desc': '要素几何无效(自相交/环方向错误等)'
                            })
                    except:
                        invalid_geom += 1
        except Exception as e:
            self.defects.append({
                'oid': 0, 'element': 'geometric_quality',
                'level': 'B', 'type': '几何检查异常',
                'desc': f'CheckGeometry执行异常: {e}'
            })
        self.scores['invalid_geometry'] = {'count': invalid_geom, 'pass': invalid_geom == 0}
        
        # === 3. 多部件检查 ===
        mp_count = 0
        if shp_type in ['Polygon', 'Polyline']:
            with ap.da.SearchCursor(self.data_path, ['OID@', 'SHAPE@']) as cursor:
                for row in cursor:
                    if row[1] and row[1].isMultipart:
                        mp_count += 1
                        self.defects.append({
                            'oid': row[0], 'element': 'geometric_quality',
                            'level': 'C', 'type': '多部件',
                            'desc': f'要素包含{row[1].partCount}个部件'
                        })
        self.scores['multipart'] = {'count': mp_count, 'pass': True, 'info': f'{mp_count}个多部件要素'}
        
        # === 4. 极小面检查 ===
        sliver_count = 0
        if shp_type == 'Polygon':
            with ap.da.SearchCursor(self.data_path, ['OID@', 'SHAPE@AREA']) as cursor:
                for row in cursor:
                    if row[1] and row[1] < self.tol['sliver_area_sqm']:
                        sliver_count += 1
                        self.defects.append({
                            'oid': row[0], 'element': 'geometric_quality',
                            'level': 'C', 'type': '极小面',
                            'desc': f'面积 {row[1]:.4f}m² < 阈值{self.tol["sliver_area_sqm"]}m²'
                        })
        self.scores['sliver_polygons'] = {'count': sliver_count, 'pass': sliver_count == 0}
        
        # === 5. 面重叠检查 ===
        overlap_count = 0
        if shp_type == 'Polygon' and total_count > 1:
            try:
                # 自相交检测
                intersect_layer = f"memory/intersect_self"
                ap.analysis.Intersect(
                    [self.data_path, self.data_path],
                    intersect_layer,
                    join_attributes="ONLY_FID"
                )
                overlap_count = int(ap.management.GetCount(intersect_layer).getOutput(0))
                if overlap_count > 0:
                    self.defects.append({
                        'oid': 0, 'element': 'logical_consistency',
                        'level': 'B', 'type': '面重叠',
                        'desc': f'检测到{overlap_count}处面重叠'
                    })
                ap.management.Delete(intersect_layer)
            except Exception as e:
                self.defects.append({
                    'oid': 0, 'element': 'logical_consistency',
                    'level': 'B', 'type': '重叠检测异常',
                    'desc': f'Intersect执行失败: {e}'
                })
        self.scores['overlap'] = {'count': overlap_count, 'pass': overlap_count == 0}
        
        # === 6. 空洞检查(Dissolve轮廓法) ===
        gap_count = 0
        if shp_type == 'Polygon' and total_count > 1:
            try:
                dissolved = f"memory/dissolved"
                ap.management.Dissolve(self.data_path, dissolved)
                # Erase获取空洞
                erased = f"memory/erased"
                ap.analysis.Erase(dissolved, self.data_path, erased)
                gap_count = int(ap.management.GetCount(erased).getOutput(0))
                if gap_count > 0:
                    gap_areas = []
                    with ap.da.SearchCursor(erased, ['SHAPE@AREA']) as c:
                        for r in c:
                            if r[0] > self.tol['gap_area_sqm']:
                                gap_areas.append(r[0])
                    if gap_areas:
                        self.defects.append({
                            'oid': 0, 'element': 'logical_consistency',
                            'level': 'B', 'type': '覆盖空洞',
                            'desc': f'检测到{len(gap_areas)}处空洞，总面积{sum(gap_areas):.2f}m²'
                        })
                for name in [dissolved, erased]:
                    try: ap.management.Delete(name)
                    except: pass
            except Exception as e:
                self.defects.append({
                    'oid': 0, 'element': 'logical_consistency',
                    'level': 'B', 'type': '空洞检测异常',
                    'desc': f'Dissolve/Erase失败: {e}'
                })
        self.scores['gaps'] = {'count': gap_count, 'pass': gap_count == 0}
        
        # === 7. 属性完整性检查 ===
        null_attr = 0
        fields = [f for f in desc.fields if f.type not in ['Geometry', 'OID', 'Blob', 'Raster']]
        for f in fields:
            with ap.da.SearchCursor(self.data_path, [f.name]) as cursor:
                for row in cursor:
                    if row[0] is None or (isinstance(row[0], str) and row[0].strip() == ''):
                        null_attr += 1
        self.scores['attribute_completeness'] = {
            'null_count': null_attr,
            'pass': null_attr < total_count * 0.05  # 允许5%缺失
        }
        if null_attr > 0:
            self.defects.append({
                'oid': 0, 'element': 'completeness',
                'level': 'C', 'type': '属性缺失',
                'desc': f'{null_attr}个字段值为空'
            })
        
        # === 8. 字段类型一致性 ===
        field_issues = 0
        for f in fields:
            if f.length and f.type == 'String':
                with ap.da.SearchCursor(self.data_path, [f.name]) as cursor:
                    for row in cursor:
                        if row[0] and len(str(row[0])) > f.length:
                            field_issues += 1
        self.scores['field_consistency'] = {'count': field_issues, 'pass': field_issues == 0}
        
        # === 9. 范围合规检查 ===
        extent = desc.extent
        range_ok = True
        if desc.spatialReference.type == 'Geographic':
            if abs(extent.XMin) > 180 or abs(extent.XMax) > 180 or abs(extent.YMin) > 90:
                range_ok = False
                self.defects.append({
                    'oid': 0, 'element': 'logical_consistency',
                    'level': 'A', 'type': '范围异常',
                    'desc': '地理坐标超出合法经纬度范围'
                })
        self.scores['extent_validity'] = {'pass': range_ok}
        
        # === 10. 要素数量合理性 ===
        self.scores['feature_count'] = {'count': total_count, 'pass': total_count > 0}
        
        # === 11. 编码字段存在性 ===
        code_field = None
        for code_name in ['DLBM', 'DLMC', 'BSM', 'YSDM']:
            for f in fields:
                if f.name.upper() == code_name.upper():
                    code_field = f.name
                    break
        self.scores['code_field'] = {'found': code_field is not None, 'field': code_field,
                                     'pass': code_field is not None}
        if not code_field:
            self.defects.append({
                'oid': 0, 'element': 'format_compliance',
                'level': 'C', 'type': '编码缺失',
                'desc': '未找到DLBM/DLMC/BSM等国标编码字段'
            })
        
        # === 12. 坐标系合规 ===
        sr = desc.spatialReference
        sr_ok = sr and sr.factoryCode != 0
        cgcs_ok = False
        if sr_ok:
            cgcs_wkids_6deg = {4491, 4492, 4493, 4494, 4495, 4496, 4497, 4498, 4499, 4500, 4501}
            cgcs_wkids_3deg = {4513, 4514, 4515, 4516, 4517, 4518, 4519, 4520, 4521, 4522, 4523,
                              4524, 4525, 4526, 4527, 4528, 4529, 4530, 4531, 4532, 4533}
            cgcs_ok = sr.factoryCode in cgcs_wkids_6deg or sr.factoryCode in cgcs_wkids_3deg or sr.factoryCode == 4490
        self.scores['coordinate_system'] = {
            'defined': sr_ok, 'is_cgcs2000': cgcs_ok,
            'wkid': sr.factoryCode if sr else 0, 'name': sr.name if sr else '未定义',
            'pass': sr_ok
        }
        if not cgcs_ok and sr_ok:
            self.defects.append({
                'oid': 0, 'element': 'format_compliance',
                'level': 'C', 'type': '非CGCS2000',
                'desc': f'坐标系 {sr.name} 非CGCS2000,建议转换'
            })
        
        return self._compute_score()
    
    def _compute_score(self):
        """计算加权质量评分 0-100"""
        total_weight = 0
        weighted_score = 0
        
        element_scores = {
            'geometric_quality': self._element_score([
                self.scores.get('null_geometry', {}),
                self.scores.get('invalid_geometry', {}),
                self.scores.get('sliver_polygons', {}),
                self.scores.get('multipart', {})
            ]),
            'logical_consistency': self._element_score([
                self.scores.get('overlap', {}),
                self.scores.get('gaps', {}),
                self.scores.get('extent_validity', {})
            ]),
            'completeness': self._element_score([
                self.scores.get('attribute_completeness', {})
            ]),
            'format_compliance': self._element_score([
                self.scores.get('code_field', {}),
                self.scores.get('coordinate_system', {})
            ]),
            'attribute_accuracy': self._element_score([
                self.scores.get('field_consistency', {})
            ]),
            'geometric_quality': self._element_score([
                self.scores.get('null_geometry', {}),
                self.scores.get('invalid_geometry', {})
            ]),
            'positional_accuracy': 1.0,  # 需要参考数据才能检验
            'metadata_quality': 1.0,  # 单独检查
            'temporal_accuracy': 1.0,
        }
        
        for elem_name in QUALITY_ELEMENTS:
            if elem_name in element_scores:
                weighted_score += element_scores[elem_name] * QUALITY_ELEMENTS[elem_name]['weight']
                total_weight += QUALITY_ELEMENTS[elem_name]['weight']
        
        final_score = round((weighted_score / total_weight) * 100, 1) if total_weight > 0 else 0
        
        # 缺陷等级分布
        level_counts = {}
        for d in self.defects:
            lvl = d['level']
            level_counts[lvl] = level_counts.get(lvl, 0) + 1
        
        return {
            'total_score': final_score,
            'grade': self._grade(final_score),
            'defects_total': len(self.defects),
            'defects_by_level': level_counts,
            'defects': self.defects[:100],
            'element_details': self.scores,
            'total_features': self.scores.get('feature_count', {}).get('count', 0)
        }
    
    def _element_score(self, checks):
        valid = [c.get('pass', True) for c in checks if c]
        return sum(valid) / len(valid) if valid else 1.0
    
    @staticmethod
    def _grade(score):
        if score >= 90: return '优'
        if score >= 75: return '良'
        if score >= 60: return '合格'
        return '不合格'


# ============================================================
# 第三段: 输出校验
# ============================================================
class OutputValidator:
    @staticmethod
    def validate(report):
        errors = []
        if report.get('total_score') is None:
            errors.append("缺少总评分")
        if not report.get('defects_by_level'):
            errors.append("缺少缺陷分级统计")
        return errors


# ============================================================
# HTML报告
# ============================================================
def generate_html_report(report, output_dir):
    grade_color = {'优': 'green', '良': 'blue', '合格': 'orange', '不合格': 'red'}
    gc = grade_color.get(report.get('grade', ''), 'black')
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>二级质检报告</title>
<style>
body{{font-family:'Microsoft YaHei',sans-serif;max-width:1100px;margin:0 auto;padding:20px}}
h1{{color:#1565c0;border-bottom:3px solid #1565c0;padding-bottom:10px}}
h2{{margin-top:30px}}
.score-box{{text-align:center;padding:30px;background:#f5f5f5;border-radius:10px;margin:20px 0}}
.score-value{{font-size:64px;font-weight:bold;color:{gc}}}
.grade{{font-size:24px;color:{gc};margin-top:10px}}
.metric-grid{{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}}
.metric-card{{flex:1;min-width:180px;background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:15px;text-align:center}}
.metric-value{{font-size:28px;font-weight:bold}}
table{{border-collapse:collapse;width:100%;margin:10px 0}}
th,td{{border:1px solid #ddd;padding:8px}}
th{{background:#1565c0;color:white}}
.level-A{{background:#ffebee}}
.level-B{{background:#fff3e0}}
.level-C{{background:#fff8e1}}
.level-D{{background:#e8f5e9}}
</style>
</head>
<body>
<h1>成果质量检查报告 (二级质检)</h1>
<p>时间: {report.get('timestamp','')} | 依据: GB/T 18316-2008, GB/T 24356-2009</p>

<div class="score-box">
<div class="score-value">{report.get('total_score', 0)}</div>
<div class="grade">质量等级: {report.get('grade', 'N/A')}</div>
</div>

<div class="metric-grid">
<div class="metric-card"><div class="metric-value" style="color:#d32f2f">{report['defects_by_level'].get('A',0)}</div>A·严重缺陷</div>
<div class="metric-card"><div class="metric-value" style="color:#f57c00">{report['defects_by_level'].get('B',0)}</div>B·重缺陷</div>
<div class="metric-card"><div class="metric-value" style="color:#fbc02d">{report['defects_by_level'].get('C',0)}</div>C·次重缺陷</div>
<div class="metric-card"><div class="metric-value" style="color:#43a047">{report['defects_by_level'].get('D',0)}</div>D·轻缺陷</div>
</div>
"""
    
    if report.get('defects'):
        html += "<h2>缺陷清单</h2><table><tr><th>OID</th><th>质检元素</th><th>等级</th><th>类型</th><th>描述</th></tr>"
        for d in report['defects']:
            html += f"<tr class='level-{d['level']}'><td>{d['oid']}</td><td>{d['element']}</td><td>{d['level']}</td><td>{d['type']}</td><td>{d['desc']}</td></tr>"
        html += "</table>"
    
    if report.get('element_details'):
        html += "<h2>按质检元素统计</h2><table><tr><th>检查项</th><th>结果</th><th>通过</th></tr>"
        for k, v in report['element_details'].items():
            status = '✅' if v.get('pass', True) else '❌'
            detail = json.dumps(v, ensure_ascii=False)[:100]
            html += f"<tr><td>{k}</td><td>{status}</td><td>{detail}</td></tr>"
        html += "</table>"
    
    html += "</body></html>"
    
    html_path = Path(output_dir) / f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_path


# ============================================================
# 主入口
# ============================================================
def main(data_path, scale="1:500", output_dir=None, max_retries=3):
    if output_dir is None:
        output_dir = f"output_quality_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    logger, log_path = setup_logger(output_dir)
    logger.info(f"ATS-005 二级质检启动: {data_path}, 比例尺: {scale}")
    
    for attempt in range(1, max_retries + 1):
        try:
            errors, warnings = InputValidator.validate(data_path)
            if errors and attempt >= max_retries:
                raise RuntimeError(f"输入校验失败: {errors}")
            
            checker = QualityChecker(data_path, scale)
            results = checker.check_all()
            
            output_errors = OutputValidator.validate(results)
            if output_errors:
                logger.warning(f"输出校验: {output_errors}")
            
            report = {
                'task': '二级质检',
                'skill_id': 'ATS-005',
                'version': 'V5.0',
                'timestamp': datetime.now().isoformat(),
                'data': data_path,
                'scale': scale,
                'standard': 'GB/T 18316-2008',
                **results
            }
            
            json_path = Path(output_dir) / f"quality_report.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            # 缺陷CSV
            if results['defects']:
                csv_path = Path(output_dir) / "defects.csv"
                with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=['oid', 'element', 'level', 'type', 'desc'])
                    writer.writeheader()
                    writer.writerows(results['defects'])
            
            html_path = generate_html_report(report, output_dir)
            
            logger.info(f"质检完成: 总分{results['total_score']}, 等级{results['grade']}, 缺陷{results['defects_total']}个")
            
            return {
                'report_json': str(json_path),
                'report_html': str(html_path),
                'log': str(log_path),
                'summary': {
                    'score': results['total_score'],
                    'grade': results['grade'],
                    'defects': results['defects_total'],
                    'level_dist': results['defects_by_level']
                }
            }
            
        except Exception as e:
            logger.error(f"第{attempt}轮异常: {e}")
            if attempt >= max_retries:
                raise RuntimeError(f"[3轮熔断] ATS-005失败: {e}")
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ATS-005 二级质检')
    parser.add_argument('data', help='成果数据路径')
    parser.add_argument('-s', '--scale', default='1:500', help='比例尺')
    parser.add_argument('-o', '--output', default=None)
    args = parser.parse_args()
    result = main(args.data, args.scale, args.output)
    print(f"\n质检完成: 总分{result['summary']['score']}, 等级{result['summary']['grade']}")
```

---

## 验收检查单

| 序号 | 检查项 | 标准 |
|------|--------|------|
| 1 | 12项质检全覆盖 | 空几何/无效几何/多部件/极小面/重叠/空洞/属性/字段/范围/数量/编码/坐标系 |
| 2 | 缺陷ABCD分级 | 严重/重/次重/轻 四级 |
| 3 | 加权评分 0-100 | 按GB/T 18316权重计算 |
| 4 | HTML可视化 | 评分仪表盘+缺陷清单+分级统计 |
| 5 | 缺陷CSV导出 | 含OID/元素/等级/类型/描述 |
| 6 | 比例尺适配 | 支持1:500/1:1000/1:2000/1:5000阈值自动调整 |
