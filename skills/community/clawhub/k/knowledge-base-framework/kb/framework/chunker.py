"""
Text Chunking for Knowledge Base
===============================

Phase 5: Sentence-level chunking with SpaCy/NLTK.
Creates smaller, more precise chunks for better retrieval.

Source: KB_Erweiterungs_Plan.md (Phase 5)
"""

import logging
from typing import Optional, List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Single text chunk with metadata."""
    text: str
    chunk_index: int  # 0-based index within document
    total_chunks: int
    char_start: int
    char_end: int
    sentence_count: int


class SentenceChunker:
    """
    Sentence-level text chunker.
    
    Splits text into sentence-based chunks with configurable:
    - max chunk size (characters)
    - overlap between chunks
    
    Falls back to simple sentence splitting if SpaCy/NLTK unavailable.
    """
    
    def __init__(
        self,
        max_chunk_size: int = 500,
        overlap: int = 50,
        language: str = "de"
    ):
        """
        Initialize SentenceChunker.
        
        Args:
            max_chunk_size: Maximum characters per chunk
            overlap: Character overlap between chunks
            language: Language code ("de", "en")
        """
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.language = language
        self._sentence_splitter = None
        self._load_sentence_splitter()
        
        logger.info(f"SentenceChunker init: max_chunk={max_chunk_size}, overlap={overlap}, lang={language}")
    
    def _load_sentence_splitter(self) -> None:
        """Load sentence splitting backend (SpaCy > NLTK > simple)."""
        # Try SpaCy first
        try:
            import spacy
            try:
                # Try to load German model
                self._nlp = spacy.load("de_core_news_sm")
            except OSError:
                try:
                    # Fallback to English
                    self._nlp = spacy.load("en_core_web_sm")
                except OSError:
                    logger.warning("SpaCy models not available, using NLTK")
                    self._nlp = None
            
            if self._nlp:
                self._sentence_splitter = self._split_sentences_spacy
                logger.info("Sentence splitter: SpaCy")
                return
        except ImportError:
            logger.warning("SpaCy not available")
        
        # Try NLTK
        try:
            import nltk
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
            try:
                nltk.data.find('tokenizers/punkt_tab')
                self._tokenizer = nltk.data.load('tokenizers/punkt_tab/german.pickle')
            except (LookupError, ValueError):
                self._tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
            
            self._sentence_splitter = self._split_sentences_nltk
            logger.info("Sentence splitter: NLTK")
            return
        except ImportError:
            logger.warning("NLTK not available")
        except Exception as e:
            logger.warning(f"NLTK sentence splitter error: {e}")
        
        # Fallback: simple regex
        self._sentence_splitter = self._split_sentences_simple
        logger.warning("Sentence splitter: Simple regex (limited)")
    
    def _split_sentences_spacy(self, text: str) -> List[str]:
        """Split text into sentences using SpaCy."""
        doc = self._nlp(text)
        return [str(sent).strip() for sent in doc.sents if str(sent).strip()]
    
    def _split_sentences_nltk(self, text: str) -> List[str]:
        """Split text into sentences using NLTK."""
        sentences = self._tokenizer.tokenize(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_sentences_simple(self, text: str) -> List[str]:
        """Simple sentence splitting using regex."""
        import re
        # Split on sentence-ending punctuation followed by space
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentence strings
        """
        if not text:
            return []
        return self._sentence_splitter(text)
    
    def chunk_text(self, text: str) -> List[Chunk]:
        """
        Split text into sentence-based chunks.
        
        Chunks are built by combining sentences until max_chunk_size is reached.
        Sentences are never split (keeps semantic coherence).
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of Chunk objects
        """
        if not text:
            return []
        
        sentences = self.split_into_sentences(text)
        if not sentences:
            # Fallback: treat entire text as single chunk
            return [Chunk(
                text=text[:self.max_chunk_size],
                chunk_index=0,
                total_chunks=1,
                char_start=0,
                char_end=len(text[:self.max_chunk_size]),
                sentence_count=1
            )]
        
        chunks: List[Chunk] = []
        current_chunk_sentences: List[str] = []
        current_chunk_size = 0
        current_char_start = 0
        pos = 0
        
        for sentence in sentences:
            sentence_len = len(sentence)
            
            # If adding this sentence exceeds max, save current chunk
            if current_chunk_size + sentence_len > self.max_chunk_size and current_chunk_sentences:
                char_end = pos
                chunk_text = " ".join(current_chunk_sentences)
                chunks.append(Chunk(
                    text=chunk_text,
                    chunk_index=len(chunks),
                    total_chunks=0,  # Will update later
                    char_start=current_char_start,
                    char_end=char_end,
                    sentence_count=len(current_chunk_sentences)
                ))
                
                # Start new chunk with overlap
                if self.overlap > 0 and len(chunks) > 0:
                    # Find overlap point
                    overlap_text = " ".join(current_chunk_sentences)
                    # Calculate where to start for overlap
                    overlap_start = max(0, len(overlap_text) - self.overlap)
                    # Find a good split point (at sentence boundary)
                    overlap_pos = overlap_text.rfind('. ', overlap_start)
                    if overlap_pos == -1:
                        overlap_pos = overlap_text.rfind('! ', overlap_start)
                    if overlap_pos == -1:
                        overlap_pos = overlap_text.rfind('? ', overlap_start)
                    if overlap_pos != -1:
                        current_char_start = current_char_start + overlap_pos + 2
                        overlap_sentences = overlap_text[overlap_pos+2:].split('. ')
                        if overlap_sentences and overlap_sentences[-1]:
                            current_chunk_sentences = [overlap_sentences[-1]]
                            current_chunk_size = len(current_chunk_sentences[0])
                        else:
                            current_chunk_sentences = []
                            current_chunk_size = 0
                    else:
                        current_chunk_sentences = []
                        current_chunk_size = 0
                else:
                    current_chunk_sentences = []
                    current_chunk_size = 0
                    current_char_start = pos
            
            # Add sentence to current chunk
            if current_chunk_sentences or sentence_len <= self.max_chunk_size:
                if current_chunk_sentences:
                    current_chunk_sentences.append(sentence)
                    current_chunk_size += sentence_len + 1  # +1 for space
                else:
                    current_chunk_sentences = [sentence]
                    current_chunk_size = sentence_len
            else:
                # Single sentence exceeds max_chunk_size
                # Truncate it
                chunks.append(Chunk(
                    text=sentence[:self.max_chunk_size],
                    chunk_index=len(chunks),
                    total_chunks=0,
                    char_start=pos,
                    char_end=pos + self.max_chunk_size,
                    sentence_count=1
                ))
            
            pos += sentence_len + 1  # +1 for the separator we removed
        
        # Don't forget the last chunk
        if current_chunk_sentences:
            chunks.append(Chunk(
                text=" ".join(current_chunk_sentences),
                chunk_index=len(chunks),
                total_chunks=0,
                char_start=current_char_start,
                char_end=pos,
                sentence_count=len(current_chunk_sentences)
            ))
        
        # Update total_chunks
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total
        
        return chunks
    
    def chunk_text_overlap(self, text: str) -> List[str]:
        """
        Simple chunking with sentence-level overlap.
        
        More aggressive overlap for better context preservation.
        
        Args:
            text: Input text
            
        Returns:
            List of chunk strings (text only)
        """
        chunks = self.chunk_text(text)
        return [c.text for c in chunks]


