#!/usr/bin/env python3
"""
HappyHorse 视频创作助手 - 核心功能模块 v1.1
阿里云百炼（DashScope）HappyHorse 视频生成
支持文生视频和图生视频两种模式

v1.1 (2026-04-28):
- 默认时长从 15 秒改为 10 秒
- 支持用户选择时长（10s/15s）

v1.0 (2026-04-28):
- 使用 DashScope API（阿里百炼）
- 支持图生视频（首帧/尾帧模式）
- 支持文生视频
- 异步任务轮询
"""

import requests
import json
import time
import os
from datetime import datetime

# 配置
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
VIDEO_ENDPOINT = f"{BASE_URL}/services/aigc/video-generation/video-synthesis"
TASK_ENDPOINT = f"{BASE_URL}/tasks"

# 临时目录
TEMP_DIR = "/root/.openclaw/workspace/happyhorse-video-temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# 默认 API Key
DEFAULT_API_KEY = "sk-d05aba5a2dae4453b97ed07fdb983e5a"


class HappyHorseCreator:
    """HappyHorse 视频生成器 v1.1"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or DEFAULT_API_KEY
        self.temp_dir = TEMP_DIR
        
    def create_video_task(self, prompt, duration=10, resolution="720P", ratio="16:9",
                         image_url=None, end_frame_url=None, model=None):
        """
        创建视频生成任务
        
        Args:
            prompt: 视频描述提示词
            duration: 时长（秒），10 或 15 秒，默认 10 秒
            resolution: 分辨率 480P/720P/1080P
            ratio: 比例 16:9/9:16/1:1
            image_url: 首帧图片 URL（图生视频模式，可选）
            end_frame_url: 尾帧图片 URL（首尾帧模式，可选）
            model: 模型 ID（默认 happyhorse-1.0-i2v 或 happyhorse-1.0-t2v）
            
        Returns:
            task_id: 任务 ID，失败返回 None
        """
        # 自动选择模型
        if model is None:
            model = "happyhorse-1.0-i2v" if image_url else "happyhorse-1.0-t2v"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-DashScope-Async": "enable"  # ⚠️ 必须设置异步模式
        }
        
        # 构建 input 参数
        input_data = {"prompt": prompt}
        
        # 如果有图片，添加到 media 数组
        if image_url:
            media = [{"type": "first_frame", "url": image_url}]
            if end_frame_url:
                media.append({"type": "last_frame", "url": end_frame_url})
            input_data["media"] = media
        
        payload = {
            "model": model,
            "input": input_data,
            "parameters": {
                "resolution": resolution,
                "ratio": ratio,
                "duration": duration
            }
        }
        
        mode = "图生视频" if image_url else "文生视频"
        if image_url and end_frame_url:
            mode = "图生视频（首尾帧）"
            
        print(f"🎬 创建{mode}视频任务...")
        print(f"   模型：{model}")
        print(f"   分辨率：{resolution} | 比例：{ratio} | 时长：{duration}秒")
        print(f"   提示词：{prompt[:50]}...")
        
        try:
            response = requests.post(VIDEO_ENDPOINT, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if "output" in result and "task_id" in result["output"]:
                    task_id = result["output"]["task_id"]
                    print(f"✅ 任务创建成功！Task ID: {task_id}")
                    return task_id
                else:
                    print(f"⚠️ 响应格式异常: {result}")
                    return None
            else:
                print(f"❌ 任务创建失败：{response.status_code}")
                print(f"   错误：{response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常：{e}")
            return None
    
    def get_task_status(self, task_id):
        """
        查询任务状态
        
        Args:
            task_id: 任务 ID
            
        Returns:
            (status, result): 状态和完整结果
        """
        url = f"{TASK_ENDPOINT}/{task_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if "output" in result:
                    status = result["output"].get("task_status", "unknown")
                    return status, result
                return "unknown", result
            else:
                return "error", {"error": response.text}
                
        except Exception as e:
            return "error", {"error": str(e)}
    
    def wait_for_completion(self, task_id, timeout=600, interval=10):
        """
        等待任务完成
        
        Args:
            task_id: 任务 ID
            timeout: 超时时间（秒）
            interval: 轮询间隔（秒）
            
        Returns:
            result: 完成结果，失败返回 None
        """
        print(f"⏳ 等待视频生成完成...")
        print(f"   🕐 预计等待 1-5 分钟，最长等待 {timeout} 秒")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status, result = self.get_task_status(task_id)
            
            elapsed = time.time() - start_time
            print(f"   [{int(elapsed)}s] 状态：{status}")
            
            if status == "SUCCEEDED":
                print(f"✅ 视频生成完成！")
                return result
            elif status == "FAILED":
                error_code = result.get("output", {}).get("code", "未知错误")
                error_message = result.get("output", {}).get("message", "")
                print(f"❌ 视频生成失败：{error_code} - {error_message}")
                return None
            elif status == "PENDING":
                print(f"   任务排队中...")
            elif status == "RUNNING":
                print(f"   视频生成中...")
            
            time.sleep(interval)
        
        print(f"⏰ 等待超时（{timeout}s）")
        return None
    
    def extract_video_url(self, result):
        """从结果中提取视频 URL"""
        if "output" in result:
            return result["output"].get("video_url")
        return None
    
    def download_video(self, video_url, output_path=None):
        """
        下载生成的视频
        
        Args:
            video_url: 视频 URL
            output_path: 保存路径（默认自动生成）
            
        Returns:
            file_path: 下载的文件路径
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{self.temp_dir}/video_{timestamp}.mp4"
        
        print(f"📥 下载视频到：{output_path}")
        
        try:
            response = requests.get(video_url, stream=True, timeout=120)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ 视频下载成功！")
                
                # 显示文件大小
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小：{size_mb:.2f} MB")
                
                return output_path
            else:
                print(f"❌ 视频下载失败：{response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 下载异常：{e}")
            return None
    
    def generate_video(self, prompt, duration=10, resolution="720P", ratio="16:9",
                      image_url=None, end_frame_url=None, model=None, output_path=None):
        """
        生成视频（完整流程）
        
        Args:
            prompt: 视频描述提示词
            duration: 时长（秒），10 或 15 秒，默认 10 秒
            resolution: 分辨率
            ratio: 比例
            image_url: 首帧图片 URL（图生视频模式，可选）
            end_frame_url: 尾帧图片 URL（首尾帧模式，可选）
            model: 模型 ID（可选）
            output_path: 输出路径（可选）
            
        Returns:
            (success, video_path): 是否成功和视频路径
        """
        if image_url and end_frame_url:
            mode = "图生视频（首尾帧）"
        elif image_url:
            mode = "图生视频（首帧）"
        else:
            mode = "文生视频"
            
        print(f"\n🎬 {mode}: {prompt[:50]}...")
        
        # 创建任务
        task_id = self.create_video_task(
            prompt, duration, resolution, ratio,
            image_url=image_url,
            end_frame_url=end_frame_url,
            model=model
        )
        if not task_id:
            return False, None
        
        # 等待完成
        result = self.wait_for_completion(task_id)
        if not result:
            return False, None
        
        # 提取 URL
        video_url = self.extract_video_url(result)
        if not video_url:
            print("❌ 未找到视频 URL")
            print(f"   响应内容：{json.dumps(result, indent=2, ensure_ascii=False)}")
            return False, None
        
        print(f"   📹 视频 URL：{video_url}")
        
        # 下载视频
        downloaded_path = self.download_video(video_url, output_path)
        if downloaded_path:
            return True, downloaded_path
        else:
            return False, None


def main():
    """测试函数"""
    creator = HappyHorseCreator()
    
    # 测试图生视频
    prompt = "镜头缓缓推进，阳光洒在咖啡杯上，蒸汽袅袅升起，温馨咖啡馆氛围"
    
    success, video_path = creator.generate_video(
        prompt=prompt,
        image_url="http://43.167.197.36/img2.jpg",
        duration=10
    )
    
    if success:
        print(f"\n🎉 视频生成成功！")
        print(f"   路径：{video_path}")
    else:
        print(f"\n❌ 视频生成失败")


if __name__ == "__main__":
    main()
