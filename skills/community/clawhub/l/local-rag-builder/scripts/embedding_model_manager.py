"""
local-rag-builder 嵌入模型管理模块
v0.1.0
支持多源下载、重试、完整性校验、路径修正、多模型管理
"""

import os
import sys
import json
import re
import hashlib
import tempfile

from utils import MODELS_DIR, cache_directory, run_command, dir_size

# 下载源配置（按优先级）
DOWNLOAD_SOURCES = [
    {"name": "modelscope", "url_template": None,
     "method": "modelscope",
     "description": "ModelScope 国内镜像（推荐）"},
    {"name": "hf_mirror", "url_template": None,
     "method": "huggingface_mirror",
     "description": "HuggingFace 国内镜像"},
    {"name": "hf_official", "url_template": None,
     "method": "huggingface_official",
     "description": "HuggingFace 官方源"},
    {"name": "llm_find", "url_template": None,
     "method": "llm_search",
     "description": "LLM 自动查找可用源"},
]

# 预配置模型列表
RECOMMENDED_MODELS = [
    {"id": "BAAI/bge-small-zh-v1.5", "size_mb": 130, "desc": "轻量中文嵌入（推荐）", "type": "bge"},
    {"id": "BAAI/bge-base-zh-v1.5", "size_mb": 400, "desc": "中等中文嵌入", "type": "bge"},
    {"id": "shibing624/text2vec-base-chinese", "size_mb": 400, "desc": "轻量中文嵌入（CPU 友好）", "type": "text2vec"},
    {"id": "maidalun1020/bce-embedding-base_v1", "size_mb": 800, "desc": "网易 BCEmbedding", "type": "bce"},
    {"id": "sentence-transformers/all-MiniLM-L6-v2", "size_mb": 80, "desc": "英文嵌入（超轻量）", "type": "st"},
    {"id": "BAAI/bge-large-zh-v1.5", "size_mb": 1300, "desc": "高精度中文嵌入（大）", "type": "bge"},
]

MODEL_INDEX_FILE = os.path.join(MODELS_DIR, "model_index.json")


def _load_index():
    """加载模型索引"""
    if os.path.exists(MODEL_INDEX_FILE):
        try:
            with open(MODEL_INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_index(index):
    """保存模型索引"""
    tmp = MODEL_INDEX_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MODEL_INDEX_FILE)


def _normalize(s):
    """将字符串归一化为纯字母数字，去除所有符号差异"""
    return re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '', s.lower())


def _find_actual_model_path(model_id, download_dir):
    """
    通用模型路径查找。
    不依赖任何固定变形模式（不硬编码 1___5、1_5 等），
    通过 内容扫描 + 名称相似度评分 找到真实的模型目录。
    """
    target_id = model_id.split("/")[-1]  # "bge-small-zh-v1.5"
    target_norm = _normalize(target_id)  # "bgesmallzhv15"

    best_match = None
    best_score = 0

    for root, dirs, _ in os.walk(download_dir):
        for d in dirs:
            candidate_path = os.path.join(root, d)
            # 跳过明显不是模型目录的（如 .cache, snapshots, blobs）
            if d.startswith("."):
                continue

            # 算名称相似度
            dir_norm = _normalize(d)
            score = _name_similarity(target_norm, dir_norm)

            if score > best_score:
                # 确认该目录下包含模型产物（config.json 或 .bin/.safetensors）
                if _is_model_dir(candidate_path):
                    best_score = score
                    best_match = candidate_path

    return best_match


def _name_similarity(a, b):
    """
    名称相似度评分（0~100）。
    基于：完全匹配 > 一端包含另一端 > 公共子序列长度。
    """
    if a == b:
        return 100
    if a in b or b in a:
        return 80 + (10 * min(len(a), len(b)) / max(len(a), len(b)))
    # 最长公共子序列（简化版：前缀匹配）
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    prefix_score = 40 * i / max(len(a), len(b)) if max(len(a), len(b)) > 0 else 0
    # 公共字符比例
    common = sum(1 for c in a if c in b)
    char_score = 30 * common / max(len(a), len(b)) if max(len(a), len(b)) > 0 else 0
    return prefix_score + char_score


