#!/usr/bin/env python3
"""Generate NBA Playoffs team banter flair images."""

import sys
import os

TEAM_COLORS = {
    # Eastern Conference
    "celtics": ("#007A33", "#BA9653"),
    "nets": ("#000000", "#FFFFFF"),
    "knicks": ("#F58426", "#006BB6"),
    "76ers": ("#006BB6", "#EDBB00"),
    "raptors": ("#CE1141", "#000000"),
    "bulls": ("#CE1141", "#000000"),
    "cavaliers": ("#860038", "#BC945C"),
    "pistons": ("#C8102E", "#006BB6"),
    "pacers": ("#002D62", "#FDBB30"),
    "bucks": ("#00471B", "#EEE1C6"),
    "hawks": ("#E31837", "#C1D32F"),
    "hornets": ("#00788C", "#1B116E"),
    "heat": ("#98002C", "#F9A01B"),
    "magic": ("#0077C8", "#C4CED4"),
    "wizards": ("#002B5C", "#E31837"),
    # Western Conference
    "nuggets": ("#0E2240", "#FEC524"),
    "timberwolves": ("#C8102E", "#006BB6"),
    "thunder": ("#007AC1", "#EF3B24"),
    "trail blazers": ("#E31837", "#000000"),
    "jazz": ("#002B5C", "#00627D"),
    "warriors": ("#1B429F", "#FFC72C"),
    "clippers": ("#C8102E", "#1D1160"),
    "lakers": ("#552583", "#FDB927"),
    "suns": ("#1D1160", "#E56020"),
    "kings": ("#5A2D81", "#63727A"),
    "mavericks": ("#00538C", "#002B5E"),
    "rockets": ("#CE1141", "#000000"),
    "grizzlies": ("#121F4D", "#BFD2EA"),
    "pelicans": ("#0C2340", "#C9982A"),
    "spurs": ("#C4CED4", "#000000"),
}

WIN_MESSAGES = [
    "Got the W 🏀",
    "Nothing but net",
    "Victory tastes good",
    "Bucket secured",
    "Championship energy",
]

LOSS_MESSAGES = [
    "Tough one 🤕",
    "Back to the lab",
    "See you next season",
    "On to the next one",
]


def generate_flair(team_name, result="win", output_path=None):
    """Generate an SVG banter flair image."""
    team_key = team_name.lower().strip()
    colors = TEAM_COLORS.get(team_key, ("#1B429F", "#FEC524"))
    color1, color2 = colors

    if result == "win":
        message = WIN_MESSAGES[int(hash(team_name) % len(WIN_MESSAGES))]
        bg_color = color1
        text_color = "white"
        sub_color = "rgba(255,255,255,0.9)"
        accent_color = "#FFD700"
    else:
        message = LOSS_MESSAGES[int(hash(team_name) % len(LOSS_MESSAGES))]
        bg_color = "#1a1a1a"
        text_color = "#ff6b6b"
        sub_color = "#aaaaaa"
        accent_color = "#666666"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="400" height="200" fill="{bg_color}" rx="16"/>
  <text x="200" y="70" font-family="Arial Black, sans-serif" font-size="22" font-weight="900" fill="{text_color}" text-anchor="middle">{message}</text>
  <text x="200" y="105" font-family="Arial, sans-serif" font-size="18" fill="white" text-anchor="middle" opacity="0.95">{team_name.upper()}</text>
  <text x="200" y="140" font-family="Arial, sans-serif" font-size="13" fill="{sub_color}" text-anchor="middle">NBA Playoffs 2026</text>
  <text x="200" y="185" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.5)" text-anchor="middle">openclaw.ai</text>
</svg>"""

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg)
        return output_path

    return svg


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate-flair.py <team_name> <win|loss> [output_path]")
        sys.exit(1)

    team = sys.argv[1]
    result = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    path = generate_flair(team, result, output)
    if output:
        print(f"Generated: {path}")
    else:
        print(generate_flair(team, result))