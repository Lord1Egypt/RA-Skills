"""
上传知识卡到向量存储并支持问答

功能：
1. 递归扫描知识卡目录
2. 上传到向量存储（支持OpenAI或本地LM Studio）
3. 返回vector_store_id用于后续问答

配置：
- 从项目根目录的.env读取配置
- 支持本地LM Studio（OpenAI兼容接口）

使用：
    python upload_to_openai.py --cards data/cards/ --name wangqi-knowledge
"""

import os
import argparse
from pathlib import Path
from typing import Optional
from runtime_paths import (
    DEFAULT_CARDS_DIR,
    DEFAULT_SKILL_PATH,
    DEFAULT_VECTOR_STORE_ID_PATH,
    load_runtime_env,
)

# 加载.env配置
load_runtime_env()

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("ERROR: openai package is required. Install with: pip install openai")


def get_client() -> OpenAI:
    """
    获取OpenAI客户端（支持本地LM Studio）
    
    从.env读取配置：
    - API_KEY / BASE_URL: Chat模型
    - EMBEDDING_API_KEY / EMBEDDING_BASE_URL: Embedding模型
    """
    if not HAS_OPENAI:
        raise RuntimeError("openai package is required")
    
    # 优先使用EMBEDDING配置，fallback到通用配置
    api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
    base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
    
    # 如果BASE_URL存在，说明是本地服务
    if base_url:
        print(f"Using local service: {base_url}")
        return OpenAI(api_key=api_key, base_url=base_url)
    else:
        # 使用官方OpenAI
        print("Using OpenAI official API")
        return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def get_chat_client() -> OpenAI:
    """获取Chat模型客户端"""
    if not HAS_OPENAI:
        raise RuntimeError("openai package is required")
    
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    else:
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def upload_cards_to_openai(
    cards_dir: str,
    vector_store_name: str = "wangqi-knowledge",
    api_key: Optional[str] = None
) -> str:
    """
    上传知识卡到OpenAI Vector Store
    
    注意：此脚本仅适用于官方OpenAI API，不支持本地LM Studio
    
    Args:
        cards_dir: 知识卡目录（递归扫描）
        vector_store_name: Vector Store名称
        api_key: OpenAI API密钥
    
    Returns:
        vector_store_id
    """
    if not HAS_OPENAI:
        raise RuntimeError("openai package is required")
    
    # 检查是否使用本地服务
    base_url = os.getenv("BASE_URL")
    if base_url and "openai.com" not in base_url:
        print("ERROR: This script only works with official OpenAI API.")
        print(f"Current BASE_URL: {base_url}")
        print("For local LLM, use build_local_index.py with ChromaDB instead.")
        return ""
    
    # 使用官方OpenAI
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set. Please set it in .env or pass --api-key")
        return ""
    
    client = OpenAI(api_key=api_key)
    
    # 1. 创建Vector Store
    print(f"Creating vector store: {vector_store_name}")
    vector_store = client.vector_stores.create(
        name=vector_store_name,
        expires_after={"anchor": "last_active_at", "days": 30}  # 30天无活动后过期
    )
    print(f"Vector store created: {vector_store.id}")
    
    # 2. 递归扫描知识卡
    cards_path = Path(cards_dir)
    card_files = list(cards_path.rglob("*.json"))
    print(f"Found {len(card_files)} knowledge cards")
    
    if not card_files:
        print("WARNING: No knowledge cards found!")
        return vector_store.id
    
    # 3. 上传文件
    uploaded_count = 0
    for i, card_file in enumerate(card_files, 1):
        try:
            print(f"Uploading [{i}/{len(card_files)}]: {card_file.name}")
            
            with open(card_file, "rb") as f:
                # 使用upload_and_poll等待处理完成
                result = client.vector_stores.files.upload_and_poll(
                    vector_store_id=vector_store.id,
                    file=f
                )
            
            if result.status == "completed":
                uploaded_count += 1
            else:
                print(f"  WARNING: File processing status: {result.status}")
                
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
    
    print(f"\nUpload complete: {uploaded_count}/{len(card_files)} files")
    print(f"Vector Store ID: {vector_store.id}")
    
    return vector_store.id


def test_query(vector_store_id: str, question: str, skill_path: str = DEFAULT_SKILL_PATH):
    """
    测试问答功能
    
    Args:
        vector_store_id: Vector Store ID
        question: 测试问题
        skill_path: SKILL.md路径
    """
    client = OpenAI()
    
    # 读取SKILL.md作为系统指令
    with open(skill_path, "r", encoding="utf-8") as f:
        system_instruction = f.read()
    
    print(f"\nQuestion: {question}")
    print("-" * 50)
    
    response = client.responses.create(
        model="gpt-4o",
        instructions=system_instruction,
        input=question,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }]
    )
    
    print(response.output_text)


def main():
    parser = argparse.ArgumentParser(description="Upload knowledge cards to OpenAI Vector Store")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Knowledge cards directory")
    parser.add_argument("--name", default="wangqi-knowledge", help="Vector store name")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env)")
    parser.add_argument("--test", help="Test query after upload")
    parser.add_argument("--skill", default=DEFAULT_SKILL_PATH, help="SKILL.md path for test query")
    parser.add_argument("--id-file", default=DEFAULT_VECTOR_STORE_ID_PATH, help="Path to save vector store ID")
    
    args = parser.parse_args()
    
    # 上传
    vector_store_id = upload_cards_to_openai(
        cards_dir=args.cards,
        vector_store_name=args.name,
        api_key=args.api_key
    )
    
    # 保存ID到文件
    id_file = Path(args.id_file)
    id_file.parent.mkdir(parents=True, exist_ok=True)
    with open(id_file, "w", encoding="utf-8") as f:
        f.write(vector_store_id)
    print(f"\nVector Store ID saved to {id_file}")
    
    # 测试查询
    if args.test:
        test_query(vector_store_id, args.test, args.skill)


if __name__ == "__main__":
    main()