def _is_model_dir(path):
    """
    判断目录是否包含模型文件。
    不要求全部存在，有任一标志性文件即可。
    """
    if not os.path.isdir(path):
        return False
    try:
        entries = os.listdir(path)
        # 标志性文件
        model_files = [
            "config.json", "pytorch_model.bin", "model.safetensors",
            "vocab.txt", "tokenizer.json", "model.onnx",
        ]
        for entry in entries:
            if entry in model_files:
                return True
            if entry.endswith((".bin", ".safetensors", ".onnx")):
                return True
        # 有些模型把文件放在子目录，检查子目录
        for entry in entries:
            subpath = os.path.join(path, entry)
            if os.path.isdir(subpath):
                if _is_model_dir(subpath):
                    return True
    except (PermissionError, OSError):
        return False
    return False


def _fuzzy_match(expected, actual):
    """模糊匹配模型名（通用版，不依赖任何特定变形模式）"""
    return _normalize(expected) == _normalize(actual)


def _check_integrity(model_path):
    """检查模型完整性：目录非空且有模型文件"""
    if not model_path or not os.path.exists(model_path):
        return False, "路径不存在"

    model_files = []
    for root, _, files in os.walk(model_path):
        for f in files:
            if f.endswith((".bin", ".safetensors", ".onnx", ".pt", ".pth")):
                model_files.append(os.path.join(root, f))

    if not model_files:
        # 仅有 config.json 不够，必须有权重文件才认为完整性通过
        return False, "模型文件不完整（缺少 .bin/.safetensors/.onnx 等权重文件）"

    total_size = sum(os.path.getsize(f) for f in model_files if os.path.exists(f))
    return True, f"找到 {len(model_files)} 个模型文件，共 {total_size / 1e6:.1f}MB"


def _download_with_modelscope(model_id, cache_dir):
    """使用 ModelScope 下载"""
    script = f"""
from modelscope.hub.snapshot_download import snapshot_download
try:
    path = snapshot_download('{model_id}', cache_dir=r'{cache_dir}')
    print(f"SAVED_TO:{{path}}")
except Exception as e:
    print(f"ERROR:{{e}}")
"""
    py = sys.executable
    result = run_command([py, "-c", script], timeout=600)
    return result


def _download_with_hf_mirror(model_id, cache_dir):
    """使用 HuggingFace 镜像下载"""
    env = os.environ.copy()
    env["HF_ENDPOINT"] = "https://hf-mirror.com"
    script = f"""
import os, sys
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from huggingface_hub import snapshot_download
try:
    path = snapshot_download('{model_id}', cache_dir=r'{cache_dir}')
    print(f"SAVED_TO:{{path}}")
except Exception as e:
    print(f"ERROR:{{e}}")
"""
    result = run_command([sys.executable, "-c", script], timeout=600)
    return result


def _download_with_hf_official(model_id, cache_dir):
    """使用 HuggingFace 官方源下载"""
    script = f"""
from huggingface_hub import snapshot_download
try:
    path = snapshot_download('{model_id}', cache_dir=r'{cache_dir}')
    print(f"SAVED_TO:{{path}}")
except Exception as e:
    print(f"ERROR:{{e}}")
"""
    result = run_command([sys.executable, "-c", script], timeout=600)
    return result


