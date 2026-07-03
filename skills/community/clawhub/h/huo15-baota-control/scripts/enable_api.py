#!/usr/bin/env python3
# 用宝塔自身的 panelApi 正式开启 API + 设白名单 + 取出明文 token。
# 必须用宝塔 pyenv python 运行，cwd=/www/server/panel。
import os, sys, json
os.chdir('/www/server/panel')
sys.path.insert(0, '/www/server/panel')
sys.path.insert(0, '/www/server/panel/class')
import public
from panelApi import panelApi

class G(dict):
    __getattr__ = dict.get

api = panelApi()
whitelist = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'

data = api.get_api_config()
if not data.get('open'):
    api.set_token(G(t_type='2'))          # 开启 API（生成 token/token_crypt）
api.set_token(G(t_type='3', limit_addr=whitelist))   # 设 IP 白名单

data = api.get_api_config()
out = {'open': data.get('open'),
       'limit_addr': data.get('limit_addr'),
       'key': data.get('key')}
if 'token_crypt' in data:
    out['token_plain'] = public.de_crypt(data['token'], data['token_crypt'])
else:
    out['token_plain'] = data.get('token')
print(json.dumps(out, ensure_ascii=False))
