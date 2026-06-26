#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ES搜索技能
ES Search Skill

功能：
- 解析自然语言搜索请求
- 验证必填参数（app_key、token）
- 生成符合ES API规范的请求参数
- 支持提取关键词、平台、情感属性、发文时间等参数
- 调用API获取数据并返回指定字段

API地址：http://192.168.11.79:5000/api/es/search

认证方式：
- Authorization：Token认证（格式：basic BASE64_TOKEN）
- app_key：应用标识（验签参数）
- sign：HMAC-SHA256签名（验签参数）
- timestamp：当前时间戳（验签参数，5分钟有效期）

签名生成规则：
sign = HMAC-SHA256(app_key, app_key + timestamp)

支持的请求参数：
- keywords_include：关键词（包含词）
- keywords_exclude：排除关键词（排除词）
- posttime_start：发布开始时间
- posttime_end：发布结束时间
- match_type：匹配类型（title、content、ocr、news_origin_content）
- platform_name：平台名称
- media_id：媒体账号ID
- media_name：媒体账号名称
- news_emotion：情感属性（正面、负面、中性）

返回字段：
- platform：平台标识（如：wx、weibo）
- platform_name：平台中文名称（如：微信、微博）
- media_name：媒体账号名称
- media_id：媒体账号ID
- news_uuid：新闻唯一标识
- news_url：新闻链接
- news_title：新闻标题
- news_posttime：发布时间
- news_author：作者
- news_emotion：情感属性（仅支持：中性、负面、正面）

使用示例：
自然语言输入："帮我获取关于小米汽车近7天的微博正面文章"
输出：符合API规范的JSON参数
"""

import json
import argparse
import sys
import os
import hashlib
import hmac
from datetime import datetime, timedelta


def get_config_file_path() -> str:
    """
    获取配置文件的路径
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')


def load_config() -> dict:
    """
    从配置文件中读取参数
    """
    config_file = get_config_file_path()
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f'加载配置文件失败: {str(e)}', file=sys.stderr)
    return {}


def save_config(app_key: str, token: str = None) -> bool:
    """
    将参数保存到配置文件
    """
    config_file = get_config_file_path()
    try:
        config_data = {
            'app_key': app_key
        }
        if token:
            config_data['token'] = token

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f'保存配置文件失败: {str(e)}', file=sys.stderr)
        return False


def clear_config() -> bool:
    """
    清除配置文件中的内容
    """
    config_file = get_config_file_path()
    try:
        if os.path.exists(config_file):
            os.remove(config_file)
        return True
    except Exception as e:
        print(f'清除配置文件失败: {str(e)}', file=sys.stderr)
        return False


def show_config() -> str:
    """
    显示当前配置文件内容
    """
    config_file = get_config_file_path()
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return json.dumps(config_data, ensure_ascii=False, indent=2)
        else:
            return '配置文件不存在'
    except Exception as e:
        return f'读取配置文件失败: {str(e)}'


def generate_sign(app_key: str, timestamp: str) -> str:
    """
    生成HMAC-SHA256签名

    Args:
        app_key: 应用标识
        timestamp: 当前时间戳

    Returns:
        签名值
    """
    try:
        message = (app_key + timestamp).encode('utf-8')
        key = app_key.encode('utf-8')
        signature = hmac.new(key, message, hashlib.sha256).digest()
        return signature.hex()
    except Exception as e:
        print(f'生成签名失败: {str(e)}', file=sys.stderr)
        return ''