class SimpleChunker:
    """
    Simple fixed-size chunker (fallback without NLP).
    
    Splits text at word boundaries near target chunk size.
    """
    
    def __init__(self, max_chunk_size: int = 500, overlap: int = 50):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> List[Chunk]:
        """Split text into chunks at word boundaries."""
        if not text:
            return []
        
        words = text.split()
        chunks: List[Chunk] = []
        current_words: List[str] = []
        current_size = 0
        current_char_start = 0
        global_pos = 0
        
        for word in words:
            word_len = len(word) + 1  # +1 for space
            
            if current_size + word_len > self.max_chunk_size and current_words:
                chunk_text = " ".join(current_words)
                chunks.append(Chunk(
                    text=chunk_text,
                    chunk_index=len(chunks),
                    total_chunks=0,
                    char_start=current_char_start,
                    char_end=global_pos,
                    sentence_count=1
                ))
                
                # Overlap
                overlap_text = " ".join(current_words)
                if self.overlap > 0:
                    overlap_words = overlap_text[-self.overlap:].split()
                    # Find where these overlap words start
                    for i in range(len(current_words) - len(overlap_words) + 1):
                        if " ".join(current_words[i:i+len(overlap_words)]) == " ".join(overlap_words):
                            current_words = current_words[i:]
                            current_char_start = global_pos - len(chunk_text) + len(chunk_text) - sum(len(w)+1 for w in current_words)
                            break
                    else:
                        current_words = []
                else:
                    current_words = []
                current_size = sum(len(w) + 1 for w in current_words)
            else:
                current_words.append(word)
                current_size += word_len
            
            global_pos += word_len
        
        if current_words:
            chunks.append(Chunk(
                text=" ".join(current_words),
                chunk_index=len(chunks),
                total_chunks=0,
                char_start=current_char_start,
                char_end=global_pos,
                sentence_count=1
            ))
        
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total
        
        return chunks


