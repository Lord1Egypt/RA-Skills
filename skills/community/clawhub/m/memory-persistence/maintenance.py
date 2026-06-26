"""
Memory Maintenance - Periodic review and consolidation of memories
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from memory_system.storage import MemoryEntry


class MemoryMaintenance:
    """
    Periodic memory maintenance tasks:
    - Review old memories
    - Consolidate similar memories
    - Expand short/sparse memories
    - Mark outdated memories
    """
    
    def __init__(
        self,
        memory_manager,
        summarizer=None,
        embedding_handler=None
    ):
        """
        Initialize Memory Maintenance
        
        Args:
            memory_manager: MemoryManager instance
            summarizer: MemorySummarizer for LLM tasks (auto-created if None)
            embedding_handler: EmbeddingHandler for similarity checks
        """
        self.memory_manager = memory_manager
        self.summarizer = summarizer
        self.embedding_handler = embedding_handler
    
    def _get_summarizer(self):
        """Lazy load summarizer"""
        if self.summarizer is None:
            from summarizer import MemorySummarizer
            self.summarizer = MemorySummarizer()
        return self.summarizer
    
    def run_review(
        self,
        older_than_days: int = 7,
        max_memories: int = 10
    ) -> Dict[str, Any]:
        """
        Review old memories and suggest improvements
        
        Args:
            older_than_days: Check memories older than N days
            max_memories: Maximum number to review
        
        Returns:
            Dict with review results
        """
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        all_memories = self.memory_manager.list()
        
        # Filter old memories
        old_memories = []
        for m in all_memories:
            try:
                mtime = datetime.fromisoformat(m.timestamp)
                if mtime < cutoff_date:
                    old_memories.append(m)
            except:
                continue
        
        if not old_memories:
            return {
                "status": "no_old_memories",
                "message": f"No memories older than {older_than_days} days",
                "reviewed": 0
            }
        
        old_memories.sort(key=lambda x: x.timestamp)
        to_review = old_memories[:max_memories]
        
        review_results = []
        for mem in to_review:
            review = self._review_memory(mem)
            review_results.append(review)
        
        return {
            "status": "reviewed",
            "reviewed": len(review_results),
            "total_old": len(old_memories),
            "cutoff_days": older_than_days,
            "results": review_results
        }
    
    def _review_memory(self, memory: MemoryEntry) -> Dict[str, Any]:
        """Review a single memory and suggest improvements"""
        result = {
            "id": memory.id,
            "content": memory.content,
            "timestamp": memory.timestamp,
            "tags": memory.tags,
            "issues": [],
            "suggestions": []
        }
        
        content = memory.content.strip()
        
        # Check for issues
        if len(content) < 20:
            result["issues"].append("too_short")
            result["suggestions"].append("expand_summary")
        
        if not memory.tags:
            result["issues"].append("no_tags")
            result["suggestions"].append("add_tags")
        
        if memory.embedding is None and self.embedding_handler:
            result["issues"].append("no_embedding")
            result["suggestions"].append("add_embedding")
        
        # Check for outdated indicators
        outdated_words = ["今天", "现在", "当前", "目前", " recently", "currently"]
        if any(word in content for word in outdated_words):
            result["issues"].append("possibly_outdated")
            result["suggestions"].append("verify_or_update")
        
        return result
    
    def consolidate_similar(
        self,
        threshold: float = 0.85,
        dry_run: bool = True,
        auto_delete: bool = False
    ) -> Dict[str, Any]:
        """
        Find and suggest similar memories for consolidation.
        
        ⚠️ Note: This method NEVER auto-deletes. It only flags pairs for review.
        Use consolidate_and_merge() to actually merge with user confirmation.
        
        Args:
            threshold: Similarity threshold (0-1)
            dry_run: Always True - this method only suggests, never deletes
        
        Returns:
            Dict with suggested consolidation pairs
        """
        all_memories = self.memory_manager.list()
        
        if len(all_memories) < 2:
            return {
                "status": "insufficient_memories",
                "message": "Need at least 2 memories to find similarities",
                "pairs": []
            }
        
        # Find similar pairs
        similar_pairs = []
        processed = set()
        
        for i, mem_a in enumerate(all_memories):
            for mem_b in all_memories[i+1:]:
                if mem_a.id == mem_b.id:
                    continue
                
                similarity = self._calculate_similarity(mem_a, mem_b)
                
                if similarity >= threshold:
                    pair_key = tuple(sorted([mem_a.id, mem_b.id]))
                    if pair_key not in processed:
                        # Determine which to keep (newer)
                        if mem_a.timestamp > mem_b.timestamp:
                            keep_id, drop_id = mem_a.id, mem_b.id
                            keep_content = mem_a.content[:50]
                            drop_content = mem_b.content[:50]
                        else:
                            keep_id, drop_id = mem_b.id, mem_a.id
                            keep_content = mem_b.content[:50]
                            drop_content = mem_a.content[:50]
                        
                        similar_pairs.append({
                            "keep_id": keep_id,
                            "drop_id": drop_id,
                            "keep_content": keep_content + "...",
                            "drop_content": drop_content + "...",
                            "similarity": similarity
                        })
                        processed.add(pair_key)
        
        if not similar_pairs:
            return {
                "status": "no_similar_found",
                "message": "No similar memory pairs found",
                "pairs": []
            }
        
        return {
            "status": "found_similar",
            "message": f"Found {len(similar_pairs)} similar pairs - review and delete manually",
            "pairs": similar_pairs[:10],  # Limit output
            "action_needed": "USER_CONFIRMATION_REQUIRED"
        }
    
    def consolidate_and_merge(
        self,
        keep_id: str,
        drop_id: str,
        confirm: bool = False
    ) -> Dict[str, Any]:
        """
        Merge two memories, keeping one and deleting the other.
        
        ⚠️ Requires explicit user confirmation before deletion.
        
        Args:
            keep_id: ID of memory to keep
            drop_id: ID of memory to delete
            confirm: Must be True to actually delete
        
        Returns:
            Result dict
        """
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": "Set confirm=True to actually delete the memory",
                "keep_id": keep_id,
                "drop_id": drop_id
            }
        
        keep_mem = self.memory_manager.get(keep_id)
        drop_mem = self.memory_manager.get(drop_id)
        
        if not keep_mem or not drop_mem:
            return {
                "status": "memory_not_found",
                "message": "One or both memories not found"
            }
        
        # Merge tags
        merged_tags = list(set(keep_mem.tags + drop_mem.tags))
        
        # Update keeper with merged info
        keep_mem.tags = merged_tags
        keep_mem.content = f"{keep_mem.content}\n\n# Merged from {drop_id[:8]}...\n{drop_mem.content}"
        keep_mem.metadata = keep_mem.metadata or {}
        keep_mem.metadata['merged_from'] = drop_id
        
        self.memory_manager.storage.save(keep_mem)
        self.memory_manager.delete(drop_id)
        
        return {
            "status": "merged",
            "message": f"Kept {keep_id[:8]}..., deleted {drop_id[:8]}...",
            "keep_id": keep_id,
            "drop_id": drop_id
        }
    
    def _calculate_similarity(self, mem_a: MemoryEntry, mem_b: MemoryEntry) -> float:
        """Calculate similarity between two memories"""
        # If both have embeddings, use cosine similarity
        if mem_a.embedding and mem_b.embedding:
            import numpy as np
            from memory_system.embedding import EmbeddingHandler
            
            emb_a = np.array(mem_a.embedding)
            emb_b = np.array(mem_b.embedding)
            
            # Cosine similarity
            dot = np.dot(emb_a, emb_b)
            norm_a = np.linalg.norm(emb_a)
            norm_b = np.linalg.norm(emb_b)
            
            return float(dot / (norm_a * norm_b))
        
        # Fallback: text-based similarity
        text_a = mem_a.content.lower()
        text_b = mem_b.content.lower()
        
        # Simple word overlap
        words_a = set(text_a.split())
        words_b = set(text_b.split())
        
        if not words_a or not words_b:
            return 0.0
        
        intersection = words_a.intersection(words_b)
        union = words_a.union(words_b)
        
        return len(intersection) / len(union)
    
    def expand_summary(
        self,
        memory_id: str,
        conversation_context: str = None
    ) -> Optional[MemoryEntry]:
        """
        Expand a short memory into more detailed summary using LLM
        
        Args:
            memory_id: ID of memory to expand
            conversation_context: Optional conversation context for expansion
        
        Returns:
            Updated MemoryEntry or None
        """
        memory = self.memory_manager.get(memory_id)
        if not memory:
            return None
        
        if len(memory.content.strip()) >= 50:
            return memory  # Already detailed enough
        
        # Use LLM to expand
        summarizer = self._get_summarizer()
        
        context_str = f"Context:\n{conversation_context}" if conversation_context else ""
        
        prompt = f"""Expand the following memory into a more detailed summary.
