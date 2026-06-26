#!/usr/bin/env python3
"""
MV 托管模式 API 调用脚本
支持三种音乐生成模式：提示词(prompt)、自定义(custom)、上传(upload)
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


def _check_requests():
    """检查并导入 requests 库"""
    try:
        import requests
        return requests
    except ImportError:
        print("错误: 需要安装 requests 库", file=sys.stderr)
        print("请运行: pip install requests", file=sys.stderr)
        sys.exit(1)


class MVTrusteeAPI:
    """MV 托管模式 API 客户端"""

    def __init__(self):
        requests = _check_requests()
        self.api_key = os.getenv("GIGGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "未找到 GIGGLE_API_KEY，请设置系统环境变量：\n"
                "export GIGGLE_API_KEY=your_api_key\n"
                "API Key 可在 [Giggle.pro](https://giggle.pro/) 账号设置中获取。"
            )
        self.base_url = "https://giggle.pro"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def create_project(self, name: str, aspect: str) -> Dict[str, Any]:
        """创建 MV 项目"""
        url = f"{self.base_url}/api/v1/project/create"
        data = {
            "name": name,
            "type": "mv",
            "aspect": aspect,
            "mode": "trustee"
        }
        try:
            headers = {"x-auth": self.api_key}
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
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

    def create_and_submit(
        self,
        project_name: str,
        music_generate_type: str,
        aspect: str,
        reference_image: str = "",
        reference_image_url: str = "",
        scene_description: str = "",
        subtitle_enabled: bool = False,
        prompt: str = "",
        vocal_gender: str = "auto",
        instrumental: bool = False,
        lyrics: str = "",
        style: str = "",
        title: str = "",
        music_asset_id: str = "",
    ) -> Dict[str, Any]:
        """
        创建项目并提交任务（合并为一步，AI 只需调用此方法一次，不要分开调用 create_project 和 submit_mv_task）
        返回包含 project_id 和提交结果的字典
        """
        create_result = self.create_project(name=project_name, aspect=aspect)
        code = create_result.get("code")
        if isinstance(code, str):
            code = int(code) if code.isdigit() else 0
        if code != 0 and code != 200:
            return create_result

        project_id = create_result.get("data", {}).get("project_id")
        if not project_id:
            return {"code": -1, "msg": "创建项目失败: 未获取到项目ID", "data": None}

        submit_result = self.submit_mv_task(
            project_id=project_id,
            music_generate_type=music_generate_type,
            aspect=aspect,
            reference_image=reference_image,
            reference_image_url=reference_image_url,
            scene_description=scene_description,
            subtitle_enabled=subtitle_enabled,
            prompt=prompt,
            vocal_gender=vocal_gender,
            instrumental=instrumental,
            lyrics=lyrics,
            style=style,
            title=title,
            music_asset_id=music_asset_id,
        )
        sub_code = submit_result.get("code")
        if isinstance(sub_code, str):
            sub_code = int(sub_code) if sub_code.isdigit() else -1
        if sub_code not in (0, 200):
            return submit_result
        return {
            "code": 200,
            "msg": "success",
            "data": {"project_id": project_id, **submit_result.get("data", {})},
        }

    @staticmethod
    def _validate_base64_image(value: str, field_name: str) -> Optional[str]:
        """校验 base64 格式的参考图，返回错误信息或 None"""
        if not value:
            return None
        if value.startswith(("http://", "https://")):
            return None
        if re.match(r"^data:image/[^;]+;base64,", value):
            return (
                f"{field_name} 包含 data:image/xxx;base64, 前缀，"
                "请直接传递纯 Base64 编码字符串，不要添加前缀"
            )
        is_short_id = len(value) <= 32 and re.match(r"^[a-zA-Z0-9_-]+$", value)
        if is_short_id:
            return None
        try:
            decoded = base64.b64decode(value, validate=True)
            if len(decoded) < 8:
                return f"{field_name} 的 Base64 解码后数据过短，不是有效的图片"
        except Exception:
            return f"{field_name} 不是有效的 Base64 编码字符串，请检查格式"
        return None

    def submit_mv_task(
        self,
        project_id: str,
        music_generate_type: str,
        aspect: str,
        reference_image: str = "",
        reference_image_url: str = "",
        scene_description: str = "",
        subtitle_enabled: bool = False,
        # prompt 模式
        prompt: str = "",
        vocal_gender: str = "auto",
        instrumental: bool = False,
        # custom 模式
        lyrics: str = "",
        style: str = "",
        title: str = "",
        # upload 模式
        music_asset_id: str = "",
    ) -> Dict[str, Any]:
        """
        提交 MV 托管任务

        Args:
            project_id: 项目 ID
            music_generate_type: prompt / custom / upload
            aspect: 16:9 或 9:16
            reference_image: 参考图 asset_id（与 reference_image_url 二选一）
            reference_image_url: 参考图下载链接（与 reference_image 二选一）
            scene_description: 场景描述，默认空
            subtitle_enabled: 字幕开关，默认 False
            prompt, vocal_gender, instrumental: 提示词模式参数
            lyrics, style, title: 自定义模式参数
            music_asset_id: 上传模式参数
        """
        for val, name in [
            (reference_image, "reference_image"),
            (reference_image_url, "reference_image_url"),
        ]:
            err = self._validate_base64_image(val, name)
            if err:
                raise ValueError(err)

        url = f"{self.base_url}/api/v1/trustee_mode/mv/submit"
        data = {
            "project_id": project_id,
            "music_generate_type": music_generate_type,
            "aspect": aspect,
            "scene_description": scene_description,
            "subtitle_enabled": subtitle_enabled,
        }
        if reference_image:
            data["reference_image"] = reference_image
        elif reference_image_url:
            data["reference_image_url"] = reference_image_url

        if music_generate_type == "prompt":
            data["prompt"] = prompt
            data["vocal_gender"] = vocal_gender
            data["instrumental"] = instrumental
        elif music_generate_type == "custom":
            data["lyrics"] = lyrics
            data["style"] = style
            data["title"] = title
        elif music_generate_type == "upload":
            data["music_asset_id"] = music_asset_id

        try:
            headers = {"x-auth": self.api_key}
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
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
        """查询 MV 托管进度"""
        url = f"{self.base_url}/api/v1/trustee_mode/mv/query"
        params = {"project_id": project_id}
        try:
            headers = {"x-auth": self.api_key}
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            result = response.json()
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

    def pay(self, project_id: str) -> Dict[str, Any]:
        """MV 托管支付（模型固定，仅传 project_id）"""
        url = f"{self.base_url}/api/v1/trustee_mode/mv/pay"
        data = {"project_id": project_id}
        try:
            headers = {"x-auth": self.api_key}
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
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

    def retry(self, project_id: str, current_step: str) -> Dict[str, Any]:
        """重试失败步骤，从指定 current_step 重新执行"""
        url = f"{self.base_url}/api/v1/trustee_mode/mv/retry"
        data = {"project_id": project_id, "current_step": current_step}
        try:
            headers = {"x-auth": self.api_key}
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            code = result.get("code")
            if isinstance(code, str):
                code = int(code) if code.isdigit() else 0
            if code != 0 and code != 200:
                print(f"重试失败: {result.get('msg', '未知错误')}")
                return result
            return result
        except Exception as e:
            print(f"请求失败: {e}")
            return {"code": -1, "msg": str(e)}

    def execute_workflow(
        self,
        music_generate_type: str,
        aspect: str,
        project_name: str,
        reference_image: str = "",
        reference_image_url: str = "",
        scene_description: str = "",
        subtitle_enabled: bool = False,
        prompt: str = "",
        vocal_gender: str = "auto",
        instrumental: bool = False,
        lyrics: str = "",
        style: str = "",
        title: str = "",
        music_asset_id: str = "",
    ) -> Dict[str, Any]:
        """
        执行完整工作流：创建项目 -> 提交任务 -> 查询进度 -> 支付 -> 等待完成
        """
        start_time = datetime.now()
        timeout = timedelta(hours=1)
        query_interval = 3

        # 校验必填
        if not reference_image and not reference_image_url:
            return {"code": -1, "msg": "reference_image 或 reference_image_url 至少提供一个", "data": None}
        if music_generate_type == "prompt" and not prompt:
            return {"code": -1, "msg": "提示词模式必须提供 prompt", "data": None}
        if music_generate_type == "custom" and not (lyrics and style and title):
            return {"code": -1, "msg": "自定义模式必须提供 lyrics, style, title", "data": None}
        if music_generate_type == "upload" and not music_asset_id:
            return {"code": -1, "msg": "上传模式必须提供 music_asset_id", "data": None}

        # 步骤1：创建项目并提交任务（合并一步）
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 步骤1: 创建项目并提交任务...", file=sys.stderr)
        cs_result = self.create_and_submit(
            project_name=project_name,
            music_generate_type=music_generate_type,
            aspect=aspect,
            reference_image=reference_image,
            reference_image_url=reference_image_url,
            scene_description=scene_description,
            subtitle_enabled=subtitle_enabled,
            prompt=prompt,
            vocal_gender=vocal_gender,
            instrumental=instrumental,
            lyrics=lyrics,
            style=style,
            title=title,
            music_asset_id=music_asset_id,
        )
        code = cs_result.get("code")
        if isinstance(code, str):
            code = int(code) if code.isdigit() else 0
        if code != 0 and code != 200:
            return {"code": code, "msg": cs_result.get("msg", "创建并提交失败"), "data": None}
        project_id = cs_result.get("data", {}).get("project_id")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{project_id}] 项目创建并任务提交成功", file=sys.stderr)

        # 步骤2：轮询进度与支付
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{project_id}] 步骤2: 查询进度...", file=sys.stderr)
        paid = False
        max_retries = 5
        retry_delay = 5

        while True:
            if datetime.now() - start_time > timeout:
                return {"code": -1, "msg": "工作流超时（超过1小时）", "data": None}

            query_result = None
            query_success = False
            retry_count = 0

            while retry_count < max_retries:
                try:
                    query_result = self.query_progress(project_id)
                    code = query_result.get("code")
                    if isinstance(code, str):
                        code = int(code) if code.isdigit() else 0
                    if code == 0 or code == 200:
                        query_success = True
                        break
                    error_msg = str(query_result.get("msg", ""))
                    is_network_error = any(
                        x in error_msg for x in ["Connection", "Remote", "timeout", "aborted", "disconnected"]
                    )
                    if not is_network_error:
                        return {"code": code, "msg": f"查询失败: {error_msg}", "data": None}
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{project_id}] 网络错误，{retry_delay}秒后重试 ({retry_count}/{max_retries})", file=sys.stderr)
                        time.sleep(retry_delay)
                    else:
                        time.sleep(query_interval)
                        break
                except Exception as e:
                    error_str = str(e)
                    is_network_error = any(
                        x in error_str for x in ["Connection", "Remote", "timeout", "aborted", "disconnected"]
                    )
                    if not is_network_error:
                        return {"code": -1, "msg": f"查询异常: {error_str}", "data": None}
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(retry_delay)
                    else:
                        time.sleep(query_interval)
                        break

            if not query_success:
                continue

            data = query_result.get("data", {})
            status = data.get("status", "unknown")
            current_step = data.get("current_step", "")
            pay_status = data.get("pay_status", "")
            err_msg = data.get("err_msg", "")

            if status == "failed" or err_msg:
                return {"code": -1, "msg": f"任务失败: {err_msg or '未知错误'}", "data": None}

            steps = data.get("steps", [])
            for step in steps:
                for sub in step.get("sub_steps", []):
                    if sub.get("status") == "failed" or sub.get("error"):
                        return {"code": -1, "msg": f"子步骤失败: {sub.get('step', '')} - {sub.get('error', '')}", "data": None}

            if not paid and (pay_status == "pending" or (current_step and "pay" in current_step.lower())):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [{project_id}] 执行支付...", file=sys.stderr)
                pay_result = self.pay(project_id)
                code = pay_result.get("code")
                if isinstance(code, str):
                    code = int(code) if code.isdigit() else 0
                if code != 0 and code != 200:
                    return {"code": code, "msg": f"支付失败: {pay_result.get('msg', '未知错误')}", "data": None}
                paid = True
                continue

            video_asset = data.get("video_asset", {})
            download_url = video_asset.get("download_url") if video_asset else None
            if video_asset and download_url:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [{project_id}] 任务完成: {download_url}", file=sys.stderr)
                return {
                    "code": 200,
                    "msg": "success",
                    "uuid": query_result.get("uuid", ""),
                    "data": {"project_id": project_id, "download_url": download_url, "video_asset": video_asset, "status": "completed"},
                }

            print(f"[{datetime.now().strftime('%H:%M:%S')}] [{project_id}] 状态: {status}, 步骤: {current_step}, 支付状态: {pay_status}", file=sys.stderr)
            time.sleep(query_interval)


def main():
    parser = argparse.ArgumentParser(description="MV 托管模式 API 调用工具", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pretty", action="store_true", help="美化 JSON")
    sub = parser.add_subparsers(dest="command")

    csp = sub.add_parser("create-submit", help="创建项目并提交任务（一步完成，推荐）")
    csp.add_argument("--mode", required=True, choices=["prompt", "custom", "upload"])
    csp.add_argument("--aspect", required=True, choices=["16:9", "9:16"])
    csp.add_argument("--project-name", required=True)
    csp.add_argument("--reference-image", default="")
    csp.add_argument("--reference-image-url", default="")
    csp.add_argument("--scene-description", default="")
    csp.add_argument("--subtitle", action="store_true")
    csp.add_argument("--prompt", default="")
    csp.add_argument("--vocal-gender", default="auto")
    csp.add_argument("--instrumental", action="store_true")
    csp.add_argument("--lyrics", default="")
    csp.add_argument("--style", default="")
    csp.add_argument("--title", default="")
    csp.add_argument("--music-asset-id", default="")

    cp = sub.add_parser("create", help="[仅调试用] 单独创建项目")
    cp.add_argument("--name", required=True)
    cp.add_argument("--aspect", required=True, choices=["16:9", "9:16"])

    sp = sub.add_parser("submit", help="[仅调试用] 单独提交任务（需已有 project_id）")
    sp.add_argument("--project-id", required=True)
    sp.add_argument("--mode", required=True, choices=["prompt", "custom", "upload"])
    sp.add_argument("--aspect", required=True, choices=["16:9", "9:16"])
    sp.add_argument("--reference-image", default="")
    sp.add_argument("--reference-image-url", default="")
    sp.add_argument("--scene-description", default="")
    sp.add_argument("--subtitle", action="store_true")
    sp.add_argument("--prompt", default="")
    sp.add_argument("--vocal-gender", default="auto")
    sp.add_argument("--instrumental", action="store_true")
    sp.add_argument("--lyrics", default="")
    sp.add_argument("--style", default="")
    sp.add_argument("--title", default="")
    sp.add_argument("--music-asset-id", default="")

    qp = sub.add_parser("query", help="查询进度")
    qp.add_argument("--project-id", required=True)

    pp = sub.add_parser("pay", help="支付")
    pp.add_argument("--project-id", required=True)

    rp = sub.add_parser("retry", help="重试失败步骤")
    rp.add_argument("--project-id", required=True)
    rp.add_argument("--current-step", required=True, help="如 music-generate, storyboard, shot, editor")

    wp = sub.add_parser("workflow", help="完整工作流")
    wp.add_argument("--mode", required=True, choices=["prompt", "custom", "upload"])
    wp.add_argument("--aspect", required=True, choices=["16:9", "9:16"])
    wp.add_argument("--project-name", required=True)
    wp.add_argument("--reference-image", default="")
    wp.add_argument("--reference-image-url", default="")
    wp.add_argument("--scene-description", default="")
    wp.add_argument("--subtitle", action="store_true")
    wp.add_argument("--prompt", default="")
    wp.add_argument("--vocal-gender", default="auto")
    wp.add_argument("--instrumental", action="store_true")
    wp.add_argument("--lyrics", default="")
    wp.add_argument("--style", default="")
    wp.add_argument("--title", default="")
    wp.add_argument("--music-asset-id", default="")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    api = MVTrusteeAPI()

    if args.command == "create-submit":
        r = api.create_and_submit(
            project_name=args.project_name,
            music_generate_type=args.mode,
            aspect=args.aspect,
            reference_image=args.reference_image,
            reference_image_url=args.reference_image_url,
            scene_description=args.scene_description,
            subtitle_enabled=args.subtitle,
            prompt=args.prompt,
            vocal_gender=args.vocal_gender,
            instrumental=args.instrumental,
            lyrics=args.lyrics,
            style=args.style,
            title=args.title,
            music_asset_id=args.music_asset_id,
        )
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.pretty else json.dumps(r, ensure_ascii=False))

    elif args.command == "create":
        r = api.create_project(name=args.name, aspect=args.aspect)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.pretty else json.dumps(r, ensure_ascii=False))

    elif args.command == "submit":
        r = api.submit_mv_task(
            project_id=args.project_id,
            music_generate_type=args.mode,
            aspect=args.aspect,
            reference_image=args.reference_image,
            reference_image_url=args.reference_image_url,
            scene_description=args.scene_description,
            subtitle_enabled=args.subtitle,
            prompt=args.prompt,
            vocal_gender=args.vocal_gender,
            instrumental=args.instrumental,
            lyrics=args.lyrics,
            style=args.style,
            title=args.title,
            music_asset_id=args.music_asset_id,
        )
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.pretty else json.dumps(r, ensure_ascii=False))

    elif args.command == "query":
        r = api.query_progress(args.project_id)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.pretty else json.dumps(r, ensure_ascii=False))

    elif args.command == "pay":
        r = api.pay(args.project_id)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.pretty else json.dumps(r, ensure_ascii=False))

    elif args.command == "retry":
        r = api.retry(project_id=args.project_id, current_step=args.current_step)
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.pretty else json.dumps(r, ensure_ascii=False))

    elif args.command == "workflow":
        r = api.execute_workflow(
            music_generate_type=args.mode,
            aspect=args.aspect,
            project_name=args.project_name,
            reference_image=args.reference_image,
            reference_image_url=args.reference_image_url,
            scene_description=args.scene_description,
            subtitle_enabled=args.subtitle,
            prompt=args.prompt,
            vocal_gender=args.vocal_gender,
            instrumental=args.instrumental,
            lyrics=args.lyrics,
            style=args.style,
            title=args.title,
            music_asset_id=args.music_asset_id,
        )
        print(json.dumps(r, indent=2, ensure_ascii=False) if args.pretty else json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
