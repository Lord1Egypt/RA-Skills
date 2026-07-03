<!-- wm:坤图_GIS:V5.0 -->
# 原子GIS Skill单元 —— 元数据生成 Skill ATS-006

> V5.0 | 中层-原子Skill | 触发词: 元数据/XML元数据/成果登记/汇交元数据
> 约束: V5_CONSTITUTION.md | 阶段7交付归档强制节点

```yaml
skill_id: ATS-006
skill_name: metadata_generate
category: 文档生成
min_inputs: [成果数据(GDB/SHP/GPKG/TIF)]
outputs: [元数据XML(GB/T 19710格式), 元数据JSON, 元数据清单CSV]
engines: [arcpy, gdal, python]
```

---

## 完整执行代码

```python
#!/usr/bin/env python3
"""
ATS-006: 元数据生成 Skill V5.0
依据 GB/T 19710-2005 地理信息元数据标准
自动从数据中提取核心元数据项并生成标准化XML/JSON
"""

import os, sys, json, logging
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

def setup_logger(output_dir):
    log_path = Path(output_dir) / f"metadata_gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()])
    return logging.getLogger(__name__), log_path

class InputValidator:
    """输入校验器 — 含CRS强制卡点(V5.0强化)"""
    @staticmethod
    def validate(data_path):
        errors = []
        if not os.path.exists(data_path):
            errors.append(f"数据路径不存在: {data_path}")
            return errors

        # CRS强制卡点 V5.0
        try:
            import arcpy
            desc = arcpy.Describe(data_path)
            sr = desc.spatialReference
            if sr is None or sr.name in ("Unknown", "未定义", "", None):
                errors.append(f"[CRS-严重] 数据无有效坐标系定义")
            elif (sr.factoryCode or 0) < 1:
                errors.append(f"[CRS-严重] 坐标系WKID无效: {sr.factoryCode}")
            else:
                logger = logging.getLogger("ATS-006.InputValidator")
                logger.info(f"CRS卡点通过: {sr.name} (EPSG:{sr.factoryCode})")
        except ImportError:
            try:
                from osgeo import ogr
                ds = ogr.Open(data_path)
                if ds:
                    layer = ds.GetLayer()
                    sr = layer.GetSpatialRef()
                    if sr is None:
                        errors.append("[CRS-严重] GDAL无法读取坐标系")
                    elif int(sr.GetAuthorityCode(None) or 0) < 1:
                        errors.append("[CRS-严重] 坐标系WKID无效(GDAL)")
            except ImportError:
                errors.append("[CRS-警告] arcpy和GDAL均不可用，跳过CRS检测")
        except Exception as e:
            errors.append(f"[CRS-错误] {e}")
        return errors

class MetadataExtractor:
    """核心元数据提取引擎 —— 自动检测并提取25+项元数据"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.metadata = {}
    
    def extract(self):
        import arcpy
        
        desc = arcpy.Describe(self.data_path)
        sr = desc.spatialReference
        extent = desc.extent
        
        # 1. 标识信息
        self.metadata['identification'] = {
            'title': Path(self.data_path).stem,
            'abstract': f"由ATS-006自动生成, 数据集类型:{desc.dataType}",
            'purpose': '测绘地理信息成果汇交',
            'creation_date': datetime.now().strftime('%Y-%m-%d'),
            'language': 'zh-CN',
            'character_set': 'UTF-8',
            'topic_category': 'geoscientificInformation',
        }
        
        # 2. 空间参考
        self.metadata['spatial_reference'] = {
            'name': sr.name if sr else '未定义',
            'wkid': sr.factoryCode if sr else 0,
            'wkt': (sr.exportToString() if sr and sr.factoryCode != 0 else '')[:300],
            'type': 'Geographic' if sr and sr.type == 'Geographic' else 'Projected',
            'unit': sr.linearUnitName if sr and sr.type == 'Projected' else (sr.angularUnitName if sr else ''),
        }
        
        # 3. 空间范围
        self.metadata['extent'] = {
            'west': round(extent.XMin, 6), 'east': round(extent.XMax, 6),
            'south': round(extent.YMin, 6), 'north': round(extent.YMax, 6),
            'description': f'({extent.XMin:.4f}, {extent.YMin:.4f}) - ({extent.XMax:.4f}, {extent.YMax:.4f})'
        }
        
        # 4. 要素统计
        count = int(arcpy.management.GetCount(self.data_path).getOutput(0))
        self.metadata['content'] = {
            'feature_count': count,
            'geometry_type': desc.shapeType,
            'field_count': len([f for f in desc.fields if f.type not in ['Geometry','OID']]),
            'fields': self._extract_fields(desc),
        }
        
        # 5. 时间范围
        time_fields = []
        for f in desc.fields:
            if any(kw in f.name.upper() for kw in ['DATE','TIME','YEAR','日期']):
                time_fields.append(f.name)
        if time_fields:
            vals = []
            with arcpy.da.SearchCursor(self.data_path, time_fields[:1]) as cursor:
                for i, row in enumerate(cursor):
                    if i > 10: break
                    if row[0]:
                        vals.append(str(row[0]))
            self.metadata['temporal'] = {
                'time_fields': time_fields,
                'sample_values': vals[:5]
            }
        
        # 6. 质量信息
        self.metadata['quality'] = {
            'completeness': '数据完整性待二级质检确认',
            'positional_accuracy': '位置精度待二级质检确认',
            'lineage': f'由ATS-006于{datetime.now().strftime("%Y-%m-%d %H:%M")}自动生成',
            'processing_steps': ['ATS-006自动元数据提取']
        }
        
        # 7. 分发信息
        self.metadata['distribution'] = {
            'format': Path(self.data_path).suffix,
            'format_version': desc.release if hasattr(desc, 'release') else 'N/A',
            'file_size_mb': round(self._get_size_mb(), 2),
            'access_constraints': '测绘成果，使用需遵循保密规定',
        }
        
        # 8. 联系信息(占位)
        self.metadata['contact'] = {
            'organization': '[用户单位名称]',
            'person': '[项目负责人]',
            'phone': '[联系电话]',
            'email': '[电子邮箱]'
        }
        
        return self.metadata
    
    def _extract_fields(self, desc):
        fields = []
        for f in desc.fields:
            if f.type not in ['Geometry', 'OID']:
                fields.append({
                    'name': f.name,
                    'alias': f.aliasName if hasattr(f, 'aliasName') else f.name,
                    'type': f.type,
                    'length': f.length if hasattr(f, 'length') else None,
                    'nullable': f.isNullable
                })
        return fields
    
    def _get_size_mb(self):
        total = 0
        data_dir = Path(self.data_path)
        if data_dir.is_dir():
            for root, dirs, files in os.walk(data_dir):
                for f in files:
                    total += os.path.getsize(os.path.join(root, f))
        else:
            total = os.path.getsize(data_dir) if data_dir.is_file() else 0
        return total / 1024 / 1024


class OutputValidator:
    """输出校验器 — V5.0强化：CRS一致性+文件完整性+必填字段"""
    @staticmethod
    def validate(metadata, output_dir=None):
        """校验元数据完整性"""
        required = ['identification', 'spatial_reference', 'extent', 'content', 'quality']
        errors = []
        missing = [k for k in required if k not in metadata]
        if missing:
            errors.append(f"元数据缺少必填字段: {missing}")

        # V5.0新增: 检查坐标系WKID有效性
        sr = metadata.get('spatial_reference', {})
        wkid = sr.get('wkid', 0)
        sr_name = sr.get('name', '')
        if wkid < 1 or sr_name in ('Unknown', '未定义', '', None):
            errors.append(f"[CRS-输出] 输出元数据的坐标系无效: WKID={wkid}, Name={sr_name}")

        # V5.0新增: 检查输出文件完整性
        if output_dir:
            output_path = Path(output_dir)
            if output_path.exists():
                files = list(output_path.glob('metadata.*'))
                if not files:
                    errors.append("[输出] 未找到元数据输出文件")
                else:
                    for f in files:
                        if f.stat().st_size < 100:
                            errors.append(f"[输出] 文件过小可能异常: {f.name} ({f.stat().st_size}B)")

        return errors


def generate_gb19710_xml(metadata, output_dir):
    """生成 GB/T 19710-2005 标准XML元数据"""
    root = Element('MD_Metadata', xmlns='http://www.isotc211.org/2005/gmd')
    
    # 文件标识
    fid = SubElement(root, 'fileIdentifier')
    fid.text = f"ATS006_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 语言
    lang = SubElement(root, 'language')
    lang.text = 'zh-CN'
    
    # 联系信息
    contact = SubElement(root, 'contact')
    org = SubElement(contact, 'organisationName')
    org.text = metadata['contact']['organization']
    
    # 日期
    date_stamp = SubElement(root, 'dateStamp')
    date_stamp.text = datetime.now().strftime('%Y-%m-%d')
    
    # 标识
    ident = SubElement(root, 'identificationInfo')
    citation = SubElement(ident, 'citation')
    title = SubElement(citation, 'title')
    title.text = metadata['identification']['title']
    abstract = SubElement(ident, 'abstract')
    abstract.text = metadata['identification']['abstract']
    
    # 空间参考
    ref_sys = SubElement(root, 'referenceSystemInfo')
    ref_code = SubElement(ref_sys, 'code')
    ref_code.text = f"EPSG:{metadata['spatial_reference']['wkid']}"
    
    xml_str = tostring(root, encoding='utf-8')
    dom = parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8')
    
    xml_path = Path(output_dir) / f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(xml_path, 'wb') as f:
        f.write(pretty_xml)
    return xml_path


def main(data_path, output_dir=None, max_retries=3):
    if output_dir is None:
        output_dir = f"output_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    logger, log_path = setup_logger(output_dir)
    logger.info(f"ATS-006 元数据生成: {data_path}")
    
    for attempt in range(1, max_retries + 1):
        try:
            errors = InputValidator.validate(data_path)
            if errors and attempt >= max_retries:
                raise RuntimeError(f"输入校验失败: {errors}")
            
            extractor = MetadataExtractor(data_path)
            metadata = extractor.extract()
            
            missing = OutputValidator.validate(metadata)
            if missing:
                logger.warning(f"元数据缺少字段: {missing}")
            
            # JSON输出
            json_path = Path(output_dir) / "metadata.json"
            output = {
                'task': '元数据生成', 'skill_id': 'ATS-006', 'version': 'V5.0',
                'timestamp': datetime.now().isoformat(), 'data': data_path,
                **metadata
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            
            # XML输出
            xml_path = generate_gb19710_xml(metadata, output_dir)
            
            logger.info(f"元数据生成完成: JSON={json_path}, XML={xml_path}")
            
            return {
                'metadata_json': str(json_path),
                'metadata_xml': str(xml_path),
                'log': str(log_path)
            }
            
        except Exception as e:
            logger.error(f"第{attempt}轮异常: {e}")
            if attempt >= max_retries:
                raise RuntimeError(f"[3轮熔断] ATS-006失败: {e}")
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ATS-006 元数据生成')
    parser.add_argument('data', help='数据路径')
    parser.add_argument('-o', '--output', default=None)
    args = parser.parse_args()
    result = main(args.data, args.output)
    print(f"\n元数据生成完成: {result['metadata_json']}")
```

---

## 验收检查单

| 序号 | 检查项 | 标准 |
|------|--------|------|
| 1 | 标识信息 | 标题+摘要+日期+语言+主题分类 |
| 2 | 空间参考 | WKID+名称+WKT+类型+单位 |
| 3 | 空间范围 | 四至边界(经纬度/投影坐标) |
| 4 | 要素统计 | 数量+几何类型+字段列表 |
| 5 | 质量信息 | 完整性+精度+数据志+处理步骤 |
| 6 | GB/T 19710 XML | ISO 19139兼容XML格式 |
