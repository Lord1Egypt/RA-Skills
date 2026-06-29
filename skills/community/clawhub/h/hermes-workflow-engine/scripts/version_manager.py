"""
Hermes Workflow Version Manager v1.0
版本管理 — 版本化存储、对比、回滚、变更日志
"""

import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from copy import deepcopy


WORKFLOWS_DIR = Path.home() / '.hermes' / 'workflow-engine' / 'workflows'


class VersionManager:
    """工作流版本管理器"""

    def __init__(self, workflows_dir: str = None):
        self.workflows_dir = Path(workflows_dir or WORKFLOWS_DIR)
        self.workflows_dir.mkdir(parents=True, exist_ok=True)

    def _wf_dir(self, name: str) -> Path:
        return self.workflows_dir / name

    def _version_path(self, name: str, version: str) -> Path:
        return self._wf_dir(name) / f"v{version}.yaml"

    def _current_link(self, name: str) -> Path:
        return self._wf_dir(name) / 'current.yaml'

    def _changelog_path(self, name: str) -> Path:
        return self._wf_dir(name) / 'changelog.md'

    def _metrics_path(self, name: str) -> Path:
        return self._wf_dir(name) / 'metrics.json'

    # ─── 版本操作 ─────────────────────────────────────────

    def save_version(self, name: str, yaml_content: str, version: str = None, message: str = "") -> dict:
        """保存新版本"""
        import yaml
        spec = yaml.safe_load(yaml_content)
        if not version:
            version = spec.get('version', '1.0')

        wf_dir = self._wf_dir(name)
        wf_dir.mkdir(parents=True, exist_ok=True)

        # 保存版本文件
        vpath = self._version_path(name, version)
        with open(vpath, 'w', encoding='utf-8') as f:
            f.write(yaml_content)

        # 更新current链接
        current = self._current_link(name)
        if current.is_symlink() or current.exists():
            current.unlink()
        current.symlink_to(vpath.name)

        # 更新变更日志
        self._append_changelog(name, version, message, yaml_content)

        # 更新元信息
        meta = self._load_meta(name)
        meta['versions'].append({
            'version': version,
            'saved_at': datetime.now().isoformat(),
            'message': message,
            'hash': hashlib.md5(yaml_content.encode()).hexdigest()[:8],
        })
        meta['current'] = version
        self._save_meta(name, meta)

        return {'name': name, 'version': version, 'path': str(vpath)}

    def list_versions(self, name: str) -> list:
        """列出所有版本"""
        wf_dir = self._wf_dir(name)
        if not wf_dir.exists():
            return []
        versions = []
        for f in sorted(wf_dir.glob('v*.yaml')):
            v = f.stem[1:]  # 去掉'v'前缀
            versions.append({
                'version': v,
                'path': str(f),
                'size': f.stat().st_size,
                'modified': datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
        return versions

    def get_current(self, name: str) -> str:
        """获取当前版本的YAML内容"""
        current = self._current_link(name)
        if current.is_symlink():
            target = current.resolve()
            if target.exists():
                return target.read_text(encoding='utf-8')
        # fallback: 找最新版本
        versions = self.list_versions(name)
        if versions:
            return Path(versions[-1]['path']).read_text(encoding='utf-8')
        return None

    def get_version(self, name: str, version: str) -> str:
        """获取指定版本"""
        vpath = self._version_path(name, version)
        if vpath.exists():
            return vpath.read_text(encoding='utf-8')
        return None

    def rollback(self, name: str, version: str) -> dict:
        """回滚到指定版本"""
        content = self.get_version(name, version)
        if not content:
            return {'success': False, 'error': f'版本 {version} 不存在'}

        # 创建新版本（回滚版本+1）
        import yaml
        spec = yaml.safe_load(content)
        old_ver = spec.get('version', version)
        spec['version'] = version
        new_yaml = yaml.dump(spec, allow_unicode=True, default_flow_style=False)

        # 更新current链接
        current = self._current_link(name)
        if current.is_symlink() or current.exists():
            current.unlink()
        current.symlink_to(self._version_path(name, version).name)

        # 记录回滚
        meta = self._load_meta(name)
        meta['current'] = version
        meta.setdefault('rollbacks', []).append({
            'from': old_ver,
            'to': version,
            'at': datetime.now().isoformat(),
        })
        self._save_meta(name, meta)
        self._append_changelog(name, version, f"回滚到版本 {version}", content)

        return {'success': True, 'name': name, 'rolled_back_to': version}

    # ─── 版本对比 ─────────────────────────────────────────

    def diff(self, name: str, v1: str, v2: str) -> dict:
        """对比两个版本"""
        import yaml
        content1 = self.get_version(name, v1)
        content2 = self.get_version(name, v2)
        if not content1 or not content2:
            return {'error': '版本不存在'}

        spec1 = yaml.safe_load(content1)
        spec2 = yaml.safe_load(content2)

        changes = []

        # 步骤对比
        steps1 = {s['id']: s for s in spec1.get('steps', [])}
        steps2 = {s['id']: s for s in spec2.get('steps', [])}

        added = set(steps2.keys()) - set(steps1.keys())
        removed = set(steps1.keys()) - set(steps2.keys())
        common = set(steps1.keys()) & set(steps2.keys())

        for sid in added:
            changes.append({'type': 'added', 'step': sid, 'detail': steps2[sid]})
        for sid in removed:
            changes.append({'type': 'removed', 'step': sid, 'detail': steps1[sid]})
        for sid in common:
            if json.dumps(steps1[sid], sort_keys=True) != json.dumps(steps2[sid], sort_keys=True):
                changes.append({
                    'type': 'modified', 'step': sid,
                    'old': steps1[sid], 'new': steps2[sid]
                })

        # 其他字段对比
        for key in ['name', 'description', 'trigger', 'resources']:
            if spec1.get(key) != spec2.get(key):
                changes.append({
                    'type': 'field_changed', 'field': key,
                    'old': spec1.get(key), 'new': spec2.get(key)
                })

        return {
            'v1': v1, 'v2': v2,
            'total_changes': len(changes),
            'changes': changes,
        }

    # ─── 指标追踪 ─────────────────────────────────────────

    def record_run(self, name: str, version: str, metrics: dict):
        """记录运行指标"""
        mpath = self._metrics_path(name)
        data = {}
        if mpath.exists():
            data = json.loads(mpath.read_text())

        key = f"v{version}"
        data.setdefault(key, []).append({
            'run_at': datetime.now().isoformat(),
            'duration': metrics.get('duration'),
            'tokens': metrics.get('tokens'),
            'success': metrics.get('success'),
            'steps_completed': metrics.get('steps_completed'),
            'steps_total': metrics.get('steps_total'),
        })

        mpath.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def get_metrics(self, name: str, version: str = None) -> dict:
        """获取运行指标"""
        mpath = self._metrics_path(name)
        if not mpath.exists():
            return {}
        data = json.loads(mpath.read_text())
        if version:
            return data.get(f"v{version}", [])
        return data

    # ─── 内部方法 ─────────────────────────────────────────

    def _load_meta(self, name: str) -> dict:
        meta_path = self._wf_dir(name) / 'meta.json'
        if meta_path.exists():
            return json.loads(meta_path.read_text())
        return {'name': name, 'versions': [], 'current': None}

    def _save_meta(self, name: str, meta: dict):
        meta_path = self._wf_dir(name) / 'meta.json'
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    def _append_changelog(self, name: str, version: str, message: str, content: str):
        cpath = self._changelog_path(name)
        entry = f"\n## v{version} ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
        if message:
            entry += f"{message}\n\n"
        # 提取步骤列表
        import yaml
        try:
            spec = yaml.safe_load(content)
            steps = spec.get('steps', [])
            entry += f"步骤 ({len(steps)}):\n"
            for s in steps:
                entry += f"- [{s.get('type', 'llm')}] {s.get('name', s['id'])}\n"
        except:
            pass
        entry += "\n---\n"

        with open(cpath, 'a', encoding='utf-8') as f:
            f.write(entry)

    # ─── 列表 ─────────────────────────────────────────────

    def list_workflows(self) -> list:
        """列出所有已管理工作流"""
        workflows = []
        for d in sorted(self.workflows_dir.iterdir()):
            if d.is_dir() and not d.name.startswith('_'):
                meta = self._load_meta(d.name)
                versions = self.list_versions(d.name)
                workflows.append({
                    'name': d.name,
                    'current': meta.get('current'),
                    'versions': len(versions),
                    'latest': versions[-1]['version'] if versions else None,
                })
        return workflows


def format_version_list(name: str, versions: list, current: str = None) -> str:
    """格式化版本列表"""
    lines = [f"═══ {name} 版本列表 ═══", ""]
    for v in versions:
        tag = " ← current" if v['version'] == current else ""
        lines.append(f"  v{v['version']}{tag}")
        lines.append(f"    修改时间: {v['modified'][:16]}")
        lines.append(f"    文件大小: {v['size']} bytes")
    return '\n'.join(lines)


def format_diff_report(diff: dict) -> str:
    """格式化对比报告"""
    lines = [
        f"═══ 版本对比: v{diff['v1']} → v{diff['v2']} ═══",
        f"变更总数: {diff['total_changes']}",
        "",
    ]
    for change in diff['changes']:
        if change['type'] == 'added':
            lines.append(f"  ➕ 新增步骤: {change['step']}")
        elif change['type'] == 'removed':
            lines.append(f"  ➖ 删除步骤: {change['step']}")
        elif change['type'] == 'modified':
            lines.append(f"  📝 修改步骤: {change['step']}")
        elif change['type'] == 'field_changed':
            lines.append(f"  🔄 字段变更: {change['field']}")
    return '\n'.join(lines)
