#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import warnings
# 过滤requests依赖版本警告
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="urllib3 (.*) or chardet/(.*) doesn't match a supported version!")
import argparse
import sqlite3
import requests
import json
import os
import datetime
import subprocess
from PIL import Image
from dotenv import load_dotenv

# 加载.env配置
load_dotenv()
API_KEY = os.getenv('API_KEY')

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'set.json')
DB_PATH = os.path.join(BASE_DIR, 'data', 'works.db')

# 加载配置
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)
SAVE_BASE_PATH = CONFIG.get('save_path', os.path.join(os.path.expanduser("~"), "Desktop", "banana"))
os.makedirs(SAVE_BASE_PATH, exist_ok=True)

# 如果.env中没有API_KEY，则使用set.json中的apikey
if not API_KEY and CONFIG['server'].get('apikey'):
    API_KEY = CONFIG['server']['apikey']
    print(f"[警告] 使用set.json中的apikey，建议迁移到.env文件")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def main():
    parser = argparse.ArgumentParser(description='独立任务处理脚本')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-task_id', type=str, help='模型接口返回的task_id')
    group.add_argument('-id', type=int, help='数据库中任务的主键ID')
    parser.add_argument('-num', type=int, default=1, choices=[1,2,4,6,9], help='宫格数，默认读取数据库值')
    args = parser.parse_args()
    
    # 1. 查询数据库任务
    conn = get_db_connection()
    work = None
    if args.id:
        work = conn.execute('SELECT * FROM works WHERE id = ?', (args.id,)).fetchone()
        if not work:
            print(f"错误：数据库中未找到ID={args.id}的任务")
            conn.close()
            return
        task_id = work['task_id']
        work_id = args.id
        print(f"找到已有任务: work_id={work_id}, task_id={task_id}")
    else:
        task_id = args.task_id
        work = conn.execute('SELECT * FROM works WHERE task_id = ?', (task_id,)).fetchone()
        if not work:
            print(f"错误：数据库中未找到task_id={task_id}的任务，请先在前端提交任务")
            conn.close()
            return
        work_id = work['id']
        print(f"找到已有任务: work_id={work_id}, task_id={task_id}")
    
    num = work['num']
    print(f"任务配置: 宫格数={num}")
    
    # 2. 调用接口查询任务
    print("正在查询模型接口...")
    
    # 使用环境变量中的 API_KEY，如果没有则使用配置文件中的
    api_key = API_KEY or CONFIG['server'].get('apikey', '')
    if not api_key:
        error_msg = "未配置API_KEY，请在.env文件或set.json中配置"
        print(f"[错误] {error_msg}")
        conn.execute("UPDATE works SET state = 99, error = ? WHERE id = ?", (error_msg, work_id))
        conn.commit()
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    payload = {"id": task_id,"action": "retrieve"}
    
    try:
        response = requests.post(CONFIG['server']['task_url'], headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        print(f"接口返回成功: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # 只有接口明确返回success=false且有error信息时才判定为失败
        if data.get('response') and not data['response'].get('success') and data['response'].get('error'):
            error_msg = data['response'].get('error', '接口返回失败')
            print(f"任务明确失败: {error_msg}")
            conn.execute("UPDATE works SET state = 99, error = ?, respond = ? WHERE id = ?", (error_msg, json.dumps(data), work_id))
            conn.commit()
            return
        
        # 其他情况（返回空、无response、无data等）都视为临时问题，继续重试
        if not data.get('response') or not data['response'].get('data') or len(data['response']['data']) == 0:
            print(f"接口返回数据不完整，继续重试...")
            raise Exception("临时数据异常，继续重试")
        
        # 3. 下载图片
        image_url = data['response']['data'][0].get('image_url')
        if not image_url:
            error_msg = "图片URL为空"
            print(f"任务失败: {error_msg}")
            conn.execute("UPDATE works SET state = 99, error = ?, respond = ? WHERE id = ?", (error_msg, json.dumps(data), work_id))
            conn.commit()
            return
        
        print(f"开始下载图片: {image_url}")
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        save_dir = os.path.join(SAVE_BASE_PATH, now)
        os.makedirs(save_dir, exist_ok=True)
        
        ext = image_url.split('.')[-1].split('?')[0].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            ext = 'png'
        main_path = os.path.join(save_dir, f'main.{ext}')
        
        img_response = requests.get(image_url, stream=True, timeout=60)
        img_response.raise_for_status()
        with open(main_path, 'wb') as f:
            for chunk in img_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"图片下载完成，保存到: {main_path}, 大小: {os.path.getsize(main_path)} bytes")
        
        # 4. 生成缩略图
        img = Image.open(main_path)
        img.thumbnail((480, 480))
        thumb_path = os.path.join(save_dir, f'480p.{ext}')
        img.save(thumb_path)
        print("缩略图生成完成")
        
        # 5. 调用cut.py切割图片（仅num>1时切割）
        if num > 1:
            print(f"开始切割图片，宫格数={num}")
            cut_cmd = [
                'python', os.path.join(BASE_DIR, 'cut.py'),
                '-path', main_path,
                '-num', str(num),
                '-out', save_dir
            ]
            result = subprocess.run(cut_cmd, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                print(f"图片切割成功: {result.stdout}")
            else:
                print(f"图片切割失败: {result.stderr}")
        else:
            print(f"宫格数=1，不需要切割")
            # 单张的情况复制一份命名为1.ext
            single_path = os.path.join(save_dir, f'1.{ext}')
            with open(main_path, 'rb') as f_src, open(single_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
            print(f"已生成单张图片: 1.{ext}")
        
        # 6. 保存data.txt
        with open(os.path.join(save_dir, 'data.txt'), 'w', encoding='utf-8') as f:
            f.write(f"ID: {work_id}\n")
            f.write(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"模型: {work['model']}\n")
            f.write(f"提示词: {work['prompt']}\n")
            f.write(f"分辨率: {work['ratio']}\n")
            f.write(f"质量: {work['quality']}\n")
            f.write(f"切割方式: {num}宫格\n")
            f.write(f"任务ID: {task_id}\n")
            f.write(f"原始图片地址: {image_url}\n")
            f.write(f"\n接口返回内容:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # 7. 更新数据库
        conn.execute('''
            UPDATE works SET state = 10, path = ?, filename = ?, ext = ?, error = '', respond = ? WHERE id = ?
        ''', (save_dir, f'main.{ext}', ext, json.dumps(data), work_id))
        conn.commit()
        print(f"任务处理完成，work_id={work_id}，保存路径: {save_dir}")
        
    except Exception as e:
        import traceback
        error_msg = f"处理失败: {str(e)}"
        print(f"[错误] {error_msg}")
        traceback.print_exc()
        conn.execute("UPDATE works SET state = 99, error = ? WHERE id = ?", (error_msg, work_id))
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
