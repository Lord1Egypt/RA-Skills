#!/usr/bin/env python3
"""
PoliBERT Sentiment Analysis Tool with Reddit Data Source
Analyzes political sentiment using PoliBERTweet model + Reddit data
"""

import argparse
import json
import sys
from typing import List, Dict, Optional, Tuple

try:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
    import torch
except ImportError:
    print("Error: Required packages not installed.", file=sys.stderr)
    print("Install: pip install transformers torch", file=sys.stderr)
    sys.exit(1)

# Try to import Reddit API
try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False
    print("Note: praw not installed. Reddit features disabled.", file=sys.stderr)
    print("Install: pip install praw", file=sys.stderr)

# Model configuration
MODEL_NAME = "kornosk/polibertweet-political-twitter-roberta-mlm"
SUPPORTED_LABELS = ["SUPPORT", "OPPOSE", "NEUTRAL"]

# Reddit configuration
REDDIT_SUBREDDITS = ["politics", "Conservative", "democrats", "Republican", "PoliticalDiscussion"]


def load_model():
    """Load PoliBERTweet model and tokenizer."""
    try:
        device = 0 if torch.cuda.is_available() else -1
        
        print("Loading PoliBERTweet model...", file=sys.stderr)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=3,
            id2label={0: "SUPPORT", 1: "OPPOSE", 2: "NEUTRAL"},
            label2id={"SUPPORT": 0, "OPPOSE": 1, "NEUTRAL": 2}
        )
        
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            device=device
        )
        
        print("✅ Model loaded", file=sys.stderr)
        return sentiment_pipeline
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        print("Note: First run will download ~500MB model from HuggingFace", file=sys.stderr)
        sys.exit(1)


def get_reddit_posts(query: str, subreddits: List[str] = None, limit: int = 100) -> List[str]:
    """Fetch Reddit posts mentioning the query."""
    if not PRAW_AVAILABLE:
        print("Error: praw not installed. Cannot fetch Reddit data.", file=sys.stderr)
        print("Install: pip install praw", file=sys.stderr)
        return []
    
    if subreddits is None:
        subreddits = REDDIT_SUBREDDITS
    
    try:
        # Read Reddit credentials from environment or config
        reddit = praw.Reddit(
            client_id=None,  # Will use read-only mode
            client_secret=None,
            user_agent="PoliticalSentimentAnalysis/1.0"
        )
        
        texts = []
        for subreddit_name in subreddits[:3]:  # Limit to 3 subreddits to avoid rate limits
            try:
                subreddit = reddit.subreddit(subreddit_name)
                # Search for posts
                for post in subreddit.search(query, limit=limit//len(subreddits)):
                    if post.selftext:
                        texts.append(post.selftext[:500])
                    if post.title:
                        texts.append(post.title)
                    # Get top comments
                    post.comments.replace_more(limit=0)
                    for comment in post.comments[:5]:
                        if hasattr(comment, 'body'):
                            texts.append(comment.body[:300])
            except Exception as e:
                print(f"Warning: Could not fetch from r/{subreddit_name}: {e}", file=sys.stderr)
                continue
        
        return texts
    except Exception as e:
        print(f"Error fetching Reddit data: {e}", file=sys.stderr)
        return []


def analyze_text(text: str, pipeline) -> Dict:
    """Analyze single text for political sentiment."""
    try:
        result = pipeline(text[:512])[0]  # Truncate to 512 tokens
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "sentiment": result["label"],
            "confidence": round(result["score"] * 100, 2)
        }
    except Exception as e:
        return {
            "text": text[:100],
            "sentiment": "ERROR",
            "confidence": 0,
            "error": str(e)
        }


def analyze_batch(texts: List[str], pipeline) -> List[Dict]:
    """Analyze multiple texts."""
    return [analyze_text(t, pipeline) for t in texts if t.strip()]


