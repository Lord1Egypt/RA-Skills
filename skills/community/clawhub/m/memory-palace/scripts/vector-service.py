#!/usr/bin/env python3
"""
Vector Service for Memory Palace

A lightweight HTTP service for vector embeddings using BGE-small-zh-v1.5 model.
Provides encoding and similarity search capabilities.

Usage:
    python vector-service.py [--port 8765] [--host 127.0.0.1]

API Endpoints:
    POST /encode - Encode texts to vectors
    POST /search - Search similar documents
    POST /index - Index a document
    POST /remove - Remove from index
    GET /health - Health check
"""

import argparse
import json
import os
import sqlite3
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
import numpy as np
from sentence_transformers import SentenceTransformer

# Global model and database
model: Optional[SentenceTransformer] = None
db_path: Optional[str] = None
db_conn: Optional[sqlite3.Connection] = None


def get_db_path() -> str:
    """Get database path from environment or default."""
    return os.environ.get('VECTOR_DB_PATH', '/data/agent-memory-palace/data/vectors.db')


def check_db_path_writable(db_path: str) -> None:
    """Check if database path is writable, raise clear error if not."""
    db_dir = os.path.dirname(db_path)
    
    # Ensure directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Check if directory exists and is writable
    if os.path.exists(db_dir):
        if not os.access(db_dir, os.W_OK):
            raise PermissionError(
                f"Database directory is not writable: {db_dir}\n"
                f"Please check permissions or specify a different path with --db-path"
            )
    else:
        # Try to create the directory
        try:
            os.makedirs(db_dir, exist_ok=True)
        except PermissionError as e:
            raise PermissionError(
                f"Cannot create database directory: {db_dir}\n"
                f"Error: {e}\n"
                f"Please check permissions or specify a different path with --db-path"
            )


