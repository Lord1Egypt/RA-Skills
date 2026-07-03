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
    {"name": "hf_direct", "url_template": None,
     "method": "hf_direct",
     "description": "HF 直接下载（逐文件，稳定）"},
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

# Rerank / 路由模型列表（与嵌入模型分开管理）
RECOMMENDED_RERANK_MODELS = [
    {"id": "BAAI/bge-reranker-v2-m3", "size_mb": 1136, "desc": "多语言通用路由/rerank（推荐）", "type": "rerank"},
    {"id": "BAAI/bge-reranker-large", "size_mb": 1120, "desc": "中英通用 rerank", "type": "rerank"},
    {"id": "BAAI/bge-reranker-base", "size_mb": 556, "desc": "轻量 rerank（CPU 友好）", "type": "rerank"},
    {"id": "BAAI/bge-reranker-v2.5-gemma2-lightweight", "size_mb": 3000, "desc": "高精度 rerank（大）", "type": "rerank"},
    {"id": "mixedbread-ai/mxbai-rerank-base-v1", "size_mb": 556, "desc": "MIT 协议，可商用轻量", "type": "rerank"},
    {"id": "Alibaba-NLP/gte-multilingual-reranker-base", "size_mb": 600, "desc": "阿里出品，中文友好", "type": "rerank"},
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
    sys.exit(1)
"""
    py = sys.executable
    result = run_command([py, "-c", script], timeout=600)
    return result


def _download_with_hf_mirror(model_id, cache_dir):
    """使用 HuggingFace 镜像下载"""
    env = os.environ.copy()
    env["HF_ENDPOINT"] = "https://hf-mirror.com"
    env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"  # 关闭 tqdm 进度条，避免 \r 导致管道阻塞
    script = f"""
import os, sys
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
from huggingface_hub import snapshot_download
try:
    path = snapshot_download('{model_id}', cache_dir=r'{cache_dir}')
    print(f"SAVED_TO:{{path}}")
except Exception as e:
    print(f"ERROR:{{e}}")
    sys.exit(1)
"""
    result = run_command([sys.executable, "-c", script], timeout=1800)
    return result


def _download_with_hf_official(model_id, cache_dir):
    """使用 HuggingFace 官方源下载"""
    script = f"""
import os, sys
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
from huggingface_hub import snapshot_download
try:
    path = snapshot_download('{model_id}', cache_dir=r'{cache_dir}')
    print(f"SAVED_TO:{{path}}")
except Exception as e:
    print(f"ERROR:{{e}}")
    sys.exit(1)
"""
    result = run_command([sys.executable, "-c", script], timeout=1800)
    return result


def _download_with_hf_direct(model_id, cache_dir):
    """直接使用 hf_hub_download 逐文件下载（不经过子进程，避免 \r 死锁 + 超时问题）"""
    from huggingface_hub import hf_hub_download, list_repo_files
    import os, time

    # 设置镜像源（主进程可能未设 HF_ENDPOINT）
    os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
    os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

    try:
        files = list_repo_files(model_id)
    except Exception as e:
        # 镜像失败时降级到官方源
        os.environ["HF_ENDPOINT"] = "https://huggingface.co"
        try:
            files = list_repo_files(model_id)
        except Exception as e2:
            return {"success": False, "stdout": "", "stderr": f"list_repo_files 全部失败: {e} / {e2}", "returncode": 1}

    # 排除非必要的文件（onnx 多份权重只保留一种）
    skip_patterns = ["onnx/", ".gitattributes"]
    essentials = [f for f in files if not any(p in f for p in skip_patterns)]
    print(f"  需要下载 {len(essentials)} 个文件（跳过 {len(files)-len(essentials)} 个非必要文件）")

    total_bytes = 0
    stdout_lines = []
    success = True

    for filename in essentials:
        try:
            print(f"    下载 {filename}...", end="", flush=True)
            t0 = time.time()
            path = hf_hub_download(model_id, filename, cache_dir=cache_dir)
            elapsed = time.time() - t0
            size = os.path.getsize(path)
            total_bytes += size
            speed = size / elapsed / (1024*1024) if elapsed > 0 else 0
            size_str = f"{size/1024/1024:.1f}MB" if size > 1024*1024 else f"{size/1024:.0f}KB"
            print(f" {size_str} ({speed:.1f} MB/s)")
            stdout_lines.append(f"SAVED_TO:{path}")
        except Exception as e:
            print(f" 失败: {e}")
            success = False
            # 单个文件失败不影响整个下载（继续下一个）
            continue

    if success:
        # 找到最终的 snapshot 目录
        model_dir = os.path.join(cache_dir, f"models--{model_id.replace('/', '--')}", "snapshots")
        if os.path.isdir(model_dir):
            snaps = os.listdir(model_dir)
            if snaps:
                final_path = os.path.join(model_dir, snaps[0])
                stdout_lines.append(f"FINAL_PATH:{final_path}")

    return {
        "success": success,
        "stdout": "\n".join(stdout_lines),
        "stderr": "",
        "returncode": 0 if success else 1,
    }


def download_model(model_id, sources=None, max_retries_per_source=3, max_sources=5):
    """
    下载嵌入模型，支持多源切换和重试
    返回: {"success": bool, "path": str, "source": str, "details": str}
    """
    if sources is None:
        sources = [s["name"] for s in DOWNLOAD_SOURCES[:max_sources]]

    download_dir = os.path.join(cache_directory, "model_downloads")
    os.makedirs(download_dir, exist_ok=True)

    # 清理旧的不完整下载残留（确保断点续存能命中）
    blobs_dir = os.path.join(download_dir, f"models--{model_id.replace('/', '--')}", "blobs")
    if os.path.isdir(blobs_dir):
        cleaned = 0
        for fn in os.listdir(blobs_dir):
            if fn.endswith(".incomplete"):
                try:
                    os.remove(os.path.join(blobs_dir, fn))
                    cleaned += 1
                except OSError:
                    pass
        if cleaned:
            print(f"  清理旧不完整文件 {cleaned} 个")

    source_methods = {
        "modelscope": _download_with_modelscope,
        "hf_mirror": _download_with_hf_mirror,
        "hf_official": _download_with_hf_official,
        "hf_direct": _download_with_hf_direct,
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


def check_model_downloaded(model_id):
    """检查模型是否已下载"""
    models = list_downloaded_models()
    for m in models:
        if m["model_id"].lower() == model_id.lower():
            return True, m.get("path", "")
    return False, ""


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="嵌入模型管理工具")
    parser.add_argument("--download", type=str, help="下载模型（HuggingFace ID）")
    parser.add_argument("--interactive", action="store_true", help="交互式选择嵌入模型下载")
    parser.add_argument("--interactive-rerank", action="store_true", dest="interactive_rerank",
                        help="交互式选择 rerank/路由模型下载")
    parser.add_argument("--list", action="store_true", help="列出已下载模型")
    parser.add_argument("--list-rerank", action="store_true", dest="list_rerank",
                        help="列出已下载的 rerank/路由模型")
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

    elif args.list_rerank:
        models = list_downloaded_models()
        if args.json:
            print(json.dumps(models, ensure_ascii=False, indent=2))
        else:
            rerank_ids = {m["id"].lower() for m in RECOMMENDED_RERANK_MODELS}
            rerank_dl = [m for m in models if m["model_id"].lower() in rerank_ids or
                         any(r in m["model_id"].lower() for r in ["rerank", "reranker"])]
            if not rerank_dl:
                print("未下载任何 rerank/路由模型")
            else:
                print(f"已下载 rerank/路由模型 ({len(rerank_dl)}):")
                for m in rerank_dl:
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

    elif args.interactive_rerank:
        print("\n推荐 rerank/路由模型:")
        print("-" * 80)
        print(f"{'#':<3} {'模型 ID':<50} {'大小':<10} {'说明':<25}")
        print("-" * 80)
        for i, m in enumerate(RECOMMENDED_RERANK_MODELS, 1):
            print(f"{i:<3} {m['id']:<50} {m['size_mb']:<10} {m['desc']:<25}")
        print("-" * 80)
        print("0) 自定义模型 ID")

        try:
            choice = input("\n请选择 (0-{}): ".format(len(RECOMMENDED_RERANK_MODELS))).strip()
            if choice == "0":
                model_id = input("输入 HuggingFace 模型 ID: ").strip()
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(RECOMMENDED_RERANK_MODELS):
                    model_id = RECOMMENDED_RERANK_MODELS[idx]["id"]
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
