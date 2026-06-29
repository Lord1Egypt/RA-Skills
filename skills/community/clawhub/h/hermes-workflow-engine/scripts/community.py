"""
Hermes Workflow Community Hub v1.0
协作共享 — 导出、导入、社区库、评分、同步
"""

import json
import tarfile
import hashlib
from pathlib import Path
from datetime import datetime


COMMUNITY_DIR = Path.home() / '.hermes' / 'workflow-engine' / '_community'
LOCAL_DIR = Path.home() / '.hermes' / 'workflow-engine' / 'workflows'


class CommunityHub:
    """工作流社区共享中心"""

    def __init__(self, community_dir: str = None):
        self.community_dir = Path(community_dir or COMMUNITY_DIR)
        self.community_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.community_dir / 'index.json'

    # ─── 导出 ─────────────────────────────────────────────

    def export_workflow(self, name: str, output_path: str = None) -> str:
        """导出工作流为.tgz包"""
        wf_dir = LOCAL_DIR / name
        if not wf_dir.exists():
            raise FileNotFoundError(f"工作流 {name} 不存在")

        if not output_path:
            output_path = str(self.community_dir / f"{name}.tgz")

        with tarfile.open(output_path, 'w:gz') as tar:
            # 打包所有版本文件
            for f in wf_dir.iterdir():
                if f.is_file() and not f.name.startswith('.'):
                    tar.add(f, arcname=f"{name}/{f.name}")

            # 添加导出元信息
            meta = self._build_export_meta(name)
            meta_bytes = json.dumps(meta, ensure_ascii=False, indent=2).encode('utf-8')
            import io
            meta_info = tarfile.TarInfo(name=f"{name}/export_meta.json")
            meta_info.size = len(meta_bytes)
            tar.addfile(meta_info, io.BytesIO(meta_bytes))

        return output_path

    def _build_export_meta(self, name: str) -> dict:
        """构建导出元信息"""
        meta_path = LOCAL_DIR / name / 'meta.json'
        meta = {}
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())

        return {
            'name': name,
            'exported_at': datetime.now().isoformat(),
            'exported_by': '小狗 Workflow Engine',
            'current_version': meta.get('current'),
            'versions': [v['version'] for v in meta.get('versions', [])],
            'description': self._get_description(name),
            'author': self._get_author(name),
            'tags': self._get_tags(name),
        }

    def _get_description(self, name: str) -> str:
        """从当前版本获取描述"""
        current = LOCAL_DIR / name / 'current.yaml'
        if current.exists():
            try:
                import yaml
                content = current.resolve().read_text(encoding='utf-8')
                spec = yaml.safe_load(content)
                return spec.get('description', '')
            except:
                pass
        return ''

    def _get_author(self, name: str) -> str:
        current = LOCAL_DIR / name / 'current.yaml'
        if current.exists():
            try:
                import yaml
                content = current.resolve().read_text(encoding='utf-8')
                spec = yaml.safe_load(content)
                return spec.get('author', 'unknown')
            except:
                pass
        return 'unknown'

    def _get_tags(self, name: str) -> list:
        current = LOCAL_DIR / name / 'current.yaml'
        if current.exists():
            try:
                import yaml
                content = current.resolve().read_text(encoding='utf-8')
                spec = yaml.safe_load(content)
                return spec.get('tags', [])
            except:
                pass
        return []

    # ─── 导入 ─────────────────────────────────────────────

    def import_workflow(self, tgz_path: str, force: bool = False) -> dict:
        """从.tgz包导入工作流"""
        tgz_path = Path(tgz_path)
        if not tgz_path.exists():
            return {'success': False, 'error': f'文件不存在: {tgz_path}'}

        with tarfile.open(tgz_path, 'r:gz') as tar:
            # 读取导出元信息
            export_meta = None
            for member in tar.getmembers():
                if member.name.endswith('export_meta.json'):
                    f = tar.extractfile(member)
                    if f:
                        export_meta = json.loads(f.read().decode('utf-8'))
                    break

            if not export_meta:
                return {'success': False, 'error': '无效的工作流包：缺少export_meta.json'}

            name = export_meta['name']
            wf_dir = LOCAL_DIR / name

            # 检查是否已存在
            if wf_dir.exists() and not force:
                return {
                    'success': False,
                    'error': f'工作流 {name} 已存在，使用 force=True 覆盖',
                    'existing_versions': len(list(wf_dir.glob('v*.yaml'))),
                }

            # 解压
            wf_dir.mkdir(parents=True, exist_ok=True)
            for member in tar.getmembers():
                if member.isfile():
                    # 去掉顶层目录名
                    parts = member.name.split('/', 1)
                    if len(parts) > 1:
                        target = wf_dir / parts[1]
                        with tar.extractfile(member) as source:
                            target.write_bytes(source.read())

        return {
            'success': True,
            'name': name,
            'description': export_meta.get('description', ''),
            'versions': export_meta.get('versions', []),
            'author': export_meta.get('author', 'unknown'),
        }

    # ─── 社区库 ─────────────────────────────────────────

    def publish_to_community(self, name: str) -> dict:
        """发布到本地社区库"""
        tgz_path = self.export_workflow(name)

        # 更新索引
        index = self._load_index()
        index[name] = {
            'name': name,
            'description': self._get_description(name),
            'author': self._get_author(name),
            'tags': self._get_tags(name),
            'published_at': datetime.now().isoformat(),
            'path': tgz_path,
            'downloads': index.get(name, {}).get('downloads', 0),
            'rating': index.get(name, {}).get('rating', 0),
            'rating_count': index.get(name, {}).get('rating_count', 0),
        }
        self._save_index(index)

        return {'success': True, 'name': name, 'path': tgz_path}

    def list_community(self, tag: str = None) -> list:
        """列出社区工作流"""
        index = self._load_index()
        workflows = list(index.values())

        if tag:
            workflows = [w for w in workflows if tag in w.get('tags', [])]

        # 按评分排序
        workflows.sort(key=lambda x: x.get('rating', 0), reverse=True)
        return workflows

    def search_community(self, keyword: str) -> list:
        """搜索社区工作流"""
        index = self._load_index()
        results = []
        keyword_lower = keyword.lower()

        for name, info in index.items():
            if (keyword_lower in name.lower() or
                keyword_lower in info.get('description', '').lower() or
                keyword_lower in ' '.join(info.get('tags', [])).lower()):
                results.append(info)

        return results

    def install_from_community(self, name: str) -> dict:
        """从社区安装工作流"""
        index = self._load_index()
        if name not in index:
            return {'success': False, 'error': f'社区中没有找到工作流: {name}'}

        info = index[name]
        tgz_path = info.get('path')

        if not tgz_path or not Path(tgz_path).exists():
            return {'success': False, 'error': '工作流包文件不存在'}

        result = self.import_workflow(tgz_path, force=True)

        if result['success']:
            # 更新下载计数
            index[name]['downloads'] = index[name].get('downloads', 0) + 1
            self._save_index(index)

        return result

    def rate_workflow(self, name: str, rating: int) -> dict:
        """评分（1-5星）"""
        if rating < 1 or rating > 5:
            return {'success': False, 'error': '评分必须在1-5之间'}

        index = self._load_index()
        if name not in index:
            return {'success': False, 'error': f'工作流不存在: {name}'}

        info = index[name]
        old_rating = info.get('rating', 0)
        old_count = info.get('rating_count', 0)

        # 计算新平均分
        new_count = old_count + 1
        new_rating = round((old_rating * old_count + rating) / new_count, 1)

        info['rating'] = new_rating
        info['rating_count'] = new_count
        index[name] = info
        self._save_index(index)

        return {'success': True, 'name': name, 'new_rating': new_rating, 'rating_count': new_count}

    # ─── 同步 ─────────────────────────────────────────────

    def check_updates(self) -> list:
        """检查本地工作流是否有更新（社区版本对比本地）"""
        index = self._load_index()
        updates = []

        for name, info in index.items():
            local_meta = LOCAL_DIR / name / 'meta.json'
            if not local_meta.exists():
                updates.append({'name': name, 'status': 'not_installed'})
                continue

            local = json.loads(local_meta.read_text())
            local_ver = local.get('current')
            # 社区最新版本从导出元信息获取
            tgz = info.get('path')
            if tgz and Path(tgz).exists():
                try:
                    with tarfile.open(tgz, 'r:gz') as tar:
                        for member in tar.getmembers():
                            if member.name.endswith('export_meta.json'):
                                f = tar.extractfile(member)
                                if f:
                                    export_meta = json.loads(f.read().decode('utf-8'))
                                    community_ver = export_meta.get('current_version')
                                    if community_ver != local_ver:
                                        updates.append({
                                            'name': name,
                                            'local_version': local_ver,
                                            'community_version': community_ver,
                                            'status': 'update_available',
                                        })
                                break
                except:
                    pass

        return updates

    # ─── 内部方法 ─────────────────────────────────────────

    def _load_index(self) -> dict:
        if self.index_path.exists():
            return json.loads(self.index_path.read_text())
        return {}

    def _save_index(self, index: dict):
        self.index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2))


def format_community_list(workflows: list) -> str:
    """格式化社区工作流列表"""
    if not workflows:
        return "社区库为空，还没有人发布工作流"

    lines = ["═══ 社区工作流库 ═══", ""]
    for w in workflows:
        stars = '⭐' * int(w.get('rating', 0))
        lines.append(f"  📦 {w['name']}")
        lines.append(f"     {w.get('description', '无描述')}")
        lines.append(f"     作者: {w.get('author', '?')} | 评分: {stars} ({w.get('rating', 0)}) | 下载: {w.get('downloads', 0)}")
        if w.get('tags'):
            lines.append(f"     标签: {', '.join(w['tags'])}")
        lines.append("")
    return '\n'.join(lines)
