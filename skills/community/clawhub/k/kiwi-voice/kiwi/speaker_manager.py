#!/usr/bin/env python3
"""
Speaker Manager - Voice Priority + Access Control

Extended voice management system:
- Priority hierarchy (OWNER > FRIEND > GUEST > BLOCKED)
- Hot cache for fast identification
- Auto-learning of new voices
- Last speaker context
"""

import os
import json
import time
import threading
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import IntEnum
from datetime import datetime, timedelta

import numpy as np

from kiwi.utils import kiwi_log
from kiwi.i18n import t

try:
    from kiwi.speaker_id import SpeakerIdentifier, SpeakerProfile
    BASE_AVAILABLE = True
except ImportError:
    BASE_AVAILABLE = False
    kiwi_log("SPEAKER_MANAGER", "speaker_id module not available", level="WARNING")


class VoicePriority(IntEnum):
    """Voice priorities (lower = higher priority)."""
    SELF = -1      # Kiwi TTS (echo filtering only)
    OWNER = 0      # Owner - maximum priority
    FRIEND = 1     # Remembered friends/acquaintances
    GUEST = 2      # Unknown guests
    BLOCKED = 99   # Blacklist (full ignore)


@dataclass
class VoiceContext:
    """Last speaker context."""
    speaker_id: str = ""
    speaker_name: str = ""
    priority: VoicePriority = VoicePriority.GUEST
    confidence: float = 0.0
    last_command: str = ""
    timestamp: float = 0.0
    is_processing: bool = False
    
    def is_valid(self) -> bool:
        """Context is valid for 30 seconds."""
        return (
            self.speaker_id and 
            time.time() - self.timestamp < 30.0
        )
    
    def update(self, speaker_id: str, speaker_name: str, priority: VoicePriority, confidence: float, command: str = ""):
        """Update the context."""
        self.speaker_id = speaker_id
        self.speaker_name = speaker_name
        self.priority = priority
        self.confidence = confidence
        self.last_command = command
        self.timestamp = time.time()
    
    def clear(self):
        """Clear the context."""
        self.speaker_id = ""
        self.speaker_name = ""
        self.priority = VoicePriority.GUEST
        self.confidence = 0.0
        self.last_command = ""
        self.timestamp = 0.0


@dataclass
class ExtendedSpeakerProfile:
    """Extended speaker profile."""
    # From speaker_id
    name: str
    embeddings: List[List[float]]
    priority: str  # "owner", "guest", "self"
    created_at: str = ""
    
    # New fields
    speaker_id: str = ""  # Unique ID (owner, friend_name, guest_UUID)
    display_name: str = ""  # Display name
    is_blocked: bool = False
    auto_learned: bool = False
    last_seen: str = ""
    confidence_threshold: float = 0.70
    
    def get_base_profile(self):
        """Convert to base SpeakerProfile."""
        if not BASE_AVAILABLE:
            return None
        return SpeakerProfile(
            name=self.name,
            embeddings=self.embeddings,
            priority=self.priority,
            created_at=self.created_at
        )
    
    @classmethod
    def from_base(cls, base, speaker_id: str = "") -> "ExtendedSpeakerProfile":
        """Create from a base profile."""
        return cls(
            name=base.name,
            embeddings=base.embeddings,
            priority=base.priority,
            created_at=base.created_at,
            speaker_id=speaker_id or base.name.lower().replace(" ", "_"),
            display_name=base.name,
            last_seen=datetime.now().isoformat()
        )


