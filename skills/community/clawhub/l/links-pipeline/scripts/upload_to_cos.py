#!/usr/bin/env python3
"""上传处理结果到对象存储（从config.yaml读取配置）"""
import subprocess, sys, json, yaml, os
from pathlib import Path

def load_storage_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        config = yaml.safe_load(config_path.read_text())
        return config.get("storage", {})
    return {}

def upload(local_path: str, target_path: str) -> bool:
    """调用系统工具上传到对象存储"""
    sc = load_storage_config()
    stype = sc.get("type", "local")
    
    if stype == "cos":
        cos = sc.get("cos", {})
        bucket = cos.get("bucket", "")
        region = cos.get("region", "")
        # 优先使用 ~/.cos.conf 中的凭据
        result = subprocess.run(
            ["coscmd", "-b", bucket, "-r", region,
             "upload", local_path, target_path],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    else:
        # 本地模式：直接复制
        result = subprocess.run(["cp", local_path, target_path],
                                capture_output=True, text=True, timeout=10)
        return result.returncode == 0

def save_and_upload(text: str, filename: str, target_cos_path: str) -> dict:
    """本地保存并上传"""
    local_path = f"/tmp/links-pipeline/{filename}"
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    Path(local_path).write_text(text, encoding="utf-8")
    
    ok = upload(local_path, target_cos_path)
    return {
        "ok": ok,
        "local_path": local_path,
        "target_path": target_cos_path
    }

if __name__ == "__main__":
    data = json.load(sys.stdin)
    result = save_and_upload(data["text"], data["filename"], data["target_path"])
    print(json.dumps(result, ensure_ascii=False))
