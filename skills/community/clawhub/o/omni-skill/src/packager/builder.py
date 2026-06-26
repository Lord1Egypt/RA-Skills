import os
import json
import shutil
import hashlib
from .scanner import scan_directory

def calculate_sha256(file_path):
    """计算单个文件的安全哈希算法二五六(SHA-256)校验和"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_checksum_file(target_dir):
    """为目标目录中的所有文件生成统一校验和文件"""
    checksum_path = os.path.join(target_dir, "checksum.txt")
    checksums = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file == "checksum.txt":
                continue
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, target_dir)
            file_hash = calculate_sha256(file_path)
            checksums.append(f"{file_hash}  {rel_path}")

    with open(checksum_path, "w", encoding="utf-8") as f:
        f.write("\n".join(checksums) + "\n")
    return checksum_path

def inject_gateway_template(target_dir, runtime):
    """根据运行时环境自动注入万能网关模板"""
    file_name = ""
    template_content = ""

    if runtime == "python":
        file_name = "omni_gateway.py"
        template_content = '''# 万能网关自动注入模板 (Omni Gateway Auto-Injected)
def gateway_handler(event, context):
    print("万能网关已为蟒蛇运行环境触发")
    return {"status": 200, "message": "成功"}
'''
    elif runtime == "node":
        file_name = "omni_gateway.js"
        template_content = '''// 万能网关自动注入模板 (Omni Gateway Auto-Injected)
exports.gatewayHandler = async (event, context) => {
    console.log("万能网关已为节点运行环境触发");
    return { status: 200, message: "成功" };
};
'''
    elif runtime == "binary":
        file_name = "omni_gateway.sh"
        template_content = '''#!/bin/bash
# 万能网关自动注入模板 (Omni Gateway Auto-Injected)
echo "万能网关已为二进制运行环境触发"
exit 0
'''
    elif runtime == "prompt":
        file_name = "omni_gateway.md"
        template_content = '''<!-- 万能网关自动注入模板 (Omni Gateway Auto-Injected) -->
> 万能网关已为提示词运行环境初始化。
'''
    else:
        file_name = "omni_gateway.txt"
        template_content = "万能网关已初始化。"

    if file_name:
        with open(os.path.join(target_dir, file_name), "w", encoding="utf-8") as f:
            f.write(template_content)

def build_package(source_dir, target_dir):
    """构建通用核心包"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 第一步：扫描源目录获取元数据
    meta_info = scan_directory(source_dir)

    # 第二步：将源文件安全迁移至目标目录
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # 第三步：注入万能网关模板
    inject_gateway_template(target_dir, meta_info["runtime"])

    # 第四步：构建并写入清单文件
    manifest_path = os.path.join(target_dir, "manifest.json")
    manifest_data = {
        "version": "1.0.0",
        "protocol": "omni-multi-runtime-v1",
        "metadata": meta_info
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=4, ensure_ascii=False)

    # 第五步：生成全包哈希校验和
    checksum_path = generate_checksum_file(target_dir)

    return manifest_path, checksum_path
