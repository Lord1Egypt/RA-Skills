<!-- wm:坤图_GIS:V5.0 -->
# 原子GIS Skill单元 —— 项目归档报告 Skill ATS-010

> V5.0 | 中层-原子Skill | 触发词: 项目归档/成果打包/交付归档/归档清单
> 约束: V5_CONSTITUTION.md | 阶段7强制归档节点

```yaml
skill_id: ATS-010
skill_name: project_archive
category: 文档生成
min_inputs: [项目目录, 成果数据]
outputs: [归档目录结构, 归档清单CSV+JSON, 归档报告HTML, MD5校验文件]
engines: [python, arcpy]
```

---

## 完整执行代码

```python
#!/usr/bin/env python3
"""
ATS-010: 项目归档报告 Skill V5.0
自动生成标准化归档目录、文件清单、MD5校验、归档报告
"""

import os, sys, json, logging, csv, hashlib, shutil
from datetime import datetime
from pathlib import Path

ARCHIVE_TEMPLATE = {
    "01_原始数据": ["现场采集数据", "外协成果", "基础地理数据"],
    "02_处理过程": ["中间成果", "临时文件", "版本快照"],
    "03_最终成果": ["矢量成果", "栅格成果", "三维模型", "文档成果"],
    "04_质检报告": ["自查报告", "二级检查报告", "验收意见"],
    "05_元数据": ["成果元数据XML", "图幅接合表", "要素分类说明"],
    "06_文档资料": ["技术设计书", "技术总结", "检查报告", "验收报告"],
    "07_附件": ["照片", "视频", "扫描件", "其他"],
}


def setup_logger(output_dir):
    log_path = Path(output_dir) / f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[logging.FileHandler(log_path, encoding='utf-8'), logging.StreamHandler()])
    return logging.getLogger(__name__), log_path


class InputValidator:
    @staticmethod
    def validate(project_dir):
        errors = []
        if not os.path.exists(project_dir):
            errors.append(f"项目目录不存在: {project_dir}")
        return errors


class ProjectArchiver:
    """项目归档核心引擎"""
    
    def __init__(self, project_dir, project_name='PROJECT', output_dir=None):
        self.project_dir = project_dir
        self.project_name = project_name
        self.output_dir = output_dir or f"archive_{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.manifest = []
        self.stats = {}
    
    def create_archive_structure(self):
        """创建标准化归档目录结构"""
        archive_root = Path(self.output_dir)
        archive_root.mkdir(parents=True, exist_ok=True)
        
        created = []
        for category, subdirs in ARCHIVE_TEMPLATE.items():
            cat_path = archive_root / category
            cat_path.mkdir(exist_ok=True)
            created.append(str(cat_path))
            for sub in subdirs:
                sub_path = cat_path / sub
                sub_path.mkdir(exist_ok=True)
        
        return str(archive_root), created
    
    def scan_and_inventory(self):
        """扫描项目目录，生成文件清单"""
        total_size = 0
        file_types = {}
        
        for root, dirs, files in os.walk(self.project_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, self.project_dir)
                file_size = os.path.getsize(filepath)
                file_ext = Path(filename).suffix.lower()
                
                total_size += file_size
                file_types[file_ext] = file_types.get(file_ext, 0) + 1
                
                # 计算MD5
                md5 = self._compute_md5(filepath) if file_size < 50 * 1024 * 1024 else 'SKIP(>50MB)'
                
                self.manifest.append({
                    'relative_path': rel_path,
                    'filename': filename,
                    'extension': file_ext,
                    'size_bytes': file_size,
                    'size_mb': round(file_size / 1024 / 1024, 3),
                    'md5': md5,
                    'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
                })
        
        self.stats = {
            'total_files': len(self.manifest),
            'total_size_mb': round(total_size / 1024 / 1024, 2),
            'total_size_gb': round(total_size / 1024 / 1024 / 1024, 3),
            'file_types': file_types,
            'scan_time': datetime.now().isoformat(),
            'scan_root': self.project_dir
        }
        
        return self.manifest, self.stats
    
    def _compute_md5(self, filepath, chunk_size=8192):
        """计算文件MD5"""
        md5 = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    md5.update(chunk)
            return md5.hexdigest()
        except:
            return 'ERROR'
    
    def classify_files(self):
        """根据文件类型自动分类至归档目录"""
        classification = {}
        category_map = {
            '.shp': '03_最终成果/矢量成果',
            '.gdb': '03_最终成果/矢量成果',
            '.gpkg': '03_最终成果/矢量成果',
            '.tif': '03_最终成果/栅格成果',
            '.img': '03_最终成果/栅格成果',
            '.dwg': '01_原始数据/外协成果',
            '.dxf': '01_原始数据/外协成果',
            '.osgb': '03_最终成果/三维模型',
            '.obj': '03_最终成果/三维模型',
            '.3dtiles': '03_最终成果/三维模型',
            '.xml': '05_元数据/成果元数据XML',
            '.json': '05_元数据',
            '.csv': '05_元数据',
            '.pdf': '06_文档资料',
            '.doc': '06_文档资料',
            '.docx': '06_文档资料',
            '.xls': '06_文档资料',
            '.xlsx': '06_文档资料',
            '.jpg': '07_附件/照片',
            '.png': '07_附件/照片',
            '.mp4': '07_附件/视频',
        }
        
        for item in self.manifest:
            ext = item['extension']
            category = category_map.get(ext, '07_附件/其他')
            if category not in classification:
                classification[category] = []
            classification[category].append(item)
        
        return classification
    
    def generate_archive_package(self, classification, archive_root):
        """将分类文件复制到归档目录"""
        copy_log = []
        for category, files in classification.items():
            target_dir = os.path.join(archive_root, category)
            os.makedirs(target_dir, exist_ok=True)
            
            for item in files:
                src = os.path.join(self.project_dir, item['relative_path'])
                dst = os.path.join(target_dir, item['filename'])
                try:
                    shutil.copy2(src, dst)
                    copy_log.append({'file': item['relative_path'], 'destination': dst, 'status': 'OK'})
                except Exception as e:
                    copy_log.append({'file': item['relative_path'], 'destination': dst, 'status': f'ERROR: {e}'})
        
        return copy_log
    
    def export_manifest_csv(self):
        """导出清单CSV"""
        csv_path = os.path.join(self.output_dir, 'archive_manifest.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['relative_path', 'filename', 'extension', 
                                                    'size_mb', 'md5', 'modified'])
            writer.writeheader()
            writer.writerows(self.manifest)
        return csv_path
    
    def generate_html_report(self):
        """生成归档报告HTML"""
        stats = self.stats
        type_list = sorted(stats['file_types'].items(), key=lambda x: -x[1])
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>项目归档报告</title>
<style>
body{{font-family:'Microsoft YaHei',sans-serif;max-width:1100px;margin:0 auto;padding:20px}}
h1{{color:#2e7d32;border-bottom:3px solid #2e7d32;padding-bottom:10px}}
h2{{margin-top:30px}}
.stats{{display:flex;flex-wrap:wrap;gap:15px;margin:20px 0}}
.stat-card{{flex:1;min-width:160px;background:#e8f5e9;border-radius:8px;padding:15px;text-align:center}}
.stat-value{{font-size:32px;font-weight:bold;color:#2e7d32}}
.stat-label{{font-size:13px;color:#666;margin-top:5px}}
table{{border-collapse:collapse;width:100%;margin:10px 0}}
th,td{{border:1px solid #ddd;padding:8px;font-size:13px}}
th{{background:#2e7d32;color:white}}
tr:nth-child(even){{background:#f9fbe7}}
</style>
</head>
<body>
<h1>项目归档报告</h1>
<p>项目: {self.project_name} | 时间: {stats['scan_time']} | 来源: {stats['scan_root']}</p>

<div class="stats">
<div class="stat-card"><div class="stat-value">{stats['total_files']}</div><div class="stat-label">文件总数</div></div>
<div class="stat-card"><div class="stat-value">{stats['total_size_mb']}</div><div class="stat-label">总大小(MB)</div></div>
<div class="stat-card"><div class="stat-value">{stats['total_size_gb']}</div><div class="stat-label">总大小(GB)</div></div>
<div class="stat-card"><div class="stat-value">{len(stats['file_types'])}</div><div class="stat-label">文件类型</div></div>
</div>

<h2>文件类型分布</h2>
<table><tr><th>类型</th><th>数量</th><th>占比</th></tr>
"""
        for ext, cnt in type_list:
            pct = round(cnt / stats['total_files'] * 100, 1) if stats['total_files'] else 0
            html += f"<tr><td>{ext}</td><td>{cnt}</td><td>{pct}%</td></tr>"
        html += "</table>"
        
        html += f"<h2>归档目录结构</h2><table><tr><th>序号</th><th>目录</th><th>子目录</th></tr>"
        for i, (cat, subs) in enumerate(ARCHIVE_TEMPLATE.items(), 1):
            html += f"<tr><td>{i}</td><td><b>{cat}</b></td><td>{', '.join(subs)}</td></tr>"
        html += "</table>"
        
        html += "</body></html>"
        
        html_path = os.path.join(self.output_dir, 'archive_report.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return html_path


class OutputValidator:
    @staticmethod
    def validate(manifest, stats):
        errors = []
        if not manifest:
            errors.append("文件清单为空")
        if stats.get('total_files', 0) > 10000:
            errors.append(f"文件数量异常大: {stats['total_files']}，请确认")
        return errors


def main(project_dir, project_name='PROJECT', output_dir=None, copy_files=False, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            errors = InputValidator.validate(project_dir)
            if errors and attempt >= max_retries:
                raise RuntimeError(f"输入校验失败: {errors}")
            
            archiver = ProjectArchiver(project_dir, project_name, output_dir)
            logger, log_path = setup_logger(archiver.output_dir)
            logger.info(f"ATS-010 项目归档: {project_dir}")
            
            # 创建归档目录
            archive_root, created_dirs = archiver.create_archive_structure()
            logger.info(f"创建归档目录: {archive_root}, {len(created_dirs)}个子目录")
            
            # 扫描清单
            manifest, stats = archiver.scan_and_inventory()
            logger.info(f"文件清单: {stats['total_files']}个文件, {stats['total_size_mb']}MB")
            
            # 自动分类
            classification = archiver.classify_files()
            
            # 生成报告
            csv_path = archiver.export_manifest_csv()
            html_path = archiver.generate_html_report()
            
            # 可选: 复制文件
            copy_log = None
            if copy_files:
                copy_log = archiver.generate_archive_package(classification, archive_root)
                logger.info(f"文件复制: {len(copy_log)}个, 成功{sum(1 for c in copy_log if c['status']=='OK')}个")
            
            output_errors = OutputValidator.validate(manifest, stats)
            if output_errors:
                logger.warning(f"输出校验: {output_errors}")
            
            report = {
                'task': '项目归档', 'skill_id': 'ATS-010', 'version': 'V5.0',
                'timestamp': datetime.now().isoformat(),
                'project_name': project_name,
                'project_dir': str(project_dir),
                'archive_dir': archive_root,
                'stats': stats,
                'classification_summary': {k: len(v) for k, v in classification.items()},
                'copy_log': copy_log
            }
            
            report_path = os.path.join(archiver.output_dir, 'archive_report.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            return {
                'archive_dir': archive_root,
                'manifest_csv': csv_path,
                'report_html': html_path,
                'report_json': report_path,
                'log': str(log_path),
                'summary': {
                    'files': stats['total_files'],
                    'size_mb': stats['total_size_mb'],
                    'types': len(stats['file_types'])
                }
            }
            
        except Exception as e:
            if attempt >= max_retries:
                raise RuntimeError(f"[3轮熔断] ATS-010失败: {e}")
            continue


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ATS-010 项目归档')
    parser.add_argument('dir', help='项目目录路径')
    parser.add_argument('-n', '--name', default='PROJECT', help='项目名称')
    parser.add_argument('-o', '--output', default=None)
    parser.add_argument('-c', '--copy', action='store_true', help='复制文件至归档目录')
    args = parser.parse_args()
    result = main(args.dir, args.name, args.output, args.copy)
    print(f"归档完成: {result['summary']}")
```

---

## 验收检查单

| 序号 | 检查项 | 标准 |
|------|--------|------|
| 1 | 归档目录 | 7大类+多级子目录完整创建 |
| 2 | 文件清单 | 含相对路径/大小/MD5/修改时间 |
| 3 | 文件分类 | 按扩展名自动归类至对应目录 |
| 4 | 统计报表 | 总数/大小/类型分布 |
| 5 | MD5校验 | ≤50MB文件自动计算MD5 |
| 6 | HTML报告 | 含统计卡片+类型分布+目录结构 |