def chunk_document(
    text: str,
    max_chunk_size: int = 500,
    overlap: int = 50,
    language: str = "de",
    use_nlp: bool = True
) -> List[str]:
    """
    Convenience function to chunk a document.
    
    Args:
        text: Document text
        max_chunk_size: Max characters per chunk
        overlap: Overlap between chunks
        language: Language code
        use_nlp: Use NLP-based sentence splitting
        
    Returns:
        List of chunk strings
    """
    if use_nlp:
        chunker = SentenceChunker(max_chunk_size=max_chunk_size, overlap=overlap, language=language)
    else:
        chunker = SimpleChunker(max_chunk_size=max_chunk_size, overlap=overlap)
    
    return chunker.chunk_text_overlap(text)


# =============================================================================
# Main: Quick Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Sentence Chunker - Quick Test")
    print("=" * 60)
    
    chunker = SentenceChunker(max_chunk_size=200, overlap=30)
    
    test_text = """
    Die MTHFR-Genmutation ist eine der häufigsten genetischen Varianten beim Menschen. 
    Sie betrifft das MTHFR-Gen, das für das Enzym Methylentetrahydrofolat-Reduktase kodiert. 
    Dieses Enzym ist entscheidend für den Folsäure-Stoffwechsel und die Methylierung. 
    Bei Personen mit dieser Mutation kann der Homocystein-Spiegel erhöht sein. 
    Eine Behandlung umfasst typischerweise die Supplementierung mit 5-MTHF, der aktiven Form der Folsäure. 
    Vitamin B12 und B6 werden oft als Cofaktoren empfohlen. 
    Regular exercise is also important for overall health. 
    Herzinfarkt ist eine ernste Erkrankung. 
    Die Diagnose erfolgt durch EKG und Blutuntersuchungen.
    """
    
    print(f"\n[1] Test Text ({len(test_text)} chars):")
    print(f"   {test_text[:100]}...")
    
    print(f"\n[2] Sentences ({len(chunker.split_into_sentences(test_text))}):")
    for i, sent in enumerate(chunker.split_into_sentences(test_text)):
        print(f"   {i+1}. {sent[:60]}{'...' if len(sent) > 60 else ''}")
    
    print(f"\n[3] Chunks ({chunker.max_chunk_size} char limit):")
    chunks = chunker.chunk_text(test_text)
    print(f"   Total chunks: {len(chunks)}")
    for chunk in chunks:
        print(f"\n   Chunk {chunk.chunk_index+1}/{chunk.total_chunks} ({len(chunk.text)} chars, {chunk.sentence_count} sentences):")
        print(f"   {chunk.text[:80]}{'...' if len(chunk.text) > 80 else ''}")
    
    print(f"\n[4] Simple overlap chunks:")
    simple_chunks = chunker.chunk_text_overlap(test_text)
    print(f"   {len(simple_chunks)} chunks: {[len(c) for c in simple_chunks]}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)