Keep the core information but add relevant context.

Original memory:
{memory.content}

{context_str}

Provide an expanded version that is at least 3 sentences long while preserving the key information."""
        
        try:
            response = summarizer._call_llm(prompt)
            
            if response and len(response.strip()) > len(memory.content):
                memory.content = response.strip()
                memory.metadata = memory.metadata or {}
                memory.metadata['expanded'] = True
                memory.metadata['original_content'] = memory.content[:100]
                
                self.memory_manager.storage.save(memory)
                return memory
        except Exception as e:
            print(f"Error expanding memory: {e}")
        
        return memory
    
    def mark_outdated(
        self,
        memory_id: str,
        reason: str = None
    ) -> Optional[MemoryEntry]:
        """
        Mark a memory as outdated
        
        Args:
            memory_id: ID of memory to mark
            reason: Reason for marking as outdated
        
        Returns:
            Updated MemoryEntry or None
        """
        memory = self.memory_manager.get(memory_id)
        if not memory:
            return None
        
        memory.metadata = memory.metadata or {}
        memory.metadata['outdated'] = True
        memory.metadata['outdated_reason'] = reason
        memory.metadata['marked_outdated_at'] = datetime.now().isoformat()
        
        self.memory_manager.storage.save(memory)
        return memory
    
    def unmark_outdated(self, memory_id: str) -> Optional[MemoryEntry]:
        """Remove outdated标记 from a memory"""
        memory = self.memory_manager.get(memory_id)
        if not memory:
            return None
        
        if memory.metadata:
            memory.metadata.pop('outdated', None)
            memory.metadata.pop('outdated_reason', None)
            memory.metadata.pop('marked_outdated_at', None)
        
        self.memory_manager.storage.save(memory)
        return memory
    
    def list_outdated(self) -> List[MemoryEntry]:
        """List all memories marked as outdated"""
        all_memories = self.memory_manager.list()
        outdated = []
        
        for mem in all_memories:
            if mem.metadata and mem.metadata.get('outdated'):
                outdated.append(mem)
        
        return outdated
    
    def auto_enhance(
        self,
        older_than_days: int = 7,
        add_embeddings: bool = True,
        add_tags: bool = True
    ) -> Dict[str, Any]:
        """
        Automatically enhance old memories by adding missing embeddings/tags
        
        Args:
            older_than_days: Enhance memories older than N days
            add_embeddings: Add missing embeddings
            add_tags: Suggest tags for untagged memories
        
        Returns:
            Dict with enhancement results
        """
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        all_memories = self.memory_manager.list()
        
        enhanced = {"embeddings_added": 0, "tags_suggested": 0, "memories": []}
        
        for mem in all_memories:
            try:
                mtime = datetime.fromisoformat(mem.timestamp)
                if mtime > cutoff_date:
                    continue  # Skip new memories
            except:
                continue
            
            changes = []
            
            # Add embedding if missing
            if add_embeddings and mem.embedding is None:
                if self.embedding_handler:
                    self.embedding_handler.encode_single(mem.content)
                    # This would need to be saved back
                    enhanced["embeddings_added"] += 1
                    changes.append("embedding")
            
            # Suggest tags if missing
            if add_tags and not mem.tags:
                # Generate tags based on content
                suggested_tags = self._suggest_tags(mem.content)
                mem.tags = suggested_tags
                enhanced["tags_suggested"] += 1
                changes.append(f"tags:{','.join(suggested_tags)}")
            
            if changes:
                self.memory_manager.storage.save(mem)
                enhanced["memories"].append({
                    "id": mem.id,
                    "content_preview": mem.content[:50],
                    "changes": changes
                })
        
        return enhanced
    
    def _suggest_tags(self, content: str) -> List[str]:
        """Suggest tags for content using keyword analysis"""
        tags = []
        
        # Simple keyword-based tagging
        keywords = {
            "偏好": ["喜欢", "不喜欢", "想要", "希望", "prefer", "like"],
            "设置": ["配置", "设置", "option", "setting", "config"],
            "工作": ["工作", "项目", "任务", "meeting", "deadline"],
            "技术": ["代码", "bug", "api", "服务器", "部署"],
            "用户": ["用户", "客户", "customer", "user"],
            "决策": ["决定", "决策", "选择", "decision", "choose"]
        }
        
        content_lower = content.lower()
        
        for tag, words in keywords.items():
            if any(word in content_lower for word in words):
                tags.append(tag)
        
        if not tags:
            tags.append("general")
        
        return tags[:3]  # Max 3 tags
    
    def suggest_tags_llm(self, content: str) -> List[str]:
        """
        Suggest tags using LLM for smarter categorization
        
        Args:
            content: Memory content
        
        Returns:
            List of suggested tags
        """
        summarizer = self._get_summarizer()
        
        prompt = f"""Analyze the following memory content and suggest 2-4 appropriate tags.

