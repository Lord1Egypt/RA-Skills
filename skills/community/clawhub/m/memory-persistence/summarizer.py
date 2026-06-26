"""
Memory Summarizer - Auto-summarize conversations into memories
"""
import sys
import json
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import List, Dict, Any, Optional
from memory_system.storage import MemoryEntry


class OpenClawModelDetector:
    """Detect OpenClaw's configured model"""
    
    @staticmethod
    def detect() -> Optional[Dict[str, str]]:
        """
        Detect OpenClaw's configured model from config file
        
        Returns:
            Dict with provider, model, base_url, api_key or None
        """
        # Try multiple config locations
        config_paths = [
            Path.home() / '.openclaw' / 'openclaw.json',
            Path.home() / '.openclaw' / '.openclaw.json',
        ]
        
        for config_path in config_paths:
            if not config_path.exists():
                continue
                
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Navigate to model config
                if 'agents' not in config:
                    continue
                    
                agents = config.get('agents', {})
                model_config = agents.get('model', {})
                primary = model_config.get('primary', '')
                
                if not primary:
                    continue
                
                # Parse provider/model from primary (e.g., "minimax-portal/MiniMax-M2.5")
                if '/' in primary:
                    provider, model = primary.split('/', 1)
                else:
                    provider = 'openai'
                    model = primary
                
                # Get provider-specific settings
                providers = model_config.get('providers', {})
                provider_config = providers.get(provider, {})
                base_url = provider_config.get('baseUrl', '')
                api_key = provider_config.get('apiKey', '')
                
                # Map provider names
                provider_map = {
                    'minimax': 'openai',  # MiniMax uses OpenAI-compatible API
                    'minimax-portal': 'openai',
                    'anthropic': 'anthropic',
                    'openai': 'openai',
                }
                
                mapped_provider = provider_map.get(provider, 'openai')
                
                return {
                    'provider': mapped_provider,
                    'model': model,
                    'base_url': base_url,
                    'api_key': api_key or None  # Will use env var if None
                }
                
            except Exception as e:
                continue
        
        return None


