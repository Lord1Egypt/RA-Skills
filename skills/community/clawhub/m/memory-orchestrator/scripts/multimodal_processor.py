#!/usr/bin/env python3
"""
多模态记忆处理器
支持图像 (CLIP) 和音频 (Whisper) 的统一记忆存储与检索

功能:
- 图像 → CLIP 嵌入 → 存储
- 音频 → Whisper 转录 → 文本嵌入 → 存储
- 跨模态统一检索

依赖:
- sentence-transformers (CLIP + 文本嵌入)
- openai-whisper (音频转录)
- Pillow (图像处理)
- faiss (向量索引)
"""

import os
import sys
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, asdict
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
LOCAL_MEMORY_VENV = WORKSPACE / "skills" / "local-memory" / "venv"
MODELS_DIR = WORKSPACE / "skills" / "local-memory" / "models"
MEMORY_DIR = WORKSPACE / "memory"
MULTIMODAL_DIR = MEMORY_DIR / "multimodal"

# 添加 venv 到路径
if (LOCAL_MEMORY_VENV / "lib").exists():
    for p in (LOCAL_MEMORY_VENV / "lib").glob("python*"):
        site_packages = p / "site-packages"
        if site_packages.exists():
            sys.path.insert(0, str(site_packages))
            break

# 模型状态
MODEL_STATUS = {
    "clip": False,
    "whisper": False,
    "text_embedding": False
}

# 全局模型缓存
_MODELS = {}


@dataclass
class MultimodalEntry:
    """多模态记忆条目"""
    id: str
    type: str  # "image" | "audio"
    source: str
    timestamp: str
    embedding: List[float]
    metadata: Dict[str, Any]
    content: Optional[str] = None  # 音频转录文本或图像描述
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


def check_models() -> Dict[str, bool]:
    """检查模型可用性"""
    status = {"clip": False, "whisper": False, "text_embedding": False}
    
    # 检查 CLIP 模型
    clip_path = MODELS_DIR / "clip-ViT-B-32"
    if clip_path.exists() and any(clip_path.iterdir()):
        status["clip"] = True
    else:
        # 检查 HuggingFace 缓存
        cache_path = Path.home() / ".cache" / "huggingface"
        if cache_path.exists():
            status["clip"] = "partial"  # 可能需要下载
    
    # 检查 Whisper 模型
    whisper_cache = Path.home() / ".cache" / "whisper"
    if whisper_cache.exists():
        tiny_pt = whisper_cache / "tiny.pt"
        base_pt = whisper_cache / "base.pt"
        status["whisper"] = tiny_pt.exists() or base_pt.exists()
    
    # 检查文本嵌入模型
    text_model_path = MODELS_DIR / "all-MiniLM-L6-v2"
    if text_model_path.exists() and any(text_model_path.iterdir()):
        status["text_embedding"] = True
    
    return status


def load_text_embedding_model():
    """加载文本嵌入模型"""
    global _MODELS
    
    if "text_embedding" in _MODELS:
        return _MODELS["text_embedding"]
    
    try:
        from sentence_transformers import SentenceTransformer
        
        model_path = MODELS_DIR / "all-MiniLM-L6-v2"
        if model_path.exists():
            model = SentenceTransformer(str(model_path))
        else:
            logger.info("Downloading text embedding model...")
            model = SentenceTransformer('all-MiniLM-L6-v2')
        
        _MODELS["text_embedding"] = model
        MODEL_STATUS["text_embedding"] = True
        return model
        
    except Exception as e:
        logger.error(f"Failed to load text embedding model: {e}")
        return None


