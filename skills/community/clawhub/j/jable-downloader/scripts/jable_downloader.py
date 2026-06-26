#!/usr/bin/env python3
"""
Jable.tv Video Downloader v20 - Flask-SocketIO Real-time Progress Push + Auto IP Detection + Crash Protection
"""

import sys
import os
import re
import subprocess
import urllib.request
import time
import shutil
import platform
import json
import threading
import queue
import socket
import signal
from pathlib import Path
from urllib.parse import quote

PORT = 5000

# Optional netifaces, lazy import
netifaces = None
try:
    import netifaces
except ImportError:
    pass

def get_all_accessible_ips():
    """Get all accessible IP addresses"""
    ips = []
    
    # Method 1: Use netifaces to get IPs from all network interfaces (if installed)
    if netifaces:
        try:
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip = addrs[netifaces.AF_INET][0]['addr']
                    if ip and not ip.startswith('127.'):
                        ips.append(ip)
        except:
            pass
    
    # Method 2: Detect via UDP socket connection (fallback)
    if not ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
            if ip:
                ips.append(ip)
            s.close()
        except:
            pass
    
    # Ensure at least one IP
    if not ips:
        ips = ['127.0.0.1', 'localhost']
    
    # Remove duplicates
    ips = list(set(ips))
    return ips

# Lazy initialization, get IP only when needed
_accessible_urls = None

def get_accessible_urls():
    """Get all accessible URL lists"""
    global _accessible_urls
    if _accessible_urls is None:
        ips = get_all_accessible_ips()
        _accessible_urls = [f"http://{ip}:{PORT}" for ip in ips]
    return _accessible_urls

# Global state (in memory)
progress_state = {
    "status": "idle",
    "jobs": [],
    "total": 0,
    "completed": 0,
    "failed": 0
}
state_lock = threading.Lock()

# SocketIO global instance
socketio = None

def get_default_videos_dir():
    home = Path.home()
    system = platform.system()
    if system == "Linux":
        try:
            res = subprocess.run(['xdg-user-dir', 'VIDEOS'], capture_output=True, text=True, check=True)
            path = Path(res.stdout.strip())
            if path.exists(): return str(path)
        except: pass
    candidates = ["Videos", "Movies", "影片", "動画"]
    for name in candidates:
        p = home / name
        if p.exists(): return str(p)
    return str(home)

def broadcast_update():
    """Broadcast progress update to local SocketIO clients"""
    global socketio
    if socketio:
        try:
            # Directly push local memory state, no HTTP requests involved
            socketio.emit('progress_update', progress_state)
        except:
            pass

def send_to_server(endpoint, data):
    """(Disabled) To avoid server load"""
    pass

def init_progress():
    with state_lock:
        global progress_state
        progress_state = {"status": "idle", "jobs": [], "total": 0, "completed": 0, "failed": 0}
        global last_notify_time
        last_notify_time = {}
    broadcast_update()

def add_job(title, url, actress, notify=True):
    with state_lock:
        global progress_state
        job_id = len(progress_state["jobs"])
        job = {"id": job_id, "title": title[:50], "actress": actress, "url": url, 
               "progress": 0, "speed": "", "eta": "", "status": "waiting"}
        progress_state["jobs"].append(job)
        progress_state["total"] = len(progress_state["jobs"])
        progress_state["status"] = "downloading"
    broadcast_update()
    return job_id

def update_job_progress(job_id, progress, speed="", eta="", notify=True):
    """Update progress with built-in 1-second throttle protection"""
    import time
    current_time = time.time()
    
    global last_notify_time
    last = last_notify_time.get(job_id, 0)
    
    # Strict control: Update at most once per second to avoid flooding SocketIO
    if current_time - last < 1.0:
        return
        
    last_notify_time[job_id] = current_time
    
    with state_lock:
        for job in progress_state["jobs"]:
            if job["id"] == job_id:
                job["progress"] = progress
                job["speed"] = speed
                job["eta"] = eta
                job["status"] = "downloading"
                break
    broadcast_update()

