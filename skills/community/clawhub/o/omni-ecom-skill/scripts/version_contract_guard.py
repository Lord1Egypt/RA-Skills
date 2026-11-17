"""Keep product, plugin and visible version identity consistent."""
import json
import re
from pathlib import Path

from adjudication_guard import require


VERSION=re.compile(r'^2\.0\.3(?:-candidate\.[1-9][0-9]*)?$')


def read(path):
    value=json.loads(path.read_text(encoding='utf-8-sig'))
    require(isinstance(value,dict),'version_json_invalid')
    return value


def validate_version_contract(root):
    root=Path(root).resolve()
    info=read(root/'version-info.json')
    version=info.get('team_version')
    require(isinstance(version,str) and VERSION.fullmatch(version),'team_version_invalid')
    require(info.get('team_id')=='omni-ecom' and info.get('previous_version')=='2.0.2',
            'version_lineage_invalid')
    status=info.get('release_status')
    require(status in ('candidate','released'),'release_status_invalid')
    if status=='candidate':
        require('-candidate.' in version and info.get('release_ready') is False and info.get('release_date') is None,
                'candidate_metadata_invalid')
    else:
        require(version=='2.0.3' and info.get('release_ready') is True and
                isinstance(info.get('release_date'),str) and re.fullmatch(r'20\d{2}-\d{2}-\d{2}',info['release_date']),
                'released_metadata_invalid')
    changes=info.get('changes')
    require(isinstance(changes,list) and len(changes)>=4 and len(changes)==len(set(changes)) and
            all(isinstance(x,str) and x.strip() for x in changes),'version_changes_invalid')
    plugin=read(root/'.codebuddy-plugin'/'plugin.json')
    require(plugin.get('name')=='omni-ecom' and plugin.get('version')==version,'plugin_version_drift')
    skill=(root/'SKILL.md').read_text(encoding='utf-8-sig')
    readme=(root/'README.md').read_text(encoding='utf-8-sig')
    lead=(root/'agents'/'omni-ecom-team-lead.md').read_text(encoding='utf-8-sig')
    require(version in skill and version in readme and version in lead,'visible_version_drift')
    require(('候选版不得安装成正式版' in skill) if status=='candidate' else
            ('candidate_version_not_release_ready' not in skill),'visible_release_status_drift')
    return dict(status='version_contract_verified',team_version=version,previous_version='2.0.2',
                release_status=status,release_ready=info['release_ready'])