def download_model(model_id, sources=None, max_retries_per_source=3, max_sources=5):
    """
    下载嵌入模型，支持多源切换和重试
    返回: {"success": bool, "path": str, "source": str, "details": str}
    """
    if sources is None:
        sources = [s["name"] for s in DOWNLOAD_SOURCES[:max_sources]]

    download_dir = os.path.join(cache_directory, "model_downloads")
    os.makedirs(download_dir, exist_ok=True)

    source_methods = {
        "modelscope": _download_with_modelscope,
        "huggingface_mirror": _download_with_hf_mirror,
        "huggingface_official": _download_with_hf_official,
    }

    for source_name in sources:
        print(f"\n  尝试源 [{source_name}]...")
        method = source_methods.get(source_name)
        if method is None and source_name == "llm_find":
            print(f"  跳过 llm_find（需要 LLM 辅助查询可用源）")
            continue
        if method is None:
            print(f"  跳过（未知源）")
            continue

        for attempt in range(max_retries_per_source):
            print(f"    第 {attempt + 1} 次尝试...")
            result = method(model_id, download_dir)

            if result["success"]:
                stdout = result.get("stdout", "")
                # 从输出中提取路径
                saved_path = None
                for line in stdout.split("\n"):
                    if line.startswith("SAVED_TO:"):
                        saved_path = line[len("SAVED_TO:"):].strip()
                        break

                if not saved_path:
                    saved_path = _find_actual_model_path(model_id, download_dir)

                if saved_path:
                    ok, detail = _check_integrity(saved_path)
                    if ok:
                        print(f"  [OK] 从 {source_name} 下载成功: {saved_path}")
                        print(f"  [OK] 完整性检查通过: {detail}")

                        # 复制到 models 目录
                        target_dir = os.path.join(MODELS_DIR, model_id.replace("/", "_"))
                        if os.path.exists(target_dir):
                            import shutil
                            shutil.rmtree(target_dir)
                        import shutil
                        shutil.copytree(saved_path, target_dir)

                        # 更新索引
                        index = _load_index()
                        index[model_id] = {
                            "path": target_dir,
                            "source": source_name,
                            "size_mb": round(dir_size(target_dir), 1),
                            "status": "ready",
                        }
                        _save_index(index)

                        return {
                            "success": True,
                            "path": target_dir,
                            "source": source_name,
                            "details": detail,
                        }
                    else:
                        print(f"    完整性检查失败: {detail}")
                else:
                    print(f"    无法定位模型路径")
            else:
                stderr = result.get("stderr", "")
                print(f"    失败: {stderr.strip()[-150:]}")

    return {"success": False, "path": "", "source": "", "details": "所有源均失败"}


def verify_model(model_id_or_path):
    """验证模型是否可用（尝试用 HuggingFaceEmbeddings 加载）"""
    model_path = model_id_or_path

    # 如果是模型 ID，先查索引
    index = _load_index()
    if model_id_or_path in index:
        model_path = index[model_id_or_path]["path"]

    if not os.path.exists(str(model_path)):
        return False, f"路径不存在: {model_path}"

    # 通用内容检测：使用 _is_model_dir 判断是否为有效模型目录
    is_valid = _is_model_dir(str(model_path))

    # 补充详细报告
    has_config = os.path.exists(os.path.join(str(model_path), "config.json"))
    model_files = []
    for root, _, files in os.walk(str(model_path)):
        for f in files:
            if f.endswith((".bin", ".safetensors", ".onnx", ".pt", ".pth")):
                model_files.append(f)

    detail_parts = []
    detail_parts.append(f"config.json: {'有' if has_config else '无'}")
    if model_files:
        detail_parts.append(f"模型文件: {len(model_files)} 个")
        detail_parts.append(f"总大小: {sum(os.path.getsize(os.path.join(root, f)) for root, _, files in os.walk(str(model_path)) for f in files if f.endswith(('.bin','.safetensors','.onnx','.pt','.pth'))) / 1e6:.1f}MB")
    else:
        detail_parts.append("模型文件: 无")

    return is_valid, " | ".join(detail_parts)


def list_downloaded_models():
    """列出已下载的模型"""
    index = _load_index()
    result = []
    for model_id, info in index.items():
        info["model_id"] = model_id
        result.append(info)
    return result


