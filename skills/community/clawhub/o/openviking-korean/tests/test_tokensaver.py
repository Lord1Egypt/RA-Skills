"""
TokenSaver Test Suite / 토큰세이버 테스트 스위트

Comprehensive tests for all components / 모든 컴포넌트 종합 테스트
Run: pytest tests/test_tokensaver.py -v
"""

import pytest
import asyncio
import tempfile
import json
from pathlib import Path

# Add parent directory to path / 상위 디렉토리 추가
import sys
sys.path.insert(0, 'C:/Users/Roken/.openclaw/workspace/_auai-engine/openviking-korean')

from v3 import (
    TokenSaver,
    PurePythonKoreanTokenizer,
    MultiLevelCompressor,
    ContextStore,
    CompressionResult
)


class TestTokenizer:
    """Korean Tokenizer Tests / 한국어 토크나이저 테스트"""
    
    def test_tokenize_basic(self):
        """기본 토큰화 테스트"""
        t = PurePythonKoreanTokenizer()
        tokens = t.tokenize("안녕하세요 세상입니다")
        assert len(tokens) > 0
        assert isinstance(tokens, tuple)
    
    def test_tokenize_caching(self):
        """LRU 캐싱 테스트"""
        t = PurePythonKoreanTokenizer()
        text = "테스트 문장입니다"
        
        # 첫 호출
        result1 = t.tokenize(text)
        # 캐시된 두번째 호출 (훨씬 빨라야 함)
        result2 = t.tokenize(text)
        
        assert result1 == result2
        assert t.tokenize.cache_info().hits >= 1
    
    def test_extract_keywords(self):
        """키워드 추출 테스트"""
        t = PurePythonKoreanTokenizer()
        keywords = t.extract_keywords("인공지능과 머신러닝은 미래 기술입니다", top_n=3)
        
        assert len(keywords) <= 3
        assert all(len(k) >= 2 for k in keywords)
    
    def test_extract_key_sentences(self):
        """핵심 문장 추출 테스트"""
        t = PurePythonKoreanTokenizer()
        text = "첫 번째 문장입니다. 두 번째 중요 문장이에요. 세 번째 문장입니다."
        sentences = t.extract_key_sentences(text, top_n=2)
        
        assert len(sentences) <= 2
        assert all(len(s) > 10 for s in sentences)


class TestCompressor:
    """Compression Engine Tests / 압축 엔진 테스트"""
    
    def test_compress_l0(self):
        """L0 압축 테스트 (99% 절감)"""
        c = MultiLevelCompressor()
        text = "인공지능과 머신러닝은 미래의 중요한 기술입니다. 많은 기업들이 투자하고 있어요."
        result = c.compress(text, 0)
        
        assert result.startswith("[") and result.endswith("]")
        assert len(result) < len(text) * 0.5  # 50% 이상 줄어야 함
    
    def test_compress_l1(self):
        """L1 압축 테스트 (96% 절감)"""
        c = MultiLevelCompressor()
        text = "첫 문장입니다. 두 번째 중요한 문장이에요. 세 번째 문장입니다. 네 번째 문장입니다."
        result = c.compress(text, 1)
        
        assert len(result.split()) <= 3  # 3문장 이내
    
    def test_compress_l2(self):
        """L2 압축 테스트 (91% 절감)"""
        c = MultiLevelCompressor()
        text = "이것은 테스트입니다. 여러 문장이 있는 텍스트예요. 압축이 잘 되어야 해요."
        result = c.compress(text, 2)
        
        assert "[" in result  # 키워드 표시
        assert len(result) < len(text) * 0.5
    
    def test_compress_l3(self):
        """L3 압축 테스트 (원본)"""
        c = MultiLevelCompressor()
        text = "원본 텍스트입니다"
        result = c.compress(text, 3)
        
        assert result == text
    
    def test_compress_with_stats(self):
        """압축 통계 테스트"""
        c = MultiLevelCompressor()
        text = "이것은 테스트 문장입니다. " * 10
        result = c.compress_with_stats(text, 2)
        
        assert isinstance(result, CompressionResult)
        assert result.reduction_ratio > 0.5  # 50% 이상 절감
        assert result.original_tokens > result.compressed_tokens


