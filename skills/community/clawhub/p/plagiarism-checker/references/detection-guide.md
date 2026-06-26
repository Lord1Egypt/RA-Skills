# Detection Guide

## Detection Threshold Standards

| Originality | AI Probability | Risk Level | Recommendation |
|-------------|----------------|------------|----------------|
| ≥ 85% | < 20% | 🟢 Low Risk | Pass, suitable for submission |
| 60–84% | 20–50% | 🟡 Medium Risk | Recommend rewriting high-similarity paragraphs |
| 30–59% | 50–75% | 🟠 High Risk | Requires substantial rewriting or addition of original content |
| < 30% | > 75% | 🔴 Extremely High Risk | Severe plagiarism or nearly pure AI generation |

## Detection Methods

### 1. String Matching (SimHash / n-gram)
- Segment text into n-gram phrases (n=3~5)
- Compute SimHash fingerprints
- Compare against pre-built database, calculate Hamming distance

### 2. AI Generation Detection (Statistical Features)
- **Perplexity**: The difficulty level for a language model to predict the text
- **Burstiness**: Variance in sentence length; high burstiness = more human-like
- **Vocabulary Distribution**: AI tends to use high-frequency words; human vocabulary is more dispersed

### 3. Semantic Similarity (Sentence Transformers)
- Use `all-MiniLM-L6-v2` to compute sentence vectors
- Cosine similarity > 0.85 is considered highly similar

## Best Practices

1. Text must be **at least 100 words** for statistical significance
2. **Quoted portions** will be flagged; sources must be noted in the report
3. **Technical terminology** may produce false positives (universally used academic terms)
4. **Hybrid detection** is more accurate than any single method