class MemorySummarizer:
    """
    Summarizes conversations and extracts key information for memory storage.
    
    Uses LLM to analyze conversation history and generate structured memory entries.
    Automatically detects OpenClaw's configured model.
    """
    
    def __init__(
        self,
        llm_provider: str = None,
        api_key: str = None,
        model: str = None,
        base_url: str = None
    ):
        """
        Initialize Memory Summarizer
        
        Args:
            llm_provider: LLM provider name (openai, anthropic, ollama). Auto-detected if None.
            api_key: API key for the provider
            model: Model name. Auto-detected from OpenClaw if None.
            base_url: Base URL for API (for custom endpoints)
        """
        # Try to detect from OpenClaw config
        detected = OpenClawModelDetector.detect()
        
        self.llm_provider = llm_provider or (detected['provider'] if detected else 'openai')
        self.api_key = api_key or (detected['api_key'] if detected else None)
        self.model = model or (detected['model'] if detected else 'gpt-4')
        self.base_url = base_url or (detected['base_url'] if detected else None)
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment or config"""
        if self.api_key:
            return self.api_key
            
        import os
        env_vars = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
        }
        var_name = env_vars.get(self.llm_provider, 'OPENAI_API_KEY')
        return os.environ.get(var_name)
    
    def summarize(
        self,
        conversation: str,
        context: str = None,
        max_memories: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Summarize a conversation and extract key memories
        
        Args:
            conversation: Raw conversation text (multi-line)
            context: Optional context about the user/session
            max_memories: Maximum number of memory entries to generate
        
        Returns:
            List of memory dictionaries with content, tags, and metadata
        """
        prompt = self._build_prompt(conversation, context, max_memories)
        response = self._call_llm(prompt)
        return self._parse_response(response)
    
    def _build_prompt(
        self,
        conversation: str,
        context: str,
        max_memories: int
    ) -> str:
        """Build the summarization prompt"""
        context_str = f"\n\nUser Context: {context}" if context else ""
        
        return f"""You are a memory extraction system. Analyze the following conversation and extract key information that should be remembered.{context_str}

CONVERSATION:
---
{conversation}
---

Extract up to {max_memories} key pieces of information from this conversation. For each piece, provide:
1. A concise summary (1-2 sentences)
2. Appropriate tags
3. A memory type category

Output format (JSON array):
[
  {{
    "content": "What was learned/decided",
    "tags": ["tag1", "tag2"],
    "memory_type": "preference|fact|action|relationship|other"
  }}
]

Focus on:
- User preferences and settings
- Important facts about the user
- Action items or todos
- Relationships between people
- Technical decisions or configurations

Return ONLY valid JSON, no markdown formatting."""
    
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM API"""
        if self.llm_provider == "openai":
            return self._call_openai(prompt)
        elif self.llm_provider == "anthropic":
            return self._call_anthropic(prompt)
        elif self.llm_provider == "ollama":
            return self._call_ollama(prompt)
        else:
            # Default to openai
            return self._call_openai(prompt)
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI-compatible API"""
        import openai
        
        api_key = self._get_api_key()
        
        client_kwargs = {'api_key': api_key} if api_key else {}
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        client = openai.OpenAI(**client_kwargs)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        import anthropic
        
        api_key = self._get_api_key()
        
        client_kwargs = {'api_key': api_key} if api_key else {}
        
        client = anthropic.Anthropic(**client_kwargs)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API (local)"""
        import requests
        
        url = (self.base_url or "http://localhost:11434") + "/api/generate"
        
        response = requests.post(url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        
        return response.json().get('response', '')
    
    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response into memory dictionaries"""
        import json
        
        # Try to extract JSON from the response
        try:
            # Handle markdown code blocks
            if '```json' in response:
                start = response.find('```json') + 7
                end = response.find('```', start)
                response = response[start:end]
            elif '```' in response:
                start = response.find('```') + 3
                end = response.find('```', start)
                response = response[start:end]
            
            data = json.loads(response.strip())
            return data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            # Fallback: return raw text as single memory
            return [{
                "content": response.strip(),
                "tags": ["raw", "unparsed"],
                "memory_type": "other"
            }]


class ConversationMemoryProcessor:
    """
    Process conversation history and auto-save to memory manager
    """
    
    def __init__(
        self,
        memory_manager,
        summarizer: MemorySummarizer = None,
        auto_save: bool = False
    ):
        """
        Initialize processor
        
        Args:
            memory_manager: MemoryManager instance to save memories
            summarizer: MemorySummarizer instance (auto-created if None)
            auto_save: If True, auto-save generated memories
        """
        self.memory_manager = memory_manager
        self.summarizer = summarizer or MemorySummarizer()
        self.auto_save = auto_save
    
    def process(
        self,
        conversation: str,
        context: str = None,
        tags: List[str] = None
    ) -> List[MemoryEntry]:
        """
        Process conversation and optionally save to memory
        
        Args:
            conversation: Raw conversation text
            context: Optional context
            tags: Additional tags to add to all memories
        
        Returns:
            List of MemoryEntry objects (saved if auto_save=True)
        """
        # Summarize
        summaries = self.summarizer.summarize(conversation, context)
        
        entries = []
        for summary in summaries:
            content = summary.get('content', '')
            if not content:
                continue
            
            # Build tags
            memory_tags = summary.get('tags', [])
            if tags:
                memory_tags = memory_tags + tags
            
            # Build metadata
            metadata = {
                'memory_type': summary.get('memory_type', 'other'),
                'source': 'conversation_summary'
            }
            
            if self.auto_save:
                entry = self.memory_manager.add(
                    content=content,
                    tags=memory_tags,
                    metadata=metadata
                )
            else:
                # Create entry without saving
                from datetime import datetime
                import hashlib
                
                entry_id = hashlib.sha256(
                    f"{content[:100]}{datetime.now().isoformat()}".encode()
                ).hexdigest()[:16]
                
                entry = MemoryEntry(
                    id=entry_id,
                    content=content,
                    timestamp=datetime.now().isoformat(),
                    tags=memory_tags,
                    metadata=metadata
                )
            
            entries.append(entry)
        
        return entries