def analyze_candidate(candidate: str, sample_texts: List[str], pipeline=None) -> Dict:
    """Analyze sentiment toward a political candidate."""
    if pipeline is None:
        pipeline = load_model()
    
    results = analyze_batch(sample_texts, pipeline)
    
    # Aggregate results
    total = len(results)
    if total == 0:
        return {"error": "No valid texts provided"}
    
    support = sum(1 for r in results if r["sentiment"] == "SUPPORT")
    oppose = sum(1 for r in results if r["sentiment"] == "OPPOSE")
    neutral = sum(1 for r in results if r["sentiment"] == "NEUTRAL")
    
    avg_confidence = sum(r["confidence"] for r in results if "confidence" in r) / total
    
    return {
        "candidate": candidate,
        "total_analyzed": total,
        "sentiment_breakdown": {
            "support": {"count": support, "percentage": round(support/total*100, 1)},
            "oppose": {"count": oppose, "percentage": round(oppose/total*100, 1)},
            "neutral": {"count": neutral, "percentage": round(neutral/total*100, 1)}
        },
        "average_confidence": round(avg_confidence, 2),
        "net_sentiment": round((support - oppose) / total * 100, 1),
        "sample_results": results[:5]  # First 5 examples
    }


def main():
    parser = argparse.ArgumentParser(
        description="PoliBERT Political Sentiment Analysis (with Reddit support)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --text "J.D. Vance is the future of the Republican party"
  %(prog)s --candidate "J.D. Vance" --reddit --limit 50
  %(prog)s --candidate "Trump" --file tweets.txt
  %(prog)s --query "2028 election" --reddit --subreddits politics,Conservative
        """
    )
    
    parser.add_argument("--text", help="Single text to analyze")
    parser.add_argument("--candidate", help="Political candidate name")
    parser.add_argument("--query", help="Search query for Reddit")
    parser.add_argument("--file", help="File containing texts (one per line)")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--reddit", action="store_true", help="Fetch from Reddit")
    parser.add_argument("--subreddits", help="Comma-separated subreddit list (default: politics,Conservative,democrats)")
    parser.add_argument("--limit", type=int, default=100, help="Max posts to fetch (default: 100)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.text:
        # Single text analysis
        pipeline = load_model()
        result = analyze_text(args.text, pipeline)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Text: {result['text']}")
            print(f"Sentiment: {result['sentiment']} ({result['confidence']}% confidence)")
    
    elif args.candidate or args.query:
        # Candidate/Query sentiment analysis
        search_term = args.candidate or args.query
        texts = []
        
        # Fetch from Reddit if requested
        if args.reddit:
            if not PRAW_AVAILABLE:
                print("Error: --reddit requires 'praw' package. Install: pip install praw", file=sys.stderr)
                sys.exit(1)
            
            subreddits = args.subreddits.split(",") if args.subreddits else None
            print(f"🔍 Fetching Reddit posts for: {search_term}", file=sys.stderr)
            texts = get_reddit_posts(search_term, subreddits, args.limit)
            print(f"📥 Fetched {len(texts)} posts/comments", file=sys.stderr)
            
            if not texts:
                print("⚠️  No Reddit data found. Using sample data.", file=sys.stderr)
        
        if args.file:
            try:
                with open(args.file, 'r') as f:
                    file_texts = [line.strip() for line in f if line.strip()]
                    texts.extend(file_texts)
            except FileNotFoundError:
                print(f"Error: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
        elif args.stdin:
            stdin_texts = [line.strip() for line in sys.stdin if line.strip()]
            texts.extend(stdin_texts)
        
        # If no data source provided, use sample data
        if not texts:
            print("⚠️  No data source provided. Using sample texts for demo.", file=sys.stderr)
            texts = [
                f"{search_term} is the best choice for 2028, very strong leader",
                f"I strongly oppose {search_term}, terrible policies",
                f"{search_term} has interesting policies but uncertain future",
                f"Can't wait to vote for {search_term} in the primary",
                f"{search_term} is not qualified to be president",
                f"Mixed feelings about {search_term}, need to see more",
            ]
        
        # Analyze
        pipeline = load_model()
        result = analyze_candidate(search_term, texts, pipeline)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            source_info = "Reddit" if args.reddit else "Local"
            print(f"\n📊 Sentiment Analysis: {result['candidate']}")
            print(f"Source: {source_info} | Total analyzed: {result['total_analyzed']}")
            print(f"\nSupport: {result['sentiment_breakdown']['support']['percentage']}% ({result['sentiment_breakdown']['support']['count']})")
            print(f"Oppose: {result['sentiment_breakdown']['oppose']['percentage']}% ({result['sentiment_breakdown']['oppose']['count']})")
            print(f"Neutral: {result['sentiment_breakdown']['neutral']['percentage']}% ({result['sentiment_breakdown']['neutral']['count']})")
            print(f"\nNet Sentiment: {result['net_sentiment']:+.1f}%")
            print(f"Avg Confidence: {result['average_confidence']}%")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
