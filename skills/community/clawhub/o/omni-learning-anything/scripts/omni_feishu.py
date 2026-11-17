"""Import an embedded-image DOCX into Feishu and resume saved import tickets."""
import json
import os
from urllib.parse import unquote
from omni_http import HTTP, business, segment, document_data, check_text, check_links, verified
from omni_delivery import verify_url

BASE = 'https://open.feishu.cn/open-apis'


def document_links(value):
    if isinstance(value, dict):
        link = value.get('link')
        if isinstance(link, dict) and isinstance(link.get('url'), str):
            yield unquote(link['url'])
        for child in value.values(): yield from document_links(child)
    elif isinstance(value, list):
        for child in value: yield from document_links(child)


def publish(root, manifest, target, receipt, checkpoint, client=None):
    if client is None and target.get('mode') == 'cli':
        from omni_official_cli import FeishuCLI
        client = FeishuCLI(target, root)
    client = client or HTTP(); refs = target.get('credential_env', {})
    if hasattr(client, 'check_identity'): client.check_identity()
    if target.get('mode') == 'cli':
        token = None
    elif refs.get('token'):
        token = os.environ[refs['token']]
    else:
        response = client.json('POST', BASE + '/auth/v3/tenant_access_token/internal',
                               json={'app_id': os.environ[refs['app_id']], 'app_secret': os.environ[refs['app_secret']]})
        business(response, 'code'); token = response['tenant_access_token']
    headers = {'Authorization': 'Bearer ' + token} if token else {}; data = document_data(root, manifest)
    path = root / manifest['artifacts']['docx']
    if path.stat().st_size > 20 * 1024 * 1024:
        raise ValueError('Feishu media upload is limited to 20 MB; reduce the image.')
    if not receipt.get('task_id') and not receipt.get('remote_id'):
        if not receipt.get('upload_token'):
            with path.open('rb') as f:
                response = client.json('POST', BASE + '/drive/v1/medias/upload_all', headers=headers,
                    data={'file_name': path.name, 'parent_type': 'ccm_import_open', 'parent_node': '', 'size': str(path.stat().st_size),
                          'extra': json.dumps({'obj_type': 'docx', 'file_extension': 'docx'})},
                    files={'file': (path.name, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
            upload_token=business(response, 'code').get('file_token'); segment(upload_token)
            checkpoint(upload_token=upload_token)
        checkpoint(status='creating')
        response = client.json('POST', BASE + '/drive/v1/import_tasks', headers=headers,
            json={'file_extension': 'docx', 'file_token': receipt['upload_token'], 'type': 'docx',
                  'file_name': data['title'], 'point': {'mount_type': 1, 'mount_key': target['destination']['folder_token']}})
        ticket=business(response, 'code').get('ticket'); segment(ticket)
        checkpoint(task_id=ticket, status='pending')
    if not receipt.get('remote_id'):
        response = client.json('GET', BASE + '/drive/v1/import_tasks/' + segment(receipt['task_id']), headers=headers)
        result = business(response, 'code')['result']
        if result.get('job_status') in (1, 2) or (result.get('job_status') == 0 and not result.get('token')):
            return {'status': 'pending'}
        if result.get('job_status') != 0:
            return {'status': 'failed', 'error': 'Feishu import failed; inspect the saved task before retrying.'}
        if not result.get('token') or not result.get('url'):
            raise ValueError('Feishu import result lacks a document identifier.')
        verify_url('feishu', result['url'])
        checkpoint(remote_id=result['token'], url=result['url'], status='pending')
    doc_id = segment(receipt['remote_id'])
    response = client.json('GET', BASE + '/docx/v1/documents/' + doc_id + '/raw_content', headers=headers)
    text = business(response, 'code').get('content', ''); check_text(text, data)
    items = []; page_token = None
    for _ in range(100):
        params = {'page_size': 500}
        if page_token: params['page_token'] = page_token
        response = client.json('GET', BASE + '/docx/v1/documents/' + doc_id + '/blocks', headers=headers, params=params)
        result = business(response, 'code'); items.extend(result.get('items', []))
        if not result.get('has_more'): break
        page_token = result.get('page_token')
        if not page_token: raise ValueError('Incomplete Feishu block pagination.')
    else:
        raise ValueError('Feishu block pagination limit exceeded.')
    if not any(item.get('block_type') == 27 and item.get('image', {}).get('token') for item in items):
        raise ValueError('Imported Feishu document has no image block.')
    # Feishu stores percent-encoded hrefs; verify actual link targets exactly.
    check_links(list(document_links(items)), data)
    if target.get('mode') == 'cli':
        page_token = None
        for _ in range(100):
            params = {'folder_token': target['destination']['folder_token'], 'page_size': 200}
            if page_token: params['page_token'] = page_token
            listing = business(client.json('GET', BASE + '/drive/v1/files', headers=headers, params=params), 'code')
            found = next((f for f in listing.get('files', []) if f.get('token') == receipt['remote_id']), None)
            if found:
                if found.get('name') != data['title']: raise ValueError('Feishu title does not match the reviewed document.')
                break
            if not listing.get('has_more'): raise ValueError('Feishu document was not found in the confirmed folder.')
            page_token = listing.get('next_page_token')
            if not page_token: raise ValueError('Feishu folder readback is incomplete.')
        else: raise ValueError('Feishu folder pagination limit exceeded.')
    return verified(receipt['remote_id'], receipt['url'])