def load_clip_model():
    """加载 CLIP 图像嵌入模型"""
    global _MODELS
    
    if "clip" in _MODELS:
        return _MODELS["clip"]
    
    try:
        from sentence_transformers import SentenceTransformer
        
        model_path = MODELS_DIR / "clip-ViT-B-32"
        if model_path.exists() and any(model_path.iterdir()):
            logger.info(f"Loading CLIP from {model_path}")
            model = SentenceTransformer(str(model_path))
        else:
            logger.info("Downloading CLIP model (this may take a while)...")
            model = SentenceTransformer('clip-ViT-B-32')
            # 保存模型
            model_path.mkdir(parents=True, exist_ok=True)
            model.save(str(model_path))
        
        _MODELS["clip"] = model
        MODEL_STATUS["clip"] = True
        return model
        
    except Exception as e:
        logger.error(f"Failed to load CLIP model: {e}")
        return None


def load_whisper_model(model_size: str = "tiny"):
    """加载 Whisper 音频转录模型"""
    global _MODELS
    
    cache_key = f"whisper_{model_size}"
    if cache_key in _MODELS:
        return _MODELS[cache_key]
    
    try:
        import whisper
        
        logger.info(f"Loading Whisper {model_size} model...")
        model = whisper.load_model(model_size)
        
        _MODELS[cache_key] = model
        MODEL_STATUS["whisper"] = True
        return model
        
    except Exception as e:
        logger.error(f"Failed to load Whisper model: {e}")
        return None


