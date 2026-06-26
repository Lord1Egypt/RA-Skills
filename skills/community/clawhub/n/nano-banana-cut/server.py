# -*- coding: utf-8 -*-
import warnings
# 过滤requests依赖版本警告
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="urllib3 (.*) or chardet/(.*) doesn't match a supported version!")
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sqlite3
import json
import requests
import datetime
import os
import sys
from PIL import Image
import zipfile
import io
import time
import threading
import subprocess
from dotenv import load_dotenv

# 加载.env配置
load_dotenv()
API_KEY = os.getenv('API_KEY')
PLATFORM_TOKEN = os.getenv('PLATFORM_TOKEN')

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

PORT = 697
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'works.db')
CONFIG_PATH = os.path.join(BASE_DIR, 'set.json')
PROMPT_PATH = os.path.join(BASE_DIR, 'prompt.md')

# 全局轮询锁，防止并发请求
polling_lock = False

# 初始化目录
os.makedirs(DATA_DIR, exist_ok=True)
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)
SAVE_BASE_PATH = CONFIG.get('save_path', os.path.join(os.path.expanduser("~"), "Desktop", "banana"))
os.makedirs(SAVE_BASE_PATH, exist_ok=True)

# 检查API_KEY配置，创建.env文件如果不存在
env_path = os.path.join(BASE_DIR, '.env')
if not os.path.exists(env_path):
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write("# 请访问 https://share.acedata.cloud/r/1uN88BrUTQ 获取以下配置\n")
        f.write("API_KEY=\n")
        f.write("PLATFORM_TOKEN=\n")

