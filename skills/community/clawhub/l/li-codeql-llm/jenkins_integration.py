#!/usr/bin/env python3
"""
Jenkins 集成模块
Jenkins Integration Module

支持:
- 触发 Jenkins 任务
- 上传 SARIF 结果
- 获取构建状态
- 下载扫描报告
"""

import os
import base64
import requests
from typing import Optional, Dict
from pathlib import Path


class JenkinsClient:
    """Jenkins API 客户端"""
    
    def __init__(self, url: str, username: str, token: str):
        """
        初始化 Jenkins 客户端
        
        Args:
            url: Jenkins 服务器 URL
            username: Jenkins 用户名
            token: Jenkins API Token
        """
        self.url = url.rstrip('/')
        self.username = username
        self.token = token
        self.session = requests.Session()
        self.session.auth = (username, token)
    
    def test_connection(self) -> bool:
        """测试 Jenkins 连接"""
        try:
            response = self.session.get(f"{self.url}/api/json", timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Jenkins 连接失败 / Connection failed: {e}")
            return False
    
    def get_job_info(self, job_name: str) -> Optional[Dict]:
        """获取任务信息"""
        try:
            response = self.session.get(
                f"{self.url}/job/{job_name}/api/json",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ 获取任务信息失败 / Get job info failed: {e}")
            return None
    
    def trigger_build(self, job_name: str, parameters: Dict = None) -> Optional[int]:
        """
        触发构建
        
        Args:
            job_name: 任务名称
            parameters: 构建参数
        
        Returns:
            构建队列 ID，失败返回 None
        """
        url = f"{self.url}/job/{job_name}/build"
        
        if parameters:
            url += "WithParameters"
            data = parameters
        else:
            data = {}
        
        try:
            response = self.session.post(url, data=data, timeout=30)
            
            if response.status_code in [200, 201]:
                # 从响应头获取队列 ID
                queue_id = response.headers.get('X-Jenkins-Queue-Id')
                print(f"✅ 构建已触发 / Build triggered, Queue ID: {queue_id}")
                return int(queue_id) if queue_id else None
            else:
                print(f"❌ 触发构建失败 / Trigger build failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 异常 / Exception: {e}")
            return None
    
    def upload_sarif(self, job_name: str, sarif_file: str, build_number: str = None) -> bool:
        """
        上传 SARIF 文件到 Jenkins
        
        Args:
            job_name: 任务名称
            sarif_file: SARIF 文件路径
            build_number: 构建号（可选）
        
        Returns:
            bool: 是否成功
        """
        sarif_path = Path(sarif_file)
        
        if not sarif_path.exists():
            print(f"❌ SARIF 文件不存在 / SARIF file not found: {sarif_file}")
            return False
        
        # 读取 SARIF 文件
        with open(sarif_path, 'rb') as f:
            sarif_content = f.read()
        
        # 构建 API URL
        if build_number:
            url = f"{self.url}/job/{job_name}/{build_number}/artifact/"
        else:
            url = f"{self.url}/job/{job_name}/lastBuild/artifact/"
        
        # 使用 curl 上传（更可靠）
        import subprocess
        
        curl_cmd = [
            'curl', '-u', f'{self.username}:{self.token}',
            '-F', f'file=@{sarif_path}',
            '-F', 'relativePath=codeql-results.sarif',
            url
        ]
        
        try:
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✅ SARIF 已上传 / SARIF uploaded: {sarif_file}")
                return True
            else:
                print(f"❌ 上传失败 / Upload failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 异常 / Exception: {e}")
            return False
    
    def get_build_status(self, job_name: str, build_number: str) -> Optional[Dict]:
        """获取构建状态"""
        try:
            response = self.session.get(
                f"{self.url}/job/{job_name}/{build_number}/api/json",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'number': data.get('number'),
                    'result': data.get('result'),
                    'status': data.get('building', False),
                    'duration': data.get('duration'),
                    'timestamp': data.get('timestamp')
                }
            return None
        except Exception as e:
            print(f"❌ 获取构建状态失败 / Get build status failed: {e}")
            return None
    
    def get_build_artifacts(self, job_name: str, build_number: str) -> list:
        """获取构建产物列表"""
        try:
            response = self.session.get(
                f"{self.url}/job/{job_name}/{build_number}/api/json",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('artifacts', [])
            return []
        except Exception as e:
            print(f"❌ 获取构建产物失败 / Get artifacts failed: {e}")
            return []
    
    def download_artifact(self, job_name: str, build_number: str, 
                         artifact_path: str, output_path: str) -> bool:
        """下载构建产物"""
        try:
            url = f"{self.url}/job/{job_name}/{build_number}/artifact/{artifact_path}"
            response = self.session.get(url, timeout=60, stream=True)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ 产物已下载 / Artifact downloaded: {output_path}")
                return True
            else:
                print(f"❌ 下载失败 / Download failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 异常 / Exception: {e}")
            return False


def create_jenkins_client_from_config(config) -> Optional[JenkinsClient]:
    """从配置创建 Jenkins 客户端"""
    url = config.get('JENKINS_URL', 'http://localhost:8080')
    username = config.get('JENKINS_USER', 'devops')
    token = config.get('JENKINS_TOKEN', '')
    
    if not token or token == 'your-jenkins-token-here':
        print("⚠️  Jenkins Token 未配置 / Jenkins Token not configured")
        print("💡 请在 .env 文件中设置 JENKINS_TOKEN")
        return None
    
    return JenkinsClient(url, username, token)


if __name__ == '__main__':
    # 测试 Jenkins 连接
    import sys
    from config_loader import get_config
    
    config = get_config()
    
    print("🔍 测试 Jenkins 连接 / Testing Jenkins connection...")
    
    client = create_jenkins_client_from_config(config)
    
    if client:
        if client.test_connection():
            print("✅ Jenkins 连接成功 / Jenkins connection successful")
            
            # 获取任务信息
            job_name = config.get('JENKINS_JOB_NAME', 'codeql-security-scan')
            job_info = client.get_job_info(job_name)
            
            if job_info:
                print(f"\n📋 任务信息 / Job Info:")
                print(f"   名称 / Name: {job_info.get('name')}")
                print(f"   颜色 / Color: {job_info.get('color')}")
                print(f"   可构建 / Buildable: {job_info.get('buildable')}")
                
                last_build = job_info.get('lastBuild', {})
                if last_build:
                    print(f"\n   最后构建 / Last Build:")
                    print(f"      构建号 / Number: {last_build.get('number')}")
                    print(f"      结果 / Result: {last_build.get('result')}")
            else:
                print(f"⚠️  任务不存在 / Job not found: {job_name}")
        else:
            print("❌ Jenkins 连接失败 / Jenkins connection failed")
            print("\n请检查配置:")
            print(f"   URL: {config.get('JENKINS_URL')}")
            print(f"   用户 / User: {config.get('JENKINS_USER')}")
            sys.exit(1)
    else:
        print("❌ 无法创建 Jenkins 客户端 / Cannot create Jenkins client")
        sys.exit(1)