def generate_id(file_path: str, entry_type: str) -> str:
    """生成唯一 ID"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    hash_part = hashlib.md5(file_path.encode()).hexdigest()[:8]
    return f"{entry_type}_{timestamp}_{hash_part}"


def extract_image_metadata(image_path: Path) -> Dict[str, Any]:
    """提取图像元数据"""
    metadata = {
        "filename": image_path.name,
        "source": str(image_path),
        "size": None,
        "format": None,
        "mode": None
    }
    
    try:
        from PIL import Image
        
        with Image.open(image_path) as img:
            metadata["size"] = img.size
            metadata["format"] = img.format
            metadata["mode"] = img.mode
            
            # 提取 EXIF 数据
            try:
                from PIL.ExifTags import TAGS
                exif = img._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag in ["DateTime", "Make", "Model"]:
                            metadata[tag.lower()] = str(value)
            except Exception:
                pass
                
    except Exception as e:
        logger.warning(f"Failed to extract image metadata: {e}")
    
    return metadata


def process_image(image_path: str, caption: Optional[str] = None) -> Optional[MultimodalEntry]:
    """
    处理图像文件
    生成 CLIP 嵌入并存储
    """
    image_path = Path(image_path)
    
    if not image_path.exists():
        logger.error(f"Image file not found: {image_path}")
        return None
    
    # 支持的图像格式
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    if image_path.suffix.lower() not in supported_formats:
        logger.error(f"Unsupported image format: {image_path.suffix}")
        return None
    
    # 加载 CLIP 模型
    clip_model = load_clip_model()
    if clip_model is None:
        logger.error("CLIP model not available")
        return None
    
    try:
        from PIL import Image
        import numpy as np
        
        # 提取元数据
        metadata = extract_image_metadata(image_path)
        
        # 生成图像嵌入
        with Image.open(image_path) as img:
            # 转换为 RGB (处理 RGBA 等格式)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            embedding = clip_model.encode(img, convert_to_tensor=False)
        
        # 生成描述（如果未提供）
        if caption is None:
            caption = f"Image: {metadata['filename']}"
            if 'datetime' in metadata:
                caption += f", taken on {metadata['datetime']}"
            if 'model' in metadata:
                caption += f", camera: {metadata['model']}"
        
        # 创建条目
        entry = MultimodalEntry(
            id=generate_id(str(image_path), "img"),
            type="image",
            source=str(image_path),
            timestamp=datetime.now().isoformat(),
            embedding=embedding.tolist(),
            metadata=metadata,
            content=caption
        )
        
        logger.info(f"Processed image: {image_path.name} (embedding dim: {len(embedding)})")
        return entry
        
    except Exception as e:
        logger.error(f"Failed to process image: {e}")
        return None


def process_audio(audio_path: str, language: str = "zh", model_size: str = "tiny") -> Optional[MultimodalEntry]:
    """
    处理音频文件
    使用 Whisper 转录并生成文本嵌入
    """
    audio_path = Path(audio_path)
    
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        return None
    
    # 支持的音频格式
    supported_formats = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.webm'}
    if audio_path.suffix.lower() not in supported_formats:
        logger.error(f"Unsupported audio format: {audio_path.suffix}")
        return None
    
    # 加载 Whisper 模型
    whisper_model = load_whisper_model(model_size)
    if whisper_model is None:
        logger.error("Whisper model not available")
        return None
    
    # 加载文本嵌入模型
    text_model = load_text_embedding_model()
    if text_model is None:
        logger.error("Text embedding model not available")
        return None
    
    try:
        import numpy as np
        
        # Whisper 转录
        logger.info(f"Transcribing audio: {audio_path.name}")
        result = whisper_model.transcribe(str(audio_path), language=language)
        
        transcript = result.get("text", "")
        segments = result.get("segments", [])
        
        # 计算音频时长
        duration = sum(s.get("end", 0) - s.get("start", 0) for s in segments)
        
        # 生成文本嵌入
        embedding = text_model.encode(transcript, convert_to_tensor=False)
        
        # 创建条目
        entry = MultimodalEntry(
            id=generate_id(str(audio_path), "audio"),
            type="audio",
            source=str(audio_path),
            timestamp=datetime.now().isoformat(),
            embedding=embedding.tolist(),
            metadata={
                "filename": audio_path.name,
                "duration": duration,
                "language": language,
                "segment_count": len(segments)
            },
            content=transcript
        )
        
        logger.info(f"Processed audio: {audio_path.name} ({duration:.1f}s, {len(transcript)} chars)")
        return entry
        
    except Exception as e:
        logger.error(f"Failed to process audio: {e}")
        return None


def store_entry(entry: MultimodalEntry, output_dir: Optional[Path] = None) -> bool:
    """存储多模态条目到 JSONL 文件"""
    if output_dir is None:
        output_dir = MULTIMODAL_DIR / f"{entry.type}s"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "index.jsonl"
    
    try:
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
        
        logger.info(f"Stored entry: {entry.id} -> {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to store entry: {e}")
        return False


def search_multimodal(query: str, top_k: int = 5, modalities: List[str] = None) -> List[Dict[str, Any]]:
    """
    跨模态搜索
    使用文本查询检索文本/图像/音频记忆
    """
    if modalities is None:
        modalities = ["text", "image", "audio"]
    
    results = []
    
    # 文本模态搜索
    if "text" in modalities:
        text_results = search_text(query, top_k)
        results.extend(text_results)
    
    # 音频模态搜索 (使用文本嵌入)
    if "audio" in modalities:
        audio_results = search_audio(query, top_k)
        results.extend(audio_results)
    
    # 图像模态搜索 (使用 CLIP 文本编码)
    if "image" in modalities:
        image_results = search_image(query, top_k)
        results.extend(image_results)
    
    # 按分数排序
    results.sort(key=lambda x: x.get("score", float('inf')))
    
    return results[:top_k]


def search_text(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """搜索文本记忆"""
    results = []
    
    try:
        import faiss
        import numpy as np
        
        text_model = load_text_embedding_model()
        if text_model is None:
            return results
        
        # 编码查询
        query_emb = text_model.encode([query])
        
        # 加载文本索引
        index_path = WORKSPACE / "index" / "memory_index.faiss"
        meta_path = WORKSPACE / "index" / "metadata.json"
        
        if index_path.exists() and meta_path.exists():
            index = faiss.read_index(str(index_path))
            with open(meta_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            scores, indices = index.search(query_emb.astype(np.float32), top_k)
            
            for idx, score in zip(indices[0], scores[0]):
                if idx >= 0 and idx < len(metadata):
                    results.append({
                        "type": "text",
                        "source": metadata[idx].get("source", "unknown"),
                        "score": float(score),
                        "similarity": 1 / (1 + float(score))
                    })
        
    except Exception as e:
        logger.warning(f"Text search failed: {e}")
    
    return results


def search_audio(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """搜索音频记忆"""
    results = []
    
    try:
        import faiss
        import numpy as np
        
        text_model = load_text_embedding_model()
        if text_model is None:
            return results
        
        # 编码查询
        query_emb = text_model.encode([query])
        
        # 加载音频索引
        index_path = MULTIMODAL_DIR / "audio" / "index.faiss"
        data_path = MULTIMODAL_DIR / "audio" / "index.jsonl"
        
        if not index_path.exists() or not data_path.exists():
            return results
        
        # 加载音频数据
        entries = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                entries.append(json.loads(line))
        
        if not entries:
            return results
        
        index = faiss.read_index(str(index_path))
        scores, indices = index.search(query_emb.astype(np.float32), min(top_k, len(entries)))
        
        for idx, score in zip(indices[0], scores[0]):
            if idx >= 0 and idx < len(entries):
                entry = entries[idx]
                results.append({
                    "type": "audio",
                    "source": entry.get("source", "unknown"),
                    "transcript_preview": entry.get("content", "")[:100] + "...",
                    "score": float(score),
                    "similarity": 1 / (1 + float(score))
                })
        
    except Exception as e:
        logger.warning(f"Audio search failed: {e}")
    
    return results


def search_image(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """搜索图像记忆 (使用 CLIP 文本编码)"""
    results = []
    
    try:
        import faiss
        import numpy as np
        
        clip_model = load_clip_model()
        if clip_model is None:
            return results
        
        # 使用 CLIP 文本编码
        query_emb = clip_model.encode([query])
        
        # 加载图像索引
        index_path = MULTIMODAL_DIR / "images" / "index.faiss"
        data_path = MULTIMODAL_DIR / "images" / "index.jsonl"
        
        if not index_path.exists() or not data_path.exists():
            return results
        
        # 加载图像数据
        entries = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                entries.append(json.loads(line))
        
        if not entries:
            return results
        
        index = faiss.read_index(str(index_path))
        scores, indices = index.search(query_emb.astype(np.float32), min(top_k, len(entries)))
        
        for idx, score in zip(indices[0], scores[0]):
            if idx >= 0 and idx < len(entries):
                entry = entries[idx]
                results.append({
                    "type": "image",
                    "source": entry.get("source", "unknown"),
                    "caption": entry.get("content", "N/A"),
                    "score": float(score),
                    "similarity": 1 / (1 + float(score))
                })
        
    except Exception as e:
        logger.warning(f"Image search failed: {e}")
    
    return results


def build_index(modality: str = "all"):
    """
    为多模态数据构建 FAISS 索引
    """
    try:
        import faiss
        import numpy as np
    except ImportError:
        logger.error("FAISS not installed")
        return False
    
    success = True
    
    if modality in ["all", "image"]:
        success &= _build_index_for_type("image")
    
    if modality in ["all", "audio"]:
        success &= _build_index_for_type("audio")
    
    return success


def _build_index_for_type(entry_type: str) -> bool:
    """为指定类型构建索引"""
    data_path = MULTIMODAL_DIR / f"{entry_type}s" / "index.jsonl"
    index_path = MULTIMODAL_DIR / f"{entry_type}s" / "index.faiss"
    
    if not data_path.exists():
        logger.info(f"No data found for {entry_type}")
        return True
    
    # 读取所有条目
    entries = []
    embeddings = []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            if "embedding" in entry:
                entries.append(entry)
                embeddings.append(entry["embedding"])
    
    if not embeddings:
        logger.info(f"No embeddings found for {entry_type}")
        return True
    
    # 构建 FAISS 索引
    embeddings_array = np.array(embeddings, dtype=np.float32)
    dimension = embeddings_array.shape[1]
    
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_array)
    
    # 保存索引
    faiss.write_index(index, str(index_path))
    
    logger.info(f"Built {entry_type} index: {len(entries)} entries, dimension {dimension}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="多模态记忆处理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 处理图像
  python multimodal_processor.py image /path/to/image.jpg
  
  # 处理音频
  python multimodal_processor.py audio /path/to/audio.mp3 --language zh
  
  # 搜索
  python multimodal_processor.py search "今天的会议内容" --top-k 5
  
  # 构建索引
  python multimodal_processor.py build-index --modality all
  
  # 检查模型状态
  python multimodal_processor.py status
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 图像处理命令
    image_parser = subparsers.add_parser("image", help="处理图像文件")
    image_parser.add_argument("path", help="图像文件路径")
    image_parser.add_argument("--caption", help="自定义描述")
    
    # 音频处理命令
    audio_parser = subparsers.add_parser("audio", help="处理音频文件")
    audio_parser.add_argument("path", help="音频文件路径")
    audio_parser.add_argument("--language", default="zh", help="音频语言 (默认: zh)")
    audio_parser.add_argument("--model", default="tiny", choices=["tiny", "base", "small", "medium"], help="Whisper 模型大小")
    
    # 搜索命令
    search_parser = subparsers.add_parser("search", help="跨模态搜索")
    search_parser.add_argument("query", help="搜索查询")
    search_parser.add_argument("--top-k", type=int, default=5, help="返回结果数量")
    search_parser.add_argument("--modalities", nargs="+", default=["text", "audio", "image"], help="搜索模态")
    
    # 构建索引命令
    build_parser = subparsers.add_parser("build-index", help="构建向量索引")
    build_parser.add_argument("--modality", default="all", choices=["all", "image", "audio"], help="索引类型")
    
    # 状态检查命令
    subparsers.add_parser("status", help="检查模型状态")
    
    args = parser.parse_args()
    
    if args.command == "status":
        status = check_models()
        print("\n📊 模型状态检查")
        print("=" * 40)
        for model, available in status.items():
            icon = "✅" if available == True else "⚠️" if available == "partial" else "❌"
            print(f"  {icon} {model}: {'可用' if available == True else '部分可用' if available == 'partial' else '未安装'}")
        print()
        
    elif args.command == "image":
        entry = process_image(args.path, args.caption)
        if entry:
            store_entry(entry)
            print(f"✅ 图像处理完成: {entry.id}")
        else:
            print("❌ 图像处理失败")
            sys.exit(1)
            
    elif args.command == "audio":
        entry = process_audio(args.path, args.language, args.model)
        if entry:
            store_entry(entry)
            print(f"✅ 音频处理完成: {entry.id}")
            print(f"📝 转录文本: {entry.content[:200]}...")
        else:
            print("❌ 音频处理失败")
            sys.exit(1)
            
    elif args.command == "search":
        results = search_multimodal(args.query, args.top_k, args.modalities)
        
        print(f"\n🔍 搜索结果: \"{args.query}\"")
        print("=" * 60)
        
        if not results:
            print("❌ 未找到相关结果")
        else:
            for i, r in enumerate(results, 1):
                print(f"\n{i}. [{r['type'].upper()}] {r['source']}")
                if 'transcript_preview' in r:
                    print(f"   📝 {r['transcript_preview']}")
                if 'caption' in r:
                    print(f"   🖼️ {r['caption']}")
                print(f"   📊 相似度: {r['similarity']:.2%}")
                
    elif args.command == "build-index":
        if build_index(args.modality):
            print(f"✅ 索引构建完成: {args.modality}")
        else:
            print("❌ 索引构建失败")
            sys.exit(1)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
