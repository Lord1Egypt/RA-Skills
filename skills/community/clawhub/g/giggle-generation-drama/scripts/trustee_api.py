#!/usr/bin/env python3
"""
托管模式V2 API调用脚本
支持创建项目、提交任务、查询进度和支付功能
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

# 延迟导入requests，只在需要时导入
def _check_requests():
    """检查并导入requests库"""
    try:
        import requests
        return requests
    except ImportError:
        print("错误: 需要安装 requests 库", file=sys.stderr)
        print("请运行: pip install requests", file=sys.stderr)
        sys.exit(1)


class TrusteeModeAPI:
    """托管模式V2 API客户端"""
    
    def __init__(self):
        """
        初始化API客户端
        """
        requests = _check_requests()  # 延迟导入
        self.api_key = os.getenv("GIGGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "未找到 GIGGLE_API_KEY，请设置系统环境变量：\n"
                "export GIGGLE_API_KEY=your_api_key\n"
                "API Key 可在 [Giggle.pro](https://giggle.pro/) 账号设置中获取。"
            )
        self.base_url = "https://giggle.pro"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-auth': self.api_key
        })

    def _create_project(self, name: str, project_type: str, aspect: str, mode: str = "trustee") -> Dict[str, Any]:
        """
        创建项目（仅供内部调用，不对外暴露 CLI）
        
        Args:
            name: 项目名称
            project_type: 项目类型 (director/narration/short-film)
            aspect: 视频宽高比 (16:9/9:16)
            mode: 项目模式 (trustee)
        
        Returns:
            API响应数据
        """
        url = f"{self.base_url}/api/v1/project/create"
        data = {
            "name": name,
            "type": project_type,
            "aspect": aspect,
            "mode": mode
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            # 兼容不同的响应格式：code可能是字符串"200"或数字200
            code = result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            
            if code != 0 and code != 200:
                print(f"创建项目失败: {result.get('msg', '未知错误')}")
                return result
            
            return result
        except Exception as e:
            print(f"请求失败: {e}")
            return {"code": -1, "msg": str(e)}
    
    def _create_and_submit(self, project_name: str, project_type: str, diy_story: str,
                           aspect: str, video_duration: str, language: str,
                           style_id: Optional[int] = None,
                           character_info: Optional[list] = None) -> Dict[str, Any]:
        """
        创建项目并提交任务（合并为一步，仅供内部调用）
        character_info: [{"name": "角色名", "url": "图片URL"}, ...]
        返回 project_id 或错误信息
        """
        url_create = f"{self.base_url}/api/v1/project/create"
        data_create = {
            "name": project_name,
            "type": project_type,
            "aspect": aspect,
            "mode": "trustee"
        }

        try:
            response = self.session.post(url_create, json=data_create)
            response.raise_for_status()
            create_result = response.json()

            code = create_result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0

            if code != 0 and code != 200:
                return {
                    "code": code,
                    "msg": f"创建项目失败: {create_result.get('msg', '未知错误')}",
                    "data": None
                }

            project_id = create_result.get("data", {}).get("project_id")
            if not project_id:
                return {
                    "code": -1,
                    "msg": "创建项目失败: 未获取到项目ID",
                    "data": None
                }

            url_submit = f"{self.base_url}/api/v1/trustee_mode/submit-v2"
            data_submit = {
                "project_id": project_id,
                "diy_story": diy_story,
                "aspect": aspect,
                "video_duration": video_duration,
                "language": language
            }
            if style_id is not None:
                data_submit["style_id"] = style_id
            if character_info is not None and len(character_info) > 0:
                data_submit["character_info"] = character_info

            response = self.session.post(url_submit, json=data_submit)
            response.raise_for_status()
            submit_result = response.json()

            code = submit_result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0

            if code != 0 and code != 200:
                return {
                    "code": code,
                    "msg": f"提交任务失败: {submit_result.get('msg', '未知错误')}",
                    "data": None
                }

            return {"code": 200, "msg": "success", "data": {"project_id": project_id}}
        except Exception as e:
            return {"code": -1, "msg": str(e), "data": None}

    def submit_task(self, project_id: str, diy_story: str, aspect: str,
                   video_duration: str, language: str, style_id: Optional[int] = None) -> Dict[str, Any]:
        """
        提交任务
        
        Args:
            project_id: 项目ID
            diy_story: 自定义故事内容
            aspect: 视频宽高比 (16:9/9:16)
            video_duration: 视频时长 (auto/30/60/120/180/240/300)
            language: 语言 (zh/en)
            style_id: 风格ID（可选，如果不提供则不传此参数）
        
        Returns:
            API响应数据
        """
        url = f"{self.base_url}/api/v1/trustee_mode/submit-v2"
        data = {
            "project_id": project_id,
            "diy_story": diy_story,
            "aspect": aspect,
            "video_duration": video_duration,
            "language": language
        }
        
        # 只有当提供了style_id时才添加到请求中
        if style_id is not None:
            data["style_id"] = style_id
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            # 兼容不同的响应格式：code可能是字符串"200"或数字200
            code = result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            
            if code != 0 and code != 200:
                print(f"提交任务失败: {result.get('msg', '未知错误')}")
                return result
            
            return result
        except Exception as e:
            print(f"请求失败: {e}")
            return {"code": -1, "msg": str(e)}
    
    def query_progress(self, project_id: str) -> Dict[str, Any]:
        """
        查询任务进度
        
        Args:
            project_id: 项目ID
        
        Returns:
            API响应数据
        """
        url = f"{self.base_url}/api/v1/trustee_mode/query-v2"
        params = {"project_id": project_id}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            # 兼容不同的响应格式：code可能是字符串"200"或数字200
            code = result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            
            if code != 0 and code != 200:
                print(f"查询失败: {result.get('msg', '未知错误')}")
                return result
            
            return result
        except Exception as e:
            print(f"请求失败: {e}")
            return {"code": -1, "msg": str(e)}
    
    def pay(self, project_id: str, video_first_model: str, 
           video_second_model: str, image_first_model: str) -> Dict[str, Any]:
        """
        支付
        
        Args:
            project_id: 项目ID
            video_first_model: 视频首选模型
            video_second_model: 视频备选模型
            image_first_model: 图片首选模型
        
        Returns:
            API响应数据
        """
        url = f"{self.base_url}/api/v1/trustee_mode/pay"
        data = {
            "project_id": project_id,
            "video_first_model": video_first_model,
            "video_second_model": video_second_model,
            "image_first_model": image_first_model
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            # 兼容不同的响应格式：code可能是字符串"200"或数字200
            code = result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            
            if code != 0 and code != 200:
                print(f"支付失败: {result.get('msg', '未知错误')}")
                return result
            
            return result
        except Exception as e:
            print(f"请求失败: {e}")
            return {"code": -1, "msg": str(e)}
    
    def get_styles(self, page: int = 1, page_size: int = 999, language: str = "zh") -> Dict[str, Any]:
        """
        获取风格列表
        
        Args:
            page: 页码（默认1）
            page_size: 每页数量（默认999）
            language: 语言（默认zh，可选zh/en）
        
        Returns:
            API响应数据
        """
        url = f"{self.base_url}/api/v1/ai_style/list"
        params = {
            "page": page,
            "page_size": page_size,
            "language": language
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            # 兼容不同的响应格式
            code = result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            
            if code != 0 and code != 200:
                print(f"获取风格列表失败: {result.get('msg', '未知错误')}")
                return result
            
            return result
        except Exception as e:
            print(f"请求失败: {e}")
            return {"code": -1, "msg": str(e)}
    
    def execute_workflow(self, diy_story: str, aspect: str, project_name: str,
                        video_duration: str = "auto", style_id: Optional[int] = None,
                        project_type: str = "director",
                        character_info: Optional[list] = None,
                        video_first_model: str = "grok",
                        video_second_model: str = "seedance15-pro",
                        image_first_model: str = "seedream45") -> Dict[str, Any]:
        """
        执行完整工作流（一步完成：创建项目+提交任务 -> 查询进度 -> 支付 -> 等待完成）
        
        Args:
            diy_story: 故事创意内容
            aspect: 视频宽高比 (16:9/9:16)
            project_name: 项目名称
            video_duration: 视频时长 (auto/30/60/120/180/240/300)，默认为"auto"
            style_id: 风格ID（可选）
            project_type: 项目类型 (director/narration/short-film)，默认为"director"（短剧模式）
            character_info: 角色图片（可选），格式: [{"name": "角色名", "url": "图片URL"}, ...]
        
        Returns:
            包含下载链接的响应数据，或失败信息
        """
        start_time = datetime.now()
        timeout = timedelta(hours=1)  # 固定超时时间为1小时
        query_interval = 3  # 固定查询间隔为3秒
        language = "zh"  # 固定语言为中文
        
        # 步骤1：创建项目并提交任务（合并为一步）
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 步骤1: 创建项目并提交任务...", file=sys.stderr)
        create_submit_result = self._create_and_submit(
            project_name=project_name,
            project_type=project_type,
            diy_story=diy_story,
            aspect=aspect,
            video_duration=video_duration,
            language=language,
            style_id=style_id,
            character_info=character_info
        )

        code = create_submit_result.get("code")
        if isinstance(code, str):
            code = int(code) if code.isdigit() else 0
        if code != 0 and code != 200:
            return {
                "code": code if code else -1,
                "msg": create_submit_result.get("msg", "创建或提交失败"),
                "data": None
            }

        project_id = create_submit_result.get("data", {}).get("project_id")
        if not project_id:
            return {"code": -1, "msg": "未获取到项目ID", "data": None}

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 项目创建并任务提交成功，项目ID: {project_id}", file=sys.stderr)

        # 步骤2：循环查询进度
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 步骤2: 开始查询进度...", file=sys.stderr)
        
        paid = False  # 标记是否已支付，避免重复支付
        max_retries = 5  # 最大重试次数
        retry_delay = 5  # 重试延迟（秒）
        
        while True:
            # 检查超时
            if datetime.now() - start_time > timeout:
                return {
                    "code": -1,
                    "msg": "工作流超时（超过1小时）",
                    "data": None
                }
            
            # 查询进度（带重试机制）
            query_result = None
            query_success = False
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    query_result = self.query_progress(project_id)
                    code = query_result.get("code")
                    if isinstance(code, str):
                        code = int(code) if code.isdigit() else 0
                    
                    # 如果查询成功（code为0或200），跳出重试循环
                    if code == 0 or code == 200:
                        query_success = True
                        break
                    
                    # 检查错误信息，判断是否为网络错误
                    error_msg = query_result.get("msg", "")
                    error_str = str(error_msg)
                    
                    # 判断是否为网络错误
                    is_network_error = (
                        "Connection" in error_str or 
                        "Remote" in error_str or 
                        "timeout" in error_str.lower() or
                        "aborted" in error_str.lower() or
                        "disconnected" in error_str.lower()
                    )
                    
                    # 如果是业务错误（非网络错误），直接返回
                    if not is_network_error:
                        return {
                            "code": code,
                            "msg": f"查询进度失败: {error_msg}",
                            "data": None
                        }
                    
                    # 网络错误，继续重试
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 网络错误，{retry_delay}秒后重试 ({retry_count}/{max_retries}): {error_msg}", file=sys.stderr)
                        time.sleep(retry_delay)
                    else:
                        # 达到最大重试次数，但不退出，等待后继续下一次循环
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 网络错误，已达到最大重试次数，等待{query_interval}秒后继续查询...", file=sys.stderr)
                        time.sleep(query_interval)
                        break
                        
                except Exception as e:
                    # 捕获异常，判断是否为网络错误
                    error_str = str(e)
                    is_network_error = (
                        "Connection" in error_str or 
                        "Remote" in error_str or 
                        "timeout" in error_str.lower() or
                        "aborted" in error_str.lower() or
                        "disconnected" in error_str.lower()
                    )
                    
                    if is_network_error:
                        retry_count += 1
                        if retry_count < max_retries:
                            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 网络异常，{retry_delay}秒后重试 ({retry_count}/{max_retries}): {error_str}", file=sys.stderr)
                            time.sleep(retry_delay)
                        else:
                            # 达到最大重试次数，但不退出，等待后继续下一次循环
                            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 网络异常，已达到最大重试次数，等待{query_interval}秒后继续查询...", file=sys.stderr)
                            time.sleep(query_interval)
                            break
                    else:
                        # 非网络错误，直接返回
                        return {
                            "code": -1,
                            "msg": f"查询进度失败: {error_str}",
                            "data": None
                        }
            
            # 如果查询失败（网络错误且重试后仍失败），继续下一次循环
            if not query_success:
                continue
            
            # 查询成功，继续处理
            code = query_result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            
            data = query_result.get("data", {})
            status = data.get("status", "unknown")
            current_step = data.get("current_step", "")
            pay_status = data.get("pay_status", "")
            err_msg = data.get("err_msg", "")
            
            # 检查是否有错误
            if status == "failed" or err_msg:
                return {
                    "code": -1,
                    "msg": f"任务失败: {err_msg or '未知错误'}",
                    "data": None
                }
            
            # 检查子步骤是否有失败
            steps = data.get("steps", [])
            for step in steps:
                sub_steps = step.get("sub_steps", [])
                for sub_step in sub_steps:
                    sub_status = sub_step.get("status", "")
                    sub_error = sub_step.get("error", "")
                    if sub_status == "failed" or sub_error:
                        return {
                            "code": -1,
                            "msg": f"子步骤失败: {sub_step.get('step', '未知步骤')} - {sub_error or '未知错误'}",
                            "data": None
                        }
            
            # 检查是否需要支付（只在未支付且状态为待支付时执行）
            if not paid and (pay_status == "pending" or (current_step and "pay" in current_step.lower())):
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 检测到待支付状态，执行支付...", file=sys.stderr)
                pay_result = self.pay(
                    project_id=project_id,
                    video_first_model=video_first_model,
                    video_second_model=video_second_model,
                    image_first_model=image_first_model
                )
                
                code = pay_result.get("code")
                if isinstance(code, str):
                    code = int(code) if code.isdigit() else 0
                
                if code != 0 and code != 200:
                    return {
                        "code": code,
                        "msg": f"支付失败: {pay_result.get('msg', '未知错误')}",
                        "data": None
                    }
                
                paid = True  # 标记已支付
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 支付成功，继续查询进度...", file=sys.stderr)
                # 支付后立即再次查询进度
                continue
            
            # 检查是否完成
            if status == "completed":
                video_asset = data.get("video_asset", {})
                download_url = video_asset.get("download_url") if video_asset else None
                
                if video_asset and download_url:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任务完成！视频下载链接: {download_url}", file=sys.stderr)
                    return {
                        "code": 200,
                        "msg": "success",
                        "uuid": query_result.get("uuid", ""),
                        "data": {
                            "project_id": project_id,
                            "download_url": download_url,
                            "video_asset": video_asset,
                            "status": status
                        }
                    }
                else:
                    # 已完成但还没有下载链接，继续等待
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任务状态为完成，但尚未生成下载链接，继续等待...", file=sys.stderr)
            
            # 输出当前状态
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 当前状态: {status}, 当前步骤: {current_step}, 支付状态: {pay_status}", file=sys.stderr)
            
            # 等待后继续查询
            time.sleep(query_interval)


def print_response(result: Dict[str, Any], pretty: bool = True):
    """打印响应结果"""
    if pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="托管模式V2 API调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='美化JSON输出'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 提交任务命令
    submit_parser = subparsers.add_parser('submit', help='提交任务')
    submit_parser.add_argument('--project-id', required=True, help='项目ID')
    submit_parser.add_argument('--story', required=True, dest='diy_story', help='自定义故事内容')
    submit_parser.add_argument('--aspect', required=True, choices=['16:9', '9:16'],
                               help='视频宽高比: 16:9 或 9:16')
    submit_parser.add_argument('--style-id', type=int, help='风格ID（可选，建议先使用 styles 命令查询可用风格）')
    submit_parser.add_argument('--duration', required=True, dest='video_duration',
                              choices=['auto', '30', '60', '120', '180', '240', '300'],
                              help='视频时长: auto/30/60/120/180/240/300')
    submit_parser.add_argument('--language', required=True, choices=['zh', 'en'], help='语言: zh 或 en')
    
    # 查询进度命令
    query_parser = subparsers.add_parser('query', help='查询任务进度')
    query_parser.add_argument('--project-id', required=True, help='项目ID')
    query_parser.add_argument('--poll', action='store_true', help='轮询查询直到完成')
    query_parser.add_argument('--interval', type=int, default=3, help='轮询间隔（秒，默认3秒）')
    
    # 支付命令
    pay_parser = subparsers.add_parser('pay', help='支付')
    pay_parser.add_argument('--project-id', required=True, help='项目ID')
    pay_parser.add_argument('--video-first-model', required=True, help='视频首选模型')
    pay_parser.add_argument('--video-second-model', required=True, help='视频备选模型')
    pay_parser.add_argument('--image-first-model', required=True, help='图片首选模型')
    
    # 获取风格列表命令
    styles_parser = subparsers.add_parser('styles', help='获取风格列表')
    styles_parser.add_argument('--page', type=int, default=1, help='页码（默认1）')
    styles_parser.add_argument('--page-size', type=int, default=999, dest='page_size', help='每页数量（默认999）')
    styles_parser.add_argument('--language', default='zh', choices=['zh', 'en'], help='语言（默认zh，可选zh/en）')
    styles_parser.add_argument('--table', action='store_true', help='以表格形式输出')
    
    # 完整工作流命令
    workflow_parser = subparsers.add_parser('workflow', help='执行完整工作流（创建项目+提交任务合并为一步，然后查询进度->支付->等待完成）')
    workflow_parser.add_argument('--story', required=True, dest='diy_story', help='故事创意内容')
    workflow_parser.add_argument('--aspect', required=True, choices=['16:9', '9:16'], help='视频宽高比: 16:9 或 9:16')
    workflow_parser.add_argument('--duration', default='auto', dest='video_duration',
                                choices=['auto', '30', '60', '120', '180', '240', '300'],
                                help='视频时长: auto/30/60/120/180/240/300（默认: auto）')
    workflow_parser.add_argument('--project-name', required=True, dest='project_name', help='项目名称')
    workflow_parser.add_argument('--style-id', type=int, help='风格ID（可选）')
    workflow_parser.add_argument('--project-type', default='director', dest='project_type',
                                choices=['director', 'narration', 'short-film'],
                                help='项目类型: director（短剧模式）、narration（旁白模式）或 short-film（短片模式）（默认: director）')
    workflow_parser.add_argument('--character-info', dest='character_info',
                                help='角色图片 JSON，格式: [{"name":"角色名","url":"图片URL"}]')
    workflow_parser.add_argument('--video-first-model', default='grok', dest='video_first_model',
                                help='视频首选模型（默认: grok）')
    workflow_parser.add_argument('--video-second-model', default='seedance15-pro', dest='video_second_model',
                                help='视频备选模型（默认: seedance15-pro）')
    workflow_parser.add_argument('--image-first-model', default='seedream45', dest='image_first_model',
                                help='图片首选模型（默认: seedream45）')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # 只有在实际需要调用API时才初始化客户端（会检查requests）
    api = TrusteeModeAPI()
    
    if args.command == 'submit':
        result = api.submit_task(
            project_id=args.project_id,
            diy_story=args.diy_story,
            aspect=args.aspect,
            video_duration=args.video_duration,
            language=args.language,
            style_id=args.style_id if hasattr(args, 'style_id') and args.style_id is not None else None
        )
        print_response(result, args.pretty)
        
        # 兼容不同的响应格式：code可能是字符串"200"或数字200
        code = result.get("code")
        if isinstance(code, str):
            code = int(code) if code.isdigit() else 0
        
        if code == 0 or code == 200:
            task_id = result.get("data", {}).get("task_id")
            if task_id:
                print(f"\n任务ID: {task_id}", file=sys.stderr)
    
    elif args.command == 'query':
        if args.poll:
            # 轮询模式
            print(f"开始轮询查询项目 {args.project_id}...", file=sys.stderr)
            while True:
                result = api.query_progress(args.project_id)
                
                # 兼容不同的响应格式：code可能是字符串"200"或数字200
                code = result.get("code")
                if isinstance(code, str):
                    code = int(code) if code.isdigit() else 0
                
                if code != 0 and code != 200:
                    print_response(result, args.pretty)
                    break
                
                # 如果成功，继续处理数据
                
                data = result.get("data", {})
                status = data.get("status", "unknown")
                current_step = data.get("current_step", "")
                
                print(f"\n任务状态: {status}, 当前步骤: {current_step}", file=sys.stderr)
                print_response(result, args.pretty)
                
                if status == "completed":
                    video_asset = data.get("video_asset", {})
                    if video_asset:
                        print(f"\n视频下载URL: {video_asset.get('download_url')}", file=sys.stderr)
                        print(f"视频时长: {video_asset.get('duration')}秒", file=sys.stderr)
                    break
                elif status == "failed":
                    err_msg = data.get("err_msg", "")
                    print(f"\n任务失败: {err_msg}", file=sys.stderr)
                    break
                
                time.sleep(args.interval)
        else:
            # 单次查询
            result = api.query_progress(args.project_id)
            print_response(result, args.pretty)
    
    elif args.command == 'pay':
        result = api.pay(
            project_id=args.project_id,
            video_first_model=args.video_first_model,
            video_second_model=args.video_second_model,
            image_first_model=args.image_first_model
        )
        print_response(result, args.pretty)
        
        # 兼容不同的响应格式：code可能是字符串"200"或数字200
        code = result.get("code")
        if isinstance(code, str):
            code = int(code) if code.isdigit() else 0
        
        if code == 0 or code == 200:
            data = result.get("data", {})
            order_id = data.get("order_id")
            price = data.get("price")
            if order_id:
                print(f"\n项目ID: {order_id}, 消耗积分: {price}", file=sys.stderr)
    
    elif args.command == 'styles':
        result = api.get_styles(page=args.page, page_size=args.page_size, language=args.language)
        
        if args.table:
            # 表格形式输出
            code = result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            
            if code == 0 or code == 200:
                data = result.get("data", {})
                styles = data.get("list", [])
                
                if styles:
                    print(f"\n{'ID':<8} {'名称':<20} {'分类':<15} {'描述':<50}", file=sys.stderr)
                    print("-" * 95, file=sys.stderr)
                    for style in styles:
                        style_id = style.get("id", "")
                        name = style.get("name", "")[:18]
                        category = style.get("category", "")[:13]
                        description = style.get("description", "")[:48]
                        print(f"{style_id:<8} {name:<20} {category:<15} {description:<50}", file=sys.stderr)
                    
                    pagination = data.get("pagination", {})
                    total = pagination.get("total", 0)
                    print(f"\n总计: {total} 个风格", file=sys.stderr)
                else:
                    print("未找到风格列表", file=sys.stderr)
            else:
                print_response(result, args.pretty)
        else:
            print_response(result, args.pretty)
    
    elif args.command == 'workflow':
        character_info = None
        if getattr(args, 'character_info', None):
            try:
                character_info = json.loads(args.character_info)
            except json.JSONDecodeError:
                print("错误: character-info 必须是有效的 JSON 数组", file=sys.stderr)
                sys.exit(1)
        result = api.execute_workflow(
            diy_story=args.diy_story,
            aspect=args.aspect,
            project_name=args.project_name,
            video_duration=args.video_duration,
            style_id=args.style_id if hasattr(args, 'style_id') and args.style_id is not None else None,
            project_type=args.project_type,
            character_info=character_info,
            video_first_model=args.video_first_model,
            video_second_model=args.video_second_model,
            image_first_model=args.image_first_model
        )
        print_response(result, args.pretty)


if __name__ == '__main__':
    main()
