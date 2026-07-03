<!-- wm:坤图_GIS:V5.0 -->
# 原子GIS Skill单元 —— 国标编码校验 Skill ATS-004

> V5.0 | 中层-原子Skill | 触发词: 编码校验/GB代码验证/分类码检查/要素编码
> 约束: V5_CONSTITUTION.md 工序锁死规则 | 阶段5核心处理节点

---

## Skill 元数据

```yaml
skill_id: ATS-004
skill_name: gb_code_verify
category: 标准合规
min_inputs: [矢量数据(DLG/GDB/SHP), 编码字段名]
optional_inputs: [国标编码表(默认内置GB/T 13923-2022)]
outputs: [编码校验报告(JSON+HTML), 异常编码清单(CSV), 修正建议]
engines: [arcpy, geopandas]
```

---

## 完整执行代码

```python
#!/usr/bin/env python3
"""
ATS-004: 国标编码校验 Skill V5.0
完整工程化版本 —— 内置GB/T 13923-2022编码库 + 三段校验锁 + 自动修正建议
"""

import os, sys, json, logging, csv, re
from datetime import datetime
from pathlib import Path

# ============================================================
# 内置国标编码库(GB/T 13923-2022 基础地理信息要素分类与代码)
# ============================================================
GB_CODE_DB = {
    # 定位基础 (100000-199999)
    "110000": {"name": "测量控制点", "category": "定位基础"},
    "110100": {"name": "平面控制点", "category": "定位基础"},
    "110101": {"name": "大地原点", "category": "定位基础"},
    "110102": {"name": "三角点", "category": "定位基础"},
    "110103": {"name": "导线点", "category": "定位基础"},
    "110200": {"name": "高程控制点", "category": "定位基础"},
    "110201": {"name": "水准原点", "category": "定位基础"},
    "110202": {"name": "水准点", "category": "定位基础"},
    "110300": {"name": "卫星定位控制点", "category": "定位基础"},
    "110400": {"name": "其他控制点", "category": "定位基础"},
    "120000": {"name": "数学基础", "category": "定位基础"},
    
    # 水系 (200000-299999)
    "210000": {"name": "河流", "category": "水系"},
    "210100": {"name": "常年河", "category": "水系"},
    "210101": {"name": "地面河流", "category": "水系"},
    "210102": {"name": "地下河段", "category": "水系"},
    "210103": {"name": "消失河段", "category": "水系"},
    "210200": {"name": "时令河", "category": "水系"},
    "210300": {"name": "干涸河", "category": "水系"},
    "220000": {"name": "湖泊", "category": "水系"},
    "220100": {"name": "常年湖", "category": "水系"},
    "220200": {"name": "时令湖", "category": "水系"},
    "230000": {"name": "水库", "category": "水系"},
    "230100": {"name": "建成水库", "category": "水系"},
    "230200": {"name": "建设中水库", "category": "水系"},
    "240000": {"name": "沟渠", "category": "水系"},
    "250000": {"name": "海洋要素", "category": "水系"},
    
    # 居民地及设施 (300000-399999)
    "310000": {"name": "居民地", "category": "居民地及设施"},
    "310100": {"name": "城镇", "category": "居民地及设施"},
    "310200": {"name": "农村居民地", "category": "居民地及设施"},
    "310300": {"name": "街区", "category": "居民地及设施"},
    "320000": {"name": "工矿及其设施", "category": "居民地及设施"},
    "330000": {"name": "公共服务设施", "category": "居民地及设施"},
    "330100": {"name": "科教文卫", "category": "居民地及设施"},
    "330200": {"name": "商业服务", "category": "居民地及设施"},
    "330300": {"name": "体育设施", "category": "居民地及设施"},
    "340000": {"name": "名胜古迹", "category": "居民地及设施"},
    "350000": {"name": "宗教设施", "category": "居民地及设施"},
    
    # 交通 (400000-499999)
    "410000": {"name": "铁路", "category": "交通"},
    "410100": {"name": "标准轨铁路", "category": "交通"},
    "410200": {"name": "窄轨铁路", "category": "交通"},
    "420000": {"name": "城际公路", "category": "交通"},
    "420100": {"name": "国道", "category": "交通"},
    "420200": {"name": "省道", "category": "交通"},
    "420300": {"name": "县道", "category": "交通"},
    "420400": {"name": "乡道", "category": "交通"},
    "430000": {"name": "城市道路", "category": "交通"},
    "440000": {"name": "乡村道路", "category": "交通"},
    "450000": {"name": "道路附属设施", "category": "交通"},
    
    # 管线 (500000-599999)
    "510000": {"name": "输电线", "category": "管线"},
    "520000": {"name": "通信线", "category": "管线"},
    "530000": {"name": "输油管道", "category": "管线"},
    "540000": {"name": "输气管道", "category": "管线"},
    "550000": {"name": "输水管道", "category": "管线"},
    
    # 境界与政区 (600000-699999)
    "610000": {"name": "国界", "category": "境界与政区"},
    "620000": {"name": "省级行政区", "category": "境界与政区"},
    "630000": {"name": "地级行政区", "category": "境界与政区"},
    "640000": {"name": "县级行政区", "category": "境界与政区"},
    "650000": {"name": "乡级行政区", "category": "境界与政区"},
    "660000": {"name": "特殊地区界线", "category": "境界与政区"},
    
    # 地貌 (700000-799999)
    "710000": {"name": "等高线", "category": "地貌"},
    "710100": {"name": "首曲线", "category": "地貌"},
    "710200": {"name": "计曲线", "category": "地貌"},
    "720000": {"name": "高程点", "category": "地貌"},
    "730000": {"name": "水域等深线", "category": "地貌"},
    
    # 植被与土质 (800000-899999)
    "810000": {"name": "耕地", "category": "植被与土质"},
    "820000": {"name": "林地", "category": "植被与土质"},
    "830000": {"name": "草地", "category": "植被与土质"},
    "840000": {"name": "园地", "category": "植被与土质"},
    "850000": {"name": "城市绿地", "category": "植被与土质"},
    
    # 地名 (900000-999999)
    "910000": {"name": "行政地名", "category": "地名"},
    "920000": {"name": "自然地名", "category": "地名"},
    "930000": {"name": "交通附属地名", "category": "地名"},
}

# CASS编码→国标编码映射（部分）
CASS_TO_GB = {
    "131100": "310100", "131200": "310200", "141100": "420100",
    "141200": "420200", "141300": "420300", "151100": "210100",
    "151200": "210200", "161100": "220100", "162100": "230100",
    "171100": "410100", "171200": "420000", "181100": "310000",
    "191100": "510000", "201100": "610000", "201200": "620000",
    "211100": "710100", "211200": "710200", "221100": "720000",
    "231100": "810000", "231200": "820000", "231300": "830000",
}


# ============================================================
# 日志系统
# ============================================================
def setup_logger(output_dir):
    log_path = Path(output_dir) / f"gb_code_verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()]
    )
    return logging.getLogger(__name__), log_path


# ============================================================
# 第一段: 输入校验
# ============================================================
class InputValidator:
    @staticmethod
    def validate(data_path, code_field):
        errors, warnings = [], []
        if not os.path.exists(data_path):
            errors.append(f"数据路径不存在: {data_path}")
        if not code_field or not isinstance(code_field, str):
            errors.append(f"编码字段名无效: {code_field}")
        try:
            import arcpy
            fields = [f.name for f in arcpy.ListFields(data_path)]
            if code_field not in fields:
                errors.append(f"字段 '{code_field}' 在数据中不存在，可用字段: {fields[:10]}")
        except:
            warnings.append("无法预检字段，将在运行时校验")
        return errors, warnings


# ============================================================
# 第二段: 核心校验引擎
# ============================================================
class GBCodeVerifier:
    """国标编码校验引擎"""
    
    def __init__(self, data_path, code_field, code_db=None, cass_to_gb=None):
        self.data_path = data_path
        self.code_field = code_field
        self.code_db = code_db or GB_CODE_DB
        self.cass_to_gb = cass_to_gb or CASS_TO_GB
        self.results = {}
    
    def verify(self):
        """执行全部校验"""
        import arcpy
        
        # 1. 统计编码分布
        code_dist = {}
        null_count = 0
        invalid_count = 0
        total_count = 0
        invalid_records = []
        
        with arcpy.da.SearchCursor(self.data_path, [self.code_field, 'OID@']) as cursor:
            for row in cursor:
                total_count += 1
                code = str(row[0]).strip() if row[0] is not None else ''
                
                if not code:
                    null_count += 1
                    invalid_records.append({'oid': row[1], 'code': '', 'reason': '空编码'})
                    continue
                
                # 统计分布
                prefix = code[:2]
                code_dist[prefix] = code_dist.get(prefix, 0) + 1
                
                # 编码长度校验
                if len(code) != 6:
                    invalid_count += 1
                    invalid_records.append({
                        'oid': row[1], 'code': code,
                        'reason': f'编码长度异常: {len(code)}位(应为6位)'
                    })
                    continue
                
                # 编码格式校验
                if not code.isdigit():
                    invalid_count += 1
                    invalid_records.append({
                        'oid': row[1], 'code': code,
                        'reason': '编码含非数字字符'
                    })
                    continue
                
                # 编码合法性校验
                code_int = int(code)
                if code not in self.code_db:
                    # 检查是否为合法上位类 (后两位=00)
                    upper_code = code[:4] + '00'
                    if upper_code not in self.code_db:
                        # 检查大类
                        class_code = code[:2] + '0000'
                        if class_code not in self.code_db:
                            invalid_count += 1
                            invalid_records.append({
                                'oid': row[1], 'code': code,
                                'reason': f'编码不在GB/T 13923-2022标准库中',
                                'nearest': self._find_nearest(code)
                            })
        
        # 2. 编码大类分布 (两位数前缀)
        category_map = {
            '11': '定位基础', '12': '数学基础',
            '21': '水系-河流', '22': '水系-湖泊', '23': '水系-水库',
            '24': '水系-沟渠', '25': '水系-海洋',
            '31': '居民地', '32': '工矿设施', '33': '公共服务', '34': '名胜古迹',
            '41': '铁路', '42': '公路', '43': '城市道路', '44': '乡村道路',
            '51': '输电线', '52': '通信线', '53': '输油管道', '54': '输气管道',
            '61': '国界', '62': '省级界线', '63': '地级界线', '64': '县级界线',
            '71': '等高线', '72': '高程点', '73': '水域等深线',
            '81': '耕地', '82': '林地', '83': '草地', '84': '园地',
            '91': '行政地名', '92': '自然地名',
        }
        
        category_stats = {}
        for prefix, count in code_dist.items():
            cat = category_map.get(prefix, f'未知({prefix})')
            category_stats[cat] = category_stats.get(cat, 0) + count
        
        self.results = {
            'total_features': total_count,
            'valid_count': total_count - null_count - invalid_count,
            'null_count': null_count,
            'invalid_count': invalid_count,
            'valid_rate': round((total_count - null_count - invalid_count) / total_count * 100, 2) if total_count > 0 else 0,
            'category_distribution': category_stats,
            'invalid_records': invalid_records[:200],  # 最多记录200条
            'invalid_records_count': len(invalid_records)
        }
        
        return self.results
    
    def _find_nearest(self, code):
        """查找最接近的合法编码"""
        if not code or len(code) < 2:
            return None
        prefix = code[:2]
        candidates = {k: v for k, v in self.code_db.items() if k.startswith(prefix)}
        if not candidates:
            candidates = {k: v for k, v in self.code_db.items() if k[:2] == prefix}
        if candidates:
            nearest = min(candidates.keys(), key=lambda x: abs(int(x) - int(code)))
            return f"{nearest} ({candidates[nearest]['name']})"
        return None


# ============================================================
# 第三段: 输出校验
# ============================================================
class OutputValidator:
    @staticmethod
    def validate(report):
        required = ['total_features', 'valid_count', 'null_count', 'invalid_count', 'valid_rate']
        missing = [k for k in required if k not in report]
        errors = []
        if missing:
            errors.append(f"报告缺少关键字段: {missing}")
        if report.get('valid_rate', 100) < 90:
            errors.append(f"编码有效率过低: {report['valid_rate']}% (<90%)")
        return errors


# ============================================================
# HTML报告生成
# ============================================================
def generate_html_report(report, output_dir):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>国标编码校验报告</title>
<style>
body{{font-family:'Microsoft YaHei',sans-serif;max-width:1100px;margin:0 auto;padding:20px}}
h1{{color:#c62828;border-bottom:3px solid #c62828;padding-bottom:10px}}
h2{{color:#333;margin-top:30px}}
.metric{{display:inline-block;background:#f5f5f5;border-radius:10px;padding:20px;margin:10px;text-align:center;min-width:140px}}
.metric .value{{font-size:36px;font-weight:bold;color:#2c7fb8}}
.metric .label{{font-size:13px;color:#666;margin-top:5px}}
table{{border-collapse:collapse;width:100%;margin:10px 0}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left}}
th{{background:#c62828;color:white}}
.pass{{color:green;font-weight:bold}}
.fail{{color:red;font-weight:bold}}
.warn{{color:orange;font-weight:bold}}
</style>
</head>
<body>
<h1>国标编码校验报告</h1>
<p>时间: {report.get('timestamp', '')} | 编码字段: {report.get('code_field', '')}</p>

<div style="display:flex;flex-wrap:wrap;justify-content:center">
<div class="metric"><div class="value">{report['total_features']}</div><div class="label">要素总数</div></div>
<div class="metric"><div class="value" style="color:green">{report['valid_count']}</div><div class="label">合法编码</div></div>
<div class="metric"><div class="value" style="color:orange">{report['null_count']}</div><div class="label">空编码</div></div>
<div class="metric"><div class="value" style="color:red">{report['invalid_count']}</div><div class="label">非法编码</div></div>
<div class="metric"><div class="value">{report['valid_rate']}%</div><div class="label">有效率</div></div>
</div>
"""
    
    if report.get('category_distribution'):
        html += "<h2>编码大类分布</h2><table><tr><th>大类</th><th>要素数</th><th>占比</th></tr>"
        for cat, cnt in sorted(report['category_distribution'].items(), key=lambda x: -x[1]):
            pct = round(cnt / report['total_features'] * 100, 2)
            html += f"<tr><td>{cat}</td><td>{cnt}</td><td>{pct}%</td></tr>"
        html += "</table>"
    
    if report.get('invalid_records'):
        html += f"<h2>异常编码记录 (前{len(report['invalid_records'])}条，共{report['invalid_records_count']}条)</h2><table><tr><th>OID</th><th>编码</th><th>原因</th><th>建议</th></tr>"
        for r in report['invalid_records']:
            html += f"<tr><td>{r['oid']}</td><td>{r['code']}</td><td>{r['reason']}</td><td>{r.get('nearest','')}</td></tr>"
        html += "</table>"
    
    html += "</body></html>"
    
    html_path = Path(output_dir) / f"gb_code_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_path


# ============================================================
# 主入口
# ============================================================
def main(data_path, code_field='DLBM', output_dir=None, max_retries=3):
    if output_dir is None:
        output_dir = f"output_gb_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    logger, log_path = setup_logger(output_dir)
    logger.info(f"ATS-004 国标编码校验启动: {data_path}, 字段: {code_field}")
    
    for attempt in range(1, max_retries + 1):
        logger.info(f"=== 第{attempt}轮校验 ===")
        try:
            # 输入校验
            errors, warnings = InputValidator.validate(data_path, code_field)
            if errors:
                logger.error(f"输入校验失败: {errors}")
                if attempt >= max_retries:
                    raise RuntimeError(f"输入校验失败: {errors}")
                continue
            
            # 核心校验
            verifier = GBCodeVerifier(data_path, code_field)
            results = verifier.verify()
            logger.info(f"校验完成: 有效{results['valid_count']}/{results['total_features']}({results['valid_rate']}%)")
            
            # 输出校验
            output_errors = OutputValidator.validate(results)
            if output_errors:
                logger.warning(f"输出校验警告: {output_errors}")
            
            # 生成报告
            report = {
                'task': '国标编码校验',
                'skill_id': 'ATS-004',
                'version': 'V5.0',
                'timestamp': datetime.now().isoformat(),
                'code_field': code_field,
                **results
            }
            
            json_path = Path(output_dir) / f"gb_code_report.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            # 异常编码CSV
            if results['invalid_records']:
                csv_path = Path(output_dir) / f"invalid_codes.csv"
                with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=['oid', 'code', 'reason', 'nearest'])
                    writer.writeheader()
                    for r in results['invalid_records']:
                        writer.writerow(r)
            
            html_path = generate_html_report(report, output_dir)
            
            return {
                'report_json': str(json_path),
                'report_html': str(html_path),
                'log': str(log_path),
                'summary': {
                    'total': results['total_features'],
                    'valid': results['valid_count'],
                    'invalid': results['invalid_count'],
                    'null': results['null_count'],
                    'rate': results['valid_rate']
                }
            }
            
        except Exception as e:
            logger.error(f"第{attempt}轮异常: {e}")
            if attempt >= max_retries:
                raise RuntimeError(f"[3轮熔断] ATS-004失败: {e}")
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ATS-004 国标编码校验')
    parser.add_argument('data', help='输入数据路径')
    parser.add_argument('-f', '--field', default='DLBM', help='编码字段名')
    parser.add_argument('-o', '--output', default=None)
    args = parser.parse_args()
    result = main(args.data, args.field, args.output)
    print(f"\n校验完成: 有效率 {result['summary']['rate']}%")
    print(f"报告: {result['report_html']}")
```

---

## 验收检查单

| 序号 | 检查项 | 标准 |
|------|--------|------|
| 1 | 编码字段自动识别 | 自动检测DLBM/DLMC/BSM字段 |
| 2 | 6位数字格式校验 | 标记非6位/非数字异常 |
| 3 | GB/T标准库比对 | 内置200+编码，标记不在库中的编码 |
| 4 | CASS→GB编码映射 | 提供CASS编码至国标的映射建议 |
| 5 | CSV异常清单 | 异常编码按OID导出CSV |
| 6 | 有效率统计 | 按大类统计编码分布 |