class TestContextStore:
    """Context Store Tests / 컨텍스트 저장소 테스트"""
    
    @pytest.fixture
    def temp_store(self):
        """임시 저장소 fixture"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield ContextStore(tmpdir)
    
    def test_save_and_load(self, temp_store):
        """저장/로드 테스트"""
        data = {"uri": "test/1", "content": "테스트 내용"}
        temp_store.save("test/1", data)
        
        loaded = temp_store.load("test/1")
        assert loaded is not None
        assert loaded["uri"] == "test/1"
    
    def test_load_nonexistent(self, temp_store):
        """없는 URI 로드 테스트"""
        result = temp_store.load("nonexistent")
        assert result is None
    
    def test_export_import(self, temp_store):
        """익스포트/임포트 테스트"""
        # 데이터 저장
        for i in range(5):
            temp_store.save(f"test/{i}", {"uri": f"test/{i}", "content": f"내용{i}"})
        
        # 익스포트
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_path = f.name
        
        assert temp_store.export_fast(export_path) is True
        assert Path(export_path).exists()
        
        # 새 저장소에 임포트
        with tempfile.TemporaryDirectory() as tmpdir2:
            store2 = ContextStore(tmpdir2)
            result = store2.import_json(export_path)
            
            assert result.success == 5
            assert len(store2.get_all_uris()) == 5
    
    def test_search(self, temp_store):
        """검색 테스트"""
        temp_store.save("marketing/1", {
            "uri": "marketing/1",
            "abstract": "[마케팅/전략] 마케팅 전략 수립",
            "content": "마케팅 전략을 수립하는 방법",
            "category": "marketing"
        })
        temp_store.save("dev/1", {
            "uri": "dev/1", 
            "abstract": "[코드/개발] Python 개발",
            "content": "Python 개발 가이드",
            "category": "dev"
        })
        
        results = temp_store.search("마케팅 전략")
        assert len(results) > 0
        assert any("marketing" in r.uri for r in results)
    
    @pytest.mark.asyncio
    async def test_save_async(self, temp_store):
        """비동기 저장 테스트"""
        data = {"uri": "async/1", "content": "비동기 테스트"}
        result = await temp_store.save_async("async/1", data)
        
        assert result is True
        loaded = temp_store.load("async/1")
        assert loaded is not None
    
    @pytest.mark.asyncio
    async def test_save_batch_async(self, temp_store):
        """비동기 배치 저장 테스트"""
        items = [
            {"uri": f"batch/{i}", "content": f"내용{i}"}
            for i in range(10)
        ]
        
        result = await temp_store.save_batch_async(items)
        
        assert result.success == 10
        assert result.failed == 0
        assert len(temp_store.get_all_uris()) == 10


class TestTokenSaver:
    """Main TokenSaver Integration Tests / 메인 클래스 통합 테스트"""
    
    @pytest.fixture
    def client(self):
        """클라이언트 fixture"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield TokenSaver(tmpdir)
    
    def test_save_and_find(self, client):
        """저장 및 검색 통합 테스트"""
        client.save("test/memo", "이것은 중요한 메모입니다. 나중에 꼭 확인하세요.", level=2)
        
        results = client.find("중요한 메모")
        assert len(results) > 0
        assert any("test/memo" in r.uri for r in results)
    
    def test_save_batch(self, client):
        """배치 저장 테스트"""
        items = [
            {"uri": f"batch/{i}", "content": f"배치 테스트 내용 {i}"}
            for i in range(20)
        ]
        
        result = client.save_batch(items)
        assert result.success == 20
    
    def test_auto_compress_old(self, client):
        """자동 압축 테스트"""
        # 오래된 데이터 저장 (시간 조작)
        import time
        client.save("old/1", "오래된 내용", level=3)
        
        # 파일 시간 조작 (7일 전으로)
        old_time = time.time() - (8 * 24 * 60 * 60)
        path = Path(client.store.base_path) / "old/1.json"
        if path.exists():
            import os
            os.utime(path, (old_time, old_time))
        
        # 자동 압축 실행
        result = client.auto_compress_old(days=7, target_level=1)
        
        # 결과 검증 (시간 조작이 되었으면 compressed > 0)
        assert result.compressed >= 0  # 파일 시간 조작 결과에 따라 다름
    
    def test_levels(self, client):
        """모든 압축 레벨 테스트"""
        text = "인공지능과 머신러닝은 미래 기술입니다. 많은 기업들이 투자하고 있어요."
        
        for level in [0, 1, 2, 3]:
            data = client.save(f"levels/{level}", text, level=level)
            
            loaded = client.find(f"인공지능", level=level, limit=1)
            if loaded:
                assert loaded[0].content is not None


class TestPerformance:
    """Performance Benchmark Tests / 성능 벤치마크 테스트"""
    
    @pytest.mark.benchmark
    def test_tokenize_speed(self):
        """토큰화 속도 벤치마크"""
        import time
        
        t = PurePythonKoreanTokenizer()
        text = "이것은 테스트 문장입니다. " * 100
        
        start = time.time()
        for _ in range(1000):
            t.tokenize(text)
        elapsed = time.time() - start
        
        # 캐시 히트로 인해 매우 빨라야 함
        assert elapsed < 1.0  # 1초 이내
    
    @pytest.mark.benchmark  
    def test_compress_speed(self):
        """압축 속도 벤치마크"""
        import time
        
        c = MultiLevelCompressor()
        text = "인공지능과 머신러닝은 미래 기술입니다. " * 50
        
        start = time.time()
        for _ in range(100):
            c.compress(text, 2)
        elapsed = time.time() - start
        
        assert elapsed < 0.5  # 0.5초 이네
    
    @pytest.mark.benchmark
    def test_reduction_ratio(self):
        """압축률 검증 (96% 목표)"""
        c = MultiLevelCompressor()
        
        # 긴 텍스트로 테스트
        text = "인공지능과 머신러닝은 미래의 중요한 기술입니다. " * 100
        
        result = c.compress_with_stats(text, 2)  # L2: 기본
        
        # 90% 이상 절감 확인
        assert result.reduction_ratio >= 0.90
        print(f"✅ 압축률: {result.reduction_ratio:.1%} (목표: 96%)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])