def init_db():
    """Initialize SQLite database for vector storage."""
    global db_conn, db_path
    db_path = get_db_path()
    
    # Check if path is writable before proceeding
    check_db_path_writable(db_path)
    
    db_conn = sqlite3.connect(db_path, check_same_thread=False)
    db_conn.execute('''
        CREATE TABLE IF NOT EXISTS vectors (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            embedding BLOB NOT NULL,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db_conn.execute('CREATE INDEX IF NOT EXISTS idx_vectors_created ON vectors(created_at)')
    db_conn.commit()


def get_model_cache_dir() -> str:
    """Get model cache directory from environment or use project default."""
    # Check environment variable first
    if 'BGE_MODEL_CACHE_DIR' in os.environ:
        cache_dir = os.environ['BGE_MODEL_CACHE_DIR']
    else:
        # Default to project directory under model_cache/
        project_dir = '/data/agent-memory-palace'
        cache_dir = os.path.join(project_dir, 'model_cache')
    
    # Ensure directory exists
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def get_model_path() -> str:
    """Get model path from environment or use local cached model."""
    # Check environment variable first
    model_path = os.environ.get('BGE_MODEL_PATH')
    if model_path and os.path.exists(model_path):
        return model_path
    # Default local model path
    local_model = os.path.expanduser('~/.openclaw/models/embedding/bge-small-zh-v1.5')
    if os.path.exists(local_model):
        return local_model
    # Fallback to HuggingFace model name (requires network)
    return 'BAAI/bge-small-zh-v1.5'


def load_model():
    """Load the BGE model with custom cache directory."""
    global model
    
    # Get model path (local or HuggingFace)
    model_path = get_model_path()
    
    # Use mirror if huggingface.co is unreachable and model is not local
    if not os.path.exists(model_path) and 'HF_ENDPOINT' not in os.environ:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    
    print(f"Loading model: {model_path}", file=sys.stderr, flush=True)
    
    # Load model (local path or HuggingFace name)
    model = SentenceTransformer(model_path)
    print(f"Model loaded. Embedding dimension: {model.get_sentence_embedding_dimension()}", 
          file=sys.stderr, flush=True)


def encode_texts(texts: list[str]) -> list[list[float]]:
    """Encode texts to vectors."""
    if model is None:
        raise RuntimeError("Model not loaded")
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return float(np.dot(vec1, vec2))


def search_similar(query_embedding: list[float], top_k: int = 10, 
                   filter_dict: Optional[dict] = None) -> list[dict]:
    """Search for similar documents."""
    if db_conn is None:
        raise RuntimeError("Database not initialized")
    
    query_vec = np.array(query_embedding, dtype=np.float32)
    
    cursor = db_conn.execute('SELECT id, content, embedding, metadata FROM vectors')
    results = []
    
    for row in cursor:
        id_, content, embedding_blob, metadata_json = row
        doc_vec = np.frombuffer(embedding_blob, dtype=np.float32)
        
        # Apply filters if provided
        if filter_dict and metadata_json:
            metadata = json.loads(metadata_json)
            skip = False
            for key, value in filter_dict.items():
                if key in metadata:
                    if isinstance(value, list):
                        # Check if any filter value matches
                        if not any(v in metadata[key] for v in value):
                            skip = True
                            break
                    elif metadata[key] != value:
                        skip = True
                        break
            if skip:
                continue
        
        similarity = cosine_similarity(query_vec, doc_vec)
        results.append({
            'id': id_,
            'score': similarity,
            'metadata': json.loads(metadata_json) if metadata_json else None
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]


def index_document(id_: str, content: str, metadata: Optional[dict] = None):
    """Index a document."""
    if db_conn is None:
        raise RuntimeError("Database not initialized")
    if model is None:
        raise RuntimeError("Model not loaded")
    
    # Generate embedding
    embedding = model.encode([content], normalize_embeddings=True)[0]
    embedding_blob = embedding.astype(np.float32).tobytes()
    
    # Store in database
    metadata_json = json.dumps(metadata) if metadata else None
    db_conn.execute('''
        INSERT OR REPLACE INTO vectors (id, content, embedding, metadata)
        VALUES (?, ?, ?, ?)
    ''', (id_, content, embedding_blob, metadata_json))
    db_conn.commit()


def remove_document(id_: str):
    """Remove a document from the index."""
    if db_conn is None:
        raise RuntimeError("Database not initialized")
    
    db_conn.execute('DELETE FROM vectors WHERE id = ?', (id_,))
    db_conn.commit()


class VectorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for vector service."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def send_json_response(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def read_json_body(self) -> dict:
        """Read JSON body from request."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        return json.loads(body.decode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self.send_json_response({
                'status': 'ok',
                'model': os.environ.get('BGE_MODEL', 'BAAI/bge-small-zh-v1.5'),
                'dimension': model.get_sentence_embedding_dimension() if model else None
            })
        else:
            self.send_json_response({'error': 'Not found'}, 404)
    
    def do_POST(self):
        """Handle POST requests."""
        try:
            if self.path == '/encode':
                data = self.read_json_body()
                texts = data.get('texts', [])
                if not texts:
                    self.send_json_response({'error': 'texts required'}, 400)
                    return
                embeddings = encode_texts(texts)
                self.send_json_response({'embeddings': embeddings})
            
            elif self.path == '/search':
                data = self.read_json_body()
                query = data.get('query')
                top_k = data.get('topK', 10)
                filter_dict = data.get('filter')
                
                if not query:
                    self.send_json_response({'error': 'query required'}, 400)
                    return
                
                # Encode query
                query_embedding = encode_texts([query])[0]
                # Search
                results = search_similar(query_embedding, top_k, filter_dict)
                self.send_json_response({'results': results})
            
            elif self.path == '/index':
                data = self.read_json_body()
                id_ = data.get('id')
                content = data.get('content')
                metadata = data.get('metadata')
                
                if not id_ or not content:
                    self.send_json_response({'error': 'id and content required'}, 400)
                    return
                
                index_document(id_, content, metadata)
                self.send_json_response({'status': 'indexed', 'id': id_})
            
            elif self.path == '/remove':
                data = self.read_json_body()
                id_ = data.get('id')
                
                if not id_:
                    self.send_json_response({'error': 'id required'}, 400)
                    return
                
                remove_document(id_)
                self.send_json_response({'status': 'removed', 'id': id_})
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except json.JSONDecodeError:
            self.send_json_response({'error': 'Invalid JSON'}, 400)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)


def main():
    global model, db_conn
    
    parser = argparse.ArgumentParser(description='Vector Service for Memory Palace')
    parser.add_argument('--port', type=int, default=8765, help='Port to listen on')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--db-path', type=str, default=None, help='Custom database path for vector storage')
    args = parser.parse_args()
    
    # Set custom DB path if provided
    if args.db_path:
        os.environ['VECTOR_DB_PATH'] = args.db_path
    
    # Initialize
    print("Initializing vector service...", file=sys.stderr, flush=True)
    load_model()
    init_db()
    
    # Start server
    server = HTTPServer((args.host, args.port), VectorHandler)
    print(f"Vector service running on http://{args.host}:{args.port}", 
          file=sys.stderr, flush=True)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...", file=sys.stderr, flush=True)
        server.shutdown()
        if db_conn:
            db_conn.close()


if __name__ == '__main__':
    main()