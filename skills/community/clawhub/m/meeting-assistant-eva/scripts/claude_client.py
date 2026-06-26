#!/usr/bin/env python3
"""
Claude API client for real-time meeting analysis.

Handles:
  - Real-time screenshot (vision) + transcript analysis
  - Chat command response with conversation history
  - Final meeting summary generation
  - Medical mode: terminology, patient summary, prescription detection
"""

import base64
import json
import os
import re
from datetime import datetime
from pathlib import Path

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

SKILL_DIR = Path(__file__).resolve().parent.parent

# ─── System Prompts ───────────────────────────────────────────────────────────

_SYSTEM_GENERAL = """You are an intelligent AI meeting assistant attending a video meeting as a bot participant.

Your role:
- Monitor and understand the ongoing conversation
- Provide concise, useful insights and summaries
- Answer participants' questions via meeting chat
- Flag important action items and decisions
- Help participants stay focused and productive

Guidelines:
- Keep chat responses SHORT (2-5 sentences max) — people are in an active meeting
- Only send a chat message when it adds clear value
- Be helpful and professional
- Use the participant's language (Chinese or English) to match the meeting
"""

_SYSTEM_MEDICAL = """You are an AI medical consultation assistant attending a video meeting as a bot participant.

Your role:
- Monitor the doctor-patient conversation
- Translate medical terminology into patient-friendly language
- Flag important medication, dosage, and treatment information
- Generate patient-friendly summaries of medical advice
- Help bridge communication between doctor and patient

Strict guidelines:
- NEVER make independent medical diagnoses
- Always note: "以下解释仅供参考，请遵医嘱" (for informational purposes only)
- Flag prescription information clearly with ⚠️
- Keep chat responses concise — people are in a live consultation
- Use simple, accessible language when explaining to patients
- When medical terms are mentioned, proactively explain them in plain language
"""

# ─── Medical Term Detection Patterns ─────────────────────────────────────────

MEDICAL_PATTERNS = [
    # Diseases / conditions
    r'诊断|diagnosis|病症|症状|symptom|疾病|disease',
    # Medications
    r'药|medication|medicine|处方|prescription|剂量|dosage|用法|毫克|mg|片|capsule',
    # Procedures
    r'手术|surgery|检查|examination|化验|test|影像|imaging|CT|MRI|X光',
    # Instructions
    r'医嘱|advice|注意事项|precaution|禁忌|contraindication|副作用|side effect',
    # Follow-up
    r'复诊|follow.?up|下次|next appointment|随访',
]

_MEDICAL_RE = re.compile('|'.join(MEDICAL_PATTERNS), re.IGNORECASE)


def _has_medical_content(text: str) -> bool:
    return bool(_MEDICAL_RE.search(text))


# ─── Main Client Class ────────────────────────────────────────────────────────

