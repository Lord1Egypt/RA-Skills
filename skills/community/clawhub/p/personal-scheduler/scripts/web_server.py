#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web 服务器 - 提供日程管理界面
"""

from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
from scheduler import PersonalScheduler

app = Flask(__name__)
scheduler = PersonalScheduler()

web_dir = Path(__file__).parent.parent / "web"

@app.route('/')
def index():
    return send_from_directory(web_dir, 'index.html')

@app.route('/api/events')
def get_events():
    """获取日程列表"""
    date = request.args.get('date')
    events = scheduler.list_events(date)
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def create_event():
    """创建日程"""
    data = request.json
    event_id = scheduler.add_event(
        title=data.get('title'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        location=data.get('location'),
        description=data.get('description')
    )
    return jsonify({'success': True, 'id': event_id})

if __name__ == '__main__':
    print("="*50)
    print("日程管理 Web 服务")
    print("="*50)
    print("访问地址: http://localhost:8080")
    print("="*50)
    app.run(host='0.0.0.0', port=8080, debug=True)
