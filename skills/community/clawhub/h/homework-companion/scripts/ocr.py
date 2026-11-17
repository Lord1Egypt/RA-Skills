#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作业题目 OCR 识别 —— 基于腾讯云通用印刷体 / 手写体 OCR。

用法:
  python ocr.py --image <图片路径> [--mode accurate|handwriting]

输出: 识别出的题目文本 (UTF-8, 每行一段), 写到 stdout。
依赖: tencentcloud-sdk-python (见 requirements.txt)
"""
import os
import sys
import base64
import argparse


def _load_cred():
    sid = os.environ.get("TENCENTCLOUD_SECRET_ID")
    skey = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not sid or not skey:
        sys.stderr.write(
            "请先设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY\n"
        )
        sys.exit(3)
    return sid, skey


def recognize(image_path, mode="accurate"):
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.ocr.v20181119 import ocr_client, models
    except ImportError:
        sys.stderr.write(
            "缺少依赖 tencentcloud-sdk-python，请先执行: "
            "pip install -r requirements.txt\n"
        )
        sys.exit(2)

    sid, skey = _load_cred()
    cred = credential.Credential(sid, skey)
    http_profile = HttpProfile()
    http_profile.endpoint = "ocr.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = ocr_client.OcrClient(cred, "ap-guangzhou", client_profile)

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    if mode == "handwriting":
        req = models.GeneralHandwritingOCRRequest()
        req.ImageBase64 = img_b64
        resp = client.GeneralHandwritingOCR(req)
    else:
        req = models.GeneralAccurateOCRRequest()
        req.ImageBase64 = img_b64
        resp = client.GeneralAccurateOCR(req)

    texts = [t.DetectedText for t in resp.TextDetections]
    return "\n".join(texts)


def main():
    parser = argparse.ArgumentParser(description="作业题目 OCR 识别")
    parser.add_argument("--image", required=True, help="题目图片路径")
    parser.add_argument(
        "--mode",
        choices=["accurate", "handwriting"],
        default="accurate",
        help="accurate=印刷体高精度(默认), handwriting=手写体",
    )
    args = parser.parse_args()
    sys.stdout.write(recognize(args.image, args.mode) + "\n")


if __name__ == "__main__":
    main()
