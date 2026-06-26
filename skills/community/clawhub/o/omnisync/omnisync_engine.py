import hashlib
import logging
from typing import Any, Dict, Tuple

# Configuration
logger = logging.getLogger("OmniSyncStandard")

class OmniSyncEngine:
    """
    Standard Engine for OmniSync - Standalone SHA-256 Implementation.
    No external dependencies on Carbonio/Breaker cores.
    """
    def __init__(self, mode: str = "standard"):
        self.mode = mode
        logger.info(f"⚙️ OmniSync Engine initialized in '{mode}' mode.")

    @staticmethod
    def compute_hash(content: str) -> str:
        """Computes the SHA-256 hash for integrity validation."""
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_linear_diff(self, old: str, new: str) -> Tuple[bool, str]:
        """Calculates a high-performance linear diff between two strings."""
        if old == new:
            return False, ""
        
        # Divergence finding logic (O(N))
        min_len = min(len(old), len(new))
        idx = 0
        while idx < min_len and old[idx] == new[idx]:
            idx += 1
            
        # Delta extraction
        delta = new[idx:]
        
        # --- INTERNAL INTEGRITY GUARD ---
        # Safeguard: Detect and block destructive shell patterns to prevent accidental 
        # execution of high-risk commands through the sync feed.
        destructive_patterns = ["rm -rf", "chmod ", "wget ", "curl ", "bash -i"]
        for pattern in destructive_patterns:
            if pattern in delta:
                logger.warning(f"🚫 [OmniSync] Suspicious pattern detected: '{pattern}'")
                return True, "[OMNISYNC_SAFE: Destructive Pattern Detected]"
        
        return True, delta

    def execute_sync(self, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution loop for sync tools."""
        new_content = tool_args.get("new_content", "")
        old_content = tool_args.get("old_content", "")
        last_hash = tool_args.get("last_hash", "")
        
        current_hash = self.compute_hash(new_content)
        
        # Validation against client cursor
        if last_hash and current_hash == last_hash:
            return {
                "status": "success",
                "changed": False,
                "delta": "",
                "cursor": current_hash,
                "engine": f"omnisync_{self.mode}"
            }
            
        changed, delta = self._get_linear_diff(old_content, new_content)
        
        return {
            "status": "success",
            "changed": changed,
            "delta": delta,
            "cursor": current_hash,
            "engine": f"omnisync_{self.mode}",
            "tokens_saved": max(0, len(new_content) - len(delta))
        }

if __name__ == "__main__":
    # Internal validation test
    engine = OmniSyncEngine()
    old_st = "System status: Operational"
    new_st = "System status: Operational. Update: New security patches applied."
    result = engine.execute_sync({
        "old_content": old_st,
        "new_content": new_st,
        "last_hash": engine.compute_hash(old_st)
    })
    print(f"Sync Result: {result['delta']} (Saved {result['tokens_saved']} tokens)")
