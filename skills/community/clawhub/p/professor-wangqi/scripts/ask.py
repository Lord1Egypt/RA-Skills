"""
Wang Qi Professor TCM Constitution Assistant - Q&A Script

Usage:
    python ask.py "question"
    python ask.py --interactive
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from typing import Tuple, Optional
from chroma_compat import list_collection_names
from runtime_paths import DEFAULT_PERSIST_DIR, DEFAULT_SKILL_PATH, load_runtime_env

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load .env config
load_runtime_env()

try:
    import chromadb
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


def get_chat_client():
    """Get Chat model client"""
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    model = os.getenv("MODEL_NAME", "qwen/qwen3.6-35b-a3b")
    
    print(f"Chat model: {model}")
    print(f"Chat service: {base_url}")
    
    return OpenAI(api_key=api_key, base_url=base_url), model


class LocalEmbeddingFunction:
    """Local Embedding Function"""

    def __init__(self):
        api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
        base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
        self.max_retries = int(os.getenv("EMBEDDING_MAX_RETRIES", "2"))
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self._name = "local_embedding"

    @property
    def name(self):
        return self._name

    def __call__(self, input):
        embeddings = []
        for text in input:
            last_error = None
            for attempt in range(self.max_retries + 1):
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=[text]
                    )
                    embeddings.append(response.data[0].embedding)
                    last_error = None
                    break
                except Exception as e:
                    last_error = e
                    if attempt < self.max_retries:
                        time.sleep(attempt + 1)
            if last_error is not None:
                # Fail loudly - don't silently return zero vectors
                # This prevents the system from giving seemingly valid but 
                # actually irrelevant answers when embedding service is down
                raise RuntimeError(
                    f"Embedding service failed: {last_error}\n"
                    f"Please check:\n"
                    f"  1. Is the embedding service running at {self.client.base_url}?\n"
                    f"  2. Is the model '{self.model}' available?\n"
                    f"  3. Check EMBEDDING_BASE_URL and EMBEDDING_API_KEY in .env"
                )
        return embeddings


def retrieve_context(query: str, collection_name: str, persist_dir: str, n_results: int = 5) -> Tuple[str, int]:
    """
    Retrieve relevant context from ChromaDB
    
    Returns:
        Tuple of (context_string, retrieval_count)
    """
    if not HAS_CHROMA:
        logger.warning("ChromaDB not available")
        return "", 0

    try:
        start_time = time.time()
        
        # Check if persist directory exists
        if not Path(persist_dir).exists():
            logger.error(f"ChromaDB directory not found: {persist_dir}")
            logger.info("Run: python scripts/build_local_index.py to create the index")
            return "", 0
        
        client = chromadb.PersistentClient(path=persist_dir)
        
        # Check if collection exists
        collections = list_collection_names(client.list_collections())
        if collection_name not in collections:
            logger.error(f"Collection '{collection_name}' not found")
            logger.info(f"Available collections: {collections}")
            logger.info("Run: python scripts/build_local_index.py to create the index")
            return "", 0
        
        collection = client.get_collection(name=collection_name)
        
        # Check if collection has documents
        doc_count = collection.count()
        if doc_count == 0:
            logger.warning(f"Collection '{collection_name}' is empty")
            logger.info("Run: python scripts/build_local_index.py to populate the index")
            return "", 0

        # Generate query embedding
        logger.debug(f"Generating embedding for query: {query[:50]}...")
        embedding_func = LocalEmbeddingFunction()
        query_embedding = embedding_func([query])[0]

        # Query with manually generated embedding
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Process results
        contexts = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            source_type = meta.get("source_type", "")
            title = meta.get("title", "")
            evidence_tag = "[论文]" if source_type == "paper" else "[诊疗经验]"
            contexts.append(f"{evidence_tag} {title}\n{doc}")
        
        elapsed = time.time() - start_time
        logger.info(f"Retrieved {len(contexts)} documents in {elapsed:.2f}s")
        
        return "\n\n---\n\n".join(contexts), len(contexts)
    
    except chromadb.errors.InvalidCollectionException as e:
        logger.error(f"Invalid collection: {e}")
        logger.info("The collection may be corrupted. Try rebuilding the index.")
        return "", 0
    
    except Exception as e:
        logger.error(f"Retrieval error: {type(e).__name__}: {e}")
        logger.debug("Full error details:", exc_info=True)
        return "", 0


def load_skill_instruction(skill_path: str) -> str:
    """Load SKILL.md as system instruction"""
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()
    
    return content


def ask(
    question: str,
    skill_path: str = None,
    collection_name: str = "wangqi_knowledge",
    persist_dir: str = None,
    n_results: int = 5,
    verbose: bool = True
) -> Tuple[str, int]:
    """
    Ask Wang Qi Professor Academic Assistant
    
    Args:
        question: User question
        skill_path: SKILL.md path
        collection_name: ChromaDB collection name
        persist_dir: ChromaDB persist directory
        n_results: Number of results to retrieve
        verbose: Print progress messages
    
    Returns:
        Tuple of (answer_text, retrieval_count)
    """
    # Set defaults
    if skill_path is None:
        skill_path = DEFAULT_SKILL_PATH
    if persist_dir is None:
        persist_dir = DEFAULT_PERSIST_DIR
    
    if not HAS_OPENAI:
        raise RuntimeError("openai package is required. Install with: pip install openai")
    
    start_time = time.time()
    
    # 1. Load system instruction
    if verbose:
        logger.info("Loading skill instructions...")
    skill_instruction = load_skill_instruction(skill_path)
    
    # 2. Retrieve relevant context
    context, retrieval_count = retrieve_context(question, collection_name, persist_dir, n_results)
    
    if verbose:
        if retrieval_count > 0:
            print(f"\nRetrieved {retrieval_count} relevant documents")
        else:
            print("\nWarning: No context retrieved - answering from general knowledge")
    
    # 3. Build prompt
    system_prompt = skill_instruction
    
    user_prompt = f"""Please answer the following question based on the provided reference materials. Cite sources.