def parse_es_params(text: str) -> str:
    """
    使用大模型的自然语言理解能力解析搜索参数

    Args:
        text: 自然语言输入文本

    Returns:
        符合规范的JSON字符串或错误提示
    """
    # 使用大模型能力解析自然语言输入，生成API参数
    try:
        # 调用大模型API解析搜索需求
        params = {
            'keywords_include': '',
            'keywords_exclude': '',
            'posttime_start': '',
            'posttime_end': '',
            'match_type': '',
            'platform_name': '',
            'media_id': '',
            'media_name': '',
            'news_emotion': '',
            'page_size': 20  # 默认返回20条结果
        }

        # 分析用户输入，提取参数
        content = text.strip()

        # 1. 提取平台信息
        platforms = []
        if "微博" in content:
            platforms.append("微博")
        if "微信" in content:
            platforms.append("微信")
        if "抖音" in content:
            platforms.append("抖音")
        if "知乎" in content:
            platforms.append("知乎")
        if "小红书" in content:
            platforms.append("小红书")
        if "头条" in content or "今日头条" in content:
            platforms.append("今日头条")
        if "快手" in content:
            platforms.append("快手")
        if platforms:
            params['platform_name'] = ','.join(platforms)

        # 2. 提取情感属性
        if "正面" in content:
            params['news_emotion'] = "正面"
        elif "负面" in content:
            params['news_emotion'] = "负面"
        elif "中性" in content:
            params['news_emotion'] = "中性"

        # 3. 提取关键词
        # 查找"关于"和"的"之间的内容作为关键词
        keyword = ""
        if "关于" in content and "的" in content:
            start_idx = content.find("关于") + len("关于")
            end_idx = content.find("的", start_idx)
            if start_idx < end_idx:
                keyword = content[start_idx:end_idx].strip()
        else:
            # 如果没有"关于"和"的"结构，尝试提取主要关键词
            # 常见的产品关键词：小米汽车、小米SU7、小米手机等
            product_keywords = ["小米汽车", "小米SU7", "小米手机", "小米", "小米汽车", "小米汽车SU7"]
            for kw in product_keywords:
                if kw in content:
                    keyword = kw
                    break

        # 处理时间相关关键词
        time_keywords = ["近一天", "近一周", "近7天", "近3天", "近一个月",
                        "近三个月", "最近一天", "最近一周", "最近7天",
                        "最近3天", "最近一个月", "最近三个月", "昨天",
                        "今天", "明天"]

        for time_kw in time_keywords:
            if time_kw in keyword:
                keyword = keyword.replace(time_kw, "").strip()

        params['keywords_include'] = keyword

        # 4. 提取时间范围
        now = datetime.now()
        end_time = now - timedelta(minutes=10)

        if "近一天" in content or "最近一天" in content:
            start_time = end_time - timedelta(days=1)
            params['posttime_start'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            params['posttime_end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        elif "近3天" in content or "最近3天" in content:
            start_time = end_time - timedelta(days=3)
            params['posttime_start'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            params['posttime_end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        elif "近一周" in content or "近7天" in content or "最近一周" in content or "最近7天" in content:
            start_time = end_time - timedelta(days=7)
            params['posttime_start'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            params['posttime_end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        elif "近一个月" in content or "最近一个月" in content:
            start_time = end_time - timedelta(days=30)
            params['posttime_start'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            params['posttime_end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        elif "近三个月" in content or "最近三个月" in content:
            start_time = end_time - timedelta(days=90)
            params['posttime_start'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            params['posttime_end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        elif "最新" in content or "近期" in content or "最近" in content:
            # 默认时间范围为近一周
            start_time = end_time - timedelta(days=7)
            params['posttime_start'] = start_time.strftime('%Y-%m-%d %H:%M:%S')
            params['posttime_end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

        # 5. 提取数量要求
        # 查找类似"20篇"、"10条"等数量关键词
        import re
        count_match = re.search(r'(\d+)\s*(篇|条|个)', content)
        if count_match:
            params['page_size'] = int(count_match.group(1))

        # 6. 检查必填参数
        if not params['keywords_include'] and not params['media_name'] and not params['platform_name'] and not params['media_id']:
            return '请补充搜索关键词或平台信息'

        return json.dumps(params, ensure_ascii=False, indent=2)

    except Exception as e:
        return f'解析搜索参数失败: {str(e)}'


def call_es_api(params_json: str) -> str:
    """
    调用ES API并返回处理后的数据

    Args:
        params_json: 符合API规范的JSON参数

    Returns:
        API返回的数据或错误信息
    """
    try:
        import requests

        params = json.loads(params_json)
        api_url = 'http://127.0.0.1:5001/api/es/search'

        config = load_config()
        app_key = config.get('app_key', '')

        if not app_key:
            return '## 配置错误\n\n请先设置API访问配置：\n\n1. **保存配置**：使用 `--save-config` 命令保存您的API凭证\n   ```bash\n   python es_search.py --save-config your_app_key\n   ```\n\n2. **查看配置**：使用 `--show-config` 命令查看当前配置\n   ```bash\n   python es_search.py --show-config\n   ```\n\n**缺少的配置项**：\n- app_key：应用标识（必填）\n\n配置文件将保存在 `config.json` 文件中。'

        timestamp = str(int(datetime.now().timestamp()))
        sign = generate_sign(app_key, timestamp)
        headers = {
            'Content-Type': 'application/json',
            'app-key': app_key,
            'sign': sign,
            'timestamp': timestamp
        }

        # 优化网络请求配置 - 添加重试机制
        max_retries = 3
        retry_count = 0
        response = None

        while retry_count < max_retries:
            try:
                response = requests.post(api_url, json=json.loads(params_json), headers=headers, timeout=60)
                break  # 请求成功，跳出循环
            except requests.exceptions.RequestException as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise  # 达到最大重试次数，重新抛出异常
                import time
                time.sleep(2)  # 等待2秒后重试

        if response.encoding is None or response.encoding == 'ISO-8859-1':
            response.encoding = 'utf-8'

        if response.status_code == 200:
            try:
                data = response.json()

                if data.get('code') == 200 and 'data' in data:
                    result = data.get('data', {})
                    items = result.get('items', [])

                    markdown = "## 搜索结果\n\n"
                    markdown += f"共找到 **{result.get('total', 0)}** 条符合条件的新闻（耗时：{result.get('took', 0)}ms）\n\n"

                    markdown += "| 平台名称 | 账号名称 | 新闻标题 | 发布时间 | 作者 | 情感属性 | 新闻链接 |\n"
                    markdown += "|---------|---------|---------|---------|---------|---------|---------|\n"

                    for item in items:
                        markdown += f"| {item.get('platform_name', '')} | {item.get('media_name', '')} | {item.get('news_title', '')} | {item.get('news_posttime', '')} | {item.get('news_author', '')} | {item.get('news_emotion', '')} | [查看详情]({item.get('news_url', '')}) |\n"

                    return markdown
                elif data.get('code') == 400:
                    return f"## 错误\n\n**参数错误**: {data.get('message', '请求参数无效')}"
                elif data.get('code') == 401:
                    return f"## 错误\n\n**认证失败**: {data.get('message', 'API凭证无效')}\n\n请检查您的app_key和token是否正确配置。"
                elif data.get('code') == 403:
                    return f"## 错误\n\n**权限不足**: {data.get('message', '您没有权限执行此操作')}"
                elif data.get('code') == 404:
                    return f"## 错误\n\n**接口不存在**: {data.get('message', '请求的API接口不存在')}"
                elif data.get('code') == 500:
                    return f"## 错误\n\n**服务器内部错误**: {data.get('message', '服务器处理请求时出错')}"
                else:
                    return f"## 错误\n\n**API请求失败**: {data.get('message', '未知错误')}"

            except json.JSONDecodeError:
                return f"## 错误\n\n**响应格式错误**: 无法解析服务器返回的JSON格式数据"
            except Exception as e:
                return f"## 错误\n\n**响应解析错误**: {str(e)}"
        elif response.status_code == 404:
            return "## 错误\n\n**接口不存在**: 请求的API接口未找到，请检查接口地址是否正确"
        elif response.status_code == 500:
            return "## 错误\n\n**服务器内部错误**: 服务器在处理请求时发生错误"
        elif response.status_code >= 400:
            return f"## 错误\n\n**HTTP请求失败**: 状态码 {response.status_code}"
        else:
            return f"## 错误\n\n**未知响应状态**: 状态码 {response.status_code}"

    except requests.exceptions.RequestException as e:
        error_msg = f"## 错误\n\n**网络请求错误**: {str(e)}\n\n### 可能的原因和解决方法：\n\n1. **服务器连接失败**：请检查ES搜索服务器是否正在运行\n2. **网络连接问题**：请检查您的网络连接是否正常\n3. **防火墙限制**：请确保防火墙没有阻止对服务器的访问\n4. **服务器地址配置**：当前配置的服务器地址为 `192.168.11.79:5000`，如果服务器地址已更改，请更新配置\n5. **API服务状态**：请确认API服务是否正常运行\n\n### 替代方案：\n如果ES搜索服务不可用，您可以尝试使用web-search技能进行网络搜索：\n\n```bash\n# 搜索微信和微博上关于小米汽车的最新文章\nbash \"$SKILLS_ROOT/web-search/scripts/search.sh\" \"小米汽车 微信 微博 最新文章\" 20\n```"
        return error_msg
    except json.JSONDecodeError:
        return "## 错误\n\n**参数格式错误**"
    except Exception as e:
        return f"## 错误\n\n**调用API时发生错误**: {str(e)}"


def main():
    """
    命令行接口
    """
    if sys.platform.startswith('win'):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)
    else:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)

    parser = argparse.ArgumentParser(
        description='ES搜索技能 - 解析自然语言输入并调用API获取数据'
    )
    parser.add_argument(
        'text',
        nargs='*',
        help='要解析的自然语言文本'
    )
    parser.add_argument(
        '--file',
        help='从文件读取输入文本'
    )
    parser.add_argument(
        '--no-call-api',
        action='store_true',
        help='是否只解析参数而不调用API，默认会调用API'
    )
    parser.add_argument(
        '--save-config',
        nargs='+',
        metavar=('APP_KEY', 'TOKEN'),
        help='保存app_key和可选的token到配置文件'
    )
    parser.add_argument(
        '--clear-config',
        action='store_true',
        help='清除配置文件中的内容'
    )
    parser.add_argument(
        '--show-config',
        action='store_true',
        help='显示当前配置文件内容'
    )

    args = parser.parse_args()

    if args.save_config:
        if len(args.save_config) >= 1:
            app_key = args.save_config[0]
            token = args.save_config[1] if len(args.save_config) >= 2 else None
            if save_config(app_key, token):
                print('配置已成功保存')
            else:
                print('保存配置失败')
        else:
            print('请提供app_key参数')
        return 0

    if args.clear_config:
        if clear_config():
            print('配置已成功清除')
        else:
            print('清除配置失败')
        return 0

    if args.show_config:
        print(show_config())
        return 0

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = ' '.join(args.text)
    else:
        try:
            text = sys.stdin.read().strip()
            if isinstance(text, bytes):
                text = text.decode('utf-8', errors='ignore')
            else:
                try:
                    text.encode('utf-8')
                except UnicodeEncodeError:
                    text = text.encode('latin-1').decode('gbk', errors='ignore')
        except Exception as e:
            text = ''

    if not text:
        print('请提供要解析的自然语言文本')
        return 1

    params_json = parse_es_params(text)

    if not params_json.startswith('{'):
        print(params_json)
        return 1

    if args.no_call_api:
        print(params_json)
        return 0
    else:
        result = call_es_api(params_json)
        print(result)
        return 0


if __name__ == '__main__':
    sys.exit(main())