Memory content:
{content}

Output format: A JSON array of tag strings, e.g.: ["标签1", "标签2", "标签3"]

Tags should be:
- Concise (1-3 Chinese characters each)
- Categorical (偏好, 设置, 技术, 工作, 用户, 项目, etc.)
- Specific to the content

Return ONLY valid JSON, no markdown formatting."""
        
        try:
            response = summarizer._call_llm(prompt)
            
            # Parse JSON response
            import json
            if '```json' in response:
                start = response.find('```json') + 7
                end = response.find('```', start)
                response = response[start:end]
            elif '```' in response:
                start = response.find('```') + 3
                end = response.find('```', start)
                response = response[start:end]
            
            tags = json.loads(response.strip())
            if isinstance(tags, list):
                return [str(t) for t in tags][:5]  # Max 5 tags
        except Exception as e:
            # Fallback to keyword-based
            return self._suggest_tags(content)
        
        return self._suggest_tags(content)
    
    def suggest_tags_for_memories(
        self,
        limit: int = 10,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        Suggest tags for untagged memories
        
        Args:
            limit: Maximum number to process
            use_llm: Use LLM for smarter suggestions (fallback to keyword)
        
        Returns:
            Dict with suggestions
        """
        all_memories = self.memory_manager.list()
        untagged = [m for m in all_memories if not m.tags]
        
        if not untagged:
            return {"status": "no_untagged", "count": 0}
        
        to_process = untagged[:limit]
        results = []
        
        for mem in to_process:
            if use_llm:
                tags = self.suggest_tags_llm(mem.content)
            else:
                tags = self._suggest_tags(mem.content)
            
            results.append({
                "id": mem.id,
                "content_preview": mem.content[:50],
                "current_tags": mem.tags or [],
                "suggested_tags": tags
            })
        
        return {
            "status": "success",
            "count": len(results),
            "remaining_untagged": len(untagged) - len(results),
            "suggestions": results
        }
    
    def generate_report(self) -> str:
        """Generate a maintenance report"""
        all_memories = self.memory_manager.list()
        
        total = len(all_memories)
        with_embedding = sum(1 for m in all_memories if m.embedding)
        without_embedding = total - with_embedding
        with_tags = sum(1 for m in all_memories if m.tags)
        without_tags = total - with_tags
        outdated = len(self.list_outdated())
        
        # Age distribution
        now = datetime.now()
        age_buckets = {
            "recent (< 7 days)": 0,
            "week": 0,
            "month": 0,
            "old (> 30 days)": 0
        }
        
        for m in all_memories:
            try:
                mtime = datetime.fromisoformat(m.timestamp)
                age = (now - mtime).days
                
                if age < 7:
                    age_buckets["recent (< 7 days)"] += 1
                elif age < 30:
                    age_buckets["week"] += 1
                elif age < 30:
                    age_buckets["month"] += 1
                else:
                    age_buckets["old (> 30 days)"] += 1
            except:
                continue
        
        report = f"""
📊 Memory Maintenance Report
{'=' * 40}

📦 Total Memories: {total}
   ├─ With embeddings: {with_embedding}
   ├─ Without embeddings: {without_embedding}
   ├─ With tags: {with_tags}
   ├─ Without tags: {without_tags}
   └─ Marked outdated: {outdated}

📅 Age Distribution:
   ├─ Recent (< 7 days): {age_buckets['recent (< 7 days)']}
   ├─ 7-30 days: {age_buckets['week']}
   └─ Old (> 30 days): {age_buckets['old (> 30 days)']}

💡 Suggestions:
   - Run consolidation if similar memories exist
   - Add embeddings to {without_embedding} memories
   - Tag {without_tags} untagged memories
"""
        return report
