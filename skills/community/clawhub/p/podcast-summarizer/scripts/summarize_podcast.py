#!/usr/bin/env python3
"""
Podcast Summarizer - Summarize podcast episodes from various platforms.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import requests

def get_spotify_episode_info(url: str) -> dict:
    """Extract episode info from Spotify URL using oEmbed API."""
    # Try oEmbed first
    oembed_url = f"https://open.spotify.com/oembed?url={url}"
    try:
        resp = requests.get(oembed_url, timeout=10)
        if resp.ok:
            data = resp.json()
            return {
                "title": data.get("title", ""),
                "provider": "spotify",
                "thumbnail": data.get("thumbnail_url"),
            }
    except:
        pass
    return {"provider": "spotify", "title": "Unknown"}

def find_soundon_rss(show_name: str) -> str | None:
    """Try to find SoundOn RSS feed for a show."""
    # SoundOn RSS pattern: https://feeds.soundon.fm/podcasts/{show_id}.xml
    # We need to search for the show
    search_url = f"https://player.soundon.fm/api/search?q={show_name}&type=podcast"
    try:
        resp = requests.get(search_url, timeout=10)
        if resp.ok:
            data = resp.json()
            if data.get("podcasts"):
                podcast = data["podcasts"][0]
                podcast_id = podcast.get("id")
                if podcast_id:
                    return f"https://feeds.soundon.fm/podcasts/{podcast_id}.xml"
    except Exception as e:
        print(f"SoundOn search failed: {e}", file=sys.stderr)
    return None

def parse_rss_feed(feed_url: str) -> list[dict]:
    """Parse RSS feed and return episodes."""
    resp = requests.get(feed_url, timeout=30)
    resp.raise_for_status()
    
    root = ET.fromstring(resp.content)
    channel = root.find("channel")
    
    episodes = []
    for item in channel.findall("item"):
        title = item.findtext("title", "")
        description = item.findtext("description", "")
        
        # Find audio URL
        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else None
        
        # Try media:content as fallback
        if not audio_url:
            for child in item:
                if "content" in child.tag.lower() and child.get("url"):
                    audio_url = child.get("url")
                    break
        
        episodes.append({
            "title": title,
            "description": description,
            "audio_url": audio_url,
        })
    
    return episodes

def download_audio(url: str, output_path: str) -> bool:
    """Download audio file."""
    print(f"Downloading audio from {url[:80]}...", file=sys.stderr)
    try:
        resp = requests.get(url, timeout=300, stream=True)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)
        return False

def transcribe_audio(audio_path: str, language: str = "auto") -> str:
    """Transcribe audio using Whisper."""
    print("Transcribing audio with Whisper...", file=sys.stderr)
    
    cmd = ["whisper", audio_path, "--output_format", "txt"]
    if language != "auto":
        cmd.extend(["--language", language])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        
        # Whisper outputs to {input_name}.txt
        txt_path = audio_path.rsplit(".", 1)[0] + ".txt"
        if os.path.exists(txt_path):
            with open(txt_path) as f:
                return f.read()
        
        return result.stdout
    except subprocess.TimeoutExpired:
        print("Transcription timed out", file=sys.stderr)
        return ""
    except FileNotFoundError:
        print("Whisper not found. Install with: pip install openai-whisper", file=sys.stderr)
        return ""

def summarize_text(text: str, length: str = "medium", title: str = "") -> str:
    """Summarize text using LLM."""
    print("Generating summary...", file=sys.stderr)
    
    length_instructions = {
        "short": "Provide a brief 2-3 paragraph summary.",
        "medium": "Provide a detailed summary with key points and takeaways.",
        "long": "Provide a comprehensive summary with all major topics, examples, and insights.",
    }
    
    prompt = f"""Summarize this podcast episode transcript.

Title: {title}

{length_instructions.get(length, length_instructions['medium'])}

Format:
1. 📌 Main Topic (1 sentence)
2. 🎯 Key Points (bullet list)
3. 💡 Insights & Takeaways
4. 🗣️ Notable Quotes (if any)

Transcript:
{text[:50000]}  # Limit for context window
"""
    
    # Try Gemini first
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini failed: {e}", file=sys.stderr)
    
    # Fallback to OpenAI
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI failed: {e}", file=sys.stderr)
    
    return "Error: No API key available for summarization."

def main():
    parser = argparse.ArgumentParser(description="Summarize podcast episodes")
    parser.add_argument("url", help="Podcast episode URL (Spotify, Apple, RSS, or MP3)")
    parser.add_argument("--episode", "-e", type=int, default=1, help="Episode number from RSS (1=latest)")
    parser.add_argument("--language", "-l", default="auto", help="Language for transcription")
    parser.add_argument("--length", choices=["short", "medium", "long"], default="medium")
    parser.add_argument("--transcript-only", action="store_true", help="Output transcript only")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--show-name", help="Show name for RSS lookup")
    
    args = parser.parse_args()
    url = args.url
    
    episode_info = {"title": "", "audio_url": None, "description": ""}
    
    # Detect platform
    if "spotify.com" in url:
        print("Detected Spotify URL", file=sys.stderr)
        info = get_spotify_episode_info(url)
        episode_info["title"] = info.get("title", "")
        
        # Try to find RSS feed via SoundOn
        if args.show_name:
            rss_url = find_soundon_rss(args.show_name)
            if rss_url:
                print(f"Found RSS feed: {rss_url}", file=sys.stderr)
                episodes = parse_rss_feed(rss_url)
                if episodes:
                    ep = episodes[args.episode - 1]
                    episode_info.update(ep)
    
    elif "apple.com/podcast" in url or "podcasts.apple.com" in url:
        print("Detected Apple Podcasts URL", file=sys.stderr)
        # TODO: Implement Apple Podcasts scraping
        
    elif url.endswith(".xml") or "feed" in url.lower() or "rss" in url.lower():
        print("Detected RSS feed", file=sys.stderr)
        episodes = parse_rss_feed(url)
        if episodes:
            episode_info = episodes[args.episode - 1]
            print(f"Selected episode: {episode_info['title']}", file=sys.stderr)
    
    elif url.endswith(".mp3") or url.endswith(".m4a"):
        print("Detected direct audio URL", file=sys.stderr)
        episode_info["audio_url"] = url
        episode_info["title"] = os.path.basename(urlparse(url).path)
    
    # If no audio URL, just output description
    if not episode_info.get("audio_url"):
        print("No audio URL found. Outputting episode description.", file=sys.stderr)
        output = f"# {episode_info['title']}\n\n{episode_info.get('description', 'No description available.')}"
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
        print(output)
        return
    
    # Download and transcribe
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "episode.mp3")
        
        if download_audio(episode_info["audio_url"], audio_path):
            transcript = transcribe_audio(audio_path, args.language)
            
            if args.transcript_only:
                output = transcript
            else:
                output = summarize_text(transcript, args.length, episode_info.get("title", ""))
            
            if args.output:
                with open(args.output, "w") as f:
                    f.write(output)
            print(output)
        else:
            print("Failed to download audio", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
