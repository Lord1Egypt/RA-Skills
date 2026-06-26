# -*- coding: utf-8 -*-
"""
TravelSmart API Server
Flask 提供：
  1. demo.html 前端页面
  2. 三个场景的 API
  3. /notify 推送飞书消息（供量化系统回调）
"""
import io
import sys
import json
import os
import threading
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, '.')
from src.scenes.highway import HighwayScene
from src.scenes.hotel import HotelScene
from src.scenes.taxi import TaxiScene
from src.clients.amap import AmapClient
from src.config.settings import AMAP_KEY

app = Flask(__name__, static_folder='.')
CORS(app)

amap = AmapClient()

# ---------- 前端页面 ----------
@app.route('/')
def index():
    return send_file('demo.html')

# ---------- 高速出口 ----------
@app.route('/api/travel-smart/highway', methods=['POST'])
def api_highway():
    body = request.json
    try:
        result = HighwayScene(amap).recommend(
            body.get('highway', ''),
            float(body.get('lng', 0)),
            float(body.get('lat', 0)),
            body.get('destination', ''),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------- 住宿推荐 ----------
@app.route('/api/travel-smart/hotel', methods=['POST'])
def api_hotel():
    body = request.json
    try:
        result = HotelScene(amap).recommend(
            float(body.get('lng', 0)),
            float(body.get('lat', 0)),
            budget=int(body.get('budget', 300)),
            people=int(body.get('people', 2)),
            next_day_lng=body.get('nextLng'),
            next_day_lat=body.get('nextLat'),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------- 地理编码（地址→经纬度） ----------
@app.route('/api/travel-smart/geocode', methods=['POST'])
def api_geocode():
    body = request.json
    address = body.get('address', '').strip()
    if not address:
        return jsonify({'error': '地址不能为空'}), 400
    try:
        result = amap.geocode(address)
        if result:
            return jsonify({
                'lng': result['lng'],
                'lat': result['lat'],
                'formatted': f"{result.get('province','')}{result.get('city','')}{result.get('district','')}",
            })
        return jsonify({'error': '未找到该地址'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------- 打车点 ----------
@app.route('/api/travel-smart/taxi', methods=['POST'])
def api_taxi():
    body = request.json
    try:
        result = TaxiScene(amap).recommend(
            float(body.get('lng', 0)),
            float(body.get('lat', 0)),
            float(body.get('destLng', 0)),
            float(body.get('destLat', 0)),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------- 飞书通知（供量化系统回调） ----------
# 飞书通知配置（通过环境变量注入，不硬编码）
FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', '')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', '')
FEISHU_CHAT_ID = os.getenv('FEISHU_CHAT_ID', 'oc_b596d3738065b40181b73144a8943999')
FEISHU_TOKEN_TTL = 7100  # token有效期2小时，提前10分钟刷新

_feishu_token = ''
_feishu_token_time = 0

def _get_feishu_token() -> str:
    global _feishu_token, _feishu_token_time
    import time
    if _feishu_token and (time.time() - _feishu_token_time) < FEISHU_TOKEN_TTL:
        return _feishu_token
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    payload = json.dumps({'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}).encode()
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            _feishu_token = data.get('tenant_access_token', '')
            _feishu_token_time = time.time()
            return _feishu_token
    except Exception as e:
        print(f'[Feishu] token获取失败: {e}')
        return ''

def _send_feishu_message(token: str, text: str) -> bool:
    """发送飞书富文本消息到群"""
    if not token:
        return False
    url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id'
    payload = {
        'receive_id': FEISHU_CHAT_ID,
        'msg_type': 'text',
        'content': json.dumps({'text': text})
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f'[Feishu] 发送失败: {e}')
        return False

# 全局 token 缓存（线程安全）
_token_cache = {'token': '', 'time': 0}
_token_lock = threading.Lock()

@app.route('/notify', methods=['POST'])
def api_notify():
    """
    供量化系统回调，同步推送飞书消息
    Body: { "text": "消息内容" }
    """
    body = request.json or {}
    text = body.get('text', '')
    if not text:
        return jsonify({'error': 'text is required'}), 400

    # 同步获取 token 并发送
    token = _get_feishu_token()
    ok = _send_feishu_message(token, text)
    print(f'[Notify] 飞书推送: {"成功" if ok else "失败"} - {text[:40]}...')
    return jsonify({'status': 'sent' if ok else 'failed'})

if __name__ == '__main__':
    if not AMAP_KEY:
        print('❌ AMAP_KEY 未配置，请先设置环境变量或 config/api_keys.yaml')
        sys.exit(1)
    print('✅ TravelSmart API 服务启动: http://localhost:5188')
    print('   /notify 端点已就绪（供量化系统回调推送飞书）')
    app.run(host='0.0.0.0', port=5188, debug=False, threaded=True)
