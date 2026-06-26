#!/usr/bin/env python3
"""Segment transcripts into topical sections."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils import Segmentation, TopicSegment, get_openai_config, get_segmentation_cache_path


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Segment transcripts into topical sections"
    )
    parser.add_argument(
        '--transcript',
        type=str,
        help='Path to transcript JSON file or JSON string'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output path for segmentation JSON'
    )
    parser.add_argument(
        '--method',
        choices=['sliding', 'llm'],
        default='llm',
        help='Segmentation method: sliding (embedding-based) or llm (LLM-based)'
    )
    return parser.parse_args()


def _extract_response_text(response: Any) -> str:
    """Extract text from OpenAI response object variants."""
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text
    if hasattr(response, "choices") and response.choices:
        choice = response.choices[0]
        if hasattr(choice, "message") and getattr(choice.message, "content", None):
            return choice.message.content
    if hasattr(response, "content") and response.content:
        chunks = response.content
        first = chunks[0]
        if isinstance(first, dict):
            return first.get("text", "")
        if hasattr(first, "text"):
            return first.text
    return ""


def _parse_segment_json(response_text: str) -> Optional[List[Dict[str, Any]]]:
    """Parse JSON array from model response."""
    try:
        parsed = json.loads(response_text)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass

    match = re.search(r"\[.*\]", response_text, re.DOTALL)
    if not match:
        return None
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, list) else None


def _estimate_total_duration(transcript_data: Dict[str, Any]) -> float:
    """Estimate transcript duration using timestamps if available."""
    segments = transcript_data.get("segments") or []
    if segments:
        try:
            end_time = max(float(seg.get("end", 0.0)) for seg in segments)
            if end_time > 0:
                return end_time
        except Exception:
            pass

    text = transcript_data.get("full_text", "")
    words = max(1, len(text.split()))
    return words * 0.33  # ~180 words/minute


def _topics_from_segment_data(
    segment_data: List[Dict[str, Any]],
    total_duration: float,
) -> List[TopicSegment]:
    """Convert plain dict segment payloads to TopicSegment models."""
    if not segment_data:
        return []

    segment_duration = total_duration / len(segment_data)
    topics: List[TopicSegment] = []

    for i, seg_data in enumerate(segment_data):
        raw_density = seg_data.get("information_density", 0.5)
        try:
            density = max(0.0, min(1.0, float(raw_density)))
        except (TypeError, ValueError):
            density = 0.5

        key_entities = seg_data.get("key_entities", [])
        if not isinstance(key_entities, list):
            key_entities = []

        start_time = round(i * segment_duration, 3)
        end_time = round((i + 1) * segment_duration, 3)
        topics.append(
            TopicSegment(
                topic_id=i,
                label=str(seg_data.get("label", "Unknown topic")),
                start_time=start_time,
                end_time=end_time,
                duration_seconds=round(end_time - start_time, 3),
                key_entities=[str(item) for item in key_entities],
                summary=str(seg_data.get("summary", "")),
                information_density=density,
            )
        )

    return topics


def segment_with_llm(transcript_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Use LLM to identify topical segments."""
    transcript_text = transcript_data.get("full_text", "")
    if not transcript_text.strip():
        return None

    try:
        from openai import OpenAI
    except Exception as exc:
        print(f"Error loading OpenAI client: {exc}", file=sys.stderr)
        return None

    try:
        config = get_openai_config()
        client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
    except Exception as exc:
        print(f"Error creating OpenAI client: {exc}", file=sys.stderr)
        return None

    max_words = 10000
    text_preview = " ".join(transcript_text.split()[:max_words])
    prompt = f"""Analyze this podcast transcript and identify distinct topical segments.

For each major topic discussed, provide:
1. label (short topic title)
2. key_entities (array of strings)
3. summary (1-2 sentences)
4. information_density (number between 0 and 1)

Return strictly a JSON array and nothing else.

Transcript:
{text_preview}
"""

    model = config.get("model", "gpt-4o-mini")
    response_text = ""

    # Preferred OpenAI Python API.
    try:
        response = client.responses.create(
            model=model,
            input=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_output_tokens=2000,
        )
        response_text = _extract_response_text(response)
    except Exception:
        # Backward-compatible fallback for older client surfaces.
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000,
            )
            response_text = _extract_response_text(response)
        except Exception as exc:
            print(f"Error segmenting with LLM: {exc}", file=sys.stderr)
            return None

    segment_data = _parse_segment_json(response_text)
    if not segment_data:
        print("Error parsing LLM segment JSON", file=sys.stderr)
        return None

    total_duration = _estimate_total_duration(transcript_data)
    topics = _topics_from_segment_data(segment_data, total_duration)
    if not topics:
        return None

    return {
        "topics": topics,
        "total_topics": len(topics),
        "avg_topic_duration_seconds": total_duration / len(topics),
    }


