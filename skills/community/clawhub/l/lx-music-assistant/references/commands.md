# LX Music CLI Commands Reference

## Installation

```bash
npm install -g lx-music-cli
```

## Global Commands

| Command | Alias | Description | Example |
|---------|-------|-------------|---------|
| `lx play` | - | Play or resume | `lx play` |
| `lx pause` | - | Pause playback | `lx pause` |
| `lx toggle` | - | Toggle play/pause | `lx toggle` |
| `lx next` | - | Next track | `lx next` |
| `lx prev` | - | Previous track | `lx prev` |
| `lx status` | - | Full player status | `lx status` |
| `lx now` | - | Current song info | `lx now` |
| `lx lyric` | - | Show lyrics | `lx lyric` |
| `lx watch` | - | Real-time status stream | `lx watch` |
| `lx volume <0-100>` | `vol` | Set volume | `lx volume 50` |
| `lx mute` | - | Mute audio | `lx mute` |
| `lx unmute` | - | Unmute audio | `lx unmute` |
| `lx search <keywords>` | - | Open search page | `lx search "周杰伦"` |
| `lx search -p <name>` | - | Search and play | `lx search -p "晴天-周杰伦"` |
| `lx songlist <source> <id>` | - | Open playlist | `lx songlist kw 3373919903` |
| `lx songlist-play <source> <id>` | - | Play playlist | `lx songlist-play kw 3373919903` |
| `lx collect` | - | Favorite song | `lx collect` |
| `lx uncollect` | - | Unfavorite song | `lx uncollect` |
| `lx dislike` | - | Dislike song | `lx dislike` |
| `lx config` | - | Show config | `lx config` |
| `lx config host <host>` | - | Set API host | `lx config host 127.0.0.1` |
| `lx config port <port>` | - | Set API port | `lx config port 23330` |

## Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help |
| `-v, --version` | Show version |

## Configuration File

Location: `~/.lx-music-cli/config.json`

```json
{
  "host": "127.0.0.1",
  "port": 23330
}
```
