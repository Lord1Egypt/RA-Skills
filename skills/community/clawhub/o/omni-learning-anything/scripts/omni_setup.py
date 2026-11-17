"""Selected-route setup recipe. No installs, remote probes, login or settings writes."""
import importlib.util
import shutil
import sys
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from omni_delivery import MODES,default_formats

PACKAGES={'tzdata':'tzdata>=2025.1','docx':'python-docx>=1.1,<2','PIL':'Pillow>=10,<13','pypdf':'pypdf>=5,<7',
          'pypdfium2':'pypdfium2>=4,<6','requests':'requests>=2.32,<3','keyring':'keyring>=25.0,<26','qcloud_cos':'cos-python-sdk-v5>=1.9,<2'}
TOOLS={'notion':('ntn','https://developers.notion.com/cli/get-started/installation'),
       'feishu':('lark-cli','https://github.com/larksuite/cli'),
       'dingtalk':('dws','https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases')}
DEFAULT_MODES={'obsidian':'local','notion':'cli','feishu':'cli','dingtalk':'cli','tencent':'mcp'}


def plan(platform,mode=None,*,material_format=None):
    mode=mode or DEFAULT_MODES.get(platform,'local')
    if platform not in MODES or mode not in MODES[platform]:raise ValueError('Choose a supported destination and mode before setup.')
    if material_format not in (None,'pdf','txt','markdown','html','docx','doc','rtf','epub','pptx','srt','vtt'):
        raise ValueError('Choose a documented input format; extraction is not guaranteed by setup.')
    formats=default_formats({'delivery':{'platform':platform,'mode':mode}});modules=[];tools=[]
    try:ZoneInfo('UTC')
    except ZoneInfoNotFoundError:modules.append('tzdata')
    if 'docx' in formats:modules+=['docx','PIL']
    if 'pdf' in formats:modules+=['pypdf','pypdfium2'];tools.append({'name':'XeLaTeX','next_action':'Check the existing official TeX distribution; compile and inspect the actual plan to verify packages/fonts.'})
    if material_format=='pdf' and 'pypdf' not in modules:modules.append('pypdf')
    if mode in ('api','mcp'):modules.append('requests')
    if platform=='tencent' and mode=='mcp':modules.append('keyring')
    if platform=='tencent' and mode=='api':modules.append('qcloud_cos')
    if mode=='cli':
        name,url=TOOLS[platform];binary=shutil.which(name)
        tools.append({'name':name,'available':bool(binary),'path':binary,'official_install':url,
                      'next_action':'Reuse the installed official CLI and inspect status; install from the official source only if absent.'})
    missing=[]
    for module in modules:
        try:found=importlib.util.find_spec(module) is not None
        except (ImportError,ValueError):found=False
        if not found:missing.append(module)
    packages=[PACKAGES[m] for m in modules]
    cloud=platform in ('notion','feishu','dingtalk','tencent','generic')
    return {'platform':platform,'mode':mode,'python':sys.version.split()[0],'formats':formats,'modules':modules,
            'packages':packages,'missing_modules':missing,
            'pip_argv':[sys.executable,'-m','pip','install',*[PACKAGES[m] for m in missing]] if missing else [],
            'tools':tools,'authorization':'unknown' if cloud else 'not_required','native_discovery':'unknown',
            'next_action':'Use/reuse the selected named connection; ask only for missing location/official authorization, then doctor and actual plan publish/readback.' if cloud else 'Confirm the external course folder, run doctor with selected settings, render and inspect the actual plan.',
            'note':'Agent-operated recipe only. Use a supported interpreter/isolated environment outside the Skill folder. No dependency install, authorization, discovery or successful delivery is inferred.'}
