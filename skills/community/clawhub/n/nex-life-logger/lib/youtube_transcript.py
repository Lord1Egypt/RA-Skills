"""
Nex Life Logger - YouTube Transcript Fetcher
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Compatible with youtube-transcript-api v0.x (legacy) and v1.x (current).
"""
import logging
from storage import save_transcript, get_transcript

log = logging.getLogger("life-logger.youtube")


def _fetch_with_new_api(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    try:
        result = api.fetch(video_id, languages=("en", "en-US", "en-GB"))
        snippets = [snippet.text for snippet in result]
        if snippets:
            return " ".join(snippets)
    except Exception as e:
        log.debug("Direct English fetch failed for %s: %s", video_id, e)
    try:
        transcript_list = api.list(video_id)
        try:
            transcript = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
            result = api.fetch(video_id, languages=[transcript.language_code])
            snippets = [snippet.text for snippet in result]
            if snippets:
                return " ".join(snippets)
        except Exception:
            pass
        try:
            transcript = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
            result = api.fetch(video_id, languages=[transcript.language_code])
            snippets = [snippet.text for snippet in result]
            if snippets:
                return " ".join(snippets)
        except Exception:
            pass
        try:
            for t in transcript_list:
                translated = t.translate("en")
                result = translated.fetch()
                snippets = [snippet.text for snippet in result]
                if snippets:
                    return " ".join(snippets)
        except Exception:
            pass
    except Exception as e:
        log.debug("Transcript listing failed for %s: %s", video_id, e)
    return None


def _fetch_with_legacy_api(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = None
    try:
        transcript = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
    except Exception:
        try:
            transcript = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
        except Exception:
            try:
                for t in transcript_list:
                    transcript = t.translate("en")
                    break
            except Exception:
                pass
    if transcript is None:
        return None
    entries = transcript.fetch()
    return " ".join(entry.get("text", "") for entry in entries)


def _detect_api_version():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        if hasattr(api, "fetch") and hasattr(api, "list"):
            return "v1"
    except TypeError:
        pass
    return "v0"


_api_version = None


def fetch_transcript(video_id, title=""):
    global _api_version
    if not video_id:
        return None
    existing = get_transcript(video_id)
    if existing:
        log.debug("Transcript for %s already cached", video_id)
        return existing
    try:
        if _api_version is None:
            _api_version = _detect_api_version()
            log.info("youtube-transcript-api detected as %s", _api_version)
        if _api_version == "v1":
            full_text = _fetch_with_new_api(video_id)
        else:
            full_text = _fetch_with_legacy_api(video_id)
        if not full_text:
            log.warning("No transcript available for %s (title: %s)", video_id, title)
            return None
        full_text = full_text.replace("\n", " ").replace("  ", " ").strip()
        from config import MAX_TRANSCRIPT_LENGTH
        full_text = full_text[:MAX_TRANSCRIPT_LENGTH]
        if full_text:
            save_transcript(video_id, full_text, title=title)
            log.info("Transcript saved for %s (%d chars) - %s", video_id, len(full_text), title)
            return full_text
    except Exception as e:
        log.warning("Failed to fetch transcript for %s (title: %s): %s: %s", video_id, title, type(e).__name__, e)
    return None


def fetch_transcript_for_url(url, title=""):
    from urllib.parse import urlparse, parse_qs
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        if "youtube.com" in host:
            qs = parse_qs(parsed.query)
            video_id = qs.get("v", [""])[0]
        elif "youtu.be" in host:
            video_id = parsed.path.lstrip("/")
        else:
            return None
        if video_id:
            return fetch_transcript(video_id, title=title)
    except Exception as e:
        log.warning("Failed to parse YouTube URL %s: %s", url, e)
    return None