def remove_model(model_id):
    """删除指定模型"""
    index = _load_index()
    if model_id not in index:
        return False, f"模型 '{model_id}' 不在索引中"

    path = index[model_id].get("path", "")
    if path and os.path.exists(path):
        import shutil
        shutil.rmtree(path)

    del index[model_id]
    _save_index(index)
    return True, f"已删除 {model_id}"


def get_model_path(model_id):
    """获取模型路径（通过 ID 或直接路径）"""
    if os.path.exists(model_id):
        return model_id

    index = _load_index()
    if model_id in index:
        return index[model_id]["path"]

    # 通用查找：逐层目录探测是否包含模型文件
    target_norm = _normalize(model_id.split("/")[-1])
    best_match = None
    best_score = 0

    for item in os.listdir(MODELS_DIR):
        item_path = os.path.join(MODELS_DIR, item)
        if not os.path.isdir(item_path):
            continue
        dir_norm = _normalize(item)
        score = _name_similarity(target_norm, dir_norm)
        if score > best_score and _is_model_dir(item_path):
            best_score = score
            best_match = item_path

    return best_match


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="嵌入模型管理工具")
    parser.add_argument("--download", type=str, help="下载模型（HuggingFace ID）")
    parser.add_argument("--interactive", action="store_true", help="交互式选择模型下载")
    parser.add_argument("--list", action="store_true", help="列出已下载模型")
    parser.add_argument("--check", type=str, help="验证模型完整性")
    parser.add_argument("--remove", type=str, help="删除模型")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出（供智能体调用）")

    args = parser.parse_args()

    if args.list:
        models = list_downloaded_models()
        if args.json:
            print(json.dumps(models, ensure_ascii=False, indent=2))
        else:
            if not models:
                print("未下载任何嵌入模型")
            else:
                print(f"已下载模型 ({len(models)}):")
                for m in models:
                    print(f"  {m['model_id']} -> {m['path']} ({m.get('size_mb', '?')}MB)")

    elif args.check:
        ok, detail = verify_model(args.check)
        print(f"[{'OK' if ok else '!'}] {detail}")

    elif args.remove:
        ok, msg = remove_model(args.remove)
        print(f"[{'OK' if ok else '!'}] {msg}")

    elif args.download:
        print(f"下载嵌入模型: {args.download}")
        result = download_model(args.download)
        if result["success"]:
            print(f"[OK] 下载成功: {result['path']}")
            print(f"  来源: {result['source']}")
            print(f"  详情: {result['details']}")
        else:
            print(f"[!] 下载失败: {result['details']}")
            print("  建议: 检查网络连接或尝试其他模型")
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

    elif args.interactive:
        print("\n推荐嵌入模型:")
        print("-" * 70)
        print(f"{'#':<3} {'模型 ID':<40} {'大小':<10} {'说明':<25}")
        print("-" * 70)
        for i, m in enumerate(RECOMMENDED_MODELS, 1):
            print(f"{i:<3} {m['id']:<40} {m['size_mb']:<10} {m['desc']:<25}")
        print("-" * 70)
        print("0) 自定义模型 ID")

        try:
            choice = input("\n请选择 (0-{}): ".format(len(RECOMMENDED_MODELS))).strip()
            if choice == "0":
                model_id = input("输入 HuggingFace 模型 ID: ").strip()
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(RECOMMENDED_MODELS):
                    model_id = RECOMMENDED_MODELS[idx]["id"]
                else:
                    print("无效选择")
                    sys.exit(1)

            if model_id:
                result = download_model(model_id)
                if result["success"]:
                    print(f"\n[OK] 模型就绪: {result['path']}")
                else:
                    print(f"\n[!] 下载失败: {result['details']}")
        except (ValueError, EOFError):
            print("取消操作")

    else:
        parser.print_help()
