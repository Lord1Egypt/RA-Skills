"""Base detector interface and Match data structure."""

from dataclasses import dataclass


@dataclass
class Match:
    """A single PII match result."""
    label: str
    confidence: float
    masked_preview: str
    start: int
    end: int
    region: str = ""  # ISO country code: CN, US, AU, SG, MY, TH, ID, DE, UK, FR


class BaseDetector:
    """Base class for all PII detectors."""
    label = ""

    def detect(self, text):
        """Scan text and return list of Match objects.

        Args:
            text: Input string to scan.

        Returns:
            list[Match]: Detected PII matches.
        """
        raise NotImplementedError

    def _mask(self, value, keep_start=3, keep_end=4, mask_char="*"):
        """Mask a string, keeping only start/end characters visible.

        Args:
            value: Original string to mask.
            keep_start: Number of characters to keep at the start.
            keep_end: Number of characters to keep at the end.
            mask_char: Character used for masking.

        Returns:
            Masked string.
        """
        if len(value) <= keep_start + keep_end:
            return mask_char * len(value)
        mid_len = len(value) - keep_start - keep_end
        return value[:keep_start] + mask_char * mid_len + value[-keep_end:] if keep_end else value[:keep_start] + mask_char * mid_len
