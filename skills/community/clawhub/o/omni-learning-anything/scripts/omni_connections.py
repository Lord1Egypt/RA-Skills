"""Guided read-only connection checks and metadata-only reusable profiles."""
import json
import os
import re
import shutil
import shlex
import stat
import sys
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from omni_delivery import validate_delivery
from omni_official_cli import CLIError,NotionCLI,FeishuCLI
from omni_http import business

GUIDE='references/onboarding.md'
INSTALL={'notion':'npm install --global ntn','feishu':'npx @larksuite/cli@latest install'}


def location(platform,value):
    if platform=='obsidian':
        path=Path(value).expanduser().resolve()
        if not path.is_dir():raise ValueError('Select an existing Obsidian Vault directory.')
        return {'vault_path':str(path)}
    u=urlsplit(value);host=u.hostname or ''
    if u.scheme!='https' or u.username or u.password or u.port not in (None,443) or any(re.search(r'token|secret|key|auth',k,re.I) for k in parse_qs(u.query)):
        raise ValueError('Use an official page/folder HTTPS link without credentials.')
    if platform=='notion':
        if not any(host==h or host.endswith('.'+h) for h in ('notion.so','notion.site','notion.com')):raise ValueError('Select a Notion parent-page link.')
        found=re.search(r'([a-fA-F0-9]{32}|[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12})/?$',u.path)
        if not found:raise ValueError('Notion parent link needs a page identifier.')
        return {'parent_page_id':found.group(1).replace('-','').lower()}
    if platform=='feishu':
        found=re.fullmatch(r'/drive/folder/([a-zA-Z0-9]+)/?',u.path)
        if not (host=='feishu.cn' or host.endswith('.feishu.cn')) or not found:raise ValueError('Select a Feishu course folder link, not a document or Wiki link.')
        return {'folder_token':found.group(1)}
    if platform=='tencent':
        if host!='docs.qq.com':raise ValueError('Select an official Tencent Docs folder or home link.')
        if u.path.rstrip('/') in ('/desktop','/desktop/mydoc'):return {'folder_id':'/'}
        found=re.fullmatch(r'/desktop/mydoc/folder/([A-Za-z0-9_-]+)/?',u.path)
        if not found:raise ValueError('Select a Tencent personal folder link or confirm the home root.')
        return {'folder_id':found.group(1)}
    if platform=='dingtalk':
        found=re.fullmatch(r'/i/nodes/([A-Za-z0-9_-]+)/?',u.path)
        if host!='alidocs.dingtalk.com' or not found:raise ValueError('Select an official DingTalk document folder link.')
        return {'folder_id':found.group(1)}
    raise ValueError('Guided connect currently supports Notion, Feishu and Obsidian.')


def directory(base=None):
    return Path(base) if base is not None else Path.home()/'.config/omni-learning-anything/connections'


def profile_path(name,base=None):
    if not isinstance(name,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',name):raise ValueError('Connection name: lowercase letters, digits, hyphens or underscores; start with a letter.')
    return directory(base)/(name+'.json')


def load(name,base=None):
    path=profile_path(name,base)
    if path.is_symlink():raise ValueError('Connection profiles cannot be symlinks.')
    info=path.stat()
    if os.name=='posix' and (info.st_uid!=os.getuid() or stat.S_IMODE(info.st_mode)&0o077):raise ValueError('Connection profile must be owned by this user with owner-only permissions.')
    value=json.loads(path.read_text())
    if not isinstance(value,dict) or set(value)!={'version','delivery'} or value['version']!=1:raise ValueError('Invalid connection profile.')
    validate_delivery(value['delivery'])
    return value['delivery']


def save(name,target,base=None):
    validate_delivery(target);path=profile_path(name,base)
    if path.exists() or path.is_symlink():
        if load(name,base)==target:return
        raise ValueError('Connection name already exists; choose a new name to preserve approved courses.')
    parent=path.parent
    if parent.is_symlink():raise ValueError('Connection directory cannot be a symlink.')
    parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    value=json.dumps({'version':1,'delivery':target},ensure_ascii=False,indent=2)
    flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0)
    fd=os.open(path,flags,0o600)
    with os.fdopen(fd,'w') as f:f.write(value+'\n')


def list_connections(base=None):
    result=[];parent=directory(base)
    if not parent.exists():return result
    for path in sorted(parent.glob('*.json')):
        if path.is_symlink():continue
        try:target=load(path.stem,base)
        except (ValueError,OSError):continue
        result.append({'name':path.stem,'delivery':target})
    return result


def blocked(platform,stage,action,command=None,scopes=()):
    result={'ready':False,'platform':platform,'stage':stage,'next_action':action,'guide':GUIDE}
    if command:
        if isinstance(command,list):
            result['agent_argv']=command;result['agent_command']=shlex.join(command)
        else:result['agent_command']=command
    if scopes:result['missing_scopes']=list(scopes)
    return result


