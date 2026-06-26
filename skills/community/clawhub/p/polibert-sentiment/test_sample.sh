#!/bin/bash
# Test PoliBERT with sample data

cd /Users/yirongcao/.openclaw/workspace/skills/polibert-sentiment
source venv/bin/activate

# Test with sample texts
echo "Testing PoliBERT with sample political texts..."

python3 << 'EOF'
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

MODEL_NAME = "kornosk/polibertweet-political-twitter-roberta-mlm"

print("Loading PoliBERTweet model...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label={0: "SUPPORT", 1: "OPPOSE", 2: "NEUTRAL"},
        label2id={"SUPPORT": 0, "OPPOSE": 1, "NEUTRAL": 2}
    )
    
    # Test texts about J.D. Vance and 2028 election
    texts = [
        "J.D. Vance is the best choice for 2028, strong leader for America",
        "I strongly oppose J.D. Vance, terrible policies for working families", 
        "J.D. Vance has interesting ideas but unclear if he can win",
        "Can't wait to vote for J.D. Vance in the Republican primary",
        "J.D. Vance is not qualified to be president, too inexperienced",
        "Mixed feelings about Vance 2028, need to see more from him",
        "Trump should run again instead of Vance",
        "Vance represents the future of the Republican party",
    ]
    
    sentiment_pipe = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
    print("\n" + "="*60)
    print("PoliBERT Sentiment Analysis: J.D. Vance 2028")
    print("="*60)
    
    results = []
    for text in texts:
        result = sentiment_pipe(text[:512])[0]
        results.append(result)
        print(f"\nText: {text[:60]}...")
        print(f"Sentiment: {result['label']} ({result['score']*100:.1f}% confidence)")
    
    # Aggregate
    support = sum(1 for r in results if r['label'] == 'SUPPORT')
    oppose = sum(1 for r in results if r['label'] == 'OPPOSE')
    neutral = sum(1 for r in results if r['label'] == 'NEUTRAL')
    
    total = len(results)
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total analyzed: {total}")
    print(f"Support: {support/total*100:.1f}% ({support})")
    print(f"Oppose: {oppose/total*100:.1f}% ({oppose})")
    print(f"Neutral: {neutral/total*100:.1f}% ({neutral})")
    print(f"Net Sentiment: {(support-oppose)/total*100:+.1f}%")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
EOF
