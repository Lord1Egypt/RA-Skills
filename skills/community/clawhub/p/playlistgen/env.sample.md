# PlaylistGen Environment Variables
# Copy this file to .env and fill in your values

# ── Required ────────────────────────────────────────────────────────────────

# Path to your local music directory (must be readable by the server)
MUSIC_DIR=/path/to/your/Music

# ── API Keys (at least one required) ────────────────────────────────────────

# Claude Haiku — recommended for both indexing and playlist generation
ANTHROPIC_API_KEY=

# MiniMax M2.7 — fallback
MINIMAX_API_KEY=

# ── Optional ────────────────────────────────────────────────────────────────

# SQLite database path (default: music.db in this directory)
# DB_PATH=./music.db

# Server port (default: 5678)
# PORT=5678

# Public URL returned in playlist links — set to your LAN/Tailscale IP
# so links work on other devices
# MUSIC_SERVER_URL=http://192.168.1.100:5678