def complete_job(job_id, success=True, notify=True):
    with state_lock:
        for job in progress_state["jobs"]:
            if job["id"] == job_id:
                job["progress"] = 100 if success else 0
                job["status"] = "completed" if success else "failed"
                if success:
                    progress_state["completed"] = progress_state.get("completed", 0) + 1
                else:
                    progress_state["failed"] = progress_state.get("failed", 0) + 1
                break
        if all(j["status"] in ["completed", "failed"] for j in progress_state["jobs"]):
            progress_state["status"] = "completed"
    broadcast_update()

# Flask-SocketIO Server
from flask import Flask, render_template_string, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jable-secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jable Download Progress</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 28px; }
        .stats { display: flex; justify-content: center; gap: 30px; margin-bottom: 30px; }
        .stat { background: rgba(255,255,255,0.1); padding: 15px 30px; border-radius: 10px; text-align: center; }
        .stat-value { color: #667eea; font-size: 24px; font-weight: bold; }
        .stat-label { color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 5px; }
        .jobs { display: flex; flex-direction: column; gap: 15px; }
        .job-card { background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .job-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .job-title { font-weight: bold; color: #1a1a2e; font-size: 14px; }
        .job-status { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .job-status.waiting { background: #e0e0e0; color: #666; }
        .job-status.downloading { background: #fff3cd; color: #856404; }
        .job-status.completed { background: #d4edda; color: #155724; }
        .job-status.failed { background: #f8d7da; color: #721c24; }
        .progress-container { background: #e9ecef; border-radius: 8px; height: 24px; overflow: hidden; margin-bottom: 8px; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); width: 0%; transition: width 0.3s ease; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; }
        .job-info { display: flex; justify-content: space-between; font-size: 12px; color: #6c757d; }
        .url-box { text-align: center; margin-top: 30px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; }
        .url-box a { color: #667eea; text-decoration: none; }
        .empty { text-align: center; color: rgba(255,255,255,0.5); padding: 50px; }
        .connected { position: fixed; top: 10px; right: 10px; padding: 5px 10px; background: #28a745; color: white; border-radius: 5px; font-size: 12px; }
        .disconnected { background: #dc3545; }
    </style>
</head>
<body>
    <div class="connected" id="connectionStatus">🔴 Connecting...</div>
    <div class="container">
        <h1>📥 Jable Download Progress</h1>
        <div class="stats">
            <div class="stat"><div class="stat-value" id="total">0</div><div class="stat-label">Total</div></div>
            <div class="stat"><div class="stat-value" id="completed">0</div><div class="stat-label">Completed</div></div>
            <div class="stat"><div class="stat-value" id="failed">0</div><div class="stat-label">Failed</div></div>
        </div>
        <div class="jobs" id="jobs"></div>
        <div class="url-box" id="urlBox"><a href="#">Loading...</a></div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
    <script>
        const socket = io();
        
        const statusEl = document.getElementById('connectionStatus');
        
        socket.on('connect', function() {
            statusEl.textContent = '🟢 Connected';
            statusEl.classList.remove('disconnected');
        });
        
        socket.on('disconnect', function() {
            statusEl.textContent = '🔴 Disconnected';
            statusEl.classList.add('disconnected');
        });
        
        socket.on('progress_update', function(data) {
            renderJobs(data);
        });
        
        function renderJobs(data) {
            const container = document.getElementById('jobs');
            const jobs = data.jobs || [];
            if (jobs.length === 0) { 
                container.innerHTML = '<div class="empty">Waiting for tasks...</div>'; 
                return; 
            }
            container.innerHTML = jobs.map(job => `
                <div class="job-card">
                    <div class="job-header">
                        <div class="job-title">${job.title || 'Unknown'}</div>
                        <div class="job-status ${job.status}">${getStatusText(job.status)}</div>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: ${job.progress}%">${job.progress}%</div>
                    </div>
                    <div class="job-info">
                        <span>${job.actress || ''}</span>
                        <span>${job.speed || ''} ${job.eta || ''}</span>
                    </div>
                </div>
            `).join('');
            document.getElementById('total').textContent = data.total || 0;
            document.getElementById('completed').textContent = data.completed || 0;
            document.getElementById('failed').textContent = data.failed || 0;
        }
        
        function getStatusText(status) {
            const map = {'waiting': 'Waiting', 'downloading': 'Downloading', 'completed': '✅ Done', 'failed': '❌ Failed'};
            return map[status] || status;
        }
        
        // Get all accessible URLs
        fetch('/urls').then(r => r.json()).then(data => {
            const urlBox = document.getElementById('urlBox');
            urlBox.innerHTML = data.urls.map(url => 
                `<a href="${url}" target="_blank">${url}</a>`
            ).join('<br>');
        });
        
        // Polling fallback: Poll API every 3 seconds
        setInterval(() => {
            fetch('/api/progress')
                .then(r => r.json())
                .then(data => renderJobs(data))
                .catch(() => {});
        }, 3000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/urls')
def get_urls():
    return jsonify({"urls": get_accessible_urls()})

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current progress status"""
    with state_lock:
        return jsonify(progress_state)

@app.route('/api/add_job', methods=['POST'])
def api_add_job():
    """Add job from client"""
    import json
    data = request.get_json()
    url = data.get('url', '')
    
    # Check if job with same URL already exists to avoid duplicates
    with state_lock:
        existing = [j for j in progress_state["jobs"] if j.get("url") == url]
        if existing:
            job_id = existing[0]["id"]
        else:
            job_id = add_job(data.get('title', ''), url, data.get('actress', ''), notify=False)
    
    broadcast_update()
    return jsonify({"job_id": job_id})

@app.route('/api/update_progress', methods=['POST'])
def api_update_progress():
    """Update progress from client"""
    import json
    data = request.get_json()
    update_job_progress(data.get('job_id', 0), data.get('progress', 0), data.get('speed', ''), data.get('eta', ''), notify=False)
    return jsonify({"success": True})

@app.route('/api/complete_job', methods=['POST'])
def api_complete_job():
    """Complete job from client"""
    import json
    data = request.get_json()
    complete_job(data.get('job_id', 0), data.get('success', False), notify=False)
    return jsonify({"success": True})

# Download functions
def normalize_url(input_str):
    input_str = input_str.strip()
    if input_str.startswith('http://') or input_str.startswith('https://'):
        return input_str.rstrip('/') + '/'
    return f"https://jable.tv/videos/{input_str}/"

def get_real_hls_url(page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Referer': 'https://jable.tv/'}
    try:
        req = urllib.request.Request(page_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        title_match = re.search(r'<h4[^>]*>([^<]+)</h4>', html)
        title = re.sub(r'[\\/:*?"<>|]', '_', title_match.group(1).strip()) if title_match else "video"
        hls_match = re.search(r"hlsUrl\s*=\s*'([^']+)'", html)
        if not hls_match: hls_match = re.search(r'source\s*:\s*"([^"]+\.m3u8)"', html)
        if hls_match: return title, hls_match.group(1)
    except: pass
    return None, None

def extract_actress_name(title):
    name_match = re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]+$', title.strip())
    return name_match.group(0).strip() if name_match else "Unknown"

def organize_by_actress(output_path, actress_name):
    output_dir = os.path.dirname(output_path)
    actress_dir = os.path.join(output_dir, actress_name)
    if not os.path.exists(actress_dir): os.makedirs(actress_dir)
    new_path = os.path.join(actress_dir, os.path.basename(output_path))
    if output_path != new_path: shutil.move(output_path, new_path)
    return new_path

def search_actress_videos(actress_name):
    print(f"🔍 Searching: {actress_name}")
    search_url = f"https://jable.tv/search/{quote(actress_name)}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    videos = []
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        for m in re.findall(r'<h6 class="title"><a href="(https://jable\.tv/videos/[^"]+/)">([^<]+)</a></h6>', html):
            videos.append({'url': m[0], 'title': m[1].strip()})
    except Exception as e: print(f"Error: {e}")
    return videos

def check_already_downloaded(video_title, videos_dir):
    if not os.path.exists(videos_dir): return False
    code = re.search(r'([A-Z]+-\d+)', video_title, re.I)
    if code:
        for root, dirs, files in os.walk(videos_dir):
            # Fix: Check if code is "contained in" filename (substring match), not "equals" filename
            if any(code.group(1).upper() in f.upper() for f in files): return True
    return False

def cleanup_temp_files(output_path):
    """Clean up temporary files generated during download"""
    if not output_path: return
    base_dir = os.path.dirname(output_path)
    filename = os.path.basename(output_path)
    # Find all related .part, .part-Frag*, .ytdl files
    if os.path.exists(base_dir):
        for f in os.listdir(base_dir):
            if (f.startswith(filename + '.part') or 
                f.startswith('.' + filename + '.part') or
                f == filename + '.ytdl' or
                f == '.' + filename + '.ytdl'):
                try:
                    os.remove(os.path.join(base_dir, f))
                    print(f"🧹 Cleaned temp file: {f}")
                except: pass

def download_single_video(job_id, url, output_dir, max_retries=2):
    # Update status to downloading
    with state_lock:
        for job in progress_state["jobs"]:
            if job["id"] == job_id: job["status"] = "downloading"
    broadcast_update()
    
    title, m3u8_url = get_real_hls_url(url)
    if not m3u8_url: 
        complete_job(job_id, False)
        return {"success": False, "title": title}
    
    actress = extract_actress_name(title)
    output_path = os.path.join(output_dir, f"{title}.mp4")
    
    for attempt in range(max_retries):
        cmd = ['yt-dlp', '--force-ipv4', '--concurrent-fragments', '16', '--referer', 'https://jable.tv/', '-o', output_path, m3u8_url]
        
        print(f"⬇️ Downloading: {title} (attempt {attempt + 1}/{max_retries})")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        for line in process.stdout:
            if '[download]' in line:
                p = re.search(r'([\d.]+)%', line)
                if p:
                    speed = re.search(r'at\s+([\d.]+[KMGiB]*[/s]*)', line)
                    eta = re.search(r'ETA\s+([\d:]+)', line)
                    update_job_progress(job_id, float(p.group(1)), speed.group(1) if speed else "", eta.group(1) if eta else "")
        
        process.wait()
        if process.returncode == 0 and os.path.exists(output_path):
            organize_by_actress(output_path, actress)
            cleanup_temp_files(output_path)
            complete_job(job_id, True)
            print(f"✅ Completed: {title}")
            return {"success": True, "title": title}
        
        print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
        cleanup_temp_files(output_path)
    
    # Both attempts failed
    cleanup_temp_files(output_path)
    complete_job(job_id, False)
    print(f"❌ Failed: {title}")
    return {"success": False, "title": title}

def download_worker(task_queue, output_dir, failed_titles=None):
    """Download worker thread"""
    while True:
        try:
            task = task_queue.get(timeout=1)
            if task is None: break
            job_id, url, title = task
            result = download_single_video(job_id, url, output_dir)
            if failed_titles is not None and not result.get("success", False):
                failed_titles.append(result.get("title", ""))
            task_queue.task_done()
        except: continue

def start_downloads(video_list, output_dir, max_concurrent=3, actress_name=None):
    init_progress()
    task_queue = queue.Queue()
    failed_titles = []  # Track failed videos
    
    # Initial video list
    for v in video_list:
        title = v['title']
        actress = extract_actress_name(title)
        job_id = add_job(title, v['url'], actress)
        task_queue.put((job_id, v['url'], title))
    
    target_count = len(video_list)
    current_count = len(video_list)
    
    print(f"🚀 Starting download of {len(video_list)} videos (concurrent: {max_concurrent})")
    
    threads = []
    for _ in range(max_concurrent):
        t = threading.Thread(target=download_worker, args=(task_queue, output_dir, failed_titles))
        t.start()
        threads.append(t)
    
    task_queue.join()
    for _ in range(max_concurrent): task_queue.put(None)
    for t in threads: t.join()
    
    # If there are failed videos, try to find other videos to fill the gap
    if failed_titles and actress_name and current_count < target_count:
        print(f"⚠️ {len(failed_titles)} videos failed to download, trying to find other videos...")
        
        # Search for more videos
        all_videos = search_actress_videos(actress_name)
        # Exclude already downloaded and failed attempts
        downloaded_titles = [v['title'] for v in video_list]
        downloaded_titles.extend(failed_titles)
        
        extra_videos = []
        for v in all_videos:
            if v['title'] not in downloaded_titles and not check_already_downloaded(v['title'], output_dir):
                extra_videos.append(v)
                downloaded_titles.append(v['title'])
                if len(extra_vitles) >= len(failed_titles):
                    break
        
        if extra_videos:
            print(f"📥 Added {len(extra_videos)} extra videos for download...")
            for v in extra_videos:
                title = v['title']
                actress = extract_actress_name(title)
                job_id = add_job(title, v['url'], actress)
                task_queue.put((job_id, v['url'], title))
            
            # Re-run downloads
            threads = []
            for _ in range(min(max_concurrent, len(extra_videos))):
                t = threading.Thread(target=download_worker, args=(task_queue, output_dir, failed_titles))
                t.start()
                threads.append(t)
            
            task_queue.join()
            for _ in range(max_concurrent): task_queue.put(None)
            for t in threads: t.join()
    
    print("🎉 All completed!")

def send_telegram_notification():
    """Send Telegram notification with all accessible URLs"""
    urls = get_accessible_urls()
    # Use Markdown Hyperlink format: [display text](url)
    urls_text = '\n'.join([f"[🔗 {url}]({url})" for url in urls])
    try:
        subprocess.run(["openclaw", "message", "send", "--channel", "telegram", "--target", "417705913", 
                       "--message", f"📥 Jable Download Started!\n\n{urls_text}"], 
                       capture_output=True, timeout=10)
    except: pass

def run_server():
    """Run SocketIO server in separate thread"""
    urls = get_accessible_urls()
    print(f"🚀 Starting server:")
    for url in urls:
        print(f"   {url}")
    init_progress()
    socketio.run(app, host='0.0.0.0', port=PORT, debug=False, allow_unsafe_werkzeug=True)

def cleanup_all_temp_files(output_dir):
    """Clean up all temporary files in the specified directory"""
    if not os.path.exists(output_dir):
        return
    cleaned = 0
    for f in os.listdir(output_dir):
        if '.part' in f or f.endswith('.ytdl'):
            try:
                os.remove(os.path.join(output_dir, f))
                cleaned += 1
            except:
                pass
    if cleaned > 0:
        print(f"🧹 Cleaned {cleaned} temporary files")

def signal_handler(signum, frame):
    """Handle interrupt signal, cleanup and exit"""
    print("\n⚠️ Received interrupt signal, cleaning up...")
    output_dir = get_default_videos_dir()
    cleanup_all_temp_files(output_dir)
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Clean up previous temp files on startup
    output_dir = get_default_videos_dir()
    cleanup_all_temp_files(output_dir)
    
    if len(sys.argv) >= 2 and sys.argv[1] == '--server':
        run_server()
        sys.exit(0)
    
    # --- Auto start background server in download mode ---
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Wait for server to start and show IP
    send_telegram_notification()
    
    # Parse arguments
    if len(sys.argv) >= 2 and sys.argv[1] == '--search':
        actress_name = sys.argv[2] if len(sys.argv) >= 3 else None
        count = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
        output_dir = sys.argv[4] if len(sys.argv) >= 5 else get_default_videos_dir()
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Client mode: Don't start server, connect directly to main server
        
        # Execute download
        videos = search_actress_videos(actress_name)
        if not videos: print(f"❌ Cannot find '{actress_name}'"); sys.exit(1)
        new_videos = [v for v in videos if not check_already_downloaded(v['title'], output_dir)][:count]
        print(f"📥 Will download {len(new_videos)} videos")
        start_downloads(new_videos, output_dir, max_concurrent=3, actress_name=actress_name)
        
    elif len(sys.argv) >= 2:
        # Single video
        video_id = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) >= 3 else get_default_videos_dir()
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Client mode: Don't start server, connect directly to main server
        
        # Execute download - Get title first
        url = normalize_url(video_id)
        print(f"🔍 Getting video info: {url}")
        title, m3u8_url = get_real_hls_url(url)
        if title:
            videos = [{'url': url, 'title': title}]
            print(f"📥 Will download: {title}")
        else:
            videos = [{'url': url, 'title': f'{video_id}'}]
            print(f"📥 Will download 1 video")
        start_downloads(videos, output_dir, max_concurrent=1)
    else:
        print("Usage: jable_downloader.py --search <actress> <count> [directory]")
        print("     jable_downloader.py <video_id> [directory]")
        sys.exit(1)
