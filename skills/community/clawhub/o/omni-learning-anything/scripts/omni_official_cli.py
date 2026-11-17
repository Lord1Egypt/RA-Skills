"""Official CLI API transports; upstream tools own credentials and login lifecycle."""
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


class CLIError(RuntimeError):
    def __init__(self, kind='operation', scopes=()):
        self.kind=kind if kind in ('authorization','authentication','config','network','validation','region','operation') else 'operation'
        self.scopes=[s for s in scopes if isinstance(s,str) and re.fullmatch(r'[a-zA-Z0-9_.:-]{1,140}',s)]
        super().__init__('Official CLI '+self.kind+' failed; check connection guidance and reconcile any existing write.')


def run(args, *, input=None, cwd=None, env=None, timeout=90):
    try:
        r=subprocess.run(args,input=input,cwd=cwd,env=env,capture_output=True,text=True,timeout=timeout)
        if r.returncode:
            try: error=json.loads(r.stderr).get('error',{})
            except (ValueError,AttributeError): error={}
            raise CLIError(error.get('type'),error.get('missing_scopes',[]))
        value=json.loads(r.stdout)
        if not isinstance(value,dict): raise CLIError()
        if value.get('ok') is False:
            error=value.get('error',{});raise CLIError(error.get('type'),error.get('missing_scopes',[]))
        return value
    except CLIError: raise
    except Exception: raise CLIError() from None


def api_path(url, host, prefix):
    u=urlsplit(url)
    if u.scheme!='https' or u.hostname!=host or u.username or u.password or u.port not in (None,443) or u.query or u.fragment or not u.path.startswith(prefix):
        raise ValueError('Use only the selected official API endpoint.')
    return u.path


class NotionCLI:
    def __init__(self,target,runner=None):
        self.target=target;self.runner=runner or run

    def environment(self):
        env=dict(os.environ,NOTION_API_BASE_URL='https://api.notion.com',NOTION_ENV='prod',NO_COLOR='1',NO_HYPERLINK='1')
        workspace=self.target.get('destination',{}).get('workspace_id')
        if workspace:env['NOTION_WORKSPACE_ID']=workspace
        return env

    def json(self,method,url,**kw):
        path=api_path(url,'api.notion.com','/v1/')
        args=['ntn','api',path,'-X',method,'--notion-version','2026-03-11']
        for key,value in kw.get('params',{}).items():args.append(str(key)+'=='+str(value))
        body=None
        if 'json' in kw:
            args.extend(['--data','@-']);body=json.dumps(kw['json'],ensure_ascii=False)
        if kw.get('files'):
            if body is not None:raise ValueError('Do not mix multipart and JSON bodies.')
            f=kw['files']['file'][1];args.extend(['--file',str(Path(f.name).resolve())])
        return self.runner(args,input=body,env=self.environment())

    def check_identity(self):
        user=self.json('GET','https://api.notion.com/v1/users/me')
        ident=user.get('id')
        if not isinstance(ident,str) or not ident:raise ValueError('Notion identity was not verified.')
        if self.target.get('account_id') and ident!=self.target['account_id']:raise ValueError('Notion account changed; reconnect the confirmed account.')
        return {'id':ident,'name':user.get('name','')}


class FeishuCLI:
    def __init__(self,target,root=None,runner=None):
        self.target=target;self.root=Path(root or Path.cwd()).resolve();self.runner=runner or run;self.identity_checked=False

    def call(self,args,**kw):
        argv=['lark-cli']
        if self.target.get('cli_profile'):argv+=['--profile',self.target['cli_profile']]
        env=dict(os.environ,LARKSUITE_CLI_NO_UPDATE_NOTIFIER='1',LARKSUITE_CLI_NO_SKILLS_NOTIFIER='1')
        return self.runner(argv+args,env=env,cwd=self.root,**kw)

    def check_identity(self):
        self.identity_checked=False
        raw=self.call(['auth','status','--json','--verify'])
        data=raw.get('data',raw);user=data.get('identities',{}).get('user',{})
        ident=user.get('openId')
        if data.get('brand')!='feishu':raise CLIError('region')
        if user.get('available') is not True or user.get('verified') is not True or not isinstance(ident,str) or not ident:
            raise CLIError('authentication')
        if self.target.get('account_id') and ident!=self.target['account_id']:raise ValueError('Feishu account changed; reconnect the confirmed account.')
        self.identity_checked=True
        return {'id':ident,'name':user.get('userName','')}

    def json(self,method,url,**kw):
        path=api_path(url,'open.feishu.cn','/open-apis/')
        if not self.identity_checked:self.check_identity()
        params=kw.get('params',{});body=kw.get('json',kw.get('data'))
        args=['api',method,path,'--as','user','--json'];stdin=None
        # Folder listing has a typed resource; docx/import APIs lack typed commands.
        if method=='GET' and path=='/open-apis/drive/v1/files':
            args=['drive','files','list','--as','user','--json']
        if params:args+=['--params',json.dumps(params)]
        if kw.get('files'):
            file=Path(kw['files']['file'][1].name).resolve()
            if not file.is_relative_to(self.root):raise ValueError('Upload must use a reviewed file inside the course.')
            args+=['--file','file='+file.relative_to(self.root).as_posix()]
            if body is not None:args+=['--data',json.dumps(body)]
        elif body is not None:
            args+=['--data','-'];stdin=json.dumps(body,ensure_ascii=False)
        result=self.call(args,input=stdin)
        if result.get('ok') is not True or result.get('identity')!='user':raise ValueError('Feishu command did not confirm user identity and success.')
        value=result.get('data')
        if not isinstance(value,dict):raise ValueError('Feishu API returned no structured document data.')
        return value if 'code' in value else {'code':0,'data':value}
