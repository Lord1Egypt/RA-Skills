#!/usr/bin/env python3
"""
生成字幕下载脚本 (用于在 NAS 上直接运行)
"""

from smb.SMBConnection import SMBConnection
import os
import sys

# SMB 配置
SMB_CONFIG = {
    "username": "13917908083",
    "password": "Roger0808",
    "server_name": "Z4ProPlus-X6L8",
    "server_ip": "192.168.1.246",
    "share_name": "super8083",
    "remote_path": "qb/downloads"
}

def connect_smb():
    conn = SMBConnection(
        SMB_CONFIG["username"], SMB_CONFIG["password"],
        "openclaw-client", SMB_CONFIG["server_name"], use_ntlm_v2=True
    )
    if conn.connect(SMB_CONFIG["server_ip"], 445, timeout=10):
        return conn
    return None

def scan_videos(conn, subdir=""):
    """扫描视频文件"""
    path = f"{SMB_CONFIG['remote_path']}/{subdir}".strip("/")
    videos = []
    
    try:
        files = conn.listPath(SMB_CONFIG["share_name"], path)
        for f in files:
            if f.filename in ['.', '..', '.DS_Store']:
                continue
            
            relative_path = f"{subdir}/{f.filename}".strip("/") if subdir else f.filename
            full_path = f"{path}/{f.filename}".strip("/")
            
            if f.isDirectory:
                videos.extend(scan_videos(conn, relative_path))
            else:
                video_exts = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
                if any(f.filename.lower().endswith(ext) for ext in video_exts):
                    videos.append({
                        'filename': f.filename,
                        'relative_dir': subdir,
                        'full_dir': f"qb/downloads/{subdir}".strip("/")
                    })
    except Exception as e:
        print(f"⚠️  扫描失败 {path}: {e}")
    
    return videos

def generate_script(videos, output_file="download_subtitles.sh"):
    """生成字幕下载脚本"""
    
    script_lines = [
        "#!/bin/bash",
        "# 自动生成的字幕下载脚本",
        "# 用法: 将此脚本复制到 NAS 上运行",
        "",
        "# 配置下载路径",
        f'DOWNLOAD_PATH="/path/to/qb/downloads"',
        "",
        "# 检查 subliminal 是否安装",
        'if ! command -v subliminal \u0026\u003e /dev/null; then',
        '    echo "正在安装 subliminal..."',
        '    pip3 install subliminal',
        "fi",
        "",
        "# 切换到下载目录",
        'cd "$DOWNLOAD_PATH" || exit 1',
        "",
        "# 字幕下载统计",
        "TOTAL=0",
        "SUCCESS=0",
        "FAILED=0",
        "",
        "echo '========================================'",
        "echo '🎥 开始下载字幕'",
        "echo '========================================'",
        ""
    ]
    
    for video in videos:
        full_dir = video['full_dir']
        filename = video['filename']
        
        script_lines.extend([
            f"",
            f"# {filename}",
            f'TOTAL=$((TOTAL + 1))',
            f'echo "[$TOTAL/{len(videos)}] {filename}"',
            f'if [ -f "{full_dir}/{filename}" ]; then',
            f'    if subliminal download -l zh -l en "{full_dir}/{filename}" 2\u003e/dev/null; then',
            f'        SUCCESS=$((SUCCESS + 1))',
            f'        echo "  ✅ 成功"',
            f'    else',
            f'        FAILED=$((FAILED + 1))',
            f'        echo "  ❌ 失败"',
            f'    fi',
            f'else',
            f'    echo "  ⚠️  文件不存在"',
            f'fi'
        ])
    
    script_lines.extend([
        "",
        "echo ''",
        "echo '========================================'",
        "echo '📊 下载完成!'",
        "echo \"    总计: \$TOTAL\"",
        "echo \"    成功: \$SUCCESS\"",
        "echo \"    失败: \$FAILED\"",
        "echo '========================================'"
    ])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script_lines))
    
    # 添加执行权限
    os.chmod(output_file, 0o755)
    
    return output_file

def main():
    print("="*60)
    print("📝 字幕下载脚本生成器")
    print("="*60)
    
    print("\\n🔌 连接 SMB...")
    conn = connect_smb()
    if not conn:
        print("❌ SMB 连接失败")
        return 1
    
    print("✅ SMB 连接成功\\n")
    
    print("🔍 扫描视频文件...")
    videos = scan_videos(conn)
    conn.close()
    
    print(f"✅ 找到 {len(videos)} 个视频\\n")
    
    if not videos:
        print("❌ 没有找到视频")
        return 1
    
    # 生成脚本
    output_file = "/home/roger/.openclaw/workspace/download_subtitles.sh"
    script_path = generate_script(videos, output_file)
    
    print(f"📄 脚本已生成: {script_path}")
    print(f"\\n📋 使用方法:")
    print(f"   1. 将脚本复制到你的 NAS (例如通过 SMB)")
    print(f"   2. SSH 登录到 NAS")
    print(f"   3. 修改脚本中的 DOWNLOAD_PATH 路径")
    print(f"   4. 运行: bash download_subtitles.sh")
    print(f"\\n💡 或者直接在 Mac 上运行:")
    print(f"   cd /Volumes/super8083/qb/downloads")
    print(f"   # 然后为每个视频运行:")
    print(f"   subliminal download -l zh -l en '视频文件名.mkv'")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
