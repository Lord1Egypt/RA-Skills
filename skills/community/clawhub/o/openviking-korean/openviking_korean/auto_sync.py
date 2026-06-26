#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenViking Korean - 자동 동기화 모듈

heartbeat 시 자동으로 관련 컨텍스트 검색
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

from .vector_store import VectorStore, create_vector_store
from .tokenizer import KoreanTokenizer, create_default_tokenizer


class AutoSync:
    """자동 동기화 - 스마트 컨텍스트 로딩"""
    
    def __init__(self,
                 workspace_path: str = "~/.openclaw/workspace",
                 cache_ttl: int = 3600):  # 1시간 캐시
        """
        Args:
            workspace_path: 워크스페이스 경로
            cache_ttl: 캐시 유효시간 (초)
        """
        self.workspace_path = Path(workspace_path).expanduser()
        self.cache_ttl = cache_ttl
        
        # 컴포넌트 초기화
        self.vector_store = create_vector_store(str(workspace_path))
        self.tokenizer = create_default_tokenizer()
        
        # 세션 컨텍스트
        self.session_context: Dict[str, Any] = {
            "last_query": None,
            "last_results": [],
            "loaded_uris": set(),
            "query_history": []
        }
        
        # 캐시 파일
        self.cache_file = self.workspace_path / ".openviking" / "sync_cache.json"
        self._load_session_cache()
    
    def _load_session_cache(self):
        """세션 캐시 로드"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.session_context.update(data)
            except:
                pass
    
    def _save_session_cache(self):
        """세션 캐시 저장"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            # set은 JSON으로 못 저장하니 list로 변환
            data = {
                "last_query": self.session_context["last_query"],
                "last_results": self.session_context["last_results"],
                "loaded_uris": list(self.session_context["loaded_uris"]),
                "query_history": self.session_context["query_history"][-20:]  # 최근 20개만
            }
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def analyze_current_context(self, 
                               recent_messages: List[str] = None,
                               max_messages: int = 5) -> Dict[str, Any]:
        """
        현재 컨텍스트 분석
        
        Args:
            recent_messages: 최근 메시지들
            max_messages: 분석할 최대 메시지 수
        
        Returns:
            분석 결과
        """
        # 현재 워크스페이스 상태
        context = {
            "timestamp": datetime.now().isoformat(),
            "workspace": str(self.workspace_path),
            "analysis": {}
        }
        
        # 1. MEMORY.md 상태
        memory_file = self.workspace_path / "MEMORY.md"
        if memory_file.exists():
            stat = memory_file.stat()
            context["analysis"]["memory"] = {
                "exists": True,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        else:
            context["analysis"]["memory"] = {"exists": False}
        
        # 2. context-summary.md (L0)
        summary_file = self.workspace_path / "context-summary.md"
        if summary_file.exists():
            stat = summary_file.stat()
            context["analysis"]["l0_summary"] = {
                "exists": True,
                "size": stat.st_size
            }
        
        # 3. 오늘의 로그
        today = datetime.now().strftime("%Y-%m-%d")
        today_log = self.workspace_path / "memory" / f"{today}.md"
        if today_log.exists():
            context["analysis"]["today_log"] = {"exists": True}
        
        # 4. 최근 메시지 분석
        if recent_messages:
            combined_text = ' '.join(recent_messages[-max_messages:])
            keywords = self.tokenizer.extract_keywords(combined_text, top_n=5)
            context["analysis"]["recent_keywords"] = [k[0] for k in keywords]
        
        return context
    
    def find_relevant_context(self,
                             query: str,
                             top_k: int = 3,
                             min_score: float = 0.3) -> List[Dict[str, Any]]:
        """
        관련 컨텍스트 검색
        
        Args:
            query: 검색 쿼리
            top_k: 상위 k개
            min_score: 최소 점수
        
        Returns:
            검색 결과 리스트
        """
        # 쿼리 확장
        expanded_tokens = self.tokenizer.expand_query(query)
        expanded_query = ' '.join(expanded_tokens)
        
        # 벡터 검색
        results = self.vector_store.search(expanded_query, top_k, min_score)
        
        # 이미 로드된 것은 제외
        new_results = []
        for r in results:
            if r["uri"] not in self.session_context["loaded_uris"]:
                new_results.append(r)
        
        # 세션 업데이트
        self.session_context["last_query"] = query
        self.session_context["last_results"] = results
        self.session_context["query_history"].append({
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "result_count": len(results)
        })
        
        return new_results
    
    def on_heartbeat(self,
                    recent_messages: List[str] = None,
                    current_task: str = None) -> Dict[str, Any]:
        """
        heartbeat 이벤트 핸들러
        
        Args:
            recent_messages: 최근 메시지들
            current_task: 현재 작업
        
        Returns:
            자동 로드할 컨텍스트
        """
        result = {
            "action": "none",
            "context": None,
            "message": None
        }
        
        # 현재 컨텍스트 분석
        analysis = self.analyze_current_context(recent_messages)
        keywords = analysis["analysis"].get("recent_keywords", [])
        
        # 키워드가 있으면 검색
        if keywords:
            query = ' '.join(keywords)
            relevant = self.find_relevant_context(query, top_k=2)
            
            if relevant:
                result["action"] = "load_context"
                result["context"] = relevant
                result["message"] = f"관련 컨텍스트 발견: {[r['uri'] for r in relevant]}"
                
                # 로드된 것으로 표시
                for r in relevant:
                    self.session_context["loaded_uris"].add(r["uri"])
        
        # 현재 작업이 있으면 관련 컨텍스트 검색
        if current_task:
            task_results = self.find_relevant_context(current_task, top_k=1)
            if task_results:
                if result["context"] is None:
                    result["context"] = []
                result["context"].extend(task_results)
                result["action"] = "load_context"
        
        # 캐시 저장
        self._save_session_cache()
        
        return result
    
    def index_workspace(self):
        """워크스페이스 전체 인덱싱"""
        documents = []
        
        # MEMORY.md
        memory_file = self.workspace_path / "MEMORY.md"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                documents.append(("MEMORY.md", f.read(), {"type": "long_term_memory"}))
        
        # context-summary.md
        summary_file = self.workspace_path / "context-summary.md"
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                documents.append(("context-summary.md", f.read(), {"type": "l0_summary"}))
        
        # memory/*.md
        memory_dir = self.workspace_path / "memory"
        if memory_dir.exists():
            for md_file in memory_dir.glob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        documents.append((f"memory/{md_file.name}", f.read(), {"type": "daily_log"}))
                except UnicodeDecodeError:
                    pass
        
        # AGENTS.md
        agents_file = self.workspace_path / "AGENTS.md"
        if agents_file.exists():
            with open(agents_file, 'r', encoding='utf-8') as f:
                documents.append(("AGENTS.md", f.read(), {"type": "workspace_config"}))
        
        # USER.md
        user_file = self.workspace_path / "USER.md"
        if user_file.exists():
            with open(user_file, 'r', encoding='utf-8') as f:
                documents.append(("USER.md", f.read(), {"type": "user_profile"}))
        
        # 일괄 인덱싱
        self.vector_store.batch_index(documents)
        
        return len(documents)
    
    def get_stats(self) -> Dict[str, Any]:
        """통계 정보"""
        return {
            "vector_store": self.vector_store.stats(),
            "session": {
                "loaded_uris_count": len(self.session_context["loaded_uris"]),
                "query_history_count": len(self.session_context["query_history"])
            }
        }
    
    def clear_session(self):
        """세션 초기화"""
        self.session_context = {
            "last_query": None,
            "last_results": [],
            "loaded_uris": set(),
            "query_history": []
        }
        self._save_session_cache()


def create_auto_sync(workspace_path: str = "~/.openclaw/workspace") -> AutoSync:
    """자동 동기화 인스턴스 생성"""
    sync = AutoSync(workspace_path)
    sync.index_workspace()  # 초기 인덱싱
    return sync


if __name__ == "__main__":
    # 테스트
    sync = create_auto_sync()
    
    print("=== 통계 ===")
    print(json.dumps(sync.get_stats(), ensure_ascii=False, indent=2))
    
    print("\n=== 검색 테스트 ===")
    results = sync.find_relevant_context("마케팅 전략")
    for r in results:
        print(f"[{r['score']:.2f}] {r['uri']}")
    
    print("\n=== Heartbeat 테스트 ===")
    heartbeat_result = sync.on_heartbeat(
        recent_messages=["마케팅 전략을 짜야 해요", "광고 예산을 어떻게 쓸까요?"],
        current_task="마케팅 캠페인 기획"
    )
    print(json.dumps(heartbeat_result, ensure_ascii=False, indent=2))