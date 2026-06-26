#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓看盘系统 - 统一网页版
整合所有功能，提供完整的股票投资管理解决方案
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import requests
import json
import os
import socket
import threading
import time
from datetime import datetime
import webbrowser
import markdown
from flask_sock import Sock
import logging

# 导入分离的管理器
from holding_manager import HoldingManager
from llm_manager import LLMManager

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'llm_manager.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('Manager')

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 初始化WebSocket支持
sock = Sock(app)

# 初始化管理器
holding_manager = HoldingManager('portfolio.db')
llm_manager = LLMManager('portfolio.db', holding_manager)

# 组合管理器，保持原有接口兼容
class CombinedManager:
    def __init__(self, holding_manager, llm_manager):
        self.holding_manager = holding_manager
        self.llm_manager = llm_manager
        self.init_database()
        self.auto_update_thread = None
        self.auto_update_running = False
    
    # 持仓管理方法委托
    def init_database(self):
        # 同时初始化两个管理器的数据库
        self.holding_manager.init_database()
        self.llm_manager.init_llm_database()
    
    def get_stock_price(self, *args, **kwargs):
        return self.holding_manager.get_stock_price(*args, **kwargs)
    
    def get_stock_detail(self, *args, **kwargs):
        return self.holding_manager.get_stock_detail(*args, **kwargs)
    
    def update_all_prices(self, *args, **kwargs):
        return self.holding_manager.update_all_prices(*args, **kwargs)
    
    def get_portfolio_data(self, *args, **kwargs):
        return self.holding_manager.get_portfolio_data(*args, **kwargs)
    
    def add_holding(self, *args, **kwargs):
        return self.holding_manager.add_holding(*args, **kwargs)
    
    def delete_holding(self, *args, **kwargs):
        return self.holding_manager.delete_holding(*args, **kwargs)
    
    def edit_holding(self, *args, **kwargs):
        return self.holding_manager.edit_holding(*args, **kwargs)
    
    def edit_holding_multiple(self, *args, **kwargs):
        return self.holding_manager.edit_holding_multiple(*args, **kwargs)
    
    def get_operation_logs(self, *args, **kwargs):
        return self.holding_manager.get_operation_logs(*args, **kwargs)
    
    def generate_report(self, *args, **kwargs):
        return self.holding_manager.generate_report(*args, **kwargs)
    
    def start_auto_update(self, *args, **kwargs):
        return self.holding_manager.start_auto_update(*args, **kwargs)
    
    def stop_auto_update(self, *args, **kwargs):
        return self.holding_manager.stop_auto_update(*args, **kwargs)
    
    # 大模型管理方法委托
    def get_llm_config(self, *args, **kwargs):
        return self.llm_manager.get_llm_config(*args, **kwargs)
    
    def update_llm_config(self, *args, **kwargs):
        return self.llm_manager.update_llm_config(*args, **kwargs)
    
    def call_llm(self, *args, **kwargs):
        return self.llm_manager.call_llm(*args, **kwargs)
    
    def analyze_stock(self, *args, **kwargs):
        return self.llm_manager.analyze_stock(*args, **kwargs)

# 使用组合管理器保持原有接口兼容
manager = CombinedManager(holding_manager, llm_manager)

