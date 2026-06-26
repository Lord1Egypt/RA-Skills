#!/usr/bin/env python3
"""
lobster-novel: Style lock (inspired by my-novel-writer).
Extracts writing style profile from reference text,
injects it into writing prompts to maintain consistency.
"""
import re, json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict


@dataclass
class StyleProfile:
    """A writing style fingerprint."""
    pov: str = "third-limited"               # first / second / third-omni / third-limited
    tense: str = "past"                      # past / present
    paragraph_avg_len: int = 0               # average Chinese chars per paragraph
    sentence_avg_len: float = 0.0            # average chars per sentence
    dialog_ratio: float = 0.0                # percentage of text in dialog
    description_ratio: float = 0.0           # percentage of description vs action
    vocabulary_level: str = "neutral"        # simple / neutral / literary
    common_openings: List[str] = field(default_factory=list)
    common_endings: List[str] = field(default_factory=list)
    favored_phrases: List[str] = field(default_factory=list)
    avoided_phrases: List[str] = field(default_factory=list)
    tone_adjectives: List[str] = field(default_factory=list)
    sample_sentence: str = ""

    def to_prompt_injection(self) -> str:
        """Format as prompt injection for chapter generation."""
        parts = [
            "## Writing Style Guide\n",
            f"POV: {self.pov}",
            f"Tense: {self.tense}",
            f"Vocabulary: {self.vocabulary_level}",
        ]
        if self.paragraph_avg_len:
            parts.append(f"Target paragraph length: ~{self.paragraph_avg_len} chars")
        if self.dialog_ratio:
            parts.append(f"Dialog ratio target: ~{self.dialog_ratio:.0%}")
        if self.favored_phrases:
            parts.append(f"Use phrases like: {', '.join(self.favored_phrases[:5])}")
        if self.avoided_phrases:
            parts.append(f"Avoid: {', '.join(self.avoided_phrases[:5])}")
        if self.tone_adjectives:
            parts.append(f"Tone: {', '.join(self.tone_adjectives[:5])}")
        if self.sample_sentence:
            parts.append(f"\nReference style sample:\n> {self.sample_sentence[:120]}")
        return "\n".join(parts)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StyleProfile":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class StyleLock:
    """Extract and apply writing style profiles."""

    @staticmethod
    def extract_from_text(text: str, title: str = "") -> StyleProfile:
        """Build a style profile from sample text."""
        paras = [p for p in text.split("\n\n") if p.strip()]

        # POV detection
        pov = "third-limited"
        first_person = len(re.findall(r'\b我\b', text))
        second_person = len(re.findall(r'\b你\b', text))
        if first_person > second_person * 3 and first_person > 20:
            pov = "first"
        elif second_person > first_person * 2:
            pov = "second"

        # Paragraph length
        para_lens = [len([c for c in p if '\u4e00' <= c <= '\u9fff']) for p in paras]
        avg_para = int(sum(para_lens) / len(para_lens)) if para_lens else 0

        # Sentence length
        sentences = re.split(r'[。！？!?\n]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        avg_sent = round(sum(len(s) for s in sentences) / len(sentences), 1) if sentences else 0

        # Dialog ratio
        dialog = re.findall(r'[""「『]([^"」』]{3,})[""」』]', text)
        total_chars = len(text)
        dialog_chars = sum(len(d) for d in dialog)
        dialog_ratio = round(dialog_chars / max(total_chars, 1), 2)

        # Description vs action ratio
        desc_markers = len(re.findall(r'(是|有|像|仿佛|如同|似乎|看起来)', text))
        total_words = len(re.findall(r'[\u4e00-\u9fff]', text))
        desc_ratio = round(desc_markers / max(total_words, 1) * 10, 1)

        # Vocabulary level
        simple_words = len(re.findall(r'(的|了|在|是|有|和|就|也|都|而|但|或)', text))
        literary_patterns = len(re.findall(r'(之|其|乃|亦|尚|颇|甚|皆|均|惟|俱)', text))
        vocab_level = "simple" if literary_patterns < simple_words * 0.05 else \
                      "literary" if literary_patterns > simple_words * 0.2 else "neutral"

        # Common openings
        first_sentences = []
        for p in paras:
            s = p.strip()[:30]
            if len(s) > 5:
                first_sentences.append(s)
        common_openings = list(set(first_sentences[:3]))

        # Favored phrases (frequent 2-char patterns)
        chars = re.findall(r'[\u4e00-\u9fff]', text)
        bigrams = [''.join(chars[i:i+2]) for i in range(len(chars)-1)]
        freq = {}
        for bg in bigrams:
            if len(bg) == 2:
                freq[bg] = freq.get(bg, 0) + 1
        favored = sorted(freq.items(), key=lambda x: -x[1])
        favored_phrases = [w for w, c in favored[:8] if c > 1]

        # Tone adjectives
        tone_words = re.findall(r'(轻松|压抑|紧张|温暖|冷峻|诙谐|沉重|明快|细腻|粗犷|简约|华丽|朴实|犀利|温柔)', text)
        tone_set = list(set(tone_words))

        # Sample sentence (first complete sentence)
        sample = ""
        for s in sentences:
            if len(s) > 15:
                sample = s[:100]
                break

        return StyleProfile(
            pov=pov,
            paragraph_avg_len=avg_para,
            sentence_avg_len=avg_sent,
            dialog_ratio=dialog_ratio,
            description_ratio=desc_ratio,
            vocabulary_level=vocab_level,
            common_openings=common_openings[:3],
            favored_phrases=favored_phrases[:5],
            avoided_phrases=[],
            tone_adjectives=tone_set[:5],
            sample_sentence=sample,
        )

    @staticmethod
    def save_profile(profile: StyleProfile, path: Path):
        """Save profile to JSON."""
        path.write_text(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def load_profile(path: Path) -> Optional[StyleProfile]:
        """Load profile from JSON."""
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return StyleProfile.from_dict(data)
        except Exception:
            return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="style lock tool")
    parser.add_argument("file", help="reference text to analyze")
    parser.add_argument("--save", help="save profile to file")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    profile = StyleLock.extract_from_text(text)
    print("=== Style Profile ===")
    print(profile.to_prompt_injection())
    if args.save:
        StyleLock.save_profile(profile, Path(args.save))
        print(f"\nSaved: {args.save}")
