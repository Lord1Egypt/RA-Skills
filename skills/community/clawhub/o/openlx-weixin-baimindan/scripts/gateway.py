#!/usr/bin/env python3
"""Pass prepared JSON to the existing gateway without rewriting content."""
import json, os, sys, http.client, urllib.request, urllib.error

def request(h):
 target=h.get('target_account'); action=h.get('requested_action'); payload=h.get('prepared_payload_or_reference')
 if not target: raise ValueError('TARGET_ACCOUNT_MISSING')
 if not h.get('user_intent'): raise ValueError('USER_INTENT_MISSING')
 if not isinstance(payload,dict): raise ValueError('PREPARED_PAYLOAD_MISSING: supply resolved JSON object')
 if payload.get('appid')!=target: raise ValueError('TARGET_ACCOUNT_MISMATCH')
 media_type=payload.get('type','article')
 if action in ('CREATE_DRAFT','SUBMIT_EXPLICIT_PUBLISH') and media_type in ('voice','video'):
  raise ValueError('MEDIA_UPLOAD_ONLY: use UPLOAD_MEDIA; material upload is not public publication')
 if action=='CREATE_DRAFT':
  if payload.get('is_draft') is not True: raise ValueError('DRAFT_FLAG_REQUIRED')
  endpoint='publish'
 elif action=='SUBMIT_EXPLICIT_PUBLISH':
  if h.get('explicit_publication_confirmation') is not True or payload.get('is_draft') is not False: raise ValueError('EXPLICIT_PUBLICATION_CONFIRMATION_REQUIRED')
  endpoint='publish'
 elif action=='UPLOAD_MEDIA':
  if media_type not in ('video','voice') or not payload.get('media_url'): raise ValueError('MEDIA_PAYLOAD_REQUIRED')
  if media_type=='video' and not payload.get('title'): raise ValueError('VIDEO_TITLE_REQUIRED')
  endpoint='publish'
 elif action=='QUERY_STATUS':
  endpoint='draft-get' if payload.get('media_id') else 'publish-status' if payload.get('publish_id') else None
  if not endpoint: raise ValueError('QUERY_ID_MISSING')
 elif action=='CHECK_AUTHORIZATION': endpoint='draft-count'
 else: raise ValueError('ACTION_UNSUPPORTED')
 allowed={'appid','type','title','content','images','image_urls','cover_url','cover_base64','media_url','source_url','is_draft','author','digest','cover_media_id','thumb_media_id','media_id','publish_id','content_source_url','need_open_comment','only_fans_can_comment','show_cover_pic'}
 if set(payload)-allowed: raise ValueError('UNSUPPORTED_PAYLOAD_FIELDS: remove unrelated fields')
 if action=='CREATE_DRAFT' and media_type not in ('article','newspic','reproduce'): raise ValueError('DRAFT_TYPE_UNSUPPORTED')
 if action=='SUBMIT_EXPLICIT_PUBLISH' and media_type not in ('article','newspic','reproduce','existing'): raise ValueError('PUBLISH_TYPE_UNSUPPORTED')
 key=os.environ.get('OPENLX_WEIXIN_API_KEY')
 if not key: raise ValueError('OPENLX_ACCESS_CREDENTIAL_MISSING')
 headers={'Content-Type':'application/json','x-api-key':key}
 # Gateway does not guarantee idempotency-key deduplication. Never blind retry a write.
 req=urllib.request.Request('https://wx.openlx.cn/v2/proxy/'+endpoint,data=json.dumps(payload,ensure_ascii=False).encode(),headers=headers)
 try:
  with urllib.request.urlopen(req,timeout=180) as r: return json.load(r)
 except urllib.error.HTTPError as e:
  return {'status':'SUBMITTED_UNVERIFIED' if endpoint=='publish' and (e.code==408 or e.code>=500) else 'GATEWAY_REJECTED','http_status':e.code,'retry_write':False}
 except (TimeoutError,urllib.error.URLError,http.client.HTTPException,ValueError,ConnectionError,OSError): return {'status':'SUBMITTED_UNVERIFIED' if endpoint=='publish' else 'QUERY_UNAVAILABLE','retry_write':False}
if __name__=='__main__':
 try: print(json.dumps(request(json.load(open(sys.argv[1]))),ensure_ascii=False))
 except Exception as e: print(str(e),file=sys.stderr); sys.exit(1)