def get_local_ip():
    """获取本地IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/api/portfolio')
def get_portfolio():
    """获取持仓数据"""
    try:
        portfolio_data = manager.get_portfolio_data()
        
        if portfolio_data:
            return jsonify({
                'status': 'success',
                **portfolio_data
            })
        else:
            return jsonify({
                'status': 'error',
                'error': '获取数据失败'
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/portfolio/update', methods=['POST'])
def update_prices():
    """更新持仓价格"""
    result = manager.update_all_prices()
    return jsonify(result)

@app.route('/api/portfolio/add', methods=['POST'])
def add_holding():
    """新增持仓记录"""
    try:
        data = request.get_json()
        
        required_fields = ['symbol', 'quantity', 'cost_price']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'error': f'缺少字段: {field}'
                }), 400
        
        result = manager.add_holding(
            data['symbol'],
            data.get('name', ''),
            data['quantity'],
            data['cost_price']
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/portfolio/delete/<symbol>', methods=['DELETE'])
def delete_holding(symbol):
    """删除持仓记录"""
    result = manager.delete_holding(symbol)
    return jsonify(result)

@app.route('/api/portfolio/edit/<symbol>', methods=['PUT'])
def edit_holding(symbol):
    """编辑持仓记录"""
    try:
        data = request.get_json()
        field = data.get('field', 'quantity')
        value = data.get('value', 0)
        
        result = manager.edit_holding(symbol, field, value)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/portfolio/edit-multiple/<symbol>', methods=['PUT'])
def edit_holding_multiple(symbol):
    """批量编辑持仓记录"""
    try:
        data = request.get_json()
        
        result = manager.edit_holding_multiple(symbol, data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/portfolio/logs')
def get_logs():
    """获取操作记录"""
    result = manager.get_operation_logs()
    return jsonify(result)

@app.route('/api/portfolio/report')
def generate_report():
    """生成持仓报告"""
    result = manager.generate_report()
    return jsonify(result)

@app.route('/api/portfolio/export')
def export_report():
    """导出持仓报告"""
    result = manager.generate_report()
    
    if result['status'] == 'success':
        report_path = result['report_path']
        return send_file(report_path, as_attachment=True)
    else:
        return jsonify(result)

@app.route('/api/stock/price/<symbol>')
def get_stock_price_api(symbol):
    """查询股票价格"""
    try:
        result = manager.get_stock_price(symbol)
        if result:
            return jsonify({
                'status': 'success',
                'symbol': result['symbol'] if 'symbol' in result else symbol,
                'name': result['name'],
                'price': result['price']
            })
        else:
            return jsonify({
                'status': 'error',
                'error': '未找到股票信息'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/stock/detail/<symbol>')
def get_stock_detail_api(symbol):
    """查询股票详细信息"""
    try:
        result = manager.get_stock_detail(symbol)
        if result:
            return jsonify({
                'status': 'success',
                'data': result
            })
        else:
            return jsonify({
                'status': 'error',
                'error': '未找到股票信息'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

# ------------------- 大模型相关API -------------------
@app.route('/api/llm/config', methods=['GET'])
def get_llm_config_api():
    """获取大模型配置"""
    result = manager.get_llm_config()
    return jsonify(result)

@app.route('/api/llm/config', methods=['POST'])
def update_llm_config_api():
    """更新大模型配置"""
    try:
        data = request.get_json()
        config_id = data.get('id', 1)
        model_type = data.get('model_type', 'openai')
        model_name = data.get('model_name', 'gpt-3.5-turbo')
        api_url = data.get('api_url', 'https://api.openai.com/v1/chat/completions')
        api_key = data.get('api_key', '')
        api_id = data.get('api_id', '')
        enabled = data.get('enabled', True)
        
        result = manager.update_llm_config(config_id, model_type, model_name, api_url, api_key, api_id, enabled)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/stock/analyze/<symbol>')
def analyze_stock_api(symbol):
    """分析股票"""
    try:
        result = manager.analyze_stock(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@sock.route('/api/stock/analyze_websocket/<symbol>')
def analyze_stock_websocket(sock, symbol):
    """WebSocket流式分析股票"""
    try:
        # 获取股票详细信息
        stock_detail = manager.get_stock_detail(symbol)
        if not stock_detail:
            sock.send(json.dumps({'status': 'error', 'error': f'获取股票{symbol}信息失败'}))
            sock.close()
            return
        
        # 获取持仓信息
        holding_info = manager.holding_manager.get_single_holding(symbol)
        holding_text = ""
        if holding_info:
            holding_text = f"""\n我的持仓情况：
持仓数量：{holding_info['quantity']}股
成本价：{holding_info['cost_price']}元
当前盈亏：{holding_info['pnl']}元 ({holding_info['pnl_percent']}%)"""
        else:
            holding_text = "\n（注：我目前没有持有该股）"
        
        # 构建prompt
        prompt = f"""请分析以下股票：

股票名称：{stock_detail['name']}
股票代码：{symbol}
当前价格：{stock_detail['current']}元
今日开盘：{stock_detail['open']}元
今日最高：{stock_detail['high']}元
今日最低：{stock_detail['low']}元
昨日收盘：{stock_detail['pre_close']}元
涨跌额：{stock_detail['change']}元
涨跌幅：{stock_detail['change_percent']}%
{holding_text}

近200个5分钟数据：
{json.dumps(stock_detail.get('min_data', {}), ensure_ascii=False)}

