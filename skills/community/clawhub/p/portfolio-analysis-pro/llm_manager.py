#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型管理器 - 负责与大模型相关的所有功能
"""

import sqlite3
import requests
import json
import logging
import os
from datetime import datetime
import markdown

# 配置日志
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

logger = logging.getLogger('LLMManager')

class LLMManager:
    """大模型管理器 - 处理所有与大模型相关的功能"""
    
    def __init__(self, db_path='portfolio.db', holding_manager=None):
        self.db_path = db_path
        self.holding_manager = holding_manager
        logger.info(f'初始化LLMManager，数据库路径：{db_path}')
        self.init_llm_database()
    
    def init_llm_database(self):
        """初始化大模型配置表"""
        logger.info(f'初始化大模型数据库，路径：{self.db_path}')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建大模型配置表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS llm_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_type TEXT NOT NULL,  -- openai, baichuan, volcano
            model_name TEXT NOT NULL,
            api_url TEXT NOT NULL,
            api_key TEXT NOT NULL,
            api_id TEXT,
            enabled INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        logger.info('创建大模型配置表完成')
        
        # 插入默认配置（如果不存在）
        cursor.execute('SELECT COUNT(*) FROM llm_config')
        if cursor.fetchone()[0] == 0:
            # 插入OpenAI默认配置
            cursor.execute('''
            INSERT INTO llm_config (model_type, model_name, api_url, api_key, api_id, enabled)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', ('openai', 'gpt-3.5-turbo', 'https://api.openai.com/v1/chat/completions', '', '', 1))
            
            # 插入MiniMax默认配置
            cursor.execute('''
            INSERT INTO llm_config (model_type, model_name, api_url, api_key, api_id, enabled)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', ('minimax', 'M2.7', 'https://api.minimaxi.com/v1/chat/completions', '', '', 0))
            
            logger.info('插入默认大模型配置完成')
        
        conn.commit()
        conn.close()
        logger.info('大模型数据库初始化完成')
    
    def get_llm_config(self):
        """获取大模型配置"""
        logger.info('获取大模型配置')
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, model_type, model_name, api_url, api_key, api_id, enabled
            FROM llm_config
            ORDER BY id
            ''')
            
            configs = []
            for row in cursor.fetchall():
                configs.append({
                    'id': row[0],
                    'model_type': row[1],
                    'model_name': row[2],
                    'api_url': row[3],
                    'api_key': row[4],
                    'api_id': row[5],
                    'enabled': bool(row[6])
                })
            
            conn.close()
            logger.info(f'获取到大模型配置 {len(configs)} 条')
            return {'status': 'success', 'data': configs}
            
        except Exception as e:
            logger.error(f'获取大模型配置失败: {str(e)}')
            return {'status': 'error', 'error': str(e)}
    
    def update_llm_config(self, config_id, model_type, model_name, api_url, api_key, api_id, enabled):
        """更新大模型配置"""
        logger.info(f'更新大模型配置，ID: {config_id}, 模型类型: {model_type}, 模型名称: {model_name}')
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 更新配置
            cursor.execute('''
            UPDATE llm_config 
            SET model_type = ?, model_name = ?, api_url = ?, api_key = ?, api_id = ?, enabled = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (model_type, model_name, api_url, api_key, api_id, 1 if enabled else 0, config_id))
            
            if cursor.rowcount == 0:
                # 如果没有找到记录，插入新记录
                cursor.execute('''
                INSERT INTO llm_config (model_type, model_name, api_url, api_key, api_id, enabled)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (model_type, model_name, api_url, api_key, api_id, 1 if enabled else 0))
                logger.info(f'插入新的大模型配置，模型类型: {model_type}, 模型名称: {model_name}')
            else:
                logger.info(f'更新大模型配置成功，ID: {config_id}')
            
            conn.commit()
            conn.close()
            return {'status': 'success', 'message': '大模型配置更新成功'}
            
        except Exception as e:
            logger.error(f'更新大模型配置失败: {str(e)}')
            return {'status': 'error', 'error': str(e)}
    
    def call_llm(self, prompt, stream=False):
        """调用大模型"""
        logger.info('开始调用大模型')
        try:
            # 获取启用的大模型配置
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT model_type, model_name, api_url, api_key, api_id
            FROM llm_config
            WHERE enabled = 1
            LIMIT 1
            ''')
            
            config = cursor.fetchone()
            conn.close()
            
            if not config:
                logger.error('未找到启用的大模型配置')
                return {'status': 'error', 'error': '未找到启用的大模型配置'}
            
            model_type, model_name, api_url, api_key, api_id = config
            logger.info(f'使用模型配置: 类型={model_type}, 名称={model_name}, API地址={api_url}')
            
            if model_type == 'openai':
                # 调用OpenAI API
                logger.info('调用OpenAI API')
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
                
                data = {
                    'model': model_name,
                    'messages': [
                        {'role': 'system', 'content': '你是一位专业的股票分析师，请基于提供的数据进行分析并给出操作建议。中文回答！'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'stream': stream
                }
                
                response = requests.post(api_url, headers=headers, json=data, timeout=300, stream=stream)
                
                if stream:
                    logger.info('OpenAI API 流式响应')
                    return response
                else:
                    if response.status_code == 200:
                        result = response.json()
                        # 将markdown转换为html
                        markdown_content = result['choices'][0]['message']['content']
                        html_content = markdown.markdown(markdown_content)
                        logger.info('OpenAI API 调用成功')
                        return {
                            'status': 'success',
                            'content': html_content,
                            'original_content': markdown_content
                        }
                    else:
                        logger.error(f'OpenAI API调用失败: {response.status_code}, {response.text}')
                        return {
                            'status': 'error',
                            'error': f'OpenAI API调用失败: {response.text}'
                        }
                    
            elif model_type == 'baichuan':
                # 调用百炼API
                logger.info('调用百炼API')
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
                
                data = {
                    'model': model_name,
                    'messages': [
                        {'role': 'system', 'content': '你是一位专业的股票分析师，请基于提供的数据进行分析并给出操作建议。'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'stream': stream
                }
                
                response = requests.post(api_url, headers=headers, json=data, timeout=30, stream=stream)
                
                if stream:
                    logger.info('百炼API 流式响应')
                    return response
                else:
                    if response.status_code == 200:
                        result = response.json()
                        # 将markdown转换为html
                        markdown_content = result['choices'][0]['message']['content']
                        html_content = markdown.markdown(markdown_content)
                        logger.info('百炼API 调用成功')
                        return {
                            'status': 'success',
                            'content': html_content,
                            'original_content': markdown_content
                        }
                    else:
                        logger.error(f'百炼API调用失败: {response.status_code}, {response.text}')
                        return {
                            'status': 'error',
                            'error': f'百炼API调用失败: {response.text}'
                        }
                    
            elif model_type == 'volcano':
                # 调用火山引擎API
                logger.info('调用火山引擎API')
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}',
                    'X-Volc-Auth-AK': api_id if api_id else ''
                }
                
                data = {
                    'model': model_name,
                    'messages': [
                        {'role': 'system', 'content': '你是一位专业的股票分析师，请基于提供的数据进行分析并给出操作建议。'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'stream': stream
                }
                logger.info(f'火山引擎API调用请求: {api_url}')
                response = requests.post(api_url, headers=headers, json=data, timeout=30, stream=stream)
                logger.info(f'火山引擎API调用响应: {response}')
                
                if stream:
                    logger.info('火山引擎API 流式响应')
                    return response
                else:
                    if response.status_code == 200:
                        result = response.json()
                        # 将markdown转换为html
                        markdown_content = result['choices'][0]['message']['content']
                        html_content = markdown.markdown(markdown_content)
                        logger.info('火山引擎API 调用成功')
                        return {
                            'status': 'success',
                            'content': html_content,
                            'original_content': markdown_content
                        }
                    else:
                        logger.error(f'火山引擎API调用失败: {response.status_code}, {response.text}')
                        return {
                            'status': 'error',
                            'error': f'火山引擎API调用失败: {response.text}'
                        }
                    
            elif model_type == 'minimax':
                # 调用MiniMax API
                logger.info('调用MiniMax API')
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
                
                # 添加tokenplan支持，根据MiniMax API文档，格式与OpenAI类似
                data = {
                    'model': model_name,
                    'messages': [
                        {'role': 'system', 'content': '你是一位专业的股票分析师，请基于提供的数据进行分析并给出操作建议。中文回答！'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'stream': stream
                }
                
                # 如果api_id存在，可能用于tokenplan相关配置
                if api_id:
                    data['tokenplan'] = api_id
                
                logger.info(f'MiniMax API调用请求: {api_url}, stream:{stream}')
                logger.info(f'MiniMax API请求头: {headers}')
                logger.info(f'MiniMax API请求数据: {json.dumps(data, ensure_ascii=False)}')
                
                response = requests.post(api_url, headers=headers, json=data, timeout=300, stream=stream)
                logger.info(f'MiniMax API调用响应状态: {response.status_code}')
                logger.info(f'MiniMax API调用响应头: {dict(response.headers)}')
                
                # 对于流式响应，不尝试解析JSON
                if stream:
                    logger.info('MiniMax API 流式响应')
                    return response
                else:
                    # 非流式响应，尝试解析JSON
                    logger.info(f'MiniMax API调用响应内容: {response.text}')
                    
                    if response.status_code == 200:
                        try:
                            result = response.json()
                            logger.info(f'MiniMax API响应JSON: {json.dumps(result, ensure_ascii=False)}')
                            
                            # 将markdown转换为html
                            if result.get('choices') and len(result['choices']) > 0 and result['choices'][0].get('message'):
                                markdown_content = result['choices'][0]['message']['content']
                                html_content = markdown.markdown(markdown_content)
                                logger.info('MiniMax API 调用成功')
                                return {
                                    'status': 'success',
                                    'content': html_content,
                                    'original_content': markdown_content
                                }
                            else:
                                logger.error(f'MiniMax API响应格式不正确: {json.dumps(result, ensure_ascii=False)}')
                                return {
                                    'status': 'error',
                                    'error': f'MiniMax API响应格式不正确: 缺少必要字段'
                                }
                        except json.JSONDecodeError as e:
                            logger.error(f'MiniMax API响应JSON解析失败: {str(e)}, 响应内容: {response.text}')
                            return {
                                'status': 'error',
                                'error': f'MiniMax API响应JSON解析失败: {str(e)}'
                            }
                    else:
                        logger.error(f'MiniMax API调用失败: {response.status_code}, {response.text}')
                        return {
                            'status': 'error',
                            'error': f'MiniMax API调用失败: {response.status_code}, {response.text}'
                        }
                    
            else:
                logger.error(f'不支持的模型类型: {model_type}')
                return {'status': 'error', 'error': f'不支持的模型类型: {model_type}'}
                
        except Exception as e:
            logger.error(f'大模型调用异常: {str(e)}')
            return {'status': 'error', 'error': str(e)}
    
    def analyze_stock(self, symbol):
        """分析股票"""
        logger.info(f'开始分析股票: {symbol}')
        try:
            # 获取股票详细信息（需要调用持仓管理器的方法）
            if not self.holding_manager:
                logger.error('持仓管理器未初始化')
                return {'status': 'error', 'error': '持仓管理器未初始化'}
                
            stock_detail = self.holding_manager.get_stock_detail(symbol)
            if not stock_detail:
                logger.error(f'获取股票{symbol}信息失败')
                return {'status': 'error', 'error': f'获取股票{symbol}信息失败'}
            
            logger.info(f'获取股票{symbol}({stock_detail["name"]})信息成功')
            
            # 获取持仓信息
            holding_info = self.holding_manager.get_single_holding(symbol)
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
            
            # 调用大模型
            logger.info(f'调用大模型分析股票{symbol}')
            result = self.call_llm(prompt)
            logger.info(f'股票{symbol}分析完成')
            return result
            
        except Exception as e:
            logger.error(f'股票{symbol}分析异常: {str(e)}')
            return {'status': 'error', 'error': str(e)}
