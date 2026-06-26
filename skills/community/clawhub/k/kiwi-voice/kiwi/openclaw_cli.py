#!/usr/bin/env python3
"""OpenClaw CLI client for Kiwi Voice."""

import os
import re
import subprocess
import sys
import time
from typing import Optional

from kiwi.utils import kiwi_log
from kiwi.i18n import t


class OpenClawCLI:
    """Client for communicating with OpenClaw via CLI."""

    def __init__(
        self,
        openclaw_bin: str = "openclaw",
        session_id: str = "kiwi-voice",
        agent: Optional[str] = None,
        timeout: int = 120,
        model: Optional[str] = None,
        retry_max: int = 3,
        retry_delays: list = None,
    ):
        self.openclaw_bin = self._resolve_openclaw_path(openclaw_bin)
        self.session_id = session_id
        self.agent = agent
        self.timeout = timeout
        self.model = model
        self.retry_max = retry_max
        self.retry_delays = retry_delays or [0.5, 1.0, 2.0]
        self.session_key = f"agent:{self.session_id}:{self.session_id}"
        self._current_process: Optional[subprocess.Popen] = None
        self._is_processing = False
        self._check_cli()

    def _resolve_openclaw_path(self, openclaw_bin: str) -> str:
        """Returns bin as-is, relying on PATH unless an explicit file path is provided."""
        if os.path.exists(openclaw_bin):
            return openclaw_bin
        return openclaw_bin

    def _get_command(self, args: list) -> list:
        """Build a command taking platform into account."""
        if self.openclaw_bin.endswith('.mjs'):
            return ["node", self.openclaw_bin] + args
        return [self.openclaw_bin] + args

    def _check_cli(self):
        """Check openclaw CLI availability."""
        try:
            cmd = self._get_command(["--version"])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                kiwi_log("OPENCLAW", f"CLI found: {version}", level="INFO")
                if self.openclaw_bin.endswith('.mjs'):
                    kiwi_log("OPENCLAW", f"Using: node {self.openclaw_bin}", level="INFO")
            else:
                kiwi_log("OPENCLAW", f"CLI check failed: {result.stderr}", level="ERROR")
        except FileNotFoundError:
            kiwi_log("OPENCLAW", f"ERROR: '{self.openclaw_bin}' not found", level="ERROR")
            kiwi_log("OPENCLAW", "Make sure OpenClaw is installed: npm install -g openclaw", level="ERROR")
            sys.exit(1)
        except Exception as e:
            kiwi_log("OPENCLAW", f"CLI check error: {e}", level="ERROR")

    def is_processing(self) -> bool:
        """Check if processing is currently in progress."""
        return self._is_processing

    def cancel(self) -> bool:
        """Cancel the current processing."""
        if self._current_process and self._is_processing:
            kiwi_log("OPENCLAW", "Cancelling current operation...", level="INFO")
            try:
                self._current_process.terminate()
                self._current_process.wait(timeout=2)
                self._is_processing = False
                self._current_process = None
                kiwi_log("OPENCLAW", "Cancelled successfully", level="INFO")
                return True
            except Exception as e:
                kiwi_log("OPENCLAW", f"Cancel error: {e}", level="ERROR")
                try:
                    self._current_process.kill()
                except:
                    pass
                self._is_processing = False
                self._current_process = None
        return False

    def _is_rate_limit_error(self, stderr: str) -> bool:
        """Check if the error is a rate_limit error."""
        if not stderr:
            return False
        rate_limit_indicators = [
            "rate_limit",
            "rate limit",
            "cooldown",
            "all profiles unavailable",
            "Provider openrouter is in cooldown",
        ]
        stderr_lower = stderr.lower()
        return any(indicator in stderr_lower for indicator in rate_limit_indicators)

    def chat(self, message: str) -> str:
        """Send a message to an existing session via agent CLI with retry on rate_limit.

        FIX: Uses subprocess.run() instead of unreliable streaming reads.
        """
        args = [
            "agent",
            "--session-id", self.session_id,
            "--message", message,
            "--timeout", str(self.timeout),
        ]

        if self.agent:
            args.extend(["--agent", self.agent])

        cmd = self._get_command(args)

        # Retry loop with increasing delays
        for attempt in range(self.retry_max + 1):
            if attempt > 0:
                delay = self.retry_delays[min(attempt - 1, len(self.retry_delays) - 1)]
                kiwi_log("OPENCLAW", f"Retry {attempt}/{self.retry_max} after {delay}s...", level="WARNING")
                time.sleep(delay)

            kiwi_log("OPENCLAW", f"Sending to session {self.session_id}: {message[:50]}..." + (f" (attempt {attempt + 1})" if attempt > 0 else ""), level="INFO")
            self._is_processing = True

            try:
                # FIX: Use subprocess.run() instead of Popen + streaming
                # This is more reliable and guarantees reading all stdout
                start_time = time.time()
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    timeout=self.timeout + 30,
                )

                stdout = result.stdout
                stderr = result.stderr
                returncode = result.returncode
                self._is_processing = False

                if returncode == 0:
                    response = self._clean_response(stdout)

                    if response:
                        total_time = time.time() - start_time
                        kiwi_log("OPENCLAW", f"Response complete ({total_time:.2f}s): {response[:80]}...", level="INFO")
                        return response
                    else:
                        kiwi_log("OPENCLAW", "Empty response after cleaning", level="WARNING")
                        return t("cli_errors.empty_response")
                else:
                    # Check if the error is a rate_limit
                    if self._is_rate_limit_error(stderr) and attempt < self.retry_max:
                        kiwi_log("OPENCLAW", "Rate limit detected, will retry...", level="WARNING")
                        continue

                    kiwi_log("OPENCLAW", f"CLI error (code {returncode})", level="ERROR")
                    kiwi_log("OPENCLAW", f"stderr: {stderr[:200]}", level="ERROR")
                    return t("cli_errors.processing_error")

            except subprocess.TimeoutExpired:
                self._is_processing = False
                kiwi_log("OPENCLAW", "Timeout expired", level="WARNING")
                return t("cli_errors.timeout")
            except Exception as e:
                self._is_processing = False
                kiwi_log("OPENCLAW", f"Error: {e}", level="ERROR")
                return t("cli_errors.generic_error", error=str(e))

        # All attempts exhausted
        return t("cli_errors.rate_limit")

    def _clean_response(self, text: str) -> str:
        """Clean the response by removing the OpenClaw banner and extra formatting."""
        if not text:
            return ""

        lines = text.split('\n')
        cleaned_lines = []

        # Patterns for filtering the OpenClaw banner
        banner_patterns = [
            r'^🦞\s*OpenClaw',           # 🦞 OpenClaw ...
            r'^OpenClaw\s+\d',           # OpenClaw 2026.2.3...
            r'^\s*\|+\s*$',              # Spinners: |, ||, |||
            r'^\s*[o\-/\⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏]+\s*$',  # Animation spinners
            r'^\s*Your inbox.*',          # Banner text
            r'^\s*WhatsApp automation.*', # Banner text
            r'^\s*EXFOLIATE.*',           # Banner text
        ]

        for line in lines:
            line_stripped = line.strip()

            # Skip empty lines
            if not line_stripped:
                continue

            # Check banner patterns
            is_banner = False
            for pattern in banner_patterns:
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    is_banner = True
                    break

            if is_banner:
                continue

            # Look for the Kiwi response line (starts with 🥝)
            if line_stripped.startswith('🥝'):
                # Extract text after emoji and spaces
                response_text = line_stripped[1:].strip()
                if response_text:
                    cleaned_lines.append(response_text)
            else:
                cleaned_lines.append(line_stripped)

        # Join lines
        text = ' '.join(cleaned_lines).strip()

        # Remove markdown formatting
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        text = re.sub(r'#+\s*', '', text)

        # Remove extra spaces
        while '  ' in text:
            text = text.replace('  ', ' ')

        # Remove leading "Киви, " or "Киви " from the response
        text_lower = text.lower()
        if text_lower.startswith('киви, '):
            text = text[6:].strip()
            kiwi_log("CLEAN", "Removed 'Киви, ' prefix from response", level="INFO")
        elif text_lower.startswith('киви '):
            text = text[5:].strip()
            kiwi_log("CLEAN", "Removed 'Киви ' prefix from response", level="INFO")

        return text