请基于以上数据，分析股票的走势情况，并结合我的持仓情况给出后续操作建议（持仓、买入、卖出、观望等）。"""
        
        # 调用大模型的流式接口
        response = manager.call_llm(prompt, stream=True)
        
        # 检查是否是错误响应
        if isinstance(response, dict) and response.get('status') == 'error':
            sock.send(json.dumps(response))
            sock.close()
            return
        
        # 累积原始内容以便完整转换Markdown
        accumulated_content = ""
        
        # 流式处理响应
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                try:
                    # 解析大模型返回的SSE格式数据
                    chunk_str = chunk.decode('utf-8')
                    logger.info(f'接收到流式响应块: {chunk_str}')
                    lines = chunk_str.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        if line.startswith('data: '):
                            data_str = line[6:]
                            logger.info(f'解析到数据行: {data_str}')
                            if data_str == '[DONE]':
                                logger.info('接收到流结束信号')
                                break
                            
                            try:
                                # 检查数据是否为空
                                if not data_str.strip():
                                    logger.warning('接收到空数据')
                                    continue
                                    
                                data = json.loads(data_str)
                                logger.info(f'解析JSON数据: {json.dumps(data, ensure_ascii=False)}')
                                # 获取内容片段
                                if data.get('choices') and len(data['choices']) > 0:
                                    if data['choices'][0].get('delta'):
                                        content = data['choices'][0]['delta'].get('content', '')
                                    elif data['choices'][0].get('message'):
                                        # 处理非流式格式的响应
                                        content = data['choices'][0]['message'].get('content', '')
                                    else:
                                        content = ''
                                        logger.warning(f'未知的响应格式: {json.dumps(data, ensure_ascii=False)}')
                                    
                                    if content:
                                        # 累积内容
                                        accumulated_content += content
                                        # 使用完整累积内容重新转换为HTML，确保Markdown格式正确
                                        html_content = markdown.markdown(accumulated_content)
                                        # 通过WebSocket发送消息
                                        sock.send(json.dumps({
                                            'status': 'success',
                                            'content': html_content,
                                            'original': accumulated_content,
                                            'chunk': content
                                        }))
                            except json.JSONDecodeError as e:
                                logger.error(f'JSON解析失败: {str(e)}, 数据: {data_str}')
                                # 发送详细的错误信息给前端
                                sock.send(json.dumps({
                                    'status': 'error', 
                                    'error': f'JSON解析失败: {str(e)}, 数据: {data_str}'
                                }))
                                continue
                except Exception as e:
                    logger.error(f'流式响应处理异常: {str(e)}')
                    sock.send(json.dumps({'status': 'error', 'error': f'解析数据失败: {str(e)}'}))
                    sock.close()
                    return
        
        # 发送完成信号
        sock.send(json.dumps({'status': 'done'}))
        # 不再等待，由前端控制连接关闭
        
    except Exception as e:
        # 确保在异常时关闭连接
        try:
            sock.send(json.dumps({'status': 'error', 'error': str(e)}))
        except:
            pass
        sock.close()

def start_server(host='0.0.0.0', port=5000, debug=False, auto_update=True):
    """启动Web服务器"""
    print("="*60)
    print("🚀 持仓看盘系统 - 统一网页版")
    print("="*60)
    
    local_ip = get_local_ip()
    
    print(f"📡 访问地址:")
    print(f"   本地: http://localhost:{port}")
    print(f"   局域网: http://{local_ip}:{port}")
    print(f"   移动端: http://{local_ip}:{port}")
    print()
    print("🎯 功能特性:")
    print("   📊 持仓管理 - 增删改查")
    print("   🔄 实时价格 - 自动更新")
    print("   📈 数据分析 - 盈亏统计")
    print("   📋 操作记录 - 完整追溯")
    print("   📄 报告导出 - Markdown格式")
    print()
    print("🔧 按 Ctrl+C 停止服务")
    print("="*60)
    
    # 启动自动更新
    if auto_update:
        manager.start_auto_update(interval_seconds=300)
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        manager.stop_auto_update()
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")

def main():
    """主函数"""
    print("🔍 系统初始化...")
    
    # 检查数据库
    if not os.path.exists('portfolio.db'):
        print("⚠️  数据库不存在，正在创建...")
        manager.init_database()
    
    print("✅ 系统就绪")
    print()
    
    # 启动服务器
    start_server(host='0.0.0.0', port=5000, debug=False, auto_update=True)

if __name__ == '__main__':
    main()
