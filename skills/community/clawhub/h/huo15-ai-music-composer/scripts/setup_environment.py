#!/usr/bin/env python3
"""
AI 音乐创技能环境设置脚本
安装依赖、检查 GPU、验证服务

作者：聚星逸 AI 团队
版本：v1.0.0 (2026.07)
"""

import os
import sys
import json
import subprocess
import platform
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class EnvironmentSetup:
    """环境设置类"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.gpu_info = None
        self.docker_info = None
        
    def _get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'cpu_count': os.cpu_count()
        }
    
    def check_gpu(self) -> Dict:
        """检查 GPU 可用性"""
        gpu_info = {
            'available': False,
            'devices': [],
            'cuda_version': None,
            'recommended': False
        }
        
        try:
            # 检查 nvidia-smi
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,compute_cap', '--format=csv,noheader'],
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                gpu_info['available'] = True
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        name, memory, compute_cap = [x.strip() for x in line.split(',')]
                        gpu_info['devices'].append({
                            'name': name,
                            'memory': memory,
                            'compute_capability': compute_cap,
                            'memory_gb': self._parse_memory(memory)
                        })
                        
                # 检查是否满足推荐配置（至少 18GB 显存）
                gpu_info['recommended'] = any(
                    device['memory_gb'] >= 18 for device in gpu_info['devices']
                )
                
            # 检查 CUDA 版本
            try:
                cuda_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
                if cuda_result.returncode == 0:
                    for line in cuda_result.stdout.split('\n'):
                        if 'release' in line.lower():
                            gpu_info['cuda_version'] = line.strip()
                            break
            except FileNotFoundError:
                pass
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        self.gpu_info = gpu_info
        return gpu_info
    
    def _parse_memory(self, memory_str: str) -> float:
        """解析显存字符串"""
        try:
            if 'MiB' in memory_str:
                return float(memory_str.replace(' MiB', '')) / 1024
            elif 'GiB' in memory_str:
                return float(memory_str.replace(' GiB', ''))
            else:
                return 0
        except:
            return 0
    
    def check_docker(self) -> Dict:
        """检查 Docker 可用性"""
        docker_info = {
            'available': False,
            'version': None,
            'compose_version': None,
            'running_containers': []
        }
        
        try:
            # 检查 Docker
            result = subprocess.run(['docker', 'version', '--format', 'json'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                docker_info['available'] = True
                version_data = json.loads(result.stdout)
                docker_info['version'] = version_data.get('Client', {}).get('Version')
            
            # 检查 Docker Compose
            try:
                compose_result = subprocess.run(['docker-compose', '--version'], 
                                              capture_output=True, text=True)
                if compose_result.returncode == 0:
                    docker_info['compose_version'] = compose_result.stdout.strip()
            except FileNotFoundError:
                # 尝试新版 Docker Compose 插件
                try:
                    compose_result = subprocess.run(['docker', 'compose', 'version'], 
                                                  capture_output=True, text=True)
                    if compose_result.returncode == 0:
                        docker_info['compose_version'] = compose_result.stdout.strip()
                except FileNotFoundError:
                    pass
            
            # 检查运行中的容器
            try:
                ps_result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                                         capture_output=True, text=True)
                if ps_result.returncode == 0:
                    # 解析 JSON 格式的容器列表
                    containers = []
                    for line in ps_result.stdout.strip().split('\n'):
                        if line.strip():
                            try:
                                container = json.loads(line)
                                containers.append({
                                    'id': container.get('ID'),
                                    'name': container.get('Names'),
                                    'image': container.get('Image'),
                                    'status': container.get('Status')
                                })
                            except json.JSONDecodeError:
                                pass
                    docker_info['running_containers'] = containers
                    
            except:
                pass
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        self.docker_info = docker_info
        return docker_info
    
    def check_python_packages(self) -> Dict[str, bool]:
        """检查 Python 包"""
        required_packages = {
            'torch': 'torch',
            'torchaudio': 'torchaudio', 
            'numpy': 'numpy',
            'scipy': 'scipy',
            'aiohttp': 'aiohttp',
            'redis': 'redis',
            'aiofiles': 'aiofiles',
            'jwt': 'PyJWT',
            'bcrypt': 'bcrypt'
        }
        
        available_packages = {}
        
        for package, import_name in required_packages.items():
            try:
                __import__(import_name)
                available_packages[package] = True
            except ImportError:
                available_packages[package] = False
                
        return available_packages
    
    def install_requirements(self, requirements_file: str = None) -> bool:
        """安装依赖包"""
        if not requirements_file:
            requirements_content = '''
torch>=2.0.0
torchaudio>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
aiohttp[speedups]>=3.8.0
redis>=4.5.0
aiofiles>=23.0.0
PyJWT>=2.6.0
bcrypt>=4.0.0
tqdm>=4.65.0
pydub>=0.25.1
librosa>=0.10.0
soundfile>=0.12.0
ffmpeg-python>=0.2.0
'''
            
            with open('requirements.txt', 'w') as f:
                f.write(requirements_content)
            requirements_file = 'requirements.txt'
        
        try:
            print("📦 安装 Python 依赖...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', requirements_file,
                '--no-cache-dir', '--upgrade'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 依赖安装成功")
                return True
            else:
                print(f"❌ 依赖安装失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 安装过程中出错: {e}")
            return False
    
    def generate_docker_compose(self, output_path: str = 'docker-compose.yml'):
        """生成 Docker Compose 配置文件"""
        compose_config = '''
version: '3.8'

services:
  redis-cache:
    image: redis:7-alpine
    container_name: ai_music_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  minio-storage:
    image: minio/minio:latest
    container_name: ai_music_storage
    restart: unless-stopped
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    command: server /data --console-address ":9001"

  voice-clone-service:
    image: registry.huo15.com/ai-music/voice-clone:v4.1
    container_name: voice_clone
    runtime: nvidia
    restart: unless-stopped
    ports:
      - "8001:8001"
    volumes:
      - ${DATA_DIR:-./data}:/data
      - ${TEMP_DIR:-./temp}:/tmp
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - MODEL_CACHE_DIR=/data/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  music-gen-service:
    image: registry.huo15.com/ai-music/suno-engine:v4
    container_name: music_gen
    runtime: nvidia
    restart: unless-stopped
    ports:
      - "8002:8002"
    volumes:
      - ${DATA_DIR:-./data}:/data
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  lyrics-service:
    image: registry.huo15.com/ai-music/lyrics-gpt7:latest
    container_name: lyrics_ai
    restart: unless-stopped
    ports:
      - "8003:8003"
    volumes:
      - ${DATA_DIR:-./data}:/data
    deploy:
      resources:
        limits:
          memory: 32G

  audio-process-service:
    image: registry.huo15.com/ai-music/audio-process:v4
    container_name: audio_process
    restart: unless-stopped
    ports:
      - "8004:8004"
    volumes:
      - ${DATA_DIR:-./data}:/data

  api-server:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: ai_music_api
    restart: unless-stopped
    ports:
      - "8788:8788"
    volumes:
      - ${DATA_DIR:-./data}:/app/data
      - ${CONFIG_DIR:-./config}:/app/config
    environment:
      - REDIS_URL=redis://redis-cache:6379/0
      - DATA_DIR=/app/data
    depends_on:
      - redis-cache
      - minio-storage
      - voice-clone-service
      - music-gen-service
      - lyrics-service
      - audio-process-service

volumes:
  redis_data:
  minio_data:
'''

        with open(output_path, 'w') as f:
            f.write(compose_config)
        
        print(f"✅ Docker Compose 配置已保存到: {output_path}")
    
    def print_system_report(self):
        """打印系统检查报告"""
        print("\n" + "="*60)
        print("🎵 AI 音乐创作环境检查报告")
        print("="*60)
        
        # 系统信息
        print(f"\n🖥️  系统信息:")
        print(f"   平台: {self.system_info['platform']}")
        print(f"   版本: {self.system_info['platform_version']}")
        print(f"   Python: {self.system_info['python_version']}")
        print(f"   CPU 核心: {self.system_info['cpu_count']}")
        
        # GPU 信息
        if self.gpu_info:
            print(f"\n🎮 GPU 信息:")
            if self.gpu_info['available']:
                print(f"   ✅ GPU 可用: {len(self.gpu_info['devices'])} 设备")
                for i, device in enumerate(self.gpu_info['devices'], 1):
                    memory_str = f"{device['memory_gb']:.1f}GB" if device['memory_gb'] > 0 else "N/A"
                    print(f"     {i}. {device['name']} (显存: {memory_str})")
                
                if self.gpu_info['recommended']:
                    print(f"   ✅ 配置符合推荐要求 (≥18GB 显存)")
                else:
                    print(f"   ⚠️  建议升级到 18GB+ 显存 GPU")
                    
                if self.gpu_info['cuda_version']:
                    print(f"   CUDA 版本: {self.gpu_info['cuda_version']}")
            else:
                print(f"   ❌ 未检测到可用的 GPU")
                print(f"   💡 提示: 本技能需要 NVIDIA GPU 才能正常运行")
        
        # Docker 信息
        if self.docker_info:
            print(f"\n🐳 Docker 信息:")
            if self.docker_info['available']:
                print(f"   ✅ Docker 可用: {self.docker_info['version']}")
                if self.docker_info['compose_version']:
                    print(f"   ✅ Docker Compose: {self.docker_info['compose_version']}")
                else:
                    print(f"   ⚠️  未安装 Docker Compose")
                    
                if self.docker_info['running_containers']:
                    print(f"   运行中容器: {len(self.docker_info['running_containers'])}")
                else:
                    print(f"   当前无运行容器")
            else:
                print(f"   ❌ Docker 不可用")
                print(f"   💡 提示: 推荐使用 Docker 部署以获得最佳体验")
        
        print("\n" + "="*60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI 音乐创作环境设置')
    parser.add_argument('--check-only', action='store_true', 
                       help='仅检查环境，不安装依赖')
    parser.add_argument('--install', action='store_true',
                       help='安装依赖包')
    parser.add_argument('--generate-compose', action='store_true',
                       help='生成 Docker Compose 配置')
    parser.add_argument('--requirements', help='指定 requirements.txt 文件路径')
    parser.add_argument('--output-compose', default='docker-compose.yml',
                       help='Docker Compose 输出路径')
    
    args = parser.parse_args()
    
    setup = EnvironmentSetup()
    
    print("🔍 开始环境检查...")
    
    # 执行检查
    print("\n📋 检查 GPU...")
    gpu_result = setup.check_gpu()
    
    print("📋 检查 Docker...")
    docker_result = setup.check_docker()
    
    print("📋 检查 Python 包...")
    packages = setup.check_python_packages()
    missing_packages = [pkg for pkg, available in packages.items() if not available]
    
    # 打印报告
    setup.print_system_report()
    
    if missing_packages:
        print(f"\n📦 缺少依赖包: {', '.join(missing_packages)}")
        if args.install:
            success = setup.install_requirements(args.requirements)
            if not success:
                print("❌ 依赖安装失败，请检查错误信息")
                sys.exit(1)
        else:
            print("💡 使用 --install 安装依赖包")
    else:
        print("\n✅ 所有 Python 依赖已安装")
    
    if args.generate_compose:
        setup.generate_docker_compose(args.output_compose)
    
    # 总结建议
    print("\n💡 建议:")
    if not gpu_result['available']:
        print("- 需要 NVIDIA GPU 才能运行 AI 音乐生成模型")
    elif not gpu_result['recommended']:
        print("- 建议升级到 18GB+ 显存的 GPU (如 RTX 4090/3090)")
    
    if not docker_result['available']:
        print("- 推荐安装 Docker 以获得最佳部署体验")
    
    if not missing_packages:
        print("- 所有环境检查完毕，可以开始使用 AI 音乐创作技能！")
    
    print("\n📚 使用帮助:")
    print("  python setup_environment.py --install --generate-compose")
    print("  docker-compose up -d")
    print("  python scripts/ai_music_server.py")

def create_dockerfile():
    """创建 API 服务的 Dockerfile"""
    dockerfile_content = '''
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    libsndfile1 \\
    libgl1-mesa-glx \\
    && rm -rf /var/lib/apt/lists/*

# 复制 Python 依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY scripts/ ./scripts/
COPY config/ ./config/
COPY data/ ./data/

# 创建数据目录
RUN mkdir -p /app/data/uploads /app/data/outputs /tmp/ai_music

# 暴露端口
EXPOSE 8788

# 启动服务
CMD ["python", "scripts/ai_music_server.py"]
'''

    with open('Dockerfile.api', 'w') as f:
        f.write(dockerfile_content)
    
    print("✅ API 服务的 Dockerfile 已创建")

def create_sample_config():
    """创建示例配置文件"""
    config_content = {
        "services": {
            "voice_clone": "http://voice-clone-service:8001",
            "music_gen": "http://music-gen-service:8002",
            "lyrics_ai": "http://lyrics-service:8003",
            "audio_process": "http://audio-process-service:8004"
        },
        "redis_url": "redis://redis-cache:6379/0",
        "storage_url": "http://minio-storage:9000",
        "minio": {
            "access_key": "minioadmin",
            "secret_key": "minioadmin123",
            "bucket": "ai-music-files"
        },
        "max_concurrent_jobs": 4,
        "temp_dir": "/tmp/ai_music",
        "output_dir": "/app/data/outputs"
    }

    os.makedirs('config', exist_ok=True)
    with open('config/music_config.json', 'w') as f:
        json.dump(config_content, f, indent=2, ensure_ascii=False)
    
    print("✅ 示例配置文件已创建: config/music_config.json")

if __name__ == "__main__":
    main()
    
    # 创建额外的配置和 Docker 文件
    if len(sys.argv) == 1 or '--generate-compose' in sys.argv:
        create_dockerfile()
        create_sample_config()