def segment_with_sliding_window(transcript_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Use a deterministic fallback segmentation when LLM mode is unavailable."""
    try:
        transcript_text = transcript_data.get("full_text", "")
        if not transcript_text.strip():
            return None

        sentences = [
            sentence.strip()
            for sentence in re.split(r"[.!?]+", transcript_text)
            if sentence.strip()
        ]
        if not sentences:
            return None

        words = transcript_text.split()
        target_segments = min(10, max(3, len(words) // 900))
        words_per_segment = max(120, len(words) // target_segments)

        topics: List[TopicSegment] = []
        current_words = 0
        current_topic_words: List[str] = []
        topic_id = 0

        for sentence in sentences:
            words = sentence.split()
            current_words += len(words)
            current_topic_words.extend(words)

            at_end = sentence == sentences[-1]
            if current_words >= words_per_segment or at_end:
                if current_topic_words:
                    topic_text = " ".join(current_topic_words)
                    topic = TopicSegment(
                        topic_id=topic_id,
                        label=f"Topic {topic_id + 1}",
                        start_time=0.0,
                        end_time=0.0,
                        duration_seconds=0.0,
                        key_entities=[],
                        summary=topic_text[:500],
                        information_density=0.6,
                    )
                    topics.append(topic)
                    current_words = 0
                    current_topic_words = []
                    topic_id += 1

        total_duration = _estimate_total_duration(transcript_data)
        if not topics:
            return None
        segment_duration = total_duration / len(topics)
        for i, topic in enumerate(topics):
            topic.start_time = round(i * segment_duration, 3)
            topic.end_time = round((i + 1) * segment_duration, 3)
            topic.duration_seconds = round(topic.end_time - topic.start_time, 3)

        return {
            "topics": topics,
            "total_topics": len(topics),
            "avg_topic_duration_seconds": segment_duration,
        }

    except Exception as exc:
        print(f"Error segmenting with sliding window: {exc}", file=sys.stderr)
        return None


def segment_transcript(transcript_data: Dict[str, Any], method: str = "llm") -> Optional[Segmentation]:
    """Segment a transcript."""
    episode_id = transcript_data.get("episode_id", "unknown")
    full_text = transcript_data.get("full_text", "")

    if not full_text:
        print(f"No transcript text provided for episode {episode_id}", file=sys.stderr)
        return None

    # Check cache
    cache_path = get_segmentation_cache_path(episode_id)
    if cache_path.exists():
        try:
            with open(cache_path, "r") as f:
                data = json.load(f)
            return Segmentation(
                episode_id=episode_id,
                topics=[TopicSegment(**t) for t in data.get("topics", [])],
                total_topics=data.get("total_topics", 0),
                avg_topic_duration_seconds=data.get("avg_topic_duration_seconds", 0),
            )
        except Exception as exc:
            print(f"Error loading cached segmentation: {exc}", file=sys.stderr)

    # Segment
    if method == "llm":
        result = segment_with_llm(transcript_data)
        if not result:
            print("Warning: LLM segmentation failed, falling back to sliding method", file=sys.stderr)
            result = segment_with_sliding_window(transcript_data)
    else:
        result = segment_with_sliding_window(transcript_data)

    if not result:
        print(f"Segmentation failed for {episode_id}", file=sys.stderr)
        return None

    # Create segmentation object
    segmentation = Segmentation(
        episode_id=episode_id,
        topics=result["topics"],
        total_topics=result["total_topics"],
        avg_topic_duration_seconds=result["avg_topic_duration_seconds"],
    )

    # Cache result
    try:
        cache_data = {
            "episode_id": episode_id,
            "topics": [
                {
                    "topic_id": t.topic_id,
                    "label": t.label,
                    "start_time": t.start_time,
                    "end_time": t.end_time,
                    "duration_seconds": t.duration_seconds,
                    "key_entities": t.key_entities,
                    "summary": t.summary,
                    "information_density": t.information_density,
                }
                for t in segmentation.topics
            ],
            "total_topics": segmentation.total_topics,
            "avg_topic_duration_seconds": segmentation.avg_topic_duration_seconds,
        }

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)
    except Exception as exc:
        print(f"Warning: Failed to cache segmentation: {exc}", file=sys.stderr)

    return segmentation


def main():
    """Main segmentation entry point."""
    args = parse_args()
    
    # Load transcript data
    transcript_data = None
    if args.transcript:
        try:
            transcript_data = json.loads(args.transcript)
        except json.JSONDecodeError:
            try:
                with open(args.transcript, 'r') as f:
                    transcript_data = json.load(f)
            except Exception as e:
                print(f"Error loading transcript data: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        # Try reading from stdin
        try:
            transcript_data = json.load(sys.stdin)
        except Exception as e:
            print(f"Error reading transcript from stdin: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Segment
    segmentation = segment_transcript(transcript_data, args.method)
    
    if not segmentation:
        sys.exit(1)
    
    # Output JSON
    output = {
        'episode_id': segmentation.episode_id,
        'topics': [
            {
                'topic_id': t.topic_id,
                'label': t.label,
                'start_time': t.start_time,
                'end_time': t.end_time,
                'duration_seconds': t.duration_seconds,
                'key_entities': t.key_entities,
                'summary': t.summary,
                'information_density': t.information_density
            }
            for t in segmentation.topics
        ],
        'total_topics': segmentation.total_topics,
        'avg_topic_duration_seconds': segmentation.avg_topic_duration_seconds
    }
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
    else:
        print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
