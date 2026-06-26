"""Configuration management for podcast-intel."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import yaml


def get_skill_root() -> Path:
    """Get the skill root directory (parent of scripts/)."""
    return Path(__file__).parent.parent.parent


def get_openclaw_root() -> Path:
    """Get OpenClaw root dir from env or default HOME path."""
    return Path(os.getenv("OPENCLAW_HOME", Path.home() / ".openclaw"))


def get_cache_dir() -> Path:
    """Get the cache directory, creating it if needed."""
    cache_dir = get_openclaw_root() / "cache" / "podcast-intel"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_diary_path() -> Path:
    """Get the diary file path."""
    diary_path = get_openclaw_root() / "workspace" / "podcast-intel" / "diary.jsonl"
    diary_path.parent.mkdir(parents=True, exist_ok=True)
    return diary_path


def get_memory_dir() -> Path:
    """Get the OpenClaw memory directory for podcast-intel."""
    memory_dir = get_openclaw_root() / "memory" / "podcast-intel"
    memory_dir.mkdir(parents=True, exist_ok=True)
    return memory_dir


def load_feeds_config(config_path: Optional[Path] = None) -> List[Dict]:
    """Load podcast feeds configuration from YAML."""
    if config_path is None:
        env_config = os.getenv("PODCAST_INTEL_FEEDS")
        if env_config:
            config_path = Path(env_config)
        else:
            # Check for user config first
            user_config = get_openclaw_root() / "config" / "podcast-intel-feeds.yaml"
            if user_config.exists():
                config_path = user_config
            else:
                # Fall back to example config
                config_path = get_skill_root() / "config" / "feeds.example.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Feeds config not found at {config_path}")
    
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)
    
    return data.get('feeds', [])


def load_interests_config(config_path: Optional[Path] = None) -> Dict:
    """Load user interests configuration from YAML."""
    if config_path is None:
        env_config = os.getenv("PODCAST_INTEL_INTERESTS")
        if env_config:
            config_path = Path(env_config)
        else:
            # Check for user config first
            user_config = get_openclaw_root() / "config" / "podcast-intel-interests.yaml"
            if user_config.exists():
                config_path = user_config
            else:
                # Fall back to example config
                config_path = get_skill_root() / "config" / "interests.example.yaml"
    
    if not config_path.exists():
        # Return empty config if not found
        return {
            'interests': {'primary': [], 'secondary': [], 'casual': []},
            'anti_interests': [],
            'boost_keywords': []
        }
    
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)
    
    return data or {'interests': {'primary': [], 'secondary': [], 'casual': []},
                     'anti_interests': [], 'boost_keywords': []}


def get_openai_config() -> Dict[str, str]:
    """Get OpenAI API configuration from environment."""
    config = {
        'api_key': os.getenv('OPENAI_API_KEY', ''),
        'base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        'model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
    }
    
    if not config['api_key']:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return config


def get_whisper_config() -> Dict[str, str]:
    """Get Whisper transcription configuration."""
    return {
        'model': os.getenv('WHISPER_MODEL', 'whisper-1'),
        'use_local': os.getenv('WHISPER_USE_LOCAL', 'false').lower() == 'true',
        'cache_dir': str(get_cache_dir() / 'transcripts'),
    }


def get_transcript_cache_path(episode_id: str) -> Path:
    """Get the path where a transcript would be cached."""
    cache_dir = get_cache_dir() / 'transcripts'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{episode_id}.json"


def get_segmentation_cache_path(episode_id: str) -> Path:
    """Get the path where segmentation would be cached."""
    cache_dir = get_cache_dir() / 'segmentations'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{episode_id}.json"


def get_analysis_cache_path(episode_id: str) -> Path:
    """Get the path where analysis would be cached."""
    cache_dir = get_cache_dir() / 'analyses'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{episode_id}.json"


def was_transcript_cached(episode_id: str) -> bool:
    """Check if transcript is cached."""
    return get_transcript_cache_path(episode_id).exists()


def was_segmentation_cached(episode_id: str) -> bool:
    """Check if segmentation is cached."""
    return get_segmentation_cache_path(episode_id).exists()


def load_diary() -> List[Dict]:
    """Load all diary entries from JSONL file."""
    diary_path = get_diary_path()
    
    if not diary_path.exists():
        return []
    
    entries = []
    with open(diary_path, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    return entries


def save_diary_entry(entry: Dict) -> None:
    """Append a diary entry to the JSONL file."""
    diary_path = get_diary_path()
    
    with open(diary_path, 'a') as f:
        f.write(json.dumps(entry) + '\n')


def save_markdown_note(content: str, filename: Optional[str] = None) -> Path:
    """Save a markdown note to the memory directory."""
    memory_dir = get_memory_dir()
    
    if filename is None:
        from datetime import datetime
        filename = datetime.now().strftime('%Y-%m-%d.md')
    
    note_path = memory_dir / filename
    
    # Append to existing file if it exists
    mode = 'a' if note_path.exists() else 'w'
    with open(note_path, mode) as f:
        f.write(content)
    
    return note_path