class SpeakerManager:
    """
    Voice manager with priority support.

    Features:
    - Hot cache in RAM for <10ms identification
    - Auto-learning at high confidence (>0.85)
    - Last speaker context (30 sec)
    - OWNER commands interrupt current tasks
    """

    # Settings
    AUTO_LEARN_THRESHOLD = 0.85  # Auto-memorize at this confidence
    IDENTIFY_THRESHOLD = 0.55     # Minimum for recognition (0.70 was too strict)
    HOT_CACHE_SIZE = 10           # Hot cache size
    CONTEXT_TIMEOUT = 30.0        # Context timeout (sec)

    # OWNER ID (configurable)
    OWNER_ID = "owner"
    OWNER_NAME = "Owner"

    def __init__(self, profiles_dir: Optional[str] = None, base_identifier: Optional["SpeakerIdentifier"] = None, owner_name: Optional[str] = None):
        """
        Args:
            profiles_dir: Directory for profiles
        """
        if owner_name:
            self.OWNER_NAME = owner_name
        self.profiles_dir = Path(profiles_dir) if profiles_dir else Path("voice_profiles")
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        # Base identification system
        # Use shared SpeakerIdentifier if provided, otherwise create new
        self.base_identifier: Optional[SpeakerIdentifier] = base_identifier
        if self.base_identifier is None and BASE_AVAILABLE:
            try:
                self.base_identifier = SpeakerIdentifier(str(self.profiles_dir))
                kiwi_log("SPEAKER_MANAGER", "Base identifier loaded (new instance)")
            except Exception as e:
                kiwi_log("SPEAKER_MANAGER", f"Failed to load base identifier: {e}", level="ERROR")
        elif self.base_identifier is not None:
            kiwi_log("SPEAKER_MANAGER", "Using shared base identifier")
        
        # Extended profiles
        self.profiles: Dict[str, ExtendedSpeakerProfile] = {}
        self._load_extended_profiles()
        
        # Hot cache for fast identification
        self._hot_cache: Dict[str, np.ndarray] = {}
        self._hot_cache_lock = threading.Lock()
        
        # Last speaker context
        self.voice_context = VoiceContext()
        
        # Temporary cache for learning
        self._temp_cache: Dict[str, List[np.ndarray]] = {}  # speaker_id -> embeddings
        self._temp_cache_lock = threading.Lock()
        
        kiwi_log("SPEAKER_MANAGER", f"Initialized with {len(self.profiles)} profiles")
    
    def _get_profiles_path(self) -> Path:
        """Path to the extended profiles file."""
        return self.profiles_dir / "extended_profiles.json"
    
    def _load_extended_profiles(self):
        """Load extended profiles."""
        path = self._get_profiles_path()
        if not path.exists():
            return
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for pid, profile_data in data.get("profiles", {}).items():
                self.profiles[pid] = ExtendedSpeakerProfile(**profile_data)
            
            kiwi_log("SPEAKER_MANAGER", f"Loaded {len(self.profiles)} extended profiles")
        except Exception as e:
            kiwi_log("SPEAKER_MANAGER", f"Error loading profiles: {e}", level="ERROR")
    
    def _save_extended_profiles(self):
        """Save extended profiles."""
        try:
            data = {
                "profiles": {
                    pid: asdict(p) for pid, p in self.profiles.items()
                }
            }
            with open(self._get_profiles_path(), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            kiwi_log("SPEAKER_MANAGER", f"Error saving profiles: {e}", level="ERROR")
    
    def _generate_speaker_id(self, name: str) -> str:
        """Generate a unique speaker_id from a name."""
        # Clean the name
        clean = "".join(c for c in name.lower() if c.isalnum() or c == "_")
        return f"friend_{clean}" if clean else f"guest_{int(time.time())}"
    
    def register_owner(self, audio: np.ndarray, sample_rate: int = 16000, name: str = None) -> bool:
        """
        Register OWNER.

        Args:
            audio: Audio sample
            sample_rate: Sample rate
            name: Name (default OWNER_NAME)

        Returns:
            True if successful
        """
        name = name or self.OWNER_NAME
        speaker_id = self.OWNER_ID
        
        kiwi_log("SPEAKER_MANAGER", f"Registering OWNER: {name} ({speaker_id})")
        
        if self.base_identifier:
            success = self.base_identifier.add_profile_sample(
                profile_id=speaker_id,
                audio=audio,
                sample_rate=sample_rate,
                name=name,
                priority="owner"
            )
            
            if success:
                # Create/update extended profile
                self.profiles[speaker_id] = ExtendedSpeakerProfile(
                    name=name,
                    embeddings=self.base_identifier.profiles[speaker_id].embeddings if speaker_id in self.base_identifier.profiles else [],
                    priority="owner",
                    speaker_id=speaker_id,
                    display_name=name,
                    is_blocked=False,
                    last_seen=datetime.now().isoformat()
                )
                self._save_extended_profiles()
                
                # Add to hot cache
                embedding = self.base_identifier.extract_embedding(audio, sample_rate)
                if embedding is not None:
                    with self._hot_cache_lock:
                        self._hot_cache[speaker_id] = embedding
                
                kiwi_log("SPEAKER_MANAGER", "OWNER registered successfully")
                return True
        
        return False
    
    def add_friend(self, audio: np.ndarray, sample_rate: int = 16000, name: str = None, 
                   auto_learn: bool = False) -> Tuple[bool, str]:
        """
        Add a friend/acquaintance.

        Args:
            audio: Audio sample
            sample_rate: Sample rate
            name: Person's name
            auto_learn: Auto-memorize without explicit adding

        Returns:
            (success, speaker_id)
        """
        if not name:
            return False, "Name required"
        
        speaker_id = self._generate_speaker_id(name)
        
        kiwi_log("SPEAKER_MANAGER", f"Adding FRIEND: {name} ({speaker_id})")
        
        if self.base_identifier:
            success = self.base_identifier.add_profile_sample(
                profile_id=speaker_id,
                audio=audio,
                sample_rate=sample_rate,
                name=name,
                priority="guest"
            )
            
            if success:
                self.profiles[speaker_id] = ExtendedSpeakerProfile(
                    name=name,
                    embeddings=self.base_identifier.profiles[speaker_id].embeddings if speaker_id in self.base_identifier.profiles else [],
                    priority="guest",
                    speaker_id=speaker_id,
                    display_name=name,
                    is_blocked=False,
                    auto_learned=auto_learn,
                    last_seen=datetime.now().isoformat()
                )
                self._save_extended_profiles()
                
                # Hot cache
                embedding = self.base_identifier.extract_embedding(audio, sample_rate)
                if embedding is not None:
                    with self._hot_cache_lock:
                        self._hot_cache[speaker_id] = embedding
                
                kiwi_log("SPEAKER_MANAGER", f"FRIEND added: {name}")
                return True, speaker_id
        
        return False, "Failed to add"
    
    def block_speaker(self, speaker_id: str) -> bool:
        """
        Block a voice (add to blacklist).

        Args:
            speaker_id: Voice ID to block

        Returns:
            True if found and blocked
        """
        # OWNER cannot be blocked
        if speaker_id == self.OWNER_ID:
            kiwi_log("SPEAKER_MANAGER", "Cannot block OWNER", level="WARNING")
            return False
        
        if speaker_id in self.profiles:
            self.profiles[speaker_id].is_blocked = True
            self._save_extended_profiles()
            
            # Remove from hot cache
            with self._hot_cache_lock:
                self._hot_cache.pop(speaker_id, None)
            
            kiwi_log("SPEAKER_MANAGER", f"BLOCKED: {speaker_id}")
            return True
        
        # If not found in profiles - create a temporary entry
        if speaker_id:
            self.profiles[speaker_id] = ExtendedSpeakerProfile(
                name="Blocked",
                embeddings=[],
                priority="guest",
                speaker_id=speaker_id,
                display_name=t("speakers.blocked_display") or "Заблокированный",
                is_blocked=True,
                last_seen=datetime.now().isoformat()
            )
            self._save_extended_profiles()
            kiwi_log("SPEAKER_MANAGER", f"BLOCKED (temp): {speaker_id}")
            return True
        
        return False
    
    def unblock_speaker(self, speaker_id: str) -> bool:
        """
        Unblock a voice.

        Args:
            speaker_id: Voice ID

        Returns:
            True if found and unblocked
        """
        if speaker_id in self.profiles:
            self.profiles[speaker_id].is_blocked = False
            self._save_extended_profiles()
            kiwi_log("SPEAKER_MANAGER", f"UNBLOCKED: {speaker_id}")
            return True
        return False
    
    def identify_speaker_fast(self, audio: np.ndarray, sample_rate: int = 16000) -> Tuple[str, VoicePriority, float, str]:
        """
        Fast speaker identification with priority.

        Uses hot cache for instant response.

        Returns:
            (speaker_id, priority, confidence, display_name)
        """
        if not self.base_identifier:
            return "unknown", VoicePriority.GUEST, 0.0, t("responses.unknown_speaker") or "Незнакомец"

        embedding = self.base_identifier.extract_embedding(audio, sample_rate)

        if embedding is None:
            kiwi_log("SPEAKER_MANAGER", "Embedding extraction returned None", level="WARNING")
            return "unknown", VoicePriority.GUEST, 0.0, t("responses.unknown_speaker") or "Незнакомец"

        # First check hot cache
        with self._hot_cache_lock:
            cache_items = list(self._hot_cache.items())

        best_id = None
        best_score = 0.0

        for sid, cached_emb in cache_items:
            if sid in self.profiles and self.profiles[sid].is_blocked:
                continue
            score = self.base_identifier.cosine_similarity(embedding, cached_emb)
            if score > best_score:
                best_score = score
                best_id = sid

        # Check threshold for hot cache
        if best_id and best_score >= self.IDENTIFY_THRESHOLD:
            priority = self._get_priority(best_id)
            name = self.profiles.get(best_id, ExtendedSpeakerProfile(name=best_id, embeddings=[], priority="guest")).display_name or best_id
            kiwi_log("SPEAKER_MANAGER", f"Hot-cache hit: {best_id} score={best_score:.3f}", level="DEBUG")
            return best_id, priority, best_score, name

        # If not found in cache - full scan
        speaker_id, score = self.base_identifier.identify_speaker(audio, sample_rate)

        if speaker_id != "unknown" and score >= self.IDENTIFY_THRESHOLD:
            priority = self._get_priority(speaker_id)

            # Check if blocked
            if speaker_id in self.profiles and self.profiles[speaker_id].is_blocked:
                return speaker_id, VoicePriority.BLOCKED, score, self.profiles[speaker_id].display_name

            # Add to hot cache
            with self._hot_cache_lock:
                self._hot_cache[speaker_id] = embedding
                if len(self._hot_cache) > self.HOT_CACHE_SIZE:
                    oldest = next(iter(self._hot_cache))
                    del self._hot_cache[oldest]

            name = self.profiles.get(speaker_id, ExtendedSpeakerProfile(name=speaker_id, embeddings=[], priority="guest")).display_name or speaker_id
            kiwi_log("SPEAKER_MANAGER", f"Identified: {speaker_id} score={score:.3f}", level="DEBUG")
            return speaker_id, priority, score, name

        # Unknown - return the REAL best score (not 0.0) for diagnostics
        kiwi_log("SPEAKER_MANAGER", f"Below threshold: best={speaker_id} score={score:.3f} (thr={self.IDENTIFY_THRESHOLD})", level="DEBUG")
        return "unknown", VoicePriority.GUEST, score, t("responses.unknown_speaker") or "Незнакомец"
    
    def _get_priority(self, speaker_id: str) -> VoicePriority:
        """Determine priority by speaker_id."""
        if speaker_id == self.OWNER_ID:
            return VoicePriority.OWNER
        if speaker_id == "self":
            return VoicePriority.SELF
        if speaker_id in self.profiles and self.profiles[speaker_id].is_blocked:
            return VoicePriority.BLOCKED
        if speaker_id in self.profiles and self.profiles[speaker_id].priority == "guest":
            return VoicePriority.FRIEND
        if speaker_id.startswith("friend_"):
            return VoicePriority.FRIEND
        if speaker_id.startswith("guest_"):
            return VoicePriority.GUEST
        if speaker_id == "unknown":
            return VoicePriority.GUEST
        return VoicePriority.GUEST
    
    def auto_learn_voice(self, audio: np.ndarray, speaker_id: str, sample_rate: int = 16000) -> bool:
        """
        Automatically learn a new voice at high confidence.

        Args:
            audio: Audio
            speaker_id: Current ID (may be "unknown")
            sample_rate: Sample rate

        Returns:
            True if a new profile was added
        """
        # Check threshold
        current_id, confidence = speaker_id, 0.0
        
        if self.base_identifier:
            _, confidence = self.base_identifier.identify_speaker(audio, sample_rate)
        
        if confidence < self.AUTO_LEARN_THRESHOLD:
            return False
        
        # Add to temporary cache
        with self._temp_cache_lock:
            if speaker_id not in self._temp_cache:
                self._temp_cache[speaker_id] = []
            
            if self.base_identifier:
                embedding = self.base_identifier.extract_embedding(audio, sample_rate)
                if embedding is not None:
                    self._temp_cache[speaker_id].append(embedding)
            
            # If enough samples accumulated (3-5) - save
            if len(self._temp_cache[speaker_id]) >= 3:
                # Generate name based on ID
                name = f"Guest_{speaker_id[-4:]}" if speaker_id.startswith("guest_") else speaker_id
                
                # Add as a temporary friend
                if self.base_identifier:
                    self.base_identifier.add_profile_sample(
                        profile_id=speaker_id,
                        audio=audio,
                        sample_rate=sample_rate,
                        name=name,
                        priority="guest"
                    )
                
                self.profiles[speaker_id] = ExtendedSpeakerProfile(
                    name=name,
                    embeddings=self.base_identifier.profiles[speaker_id].embeddings if (self.base_identifier and speaker_id in self.base_identifier.profiles) else [],
                    priority="guest",
                    speaker_id=speaker_id,
                    display_name=name,
                    is_blocked=False,
                    auto_learned=True,
                    last_seen=datetime.now().isoformat()
                )
                self._save_extended_profiles()
                
                # Clear cache
                del self._temp_cache[speaker_id]
                
                kiwi_log("SPEAKER_MANAGER", f"AUTO-LEARNED: {name} ({speaker_id})")
                return True
        
        return False
    
    def update_context(self, speaker_id: str, speaker_name: str, priority: VoicePriority, confidence: float, command: str = ""):
        """Update last speaker context."""
        self.voice_context.update(speaker_id, speaker_name, priority, confidence, command)
        kiwi_log("SPEAKER_MANAGER", f"Context updated: {speaker_name} ({priority.name}), confidence={confidence:.2f}")
    
    def get_context_speaker_id(self) -> Optional[str]:
        """Return the last speaker's ID (if context is valid)."""
        if self.voice_context.is_valid():
            return self.voice_context.speaker_id
        return None
    
    def is_owner(self, speaker_id: str) -> bool:
        """Check if this is the OWNER."""
        return speaker_id == self.OWNER_ID
    
    def is_blocked(self, speaker_id: str) -> bool:
        """Check if a voice is blocked."""
        if speaker_id == self.OWNER_ID:
            return False
        if speaker_id in self.profiles:
            return self.profiles[speaker_id].is_blocked
        return False
    
    def can_execute_command(self, speaker_id: str) -> Tuple[bool, str]:
        """
        Check if a voice can execute commands.

        Returns:
            (allowed, reason)
        """
        if speaker_id == "unknown":
            return False, t("speaker_access.unknown_voice") or "Неизвестный голос"

        if self.is_blocked(speaker_id):
            return False, t("speaker_access.voice_blocked") or "Голос заблокирован"

        priority = self._get_priority(speaker_id)

        if priority == VoicePriority.BLOCKED:
            return False, t("speaker_access.voice_blacklisted") or "Голос в чёрном списке"

        if priority == VoicePriority.SELF:
            return False, t("speaker_access.self_echo") or "Это Kiwi (эхо)"

        return True, t("speaker_access.allowed") or "Разрешено"
    
    def get_profile_info(self) -> Dict:
        """Return profile information."""
        return {
            pid: {
                "name": p.display_name,
                "priority": p.priority,
                "is_blocked": p.is_blocked,
                "auto_learned": p.auto_learned,
                "samples": len(p.embeddings),
                "last_seen": p.last_seen
            }
            for pid, p in self.profiles.items()
        }
    
    def who_am_i(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """Answer 'Who is speaking?'."""
        speaker_id, priority, confidence, name = self.identify_speaker_fast(audio, sample_rate)

        if speaker_id == self.OWNER_ID:
            return t("speakers.owner_response", name=self.OWNER_NAME, confidence=f"{confidence:.0%}") or f"Это ты, {self.OWNER_NAME}! ({confidence:.0%} уверенность)"
        elif speaker_id == "self":
            return t("speakers.self_response") or "Это я, Киви!"
        elif priority == VoicePriority.BLOCKED:
            return t("speakers.blocked_response") or "Это заблокированный голос"
        elif speaker_id.startswith("friend_"):
            return t("speakers.known_response", name=name, confidence=f"{confidence:.0%}") or f"Это {name} ({confidence:.0%} уверенность)"
        elif speaker_id != "unknown":
            return t("speakers.known_response", name=name, confidence=f"{confidence:.0%}") or f"Это {name} ({confidence:.0%} уверенность)"
        else:
            return t("speakers.unknown_response") or "Я не узнала этот голос"


# Testing
if __name__ == "__main__":
    print("[TEST] Speaker Manager Test")

    manager = SpeakerManager()

    print(f"[TEST] Profiles: {len(manager.profiles)}")
    print(f"[TEST] Profile info: {manager.get_profile_info()}")

    # Check OWNER protection
    print(f"[TEST] Owner blocked: {manager.is_blocked('owner')}")
    print(f"[TEST] Can execute (owner): {manager.can_execute_command('owner')}")