## Reference Materials
{context if context else "(未找到相关材料，请根据一般知识回答并标注为[模型推断])"}

## Question
{question}

## Answer Requirements
1. 每个学术观点必须标注出处（[论文]、[诊疗经验]、[知识归纳]或[模型推断]）
2. 区分教授原文论述与模型推断
3. 如果材料不足，明确说明
4. 涉及诊断或剂量问题时，添加安全警示
"""
    
    # 4. Call LLM
    client, model = get_chat_client()
    
    if verbose:
        print(f"\nGenerating response...")
    
    try:
        llm_start = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=8000  # Increased for longer responses
        )
        llm_elapsed = time.time() - llm_start
        
        if verbose:
            logger.info(f"LLM response generated in {llm_elapsed:.2f}s")
        
        # Handle Qwen3.x thinking mode - content may be in reasoning_content
        content = response.choices[0].message.content
        if not content:
            # Qwen3.x returns thinking in reasoning_content field
            reasoning = getattr(response.choices[0].message, 'reasoning_content', None)
            if reasoning:
                content = reasoning
            else:
                content = "(Model returned empty response)"
        
        total_elapsed = time.time() - start_time
        if verbose:
            logger.info(f"Total time: {total_elapsed:.2f}s")
        
        return content, retrieval_count
    
    except Exception as e:
        logger.error(f"LLM error: {type(e).__name__}: {e}")
        raise


def interactive_mode(
    skill_path: str = None,
    collection_name: str = "wangqi_knowledge",
    persist_dir: str = None
):
    """Interactive mode"""
    # Set defaults
    if skill_path is None:
        skill_path = DEFAULT_SKILL_PATH
    if persist_dir is None:
        persist_dir = DEFAULT_PERSIST_DIR
    
    print("=" * 60)
    print("Wang Qi Professor TCM Constitution Assistant")
    print("=" * 60)
    print("Type your question, or 'quit'/'exit' to exit")
    print()
    
    while True:
        try:
            question = input("Question: ").strip()
            
            if question.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            if not question:
                continue
            
            answer, retrieval_count = ask(
                question=question,
                skill_path=skill_path,
                collection_name=collection_name,
                persist_dir=persist_dir
            )
            
            print("\n" + "=" * 60)
            print("Answer:")
            print("=" * 60)
            print(answer)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nError: {e}")


def main():
    parser = argparse.ArgumentParser(description="Ask Wang Qi Professor Academic Assistant")
    parser.add_argument("question", nargs="?", help="Question to ask")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--skill", default=DEFAULT_SKILL_PATH, help="SKILL.md path")
    parser.add_argument("--collection", default="wangqi_knowledge", help="Collection name")
    parser.add_argument("--persist-dir", default=DEFAULT_PERSIST_DIR, help="ChromaDB persist directory")
    parser.add_argument("--n-results", type=int, default=5, help="Number of results to retrieve")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode(
            skill_path=args.skill,
            collection_name=args.collection,
            persist_dir=args.persist_dir
        )
    elif args.question:
        answer, retrieval_count = ask(
            question=args.question,
            skill_path=args.skill,
            collection_name=args.collection,
            persist_dir=args.persist_dir,
            n_results=args.n_results
        )
        print("\n" + "=" * 60)
        print("Answer:")
        print("=" * 60)
        print(answer)
    else:
        parser.print_help()


if __name__ == "__main__":
    # Fix Windows console encoding
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    main()