def connect(platform=None,value=None,*,client=None,save_as=None,profile_dir=None,connection=None,cli_profile=None,workspace_id=None,auth_profile=None,subdir='Omni Learning'):
    if connection:
        if any(x is not None for x in (platform,value,cli_profile,workspace_id,auth_profile)):raise ValueError('Reuse the saved connection without overriding its account/destination; create a new named connection for changes.')
        target=load(connection,profile_dir);platform=target['platform']
    else:
        if platform not in ('notion','feishu','obsidian','dingtalk','tencent'):raise ValueError('Choose Notion, Feishu, DingTalk, Tencent Docs or Obsidian.')
        if not value:return blocked(platform,'location','Ask only for the course parent-page/folder link, or the local Vault path.')
        dest=location(platform,value)
        if platform=='obsidian':dest['subdir']=subdir
        if platform=='notion' and workspace_id:dest['workspace_id']=workspace_id
        target={'platform':platform,'mode':'local' if platform=='obsidian' else ('mcp' if platform=='tencent' else 'cli'),'destination':dest}
        if auth_profile:
            if platform!='tencent':raise ValueError('OAuth authorization profiles apply only to Tencent Docs.')
            target['auth_profile']=auth_profile
        if cli_profile:
            if platform not in ('feishu','dingtalk'):raise ValueError('CLI profiles apply to Feishu or DingTalk.')
            target['cli_profile']=cli_profile
    validate_delivery(target)
    if platform=='obsidian':
        path=Path(target['destination']['vault_path'])
        if not path.is_dir() or not os.access(path,os.W_OK):return blocked(platform,'destination','Make the confirmed Vault directory available and writable.')
        identity=None
    elif platform=='tencent':
        from omni_tencent_mcp import Client
        if not target.get('auth_profile'):
            return blocked(platform,'authorization','Agent starts official Tencent OAuth login and shows the exact link; learner reviews the account and document permissions.',[sys.executable,str(Path(__file__).with_name('omni_learning.py')),'tencent-auth','login','--name','personal-tencent'])
        client=client or Client(target)
        try:
            identity=client.check_identity();target['account_id']=identity['id'];client.check_destination(target['destination'])
        except (ValueError,RuntimeError):return blocked(platform,'authorization','Check the selected OAuth profile and exact account/permission error; keep this destination. Reauthorize only if needed.',['omni_learning.py','tencent-auth','login','--name',target['auth_profile']])
    elif platform=='dingtalk':
        from omni_dingtalk import DingTalkCLI
        if not shutil.which('dws'):return blocked(platform,'install','Agent installs the official dws CLI after verifying the release checksum.','https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases')
        client=client or DingTalkCLI(target)
        try:
            identity=client.check_identity();target['account_id']=identity['id']
            target['cli_profile']=target.get('cli_profile') or identity['id']
            if isinstance(client,DingTalkCLI):client.target=target
            client.check_destination(target['destination'])
        except (ValueError,RuntimeError):return blocked(platform,'authorization','Check current dws auth status/doctor; complete official login or the exact organization CLI permission if required. Preserve the selected organization and folder.',['dws','auth','login'])
    else:
        binary={'notion':'ntn','feishu':'lark-cli'}[platform]
        if not shutil.which(binary):return blocked(platform,'install','Agent installs ' + binary + ' from its official distribution, then checks existing authorization.',INSTALL[platform])
        client=client or (NotionCLI(target) if platform=='notion' else FeishuCLI(target))
        try:
            identity=client.check_identity()
            target['account_id']=identity['id']
        except (CLIError,ValueError,RuntimeError) as error:
            if isinstance(error,CLIError) and error.kind=='region':
                return blocked(platform,'configuration','Selected CLI profile is not Feishu. Choose a confirmed Feishu application profile; do not overwrite the existing Lark profile or change an approved course account/location.')
            config=platform=='feishu' and isinstance(error,CLIError) and error.kind=='config'
            if platform=='notion':command=['ntn','login','--no-browser']
            elif config:
                command=['lark-cli','config','init','--new','--brand','feishu','--lang','zh']
                if target.get('cli_profile'):command+=['--name',target['cli_profile']]
            else:
                command=['lark-cli']
                if target.get('cli_profile'):command+=['--profile',target['cli_profile']]
                command+=['auth','login','--domain','docs','--domain','drive','--no-wait','--json']
            return blocked(platform,'authorization','Agent initiates official authorization; user reviews the account and requested document permissions. Do not paste passwords or tokens into chat.',command,getattr(error,'scopes',()))
        try:
            if platform=='notion':
                page=client.json('GET','https://api.notion.com/v1/pages/'+target['destination']['parent_page_id'])
                if str(page.get('id','')).replace('-','').lower()!=target['destination']['parent_page_id'].replace('-','').lower() or page.get('archived') or page.get('in_trash'):raise ValueError('Parent unavailable.')
            else:
                business(client.json('GET','https://open.feishu.cn/open-apis/drive/v1/files',params={'folder_token':target['destination']['folder_token'],'page_size':1}),'code')
        except Exception as error:
            return blocked(platform,'destination','The current identity cannot confirm the requested destination. Check the original link/access or exact missing permission; preserve this platform.',scopes=getattr(error,'scopes',()))
    if save_as:save(save_as,target,profile_dir)
    result={'ready':True,'platform':platform,'delivery':target,'guide':GUIDE,'note':'Read-only connection check; publish and inspect an actual document before claiming successful delivery.'}
    if identity:result['account']={'id':identity['id'],'name':identity.get('name','')}
    if save_as or connection:result['connection']=save_as or connection
    return result
