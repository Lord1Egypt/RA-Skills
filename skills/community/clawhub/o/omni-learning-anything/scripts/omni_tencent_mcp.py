"""Tencent Docs official OAuth/MCP API. No browser state or cookie access."""
import json
from omni_tencent_auth import Auth
ENDPOINT='https://docs.qq.com/openapi/mcp'

class MCPError(RuntimeError):
    def __init__(self,kind):self.kind=kind;super().__init__('Tencent MCP operation failed: '+kind+'. Preserve and reconcile existing writes.')

def unpack(response):
    if response.get('error'):
        import re
        message=response['error'].get('message','')
        kind='not_found' if re.search(r'\bcode:323908\b',message) else ('permission' if re.search(r'\bcode:400007\b',message) else 'rejected')
        raise MCPError(kind)
    result=response.get('result',{})
    if isinstance(result.get('structuredContent'),dict) and result['structuredContent'].get('error'):raise MCPError('business_error')
    if result.get('isError'):raise RuntimeError('Tencent document tool failed; check the exact account entitlement and permissions, then reconcile writes.')
    if isinstance(result.get('structuredContent'),dict):return result['structuredContent']
    for item in result.get('content',[]):
        if item.get('type')=='text':
            try:
                value=json.loads(item['text'])
                if isinstance(value,dict):return value
            except (ValueError,KeyError):pass
    raise RuntimeError('Tencent MCP response has no structured object.')

class Client:
    def __init__(self,target,transport=None):self.target=target;self.transport=transport
    def rpc(self,method,params):
        if self.transport:return self.transport(method,params)
        import requests
        token=Auth().token(self.target['auth_profile'])
        try:
            r=requests.post(ENDPOINT,headers={'Authorization':'Bearer '+token,'Accept':'application/json, text/event-stream'},json={'jsonrpc':'2.0','id':1,'method':method,'params':params},timeout=(10,60),allow_redirects=False)
            if r.status_code!=200:raise RuntimeError()
            return r.json()
        except Exception:raise RuntimeError('Tencent MCP request failed; check connectivity/authorization and reconcile uncertain writes.') from None
    def call(self,name,args=None):return unpack(self.rpc('tools/call',{'name':name,'arguments':args or {}}))
    def check_identity(self):
        value=self.call('get_user_info');identity=value.get('user_id')
        if not isinstance(identity,str) or not identity:raise ValueError('Tencent identity could not be confirmed.')
        if self.target.get('account_id') and self.target['account_id']!=identity:raise ValueError('Tencent account changed; preserve the course account and destination.')
        return {'id':identity,'name':value.get('nick','')}
    def check_destination(self,dest):
        folder=dest['folder_id']
        if folder=='/':return self.call('manage.folder_list',{'start':0})
        return self.call('manage.query_folder_meta',{'folder_id':folder})

def upload_url(url):
    from urllib.parse import urlsplit
    u=urlsplit(url);host=u.hostname or ''
    if u.scheme!='https' or u.username or u.password or u.port not in (None,443) or not (host=='docs.qq.com' or host.endswith('.myqcloud.com')):raise ValueError('Unexpected official Tencent upload host.')
    return url

def put_file(path,url):
    import requests
    upload_url(url)
    try:
        with path.open('rb') as stream:r=requests.put(url,data=stream,timeout=(10,90),allow_redirects=False)
        if r.status_code not in (200,201,204):raise RuntimeError()
    except Exception:raise RuntimeError('Tencent signed upload failed. Resume the retained import task after checking connectivity.') from None

def folder_contains(client,folder,file_id):
    start=0
    for _ in range(100):
        value=client.call('manage.folder_list',{'folder_id':'' if folder=='/' else folder,'start':start})
        items=value.get('list',[])
        if any(x.get('id')==file_id and not x.get('is_folder') for x in items):return True
        if value.get('finish') is True or not items:return False
        start+=len(items)
    raise ValueError('Tencent folder listing exceeded the verification limit.')

def publish(root,manifest,target,receipt,checkpoint,client=None,uploader=None):
    import hashlib,re
    from omni_http import document_data,segment,HTTP,verified
    from omni_tencent import check_docx
    from omni_delivery import verify_url
    client=client or Client(target);uploader=uploader or put_file
    client.check_identity();data=document_data(root,manifest);path=root/manifest['artifacts']['docx']
    if len(data['title'])>36:raise ValueError('Tencent document titles may contain at most 36 characters; agree a shorter title before rendering.')
    if path.stat().st_size>100*1024*1024:raise ValueError('Tencent DOCX import limit is 100 MB.')
    if not receipt.get('task_id') and not receipt.get('remote_id'):
        md5=hashlib.md5(path.read_bytes()).hexdigest();filename=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',data['title'])+'.docx'
        args={'file_md5':md5,'file_name':filename,'file_size':path.stat().st_size}
        value=client.call('manage.pre_import',args);segment(value.get('task_id'))
        if not isinstance(value.get('file_key'),str) or not value['file_key'] or len(value['file_key'])>4096:raise ValueError('Tencent pre-import returned no valid opaque upload key.')
        checkpoint(upload_task_id=value['task_id'],status='prepared')
        uploader(path,value['upload_url'])
        checkpoint(status='creating')
        result=client.call('manage.async_import',dict(args,file_key=value['file_key'],task_id=value['task_id']))
        segment(result.get('task_id'));checkpoint(task_id=result['task_id'],status='pending')
    if not receipt.get('remote_id'):
        result=client.call('manage.import_progress',{'task_id':receipt['task_id']})
        if result.get('progress')!=100:return {'status':'pending'}
        segment(result.get('file_id'));verify_url('tencent',result['file_url'])
        checkpoint(remote_id=result['file_id'],url=result['file_url'],status='pending')
    remote=receipt['remote_id'];folder=target['destination']['folder_id']
    info=client.call('manage.query_file_info',{'file_id':remote})
    if info.get('file_id')!=remote or info.get('type')!='doc':raise ValueError('Tencent import did not produce an editable Word document.')
    if info.get('title')!=data['title']:
        client.call('manage.rename_file_title',{'file_id':remote,'title':data['title']})
        info=client.call('manage.query_file_info',{'file_id':remote})
        if info.get('title')!=data['title']:raise ValueError('Tencent title verification failed.')
    if not receipt.get('placement_verified'):
        if not folder_contains(client,folder,remote):
            client.call('manage.move_file',{'file_id':remote,'target_folder_id':folder})
            if not folder_contains(client,folder,remote):raise ValueError('Tencent destination readback could not confirm placement.')
        checkpoint(placement_verified=True,status='pending')
    if not receipt.get('export_task_id'):
        # An uncertain export creates no new course document; a later export is safe.
        result=client.call('manage.export_file',{'file_id':remote});segment(result.get('task_id'))
        checkpoint(export_task_id=result['task_id'],status='pending')
    try:value=client.call('manage.export_progress',{'task_id':receipt['export_task_id']})
    except MCPError as error:
        refreshes=receipt.get('export_refreshes',0)
        if error.kind!='not_found' or refreshes>=3:raise
        checkpoint(export_task_id=None,export_refreshes=refreshes+1,status='pending')
        return {'status':'pending'}
    if value.get('progress')!=100 or not value.get('file_url'):return {'status':'pending'}
    contents=(client.download(value['file_url']) if hasattr(client,'download') else HTTP().download(value['file_url']))
    check_docx(contents,data)
    return verified(remote,receipt['url'],'Official OAuth/MCP import and export: verified title, destination, text, embedded figure and semantic hyperlinks')