class MeetingClaudeClient:
    """
    Claude API integration for meeting analysis.

    Usage:
        client = MeetingClaudeClient(config)
        result = client.analyze_meeting_state(screenshot_path, entries, mode="general")
        reply  = client.respond_to_chat("What was just prescribed?", "张医生", ...)
        md     = client.generate_final_summary(session_dir, mode="medical")
    """

    def __init__(self, config: dict):
        if not HAS_ANTHROPIC:
            raise ImportError(
                "anthropic package not installed.\n"
                "Run: pip install anthropic"
            )

        claude_cfg = config.get("claude", {})
        api_key = (
            claude_cfg.get("api_key")
            or os.environ.get("ANTHROPIC_API_KEY", "")
        )
        if not api_key:
            raise ValueError(
                "Claude API key not found.\n"
                "Set ANTHROPIC_API_KEY environment variable, or add\n"
                '  "claude": {"api_key": "sk-ant-..."}\n'
                "to config.json."
            )

        self.model = claude_cfg.get("model", "claude-sonnet-4-6")
        self.max_tokens = claude_cfg.get("max_tokens", 1024)
        self.client = anthropic.Anthropic(api_key=api_key)

        # Per-session conversation history (for chat Q&A continuity)
        self._chat_history: list[dict] = []
        self._transcript_context: list[dict] = []  # rolling window

    # ─── Image helper ─────────────────────────────────────────────────────

    def _encode_image(self, path) -> dict | None:
        """Return Anthropic image content block, or None on failure."""
        try:
            data = Path(path).read_bytes()
            b64 = base64.standard_b64encode(data).decode()
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": b64,
                },
            }
        except Exception as e:
            print(f"[Claude] Image encode failed ({path}): {e}")
            return None

    def _format_entries(self, entries: list[dict], max_entries: int = 40) -> str:
        """Format transcript entries as readable text."""
        lines = []
        for e in entries[-max_entries:]:
            speaker = e.get("speaker") or e.get("speaker_name") or "?"
            text    = e.get("text")    or e.get("content")      or ""
            ts      = e.get("timestamp", "")
            lines.append(f"[{ts}] {speaker}: {text}" if ts else f"{speaker}: {text}")
        return "\n".join(lines)

    # ─── Real-time Meeting State Analysis ─────────────────────────────────

    def analyze_meeting_state(
        self,
        screenshot_path=None,
        transcript_entries: list[dict] | None = None,
        mode: str = "general",
    ) -> dict:
        """
        Analyze current meeting state using vision + transcript.

        Returns:
            {
              "analysis": str,       # internal analysis text
              "chat_message": str | None,  # message to send to meeting chat (if any)
              "has_medical_content": bool,
              "timestamp": str,
            }
        """
        system = _SYSTEM_MEDICAL if mode == "medical" else _SYSTEM_GENERAL
        content = []

        # Add screenshot
        if screenshot_path and Path(str(screenshot_path)).exists():
            img_block = self._encode_image(screenshot_path)
            if img_block:
                content.append(img_block)

        # Build transcript text
        entries = transcript_entries or []
        # Update rolling context
        self._transcript_context.extend(entries)
        self._transcript_context = self._transcript_context[-100:]

        transcript_text = self._format_entries(entries) if entries else "(no new transcript)"

        # Build analysis prompt
        if mode == "medical":
            prompt = f"""Current meeting transcript (latest updates):
{transcript_text}

Please analyze and:
1. Identify any medical terms, medications, diagnoses, or instructions mentioned
2. Flag any prescription/dosage information with ⚠️
3. If there is meaningful medical content worth sharing with participants, write a brief chat message

Format your response as:
ANALYSIS:
<your internal analysis>

CHAT:
<message to send to meeting chat — leave blank if nothing useful to share>
"""
        else:
            prompt = f"""Current meeting transcript (latest updates):
{transcript_text}

Please analyze and:
1. What is currently being discussed?
2. Are there any action items, decisions, or important points?
3. Is there anything worth sharing in the meeting chat?

Format your response as:
ANALYSIS:
<your internal analysis>

CHAT:
<message to send to meeting chat — leave blank if nothing useful to share>
"""

        content.append({"type": "text", "text": prompt})

        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system,
                messages=[{"role": "user", "content": content}],
            )
            full_text = resp.content[0].text
        except Exception as e:
            print(f"[Claude] analyze_meeting_state error: {e}")
            return {
                "analysis": f"Analysis failed: {e}",
                "chat_message": None,
                "has_medical_content": False,
                "timestamp": datetime.now().isoformat(),
            }

        # Parse ANALYSIS / CHAT sections
        analysis = ""
        chat_msg = None

        if "ANALYSIS:" in full_text and "CHAT:" in full_text:
            parts = full_text.split("CHAT:", 1)
            analysis = parts[0].replace("ANALYSIS:", "").strip()
            chat_part = parts[1].strip()
            # Only use chat message if it has content
            if chat_part and len(chat_part) > 5:
                chat_msg = chat_part
        else:
            analysis = full_text

        # Suppress empty/placeholder chat messages
        if chat_msg and chat_msg.lower() in ("", "none", "n/a", "-", "无"):
            chat_msg = None

        has_medical = _has_medical_content(transcript_text)

        return {
            "analysis": analysis,
            "chat_message": chat_msg,
            "has_medical_content": has_medical,
            "timestamp": datetime.now().isoformat(),
        }

    # ─── Chat Command Response ─────────────────────────────────────────────

    def respond_to_chat(
        self,
        user_message: str,
        sender: str,
        context_screenshot=None,
        mode: str = "general",
    ) -> str:
        """
        Generate a reply to a participant's chat message.
        Maintains conversation history for context continuity.

        Returns:
            str: Reply message to send to meeting chat.
        """
        system = _SYSTEM_MEDICAL if mode == "medical" else _SYSTEM_GENERAL
        system += f"\n\nThe participant '{sender}' is asking you a question in the meeting chat. Respond helpfully and concisely."

        content = []

        # Include screenshot context if available
        if context_screenshot and Path(str(context_screenshot)).exists():
            img_block = self._encode_image(context_screenshot)
            if img_block:
                content.append(img_block)

        # Include recent meeting context
        context_text = ""
        if self._transcript_context:
            context_text = "Recent meeting conversation:\n" + self._format_entries(
                self._transcript_context, max_entries=20
            ) + "\n\n"

        prompt = f"{context_text}{sender} asks: {user_message}\n\nReply concisely (this is a meeting chat, keep it under 100 words)."
        content.append({"type": "text", "text": prompt})

        # Add to history and send
        self._chat_history.append({"role": "user", "content": content})

        # Keep history to last 10 turns
        history = self._chat_history[-10:]

        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=system,
                messages=history,
            )
            reply = resp.content[0].text.strip()
            # Save assistant reply as plain text in history
            self._chat_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            print(f"[Claude] respond_to_chat error: {e}")
            return f"抱歉，我暂时无法回应。({e})"

    # ─── Final Meeting Summary ─────────────────────────────────────────────

    def generate_final_summary(
        self,
        session_dir,
        mode: str = "general",
    ) -> str:
        """
        Generate a comprehensive meeting summary from session data.

        Reads: transcript_log.json, suggestions_log.json, screenshots/
        Returns: Markdown string (also saves to session_dir/meeting_summary.md)
        """
        session_dir = Path(session_dir)
        system = _SYSTEM_MEDICAL if mode == "medical" else _SYSTEM_GENERAL

        # ── Collect transcript ──
        transcript_text = "(no transcript available)"
        transcript_log = session_dir / "transcript_log.json"
        if transcript_log.exists():
            try:
                entries = json.loads(transcript_log.read_text(encoding="utf-8"))
                transcript_text = self._format_entries(entries, max_entries=500)
            except Exception:
                pass

        # ── Collect suggestions log ──
        suggestions_text = ""
        suggestions_log = session_dir / "suggestions_log.json"
        if suggestions_log.exists():
            try:
                suggestions = json.loads(suggestions_log.read_text(encoding="utf-8"))
                if suggestions:
                    lines = []
                    for s in suggestions:
                        ts = s.get("timestamp", "")
                        msg = s.get("message", "")
                        lines.append(f"[{ts}] {msg}")
                    suggestions_text = "\n".join(lines)
            except Exception:
                pass

        # ── Collect session metadata ──
        meta = {}
        meta_path = session_dir / "session.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        # ── Include a few screenshots for visual context ──
        content = []
        screenshots_dir = session_dir / "screenshots"
        if screenshots_dir.exists():
            shots = sorted(screenshots_dir.glob("*.png"))
            # Sample: first, middle, last (max 4 images to stay within token limits)
            indices = list({0, len(shots)//2, len(shots)-1}) if shots else []
            for i in sorted(set(indices)):
                if 0 <= i < len(shots):
                    img_block = self._encode_image(shots[i])
                    if img_block:
                        content.append(img_block)

        # ── Build prompt ──
        start_time = meta.get("start_time", "N/A")
        end_time   = meta.get("end_time",   "N/A")
        platform   = meta.get("platform",   "N/A")

        base_prompt = f"""Generate a comprehensive meeting summary in Markdown format.

Meeting metadata:
- Start: {start_time}
- End:   {end_time}
- Platform: {platform}
- Mode: {mode}

Full meeting transcript:
{transcript_text}
"""
        if suggestions_text:
            base_prompt += f"\nAI suggestions sent during meeting:\n{suggestions_text}\n"

        if mode == "medical":
            base_prompt += """
Please write meeting_summary.md with the following sections:

# 医疗会议摘要

## 会议基本信息
## 参与人员
## 主要讨论内容

## 医疗信息
### 症状与诊断
### 处方与用药
### 医嘱与注意事项
### 复诊安排

## 患者版简明摘要
（用通俗语言，不使用专业术语，适合患者直接阅读）

## 医学术语对照
| 专业术语 | 通俗解释 | 英文 |
|---------|---------|------|

## 待办事项
"""
        else:
            base_prompt += """
Please write meeting_summary.md with the following sections:

# 会议摘要

## 会议基本信息
## 参与人员
## 主要议题
## 关键讨论内容
## 达成的决定
## 待办事项
## 下次会议
"""

        content.append({"type": "text", "text": base_prompt})

        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system,
                messages=[{"role": "user", "content": content}],
            )
            summary_md = resp.content[0].text.strip()
        except Exception as e:
            print(f"[Claude] generate_final_summary error: {e}")
            summary_md = f"# 会议摘要生成失败\n\n错误: {e}\n"

        # Save to file
        out_path = session_dir / "meeting_summary.md"
        out_path.write_text(summary_md, encoding="utf-8")
        print(f"[Claude] Summary saved: {out_path}")

        return summary_md

    def reset_conversation(self):
        """Clear conversation history (call between meetings)."""
        self._chat_history.clear()
        self._transcript_context.clear()
