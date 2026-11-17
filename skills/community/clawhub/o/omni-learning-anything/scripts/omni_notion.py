"""Notion Markdown pages plus uploaded image blocks, with readback on retry."""
import mimetypes
import os
import re
import uuid
from omni_http import HTTP, segment, document_data, check_text, check_links, verified
from omni_delivery import verify_url

BASE = 'https://api.notion.com/v1'


def canonical_id(value):
    try:
        return str(uuid.UUID(value))
    except (ValueError, AttributeError, TypeError):
        return value


def blocks(client, page_id, headers):
    results = []; cursor = None
    for _ in range(100):
        params = {'page_size': 100}
        if cursor: params['start_cursor'] = cursor
        response = client.json('GET', BASE + '/blocks/' + segment(page_id) + '/children', headers=headers, params=params)
        results.extend(response.get('results', []))
        if not response.get('has_more'): return results
        cursor = response.get('next_cursor')
        if not cursor: raise ValueError('Incomplete Notion block pagination.')
    raise ValueError('Notion block pagination limit exceeded.')


def publish(root, manifest, target, receipt, checkpoint, client=None):
    if client is None and target.get('mode') == 'cli':
        from omni_official_cli import NotionCLI
        client = NotionCLI(target)
    client = client or HTTP()
    if hasattr(client, 'check_identity'): client.check_identity()
    headers = {'Notion-Version': '2026-03-11'}
    if target.get('mode') != 'cli':
        headers['Authorization'] = 'Bearer ' + os.environ[target['credential_env']['token']]
    data = document_data(root, manifest); parent = target['destination']['parent_page_id']; segment(parent)
    if not receipt.get('remote_id'):
        client.json('GET', BASE + '/pages/' + segment(parent), headers=headers)
        image = root / manifest['report']['figure']
        if image.stat().st_size > 20 * 1024 * 1024:
            raise ValueError('Notion direct image upload limit is 20 MB.')
        if not receipt.get('upload_id'):
            upload = client.json('POST', BASE + '/file_uploads', headers=headers,
                                 json={'filename': image.name, 'content_type': mimetypes.guess_type(image.name)[0], 'mode': 'single_part'})
            segment(upload.get('id')); checkpoint(upload_id=upload['id'])
        if not receipt.get('upload_complete'):
            with image.open('rb') as f:
                uploaded = client.json('POST', BASE + '/file_uploads/' + segment(receipt['upload_id']) + '/send',
                                       headers=headers, files={'file': (image.name, f, mimetypes.guess_type(image.name)[0])})
            if uploaded.get('status') != 'uploaded':
                raise ValueError('Notion image upload not completed.')
            checkpoint(upload_complete=True)
        markdown = (root / manifest['artifacts']['markdown']).read_text()
        # Local image paths never enter cloud Markdown. Attach the uploaded image via blocks.
        markdown = re.sub(r'^!\[.*?\]\([^\n]+\)\s*$', data['figure']['caption'], markdown, flags=re.M)
        checkpoint(status='creating')
        page = client.json('POST', BASE + '/pages', headers=headers,
                           json={'parent': {'page_id': parent}, 'markdown': markdown})
        segment(page.get('id')); verify_url('notion', page['url'])
        checkpoint(remote_id=page['id'], url=page['url'], status='pending')
    page_id = receipt['remote_id']; existing = blocks(client, page_id, headers)
    images = [b for b in existing if b.get('type') == 'image']
    if not images:
        if not receipt.get('upload_id'):
            raise ValueError('Existing Notion page lacks a recoverable image upload; reconcile the page.')
        checkpoint(status='creating')
        client.json('PATCH', BASE + '/blocks/' + segment(page_id) + '/children', headers=headers,
                    json={'children': [{'object': 'block', 'type': 'image', 'image': {
                        'type': 'file_upload', 'file_upload': {'id': receipt['upload_id']},
                        'caption': [{'type': 'text', 'text': {'content': data['figure']['caption']}}]}}]})
        checkpoint(status='pending')
        images = [b for b in blocks(client, page_id, headers) if b.get('type') == 'image']
    if not images: raise ValueError('Notion image readback failed.')
    page = client.json('GET', BASE + '/pages/' + segment(page_id), headers=headers)
    if canonical_id(page.get('parent', {}).get('page_id')) != canonical_id(parent):
        raise ValueError('Notion page is outside the configured parent.')
    title = ''.join(x.get('plain_text', x.get('text', {}).get('content', '')) for x in page.get('properties', {}).get('title', {}).get('title', []))
    if title != data['title']: raise ValueError('Notion page title readback differs.')
    response = client.json('GET', BASE + '/pages/' + segment(page_id) + '/markdown', headers=headers)
    if response.get('truncated') or response.get('unknown_block_ids'):
        raise ValueError('Notion returned incomplete page content.')
    # Notion escapes literal Markdown punctuation in its canonical readback.
    text = re.sub(r'\\([\\`*_{}\[\]()#+.!<>|~-])', r'\1', response.get('markdown', ''))
    check_text(text, data, include_title=False); check_links(text, data)
    return verified(page_id, receipt['url'])
