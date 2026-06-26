import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import os

# 中文分词
def chinese_tokenizer(text):
    return jieba.lcut(text)

class EmbeddingModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_vectorizer()
        return cls._instance
    
    def _init_vectorizer(self):
        """初始化TF-IDF向量器，纯本地，不需要联网下载模型"""
        print("初始化TF-IDF中文向量器...")
        self.vectorizer = TfidfVectorizer(
            tokenizer=chinese_tokenizer,
            max_features=10000,  # 最大词表大小
            ngram_range=(1, 2),  # 1-2元语法
            stop_words=self._load_stop_words()
        )
        # 预热向量器
        self.vectorizer.fit(["这是一个测试文本，用于初始化TF-IDF向量器"])
        self.dimension = len(self.vectorizer.get_feature_names_out())
        print(f"向量器初始化完成，维度: {self.dimension}")
    
    def _load_stop_words(self):
        """加载常用中文停用词"""
        stop_words = [
            '的', '了', '和', '是', '在', '我', '有', '就', '也', '都', '要', '这个', '那个',
            '可以', '就是', '我们', '你们', '他们', '它们', '哦', '嗯', '啊', '吧', '呢', '吗'
        ]
        return stop_words
    
    def encode(self, text, normalize=True):
        """文本转向量"""
        if not text or not isinstance(text, str):
            return np.zeros(self.dimension, dtype=np.float32)
        
        # 预处理文本
        text = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', text)
        if not text.strip():
            return np.zeros(self.dimension, dtype=np.float32)
        
        # 生成TF-IDF向量
        vector = self.vectorizer.transform([text]).toarray()[0]
        if normalize and np.linalg.norm(vector) > 0:
            vector = vector / np.linalg.norm(vector)
        
        return vector.astype(np.float32)
    
    def encode_batch(self, texts, normalize=True):
        """批量文本转向量"""
        if not texts:
            return []
        
        vectors = []
        for text in texts:
            vectors.append(self.encode(text, normalize))
        return vectors

# 全局单例
embedding_model = EmbeddingModel()