# 配置校验接口
@app.route('/api/config/check', methods=['GET'])
def check_config():
    if not API_KEY:
        return jsonify({"success": False, "msg": "未配置API_KEY", "need_config": True})
    return jsonify({"success": True, "msg": "配置正常"})

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            date TEXT NOT NULL,
            state INTEGER DEFAULT 1,
            prompt TEXT NOT NULL,
            ratio TEXT NOT NULL,
            quality TEXT NOT NULL,
            task_id TEXT,
            num INTEGER DEFAULT 1,
            path TEXT,
            filename TEXT,
            ext TEXT,
            request_data TEXT,
            error TEXT,
            respond TEXT
        )
    ''')
    
    # 检查是否需要添加 respond 字段（兼容旧数据库）
    c.execute("PRAGMA table_info(works)")
    columns = [col[1] for col in c.fetchall()]
    if 'respond' not in columns:
        print("检测到旧数据库，正在添加 respond 字段...")
        c.execute("ALTER TABLE works ADD COLUMN respond TEXT")
        print("respond 字段添加成功")
    
    conn.commit()
    conn.close()

init_db()

# 获取数据库连接
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 切割图片
def cut_image(image_path, num, output_dir, ext):
    try:
        img = Image.open(image_path)
        width, height = img.size
        is_landscape = width > height
        
        if num == 1:
            img.save(os.path.join(output_dir, f'1.{ext}'))
            return True
        elif num == 2:
            if is_landscape:
                w = width // 2
                for i in range(2):
                    box = (i*w, 0, (i+1)*w, height)
                    region = img.crop(box)
                    region.save(os.path.join(output_dir, f'{i+1}.{ext}'))
            else:
                h = height // 2
                for i in range(2):
                    box = (0, i*h, width, (i+1)*h)
                    region = img.crop(box)
                    region.save(os.path.join(output_dir, f'{i+1}.{ext}'))
        elif num == 4:
            w = width // 2
            h = height // 2
            idx = 1
            for i in range(2):
                for j in range(2):
                    box = (j*w, i*h, (j+1)*w, (i+1)*h)
                    region = img.crop(box)
                    region.save(os.path.join(output_dir, f'{idx}.{ext}'))
                    idx += 1
        elif num == 6:
            if is_landscape:
                w = width // 3
                h = height // 2
                idx = 1
                for i in range(2):
                    for j in range(3):
                        box = (j*w, i*h, (j+1)*w, (i+1)*h)
                        region = img.crop(box)
                        region.save(os.path.join(output_dir, f'{idx}.{ext}'))
                        idx += 1
            else:
                w = width // 2
                h = height // 3
                idx = 1
                for i in range(3):
                    for j in range(2):
                        box = (j*w, i*h, (j+1)*w, (i+1)*h)
                        region = img.crop(box)
                        region.save(os.path.join(output_dir, f'{idx}.{ext}'))
                        idx += 1
        elif num == 9:
            w = width // 3
            h = height // 3
            idx = 1
            for i in range(3):
                for j in range(3):
                    box = (j*w, i*h, (j+1)*w, (i+1)*h)
                    region = img.crop(box)
                    region.save(os.path.join(output_dir, f'{idx}.{ext}'))
                    idx += 1
        return True
    except Exception as e:
        print(f"图片切割失败: {e}")
        return False

# 轮询获取任务结果
def poll_task(task_id, work_id):
    global polling_lock
    if polling_lock:
        print(f"已有任务在轮询中，跳过任务 {work_id}")
        return
    
    polling_lock = True
    try:
        conn = get_db_connection()
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        max_retries = 50
        retry_count = 0
        
        print("\n" + "="*50)
        print(f"开始处理任务 work_id={work_id}, task_id={task_id}")
        print(f"请求地址: {CONFIG['server']['task_url']}")
        print(f"API Key: {CONFIG['server']['apikey'][:10]}...")
        
        while retry_count < max_retries:
            try:
                print(f"\n第 {retry_count+1} 次查询...")
                # 按照接口文档要求，仅提交id字段
                payload = {
                    "id": task_id
                }
                print(f"请求参数: {json.dumps(payload, indent=2)}")
                
                response = requests.post(CONFIG['server']['task_url'], headers=headers, json=payload, timeout=120)
                print(f"返回状态码: {response.status_code}")
                print(f"返回原始内容: {repr(response.text)}")
                
                response.raise_for_status()
                data = response.json()
                print(f"JSON解析成功，返回内容: {data}")
                
                # 处理空返回的情况
                if not data or not data.get('response'):
                    print(f"[警告] 返回数据为空或无response字段，继续重试...")
                    raise Exception("返回数据为空")
                
                if data['response'].get('success') and data['response'].get('data'):
                    image_url = data['response']['data'][0].get('image_url')
                    print(f"[成功] 生成成功，图片地址: {image_url}")
                    if not image_url:
                        error_msg = "图片地址为空"
                        print(f"[错误] {error_msg}")
                        conn.execute("UPDATE works SET state = 99, error = ? WHERE id = ?", (error_msg, work_id))
                        conn.commit()
                        break
                    
                    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    save_dir = os.path.join(SAVE_BASE_PATH, now)
                    os.makedirs(save_dir, exist_ok=True)
                    
                    try:
                        print(f"开始下载图片: {image_url}")
                        ext = image_url.split('.')[-1].split('?')[0].lower()
                        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                            ext = 'png'
                        main_path = os.path.join(save_dir, f'main.{ext}')
                        
                        img_response = requests.get(image_url, stream=True, timeout=60)
                        img_response.raise_for_status()
                        with open(main_path, 'wb') as f:
                            for chunk in img_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"图片下载完成，大小: {os.path.getsize(main_path)} bytes")
                    except Exception as e:
                        error_msg = f"图片下载失败: {str(e)}"
                        print(f"[错误] {error_msg}")
                        conn.execute("UPDATE works SET state = 99, error = ? WHERE id = ?", (error_msg, work_id))
                        conn.commit()
                        break
                    
                    img = Image.open(main_path)
                    img.thumbnail((480, 480))
                    thumb_path = os.path.join(save_dir, f'480p.{ext}')
                    img.save(thumb_path)
                    
                    work = conn.execute("SELECT num FROM works WHERE id = ?", (work_id,)).fetchone()
                    cut_image(main_path, work['num'], save_dir, ext)
                    
                    work_data = conn.execute("SELECT * FROM works WHERE id = ?", (work_id,)).fetchone()
                    with open(os.path.join(save_dir, 'data.txt'), 'w', encoding='utf-8') as f:
                        f.write(f"ID: {work_data['id']}\n")
                        f.write(f"生成时间: {work_data['date']}\n")
                        f.write(f"模型: {work_data['model']}\n")
                        f.write(f"提示词: {work_data['prompt']}\n")
                        f.write(f"分辨率: {work_data['ratio']}\n")
                        f.write(f"质量: {work_data['quality']}\n")
                        f.write(f"切割方式: {work_data['num']}宫格\n")
                        f.write(f"任务ID: {task_id}\n")
                        f.write(f"原始图片地址: {image_url}\n")
                    
                    conn.execute('''
                        UPDATE works SET state = 10, path = ?, filename = ?, ext = ? WHERE id = ?
                    ''', (save_dir, f'main.{ext}', ext, work_id))
                    conn.commit()
                    break
                    
                elif data.get('response') and not data['response'].get('success'):
                    error_msg = data['response'].get('error', '生成失败')
                    print(f"[错误] 生成失败: {error_msg}")
                    conn.execute("UPDATE works SET state = 99, error = ? WHERE id = ?", (error_msg, work_id))
                    conn.commit()
                    break
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"网络请求失败: {str(e)}"
                print(f"[警告] {error_msg}，继续重试...")
                conn.execute("UPDATE works SET error = ? WHERE id = ?", (error_msg, work_id))
                conn.commit()
            except json.JSONDecodeError as e:
                error_msg = f"返回数据解析失败: {str(e)}"
                print(f"[警告] {error_msg}，继续重试...")
                conn.execute("UPDATE works SET error = ? WHERE id = ?", (error_msg, work_id))
                conn.commit()
            except Exception as e:
                import traceback
                error_msg = f"请求异常: {str(e)}"
                print(f"[警告] {error_msg}，继续重试...")
                conn.execute("UPDATE works SET error = ? WHERE id = ?", (str(e), work_id))
                conn.commit()
            
            retry_count += 1
            # 前30次每6秒查询一次，30次后每60秒查询一次
            if retry_count < 30:
                time.sleep(6)
            else:
                time.sleep(60)
        
        if retry_count >= max_retries:
            error_msg = f"轮询超时，共尝试{max_retries}次"
            print(f"[错误] {error_msg}")
            conn.execute("UPDATE works SET state = 99, error = ? WHERE id = ?", (error_msg, work_id))
            conn.commit()
        conn.close()
        print("="*50)
        print(f"任务处理结束 work_id={work_id}")
    finally:
        polling_lock = False

# 启动时恢复未完成的任务
def resume_pending_tasks():
    conn = get_db_connection()
    # 恢复处理中(1)和失败但有task_id(99)的任务，重新查询
    pending_works = conn.execute("SELECT id, task_id FROM works WHERE state = 1 OR (state = 99 AND task_id IS NOT NULL)").fetchall()
    conn.close()
    for work in pending_works:
        if work['task_id']:
            print(f"恢复任务: work_id={work['id']}, task_id={work['task_id']}")
            threading.Thread(target=poll_task, args=(work['task_id'], work['id']), daemon=True).start()

# 【注意】任务恢复由前端 loadWorks() 自动处理，无需服务端干预
# resume_pending_tasks()

# 路由
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# 管理后台页面
@app.route('/admin')
def admin_page():
    return send_from_directory(os.path.join(BASE_DIR, 'templates'), 'admin.html')

# 管理后台获取所有任务接口
@app.route('/api/admin/works', methods=['GET'])
def admin_get_works():
    try:
        conn = get_db_connection()
        works = conn.execute('SELECT * FROM works ORDER BY id DESC').fetchall()
        conn.close()
        result = [dict(work) for work in works]
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# 手动重试任务接口
@app.route('/api/admin/retry/<int:id>', methods=['POST'])
def admin_retry_task(id):
    try:
        conn = get_db_connection()
        work = conn.execute('SELECT id, task_id FROM works WHERE id = ?', (id,)).fetchone()
        if not work or not work['task_id']:
            return jsonify({"success": False, "msg": "任务不存在或无task_id"})
        # 重置状态为处理中，清空错误信息，由前端发起轮询
        conn.execute("UPDATE works SET state = 1, error = '' WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "msg": "任务已重置为处理中，请等待前端轮询结果"})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# 关闭任务接口
@app.route('/api/admin/close/<int:id>', methods=['POST'])
def admin_close_task(id):
    try:
        conn = get_db_connection()
        conn.execute("UPDATE works SET state = 99, error = '手动关闭任务' WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "msg": "任务已关闭，状态变为失败"})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# 保存配置接口
@app.route('/api/config/save', methods=['POST'])
def save_config():
    try:
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        platform_token = data.get('platform_token', '').strip()
        
        if not api_key:
            return jsonify({"success": False, "msg": "API_KEY为必填项，请填写"}), 400
        
        # 写入.env文件
        env_path = os.path.join(BASE_DIR, '.env')
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(f"API_KEY={api_key}\n")
            f.write(f"PLATFORM_TOKEN={platform_token}\n")
        
        # 全局更新配置
        global API_KEY, PLATFORM_TOKEN
        API_KEY = api_key
        PLATFORM_TOKEN = platform_token
        
        return jsonify({"success": True, "msg": "配置保存成功，请刷新页面生效"})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# 图片上传接口
@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if not PLATFORM_TOKEN:
            return jsonify({"success": False, "msg": "未配置PLATFORM_TOKEN，请先配置密钥", "need_config": True}), 401
        
        if 'file' not in request.files:
            return jsonify({"success": False, "msg": "没有上传文件"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "msg": "没有选择文件"}), 400
        
        # 保存临时文件
        temp_dir = os.path.join(BASE_DIR, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        # 调用upload.py上传
        from upload import upload_image, init_upload_table
        init_upload_table()
        result = upload_image(temp_path)
        
        # 删除临时文件
        os.remove(temp_path)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# 删除任务接口
@app.route('/api/admin/delete/<int:id>', methods=['POST'])
def admin_delete_task(id):
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM works WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "msg": "任务已删除"})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        "success": True,
        "data": {
            "models": CONFIG['models'],
            "resolutions": CONFIG['resolutions'],
            "qualities": CONFIG['qualities']
        }
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        model = data.get('model', 0)
        ratio_idx = data.get('ratio', 0)
        quality_idx = data.get('quality', 0)
        num = data.get('num', 1)
        images = data.get('images', [])
        
        if not prompt and not images:
            return jsonify({"success": False, "msg": "请输入提示词或上传参考图"}), 400
        
        with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        full_prompt = system_prompt.replace('{num}', str(num)).replace('{prompt}', prompt)
        
        model_config = CONFIG['models'][model]
        ratio_config = CONFIG['resolutions'][ratio_idx]
        quality_config = CONFIG['qualities'][quality_idx]
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        # 有参考图时使用edit模式，否则使用generate模式
        if images and len(images) > 0:
            payload = {
                "action": "edit",
                "model": model_config['model'],
                "prompt": full_prompt,
                "aspect_ratio": ratio_config['ratio'],
                "resolution": quality_config['size'],
                "count": 1,
                "image_urls": images,
                "callback_url": "aaa"
            }
        else:
            payload = {
                "action": "generate",
                "model": model_config['model'],
                "prompt": full_prompt,
                "aspect_ratio": ratio_config['ratio'],
                "resolution": quality_config['size'],
                "num_images": 1,
                "callback_url": "aaa"
            }
        
        print(f"生成请求URL: {CONFIG['server']['url']}")
        print(f"请求头: {json.dumps(headers, indent=2)}")
        print(f"请求payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        response = requests.post(CONFIG['server']['url'], headers=headers, json=payload, timeout=120)
        print(f"返回状态码: {response.status_code}")
        print(f"返回内容: {repr(response.text)}")
        response.raise_for_status()
        result = response.json()
        
        if not result.get('task_id'):
            return jsonify({"success": False, "msg": "获取任务ID失败: " + result.get('error', '未知错误')}), 400
        
        task_id = result['task_id']
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO works (model, date, prompt, ratio, quality, task_id, num, request_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (model_config['name'], now, prompt, ratio_config['name'], quality_config['name'], task_id, num, json.dumps(payload)))
        work_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # 【已修复】不再后端启动轮询，改由前端控制轮询，支持多任务并发
        # threading.Thread(target=poll_task, args=(task_id, work_id), daemon=True).start()
        
        return jsonify({"success": True, "msg": "任务提交成功", "work_id": work_id})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

@app.route('/api/works', methods=['GET'])
def get_works():
    try:
        conn = get_db_connection()
        works = conn.execute('SELECT * FROM works WHERE state > 0 ORDER BY date DESC').fetchall()
        conn.close()
        
        result = []
        for work in works:
            item = dict(work)
            # 仅对成功完成的任务(状态10)检测图片是否存在
            if item['state'] == 10 and item['path']:
                thumb_path = os.path.join(item['path'], f'480p.{item["ext"]}')
                if not os.path.exists(thumb_path):
                    conn = get_db_connection()
                    conn.execute("UPDATE works SET state = 0 WHERE id = ?", (item['id'],))
                    conn.commit()
                    conn.close()
                    item['state'] = 0
            result.append(item)
        
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

@app.route('/api/work/<int:id>', methods=['GET'])
def get_work(id):
    try:
        conn = get_db_connection()
        work = conn.execute('SELECT * FROM works WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        if not work:
            return jsonify({"success": False, "msg": "作品不存在"}), 404
        
        work_dict = dict(work)
        # 仅对成功完成的任务(状态10)检测图片是否存在
        if work_dict['state'] == 10 and work_dict['path']:
            main_path = os.path.join(work_dict['path'], f'main.{work_dict["ext"]}')
            if not os.path.exists(main_path):
                conn = get_db_connection()
                conn.execute("UPDATE works SET state = 0 WHERE id = ?", (id,))
                conn.commit()
                conn.close()
                work_dict['state'] = 0
                return jsonify({"success": True, "data": work_dict})
            
            images = []
            for i in range(1, work_dict['num'] + 1):
                img_path = f'/{work_dict["path"].replace(os.sep, "/")}/{i}.{work_dict["ext"]}'
                images.append(img_path)
            
            work_dict['images'] = images
            work_dict['main_image'] = f'/{work_dict["path"].replace(os.sep, "/")}/main.{work_dict["ext"]}'
            work_dict['thumb_image'] = f'/{work_dict["path"].replace(os.sep, "/")}/480p.{work_dict["ext"]}'
        
        return jsonify({"success": True, "data": work_dict})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# 全局锁，防止同一个任务重复执行
running_tasks = set()

@app.route('/api/poll/<int:id>', methods=['GET'])
def poll_work(id):
    try:
        conn = get_db_connection()
        work = conn.execute('SELECT id, state, error, task_id FROM works WHERE id = ?', (id,)).fetchone()
        if not work:
            conn.close()
            return jsonify({"success": False, "msg": "任务不存在"}), 404
        
        respond_data = None
        
        # 处理中且没有在执行的任务，调用task.py异步处理
        if work['state'] == 1 and work['task_id'] and id not in running_tasks:
            # 标记任务正在执行，防止重复调用
            running_tasks.add(id)
            # 后台线程调用task.py处理任务
            def run_task():
                try:
                    cmd = [sys.executable, os.path.join(BASE_DIR, 'task.py'), '-id', str(id)]
                    subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=300)
                finally:
                    # 执行完成移除锁
                    if id in running_tasks:
                        running_tasks.remove(id)
            
            threading.Thread(target=run_task, daemon=True).start()
            respond_data = {"msg": "任务已开始处理，请稍候"}
        
        # 读取最新的任务状态
        conn = get_db_connection()
        work = conn.execute('SELECT id, state, error, task_id, respond FROM works WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        respond = None
        if work['respond']:
            try:
                respond = json.loads(work['respond'])
            except:
                respond = work['respond']
        
        return jsonify({
            "success": True, 
            "data": {
                "state": work['state'], 
                "error": work['error'],
                "task_id": work['task_id'],
                "task_url": CONFIG['server']['task_url'],
                "respond": respond
            }
        })
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

@app.route('/api/download/<int:id>', methods=['GET'])
def download_work(id):
    try:
        conn = get_db_connection()
        work = conn.execute('SELECT * FROM works WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        if not work or work['state'] != 10 or not work['path']:
            return jsonify({"success": False, "msg": "作品不存在或未生成完成"}), 404
        
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            main_path = os.path.join(work['path'], f'main.{work["ext"]}')
            if os.path.exists(main_path):
                zf.write(main_path, f'main.{work["ext"]}')
            
            thumb_path = os.path.join(work['path'], f'480p.{work["ext"]}')
            if os.path.exists(thumb_path):
                zf.write(thumb_path, f'480p.{work["ext"]}')
            
            for i in range(1, work['num'] + 1):
                img_path = os.path.join(work['path'], f'{i}.{work["ext"]}')
                if os.path.exists(img_path):
                    zf.write(img_path, f'{i}.{work["ext"]}')
            
            data_path = os.path.join(work['path'], 'data.txt')
            if os.path.exists(data_path):
                zf.write(data_path, 'data.txt')
        
        memory_file.seek(0)
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{work["id"]}_{work["prompt"][:20].replace(" ", "_")}.zip'
        )
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

@app.route('/api/open-folder/<int:id>', methods=['POST'])
def open_folder(id):
    try:
        conn = get_db_connection()
        work = conn.execute('SELECT path FROM works WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        if not work or not work['path'] or not os.path.exists(work['path']):
            return jsonify({"success": False, "msg": "目录不存在"}), 404
        
        os.startfile(work['path'])
        return jsonify({"success": True, "msg": "已打开文件夹"})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    try:
        os._exit(0)
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# 图片N宫格裁剪接口
@app.route('/api/cut', methods=['POST'])
def api_cut_image():
    try:
        data = request.get_json()
        path = data.get('path')
        num = data.get('num')
        out = data.get('out', None)
        
        if not path or not num:
            return jsonify({"success": False, "msg": "参数缺失，path(图片路径)和num(宫格数)为必填项"})
        
        # 构造cut.py命令
        cmd = [sys.executable, os.path.join(BASE_DIR, 'cut.py'), '-path', path, '-num', str(num)]
        if out:
            cmd.extend(['-out', out])
        
        # 执行裁剪命令
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            return jsonify({
                "success": True,
                "msg": "图片裁剪成功",
                "output_log": result.stdout
            })
        else:
            return jsonify({
                "success": False,
                "msg": "图片裁剪失败",
                "error_log": result.stderr
            })
    except Exception as e:
        return jsonify({"success": False, "msg": f"接口异常：{str(e)}"}), 500

@app.route('/<path:filepath>')
def serve_file(filepath):
    if '..' in filepath or filepath.startswith('/'):
        return "Invalid path", 403
    full_path = os.path.join('/', filepath)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path))
    return "File not found", 404

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == '-task_id':
        task_id = sys.argv[2]
        print(f"手动查询任务: {task_id}")
        conn = get_db_connection()
        # 先查询是否已存在该task_id的任务
        exist_work = conn.execute("SELECT id, num FROM works WHERE task_id = ?", (task_id,)).fetchone()
        if exist_work:
            work_id = exist_work['id']
            num = exist_work['num']
            print(f"找到已存在任务 work_id={work_id}, 宫格数={num}")
            poll_task(task_id, work_id)
        else:
            # 不存在则新建，默认1宫格
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO works (model, date, prompt, ratio, quality, task_id, num, request_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ("手动查询任务", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "手动导入任务", "1:1 方形", "2K", task_id, 1, "{}"))
            work_id = cursor.lastrowid
            conn.commit()
            poll_task(task_id, work_id)
        conn.close()
        print(f"任务处理完成，work_id={work_id}")
    else:
        print(f"banana-cut 服务启动成功，访问地址：http://localhost:{PORT}")
        app.run(host='0.0.0.0', port=PORT, debug=False)
